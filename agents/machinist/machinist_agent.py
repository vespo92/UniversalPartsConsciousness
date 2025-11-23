"""
Agent_13: MACHINIST - Industrial & Manufacturing Equipment Intelligence

Industrial machinery represents billions of dollars in capital equipment that
must stay running. When a 1985 CNC machine needs a part, finding compatibility
requires deep knowledge of industrial standards, retrofits, and reverse engineering.

Domains:
- CNC machines (mills, lathes, routers, EDM)
- PLCs and industrial automation
- Motors, drives, and motion control
- Hydraulic and pneumatic systems
- Industrial sensors and instrumentation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import asyncio


class EquipmentType(Enum):
    """Industrial equipment classifications"""
    CNC_MILL = "cnc_mill"
    CNC_LATHE = "cnc_lathe"
    CNC_ROUTER = "cnc_router"
    CNC_EDM = "cnc_edm"
    CNC_GRINDER = "cnc_grinder"
    PLC_SYSTEM = "plc_system"
    SERVO_SYSTEM = "servo_system"
    VFD_DRIVE = "vfd_drive"
    HYDRAULIC = "hydraulic"
    PNEUMATIC = "pneumatic"
    INDUSTRIAL_ROBOT = "industrial_robot"


class ComponentCategory(Enum):
    """Industrial component categories"""
    CONTROL_SYSTEM = "control_system"
    SERVO_DRIVE = "servo_drive"
    SERVO_MOTOR = "servo_motor"
    SPINDLE_DRIVE = "spindle_drive"
    SPINDLE_MOTOR = "spindle_motor"
    PLC_CPU = "plc_cpu"
    PLC_IO_MODULE = "plc_io_module"
    HMI_DISPLAY = "hmi_display"
    CRT_MONITOR = "crt_monitor"
    POWER_SUPPLY = "power_supply"
    ENCODER = "encoder"
    VFD = "vfd"
    CONTACTOR = "contactor"
    SENSOR = "sensor"


class RetrofitType(Enum):
    """Types of retrofit solutions"""
    DROP_IN = "drop_in"              # Direct replacement
    ADAPTER_REQUIRED = "adapter"     # Needs mechanical/electrical adapter
    PARTIAL_RETROFIT = "partial"     # Replaces some components
    COMPLETE_RETROFIT = "complete"   # Full system replacement
    CUSTOM_SOLUTION = "custom"       # Requires engineering


@dataclass
class RetrofitSolution:
    """A retrofit solution for obsolete industrial equipment"""
    solution_name: str
    vendor: str
    part_number: str
    retrofit_type: RetrofitType
    price_usd: float
    installation_hours: float
    compatibility_score: float      # 0.0 to 1.0
    requires_modifications: List[str]
    preserves_functionality: List[str]
    adds_functionality: List[str]
    notes: str
    documentation_url: Optional[str] = None


@dataclass
class ServoDriveMatch:
    """Cross-reference match for servo drives"""
    original_drive: str
    replacement_drive: str
    manufacturer: str
    compatibility_score: float
    power_match: bool
    voltage_match: bool
    encoder_compatibility: str      # "Direct", "Adapter", "Incompatible"
    wiring_changes: List[str]
    parameter_mapping_available: bool
    price_vs_original: float        # Ratio (0.4 = 60% savings)
    notes: str


@dataclass
class PLCMigrationPlan:
    """Migration plan from one PLC platform to another"""
    source_plc: str
    recommended_target: str
    target_manufacturer: str
    io_compatibility_score: float   # 0.0 to 1.0
    code_conversion_tool: Optional[str]
    estimated_downtime_hours: float
    estimated_cost_usd: float
    io_mapping: Dict[str, str]      # Source I/O -> Target I/O
    software_changes: List[str]
    hardware_changes: List[str]
    alternatives: List[Dict[str, Any]]
    risks: List[str]
    notes: str


@dataclass
class IndustrialMotorSpec:
    """Industrial motor specification"""
    manufacturer: str
    model: str
    motor_type: str                 # "AC Induction", "AC Servo", "DC Servo", "Stepper"
    power_kw: float
    voltage: int
    current_amps: float
    rpm_rated: int
    rpm_max: int
    torque_nm: float
    encoder_type: Optional[str]
    encoder_resolution: Optional[int]
    frame_size: str
    mounting: str                   # "Flange", "Foot", "Face"
    ip_rating: str
    cooling: str                    # "Fan", "Natural", "Liquid"


@dataclass
class IndustrialFastenerRecommendation:
    """Industrial fastener recommendation for specific applications"""
    specification: str              # "M12x1.25-12.9 Socket Head"
    material: str
    coating: str
    torque_nm: float
    preload_kn: float
    thread_locker: Optional[str]
    anti_vibration: Optional[str]   # "Nord-Lock", "Belleville", etc.
    application_notes: str
    alternative: Optional[str]
    mil_spec: Optional[str]
    din_spec: Optional[str]


@dataclass
class CNCControllerSpec:
    """CNC controller specification"""
    manufacturer: str
    model: str
    generation: str
    year_introduced: int
    year_discontinued: Optional[int]
    axes_supported: int
    spindle_channels: int
    interface_type: str             # "Parallel", "Serial", "Ethernet"
    programming_language: str       # "G-code variant"
    max_block_rate: int             # Blocks per second
    memory_kb: int
    display_type: str
    compatible_drives: List[str]
    retrofit_options: List[str]


class MachinistAgent:
    """
    Agent_13: MACHINIST - Industrial & Manufacturing Equipment Intelligence

    Core responsibilities:
    1. CNC retrofit solutions (displays, controls, drives)
    2. Servo drive cross-reference across manufacturers
    3. PLC migration planning
    4. Industrial motor cross-reference
    5. Industrial fastener selection for machine applications

    Message Bus Topics:
    - upc.industrial.retrofit.query: Incoming retrofit requests
    - upc.industrial.retrofit.found: Retrofit solutions found
    - upc.industrial.plc.migration: PLC migration requests
    - upc.industrial.servo.crossref: Servo cross-reference requests
    - upc.industrial.fastener.query: Industrial fastener queries
    """

    AGENT_ID = "AGENT_13"
    AGENT_NAME = "Industrial Equipment Intelligence"
    AGENT_ALIAS = "MACHINIST"

    def __init__(self):
        self.cnc_controllers = self._initialize_cnc_controllers()
        self.servo_drives = self._initialize_servo_drives()
        self.plc_platforms = self._initialize_plc_platforms()
        self.retrofit_catalog = self._initialize_retrofit_catalog()
        self.motor_database = self._initialize_motors()

    def _initialize_cnc_controllers(self) -> Dict[str, CNCControllerSpec]:
        """Initialize CNC controller database"""
        return {
            "fanuc_6m": CNCControllerSpec(
                manufacturer="Fanuc",
                model="System 6M",
                generation="6",
                year_introduced=1979,
                year_discontinued=1985,
                axes_supported=3,
                spindle_channels=1,
                interface_type="Parallel",
                programming_language="Fanuc G-code",
                max_block_rate=100,
                memory_kb=32,
                display_type="CRT 9-inch monochrome",
                compatible_drives=["Fanuc DC servo"],
                retrofit_options=["LCD monitor retrofit", "Centroid control retrofit", "Mach3/4 retrofit"]
            ),
            "fanuc_0m": CNCControllerSpec(
                manufacturer="Fanuc",
                model="System 0M",
                generation="0",
                year_introduced=1985,
                year_discontinued=1995,
                axes_supported=4,
                spindle_channels=1,
                interface_type="Serial",
                programming_language="Fanuc G-code",
                max_block_rate=200,
                memory_kb=128,
                display_type="CRT 9-inch color",
                compatible_drives=["Fanuc AC servo Series 0"],
                retrofit_options=["LCD monitor retrofit", "Fanuc 0i upgrade", "Third-party CNC"]
            ),
            "fanuc_10m": CNCControllerSpec(
                manufacturer="Fanuc",
                model="System 10M",
                generation="10",
                year_introduced=1985,
                year_discontinued=1992,
                axes_supported=4,
                spindle_channels=1,
                interface_type="Serial",
                programming_language="Fanuc G-code",
                max_block_rate=250,
                memory_kb=256,
                display_type="CRT 12-inch color",
                compatible_drives=["Fanuc AC servo Series 10"],
                retrofit_options=["LCD retrofit", "Fanuc 16i/18i upgrade"]
            ),
            "fanuc_16m": CNCControllerSpec(
                manufacturer="Fanuc",
                model="System 16M",
                generation="16",
                year_introduced=1990,
                year_discontinued=2000,
                axes_supported=6,
                spindle_channels=2,
                interface_type="Serial/Ethernet",
                programming_language="Fanuc G-code",
                max_block_rate=500,
                memory_kb=1024,
                display_type="CRT/LCD",
                compatible_drives=["Fanuc AC servo Series 16", "Alpha series"],
                retrofit_options=["LCD upgrade", "Fanuc 30i upgrade"]
            ),
            "siemens_810d": CNCControllerSpec(
                manufacturer="Siemens",
                model="Sinumerik 810D",
                generation="810D",
                year_introduced=1996,
                year_discontinued=2010,
                axes_supported=5,
                spindle_channels=2,
                interface_type="Profibus",
                programming_language="Siemens G-code/ShopMill",
                max_block_rate=1000,
                memory_kb=4096,
                display_type="LCD",
                compatible_drives=["Simodrive 611"],
                retrofit_options=["840D sl upgrade", "Drive modernization"]
            ),
            "haas_classic": CNCControllerSpec(
                manufacturer="Haas",
                model="Classic Control",
                generation="Classic",
                year_introduced=1988,
                year_discontinued=2006,
                axes_supported=4,
                spindle_channels=1,
                interface_type="Serial",
                programming_language="Haas G-code",
                max_block_rate=300,
                memory_kb=750,
                display_type="CRT",
                compatible_drives=["Haas proprietary"],
                retrofit_options=["Haas NGC upgrade"]
            ),
        }

    def _initialize_servo_drives(self) -> Dict[str, Dict]:
        """Initialize servo drive cross-reference database"""
        return {
            # Fanuc drives
            "fanuc_a06b-6079-h106": {
                "manufacturer": "Fanuc",
                "model": "A06B-6079-H106",
                "series": "Alpha",
                "power_kw": 3.7,
                "voltage": 200,
                "current_a": 18,
                "interface": "Serial (FSSB)",
                "encoder_type": "Serial (Fanuc)",
                "equivalents": [
                    {"model": "Yaskawa SGDV-2R8A11A", "compatibility": 0.85, "adapter_needed": True},
                    {"model": "Mitsubishi MR-J4-40A", "compatibility": 0.80, "adapter_needed": True},
                ]
            },
            "fanuc_a06b-6096-h206": {
                "manufacturer": "Fanuc",
                "model": "A06B-6096-H206",
                "series": "Beta i",
                "power_kw": 5.5,
                "voltage": 200,
                "current_a": 26,
                "interface": "Serial (FSSB)",
                "encoder_type": "Serial (Fanuc)",
                "equivalents": [
                    {"model": "Yaskawa SGDV-5R5A11A", "compatibility": 0.82, "adapter_needed": True},
                ]
            },
            # Yaskawa drives
            "yaskawa_sgdv-2r8a11a": {
                "manufacturer": "Yaskawa",
                "model": "SGDV-2R8A11A",
                "series": "Sigma-5",
                "power_kw": 3.0,
                "voltage": 200,
                "current_a": 14,
                "interface": "MECHATROLINK-II",
                "encoder_type": "Serial (Yaskawa)",
                "equivalents": [
                    {"model": "Mitsubishi MR-J4-40A", "compatibility": 0.90, "adapter_needed": False},
                    {"model": "Delta ASDA-A2", "compatibility": 0.75, "adapter_needed": True},
                ]
            },
            # Mitsubishi drives
            "mitsubishi_mr-j4-40a": {
                "manufacturer": "Mitsubishi",
                "model": "MR-J4-40A",
                "series": "MR-J4",
                "power_kw": 4.0,
                "voltage": 200,
                "current_a": 19,
                "interface": "SSCNET III/H",
                "encoder_type": "Serial (Mitsubishi)",
                "equivalents": [
                    {"model": "Yaskawa SGDV-3R8A11A", "compatibility": 0.88, "adapter_needed": False},
                    {"model": "Panasonic MINAS A6", "compatibility": 0.85, "adapter_needed": True},
                ]
            },
            # Siemens drives
            "siemens_6sn1123-1aa00-0ca2": {
                "manufacturer": "Siemens",
                "model": "6SN1123-1AA00-0CA2",
                "series": "Simodrive 611",
                "power_kw": 5.0,
                "voltage": 400,
                "current_a": 12,
                "interface": "Profibus/Drive-CLiQ",
                "encoder_type": "EnDat/Resolver",
                "equivalents": [
                    {"model": "Siemens S120", "compatibility": 0.95, "adapter_needed": False},
                    {"model": "Bosch Rexroth IndraDrive", "compatibility": 0.70, "adapter_needed": True},
                ]
            },
        }

    def _initialize_plc_platforms(self) -> Dict[str, Dict]:
        """Initialize PLC platform database for migration planning"""
        return {
            "allen_bradley_slc500": {
                "manufacturer": "Allen-Bradley",
                "model": "SLC 500",
                "series": "SLC",
                "year_introduced": 1991,
                "status": "Discontinued",
                "programming": "RSLogix 500",
                "io_types": ["Discrete", "Analog", "High-speed counter"],
                "communication": ["DH+", "DH-485", "Ethernet (module)"],
                "migration_targets": [
                    {"target": "CompactLogix", "compatibility": 0.92, "tool": "Studio 5000 Logix Designer"},
                    {"target": "Micro800", "compatibility": 0.75, "tool": "Connected Components Workbench"},
                ]
            },
            "allen_bradley_plc5": {
                "manufacturer": "Allen-Bradley",
                "model": "PLC-5",
                "series": "PLC-5",
                "year_introduced": 1985,
                "status": "Discontinued",
                "programming": "RSLogix 5",
                "io_types": ["Discrete", "Analog", "Motion"],
                "communication": ["DH+", "Ethernet", "ControlNet"],
                "migration_targets": [
                    {"target": "ControlLogix", "compatibility": 0.88, "tool": "Studio 5000"},
                    {"target": "CompactLogix", "compatibility": 0.82, "tool": "Studio 5000"},
                ]
            },
            "siemens_s5": {
                "manufacturer": "Siemens",
                "model": "S5-115U",
                "series": "SIMATIC S5",
                "year_introduced": 1979,
                "status": "Obsolete",
                "programming": "STEP 5",
                "io_types": ["Discrete", "Analog"],
                "communication": ["MPI", "Profibus"],
                "migration_targets": [
                    {"target": "S7-1500", "compatibility": 0.85, "tool": "TIA Portal Migration"},
                    {"target": "S7-1200", "compatibility": 0.78, "tool": "TIA Portal"},
                ]
            },
            "siemens_s7_300": {
                "manufacturer": "Siemens",
                "model": "S7-300",
                "series": "SIMATIC S7",
                "year_introduced": 1994,
                "status": "Active (phasing out)",
                "programming": "STEP 7 / TIA Portal",
                "io_types": ["Discrete", "Analog", "Motion", "Safety"],
                "communication": ["MPI", "Profibus", "Profinet"],
                "migration_targets": [
                    {"target": "S7-1500", "compatibility": 0.95, "tool": "TIA Portal Migration"},
                ]
            },
            "mitsubishi_fx2n": {
                "manufacturer": "Mitsubishi",
                "model": "FX2N",
                "series": "FX",
                "year_introduced": 1997,
                "status": "Discontinued",
                "programming": "GX Developer",
                "io_types": ["Discrete", "Analog", "Positioning"],
                "communication": ["RS-485", "CC-Link (module)"],
                "migration_targets": [
                    {"target": "FX5U", "compatibility": 0.90, "tool": "GX Works3"},
                    {"target": "iQ-R", "compatibility": 0.85, "tool": "GX Works3"},
                ]
            },
            "omron_c200h": {
                "manufacturer": "Omron",
                "model": "C200H",
                "series": "C200",
                "year_introduced": 1988,
                "status": "Obsolete",
                "programming": "CX-Programmer",
                "io_types": ["Discrete", "Analog"],
                "communication": ["Host Link", "Controller Link"],
                "migration_targets": [
                    {"target": "NX1P2", "compatibility": 0.82, "tool": "Sysmac Studio"},
                    {"target": "CJ2M", "compatibility": 0.88, "tool": "CX-Programmer"},
                ]
            },
        }

    def _initialize_retrofit_catalog(self) -> Dict[str, List[RetrofitSolution]]:
        """Initialize CNC retrofit solution catalog"""
        return {
            "fanuc_crt_monitor": [
                RetrofitSolution(
                    solution_name="LCD Direct Replacement",
                    vendor="CNCMonitors.com",
                    part_number="FAN-LCD-12",
                    retrofit_type=RetrofitType.DROP_IN,
                    price_usd=850,
                    installation_hours=2,
                    compatibility_score=0.95,
                    requires_modifications=["May need brightness adjustment"],
                    preserves_functionality=["All original features"],
                    adds_functionality=["Sharper display", "Lower power consumption"],
                    notes="Direct CRT replacement, plug-and-play for most Fanuc 0/6/10/15/16 series"
                ),
                RetrofitSolution(
                    solution_name="Industrial LCD Kit",
                    vendor="Mazak Parts USA",
                    part_number="LCD-FANUC-UNIV",
                    retrofit_type=RetrofitType.ADAPTER_REQUIRED,
                    price_usd=1200,
                    installation_hours=4,
                    compatibility_score=0.98,
                    requires_modifications=["Mounting adapter", "Video converter box"],
                    preserves_functionality=["All original features"],
                    adds_functionality=["VGA output", "Brightness control"],
                    notes="Universal kit for various Fanuc generations"
                ),
            ],
            "fanuc_complete_control": [
                RetrofitSolution(
                    solution_name="Centroid M400",
                    vendor="Centroid CNC",
                    part_number="M400-RETROFIT",
                    retrofit_type=RetrofitType.COMPLETE_RETROFIT,
                    price_usd=8500,
                    installation_hours=40,
                    compatibility_score=1.0,
                    requires_modifications=[
                        "Remove original control",
                        "Install new servo drives",
                        "Rewire I/O"
                    ],
                    preserves_functionality=["Basic machine motion"],
                    adds_functionality=[
                        "USB file transfer",
                        "15.6 inch touchscreen",
                        "Ethernet connectivity",
                        "Modern conversational programming",
                        "DXF import"
                    ],
                    notes="Complete modern control replacement. Excellent for machines with worn original controls.",
                    documentation_url="https://www.centroidcnc.com/centroid_diy/m400_retrofit.html"
                ),
                RetrofitSolution(
                    solution_name="MACH4 Industrial",
                    vendor="Newfangled Solutions",
                    part_number="MACH4-IND",
                    retrofit_type=RetrofitType.COMPLETE_RETROFIT,
                    price_usd=5000,
                    installation_hours=60,
                    compatibility_score=0.90,
                    requires_modifications=[
                        "PC hardware required",
                        "Motion control board",
                        "New servo drives (optional)"
                    ],
                    preserves_functionality=["Basic motion"],
                    adds_functionality=[
                        "PC-based control",
                        "Plugin ecosystem",
                        "Custom screens"
                    ],
                    notes="Flexible PC-based solution. Requires more technical expertise.",
                    documentation_url="https://www.machsupport.com"
                ),
            ],
            "siemens_simodrive_611": [
                RetrofitSolution(
                    solution_name="Siemens S120 Upgrade",
                    vendor="Siemens",
                    part_number="S120-UPGRADE-KIT",
                    retrofit_type=RetrofitType.PARTIAL_RETROFIT,
                    price_usd=12000,
                    installation_hours=24,
                    compatibility_score=0.95,
                    requires_modifications=[
                        "Drive cabinet modifications",
                        "Updated parameterization"
                    ],
                    preserves_functionality=["All Sinumerik functions"],
                    adds_functionality=[
                        "Better diagnostics",
                        "Energy regeneration",
                        "Safety integrated"
                    ],
                    notes="Official Siemens upgrade path. Maintains full compatibility."
                ),
            ],
        }

    def _initialize_motors(self) -> Dict[str, IndustrialMotorSpec]:
        """Initialize industrial motor database"""
        return {
            "fanuc_a06b-0123-b175": IndustrialMotorSpec(
                manufacturer="Fanuc",
                model="A06B-0123-B175",
                motor_type="AC Servo",
                power_kw=3.0,
                voltage=200,
                current_amps=14,
                rpm_rated=3000,
                rpm_max=6000,
                torque_nm=9.55,
                encoder_type="Fanuc Serial Encoder",
                encoder_resolution=1000000,
                frame_size="Fanuc 10S",
                mounting="Flange",
                ip_rating="IP54",
                cooling="Fan"
            ),
            "yaskawa_sgmgv-09a": IndustrialMotorSpec(
                manufacturer="Yaskawa",
                model="SGMGV-09A",
                motor_type="AC Servo",
                power_kw=0.9,
                voltage=200,
                current_amps=5.5,
                rpm_rated=3000,
                rpm_max=5000,
                torque_nm=2.86,
                encoder_type="Yaskawa Serial Encoder",
                encoder_resolution=8388608,
                frame_size="60mm",
                mounting="Flange",
                ip_rating="IP65",
                cooling="Natural"
            ),
            "siemens_1fk7060": IndustrialMotorSpec(
                manufacturer="Siemens",
                model="1FK7060-5AF71",
                motor_type="AC Servo",
                power_kw=2.0,
                voltage=400,
                current_amps=4.7,
                rpm_rated=3000,
                rpm_max=6000,
                torque_nm=6.4,
                encoder_type="EnDat 2.2",
                encoder_resolution=2048,
                frame_size="60mm",
                mounting="Flange/Foot",
                ip_rating="IP64",
                cooling="Natural"
            ),
        }

    def find_cnc_retrofit(
        self,
        machine_brand: str,
        machine_model: str,
        failed_component: str
    ) -> List[RetrofitSolution]:
        """
        Find retrofit solutions for aging CNC equipment.

        Args:
            machine_brand: CNC brand (Fanuc, Siemens, etc.)
            machine_model: Control model (6M, 0M, 810D, etc.)
            failed_component: Component that needs replacement

        Returns:
            List of retrofit solutions sorted by compatibility score
        """
        results = []
        brand_lower = machine_brand.lower()
        component_lower = failed_component.lower()

        # CRT/Monitor replacement
        if any(term in component_lower for term in ["crt", "monitor", "display", "screen"]):
            if "fanuc" in brand_lower:
                results.extend(self.retrofit_catalog.get("fanuc_crt_monitor", []))

        # Complete control replacement
        if any(term in component_lower for term in ["control", "cnc", "cpu", "main board"]):
            if "fanuc" in brand_lower:
                results.extend(self.retrofit_catalog.get("fanuc_complete_control", []))

        # Drive replacement
        if any(term in component_lower for term in ["drive", "servo", "simodrive"]):
            if "siemens" in brand_lower:
                results.extend(self.retrofit_catalog.get("siemens_simodrive_611", []))

        # Sort by compatibility score
        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        return results

    def cross_reference_servo_drives(
        self,
        original_drive: str,
        motor_specs: Optional[Dict] = None
    ) -> List[ServoDriveMatch]:
        """
        Find compatible servo drives across manufacturers.

        Args:
            original_drive: Original drive model/part number
            motor_specs: Optional motor specifications for better matching

        Returns:
            List of compatible drive matches
        """
        results = []
        drive_key = original_drive.lower().replace(" ", "-").replace("_", "-")

        # Find the original drive in database
        original_info = None
        for key, info in self.servo_drives.items():
            if drive_key in key or info["model"].lower().replace(" ", "-") == drive_key:
                original_info = info
                break

        if not original_info:
            # Return generic recommendations
            return [ServoDriveMatch(
                original_drive=original_drive,
                replacement_drive="Contact supplier for cross-reference",
                manufacturer="Various",
                compatibility_score=0.0,
                power_match=False,
                voltage_match=False,
                encoder_compatibility="Unknown",
                wiring_changes=["Requires engineering analysis"],
                parameter_mapping_available=False,
                price_vs_original=1.0,
                notes=f"Drive {original_drive} not found in database. Manual cross-reference required."
            )]

        # Find equivalents
        for equiv in original_info.get("equivalents", []):
            power_match = True
            voltage_match = True

            # Check motor specs compatibility if provided
            if motor_specs:
                if motor_specs.get("power_kw"):
                    power_match = abs(motor_specs["power_kw"] - original_info["power_kw"]) < 1.0
                if motor_specs.get("voltage"):
                    voltage_match = motor_specs["voltage"] == original_info["voltage"]

            encoder_compat = "Adapter needed" if equiv.get("adapter_needed") else "Direct"

            results.append(ServoDriveMatch(
                original_drive=original_drive,
                replacement_drive=equiv["model"],
                manufacturer=equiv["model"].split()[0] if " " in equiv["model"] else "Various",
                compatibility_score=equiv["compatibility"],
                power_match=power_match,
                voltage_match=voltage_match,
                encoder_compatibility=encoder_compat,
                wiring_changes=["Different connector pinout", "Parameter setup required"],
                parameter_mapping_available=equiv["compatibility"] > 0.85,
                price_vs_original=0.4 if "Delta" in equiv["model"] else 0.7,
                notes=f"Cross-reference from {original_info['manufacturer']} to {equiv['model']}"
            ))

        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        return results

    def find_plc_migration_path(
        self,
        source_plc: str,
        current_io_count: Optional[Dict] = None
    ) -> Optional[PLCMigrationPlan]:
        """
        Plan PLC migration with I/O mapping and conversion tools.

        Args:
            source_plc: Source PLC model
            current_io_count: Optional dict with I/O counts

        Returns:
            PLCMigrationPlan with recommendations
        """
        source_key = None
        source_info = None

        # Find source PLC in database
        for key, info in self.plc_platforms.items():
            if (info["model"].lower() in source_plc.lower() or
                source_plc.lower() in info["model"].lower()):
                source_key = key
                source_info = info
                break

        if not source_info:
            return None

        # Get best migration target
        if not source_info.get("migration_targets"):
            return None

        best_target = source_info["migration_targets"][0]

        # Build migration plan
        io_mapping = {}
        if current_io_count:
            # Map I/O modules
            for io_type in ["discrete_in", "discrete_out", "analog_in", "analog_out"]:
                if io_type in current_io_count:
                    io_mapping[io_type] = f"Map to {best_target['target']} equivalent module"

        return PLCMigrationPlan(
            source_plc=source_info["model"],
            recommended_target=best_target["target"],
            target_manufacturer=source_info["manufacturer"],
            io_compatibility_score=best_target["compatibility"],
            code_conversion_tool=best_target.get("tool"),
            estimated_downtime_hours=8 if best_target["compatibility"] > 0.9 else 16,
            estimated_cost_usd=5000 + (2000 if best_target["compatibility"] < 0.85 else 0),
            io_mapping=io_mapping,
            software_changes=[
                "Convert ladder logic",
                "Update communication settings",
                "Reconfigure HMI addresses"
            ],
            hardware_changes=[
                f"Install {best_target['target']} rack and modules",
                "Update power supply if needed",
                "Replace I/O wiring terminations"
            ],
            alternatives=[
                {"plc": alt["target"], "compatibility": alt["compatibility"]}
                for alt in source_info["migration_targets"][1:]
            ],
            risks=[
                "Program conversion may require manual adjustment",
                "Custom functions may not have direct equivalents",
                "Production downtime during cutover"
            ],
            notes=f"Migration from {source_info['model']} to {best_target['target']} using {best_target.get('tool', 'manual conversion')}"
        )

    def find_industrial_fastener(
        self,
        application: str,
        environment: str,
        load_requirements: Dict
    ) -> IndustrialFastenerRecommendation:
        """
        Recommend industrial fasteners for machine applications.

        Industrial fasteners have different requirements than automotive:
        - Higher preloads
        - Vibration resistance critical
        - Coolant/oil exposure
        - Precise torque control

        Args:
            application: Application description
            environment: Operating environment
            load_requirements: Dict with preload_kn, fatigue_cycles, etc.

        Returns:
            IndustrialFastenerRecommendation
        """
        preload_kn = load_requirements.get("preload_kn", 50)
        fatigue_cycles = load_requirements.get("fatigue_cycles", 1e6)

        # Determine fastener grade based on preload
        if preload_kn > 80:
            grade = "12.9"
            material = "Alloy Steel, Quenched & Tempered"
        elif preload_kn > 50:
            grade = "10.9"
            material = "Medium Carbon Steel, Q&T"
        else:
            grade = "8.8"
            material = "Medium Carbon Steel"

        # Determine size based on preload (rough calculation)
        # M10 10.9 ~ 49kN proof load, M12 10.9 ~ 85kN
        if preload_kn > 80:
            size = "M14x1.5"
            torque = 190
        elif preload_kn > 50:
            size = "M12x1.25"
            torque = 115
        elif preload_kn > 30:
            size = "M10x1.25"
            torque = 65
        else:
            size = "M8x1.25"
            torque = 35

        # Coating based on environment
        coolant_exposure = "coolant" in environment.lower()
        vibration = "vibration" in environment.lower()

        if coolant_exposure:
            coating = "Geomet 500 (corrosion + lubricity)"
        else:
            coating = "Black Oxide or Zinc Flake"

        # Anti-vibration
        anti_vib = None
        if vibration or fatigue_cycles > 1e7:
            anti_vib = "Nord-Lock washer pair"

        # Thread locker
        thread_lock = None
        if vibration:
            thread_lock = "Loctite 271 (high strength)" if preload_kn > 50 else "Loctite 243 (medium)"

        spec = f"{size}-{grade} Socket Head Cap Screw"

        return IndustrialFastenerRecommendation(
            specification=spec,
            material=material,
            coating=coating,
            torque_nm=torque,
            preload_kn=preload_kn,
            thread_locker=thread_lock,
            anti_vibration=anti_vib,
            application_notes=f"For {application} in {environment}",
            alternative="Superbolt tensioner for critical or frequently-serviced joints" if preload_kn > 80 else None,
            mil_spec="MIL-DTL-1222" if grade == "12.9" else None,
            din_spec="DIN 912" if "Socket" in spec else "DIN 931"
        )

    def get_controller_info(self, manufacturer: str, model: str) -> Optional[CNCControllerSpec]:
        """Get detailed information about a CNC controller"""
        key = f"{manufacturer.lower()}_{model.lower().replace(' ', '_').replace('-', '_')}"

        for db_key, spec in self.cnc_controllers.items():
            if key in db_key or model.lower() in spec.model.lower():
                return spec
        return None


# Demo usage
if __name__ == "__main__":
    agent = MachinistAgent()

    print("=" * 60)
    print("Agent_13: MACHINIST - Industrial Equipment Intelligence")
    print("=" * 60)

    # Test CNC retrofit
    print("\n--- CNC Retrofit Search ---")
    retrofits = agent.find_cnc_retrofit("Fanuc", "6M", "CRT Monitor")
    for retrofit in retrofits:
        print(f"\nSolution: {retrofit.solution_name}")
        print(f"  Vendor: {retrofit.vendor}")
        print(f"  Price: ${retrofit.price_usd}")
        print(f"  Install time: {retrofit.installation_hours} hours")
        print(f"  Compatibility: {retrofit.compatibility_score:.0%}")
        print(f"  Type: {retrofit.retrofit_type.value}")

    # Test servo drive cross-reference
    print("\n--- Servo Drive Cross-Reference ---")
    matches = agent.cross_reference_servo_drives(
        "A06B-6079-H106",
        {"type": "AC servo", "power_kw": 3.7, "voltage": 200}
    )
    for match in matches:
        print(f"\nOriginal: {match.original_drive}")
        print(f"  Replacement: {match.replacement_drive}")
        print(f"  Compatibility: {match.compatibility_score:.0%}")
        print(f"  Encoder: {match.encoder_compatibility}")
        print(f"  Price vs original: {match.price_vs_original:.0%}")

    # Test PLC migration
    print("\n--- PLC Migration Planning ---")
    plan = agent.find_plc_migration_path("Allen-Bradley SLC 500")
    if plan:
        print(f"Source: {plan.source_plc}")
        print(f"Target: {plan.recommended_target}")
        print(f"I/O Compatibility: {plan.io_compatibility_score:.0%}")
        print(f"Conversion Tool: {plan.code_conversion_tool}")
        print(f"Estimated Downtime: {plan.estimated_downtime_hours} hours")
        print("Risks:")
        for risk in plan.risks:
            print(f"  - {risk}")

    # Test industrial fastener
    print("\n--- Industrial Fastener Selection ---")
    fastener = agent.find_industrial_fastener(
        application="CNC spindle mount",
        environment="coolant exposure, high vibration",
        load_requirements={"preload_kn": 60, "fatigue_cycles": 1e7}
    )
    print(f"Specification: {fastener.specification}")
    print(f"Material: {fastener.material}")
    print(f"Coating: {fastener.coating}")
    print(f"Torque: {fastener.torque_nm} Nm")
    print(f"Thread Locker: {fastener.thread_locker}")
    print(f"Anti-vibration: {fastener.anti_vibration}")
