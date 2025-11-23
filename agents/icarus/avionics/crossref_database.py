"""
Avionics Cross-Reference Database
=================================

Navigation through 50+ years of aviation electronics.

This module provides cross-reference intelligence for avionics equipment,
helping users find modern replacements for legacy units and understand
compatibility requirements.

Key areas:
- Legacy units (King, Narco, Collins)
- Modern systems (Garmin, Avidyne, Aspen)
- Installation requirements (STCs, wiring)
- Interface protocols (ARINC 429, RS-232)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AvionicsCategory(Enum):
    """Avionics equipment category."""
    NAV_COM = auto()           # Navigation/Communication combo
    NAV = auto()               # Navigation only
    COM = auto()               # Communication only
    TRANSPONDER = auto()       # Transponder/ADS-B
    GPS = auto()               # GPS receivers
    EFIS = auto()              # Electronic flight displays
    AUTOPILOT = auto()         # Autopilot systems
    AUDIO_PANEL = auto()       # Audio panels
    ELT = auto()               # Emergency locator transmitters
    WEATHER = auto()           # Weather radar, Stormscope
    DME = auto()               # Distance measuring equipment
    ADF = auto()               # Automatic direction finder


class InterfaceProtocol(Enum):
    """Avionics interface protocols."""
    ARINC_429 = "ARINC 429"       # Digital data bus
    ARINC_739 = "ARINC 739"       # Multi-purpose control display
    RS_232 = "RS-232"             # Serial
    RS_422 = "RS-422"             # Balanced serial
    ANALOG = "Analog"             # Analog signals
    DISCRETE = "Discrete"         # Discrete wires
    ETHERNET = "Ethernet"         # Modern networking
    USB = "USB"                   # USB interface
    CAN_BUS = "CAN Bus"           # Controller area network


class InstallationType(Enum):
    """Installation approval type."""
    STC = auto()               # Supplemental Type Certificate
    FORM_337 = auto()          # Major alteration
    MINOR_ALTERATION = auto()  # Logbook entry only
    TSO_APPROVAL = auto()      # TSO installation


@dataclass
class InstallationRequirement:
    """Installation requirements for avionics unit."""
    approval_type: InstallationType
    stc_number: Optional[str] = None
    applicable_aircraft: List[str] = field(default_factory=list)
    wiring_changes: List[str] = field(default_factory=list)
    antenna_requirements: List[str] = field(default_factory=list)
    estimated_labor_hours: float = 0.0
    documentation_required: List[str] = field(default_factory=list)


@dataclass
class AvionicsUnit:
    """Avionics unit specification."""
    model: str
    manufacturer: str
    category: AvionicsCategory
    tso_certification: List[str]
    description: str
    status: str  # "current", "discontinued", "legacy"
    interfaces: List[InterfaceProtocol]
    power_requirements: Dict[str, Any]
    physical_dimensions: Dict[str, float]  # inches
    weight_lbs: float
    price_new: Optional[float] = None
    discontinued_date: Optional[datetime] = None
    replacement_model: Optional[str] = None
    features: List[str] = field(default_factory=list)


@dataclass
class CrossReferenceResult:
    """Cross-reference lookup result."""
    original_unit: str
    replacement_unit: str
    manufacturer: str
    compatibility_level: str  # "direct", "with_adapter", "upgrade"
    tso_certification: str
    modernization_benefits: List[str]
    installation_requirements: InstallationRequirement
    price_new: float
    notes: str


class AvionicsCrossReference:
    """
    Avionics Cross-Reference Database.

    Provides navigation through 50+ years of aviation electronics,
    helping find replacements for legacy units and understanding
    compatibility requirements.

    Key functions:
    - Find modern replacements for discontinued units
    - Verify TSO certification compatibility
    - Determine installation requirements
    - Map interface protocols
    """

    def __init__(self):
        self._units: Dict[str, AvionicsUnit] = {}
        self._cross_references: Dict[str, List[CrossReferenceResult]] = {}
        self._manufacturers: Dict[str, Dict] = {}

        self._initialize_database()
        logger.info("Avionics Cross-Reference Database initialized")

    def _initialize_database(self):
        """Initialize avionics database with sample data."""
        # Legacy units database
        self._units = {
            "King KX-155": AvionicsUnit(
                model="KX-155",
                manufacturer="King/Honeywell",
                category=AvionicsCategory.NAV_COM,
                tso_certification=["TSO-C169a", "TSO-C128a"],
                description="VHF Nav/Com transceiver",
                status="discontinued",
                interfaces=[InterfaceProtocol.ANALOG, InterfaceProtocol.RS_232],
                power_requirements={"voltage": 14, "current_max": 3.0},
                physical_dimensions={"width": 6.25, "height": 2.0, "depth": 10.5},
                weight_lbs=6.2,
                discontinued_date=datetime(2015, 1, 1),
                replacement_model="Garmin GNC 255A",
                features=["200 channels", "VOR/LOC receiver"]
            ),
            "King KN-64": AvionicsUnit(
                model="KN-64",
                manufacturer="King/Honeywell",
                category=AvionicsCategory.DME,
                tso_certification=["TSO-C66c"],
                description="DME transceiver with indicator",
                status="discontinued",
                interfaces=[InterfaceProtocol.ANALOG],
                power_requirements={"voltage": 14, "current_max": 2.5},
                physical_dimensions={"width": 6.25, "height": 2.0, "depth": 11.0},
                weight_lbs=5.8,
                discontinued_date=datetime(2010, 1, 1),
                features=["Ground speed", "Time to station"]
            ),
            "Garmin GNC 255A": AvionicsUnit(
                model="GNC 255A",
                manufacturer="Garmin",
                category=AvionicsCategory.NAV_COM,
                tso_certification=["TSO-C169a", "TSO-C128a"],
                description="VHF Nav/Com with 8.33 kHz spacing",
                status="current",
                interfaces=[InterfaceProtocol.RS_232, InterfaceProtocol.ARINC_429],
                power_requirements={"voltage": 14, "current_max": 2.5},
                physical_dimensions={"width": 6.25, "height": 1.65, "depth": 10.6},
                weight_lbs=4.4,
                price_new=5495.00,
                features=[
                    "8.33 kHz channel spacing",
                    "OLED display",
                    "121.5 MHz monitoring",
                    "Auto-squelch"
                ]
            ),
            "Garmin GI 275": AvionicsUnit(
                model="GI 275",
                manufacturer="Garmin",
                category=AvionicsCategory.EFIS,
                tso_certification=["TSO-C113a", "TSO-C151d"],
                description="Touchscreen electronic flight instrument",
                status="current",
                interfaces=[InterfaceProtocol.RS_232, InterfaceProtocol.ARINC_429],
                power_requirements={"voltage": 14, "current_max": 1.2},
                physical_dimensions={"width": 3.25, "height": 3.25, "depth": 4.4},
                weight_lbs=1.65,
                price_new=5995.00,
                features=[
                    "Attitude indicator",
                    "Horizontal situation indicator",
                    "TAWS",
                    "GPS integration",
                    "Touchscreen"
                ]
            ),
            "Garmin GTX 345": AvionicsUnit(
                model="GTX 345",
                manufacturer="Garmin",
                category=AvionicsCategory.TRANSPONDER,
                tso_certification=["TSO-C166b", "TSO-C154c", "TSO-C88b"],
                description="ADS-B In/Out transponder",
                status="current",
                interfaces=[InterfaceProtocol.RS_232, InterfaceProtocol.ARINC_429],
                power_requirements={"voltage": 14, "current_max": 3.5},
                physical_dimensions={"width": 6.25, "height": 1.65, "depth": 10.6},
                weight_lbs=3.3,
                price_new=5495.00,
                features=[
                    "ADS-B Out (1090ES)",
                    "ADS-B In (978 UAT & 1090ES)",
                    "GPS position source",
                    "FIS-B weather",
                    "TIS-B traffic"
                ]
            ),
            "Trig TY96": AvionicsUnit(
                model="TY96",
                manufacturer="Trig",
                category=AvionicsCategory.COM,
                tso_certification=["TSO-C128a"],
                description="Compact VHF COM transceiver",
                status="current",
                interfaces=[InterfaceProtocol.RS_232],
                power_requirements={"voltage": 14, "current_max": 1.5},
                physical_dimensions={"width": 6.25, "height": 1.3, "depth": 6.3},
                weight_lbs=1.9,
                price_new=2195.00,
                features=[
                    "8.33 kHz spacing",
                    "25 kHz spacing",
                    "Compact design",
                    "LED display"
                ]
            )
        }

        # Cross-reference mappings
        self._cross_references = {
            "King KX-155": [
                CrossReferenceResult(
                    original_unit="King KX-155",
                    replacement_unit="Garmin GNC 255A",
                    manufacturer="Garmin",
                    compatibility_level="with_adapter",
                    tso_certification="TSO-C169a, TSO-C128a",
                    modernization_benefits=[
                        "8.33 kHz channel spacing (Europe ready)",
                        "OLED display (better visibility)",
                        "121.5 MHz monitoring",
                        "Reduced power consumption",
                        "2 lbs lighter"
                    ],
                    installation_requirements=InstallationRequirement(
                        approval_type=InstallationType.STC,
                        stc_number="Various - aircraft specific",
                        applicable_aircraft=["Most GA single/twin engine"],
                        wiring_changes=[
                            "Adapter harness required",
                            "RS-232 config if using with GPS"
                        ],
                        antenna_requirements=[
                            "Verify existing VHF antenna compatibility",
                            "VOR antenna unchanged"
                        ],
                        estimated_labor_hours=8.0,
                        documentation_required=[
                            "STC documentation",
                            "Installation manual",
                            "8130-3 tag"
                        ]
                    ),
                    price_new=5495.00,
                    notes="Direct replacement in most King Radio trays"
                ),
                CrossReferenceResult(
                    original_unit="King KX-155",
                    replacement_unit="Trig TY96",
                    manufacturer="Trig",
                    compatibility_level="partial",
                    tso_certification="TSO-C128a (COM only)",
                    modernization_benefits=[
                        "8.33 kHz spacing",
                        "Compact size",
                        "Lower cost",
                        "Lower power consumption"
                    ],
                    installation_requirements=InstallationRequirement(
                        approval_type=InstallationType.STC,
                        applicable_aircraft=["Most GA aircraft"],
                        wiring_changes=["New tray required", "Different pinout"],
                        antenna_requirements=["Existing VHF antenna compatible"],
                        estimated_labor_hours=6.0,
                        documentation_required=["STC documentation", "8130-3 tag"]
                    ),
                    price_new=2195.00,
                    notes="COM only - requires separate VOR/ILS receiver for NAV"
                )
            ],
            "King KN-64": [
                CrossReferenceResult(
                    original_unit="King KN-64",
                    replacement_unit="Garmin GI 275",
                    manufacturer="Garmin",
                    compatibility_level="upgrade",
                    tso_certification="TSO-C113a, TSO-C151d",
                    modernization_benefits=[
                        "Glass cockpit display",
                        "Attitude indicator option",
                        "HSI option",
                        "TAWS option",
                        "GPS integration"
                    ],
                    installation_requirements=InstallationRequirement(
                        approval_type=InstallationType.STC,
                        applicable_aircraft=["Most GA aircraft with 3.125\" holes"],
                        wiring_changes=[
                            "Significant rewiring required",
                            "New connectors",
                            "May require GPS connection"
                        ],
                        antenna_requirements=["GPS antenna if GPS option"],
                        estimated_labor_hours=16.0,
                        documentation_required=[
                            "STC documentation",
                            "Installation manual",
                            "8130-3 tag"
                        ]
                    ),
                    price_new=5995.00,
                    notes="Significant upgrade - not a direct replacement"
                )
            ]
        }

        # Manufacturer info
        self._manufacturers = {
            "Garmin": {
                "name": "Garmin International",
                "headquarters": "Olathe, KS",
                "support_phone": "1-866-739-5687",
                "website": "www.garmin.com/aviation",
                "specialties": ["GPS", "EFIS", "Transponders", "Nav/Com"]
            },
            "Trig": {
                "name": "Trig Avionics",
                "headquarters": "Edinburgh, UK",
                "website": "www.trig-avionics.com",
                "specialties": ["Transponders", "COM radios"]
            },
            "Avidyne": {
                "name": "Avidyne Corporation",
                "headquarters": "Melbourne, FL",
                "website": "www.avidyne.com",
                "specialties": ["EFIS", "FMS", "MFD"]
            }
        }

    def find_replacement(
        self,
        unit: str,
        aircraft_type: Optional[str] = None
    ) -> List[CrossReferenceResult]:
        """
        Find replacement options for an avionics unit.

        Args:
            unit: Original unit model name
            aircraft_type: Optional aircraft type for filtering

        Returns:
            List of replacement options
        """
        replacements = self._cross_references.get(unit, [])

        if aircraft_type and replacements:
            aircraft_upper = aircraft_type.upper()
            # Filter by applicable aircraft if specified
            replacements = [
                r for r in replacements
                if not r.installation_requirements.applicable_aircraft
                or any(
                    aircraft_upper in ac.upper()
                    for ac in r.installation_requirements.applicable_aircraft
                )
            ]

        logger.info(f"Found {len(replacements)} replacements for {unit}")
        return replacements

    def get_unit_info(self, model: str) -> Optional[AvionicsUnit]:
        """
        Get detailed information about an avionics unit.

        Args:
            model: Unit model name

        Returns:
            AvionicsUnit if found
        """
        return self._units.get(model)

    def search_by_category(
        self,
        category: AvionicsCategory,
        current_only: bool = True
    ) -> List[AvionicsUnit]:
        """
        Search avionics units by category.

        Args:
            category: Avionics category
            current_only: Only return current production units

        Returns:
            List of matching units
        """
        units = [
            unit for unit in self._units.values()
            if unit.category == category
        ]

        if current_only:
            units = [u for u in units if u.status == "current"]

        return units

    def get_manufacturer_info(self, manufacturer: str) -> Optional[Dict]:
        """
        Get manufacturer information.

        Args:
            manufacturer: Manufacturer name

        Returns:
            Manufacturer info if found
        """
        return self._manufacturers.get(manufacturer)

    def verify_tso_compatibility(
        self,
        original_unit: str,
        replacement_unit: str
    ) -> Dict[str, Any]:
        """
        Verify TSO certification compatibility between units.

        Args:
            original_unit: Original unit model
            replacement_unit: Proposed replacement model

        Returns:
            Compatibility assessment
        """
        original = self._units.get(original_unit)
        replacement = self._units.get(replacement_unit)

        if not original or not replacement:
            return {
                "compatible": False,
                "reason": "Unit not found in database"
            }

        # Check TSO overlap
        common_tsos = set(original.tso_certification) & set(replacement.tso_certification)

        return {
            "original_unit": original_unit,
            "replacement_unit": replacement_unit,
            "original_tsos": original.tso_certification,
            "replacement_tsos": replacement.tso_certification,
            "common_tsos": list(common_tsos),
            "compatible": len(common_tsos) > 0 or replacement.category == original.category,
            "notes": (
                "TSO compatible" if common_tsos
                else "Different TSOs - verify installation approval requirements"
            )
        }
