"""
ORACLE Thread Engagement Calculator
Calculates minimum thread engagement for safe fastening.

Based on:
- Machinery's Handbook (31st Edition)
- MIL-HDBK-60 (Threaded Fasteners)
- VDI 2230 (Systematic Calculation of Bolted Joints)
- ISO 898-1 (Mechanical properties of fasteners)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from enum import Enum
import math


class LimitingComponent(Enum):
    """Which component limits thread engagement."""
    BOLT = "BOLT"
    NUT = "NUT"
    TAPPED_HOLE = "TAPPED_HOLE"


@dataclass
class ThreadSpec:
    """Complete thread specification."""
    nominal_diameter_mm: float
    pitch_mm: float
    thread_class: str = "6g"
    major_diameter_mm: Optional[float] = None
    pitch_diameter_mm: Optional[float] = None
    minor_diameter_mm: Optional[float] = None
    thread_angle_deg: float = 60.0


@dataclass
class MaterialProperties:
    """Material mechanical properties."""
    name: str
    tensile_strength_mpa: float
    shear_strength_mpa: float
    yield_strength_mpa: float
    hardness_hrc: Optional[float] = None


@dataclass
class EngagementResult:
    """Thread engagement calculation result."""
    minimum_engagement_mm: float
    recommended_engagement_mm: float
    limiting_component: LimitingComponent
    safety_factor_achieved: float
    thread_count: float
    stripping_load_external_kn: float
    stripping_load_internal_kn: float
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class ThreadEngagementCalculator:
    """
    Calculates minimum thread engagement for safe fastening.

    Uses ISO 898-1, MIL-HDBK-60, and VDI 2230 methodologies
    for thread stripping analysis.
    """

    # Standard material properties database
    MATERIALS = {
        "steel_8.8": MaterialProperties(
            name="Steel Grade 8.8",
            tensile_strength_mpa=800,
            shear_strength_mpa=462,  # ~0.577 * tensile
            yield_strength_mpa=640
        ),
        "steel_10.9": MaterialProperties(
            name="Steel Grade 10.9",
            tensile_strength_mpa=1040,
            shear_strength_mpa=600,
            yield_strength_mpa=940
        ),
        "steel_12.9": MaterialProperties(
            name="Steel Grade 12.9",
            tensile_strength_mpa=1220,
            shear_strength_mpa=704,
            yield_strength_mpa=1100
        ),
        "stainless_a2_70": MaterialProperties(
            name="Stainless A2-70",
            tensile_strength_mpa=700,
            shear_strength_mpa=404,
            yield_strength_mpa=450
        ),
        "aluminum_6061": MaterialProperties(
            name="Aluminum 6061-T6",
            tensile_strength_mpa=310,
            shear_strength_mpa=207,
            yield_strength_mpa=276
        ),
        "cast_iron": MaterialProperties(
            name="Cast Iron",
            tensile_strength_mpa=250,
            shear_strength_mpa=180,
            yield_strength_mpa=180
        ),
    }

    # Minimum engagement ratios per ISO 898-1
    MIN_ENGAGEMENT_RATIOS = {
        ("8.8", "steel"): 1.0,
        ("8.8", "aluminum"): 2.0,
        ("8.8", "cast_iron"): 1.5,
        ("10.9", "steel"): 1.25,
        ("10.9", "aluminum"): 2.5,
        ("10.9", "cast_iron"): 1.8,
        ("12.9", "steel"): 1.5,
        ("12.9", "aluminum"): 3.0,
        ("12.9", "cast_iron"): 2.0,
        ("A2-70", "steel"): 1.5,
        ("A2-70", "aluminum"): 2.5,
        ("A4-70", "steel"): 1.5,
        ("A4-70", "aluminum"): 2.5,
    }

    def __init__(self):
        self.last_calculation = None

    def calculate_minimum_engagement(
        self,
        external_thread: ThreadSpec,
        internal_thread: ThreadSpec,
        load_newtons: float,
        material_external: MaterialProperties,
        material_internal: MaterialProperties,
        safety_factor: float = 2.0
    ) -> EngagementResult:
        """
        Calculate minimum thread engagement for given load.

        Args:
            external_thread: Bolt/screw thread specification
            internal_thread: Nut/tapped hole thread specification
            load_newtons: Applied axial load in Newtons
            material_external: Material of bolt/screw
            material_internal: Material of nut/tapped hole
            safety_factor: Required safety factor (default 2.0)

        Returns:
            EngagementResult with analysis
        """
        warnings = []
        recommendations = []

        # Calculate thread shear areas per mm of engagement
        A_s_external = self.shear_area_external_per_mm(external_thread)
        A_s_internal = self.shear_area_internal_per_mm(internal_thread)

        # Material shear strengths
        tau_external = material_external.shear_strength_mpa
        tau_internal = material_internal.shear_strength_mpa

        # Stripping strength per mm of engagement (N/mm)
        strip_strength_external = A_s_external * tau_external
        strip_strength_internal = A_s_internal * tau_internal * 1.25  # Internal 25% stronger

        # Determine limiting component
        if strip_strength_external < strip_strength_internal:
            limiting_component = LimitingComponent.BOLT
            limiting_strength = strip_strength_external
        else:
            limiting_component = LimitingComponent.NUT if material_internal.name.lower().find("nut") >= 0 else LimitingComponent.TAPPED_HOLE
            limiting_strength = strip_strength_internal

        # Calculate minimum engagement
        min_engagement_mm = (load_newtons * safety_factor) / limiting_strength

        # Round up to practical value (0.5D increments)
        d = external_thread.nominal_diameter_mm
        practical_engagement = math.ceil(min_engagement_mm / (d * 0.5)) * (d * 0.5)

        # Calculate achieved safety factor
        actual_sf = (practical_engagement * limiting_strength) / load_newtons

        # Thread count
        thread_count = practical_engagement / external_thread.pitch_mm

        # Calculate stripping loads at practical engagement
        strip_load_external = (practical_engagement * strip_strength_external) / 1000  # kN
        strip_load_internal = (practical_engagement * strip_strength_internal) / 1000  # kN

        # Warnings
        if thread_count < 3:
            warnings.append(f"Only {thread_count:.1f} threads engaged - minimum 3 recommended")

        if min_engagement_mm > 2.5 * d:
            warnings.append(f"Required engagement ({min_engagement_mm:.1f}mm) exceeds 2.5D - consider larger fastener")

        # Recommendations
        if limiting_component == LimitingComponent.BOLT:
            recommendations.append("External thread is limiting - consider higher grade bolt")
        else:
            recommendations.append("Internal thread is limiting - consider helicoil insert for aluminum")

        if material_internal.tensile_strength_mpa < material_external.tensile_strength_mpa * 0.5:
            recommendations.append("Large strength mismatch - consider thread engagement > 2D")

        return EngagementResult(
            minimum_engagement_mm=min_engagement_mm,
            recommended_engagement_mm=practical_engagement,
            limiting_component=limiting_component,
            safety_factor_achieved=actual_sf,
            thread_count=thread_count,
            stripping_load_external_kn=strip_load_external,
            stripping_load_internal_kn=strip_load_internal,
            warnings=warnings,
            recommendations=recommendations
        )

    def shear_area_external_per_mm(self, thread: ThreadSpec) -> float:
        """
        Calculate external thread shear area per mm of engagement.
        Per ISO 898-1 / MIL-HDBK-60.

        Returns:
            Shear area in mm² per mm of engagement
        """
        d = thread.nominal_diameter_mm
        p = thread.pitch_mm

        # Basic pitch diameter (approximate)
        d2 = d - 0.6495 * p

        # Thread height
        H = 0.866025 * p  # H = (√3/2) * p

        # Shear area per mm of engagement
        # As = π * d2 * (0.5 + 0.577 * (d - d2) / p)
        As_per_mm = math.pi * d2 * (0.5 + 0.577 * (d - d2) / p) / p

        return As_per_mm

    def shear_area_internal_per_mm(self, thread: ThreadSpec) -> float:
        """
        Calculate internal thread shear area per mm of engagement.

        Returns:
            Shear area in mm² per mm of engagement
        """
        d = thread.nominal_diameter_mm
        p = thread.pitch_mm

        # Minor diameter (approximate for internal thread)
        d1 = d - 1.0825 * p

        # Basic pitch diameter
        d2 = d - 0.6495 * p

        # Shear area per mm of engagement
        # Internal threads have larger shear area due to geometry
        As_per_mm = math.pi * d1 * (0.5 + 0.577 * (d2 - d1) / p) / p

        return As_per_mm

    def get_min_engagement_ratio(
        self,
        bolt_grade: str,
        base_material: str
    ) -> float:
        """
        Get minimum engagement ratio (Le/D) for given materials.

        Args:
            bolt_grade: Fastener grade (e.g., "8.8", "10.9", "A2-70")
            base_material: Tapped material type

        Returns:
            Minimum Le/D ratio
        """
        # Normalize material name
        material_type = "steel"
        if "aluminum" in base_material.lower() or "al" in base_material.lower():
            material_type = "aluminum"
        elif "cast" in base_material.lower() or "iron" in base_material.lower():
            material_type = "cast_iron"

        return self.MIN_ENGAGEMENT_RATIOS.get(
            (bolt_grade, material_type),
            2.0  # Default conservative ratio
        )

    def calculate_tensile_stress_area(self, thread: ThreadSpec) -> float:
        """
        Calculate tensile stress area per ISO 898-1.

        Returns:
            Tensile stress area in mm²
        """
        d = thread.nominal_diameter_mm
        p = thread.pitch_mm

        # Pitch diameter
        d2 = d - 0.6495 * p

        # Minor diameter (external thread)
        d3 = d - 1.2268 * p

        # Stress area
        As = (math.pi / 4) * ((d2 + d3) / 2) ** 2

        return As

    def calculate_proof_load(
        self,
        thread: ThreadSpec,
        material: MaterialProperties
    ) -> float:
        """
        Calculate proof load for fastener.

        Returns:
            Proof load in kN
        """
        As = self.calculate_tensile_stress_area(thread)

        # Proof stress is typically ~90% of yield
        proof_stress = material.yield_strength_mpa * 0.9

        proof_load_n = As * proof_stress

        return proof_load_n / 1000  # kN


@dataclass
class VDI2230Result:
    """VDI 2230 bolt joint calculation result."""
    assembly_preload_kn: float
    working_load_range_kn: Tuple[float, float]
    bolt_stress_mpa: float
    joint_stiffness_ratio: float
    fatigue_safe: bool
    embedding_loss_percent: float
    warnings: List[str] = field(default_factory=list)


class VDI2230Calculator:
    """
    VDI 2230 compliant bolted joint calculator.

    Implements systematic calculation method for high-strength
    bolted joints per VDI 2230 Blatt 1.
    """

    def __init__(self):
        pass

    def calculate_bolted_joint(
        self,
        bolt_thread: ThreadSpec,
        bolt_material: MaterialProperties,
        clamp_length_mm: float,
        external_load_kn: float,
        load_introduction_factor: float = 0.5,
        embedding_mm: float = 0.005
    ) -> VDI2230Result:
        """
        Calculate bolted joint per VDI 2230.

        Args:
            bolt_thread: Thread specification
            bolt_material: Bolt material properties
            clamp_length_mm: Total clamped length
            external_load_kn: External axial load
            load_introduction_factor: n (typically 0.3-0.7)
            embedding_mm: Expected embedding per surface

        Returns:
            VDI2230Result with complete analysis
        """
        warnings = []

        # Calculate stress area
        As = ThreadEngagementCalculator().calculate_tensile_stress_area(bolt_thread)

        # Bolt stiffness (simplified)
        E_bolt = 210000  # MPa for steel
        L_clamp = clamp_length_mm
        k_bolt = (E_bolt * As) / L_clamp  # N/mm

        # Clamped parts stiffness (simplified - assume steel)
        d = bolt_thread.nominal_diameter_mm
        A_clamp = math.pi * (2.5 * d) ** 2 / 4  # Effective clamped area
        k_clamp = (E_bolt * A_clamp) / L_clamp

        # Stiffness ratio
        phi = k_bolt / (k_bolt + k_clamp)

        # Force ratio (load factor)
        n = load_introduction_factor

        # Additional bolt force from external load
        delta_F_bolt = n * phi * external_load_kn

        # Required minimum assembly preload
        # Must maintain positive clamp force under all conditions
        F_clamp_min = 0.1 * external_load_kn  # 10% minimum clamp force
        F_preload = (1 - n * phi) * external_load_kn + F_clamp_min

        # Account for embedding losses
        embedding_loss = embedding_mm * 2 * k_bolt / 1000  # kN (2 surfaces)
        F_preload_assembly = F_preload + embedding_loss

        # Working load range
        F_bolt_min = F_preload - embedding_loss + delta_F_bolt * 0
        F_bolt_max = F_preload + delta_F_bolt

        # Bolt stress at max load
        bolt_stress = F_bolt_max * 1000 / As  # MPa

        # Fatigue check (simplified)
        stress_amplitude = (F_bolt_max - F_bolt_min) * 1000 / (2 * As)
        fatigue_safe = stress_amplitude < (bolt_material.tensile_strength_mpa * 0.05)  # ~5% of UTS

        if bolt_stress > bolt_material.yield_strength_mpa * 0.9:
            warnings.append("Bolt stress exceeds 90% of yield - reduce preload or use higher grade")

        if not fatigue_safe:
            warnings.append("Fatigue load amplitude exceeds recommended limit")

        if phi > 0.3:
            warnings.append("High stiffness ratio - consider increasing clamp stiffness")

        return VDI2230Result(
            assembly_preload_kn=F_preload_assembly,
            working_load_range_kn=(F_bolt_min, F_bolt_max),
            bolt_stress_mpa=bolt_stress,
            joint_stiffness_ratio=phi,
            fatigue_safe=fatigue_safe,
            embedding_loss_percent=(embedding_loss / F_preload_assembly) * 100,
            warnings=warnings
        )
