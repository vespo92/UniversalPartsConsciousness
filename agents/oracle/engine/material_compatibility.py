"""
ORACLE Material Compatibility Checker
Galvanic corrosion, thermal expansion, and chemical compatibility.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class GalvanicRisk(Enum):
    """Galvanic corrosion risk levels."""
    SAFE = "SAFE"           # No corrosion risk
    LOW = "LOW"             # Minor risk, acceptable in most environments
    MODERATE = "MODERATE"   # Noticeable risk, consider protection
    SEVERE = "SEVERE"       # High risk, isolation required


class Environment(Enum):
    """Operating environment."""
    INDOOR = "INDOOR"
    OUTDOOR = "OUTDOOR"
    MARINE = "MARINE"
    CHEMICAL = "CHEMICAL"
    HIGH_TEMP = "HIGH_TEMP"
    CRYOGENIC = "CRYOGENIC"


@dataclass
class MaterialProperties:
    """Complete material properties for compatibility analysis."""
    name: str
    material_type: str  # steel, stainless, aluminum, etc.

    # Mechanical properties
    tensile_strength_mpa: float
    yield_strength_mpa: float
    hardness_hrc: Optional[float] = None

    # Electrochemical properties
    galvanic_series_position: float = 0.0  # mV vs SCE
    passivation: bool = False

    # Thermal properties
    thermal_expansion_coeff: float = 12.0  # μm/m·°C
    max_service_temp_c: float = 200.0
    min_service_temp_c: float = -40.0

    # Chemical resistance
    acid_resistant: bool = False
    alkali_resistant: bool = True
    oxidation_resistant: bool = False


@dataclass
class CompatibilityResult:
    """Material compatibility analysis result."""
    is_compatible: bool
    galvanic_risk: GalvanicRisk
    thermal_compatible: bool
    chemical_compatible: bool
    strength_compatible: bool

    galvanic_potential_mv: float
    thermal_mismatch_um_per_m_c: float

    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class MaterialCompatibilityChecker:
    """
    Comprehensive material compatibility analysis.

    Analyzes:
    - Galvanic corrosion risk
    - Thermal expansion compatibility
    - Chemical compatibility
    - Strength matching
    """

    # Galvanic series (approximate values vs SCE in seawater)
    GALVANIC_SERIES = {
        "magnesium": -1600,
        "zinc": -1100,
        "aluminum_pure": -840,
        "aluminum_6061": -740,
        "aluminum_7075": -730,
        "cadmium": -700,
        "steel": -610,
        "cast_iron": -610,
        "steel_low_alloy": -600,
        "stainless_410": -520,
        "tin": -490,
        "lead": -460,
        "nickel": -250,
        "brass": -270,
        "bronze": -270,
        "copper": -200,
        "stainless_304": -80,
        "stainless_316": -50,
        "monel": -50,
        "titanium": -50,
        "graphite": +250,
        "gold": +250,
        "platinum": +250,
    }

    # Thermal expansion coefficients (μm/m·°C)
    THERMAL_EXPANSION = {
        "steel": 12.0,
        "stainless_304": 17.3,
        "stainless_316": 16.0,
        "aluminum": 23.6,
        "aluminum_6061": 23.6,
        "aluminum_7075": 23.4,
        "copper": 17.0,
        "brass": 19.0,
        "bronze": 18.0,
        "titanium": 8.6,
        "cast_iron": 10.5,
        "magnesium": 26.0,
        "nickel": 13.3,
        "inconel": 12.8,
    }

    # Maximum galvanic potential difference (mV) for risk levels
    GALVANIC_THRESHOLDS = {
        GalvanicRisk.SAFE: 50,       # < 50mV: Safe
        GalvanicRisk.LOW: 150,       # 50-150mV: Low risk
        GalvanicRisk.MODERATE: 300,  # 150-300mV: Moderate risk
        # > 300mV: Severe risk
    }

    def __init__(self):
        pass

    def check_compatibility(
        self,
        material_a: str,
        material_b: str,
        environment: Environment = Environment.INDOOR,
        temperature_range: Tuple[float, float] = (-20, 80),
        require_strength_match: bool = False
    ) -> CompatibilityResult:
        """
        Check compatibility between two materials.

        Args:
            material_a: First material (typically fastener)
            material_b: Second material (typically base)
            environment: Operating environment
            temperature_range: Operating temperature range (min, max) °C
            require_strength_match: Whether strength matching is required

        Returns:
            CompatibilityResult with complete analysis
        """
        warnings = []
        recommendations = []

        # Normalize material names
        mat_a = self._normalize_material_name(material_a)
        mat_b = self._normalize_material_name(material_b)

        # Galvanic compatibility
        galvanic_result = self._check_galvanic_compatibility(
            mat_a, mat_b, environment
        )

        if galvanic_result["risk"] == GalvanicRisk.SEVERE:
            warnings.append(
                f"SEVERE galvanic corrosion risk between {material_a} and {material_b}"
            )
            recommendations.append("Use isolation washer or coating")
            recommendations.append("Consider alternative material pairing")
        elif galvanic_result["risk"] == GalvanicRisk.MODERATE:
            warnings.append(
                f"Moderate galvanic corrosion risk - consider isolation or coating"
            )

        # Thermal compatibility
        thermal_result = self._check_thermal_compatibility(
            mat_a, mat_b, temperature_range
        )

        if not thermal_result["compatible"]:
            warnings.append(
                f"Thermal expansion mismatch: {thermal_result['mismatch']:.1f} μm/m·°C"
            )
            recommendations.append("Consider thermal isolation or flexible mounting")

        # Chemical compatibility (simplified)
        chemical_compatible = self._check_chemical_compatibility(
            mat_a, mat_b, environment
        )

        # Strength matching (simplified)
        strength_compatible = True  # Would need actual values

        # Overall compatibility
        is_compatible = (
            galvanic_result["risk"] != GalvanicRisk.SEVERE and
            thermal_result["compatible"] and
            chemical_compatible and
            (not require_strength_match or strength_compatible)
        )

        return CompatibilityResult(
            is_compatible=is_compatible,
            galvanic_risk=galvanic_result["risk"],
            thermal_compatible=thermal_result["compatible"],
            chemical_compatible=chemical_compatible,
            strength_compatible=strength_compatible,
            galvanic_potential_mv=galvanic_result["potential_diff"],
            thermal_mismatch_um_per_m_c=thermal_result["mismatch"],
            recommendations=recommendations,
            warnings=warnings
        )

    def get_galvanic_risk(
        self,
        material_a: str,
        material_b: str,
        environment: Environment = Environment.INDOOR
    ) -> GalvanicRisk:
        """Quick galvanic risk check between two materials."""
        mat_a = self._normalize_material_name(material_a)
        mat_b = self._normalize_material_name(material_b)

        result = self._check_galvanic_compatibility(mat_a, mat_b, environment)
        return result["risk"]

    def get_thermal_expansion_difference(
        self,
        material_a: str,
        material_b: str
    ) -> float:
        """Get thermal expansion coefficient difference."""
        mat_a = self._normalize_material_name(material_a)
        mat_b = self._normalize_material_name(material_b)

        exp_a = self.THERMAL_EXPANSION.get(mat_a, 12.0)
        exp_b = self.THERMAL_EXPANSION.get(mat_b, 12.0)

        return abs(exp_a - exp_b)

    def calculate_thermal_stress(
        self,
        material_a: str,
        material_b: str,
        length_mm: float,
        delta_temp_c: float,
        youngs_modulus_mpa: float = 200000
    ) -> Dict:
        """
        Calculate thermal stress from expansion mismatch.

        Args:
            material_a: First material
            material_b: Second material
            length_mm: Length of constrained section
            delta_temp_c: Temperature change
            youngs_modulus_mpa: Young's modulus of constraining material

        Returns:
            Dict with expansion difference and induced stress
        """
        mat_a = self._normalize_material_name(material_a)
        mat_b = self._normalize_material_name(material_b)

        exp_a = self.THERMAL_EXPANSION.get(mat_a, 12.0)  # μm/m·°C
        exp_b = self.THERMAL_EXPANSION.get(mat_b, 12.0)

        # Differential expansion
        delta_alpha = abs(exp_a - exp_b) * 1e-6  # Convert to m/m·°C

        # Free expansion difference
        delta_L_mm = delta_alpha * length_mm * delta_temp_c * 1000

        # Thermal strain if fully constrained
        thermal_strain = delta_alpha * delta_temp_c

        # Thermal stress if fully constrained
        thermal_stress_mpa = youngs_modulus_mpa * thermal_strain

        return {
            "expansion_diff_mm": delta_L_mm,
            "thermal_strain": thermal_strain,
            "thermal_stress_mpa": thermal_stress_mpa,
            "warning": "High thermal stress" if thermal_stress_mpa > 100 else None
        }

    def recommend_coating(
        self,
        material_a: str,
        material_b: str,
        environment: Environment
    ) -> List[str]:
        """Recommend protective coatings for material pair."""
        risk = self.get_galvanic_risk(material_a, material_b, environment)

        recommendations = []

        if risk in [GalvanicRisk.MODERATE, GalvanicRisk.SEVERE]:
            if "aluminum" in material_a.lower() or "aluminum" in material_b.lower():
                recommendations.append("Anodize aluminum component")
                recommendations.append("Use cadmium or zinc plated fasteners")

            if "steel" in material_a.lower():
                recommendations.append("Zinc plating (galvanizing)")
                recommendations.append("Zinc-nickel plating for higher corrosion resistance")

            if environment == Environment.MARINE:
                recommendations.append("Consider stainless steel 316 or titanium")
                recommendations.append("Use marine-grade epoxy coating")

            recommendations.append("Install nylon/plastic isolation washers")
            recommendations.append("Apply anti-corrosion compound (e.g., Loctite 7649)")

        return recommendations

    def _normalize_material_name(self, material: str) -> str:
        """Normalize material name for lookup."""
        name = material.lower().strip()
        name = name.replace("-", "_").replace(" ", "_")

        # Common aliases
        aliases = {
            "ss304": "stainless_304",
            "ss316": "stainless_316",
            "al6061": "aluminum_6061",
            "al7075": "aluminum_7075",
            "ss": "stainless_304",
            "carbon_steel": "steel",
            "mild_steel": "steel",
        }

        return aliases.get(name, name)

    def _check_galvanic_compatibility(
        self,
        mat_a: str,
        mat_b: str,
        environment: Environment
    ) -> Dict:
        """Check galvanic corrosion risk."""
        # Get galvanic series positions
        pos_a = self._get_galvanic_position(mat_a)
        pos_b = self._get_galvanic_position(mat_b)

        # Calculate potential difference
        potential_diff = abs(pos_a - pos_b)

        # Determine risk level
        if potential_diff < self.GALVANIC_THRESHOLDS[GalvanicRisk.SAFE]:
            risk = GalvanicRisk.SAFE
        elif potential_diff < self.GALVANIC_THRESHOLDS[GalvanicRisk.LOW]:
            risk = GalvanicRisk.LOW
        elif potential_diff < self.GALVANIC_THRESHOLDS[GalvanicRisk.MODERATE]:
            risk = GalvanicRisk.MODERATE
        else:
            risk = GalvanicRisk.SEVERE

        # Increase risk for harsh environments
        if environment in [Environment.MARINE, Environment.CHEMICAL]:
            if risk == GalvanicRisk.LOW:
                risk = GalvanicRisk.MODERATE
            elif risk == GalvanicRisk.MODERATE:
                risk = GalvanicRisk.SEVERE

        return {
            "risk": risk,
            "potential_diff": potential_diff,
            "anode": mat_a if pos_a < pos_b else mat_b,
            "cathode": mat_b if pos_a < pos_b else mat_a,
        }

    def _get_galvanic_position(self, material: str) -> float:
        """Get galvanic series position for material."""
        # Try exact match first
        if material in self.GALVANIC_SERIES:
            return self.GALVANIC_SERIES[material]

        # Try partial matches
        for key, value in self.GALVANIC_SERIES.items():
            if key in material or material in key:
                return value

        # Default to steel
        return self.GALVANIC_SERIES["steel"]

    def _check_thermal_compatibility(
        self,
        mat_a: str,
        mat_b: str,
        temp_range: Tuple[float, float]
    ) -> Dict:
        """Check thermal expansion compatibility."""
        exp_a = self.THERMAL_EXPANSION.get(mat_a, 12.0)
        exp_b = self.THERMAL_EXPANSION.get(mat_b, 12.0)

        mismatch = abs(exp_a - exp_b)

        # Temperature swing
        delta_t = abs(temp_range[1] - temp_range[0])

        # Compatible if mismatch < 5 μm/m·°C for small temp range
        # or < 3 μm/m·°C for large temp range
        if delta_t > 100:
            threshold = 3.0
        else:
            threshold = 5.0

        compatible = mismatch <= threshold

        return {
            "compatible": compatible,
            "mismatch": mismatch,
            "exp_a": exp_a,
            "exp_b": exp_b,
        }

    def _check_chemical_compatibility(
        self,
        mat_a: str,
        mat_b: str,
        environment: Environment
    ) -> bool:
        """Check chemical compatibility (simplified)."""
        # Special case checks
        if environment == Environment.CHEMICAL:
            # Aluminum not suitable for alkaline environments
            if "aluminum" in mat_a or "aluminum" in mat_b:
                return False

        return True


# Convenience function for quick galvanic risk lookup
def get_galvanic_risk_matrix() -> Dict[Tuple[str, str], GalvanicRisk]:
    """
    Get complete galvanic risk matrix for common materials.

    Returns:
        Dictionary mapping (material_a, material_b) to GalvanicRisk
    """
    checker = MaterialCompatibilityChecker()
    materials = [
        "steel", "stainless_304", "stainless_316",
        "aluminum", "brass", "copper", "titanium"
    ]

    matrix = {}
    for a in materials:
        for b in materials:
            risk = checker.get_galvanic_risk(a, b)
            matrix[(a, b)] = risk

    return matrix
