"""
Industrial Fastener Selection Engine

Industrial fasteners have different requirements than automotive:
- Higher preloads and tighter torque control
- Vibration resistance critical (machinery runs continuously)
- Coolant and cutting fluid exposure
- Precise positioning and repeatability
- Frequent maintenance cycles
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import math


class FastenerApplication(Enum):
    """Industrial fastener application types"""
    SPINDLE_MOUNT = "spindle_mount"
    BALLSCREW_MOUNT = "ballscrew_mount"
    LINEAR_GUIDE = "linear_guide"
    GEARBOX = "gearbox"
    MOTOR_MOUNT = "motor_mount"
    TOOLHOLDER = "toolholder"
    FIXTURE = "fixture"
    STRUCTURAL = "structural"
    COVER_PANEL = "cover_panel"
    GENERAL = "general"


class ThreadType(Enum):
    """Thread types for industrial fasteners"""
    METRIC_COARSE = "metric_coarse"
    METRIC_FINE = "metric_fine"
    UNC = "unc"
    UNF = "unf"
    BSW = "bsw"
    BSF = "bsf"


class CoatingType(Enum):
    """Fastener coating/finish types"""
    BLACK_OXIDE = "black_oxide"
    ZINC_PLATED = "zinc_plated"
    ZINC_FLAKE = "zinc_flake"
    GEOMET = "geomet"
    DACROMET = "dacromet"
    PHOSPHATE = "phosphate"
    NICKEL = "nickel"
    CHROME = "chrome"
    PLAIN = "plain"
    PTFE = "ptfe"


@dataclass
class IndustrialFastener:
    """Industrial fastener specification"""
    size: str                              # "M10x1.25"
    grade: str                             # "10.9", "12.9", "A4-80"
    head_type: str                         # "Socket", "Hex", "Button"
    thread_type: ThreadType
    material: str
    coating: CoatingType
    length_mm: float

    # Mechanical properties
    tensile_strength_mpa: float
    yield_strength_mpa: float
    proof_load_kn: float

    # Application data
    recommended_torque_nm: float
    clamp_force_kn: float
    k_factor: float                        # Torque coefficient

    # Standards
    din_standard: Optional[str]
    iso_standard: Optional[str]
    mil_spec: Optional[str]


@dataclass
class AntiVibrationSolution:
    """Anti-vibration fastening solution"""
    name: str
    manufacturer: str
    mechanism: str                         # "Wedge lock", "Prevailing torque", "Adhesive"
    reusable: bool
    temperature_max_c: int
    preload_retention_percent: float
    cost_factor: float                     # Multiplier vs standard washer
    notes: str


@dataclass
class TorqueSpecification:
    """Detailed torque specification"""
    nominal_torque_nm: float
    tolerance_percent: float
    angle_after_snug_degrees: Optional[float]  # For angle-controlled tightening
    sequence: Optional[List[float]]            # Multi-pass sequence
    lubrication: str
    k_factor: float
    clamp_force_kn: float
    notes: str


class IndustrialFastenerEngine:
    """
    Engine for industrial fastener selection and specification

    Covers:
    - Machine tool fasteners (high preload, vibration resistance)
    - Precision assembly (controlled torque)
    - High-temperature applications
    - Corrosion-resistant requirements
    - Fatigue-critical joints
    """

    def __init__(self):
        self.fastener_database = self._initialize_fasteners()
        self.anti_vibration = self._initialize_anti_vibration()
        self.torque_tables = self._initialize_torque_tables()

    def _initialize_fasteners(self) -> Dict[str, IndustrialFastener]:
        """Initialize industrial fastener database"""
        fasteners = {}

        # Class 10.9 Socket Head Cap Screws (DIN 912)
        for size, data in [
            ("M6", {"pitch": 1.0, "proof_kn": 14.4, "torque": 12, "tensile": 1040}),
            ("M8", {"pitch": 1.25, "proof_kn": 26.4, "torque": 28, "tensile": 1040}),
            ("M10", {"pitch": 1.5, "proof_kn": 41.2, "torque": 55, "tensile": 1040}),
            ("M12", {"pitch": 1.75, "proof_kn": 60.5, "torque": 95, "tensile": 1040}),
            ("M14", {"pitch": 2.0, "proof_kn": 83.0, "torque": 150, "tensile": 1040}),
            ("M16", {"pitch": 2.0, "proof_kn": 113, "torque": 230, "tensile": 1040}),
            ("M20", {"pitch": 2.5, "proof_kn": 176, "torque": 450, "tensile": 1040}),
        ]:
            fasteners[f"{size}-10.9-shcs"] = IndustrialFastener(
                size=f"{size}x{data['pitch']}",
                grade="10.9",
                head_type="Socket Head Cap Screw",
                thread_type=ThreadType.METRIC_COARSE,
                material="Alloy Steel, Quenched & Tempered",
                coating=CoatingType.BLACK_OXIDE,
                length_mm=30,  # Default
                tensile_strength_mpa=data["tensile"],
                yield_strength_mpa=940,
                proof_load_kn=data["proof_kn"],
                recommended_torque_nm=data["torque"],
                clamp_force_kn=data["proof_kn"] * 0.75,
                k_factor=0.12,
                din_standard="DIN 912",
                iso_standard="ISO 4762",
                mil_spec=None
            )

        # Class 12.9 Socket Head Cap Screws
        for size, data in [
            ("M6", {"pitch": 1.0, "proof_kn": 17.0, "torque": 14, "tensile": 1220}),
            ("M8", {"pitch": 1.25, "proof_kn": 31.1, "torque": 33, "tensile": 1220}),
            ("M10", {"pitch": 1.5, "proof_kn": 48.5, "torque": 65, "tensile": 1220}),
            ("M12", {"pitch": 1.75, "proof_kn": 71.3, "torque": 115, "tensile": 1220}),
            ("M14", {"pitch": 2.0, "proof_kn": 97.7, "torque": 180, "tensile": 1220}),
            ("M16", {"pitch": 2.0, "proof_kn": 133, "torque": 280, "tensile": 1220}),
        ]:
            fasteners[f"{size}-12.9-shcs"] = IndustrialFastener(
                size=f"{size}x{data['pitch']}",
                grade="12.9",
                head_type="Socket Head Cap Screw",
                thread_type=ThreadType.METRIC_COARSE,
                material="Alloy Steel, Quenched & Tempered",
                coating=CoatingType.BLACK_OXIDE,
                length_mm=30,
                tensile_strength_mpa=data["tensile"],
                yield_strength_mpa=1100,
                proof_load_kn=data["proof_kn"],
                recommended_torque_nm=data["torque"],
                clamp_force_kn=data["proof_kn"] * 0.75,
                k_factor=0.12,
                din_standard="DIN 912",
                iso_standard="ISO 4762",
                mil_spec="MIL-DTL-1222"
            )

        # Fine thread versions (higher preload for same size)
        for size, data in [
            ("M10x1.25", {"proof_kn": 44.8, "torque": 60}),
            ("M12x1.25", {"proof_kn": 71.5, "torque": 115}),
            ("M14x1.5", {"proof_kn": 92.4, "torque": 175}),
        ]:
            fasteners[f"{size}-12.9-shcs-fine"] = IndustrialFastener(
                size=size,
                grade="12.9",
                head_type="Socket Head Cap Screw",
                thread_type=ThreadType.METRIC_FINE,
                material="Alloy Steel, Quenched & Tempered",
                coating=CoatingType.BLACK_OXIDE,
                length_mm=30,
                tensile_strength_mpa=1220,
                yield_strength_mpa=1100,
                proof_load_kn=data["proof_kn"],
                recommended_torque_nm=data["torque"],
                clamp_force_kn=data["proof_kn"] * 0.75,
                k_factor=0.12,
                din_standard="DIN 912",
                iso_standard="ISO 4762",
                mil_spec="MIL-DTL-1222"
            )

        return fasteners

    def _initialize_anti_vibration(self) -> Dict[str, AntiVibrationSolution]:
        """Initialize anti-vibration solutions"""
        return {
            "nord_lock": AntiVibrationSolution(
                name="Nord-Lock Wedge-Locking Washer",
                manufacturer="Nord-Lock",
                mechanism="Wedge lock - radial teeth create wedge action",
                reusable=True,
                temperature_max_c=200,
                preload_retention_percent=100,
                cost_factor=10,
                notes="Gold standard for vibration. Pairs of washers required. Works by creating higher friction than loosening torque."
            ),
            "belleville": AntiVibrationSolution(
                name="Belleville Spring Washer",
                manufacturer="Various",
                mechanism="Spring force maintains preload through thermal/settling",
                reusable=True,
                temperature_max_c=300,
                preload_retention_percent=85,
                cost_factor=2,
                notes="Good for thermal cycling. Can be stacked for more deflection."
            ),
            "serrated_flange": AntiVibrationSolution(
                name="Serrated Flange Bolt",
                manufacturer="Various",
                mechanism="Serrations bite into surface, increase friction",
                reusable=False,
                temperature_max_c=150,
                preload_retention_percent=70,
                cost_factor=1.2,
                notes="Integrated solution. Damages surface - not for precision applications."
            ),
            "loctite_271": AntiVibrationSolution(
                name="Loctite 271 Thread Locker",
                manufacturer="Henkel",
                mechanism="Anaerobic adhesive fills thread gaps",
                reusable=False,
                temperature_max_c=150,
                preload_retention_percent=95,
                cost_factor=0.5,
                notes="High strength, permanent. Requires heat or hand tools for removal."
            ),
            "loctite_243": AntiVibrationSolution(
                name="Loctite 243 Thread Locker",
                manufacturer="Henkel",
                mechanism="Anaerobic adhesive, medium strength",
                reusable=False,
                temperature_max_c=150,
                preload_retention_percent=85,
                cost_factor=0.5,
                notes="Medium strength, removable with hand tools. Oil tolerant."
            ),
            "helicoil": AntiVibrationSolution(
                name="HeliCoil Plus with Locking Feature",
                manufacturer="Stanley Engineered Fastening",
                mechanism="Wire thread insert with grip coils",
                reusable=True,
                temperature_max_c=250,
                preload_retention_percent=90,
                cost_factor=5,
                notes="For soft materials (aluminum) or thread repair with locking."
            ),
        }

    def _initialize_torque_tables(self) -> Dict[str, Dict]:
        """Initialize torque specification tables"""
        return {
            # K-factors for different conditions
            "k_factors": {
                "dry": 0.20,
                "light_oil": 0.15,
                "moly_paste": 0.10,
                "anti_seize": 0.12,
                "wax": 0.13,
                "cadmium_dry": 0.16,
                "zinc_dry": 0.17,
                "phosphate_oil": 0.13,
                "black_oxide_oil": 0.12,
            },
            # Typical tightening sequences
            "sequences": {
                "circular_4_bolt": [0.3, 0.6, 1.0],           # Star pattern
                "circular_6_bolt": [0.3, 0.6, 1.0],
                "circular_8_bolt": [0.25, 0.5, 0.75, 1.0],
                "linear": [0.5, 1.0],
                "critical_joint": [0.3, 0.5, 0.7, 0.9, 1.0],
            }
        }

    def recommend_fastener(
        self,
        application: FastenerApplication,
        clamp_force_required_kn: float,
        environment: str,
        thread_engagement_mm: Optional[float] = None
    ) -> Dict:
        """
        Recommend industrial fastener for application.

        Args:
            application: Application type
            clamp_force_required_kn: Required clamping force
            environment: Operating environment description
            thread_engagement_mm: Available thread engagement depth

        Returns:
            Fastener recommendation with specifications
        """
        # Determine grade based on application
        if application in [FastenerApplication.SPINDLE_MOUNT, FastenerApplication.BALLSCREW_MOUNT]:
            preferred_grade = "12.9"
            thread_type = "fine"
        elif application in [FastenerApplication.LINEAR_GUIDE, FastenerApplication.MOTOR_MOUNT]:
            preferred_grade = "10.9"
            thread_type = "fine"
        else:
            preferred_grade = "10.9"
            thread_type = "coarse"

        # Find suitable size
        selected_fastener = None
        for key, fastener in self.fastener_database.items():
            if fastener.grade != preferred_grade:
                continue
            if fastener.clamp_force_kn >= clamp_force_required_kn:
                if thread_type == "fine" and "fine" not in key:
                    continue
                if thread_type == "coarse" and "fine" in key:
                    continue
                selected_fastener = fastener
                break

        if not selected_fastener:
            # Fall back to largest available
            selected_fastener = list(self.fastener_database.values())[-1]

        # Determine coating
        coolant_exposure = any(term in environment.lower() for term in ["coolant", "cutting fluid", "oil", "wet"])
        high_temp = any(term in environment.lower() for term in ["high temp", "heat", "hot"])

        if coolant_exposure:
            recommended_coating = CoatingType.GEOMET
            coating_notes = "Geomet 500 provides excellent corrosion resistance and consistent friction"
        elif high_temp:
            recommended_coating = CoatingType.PHOSPHATE
            coating_notes = "Phosphate coating suitable for high temperature"
        else:
            recommended_coating = CoatingType.BLACK_OXIDE
            coating_notes = "Standard black oxide with oil"

        # Determine anti-vibration
        vibration_critical = any(term in environment.lower() for term in ["vibration", "cyclic", "dynamic"])
        if vibration_critical:
            anti_vib = self.anti_vibration["nord_lock"]
            anti_vib_notes = "Nord-Lock washers strongly recommended for vibrating machinery"
        else:
            anti_vib = None
            anti_vib_notes = "Standard washer sufficient for static applications"

        return {
            "fastener": {
                "size": selected_fastener.size,
                "grade": selected_fastener.grade,
                "head_type": selected_fastener.head_type,
                "material": selected_fastener.material,
                "din_standard": selected_fastener.din_standard,
            },
            "coating": {
                "type": recommended_coating.value,
                "notes": coating_notes,
            },
            "torque": {
                "value_nm": selected_fastener.recommended_torque_nm,
                "clamp_force_kn": selected_fastener.clamp_force_kn,
                "k_factor": selected_fastener.k_factor,
            },
            "anti_vibration": {
                "solution": anti_vib.name if anti_vib else "Standard flat washer",
                "notes": anti_vib_notes,
            },
            "thread_locker": "Loctite 243" if vibration_critical else "Optional",
            "application": application.value,
        }

    def calculate_torque(
        self,
        fastener_size: str,
        grade: str,
        target_clamp_force_kn: float,
        lubrication: str = "light_oil"
    ) -> TorqueSpecification:
        """
        Calculate torque specification for target clamp force.

        Uses: T = K * D * F
        Where:
            T = Torque (Nm)
            K = Friction coefficient (k-factor)
            D = Nominal diameter (mm)
            F = Clamp force (kN)
        """
        # Parse size
        if fastener_size.startswith("M"):
            diameter_mm = int(fastener_size[1:].split("x")[0])
        else:
            diameter_mm = 10  # Default

        # Get K-factor
        k_factor = self.torque_tables["k_factors"].get(lubrication, 0.15)

        # Calculate torque
        torque_nm = k_factor * diameter_mm * target_clamp_force_kn

        return TorqueSpecification(
            nominal_torque_nm=round(torque_nm, 1),
            tolerance_percent=10,
            angle_after_snug_degrees=None,
            sequence=self.torque_tables["sequences"]["linear"],
            lubrication=lubrication,
            k_factor=k_factor,
            clamp_force_kn=target_clamp_force_kn,
            notes=f"Calculated for {fastener_size} {grade} with {lubrication} lubrication"
        )

    def get_anti_vibration_solutions(
        self,
        temperature_c: int = 100,
        reusable_required: bool = False
    ) -> List[AntiVibrationSolution]:
        """Get applicable anti-vibration solutions"""
        results = []
        for solution in self.anti_vibration.values():
            if solution.temperature_max_c >= temperature_c:
                if not reusable_required or solution.reusable:
                    results.append(solution)

        return sorted(results, key=lambda x: x.preload_retention_percent, reverse=True)
