"""
Failure Clustering Engine
Groups failures by characteristics for pattern detection.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import uuid

from ..types import FailureRecord, FailureCluster


logger = logging.getLogger(__name__)


@dataclass
class ClusteringConfig:
    """Configuration for failure clustering"""
    min_cluster_size: int = 3
    similarity_threshold: float = 0.6
    max_clusters: int = 100
    use_embeddings: bool = True


class FailureClusteringEngine:
    """
    Groups failures into clusters based on shared characteristics.

    Clustering dimensions:
    - Material type
    - Part type
    - Environment conditions
    - Load patterns
    - Age at failure
    - Prior events
    """

    def __init__(self, config: Optional[ClusteringConfig] = None):
        self.config = config or ClusteringConfig()

    def cluster(
        self,
        failures: List[FailureRecord],
    ) -> List[FailureCluster]:
        """
        Cluster failures into groups with similar characteristics.

        Uses a hierarchical approach:
        1. First group by failure mode (if known)
        2. Then sub-cluster by characteristics
        """
        if len(failures) < self.config.min_cluster_size:
            return []

        clusters = []

        # Primary grouping by failure mode
        by_mode: Dict[str, List[FailureRecord]] = defaultdict(list)
        for failure in failures:
            by_mode[failure.failure_mode].append(failure)

        # For each failure mode, create sub-clusters
        for mode, mode_failures in by_mode.items():
            if len(mode_failures) < self.config.min_cluster_size:
                continue

            # Use characteristic-based clustering
            mode_clusters = self._cluster_by_characteristics(mode_failures)
            clusters.extend(mode_clusters)

        # Limit number of clusters
        clusters = sorted(
            clusters,
            key=lambda c: len(c.failures),
            reverse=True
        )[:self.config.max_clusters]

        return clusters

    def _cluster_by_characteristics(
        self,
        failures: List[FailureRecord],
    ) -> List[FailureCluster]:
        """Cluster failures by their characteristics"""
        clusters = []

        # Group by material + part type combination
        groups: Dict[Tuple[str, str], List[FailureRecord]] = defaultdict(list)

        for failure in failures:
            key = (failure.material or "unknown", failure.part_type or "unknown")
            groups[key].append(failure)

        for (material, part_type), group_failures in groups.items():
            if len(group_failures) < self.config.min_cluster_size:
                continue

            # Further sub-cluster by environment and age
            sub_clusters = self._sub_cluster_by_conditions(group_failures)

            for sub_failures in sub_clusters:
                if len(sub_failures) >= self.config.min_cluster_size:
                    cluster = self._create_cluster(sub_failures)
                    clusters.append(cluster)

        return clusters

    def _sub_cluster_by_conditions(
        self,
        failures: List[FailureRecord],
    ) -> List[List[FailureRecord]]:
        """Sub-cluster by environmental conditions and age"""
        # Simple binning by age range
        age_bins: Dict[str, List[FailureRecord]] = defaultdict(list)

        for failure in failures:
            age = failure.age_at_failure or 0
            if age < 100:
                bin_key = "infant"
            elif age < 1000:
                bin_key = "early"
            elif age < 10000:
                bin_key = "midlife"
            else:
                bin_key = "mature"

            age_bins[bin_key].append(failure)

        return list(age_bins.values())

    def _create_cluster(
        self,
        failures: List[FailureRecord],
    ) -> FailureCluster:
        """Create a cluster from a group of failures"""
        cluster_id = str(uuid.uuid4())

        # Extract common characteristics
        common_chars = self._extract_common_characteristics(failures)

        # Calculate cluster coherence
        similarity = self._calculate_cluster_similarity(failures)

        return FailureCluster(
            cluster_id=cluster_id,
            failures=[f.id for f in failures],
            common_characteristics=common_chars,
            similarity_score=Decimal(str(similarity)),
        )

    def _extract_common_characteristics(
        self,
        failures: List[FailureRecord],
    ) -> Dict[str, Any]:
        """Extract characteristics common to all failures in group"""
        characteristics = {}

        # Materials
        materials = [f.material for f in failures if f.material]
        if materials:
            material_counts = defaultdict(int)
            for m in materials:
                material_counts[m] += 1
            common_materials = [
                m for m, c in material_counts.items()
                if c / len(failures) > 0.5
            ]
            characteristics["materials"] = common_materials

        # Part types
        part_types = [f.part_type for f in failures if f.part_type]
        if part_types:
            type_counts = defaultdict(int)
            for t in part_types:
                type_counts[t] += 1
            common_types = [
                t for t, c in type_counts.items()
                if c / len(failures) > 0.5
            ]
            characteristics["part_types"] = common_types

        # Environment
        env_keys: Set[str] = set()
        for f in failures:
            if f.environment:
                env_keys.update(f.environment.keys())

        if env_keys:
            common_env = {}
            for key in env_keys:
                values = [
                    f.environment.get(key) for f in failures
                    if f.environment and key in f.environment
                ]
                if len(values) / len(failures) > 0.5:
                    # Find most common value
                    value_counts = defaultdict(int)
                    for v in values:
                        value_counts[str(v)] += 1
                    if value_counts:
                        common_value = max(value_counts.items(), key=lambda x: x[1])
                        common_env[key] = common_value[0]

            if common_env:
                characteristics["environment"] = common_env

        # Age range
        ages = [f.age_at_failure for f in failures if f.age_at_failure is not None]
        if ages:
            characteristics["age_range"] = {
                "min": min(ages),
                "max": max(ages),
                "mean": sum(ages) / len(ages),
            }

        # Load patterns
        load_patterns = []
        for f in failures:
            if f.load_conditions:
                pattern = f.load_conditions.get("pattern")
                if pattern:
                    load_patterns.append(pattern)

        if load_patterns:
            pattern_counts = defaultdict(int)
            for p in load_patterns:
                pattern_counts[p] += 1
            if pattern_counts:
                common_pattern = max(pattern_counts.items(), key=lambda x: x[1])
                if common_pattern[1] / len(failures) > 0.5:
                    characteristics["load_pattern"] = common_pattern[0]

        # Prior events
        all_prior_events: List[str] = []
        for f in failures:
            all_prior_events.extend(f.prior_events)

        if all_prior_events:
            event_counts = defaultdict(int)
            for e in all_prior_events:
                event_counts[e] += 1
            common_events = [
                e for e, c in event_counts.items()
                if c / len(failures) > 0.3
            ]
            characteristics["prior_events"] = common_events

        return characteristics

    def _calculate_cluster_similarity(
        self,
        failures: List[FailureRecord],
    ) -> float:
        """Calculate average similarity within cluster"""
        if len(failures) < 2:
            return 1.0

        total_similarity = 0.0
        comparisons = 0

        # Sample pairs for efficiency
        sample_size = min(len(failures), 10)
        sample = failures[:sample_size]

        for i, f1 in enumerate(sample):
            for f2 in sample[i + 1:]:
                similarity = self._calculate_pair_similarity(f1, f2)
                total_similarity += similarity
                comparisons += 1

        return total_similarity / comparisons if comparisons > 0 else 0.0

    def _calculate_pair_similarity(
        self,
        f1: FailureRecord,
        f2: FailureRecord,
    ) -> float:
        """Calculate similarity between two failure records"""
        score = 0.0
        factors = 0

        # Same failure mode
        factors += 1
        if f1.failure_mode == f2.failure_mode:
            score += 1.0

        # Same material
        if f1.material and f2.material:
            factors += 1
            if f1.material == f2.material:
                score += 1.0

        # Same part type
        if f1.part_type and f2.part_type:
            factors += 1
            if f1.part_type == f2.part_type:
                score += 1.0

        # Similar age
        if f1.age_at_failure and f2.age_at_failure:
            factors += 1
            age_ratio = min(f1.age_at_failure, f2.age_at_failure) / max(f1.age_at_failure, f2.age_at_failure)
            score += age_ratio

        # Environment overlap
        if f1.environment and f2.environment:
            factors += 1
            common_keys = set(f1.environment.keys()) & set(f2.environment.keys())
            if common_keys:
                matching = sum(
                    1 for k in common_keys
                    if f1.environment[k] == f2.environment[k]
                )
                score += matching / len(common_keys)

        return score / factors if factors > 0 else 0.0

    def merge_clusters(
        self,
        clusters: List[FailureCluster],
        threshold: float = 0.8,
    ) -> List[FailureCluster]:
        """Merge highly similar clusters"""
        if len(clusters) < 2:
            return clusters

        merged = []
        used = set()

        for i, c1 in enumerate(clusters):
            if i in used:
                continue

            # Find clusters to merge with
            to_merge = [c1]
            for j, c2 in enumerate(clusters[i + 1:], i + 1):
                if j in used:
                    continue
                similarity = self._cluster_similarity(c1, c2)
                if similarity > threshold:
                    to_merge.append(c2)
                    used.add(j)

            # Merge clusters
            if len(to_merge) > 1:
                merged_cluster = self._merge_cluster_list(to_merge)
                merged.append(merged_cluster)
            else:
                merged.append(c1)

            used.add(i)

        return merged

    def _cluster_similarity(
        self,
        c1: FailureCluster,
        c2: FailureCluster,
    ) -> float:
        """Calculate similarity between two clusters"""
        chars1 = c1.common_characteristics
        chars2 = c2.common_characteristics

        score = 0.0
        factors = 0

        # Compare materials
        if "materials" in chars1 and "materials" in chars2:
            factors += 1
            overlap = set(chars1["materials"]) & set(chars2["materials"])
            if overlap:
                score += len(overlap) / max(len(chars1["materials"]), len(chars2["materials"]))

        # Compare part types
        if "part_types" in chars1 and "part_types" in chars2:
            factors += 1
            overlap = set(chars1["part_types"]) & set(chars2["part_types"])
            if overlap:
                score += len(overlap) / max(len(chars1["part_types"]), len(chars2["part_types"]))

        return score / factors if factors > 0 else 0.0

    def _merge_cluster_list(
        self,
        clusters: List[FailureCluster],
    ) -> FailureCluster:
        """Merge a list of clusters into one"""
        all_failures = []
        for c in clusters:
            all_failures.extend(c.failures)

        # Recalculate characteristics
        # (Would need actual failure records - simplified here)
        merged_chars = clusters[0].common_characteristics.copy()

        avg_similarity = sum(float(c.similarity_score) for c in clusters) / len(clusters)

        return FailureCluster(
            cluster_id=str(uuid.uuid4()),
            failures=all_failures,
            common_characteristics=merged_chars,
            similarity_score=Decimal(str(avg_similarity)),
        )
