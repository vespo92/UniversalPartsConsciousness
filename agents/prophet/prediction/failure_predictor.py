"""
Failure Predictor
Predicts which parts are likely to fail soon.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
import logging
import math

from ..types import Prediction, PredictionType, FailureRecord, Assembly


logger = logging.getLogger(__name__)


@dataclass
class Part:
    """Part data for prediction"""
    upc_id: str
    part_type: str
    material: str
    age_hours: int
    usage_intensity: float  # 0-1
    environment: Dict[str, Any]
    failure_history: List[str]
    consciousness_level: int  # 0-5


@dataclass
class PredictionConfig:
    """Configuration for failure prediction"""
    probability_threshold: float = 0.3  # Minimum probability to report
    max_predictions_per_run: int = 1000
    time_horizon_days: int = 90
    confidence_decay_factor: float = 0.95


class FailurePredictor:
    """
    Predicts which parts are likely to fail soon.

    Uses multiple factors:
    - Part age and usage history
    - Environmental conditions
    - Similar parts' failure patterns
    - Swarm collective knowledge
    """

    def __init__(self, config: Optional[PredictionConfig] = None):
        self.config = config or PredictionConfig()
        self._predictions: List[Prediction] = []
        self._failure_rates: Dict[str, float] = {}  # part_type -> rate

    def predict_failures(
        self,
        parts: List[Part],
        failure_history: List[FailureRecord],
        temporal_data: Optional[Dict[str, Any]] = None,
    ) -> List[Prediction]:
        """
        Predict which parts are likely to fail.

        Args:
            parts: Parts to analyze
            failure_history: Historical failure records
            temporal_data: Time-series data for trend analysis

        Returns:
            List of failure predictions above threshold
        """
        predictions = []

        # Build failure rate models from history
        self._build_failure_models(failure_history)

        for part in parts:
            probability = self._calculate_failure_probability(part, temporal_data)

            if probability >= self.config.probability_threshold:
                prediction = Prediction(
                    prediction_type=PredictionType.FAILURE,
                    subject_id=part.upc_id,
                    subject_type=part.part_type,
                    prediction={
                        "event": "failure",
                        "probability": probability,
                        "factors": self._get_failure_factors(part),
                    },
                    probability=Decimal(str(round(probability, 4))),
                    timeline_days=self._estimate_time_to_failure(part, probability),
                    predicted_failure_mode=self._predict_failure_mode(part),
                    prevention_actions=self._suggest_prevention(part),
                    confidence=self._calculate_prediction_confidence(part, probability),
                )
                predictions.append(prediction)

        # Sort by probability
        predictions.sort(key=lambda p: float(p.probability), reverse=True)

        # Limit results
        predictions = predictions[:self.config.max_predictions_per_run]

        self._predictions.extend(predictions)
        logger.info(f"Generated {len(predictions)} failure predictions")

        return predictions

    def _build_failure_models(
        self,
        failure_history: List[FailureRecord],
    ) -> None:
        """Build failure rate models from history"""
        from collections import defaultdict

        type_failures: Dict[str, int] = defaultdict(int)
        type_counts: Dict[str, int] = defaultdict(int)

        for failure in failure_history:
            type_failures[failure.part_type] += 1
            type_counts[failure.part_type] += 1

        # Simplified failure rates
        for part_type, failure_count in type_failures.items():
            # Assume we have 10x more parts than failures (simplified)
            estimated_population = failure_count * 10
            self._failure_rates[part_type] = failure_count / estimated_population

    def _calculate_failure_probability(
        self,
        part: Part,
        temporal_data: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Calculate failure probability for a part"""
        # Base rate from part type
        base_rate = self._failure_rates.get(part.part_type, 0.05)

        # Age factor (Weibull-like increasing hazard)
        age_factor = self._calculate_age_factor(part.age_hours)

        # Usage intensity factor
        usage_factor = 0.5 + part.usage_intensity * 0.5

        # Environmental stress factor
        env_factor = self._calculate_environmental_factor(part.environment)

        # History factor (parts that failed before are more likely to fail again)
        history_factor = 1.0 + len(part.failure_history) * 0.2

        # Combine factors
        probability = base_rate * age_factor * usage_factor * env_factor * history_factor

        # Apply temporal trend if available
        if temporal_data:
            trend_factor = temporal_data.get("failure_trend_multiplier", 1.0)
            probability *= trend_factor

        return min(probability, 0.99)

    def _calculate_age_factor(self, age_hours: int) -> float:
        """Calculate age-based failure factor using bathtub curve"""
        # Early life failures (infant mortality)
        if age_hours < 100:
            return 2.0 - (age_hours / 100)

        # Useful life (low, constant rate)
        if age_hours < 5000:
            return 1.0

        # Wear-out phase (increasing failure rate)
        wear_factor = (age_hours - 5000) / 5000
        return 1.0 + wear_factor * 2

    def _calculate_environmental_factor(
        self,
        environment: Dict[str, Any],
    ) -> float:
        """Calculate environmental stress factor"""
        factor = 1.0

        # Temperature stress
        temp = environment.get("temperature", 25)
        if temp > 80:
            factor *= 1.5
        elif temp > 60:
            factor *= 1.2
        elif temp < -10:
            factor *= 1.3

        # Humidity/moisture
        if environment.get("moisture", False) or environment.get("humidity", 0) > 80:
            factor *= 1.4

        # Vibration
        if environment.get("vibration", "low") == "high":
            factor *= 1.6
        elif environment.get("vibration") == "medium":
            factor *= 1.2

        # Corrosive environment
        if environment.get("corrosive", False):
            factor *= 1.8

        return factor

    def _get_failure_factors(self, part: Part) -> List[Dict[str, Any]]:
        """Get contributing factors to failure prediction"""
        factors = []

        if part.age_hours > 5000:
            factors.append({
                "factor": "age",
                "value": part.age_hours,
                "contribution": "high",
                "description": "Part is in wear-out phase",
            })

        if part.usage_intensity > 0.8:
            factors.append({
                "factor": "usage_intensity",
                "value": part.usage_intensity,
                "contribution": "medium",
                "description": "High usage intensity",
            })

        if part.environment.get("temperature", 25) > 60:
            factors.append({
                "factor": "temperature",
                "value": part.environment.get("temperature"),
                "contribution": "medium",
                "description": "Elevated operating temperature",
            })

        if part.failure_history:
            factors.append({
                "factor": "history",
                "value": len(part.failure_history),
                "contribution": "high",
                "description": f"Previous failure history ({len(part.failure_history)} events)",
            })

        return factors

    def _estimate_time_to_failure(
        self,
        part: Part,
        probability: float,
    ) -> int:
        """Estimate days until failure"""
        # Higher probability = sooner failure
        # Base estimate from probability
        if probability > 0.8:
            base_days = 7
        elif probability > 0.6:
            base_days = 30
        elif probability > 0.4:
            base_days = 60
        else:
            base_days = 90

        # Adjust by age (older parts fail sooner)
        age_adjustment = 1.0
        if part.age_hours > 8000:
            age_adjustment = 0.5
        elif part.age_hours > 5000:
            age_adjustment = 0.7

        return int(base_days * age_adjustment)

    def _predict_failure_mode(self, part: Part) -> str:
        """Predict the most likely failure mode"""
        env = part.environment

        # Rule-based prediction
        if env.get("corrosive", False) or env.get("humidity", 0) > 80:
            return "corrosion"
        elif env.get("vibration") == "high":
            return "fatigue"
        elif env.get("temperature", 25) > 80:
            return "thermal_degradation"
        elif part.age_hours < 100:
            return "infant_mortality"
        elif part.age_hours > 8000:
            return "wear"
        else:
            return "general_fatigue"

    def _suggest_prevention(self, part: Part) -> List[str]:
        """Suggest preventive actions"""
        actions = []

        predicted_mode = self._predict_failure_mode(part)

        if predicted_mode == "corrosion":
            actions.append("Apply protective coating or replace with corrosion-resistant variant")
            actions.append("Reduce exposure to moisture/corrosive environment")

        elif predicted_mode == "fatigue":
            actions.append("Reduce vibration exposure or reinforce mounting")
            actions.append("Consider replacement with higher fatigue-rated component")

        elif predicted_mode == "thermal_degradation":
            actions.append("Improve cooling or thermal management")
            actions.append("Consider high-temperature rated alternative")

        elif predicted_mode == "wear":
            actions.append("Schedule preventive replacement")
            actions.append("Increase lubrication frequency")

        else:
            actions.append("Schedule inspection and condition assessment")
            actions.append("Consider preventive replacement")

        return actions

    def _calculate_prediction_confidence(
        self,
        part: Part,
        probability: float,
    ) -> Decimal:
        """Calculate confidence in the prediction"""
        base_confidence = 0.5

        # More data = higher confidence
        if part.age_hours > 1000:
            base_confidence += 0.1

        if part.failure_history:
            base_confidence += 0.15

        # Higher probability predictions tend to be more confident
        if probability > 0.7:
            base_confidence += 0.1

        # Consciousness level (more evolved parts provide better data)
        base_confidence += part.consciousness_level * 0.05

        return Decimal(str(min(base_confidence, 0.95)))

    def validate_prediction(
        self,
        prediction_id: str,
        actual_outcome: Dict[str, Any],
    ) -> bool:
        """Validate a prediction against actual outcome"""
        for pred in self._predictions:
            if pred.id == prediction_id:
                pred.validated = True
                pred.validated_at = datetime.now()
                pred.validation_result = actual_outcome
                return True
        return False

    def get_prediction_accuracy(self) -> Dict[str, Any]:
        """Calculate prediction accuracy metrics"""
        validated = [p for p in self._predictions if p.validated]

        if not validated:
            return {"accuracy": None, "sample_size": 0}

        correct = sum(
            1 for p in validated
            if p.validation_result and p.validation_result.get("failure_occurred", False)
        )

        return {
            "accuracy": correct / len(validated),
            "sample_size": len(validated),
            "total_predictions": len(self._predictions),
        }
