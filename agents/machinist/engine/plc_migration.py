"""
PLC Migration Engine - Plan industrial PLC platform migrations

Handles:
- Allen-Bradley (PLC-5, SLC-500, MicroLogix, ControlLogix, CompactLogix)
- Siemens (S5, S7-200, S7-300, S7-400, S7-1200, S7-1500)
- Mitsubishi (FX, Q, iQ-R series)
- Omron (C200, CJ, NX series)
- GE Fanuc / Emerson (90-30, PACSystems)
- Automation Direct (DirectLogic, Productivity)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class PLCStatus(Enum):
    """PLC lifecycle status"""
    ACTIVE = "active"
    MATURE = "mature"              # Still supported, no new development
    PHASING_OUT = "phasing_out"    # Limited support, migrate soon
    DISCONTINUED = "discontinued"   # No longer sold
    OBSOLETE = "obsolete"          # No support available


class MigrationRisk(Enum):
    """Risk level for PLC migrations"""
    LOW = "low"                    # Well-documented path, tools available
    MEDIUM = "medium"              # Some manual work required
    HIGH = "high"                  # Significant engineering effort
    VERY_HIGH = "very_high"        # Major redesign may be needed


@dataclass
class PLCPlatform:
    """PLC platform specification"""
    manufacturer: str
    model: str
    series: str
    year_introduced: int
    year_end_of_life: Optional[int]
    status: PLCStatus
    programming_software: str
    languages_supported: List[str]  # "Ladder", "FBD", "ST", "SFC", "IL"
    io_types: List[str]
    max_io_points: int
    memory_kb: int
    communication_protocols: List[str]
    scan_time_ms: float            # Typical scan time
    safety_certified: bool


@dataclass
class IOModule:
    """I/O module specification for migration mapping"""
    manufacturer: str
    model: str
    io_type: str                   # "DI", "DO", "AI", "AO", "HSC", "Encoder"
    points: int
    voltage_level: str             # "24VDC", "120VAC", "0-10V", "4-20mA"
    current_rating_ma: Optional[int]
    special_features: List[str]


@dataclass
class MigrationMapping:
    """Mapping between source and target PLC components"""
    source_component: str
    target_component: str
    compatibility: float           # 0.0 to 1.0
    wiring_changes: List[str]
    address_mapping: Dict[str, str]  # Old address -> New address
    notes: str


@dataclass
class CodeConversionResult:
    """Results of program code conversion analysis"""
    total_rungs: int
    auto_convertible_rungs: int
    manual_review_rungs: int
    incompatible_instructions: List[str]
    conversion_tool: Optional[str]
    estimated_manual_hours: float


class PLCMigrationEngine:
    """
    Engine for planning PLC platform migrations

    Supports migration analysis for:
    - I/O hardware mapping
    - Communication protocol conversion
    - Program code conversion
    - HMI address updates
    """

    def __init__(self):
        self.platforms = self._initialize_platforms()
        self.migration_paths = self._initialize_migration_paths()
        self.io_equivalents = self._initialize_io_equivalents()

    def _initialize_platforms(self) -> Dict[str, PLCPlatform]:
        """Initialize PLC platform database"""
        return {
            # Allen-Bradley
            "ab_plc5": PLCPlatform(
                manufacturer="Allen-Bradley",
                model="PLC-5",
                series="PLC-5",
                year_introduced=1985,
                year_end_of_life=2017,
                status=PLCStatus.OBSOLETE,
                programming_software="RSLogix 5",
                languages_supported=["Ladder", "SFC"],
                io_types=["Discrete", "Analog", "Motion", "High-speed counter"],
                max_io_points=3072,
                memory_kb=100,
                communication_protocols=["DH+", "Ethernet/IP", "ControlNet"],
                scan_time_ms=1.0,
                safety_certified=False
            ),
            "ab_slc500": PLCPlatform(
                manufacturer="Allen-Bradley",
                model="SLC 500",
                series="SLC",
                year_introduced=1991,
                year_end_of_life=2022,
                status=PLCStatus.OBSOLETE,
                programming_software="RSLogix 500",
                languages_supported=["Ladder"],
                io_types=["Discrete", "Analog", "High-speed counter"],
                max_io_points=4096,
                memory_kb=64,
                communication_protocols=["DH+", "DH-485", "Ethernet/IP"],
                scan_time_ms=0.9,
                safety_certified=False
            ),
            "ab_compactlogix": PLCPlatform(
                manufacturer="Allen-Bradley",
                model="CompactLogix 5380",
                series="Logix",
                year_introduced=2017,
                year_end_of_life=None,
                status=PLCStatus.ACTIVE,
                programming_software="Studio 5000 Logix Designer",
                languages_supported=["Ladder", "FBD", "ST", "SFC"],
                io_types=["Discrete", "Analog", "Motion", "Safety", "High-speed counter"],
                max_io_points=16000,
                memory_kb=20000,
                communication_protocols=["Ethernet/IP", "Modbus TCP"],
                scan_time_ms=0.2,
                safety_certified=True
            ),
            "ab_controllogix": PLCPlatform(
                manufacturer="Allen-Bradley",
                model="ControlLogix 5580",
                series="Logix",
                year_introduced=2018,
                year_end_of_life=None,
                status=PLCStatus.ACTIVE,
                programming_software="Studio 5000 Logix Designer",
                languages_supported=["Ladder", "FBD", "ST", "SFC"],
                io_types=["Discrete", "Analog", "Motion", "Safety", "Process"],
                max_io_points=128000,
                memory_kb=40000,
                communication_protocols=["Ethernet/IP", "ControlNet", "DeviceNet"],
                scan_time_ms=0.1,
                safety_certified=True
            ),
            # Siemens
            "siemens_s5": PLCPlatform(
                manufacturer="Siemens",
                model="S5-115U",
                series="SIMATIC S5",
                year_introduced=1979,
                year_end_of_life=1998,
                status=PLCStatus.OBSOLETE,
                programming_software="STEP 5",
                languages_supported=["Ladder", "IL", "FBD"],
                io_types=["Discrete", "Analog"],
                max_io_points=2048,
                memory_kb=64,
                communication_protocols=["MPI", "Profibus"],
                scan_time_ms=2.0,
                safety_certified=False
            ),
            "siemens_s7_300": PLCPlatform(
                manufacturer="Siemens",
                model="S7-300",
                series="SIMATIC S7",
                year_introduced=1994,
                year_end_of_life=2023,
                status=PLCStatus.PHASING_OUT,
                programming_software="STEP 7 / TIA Portal",
                languages_supported=["Ladder", "FBD", "ST", "IL", "SFC"],
                io_types=["Discrete", "Analog", "Motion", "Safety"],
                max_io_points=8192,
                memory_kb=2048,
                communication_protocols=["MPI", "Profibus", "Profinet"],
                scan_time_ms=0.1,
                safety_certified=True
            ),
            "siemens_s7_1500": PLCPlatform(
                manufacturer="Siemens",
                model="S7-1500",
                series="SIMATIC S7",
                year_introduced=2012,
                year_end_of_life=None,
                status=PLCStatus.ACTIVE,
                programming_software="TIA Portal",
                languages_supported=["Ladder", "FBD", "ST", "SCL", "SFC", "Graph"],
                io_types=["Discrete", "Analog", "Motion", "Safety", "Technology"],
                max_io_points=65536,
                memory_kb=30000,
                communication_protocols=["Profinet", "Profibus", "Modbus TCP", "OPC UA"],
                scan_time_ms=0.01,
                safety_certified=True
            ),
            # Mitsubishi
            "mitsubishi_fx2n": PLCPlatform(
                manufacturer="Mitsubishi",
                model="FX2N",
                series="FX",
                year_introduced=1997,
                year_end_of_life=2020,
                status=PLCStatus.DISCONTINUED,
                programming_software="GX Developer",
                languages_supported=["Ladder", "IL"],
                io_types=["Discrete", "Analog", "Positioning"],
                max_io_points=256,
                memory_kb=16,
                communication_protocols=["RS-485", "CC-Link"],
                scan_time_ms=0.65,
                safety_certified=False
            ),
            "mitsubishi_fx5u": PLCPlatform(
                manufacturer="Mitsubishi",
                model="FX5U",
                series="FX5",
                year_introduced=2016,
                year_end_of_life=None,
                status=PLCStatus.ACTIVE,
                programming_software="GX Works3",
                languages_supported=["Ladder", "FBD", "ST"],
                io_types=["Discrete", "Analog", "Positioning", "High-speed counter"],
                max_io_points=512,
                memory_kb=128,
                communication_protocols=["Ethernet", "CC-Link IE", "Modbus"],
                scan_time_ms=0.034,
                safety_certified=False
            ),
            # Omron
            "omron_c200h": PLCPlatform(
                manufacturer="Omron",
                model="C200H",
                series="C200",
                year_introduced=1988,
                year_end_of_life=2010,
                status=PLCStatus.OBSOLETE,
                programming_software="CX-Programmer",
                languages_supported=["Ladder"],
                io_types=["Discrete", "Analog"],
                max_io_points=2048,
                memory_kb=32,
                communication_protocols=["Host Link", "Controller Link"],
                scan_time_ms=1.0,
                safety_certified=False
            ),
            "omron_nx1": PLCPlatform(
                manufacturer="Omron",
                model="NX1P2",
                series="NX",
                year_introduced=2018,
                year_end_of_life=None,
                status=PLCStatus.ACTIVE,
                programming_software="Sysmac Studio",
                languages_supported=["Ladder", "ST", "FBD", "SFC"],
                io_types=["Discrete", "Analog", "Motion", "Safety"],
                max_io_points=2048,
                memory_kb=5000,
                communication_protocols=["EtherNet/IP", "EtherCAT", "Modbus TCP"],
                scan_time_ms=0.5,
                safety_certified=True
            ),
        }

    def _initialize_migration_paths(self) -> Dict[str, Dict]:
        """Initialize recommended migration paths"""
        return {
            "ab_plc5": {
                "primary": {
                    "target": "ab_controllogix",
                    "compatibility": 0.88,
                    "tool": "Studio 5000 Project Migration",
                    "risk": MigrationRisk.MEDIUM,
                    "notes": "Well-documented migration path. Most instructions convert automatically."
                },
                "alternatives": [
                    {
                        "target": "ab_compactlogix",
                        "compatibility": 0.85,
                        "tool": "Studio 5000",
                        "risk": MigrationRisk.MEDIUM,
                        "notes": "Good for smaller systems"
                    }
                ]
            },
            "ab_slc500": {
                "primary": {
                    "target": "ab_compactlogix",
                    "compatibility": 0.92,
                    "tool": "Studio 5000 Logix Designer",
                    "risk": MigrationRisk.LOW,
                    "notes": "Direct migration path with high compatibility"
                },
                "alternatives": [
                    {
                        "target": "ab_controllogix",
                        "compatibility": 0.90,
                        "tool": "Studio 5000",
                        "risk": MigrationRisk.LOW,
                        "notes": "For larger systems"
                    }
                ]
            },
            "siemens_s5": {
                "primary": {
                    "target": "siemens_s7_1500",
                    "compatibility": 0.75,
                    "tool": "TIA Portal Migration Tool",
                    "risk": MigrationRisk.HIGH,
                    "notes": "Generation gap requires significant rework. Consider hardware-in-the-loop testing."
                },
                "alternatives": [
                    {
                        "target": "siemens_s7_300",
                        "compatibility": 0.82,
                        "tool": "S5->S7 Converter",
                        "risk": MigrationRisk.MEDIUM,
                        "notes": "Intermediate step, but S7-300 is phasing out"
                    }
                ]
            },
            "siemens_s7_300": {
                "primary": {
                    "target": "siemens_s7_1500",
                    "compatibility": 0.95,
                    "tool": "TIA Portal Migration",
                    "risk": MigrationRisk.LOW,
                    "notes": "Excellent migration support. Most programs convert with minimal changes."
                }
            },
            "mitsubishi_fx2n": {
                "primary": {
                    "target": "mitsubishi_fx5u",
                    "compatibility": 0.90,
                    "tool": "GX Works3 Project Converter",
                    "risk": MigrationRisk.LOW,
                    "notes": "Same family, good compatibility"
                }
            },
            "omron_c200h": {
                "primary": {
                    "target": "omron_nx1",
                    "compatibility": 0.82,
                    "tool": "Sysmac Studio Import",
                    "risk": MigrationRisk.MEDIUM,
                    "notes": "Different architecture, but conversion tools available"
                }
            },
        }

    def _initialize_io_equivalents(self) -> Dict[str, Dict]:
        """Initialize I/O module equivalents across platforms"""
        return {
            "ab_slc_di_16": {
                "model": "1746-IB16",
                "type": "Discrete Input",
                "points": 16,
                "voltage": "24VDC",
                "equivalents": [
                    {"platform": "ab_compactlogix", "model": "5069-IB16", "notes": "Direct equivalent"},
                    {"platform": "siemens_s7_1500", "model": "6ES7521-1BH00", "notes": "Similar function"},
                ]
            },
            "ab_slc_do_16": {
                "model": "1746-OB16",
                "type": "Discrete Output",
                "points": 16,
                "voltage": "24VDC",
                "equivalents": [
                    {"platform": "ab_compactlogix", "model": "5069-OB16", "notes": "Direct equivalent"},
                    {"platform": "siemens_s7_1500", "model": "6ES7522-1BH00", "notes": "Similar function"},
                ]
            },
            "ab_slc_ai_4": {
                "model": "1746-NI4",
                "type": "Analog Input",
                "points": 4,
                "voltage": "4-20mA/0-10V",
                "equivalents": [
                    {"platform": "ab_compactlogix", "model": "5069-IF4", "notes": "Higher resolution"},
                    {"platform": "siemens_s7_1500", "model": "6ES7531-7KF00", "notes": "Similar specs"},
                ]
            },
        }

    def analyze_migration(
        self,
        source_platform: str,
        io_inventory: Optional[Dict[str, int]] = None,
        program_stats: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze migration requirements for a PLC platform.

        Args:
            source_platform: Source PLC platform key
            io_inventory: Dict of I/O module types and quantities
            program_stats: Dict with program statistics

        Returns:
            Comprehensive migration analysis
        """
        source = self.platforms.get(source_platform)
        if not source:
            return {"error": f"Unknown platform: {source_platform}"}

        migration_info = self.migration_paths.get(source_platform, {})
        primary_target = migration_info.get("primary", {})

        # Calculate estimated costs
        base_cpu_cost = 3000  # Average new CPU cost
        io_cost_per_point = 15  # Average cost per I/O point

        total_io_points = 0
        if io_inventory:
            total_io_points = sum(io_inventory.values())

        estimated_hardware_cost = base_cpu_cost + (total_io_points * io_cost_per_point)

        # Estimate engineering hours
        base_engineering_hours = 40
        if primary_target.get("risk") == MigrationRisk.LOW:
            engineering_multiplier = 1.0
        elif primary_target.get("risk") == MigrationRisk.MEDIUM:
            engineering_multiplier = 1.5
        elif primary_target.get("risk") == MigrationRisk.HIGH:
            engineering_multiplier = 2.5
        else:
            engineering_multiplier = 4.0

        estimated_engineering_hours = base_engineering_hours * engineering_multiplier

        return {
            "source": {
                "platform": source.model,
                "manufacturer": source.manufacturer,
                "status": source.status.value,
                "end_of_life": source.year_end_of_life
            },
            "recommended_target": {
                "platform": primary_target.get("target", "Unknown"),
                "compatibility": primary_target.get("compatibility", 0),
                "conversion_tool": primary_target.get("tool"),
                "risk_level": primary_target.get("risk", MigrationRisk.HIGH).value,
                "notes": primary_target.get("notes", "")
            },
            "alternatives": migration_info.get("alternatives", []),
            "estimates": {
                "hardware_cost_usd": estimated_hardware_cost,
                "engineering_hours": estimated_engineering_hours,
                "typical_downtime_hours": 8 if primary_target.get("compatibility", 0) > 0.9 else 24
            },
            "io_points_to_migrate": total_io_points,
            "warnings": self._get_migration_warnings(source, primary_target)
        }

    def _get_migration_warnings(self, source: PLCPlatform, target_info: Dict) -> List[str]:
        """Generate warnings for migration"""
        warnings = []

        if source.status == PLCStatus.OBSOLETE:
            warnings.append("Source platform is OBSOLETE - spare parts may be unavailable")

        if target_info.get("compatibility", 0) < 0.80:
            warnings.append("Low compatibility score - expect significant manual rework")

        if "Safety" in source.io_types and not target_info.get("safety_retained", True):
            warnings.append("Safety functions require re-certification after migration")

        if source.year_introduced and source.year_introduced < 1995:
            warnings.append("Legacy platform - documentation may be incomplete")

        return warnings

    def get_io_mapping(
        self,
        source_platform: str,
        target_platform: str,
        source_module: str
    ) -> Optional[Dict]:
        """Get I/O module mapping between platforms"""
        source_info = self.io_equivalents.get(source_module)
        if not source_info:
            return None

        for equiv in source_info.get("equivalents", []):
            if equiv["platform"] == target_platform:
                return {
                    "source": source_info["model"],
                    "target": equiv["model"],
                    "type": source_info["type"],
                    "points": source_info["points"],
                    "notes": equiv["notes"]
                }

        return None

    def get_platform_info(self, platform_key: str) -> Optional[PLCPlatform]:
        """Get detailed information about a PLC platform"""
        return self.platforms.get(platform_key)

    def list_obsolete_platforms(self) -> List[PLCPlatform]:
        """List all obsolete platforms that should be migrated"""
        return [
            p for p in self.platforms.values()
            if p.status in [PLCStatus.OBSOLETE, PLCStatus.DISCONTINUED]
        ]
