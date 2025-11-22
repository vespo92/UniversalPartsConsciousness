"""
Novel Failure Mode Detection
Identifies failure modes not in existing taxonomy.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..types import (
    NovelFailureMode,
    FailureRecord,
    FailureCluster,
    FailureModeStatus,
    UrgencyLevel,
)


logger = logging.getLogger(__name__)


@dataclass
class FailureTaxonomy:
    """Known failure mode taxonomy"""
    modes: Dict[str, Dict[str, Any]]  # mode_id -> mode details
    categories: List[str]
    embeddings: Optional[Dict[str, List[float]]] = None  # For similarity matching


@dataclass
class DetectionConfig:
    """Configuration for novel failure detection"""
    similarity_threshold: float = 0.7  # Below this = novel
    min_cluster_size: int = 3
    urgency_failure_count_critical: int = 50
    urgency_failure_count_high: int = 20
    confidence_min_samples: int = 10


class NovelFailureDetector:
    """
    Identifies failure modes that haven't been documented before.

    Process:
    1. Cluster recent failures by characteristics
    2. Compare each cluster to known failure taxonomy
    3. Identify clusters with low similarity to known modes
    4. Generate novel failure mode proposals
    """

    def __init__(
        self,
        taxonomy: Optional[FailureTaxonomy] = None,
        config: Optional[DetectionConfig] = None,
    ):
        self.taxonomy = taxonomy or FailureTaxonomy(modes={}, categories=[])
        self.config = config or DetectionConfig()
        self._detected_novel_modes: List[NovelFailureMode] = []

    def detect_novel_failures(
        self,
        recent_failures: List[FailureRecord],
        known_failures: Optional[FailureTaxonomy] = None,
    ) -> List[NovelFailureMode]:
        """
        Analyze recent failures to find patterns not in existing taxonomy.

        Args:
            recent_failures: List of recent failure records
            known_failures: Optional updated taxonomy

        Returns:
            List of novel failure modes detected
        """
        if known_failures:
            self.taxonomy = known_failures

        novel_modes = []

        if len(recent_failures) < self.config.min_cluster_size:
            return novel_modes

        # Step 1: Cluster recent failures by characteristics
        clusters = self._cluster_failures(recent_failures)
        logger.info(f"Created {len(clusters)} failure clusters")

        # Step 2: Check each cluster against known taxonomy
        for cluster in clusters:
            if len(cluster.failures) < self.config.min_cluster_size:
                continue

            # Find best match in taxonomy
            best_match = self._find_taxonomy_match(cluster)

            # Step 3: If similarity is low, this is a novel failure mode
            if best_match["similarity"] < self.config.similarity_threshold:
                novel_mode = self._create_novel_failure_mode(cluster, best_match)
                novel_modes.append(novel_mode)
                self._detected_novel_modes.append(novel_mode)

        logger.info(f"Detected {len(novel_modes)} novel failure modes")
        return novel_modes

    def _cluster_failures(
        self,
        failures: List[FailureRecord],
    ) -> List[FailureCluster]:
        """Cluster failures by their characteristics"""
        from .failure_clustering import FailureClusteringEngine

        clustering = FailureClusteringEngine()
        return clustering.cluster(failures)

    def _find_taxonomy_match(
        self,
        cluster: FailureCluster,
    ) -> Dict[str, Any]:
        """Find the best matching failure mode in taxonomy"""
        if not self.taxonomy.modes:
            return {"similarity": 0.0, "matched_mode": None}

        best_similarity = 0.0
        best_mode = None

        cluster_chars = cluster.common_characteristics

        for mode_id, mode_info in self.taxonomy.modes.items():
            similarity = self._calculate_similarity(cluster_chars, mode_info)
            if similarity > best_similarity:
                best_similarity = similarity
                best_mode = mode_id

        return {
            "similarity": best_similarity,
            "matched_mode": best_mode,
            "matched_mode_info": self.taxonomy.modes.get(best_mode, {}),
        }

    def _calculate_similarity(
        self,
        cluster_chars: Dict[str, Any],
        mode_info: Dict[str, Any],
    ) -> float:
        """Calculate similarity between cluster and known mode"""
        if not cluster_chars or not mode_info:
            return 0.0

        matching_attrs = 0
        total_attrs = 0

        # Compare materials
        if "common_materials" in cluster_chars and "materials" in mode_info:
            total_attrs += 1
            cluster_materials = set(cluster_chars.get("common_materials", []))
            mode_materials = set(mode_info.get("materials", []))
            if cluster_materials & mode_materials:
                matching_attrs += 1

        # Compare environment
        if "common_environment" in cluster_chars and "environment" in mode_info:
            total_attrs += 1
            if cluster_chars.get("common_environment", {}).get("primary") == mode_info.get("environment"):
                matching_attrs += 1

        # Compare load patterns
        if "common_load_pattern" in cluster_chars and "load_pattern" in mode_info:
            total_attrs += 1
            if cluster_chars.get("common_load_pattern") == mode_info.get("load_pattern"):
                matching_attrs += 1

        # Compare part types
        if "affected_part_types" in cluster_chars and "part_types" in mode_info:
            total_attrs += 1
            cluster_types = set(cluster_chars.get("affected_part_types", []))
            mode_types = set(mode_info.get("part_types", []))
            if cluster_types & mode_types:
                matching_attrs += 1

        return matching_attrs / total_attrs if total_attrs > 0 else 0.0

    def _create_novel_failure_mode(
        self,
        cluster: FailureCluster,
        best_match: Dict[str, Any],
    ) -> NovelFailureMode:
        """Create a novel failure mode from a cluster"""
        characteristics = self._extract_common_characteristics(cluster)

        return NovelFailureMode(
            cluster_id=cluster.cluster_id,
            proposed_name=self._generate_failure_name(cluster, characteristics),
            proposed_category=self._suggest_category(cluster, best_match),
            common_characteristics=characteristics,
            affected_part_types=characteristics.get("affected_part_types", []),
            conditions=self._extract_conditions(cluster),
            failure_count=len(cluster.failures),
            first_occurrence_at=self._find_first_occurrence(cluster),
            affected_parts_count=len(set(cluster.failures)),
            documentation_status=FailureModeStatus.PROPOSED,
            urgency=self._assess_urgency(cluster),
            confidence_score=self._calculate_confidence(cluster),
        )

    def _extract_common_characteristics(
        self,
        cluster: FailureCluster,
    ) -> Dict[str, Any]:
        """Find what all failures in the cluster have in common"""
        return {
            "common_materials": cluster.common_characteristics.get("materials", []),
            "common_environment": cluster.common_characteristics.get("environment", {}),
            "common_load_pattern": cluster.common_characteristics.get("load_pattern"),
            "common_age_range": cluster.common_characteristics.get("age_range", {}),
            "common_prior_events": cluster.common_characteristics.get("prior_events", []),
            "affected_part_types": cluster.common_characteristics.get("part_types", []),
        }

    def _extract_conditions(
        self,
        cluster: FailureCluster,
    ) -> Dict[str, Any]:
        """Extract failure conditions from cluster"""
        return {
            "environmental_conditions": cluster.common_characteristics.get("environment", {}),
            "load_conditions": cluster.common_characteristics.get("load_pattern"),
            "temporal_conditions": cluster.common_characteristics.get("age_range", {}),
            "precursor_events": cluster.common_characteristics.get("prior_events", []),
        }

    def _generate_failure_name(
        self,
        cluster: FailureCluster,
        characteristics: Dict[str, Any],
    ) -> str:
        """Generate a descriptive name for the novel failure mode"""
        material = "unknown"
        materials = characteristics.get("common_materials", [])
        if materials:
            material = materials[0]

        environment = characteristics.get("common_environment", {}).get("primary", "general")
        mechanism = self._infer_mechanism(cluster)

        return f"{material}_{environment}_{mechanism}_failure"

    def _infer_mechanism(self, cluster: FailureCluster) -> str:
        """Infer the failure mechanism from cluster characteristics"""
        chars = cluster.common_characteristics

        # Simple rule-based inference
        if chars.get("load_pattern") == "cyclic":
            return "fatigue"
        elif chars.get("environment", {}).get("moisture", False):
            return "corrosion"
        elif chars.get("temperature", 0) > 200:
            return "thermal"
        elif chars.get("age_range", {}).get("mean", 0) < 100:
            return "infant"
        else:
            return "stress"

    def _suggest_category(
        self,
        cluster: FailureCluster,
        best_match: Dict[str, Any],
    ) -> str:
        """Suggest a category for the novel failure mode"""
        # If there's a partial match, use its category
        if best_match.get("matched_mode_info"):
            return best_match["matched_mode_info"].get("category", "uncategorized")

        # Otherwise, infer from mechanism
        mechanism = self._infer_mechanism(cluster)
        category_map = {
            "fatigue": "mechanical_fatigue",
            "corrosion": "environmental_degradation",
            "thermal": "thermal_failure",
            "infant": "manufacturing_defect",
            "stress": "mechanical_overload",
        }
        return category_map.get(mechanism, "uncategorized")

    def _find_first_occurrence(
        self,
        cluster: FailureCluster,
    ) -> Optional[datetime]:
        """Find the first occurrence timestamp in the cluster"""
        # Would iterate through actual failure records
        # For now, return current time as placeholder
        return datetime.now()

    def _assess_urgency(
        self,
        cluster: FailureCluster,
    ) -> UrgencyLevel:
        """Assess the urgency of the novel failure mode"""
        failure_count = len(cluster.failures)

        if failure_count >= self.config.urgency_failure_count_critical:
            return UrgencyLevel.CRITICAL
        elif failure_count >= self.config.urgency_failure_count_high:
            return UrgencyLevel.HIGH
        elif failure_count >= 10:
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW

    def _calculate_confidence(
        self,
        cluster: FailureCluster,
    ) -> Decimal:
        """Calculate confidence in the novel failure mode detection"""
        failure_count = len(cluster.failures)
        coherence = float(cluster.similarity_score)

        # More failures = higher confidence
        count_factor = min(failure_count / self.config.confidence_min_samples, 1.0)

        # Higher coherence = higher confidence
        coherence_factor = coherence

        confidence = (count_factor * 0.5 + coherence_factor * 0.5)
        return Decimal(str(min(confidence, 0.95)))

    def get_detected_modes(
        self,
        status: Optional[FailureModeStatus] = None,
    ) -> List[NovelFailureMode]:
        """Get all detected novel failure modes"""
        if status:
            return [m for m in self._detected_novel_modes if m.documentation_status == status]
        return self._detected_novel_modes

    def update_mode_status(
        self,
        mode_id: str,
        new_status: FailureModeStatus,
        taxonomy_id: Optional[str] = None,
    ) -> bool:
        """Update the status of a detected novel failure mode"""
        for mode in self._detected_novel_modes:
            if mode.id == mode_id:
                mode.documentation_status = new_status
                if taxonomy_id:
                    mode.taxonomy_id = taxonomy_id
                return True
        return False
