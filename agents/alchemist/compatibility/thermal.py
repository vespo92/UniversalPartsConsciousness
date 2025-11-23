"""
Thermal Expansion Compatibility Analysis

Calculates thermal expansion mismatch between materials and
predicts stress/clearance issues across temperature ranges.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ThermalRisk(Enum):
    """Thermal mismatch risk level"""
    NEGLIGIBLE = "negligible"  # < 2 ppm/K difference
    LOW = "low"                # 2-5 ppm/K difference
    MODERATE = "moderate"      # 5-10 ppm/K difference
    HIGH = "high"              # 10-15 ppm/K difference
    SEVERE = "severe"          # > 15 ppm/K difference


class JointType(Enum):
    """Type of joint/assembly"""
    PRESS_FIT = "press_fit"         # Interference fit
    CLEARANCE_FIT = "clearance_fit"  # Sliding fit
    THREADED = "threaded"           # Bolted/screwed
    ADHESIVE = "adhesive"           # Bonded
    WELDED = "welded"               # Welded joint


@dataclass
class ThermalMismatch:
    """Thermal expansion mismatch between two materials"""
    material_a: str
    material_b: str
    cte_a_um_mk: float  # Coefficient of thermal expansion
    cte_b_um_mk: float
    cte_difference: float
    risk: ThermalRisk

    # Calculated values for specific conditions
    reference_temp_c: float
    target_temp_c: float
    dimension_mm: float
    expansion_a_mm: float
    expansion_b_mm: float
    differential_expansion_mm: float


@dataclass
class ThermalAssessment:
    """Complete thermal compatibility assessment"""
    mismatch: ThermalMismatch
    compatible: bool
    risk_description: str
    design_recommendations: List[str]
    joint_type_compatibility: Dict[JointType, bool]


class ThermalExpansionChecker:
    """
    Checks thermal expansion compatibility between materials.

    Calculates differential expansion and predicts assembly
    behavior across temperature ranges.
    """

    # Thermal expansion coefficients (µm/m·K = ppm/K)
    CTE_DATABASE: Dict[str, float] = {
        # Steels
        "carbon_steel": 11.5,
        "4140_steel": 12.3,
        "stainless_304": 17.2,
        "stainless_316": 16.0,
        "stainless_17_4ph": 10.8,
        "tool_steel": 11.0,

        # Aluminum
        "aluminum_6061": 23.6,
        "aluminum_7075": 23.4,
        "aluminum_2024": 22.9,
        "aluminum_5052": 23.8,

        # Titanium
        "titanium_grade2": 8.6,
        "ti_6al_4v": 8.6,

        # Copper alloys
        "copper": 17.0,
        "brass": 19.0,
        "bronze": 18.0,
        "beryllium_copper": 17.8,

        # Nickel alloys
        "inconel_718": 13.0,
        "inconel_625": 12.8,
        "monel_400": 13.9,
        "hastelloy_c276": 11.2,

        # Other metals
        "magnesium": 25.2,
        "zinc": 30.2,
        "tungsten": 4.5,
        "molybdenum": 5.0,
        "invar": 1.2,  # Special low-expansion alloy

        # Polymers (approximate - varies with formulation)
        "peek": 47.0,
        "ptfe": 135.0,
        "nylon": 80.0,
        "acetal": 85.0,
        "abs": 90.0,
        "polycarbonate": 68.0,

        # Ceramics
        "alumina": 8.1,
        "silicon_carbide": 4.0,
        "zirconia": 10.5,

        # Composites (typical values)
        "carbon_fiber_epoxy": 0.5,  # Along fiber direction
        "fiberglass_epoxy": 14.0,
    }

    def __init__(self):
        self._materials = self.CTE_DATABASE.copy()

    def get_cte(self, material: str) -> Optional[float]:
        """Get CTE for a material"""
        normalized = material.lower().replace(" ", "_").replace("-", "_")
        return self._materials.get(normalized)

    def check_compatibility(
        self,
        material_a: str,
        material_b: str,
        reference_temp_c: float = 20.0,
        target_temp_c: float = 100.0,
        dimension_mm: float = 100.0,
        joint_type: JointType = JointType.CLEARANCE_FIT
    ) -> ThermalAssessment:
        """
        Check thermal compatibility between two materials.

        Args:
            material_a: First material
            material_b: Second material
            reference_temp_c: Assembly temperature
            target_temp_c: Operating temperature
            dimension_mm: Critical dimension in mm
            joint_type: Type of joint/assembly

        Returns:
            ThermalAssessment with compatibility analysis
        """
        cte_a = self.get_cte(material_a)
        cte_b = self.get_cte(material_b)

        if cte_a is None:
            raise ValueError(f"Unknown material: {material_a}")
        if cte_b is None:
            raise ValueError(f"Unknown material: {material_b}")

        # Calculate CTE difference
        cte_diff = abs(cte_a - cte_b)

        # Classify risk
        risk = self._classify_risk(cte_diff)

        # Calculate actual expansions
        delta_t = target_temp_c - reference_temp_c
        expansion_a = (cte_a * delta_t * dimension_mm) / 1000  # Convert to mm
        expansion_b = (cte_b * delta_t * dimension_mm) / 1000
        differential = abs(expansion_a - expansion_b)

        mismatch = ThermalMismatch(
            material_a=material_a,
            material_b=material_b,
            cte_a_um_mk=cte_a,
            cte_b_um_mk=cte_b,
            cte_difference=cte_diff,
            risk=risk,
            reference_temp_c=reference_temp_c,
            target_temp_c=target_temp_c,
            dimension_mm=dimension_mm,
            expansion_a_mm=expansion_a,
            expansion_b_mm=expansion_b,
            differential_expansion_mm=differential
        )

        # Determine compatibility based on joint type
        compatible = self._check_joint_compatibility(mismatch, joint_type)

        # Generate description
        risk_desc = self._describe_risk(mismatch, joint_type)

        # Generate recommendations
        recommendations = self._get_recommendations(mismatch, joint_type)

        # Check all joint types
        joint_compatibility = {
            jt: self._check_joint_compatibility(mismatch, jt)
            for jt in JointType
        }

        return ThermalAssessment(
            mismatch=mismatch,
            compatible=compatible,
            risk_description=risk_desc,
            design_recommendations=recommendations,
            joint_type_compatibility=joint_compatibility
        )

    def _classify_risk(self, cte_diff: float) -> ThermalRisk:
        """Classify risk based on CTE difference"""
        if cte_diff < 2:
            return ThermalRisk.NEGLIGIBLE
        elif cte_diff < 5:
            return ThermalRisk.LOW
        elif cte_diff < 10:
            return ThermalRisk.MODERATE
        elif cte_diff < 15:
            return ThermalRisk.HIGH
        else:
            return ThermalRisk.SEVERE

    def _check_joint_compatibility(
        self,
        mismatch: ThermalMismatch,
        joint_type: JointType
    ) -> bool:
        """Check if mismatch is acceptable for joint type"""
        diff_mm = mismatch.differential_expansion_mm

        tolerances = {
            JointType.PRESS_FIT: 0.05,    # Very tight tolerance
            JointType.CLEARANCE_FIT: 0.2,  # Some allowance
            JointType.THREADED: 0.1,       # Thread engagement affected
            JointType.ADHESIVE: 0.3,       # Adhesive can accommodate some movement
            JointType.WELDED: 0.05,        # Stress builds up
        }

        tolerance = tolerances.get(joint_type, 0.1)

        # Scale tolerance with dimension
        scaled_tolerance = tolerance * (mismatch.dimension_mm / 100)

        return diff_mm < scaled_tolerance

    def _describe_risk(
        self,
        mismatch: ThermalMismatch,
        joint_type: JointType
    ) -> str:
        """Generate risk description"""
        higher_cte = (mismatch.material_a if mismatch.cte_a_um_mk > mismatch.cte_b_um_mk
                      else mismatch.material_b)
        lower_cte = (mismatch.material_b if higher_cte == mismatch.material_a
                     else mismatch.material_a)

        delta_t = mismatch.target_temp_c - mismatch.reference_temp_c
        heating = delta_t > 0

        if mismatch.risk == ThermalRisk.NEGLIGIBLE:
            return (
                f"Negligible thermal mismatch ({mismatch.cte_difference:.1f} ppm/K). "
                f"Materials are thermally compatible for most applications."
            )

        if heating:
            behavior = f"{higher_cte} will expand more than {lower_cte}"
        else:
            behavior = f"{higher_cte} will contract more than {lower_cte}"

        diff_um = mismatch.differential_expansion_mm * 1000

        return (
            f"CTE difference: {mismatch.cte_difference:.1f} ppm/K ({mismatch.risk.value} risk). "
            f"{behavior}. "
            f"For a {mismatch.dimension_mm:.0f}mm dimension and "
            f"{abs(delta_t):.0f}°C temperature change: "
            f"differential expansion = {diff_um:.1f} µm ({mismatch.differential_expansion_mm:.3f} mm). "
        )

    def _get_recommendations(
        self,
        mismatch: ThermalMismatch,
        joint_type: JointType
    ) -> List[str]:
        """Generate design recommendations"""
        recs = []

        if mismatch.risk == ThermalRisk.NEGLIGIBLE:
            return ["No special considerations needed for thermal expansion."]

        higher_cte = (mismatch.material_a if mismatch.cte_a_um_mk > mismatch.cte_b_um_mk
                      else mismatch.material_b)

        # General recommendations
        recs.append(
            f"Design clearance to accommodate {mismatch.differential_expansion_mm:.3f}mm "
            f"differential expansion"
        )

        # Joint-specific recommendations
        if joint_type == JointType.PRESS_FIT:
            recs.append(
                "Press fits may loosen at elevated temp or seize when cooled. "
                "Consider temperature range during fit specification."
            )
            if mismatch.risk in [ThermalRisk.HIGH, ThermalRisk.SEVERE]:
                recs.append(
                    "NOT RECOMMENDED: Press fit with this CTE mismatch. "
                    "Use mechanical retention or adhesive instead."
                )

        elif joint_type == JointType.THREADED:
            recs.append(
                "Thread engagement changes with temperature. "
                "Specify thread engagement for worst-case condition."
            )
            if higher_cte in [mismatch.material_a, mismatch.material_b]:
                recs.append(
                    f"If {higher_cte} is the male thread, it may seize when heated."
                )

        elif joint_type == JointType.ADHESIVE:
            recs.append(
                "Select adhesive with flexibility to accommodate thermal movement. "
                "Avoid rigid epoxies for this application."
            )
            recs.append("Consider silicone or polyurethane adhesives.")

        elif joint_type == JointType.WELDED:
            recs.append(
                "Thermal stress will build up in welded joint during temperature cycling. "
                "May cause fatigue cracking over time."
            )

        # Material substitution suggestions
        if mismatch.cte_difference > 10:
            recs.append(
                f"Consider materials with closer CTE values. "
                f"Current difference: {mismatch.cte_difference:.1f} ppm/K"
            )
            if "aluminum" in mismatch.material_a.lower() or "aluminum" in mismatch.material_b.lower():
                recs.append("Aluminum-silicon alloys have lower CTE than pure aluminum.")
            if "steel" in mismatch.material_a.lower() or "steel" in mismatch.material_b.lower():
                recs.append("Invar (36% Ni steel) has very low CTE (~1.2 ppm/K).")

        return recs

    def calculate_interference_change(
        self,
        outer_material: str,
        inner_material: str,
        nominal_diameter_mm: float,
        initial_interference_mm: float,
        reference_temp_c: float,
        target_temp_c: float
    ) -> Dict:
        """
        Calculate how interference fit changes with temperature.

        Args:
            outer_material: Material of outer (hub) component
            inner_material: Material of inner (shaft) component
            nominal_diameter_mm: Nominal fit diameter
            initial_interference_mm: Interference at reference temperature
            reference_temp_c: Assembly temperature
            target_temp_c: Operating temperature

        Returns:
            Dict with interference at target temperature and recommendations
        """
        cte_outer = self.get_cte(outer_material)
        cte_inner = self.get_cte(inner_material)

        if cte_outer is None or cte_inner is None:
            raise ValueError("Unknown material")

        delta_t = target_temp_c - reference_temp_c

        # Calculate diameter changes
        outer_expansion = (cte_outer * delta_t * nominal_diameter_mm) / 1000
        inner_expansion = (cte_inner * delta_t * nominal_diameter_mm) / 1000

        # New interference = initial + (inner expansion - outer expansion)
        # If outer expands more, interference increases (tighter)
        # If inner expands more, interference decreases (looser)
        interference_change = outer_expansion - inner_expansion
        new_interference = initial_interference_mm - interference_change

        status = "SAFE"
        if new_interference <= 0:
            status = "WARNING: Fit becomes clearance or loose"
        elif new_interference > initial_interference_mm * 1.5:
            status = "WARNING: Excessive interference may cause damage"

        return {
            "reference_interference_mm": initial_interference_mm,
            "target_interference_mm": new_interference,
            "change_mm": -interference_change,
            "change_percent": (new_interference / initial_interference_mm - 1) * 100,
            "status": status,
            "outer_expansion_mm": outer_expansion,
            "inner_expansion_mm": inner_expansion,
        }


# Demo
if __name__ == "__main__":
    checker = ThermalExpansionChecker()

    print("=== Thermal Compatibility Demo ===\n")

    # Aluminum + Stainless Steel
    result = checker.check_compatibility(
        "aluminum_6061",
        "stainless_316",
        reference_temp_c=20,
        target_temp_c=150,
        dimension_mm=100,
        joint_type=JointType.PRESS_FIT
    )

    print(f"Materials: {result.mismatch.material_a} + {result.mismatch.material_b}")
    print(f"CTE difference: {result.mismatch.cte_difference:.1f} ppm/K")
    print(f"Risk: {result.mismatch.risk.value.upper()}")
    print(f"Compatible for press fit: {result.compatible}")
    print(f"\n{result.risk_description}")

    print("\nJoint type compatibility:")
    for jt, compat in result.joint_type_compatibility.items():
        print(f"  {jt.value}: {'Yes' if compat else 'No'}")

    print("\nRecommendations:")
    for rec in result.design_recommendations[:3]:
        print(f"  - {rec}")
