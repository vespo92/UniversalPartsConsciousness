"""
Layer 1: Statistical Pattern Detection
Detects failure rate anomalies, correlations, distribution shifts, and trends.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
import logging
import math

from ..types import DetectedPattern, PatternLayer, FailureRecord


logger = logging.getLogger(__name__)


@dataclass
class AnomalyThresholds:
    """Thresholds for anomaly detection"""
    failure_rate_z_score: float = 2.5  # Standard deviations
    correlation_min: float = 0.7
    distribution_shift_threshold: float = 0.15  # KL divergence
    trend_significance: float = 0.05  # p-value


class StatisticalPatternDetector:
    """
    Layer 1: Statistical Pattern Detection

    Detects:
    - Failure rate anomalies (sudden increases)
    - Correlation discovery (unexpected relationships)
    - Distribution shifts (performance degradation clusters)
    - Trend detection (gradual changes in behavior)
    """

    def __init__(self, thresholds: Optional[AnomalyThresholds] = None):
        self.thresholds = thresholds or AnomalyThresholds()

    @property
    def layer(self) -> PatternLayer:
        return PatternLayer.STATISTICAL

    def detect(self, data: Dict[str, Any]) -> List[DetectedPattern]:
        """
        Detect statistical patterns from input data.

        Args:
            data: Dictionary containing:
                - failure_records: List[FailureRecord]
                - temporal_data: Historical time series
                - swarm_knowledge: Swarm statistics
        """
        patterns = []

        failure_records = data.get("failure_records", [])
        temporal_data = data.get("temporal_data", {})

        # Detect failure rate anomalies
        anomalies = self._detect_failure_rate_anomalies(failure_records)
        patterns.extend(anomalies)

        # Detect correlations
        correlations = self._detect_correlations(failure_records)
        patterns.extend(correlations)

        # Detect distribution shifts
        shifts = self._detect_distribution_shifts(failure_records, temporal_data)
        patterns.extend(shifts)

        # Detect trends
        trends = self._detect_trends(failure_records, temporal_data)
        patterns.extend(trends)

        return patterns

    def _detect_failure_rate_anomalies(
        self,
        failures: List[FailureRecord],
    ) -> List[DetectedPattern]:
        """Detect sudden changes in failure rates"""
        patterns = []

        if len(failures) < 10:
            return patterns

        # Group failures by part type
        by_type: Dict[str, List[FailureRecord]] = defaultdict(list)
        for failure in failures:
            by_type[failure.part_type].append(failure)

        for part_type, type_failures in by_type.items():
            if len(type_failures) < 5:
                continue

            # Calculate failure rate over time windows
            windows = self._calculate_failure_windows(type_failures)

            if len(windows) < 3:
                continue

            # Calculate statistics
            mean = sum(windows) / len(windows)
            if mean == 0:
                continue

            variance = sum((w - mean) ** 2 for w in windows) / len(windows)
            std_dev = math.sqrt(variance) if variance > 0 else 0.01

            # Check for anomalies (z-score)
            latest_rate = windows[-1]
            z_score = (latest_rate - mean) / std_dev if std_dev > 0 else 0

            if abs(z_score) > self.thresholds.failure_rate_z_score:
                direction = "increase" if z_score > 0 else "decrease"
                pattern = DetectedPattern(
                    layer=PatternLayer.STATISTICAL,
                    pattern_type="failure_rate_anomaly",
                    category="anomaly",
                    name=f"{part_type} failure rate {direction}",
                    description=(
                        f"Detected {abs(z_score):.1f} sigma {direction} in "
                        f"failure rate for {part_type}"
                    ),
                    significance_score=Decimal(str(min(abs(z_score) / 5, 1.0))),
                    evidence={
                        "part_type": part_type,
                        "z_score": z_score,
                        "mean_rate": mean,
                        "current_rate": latest_rate,
                        "direction": direction,
                    },
                    sample_size=len(type_failures),
                    confidence=Decimal(str(min(abs(z_score) / 3, 0.99))),
                )
                patterns.append(pattern)

        return patterns

    def _detect_correlations(
        self,
        failures: List[FailureRecord],
    ) -> List[DetectedPattern]:
        """Detect unexpected correlations between failure characteristics"""
        patterns = []

        if len(failures) < 20:
            return patterns

        # Analyze correlations between:
        # - Material and failure mode
        # - Environment and failure mode
        # - Part type and environment

        correlations = self._calculate_correlations(failures)

        for (attr1, val1), (attr2, val2), strength in correlations:
            if strength > self.thresholds.correlation_min:
                pattern = DetectedPattern(
                    layer=PatternLayer.STATISTICAL,
                    pattern_type="correlation",
                    category="relationship",
                    name=f"Correlation: {val1} <-> {val2}",
                    description=(
                        f"Strong correlation ({strength:.2f}) detected between "
                        f"{attr1}={val1} and {attr2}={val2}"
                    ),
                    significance_score=Decimal(str(strength)),
                    evidence={
                        "attribute_1": attr1,
                        "value_1": val1,
                        "attribute_2": attr2,
                        "value_2": val2,
                        "correlation_strength": strength,
                    },
                    sample_size=len(failures),
                    confidence=Decimal(str(strength * 0.9)),
                )
                patterns.append(pattern)

        return patterns

    def _detect_distribution_shifts(
        self,
        failures: List[FailureRecord],
        temporal_data: Dict[str, Any],
    ) -> List[DetectedPattern]:
        """Detect shifts in failure mode distributions"""
        patterns = []

        if len(failures) < 30:
            return patterns

        # Compare recent vs historical distribution
        historical_dist = temporal_data.get("historical_failure_distribution", {})
        if not historical_dist:
            return patterns

        # Calculate current distribution
        current_dist = self._calculate_failure_distribution(failures)

        # Calculate KL divergence
        divergence = self._kl_divergence(historical_dist, current_dist)

        if divergence > self.thresholds.distribution_shift_threshold:
            # Find which modes shifted most
            shifts = self._identify_distribution_shifts(historical_dist, current_dist)

            pattern = DetectedPattern(
                layer=PatternLayer.STATISTICAL,
                pattern_type="distribution_shift",
                category="trend",
                name="Failure mode distribution shift",
                description=(
                    f"Significant shift in failure mode distribution "
                    f"(KL divergence: {divergence:.3f})"
                ),
                significance_score=Decimal(str(min(divergence * 2, 1.0))),
                evidence={
                    "kl_divergence": divergence,
                    "major_shifts": shifts[:5],
                    "historical_distribution": historical_dist,
                    "current_distribution": current_dist,
                },
                sample_size=len(failures),
                confidence=Decimal(str(min(0.5 + divergence, 0.95))),
            )
            patterns.append(pattern)

        return patterns

    def _detect_trends(
        self,
        failures: List[FailureRecord],
        temporal_data: Dict[str, Any],
    ) -> List[DetectedPattern]:
        """Detect gradual trends in failure behavior"""
        patterns = []

        if len(failures) < 20:
            return patterns

        # Group by time periods and analyze trends
        time_series = self._build_time_series(failures)

        if len(time_series) < 4:
            return patterns

        # Calculate linear regression
        slope, r_squared = self._linear_regression(time_series)

        if r_squared > 0.6 and abs(slope) > 0.01:
            direction = "increasing" if slope > 0 else "decreasing"
            pattern = DetectedPattern(
                layer=PatternLayer.STATISTICAL,
                pattern_type="trend",
                category="trend",
                name=f"Failure rate trend: {direction}",
                description=(
                    f"Detected {direction} trend in failure rate "
                    f"(slope: {slope:.4f}, R²: {r_squared:.3f})"
                ),
                significance_score=Decimal(str(r_squared)),
                evidence={
                    "slope": slope,
                    "r_squared": r_squared,
                    "direction": direction,
                    "data_points": len(time_series),
                },
                sample_size=len(failures),
                confidence=Decimal(str(r_squared * 0.95)),
            )
            patterns.append(pattern)

        return patterns

    def _calculate_failure_windows(
        self,
        failures: List[FailureRecord],
        window_days: int = 7,
    ) -> List[float]:
        """Calculate failure rates in time windows"""
        if not failures:
            return []

        # Sort by timestamp
        sorted_failures = sorted(failures, key=lambda f: f.failure_timestamp)

        start = sorted_failures[0].failure_timestamp
        end = sorted_failures[-1].failure_timestamp

        windows = []
        current = start

        while current < end:
            window_end = current + timedelta(days=window_days)
            count = sum(
                1 for f in sorted_failures
                if current <= f.failure_timestamp < window_end
            )
            windows.append(count / window_days)
            current = window_end

        return windows

    def _calculate_correlations(
        self,
        failures: List[FailureRecord],
    ) -> List[Tuple[Tuple[str, str], Tuple[str, str], float]]:
        """Calculate pairwise correlations between attributes"""
        correlations = []

        # Extract attribute pairs
        pairs = [
            ("material", "failure_mode"),
            ("part_type", "failure_mode"),
            ("part_type", "environment"),
        ]

        for attr1, attr2 in pairs:
            co_occurrences: Dict[Tuple[str, str], int] = defaultdict(int)
            attr1_counts: Dict[str, int] = defaultdict(int)
            attr2_counts: Dict[str, int] = defaultdict(int)

            for failure in failures:
                val1 = getattr(failure, attr1, None) or failure.environment.get(attr1, "unknown")
                val2 = getattr(failure, attr2, "") or failure.environment.get(attr2, "unknown")

                if val1 and val2:
                    co_occurrences[(val1, val2)] += 1
                    attr1_counts[val1] += 1
                    attr2_counts[val2] += 1

            total = len(failures)
            if total == 0:
                continue

            # Calculate phi coefficient for each pair
            for (val1, val2), count in co_occurrences.items():
                expected = (attr1_counts[val1] * attr2_counts[val2]) / total
                if expected > 0:
                    # Simplified correlation measure
                    strength = (count - expected) / max(expected, 1)
                    if strength > 0:
                        correlations.append(
                            ((attr1, val1), (attr2, val2), min(strength, 1.0))
                        )

        # Sort by strength
        correlations.sort(key=lambda x: x[2], reverse=True)
        return correlations[:20]  # Top 20

    def _calculate_failure_distribution(
        self,
        failures: List[FailureRecord],
    ) -> Dict[str, float]:
        """Calculate distribution of failure modes"""
        counts: Dict[str, int] = defaultdict(int)
        for failure in failures:
            counts[failure.failure_mode] += 1

        total = len(failures)
        return {mode: count / total for mode, count in counts.items()}

    def _kl_divergence(
        self,
        p: Dict[str, float],
        q: Dict[str, float],
    ) -> float:
        """Calculate KL divergence between two distributions"""
        all_keys = set(p.keys()) | set(q.keys())
        epsilon = 1e-10

        divergence = 0.0
        for key in all_keys:
            p_val = p.get(key, epsilon)
            q_val = q.get(key, epsilon)
            if p_val > 0:
                divergence += p_val * math.log(p_val / q_val)

        return divergence

    def _identify_distribution_shifts(
        self,
        historical: Dict[str, float],
        current: Dict[str, float],
    ) -> List[Dict[str, Any]]:
        """Identify which failure modes shifted most"""
        shifts = []
        all_modes = set(historical.keys()) | set(current.keys())

        for mode in all_modes:
            hist_val = historical.get(mode, 0)
            curr_val = current.get(mode, 0)
            diff = curr_val - hist_val

            if abs(diff) > 0.02:
                shifts.append({
                    "mode": mode,
                    "historical": hist_val,
                    "current": curr_val,
                    "change": diff,
                    "direction": "increased" if diff > 0 else "decreased",
                })

        shifts.sort(key=lambda x: abs(x["change"]), reverse=True)
        return shifts

    def _build_time_series(
        self,
        failures: List[FailureRecord],
    ) -> List[Tuple[float, float]]:
        """Build time series data from failures"""
        if not failures:
            return []

        sorted_failures = sorted(failures, key=lambda f: f.failure_timestamp)
        start = sorted_failures[0].failure_timestamp

        # Weekly aggregation
        weekly_counts: Dict[int, int] = defaultdict(int)
        for failure in sorted_failures:
            week = (failure.failure_timestamp - start).days // 7
            weekly_counts[week] += 1

        if not weekly_counts:
            return []

        max_week = max(weekly_counts.keys())
        return [(float(w), float(weekly_counts.get(w, 0))) for w in range(max_week + 1)]

    def _linear_regression(
        self,
        data: List[Tuple[float, float]],
    ) -> Tuple[float, float]:
        """Simple linear regression returning slope and R-squared"""
        if len(data) < 2:
            return 0.0, 0.0

        n = len(data)
        sum_x = sum(x for x, y in data)
        sum_y = sum(y for x, y in data)
        sum_xy = sum(x * y for x, y in data)
        sum_xx = sum(x * x for x, y in data)
        sum_yy = sum(y * y for x, y in data)

        denominator = n * sum_xx - sum_x ** 2
        if denominator == 0:
            return 0.0, 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator

        # Calculate R-squared
        mean_y = sum_y / n
        ss_tot = sum((y - mean_y) ** 2 for x, y in data)
        ss_res = sum((y - (slope * x + (sum_y - slope * sum_x) / n)) ** 2 for x, y in data)

        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

        return slope, max(0, r_squared)
