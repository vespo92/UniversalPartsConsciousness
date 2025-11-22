"""
ORACLE Batch Compatibility Checker
High-throughput batch processing for compatibility checks.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import asyncio
import time


@dataclass
class BatchRequest:
    """A batch of compatibility checks."""
    batch_id: str
    pairs: List[Tuple[str, str]]  # List of (part_a_id, part_b_id) tuples
    context: Optional[Dict] = None
    priority: int = 5


@dataclass
class BatchResult:
    """Result of a batch compatibility check."""
    batch_id: str
    total_pairs: int
    compatible_count: int
    incompatible_count: int
    error_count: int

    results: List[Dict]
    total_time_ms: float
    avg_time_per_pair_ms: float

    errors: List[str] = field(default_factory=list)


class BatchCompatibilityChecker:
    """
    High-throughput batch compatibility checker.

    Target: 100 pairs in < 500ms (< 1000ms max)

    Features:
    - Parallel processing
    - Batch caching
    - Progress tracking
    - Error handling
    """

    def __init__(
        self,
        api=None,
        cache=None,
        max_concurrent: int = 20,
        chunk_size: int = 50
    ):
        """
        Initialize batch checker.

        Args:
            api: CompatibilityAPI instance
            cache: CompatibilityCache instance
            max_concurrent: Maximum concurrent checks
            chunk_size: Size of processing chunks
        """
        self.api = api
        self.cache = cache
        self.max_concurrent = max_concurrent
        self.chunk_size = chunk_size

        # Semaphore for concurrency control
        self._semaphore = asyncio.Semaphore(max_concurrent)

        # Progress tracking
        self._current_batch = None
        self._progress = 0

    async def check_batch(
        self,
        batch: BatchRequest,
        progress_callback=None
    ) -> BatchResult:
        """
        Process a batch of compatibility checks.

        Args:
            batch: BatchRequest with pairs to check
            progress_callback: Optional callback for progress updates

        Returns:
            BatchResult with all results
        """
        start_time = time.perf_counter()

        self._current_batch = batch.batch_id
        self._progress = 0

        results = []
        errors = []
        compatible_count = 0
        incompatible_count = 0
        error_count = 0

        total_pairs = len(batch.pairs)

        # Check cache for batch
        cached_results, uncached_pairs = await self._check_batch_cache(batch.pairs)

        # Add cached results
        for pair, result in cached_results.items():
            results.append({
                "part_a": pair[0],
                "part_b": pair[1],
                "cached": True,
                **result
            })
            if result.get("is_compatible"):
                compatible_count += 1
            else:
                incompatible_count += 1

        # Process uncached pairs in chunks
        chunks = self._chunk_pairs(uncached_pairs, self.chunk_size)

        for chunk_idx, chunk in enumerate(chunks):
            chunk_results = await self._process_chunk(chunk, batch.context)

            for pair, result in chunk_results:
                if "error" in result:
                    error_count += 1
                    errors.append(f"Pair {pair}: {result['error']}")
                else:
                    results.append({
                        "part_a": pair[0],
                        "part_b": pair[1],
                        "cached": False,
                        **result
                    })
                    if result.get("is_compatible"):
                        compatible_count += 1
                    else:
                        incompatible_count += 1

                    # Cache result
                    if self.cache:
                        await self._cache_result(pair, result)

            # Update progress
            processed = len(cached_results) + (chunk_idx + 1) * self.chunk_size
            self._progress = min(processed / total_pairs * 100, 100)

            if progress_callback:
                await progress_callback(self._progress, processed, total_pairs)

        total_time = (time.perf_counter() - start_time) * 1000
        avg_time = total_time / total_pairs if total_pairs > 0 else 0

        self._current_batch = None

        return BatchResult(
            batch_id=batch.batch_id,
            total_pairs=total_pairs,
            compatible_count=compatible_count,
            incompatible_count=incompatible_count,
            error_count=error_count,
            results=results,
            total_time_ms=total_time,
            avg_time_per_pair_ms=avg_time,
            errors=errors
        )

    async def check_matrix(
        self,
        part_ids: List[str],
        symmetric: bool = True
    ) -> Dict[Tuple[str, str], Dict]:
        """
        Check compatibility matrix for all pairs of parts.

        Args:
            part_ids: List of part IDs to check
            symmetric: If True, only check upper triangle (A,B same as B,A)

        Returns:
            Dict mapping (part_a, part_b) to result
        """
        pairs = []
        n = len(part_ids)

        for i in range(n):
            for j in range(i + 1 if symmetric else 0, n):
                if i != j:
                    pairs.append((part_ids[i], part_ids[j]))

        batch = BatchRequest(
            batch_id=f"matrix_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            pairs=pairs
        )

        result = await self.check_batch(batch)

        # Convert to matrix format
        matrix = {}
        for r in result.results:
            key = (r["part_a"], r["part_b"])
            matrix[key] = {
                "is_compatible": r.get("is_compatible"),
                "confidence": r.get("confidence"),
                "compatibility_type": r.get("compatibility_type"),
            }

            # Add symmetric entry if needed
            if symmetric:
                matrix[(r["part_b"], r["part_a"])] = matrix[key]

        return matrix

    async def find_compatible_group(
        self,
        part_ids: List[str],
        require_all: bool = False
    ) -> Dict:
        """
        Find which parts are compatible with each other.

        Args:
            part_ids: List of part IDs to analyze
            require_all: If True, only return parts compatible with ALL others

        Returns:
            Dict with compatibility groups and statistics
        """
        matrix = await self.check_matrix(part_ids)

        # Build adjacency list
        compatible_with = {pid: set() for pid in part_ids}

        for (a, b), result in matrix.items():
            if result.get("is_compatible"):
                compatible_with[a].add(b)
                compatible_with[b].add(a)

        # Find fully compatible parts (compatible with all others)
        n = len(part_ids)
        fully_compatible = [
            pid for pid in part_ids
            if len(compatible_with[pid]) == n - 1
        ]

        # Find compatibility groups (connected components)
        groups = self._find_groups(part_ids, compatible_with)

        # Calculate statistics
        total_pairs = len(matrix) // 2  # Symmetric
        compatible_pairs = sum(1 for r in matrix.values() if r.get("is_compatible")) // 2

        return {
            "total_parts": n,
            "fully_compatible": fully_compatible,
            "compatibility_groups": groups,
            "total_pairs": total_pairs,
            "compatible_pairs": compatible_pairs,
            "compatibility_rate": compatible_pairs / total_pairs if total_pairs > 0 else 0,
            "compatible_with": {k: list(v) for k, v in compatible_with.items()},
        }

    async def _check_batch_cache(
        self,
        pairs: List[Tuple[str, str]]
    ) -> Tuple[Dict, List[Tuple[str, str]]]:
        """Check cache for batch of pairs."""
        if not self.cache:
            return {}, pairs

        cached = {}
        uncached = []

        for pair in pairs:
            cache_key = f"compat:{pair[0]}:{pair[1]}"
            result = await self.cache.get(cache_key)

            if result:
                cached[pair] = result
            else:
                uncached.append(pair)

        return cached, uncached

    async def _process_chunk(
        self,
        pairs: List[Tuple[str, str]],
        context: Optional[Dict]
    ) -> List[Tuple[Tuple[str, str], Dict]]:
        """Process a chunk of pairs concurrently."""
        tasks = []

        for pair in pairs:
            task = self._check_single_with_semaphore(pair, context)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return list(zip(pairs, results))

    async def _check_single_with_semaphore(
        self,
        pair: Tuple[str, str],
        context: Optional[Dict]
    ) -> Dict:
        """Check single pair with concurrency control."""
        async with self._semaphore:
            return await self._check_single(pair, context)

    async def _check_single(
        self,
        pair: Tuple[str, str],
        context: Optional[Dict]
    ) -> Dict:
        """Check a single pair."""
        if self.api:
            from .compatibility_api import APIRequest
            import uuid

            request = APIRequest(
                request_id=str(uuid.uuid4()),
                action="check_compatibility",
                payload={
                    "part_a": {"id": pair[0]},
                    "part_b": {"id": pair[1]},
                    "context": context or {}
                }
            )

            response = await self.api.handle_request(request)

            if response.success:
                return response.data
            else:
                return {"error": response.error}
        else:
            # Simplified check without API
            return {
                "is_compatible": True,
                "confidence": 0.5,
                "compatibility_type": "UNKNOWN"
            }

    async def _cache_result(
        self,
        pair: Tuple[str, str],
        result: Dict
    ):
        """Cache a result."""
        if self.cache:
            cache_key = f"compat:{pair[0]}:{pair[1]}"
            await self.cache.set(cache_key, result, ttl=3600)

    def _chunk_pairs(
        self,
        pairs: List[Tuple[str, str]],
        chunk_size: int
    ) -> List[List[Tuple[str, str]]]:
        """Split pairs into chunks."""
        return [
            pairs[i:i + chunk_size]
            for i in range(0, len(pairs), chunk_size)
        ]

    def _find_groups(
        self,
        part_ids: List[str],
        compatible_with: Dict[str, set]
    ) -> List[List[str]]:
        """Find connected components (compatibility groups)."""
        visited = set()
        groups = []

        def dfs(pid, group):
            visited.add(pid)
            group.append(pid)
            for neighbor in compatible_with[pid]:
                if neighbor not in visited:
                    dfs(neighbor, group)

        for pid in part_ids:
            if pid not in visited:
                group = []
                dfs(pid, group)
                groups.append(group)

        return groups

    def get_progress(self) -> Dict:
        """Get current batch progress."""
        return {
            "batch_id": self._current_batch,
            "progress_percent": self._progress,
            "is_running": self._current_batch is not None,
        }
