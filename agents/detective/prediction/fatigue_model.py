"""
Fatigue Life Model

Physics-based fatigue life prediction.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import math


@dataclass
class FatigueLifeResult:
    """Result of fatigue life calculation"""
    cycles_to_failure: float
    hours_to_failure: float
    safety_factor: float
    limiting_factor: str
    confidence: float
    calculation_method: str


class FatigueModel:
    """
    Physics-based fatigue life prediction models.

    Implements:
    - Basquin equation (S-N curve)
    - Miner's rule (cumulative damage)
    - Goodman diagram (mean stress correction)
    - Stress concentration effects
    """

    # Material fatigue properties (endurance limit as fraction of UTS)
    MATERIAL_PROPERTIES = {
        "steel": {
            "endurance_ratio": 0.50,  # Se'/Sut for steel
            "exponent": -0.087,        # Basquin exponent b
            "has_endurance_limit": True,
            "knee_cycles": 1e6,        # Cycles to endurance limit
        },
        "aluminum": {
            "endurance_ratio": 0.40,
            "exponent": -0.12,
            "has_endurance_limit": False,  # No true endurance limit
            "knee_cycles": 5e8,
        },
        "titanium": {
            "endurance_ratio": 0.45,
            "exponent": -0.095,
            "has_endurance_limit": True,
            "knee_cycles": 1e7,
        },
    }

    # Surface finish factors (Ka)
    SURFACE_FACTORS = {
        "mirror": 1.0,
        "polished": 0.95,
        "ground": 0.90,
        "machined": 0.80,
        "hot_rolled": 0.60,
        "forged": 0.50,
        "cast": 0.40,
    }

    # Size factors (Kb) - approximation
    SIZE_FACTORS = {
        "small": 1.0,      # d < 8mm
        "medium": 0.85,    # 8mm < d < 50mm
        "large": 0.75,     # d > 50mm
    }

    def __init__(self):
        """Initialize the fatigue model."""
        pass

    async def calculate_fatigue_life(
        self,
        material: str,
        ultimate_strength_mpa: float,
        yield_strength_mpa: float,
        stress_amplitude_mpa: float,
        mean_stress_mpa: float = 0,
        stress_concentration: float = 1.0,
        surface_finish: str = "machined",
        size_category: str = "medium",
        frequency_hz: float = 1.0
    ) -> FatigueLifeResult:
        """
        Calculate fatigue life using modified Goodman approach.

        Args:
            material: Material type
            ultimate_strength_mpa: Ultimate tensile strength
            yield_strength_mpa: Yield strength
            stress_amplitude_mpa: Alternating stress amplitude
            mean_stress_mpa: Mean stress (0 for fully reversed)
            stress_concentration: Kt (geometric factor)
            surface_finish: Surface finish category
            size_category: Part size category
            frequency_hz: Loading frequency for time conversion

        Returns:
            Complete fatigue life result
        """
        # Get material properties
        mat_props = self.MATERIAL_PROPERTIES.get(
            material.lower(),
            self.MATERIAL_PROPERTIES["steel"]
        )

        # Calculate endurance limit (Se')
        se_prime = mat_props["endurance_ratio"] * ultimate_strength_mpa

        # Apply Marin factors
        ka = self.SURFACE_FACTORS.get(surface_finish.lower(), 0.80)
        kb = self.SIZE_FACTORS.get(size_category.lower(), 0.85)
        kc = 1.0  # Reliability factor (assume 50% reliability for base calc)

        # Modified endurance limit
        se = se_prime * ka * kb * kc

        # Apply stress concentration (notch sensitivity)
        q = self._calculate_notch_sensitivity(ultimate_strength_mpa)
        kf = 1 + q * (stress_concentration - 1)

        # Effective stress amplitude
        effective_amplitude = stress_amplitude_mpa * kf

        # Apply Goodman mean stress correction
        if mean_stress_mpa > 0:
            # Goodman criterion: Sa/Se + Sm/Sut = 1
            # Equivalent fully-reversed amplitude
            goodman_amplitude = effective_amplitude / (1 - mean_stress_mpa / ultimate_strength_mpa)
        else:
            goodman_amplitude = effective_amplitude

        # Check if below endurance limit
        if mat_props["has_endurance_limit"] and goodman_amplitude < se:
            return FatigueLifeResult(
                cycles_to_failure=float('inf'),
                hours_to_failure=float('inf'),
                safety_factor=se / goodman_amplitude,
                limiting_factor="Below endurance limit",
                confidence=0.85,
                calculation_method="Goodman with Marin factors"
            )

        # Calculate cycles to failure using Basquin equation
        # N = (Sa/a)^(1/b) where a and b are material constants
        # Simplified: log(N) = log(C) - m*log(S)
        b = mat_props["exponent"]
        # Calculate 'a' from endurance limit at knee
        a = se / (mat_props["knee_cycles"] ** b)

        cycles = (goodman_amplitude / a) ** (1 / b)

        # Convert to hours
        hours = cycles / (frequency_hz * 3600)

        # Calculate safety factor
        # At calculated life, what stress ratio exists
        safety_factor = se / goodman_amplitude if goodman_amplitude > 0 else float('inf')

        return FatigueLifeResult(
            cycles_to_failure=cycles,
            hours_to_failure=hours,
            safety_factor=safety_factor,
            limiting_factor="Fatigue",
            confidence=0.75,
            calculation_method="Basquin with Goodman mean stress correction"
        )

    def calculate_cumulative_damage(
        self,
        load_spectrum: list[Tuple[float, int]],
        material: str,
        ultimate_strength_mpa: float
    ) -> Dict:
        """
        Calculate cumulative damage using Miner's rule.

        Args:
            load_spectrum: List of (stress_amplitude, cycles) tuples
            material: Material type
            ultimate_strength_mpa: Ultimate tensile strength

        Returns:
            Cumulative damage analysis
        """
        mat_props = self.MATERIAL_PROPERTIES.get(
            material.lower(),
            self.MATERIAL_PROPERTIES["steel"]
        )

        se = mat_props["endurance_ratio"] * ultimate_strength_mpa
        b = mat_props["exponent"]
        a = se / (mat_props["knee_cycles"] ** b)

        total_damage = 0.0
        damage_breakdown = []

        for stress_amp, cycles in load_spectrum:
            # Calculate life at this stress
            if stress_amp < se and mat_props["has_endurance_limit"]:
                nf = float('inf')
                damage = 0
            else:
                nf = (stress_amp / a) ** (1 / b)
                damage = cycles / nf

            total_damage += damage
            damage_breakdown.append({
                "stress_mpa": stress_amp,
                "cycles": cycles,
                "life_at_stress": nf,
                "damage_fraction": damage
            })

        return {
            "total_damage": total_damage,
            "remaining_life_fraction": max(0, 1 - total_damage),
            "damage_breakdown": damage_breakdown,
            "prediction": "Failure imminent" if total_damage > 0.8 else "Safe" if total_damage < 0.5 else "Monitor closely"
        }

    def _calculate_notch_sensitivity(self, sut_mpa: float) -> float:
        """
        Calculate notch sensitivity factor q.

        Based on Peterson's formula for steel.
        """
        # Neuber constant (for steel, in mm)
        a = 0.0254 * (300 / sut_mpa) ** 1.8

        # Assume notch radius of 1mm for general calculation
        r = 1.0

        q = 1 / (1 + a / r)

        return min(max(q, 0.5), 1.0)
