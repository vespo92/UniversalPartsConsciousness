"""
ORACLE Compatibility Cache
Multi-tier caching for sub-10ms query performance.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
from collections import OrderedDict
import asyncio
import json
import hashlib


@dataclass
class CacheEntry:
    """A cached compatibility result."""
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)


class LRUCache:
    """
    Thread-safe LRU cache for in-memory caching.

    L1 cache with < 1ms access time.
    """

    def __init__(self, maxsize: int = 100000):
        self.maxsize = maxsize
        self._cache: OrderedDict = OrderedDict()
        self._lock = asyncio.Lock()
        self._stats = {"hits": 0, "misses": 0}

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]

                # Check expiry
                if datetime.now() > entry.expires_at:
                    del self._cache[key]
                    self._stats["misses"] += 1
                    return None

                # Move to end (most recently used)
                self._cache.move_to_end(key)
                entry.access_count += 1
                entry.last_accessed = datetime.now()
                self._stats["hits"] += 1
                return entry.value

            self._stats["misses"] += 1
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ):
        """Set value in cache with TTL in seconds."""
        async with self._lock:
            now = datetime.now()
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=now,
                expires_at=now + timedelta(seconds=ttl)
            )

            # If key exists, update it
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key] = entry
            else:
                # Evict oldest if at capacity
                while len(self._cache) >= self.maxsize:
                    self._cache.popitem(last=False)

                self._cache[key] = entry

    async def delete(self, key: str):
        """Delete a key from cache."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def clear(self):
        """Clear all cached data."""
        async with self._lock:
            self._cache.clear()

    def stats(self) -> Dict:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0

        return {
            "size": len(self._cache),
            "max_size": self.maxsize,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": hit_rate,
        }


