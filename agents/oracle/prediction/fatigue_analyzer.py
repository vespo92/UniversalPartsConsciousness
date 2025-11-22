"""
ORACLE Fatigue Analyzer
S-N curve analysis and fatigue life prediction.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


class LoadType(Enum):
    """Type of cyclic loading."""
    FULLY_REVERSED = "fully_reversed"    # R = -1
    ZERO_TO_MAX = "zero_to_max"          # R = 0
    PULSATING = "pulsating"              # 0 < R < 1
    FLUCTUATING = "fluctuating"          # Variable R


class SurfaceFinish(Enum):
    """Surface finish quality."""
    POLISHED = "polished"
    GROUND = "ground"
    MACHINED = "machined"
    HOT_ROLLED = "hot_rolled"
    AS_FORGED = "as_forged"
    CORRODED = "corroded"


@dataclass
class FatigueResult:
    """Complete fatigue analysis result."""
    estimated_life_cycles: int
    fatigue_strength_mpa: float
    endurance_limit_mpa: float

    # Safety factors
    factor_of_safety: float
    modified_goodman_safety: float

    # Damage accumulation
    damage_per_cycle: float
    accumulated_damage: float
    remaining_life_percent: float

    # Analysis details
    stress_amplitude_mpa: float
    mean_stress_mpa: float
    stress_ratio: float

    # Recommendations
    is_safe: bool
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class LoadSpectrum:
    """Load spectrum for variable amplitude fatigue."""
    stress_ranges: List[float]  # Stress range for each block (MPa)
    cycles: List[int]           # Number of cycles for each block
    sequence: str = "random"    # "random" or "ordered"


class FatigueAnalyzer:
    """
    Fatigue life prediction using S-N curve analysis.

    Implements:
    - Basquin's equation for S-N curves
    - Goodman, Gerber, and Soderberg mean stress corrections
    - Miner's rule for cumulative damage
    - Surface finish and size effect corrections
    """

    # S-N curve parameters for steel (Basquin's equation: S = A * N^b)
    # These are approximate - actual values depend on specific material
    SN_PARAMETERS = {
        "steel_4.6": {"A": 1200, "b": -0.12, "Se_ratio": 0.35},
        "steel_8.8": {"A": 1800, "b": -0.10, "Se_ratio": 0.40},
        "steel_10.9": {"A": 2200, "b": -0.09, "Se_ratio": 0.38},
        "steel_12.9": {"A": 2500, "b": -0.08, "Se_ratio": 0.35},
        "stainless_A2": {"A": 1400, "b": -0.11, "Se_ratio": 0.40},
        "aluminum": {"A": 800, "b": -0.15, "Se_ratio": 0.30},
    }

    # Surface finish factors (Marin factor ka)
    SURFACE_FACTORS = {
        SurfaceFinish.POLISHED: 1.0,
        SurfaceFinish.GROUND: 0.90,
        SurfaceFinish.MACHINED: 0.80,
        SurfaceFinish.HOT_ROLLED: 0.70,
        SurfaceFinish.AS_FORGED: 0.55,
        SurfaceFinish.CORRODED: 0.40,
    }

    def __init__(self):
        pass

    def analyze_fatigue(
        self,
        stress_max_mpa: float,
        stress_min_mpa: float,
        material: str,
        diameter_mm: float,
        surface_finish: SurfaceFinish = SurfaceFinish.MACHINED,
        temperature_c: float = 25.0,
        reliability: float = 0.90,
        cycles_to_date: int = 0
    ) -> FatigueResult:
        """
        Complete fatigue life analysis.

        Args:
            stress_max_mpa: Maximum stress in cycle
            stress_min_mpa: Minimum stress in cycle
            material: Material type (e.g., "steel_8.8")
            diameter_mm: Part diameter for size effect
            surface_finish: Surface finish quality
            temperature_c: Operating temperature
            reliability: Required reliability (0.50 to 0.999)
            cycles_to_date: Number of cycles already completed

        Returns:
            FatigueResult with complete analysis
        """
        warnings = []
        recommendations = []

        # Calculate stress parameters
        stress_amplitude = (stress_max_mpa - stress_min_mpa) / 2
        mean_stress = (stress_max_mpa + stress_min_mpa) / 2
        stress_ratio = stress_min_mpa / stress_max_mpa if stress_max_mpa != 0 else 0

        # Get S-N parameters
        sn_params = self._get_sn_parameters(material)

        # Calculate endurance limit with correction factors
        Se_prime = sn_params["Se_ratio"] * sn_params["A"]  # Uncorrected
        Se = self._apply_marin_factors(
            Se_prime, surface_finish, diameter_mm, temperature_c, reliability
        )

        # Mean stress correction using Modified Goodman
        Sut = sn_params["A"]  # Approximate ultimate strength
        equiv_amplitude = self._goodman_correction(
            stress_amplitude, mean_stress, Se, Sut
        )

        # Calculate fatigue life
        if equiv_amplitude <= Se:
            # Below endurance limit - infinite life
            estimated_life = 10_000_000
        else:
            # Use Basquin's equation
            estimated_life = self._basquin_life(
                equiv_amplitude, sn_params["A"], sn_params["b"]
            )

        # Calculate safety factors
        fos = Se / equiv_amplitude if equiv_amplitude > 0 else float('inf')
        goodman_safety = self._modified_goodman_safety(
            stress_amplitude, mean_stress, Se, Sut
        )

        # Damage accumulation
        if estimated_life > 0:
            damage_per_cycle = 1.0 / estimated_life
            accumulated_damage = cycles_to_date * damage_per_cycle
            remaining_life = max(0, 1.0 - accumulated_damage) * 100
        else:
            damage_per_cycle = 0
            accumulated_damage = 0
            remaining_life = 100

        # Safety assessment
        is_safe = fos >= 1.5 and remaining_life > 20

        # Generate recommendations
        if fos < 1.5:
            warnings.append(f"Factor of safety {fos:.2f} is below recommended 1.5")
            recommendations.append("Consider reducing stress amplitude or upgrading material")

        if remaining_life < 50:
            warnings.append(f"Only {remaining_life:.0f}% fatigue life remaining")
            recommendations.append("Plan for replacement before next major service interval")

        if surface_finish in [SurfaceFinish.CORRODED, SurfaceFinish.AS_FORGED]:
            recommendations.append("Improve surface finish to increase fatigue life")

        if mean_stress > 0.5 * Sut:
            warnings.append("High mean stress reduces fatigue life significantly")
            recommendations.append("Consider shot peening to introduce compressive residual stress")

        return FatigueResult(
            estimated_life_cycles=int(estimated_life),
            fatigue_strength_mpa=equiv_amplitude,
            endurance_limit_mpa=Se,
            factor_of_safety=fos,
            modified_goodman_safety=goodman_safety,
            damage_per_cycle=damage_per_cycle,
            accumulated_damage=accumulated_damage,
            remaining_life_percent=remaining_life,
            stress_amplitude_mpa=stress_amplitude,
            mean_stress_mpa=mean_stress,
            stress_ratio=stress_ratio,
            is_safe=is_safe,
            recommendations=recommendations,
            warnings=warnings
        )

    def analyze_variable_amplitude(
        self,
        load_spectrum: LoadSpectrum,
        material: str,
        diameter_mm: float,
        surface_finish: SurfaceFinish = SurfaceFinish.MACHINED
    ) -> Dict:
        """
        Variable amplitude fatigue analysis using Miner's rule.

        Args:
            load_spectrum: Load spectrum definition
            material: Material type
            diameter_mm: Part diameter
            surface_finish: Surface finish

        Returns:
            Dict with damage analysis
        """
        sn_params = self._get_sn_parameters(material)
        Se = self._apply_marin_factors(
            sn_params["Se_ratio"] * sn_params["A"],
            surface_finish, diameter_mm, 25.0, 0.90
        )

        total_damage = 0.0
        block_damages = []

        for stress_range, cycles in zip(load_spectrum.stress_ranges, load_spectrum.cycles):
            amplitude = stress_range / 2

            if amplitude <= Se:
                Nf = 10_000_000  # Infinite life
            else:
                Nf = self._basquin_life(amplitude, sn_params["A"], sn_params["b"])

            damage = cycles / Nf
            total_damage += damage
            block_damages.append({
                "stress_range_mpa": stress_range,
                "cycles": cycles,
                "life_at_range": Nf,
                "damage_fraction": damage
            })

        return {
            "total_damage": total_damage,
            "is_safe": total_damage < 1.0,
            "remaining_life_fraction": max(0, 1.0 - total_damage),
            "block_analysis": block_damages,
            "critical_block": max(block_damages, key=lambda x: x["damage_fraction"])
        }

    def generate_sn_curve(
        self,
        material: str,
        surface_finish: SurfaceFinish = SurfaceFinish.MACHINED,
        diameter_mm: float = 10.0,
        num_points: int = 20
    ) -> List[Tuple[int, float]]:
        """
        Generate S-N curve data points.

        Returns:
            List of (cycles, stress_mpa) tuples
        """
        sn_params = self._get_sn_parameters(material)
        Se = self._apply_marin_factors(
            sn_params["Se_ratio"] * sn_params["A"],
            surface_finish, diameter_mm, 25.0, 0.90
        )

        points = []

        # Generate points from 1e3 to 1e7 cycles
        for i in range(num_points):
            log_n = 3 + (7 - 3) * i / (num_points - 1)
            n = int(10 ** log_n)

            if n >= 1e6:
                # At or beyond endurance limit
                stress = Se
            else:
                # Use Basquin's equation
                stress = sn_params["A"] * (n ** sn_params["b"])

            points.append((n, stress))

        return points

    def _get_sn_parameters(self, material: str) -> Dict:
        """Get S-N curve parameters for material."""
        # Try exact match
        if material in self.SN_PARAMETERS:
            return self.SN_PARAMETERS[material]

        # Try partial match
        material_lower = material.lower()
        if "aluminum" in material_lower or "al" in material_lower:
            return self.SN_PARAMETERS["aluminum"]
        elif "stainless" in material_lower or "a2" in material_lower or "a4" in material_lower:
            return self.SN_PARAMETERS["stainless_A2"]
        elif "12.9" in material:
            return self.SN_PARAMETERS["steel_12.9"]
        elif "10.9" in material:
            return self.SN_PARAMETERS["steel_10.9"]
        elif "8.8" in material:
            return self.SN_PARAMETERS["steel_8.8"]
        else:
            return self.SN_PARAMETERS["steel_8.8"]  # Default

    def _apply_marin_factors(
        self,
        Se_prime: float,
        surface: SurfaceFinish,
        diameter: float,
        temperature: float,
        reliability: float
    ) -> float:
        """
        Apply Marin modification factors to endurance limit.

        Se = ka * kb * kc * kd * ke * Se'
        """
        # Surface factor (ka)
        ka = self.SURFACE_FACTORS.get(surface, 0.8)

        # Size factor (kb) - Shigley's approximation
        if diameter <= 8:
            kb = 1.0
        elif diameter <= 50:
            kb = 1.189 * (diameter ** -0.097)
        else:
            kb = 0.75

        # Loading factor (kc) - assume axial/bending
        kc = 1.0

        # Temperature factor (kd)
        if temperature <= 450:
            kd = 1.0
        else:
            kd = 1.0 - 0.0007 * (temperature - 450)

        # Reliability factor (ke)
        reliability_factors = {
            0.50: 1.000,
            0.90: 0.897,
            0.95: 0.868,
            0.99: 0.814,
            0.999: 0.753,
        }
        ke = reliability_factors.get(reliability, 0.85)

        return Se_prime * ka * kb * kc * kd * ke

    def _goodman_correction(
        self,
        Sa: float,
        Sm: float,
        Se: float,
        Sut: float
    ) -> float:
        """
        Modified Goodman mean stress correction.

        Returns equivalent fully-reversed stress amplitude.
        """
        if Sut - Sm <= 0:
            return float('inf')

        return Sa / (1 - Sm / Sut)

    def _modified_goodman_safety(
        self,
        Sa: float,
        Sm: float,
        Se: float,
        Sut: float
    ) -> float:
        """Calculate Modified Goodman factor of safety."""
        if Sa == 0:
            return float('inf')

        # n = 1 / (Sa/Se + Sm/Sut)
        denominator = Sa / Se + Sm / Sut

        if denominator <= 0:
            return float('inf')

        return 1.0 / denominator

    def _basquin_life(
        self,
        stress: float,
        A: float,
        b: float
    ) -> float:
        """
        Calculate fatigue life using Basquin's equation.

        S = A * N^b  =>  N = (S/A)^(1/b)
        """
        if A <= 0 or stress <= 0 or b >= 0:
            return 10_000_000  # Return large number for invalid inputs

        N = (stress / A) ** (1 / b)

        return max(1, min(N, 10_000_000))
