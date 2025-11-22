"""
ORACLE Strength Calculator
Joint strength and load analysis per ISO 898-1.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from enum import Enum
import math


class FailureMode(Enum):
    """Potential fastener failure modes."""
    TENSILE = "TENSILE"
    SHEAR = "SHEAR"
    EXTERNAL_STRIP = "EXTERNAL_STRIP"
    INTERNAL_STRIP = "INTERNAL_STRIP"
    FATIGUE = "FATIGUE"
    BEARING = "BEARING"


@dataclass
class StrengthResult:
    """Complete strength analysis result."""
    allowable_load_kn: float
    ultimate_load_kn: float
    safety_factor: float
    limiting_mode: FailureMode

    tensile_strength_kn: float
    shear_strength_kn: float
    external_strip_kn: float
    internal_strip_kn: float

    utilization_percent: float
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class JointStrengthResult:
    """Multi-fastener joint analysis result."""
    total_allowable_load_kn: float
    fastener_count: int
    load_per_fastener_kn: float
    critical_fastener_index: int
    load_distribution: List[float]
    eccentricity_factor: float
    prying_factor: float
    warnings: List[str] = field(default_factory=list)


class StrengthCalculator:
    """
    Calculates fastener and joint strength.

    Implements ISO 898-1 for metric fasteners and
    standard engineering formulas for joint analysis.
    """

    # Material tensile strengths (MPa)
    GRADE_STRENGTHS = {
        "4.6": {"tensile": 400, "yield": 240, "proof": 225},
        "4.8": {"tensile": 420, "yield": 340, "proof": 310},
        "5.8": {"tensile": 520, "yield": 420, "proof": 380},
        "8.8": {"tensile": 800, "yield": 640, "proof": 580},
        "9.8": {"tensile": 900, "yield": 720, "proof": 650},
        "10.9": {"tensile": 1040, "yield": 940, "proof": 830},
        "12.9": {"tensile": 1220, "yield": 1100, "proof": 970},
        "A2-50": {"tensile": 500, "yield": 210, "proof": 190},
        "A2-70": {"tensile": 700, "yield": 450, "proof": 410},
        "A2-80": {"tensile": 800, "yield": 600, "proof": 550},
        "A4-70": {"tensile": 700, "yield": 450, "proof": 410},
        "A4-80": {"tensile": 800, "yield": 600, "proof": 550},
    }

    # Base material shear strengths (MPa)
    BASE_MATERIALS = {
        "steel": {"tensile": 400, "shear": 231},
        "steel_high": {"tensile": 800, "shear": 462},
        "stainless": {"tensile": 500, "shear": 289},
        "aluminum_6061": {"tensile": 310, "shear": 207},
        "aluminum_7075": {"tensile": 572, "shear": 331},
        "cast_iron": {"tensile": 250, "shear": 180},
        "brass": {"tensile": 345, "shear": 200},
    }

    def __init__(self):
        pass

    def calculate_strength(
        self,
        diameter_mm: float,
        pitch_mm: float,
        grade: str,
        engagement_mm: float,
        base_material: str,
        safety_factor: float = 2.5
    ) -> StrengthResult:
        """
        Calculate complete fastener strength analysis.

        Args:
            diameter_mm: Nominal thread diameter
            pitch_mm: Thread pitch
            grade: Fastener grade (e.g., "8.8")
            engagement_mm: Thread engagement length
            base_material: Material of tapped hole/nut
            safety_factor: Required safety factor

        Returns:
            StrengthResult with all failure modes analyzed
        """
        warnings = []
        recommendations = []

        # Get material properties
        fastener_props = self.GRADE_STRENGTHS.get(grade)
        base_props = self.BASE_MATERIALS.get(base_material)

        if not fastener_props:
            fastener_props = self.GRADE_STRENGTHS["8.8"]
            warnings.append(f"Unknown grade {grade}, using 8.8 properties")

        if not base_props:
            base_props = self.BASE_MATERIALS["steel"]
            warnings.append(f"Unknown base material {base_material}, using steel properties")

        # Calculate tensile stress area (ISO 898-1)
        d2 = diameter_mm - 0.6495 * pitch_mm  # Pitch diameter
        d3 = diameter_mm - 1.2268 * pitch_mm  # Minor diameter
        As = (math.pi / 4) * ((d2 + d3) / 2) ** 2

        # Tensile strength
        tensile_kn = As * fastener_props["proof"] / 1000

        # Shear strength (bolt in single shear)
        # Use minor diameter for shear plane
        shear_area = (math.pi / 4) * d3 ** 2
        shear_kn = shear_area * fastener_props["tensile"] * 0.577 / 1000

        # Thread stripping - external (fastener threads)
        thread_shear_area = self._calculate_thread_shear_area(
            diameter_mm, pitch_mm, engagement_mm
        )
        external_strip_kn = thread_shear_area * fastener_props["tensile"] * 0.577 / 1000

        # Thread stripping - internal (base material threads)
        internal_strip_kn = (
            thread_shear_area * base_props["shear"] * 1.25 / 1000
        )  # 1.25 factor for internal threads

        # Determine limiting mode
        strengths = {
            FailureMode.TENSILE: tensile_kn,
            FailureMode.SHEAR: shear_kn,
            FailureMode.EXTERNAL_STRIP: external_strip_kn,
            FailureMode.INTERNAL_STRIP: internal_strip_kn,
        }

        limiting_mode = min(strengths, key=strengths.get)
        ultimate_kn = strengths[limiting_mode]
        allowable_kn = ultimate_kn / safety_factor

        # Generate recommendations
        if limiting_mode == FailureMode.INTERNAL_STRIP:
            recommendations.append("Internal thread is limiting - consider helicoil insert")
        elif limiting_mode == FailureMode.EXTERNAL_STRIP:
            recommendations.append("External thread is limiting - increase engagement or use larger fastener")

        engagement_ratio = engagement_mm / diameter_mm
        if engagement_ratio < 1.0:
            warnings.append(f"Engagement ratio {engagement_ratio:.2f} is below 1.0D minimum")

        return StrengthResult(
            allowable_load_kn=allowable_kn,
            ultimate_load_kn=ultimate_kn,
            safety_factor=safety_factor,
            limiting_mode=limiting_mode,
            tensile_strength_kn=tensile_kn,
            shear_strength_kn=shear_kn,
            external_strip_kn=external_strip_kn,
            internal_strip_kn=internal_strip_kn,
            utilization_percent=0.0,  # Set when checking against applied load
            recommendations=recommendations,
            warnings=warnings
        )

    def calculate_joint_strength(
        self,
        fastener_strengths: List[StrengthResult],
        pattern_type: str = "rectangular",
        eccentricity_mm: float = 0.0,
        prying_expected: bool = False
    ) -> JointStrengthResult:
        """
        Calculate strength of multi-fastener joint.

        Args:
            fastener_strengths: List of individual fastener strengths
            pattern_type: "rectangular", "circular", "linear"
            eccentricity_mm: Load eccentricity from centroid
            prying_expected: Whether prying forces are expected

        Returns:
            JointStrengthResult with joint analysis
        """
        warnings = []
        n = len(fastener_strengths)

        if n == 0:
            return JointStrengthResult(
                total_allowable_load_kn=0,
                fastener_count=0,
                load_per_fastener_kn=0,
                critical_fastener_index=0,
                load_distribution=[],
                eccentricity_factor=1.0,
                prying_factor=1.0,
                warnings=["No fasteners in joint"]
            )

        # Base load distribution (equal for now)
        base_distribution = [1.0 / n] * n

        # Eccentricity factor (simplified)
        if eccentricity_mm > 0:
            eccentricity_factor = 1.0 + (eccentricity_mm / 100)  # Simplified
            warnings.append("Eccentric loading increases load on outer fasteners")
        else:
            eccentricity_factor = 1.0

        # Prying factor
        if prying_expected:
            prying_factor = 1.25  # 25% increase for prying
            warnings.append("Prying increases effective load by 25%")
        else:
            prying_factor = 1.0

        # Find critical (weakest) fastener
        allowable_loads = [f.allowable_load_kn for f in fastener_strengths]
        critical_index = allowable_loads.index(min(allowable_loads))
        critical_strength = allowable_loads[critical_index]

        # Total joint strength limited by critical fastener
        total_allowable = (critical_strength * n) / (eccentricity_factor * prying_factor)
        load_per_fastener = total_allowable / n

        return JointStrengthResult(
            total_allowable_load_kn=total_allowable,
            fastener_count=n,
            load_per_fastener_kn=load_per_fastener,
            critical_fastener_index=critical_index,
            load_distribution=base_distribution,
            eccentricity_factor=eccentricity_factor,
            prying_factor=prying_factor,
            warnings=warnings
        )

    def calculate_preload(
        self,
        diameter_mm: float,
        pitch_mm: float,
        grade: str,
        friction_coefficient: float = 0.15,
        preload_ratio: float = 0.75
    ) -> Dict:
        """
        Calculate recommended assembly preload.

        Args:
            diameter_mm: Nominal thread diameter
            pitch_mm: Thread pitch
            grade: Fastener grade
            friction_coefficient: Friction under head and in threads
            preload_ratio: Target preload as fraction of proof load

        Returns:
            Dict with preload force and torque
        """
        # Calculate stress area
        d2 = diameter_mm - 0.6495 * pitch_mm
        d3 = diameter_mm - 1.2268 * pitch_mm
        As = (math.pi / 4) * ((d2 + d3) / 2) ** 2

        # Get proof stress
        props = self.GRADE_STRENGTHS.get(grade, self.GRADE_STRENGTHS["8.8"])
        proof_stress = props["proof"]

        # Calculate proof load
        proof_load_kn = As * proof_stress / 1000

        # Target preload
        preload_kn = proof_load_kn * preload_ratio

        # Calculate torque using simplified formula
        # T = K * d * F where K is torque coefficient
        K = friction_coefficient * (0.583 + (math.pi * d2 / (2 * pitch_mm)))
        K = min(K, 0.22)  # Cap at typical value

        torque_nm = K * diameter_mm * preload_kn  # Nm

        return {
            "proof_load_kn": proof_load_kn,
            "target_preload_kn": preload_kn,
            "preload_ratio": preload_ratio,
            "recommended_torque_nm": torque_nm,
            "torque_coefficient_k": K,
            "stress_at_preload_mpa": preload_kn * 1000 / As,
        }

    def _calculate_thread_shear_area(
        self,
        diameter_mm: float,
        pitch_mm: float,
        engagement_mm: float
    ) -> float:
        """Calculate thread shear area per ISO 898-1."""
        d = diameter_mm
        p = pitch_mm
        Le = engagement_mm

        # Pitch diameter
        d2 = d - 0.6495 * p

        # Shear area for external threads
        As = 0.5 * math.pi * d2 * Le * (0.5 + 0.577 * (d - d2) / p)

        return As

    def check_bearing_stress(
        self,
        load_kn: float,
        head_diameter_mm: float,
        hole_diameter_mm: float,
        washer_od_mm: Optional[float],
        material_yield_mpa: float
    ) -> Dict:
        """
        Check bearing stress under fastener head.

        Returns:
            Dict with bearing stress analysis
        """
        # Bearing area
        if washer_od_mm:
            outer_d = washer_od_mm
        else:
            outer_d = head_diameter_mm

        bearing_area = math.pi * (outer_d ** 2 - hole_diameter_mm ** 2) / 4

        # Bearing stress
        bearing_stress = load_kn * 1000 / bearing_area  # MPa

        # Allowable bearing stress (typically 0.9 * yield)
        allowable_bearing = material_yield_mpa * 0.9

        utilization = bearing_stress / allowable_bearing

        return {
            "bearing_area_mm2": bearing_area,
            "bearing_stress_mpa": bearing_stress,
            "allowable_stress_mpa": allowable_bearing,
            "utilization": utilization,
            "acceptable": utilization <= 1.0,
            "recommendation": "Add washer to increase bearing area" if utilization > 1.0 else None
        }
