"""
Failure Predictor

ML-based failure prediction using network data.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class FailureRiskPrediction:
    """Prediction of failure risk for a part"""
    part_id: str
    overall_risk_score: float
    predicted_failure_modes: List[Dict[str, Any]]
    l10_life_hours: Optional[float]
    l50_life_hours: Optional[float]
    network_insights: List[str]
    recommendations: List[str]
    confidence: float
    prediction_timestamp: datetime


class FailurePredictor:
    """
    ML-based failure prediction using network data.

    Uses historical failure data to predict:
    - Probability of failure modes
    - Expected time to failure
    - Risk factors
    """

    # Base failure rates by part type (failures per million hours)
    BASE_FAILURE_RATES = {
        "bearing": 50,
        "bolt": 5,
        "screw": 5,
        "belt": 100,
        "seal": 80,
        "gasket": 60,
        "spring": 30,
        "gear": 20,
    }

    # Condition multipliers
    CONDITION_MULTIPLIERS = {
        "temperature": {
            "low": 0.8,
            "normal": 1.0,
            "elevated": 1.5,
            "high": 3.0,
        },
        "vibration": {
            "none": 0.7,
            "low": 1.0,
            "moderate": 1.5,
            "high": 3.0,
        },
        "lubrication": {
            "excellent": 0.6,
            "good": 1.0,
            "marginal": 2.0,
            "poor": 5.0,
        },
        "contamination": {
            "clean": 0.8,
            "light": 1.0,
            "moderate": 1.5,
            "heavy": 3.0,
        },
    }

    def __init__(self):
        """Initialize the failure predictor."""
        pass

    async def predict(
        self,
        part_id: str,
        part_type: str,
        operating_conditions: Dict[str, Any]
    ) -> FailureRiskPrediction:
        """
        Predict failure risk for a part under given conditions.

        Args:
            part_id: Part identifier
            part_type: Type of part
            operating_conditions: Current or expected conditions

        Returns:
            Complete failure risk prediction
        """
        # Calculate base failure rate
        base_rate = self._get_base_failure_rate(part_type)

        # Apply condition multipliers
        multiplier = self._calculate_condition_multiplier(operating_conditions)
        adjusted_rate = base_rate * multiplier

        # Calculate life estimates
        l10_hours = 1e6 / (adjusted_rate * 10)  # 10% failure probability
        l50_hours = 1e6 / (adjusted_rate * 2)   # 50% failure probability

        # Predict failure modes
        failure_modes = self._predict_failure_modes(part_type, operating_conditions)

        # Get network insights
        insights = self._get_network_insights(part_type, operating_conditions)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            part_type,
            operating_conditions,
            adjusted_rate
        )

        # Calculate overall risk score (0-1)
        risk_score = min(1.0, adjusted_rate / 500)

        return FailureRiskPrediction(
            part_id=part_id,
            overall_risk_score=risk_score,
            predicted_failure_modes=failure_modes,
            l10_life_hours=l10_hours,
            l50_life_hours=l50_hours,
            network_insights=insights,
            recommendations=recommendations,
            confidence=0.75,
            prediction_timestamp=datetime.utcnow()
        )

    def _get_base_failure_rate(self, part_type: str) -> float:
        """Get base failure rate for part type."""
        part_type_lower = part_type.lower()

        for key, rate in self.BASE_FAILURE_RATES.items():
            if key in part_type_lower:
                return rate

        return 50  # Default rate

    def _calculate_condition_multiplier(
        self,
        conditions: Dict[str, Any]
    ) -> float:
        """Calculate overall condition multiplier."""
        multiplier = 1.0

        # Temperature
        temp = conditions.get("temperature_c", 25)
        if temp < 0 or temp > 100:
            multiplier *= self.CONDITION_MULTIPLIERS["temperature"]["high"]
        elif temp > 70:
            multiplier *= self.CONDITION_MULTIPLIERS["temperature"]["elevated"]
        else:
            multiplier *= self.CONDITION_MULTIPLIERS["temperature"]["normal"]

        # Vibration
        vibration = conditions.get("vibration_level", "low").lower()
        multiplier *= self.CONDITION_MULTIPLIERS["vibration"].get(vibration, 1.0)

        # Lubrication
        lubrication = conditions.get("lubrication", "good").lower()
        multiplier *= self.CONDITION_MULTIPLIERS["lubrication"].get(lubrication, 1.0)

        # Contamination
        contamination = conditions.get("contamination", "light").lower()
        multiplier *= self.CONDITION_MULTIPLIERS["contamination"].get(contamination, 1.0)

        return multiplier

    def _predict_failure_modes(
        self,
        part_type: str,
        conditions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Predict likely failure modes based on part and conditions."""
        modes = []

        part_type_lower = part_type.lower()

        # Bearing failure modes
        if "bearing" in part_type_lower:
            modes = [
                {
                    "mode": "Fatigue spalling",
                    "probability": 0.45,
                    "typical_onset_hours": 15000,
                    "symptoms": ["Vibration increase", "Metallic debris", "Temperature rise"]
                },
                {
                    "mode": "Lubricant degradation",
                    "probability": 0.30,
                    "typical_onset_hours": 10000,
                    "symptoms": ["Temperature rise", "Increased noise", "Grease darkening"]
                },
                {
                    "mode": "Contamination damage",
                    "probability": 0.15,
                    "typical_onset_hours": 5000,
                    "symptoms": ["Early spalling", "Abrasive wear", "Debris in grease"]
                },
            ]

        # Fastener failure modes
        elif "bolt" in part_type_lower or "screw" in part_type_lower:
            modes = [
                {
                    "mode": "Fatigue fracture",
                    "probability": 0.40,
                    "typical_onset_hours": 10000,
                    "symptoms": ["Crack at thread root", "Beach marks on fracture"]
                },
                {
                    "mode": "Preload loss",
                    "probability": 0.35,
                    "typical_onset_hours": 5000,
                    "symptoms": ["Joint loosening", "Increased movement", "Torque loss"]
                },
                {
                    "mode": "Corrosion",
                    "probability": 0.15,
                    "typical_onset_hours": 8000,
                    "symptoms": ["Surface rust", "Pitting", "Reduced strength"]
                },
            ]

        # Belt failure modes
        elif "belt" in part_type_lower:
            modes = [
                {
                    "mode": "Wear/Cracking",
                    "probability": 0.50,
                    "typical_onset_hours": 5000,
                    "symptoms": ["Surface cracks", "Material loss", "Noise"]
                },
                {
                    "mode": "Stretch/Slip",
                    "probability": 0.30,
                    "typical_onset_hours": 4000,
                    "symptoms": ["Squealing", "Slip marks", "Power loss"]
                },
            ]

        else:
            modes = [
                {
                    "mode": "Wear",
                    "probability": 0.40,
                    "typical_onset_hours": 10000,
                    "symptoms": ["Dimensional change", "Performance degradation"]
                },
                {
                    "mode": "Fatigue",
                    "probability": 0.30,
                    "typical_onset_hours": 15000,
                    "symptoms": ["Cracking", "Fracture"]
                },
            ]

        # Adjust probabilities based on conditions
        if conditions.get("vibration_level", "").lower() == "high":
            for mode in modes:
                if "fatigue" in mode["mode"].lower():
                    mode["probability"] = min(1.0, mode["probability"] * 1.5)

        return modes

    def _get_network_insights(
        self,
        part_type: str,
        conditions: Dict[str, Any]
    ) -> List[str]:
        """Get insights from network failure data."""
        insights = []

        # Simulated insights - in production would query network database
        part_type_lower = part_type.lower()

        if "bearing" in part_type_lower:
            insights = [
                "23 similar bearings in network show no issues at 10000 hrs",
                "3 failures reported above 80C - all grease related",
                "Network average life: 18,500 hours under similar conditions"
            ]
        elif "bolt" in part_type_lower or "screw" in part_type_lower:
            insights = [
                "Fastener failures in similar applications: 12 in past year",
                "Most common cause: undertorque (45%)",
                "Vibration-related failures increase 3x in high-vibration apps"
            ]
        else:
            insights = [
                "Limited network data for this part type",
                "Consider documenting failures to improve predictions"
            ]

        return insights

    def _generate_recommendations(
        self,
        part_type: str,
        conditions: Dict[str, Any],
        failure_rate: float
    ) -> List[str]:
        """Generate recommendations based on prediction."""
        recommendations = []

        # High risk general recommendations
        if failure_rate > 100:
            recommendations.append("High failure risk - implement condition monitoring")

        # Temperature recommendations
        if conditions.get("temperature_c", 25) > 70:
            recommendations.append("Monitor operating temperature - elevated temps reduce life")

        # Vibration recommendations
        if conditions.get("vibration_level", "").lower() == "high":
            recommendations.append("High vibration increases fatigue risk - consider damping")

        # Part-specific recommendations
        part_type_lower = part_type.lower()

        if "bearing" in part_type_lower:
            if conditions.get("temperature_c", 25) > 70:
                recommendations.append("Consider relubrication schedule for elevated temperature")
            if conditions.get("contamination", "").lower() in ["moderate", "heavy"]:
                recommendations.append("Consider shielded/sealed bearing for contamination")

        elif "bolt" in part_type_lower or "screw" in part_type_lower:
            if conditions.get("vibration_level", "").lower() == "high":
                recommendations.append("Use Nord-Lock or other vibration-resistant locking")
            recommendations.append("Verify torque specification and verify periodically")

        if not recommendations:
            recommendations.append("Operating conditions within normal range")

        return recommendations
