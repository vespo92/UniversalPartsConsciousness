"""
Composites and Advanced Materials Database

Database of composite materials including carbon fiber,
fiberglass, aramid (Kevlar), and technical ceramics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class FiberType(Enum):
    """Reinforcement fiber type"""
    CARBON = "carbon"
    GLASS_E = "glass_e"
    GLASS_S = "glass_s"
    ARAMID = "aramid"
    BASALT = "basalt"
    NATURAL = "natural"


class MatrixType(Enum):
    """Matrix material type"""
    EPOXY = "epoxy"
    POLYESTER = "polyester"
    VINYL_ESTER = "vinyl_ester"
    THERMOPLASTIC = "thermoplastic"
    CERAMIC = "ceramic"
    METAL = "metal"


class WeavePattern(Enum):
    """Fabric weave pattern"""
    UNIDIRECTIONAL = "unidirectional"
    PLAIN = "plain"
    TWILL_2X2 = "twill_2x2"
    SATIN_5HS = "satin_5hs"
    BIAXIAL = "biaxial"
    TRIAXIAL = "triaxial"
    RANDOM = "random"


@dataclass
class CompositeSpec:
    """Complete composite material specification"""
    name: str
    fiber_type: FiberType
    matrix_type: MatrixType
    weave_pattern: Optional[WeavePattern] = None

    # Mechanical Properties (fiber direction for UD)
    tensile_strength_mpa: float = 0.0
    tensile_modulus_gpa: float = 0.0
    compressive_strength_mpa: float = 0.0
    flexural_strength_mpa: float = 0.0
    shear_strength_mpa: float = 0.0

    # Transverse properties (if applicable)
    tensile_strength_transverse_mpa: Optional[float] = None
    tensile_modulus_transverse_gpa: Optional[float] = None

    # Thermal Properties
    temperature_max_c: float = 100.0
    thermal_conductivity_w_mk: float = 0.5
    cte_longitudinal_um_mk: float = 0.0
    cte_transverse_um_mk: float = 0.0

    # Physical Properties
    density_g_cm3: float = 0.0
    fiber_volume_percent: float = 50.0

    # Additional characteristics
    electrical_conductivity: str = "insulator"
    uv_resistant: bool = False
    chemical_resistance: str = "good"

    # Processing
    processing_methods: List[str] = field(default_factory=list)
    typical_applications: List[str] = field(default_factory=list)

    # Cost
    relative_cost: float = 1.0  # 1.0 = E-glass baseline

    def __post_init__(self):
        if not self.processing_methods:
            self.processing_methods = []
        if not self.typical_applications:
            self.typical_applications = []


@dataclass
class CeramicSpec:
    """Technical ceramic specification"""
    name: str
    composition: str

    # Mechanical Properties
    tensile_strength_mpa: float = 0.0
    compressive_strength_mpa: float = 0.0
    flexural_strength_mpa: float = 0.0
    hardness_hv: float = 0.0
    fracture_toughness_mpa_m05: float = 0.0

    # Thermal Properties
    temperature_max_c: float = 1000.0
    thermal_conductivity_w_mk: float = 10.0
    cte_um_mk: float = 5.0
    thermal_shock_resistance: str = "fair"

    # Physical Properties
    density_g_cm3: float = 3.0

    # Electrical
    electrical_resistivity_ohm_cm: float = 1e12

    # Applications
    typical_applications: List[str] = field(default_factory=list)
    relative_cost: float = 10.0

    def __post_init__(self):
        if not self.typical_applications:
            self.typical_applications = []


class CompositeDatabase:
    """
    Database of composite and advanced materials.

    Covers fiber-reinforced polymers (FRP), metal matrix
    composites (MMC), and technical ceramics.
    """

    def __init__(self):
        self._composites: Dict[str, CompositeSpec] = {}
        self._ceramics: Dict[str, CeramicSpec] = {}
        self._load_carbon_fiber()
        self._load_fiberglass()
        self._load_aramid()
        self._load_ceramics()

    def _load_carbon_fiber(self):
        """Load carbon fiber composite specifications"""

        self._composites["CFRP Standard Modulus UD"] = CompositeSpec(
            name="Carbon Fiber/Epoxy - Standard Modulus Unidirectional",
            fiber_type=FiberType.CARBON,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.UNIDIRECTIONAL,
            tensile_strength_mpa=1500,
            tensile_modulus_gpa=135,
            compressive_strength_mpa=1200,
            flexural_strength_mpa=1500,
            shear_strength_mpa=80,
            tensile_strength_transverse_mpa=50,
            tensile_modulus_transverse_gpa=10,
            temperature_max_c=120,  # Epoxy limited
            thermal_conductivity_w_mk=5.0,
            cte_longitudinal_um_mk=-0.5,  # Negative!
            cte_transverse_um_mk=25.0,
            density_g_cm3=1.55,
            fiber_volume_percent=60,
            electrical_conductivity="conductive",
            uv_resistant=False,
            chemical_resistance="good",
            processing_methods=["prepreg_autoclave", "filament_winding", "infusion"],
            typical_applications=["aerospace_structures", "racing", "sporting_goods"],
            relative_cost=15.0
        )

        self._composites["CFRP High Modulus UD"] = CompositeSpec(
            name="Carbon Fiber/Epoxy - High Modulus Unidirectional",
            fiber_type=FiberType.CARBON,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.UNIDIRECTIONAL,
            tensile_strength_mpa=1200,
            tensile_modulus_gpa=200,
            compressive_strength_mpa=900,
            flexural_strength_mpa=1200,
            shear_strength_mpa=60,
            temperature_max_c=120,
            thermal_conductivity_w_mk=70.0,  # High modulus = high conductivity
            cte_longitudinal_um_mk=-1.0,
            cte_transverse_um_mk=20.0,
            density_g_cm3=1.65,
            fiber_volume_percent=60,
            electrical_conductivity="conductive",
            processing_methods=["prepreg_autoclave"],
            typical_applications=["satellite_structures", "space", "high_stiffness"],
            relative_cost=40.0
        )

        self._composites["CFRP Twill 2x2"] = CompositeSpec(
            name="Carbon Fiber/Epoxy - 2x2 Twill Fabric",
            fiber_type=FiberType.CARBON,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.TWILL_2X2,
            tensile_strength_mpa=600,  # Quasi-isotropic layup
            tensile_modulus_gpa=70,
            compressive_strength_mpa=550,
            flexural_strength_mpa=700,
            shear_strength_mpa=90,
            temperature_max_c=120,
            cte_longitudinal_um_mk=2.0,
            cte_transverse_um_mk=2.0,
            density_g_cm3=1.55,
            fiber_volume_percent=55,
            electrical_conductivity="conductive",
            processing_methods=["wet_layup", "vacuum_bag", "prepreg"],
            typical_applications=["automotive", "cosmetic_parts", "general_structural"],
            relative_cost=12.0
        )

        self._composites["CFRP High Temp"] = CompositeSpec(
            name="Carbon Fiber/BMI - High Temperature",
            fiber_type=FiberType.CARBON,
            matrix_type=MatrixType.EPOXY,  # Actually BMI
            weave_pattern=WeavePattern.UNIDIRECTIONAL,
            tensile_strength_mpa=1400,
            tensile_modulus_gpa=130,
            compressive_strength_mpa=1100,
            temperature_max_c=230,  # BMI advantage
            density_g_cm3=1.58,
            fiber_volume_percent=60,
            electrical_conductivity="conductive",
            processing_methods=["prepreg_autoclave"],
            typical_applications=["jet_engines", "high_temp_aerospace", "race_exhaust"],
            relative_cost=30.0
        )

    def _load_fiberglass(self):
        """Load fiberglass composite specifications"""

        self._composites["GFRP E-Glass UD"] = CompositeSpec(
            name="E-Glass/Epoxy - Unidirectional",
            fiber_type=FiberType.GLASS_E,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.UNIDIRECTIONAL,
            tensile_strength_mpa=1000,
            tensile_modulus_gpa=40,
            compressive_strength_mpa=600,
            flexural_strength_mpa=1100,
            shear_strength_mpa=70,
            tensile_strength_transverse_mpa=40,
            tensile_modulus_transverse_gpa=8,
            temperature_max_c=120,
            thermal_conductivity_w_mk=0.3,
            cte_longitudinal_um_mk=6.0,
            cte_transverse_um_mk=20.0,
            density_g_cm3=1.90,
            fiber_volume_percent=55,
            electrical_conductivity="insulator",
            uv_resistant=False,
            chemical_resistance="good",
            processing_methods=["filament_winding", "pultrusion", "infusion"],
            typical_applications=["pipes", "tanks", "electrical"],
            relative_cost=1.0
        )

        self._composites["GFRP E-Glass Fabric"] = CompositeSpec(
            name="E-Glass/Polyester - Fabric",
            fiber_type=FiberType.GLASS_E,
            matrix_type=MatrixType.POLYESTER,
            weave_pattern=WeavePattern.PLAIN,
            tensile_strength_mpa=300,
            tensile_modulus_gpa=20,
            compressive_strength_mpa=250,
            flexural_strength_mpa=350,
            shear_strength_mpa=50,
            temperature_max_c=80,
            density_g_cm3=1.70,
            fiber_volume_percent=40,
            electrical_conductivity="insulator",
            chemical_resistance="fair",
            processing_methods=["wet_layup", "spray_up", "smc"],
            typical_applications=["boats", "automotive_body", "construction"],
            relative_cost=0.6
        )

        self._composites["GFRP S-Glass UD"] = CompositeSpec(
            name="S-Glass/Epoxy - High Strength",
            fiber_type=FiberType.GLASS_S,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.UNIDIRECTIONAL,
            tensile_strength_mpa=1500,
            tensile_modulus_gpa=55,
            compressive_strength_mpa=800,
            temperature_max_c=120,
            density_g_cm3=1.95,
            fiber_volume_percent=60,
            electrical_conductivity="insulator",
            processing_methods=["prepreg_autoclave", "filament_winding"],
            typical_applications=["aerospace", "ballistic", "pressure_vessels"],
            relative_cost=4.0
        )

    def _load_aramid(self):
        """Load aramid (Kevlar) composite specifications"""

        self._composites["AFRP Kevlar UD"] = CompositeSpec(
            name="Aramid/Epoxy - Unidirectional (Kevlar 49)",
            fiber_type=FiberType.ARAMID,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.UNIDIRECTIONAL,
            tensile_strength_mpa=1400,
            tensile_modulus_gpa=80,
            compressive_strength_mpa=280,  # Weakness!
            flexural_strength_mpa=500,
            shear_strength_mpa=50,
            temperature_max_c=150,  # Better than carbon/epoxy
            thermal_conductivity_w_mk=0.04,
            cte_longitudinal_um_mk=-4.0,  # Negative
            cte_transverse_um_mk=60.0,
            density_g_cm3=1.38,  # Lightest
            fiber_volume_percent=55,
            electrical_conductivity="insulator",
            uv_resistant=False,  # Degrades in UV
            chemical_resistance="good",
            processing_methods=["prepreg", "wet_layup", "filament_winding"],
            typical_applications=["ballistic", "aerospace", "pressure_vessels", "impact"],
            relative_cost=8.0
        )

        self._composites["AFRP Kevlar Fabric"] = CompositeSpec(
            name="Aramid/Epoxy - Plain Weave Fabric",
            fiber_type=FiberType.ARAMID,
            matrix_type=MatrixType.EPOXY,
            weave_pattern=WeavePattern.PLAIN,
            tensile_strength_mpa=500,
            tensile_modulus_gpa=30,
            compressive_strength_mpa=150,
            temperature_max_c=150,
            density_g_cm3=1.35,
            fiber_volume_percent=50,
            electrical_conductivity="insulator",
            processing_methods=["wet_layup", "vacuum_bag"],
            typical_applications=["protective_equipment", "kayaks", "canoes"],
            relative_cost=6.0
        )

    def _load_ceramics(self):
        """Load technical ceramic specifications"""

        self._ceramics["Alumina 99.5%"] = CeramicSpec(
            name="Alumina (Al2O3) 99.5%",
            composition="Al2O3 99.5%",
            tensile_strength_mpa=260,
            compressive_strength_mpa=2600,
            flexural_strength_mpa=380,
            hardness_hv=1700,
            fracture_toughness_mpa_m05=4.0,
            temperature_max_c=1700,
            thermal_conductivity_w_mk=30,
            cte_um_mk=8.1,
            thermal_shock_resistance="fair",
            density_g_cm3=3.89,
            electrical_resistivity_ohm_cm=1e14,
            typical_applications=["wear_parts", "electrical_insulators", "cutting_tools"],
            relative_cost=10.0
        )

        self._ceramics["Silicon Carbide"] = CeramicSpec(
            name="Silicon Carbide (SiC)",
            composition="SiC",
            tensile_strength_mpa=250,
            compressive_strength_mpa=3900,
            flexural_strength_mpa=450,
            hardness_hv=2800,
            fracture_toughness_mpa_m05=4.5,
            temperature_max_c=1650,
            thermal_conductivity_w_mk=120,
            cte_um_mk=4.0,
            thermal_shock_resistance="excellent",
            density_g_cm3=3.10,
            electrical_resistivity_ohm_cm=1e5,  # Semiconductor
            typical_applications=["seals", "bearings", "armor", "semiconductor"],
            relative_cost=30.0
        )

        self._ceramics["Zirconia (Y-TZP)"] = CeramicSpec(
            name="Yttria-Stabilized Zirconia (Y-TZP)",
            composition="ZrO2 + 3% Y2O3",
            tensile_strength_mpa=350,
            compressive_strength_mpa=2000,
            flexural_strength_mpa=1200,
            hardness_hv=1300,
            fracture_toughness_mpa_m05=8.0,  # Best for ceramics
            temperature_max_c=1200,
            thermal_conductivity_w_mk=2.5,
            cte_um_mk=10.5,
            thermal_shock_resistance="good",
            density_g_cm3=6.05,
            electrical_resistivity_ohm_cm=1e10,
            typical_applications=["dental", "cutting_tools", "wear_parts", "oxygen_sensors"],
            relative_cost=25.0
        )

        self._ceramics["Silicon Nitride"] = CeramicSpec(
            name="Silicon Nitride (Si3N4)",
            composition="Si3N4",
            tensile_strength_mpa=400,
            compressive_strength_mpa=3500,
            flexural_strength_mpa=700,
            hardness_hv=1600,
            fracture_toughness_mpa_m05=6.5,
            temperature_max_c=1200,
            thermal_conductivity_w_mk=30,
            cte_um_mk=3.2,
            thermal_shock_resistance="excellent",
            density_g_cm3=3.20,
            electrical_resistivity_ohm_cm=1e13,
            typical_applications=["bearings", "turbocharger_wheels", "cutting_tools"],
            relative_cost=40.0
        )

    def get_composite(self, name: str) -> Optional[CompositeSpec]:
        """Get composite by name"""
        return self._composites.get(name)

    def get_ceramic(self, name: str) -> Optional[CeramicSpec]:
        """Get ceramic by name"""
        return self._ceramics.get(name)

    def search_composites(
        self,
        fiber_type: Optional[FiberType] = None,
        min_strength_mpa: Optional[float] = None,
        min_modulus_gpa: Optional[float] = None,
        electrically_conductive: Optional[bool] = None
    ) -> List[CompositeSpec]:
        """Search composites by criteria"""
        results = []
        for comp in self._composites.values():
            if fiber_type and comp.fiber_type != fiber_type:
                continue
            if min_strength_mpa and comp.tensile_strength_mpa < min_strength_mpa:
                continue
            if min_modulus_gpa and comp.tensile_modulus_gpa < min_modulus_gpa:
                continue
            if electrically_conductive is not None:
                is_conductive = comp.electrical_conductivity == "conductive"
                if electrically_conductive != is_conductive:
                    continue
            results.append(comp)
        return results

    def search_ceramics(
        self,
        min_temperature_c: Optional[float] = None,
        min_hardness_hv: Optional[float] = None
    ) -> List[CeramicSpec]:
        """Search ceramics by criteria"""
        results = []
        for ceramic in self._ceramics.values():
            if min_temperature_c and ceramic.temperature_max_c < min_temperature_c:
                continue
            if min_hardness_hv and ceramic.hardness_hv < min_hardness_hv:
                continue
            results.append(ceramic)
        return results

    def list_composites(self) -> List[str]:
        """List all composite names"""
        return list(self._composites.keys())

    def list_ceramics(self) -> List[str]:
        """List all ceramic names"""
        return list(self._ceramics.keys())


# Demo
if __name__ == "__main__":
    db = CompositeDatabase()

    print("=== Composites Database Demo ===\n")

    print("--- Carbon Fiber Composites ---")
    cf_composites = db.search_composites(fiber_type=FiberType.CARBON)
    for comp in cf_composites:
        print(f"  {comp.name}")
        print(f"    Strength: {comp.tensile_strength_mpa} MPa, Modulus: {comp.tensile_modulus_gpa} GPa")
        print(f"    Density: {comp.density_g_cm3} g/cm3, Cost: {comp.relative_cost}x")

    print("\n--- Technical Ceramics ---")
    ceramics = db.search_ceramics(min_temperature_c=1200)
    for cer in ceramics:
        print(f"  {cer.name}")
        print(f"    Max temp: {cer.temperature_max_c}°C, Hardness: {cer.hardness_hv} HV")
