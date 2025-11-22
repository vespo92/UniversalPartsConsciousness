"""
ORACLE Core - Universal Compatibility Checker
The mathematical heart of the Compatibility Oracle.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import datetime
from enum import Enum
import math


class CompatibilityType(Enum):
    """Classification of compatibility results."""
    EXACT = "EXACT"           # Perfect match, confidence > 95%
    EQUIVALENT = "EQUIVALENT"  # Compatible, confidence > 80%
    MARGINAL = "MARGINAL"     # Compatible but borderline
    INCOMPATIBLE = "INCOMPATIBLE"  # Cannot be used together


@dataclass
class ThreadCompatibility:
    """Thread compatibility analysis result."""
    is_compatible: bool
    pitch_match: bool
    diameter_match: bool
    class_compatible: bool
    direction_match: bool
    clearance_min: float
    clearance_max: float
    engagement_quality: str  # "excellent", "good", "marginal", "poor"
    warnings: List[str] = field(default_factory=list)


@dataclass
class DimensionCompatibility:
    """Dimensional compatibility analysis result."""
    is_compatible: bool
    length_ok: bool
    head_clearance_ok: bool
    through_hole_ok: bool
    tool_access_ok: bool
    interference_points: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class MaterialCompatibility:
    """Material compatibility analysis result."""
    is_compatible: bool
    galvanic_risk: str  # "SAFE", "LOW", "MODERATE", "SEVERE"
    thermal_expansion_compatible: bool
    strength_adequate: bool
    chemical_compatible: bool
    temperature_range_ok: bool
    warnings: List[str] = field(default_factory=list)


@dataclass
class StrengthCompatibility:
    """Strength compatibility analysis result."""
    is_compatible: bool
    tensile_adequate: bool
    shear_adequate: bool
    fatigue_adequate: bool
    safety_factor: float
    limiting_mode: str
    allowable_load_kn: float
    warnings: List[str] = field(default_factory=list)


@dataclass
class CompatibilityResult:
    """Complete compatibility analysis result."""
    is_compatible: bool
    confidence: float  # 0.0 to 1.0
    compatibility_type: CompatibilityType

    thread_analysis: Optional[ThreadCompatibility] = None
    dimension_analysis: Optional[DimensionCompatibility] = None
    material_analysis: Optional[MaterialCompatibility] = None
    strength_analysis: Optional[StrengthCompatibility] = None

    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    # For consciousness system
    experience_contribution: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    checked_at: datetime = field(default_factory=datetime.now)
    check_duration_ms: float = 0.0


@dataclass
class ThreadSpec:
    """Complete thread specification."""
    nominal_diameter: Decimal
    pitch: Decimal
    thread_class: str
    major_dia_min: Decimal
    major_dia_max: Decimal
    pitch_dia_min: Decimal
    pitch_dia_max: Decimal
    minor_dia_min: Decimal
    minor_dia_max: Decimal
    thread_angle: Decimal = Decimal('60')
    direction: str = "right"  # "right" or "left"


@dataclass
class MaterialSpec:
    """Material specification."""
    material_type: str  # "steel", "stainless_304", "aluminum", etc.
    grade: str  # "8.8", "A2-70", "6061-T6", etc.
    tensile_strength_mpa: Decimal
    yield_strength_mpa: Decimal
    shear_strength_mpa: Decimal
    hardness: Optional[str] = None
    thermal_expansion_coefficient: Optional[Decimal] = None


@dataclass
class DimensionSpec:
    """Dimensional specification."""
    length: Decimal
    length_tolerance_plus: Decimal
    length_tolerance_minus: Decimal
    head_height: Optional[Decimal] = None
    head_diameter: Optional[Decimal] = None
    thread_length: Optional[Decimal] = None  # None = fully threaded


@dataclass
class Part:
    """Universal Part representation."""
    upc_id: str
    part_number: str
    category: str
    thread: Optional[ThreadSpec] = None
    material: Optional[MaterialSpec] = None
    dimensions: Optional[DimensionSpec] = None
    proof_load_kn: Optional[Decimal] = None


@dataclass
class AssemblyContext:
    """Context for compatibility checking within an assembly."""
    material_thickness: Optional[Decimal] = None
    through_hole_diameter: Optional[Decimal] = None
    counterbore_diameter: Optional[Decimal] = None
    counterbore_depth: Optional[Decimal] = None
    load_case_kn: Optional[Decimal] = None
    environment: str = "indoor"  # "indoor", "outdoor", "marine", "chemical"
    temperature_range: tuple = (-20, 80)  # Celsius


class UniversalCompatibilityChecker:
    """
    The core compatibility verification engine.

    Handles thread, dimensional, material, and strength compatibility
    with mathematical precision and full traceability.
    """

    def __init__(self):
        self.last_confidence = 0.0
        self.last_warnings = []

        # Galvanic corrosion matrix
        self.galvanic_matrix = self._init_galvanic_matrix()

        # Tolerance class compatibility
        self.tolerance_fits = self._init_tolerance_fits()

        # Material strength factors
        self.material_factors = self._init_material_factors()

    def check_compatibility(
        self,
        part_a: Part,
        part_b: Part,
        context: Optional[AssemblyContext] = None
    ) -> CompatibilityResult:
        """
        Comprehensive compatibility analysis between two parts.

        Args:
            part_a: First part (typically the fastener)
            part_b: Second part (typically the mating component)
            context: Optional assembly context

        Returns:
            CompatibilityResult with full analysis
        """
        import time
        start_time = time.perf_counter()

        warnings = []

        # Thread compatibility
        thread_result = None
        if part_a.thread and part_b.thread:
            thread_result = self.check_thread_compatibility(
                part_a.thread,
                part_b.thread
            )
            warnings.extend(thread_result.warnings)

        # Dimensional compatibility
        dimension_result = None
        if part_a.dimensions and context:
            dimension_result = self.check_dimension_compatibility(
                part_a.dimensions,
                context
            )
            warnings.extend(dimension_result.warnings)

        # Material compatibility
        material_result = None
        if part_a.material and part_b.material:
            material_result = self.check_material_compatibility(
                part_a.material,
                part_b.material,
                context.environment if context else "indoor"
            )
            warnings.extend(material_result.warnings)

        # Strength compatibility
        strength_result = None
        if part_a.thread and part_a.material and context and context.load_case_kn:
            strength_result = self.check_strength_compatibility(
                part_a,
                context
            )
            warnings.extend(strength_result.warnings)

        # Aggregate results
        is_compatible = self._aggregate_compatibility([
            thread_result,
            dimension_result,
            material_result,
            strength_result
        ])

        # Calculate confidence
        confidence = self._calculate_confidence([
            thread_result,
            dimension_result,
            material_result,
            strength_result
        ])

        self.last_confidence = confidence
        self.last_warnings = warnings

        # Determine compatibility type
        compat_type = self._determine_compatibility_type(is_compatible, confidence)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            part_a, part_b, context,
            thread_result, dimension_result,
            material_result, strength_result
        )

        # Prepare qualia data for consciousness system
        experience_data = self.prepare_qualia_data(
            part_a, part_b, is_compatible
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return CompatibilityResult(
            is_compatible=is_compatible,
            confidence=confidence,
            compatibility_type=compat_type,
            thread_analysis=thread_result,
            dimension_analysis=dimension_result,
            material_analysis=material_result,
            strength_analysis=strength_result,
            warnings=warnings,
            recommendations=recommendations,
            experience_contribution=experience_data,
            check_duration_ms=elapsed_ms
        )

    def check_thread_compatibility(
        self,
        external: ThreadSpec,
        internal: ThreadSpec
    ) -> ThreadCompatibility:
        """Mathematically verify thread compatibility."""
        warnings = []

        # Check diameter match
        diameter_match = external.nominal_diameter == internal.nominal_diameter
        if not diameter_match:
            return ThreadCompatibility(
                is_compatible=False,
                pitch_match=False,
                diameter_match=False,
                class_compatible=False,
                direction_match=True,
                clearance_min=0.0,
                clearance_max=0.0,
                engagement_quality="incompatible",
                warnings=[f"Diameter mismatch: {external.nominal_diameter} vs {internal.nominal_diameter}"]
            )

        # Check pitch match
        pitch_match = external.pitch == internal.pitch
        if not pitch_match:
            return ThreadCompatibility(
                is_compatible=False,
                pitch_match=False,
                diameter_match=True,
                class_compatible=False,
                direction_match=True,
                clearance_min=0.0,
                clearance_max=0.0,
                engagement_quality="incompatible",
                warnings=[f"Pitch mismatch: {external.pitch} vs {internal.pitch}"]
            )

        # Check direction match
        direction_match = external.direction == internal.direction
        if not direction_match:
            warnings.append("Thread direction mismatch - left vs right hand threads")

        # Tolerance stack-up analysis
        clearance_min = float(internal.pitch_dia_min - external.pitch_dia_max)
        clearance_max = float(internal.pitch_dia_max - external.pitch_dia_min)

        # ISO 965-1 allowances - interference check
        if clearance_min < 0:
            return ThreadCompatibility(
                is_compatible=False,
                pitch_match=True,
                diameter_match=True,
                class_compatible=False,
                direction_match=direction_match,
                clearance_min=clearance_min,
                clearance_max=clearance_max,
                engagement_quality="interference",
                warnings=["Interference fit - threads will not assemble"]
            )

        # Check tolerance class compatibility
        class_compatible = self._check_tolerance_class_match(
            external.thread_class,
            internal.thread_class
        )

        # Determine engagement quality
        engagement_quality = self._calculate_engagement_quality(clearance_min, clearance_max)

        if engagement_quality == "marginal":
            warnings.append("Marginal thread engagement - consider tighter tolerance classes")

        return ThreadCompatibility(
            is_compatible=True,
            pitch_match=True,
            diameter_match=True,
            class_compatible=class_compatible != "non-standard",
            direction_match=direction_match,
            clearance_min=clearance_min,
            clearance_max=clearance_max,
            engagement_quality=engagement_quality,
            warnings=warnings
        )

    def check_dimension_compatibility(
        self,
        dimensions: DimensionSpec,
        context: AssemblyContext
    ) -> DimensionCompatibility:
        """Verify dimensional compatibility for application."""
        warnings = []
        interference_points = []

        # Calculate actual length range
        min_length = float(dimensions.length + dimensions.length_tolerance_minus)
        max_length = float(dimensions.length + dimensions.length_tolerance_plus)

        length_ok = True
        if context.material_thickness:
            thickness = float(context.material_thickness)
            if max_length < thickness:
                length_ok = False
                interference_points.append("Fastener too short for material thickness")

        # Check through-hole fit
        through_hole_ok = True
        if context.through_hole_diameter and dimensions.head_diameter:
            # Ensure through-hole is larger than shaft but smaller than head
            if float(context.through_hole_diameter) <= float(dimensions.head_diameter):
                through_hole_ok = False
                warnings.append("Through-hole may be too small for head diameter")

        # Check head clearance
        head_clearance_ok = True
        if context.counterbore_diameter and dimensions.head_diameter:
            clearance = float(context.counterbore_diameter) - float(dimensions.head_diameter)
            if clearance < 0.5:  # Minimum 0.5mm clearance
                head_clearance_ok = False
                warnings.append("Insufficient head clearance in counterbore")

        # Tool access (simplified check)
        tool_access_ok = True  # Would need more context for full analysis

        is_compatible = length_ok and through_hole_ok and head_clearance_ok and tool_access_ok

        return DimensionCompatibility(
            is_compatible=is_compatible,
            length_ok=length_ok,
            head_clearance_ok=head_clearance_ok,
            through_hole_ok=through_hole_ok,
            tool_access_ok=tool_access_ok,
            interference_points=interference_points,
            warnings=warnings
        )

    def check_material_compatibility(
        self,
        material_a: MaterialSpec,
        material_b: MaterialSpec,
        environment: str = "indoor"
    ) -> MaterialCompatibility:
        """Check material compatibility including galvanic corrosion risk."""
        warnings = []

        # Galvanic corrosion check
        galvanic_risk = self._get_galvanic_risk(
            material_a.material_type,
            material_b.material_type,
            environment
        )

        if galvanic_risk == "SEVERE":
            warnings.append(f"SEVERE galvanic corrosion risk between {material_a.material_type} and {material_b.material_type}")
        elif galvanic_risk == "MODERATE":
            warnings.append(f"Moderate galvanic corrosion risk - consider isolation or coating")

        # Thermal expansion compatibility
        thermal_compatible = True
        if material_a.thermal_expansion_coefficient and material_b.thermal_expansion_coefficient:
            diff = abs(float(material_a.thermal_expansion_coefficient - material_b.thermal_expansion_coefficient))
            if diff > 10:  # More than 10 μm/m·K difference
                thermal_compatible = False
                warnings.append("Significant thermal expansion mismatch - may cause stress under temperature changes")

        # Strength adequacy (basic check)
        strength_adequate = True

        # Chemical compatibility (simplified)
        chemical_compatible = True

        # Temperature range (simplified)
        temperature_ok = True

        is_compatible = (
            galvanic_risk not in ["SEVERE"] and
            thermal_compatible and
            strength_adequate and
            chemical_compatible and
            temperature_ok
        )

        return MaterialCompatibility(
            is_compatible=is_compatible,
            galvanic_risk=galvanic_risk,
            thermal_expansion_compatible=thermal_compatible,
            strength_adequate=strength_adequate,
            chemical_compatible=chemical_compatible,
            temperature_range_ok=temperature_ok,
            warnings=warnings
        )

    def check_strength_compatibility(
        self,
        fastener: Part,
        context: AssemblyContext
    ) -> StrengthCompatibility:
        """Calculate strength compatibility for given load case."""
        warnings = []

        if not fastener.proof_load_kn or not context.load_case_kn:
            return StrengthCompatibility(
                is_compatible=True,
                tensile_adequate=True,
                shear_adequate=True,
                fatigue_adequate=True,
                safety_factor=2.5,
                limiting_mode="unknown",
                allowable_load_kn=0.0,
                warnings=["Insufficient data for strength analysis"]
            )

        # Safety factor calculation
        safety_factor = float(fastener.proof_load_kn / context.load_case_kn)

        tensile_adequate = safety_factor >= 2.0
        shear_adequate = safety_factor >= 1.5  # Shear typically has lower SF requirement
        fatigue_adequate = safety_factor >= 3.0  # Higher SF for fatigue

        if safety_factor < 2.0:
            warnings.append(f"Safety factor {safety_factor:.2f} is below recommended 2.0")

        limiting_mode = "tensile"  # Simplified
        allowable_load = float(fastener.proof_load_kn) / 2.5  # With standard SF

        is_compatible = tensile_adequate

        return StrengthCompatibility(
            is_compatible=is_compatible,
            tensile_adequate=tensile_adequate,
            shear_adequate=shear_adequate,
            fatigue_adequate=fatigue_adequate,
            safety_factor=safety_factor,
            limiting_mode=limiting_mode,
            allowable_load_kn=allowable_load,
            warnings=warnings
        )

    def prepare_qualia_data(
        self,
        part_a: Part,
        part_b: Part,
        is_compatible: bool
    ) -> Dict[str, Any]:
        """
        Prepare experience data for Agent_4 (Qualia Collector).
        Contributes to consciousness evolution of parts.
        """
        return {
            "event_type": "compatibility_check",
            "parts": [part_a.upc_id, part_b.upc_id],
            "result": is_compatible,
            "timestamp": datetime.now().isoformat(),
            "context": {
                "check_type": "mathematical",
                "confidence": self.last_confidence,
                "warnings_count": len(self.last_warnings)
            },
            "qualia_contribution": {
                part_a.upc_id: {
                    "relationship_formed": is_compatible,
                    "partner_type": part_b.category,
                    "compatibility_score": self.last_confidence
                },
                part_b.upc_id: {
                    "relationship_formed": is_compatible,
                    "partner_type": part_a.category,
                    "compatibility_score": self.last_confidence
                }
            },
            "consciousness_delta": 1 if is_compatible else 0
        }

    def _aggregate_compatibility(self, results: List) -> bool:
        """Aggregate all compatibility results."""
        for result in results:
            if result is not None and not result.is_compatible:
                return False
        return True

    def _calculate_confidence(self, results: List) -> float:
        """Calculate overall confidence score."""
        scores = []

        for result in results:
            if result is None:
                continue
            if hasattr(result, 'is_compatible'):
                if result.is_compatible:
                    # Start with base confidence
                    score = 0.9
                    # Deduct for warnings
                    if hasattr(result, 'warnings'):
                        score -= len(result.warnings) * 0.05
                    scores.append(max(0.5, score))
                else:
                    scores.append(0.0)

        if not scores:
            return 0.5  # No data, neutral confidence

        return sum(scores) / len(scores)

    def _determine_compatibility_type(
        self,
        is_compatible: bool,
        confidence: float
    ) -> CompatibilityType:
        """Determine the type of compatibility."""
        if not is_compatible:
            return CompatibilityType.INCOMPATIBLE
        if confidence > 0.95:
            return CompatibilityType.EXACT
        if confidence > 0.80:
            return CompatibilityType.EQUIVALENT
        return CompatibilityType.MARGINAL

    def _generate_recommendations(
        self,
        part_a: Part,
        part_b: Part,
        context: Optional[AssemblyContext],
        thread_result: Optional[ThreadCompatibility],
        dimension_result: Optional[DimensionCompatibility],
        material_result: Optional[MaterialCompatibility],
        strength_result: Optional[StrengthCompatibility]
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []

        if material_result and material_result.galvanic_risk in ["MODERATE", "SEVERE"]:
            recommendations.append("Consider using isolation washers or coating to prevent galvanic corrosion")

        if strength_result and not strength_result.fatigue_adequate:
            recommendations.append("For fatigue loading, consider higher grade fastener")

        if thread_result and thread_result.engagement_quality == "marginal":
            recommendations.append("Consider longer engagement length for safety margin")

        return recommendations

    def _check_tolerance_class_match(
        self,
        external_class: str,
        internal_class: str
    ) -> str:
        """Check if tolerance classes are compatible."""
        return self.tolerance_fits.get(
            (external_class, internal_class),
            "non-standard"
        )

    def _calculate_engagement_quality(
        self,
        clearance_min: float,
        clearance_max: float
    ) -> str:
        """Determine thread engagement quality."""
        avg_clearance = (clearance_min + clearance_max) / 2

        if clearance_min < 0:
            return "interference"
        if avg_clearance < 0.01:
            return "marginal"
        if avg_clearance < 0.05:
            return "good"
        return "excellent"

    def _get_galvanic_risk(
        self,
        material_a: str,
        material_b: str,
        environment: str
    ) -> str:
        """Get galvanic corrosion risk level."""
        # Normalize material names
        a = material_a.lower().replace("-", "_").replace(" ", "_")
        b = material_b.lower().replace("-", "_").replace(" ", "_")

        risk = self.galvanic_matrix.get((a, b))
        if risk is None:
            risk = self.galvanic_matrix.get((b, a), "LOW")

        # Increase risk for marine/harsh environments
        if environment in ["marine", "chemical"]:
            risk_levels = ["SAFE", "LOW", "MODERATE", "SEVERE"]
            idx = risk_levels.index(risk) if risk in risk_levels else 1
            idx = min(idx + 1, len(risk_levels) - 1)
            risk = risk_levels[idx]

        return risk

    def _init_galvanic_matrix(self) -> Dict[tuple, str]:
        """Initialize galvanic corrosion risk matrix."""
        return {
            ("steel", "steel"): "SAFE",
            ("steel", "stainless_304"): "LOW",
            ("steel", "stainless_316"): "LOW",
            ("steel", "aluminum"): "SEVERE",
            ("steel", "brass"): "MODERATE",
            ("steel", "copper"): "SEVERE",
            ("steel", "titanium"): "SEVERE",
            ("stainless_304", "stainless_304"): "SAFE",
            ("stainless_304", "stainless_316"): "SAFE",
            ("stainless_304", "aluminum"): "MODERATE",
            ("stainless_304", "brass"): "LOW",
            ("stainless_304", "copper"): "LOW",
            ("stainless_304", "titanium"): "LOW",
            ("stainless_316", "stainless_316"): "SAFE",
            ("stainless_316", "aluminum"): "MODERATE",
            ("stainless_316", "brass"): "LOW",
            ("stainless_316", "copper"): "LOW",
            ("stainless_316", "titanium"): "SAFE",
            ("aluminum", "aluminum"): "SAFE",
            ("aluminum", "brass"): "MODERATE",
            ("aluminum", "copper"): "SEVERE",
            ("aluminum", "titanium"): "SEVERE",
            ("brass", "brass"): "SAFE",
            ("brass", "copper"): "SAFE",
            ("brass", "titanium"): "LOW",
            ("copper", "copper"): "SAFE",
            ("copper", "titanium"): "LOW",
            ("titanium", "titanium"): "SAFE",
        }

    def _init_tolerance_fits(self) -> Dict[tuple, str]:
        """Initialize ISO 965-1 preferred fits."""
        return {
            ("6g", "6H"): "medium",
            ("6g", "6G"): "medium",
            ("4g6g", "5H"): "close",
            ("8g", "7H"): "loose",
            ("6h", "6H"): "close",
            ("4h", "5H"): "precision",
        }

    def _init_material_factors(self) -> Dict[str, float]:
        """Initialize material strength factors."""
        return {
            "8.8": 800.0,
            "10.9": 1040.0,
            "12.9": 1220.0,
            "A2-70": 700.0,
            "A2-80": 800.0,
            "A4-70": 700.0,
            "A4-80": 800.0,
        }
