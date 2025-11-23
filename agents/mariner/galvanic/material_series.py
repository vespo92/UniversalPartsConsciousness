"""
Galvanic Series Database - ASTM G82 Compliant

The galvanic series represents the electrochemical potential of materials
in seawater. More negative (anodic) materials corrode to protect more
positive (cathodic) materials.

Reference: ASTM G82 - Standard Guide for Development and Use of a
Galvanic Series for Predicting Galvanic Corrosion Performance
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class MarineEnvironment(Enum):
    """Marine environment classifications affecting corrosion rates"""
    FRESHWATER = "freshwater"           # Lakes, rivers - lowest conductivity
    BRACKISH = "brackish"               # Estuaries, river mouths - moderate
    SALTWATER = "saltwater"             # Ocean, coastal - standard reference
    SPLASH_ZONE = "splash_zone"         # Above waterline, constant spray - worst
    SUBMERGED = "submerged"             # Continuous submersion - less oxygen
    TROPICAL = "tropical"               # Warm saltwater - accelerated
    ARCTIC = "arctic"                   # Cold saltwater - slower
    POLLUTED = "polluted"               # Industrial harbors - variable


@dataclass
class MaterialProperties:
    """Complete properties of a marine material"""
    name: str
    galvanic_potential_v: float  # vs. saturated calomel electrode (SCE)
    density_g_cm3: float
    yield_strength_mpa: Optional[float] = None
    corrosion_rate_mm_yr: Optional[float] = None  # In flowing seawater
    common_applications: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    compatible_with: List[str] = field(default_factory=list)
    avoid_contact_with: List[str] = field(default_factory=list)


class MarineMaterial(Enum):
    """
    Marine materials with galvanic series positions.

    Values are (name, galvanic_potential_v, density, applications)
    More negative = more anodic (will corrode to protect cathode)
    """
    # Most Anodic (Active) - Sacrificial Materials
    MAGNESIUM = ("magnesium", -1.60, 1.74, ["Freshwater anodes only"])
    MAGNESIUM_AZ31B = ("magnesium_az31b", -1.58, 1.77, ["Die cast anodes"])

    # Active Anodes
    ZINC = ("zinc", -1.10, 7.14, ["Saltwater anodes", "Galvanizing"])
    ZINC_MIL = ("zinc_mil_a_18001k", -1.05, 7.14, ["Military spec anodes"])

    # Aluminum Alloys
    ALUMINUM_1100 = ("aluminum_1100", -0.95, 2.71, ["Sheet, general purpose"])
    ALUMINUM_ANODE = ("aluminum_anode_alloy", -0.90, 2.76, ["Brackish water anodes"])
    ALUMINUM_5052 = ("aluminum_5052", -0.85, 2.68, ["Marine grade sheet"])
    ALUMINUM_5086 = ("aluminum_5086", -0.83, 2.66, ["Hull plating"])
    ALUMINUM_6061_T6 = ("aluminum_6061_t6", -0.75, 2.70, ["Structural"])
    ALUMINUM_7075_T6 = ("aluminum_7075_t6", -0.73, 2.81, ["High strength, AVOID marine"])

    # Steel and Iron
    CADMIUM = ("cadmium", -0.70, 8.65, ["Obsolete, toxic coating"])
    CARBON_STEEL = ("carbon_steel", -0.60, 7.85, ["Requires coating/protection"])
    CAST_IRON = ("cast_iron", -0.55, 7.20, ["Engine blocks"])

    # Stainless Steels - Active State
    SS_304_ACTIVE = ("304_stainless_active", -0.50, 8.00, ["Crevice corrosion state"])
    SS_316_ACTIVE = ("316_stainless_active", -0.45, 8.00, ["Oxygen depleted"])

    # Lead, Tin, Solder
    LEAD = ("lead", -0.45, 11.34, ["Keel ballast"])
    TIN = ("tin", -0.40, 7.31, ["Solder component"])
    LEAD_TIN_SOLDER = ("60_40_solder", -0.42, 8.50, ["Electrical connections"])

    # Nickel and Copper Base
    NICKEL_ACTIVE = ("nickel_active", -0.35, 8.90, ["Plating"])
    NAVAL_BRASS = ("naval_brass_c46400", -0.32, 8.41, ["Propeller shafts, valves"])
    MANGANESE_BRONZE = ("manganese_bronze", -0.30, 8.30, ["Propellers"])
    BRASS = ("yellow_brass", -0.30, 8.47, ["Fittings - not recommended marine"])
    COPPER = ("copper", -0.20, 8.96, ["Plumbing, bottom paint"])

    # Marine Bronzes
    SILICON_BRONZE = ("silicon_bronze_c65500", -0.18, 8.53, ["Traditional fasteners"])
    TIN_BRONZE = ("tin_bronze_c90300", -0.16, 8.80, ["Pump bodies"])
    ALUMINUM_BRONZE = ("aluminum_bronze_c95400", -0.15, 7.45, ["High strength, careful!"])

    # Cupronickels
    CUPRONICKEL_90_10 = ("90_10_cupronickel", -0.15, 8.94, ["Heat exchangers"])
    CUPRONICKEL_70_30 = ("70_30_cupronickel", -0.10, 8.95, ["Seawater piping"])

    # Passive Stainless Steels
    SS_304_PASSIVE = ("304_stainless_passive", -0.08, 8.00, ["Interior, freshwater OK"])
    SS_316_PASSIVE = ("316_stainless_passive", 0.05, 8.00, ["Marine standard"])
    SS_316L_PASSIVE = ("316l_stainless_passive", 0.06, 8.00, ["Welded marine"])
    SS_317_PASSIVE = ("317_stainless_passive", 0.08, 8.00, ["Chemical resistance"])
    DUPLEX_2205 = ("duplex_2205", 0.10, 7.80, ["High strength marine"])

    # Premium Corrosion Resistant
    MONEL_400 = ("monel_400", 0.08, 8.83, ["Premium marine hardware"])
    MONEL_K500 = ("monel_k500", 0.10, 8.44, ["Propeller shafts"])
    INCONEL_625 = ("inconel_625", 0.12, 8.44, ["Extreme environments"])

    # Titanium
    TITANIUM_GRADE_2 = ("titanium_grade_2", 0.10, 4.51, ["Racing, aerospace marine"])
    TITANIUM_6AL4V = ("titanium_6al4v", 0.12, 4.43, ["High performance"])

    # Noble Metals
    HASTELLOY_C276 = ("hastelloy_c276", 0.12, 8.89, ["Chemical resistance"])
    SILVER = ("silver", 0.15, 10.49, ["Electrical, decorative"])
    GRAPHITE = ("graphite", 0.25, 2.25, ["Packing, CAUSES corrosion"])
    GOLD = ("gold", 0.35, 19.30, ["Plating, connectors"])
    PLATINUM = ("platinum", 0.40, 21.45, ["Reference electrode"])

    def __init__(self, name: str, potential: float, density: float, applications: List[str]):
        self._name = name
        self._potential = potential
        self._density = density
        self._applications = applications

    @property
    def galvanic_potential(self) -> float:
        return self._potential

    @property
    def density(self) -> float:
        return self._density

    @property
    def applications(self) -> List[str]:
        return self._applications


class GalvanicSeries:
    """
    Complete galvanic series database with lookup and analysis functions.

    Based on ASTM G82 with marine-specific extensions.
    """

    def __init__(self):
        self._series: Dict[str, float] = self._build_series()
        self._material_data: Dict[str, MaterialProperties] = self._build_material_data()

    def _build_series(self) -> Dict[str, float]:
        """Build the galvanic series lookup dictionary"""
        series = {}
        for material in MarineMaterial:
            series[material._name] = material._potential

        # Add common aliases
        aliases = {
            "316ss": "316_stainless_passive",
            "316 stainless": "316_stainless_passive",
            "304ss": "304_stainless_passive",
            "bronze": "silicon_bronze_c65500",
            "aluminum": "aluminum_6061_t6",
            "steel": "carbon_steel",
            "stainless": "316_stainless_passive",
            "monel": "monel_400",
            "titanium": "titanium_grade_2",
        }
        for alias, target in aliases.items():
            if target in series:
                series[alias] = series[target]

        return series

    def _build_material_data(self) -> Dict[str, MaterialProperties]:
        """Build detailed material properties database"""
        return {
            "316_stainless_passive": MaterialProperties(
                name="316 Stainless Steel (Passive)",
                galvanic_potential_v=0.05,
                density_g_cm3=8.00,
                yield_strength_mpa=205,
                corrosion_rate_mm_yr=0.001,
                common_applications=[
                    "Marine fasteners",
                    "Deck hardware",
                    "Rigging fittings",
                    "Railings",
                ],
                warnings=[
                    "Can become active in crevices",
                    "May pit in stagnant saltwater",
                    "Must be passivated after machining",
                ],
                compatible_with=[
                    "316_stainless_passive",
                    "titanium",
                    "monel_400",
                    "fiberglass",
                    "teak",
                ],
                avoid_contact_with=[
                    "aluminum",
                    "zinc",
                    "carbon_steel",
                    "graphite",
                ],
            ),
            "aluminum_6061_t6": MaterialProperties(
                name="Aluminum 6061-T6",
                galvanic_potential_v=-0.75,
                density_g_cm3=2.70,
                yield_strength_mpa=276,
                corrosion_rate_mm_yr=0.05,
                common_applications=[
                    "Mast sections",
                    "Spars",
                    "Deck hardware (anodized)",
                    "Outboard brackets",
                ],
                warnings=[
                    "MUST isolate from stainless steel",
                    "Requires anodizing for saltwater",
                    "Will corrode rapidly if unprotected",
                ],
                compatible_with=[
                    "aluminum_5052",
                    "aluminum_5086",
                    "zinc",
                ],
                avoid_contact_with=[
                    "stainless_steel",
                    "copper",
                    "bronze",
                    "graphite",
                    "carbon_fiber",
                ],
            ),
            "silicon_bronze_c65500": MaterialProperties(
                name="Silicon Bronze C65500",
                galvanic_potential_v=-0.18,
                density_g_cm3=8.53,
                yield_strength_mpa=379,
                corrosion_rate_mm_yr=0.002,
                common_applications=[
                    "Traditional wood boat fasteners",
                    "Chainplates (bronze boats)",
                    "Shaft logs",
                ],
                warnings=[
                    "NOT compatible with stainless steel",
                    "Compatible with copper bottom paint",
                    "Premium material, expensive",
                ],
                compatible_with=[
                    "copper",
                    "brass",
                    "bronze",
                    "wood",
                ],
                avoid_contact_with=[
                    "aluminum",
                    "stainless_steel",
                    "zinc",
                ],
            ),
        }

    def get_potential(self, material: str) -> Optional[float]:
        """
        Get galvanic potential for a material.

        Args:
            material: Material name or alias

        Returns:
            Galvanic potential vs. SCE in volts, or None if not found
        """
        normalized = material.lower().replace(" ", "_").replace("-", "_")
        return self._series.get(normalized)

    def get_material_data(self, material: str) -> Optional[MaterialProperties]:
        """Get detailed material properties"""
        normalized = material.lower().replace(" ", "_").replace("-", "_")
        return self._material_data.get(normalized)

    def list_materials_in_range(
        self,
        min_potential: float,
        max_potential: float
    ) -> List[Tuple[str, float]]:
        """List all materials within a galvanic potential range"""
        return [
            (name, potential)
            for name, potential in sorted(self._series.items(), key=lambda x: x[1])
            if min_potential <= potential <= max_potential
        ]

    def find_compatible_materials(
        self,
        target_material: str,
        max_voltage_difference_mv: float = 200
    ) -> List[Tuple[str, float, float]]:
        """
        Find materials compatible with target (within voltage threshold).

        Args:
            target_material: Material to find matches for
            max_voltage_difference_mv: Maximum acceptable potential difference

        Returns:
            List of (material_name, potential, voltage_difference_mv)
        """
        target_potential = self.get_potential(target_material)
        if target_potential is None:
            return []

        max_diff_v = max_voltage_difference_mv / 1000
        compatible = []

        for name, potential in self._series.items():
            diff = abs(potential - target_potential)
            if diff <= max_diff_v:
                compatible.append((name, potential, diff * 1000))

        return sorted(compatible, key=lambda x: x[2])

    def get_anodic_direction(self) -> List[Tuple[str, float]]:
        """Get materials sorted from most anodic to most cathodic"""
        return sorted(self._series.items(), key=lambda x: x[1])

    def is_more_anodic(self, material_a: str, material_b: str) -> Optional[bool]:
        """
        Determine if material_a is more anodic (will corrode first) than material_b.

        Returns:
            True if material_a is more anodic
            False if material_b is more anodic
            None if either material not found
        """
        pot_a = self.get_potential(material_a)
        pot_b = self.get_potential(material_b)

        if pot_a is None or pot_b is None:
            return None

        return pot_a < pot_b


# Environment conductivity factors
ENVIRONMENT_FACTORS: Dict[MarineEnvironment, float] = {
    MarineEnvironment.FRESHWATER: 0.3,
    MarineEnvironment.BRACKISH: 0.6,
    MarineEnvironment.SALTWATER: 1.0,
    MarineEnvironment.SPLASH_ZONE: 1.2,
    MarineEnvironment.SUBMERGED: 0.8,
    MarineEnvironment.TROPICAL: 1.3,
    MarineEnvironment.ARCTIC: 0.7,
    MarineEnvironment.POLLUTED: 1.1,
}


# Safe galvanic couples (voltage difference < 200mV in seawater)
SAFE_COUPLES: List[Tuple[str, str]] = [
    ("316_stainless_passive", "monel_400"),
    ("316_stainless_passive", "titanium_grade_2"),
    ("silicon_bronze_c65500", "copper"),
    ("naval_brass_c46400", "copper"),
    ("aluminum_5052", "aluminum_6061_t6"),
    ("90_10_cupronickel", "70_30_cupronickel"),
]


# Dangerous galvanic couples (NEVER use together)
DANGEROUS_COUPLES: List[Tuple[str, str, str]] = [
    ("aluminum", "stainless_steel", "Rapid aluminum corrosion"),
    ("aluminum", "graphite", "Severe corrosion, common in composites"),
    ("zinc", "copper", "Dezincification"),
    ("carbon_steel", "stainless_steel", "Steel pitting"),
    ("aluminum", "copper", "Severe corrosion"),
    ("magnesium", "stainless_steel", "Explosive corrosion rate"),
]
