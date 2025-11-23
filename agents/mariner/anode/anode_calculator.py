"""
Sacrificial Anode Calculator

Proper anode sizing prevents galvanic corrosion of expensive underwater
hardware. This module calculates anode requirements based on:
- Hull material and wetted area
- Propeller and shaft materials
- Through-hull fittings
- Operating environment (salt, brackish, fresh)

Anode Types:
- Zinc: Saltwater standard (MIL-A-18001K)
- Aluminum: Brackish water and versatile (MIL-DTL-24779)
- Magnesium: Freshwater only (ASTM B843)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class AnodeType(Enum):
    """Types of sacrificial anodes"""
    ZINC = "zinc"               # Saltwater standard
    ALUMINUM = "aluminum"       # Brackish, versatile
    MAGNESIUM = "magnesium"     # Freshwater only


class AnodePlacement(Enum):
    """Standard anode placement locations"""
    HULL = "hull"               # Hull anodes (bolt-on or weld-on)
    SHAFT = "shaft"             # Shaft collar anodes
    PROPELLER = "propeller"     # Prop nut or hub anodes
    TRIM_TAB = "trim_tab"       # Trim tab anodes
    RUDDER = "rudder"           # Rudder anodes
    THROUGH_HULL = "through_hull"  # Pencil anodes in heat exchangers
    SWIM_PLATFORM = "swim_platform"  # Platform protection
    OUTDRIVE = "outdrive"       # Sterndrive anodes


@dataclass
class AnodeSpec:
    """Specification for a specific anode"""
    part_number: str
    manufacturer: str
    type: AnodeType
    placement: AnodePlacement
    weight_lbs: float
    surface_area_sq_in: float
    dimensions: str
    material_spec: str           # MIL-A-18001K, etc.
    fits: List[str]              # Compatible applications
    price_range_usd: Tuple[float, float]


@dataclass
class AnodeRecommendation:
    """Recommendation for anode installation"""
    placement: AnodePlacement
    anode_type: AnodeType
    quantity: int
    size: str
    part_number: Optional[str]
    surface_area_sq_in: float
    installation_notes: str
    replacement_interval: str


@dataclass
class AnodeSystemAssessment:
    """Complete assessment of anode system requirements"""
    hull_material: str
    wetted_area_sq_ft: float
    environment: str
    total_required_area_sq_in: float
    recommended_anodes: List[AnodeRecommendation]
    anode_type: AnodeType
    inspection_interval: str
    replacement_threshold: str
    warnings: List[str]
    cost_estimate_annual: float


class SacrificialAnodeCalculator:
    """
    Calculator for sacrificial anode system sizing.

    Based on industry standards and manufacturer recommendations.
    """

    def __init__(self):
        self.anode_catalog: Dict[str, AnodeSpec] = self._build_anode_catalog()

    def _build_anode_catalog(self) -> Dict[str, AnodeSpec]:
        """Build catalog of available anodes"""
        return {
            # Mercruiser/Mercury
            "cm-821629": AnodeSpec(
                part_number="CM-821629",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.HULL,
                weight_lbs=1.0,
                surface_area_sq_in=12,
                dimensions="4\" x 2\" x 1\"",
                material_spec="MIL-A-18001K",
                fits=["Small hulls", "Trim tabs"],
                price_range_usd=(12, 18),
            ),
            "cm-821630": AnodeSpec(
                part_number="CM-821630",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.HULL,
                weight_lbs=2.5,
                surface_area_sq_in=28,
                dimensions="6\" x 3\" x 1.5\"",
                material_spec="MIL-A-18001K",
                fits=["Medium hulls", "20-30ft boats"],
                price_range_usd=(22, 32),
            ),
            "cm-821631": AnodeSpec(
                part_number="CM-821631",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.HULL,
                weight_lbs=5.0,
                surface_area_sq_in=45,
                dimensions="8\" x 4\" x 2\"",
                material_spec="MIL-A-18001K",
                fits=["Large hulls", "30ft+ boats"],
                price_range_usd=(35, 50),
            ),
            "cm-55989": AnodeSpec(
                part_number="CM-55989",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.SHAFT,
                weight_lbs=0.75,
                surface_area_sq_in=8,
                dimensions="1\" shaft collar",
                material_spec="MIL-A-18001K",
                fits=["1\" propeller shafts"],
                price_range_usd=(18, 25),
            ),
            "cm-55989-1.25": AnodeSpec(
                part_number="CM-55989-1.25",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.SHAFT,
                weight_lbs=1.0,
                surface_area_sq_in=12,
                dimensions="1.25\" shaft collar",
                material_spec="MIL-A-18001K",
                fits=["1.25\" propeller shafts"],
                price_range_usd=(22, 30),
            ),
            # Aluminum anodes (brackish)
            "cma-821629a": AnodeSpec(
                part_number="CMA-821629A",
                manufacturer="Martyr",
                type=AnodeType.ALUMINUM,
                placement=AnodePlacement.HULL,
                weight_lbs=1.0,
                surface_area_sq_in=12,
                dimensions="4\" x 2\" x 1\"",
                material_spec="MIL-DTL-24779",
                fits=["Brackish water", "Versatile"],
                price_range_usd=(15, 22),
            ),
            # Magnesium (freshwater)
            "cmm-821629m": AnodeSpec(
                part_number="CMM-821629M",
                manufacturer="Martyr",
                type=AnodeType.MAGNESIUM,
                placement=AnodePlacement.HULL,
                weight_lbs=1.0,
                surface_area_sq_in=12,
                dimensions="4\" x 2\" x 1\"",
                material_spec="ASTM B843 Type M1C",
                fits=["Freshwater ONLY", "Lakes and rivers"],
                price_range_usd=(18, 26),
            ),
            # Outdrive anodes
            "alpha_gen2_kit": AnodeSpec(
                part_number="CMM-ALPHA2KIT",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.OUTDRIVE,
                weight_lbs=2.5,
                surface_area_sq_in=35,
                dimensions="Kit",
                material_spec="MIL-A-18001K",
                fits=["Mercruiser Alpha Gen II"],
                price_range_usd=(45, 65),
            ),
            "bravo_kit": AnodeSpec(
                part_number="CMM-BRAVOKIT",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.OUTDRIVE,
                weight_lbs=4.0,
                surface_area_sq_in=50,
                dimensions="Kit",
                material_spec="MIL-A-18001K",
                fits=["Mercruiser Bravo I/II/III"],
                price_range_usd=(85, 120),
            ),
            "volvo_sx_kit": AnodeSpec(
                part_number="CMM-VOLVOSX",
                manufacturer="Martyr",
                type=AnodeType.ZINC,
                placement=AnodePlacement.OUTDRIVE,
                weight_lbs=3.5,
                surface_area_sq_in=45,
                dimensions="Kit",
                material_spec="MIL-A-18001K",
                fits=["Volvo Penta SX"],
                price_range_usd=(75, 100),
            ),
            # Pencil anodes
            "pencil_3/8": AnodeSpec(
                part_number="CM-PENCIL-3/8",
                manufacturer="Various",
                type=AnodeType.ZINC,
                placement=AnodePlacement.THROUGH_HULL,
                weight_lbs=0.1,
                surface_area_sq_in=2,
                dimensions="3/8\" x 2\"",
                material_spec="MIL-A-18001K",
                fits=["Heat exchangers", "Engine blocks"],
                price_range_usd=(3, 6),
            ),
        }

    def determine_anode_type(
        self,
        water_type: str,
        hull_material: str = "fiberglass"
    ) -> Tuple[AnodeType, str]:
        """
        Determine the appropriate anode type for operating conditions.

        CRITICAL: Using wrong anode type causes either:
        - No protection (zinc in freshwater)
        - Damage to hull (magnesium in saltwater on aluminum)
        """
        water_lower = water_type.lower()
        hull_lower = hull_material.lower()

        # Freshwater
        if "fresh" in water_lower or "lake" in water_lower or "river" in water_lower:
            if "aluminum" in hull_lower:
                return (AnodeType.MAGNESIUM,
                       "Magnesium for freshwater. NEVER use zinc - won't protect in low conductivity.")
            else:
                return (AnodeType.MAGNESIUM,
                       "Magnesium for freshwater. Zinc is ineffective in fresh water.")

        # Saltwater
        if "salt" in water_lower or "ocean" in water_lower or "sea" in water_lower:
            if "aluminum" in hull_lower:
                return (AnodeType.ZINC,
                       "Zinc for saltwater aluminum. WARNING: Magnesium is too active and can damage aluminum hulls.")
            else:
                return (AnodeType.ZINC,
                       "Zinc - standard for saltwater. MIL-A-18001K specification.")

        # Brackish
        if "brackish" in water_lower or "estuary" in water_lower:
            return (AnodeType.ALUMINUM,
                   "Aluminum anodes - works in both salt and brackish. More versatile than zinc.")

        # Default to zinc (safer assumption)
        return (AnodeType.ZINC, "Defaulting to zinc - verify water type for optimal protection.")

    def calculate_required_area(
        self,
        wetted_area_sq_ft: float,
        hull_material: str,
        propeller_material: str,
        shaft_material: str,
        num_thru_hulls: int = 0,
        environment: str = "saltwater"
    ) -> Dict:
        """
        Calculate total required anode surface area.

        Based on industry standard formulas:
        - 1% of wetted area for aluminum hulls
        - 2% of wetted area for fiberglass/steel with bronze/stainless hardware
        """
        hull_lower = hull_material.lower()
        env_lower = environment.lower()

        # Base calculation
        if "aluminum" in hull_lower:
            # Aluminum hulls need 1% rule
            base_area = wetted_area_sq_ft * 144 * 0.01  # Convert to sq.in, 1%
            hull_note = "Aluminum hull - using 1% rule"
        else:
            # Fiberglass/steel need 2% for hardware protection
            base_area = wetted_area_sq_ft * 144 * 0.02  # 2%
            hull_note = "Fiberglass/steel hull - using 2% rule for hardware"

        # Environment factor
        if "fresh" in env_lower:
            env_factor = 0.3
            env_note = "Freshwater - lower conductivity reduces corrosion rate"
        elif "brackish" in env_lower:
            env_factor = 0.7
            env_note = "Brackish water - moderate protection needed"
        else:
            env_factor = 1.0
            env_note = "Saltwater - full protection required"

        # Propeller factor
        prop_lower = propeller_material.lower()
        prop_factor = 1.0
        prop_note = ""
        if "bronze" in prop_lower:
            prop_factor = 1.2
            prop_note = "Bronze propeller - additional protection needed"
        elif "stainless" in prop_lower or "nibral" in prop_lower:
            prop_factor = 1.3
            prop_note = "Stainless/NiBrAl propeller - increased cathode area"
        elif "aluminum" in prop_lower:
            prop_factor = 0.8
            prop_note = "Aluminum propeller - similar potential to anodes"

        # Through-hull factor
        thru_hull_area = num_thru_hulls * 3  # ~3 sq.in per thru-hull

        # Calculate total
        total_area = (base_area * env_factor * prop_factor) + thru_hull_area

        return {
            "base_area_sq_in": base_area,
            "environment_factor": env_factor,
            "propeller_factor": prop_factor,
            "thru_hull_area": thru_hull_area,
            "total_required_sq_in": total_area,
            "notes": [hull_note, env_note, prop_note] if prop_note else [hull_note, env_note],
        }

    def recommend_anode_system(
        self,
        wetted_area_sq_ft: float,
        hull_material: str,
        propeller_material: str,
        shaft_material: str,
        shaft_diameter_in: float,
        drive_type: str,  # "inboard", "sterndrive", "outboard"
        environment: str = "saltwater",
        num_thru_hulls: int = 2
    ) -> AnodeSystemAssessment:
        """
        Generate complete anode system recommendation.

        Args:
            wetted_area_sq_ft: Underwater hull area
            hull_material: Hull construction material
            propeller_material: Prop material
            shaft_material: Shaft material
            shaft_diameter_in: Shaft diameter
            drive_type: Propulsion type
            environment: Water type
            num_thru_hulls: Number of bronze thru-hulls

        Returns:
            Complete system assessment with recommendations
        """
        warnings = []

        # Determine anode type
        anode_type, type_note = self.determine_anode_type(environment, hull_material)
        warnings.append(type_note)

        # Calculate required area
        area_calc = self.calculate_required_area(
            wetted_area_sq_ft,
            hull_material,
            propeller_material,
            shaft_material,
            num_thru_hulls,
            environment
        )

        recommendations = []
        remaining_area = area_calc["total_required_sq_in"]
        total_cost_low = 0
        total_cost_high = 0

        # Always recommend shaft anode for inboards
        if drive_type.lower() in ["inboard", "v-drive"]:
            shaft_anode = self._select_shaft_anode(shaft_diameter_in, anode_type)
            if shaft_anode:
                recommendations.append(AnodeRecommendation(
                    placement=AnodePlacement.SHAFT,
                    anode_type=anode_type,
                    quantity=1,
                    size=shaft_anode.dimensions,
                    part_number=shaft_anode.part_number,
                    surface_area_sq_in=shaft_anode.surface_area_sq_in,
                    installation_notes="Collar anode - install tight to prop, replace when 50% gone",
                    replacement_interval="Annually or when 50% depleted"
                ))
                remaining_area -= shaft_anode.surface_area_sq_in
                total_cost_low += shaft_anode.price_range_usd[0]
                total_cost_high += shaft_anode.price_range_usd[1]

        # Sterndrive - recommend drive kit
        if drive_type.lower() == "sterndrive":
            drive_kit = self._select_drive_kit(anode_type)
            if drive_kit:
                recommendations.append(AnodeRecommendation(
                    placement=AnodePlacement.OUTDRIVE,
                    anode_type=anode_type,
                    quantity=1,
                    size="Complete kit",
                    part_number=drive_kit.part_number,
                    surface_area_sq_in=drive_kit.surface_area_sq_in,
                    installation_notes="Replace all drive anodes as a set",
                    replacement_interval="Annually or when 50% depleted"
                ))
                remaining_area -= drive_kit.surface_area_sq_in
                total_cost_low += drive_kit.price_range_usd[0]
                total_cost_high += drive_kit.price_range_usd[1]

        # Hull anodes for remaining protection
        if remaining_area > 0:
            hull_anodes = self._calculate_hull_anodes(remaining_area, anode_type)
            for rec in hull_anodes:
                recommendations.append(rec)
                # Estimate cost
                total_cost_low += rec.quantity * 15
                total_cost_high += rec.quantity * 35

        # Pencil anodes for through-hulls
        if num_thru_hulls > 0:
            recommendations.append(AnodeRecommendation(
                placement=AnodePlacement.THROUGH_HULL,
                anode_type=anode_type,
                quantity=num_thru_hulls * 2,  # 2 pencils per thru-hull typical
                size="3/8\" x 2\" pencil",
                part_number="CM-PENCIL-3/8",
                surface_area_sq_in=num_thru_hulls * 4,
                installation_notes="Install in heat exchangers and engine blocks",
                replacement_interval="Every 6 months - inspect frequently"
            ))

        # Set inspection interval based on environment
        if "salt" in environment.lower():
            inspection = "Monthly visual inspection"
        elif "brackish" in environment.lower():
            inspection = "Every 2 months"
        else:
            inspection = "Quarterly"

        # Add warnings
        if "aluminum" in hull_material.lower():
            warnings.append("ALUMINUM HULL: Ensure anodes have good electrical contact. Check bonding system annually.")
        if "stainless" in propeller_material.lower():
            warnings.append("STAINLESS PROP: Higher cathode area - ensure adequate anode protection")

        return AnodeSystemAssessment(
            hull_material=hull_material,
            wetted_area_sq_ft=wetted_area_sq_ft,
            environment=environment,
            total_required_area_sq_in=area_calc["total_required_sq_in"],
            recommended_anodes=recommendations,
            anode_type=anode_type,
            inspection_interval=inspection,
            replacement_threshold="Replace when 50% depleted",
            warnings=warnings,
            cost_estimate_annual=(total_cost_low + total_cost_high) / 2
        )

    def _select_shaft_anode(
        self,
        shaft_diameter: float,
        anode_type: AnodeType
    ) -> Optional[AnodeSpec]:
        """Select appropriate shaft collar anode"""
        # Find closest size
        for key, anode in self.anode_catalog.items():
            if anode.placement == AnodePlacement.SHAFT and anode.type == anode_type:
                if str(shaft_diameter) in anode.dimensions or "1\"" in anode.dimensions:
                    return anode
        # Default
        return self.anode_catalog.get("cm-55989")

    def _select_drive_kit(self, anode_type: AnodeType) -> Optional[AnodeSpec]:
        """Select sterndrive anode kit"""
        for key, anode in self.anode_catalog.items():
            if anode.placement == AnodePlacement.OUTDRIVE and anode.type == anode_type:
                return anode
        return self.anode_catalog.get("alpha_gen2_kit")

    def _calculate_hull_anodes(
        self,
        required_area: float,
        anode_type: AnodeType
    ) -> List[AnodeRecommendation]:
        """Calculate hull anode requirements"""
        recommendations = []
        remaining = required_area

        # Large anodes first
        if remaining >= 45:
            large_count = int(remaining / 45)
            recommendations.append(AnodeRecommendation(
                placement=AnodePlacement.HULL,
                anode_type=anode_type,
                quantity=large_count,
                size="5 lb hull zinc",
                part_number="CM-821631",
                surface_area_sq_in=45 * large_count,
                installation_notes="Mount below waterline, distributed along hull",
                replacement_interval="Annually"
            ))
            remaining -= 45 * large_count

        # Medium anodes
        if remaining >= 28:
            med_count = int(remaining / 28)
            recommendations.append(AnodeRecommendation(
                placement=AnodePlacement.HULL,
                anode_type=anode_type,
                quantity=med_count,
                size="2.5 lb hull zinc",
                part_number="CM-821630",
                surface_area_sq_in=28 * med_count,
                installation_notes="Mount below waterline",
                replacement_interval="Annually"
            ))
            remaining -= 28 * med_count

        # Small anodes for remainder
        if remaining > 0:
            small_count = max(1, int(remaining / 12) + 1)
            recommendations.append(AnodeRecommendation(
                placement=AnodePlacement.HULL,
                anode_type=anode_type,
                quantity=small_count,
                size="1 lb hull zinc",
                part_number="CM-821629",
                surface_area_sq_in=12 * small_count,
                installation_notes="Trim tabs or small areas",
                replacement_interval="Annually"
            ))

        return recommendations
