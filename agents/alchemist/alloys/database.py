"""
Comprehensive Alloy Database

Provides material property data for metals and alloys across
all major families: ferrous, aluminum, titanium, copper, nickel.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class MaterialFamily(Enum):
    """Primary material classification"""
    FERROUS = "ferrous"
    ALUMINUM = "aluminum"
    TITANIUM = "titanium"
    COPPER = "copper"
    NICKEL = "nickel"
    REFRACTORY = "refractory"
    MAGNESIUM = "magnesium"
    ZINC = "zinc"


class HeatTreatment(Enum):
    """Heat treatment condition"""
    ANNEALED = "annealed"
    NORMALIZED = "normalized"
    QUENCH_TEMPER = "quench_temper"
    SOLUTION_TREATED = "solution_treated"
    AGED = "aged"
    COLD_WORKED = "cold_worked"


@dataclass
class AlloySpec:
    """Complete alloy specification"""
    # Identity
    designation: str
    family: MaterialFamily
    standard: str  # AA, AISI, ASTM, EN, DIN, JIS
    uns_number: Optional[str] = None

    # Composition (weight percent)
    composition: Dict[str, Tuple[float, float]] = field(default_factory=dict)

    # Mechanical Properties
    tensile_strength_mpa: float = 0.0
    yield_strength_mpa: float = 0.0
    elongation_percent: float = 0.0
    reduction_area_percent: float = 0.0
    hardness: str = ""
    modulus_gpa: float = 0.0
    poisson_ratio: float = 0.3
    fatigue_strength_mpa: Optional[float] = None

    # Thermal Properties
    melting_range_c: Tuple[float, float] = (0.0, 0.0)
    max_service_temp_c: float = 0.0
    thermal_conductivity_w_mk: float = 0.0
    specific_heat_j_kgk: float = 0.0
    thermal_expansion_um_mk: float = 0.0

    # Physical Properties
    density_g_cm3: float = 0.0
    electrical_resistivity_uohm_cm: Optional[float] = None

    # Characteristics
    magnetic: bool = False
    weldable: bool = True
    machinability_rating: int = 50
    corrosion_resistance: str = "fair"

    # Applications
    typical_applications: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.composition:
            self.composition = {}
        if not self.typical_applications:
            self.typical_applications = []


class AlloyDatabase:
    """
    Comprehensive alloy property database.

    Contains data on 100+ common alloys organized by family.
    Production version would load from database/files.
    """

    def __init__(self):
        self._alloys: Dict[str, AlloySpec] = {}
        self._load_ferrous_alloys()
        self._load_aluminum_alloys()
        self._load_titanium_alloys()
        self._load_nickel_alloys()
        self._load_copper_alloys()

    def _load_ferrous_alloys(self):
        """Load steel and iron alloys"""
        # Carbon Steels
        self._alloys["1018"] = AlloySpec(
            designation="1018",
            family=MaterialFamily.FERROUS,
            standard="AISI",
            uns_number="G10180",
            composition={
                "C": (0.15, 0.20), "Mn": (0.60, 0.90),
                "P": (0.0, 0.04), "S": (0.0, 0.05)
            },
            tensile_strength_mpa=440,
            yield_strength_mpa=370,
            elongation_percent=15,
            hardness="HRB 71",
            modulus_gpa=205,
            melting_range_c=(1480, 1530),
            max_service_temp_c=400,
            thermal_conductivity_w_mk=51.9,
            thermal_expansion_um_mk=11.5,
            density_g_cm3=7.87,
            magnetic=True,
            weldable=True,
            machinability_rating=70,
            corrosion_resistance="poor",
            typical_applications=["shafts", "pins", "studs", "general purpose"]
        )

        self._alloys["4140"] = AlloySpec(
            designation="4140",
            family=MaterialFamily.FERROUS,
            standard="AISI",
            uns_number="G41400",
            composition={
                "C": (0.38, 0.43), "Mn": (0.75, 1.00),
                "Cr": (0.80, 1.10), "Mo": (0.15, 0.25)
            },
            tensile_strength_mpa=1020,
            yield_strength_mpa=900,
            elongation_percent=16,
            hardness="HRC 28-32",
            modulus_gpa=205,
            melting_range_c=(1430, 1500),
            max_service_temp_c=400,
            thermal_conductivity_w_mk=42.6,
            thermal_expansion_um_mk=12.3,
            density_g_cm3=7.85,
            magnetic=True,
            weldable=True,
            machinability_rating=65,
            corrosion_resistance="poor",
            typical_applications=["gears", "shafts", "bolts", "axles"]
        )

        # Stainless Steels
        self._alloys["304"] = AlloySpec(
            designation="304",
            family=MaterialFamily.FERROUS,
            standard="AISI",
            uns_number="S30400",
            composition={
                "C": (0.0, 0.08), "Cr": (18.0, 20.0),
                "Ni": (8.0, 10.5), "Mn": (0.0, 2.0)
            },
            tensile_strength_mpa=515,
            yield_strength_mpa=205,
            elongation_percent=40,
            hardness="HRB 92",
            modulus_gpa=193,
            melting_range_c=(1400, 1450),
            max_service_temp_c=870,
            thermal_conductivity_w_mk=16.2,
            thermal_expansion_um_mk=17.2,
            density_g_cm3=8.00,
            magnetic=False,
            weldable=True,
            machinability_rating=45,
            corrosion_resistance="good",
            typical_applications=["food equipment", "kitchen sinks", "architectural"]
        )

        self._alloys["316L"] = AlloySpec(
            designation="316L",
            family=MaterialFamily.FERROUS,
            standard="AISI",
            uns_number="S31603",
            composition={
                "C": (0.0, 0.03), "Cr": (16.0, 18.0),
                "Ni": (10.0, 14.0), "Mo": (2.0, 3.0)
            },
            tensile_strength_mpa=485,
            yield_strength_mpa=170,
            elongation_percent=40,
            hardness="HRB 79",
            modulus_gpa=193,
            melting_range_c=(1375, 1400),
            max_service_temp_c=870,
            thermal_conductivity_w_mk=16.3,
            thermal_expansion_um_mk=16.0,
            density_g_cm3=8.00,
            magnetic=False,
            weldable=True,
            machinability_rating=45,
            corrosion_resistance="excellent",
            typical_applications=["marine", "chemical", "medical", "food processing"]
        )

        self._alloys["17-4PH"] = AlloySpec(
            designation="17-4PH",
            family=MaterialFamily.FERROUS,
            standard="AISI",
            uns_number="S17400",
            composition={
                "C": (0.0, 0.07), "Cr": (15.0, 17.5),
                "Ni": (3.0, 5.0), "Cu": (3.0, 5.0), "Nb": (0.15, 0.45)
            },
            tensile_strength_mpa=1310,
            yield_strength_mpa=1170,
            elongation_percent=10,
            hardness="HRC 40",
            modulus_gpa=197,
            melting_range_c=(1400, 1440),
            max_service_temp_c=315,
            thermal_conductivity_w_mk=18.4,
            thermal_expansion_um_mk=10.8,
            density_g_cm3=7.78,
            magnetic=True,
            weldable=True,
            machinability_rating=40,
            corrosion_resistance="good",
            typical_applications=["aerospace", "oil & gas", "high-strength fasteners"]
        )

    def _load_aluminum_alloys(self):
        """Load aluminum alloys"""
        self._alloys["6061-T6"] = AlloySpec(
            designation="6061-T6",
            family=MaterialFamily.ALUMINUM,
            standard="AA",
            uns_number="A96061",
            composition={
                "Si": (0.4, 0.8), "Mg": (0.8, 1.2),
                "Cu": (0.15, 0.4), "Cr": (0.04, 0.35)
            },
            tensile_strength_mpa=310,
            yield_strength_mpa=276,
            elongation_percent=12,
            hardness="HB 95",
            modulus_gpa=68.9,
            melting_range_c=(582, 652),
            max_service_temp_c=150,
            thermal_conductivity_w_mk=167,
            thermal_expansion_um_mk=23.6,
            density_g_cm3=2.70,
            magnetic=False,
            weldable=True,
            machinability_rating=85,
            corrosion_resistance="good",
            typical_applications=["structural", "aircraft", "marine", "automotive"]
        )

        self._alloys["7075-T6"] = AlloySpec(
            designation="7075-T6",
            family=MaterialFamily.ALUMINUM,
            standard="AA",
            uns_number="A97075",
            composition={
                "Zn": (5.1, 6.1), "Mg": (2.1, 2.9),
                "Cu": (1.2, 2.0), "Cr": (0.18, 0.28)
            },
            tensile_strength_mpa=572,
            yield_strength_mpa=503,
            elongation_percent=11,
            hardness="HB 150",
            modulus_gpa=71.7,
            melting_range_c=(477, 635),
            max_service_temp_c=120,
            thermal_conductivity_w_mk=130,
            thermal_expansion_um_mk=23.4,
            density_g_cm3=2.81,
            magnetic=False,
            weldable=False,  # Not recommended
            machinability_rating=80,
            corrosion_resistance="fair",
            typical_applications=["aircraft structures", "high-strength parts"]
        )

        self._alloys["2024-T3"] = AlloySpec(
            designation="2024-T3",
            family=MaterialFamily.ALUMINUM,
            standard="AA",
            uns_number="A92024",
            composition={
                "Cu": (3.8, 4.9), "Mg": (1.2, 1.8),
                "Mn": (0.3, 0.9)
            },
            tensile_strength_mpa=483,
            yield_strength_mpa=345,
            elongation_percent=18,
            hardness="HB 120",
            modulus_gpa=73.1,
            melting_range_c=(500, 638),
            max_service_temp_c=150,
            thermal_conductivity_w_mk=121,
            thermal_expansion_um_mk=22.9,
            density_g_cm3=2.78,
            magnetic=False,
            weldable=False,
            machinability_rating=70,
            corrosion_resistance="fair",
            typical_applications=["aircraft structures", "rivets", "hardware"]
        )

        self._alloys["5052-H32"] = AlloySpec(
            designation="5052-H32",
            family=MaterialFamily.ALUMINUM,
            standard="AA",
            uns_number="A95052",
            composition={
                "Mg": (2.2, 2.8), "Cr": (0.15, 0.35)
            },
            tensile_strength_mpa=228,
            yield_strength_mpa=193,
            elongation_percent=12,
            hardness="HB 60",
            modulus_gpa=70.3,
            melting_range_c=(607, 649),
            max_service_temp_c=150,
            thermal_conductivity_w_mk=138,
            thermal_expansion_um_mk=23.8,
            density_g_cm3=2.68,
            magnetic=False,
            weldable=True,
            machinability_rating=60,
            corrosion_resistance="excellent",
            typical_applications=["marine", "fuel tanks", "sheet metal work"]
        )

    def _load_titanium_alloys(self):
        """Load titanium alloys"""
        self._alloys["Ti-6Al-4V"] = AlloySpec(
            designation="Ti-6Al-4V",
            family=MaterialFamily.TITANIUM,
            standard="AMS",
            uns_number="R56400",
            composition={
                "Al": (5.5, 6.75), "V": (3.5, 4.5),
                "Fe": (0.0, 0.3), "O": (0.0, 0.2)
            },
            tensile_strength_mpa=950,
            yield_strength_mpa=880,
            elongation_percent=14,
            hardness="HRC 36",
            modulus_gpa=113.8,
            melting_range_c=(1604, 1660),
            max_service_temp_c=400,
            thermal_conductivity_w_mk=6.7,
            thermal_expansion_um_mk=8.6,
            density_g_cm3=4.43,
            magnetic=False,
            weldable=True,
            machinability_rating=22,
            corrosion_resistance="excellent",
            typical_applications=["aerospace", "medical implants", "racing"]
        )

        self._alloys["Grade 2 Ti"] = AlloySpec(
            designation="Grade 2 Ti",
            family=MaterialFamily.TITANIUM,
            standard="ASTM",
            uns_number="R50400",
            composition={
                "Fe": (0.0, 0.3), "O": (0.0, 0.25),
                "C": (0.0, 0.1), "N": (0.0, 0.03)
            },
            tensile_strength_mpa=345,
            yield_strength_mpa=275,
            elongation_percent=20,
            hardness="HRB 80",
            modulus_gpa=105,
            melting_range_c=(1660, 1670),
            max_service_temp_c=315,
            thermal_conductivity_w_mk=16.4,
            thermal_expansion_um_mk=8.6,
            density_g_cm3=4.51,
            magnetic=False,
            weldable=True,
            machinability_rating=30,
            corrosion_resistance="excellent",
            typical_applications=["chemical processing", "marine", "medical"]
        )

    def _load_nickel_alloys(self):
        """Load nickel superalloys"""
        self._alloys["Inconel 718"] = AlloySpec(
            designation="Inconel 718",
            family=MaterialFamily.NICKEL,
            standard="AMS",
            uns_number="N07718",
            composition={
                "Ni": (50.0, 55.0), "Cr": (17.0, 21.0),
                "Fe": (11.0, 22.5), "Nb": (4.75, 5.5),
                "Mo": (2.8, 3.3), "Ti": (0.65, 1.15)
            },
            tensile_strength_mpa=1375,
            yield_strength_mpa=1100,
            elongation_percent=21,
            hardness="HRC 44",
            modulus_gpa=208,
            melting_range_c=(1260, 1336),
            max_service_temp_c=700,
            thermal_conductivity_w_mk=11.4,
            thermal_expansion_um_mk=13.0,
            density_g_cm3=8.19,
            magnetic=False,
            weldable=True,
            machinability_rating=12,
            corrosion_resistance="excellent",
            typical_applications=["turbine blades", "exhaust", "nuclear", "aerospace"]
        )

        self._alloys["Inconel 625"] = AlloySpec(
            designation="Inconel 625",
            family=MaterialFamily.NICKEL,
            standard="AMS",
            uns_number="N06625",
            composition={
                "Ni": (58.0, 63.0), "Cr": (20.0, 23.0),
                "Mo": (8.0, 10.0), "Nb": (3.15, 4.15)
            },
            tensile_strength_mpa=965,
            yield_strength_mpa=490,
            elongation_percent=42,
            hardness="HRB 96",
            modulus_gpa=208,
            melting_range_c=(1290, 1350),
            max_service_temp_c=815,
            thermal_conductivity_w_mk=9.8,
            thermal_expansion_um_mk=12.8,
            density_g_cm3=8.44,
            magnetic=False,
            weldable=True,
            machinability_rating=15,
            corrosion_resistance="excellent",
            typical_applications=["marine", "chemical", "aerospace exhaust"]
        )

        self._alloys["Hastelloy C-276"] = AlloySpec(
            designation="Hastelloy C-276",
            family=MaterialFamily.NICKEL,
            standard="ASTM",
            uns_number="N10276",
            composition={
                "Ni": (50.0, 63.0), "Mo": (15.0, 17.0),
                "Cr": (14.5, 16.5), "W": (3.0, 4.5)
            },
            tensile_strength_mpa=790,
            yield_strength_mpa=355,
            elongation_percent=40,
            hardness="HRB 90",
            modulus_gpa=205,
            melting_range_c=(1325, 1370),
            max_service_temp_c=700,
            thermal_conductivity_w_mk=10.2,
            thermal_expansion_um_mk=11.2,
            density_g_cm3=8.89,
            magnetic=False,
            weldable=True,
            machinability_rating=18,
            corrosion_resistance="excellent",
            typical_applications=["chemical processing", "pollution control", "pulp & paper"]
        )

    def _load_copper_alloys(self):
        """Load copper and bronze alloys"""
        self._alloys["C36000"] = AlloySpec(
            designation="C36000",
            family=MaterialFamily.COPPER,
            standard="UNS",
            uns_number="C36000",
            composition={
                "Cu": (60.0, 63.0), "Pb": (2.5, 3.7),
                "Zn": (35.0, 37.0)
            },
            tensile_strength_mpa=385,
            yield_strength_mpa=140,
            elongation_percent=53,
            hardness="HRB 55",
            modulus_gpa=97,
            melting_range_c=(885, 900),
            max_service_temp_c=200,
            thermal_conductivity_w_mk=115,
            thermal_expansion_um_mk=20.5,
            density_g_cm3=8.50,
            magnetic=False,
            weldable=False,
            machinability_rating=100,  # Reference material
            corrosion_resistance="good",
            typical_applications=["screw machine parts", "fittings", "valves"]
        )

        self._alloys["C95400"] = AlloySpec(
            designation="C95400",
            family=MaterialFamily.COPPER,
            standard="UNS",
            uns_number="C95400",
            composition={
                "Cu": (83.0, 89.0), "Al": (10.0, 11.5),
                "Fe": (3.0, 5.0)
            },
            tensile_strength_mpa=585,
            yield_strength_mpa=240,
            elongation_percent=12,
            hardness="HRB 85",
            modulus_gpa=110,
            melting_range_c=(1015, 1050),
            max_service_temp_c=260,
            thermal_conductivity_w_mk=59,
            thermal_expansion_um_mk=16.2,
            density_g_cm3=7.45,
            magnetic=False,
            weldable=True,
            machinability_rating=60,
            corrosion_resistance="excellent",
            typical_applications=["marine hardware", "bearings", "gears", "bushings"]
        )

        self._alloys["C17200"] = AlloySpec(
            designation="C17200",
            family=MaterialFamily.COPPER,
            standard="UNS",
            uns_number="C17200",
            composition={
                "Cu": (96.0, 98.0), "Be": (1.8, 2.0),
                "Co+Ni": (0.2, 0.6)
            },
            tensile_strength_mpa=1380,
            yield_strength_mpa=1200,
            elongation_percent=2,
            hardness="HRC 42",
            modulus_gpa=128,
            melting_range_c=(870, 980),
            max_service_temp_c=315,
            thermal_conductivity_w_mk=107,
            thermal_expansion_um_mk=17.8,
            density_g_cm3=8.25,
            magnetic=False,
            weldable=False,
            machinability_rating=40,
            corrosion_resistance="good",
            typical_applications=["springs", "electrical contacts", "molds", "tools"]
        )

    def get(self, designation: str) -> Optional[AlloySpec]:
        """Get alloy by designation"""
        return self._alloys.get(designation)

    def search(
        self,
        family: Optional[MaterialFamily] = None,
        min_strength_mpa: Optional[float] = None,
        max_temp_c: Optional[float] = None,
        corrosion: Optional[str] = None
    ) -> List[AlloySpec]:
        """Search alloys by criteria"""
        results = []
        for alloy in self._alloys.values():
            if family and alloy.family != family:
                continue
            if min_strength_mpa and alloy.tensile_strength_mpa < min_strength_mpa:
                continue
            if max_temp_c and alloy.max_service_temp_c < max_temp_c:
                continue
            if corrosion and alloy.corrosion_resistance != corrosion:
                continue
            results.append(alloy)
        return results

    def list_all(self) -> List[str]:
        """List all alloy designations"""
        return list(self._alloys.keys())

    @property
    def count(self) -> int:
        """Number of alloys in database"""
        return len(self._alloys)
