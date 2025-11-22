"""
Predictive Insight Engine
Generates predictions about future part behavior and needs.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
import logging

from ..types import (
    Prediction,
    PredictionType,
    SwarmKnowledge,
    FailureRecord,
    Assembly,
    DetectedPattern,
)
from .failure_predictor import FailurePredictor, Part
from .emergence_predictor import EmergencePredictor


logger = logging.getLogger(__name__)


@dataclass
class EngineConfig:
    """Configuration for predictive engine"""
    enable_failure_prediction: bool = True
    enable_demand_prediction: bool = True
    enable_evolution_prediction: bool = True
    enable_emergence_prediction: bool = True
    prediction_horizon_days: int = 90


class PredictiveInsightEngine:
    """
    Generates predictions about the future state of the parts ecosystem.

    Prediction types:
    1. Failure Predictions - Which parts will fail
    2. Demand Predictions - Part demand forecasting
    3. Evolution Predictions - How part families will evolve
    4. Emergence Predictions - What new patterns will emerge
    """

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self.failure_predictor = FailurePredictor()
        self.emergence_predictor = EmergencePredictor()
        self._all_predictions: List[Prediction] = []

    def generate_predictions(
        self,
        parts_data: List[Dict[str, Any]],
        swarm_data: Dict[str, SwarmKnowledge],
        failure_history: List[FailureRecord],
        temporal_data: Optional[Dict[str, Any]] = None,
        patterns: Optional[List[DetectedPattern]] = None,
    ) -> List[Prediction]:
        """
        Generate predictions about the future state of the parts ecosystem.

        Args:
            parts_data: Part information for prediction
            swarm_data: Swarm collective knowledge
            failure_history: Historical failure data
            temporal_data: Time series trends
            patterns: Detected patterns for context

        Returns:
            List of all predictions
        """
        predictions = []

        # 1. Failure Predictions
        if self.config.enable_failure_prediction:
            parts = self._convert_to_parts(parts_data)
            failure_predictions = self.failure_predictor.predict_failures(
                parts, failure_history, temporal_data
            )
            predictions.extend(failure_predictions)

        # 2. Demand Predictions
        if self.config.enable_demand_prediction:
            demand_predictions = self._predict_demand(swarm_data, temporal_data)
            predictions.extend(demand_predictions)

        # 3. Evolution Predictions
        if self.config.enable_evolution_prediction:
            evolution_predictions = self._predict_evolution(swarm_data, patterns)
            predictions.extend(evolution_predictions)

        # 4. Emergence Predictions
        if self.config.enable_emergence_prediction:
            emergence_predictions = self.emergence_predictor.predict_emergence(
                swarm_data, patterns
            )
            predictions.extend(emergence_predictions)

        self._all_predictions.extend(predictions)
        logger.info(f"Generated {len(predictions)} total predictions")

        return predictions

    def _convert_to_parts(self, parts_data: List[Dict[str, Any]]) -> List[Part]:
        """Convert part dictionaries to Part objects"""
        parts = []
        for data in parts_data:
            part = Part(
                upc_id=data.get("upc_id", ""),
                part_type=data.get("part_type", "unknown"),
                material=data.get("material", "unknown"),
                age_hours=data.get("age_hours", 0),
                usage_intensity=data.get("usage_intensity", 0.5),
                environment=data.get("environment", {}),
                failure_history=data.get("failure_history", []),
                consciousness_level=data.get("consciousness_level", 0),
            )
            parts.append(part)
        return parts

    def _predict_demand(
        self,
        swarm_data: Dict[str, SwarmKnowledge],
        temporal_data: Optional[Dict[str, Any]] = None,
    ) -> List[Prediction]:
        """Predict future demand for parts"""
        predictions = []

        if not temporal_data:
            return predictions

        # Analyze demand trends from temporal data
        demand_trends = temporal_data.get("demand_trends", {})

        for part_type, trend_data in demand_trends.items():
            if not trend_data:
                continue

            # Simple trend extrapolation
            growth_rate = trend_data.get("growth_rate", 0)
            current_demand = trend_data.get("current_demand", 0)

            if abs(growth_rate) > 0.1:  # 10% growth threshold
                projected_demand = current_demand * (1 + growth_rate)
                direction = "increase" if growth_rate > 0 else "decrease"

                prediction = Prediction(
                    prediction_type=PredictionType.DEMAND,
                    subject_id=part_type,
                    subject_type="part_type",
                    prediction={
                        "event": f"demand_{direction}",
                        "current_demand": current_demand,
                        "projected_demand": projected_demand,
                        "growth_rate": growth_rate,
                    },
                    probability=Decimal(str(min(abs(growth_rate) * 2, 0.95))),
                    timeline_days=self.config.prediction_horizon_days,
                    confidence=Decimal(str(0.6 + min(abs(growth_rate), 0.3))),
                )
                predictions.append(prediction)

        return predictions

    def _predict_evolution(
        self,
        swarm_data: Dict[str, SwarmKnowledge],
        patterns: Optional[List[DetectedPattern]] = None,
    ) -> List[Prediction]:
        """Predict how part families will evolve"""
        predictions = []

        if not patterns:
            return predictions

        # Look for innovation layer patterns that suggest evolution
        evolution_patterns = [
            p for p in patterns
            if p.layer.name == "INNOVATION" and "evolution" in p.pattern_type.lower()
        ]

        for pattern in evolution_patterns:
            evidence = pattern.evidence

            prediction = Prediction(
                prediction_type=PredictionType.EVOLUTION,
                subject_id=evidence.get("subject", pattern.pattern_id),
                subject_type="part_family",
                prediction={
                    "event": "evolution",
                    "trend": evidence.get("trending_value"),
                    "configuration_key": evidence.get("configuration_key"),
                    "direction": evidence.get("direction", "forward"),
                },
                probability=pattern.significance_score,
                timeline_days=self.config.prediction_horizon_days,
                confidence=pattern.confidence,
            )
            predictions.append(prediction)

        return predictions

    def get_predictions_by_type(
        self,
        prediction_type: PredictionType,
    ) -> List[Prediction]:
        """Get predictions of a specific type"""
        return [
            p for p in self._all_predictions
            if p.prediction_type == prediction_type
        ]

    def get_high_priority_predictions(
        self,
        probability_threshold: float = 0.7,
    ) -> List[Prediction]:
        """Get predictions with high probability"""
        high_priority = [
            p for p in self._all_predictions
            if float(p.probability) >= probability_threshold
        ]
        return sorted(high_priority, key=lambda p: float(p.probability), reverse=True)

    def validate_predictions(
        self,
        validation_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Validate predictions against actual outcomes"""
        validated_count = 0
        correct_count = 0

        for validation in validation_data:
            prediction_id = validation.get("prediction_id")
            actual_outcome = validation.get("outcome")

            for pred in self._all_predictions:
                if pred.id == prediction_id:
                    pred.validated = True
                    pred.validated_at = datetime.now()
                    pred.validation_result = actual_outcome
                    validated_count += 1

                    # Check if prediction was correct
                    if self._check_prediction_accuracy(pred, actual_outcome):
                        correct_count += 1
                    break

        return {
            "validated": validated_count,
            "correct": correct_count,
            "accuracy": correct_count / validated_count if validated_count > 0 else None,
        }

    def _check_prediction_accuracy(
        self,
        prediction: Prediction,
        outcome: Dict[str, Any],
    ) -> bool:
        """Check if a prediction was accurate"""
        if prediction.prediction_type == PredictionType.FAILURE:
            return outcome.get("failure_occurred", False)

        elif prediction.prediction_type == PredictionType.DEMAND:
            predicted_direction = "increase" if prediction.prediction.get("growth_rate", 0) > 0 else "decrease"
            actual_direction = outcome.get("direction")
            return predicted_direction == actual_direction

        elif prediction.prediction_type == PredictionType.EMERGENCE:
            return outcome.get("emergence_occurred", False)

        return False

    def get_prediction_metrics(self) -> Dict[str, Any]:
        """Get overall prediction metrics"""
        total = len(self._all_predictions)
        validated = [p for p in self._all_predictions if p.validated]

        by_type = {}
        for pred_type in PredictionType:
            type_preds = [p for p in self._all_predictions if p.prediction_type == pred_type]
            type_validated = [p for p in type_preds if p.validated]

            by_type[pred_type.value] = {
                "total": len(type_preds),
                "validated": len(type_validated),
                "avg_probability": (
                    sum(float(p.probability) for p in type_preds) / len(type_preds)
                    if type_preds else 0
                ),
            }

        return {
            "total_predictions": total,
            "validated_predictions": len(validated),
            "by_type": by_type,
            "prediction_horizon_days": self.config.prediction_horizon_days,
        }
