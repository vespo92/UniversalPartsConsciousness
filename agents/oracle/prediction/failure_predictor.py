"""
ORACLE Failure Predictor
Probabilistic failure estimation for fasteners and joints.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


class FailureMode(Enum):
    """Potential failure modes for fasteners."""
    TENSILE_FRACTURE = "tensile_fracture"
    SHEAR_FRACTURE = "shear_fracture"
    THREAD_STRIPPING_EXT = "thread_stripping_external"
    THREAD_STRIPPING_INT = "thread_stripping_internal"
    FATIGUE_FAILURE = "fatigue_failure"
    STRESS_CORROSION = "stress_corrosion_cracking"
    HYDROGEN_EMBRITTLEMENT = "hydrogen_embrittlement"
    LOOSENING = "loosening"
    BEARING_FAILURE = "bearing_failure"
    GALVANIC_CORROSION = "galvanic_corrosion"
    CREEP = "creep"


class RiskLevel(Enum):
    """Risk level classification."""
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FailurePrediction:
    """Complete failure prediction result."""
    overall_probability: float  # 0.0 to 1.0
    risk_level: RiskLevel
    dominant_mode: FailureMode
    expected_life_cycles: Optional[int]

    # Per-mode analysis
    mode_probabilities: Dict[FailureMode, float]
    mode_risks: Dict[FailureMode, RiskLevel]

    # Recommendations
    critical_factors: List[str]
    mitigation_actions: List[str]
    monitoring_recommendations: List[str]

    # Confidence
    confidence: float
    data_quality: str  # "high", "medium", "low"


@dataclass
class JointCondition:
    """Current condition of a fastened joint."""
    fastener_grade: str
    diameter_mm: float
    engagement_mm: float
    preload_kn: float
    applied_load_kn: float
    load_type: str  # "static", "cyclic", "impact"

    # Material conditions
    base_material: str
    environment: str
    temperature_c: float

    # Usage history
    cycles_to_date: int = 0
    years_in_service: float = 0.0
    retorque_count: int = 0

    # Observed conditions
    corrosion_observed: bool = False
    loosening_observed: bool = False
    visible_damage: bool = False


class FailurePredictor:
    """
    Probabilistic failure prediction engine.

    Analyzes multiple failure modes and estimates:
    - Probability of failure
    - Dominant failure mode
    - Expected remaining life
    - Risk level and mitigation
    """

    # Base failure rates per million hours (industry data)
    BASE_FAILURE_RATES = {
        FailureMode.TENSILE_FRACTURE: 0.1,
        FailureMode.SHEAR_FRACTURE: 0.05,
        FailureMode.THREAD_STRIPPING_EXT: 0.15,
        FailureMode.THREAD_STRIPPING_INT: 0.2,
        FailureMode.FATIGUE_FAILURE: 0.5,
        FailureMode.STRESS_CORROSION: 0.3,
        FailureMode.HYDROGEN_EMBRITTLEMENT: 0.1,
        FailureMode.LOOSENING: 1.0,
        FailureMode.BEARING_FAILURE: 0.2,
        FailureMode.GALVANIC_CORROSION: 0.4,
        FailureMode.CREEP: 0.05,
    }

    # Environment multipliers
    ENVIRONMENT_FACTORS = {
        "indoor": 1.0,
        "outdoor": 2.0,
        "marine": 5.0,
        "chemical": 4.0,
        "high_vibration": 3.0,
        "high_temperature": 2.5,
        "cryogenic": 2.0,
    }

    # Grade strength factors (higher grade = lower static failure rate)
    GRADE_FACTORS = {
        "4.6": 1.5,
        "8.8": 1.0,
        "10.9": 0.8,
        "12.9": 0.7,
        "A2-70": 1.1,
        "A4-80": 0.9,
    }

    def __init__(self):
        pass

    def predict_failure(
        self,
        condition: JointCondition,
        mission_hours: float = 10000,
        confidence_level: float = 0.95
    ) -> FailurePrediction:
        """
        Generate comprehensive failure prediction.

        Args:
            condition: Current joint condition
            mission_hours: Planned mission duration in hours
            confidence_level: Desired confidence level for predictions

        Returns:
            FailurePrediction with complete analysis
        """
        mode_probabilities = {}
        mode_risks = {}

        # Calculate probability for each failure mode
        for mode in FailureMode:
            prob = self._calculate_mode_probability(
                mode, condition, mission_hours
            )
            mode_probabilities[mode] = prob
            mode_risks[mode] = self._classify_risk(prob)

        # Overall probability (at least one failure)
        survival_prob = 1.0
        for prob in mode_probabilities.values():
            survival_prob *= (1.0 - prob)
        overall_prob = 1.0 - survival_prob

        # Dominant mode
        dominant = max(mode_probabilities, key=mode_probabilities.get)

        # Overall risk level
        overall_risk = self._classify_risk(overall_prob)

        # Expected life
        expected_life = self._estimate_life(condition, mode_probabilities)

        # Critical factors
        critical_factors = self._identify_critical_factors(condition, mode_probabilities)

        # Mitigation actions
        mitigation = self._recommend_mitigation(dominant, condition, mode_probabilities)

        # Monitoring recommendations
        monitoring = self._recommend_monitoring(dominant, condition)

        # Data quality assessment
        data_quality = self._assess_data_quality(condition)

        return FailurePrediction(
            overall_probability=overall_prob,
            risk_level=overall_risk,
            dominant_mode=dominant,
            expected_life_cycles=expected_life,
            mode_probabilities=mode_probabilities,
            mode_risks=mode_risks,
            critical_factors=critical_factors,
            mitigation_actions=mitigation,
            monitoring_recommendations=monitoring,
            confidence=confidence_level,
            data_quality=data_quality
        )

    def _calculate_mode_probability(
        self,
        mode: FailureMode,
        condition: JointCondition,
        mission_hours: float
    ) -> float:
        """Calculate failure probability for a specific mode."""
        # Base failure rate
        base_rate = self.BASE_FAILURE_RATES.get(mode, 0.1)

        # Apply modifiers
        rate = base_rate

        # Environment factor
        env_factor = self.ENVIRONMENT_FACTORS.get(condition.environment, 1.0)
        rate *= env_factor

        # Grade factor (for strength-related modes)
        if mode in [FailureMode.TENSILE_FRACTURE, FailureMode.SHEAR_FRACTURE]:
            grade_factor = self.GRADE_FACTORS.get(condition.fastener_grade, 1.0)
            rate *= grade_factor

        # Load utilization factor
        utilization = self._calculate_utilization(condition)
        if utilization > 0.8:
            rate *= (1 + (utilization - 0.8) * 5)  # Steep increase above 80%
        elif utilization > 0.6:
            rate *= (1 + (utilization - 0.6) * 2)

        # Specific mode factors
        if mode == FailureMode.FATIGUE_FAILURE:
            if condition.load_type == "cyclic":
                rate *= 5.0
            elif condition.load_type == "impact":
                rate *= 8.0

        elif mode == FailureMode.LOOSENING:
            if condition.load_type != "static":
                rate *= 3.0
            if condition.loosening_observed:
                rate *= 10.0

        elif mode == FailureMode.GALVANIC_CORROSION:
            if condition.corrosion_observed:
                rate *= 5.0

        elif mode == FailureMode.THREAD_STRIPPING_INT:
            # Lower engagement increases stripping risk
            engagement_ratio = condition.engagement_mm / condition.diameter_mm
            if engagement_ratio < 1.0:
                rate *= (2.0 - engagement_ratio)

        elif mode == FailureMode.HYDROGEN_EMBRITTLEMENT:
            # High-strength steels more susceptible
            if condition.fastener_grade in ["10.9", "12.9"]:
                rate *= 2.0

        elif mode == FailureMode.CREEP:
            # Temperature dependent
            if condition.temperature_c > 200:
                rate *= (1 + (condition.temperature_c - 200) / 100)

        # Age factor
        age_factor = 1 + condition.years_in_service * 0.1
        rate *= age_factor

        # Convert rate to probability using exponential model
        # P = 1 - exp(-λt) where λ is failure rate per hour
        lambda_per_hour = rate / 1e6  # Convert from per million hours
        probability = 1 - math.exp(-lambda_per_hour * mission_hours)

        return min(probability, 0.999)  # Cap at 99.9%

    def _calculate_utilization(self, condition: JointCondition) -> float:
        """Calculate load utilization factor."""
        # Simplified - would use actual proof load from database
        proof_loads = {
            "4.6": 3.0, "8.8": 8.0, "10.9": 11.0, "12.9": 13.0,
            "A2-70": 7.0, "A4-80": 8.0
        }

        # Approximate proof load for M5 (scale by diameter squared)
        base_proof = proof_loads.get(condition.fastener_grade, 8.0)
        proof_load = base_proof * (condition.diameter_mm / 5.0) ** 2

        if proof_load == 0:
            return 0.5

        return min(condition.applied_load_kn / proof_load, 1.5)

    def _classify_risk(self, probability: float) -> RiskLevel:
        """Classify risk level from probability."""
        if probability < 0.001:
            return RiskLevel.NEGLIGIBLE
        elif probability < 0.01:
            return RiskLevel.LOW
        elif probability < 0.1:
            return RiskLevel.MODERATE
        elif probability < 0.5:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL

    def _estimate_life(
        self,
        condition: JointCondition,
        mode_probs: Dict[FailureMode, float]
    ) -> Optional[int]:
        """Estimate remaining life in cycles."""
        if condition.load_type == "static":
            return None  # Not applicable for static loads

        # Use fatigue probability as primary indicator
        fatigue_prob = mode_probs.get(FailureMode.FATIGUE_FAILURE, 0.1)

        if fatigue_prob < 0.01:
            return 10_000_000  # Essentially infinite
        elif fatigue_prob < 0.1:
            return 1_000_000
        elif fatigue_prob < 0.3:
            return 100_000
        elif fatigue_prob < 0.5:
            return 10_000
        else:
            return 1_000

    def _identify_critical_factors(
        self,
        condition: JointCondition,
        mode_probs: Dict[FailureMode, float]
    ) -> List[str]:
        """Identify critical factors contributing to failure risk."""
        factors = []

        utilization = self._calculate_utilization(condition)
        if utilization > 0.8:
            factors.append(f"High load utilization: {utilization*100:.0f}%")

        if condition.environment in ["marine", "chemical"]:
            factors.append(f"Aggressive environment: {condition.environment}")

        if condition.load_type == "cyclic":
            factors.append("Cyclic loading increases fatigue risk")

        engagement_ratio = condition.engagement_mm / condition.diameter_mm
        if engagement_ratio < 1.0:
            factors.append(f"Low engagement ratio: {engagement_ratio:.2f}D")

        if condition.corrosion_observed:
            factors.append("Corrosion observed - accelerated degradation")

        if condition.loosening_observed:
            factors.append("Loosening observed - immediate attention required")

        if condition.temperature_c > 150:
            factors.append(f"Elevated temperature: {condition.temperature_c}°C")

        return factors

    def _recommend_mitigation(
        self,
        dominant: FailureMode,
        condition: JointCondition,
        mode_probs: Dict[FailureMode, float]
    ) -> List[str]:
        """Recommend mitigation actions."""
        actions = []

        if dominant == FailureMode.FATIGUE_FAILURE:
            actions.append("Consider higher fatigue-rated fastener (rolled threads)")
            actions.append("Review preload - optimal preload reduces fatigue stress amplitude")
            actions.append("Add vibration damping if applicable")

        elif dominant == FailureMode.LOOSENING:
            actions.append("Apply thread-locking compound (Loctite)")
            actions.append("Use locking fastener (nyloc, prevailing torque)")
            actions.append("Verify correct preload with torque wrench")

        elif dominant in [FailureMode.THREAD_STRIPPING_EXT, FailureMode.THREAD_STRIPPING_INT]:
            actions.append("Increase thread engagement length")
            actions.append("Consider helicoil insert for internal threads")
            actions.append("Reduce applied load or use larger fastener")

        elif dominant == FailureMode.GALVANIC_CORROSION:
            actions.append("Install isolation washer")
            actions.append("Apply barrier coating")
            actions.append("Consider compatible material pairing")

        elif dominant == FailureMode.STRESS_CORROSION:
            actions.append("Reduce preload to < 70% of proof load")
            actions.append("Select stress corrosion resistant material")
            actions.append("Apply protective coating")

        elif dominant == FailureMode.HYDROGEN_EMBRITTLEMENT:
            actions.append("Avoid cadmium plating on high-strength fasteners")
            actions.append("Use lower-strength alternative if load permits")
            actions.append("Bake after plating to outgas hydrogen")

        # General recommendations based on risk
        overall_prob = sum(mode_probs.values())
        if overall_prob > 0.1:
            actions.append("Implement regular inspection schedule")
            actions.append("Consider redundant fastening")

        return actions

    def _recommend_monitoring(
        self,
        dominant: FailureMode,
        condition: JointCondition
    ) -> List[str]:
        """Recommend monitoring actions."""
        monitoring = []

        if dominant == FailureMode.FATIGUE_FAILURE:
            monitoring.append("Periodic dye penetrant inspection for cracks")
            monitoring.append("Ultrasonic inspection at critical intervals")

        elif dominant == FailureMode.LOOSENING:
            monitoring.append("Regular torque verification checks")
            monitoring.append("Mark fastener and base for visual loosening detection")

        elif dominant in [FailureMode.GALVANIC_CORROSION, FailureMode.STRESS_CORROSION]:
            monitoring.append("Visual inspection for corrosion products")
            monitoring.append("Measure corrosion rate with coupons")

        # Age-based recommendations
        if condition.years_in_service > 5:
            monitoring.append("Consider replacement based on age")

        if condition.cycles_to_date > 100000:
            monitoring.append("Fatigue life may be approaching limit")

        return monitoring

    def _assess_data_quality(self, condition: JointCondition) -> str:
        """Assess quality of input data."""
        score = 3  # Start with medium

        # Good indicators
        if condition.fastener_grade:
            score += 1
        if condition.preload_kn > 0:
            score += 1
        if condition.cycles_to_date > 0:
            score += 1

        # Poor indicators
        if condition.applied_load_kn == 0:
            score -= 1
        if condition.engagement_mm == 0:
            score -= 1

        if score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
