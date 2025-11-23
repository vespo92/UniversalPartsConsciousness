"""
Polymer and Elastomer Database

Comprehensive database of engineering plastics, rubbers, and
elastomers with temperature, chemical, and mechanical properties.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class PolymerFamily(Enum):
    """Primary polymer classification"""
    THERMOPLASTIC = "thermoplastic"
    THERMOSET = "thermoset"
    ELASTOMER = "elastomer"
    FLUOROPOLYMER = "fluoropolymer"


class ChemicalResistance(Enum):
    """Chemical resistance rating"""
    EXCELLENT = "excellent"  # No effect
    GOOD = "good"            # Minor swelling or weight gain
    FAIR = "fair"            # Noticeable degradation
    POOR = "poor"            # Rapid degradation
    NOT_RECOMMENDED = "not_recommended"


@dataclass
class PolymerSpec:
    """Complete polymer specification"""
    # Identity
    name: str
    abbreviation: str
    trade_names: List[str]
    family: PolymerFamily

    # Thermal Properties
    temp_min_c: float
    temp_max_continuous_c: float
    temp_max_short_term_c: float
    glass_transition_c: Optional[float] = None
    melting_point_c: Optional[float] = None
    heat_deflection_c: Optional[float] = None

    # Mechanical Properties
    tensile_strength_mpa: float = 0.0
    tensile_modulus_mpa: float = 0.0
    elongation_percent: float = 0.0
    flexural_strength_mpa: float = 0.0
    hardness_shore: str = ""
    impact_strength_kj_m2: Optional[float] = None

    # Physical Properties
    density_g_cm3: float = 0.0
    water_absorption_percent: float = 0.0
    coefficient_friction: float = 0.4

    # Electrical
    dielectric_constant: Optional[float] = None
    volume_resistivity_ohm_cm: Optional[float] = None

    # Chemical Resistance (key chemicals)
    chemical_resistance: Dict[str, ChemicalResistance] = field(default_factory=dict)

    # Processing
    sterilization_methods: List[str] = field(default_factory=list)
    food_contact_approved: bool = False
    uv_resistant: bool = False

    # Applications
    typical_applications: List[str] = field(default_factory=list)
    cost_factor: float = 1.0  # Relative to ABS

    def __post_init__(self):
        if not self.chemical_resistance:
            self.chemical_resistance = {}
        if not self.sterilization_methods:
            self.sterilization_methods = []
        if not self.typical_applications:
            self.typical_applications = []
        if not self.trade_names:
            self.trade_names = []


class PolymerDatabase:
    """
    Comprehensive polymer property database.

    Covers engineering plastics, high-performance polymers,
    and elastomers commonly used in mechanical engineering.
    """

    def __init__(self):
        self._polymers: Dict[str, PolymerSpec] = {}
        self._load_engineering_plastics()
        self._load_high_performance()
        self._load_elastomers()
        self._load_fluoropolymers()

    def _load_engineering_plastics(self):
        """Load common engineering thermoplastics"""

        self._polymers["Nylon 6/6"] = PolymerSpec(
            name="Polyamide 6/6",
            abbreviation="PA66",
            trade_names=["Zytel", "Ultramid", "Durethan"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-40,
            temp_max_continuous_c=80,
            temp_max_short_term_c=120,
            glass_transition_c=50,
            melting_point_c=260,
            heat_deflection_c=75,
            tensile_strength_mpa=82,
            tensile_modulus_mpa=3000,
            elongation_percent=50,
            flexural_strength_mpa=110,
            hardness_shore="D83",
            density_g_cm3=1.14,
            water_absorption_percent=2.5,
            coefficient_friction=0.35,
            chemical_resistance={
                "water": ChemicalResistance.GOOD,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.GOOD,
                "acids_dilute": ChemicalResistance.POOR,
                "bases": ChemicalResistance.POOR,
                "alcohols": ChemicalResistance.GOOD,
            },
            sterilization_methods=["autoclave", "gamma", "eto"],
            food_contact_approved=True,
            typical_applications=["gears", "bearings", "bushings", "fasteners"],
            cost_factor=1.5
        )

        self._polymers["Acetal"] = PolymerSpec(
            name="Polyoxymethylene",
            abbreviation="POM",
            trade_names=["Delrin", "Celcon", "Hostaform"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-40,
            temp_max_continuous_c=90,
            temp_max_short_term_c=120,
            glass_transition_c=-60,
            melting_point_c=175,
            heat_deflection_c=110,
            tensile_strength_mpa=70,
            tensile_modulus_mpa=3100,
            elongation_percent=40,
            flexural_strength_mpa=97,
            hardness_shore="D80",
            density_g_cm3=1.42,
            water_absorption_percent=0.2,
            coefficient_friction=0.20,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.GOOD,
                "acids_dilute": ChemicalResistance.FAIR,
                "acids_strong": ChemicalResistance.NOT_RECOMMENDED,
                "bases": ChemicalResistance.GOOD,
                "solvents": ChemicalResistance.GOOD,
            },
            sterilization_methods=["eto", "gamma"],
            food_contact_approved=True,
            typical_applications=["gears", "bearings", "springs", "fasteners"],
            cost_factor=2.0
        )

        self._polymers["ABS"] = PolymerSpec(
            name="Acrylonitrile Butadiene Styrene",
            abbreviation="ABS",
            trade_names=["Cycolac", "Terluran", "Novodur"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-40,
            temp_max_continuous_c=70,
            temp_max_short_term_c=85,
            glass_transition_c=105,
            heat_deflection_c=98,
            tensile_strength_mpa=45,
            tensile_modulus_mpa=2300,
            elongation_percent=20,
            flexural_strength_mpa=75,
            hardness_shore="R100",
            density_g_cm3=1.05,
            water_absorption_percent=0.3,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.GOOD,
                "fuels": ChemicalResistance.FAIR,
                "acids_dilute": ChemicalResistance.GOOD,
                "bases": ChemicalResistance.GOOD,
                "solvents": ChemicalResistance.POOR,
            },
            sterilization_methods=["eto"],
            food_contact_approved=True,
            typical_applications=["housings", "enclosures", "automotive trim"],
            cost_factor=1.0
        )

        self._polymers["Polycarbonate"] = PolymerSpec(
            name="Polycarbonate",
            abbreviation="PC",
            trade_names=["Lexan", "Makrolon", "Calibre"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-40,
            temp_max_continuous_c=115,
            temp_max_short_term_c=135,
            glass_transition_c=147,
            heat_deflection_c=132,
            tensile_strength_mpa=65,
            tensile_modulus_mpa=2400,
            elongation_percent=110,
            flexural_strength_mpa=93,
            hardness_shore="R118",
            impact_strength_kj_m2=65,
            density_g_cm3=1.20,
            water_absorption_percent=0.15,
            chemical_resistance={
                "water": ChemicalResistance.GOOD,
                "oils": ChemicalResistance.GOOD,
                "fuels": ChemicalResistance.FAIR,
                "acids_dilute": ChemicalResistance.FAIR,
                "bases": ChemicalResistance.POOR,
                "alcohols": ChemicalResistance.FAIR,
                "solvents": ChemicalResistance.POOR,
            },
            sterilization_methods=["eto", "gamma"],
            food_contact_approved=True,
            typical_applications=["safety glasses", "lenses", "housings", "medical"],
            cost_factor=2.5
        )

        self._polymers["UHMWPE"] = PolymerSpec(
            name="Ultra-High Molecular Weight Polyethylene",
            abbreviation="UHMWPE",
            trade_names=["Tivar", "Polystone"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-200,
            temp_max_continuous_c=80,
            temp_max_short_term_c=100,
            melting_point_c=135,
            tensile_strength_mpa=40,
            tensile_modulus_mpa=800,
            elongation_percent=350,
            hardness_shore="D65",
            density_g_cm3=0.93,
            water_absorption_percent=0.01,
            coefficient_friction=0.10,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.GOOD,
                "acids_dilute": ChemicalResistance.EXCELLENT,
                "acids_strong": ChemicalResistance.EXCELLENT,
                "bases": ChemicalResistance.EXCELLENT,
                "solvents_aromatic": ChemicalResistance.FAIR,
            },
            sterilization_methods=["gamma", "eto"],
            food_contact_approved=True,
            typical_applications=["wear strips", "bearings", "medical implants", "liners"],
            cost_factor=3.0
        )

    def _load_high_performance(self):
        """Load high-performance engineering plastics"""

        self._polymers["PEEK"] = PolymerSpec(
            name="Polyether Ether Ketone",
            abbreviation="PEEK",
            trade_names=["Victrex PEEK", "Ketron", "Ensinger TECAPEEK"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-60,
            temp_max_continuous_c=250,
            temp_max_short_term_c=300,
            glass_transition_c=143,
            melting_point_c=343,
            heat_deflection_c=152,
            tensile_strength_mpa=100,
            tensile_modulus_mpa=3600,
            elongation_percent=45,
            flexural_strength_mpa=170,
            hardness_shore="D85",
            density_g_cm3=1.32,
            water_absorption_percent=0.1,
            coefficient_friction=0.35,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.EXCELLENT,
                "acids_dilute": ChemicalResistance.EXCELLENT,
                "acids_strong": ChemicalResistance.GOOD,
                "bases": ChemicalResistance.EXCELLENT,
                "solvents": ChemicalResistance.EXCELLENT,
                "steam": ChemicalResistance.EXCELLENT,
            },
            sterilization_methods=["autoclave", "gamma", "eto", "steam"],
            food_contact_approved=True,
            uv_resistant=True,
            typical_applications=["aerospace", "medical", "oil & gas", "semiconductor"],
            cost_factor=15.0
        )

        self._polymers["PPS"] = PolymerSpec(
            name="Polyphenylene Sulfide",
            abbreviation="PPS",
            trade_names=["Ryton", "Fortron", "Torelina"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-40,
            temp_max_continuous_c=200,
            temp_max_short_term_c=260,
            glass_transition_c=90,
            melting_point_c=285,
            heat_deflection_c=135,
            tensile_strength_mpa=80,
            tensile_modulus_mpa=3800,
            elongation_percent=3,
            flexural_strength_mpa=145,
            hardness_shore="R123",
            density_g_cm3=1.35,
            water_absorption_percent=0.02,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.EXCELLENT,
                "acids_dilute": ChemicalResistance.EXCELLENT,
                "bases": ChemicalResistance.EXCELLENT,
                "solvents": ChemicalResistance.EXCELLENT,
            },
            sterilization_methods=["autoclave", "gamma", "eto"],
            typical_applications=["pump components", "electrical", "automotive"],
            cost_factor=8.0
        )

        self._polymers["PPSU"] = PolymerSpec(
            name="Polyphenylsulfone",
            abbreviation="PPSU",
            trade_names=["Radel", "Ultrason P"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-50,
            temp_max_continuous_c=180,
            temp_max_short_term_c=200,
            glass_transition_c=220,
            heat_deflection_c=207,
            tensile_strength_mpa=70,
            tensile_modulus_mpa=2340,
            elongation_percent=60,
            flexural_strength_mpa=105,
            impact_strength_kj_m2=70,
            density_g_cm3=1.29,
            water_absorption_percent=0.4,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "steam": ChemicalResistance.EXCELLENT,
                "acids_dilute": ChemicalResistance.GOOD,
                "bases": ChemicalResistance.EXCELLENT,
            },
            sterilization_methods=["autoclave", "gamma", "eto", "steam"],
            food_contact_approved=True,
            typical_applications=["medical instruments", "sterilization trays", "plumbing"],
            cost_factor=12.0
        )

        self._polymers["PEI"] = PolymerSpec(
            name="Polyetherimide",
            abbreviation="PEI",
            trade_names=["Ultem"],
            family=PolymerFamily.THERMOPLASTIC,
            temp_min_c=-40,
            temp_max_continuous_c=170,
            temp_max_short_term_c=200,
            glass_transition_c=217,
            heat_deflection_c=200,
            tensile_strength_mpa=105,
            tensile_modulus_mpa=3000,
            elongation_percent=60,
            flexural_strength_mpa=150,
            density_g_cm3=1.27,
            water_absorption_percent=0.25,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.EXCELLENT,
                "acids_dilute": ChemicalResistance.GOOD,
                "alcohols": ChemicalResistance.GOOD,
            },
            sterilization_methods=["autoclave", "gamma", "eto"],
            food_contact_approved=True,
            typical_applications=["aerospace", "medical", "electrical connectors"],
            cost_factor=10.0
        )

    def _load_elastomers(self):
        """Load rubber and elastomer materials"""

        self._polymers["NBR"] = PolymerSpec(
            name="Nitrile Butadiene Rubber",
            abbreviation="NBR",
            trade_names=["Buna-N"],
            family=PolymerFamily.ELASTOMER,
            temp_min_c=-30,
            temp_max_continuous_c=100,
            temp_max_short_term_c=120,
            tensile_strength_mpa=18,
            elongation_percent=400,
            hardness_shore="A70",
            density_g_cm3=1.00,
            chemical_resistance={
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.EXCELLENT,
                "water": ChemicalResistance.GOOD,
                "acids_dilute": ChemicalResistance.GOOD,
                "ozone": ChemicalResistance.POOR,
                "ketones": ChemicalResistance.POOR,
            },
            typical_applications=["o-rings", "seals", "gaskets", "hoses"],
            cost_factor=1.5
        )

        self._polymers["EPDM"] = PolymerSpec(
            name="Ethylene Propylene Diene Monomer",
            abbreviation="EPDM",
            trade_names=["Nordel", "Keltan"],
            family=PolymerFamily.ELASTOMER,
            temp_min_c=-50,
            temp_max_continuous_c=130,
            temp_max_short_term_c=150,
            tensile_strength_mpa=15,
            elongation_percent=500,
            hardness_shore="A60",
            density_g_cm3=0.86,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "steam": ChemicalResistance.EXCELLENT,
                "acids_dilute": ChemicalResistance.EXCELLENT,
                "bases": ChemicalResistance.EXCELLENT,
                "ozone": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.POOR,
                "fuels": ChemicalResistance.POOR,
            },
            sterilization_methods=["autoclave", "gamma"],
            food_contact_approved=True,
            uv_resistant=True,
            typical_applications=["weatherstripping", "roofing", "automotive seals"],
            cost_factor=2.0
        )

        self._polymers["Silicone"] = PolymerSpec(
            name="Silicone Rubber",
            abbreviation="VMQ",
            trade_names=["Silastic", "Elastosil"],
            family=PolymerFamily.ELASTOMER,
            temp_min_c=-60,
            temp_max_continuous_c=200,
            temp_max_short_term_c=230,
            tensile_strength_mpa=10,
            elongation_percent=600,
            hardness_shore="A50",
            density_g_cm3=1.10,
            chemical_resistance={
                "water": ChemicalResistance.EXCELLENT,
                "ozone": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.FAIR,
                "fuels": ChemicalResistance.POOR,
                "steam": ChemicalResistance.EXCELLENT,
            },
            sterilization_methods=["autoclave", "gamma", "eto"],
            food_contact_approved=True,
            uv_resistant=True,
            typical_applications=["medical", "food processing", "high-temp seals"],
            cost_factor=4.0
        )

    def _load_fluoropolymers(self):
        """Load fluoropolymer materials"""

        self._polymers["PTFE"] = PolymerSpec(
            name="Polytetrafluoroethylene",
            abbreviation="PTFE",
            trade_names=["Teflon", "Fluorosint"],
            family=PolymerFamily.FLUOROPOLYMER,
            temp_min_c=-200,
            temp_max_continuous_c=260,
            temp_max_short_term_c=300,
            melting_point_c=327,
            tensile_strength_mpa=25,
            tensile_modulus_mpa=500,
            elongation_percent=400,
            hardness_shore="D55",
            density_g_cm3=2.17,
            water_absorption_percent=0.01,
            coefficient_friction=0.04,
            chemical_resistance={
                "acids_strong": ChemicalResistance.EXCELLENT,
                "bases": ChemicalResistance.EXCELLENT,
                "solvents": ChemicalResistance.EXCELLENT,
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.EXCELLENT,
                "water": ChemicalResistance.EXCELLENT,
            },
            sterilization_methods=["autoclave", "gamma", "eto"],
            food_contact_approved=True,
            uv_resistant=True,
            typical_applications=["seals", "bearings", "linings", "non-stick"],
            cost_factor=8.0
        )

        self._polymers["FKM"] = PolymerSpec(
            name="Fluoroelastomer",
            abbreviation="FKM",
            trade_names=["Viton", "Fluorel", "Tecnoflon"],
            family=PolymerFamily.FLUOROPOLYMER,
            temp_min_c=-20,
            temp_max_continuous_c=200,
            temp_max_short_term_c=230,
            tensile_strength_mpa=15,
            elongation_percent=250,
            hardness_shore="A75",
            density_g_cm3=1.85,
            chemical_resistance={
                "oils": ChemicalResistance.EXCELLENT,
                "fuels": ChemicalResistance.EXCELLENT,
                "hydraulic_fluid": ChemicalResistance.EXCELLENT,
                "acids_dilute": ChemicalResistance.EXCELLENT,
                "acids_strong": ChemicalResistance.GOOD,
                "ketones": ChemicalResistance.POOR,
                "esters": ChemicalResistance.POOR,
                "amines": ChemicalResistance.POOR,
            },
            sterilization_methods=["autoclave"],
            typical_applications=["o-rings", "seals", "gaskets", "aerospace"],
            cost_factor=5.0
        )

        self._polymers["PVDF"] = PolymerSpec(
            name="Polyvinylidene Fluoride",
            abbreviation="PVDF",
            trade_names=["Kynar", "Solef"],
            family=PolymerFamily.FLUOROPOLYMER,
            temp_min_c=-40,
            temp_max_continuous_c=150,
            temp_max_short_term_c=175,
            melting_point_c=170,
            tensile_strength_mpa=50,
            tensile_modulus_mpa=2100,
            elongation_percent=50,
            hardness_shore="D75",
            density_g_cm3=1.78,
            water_absorption_percent=0.04,
            chemical_resistance={
                "acids_strong": ChemicalResistance.EXCELLENT,
                "bases": ChemicalResistance.EXCELLENT,
                "solvents": ChemicalResistance.GOOD,
                "oils": ChemicalResistance.EXCELLENT,
            },
            uv_resistant=True,
            typical_applications=["chemical processing", "piping", "coatings"],
            cost_factor=6.0
        )

    def get(self, name: str) -> Optional[PolymerSpec]:
        """Get polymer by name"""
        return self._polymers.get(name)

    def search(
        self,
        min_temp_c: Optional[float] = None,
        chemical: Optional[str] = None,
        family: Optional[PolymerFamily] = None
    ) -> List[PolymerSpec]:
        """Search polymers by criteria"""
        results = []
        for polymer in self._polymers.values():
            if min_temp_c and polymer.temp_max_continuous_c < min_temp_c:
                continue
            if family and polymer.family != family:
                continue
            if chemical:
                chem_resistance = polymer.chemical_resistance.get(chemical)
                if chem_resistance in [ChemicalResistance.POOR, ChemicalResistance.NOT_RECOMMENDED]:
                    continue
            results.append(polymer)
        return results

    def list_all(self) -> List[str]:
        """List all polymer names"""
        return list(self._polymers.keys())

    @property
    def count(self) -> int:
        """Number of polymers in database"""
        return len(self._polymers)
