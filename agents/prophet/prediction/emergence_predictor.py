"""
Emergence Predictor
Predicts what new patterns or categories might emerge.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional
import logging

from ..types import (
    Prediction,
    PredictionType,
    EmergenceIndicator,
    SwarmKnowledge,
    DetectedPattern,
    PatternLayer,
)


logger = logging.getLogger(__name__)


@dataclass
class EmergenceConfig:
    """Configuration for emergence prediction"""
    emergence_threshold: float = 0.7
    min_swarm_size: int = 100
    prediction_horizon_days: int = 180
    confidence_min: float = 0.5


class EmergencePredictor:
    """
    Predicts what new patterns or categories might emerge.

    Analyzes:
    - Swarm activity and collective learning rates
    - Pattern density and diversity
    - Cross-swarm knowledge flow
    - Precursor indicators for new behaviors
    """

    def __init__(self, config: Optional[EmergenceConfig] = None):
        self.config = config or EmergenceConfig()
        self._predictions: List[Prediction] = []

    def predict_emergence(
        self,
        swarm_knowledge: Dict[str, SwarmKnowledge],
        existing_patterns: Optional[List[DetectedPattern]] = None,
    ) -> List[Prediction]:
        """
        Predict what new patterns or categories might emerge.

        Args:
            swarm_knowledge: Knowledge from part swarms
            existing_patterns: Already detected patterns

        Returns:
            List of emergence predictions
        """
        predictions = []

        for swarm_id, knowledge in swarm_knowledge.items():
            if knowledge.member_count < self.config.min_swarm_size:
                continue

            # Calculate emergence indicators
            indicators = self._calculate_emergence_indicators(knowledge, existing_patterns)

            if indicators.score >= self.config.emergence_threshold:
                prediction = Prediction(
                    prediction_type=PredictionType.EMERGENCE,
                    subject_id=swarm_id,
                    subject_type="swarm",
                    prediction={
                        "event": "emergence",
                        "type": indicators.emergence_type,
                        "description": indicators.description,
                        "indicators": {
                            "score": float(indicators.score),
                            "emergence_type": indicators.emergence_type,
                            "estimated_timeline": indicators.estimated_timeline,
                            "estimated_impact": indicators.estimated_impact,
                        },
                    },
                    probability=Decimal(str(float(indicators.score))),
                    timeline_days=self._parse_timeline(indicators.estimated_timeline),
                    confidence=Decimal(str(float(indicators.confidence))),
                )
                predictions.append(prediction)
                self._predictions.append(prediction)

        logger.info(f"Generated {len(predictions)} emergence predictions")
        return predictions

    def _calculate_emergence_indicators(
        self,
        knowledge: SwarmKnowledge,
        patterns: Optional[List[DetectedPattern]] = None,
    ) -> EmergenceIndicator:
        """Calculate emergence indicators for a swarm"""
        # Collective learning rate indicator
        learning_rate = float(knowledge.collective_learning_rate)

        # Pattern density (patterns per member)
        patterns_for_swarm = []
        if patterns:
            patterns_for_swarm = [
                p for p in patterns
                if knowledge.swarm_id in str(p.evidence.get("swarm_ids", []))
            ]

        pattern_density = len(patterns_for_swarm) / max(knowledge.member_count, 1) * 1000

        # Success pattern emergence
        success_emergence = len(knowledge.success_patterns) / max(knowledge.member_count, 1) * 100

        # Calculate composite score
        score = (
            learning_rate * 0.4 +
            min(pattern_density, 1.0) * 0.3 +
            min(success_emergence, 1.0) * 0.3
        )

        # Determine emergence type
        emergence_type = self._determine_emergence_type(knowledge, patterns_for_swarm)

        # Estimate timeline
        timeline = self._estimate_emergence_timeline(score, learning_rate)

        # Estimate impact
        impact = self._estimate_emergence_impact(knowledge, emergence_type)

        # Calculate confidence
        confidence = self._calculate_emergence_confidence(knowledge, score)

        return EmergenceIndicator(
            swarm_id=knowledge.swarm_id,
            emergence_type=emergence_type,
            description=self._generate_emergence_description(emergence_type, knowledge),
            score=Decimal(str(round(score, 4))),
            estimated_timeline=timeline,
            estimated_impact=impact,
            confidence=Decimal(str(round(confidence, 4))),
        )

    def _determine_emergence_type(
        self,
        knowledge: SwarmKnowledge,
        patterns: List[DetectedPattern],
    ) -> str:
        """Determine the type of emergence occurring"""
        # Analyze pattern distribution
        layer_counts = {}
        for pattern in patterns:
            layer = pattern.layer.name
            layer_counts[layer] = layer_counts.get(layer, 0) + 1

        # High behavioral patterns = collective learning
        if layer_counts.get("BEHAVIORAL", 0) > len(patterns) * 0.4:
            return "collective_learning"

        # High relational patterns = network formation
        if layer_counts.get("RELATIONAL", 0) > len(patterns) * 0.3:
            return "network_formation"

        # High innovation patterns = capability emergence
        if layer_counts.get("INNOVATION", 0) > len(patterns) * 0.2:
            return "capability_emergence"

        # Default based on swarm characteristics
        if float(knowledge.collective_learning_rate) > 0.7:
            return "accelerated_learning"

        if knowledge.success_patterns:
            return "pattern_crystallization"

        return "general_emergence"

    def _estimate_emergence_timeline(
        self,
        score: float,
        learning_rate: float,
    ) -> str:
        """Estimate when emergence will manifest"""
        # Higher score and learning rate = faster emergence
        combined = (score + learning_rate) / 2

        if combined > 0.8:
            return "1-2 weeks"
        elif combined > 0.6:
            return "1-2 months"
        elif combined > 0.4:
            return "3-6 months"
        else:
            return "6+ months"

    def _estimate_emergence_impact(
        self,
        knowledge: SwarmKnowledge,
        emergence_type: str,
    ) -> str:
        """Estimate the impact of the emergence"""
        member_count = knowledge.member_count

        if member_count > 10000:
            scale = "high"
        elif member_count > 1000:
            scale = "medium"
        else:
            scale = "low"

        impact_descriptions = {
            "collective_learning": f"{scale.title()} impact - swarm developing shared expertise",
            "network_formation": f"{scale.title()} impact - compatibility network crystallizing",
            "capability_emergence": f"{scale.title()} impact - new capabilities emerging",
            "accelerated_learning": f"{scale.title()} impact - rapid knowledge growth",
            "pattern_crystallization": f"{scale.title()} impact - success patterns stabilizing",
            "general_emergence": f"{scale.title()} impact - novel behaviors forming",
        }

        return impact_descriptions.get(emergence_type, f"{scale.title()} impact expected")

    def _calculate_emergence_confidence(
        self,
        knowledge: SwarmKnowledge,
        score: float,
    ) -> float:
        """Calculate confidence in emergence prediction"""
        base_confidence = 0.5

        # Larger swarms provide more reliable signals
        if knowledge.member_count > 5000:
            base_confidence += 0.2
        elif knowledge.member_count > 1000:
            base_confidence += 0.1

        # Higher scores are more confident
        if score > 0.8:
            base_confidence += 0.15

        # Multiple success patterns increase confidence
        if len(knowledge.success_patterns) > 3:
            base_confidence += 0.1

        return min(base_confidence, 0.95)

    def _generate_emergence_description(
        self,
        emergence_type: str,
        knowledge: SwarmKnowledge,
    ) -> str:
        """Generate a human-readable description of the emergence"""
        descriptions = {
            "collective_learning": (
                f"Swarm {knowledge.swarm_id[:8]} is developing collective expertise "
                f"with {len(knowledge.success_patterns)} success patterns emerging"
            ),
            "network_formation": (
                f"Swarm {knowledge.swarm_id[:8]} is forming a compatibility network "
                f"among {knowledge.member_count} members"
            ),
            "capability_emergence": (
                f"New capabilities emerging in swarm {knowledge.swarm_id[:8]} - "
                f"potential for innovation"
            ),
            "accelerated_learning": (
                f"Swarm {knowledge.swarm_id[:8]} showing accelerated learning rate "
                f"({float(knowledge.collective_learning_rate):.2f})"
            ),
            "pattern_crystallization": (
                f"Success patterns crystallizing in swarm {knowledge.swarm_id[:8]} - "
                f"{len(knowledge.success_patterns)} patterns identified"
            ),
            "general_emergence": (
                f"Novel emergence detected in swarm {knowledge.swarm_id[:8]} - "
                f"monitoring for specific type"
            ),
        }

        return descriptions.get(emergence_type, f"Emergence detected in swarm {knowledge.swarm_id[:8]}")

    def _parse_timeline(self, timeline_str: str) -> int:
        """Parse timeline string to days"""
        timeline_map = {
            "1-2 weeks": 14,
            "1-2 months": 45,
            "3-6 months": 135,
            "6+ months": 180,
        }
        return timeline_map.get(timeline_str, 90)

    def get_high_emergence_swarms(
        self,
        threshold: float = 0.8,
    ) -> List[Prediction]:
        """Get swarms with high emergence probability"""
        return [
            p for p in self._predictions
            if float(p.probability) >= threshold
        ]