class CompatibilityMatrix:
    """
    Pre-computed compatibility matrix.

    L3 cache for common part pairings, updated nightly.
    Access time < 10ms.
    """

    def __init__(self):
        self._matrix: Dict[str, Dict[str, Any]] = {}
        self._last_updated: Optional[datetime] = None
        self._stats = {"hits": 0, "misses": 0}

    async def get(
        self,
        part_a_id: str,
        part_b_id: str
    ) -> Optional[Any]:
        """Get pre-computed compatibility."""
        # Normalize key order (smaller id first)
        if part_a_id > part_b_id:
            part_a_id, part_b_id = part_b_id, part_a_id

        if part_a_id in self._matrix:
            if part_b_id in self._matrix[part_a_id]:
                self._stats["hits"] += 1
                return self._matrix[part_a_id][part_b_id]

        self._stats["misses"] += 1
        return None

    async def set(
        self,
        part_a_id: str,
        part_b_id: str,
        result: Any
    ):
        """Set pre-computed compatibility."""
        if part_a_id > part_b_id:
            part_a_id, part_b_id = part_b_id, part_a_id

        if part_a_id not in self._matrix:
            self._matrix[part_a_id] = {}

        self._matrix[part_a_id][part_b_id] = result

    async def load_from_file(self, filepath: str):
        """Load pre-computed matrix from file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self._matrix = data.get("matrix", {})
                self._last_updated = datetime.fromisoformat(data.get("updated_at", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            self._matrix = {}

    async def save_to_file(self, filepath: str):
        """Save pre-computed matrix to file."""
        data = {
            "matrix": self._matrix,
            "updated_at": datetime.now().isoformat(),
            "entry_count": sum(len(v) for v in self._matrix.values())
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)

    def stats(self) -> Dict:
        """Get matrix statistics."""
        entry_count = sum(len(v) for v in self._matrix.values())
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0

        return {
            "part_count": len(self._matrix),
            "entry_count": entry_count,
            "last_updated": self._last_updated.isoformat() if self._last_updated else None,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": hit_rate,
        }


class CompatibilityCache:
    """
    Multi-tier caching for compatibility queries.

    Tiers:
    - L1: In-memory LRU cache (100K entries, <1ms)
    - L2: Redis shared cache (3600s TTL, <5ms) - optional
    - L3: Pre-computed compatibility matrix (updated nightly, <10ms)
    """

    def __init__(
        self,
        l1_size: int = 100000,
        l2_client=None,  # Redis client
        l3_matrix_path: Optional[str] = None
    ):
        # L1: In-memory LRU
        self.l1_cache = LRUCache(maxsize=l1_size)

        # L2: Redis (optional)
        self.l2_client = l2_client
        self.l2_ttl = 3600  # 1 hour

        # L3: Pre-computed matrix
        self.l3_matrix = CompatibilityMatrix()
        self.l3_path = l3_matrix_path

        self._initialized = False

    async def initialize(self):
        """Initialize cache layers."""
        if self._initialized:
            return

        # Load L3 matrix if path provided
        if self.l3_path:
            await self.l3_matrix.load_from_file(self.l3_path)

        self._initialized = True

    async def get(
        self,
        key: str,
        check_l3: bool = True
    ) -> Optional[Any]:
        """
        Get value from cache, checking all tiers.

        Args:
            key: Cache key
            check_l3: Whether to check L3 matrix

        Returns:
            Cached value or None
        """
        # L1 check (< 1ms)
        result = await self.l1_cache.get(key)
        if result is not None:
            return result

        # L2 check (< 5ms) if Redis available
        if self.l2_client:
            try:
                data = await self._l2_get(key)
                if data is not None:
                    # Promote to L1
                    await self.l1_cache.set(key, data)
                    return data
            except Exception:
                pass  # L2 failure is non-fatal

        # L3 check (< 10ms) for compatibility pairs
        if check_l3 and key.startswith("compat:"):
            parts = key.split(":")
            if len(parts) == 3:
                result = await self.l3_matrix.get(parts[1], parts[2])
                if result is not None:
                    # Promote to L1 and L2
                    await self.l1_cache.set(key, result)
                    if self.l2_client:
                        await self._l2_set(key, result)
                    return result

        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ):
        """
        Set value in cache (L1 and L2).

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        # Set in L1
        await self.l1_cache.set(key, value, ttl)

        # Set in L2 if available
        if self.l2_client:
            try:
                await self._l2_set(key, value, ttl)
            except Exception:
                pass  # L2 failure is non-fatal

    async def invalidate(self, key: str):
        """Invalidate a cache entry across all tiers."""
        await self.l1_cache.delete(key)

        if self.l2_client:
            try:
                await self._l2_delete(key)
            except Exception:
                pass

    async def invalidate_part(self, part_id: str):
        """
        Invalidate all cache entries involving a part.

        Called when part data is updated.
        """
        # This would need to track all keys by part
        # For now, clear L1 cache
        await self.l1_cache.clear()

    async def warmup(self, part_pairs: List[tuple]):
        """
        Pre-warm cache with common part pairs.

        Called during system startup.
        """
        for part_a, part_b in part_pairs:
            key = f"compat:{part_a}:{part_b}"
            # Check if in L3, promote to L1
            result = await self.l3_matrix.get(part_a, part_b)
            if result:
                await self.l1_cache.set(key, result)

    def stats(self) -> Dict:
        """Get comprehensive cache statistics."""
        l1_stats = self.l1_cache.stats()
        l3_stats = self.l3_matrix.stats()

        total_hits = l1_stats["hits"] + l3_stats["hits"]
        total_misses = l1_stats["misses"] + l3_stats["misses"]
        total = total_hits + total_misses
        overall_hit_rate = total_hits / total if total > 0 else 0

        return {
            "l1": l1_stats,
            "l3": l3_stats,
            "overall": {
                "total_hits": total_hits,
                "total_misses": total_misses,
                "hit_rate": overall_hit_rate,
            }
        }

    async def _l2_get(self, key: str) -> Optional[Any]:
        """Get from L2 (Redis)."""
        if not self.l2_client:
            return None

        # Would use actual Redis client
        # data = await self.l2_client.get(key)
        # return json.loads(data) if data else None
        return None

    async def _l2_set(self, key: str, value: Any, ttl: int = 3600):
        """Set in L2 (Redis)."""
        if not self.l2_client:
            return

        # Would use actual Redis client
        # await self.l2_client.setex(key, ttl, json.dumps(value))

    async def _l2_delete(self, key: str):
        """Delete from L2 (Redis)."""
        if not self.l2_client:
            return

        # Would use actual Redis client
        # await self.l2_client.delete(key)


def make_cache_key(*args) -> str:
    """
    Generate a cache key from arguments.

    Uses MD5 hash for consistent, compact keys.
    """
    key_str = ":".join(str(a) for a in args)
    return hashlib.md5(key_str.encode()).hexdigest()
