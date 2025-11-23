"""
Composite Materials Database
============================

Aviation composite materials and repair intelligence.

CRITICAL: Composite repair in aviation is NOT like automotive.
Improper repairs can be invisible and catastrophic.

This module provides:
- Composite material specifications
- Repair classification guidance
- Inspection method requirements
- SRM (Structural Repair Manual) references

Material Systems:
- CFRP (Carbon Fiber Reinforced Polymer)
- GFRP (Glass Fiber Reinforced Polymer)
- AFRP (Aramid/Kevlar Fiber Reinforced Polymer)
- Honeycomb core structures
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
import logging

logger = logging.getLogger(__name__)


class CompositeMaterialType(Enum):
    """Composite material type classification."""
    CFRP = auto()              # Carbon Fiber Reinforced Polymer
    GFRP = auto()              # Glass Fiber Reinforced Polymer
    AFRP = auto()              # Aramid (Kevlar) Fiber Reinforced Polymer
    HONEYCOMB_ALUMINUM = auto() # Aluminum honeycomb core
    HONEYCOMB_NOMEX = auto()   # Nomex honeycomb core
    FOAM_CORE = auto()         # Foam core structures
    HYBRID = auto()            # Mixed fiber types


class RepairClassification(Enum):
    """Aircraft composite repair classification."""
    NEGLIGIBLE = auto()        # Cosmetic only, no structural impact
    MINOR = auto()             # Minor structural, within SRM limits
    MAJOR = auto()             # Beyond SRM, engineering required
    BEYOND_REPAIR = auto()     # Component replacement required


class InspectionMethod(Enum):
    """Non-destructive inspection methods for composites."""
    VISUAL = auto()            # Visual inspection
    TAP_TEST = auto()          # Coin tap / tap hammer
    ULTRASONIC = auto()        # Ultrasonic inspection
    THERMOGRAPHY = auto()      # Infrared thermography
    RADIOGRAPHY = auto()       # X-ray inspection
    EDDY_CURRENT = auto()      # Eddy current (for CFRP with metal)
    SHEAROGRAPHY = auto()      # Laser shearography
    BOND_TESTER = auto()       # Mechanical impedance


class CureMethod(Enum):
    """Composite repair cure methods."""
    ROOM_TEMP = auto()         # Room temperature cure
    HEAT_BLANKET = auto()      # Heat blanket cure
    OVEN_CURE = auto()         # Oven cure
    AUTOCLAVE = auto()         # Autoclave cure
    VACUUM_BAG_RT = auto()     # Vacuum bag, room temp
    VACUUM_BAG_ELEVATED = auto()  # Vacuum bag, elevated temp


@dataclass
class CompositeMaterial:
    """Composite material specification."""
    designation: str
    material_type: CompositeMaterialType
    fiber_type: str
    matrix_type: str  # Epoxy, polyester, vinyl ester, etc.
    typical_applications: List[str]
    repair_methods: List[str]
    inspection_methods: List[InspectionMethod]
    cure_temperature_c: Optional[int] = None
    cure_time_hours: Optional[float] = None
    shelf_life_months: Optional[int] = None
    storage_temperature_c: Optional[int] = None
    special_considerations: List[str] = field(default_factory=list)


@dataclass
class RepairProcedure:
    """Composite repair procedure specification."""
    repair_type: str
    classification: RepairClassification
    applicable_materials: List[CompositeMaterialType]
    description: str
    steps: List[str]
    required_equipment: List[str]
    cure_method: CureMethod
    cure_parameters: Dict[str, Any]
    inspection_required: List[InspectionMethod]
    documentation_required: List[str]
    approval_required: str  # A&P, IA, DER, etc.
    notes: str = ""


@dataclass
class DamageAssessment:
    """Composite damage assessment result."""
    damage_type: str
    damage_size_inches: Dict[str, float]  # length, width, depth
    affected_plies: Optional[int]
    classification: RepairClassification
    repair_options: List[str]
    inspection_methods: List[InspectionMethod]
    srm_reference: Optional[str]
    engineering_required: bool
    documentation_required: List[str]


class CompositeDatabase:
    """
    Aviation Composite Materials Database.

    Provides composite material intelligence for:
    - Material identification and properties
    - Damage assessment guidance
    - Repair classification
    - Inspection method selection
    - SRM procedure references

    CRITICAL: Improper composite repairs can be invisible and catastrophic.
    All repairs must follow approved procedures and documentation requirements.
    """

    def __init__(self):
        self._materials: Dict[str, CompositeMaterial] = {}
        self._repair_procedures: Dict[str, RepairProcedure] = {}
        self._damage_limits: Dict[str, Dict] = {}

        self._initialize_database()
        logger.info("Composite Materials Database initialized")

    def _initialize_database(self):
        """Initialize composite materials database."""
        self._materials = {
            "CFRP_Epoxy": CompositeMaterial(
                designation="CFRP_Epoxy",
                material_type=CompositeMaterialType.CFRP,
                fiber_type="Carbon fiber (T300, T700, etc.)",
                matrix_type="Epoxy (350F cure typical)",
                typical_applications=[
                    "Control surfaces (ailerons, elevators, rudder)",
                    "Fairings and cowlings",
                    "Nacelles",
                    "Wing skins (composite aircraft)",
                    "Fuselage panels (composite aircraft)"
                ],
                repair_methods=[
                    "Scarf repair",
                    "Stepped repair",
                    "Bonded doubler",
                    "Bolted repair"
                ],
                inspection_methods=[
                    InspectionMethod.VISUAL,
                    InspectionMethod.TAP_TEST,
                    InspectionMethod.ULTRASONIC,
                    InspectionMethod.THERMOGRAPHY
                ],
                cure_temperature_c=177,  # 350F
                cure_time_hours=2.0,
                shelf_life_months=12,
                storage_temperature_c=-18,
                special_considerations=[
                    "Moisture sensitive - protect from humidity",
                    "UV degradation - requires paint/coating",
                    "Galvanic corrosion with aluminum - isolate",
                    "Lightning strike protection may be required"
                ]
            ),
            "GFRP_Epoxy": CompositeMaterial(
                designation="GFRP_Epoxy",
                material_type=CompositeMaterialType.GFRP,
                fiber_type="E-glass or S-glass",
                matrix_type="Epoxy",
                typical_applications=[
                    "Fairings",
                    "Cowlings",
                    "Non-structural panels",
                    "Radomes",
                    "Wingtips"
                ],
                repair_methods=[
                    "Wet layup",
                    "Prepreg repair",
                    "Vacuum bag cure",
                    "Room temperature cure"
                ],
                inspection_methods=[
                    InspectionMethod.VISUAL,
                    InspectionMethod.TAP_TEST
                ],
                cure_temperature_c=None,  # Can be RT
                shelf_life_months=6,
                special_considerations=[
                    "More forgiving than CFRP",
                    "Lower strength than CFRP",
                    "Good for non-structural repairs"
                ]
            ),
            "GFRP_Polyester": CompositeMaterial(
                designation="GFRP_Polyester",
                material_type=CompositeMaterialType.GFRP,
                fiber_type="E-glass",
                matrix_type="Polyester resin",
                typical_applications=[
                    "Fairings",
                    "Non-structural cowlings",
                    "Interior components"
                ],
                repair_methods=[
                    "Wet layup",
                    "Room temperature cure"
                ],
                inspection_methods=[
                    InspectionMethod.VISUAL,
                    InspectionMethod.TAP_TEST
                ],
                special_considerations=[
                    "Lower cost material",
                    "Strong odor during cure",
                    "Not compatible with epoxy matrix"
                ]
            ),
            "AFRP_Kevlar": CompositeMaterial(
                designation="AFRP_Kevlar",
                material_type=CompositeMaterialType.AFRP,
                fiber_type="Kevlar 49",
                matrix_type="Epoxy",
                typical_applications=[
                    "Impact resistant areas",
                    "Radomes (RF transparent)",
                    "Helicopter blades (erosion protection)",
                    "Ballistic protection"
                ],
                repair_methods=[
                    "Specialized cutting required",
                    "Hybrid repair with glass",
                    "Adhesive bonding"
                ],
                inspection_methods=[
                    InspectionMethod.VISUAL,
                    InspectionMethod.TAP_TEST,
                    InspectionMethod.ULTRASONIC
                ],
                special_considerations=[
                    "DIFFICULT TO CUT - requires special tools",
                    "Absorbs moisture - dry before repair",
                    "Fuzzy fibers when cut - hard to sand",
                    "Excellent impact resistance"
                ]
            ),
            "Honeycomb_Nomex": CompositeMaterial(
                designation="Honeycomb_Nomex",
                material_type=CompositeMaterialType.HONEYCOMB_NOMEX,
                fiber_type="Nomex aramid paper",
                matrix_type="Phenolic resin coating",
                typical_applications=[
                    "Floor panels",
                    "Control surfaces (internal)",
                    "Nacelle structures",
                    "Spoilers and flaps"
                ],
                repair_methods=[
                    "Core replacement",
                    "Potted repair",
                    "Skin repair over core"
                ],
                inspection_methods=[
                    InspectionMethod.TAP_TEST,
                    InspectionMethod.ULTRASONIC,
                    InspectionMethod.RADIOGRAPHY
                ],
                special_considerations=[
                    "Absorbs water if skin damaged",
                    "Core crush - avoid point loads",
                    "Disbond detection critical"
                ]
            )
        }

        # Repair procedures
        self._repair_procedures = {
            "scarf_repair_cfrp": RepairProcedure(
                repair_type="Scarf Repair",
                classification=RepairClassification.MINOR,
                applicable_materials=[CompositeMaterialType.CFRP],
                description="Tapered scarf joint repair for flush surface finish",
                steps=[
                    "1. Define damage extent (NDI required)",
                    "2. Mark and mask repair area",
                    "3. Remove damaged material at specified taper ratio (typ. 20:1 to 50:1)",
                    "4. Clean and prepare surface",
                    "5. Apply release film and peel ply to adjacent areas",
                    "6. Cut repair plies to size (matching orientation)",
                    "7. Apply plies with specified overlap",
                    "8. Apply vacuum bag and cure per SRM",
                    "9. Remove bag, inspect, and NDI",
                    "10. Finish surface as required"
                ],
                required_equipment=[
                    "Scarfing tool or sander",
                    "Vacuum pump and bag materials",
                    "Heat blanket with controller",
                    "Thermocouples",
                    "Approved repair materials (prepreg or wet layup)",
                    "NDI equipment"
                ],
                cure_method=CureMethod.HEAT_BLANKET,
                cure_parameters={
                    "temperature_f": 250,
                    "ramp_rate_f_min": 3,
                    "hold_time_min": 120,
                    "vacuum_inhg": 22
                },
                inspection_required=[
                    InspectionMethod.VISUAL,
                    InspectionMethod.TAP_TEST,
                    InspectionMethod.ULTRASONIC
                ],
                documentation_required=[
                    "SRM procedure reference",
                    "Material batch/lot numbers",
                    "Cure cycle data",
                    "NDI results",
                    "Logbook entry"
                ],
                approval_required="A&P with IA signoff",
                notes="Scarf ratio per SRM - typically 20:1 minimum for structural repairs"
            ),
            "potted_core_repair": RepairProcedure(
                repair_type="Potted Core Repair",
                classification=RepairClassification.MINOR,
                applicable_materials=[
                    CompositeMaterialType.HONEYCOMB_NOMEX,
                    CompositeMaterialType.HONEYCOMB_ALUMINUM
                ],
                description="Fill damaged core cells with potting compound",
                steps=[
                    "1. Remove damaged skin material",
                    "2. Remove water/contamination from core",
                    "3. Dry core if required (per SRM)",
                    "4. Fill damaged cells with approved potting compound",
                    "5. Cure potting compound",
                    "6. Apply skin repair over potted area",
                    "7. Cure and inspect"
                ],
                required_equipment=[
                    "Core drying equipment",
                    "Potting compound and applicator",
                    "Skin repair materials",
                    "Cure equipment"
                ],
                cure_method=CureMethod.ROOM_TEMP,
                cure_parameters={
                    "temperature_f": 77,
                    "cure_time_hours": 24
                },
                inspection_required=[
                    InspectionMethod.VISUAL,
                    InspectionMethod.TAP_TEST
                ],
                documentation_required=[
                    "SRM procedure reference",
                    "Material batch numbers",
                    "Logbook entry"
                ],
                approval_required="A&P mechanic",
                notes="Ensure core is completely dry before potting"
            )
        }

        # Damage limits (typical - actual limits from SRM)
        self._damage_limits = {
            "control_surface_cfrp": {
                "negligible_max_diameter_inch": 0.25,
                "minor_max_diameter_inch": 2.0,
                "major_threshold": "Engineering evaluation required",
                "edge_distance_min_inch": 1.0,
                "from_fittings_min_inch": 2.0
            },
            "fairing_gfrp": {
                "negligible_max_diameter_inch": 1.0,
                "minor_max_diameter_inch": 6.0,
                "notes": "Non-structural - larger repairs acceptable"
            }
        }

    def get_material_info(self, material: str) -> Optional[CompositeMaterial]:
        """
        Get information about a composite material.

        Args:
            material: Material designation

        Returns:
            CompositeMaterial if found
        """
        return self._materials.get(material)

    def assess_damage(
        self,
        material_type: CompositeMaterialType,
        damage_diameter_inch: float,
        location: str,
        damage_depth: str = "unknown"
    ) -> DamageAssessment:
        """
        Assess composite damage and recommend repair classification.

        Args:
            material_type: Type of composite material
            damage_diameter_inch: Maximum damage diameter in inches
            location: Location on structure (control surface, fairing, etc.)
            damage_depth: Depth assessment (surface, partial, through)

        Returns:
            DamageAssessment with classification and recommendations
        """
        # Simplified assessment - actual assessment requires SRM
        if damage_diameter_inch <= 0.25:
            classification = RepairClassification.NEGLIGIBLE
            engineering_required = False
        elif damage_diameter_inch <= 2.0:
            classification = RepairClassification.MINOR
            engineering_required = False
        else:
            classification = RepairClassification.MAJOR
            engineering_required = True

        # Determine inspection methods
        inspection_methods = [InspectionMethod.VISUAL, InspectionMethod.TAP_TEST]
        if material_type == CompositeMaterialType.CFRP or damage_diameter_inch > 1.0:
            inspection_methods.append(InspectionMethod.ULTRASONIC)

        return DamageAssessment(
            damage_type="Impact damage (assessed)",
            damage_size_inches={"diameter": damage_diameter_inch},
            affected_plies=None,
            classification=classification,
            repair_options=self._get_repair_options(material_type, classification),
            inspection_methods=inspection_methods,
            srm_reference="Refer to aircraft-specific SRM",
            engineering_required=engineering_required,
            documentation_required=[
                "Damage assessment report",
                "Photos of damage",
                "NDI results",
                "Repair procedure (if repaired)",
                "Logbook entry"
            ]
        )

    def _get_repair_options(
        self,
        material_type: CompositeMaterialType,
        classification: RepairClassification
    ) -> List[str]:
        """Get applicable repair options."""
        if classification == RepairClassification.NEGLIGIBLE:
            return ["Cosmetic fill and paint", "Surface sealer"]
        elif classification == RepairClassification.MINOR:
            if material_type == CompositeMaterialType.CFRP:
                return ["Scarf repair", "Stepped repair", "Bonded doubler"]
            else:
                return ["Wet layup repair", "Prepreg patch"]
        elif classification == RepairClassification.MAJOR:
            return ["Engineering disposition required", "Possible component replacement"]
        else:
            return ["Component replacement"]

    def get_repair_procedure(self, procedure_name: str) -> Optional[RepairProcedure]:
        """
        Get a specific repair procedure.

        Args:
            procedure_name: Name of repair procedure

        Returns:
            RepairProcedure if found
        """
        return self._repair_procedures.get(procedure_name)

    def find_materials_by_type(
        self,
        material_type: CompositeMaterialType
    ) -> List[CompositeMaterial]:
        """
        Find all materials of a specific type.

        Args:
            material_type: Composite material type

        Returns:
            List of matching materials
        """
        return [
            mat for mat in self._materials.values()
            if mat.material_type == material_type
        ]

    def get_inspection_requirements(
        self,
        material_type: CompositeMaterialType,
        repair_classification: RepairClassification
    ) -> List[InspectionMethod]:
        """
        Get required inspection methods for a repair.

        Args:
            material_type: Type of composite material
            repair_classification: Repair classification

        Returns:
            List of required inspection methods
        """
        methods = [InspectionMethod.VISUAL, InspectionMethod.TAP_TEST]

        if repair_classification in [RepairClassification.MINOR, RepairClassification.MAJOR]:
            if material_type == CompositeMaterialType.CFRP:
                methods.append(InspectionMethod.ULTRASONIC)

        if repair_classification == RepairClassification.MAJOR:
            methods.append(InspectionMethod.THERMOGRAPHY)

        return methods
