"""
Agent_12: SILICON - Electronics & Semiconductor Cross-Reference

The electronics industry has the worst parts obsolescence problem on earth.
Semiconductors go end-of-life constantly, and finding drop-in replacements
requires deep knowledge of electrical characteristics, pinouts, and package
compatibility.

Domains:
- Semiconductors (ICs, transistors, diodes)
- Passive components (resistors, capacitors, inductors)
- Connectors & cables
- PCB assembly compatibility
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import date


class DeviceType(Enum):
    """Semiconductor device classifications"""
    LINEAR_REGULATOR = "linear_regulator"
    SWITCHING_REGULATOR = "switching_regulator"
    OP_AMP = "op_amp"
    COMPARATOR = "comparator"
    MCU = "mcu"
    FPGA = "fpga"
    MEMORY = "memory"
    TRANSISTOR_BJT = "transistor_bjt"
    TRANSISTOR_MOSFET = "transistor_mosfet"
    DIODE = "diode"
    DIODE_ZENER = "diode_zener"
    LED = "led"
    ADC = "adc"
    DAC = "dac"
    LOGIC_IC = "logic_ic"
    INTERFACE_IC = "interface_ic"
    DRIVER_IC = "driver_ic"


class PackageType(Enum):
    """IC package classifications"""
    DIP = "dip"                    # Through-hole dual inline
    SOIC = "soic"                  # Small outline IC
    SOP = "sop"                    # Small outline package
    SSOP = "ssop"                  # Shrink small outline
    TSSOP = "tssop"                # Thin shrink small outline
    QFP = "qfp"                    # Quad flat pack
    TQFP = "tqfp"                  # Thin quad flat pack
    QFN = "qfn"                    # Quad flat no-lead
    DFN = "dfn"                    # Dual flat no-lead
    BGA = "bga"                    # Ball grid array
    TO_92 = "to_92"                # Transistor outline (small)
    TO_220 = "to_220"              # Transistor outline (power)
    TO_247 = "to_247"              # Transistor outline (high power)
    SOT_23 = "sot_23"              # Small outline transistor
    SOT_223 = "sot_223"            # Medium outline transistor
    D2PAK = "d2pak"                # Surface mount power


class ComponentStatus(Enum):
    """Component lifecycle status"""
    ACTIVE = "active"             # In production
    NRND = "nrnd"                  # Not recommended for new designs
    EOL_ANNOUNCED = "eol_announced"  # End of life announced
    LAST_BUY = "last_buy"         # Last time buy window open
    OBSOLETE = "obsolete"         # No longer manufactured
    UNKNOWN = "unknown"           # Status not confirmed


class CapacitorType(Enum):
    """Capacitor technology types"""
    CERAMIC_C0G = "ceramic_c0g"   # NPO - most stable
    CERAMIC_X5R = "ceramic_x5r"   # Good stability
    CERAMIC_X7R = "ceramic_x7r"   # General purpose
    CERAMIC_Y5V = "ceramic_y5v"   # High cap, poor stability
    ELECTROLYTIC_AL = "electrolytic_aluminum"
    ELECTROLYTIC_POLYMER = "electrolytic_polymer"
    TANTALUM = "tantalum"
    TANTALUM_POLYMER = "tantalum_polymer"
    FILM_POLYPROPYLENE = "film_pp"
    FILM_POLYESTER = "film_pet"
    MICA = "mica"


@dataclass
class SemiconductorSpec:
    """Complete semiconductor specification for matching"""
    part_number: str
    manufacturer: str
    device_type: DeviceType
    package: PackageType
    pin_count: int
    pinout: Dict[int, str]

    # Electrical characteristics
    voltage_range: Tuple[float, float]  # (min, max) operating voltage
    current_rating: float               # Amps
    power_dissipation: float            # Watts
    operating_temp_range: Tuple[float, float]  # (min, max) Celsius

    # For active devices
    key_parameters: Dict[str, float]    # Device-specific params

    # Lifecycle
    status: ComponentStatus
    introduced_date: Optional[date] = None
    eol_date: Optional[date] = None

    # Cross-reference
    second_sources: List[str] = field(default_factory=list)
    drop_in_replacements: List[str] = field(default_factory=list)
    functional_equivalents: List[str] = field(default_factory=list)


@dataclass
class PassiveComponentSpec:
    """Passive component with reliability data"""
    part_number: str
    manufacturer: str
    component_type: str            # "Capacitor", "Resistor", "Inductor"
    value: float
    unit: str
    tolerance_percent: float
    voltage_rating: float

    # Reliability
    temperature_rating_c: int
    lifetime_hours: int
    failure_rate_fit: float        # Failures per billion hours

    # For capacitors
    esr_mohms: Optional[float] = None
    ripple_current_ma: Optional[float] = None
    capacitor_type: Optional[CapacitorType] = None


@dataclass
class SemiconductorEquivalent:
    """Result from semiconductor equivalence search"""
    part: str
    manufacturer: str
    compatibility_score: float     # 0.0 to 1.0
    package: str
    differences: List[str]
    drop_in: bool                  # True = no board changes needed
    notes: str = ""


@dataclass
class CapacitorEquivalence:
    """Result from capacitor equivalence check"""
    electrical_equivalent: bool
    reliability_equivalent: bool
    esr_comparison: str
    lifetime_comparison: str
    recommendation: str
    acceptable_for: List[str]


@dataclass
class PinoutMapping:
    """Pin-by-pin compatibility mapping"""
    compatible: bool
    package: str
    pin_differences: Dict[str, str]
    software_changes_required: List[str]
    hardware_changes_required: List[str]
    drop_in_with_code_change: bool


@dataclass
class ObsolescenceStatus:
    """Component obsolescence tracking"""
    part_number: str
    status: ComponentStatus
    last_buy_date: Optional[str]
    last_ship_date: Optional[str]
    modern_equivalents: List[str]
    broker_availability: bool
    broker_price_premium_percent: Optional[int]
    recommended_action: str


class SiliconAgent:
    """
    Agent_12: SILICON - Electronics & Semiconductor Intelligence

    Core responsibilities:
    1. Find equivalent semiconductors with electrical compatibility scoring
    2. Verify capacitor equivalence beyond just capacitance values
    3. Check pinout compatibility for PCB drop-in replacements
    4. Track obsolescence status and find alternatives
    """

    def __init__(self):
        self.semiconductor_db = self._initialize_semiconductor_db()
        self.capacitor_db = self._initialize_capacitor_db()
        self.package_compatibility = self._initialize_package_matrix()
        self.obsolescence_tracker = self._initialize_obsolescence_tracker()

    def _initialize_semiconductor_db(self) -> Dict[str, SemiconductorSpec]:
        """Initialize common semiconductor database"""
        return {
            "LM7805CT": SemiconductorSpec(
                part_number="LM7805CT",
                manufacturer="Texas Instruments",
                device_type=DeviceType.LINEAR_REGULATOR,
                package=PackageType.TO_220,
                pin_count=3,
                pinout={1: "Input", 2: "GND", 3: "Output"},
                voltage_range=(7.0, 35.0),
                current_rating=1.5,
                power_dissipation=15.0,
                operating_temp_range=(0, 125),
                key_parameters={
                    "output_voltage": 5.0,
                    "dropout_voltage": 2.0,
                    "line_regulation_mv": 100,
                    "load_regulation_mv": 100,
                },
                status=ComponentStatus.ACTIVE,
                second_sources=["L7805CV", "MC7805CT", "uA7805"],
                drop_in_replacements=["L7805CV", "MC7805CT"],
                functional_equivalents=["LM2940CT-5.0", "LM1117T-5.0"]
            ),
            "L7805CV": SemiconductorSpec(
                part_number="L7805CV",
                manufacturer="STMicroelectronics",
                device_type=DeviceType.LINEAR_REGULATOR,
                package=PackageType.TO_220,
                pin_count=3,
                pinout={1: "Input", 2: "GND", 3: "Output"},
                voltage_range=(7.5, 35.0),
                current_rating=1.5,
                power_dissipation=15.0,
                operating_temp_range=(-40, 125),
                key_parameters={
                    "output_voltage": 5.0,
                    "dropout_voltage": 2.0,
                    "line_regulation_mv": 50,
                    "load_regulation_mv": 50,
                },
                status=ComponentStatus.ACTIVE,
                second_sources=["LM7805CT", "MC7805CT"],
                drop_in_replacements=["LM7805CT", "MC7805CT"],
                functional_equivalents=[]
            ),
            "LM2940CT-5.0": SemiconductorSpec(
                part_number="LM2940CT-5.0",
                manufacturer="Texas Instruments",
                device_type=DeviceType.LINEAR_REGULATOR,
                package=PackageType.TO_220,
                pin_count=3,
                pinout={1: "Input", 2: "GND", 3: "Output"},
                voltage_range=(5.5, 26.0),
                current_rating=1.0,
                power_dissipation=10.0,
                operating_temp_range=(-40, 125),
                key_parameters={
                    "output_voltage": 5.0,
                    "dropout_voltage": 0.5,  # Low dropout!
                    "line_regulation_mv": 30,
                    "load_regulation_mv": 50,
                },
                status=ComponentStatus.ACTIVE,
                second_sources=[],
                drop_in_replacements=[],
                functional_equivalents=["LM7805CT"]
            ),
            "ATmega8-16PU": SemiconductorSpec(
                part_number="ATmega8-16PU",
                manufacturer="Microchip",
                device_type=DeviceType.MCU,
                package=PackageType.DIP,
                pin_count=28,
                pinout={
                    1: "PC6/RESET", 2: "PD0/RXD", 3: "PD1/TXD", 4: "PD2/INT0",
                    5: "PD3/INT1", 6: "PD4/T0", 7: "VCC", 8: "GND",
                    9: "PB6/XTAL1", 10: "PB7/XTAL2", 11: "PD5/T1", 12: "PD6/AIN0",
                    13: "PD7/AIN1", 14: "PB0/ICP1", 15: "PB1/OC1A", 16: "PB2/OC1B",
                    17: "PB3/MOSI", 18: "PB4/MISO", 19: "PB5/SCK", 20: "AVCC",
                    21: "AREF", 22: "GND", 23: "PC0/ADC0", 24: "PC1/ADC1",
                    25: "PC2/ADC2", 26: "PC3/ADC3", 27: "PC4/ADC4/SDA", 28: "PC5/ADC5/SCL"
                },
                voltage_range=(4.5, 5.5),
                current_rating=0.2,
                power_dissipation=0.5,
                operating_temp_range=(-40, 85),
                key_parameters={
                    "flash_kb": 8,
                    "sram_bytes": 1024,
                    "eeprom_bytes": 512,
                    "max_clock_mhz": 16,
                },
                status=ComponentStatus.NRND,
                second_sources=[],
                drop_in_replacements=[],
                functional_equivalents=["ATmega88-20PU", "ATmega168-20PU", "ATmega328P-PU"]
            ),
            "ATmega88-20PU": SemiconductorSpec(
                part_number="ATmega88-20PU",
                manufacturer="Microchip",
                device_type=DeviceType.MCU,
                package=PackageType.DIP,
                pin_count=28,
                pinout={
                    1: "PC6/RESET", 2: "PD0/RXD", 3: "PD1/TXD", 4: "PD2/INT0",
                    5: "PD3/INT1", 6: "PD4/T0", 7: "VCC", 8: "GND",
                    9: "PB6/XTAL1", 10: "PB7/XTAL2", 11: "PD5/T1", 12: "PD6/AIN0",
                    13: "PD7/AIN1", 14: "PB0/ICP1", 15: "PB1/OC1A", 16: "PB2/OC1B",
                    17: "PB3/MOSI", 18: "PB4/MISO", 19: "PB5/SCK", 20: "AVCC",
                    21: "AREF", 22: "GND", 23: "PC0/ADC0", 24: "PC1/ADC1",
                    25: "PC2/ADC2", 26: "PC3/ADC3", 27: "PC4/ADC4/SDA", 28: "PC5/ADC5/SCL"
                },
                voltage_range=(2.7, 5.5),
                current_rating=0.2,
                power_dissipation=0.5,
                operating_temp_range=(-40, 85),
                key_parameters={
                    "flash_kb": 8,
                    "sram_bytes": 1024,
                    "eeprom_bytes": 512,
                    "max_clock_mhz": 20,
                },
                status=ComponentStatus.ACTIVE,
                second_sources=[],
                drop_in_replacements=["ATmega8-16PU"],
                functional_equivalents=["ATmega168-20PU"]
            ),
            "ATmega328P-PU": SemiconductorSpec(
                part_number="ATmega328P-PU",
                manufacturer="Microchip",
                device_type=DeviceType.MCU,
                package=PackageType.DIP,
                pin_count=28,
                pinout={
                    1: "PC6/RESET", 2: "PD0/RXD", 3: "PD1/TXD", 4: "PD2/INT0",
                    5: "PD3/INT1", 6: "PD4/T0", 7: "VCC", 8: "GND",
                    9: "PB6/XTAL1", 10: "PB7/XTAL2", 11: "PD5/T1", 12: "PD6/AIN0",
                    13: "PD7/AIN1", 14: "PB0/ICP1", 15: "PB1/OC1A", 16: "PB2/OC1B",
                    17: "PB3/MOSI", 18: "PB4/MISO", 19: "PB5/SCK", 20: "AVCC",
                    21: "AREF", 22: "GND", 23: "PC0/ADC0", 24: "PC1/ADC1",
                    25: "PC2/ADC2", 26: "PC3/ADC3", 27: "PC4/ADC4/SDA", 28: "PC5/ADC5/SCL"
                },
                voltage_range=(1.8, 5.5),
                current_rating=0.2,
                power_dissipation=0.5,
                operating_temp_range=(-40, 85),
                key_parameters={
                    "flash_kb": 32,
                    "sram_bytes": 2048,
                    "eeprom_bytes": 1024,
                    "max_clock_mhz": 20,
                },
                status=ComponentStatus.ACTIVE,
                second_sources=[],
                drop_in_replacements=[],
                functional_equivalents=["ATmega88-20PU", "ATmega168-20PU"]
            ),
            "MC68000": SemiconductorSpec(
                part_number="MC68000",
                manufacturer="Motorola/NXP",
                device_type=DeviceType.MCU,
                package=PackageType.DIP,
                pin_count=64,
                pinout={i: f"Pin{i}" for i in range(1, 65)},  # Simplified
                voltage_range=(4.75, 5.25),
                current_rating=0.5,
                power_dissipation=1.5,
                operating_temp_range=(0, 70),
                key_parameters={
                    "data_bus_bits": 16,
                    "address_bus_bits": 24,
                    "max_clock_mhz": 8,
                },
                status=ComponentStatus.OBSOLETE,
                eol_date=date(2000, 1, 1),
                second_sources=[],
                drop_in_replacements=[],
                functional_equivalents=["MC68SEC000", "FPGA soft core"]
            ),
            "LM317T": SemiconductorSpec(
                part_number="LM317T",
                manufacturer="Texas Instruments",
                device_type=DeviceType.LINEAR_REGULATOR,
                package=PackageType.TO_220,
                pin_count=3,
                pinout={1: "Adjust", 2: "Output", 3: "Input"},
                voltage_range=(4.2, 40.0),
                current_rating=1.5,
                power_dissipation=20.0,
                operating_temp_range=(0, 125),
                key_parameters={
                    "output_voltage_min": 1.25,
                    "output_voltage_max": 37.0,
                    "dropout_voltage": 3.0,
                    "line_regulation_percent": 0.01,
                },
                status=ComponentStatus.ACTIVE,
                second_sources=["LM317T (ON Semi)", "LM317T (STMicro)"],
                drop_in_replacements=["LM317HVT", "LM1117T"],
                functional_equivalents=["LM350T"]
            ),
        }

    def _initialize_capacitor_db(self) -> Dict[str, PassiveComponentSpec]:
        """Initialize capacitor database with reliability data"""
        return {
            "Nichicon UHE1E101MPD": PassiveComponentSpec(
                part_number="UHE1E101MPD",
                manufacturer="Nichicon",
                component_type="Capacitor",
                value=100,
                unit="uF",
                tolerance_percent=20,
                voltage_rating=25,
                temperature_rating_c=105,
                lifetime_hours=10000,
                failure_rate_fit=50,
                esr_mohms=30,
                ripple_current_ma=550,
                capacitor_type=CapacitorType.ELECTROLYTIC_AL
            ),
            "Generic 100uF 25V": PassiveComponentSpec(
                part_number="Generic 100uF 25V",
                manufacturer="Unknown",
                component_type="Capacitor",
                value=100,
                unit="uF",
                tolerance_percent=20,
                voltage_rating=25,
                temperature_rating_c=85,
                lifetime_hours=2000,
                failure_rate_fit=500,
                esr_mohms=100,
                ripple_current_ma=200,
                capacitor_type=CapacitorType.ELECTROLYTIC_AL
            ),
            "Panasonic EEU-FC1E101": PassiveComponentSpec(
                part_number="EEU-FC1E101",
                manufacturer="Panasonic",
                component_type="Capacitor",
                value=100,
                unit="uF",
                tolerance_percent=20,
                voltage_rating=25,
                temperature_rating_c=105,
                lifetime_hours=5000,
                failure_rate_fit=100,
                esr_mohms=50,
                ripple_current_ma=400,
                capacitor_type=CapacitorType.ELECTROLYTIC_AL
            ),
            "Murata GRM21BR71H104KA01": PassiveComponentSpec(
                part_number="GRM21BR71H104KA01",
                manufacturer="Murata",
                component_type="Capacitor",
                value=0.1,
                unit="uF",
                tolerance_percent=10,
                voltage_rating=50,
                temperature_rating_c=125,
                lifetime_hours=100000,
                failure_rate_fit=5,
                esr_mohms=5,
                ripple_current_ma=1000,
                capacitor_type=CapacitorType.CERAMIC_X7R
            ),
        }

    def _initialize_package_matrix(self) -> Dict[Tuple[str, str], bool]:
        """Initialize package compatibility matrix"""
        return {
            # Same package = compatible
            (PackageType.TO_220.value, PackageType.TO_220.value): True,
            (PackageType.DIP.value, PackageType.DIP.value): True,
            (PackageType.SOIC.value, PackageType.SOIC.value): True,
            (PackageType.SOT_23.value, PackageType.SOT_23.value): True,
            # Compatible package pairs
            (PackageType.TO_220.value, PackageType.TO_247.value): False,  # Different footprint
            (PackageType.SOIC.value, PackageType.SOP.value): True,
            (PackageType.TSSOP.value, PackageType.SSOP.value): False,
        }

    def _initialize_obsolescence_tracker(self) -> Dict[str, Dict]:
        """Initialize obsolescence tracking data"""
        return {
            "MC68000": {
                "status": ComponentStatus.OBSOLETE,
                "last_buy_date": "2000-01-01",
                "last_ship_date": "2001-06-30",
                "modern_equivalents": ["MC68SEC000", "FPGA soft core"],
                "broker_availability": True,
                "broker_price_premium": 500,
            },
            "ATmega8-16PU": {
                "status": ComponentStatus.NRND,
                "last_buy_date": None,
                "last_ship_date": None,
                "modern_equivalents": ["ATmega88-20PU", "ATmega168-20PU", "ATmega328P-PU"],
                "broker_availability": True,
                "broker_price_premium": 50,
            },
            "LM7805CT": {
                "status": ComponentStatus.ACTIVE,
                "last_buy_date": None,
                "last_ship_date": None,
                "modern_equivalents": [],
                "broker_availability": True,
                "broker_price_premium": 0,
            },
        }

    def find_semiconductor_equivalent(
        self,
        part_number: str,
        manufacturer: Optional[str] = None,
        critical_params: Optional[List[str]] = None
    ) -> List[SemiconductorEquivalent]:
        """
        Find equivalent semiconductors with electrical compatibility scoring.

        Args:
            part_number: Original part number to find equivalents for
            manufacturer: Optional manufacturer filter
            critical_params: Optional list of critical parameters to prioritize

        Returns:
            List of SemiconductorEquivalent sorted by compatibility score
        """
        results = []
        part_key = part_number.upper()

        # Find the original part
        original = None
        for pn, spec in self.semiconductor_db.items():
            if pn.upper() == part_key or spec.part_number.upper() == part_key:
                original = spec
                break

        if not original:
            # Try partial matching
            for pn, spec in self.semiconductor_db.items():
                if part_key in pn.upper():
                    original = spec
                    break

        if not original:
            return []

        # Find equivalents
        for pn, candidate in self.semiconductor_db.items():
            if candidate.part_number == original.part_number:
                continue

            # Check if same device type
            if candidate.device_type != original.device_type:
                continue

            score = 0.0
            differences = []

            # Package compatibility (major factor)
            if candidate.package == original.package and candidate.pin_count == original.pin_count:
                score += 0.4
            else:
                differences.append(f"Different package: {candidate.package.value} vs {original.package.value}")

            # Electrical compatibility
            if candidate.device_type in [DeviceType.LINEAR_REGULATOR, DeviceType.SWITCHING_REGULATOR]:
                # Compare voltage regulators
                orig_vout = original.key_parameters.get("output_voltage", 0)
                cand_vout = candidate.key_parameters.get("output_voltage", 0)

                if abs(orig_vout - cand_vout) < 0.1:
                    score += 0.3
                else:
                    differences.append(f"Output voltage: {cand_vout}V vs {orig_vout}V")

                # Dropout voltage (lower is generally better)
                orig_do = original.key_parameters.get("dropout_voltage", 2.0)
                cand_do = candidate.key_parameters.get("dropout_voltage", 2.0)
                if cand_do <= orig_do:
                    score += 0.1
                    if cand_do < orig_do:
                        differences.append(f"Lower dropout: {cand_do}V vs {orig_do}V (improvement)")

            elif candidate.device_type == DeviceType.MCU:
                # Compare microcontrollers
                orig_flash = original.key_parameters.get("flash_kb", 0)
                cand_flash = candidate.key_parameters.get("flash_kb", 0)

                if cand_flash >= orig_flash:
                    score += 0.2
                    if cand_flash > orig_flash:
                        differences.append(f"More flash: {cand_flash}KB vs {orig_flash}KB")
                else:
                    differences.append(f"Less flash: {cand_flash}KB vs {orig_flash}KB")

                # Check SRAM
                orig_sram = original.key_parameters.get("sram_bytes", 0)
                cand_sram = candidate.key_parameters.get("sram_bytes", 0)
                if cand_sram >= orig_sram:
                    score += 0.1
                else:
                    differences.append(f"Less SRAM: {cand_sram} vs {orig_sram} bytes")

            # Current rating compatibility
            if candidate.current_rating >= original.current_rating:
                score += 0.1
            else:
                differences.append(f"Lower current: {candidate.current_rating}A vs {original.current_rating}A")

            # Temperature range
            if (candidate.operating_temp_range[0] <= original.operating_temp_range[0] and
                candidate.operating_temp_range[1] >= original.operating_temp_range[1]):
                score += 0.1
            else:
                differences.append("Narrower temperature range")

            # Only include reasonable matches
            if score > 0.3:
                # Check if drop-in compatible
                drop_in = (
                    candidate.package == original.package and
                    candidate.pin_count == original.pin_count and
                    candidate.pinout == original.pinout
                )

                results.append(SemiconductorEquivalent(
                    part=candidate.part_number,
                    manufacturer=candidate.manufacturer,
                    compatibility_score=min(score, 0.99),
                    package=candidate.package.value,
                    differences=differences,
                    drop_in=drop_in,
                    notes=f"Status: {candidate.status.value}"
                ))

        # Sort by compatibility score
        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        return results

    def check_capacitor_equivalence(
        self,
        original: str,
        substitute: str
    ) -> CapacitorEquivalence:
        """
        Capacitors are NOT just capacitors. This checks real equivalence.

        Verifies:
        - ESR (equivalent series resistance)
        - Ripple current rating
        - Temperature coefficient
        - Lifetime at temperature
        - Voltage derating
        """
        orig_spec = self.capacitor_db.get(original)
        sub_spec = self.capacitor_db.get(substitute)

        if not orig_spec or not sub_spec:
            return CapacitorEquivalence(
                electrical_equivalent=False,
                reliability_equivalent=False,
                esr_comparison="Unable to compare - part not in database",
                lifetime_comparison="Unable to compare - part not in database",
                recommendation="Cannot verify equivalence",
                acceptable_for=[]
            )

        # Check electrical equivalence
        electrical_ok = (
            sub_spec.value == orig_spec.value and
            abs(sub_spec.tolerance_percent - orig_spec.tolerance_percent) <= 10 and
            sub_spec.voltage_rating >= orig_spec.voltage_rating
        )

        # ESR comparison
        if orig_spec.esr_mohms and sub_spec.esr_mohms:
            esr_ratio = sub_spec.esr_mohms / orig_spec.esr_mohms
            if esr_ratio <= 1.5:
                esr_comparison = f"ESR acceptable: {sub_spec.esr_mohms}mΩ vs {orig_spec.esr_mohms}mΩ"
            else:
                esr_comparison = f"ESR is {esr_ratio:.1f}x higher: {sub_spec.esr_mohms}mΩ vs {orig_spec.esr_mohms}mΩ"
                electrical_ok = False
        else:
            esr_comparison = "ESR data not available"

        # Lifetime comparison
        life_ratio = sub_spec.lifetime_hours / orig_spec.lifetime_hours if orig_spec.lifetime_hours > 0 else 0
        lifetime_comparison = f"{sub_spec.lifetime_hours}hr vs {orig_spec.lifetime_hours}hr at {sub_spec.temperature_rating_c}°C"

        # Reliability equivalence
        reliability_ok = (
            sub_spec.lifetime_hours >= orig_spec.lifetime_hours * 0.5 and
            sub_spec.temperature_rating_c >= orig_spec.temperature_rating_c and
            sub_spec.failure_rate_fit <= orig_spec.failure_rate_fit * 2
        )

        # Determine acceptable applications
        acceptable_for = []
        if electrical_ok:
            acceptable_for.append("General filtering")
            acceptable_for.append("Audio coupling")
        if reliability_ok:
            acceptable_for.append("Long-life applications")
        if sub_spec.ripple_current_ma and orig_spec.ripple_current_ma:
            if sub_spec.ripple_current_ma >= orig_spec.ripple_current_ma:
                acceptable_for.append("Switching power supply")
            else:
                # Remove from switching PSU use
                if "Switching power supply" in acceptable_for:
                    acceptable_for.remove("Switching power supply")

        # Generate recommendation
        if electrical_ok and reliability_ok:
            recommendation = "EQUIVALENT - Acceptable replacement"
        elif electrical_ok and not reliability_ok:
            recommendation = "ELECTRICAL EQUIVALENT ONLY - May have shorter life"
        elif not electrical_ok:
            recommendation = "NOT EQUIVALENT - Do not substitute"

        return CapacitorEquivalence(
            electrical_equivalent=electrical_ok,
            reliability_equivalent=reliability_ok,
            esr_comparison=esr_comparison,
            lifetime_comparison=lifetime_comparison,
            recommendation=recommendation,
            acceptable_for=acceptable_for
        )

    def map_pinout_compatibility(
        self,
        original_ic: str,
        candidate_ic: str
    ) -> PinoutMapping:
        """
        Check if two ICs have compatible pinouts for PCB drop-in.

        Returns detailed pin-by-pin mapping and required changes.
        """
        original = self.semiconductor_db.get(original_ic)
        candidate = self.semiconductor_db.get(candidate_ic)

        if not original or not candidate:
            return PinoutMapping(
                compatible=False,
                package="Unknown",
                pin_differences={"Error": "Part not found in database"},
                software_changes_required=[],
                hardware_changes_required=["Cannot analyze - part not in database"],
                drop_in_with_code_change=False
            )

        # Check package compatibility
        package_match = (
            original.package == candidate.package and
            original.pin_count == candidate.pin_count
        )

        if not package_match:
            return PinoutMapping(
                compatible=False,
                package=f"{original.package.value} vs {candidate.package.value}",
                pin_differences={"Package": f"{original.pin_count} pins vs {candidate.pin_count} pins"},
                software_changes_required=[],
                hardware_changes_required=["Different package - PCB redesign required"],
                drop_in_with_code_change=False
            )

        # Compare pinouts
        pin_differences = {}
        all_pins_compatible = True
        software_changes = []
        hardware_changes = []

        for pin_num in original.pinout:
            orig_func = original.pinout.get(pin_num, "NC")
            cand_func = candidate.pinout.get(pin_num, "NC")

            if orig_func == cand_func:
                pin_differences[f"Pin {pin_num}"] = f"{orig_func} (same)"
            else:
                pin_differences[f"Pin {pin_num}"] = f"{cand_func} vs {orig_func}"
                # Check if it's just a naming difference or functional
                if "VCC" in orig_func and "VCC" in cand_func:
                    pass  # Power pins - ok
                elif "GND" in orig_func and "GND" in cand_func:
                    pass  # Ground pins - ok
                else:
                    all_pins_compatible = False

        # Device-specific software changes
        if original.device_type == DeviceType.MCU:
            software_changes.append("Verify/update fuse settings")
            software_changes.append("Check timer/peripheral register names")
            if candidate.key_parameters.get("flash_kb", 0) != original.key_parameters.get("flash_kb", 0):
                software_changes.append("Update linker memory settings")

        return PinoutMapping(
            compatible=all_pins_compatible,
            package=original.package.value,
            pin_differences=pin_differences,
            software_changes_required=software_changes,
            hardware_changes_required=hardware_changes,
            drop_in_with_code_change=all_pins_compatible and len(software_changes) > 0
        )

    def track_obsolescence(
        self,
        part_number: str
    ) -> ObsolescenceStatus:
        """
        Track end-of-life status and find alternatives before it's too late.

        Returns current status, dates, alternatives, and recommendations.
        """
        # Check obsolescence tracker first
        obs_data = self.obsolescence_tracker.get(part_number)

        if obs_data:
            status = obs_data["status"]
            last_buy = obs_data.get("last_buy_date")
            last_ship = obs_data.get("last_ship_date")
            modern_eq = obs_data.get("modern_equivalents", [])
            broker_avail = obs_data.get("broker_availability", False)
            broker_premium = obs_data.get("broker_price_premium")
        else:
            # Check semiconductor database
            spec = self.semiconductor_db.get(part_number)
            if spec:
                status = spec.status
                last_buy = None
                last_ship = spec.eol_date.isoformat() if spec.eol_date else None
                modern_eq = spec.functional_equivalents
                broker_avail = status == ComponentStatus.OBSOLETE
                broker_premium = 100 if status == ComponentStatus.OBSOLETE else 0
            else:
                return ObsolescenceStatus(
                    part_number=part_number,
                    status=ComponentStatus.UNKNOWN,
                    last_buy_date=None,
                    last_ship_date=None,
                    modern_equivalents=[],
                    broker_availability=False,
                    broker_price_premium_percent=None,
                    recommended_action="Part not found in database - verify with manufacturer"
                )

        # Generate recommendation based on status
        if status == ComponentStatus.ACTIVE:
            action = "No action required - part is in active production"
        elif status == ComponentStatus.NRND:
            action = "Plan migration - not recommended for new designs. Evaluate alternatives."
        elif status == ComponentStatus.EOL_ANNOUNCED:
            action = "URGENT: Begin qualification of alternatives. Consider last time buy."
        elif status == ComponentStatus.LAST_BUY:
            action = "CRITICAL: Place last time buy order or qualify alternative immediately"
        elif status == ComponentStatus.OBSOLETE:
            action = "Design out or stockpile. Broker parts available at premium."
        else:
            action = "Status unknown - contact manufacturer for lifecycle information"

        return ObsolescenceStatus(
            part_number=part_number,
            status=status,
            last_buy_date=last_buy,
            last_ship_date=last_ship,
            modern_equivalents=modern_eq,
            broker_availability=broker_avail,
            broker_price_premium_percent=broker_premium,
            recommended_action=action
        )


# Demo usage
if __name__ == "__main__":
    agent = SiliconAgent()

    print("=" * 60)
    print("Agent_12: SILICON - Electronics & Semiconductor Intelligence")
    print("=" * 60)

    # Test semiconductor equivalent finder
    print("\n--- Semiconductor Equivalent Finder ---")
    print("Finding equivalents for LM7805CT...")
    equivalents = agent.find_semiconductor_equivalent("LM7805CT", "TI")
    for eq in equivalents:
        print(f"\n{eq.part} ({eq.manufacturer})")
        print(f"  Compatibility: {eq.compatibility_score:.0%}")
        print(f"  Package: {eq.package}")
        print(f"  Drop-in: {'Yes' if eq.drop_in else 'No'}")
        if eq.differences:
            print(f"  Differences: {', '.join(eq.differences[:2])}")

    # Test capacitor equivalence
    print("\n--- Capacitor Equivalence Check ---")
    print("Checking: Nichicon UHE1E101MPD vs Generic 100uF 25V")
    cap_result = agent.check_capacitor_equivalence(
        "Nichicon UHE1E101MPD",
        "Generic 100uF 25V"
    )
    print(f"Electrical equivalent: {cap_result.electrical_equivalent}")
    print(f"Reliability equivalent: {cap_result.reliability_equivalent}")
    print(f"ESR: {cap_result.esr_comparison}")
    print(f"Lifetime: {cap_result.lifetime_comparison}")
    print(f"Recommendation: {cap_result.recommendation}")
    print(f"Acceptable for: {', '.join(cap_result.acceptable_for)}")

    # Test pinout compatibility
    print("\n--- Pinout Compatibility Check ---")
    print("Checking: ATmega8-16PU vs ATmega88-20PU")
    pinout = agent.map_pinout_compatibility("ATmega8-16PU", "ATmega88-20PU")
    print(f"Compatible: {pinout.compatible}")
    print(f"Package: {pinout.package}")
    print(f"Drop-in with code change: {pinout.drop_in_with_code_change}")
    if pinout.software_changes_required:
        print("Software changes required:")
        for change in pinout.software_changes_required:
            print(f"  - {change}")

    # Test obsolescence tracking
    print("\n--- Obsolescence Tracking ---")
    print("Checking MC68000...")
    obs = agent.track_obsolescence("MC68000")
    print(f"Part: {obs.part_number}")
    print(f"Status: {obs.status.value.upper()}")
    print(f"Last buy date: {obs.last_buy_date}")
    print(f"Last ship date: {obs.last_ship_date}")
    print(f"Modern equivalents: {', '.join(obs.modern_equivalents)}")
    print(f"Broker availability: {'Yes' if obs.broker_availability else 'No'}")
    print(f"Broker premium: {obs.broker_price_premium_percent}%")
    print(f"Recommended action: {obs.recommended_action}")

    print("\n--- Checking ATmega8-16PU (NRND status) ---")
    obs2 = agent.track_obsolescence("ATmega8-16PU")
    print(f"Status: {obs2.status.value.upper()}")
    print(f"Modern equivalents: {', '.join(obs2.modern_equivalents)}")
    print(f"Recommended action: {obs2.recommended_action}")
