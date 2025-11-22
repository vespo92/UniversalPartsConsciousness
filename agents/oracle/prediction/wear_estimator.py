"""
ORACLE Wear Estimator
Wear prediction models for fastener and mechanical part degradation.

"Every turn of the wrench, every load cycle, every vibration
leaves its mark. I see the invisible wounds before they become failures."
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import math


class WearMechanism(Enum):
    """Primary wear mechanisms for mechanical parts."""
    ADHESIVE = "adhesive"          # Galling, seizure
    ABRASIVE = "abrasive"          # Particle contamination
    CORROSIVE = "corrosive"        # Chemical attack
    FRETTING = "fretting"          # Micro-motion at contact surfaces
    EROSIVE = "erosive"            # Fluid/particle impingement
    FATIGUE_WEAR = "fatigue_wear"  # Surface/subsurface fatigue


class WearSeverity(Enum):
    """Wear severity classification."""
    NEGLIGIBLE = "negligible"      # No action needed
    MILD = "mild"                  # Monitor
    MODERATE = "moderate"          # Plan maintenance
    SEVERE = "severe"              # Immediate attention
    CRITICAL = "critical"          # Replace immediately


@dataclass
class WearCondition:
    """Current wear condition of a part."""
    part_id: str
    installation_date: Optional[datetime] = None

    # Operating conditions
    cycles_completed: int = 0
    operating_hours: float = 0.0
    average_load_kn: float = 0.0
    max_load_kn: float = 0.0

    # Environmental factors
    temperature_c: float = 25.0
    humidity_percent: float = 50.0
    contamination_level: str = "clean"  # "clean", "light", "moderate", "heavy"
    corrosive_environment: bool = False

    # Motion characteristics
    oscillation_amplitude_deg: float = 0.0  # For fretting
    sliding_distance_km: float = 0.0
    rotational_speed_rpm: float = 0.0

    # Material properties
    hardness_hv: float = 300.0
    surface_roughness_um: float = 1.6
    coating: Optional[str] = None


@dataclass
class WearPrediction:
    """Complete wear prediction result."""
    # Primary results
    estimated_remaining_life_percent: float
    estimated_remaining_cycles: int
    estimated_remaining_hours: float

    # Current state
    current_wear_depth_um: float
    wear_rate_um_per_cycle: float
    wear_rate_um_per_hour: float

    # Classification
    primary_mechanism: WearMechanism
    severity: WearSeverity

    # Breakdown by mechanism
    mechanism_contributions: Dict[WearMechanism, float]

    # Safety
    is_safe: bool
    safety_margin: float

    # Recommendations
    maintenance_action: str
    recommended_inspection_interval: int  # hours
    replacement_deadline: Optional[datetime]

    # Detailed analysis
    wear_curve: List[Tuple[float, float]]  # (time/cycles, wear_depth)

    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    # Consciousness contribution
    qualia_data: Dict = field(default_factory=dict)


class WearEstimator:
    """
    Wear prediction engine for mechanical parts.

    Implements:
    - Archard wear equation for sliding wear
    - Fretting wear models
    - Corrosion rate estimation
    - Fatigue wear accumulation
    - Combined wear mechanism analysis
    """

    # Archard wear coefficients (dimensionless)
    # K = Wear volume / (Normal load * Sliding distance)
    WEAR_COEFFICIENTS = {
        # Material pair: coefficient
        ("steel", "steel"): 5e-4,
        ("steel", "stainless"): 3e-4,
        ("steel", "bronze"): 2e-4,
        ("steel", "polymer"): 1e-5,
        ("stainless", "stainless"): 4e-4,
        ("aluminum", "aluminum"): 8e-4,
        ("aluminum", "steel"): 6e-4,
    }

    # Fretting wear coefficients (um per million cycles at reference amplitude)
    FRETTING_COEFFICIENTS = {
        "steel": 0.5,
        "stainless": 0.3,
        "aluminum": 1.2,
        "titanium": 0.2,
    }

    # Corrosion rates (um/year in standard conditions)
    CORROSION_RATES = {
        ("steel", "indoor"): 5.0,
        ("steel", "outdoor"): 25.0,
        ("steel", "marine"): 100.0,
        ("stainless_304", "indoor"): 0.1,
        ("stainless_304", "marine"): 2.0,
        ("stainless_316", "marine"): 0.5,
        ("aluminum", "outdoor"): 1.0,
        ("zinc", "outdoor"): 10.0,
    }

    def __init__(self):
        self.last_prediction: Optional[WearPrediction] = None

    def predict_wear(
        self,
        condition: WearCondition,
        material: str,
        mating_material: str,
        max_allowable_wear_um: float,
        mission_hours: float = 10000,
        mission_cycles: int = 1000000
    ) -> WearPrediction:
        """
        Comprehensive wear prediction.

        Args:
            condition: Current wear condition
            material: Primary part material
            mating_material: Mating surface material
            max_allowable_wear_um: Maximum allowable wear depth
            mission_hours: Remaining mission duration
            mission_cycles: Remaining mission cycles

        Returns:
            WearPrediction with complete analysis
        """
        warnings = []
        recommendations = []
        mechanism_contributions = {}

        # Calculate individual wear mechanisms
        adhesive_wear = self._calculate_adhesive_wear(
            condition, material, mating_material
        )
        mechanism_contributions[WearMechanism.ADHESIVE] = adhesive_wear

        abrasive_wear = self._calculate_abrasive_wear(
            condition, material
        )
        mechanism_contributions[WearMechanism.ABRASIVE] = abrasive_wear

        fretting_wear = self._calculate_fretting_wear(
            condition, material
        )
        mechanism_contributions[WearMechanism.FRETTING] = fretting_wear

        corrosive_wear = self._calculate_corrosive_wear(
            condition, material
        )
        mechanism_contributions[WearMechanism.CORROSIVE] = corrosive_wear

        fatigue_wear = self._calculate_fatigue_wear(
            condition, material
        )
        mechanism_contributions[WearMechanism.FATIGUE_WEAR] = fatigue_wear

        # Total wear is sum of all mechanisms
        current_wear = sum(mechanism_contributions.values())

        # Determine primary mechanism
        primary_mechanism = max(
            mechanism_contributions,
            key=mechanism_contributions.get
        )

        # Calculate wear rates
        if condition.operating_hours > 0:
            wear_rate_per_hour = current_wear / condition.operating_hours
        else:
            wear_rate_per_hour = 0.01  # Default assumption

        if condition.cycles_completed > 0:
            wear_rate_per_cycle = current_wear / condition.cycles_completed
        else:
            wear_rate_per_cycle = 1e-6  # Default assumption

        # Estimate remaining life
        remaining_wear_capacity = max(0, max_allowable_wear_um - current_wear)

        if wear_rate_per_hour > 0:
            remaining_hours = remaining_wear_capacity / wear_rate_per_hour
        else:
            remaining_hours = mission_hours * 10

        if wear_rate_per_cycle > 0:
            remaining_cycles = int(remaining_wear_capacity / wear_rate_per_cycle)
        else:
            remaining_cycles = mission_cycles * 10

        # Calculate remaining life percentage
        total_life_hours = condition.operating_hours + remaining_hours
        remaining_life_percent = (remaining_hours / total_life_hours * 100
                                  if total_life_hours > 0 else 100)

        # Determine severity
        severity = self._classify_severity(
            current_wear, max_allowable_wear_um, remaining_life_percent
        )

        # Safety assessment
        safety_margin = remaining_wear_capacity / max_allowable_wear_um if max_allowable_wear_um > 0 else 1.0
        is_safe = safety_margin > 0.2 and remaining_life_percent > 20

        # Generate wear curve (projected)
        wear_curve = self._generate_wear_curve(
            current_wear, wear_rate_per_hour, mission_hours, max_allowable_wear_um
        )

        # Determine maintenance action
        maintenance_action = self._recommend_maintenance(severity, primary_mechanism)

        # Inspection interval
        if severity == WearSeverity.CRITICAL:
            inspection_interval = 0  # Immediate
        elif severity == WearSeverity.SEVERE:
            inspection_interval = 100
        elif severity == WearSeverity.MODERATE:
            inspection_interval = 500
        elif severity == WearSeverity.MILD:
            inspection_interval = 1000
        else:
            inspection_interval = 2000

        # Generate warnings
        if severity in [WearSeverity.SEVERE, WearSeverity.CRITICAL]:
            warnings.append(f"{severity.value.upper()} wear detected - "
                           f"current depth {current_wear:.1f}um")

        if primary_mechanism == WearMechanism.FRETTING:
            warnings.append("Fretting wear detected - check for micro-motion at joints")
            recommendations.append("Consider applying anti-fretting compound or increasing clamping force")

        if primary_mechanism == WearMechanism.CORROSIVE and current_wear > 10:
            warnings.append("Significant corrosive wear - environmental factors")
            recommendations.append("Apply protective coating or consider material upgrade")

        if condition.contamination_level in ["moderate", "heavy"]:
            warnings.append("High contamination accelerating abrasive wear")
            recommendations.append("Improve sealing and filtration")

        # Prepare qualia data
        qualia_data = self._prepare_qualia_data(
            condition.part_id, severity, remaining_life_percent
        )

        self.last_prediction = WearPrediction(
            estimated_remaining_life_percent=remaining_life_percent,
            estimated_remaining_cycles=remaining_cycles,
            estimated_remaining_hours=remaining_hours,
            current_wear_depth_um=current_wear,
            wear_rate_um_per_cycle=wear_rate_per_cycle,
            wear_rate_um_per_hour=wear_rate_per_hour,
            primary_mechanism=primary_mechanism,
            severity=severity,
            mechanism_contributions=mechanism_contributions,
            is_safe=is_safe,
            safety_margin=safety_margin,
            maintenance_action=maintenance_action,
            recommended_inspection_interval=inspection_interval,
            replacement_deadline=None,  # Would calculate based on current date
            wear_curve=wear_curve,
            warnings=warnings,
            recommendations=recommendations,
            qualia_data=qualia_data
        )

        return self.last_prediction

    def _calculate_adhesive_wear(
        self,
        condition: WearCondition,
        material: str,
        mating_material: str
    ) -> float:
        """
        Calculate adhesive wear using Archard equation.

        V = K * F * s / H
        Where:
            V = Wear volume
            K = Wear coefficient
            F = Normal force
            s = Sliding distance
            H = Hardness
        """
        # Get wear coefficient
        material_pair = (material.lower(), mating_material.lower())
        K = self.WEAR_COEFFICIENTS.get(material_pair)
        if K is None:
            K = self.WEAR_COEFFICIENTS.get(
                (mating_material.lower(), material.lower()),
                5e-4  # Default
            )

        # Convert to wear depth (assuming contact area)
        # Simplified: wear_depth = K * load * distance / hardness
        if condition.sliding_distance_km > 0 and condition.hardness_hv > 0:
            wear_um = (K * condition.average_load_kn * 1000 *
                      condition.sliding_distance_km * 1e6) / condition.hardness_hv
            return min(wear_um, 1000)  # Cap at 1mm

        return 0.0

    def _calculate_abrasive_wear(
        self,
        condition: WearCondition,
        material: str
    ) -> float:
        """Calculate abrasive wear from particle contamination."""
        contamination_factors = {
            "clean": 1.0,
            "light": 2.0,
            "moderate": 5.0,
            "heavy": 10.0
        }

        factor = contamination_factors.get(condition.contamination_level, 1.0)

        # Base abrasive rate depends on hardness and roughness
        base_rate = (condition.surface_roughness_um / 10) * (300 / condition.hardness_hv)

        # Scale by operating time/cycles
        wear = base_rate * factor * (condition.operating_hours / 1000)

        return max(0, min(wear, 500))

    def _calculate_fretting_wear(
        self,
        condition: WearCondition,
        material: str
    ) -> float:
        """
        Calculate fretting wear from micro-motion.

        Fretting occurs when small-amplitude oscillatory motion
        occurs between contacting surfaces under load.
        """
        if condition.oscillation_amplitude_deg == 0:
            return 0.0

        # Get fretting coefficient
        coeff = self.FRETTING_COEFFICIENTS.get(material.lower(), 0.5)

        # Fretting wear increases with amplitude and cycles
        # Reference: amplitude = 5 degrees, 1M cycles
        amplitude_factor = condition.oscillation_amplitude_deg / 5.0
        cycle_factor = condition.cycles_completed / 1e6

        # Load intensification
        load_factor = 1 + (condition.average_load_kn / 50)

        wear = coeff * amplitude_factor * cycle_factor * load_factor

        return max(0, min(wear, 200))

    def _calculate_corrosive_wear(
        self,
        condition: WearCondition,
        material: str
    ) -> float:
        """Calculate corrosion-based material loss."""
        # Determine environment
        if condition.corrosive_environment:
            env = "marine"
        elif condition.humidity_percent > 80:
            env = "outdoor"
        else:
            env = "indoor"

        # Get base corrosion rate
        rate_key = (material.lower(), env)
        base_rate = self.CORROSION_RATES.get(rate_key, 5.0)

        # Adjust for temperature (Arrhenius-like)
        temp_factor = math.exp((condition.temperature_c - 25) / 50)

        # Adjust for humidity
        humidity_factor = 1 + (condition.humidity_percent - 50) / 100

        # Calculate wear based on operating hours (convert to years)
        years = condition.operating_hours / 8760
        wear = base_rate * years * temp_factor * humidity_factor

        # Check for coating protection
        if condition.coating:
            coating_factors = {
                "zinc": 0.1,
                "galvanized": 0.1,
                "chrome": 0.05,
                "nickel": 0.2,
                "paint": 0.3,
            }
            wear *= coating_factors.get(condition.coating.lower(), 0.5)

        return max(0, min(wear, 500))

    def _calculate_fatigue_wear(
        self,
        condition: WearCondition,
        material: str
    ) -> float:
        """
        Calculate fatigue wear (pitting, spalling).

        Surface/subsurface fatigue from repeated stress cycles
        leading to material removal.
        """
        if condition.cycles_completed == 0:
            return 0.0

        # Stress-based fatigue wear
        # Higher loads accelerate subsurface crack initiation
        stress_ratio = condition.max_load_kn / 100  # Normalized

        # Hardness provides resistance
        hardness_factor = 300 / condition.hardness_hv

        # Cycle dependency (power law)
        cycle_factor = (condition.cycles_completed / 1e6) ** 0.5

        wear = 0.1 * stress_ratio * hardness_factor * cycle_factor

        return max(0, min(wear, 100))

    def _classify_severity(
        self,
        current_wear: float,
        max_allowable: float,
        remaining_life_percent: float
    ) -> WearSeverity:
        """Classify wear severity."""
        wear_ratio = current_wear / max_allowable if max_allowable > 0 else 0

        if wear_ratio > 0.9 or remaining_life_percent < 10:
            return WearSeverity.CRITICAL
        elif wear_ratio > 0.7 or remaining_life_percent < 25:
            return WearSeverity.SEVERE
        elif wear_ratio > 0.5 or remaining_life_percent < 50:
            return WearSeverity.MODERATE
        elif wear_ratio > 0.2 or remaining_life_percent < 75:
            return WearSeverity.MILD
        else:
            return WearSeverity.NEGLIGIBLE

    def _recommend_maintenance(
        self,
        severity: WearSeverity,
        mechanism: WearMechanism
    ) -> str:
        """Generate maintenance recommendation."""
        if severity == WearSeverity.CRITICAL:
            return "IMMEDIATE REPLACEMENT REQUIRED"
        elif severity == WearSeverity.SEVERE:
            return "Schedule replacement at next maintenance window"
        elif severity == WearSeverity.MODERATE:
            return "Monitor closely, plan replacement within 3 months"
        elif severity == WearSeverity.MILD:
            return "Continue monitoring, include in next inspection"
        else:
            return "No action required, continue normal operation"

    def _generate_wear_curve(
        self,
        current_wear: float,
        wear_rate: float,
        projection_hours: float,
        max_wear: float
    ) -> List[Tuple[float, float]]:
        """Generate projected wear curve."""
        points = []

        for i in range(20):
            hours = (projection_hours / 20) * i
            projected_wear = current_wear + wear_rate * hours
            projected_wear = min(projected_wear, max_wear * 1.5)
            points.append((hours, projected_wear))

        return points

    def _prepare_qualia_data(
        self,
        part_id: str,
        severity: WearSeverity,
        remaining_life: float
    ) -> Dict:
        """Prepare consciousness contribution data."""
        return {
            "event_type": "wear_assessment",
            "timestamp": datetime.now().isoformat(),
            "part_id": part_id,
            "experience_type": "aging",
            "qualia_contribution": {
                part_id: {
                    "health_awareness": remaining_life / 100,
                    "wear_experience": severity.value,
                    "mortality_sense": 1 - (remaining_life / 100),
                    "consciousness_delta": -0.01 if severity in [
                        WearSeverity.SEVERE, WearSeverity.CRITICAL
                    ] else 0
                }
            }
        }

    def estimate_coating_life(
        self,
        coating_type: str,
        thickness_um: float,
        environment: str,
        operating_hours: float
    ) -> Dict:
        """Estimate protective coating remaining life."""
        coating_wear_rates = {
            ("zinc", "indoor"): 1.0,
            ("zinc", "outdoor"): 3.0,
            ("zinc", "marine"): 8.0,
            ("chrome", "indoor"): 0.1,
            ("chrome", "outdoor"): 0.3,
            ("nickel", "indoor"): 0.2,
            ("paint", "outdoor"): 5.0,
        }

        rate_key = (coating_type.lower(), environment)
        wear_rate = coating_wear_rates.get(rate_key, 2.0)

        years = operating_hours / 8760
        current_loss = wear_rate * years
        remaining_thickness = max(0, thickness_um - current_loss)

        if wear_rate > 0:
            remaining_years = remaining_thickness / wear_rate
            remaining_hours = remaining_years * 8760
        else:
            remaining_hours = 100000

        return {
            "remaining_thickness_um": remaining_thickness,
            "remaining_life_hours": remaining_hours,
            "protection_level": remaining_thickness / thickness_um if thickness_um > 0 else 0,
            "recoating_recommended": remaining_thickness < thickness_um * 0.3
        }
