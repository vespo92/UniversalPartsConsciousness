"""
Coatings and Surface Treatments Database

Comprehensive database of protective coatings, platings,
and surface treatments with specifications and compatibility data.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class CoatingType(Enum):
    """Primary coating classification"""
    ELECTROPLATE = "electroplate"      # Zinc, nickel, chrome, etc.
    CONVERSION = "conversion"          # Phosphate, chromate, anodize
    MECHANICAL = "mechanical"          # Mechanical zinc, sherardizing
    ORGANIC = "organic"                # Paint, powder coat, e-coat
    THERMAL_SPRAY = "thermal_spray"    # Flame spray, plasma spray
    VAPOR_DEPOSITION = "vapor_deposition"  # PVD, CVD
    DIFFUSION = "diffusion"            # Carburizing, nitriding


class ApplicationMethod(Enum):
    """How the coating is applied"""
    IMMERSION = "immersion"
    ELECTROCHEMICAL = "electrochemical"
    SPRAY = "spray"
    THERMAL = "thermal"
    VACUUM = "vacuum"
    MECHANICAL = "mechanical"


@dataclass
class CoatingSpec:
    """Complete coating specification"""
    name: str
    coating_type: CoatingType
    application_method: ApplicationMethod

    # Physical properties
    thickness_um: Tuple[float, float]  # Min, max typical
    hardness: Optional[str] = None
    color: str = ""

    # Performance
    salt_spray_hours: int = 0  # ASTM B117 hours to red rust
    temperature_max_c: float = 100.0
    friction_coefficient: Optional[float] = None

    # Compatibility
    compatible_substrates: List[str] = field(default_factory=list)
    not_recommended_for: List[str] = field(default_factory=list)

    # Risks
    hydrogen_embrittlement_risk: bool = False
    he_risk_threshold_hrc: Optional[int] = None  # HRC above which HE is concern

    # Standards
    standards: List[str] = field(default_factory=list)

    # Environmental
    rohs_compliant: bool = True
    contains_hex_chrome: bool = False
    contains_cadmium: bool = False

    # Cost and availability
    relative_cost: float = 1.0  # 1.0 = zinc plate baseline
    typical_applications: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.compatible_substrates:
            self.compatible_substrates = []
        if not self.not_recommended_for:
            self.not_recommended_for = []
        if not self.standards:
            self.standards = []
        if not self.typical_applications:
            self.typical_applications = []


class CoatingDatabase:
    """
    Database of protective coatings and surface treatments.

    Covers electroplating, conversion coatings, organic coatings,
    and specialized treatments for corrosion and wear protection.
    """

    def __init__(self):
        self._coatings: Dict[str, CoatingSpec] = {}
        self._load_electroplate_coatings()
        self._load_conversion_coatings()
        self._load_mechanical_coatings()
        self._load_organic_coatings()

    def _load_electroplate_coatings(self):
        """Load electroplated coating specifications"""

        self._coatings["Zinc Electroplate"] = CoatingSpec(
            name="Zinc Electroplate",
            coating_type=CoatingType.ELECTROPLATE,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(5, 25),
            hardness="HV 50-60",
            color="Silver/Blue/Yellow/Black (chromate dependent)",
            salt_spray_hours=96,  # Clear chromate
            temperature_max_c=120,
            compatible_substrates=["carbon_steel", "low_alloy_steel", "cast_iron"],
            not_recommended_for=["high_strength_steel_hrc40+", "stainless_steel"],
            hydrogen_embrittlement_risk=True,
            he_risk_threshold_hrc=39,
            standards=["ASTM B633", "ISO 4042", "QQ-Z-325"],
            rohs_compliant=True,  # If trivalent chromate
            contains_hex_chrome=False,  # Modern processes
            relative_cost=1.0,
            typical_applications=["fasteners", "brackets", "general hardware"]
        )

        self._coatings["Zinc-Nickel Electroplate"] = CoatingSpec(
            name="Zinc-Nickel Electroplate",
            coating_type=CoatingType.ELECTROPLATE,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(8, 15),
            hardness="HV 350-450",
            color="Silver-gray",
            salt_spray_hours=720,  # With passivate
            temperature_max_c=250,
            friction_coefficient=0.12,
            compatible_substrates=["carbon_steel", "alloy_steel", "cast_iron"],
            not_recommended_for=["high_strength_steel_hrc40+"],
            hydrogen_embrittlement_risk=True,
            he_risk_threshold_hrc=39,
            standards=["ASTM B841", "ISO 19598"],
            relative_cost=3.0,
            typical_applications=["automotive", "aerospace fasteners", "brake components"]
        )

        self._coatings["Cadmium Plate"] = CoatingSpec(
            name="Cadmium Plate",
            coating_type=CoatingType.ELECTROPLATE,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(8, 25),
            hardness="HV 65",
            color="Silver",
            salt_spray_hours=500,
            temperature_max_c=230,
            friction_coefficient=0.08,
            compatible_substrates=["carbon_steel", "alloy_steel"],
            not_recommended_for=["high_strength_steel"],
            hydrogen_embrittlement_risk=True,
            he_risk_threshold_hrc=39,
            standards=["QQ-P-416", "AMS-QQ-P-416"],
            rohs_compliant=False,
            contains_cadmium=True,
            relative_cost=4.0,
            typical_applications=["aerospace_legacy", "military_legacy"]
        )

        self._coatings["Nickel Electroplate"] = CoatingSpec(
            name="Nickel Electroplate",
            coating_type=CoatingType.ELECTROPLATE,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(10, 50),
            hardness="HV 150-400",
            color="Silver",
            salt_spray_hours=200,
            temperature_max_c=400,
            compatible_substrates=["carbon_steel", "copper", "brass", "aluminum"],
            hydrogen_embrittlement_risk=True,
            he_risk_threshold_hrc=39,
            standards=["ASTM B689", "AMS 2403"],
            relative_cost=2.5,
            typical_applications=["decorative", "engineering", "undercoat_for_chrome"]
        )

        self._coatings["Electroless Nickel"] = CoatingSpec(
            name="Electroless Nickel",
            coating_type=CoatingType.ELECTROPLATE,
            application_method=ApplicationMethod.IMMERSION,
            thickness_um=(5, 75),
            hardness="HV 500-700 (as-plated), HV 1000 (heat treated)",
            color="Silver",
            salt_spray_hours=500,
            temperature_max_c=400,
            friction_coefficient=0.4,
            compatible_substrates=["carbon_steel", "alloy_steel", "aluminum", "copper", "titanium"],
            not_recommended_for=["lead", "tin"],
            hydrogen_embrittlement_risk=True,
            he_risk_threshold_hrc=39,
            standards=["ASTM B733", "AMS 2404", "MIL-C-26074"],
            relative_cost=5.0,
            typical_applications=["precision_parts", "wear_surfaces", "complex_geometry"]
        )

        self._coatings["Hard Chrome"] = CoatingSpec(
            name="Hard Chrome",
            coating_type=CoatingType.ELECTROPLATE,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(25, 250),
            hardness="HV 850-1050",
            color="Blue-silver",
            salt_spray_hours=100,  # Not for corrosion, for wear
            temperature_max_c=400,
            friction_coefficient=0.12,
            compatible_substrates=["carbon_steel", "alloy_steel", "stainless_steel"],
            hydrogen_embrittlement_risk=True,
            he_risk_threshold_hrc=35,
            standards=["ASTM B177", "AMS 2406", "QQ-C-320"],
            rohs_compliant=False,  # Contains hex chrome
            contains_hex_chrome=True,
            relative_cost=6.0,
            typical_applications=["hydraulic_rods", "wear_surfaces", "tooling"]
        )

    def _load_conversion_coatings(self):
        """Load conversion coating specifications"""

        self._coatings["Phosphate (Zinc)"] = CoatingSpec(
            name="Zinc Phosphate",
            coating_type=CoatingType.CONVERSION,
            application_method=ApplicationMethod.IMMERSION,
            thickness_um=(8, 25),
            color="Gray to dark gray",
            salt_spray_hours=48,  # Alone, much more with oil
            temperature_max_c=150,
            friction_coefficient=0.10,  # With oil
            compatible_substrates=["carbon_steel", "alloy_steel"],
            not_recommended_for=["stainless_steel", "aluminum"],
            hydrogen_embrittlement_risk=False,
            standards=["MIL-DTL-16232", "TT-C-490"],
            relative_cost=0.5,
            typical_applications=["paint_base", "oil_retention", "cold_forming"]
        )

        self._coatings["Phosphate (Manganese)"] = CoatingSpec(
            name="Manganese Phosphate",
            coating_type=CoatingType.CONVERSION,
            application_method=ApplicationMethod.IMMERSION,
            thickness_um=(5, 15),
            hardness="HV 250-400",
            color="Dark gray to black",
            salt_spray_hours=24,  # With oil, much more
            temperature_max_c=200,
            friction_coefficient=0.08,  # With oil
            compatible_substrates=["carbon_steel", "alloy_steel", "cast_iron"],
            hydrogen_embrittlement_risk=False,
            standards=["MIL-DTL-16232", "AMS 2530"],
            relative_cost=0.6,
            typical_applications=["gears", "bearings", "break_in_coating"]
        )

        self._coatings["Black Oxide"] = CoatingSpec(
            name="Black Oxide",
            coating_type=CoatingType.CONVERSION,
            application_method=ApplicationMethod.IMMERSION,
            thickness_um=(0.5, 2.5),
            color="Black",
            salt_spray_hours=8,  # Alone, with oil 48+
            temperature_max_c=150,
            compatible_substrates=["carbon_steel", "stainless_steel", "copper"],
            hydrogen_embrittlement_risk=False,
            standards=["MIL-DTL-13924", "AMS 2485"],
            relative_cost=0.4,
            typical_applications=["tools", "fasteners", "decorative"]
        )

        self._coatings["Anodize Type II"] = CoatingSpec(
            name="Sulfuric Anodize (Type II)",
            coating_type=CoatingType.CONVERSION,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(5, 25),
            hardness="HV 200-300",
            color="Clear or dyed",
            salt_spray_hours=336,  # Sealed
            temperature_max_c=170,
            compatible_substrates=["aluminum_alloys"],
            not_recommended_for=["steel", "copper", "titanium"],
            hydrogen_embrittlement_risk=False,
            standards=["MIL-A-8625 Type II", "AMS 2471"],
            relative_cost=1.5,
            typical_applications=["architectural", "consumer_products", "corrosion_protection"]
        )

        self._coatings["Anodize Type III"] = CoatingSpec(
            name="Hard Anodize (Type III)",
            coating_type=CoatingType.CONVERSION,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(25, 75),
            hardness="HV 400-600",
            color="Gray to dark brown",
            salt_spray_hours=336,
            temperature_max_c=170,
            friction_coefficient=0.6,  # Unlubricated
            compatible_substrates=["aluminum_alloys"],
            not_recommended_for=["2xxx_series_al", "7xxx_series_al", "steel"],
            hydrogen_embrittlement_risk=False,
            standards=["MIL-A-8625 Type III", "AMS 2469"],
            relative_cost=2.5,
            typical_applications=["wear_surfaces", "hydraulic_components", "military"]
        )

        self._coatings["Passivation (Stainless)"] = CoatingSpec(
            name="Passivation",
            coating_type=CoatingType.CONVERSION,
            application_method=ApplicationMethod.IMMERSION,
            thickness_um=(0, 1),  # Removes rather than adds
            color="No change",
            salt_spray_hours=96,  # Depends on alloy
            temperature_max_c=500,  # Limited by base metal
            compatible_substrates=["stainless_steel"],
            not_recommended_for=["carbon_steel", "aluminum"],
            hydrogen_embrittlement_risk=False,
            standards=["ASTM A967", "AMS 2700", "QQ-P-35"],
            relative_cost=0.3,
            typical_applications=["all_stainless_parts", "food_equipment", "medical"]
        )

    def _load_mechanical_coatings(self):
        """Load mechanical/zinc flake coatings"""

        self._coatings["Mechanical Zinc"] = CoatingSpec(
            name="Mechanical Zinc Plating",
            coating_type=CoatingType.MECHANICAL,
            application_method=ApplicationMethod.MECHANICAL,
            thickness_um=(8, 50),
            hardness="HV 50-60",
            color="Silver",
            salt_spray_hours=200,
            temperature_max_c=120,
            compatible_substrates=["carbon_steel", "alloy_steel", "high_strength_steel"],
            hydrogen_embrittlement_risk=False,  # Key advantage
            standards=["ASTM B695", "MIL-DTL-16232"],
            relative_cost=2.0,
            typical_applications=["high_strength_fasteners", "springs", "clips"]
        )

        self._coatings["Geomet"] = CoatingSpec(
            name="Geomet (Zinc Flake)",
            coating_type=CoatingType.MECHANICAL,
            application_method=ApplicationMethod.SPRAY,
            thickness_um=(5, 15),
            color="Silver-gray",
            salt_spray_hours=720,  # 500 series
            temperature_max_c=300,
            friction_coefficient=0.12,
            compatible_substrates=["carbon_steel", "alloy_steel", "high_strength_steel"],
            hydrogen_embrittlement_risk=False,
            standards=["ISO 10683", "Ford WSS-M21P34-A2"],
            relative_cost=2.5,
            typical_applications=["automotive_fasteners", "brake_components", "springs"]
        )

        self._coatings["Dacromet"] = CoatingSpec(
            name="Dacromet",
            coating_type=CoatingType.MECHANICAL,
            application_method=ApplicationMethod.SPRAY,
            thickness_um=(5, 25),
            color="Silver-gray",
            salt_spray_hours=500,
            temperature_max_c=300,
            friction_coefficient=0.14,
            compatible_substrates=["carbon_steel", "alloy_steel", "cast_iron"],
            hydrogen_embrittlement_risk=False,
            standards=["ISO 10683"],
            rohs_compliant=False,  # Contains hex chrome
            contains_hex_chrome=True,
            relative_cost=2.0,
            typical_applications=["automotive_legacy", "industrial"]
        )

        self._coatings["Delta-Seal"] = CoatingSpec(
            name="Delta-Seal (Topcoat for Geomet)",
            coating_type=CoatingType.MECHANICAL,
            application_method=ApplicationMethod.SPRAY,
            thickness_um=(3, 8),
            color="Various (black, silver, green)",
            salt_spray_hours=1000,  # With Geomet base
            temperature_max_c=300,
            friction_coefficient=0.08,  # Lubricated versions
            compatible_substrates=["geomet_coated_steel"],
            hydrogen_embrittlement_risk=False,
            relative_cost=3.0,
            typical_applications=["high_performance_fasteners", "controlled_friction"]
        )

    def _load_organic_coatings(self):
        """Load organic coating specifications"""

        self._coatings["Powder Coat"] = CoatingSpec(
            name="Powder Coating",
            coating_type=CoatingType.ORGANIC,
            application_method=ApplicationMethod.SPRAY,
            thickness_um=(50, 150),
            hardness="Pencil 2H-4H",
            color="Any",
            salt_spray_hours=500,  # Depends on pretreatment
            temperature_max_c=150,
            compatible_substrates=["carbon_steel", "aluminum", "zinc"],
            not_recommended_for=["plastics", "wood"],
            hydrogen_embrittlement_risk=False,
            standards=["ASTM D3451", "AAMA 2604"],
            relative_cost=1.5,
            typical_applications=["enclosures", "furniture", "automotive_trim"]
        )

        self._coatings["E-Coat"] = CoatingSpec(
            name="Electrocoat (E-Coat)",
            coating_type=CoatingType.ORGANIC,
            application_method=ApplicationMethod.ELECTROCHEMICAL,
            thickness_um=(15, 35),
            color="Black (typically)",
            salt_spray_hours=500,
            temperature_max_c=150,
            compatible_substrates=["carbon_steel", "aluminum", "zinc_plated"],
            hydrogen_embrittlement_risk=False,
            standards=["GMW14339", "Ford WSS-M2P188-A1"],
            relative_cost=1.0,
            typical_applications=["automotive_bodies", "appliances", "primers"]
        )

        self._coatings["PTFE Coating"] = CoatingSpec(
            name="PTFE Coating (Teflon)",
            coating_type=CoatingType.ORGANIC,
            application_method=ApplicationMethod.SPRAY,
            thickness_um=(15, 50),
            hardness="Low",
            color="Black, green, gray",
            salt_spray_hours=200,
            temperature_max_c=260,
            friction_coefficient=0.04,
            compatible_substrates=["carbon_steel", "stainless_steel", "aluminum"],
            hydrogen_embrittlement_risk=False,
            relative_cost=3.0,
            typical_applications=["fasteners", "food_processing", "non_stick"]
        )

    def get(self, name: str) -> Optional[CoatingSpec]:
        """Get coating by name"""
        return self._coatings.get(name)

    def search(
        self,
        coating_type: Optional[CoatingType] = None,
        min_salt_spray_hours: Optional[int] = None,
        no_he_risk: bool = False,
        rohs_compliant: bool = False
    ) -> List[CoatingSpec]:
        """Search coatings by criteria"""
        results = []
        for coating in self._coatings.values():
            if coating_type and coating.coating_type != coating_type:
                continue
            if min_salt_spray_hours and coating.salt_spray_hours < min_salt_spray_hours:
                continue
            if no_he_risk and coating.hydrogen_embrittlement_risk:
                continue
            if rohs_compliant and not coating.rohs_compliant:
                continue
            results.append(coating)
        return results

    def list_all(self) -> List[str]:
        """List all coating names"""
        return list(self._coatings.keys())

    @property
    def count(self) -> int:
        """Number of coatings in database"""
        return len(self._coatings)
