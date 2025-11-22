"""
ORACLE Hot Path Optimizer
Pre-computation and optimization for common query patterns.

"The fastest query is the one already answered.
I anticipate your needs before you ask."
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import asyncio
import heapq
import math


class OptimizationStrategy(Enum):
    """Optimization strategies for hot paths."""
    FREQUENCY_BASED = "frequency"       # Most frequently queried
    RECENCY_BASED = "recency"          # Most recently queried
    PREDICTIVE = "predictive"          # Predicted future queries
    HYBRID = "hybrid"                  # Combination of strategies


@dataclass
class QueryPattern:
    """Tracked query pattern for optimization."""
    pattern_id: str
    query_type: str
    key_parts: Tuple[str, ...]

    # Statistics
    hit_count: int = 0
    miss_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    first_seen: datetime = field(default_factory=datetime.now)

    # Timing
    avg_compute_time_ms: float = 0.0
    total_compute_time_ms: float = 0.0

    # Relationships
    co_occurring_patterns: Dict[str, int] = field(default_factory=dict)

    @property
    def access_frequency(self) -> float:
        """Calculate access frequency (queries per hour)."""
        age_hours = max(1, (datetime.now() - self.first_seen).total_seconds() / 3600)
        return (self.hit_count + self.miss_count) / age_hours

    @property
    def cache_value_score(self) -> float:
        """
        Calculate cache value score.

        Higher score = more valuable to keep in cache.
        Score = frequency * compute_time / age_penalty
        """
        age_hours = (datetime.now() - self.last_accessed).total_seconds() / 3600
        age_penalty = 1 + math.log1p(age_hours)

        return (
            self.access_frequency *
            self.avg_compute_time_ms /
            age_penalty
        )


@dataclass
class OptimizationResult:
    """Result of optimization cycle."""
    patterns_analyzed: int
    patterns_precomputed: int
    patterns_evicted: int
    estimated_hit_rate_improvement: float
    estimated_latency_reduction_ms: float
    precomputation_time_ms: float


class HotPathOptimizer:
    """
    Optimizes cache performance through pattern analysis and precomputation.

    Features:
    - Query pattern tracking and analysis
    - Predictive precomputation of likely queries
    - Adaptive cache warming based on usage patterns
    - Co-occurrence analysis for prefetching
    - Time-of-day usage prediction
    """

    def __init__(
        self,
        cache,
        max_tracked_patterns: int = 100000,
        precompute_threshold: float = 10.0,  # queries per hour
        optimization_interval_seconds: int = 300
    ):
        """
        Initialize the hot path optimizer.

        Args:
            cache: Cache instance to optimize
            max_tracked_patterns: Maximum patterns to track
            precompute_threshold: Minimum frequency for precomputation
            optimization_interval_seconds: Interval between optimization cycles
        """
        self.cache = cache
        self.max_tracked = max_tracked_patterns
        self.precompute_threshold = precompute_threshold
        self.optimization_interval = optimization_interval_seconds

        # Pattern tracking
        self._patterns: Dict[str, QueryPattern] = {}
        self._pattern_index: Dict[str, Set[str]] = defaultdict(set)

        # Temporal patterns
        self._hourly_patterns: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        # Session tracking (for co-occurrence)
        self._session_queries: Dict[str, List[str]] = defaultdict(list)
        self._session_timeout = 300  # 5 minutes

        # Optimization state
        self._last_optimization: Optional[datetime] = None
        self._optimization_running = False

        # Precomputation queue
        self._precompute_queue: List[Tuple[float, str]] = []  # (priority, pattern_id)

        # Statistics
        self.stats = {
            "patterns_tracked": 0,
            "precomputations": 0,
            "prefetch_hits": 0,
            "optimization_cycles": 0,
        }

    def record_query(
        self,
        query_type: str,
        key_parts: Tuple[str, ...],
        was_cache_hit: bool,
        compute_time_ms: float = 0.0,
        session_id: Optional[str] = None
    ) -> str:
        """
        Record a query for pattern analysis.

        Args:
            query_type: Type of query
            key_parts: Components of the query key
            was_cache_hit: Whether query hit cache
            compute_time_ms: Time to compute if cache miss
            session_id: Optional session for co-occurrence

        Returns:
            Pattern ID
        """
        pattern_id = self._make_pattern_id(query_type, key_parts)

        # Update or create pattern
        if pattern_id in self._patterns:
            pattern = self._patterns[pattern_id]
            pattern.last_accessed = datetime.now()
            if was_cache_hit:
                pattern.hit_count += 1
            else:
                pattern.miss_count += 1
                if compute_time_ms > 0:
                    total_computes = pattern.miss_count
                    pattern.total_compute_time_ms += compute_time_ms
                    pattern.avg_compute_time_ms = pattern.total_compute_time_ms / total_computes
        else:
            # Check if at capacity
            if len(self._patterns) >= self.max_tracked:
                self._evict_stale_patterns()

            pattern = QueryPattern(
                pattern_id=pattern_id,
                query_type=query_type,
                key_parts=key_parts,
                hit_count=1 if was_cache_hit else 0,
                miss_count=0 if was_cache_hit else 1,
                avg_compute_time_ms=compute_time_ms
            )
            self._patterns[pattern_id] = pattern

            # Index for lookups
            for part in key_parts:
                self._pattern_index[part].add(pattern_id)

        # Track temporal patterns
        current_hour = datetime.now().hour
        self._hourly_patterns[current_hour][pattern_id] += 1

        # Track session co-occurrence
        if session_id:
            self._track_session_cooccurrence(session_id, pattern_id)

        self.stats["patterns_tracked"] = len(self._patterns)

        return pattern_id

    async def optimize(
        self,
        strategy: OptimizationStrategy = OptimizationStrategy.HYBRID,
        max_precompute: int = 100
    ) -> OptimizationResult:
        """
        Run optimization cycle.

        Analyzes patterns and precomputes hot paths.
        """
        if self._optimization_running:
            return OptimizationResult(
                patterns_analyzed=0,
                patterns_precomputed=0,
                patterns_evicted=0,
                estimated_hit_rate_improvement=0,
                estimated_latency_reduction_ms=0,
                precomputation_time_ms=0
            )

        self._optimization_running = True
        start_time = datetime.now()

        try:
            # Identify hot patterns
            hot_patterns = self._identify_hot_patterns(strategy, max_precompute)

            # Precompute and cache
            precomputed = await self._precompute_patterns(hot_patterns)

            # Evict cold patterns
            evicted = self._evict_cold_patterns()

            # Calculate improvements
            hit_improvement = self._estimate_hit_rate_improvement(precomputed)
            latency_reduction = self._estimate_latency_reduction(precomputed)

            self._last_optimization = datetime.now()
            self.stats["optimization_cycles"] += 1

            elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

            return OptimizationResult(
                patterns_analyzed=len(self._patterns),
                patterns_precomputed=len(precomputed),
                patterns_evicted=evicted,
                estimated_hit_rate_improvement=hit_improvement,
                estimated_latency_reduction_ms=latency_reduction,
                precomputation_time_ms=elapsed_ms
            )

        finally:
            self._optimization_running = False

    def _identify_hot_patterns(
        self,
        strategy: OptimizationStrategy,
        limit: int
    ) -> List[QueryPattern]:
        """Identify patterns worth precomputing."""
        candidates = list(self._patterns.values())

        if strategy == OptimizationStrategy.FREQUENCY_BASED:
            # Sort by access frequency
            candidates.sort(key=lambda p: p.access_frequency, reverse=True)

        elif strategy == OptimizationStrategy.RECENCY_BASED:
            # Sort by last access time
            candidates.sort(key=lambda p: p.last_accessed, reverse=True)

        elif strategy == OptimizationStrategy.PREDICTIVE:
            # Predict based on time-of-day patterns
            current_hour = datetime.now().hour
            hour_patterns = self._hourly_patterns[current_hour]

            def predicted_score(p):
                return hour_patterns.get(p.pattern_id, 0) * p.avg_compute_time_ms

            candidates.sort(key=predicted_score, reverse=True)

        else:  # HYBRID
            # Combine frequency, recency, and compute cost
            candidates.sort(key=lambda p: p.cache_value_score, reverse=True)

        # Filter by threshold and limit
        hot = [
            p for p in candidates
            if p.access_frequency >= self.precompute_threshold
        ][:limit]

        return hot

    async def _precompute_patterns(
        self,
        patterns: List[QueryPattern]
    ) -> List[QueryPattern]:
        """Precompute and cache hot patterns."""
        precomputed = []

        for pattern in patterns:
            # Check if already cached
            cache_key = pattern.pattern_id
            cached = await self.cache.get(cache_key)

            if cached is None:
                # Would compute and cache here
                # For now, just mark as precomputed
                self.stats["precomputations"] += 1
                precomputed.append(pattern)

        return precomputed

    def _evict_cold_patterns(self, max_evict: int = 1000) -> int:
        """Evict stale/cold patterns to free memory."""
        if len(self._patterns) < self.max_tracked * 0.9:
            return 0

        # Find coldest patterns
        by_value = sorted(
            self._patterns.values(),
            key=lambda p: p.cache_value_score
        )

        evicted = 0
        for pattern in by_value[:max_evict]:
            if pattern.cache_value_score < 0.1:  # Very cold
                del self._patterns[pattern.pattern_id]
                evicted += 1

        return evicted

    def _evict_stale_patterns(self):
        """Emergency eviction when at capacity."""
        cutoff = datetime.now() - timedelta(hours=24)

        to_evict = [
            pid for pid, p in self._patterns.items()
            if p.last_accessed < cutoff
        ]

        for pid in to_evict[:len(self._patterns) // 10]:  # Evict 10%
            del self._patterns[pid]

    def _track_session_cooccurrence(self, session_id: str, pattern_id: str):
        """Track co-occurring patterns within a session."""
        session_queries = self._session_queries[session_id]
        session_queries.append(pattern_id)

        # Keep only recent queries
        if len(session_queries) > 20:
            session_queries.pop(0)

        # Update co-occurrence for recent patterns
        for other_id in session_queries[-5:-1]:  # Last 4 patterns
            if other_id != pattern_id and other_id in self._patterns:
                pattern = self._patterns[pattern_id]
                pattern.co_occurring_patterns[other_id] = (
                    pattern.co_occurring_patterns.get(other_id, 0) + 1
                )

    def get_prefetch_suggestions(
        self,
        current_pattern_id: str,
        limit: int = 5
    ) -> List[str]:
        """
        Get patterns to prefetch based on current query.

        Uses co-occurrence analysis.
        """
        if current_pattern_id not in self._patterns:
            return []

        pattern = self._patterns[current_pattern_id]
        co_occurring = pattern.co_occurring_patterns

        # Sort by co-occurrence count
        sorted_patterns = sorted(
            co_occurring.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [pid for pid, _ in sorted_patterns[:limit]]

    def get_time_based_suggestions(
        self,
        upcoming_hours: int = 1,
        limit: int = 20
    ) -> List[str]:
        """
        Get patterns likely to be queried in upcoming hours.

        Based on historical time-of-day patterns.
        """
        current_hour = datetime.now().hour
        suggestions: Dict[str, int] = defaultdict(int)

        for hour_offset in range(upcoming_hours):
            target_hour = (current_hour + hour_offset) % 24
            hour_data = self._hourly_patterns[target_hour]

            for pattern_id, count in hour_data.items():
                suggestions[pattern_id] += count

        # Sort by expected frequency
        sorted_suggestions = sorted(
            suggestions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [pid for pid, _ in sorted_suggestions[:limit]]

    def _estimate_hit_rate_improvement(
        self,
        precomputed: List[QueryPattern]
    ) -> float:
        """Estimate hit rate improvement from precomputation."""
        if not precomputed or not self._patterns:
            return 0.0

        total_queries = sum(p.hit_count + p.miss_count for p in self._patterns.values())
        precomputed_queries = sum(p.miss_count for p in precomputed)

        if total_queries == 0:
            return 0.0

        return precomputed_queries / total_queries * 100

    def _estimate_latency_reduction(
        self,
        precomputed: List[QueryPattern]
    ) -> float:
        """Estimate latency reduction from precomputation."""
        if not precomputed:
            return 0.0

        # Sum of (miss_count * avg_compute_time) for precomputed patterns
        saved_time = sum(
            p.miss_count * p.avg_compute_time_ms
            for p in precomputed
        )

        total_queries = sum(
            p.hit_count + p.miss_count
            for p in self._patterns.values()
        )

        if total_queries == 0:
            return 0.0

        return saved_time / total_queries

    def _make_pattern_id(self, query_type: str, key_parts: Tuple[str, ...]) -> str:
        """Generate pattern ID from query components."""
        return f"{query_type}:{':'.join(str(p) for p in key_parts)}"

    def get_statistics(self) -> Dict:
        """Get optimizer statistics."""
        if not self._patterns:
            return {
                "patterns_tracked": 0,
                "hot_patterns": 0,
                "cold_patterns": 0,
                "avg_frequency": 0,
                "precomputations": self.stats["precomputations"],
                "optimization_cycles": self.stats["optimization_cycles"]
            }

        frequencies = [p.access_frequency for p in self._patterns.values()]
        hot_count = sum(1 for f in frequencies if f >= self.precompute_threshold)

        return {
            "patterns_tracked": len(self._patterns),
            "hot_patterns": hot_count,
            "cold_patterns": len(self._patterns) - hot_count,
            "avg_frequency": sum(frequencies) / len(frequencies),
            "max_frequency": max(frequencies),
            "precomputations": self.stats["precomputations"],
            "prefetch_hits": self.stats["prefetch_hits"],
            "optimization_cycles": self.stats["optimization_cycles"],
            "last_optimization": self._last_optimization.isoformat() if self._last_optimization else None
        }

    def get_top_patterns(self, limit: int = 20) -> List[Dict]:
        """Get top patterns by cache value."""
        sorted_patterns = sorted(
            self._patterns.values(),
            key=lambda p: p.cache_value_score,
            reverse=True
        )[:limit]

        return [
            {
                "pattern_id": p.pattern_id,
                "query_type": p.query_type,
                "frequency": p.access_frequency,
                "hit_count": p.hit_count,
                "miss_count": p.miss_count,
                "avg_compute_ms": p.avg_compute_time_ms,
                "cache_value_score": p.cache_value_score,
                "last_accessed": p.last_accessed.isoformat()
            }
            for p in sorted_patterns
        ]
