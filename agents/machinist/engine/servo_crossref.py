"""
Servo Drive Cross-Reference Engine - Match servo drives across manufacturers

Handles:
- Fanuc (Alpha, Beta, AC servo series)
- Yaskawa (Sigma series)
- Mitsubishi (MR-J series)
- Siemens (Simodrive, S120)
- Bosch Rexroth (IndraDrive)
- Delta (ASDA series)
- Panasonic (MINAS series)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class DriveType(Enum):
    """Servo drive types"""
    AC_SERVO = "ac_servo"
    DC_SERVO = "dc_servo"
    STEPPER = "stepper"
    VFD = "vfd"
    SPINDLE = "spindle"


class EncoderInterface(Enum):
    """Encoder interface types"""
    INCREMENTAL_ABZ = "incremental_abz"        # A/B quadrature + Z
    ABSOLUTE_SSI = "absolute_ssi"              # Synchronous Serial Interface
    ABSOLUTE_BISS = "absolute_biss"            # BiSS-C protocol
    ABSOLUTE_ENDAT = "absolute_endat"          # Heidenhain EnDat
    RESOLVER = "resolver"                       # Analog resolver
    SERIAL_FANUC = "serial_fanuc"              # Fanuc proprietary
    SERIAL_YASKAWA = "serial_yaskawa"          # Yaskawa proprietary
    SERIAL_MITSUBISHI = "serial_mitsubishi"    # Mitsubishi proprietary
    HIPERFACE = "hiperface"                    # Sick Stegmann


class CommunicationProtocol(Enum):
    """Drive communication protocols"""
    ANALOG_VELOCITY = "analog_velocity"        # +/-10V
    ANALOG_TORQUE = "analog_torque"            # +/-10V
    PULSE_DIRECTION = "pulse_direction"        # Step/Dir
    CANOPEN = "canopen"
    PROFIBUS = "profibus"
    PROFINET = "profinet"
    ETHERCAT = "ethercat"
    ETHERNET_IP = "ethernet_ip"
    MECHATROLINK = "mechatrolink"              # Yaskawa
    SSCNET = "sscnet"                          # Mitsubishi
    FSSB = "fssb"                              # Fanuc Serial Servo Bus


@dataclass
class ServoDriveSpec:
    """Complete servo drive specification"""
    manufacturer: str
    model: str
    series: str
    drive_type: DriveType

    # Power specifications
    continuous_power_kw: float
    peak_power_kw: float
    input_voltage: int                         # AC voltage
    input_phases: int                          # 1 or 3 phase

    # Current specifications
    continuous_current_a: float
    peak_current_a: float

    # Interface
    encoder_interfaces: List[EncoderInterface]
    communication_protocols: List[CommunicationProtocol]

    # Physical
    width_mm: float
    height_mm: float
    depth_mm: float

    # Features
    regenerative_braking: bool
    safety_torque_off: bool
    multi_axis_capable: bool

    # Lifecycle
    status: str                               # "Active", "Mature", "Obsolete"
    year_introduced: int
    replacement_model: Optional[str]


@dataclass
class CrossReferenceMatch:
    """Cross-reference match result"""
    original_drive: str
    replacement_drive: str
    manufacturer: str
    compatibility_score: float                # 0.0 to 1.0

    # Match details
    power_match: str                          # "Exact", "Larger", "Smaller"
    voltage_match: bool
    encoder_adapter_needed: bool
    encoder_adapter_part: Optional[str]
    communication_match: str

    # Wiring
    wiring_changes: List[str]
    connector_adapters: List[str]

    # Parameters
    parameter_mapping_available: bool
    parameter_file: Optional[str]

    # Cost
    price_ratio: float                        # New price / Original price
    estimated_price_usd: float

    notes: str


class ServoCrossReferenceEngine:
    """
    Engine for cross-referencing servo drives across manufacturers

    Key capabilities:
    - Power/voltage matching
    - Encoder interface compatibility
    - Communication protocol mapping
    - Wiring change documentation
    - Parameter conversion guidance
    """

    def __init__(self):
        self.drives = self._initialize_drives()
        self.encoder_adapters = self._initialize_encoder_adapters()
        self.parameter_maps = self._initialize_parameter_maps()

    def _initialize_drives(self) -> Dict[str, ServoDriveSpec]:
        """Initialize servo drive database"""
        return {
            # Fanuc Alpha series
            "fanuc_a06b-6079-h104": ServoDriveSpec(
                manufacturer="Fanuc",
                model="A06B-6079-H104",
                series="Alpha",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=2.0,
                peak_power_kw=4.0,
                input_voltage=200,
                input_phases=3,
                continuous_current_a=10,
                peak_current_a=20,
                encoder_interfaces=[EncoderInterface.SERIAL_FANUC],
                communication_protocols=[CommunicationProtocol.FSSB],
                width_mm=50,
                height_mm=300,
                depth_mm=230,
                regenerative_braking=True,
                safety_torque_off=False,
                multi_axis_capable=True,
                status="Mature",
                year_introduced=2000,
                replacement_model="A06B-6240-H104"
            ),
            "fanuc_a06b-6079-h106": ServoDriveSpec(
                manufacturer="Fanuc",
                model="A06B-6079-H106",
                series="Alpha",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=3.7,
                peak_power_kw=7.4,
                input_voltage=200,
                input_phases=3,
                continuous_current_a=18,
                peak_current_a=36,
                encoder_interfaces=[EncoderInterface.SERIAL_FANUC],
                communication_protocols=[CommunicationProtocol.FSSB],
                width_mm=50,
                height_mm=300,
                depth_mm=230,
                regenerative_braking=True,
                safety_torque_off=False,
                multi_axis_capable=True,
                status="Mature",
                year_introduced=2000,
                replacement_model="A06B-6240-H106"
            ),

            # Yaskawa Sigma-5 series
            "yaskawa_sgdv-2r8a11a": ServoDriveSpec(
                manufacturer="Yaskawa",
                model="SGDV-2R8A11A",
                series="Sigma-5",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=3.0,
                peak_power_kw=6.0,
                input_voltage=200,
                input_phases=1,  # Single phase option
                continuous_current_a=14,
                peak_current_a=28,
                encoder_interfaces=[EncoderInterface.SERIAL_YASKAWA, EncoderInterface.INCREMENTAL_ABZ],
                communication_protocols=[CommunicationProtocol.MECHATROLINK, CommunicationProtocol.ANALOG_VELOCITY],
                width_mm=70,
                height_mm=220,
                depth_mm=173,
                regenerative_braking=True,
                safety_torque_off=True,
                multi_axis_capable=False,
                status="Mature",
                year_introduced=2007,
                replacement_model="SGD7S"
            ),
            "yaskawa_sgdv-5r5a11a": ServoDriveSpec(
                manufacturer="Yaskawa",
                model="SGDV-5R5A11A",
                series="Sigma-5",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=5.5,
                peak_power_kw=11.0,
                input_voltage=200,
                input_phases=3,
                continuous_current_a=26,
                peak_current_a=52,
                encoder_interfaces=[EncoderInterface.SERIAL_YASKAWA, EncoderInterface.INCREMENTAL_ABZ],
                communication_protocols=[CommunicationProtocol.MECHATROLINK, CommunicationProtocol.ANALOG_VELOCITY],
                width_mm=90,
                height_mm=250,
                depth_mm=186,
                regenerative_braking=True,
                safety_torque_off=True,
                multi_axis_capable=False,
                status="Active",
                year_introduced=2007,
                replacement_model=None
            ),

            # Mitsubishi MR-J4 series
            "mitsubishi_mr-j4-40a": ServoDriveSpec(
                manufacturer="Mitsubishi",
                model="MR-J4-40A",
                series="MR-J4",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=4.0,
                peak_power_kw=8.0,
                input_voltage=200,
                input_phases=3,
                continuous_current_a=19,
                peak_current_a=38,
                encoder_interfaces=[EncoderInterface.SERIAL_MITSUBISHI, EncoderInterface.INCREMENTAL_ABZ],
                communication_protocols=[CommunicationProtocol.SSCNET, CommunicationProtocol.PULSE_DIRECTION],
                width_mm=80,
                height_mm=215,
                depth_mm=166,
                regenerative_braking=True,
                safety_torque_off=True,
                multi_axis_capable=False,
                status="Active",
                year_introduced=2013,
                replacement_model=None
            ),

            # Siemens Simodrive 611
            "siemens_6sn1123-1aa00-0ca2": ServoDriveSpec(
                manufacturer="Siemens",
                model="6SN1123-1AA00-0CA2",
                series="Simodrive 611",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=5.0,
                peak_power_kw=10.0,
                input_voltage=400,
                input_phases=3,
                continuous_current_a=12,
                peak_current_a=24,
                encoder_interfaces=[EncoderInterface.ABSOLUTE_ENDAT, EncoderInterface.RESOLVER],
                communication_protocols=[CommunicationProtocol.PROFIBUS],
                width_mm=100,
                height_mm=340,
                depth_mm=220,
                regenerative_braking=True,
                safety_torque_off=False,
                multi_axis_capable=True,
                status="Mature",
                year_introduced=1998,
                replacement_model="Sinamics S120"
            ),

            # Delta ASDA series
            "delta_asd-a2-0421-m": ServoDriveSpec(
                manufacturer="Delta",
                model="ASD-A2-0421-M",
                series="ASDA-A2",
                drive_type=DriveType.AC_SERVO,
                continuous_power_kw=0.4,
                peak_power_kw=1.2,
                input_voltage=200,
                input_phases=1,
                continuous_current_a=2.5,
                peak_current_a=7.5,
                encoder_interfaces=[EncoderInterface.INCREMENTAL_ABZ, EncoderInterface.ABSOLUTE_BISS],
                communication_protocols=[CommunicationProtocol.PULSE_DIRECTION, CommunicationProtocol.CANOPEN],
                width_mm=60,
                height_mm=170,
                depth_mm=155,
                regenerative_braking=False,
                safety_torque_off=False,
                multi_axis_capable=False,
                status="Active",
                year_introduced=2012,
                replacement_model=None
            ),
        }

    def _initialize_encoder_adapters(self) -> Dict[str, Dict]:
        """Initialize encoder adapter database"""
        return {
            "fanuc_to_incremental": {
                "source": EncoderInterface.SERIAL_FANUC,
                "target": EncoderInterface.INCREMENTAL_ABZ,
                "adapter_part": "Custom converter required",
                "notes": "Fanuc serial encoders cannot be directly converted"
            },
            "endat_to_biss": {
                "source": EncoderInterface.ABSOLUTE_ENDAT,
                "target": EncoderInterface.ABSOLUTE_BISS,
                "adapter_part": "HEIDENHAIN EIB-392",
                "notes": "Signal converter available"
            },
            "resolver_to_incremental": {
                "source": EncoderInterface.RESOLVER,
                "target": EncoderInterface.INCREMENTAL_ABZ,
                "adapter_part": "Various RDC chips",
                "notes": "Resolver-to-digital converter required"
            },
        }

    def _initialize_parameter_maps(self) -> Dict[str, str]:
        """Initialize parameter mapping files"""
        return {
            "fanuc_to_yaskawa": "Fanuc Alpha -> Yaskawa Sigma-5 parameter map available",
            "siemens_to_bosch": "Simodrive 611 -> IndraDrive parameter map available",
            "mitsubishi_to_yaskawa": "MR-J4 -> Sigma-5 similar architecture, basic map available",
        }

    def find_cross_reference(
        self,
        original_drive: str,
        target_manufacturer: Optional[str] = None,
        motor_power_kw: Optional[float] = None,
        motor_voltage: Optional[int] = None
    ) -> List[CrossReferenceMatch]:
        """
        Find cross-reference matches for a servo drive.

        Args:
            original_drive: Original drive model/part number
            target_manufacturer: Optional preferred manufacturer
            motor_power_kw: Motor power for verification
            motor_voltage: Motor voltage for verification

        Returns:
            List of cross-reference matches sorted by compatibility
        """
        # Find original drive in database
        original_spec = None
        original_key = original_drive.lower().replace(" ", "-").replace("_", "-")

        for key, spec in self.drives.items():
            if original_key in key or spec.model.lower().replace(" ", "-") == original_key:
                original_spec = spec
                break

        if not original_spec:
            return []

        results = []

        for key, candidate in self.drives.items():
            # Skip same drive
            if candidate.model == original_spec.model:
                continue

            # Filter by manufacturer if specified
            if target_manufacturer and candidate.manufacturer.lower() != target_manufacturer.lower():
                continue

            # Calculate compatibility score
            score = self._calculate_compatibility(original_spec, candidate, motor_power_kw, motor_voltage)

            if score > 0.5:  # Only include reasonable matches
                match = self._create_match(original_spec, candidate, score)
                results.append(match)

        # Sort by compatibility score
        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        return results

    def _calculate_compatibility(
        self,
        original: ServoDriveSpec,
        candidate: ServoDriveSpec,
        motor_power_kw: Optional[float],
        motor_voltage: Optional[int]
    ) -> float:
        """Calculate compatibility score between two drives"""
        score = 0.5  # Base score

        # Power compatibility (±20% is acceptable)
        power_ratio = candidate.continuous_power_kw / original.continuous_power_kw
        if 0.8 <= power_ratio <= 1.2:
            score += 0.2
        elif 0.6 <= power_ratio <= 1.5:
            score += 0.1
        else:
            score -= 0.1

        # Voltage compatibility
        if candidate.input_voltage == original.input_voltage:
            score += 0.15
        elif abs(candidate.input_voltage - original.input_voltage) <= 30:
            score += 0.05

        # Encoder compatibility
        encoder_overlap = set(original.encoder_interfaces) & set(candidate.encoder_interfaces)
        if encoder_overlap:
            score += 0.1

        # Communication compatibility
        comm_overlap = set(original.communication_protocols) & set(candidate.communication_protocols)
        if comm_overlap:
            score += 0.05

        # Same manufacturer bonus
        if candidate.manufacturer == original.manufacturer:
            score += 0.1

        return min(1.0, max(0.0, score))

    def _create_match(
        self,
        original: ServoDriveSpec,
        candidate: ServoDriveSpec,
        score: float
    ) -> CrossReferenceMatch:
        """Create a cross-reference match object"""
        # Determine power match type
        if candidate.continuous_power_kw > original.continuous_power_kw * 1.1:
            power_match = "Larger"
        elif candidate.continuous_power_kw < original.continuous_power_kw * 0.9:
            power_match = "Smaller"
        else:
            power_match = "Exact"

        # Check encoder adapter needs
        original_encoders = set(original.encoder_interfaces)
        candidate_encoders = set(candidate.encoder_interfaces)
        encoder_adapter_needed = not bool(original_encoders & candidate_encoders)

        # Communication match
        original_comms = set(original.communication_protocols)
        candidate_comms = set(candidate.communication_protocols)
        if original_comms & candidate_comms:
            comm_match = "Compatible"
        elif CommunicationProtocol.ANALOG_VELOCITY in candidate_comms:
            comm_match = "Analog fallback available"
        else:
            comm_match = "Adapter required"

        # Estimate price (rough estimates)
        price_estimates = {
            "Fanuc": 2500,
            "Yaskawa": 1500,
            "Mitsubishi": 1400,
            "Siemens": 2000,
            "Delta": 600,
        }
        estimated_price = price_estimates.get(candidate.manufacturer, 1500)
        original_price = price_estimates.get(original.manufacturer, 2000)

        # Wiring changes
        wiring_changes = []
        if candidate.input_voltage != original.input_voltage:
            wiring_changes.append(f"Input voltage change: {original.input_voltage}V -> {candidate.input_voltage}V")
        if candidate.input_phases != original.input_phases:
            wiring_changes.append(f"Phase change: {original.input_phases}ph -> {candidate.input_phases}ph")
        wiring_changes.append("Motor power wiring may require different connector")
        wiring_changes.append("Encoder wiring reconfiguration required")

        return CrossReferenceMatch(
            original_drive=original.model,
            replacement_drive=candidate.model,
            manufacturer=candidate.manufacturer,
            compatibility_score=score,
            power_match=power_match,
            voltage_match=candidate.input_voltage == original.input_voltage,
            encoder_adapter_needed=encoder_adapter_needed,
            encoder_adapter_part=None if not encoder_adapter_needed else "See encoder adapter guide",
            communication_match=comm_match,
            wiring_changes=wiring_changes,
            connector_adapters=[],
            parameter_mapping_available=score > 0.8,
            parameter_file=None,
            price_ratio=estimated_price / original_price,
            estimated_price_usd=estimated_price,
            notes=f"Cross-reference from {original.manufacturer} {original.series} to {candidate.manufacturer} {candidate.series}"
        )

    def get_drive_spec(self, model: str) -> Optional[ServoDriveSpec]:
        """Get detailed specification for a drive model"""
        model_key = model.lower().replace(" ", "-").replace("_", "-")

        for key, spec in self.drives.items():
            if model_key in key or spec.model.lower().replace(" ", "-") == model_key:
                return spec

        return None

    def list_drives_by_power(
        self,
        min_power_kw: float,
        max_power_kw: float,
        manufacturer: Optional[str] = None
    ) -> List[ServoDriveSpec]:
        """List drives within a power range"""
        results = []

        for spec in self.drives.values():
            if min_power_kw <= spec.continuous_power_kw <= max_power_kw:
                if not manufacturer or spec.manufacturer.lower() == manufacturer.lower():
                    results.append(spec)

        return sorted(results, key=lambda x: x.continuous_power_kw)
