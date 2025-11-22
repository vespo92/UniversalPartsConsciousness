"""
Core Pattern Detection Engine
Orchestrates 5-layer emergence detection architecture.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
import logging

from ..types import (
    DetectedPattern,
    PatternLayer,
    PatternStatus,
    FailureRecord,
    Assembly,
    SwarmKnowledge,
)


logger = logging.getLogger(__name__)


@runtime_checkable
class PatternDetector(Protocol):
    """Protocol for layer-specific pattern detectors"""

    def detect(self, data: Dict[str, Any]) -> List[DetectedPattern]:
        """Detect patterns from input data"""
        ...

    @property
    def layer(self) -> PatternLayer:
        """Return the pattern layer this detector handles"""
        ...


@dataclass
class PatternDetectionConfig:
    """Configuration for pattern detection"""
    min_confidence_threshold: Decimal = Decimal("0.6")
    min_sample_size: int = 10
    significance_threshold: Decimal = Decimal("0.5")
    max_patterns_per_run: int = 1000
    enable_real_time: bool = True


class EmergenceDetectionEngine:
    """
    Core pattern detection engine implementing 5-layer architecture.

    Layer 1: Statistical Patterns - anomalies, correlations, trends
    Layer 2: Behavioral Patterns - success formulas, failure modes
    Layer 3: Relational Patterns - compatibility networks, archetypes
    Layer 4: Innovation Patterns - gaps, cross-domain insights
    Layer 5: Meta-Patterns - patterns of patterns, transcendence
    """

    def __init__(
        self,
        config: Optional[PatternDetectionConfig] = None,
        storage: Optional[Any] = None,
    ):
        self.config = config or PatternDetectionConfig()
        self.storage = storage
        self._layer_detectors: Dict[PatternLayer, PatternDetector] = {}
        self._detected_patterns: List[DetectedPattern] = []

    def register_detector(self, detector: PatternDetector) -> None:
        """Register a layer-specific detector"""
        self._layer_detectors[detector.layer] = detector
        logger.info(f"Registered detector for layer {detector.layer.name}")

    def detect_all_layers(
        self,
        failure_records: List[FailureRecord],
        assemblies: List[Assembly],
        swarm_knowledge: Dict[str, SwarmKnowledge],
        temporal_data: Optional[Dict[str, Any]] = None,
    ) -> List[DetectedPattern]:
        """
        Run detection across all 5 layers.

        Returns patterns sorted by significance.
        """
        all_patterns = []

        # Prepare unified data context
        context = {
            "failure_records": failure_records,
            "assemblies": assemblies,
            "swarm_knowledge": swarm_knowledge,
            "temporal_data": temporal_data or {},
            "existing_patterns": self._detected_patterns,
        }

        # Run each layer in sequence (earlier layers inform later ones)
        for layer in PatternLayer:
            if layer in self._layer_detectors:
                detector = self._layer_detectors[layer]
                try:
                    layer_patterns = detector.detect(context)

                    # Filter by thresholds
                    filtered = self._filter_patterns(layer_patterns)
                    all_patterns.extend(filtered)

                    # Add to context for next layers
                    context[f"layer_{layer.value}_patterns"] = filtered

                    logger.info(
                        f"Layer {layer.name}: detected {len(filtered)} patterns"
                    )
                except Exception as e:
                    logger.error(f"Error in layer {layer.name}: {e}")
            else:
                logger.warning(f"No detector registered for layer {layer.name}")

        # Sort by significance
        all_patterns.sort(
            key=lambda p: float(p.significance_score),
            reverse=True
        )

        # Limit results
        all_patterns = all_patterns[:self.config.max_patterns_per_run]

        # Store and return
        self._detected_patterns.extend(all_patterns)
        if self.storage:
            self._persist_patterns(all_patterns)

        return all_patterns

    def detect_single_layer(
        self,
        layer: PatternLayer,
        data: Dict[str, Any],
    ) -> List[DetectedPattern]:
        """Run detection for a specific layer"""
        if layer not in self._layer_detectors:
            raise ValueError(f"No detector registered for layer {layer.name}")

        detector = self._layer_detectors[layer]
        patterns = detector.detect(data)
        return self._filter_patterns(patterns)

    def _filter_patterns(
        self,
        patterns: List[DetectedPattern],
    ) -> List[DetectedPattern]:
        """Filter patterns by thresholds"""
        filtered = []
        for pattern in patterns:
            if (
                pattern.confidence >= self.config.min_confidence_threshold
                and pattern.sample_size >= self.config.min_sample_size
                and pattern.significance_score >= self.config.significance_threshold
            ):
                filtered.append(pattern)
        return filtered

    def _persist_patterns(self, patterns: List[DetectedPattern]) -> None:
        """Persist patterns to storage"""
        if not self.storage:
            return
        for pattern in patterns:
            try:
                self.storage.save_pattern(pattern.to_dict())
            except Exception as e:
                logger.error(f"Failed to persist pattern {pattern.pattern_id}: {e}")

    def get_patterns_by_layer(
        self,
        layer: PatternLayer,
        status: Optional[PatternStatus] = None,
    ) -> List[DetectedPattern]:
        """Retrieve patterns for a specific layer"""
        patterns = [p for p in self._detected_patterns if p.layer == layer]
        if status:
            patterns = [p for p in patterns if p.status == status]
        return patterns

    def confirm_pattern(self, pattern_id: str) -> bool:
        """Confirm a detected pattern"""
        for pattern in self._detected_patterns:
            if pattern.pattern_id == pattern_id:
                pattern.status = PatternStatus.CONFIRMED
                pattern.last_confirmed_at = datetime.now()
                pattern.detection_count += 1
                return True
        return False

    def invalidate_pattern(self, pattern_id: str, reason: str = "") -> bool:
        """Invalidate a previously detected pattern"""
        for pattern in self._detected_patterns:
            if pattern.pattern_id == pattern_id:
                pattern.status = PatternStatus.INVALIDATED
                pattern.evidence["invalidation_reason"] = reason
                return True
        return False

    def get_active_patterns_count(self) -> Dict[PatternLayer, int]:
        """Get count of active patterns by layer"""
        counts = {layer: 0 for layer in PatternLayer}
        for pattern in self._detected_patterns:
            if pattern.status == PatternStatus.ACTIVE:
                counts[pattern.layer] += 1
        return counts

    def calculate_emergence_score(
        self,
        swarm_id: str,
        swarm_knowledge: SwarmKnowledge,
    ) -> Decimal:
        """
        Calculate emergence score for a swarm.

        Emergence indicators:
        - Pattern density (patterns per member)
        - Cross-layer pattern connections
        - Novel pattern emergence rate
        - Collective learning indicators
        """
        patterns_for_swarm = [
            p for p in self._detected_patterns
            if swarm_id in str(p.evidence.get("swarm_ids", []))
        ]

        if not patterns_for_swarm or swarm_knowledge.member_count == 0:
            return Decimal("0.0")

        # Pattern density score (0-0.3)
        density = len(patterns_for_swarm) / swarm_knowledge.member_count
        density_score = min(Decimal(str(density)) * 10, Decimal("0.3"))

        # Layer diversity score (0-0.3)
        layers_present = set(p.layer for p in patterns_for_swarm)
        layer_score = Decimal(str(len(layers_present) / 5)) * Decimal("0.3")

        # Confidence score (0-0.2)
        avg_confidence = sum(
            p.confidence for p in patterns_for_swarm
        ) / len(patterns_for_swarm)
        confidence_score = avg_confidence * Decimal("0.2")

        # Collective learning rate (0-0.2)
        learning_score = swarm_knowledge.collective_learning_rate * Decimal("0.2")

        return density_score + layer_score + confidence_score + learning_score
