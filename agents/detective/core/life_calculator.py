"""
Life Expectancy Calculator

Calculates expected service life for parts under given conditions.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import math


@dataclass
class LifeExpectancy:
    """Expected life calculation result"""
    l10_hours: Optional[float]  # 10% failure probability
    l50_hours: Optional[float]  # 50% failure probability (median)
    limiting_factor: str
    temperature_factor: float
    load_factor: float
    reliability_at_target: float
    recommendations: List[str]
    calculation_method: str


class LifeCalculator:
    """
    Calculates expected service life for mechanical components.

    Methods used:
    - S-N curves for fatigue life
    - Miner's rule for variable amplitude loading
    - Arrhenius equation for temperature effects
    - Paris law for crack growth
    - Bearing L10/L50 calculations
    """

    # Standard bearing life exponent
    BEARING_LIFE_EXPONENT = 3.0  # Ball bearings
    BEARING_LIFE_EXPONENT_ROLLER = 10/3  # Roller bearings

    # Temperature adjustment factors (normalized to 20C)
    TEMP_FACTORS = {
        20: 1.0,
        40: 0.95,
        60: 0.85,
        80: 0.70,
        100: 0.50,
        120: 0.30,
    }

    # Standard S-N curve parameters (steel, normalized)
    SN_CURVE_PARAMS = {
        "steel_unnotched": {"m": 8, "C": 1e24, "endurance_limit": 0.4},
        "steel_notched": {"m": 5, "C": 1e18, "endurance_limit": 0.25},
        "aluminum": {"m": 7, "C": 1e20, "endurance_limit": None},  # No true endurance limit
    }

    def __init__(self):
        """Initialize the life calculator."""
        pass

    async def calculate_bearing_life(
        self,
        bearing_type: str,
        dynamic_load_rating_kn: float,
        applied_load_kn: float,
        speed_rpm: float,
        temperature_c: float = 20,
        lubrication_factor: float = 1.0,
        contamination_factor: float = 1.0
    ) -> LifeExpectancy:
        """
        Calculate bearing life using ISO 281 methodology.

        Args:
            bearing_type: Type of bearing (ball, roller)
            dynamic_load_rating_kn: Catalog dynamic load rating C (kN)
            applied_load_kn: Applied equivalent dynamic load P (kN)
            speed_rpm: Rotational speed (rpm)
            temperature_c: Operating temperature (C)
            lubrication_factor: Lubrication quality factor (0.1-4.0)
            contamination_factor: Contamination factor (0.1-1.0)

        Returns:
            Life expectancy calculation
        """
        # Select life exponent
        exponent = (self.BEARING_LIFE_EXPONENT if "ball" in bearing_type.lower()
                   else self.BEARING_LIFE_EXPONENT_ROLLER)

        # Basic L10 life in millions of revolutions
        if applied_load_kn > 0:
            l10_rev_millions = (dynamic_load_rating_kn / applied_load_kn) ** exponent
        else:
            l10_rev_millions = float('inf')

        # Convert to hours
        if speed_rpm > 0:
            l10_hours = (l10_rev_millions * 1e6) / (speed_rpm * 60)
        else:
            l10_hours = float('inf')

        # Apply adjustment factors
        temp_factor = self._get_temperature_factor(temperature_c)
        adjusted_l10 = l10_hours * lubrication_factor * contamination_factor * temp_factor

        # L50 is approximately 5x L10 for bearings
        l50_hours = adjusted_l10 * 5

        # Determine limiting factor
        limiting_factors = []
        if temp_factor < 0.8:
            limiting_factors.append("Temperature")
        if lubrication_factor < 0.5:
            limiting_factors.append("Lubrication")
        if contamination_factor < 0.5:
            limiting_factors.append("Contamination")
        if not limiting_factors:
            limiting_factors.append("Fatigue")

        # Generate recommendations
        recommendations = []
        if temperature_c > 70:
            recommendations.append(f"Operating temperature ({temperature_c}C) reduces grease life")
        if lubrication_factor < 1.0:
            recommendations.append("Consider improved lubrication")
        if contamination_factor < 1.0:
            recommendations.append("Consider sealed or shielded bearing")
        if adjusted_l10 < 10000:
            recommendations.append("Consider larger bearing or reduced load")

        return LifeExpectancy(
            l10_hours=adjusted_l10,
            l50_hours=l50_hours,
            limiting_factor=", ".join(limiting_factors),
            temperature_factor=temp_factor,
            load_factor=1.0 / (applied_load_kn / dynamic_load_rating_kn) if dynamic_load_rating_kn > 0 else 1.0,
            reliability_at_target=0.9,  # L10 = 90% reliability
            recommendations=recommendations,
            calculation_method="ISO 281 Basic Rating Life"
        )

    async def calculate_fatigue_life(
        self,
        material: str,
        stress_amplitude_mpa: float,
        ultimate_strength_mpa: float,
        stress_concentration_factor: float = 1.0,
        surface_factor: float = 1.0,
        size_factor: float = 1.0,
        reliability_factor: float = 1.0,
        temperature_c: float = 20
    ) -> LifeExpectancy:
        """
        Calculate fatigue life using S-N curve approach.

        Args:
            material: Material type (steel_unnotched, steel_notched, aluminum)
            stress_amplitude_mpa: Stress amplitude (MPa)
            ultimate_strength_mpa: Material ultimate tensile strength (MPa)
            stress_concentration_factor: Kt (geometric factor)
            surface_factor: Ka (surface finish factor)
            size_factor: Kb (size factor)
            reliability_factor: Kc (reliability factor)
            temperature_c: Operating temperature (C)

        Returns:
            Life expectancy calculation
        """
        # Get S-N curve parameters
        params = self.SN_CURVE_PARAMS.get(material, self.SN_CURVE_PARAMS["steel_notched"])

        # Calculate endurance limit (Se)
        if params["endurance_limit"]:
            se_prime = params["endurance_limit"] * ultimate_strength_mpa
        else:
            se_prime = 0.4 * ultimate_strength_mpa  # Estimate for materials without limit

        # Apply Marin factors
        se = se_prime * surface_factor * size_factor * reliability_factor

        # Apply stress concentration
        effective_stress = stress_amplitude_mpa * stress_concentration_factor

        # Check if below endurance limit
        if effective_stress < se and params["endurance_limit"] is not None:
            return LifeExpectancy(
                l10_hours=float('inf'),
                l50_hours=float('inf'),
                limiting_factor="Below endurance limit",
                temperature_factor=1.0,
                load_factor=se / effective_stress,
                reliability_at_target=0.99,
                recommendations=["Stress below endurance limit - infinite life predicted"],
                calculation_method="S-N Curve (Below Endurance Limit)"
            )

        # Calculate cycles to failure using Basquin equation
        # N = C / S^m where S is stress amplitude
        m = params["m"]
        C = params["C"]

        if effective_stress > 0:
            cycles_to_failure = C / (effective_stress ** m)
        else:
            cycles_to_failure = float('inf')

        # Apply temperature factor
        temp_factor = self._get_temperature_factor(temperature_c)
        adjusted_cycles = cycles_to_failure * temp_factor

        # Convert cycles to hours (assume 1 Hz = 3600 cycles/hour as baseline)
        l10_hours = adjusted_cycles / 3600  # This would need actual frequency

        # Generate recommendations
        recommendations = []
        if stress_concentration_factor > 2.0:
            recommendations.append(f"High stress concentration (Kt={stress_concentration_factor}) - consider redesign")
        if effective_stress > 0.8 * ultimate_strength_mpa:
            recommendations.append("Stress approaching ultimate strength - risk of static failure")
        if surface_factor < 0.7:
            recommendations.append("Poor surface finish reducing fatigue life - consider polishing")

        return LifeExpectancy(
            l10_hours=l10_hours,
            l50_hours=l10_hours * 2,  # Approximate
            limiting_factor="Fatigue",
            temperature_factor=temp_factor,
            load_factor=se / effective_stress if effective_stress > 0 else float('inf'),
            reliability_at_target=0.9,
            recommendations=recommendations,
            calculation_method=f"S-N Curve ({material})"
        )

    async def calculate_remaining_life(
        self,
        original_life_hours: float,
        current_hours: float,
        condition_factor: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculate remaining useful life.

        Args:
            original_life_hours: Originally calculated life
            current_hours: Current service hours
            condition_factor: Adjustment based on current condition (0.5-1.5)

        Returns:
            Remaining life estimate
        """
        consumed_fraction = current_hours / original_life_hours
        remaining_nominal = original_life_hours - current_hours

        # Adjust based on condition
        remaining_adjusted = remaining_nominal * condition_factor

        # Calculate reliability
        # Using simple linear degradation model
        reliability = max(0, 1 - consumed_fraction)

        return {
            "remaining_hours": max(0, remaining_adjusted),
            "consumed_fraction": min(1.0, consumed_fraction),
            "reliability": reliability,
            "condition_adjustment": condition_factor,
            "recommendation": self._get_remaining_life_recommendation(
                consumed_fraction, condition_factor
            )
        }

    def _get_temperature_factor(self, temperature_c: float) -> float:
        """Get temperature adjustment factor."""
        # Interpolate from table
        temps = sorted(self.TEMP_FACTORS.keys())

        if temperature_c <= temps[0]:
            return self.TEMP_FACTORS[temps[0]]
        if temperature_c >= temps[-1]:
            return self.TEMP_FACTORS[temps[-1]]

        # Linear interpolation
        for i in range(len(temps) - 1):
            if temps[i] <= temperature_c <= temps[i+1]:
                t1, t2 = temps[i], temps[i+1]
                f1, f2 = self.TEMP_FACTORS[t1], self.TEMP_FACTORS[t2]
                return f1 + (f2 - f1) * (temperature_c - t1) / (t2 - t1)

        return 1.0

    def _get_remaining_life_recommendation(
        self,
        consumed_fraction: float,
        condition_factor: float
    ) -> str:
        """Generate recommendation based on remaining life."""
        if consumed_fraction < 0.5:
            return "Component in good condition, continue monitoring"
        elif consumed_fraction < 0.8:
            return "Plan replacement at next convenient opportunity"
        elif consumed_fraction < 1.0:
            if condition_factor < 1.0:
                return "URGENT: Replace immediately, condition degraded"
            return "Schedule replacement soon"
        else:
            return "OVERDUE: Replace immediately"
