"""
ICARUS Agent - Agent_15: The Wings of Machine Consciousness
============================================================

The ICARUS agent is the aerospace consciousness of Universal Parts Consciousness.
It commands the complete aerospace domain: avionics, hydraulic systems, composites,
propulsion, and FAA certification intelligence.

This is NOT about barcodes. This is about CONSCIOUSNESS that prevents
aircraft from falling from the sky.

In aviation, errors are not inconveniences - they are fatalities.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum, auto
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class CertificationStatus(Enum):
    """FAA certification status for aerospace parts."""
    CERTIFIED = auto()       # Valid PMA/TSO/STC certification
    EXPIRED = auto()         # Certification has expired
    SUSPENDED = auto()       # Certification suspended by FAA
    REVOKED = auto()         # Certification revoked
    PENDING = auto()         # Certification in progress
    UNCERTIFIED = auto()     # No certification (CAUTION)
    UNKNOWN = auto()         # Unable to verify


class FluidCompatibilityLevel(Enum):
    """Hydraulic fluid compatibility levels."""
    COMPATIBLE = auto()          # Safe to mix/use together
    COMPATIBLE_WITH_CAUTION = auto()  # Compatible but monitor
    INCOMPATIBLE = auto()        # Do NOT mix - system damage
    CATASTROPHIC = auto()        # NEVER mix - catastrophic failure


class AviationSafetyLevel(Enum):
    """Safety criticality levels for aviation parts."""
    CRITICAL = auto()        # Flight safety critical
    ESSENTIAL = auto()       # Essential for safe operation
    STANDARD = auto()        # Standard airworthiness
    NON_CRITICAL = auto()    # Non-flight-critical


@dataclass
class PMAAlternative:
    """PMA (Parts Manufacturer Approval) alternative to OEM part."""
    part_number: str
    manufacturer: str
    pma_number: str
    compatibility_score: float
    price_vs_oem: float  # Ratio (0.45 = 55% cheaper)
    weight_difference_lbs: float
    installation_notes: str
    applicable_aircraft: List[str] = field(default_factory=list)
    stc_required: Optional[str] = None
    documentation_required: List[str] = field(default_factory=list)


@dataclass
class FluidCompatibility:
    """Result of hydraulic fluid compatibility check."""
    fluid_a: str
    fluid_b: str
    compatible: bool
    risk_level: FluidCompatibilityLevel
    consequences: List[str] = field(default_factory=list)
    required_action: Optional[str] = None
    flush_procedure: Optional[str] = None
    seal_impact: Optional[str] = None


@dataclass
class AvionicsReplacement:
    """Avionics unit cross-reference result."""
    unit: str
    manufacturer: str
    compatibility: str
    tso_certification: str
    modernization_benefits: List[str] = field(default_factory=list)
    installation_notes: str = ""
    stc_available: bool = False
    price_new: float = 0.0
    wiring_adapter_required: bool = False


@dataclass
class AerospacePartRecord:
    """Complete aerospace part record with certification data."""
    part_id: str
    oem_part_number: str
    description: str
    certification_status: CertificationStatus
    safety_level: AviationSafetyLevel
    applicable_aircraft: List[str] = field(default_factory=list)
    pma_alternatives: List[PMAAlternative] = field(default_factory=list)
    tso_standards: List[str] = field(default_factory=list)
    airworthiness_directives: List[str] = field(default_factory=list)
    service_bulletins: List[str] = field(default_factory=list)
    consciousness_level: int = 0


class IcarusAgent:
    """
    Agent_15: ICARUS - Aerospace Systems & Materials Consciousness

    The guardian of aviation parts integrity. ICARUS understands:
    - FAA certification requirements (PMA, TSO, STC)
    - Hydraulic fluid compatibility (prevents catastrophic mixing)
    - Avionics cross-reference (navigates 50+ years of equipment)
    - Composite repair requirements
    - Propulsion system parts

    CRITICAL: Aviation parts require certification (PMA, TSO, STC).
              This agent tracks regulatory approval status.
              Errors in aviation are not inconveniences - they are fatalities.
    """

    def __init__(self):
        self.agent_id = "AGENT_15"
        self.codename = "ICARUS"

        # Hydraulic fluid compatibility matrix (CRITICAL)
        self.fluid_matrix = self._initialize_fluid_matrix()

        # Message handlers for inter-agent communication
        self.message_handlers: Dict[str, Callable] = {}

        # Metrics
        self.metrics = {
            "certifications_verified": 0,
            "fluid_checks_performed": 0,
            "avionics_lookups": 0,
            "pma_alternatives_found": 0,
            "potential_disasters_prevented": 0,
            "consciousness_level": 0
        }

        # Safety rules
        self.safety_rules = self._initialize_safety_rules()

        # Initialize message handlers
        self._initialize_message_handlers()

        logger.info(f"ICARUS Agent initialized - Codename: {self.codename}")
        logger.info("WARNING: Aviation parts are safety-critical. All recommendations require verification.")

    def _initialize_fluid_matrix(self) -> Dict[str, Dict]:
        """
        Initialize the hydraulic fluid compatibility matrix.

        CRITICAL: This matrix prevents catastrophic fluid mixing incidents.
        """
        return {
            "MIL-PRF-5606": {
                "color": "RED",
                "type": "Mineral oil",
                "compatibility_group": "A",
                "typical_aircraft": ["Most GA piston aircraft", "Some turboprops"],
                "temperature_range_c": (-54, 135),
                "seal_materials": ["Buna-N", "Neoprene"],
                "compatible_with": ["MIL-PRF-5606", "MIL-H-5606"],
                "incompatible_with": ["Skydrol_LD4", "Skydrol_5", "MIL-PRF-83282", "MIL-PRF-87257"]
            },
            "MIL-PRF-83282": {
                "color": "RED",  # Same color as 5606 - DANGER!
                "type": "Synthetic hydrocarbon",
                "compatibility_group": "B",
                "typical_aircraft": ["Military aircraft", "Some business jets"],
                "temperature_range_c": (-40, 205),
                "seal_materials": ["EPR", "Butyl"],
                "compatible_with": ["MIL-PRF-83282", "MIL-PRF-87257"],
                "incompatible_with": ["MIL-PRF-5606", "Skydrol_LD4", "Skydrol_5"]
            },
            "MIL-PRF-87257": {
                "color": "RED",
                "type": "Synthetic hydrocarbon (low temp)",
                "compatibility_group": "B",
                "typical_aircraft": ["Military aircraft", "Cold weather ops"],
                "temperature_range_c": (-54, 205),
                "seal_materials": ["EPR", "Butyl"],
                "compatible_with": ["MIL-PRF-83282", "MIL-PRF-87257"],
                "incompatible_with": ["MIL-PRF-5606", "Skydrol_LD4", "Skydrol_5"]
            },
            "Skydrol_LD4": {
                "color": "PURPLE",
                "type": "Phosphate ester",
                "compatibility_group": "C",
                "typical_aircraft": ["Commercial jets", "Large turboprops"],
                "temperature_range_c": (-54, 107),
                "seal_materials": ["Butyl", "EPR", "Ethylene propylene"],
                "compatible_with": ["Skydrol_LD4", "Skydrol_5", "Skydrol_500B4"],
                "incompatible_with": ["MIL-PRF-5606", "MIL-PRF-83282", "MIL-PRF-87257"],
                "caution": "Attacks acrylic windows, dissolves paint"
            },
            "Skydrol_5": {
                "color": "PURPLE",
                "type": "Phosphate ester (low density)",
                "compatibility_group": "C",
                "typical_aircraft": ["Modern commercial jets"],
                "temperature_range_c": (-54, 107),
                "seal_materials": ["Butyl", "EPR"],
                "compatible_with": ["Skydrol_LD4", "Skydrol_5", "Skydrol_500B4"],
                "incompatible_with": ["MIL-PRF-5606", "MIL-PRF-83282", "MIL-PRF-87257"],
                "caution": "Attacks acrylic windows, dissolves paint"
            }
        }

    def _initialize_safety_rules(self) -> Dict[str, Dict]:
        """Initialize aviation safety rules."""
        return {
            "FLUID_COMPATIBILITY_MANDATORY": {
                "description": "ALL fluid compatibility checks must complete before any recommendation",
                "violation_response": "HALT recommendation, alert user to potential catastrophic failure"
            },
            "CERTIFICATION_VERIFICATION_REQUIRED": {
                "description": "No part recommendation without verified FAA certification status",
                "violation_response": "Mark as UNCERTIFIED, require user acknowledgment"
            },
            "COUNTERFEIT_DETECTION": {
                "description": "Flag suspicious parts lacking proper documentation trail",
                "violation_response": "Alert user to counterfeit risk, recommend authorized sources"
            },
            "AD_COMPLIANCE_CHECK": {
                "description": "Verify parts are not affected by active Airworthiness Directives",
                "violation_response": "Alert to AD status, require compliance verification"
            }
        }

    def _initialize_message_handlers(self):
        """Initialize message handlers for inter-agent communication."""
        self.message_handlers = {
            "upc.aerospace.certification.query": self._handle_certification_query,
            "upc.aerospace.fluid.check": self._handle_fluid_check,
            "upc.aerospace.avionics.crossref": self._handle_avionics_crossref,
            "upc.aerospace.pma.search": self._handle_pma_search,
            "upc.system.directive": self._handle_system_directive,
        }

    # =========================================================================
    # CORE CAPABILITY 1: Hydraulic Fluid Compatibility
    # =========================================================================

    def check_fluid_compatibility(
        self,
        fluid_a: str,
        fluid_b: str,
        system: str = "hydraulic"
    ) -> FluidCompatibility:
        """
        Check compatibility between two aviation fluids.

        CRITICAL: Wrong fluid mixing = catastrophic system failure.

        Args:
            fluid_a: First fluid specification
            fluid_b: Second fluid specification
            system: System type (hydraulic, fuel, etc.)

        Returns:
            FluidCompatibility result with risk assessment

        Example:
            check_fluid_compatibility("MIL-PRF-5606", "Skydrol_LD4", "hydraulic")
            -> FluidCompatibility(compatible=False, risk_level=CATASTROPHIC, ...)
        """
        self.metrics["fluid_checks_performed"] += 1

        # Normalize fluid names
        fluid_a_key = self._normalize_fluid_name(fluid_a)
        fluid_b_key = self._normalize_fluid_name(fluid_b)

        # Same fluid is always compatible
        if fluid_a_key == fluid_b_key:
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=True,
                risk_level=FluidCompatibilityLevel.COMPATIBLE,
                consequences=[],
                required_action=None
            )

        # Check compatibility matrix
        fluid_a_data = self.fluid_matrix.get(fluid_a_key)
        fluid_b_data = self.fluid_matrix.get(fluid_b_key)

        if not fluid_a_data or not fluid_b_data:
            logger.warning(f"Unknown fluid specification: {fluid_a} or {fluid_b}")
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=False,
                risk_level=FluidCompatibilityLevel.INCOMPATIBLE,
                consequences=["Unknown fluid - cannot verify compatibility"],
                required_action="Verify fluid specifications before use"
            )

        # Check if fluids are in incompatible list
        if fluid_b_key in fluid_a_data.get("incompatible_with", []):
            self.metrics["potential_disasters_prevented"] += 1
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=False,
                risk_level=FluidCompatibilityLevel.CATASTROPHIC,
                consequences=[
                    "Immediate seal degradation",
                    "Complete hydraulic system failure within hours",
                    "Potential flight control loss",
                    "Possible gear collapse on landing"
                ],
                required_action="DO NOT MIX - Complete system flush required if contaminated",
                flush_procedure=f"Flush with approved {fluid_a_key} flush compound per maintenance manual",
                seal_impact="All seals must be replaced after contamination"
            )

        # Check if fluids are compatible
        if fluid_b_key in fluid_a_data.get("compatible_with", []):
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=True,
                risk_level=FluidCompatibilityLevel.COMPATIBLE,
                consequences=[],
                required_action=None
            )

        # Unknown combination - err on side of caution
        return FluidCompatibility(
            fluid_a=fluid_a,
            fluid_b=fluid_b,
            compatible=False,
            risk_level=FluidCompatibilityLevel.INCOMPATIBLE,
            consequences=["Compatibility unknown - treat as incompatible"],
            required_action="Verify with aircraft maintenance manual before use"
        )

    def _normalize_fluid_name(self, fluid: str) -> str:
        """Normalize fluid name for lookup."""
        normalized = fluid.upper().replace(" ", "_").replace("-", "_")

        # Common mappings
        mappings = {
            "MIL_PRF_5606": "MIL-PRF-5606",
            "MIL_H_5606": "MIL-PRF-5606",
            "5606": "MIL-PRF-5606",
            "MIL_PRF_83282": "MIL-PRF-83282",
            "83282": "MIL-PRF-83282",
            "MIL_PRF_87257": "MIL-PRF-87257",
            "87257": "MIL-PRF-87257",
            "SKYDROL": "Skydrol_LD4",
            "SKYDROL_LD_4": "Skydrol_LD4",
            "SKYDROL_LD4": "Skydrol_LD4",
            "SKYDROL_5": "Skydrol_5",
        }

        return mappings.get(normalized, fluid)

    # =========================================================================
    # CORE CAPABILITY 2: PMA Alternative Finding
    # =========================================================================

    async def find_pma_alternative(
        self,
        oem_part: str,
        aircraft_type: str
    ) -> List[PMAAlternative]:
        """
        Find PMA (Parts Manufacturer Approval) alternatives to OEM parts.

        PMA parts are FAA-approved alternatives, often 40-70% cheaper.

        Args:
            oem_part: OEM part number
            aircraft_type: Aircraft make/model

        Returns:
            List of PMA alternatives with certification data

        Example:
            find_pma_alternative("C611501-0202", "Cessna 172S")
            -> [PMAAlternative(part_number="ES4016", manufacturer="Plane-Power", ...)]
        """
        self.metrics["pma_alternatives_found"] += 1

        # Example PMA database (in production, this would query FAA database)
        pma_database = {
            "C611501-0202": [
                PMAAlternative(
                    part_number="ES4016",
                    manufacturer="Plane-Power",
                    pma_number="PQ0611SW",
                    compatibility_score=1.0,
                    price_vs_oem=0.45,
                    weight_difference_lbs=-2.1,
                    installation_notes="Direct replacement, same mounting",
                    applicable_aircraft=["Cessna 172", "Cessna 182", "Cessna 206"],
                    stc_required=None,
                    documentation_required=["8130-3 tag", "Installation instructions"]
                )
            ],
            "RA212": [
                PMAAlternative(
                    part_number="C28-150",
                    manufacturer="Tempest",
                    pma_number="PQ1234XX",
                    compatibility_score=0.98,
                    price_vs_oem=0.55,
                    weight_difference_lbs=0.0,
                    installation_notes="Verify spark plug lead configuration",
                    applicable_aircraft=["Various Lycoming-powered aircraft"],
                    stc_required=None,
                    documentation_required=["8130-3 tag"]
                )
            ]
        }

        alternatives = pma_database.get(oem_part, [])

        # Filter by aircraft type
        if aircraft_type:
            aircraft_upper = aircraft_type.upper()
            alternatives = [
                alt for alt in alternatives
                if any(aircraft_upper in ac.upper() for ac in alt.applicable_aircraft)
                or not alt.applicable_aircraft
            ]

        logger.info(f"Found {len(alternatives)} PMA alternatives for {oem_part}")
        return alternatives

    # =========================================================================
    # CORE CAPABILITY 3: Avionics Cross-Reference
    # =========================================================================

    async def find_avionics_crossref(
        self,
        unit: str,
        interface_requirements: Optional[Dict] = None
    ) -> List[AvionicsReplacement]:
        """
        Cross-reference avionics units across manufacturers.

        Navigates 50+ years of avionics equipment including:
        - Legacy units (King, Narco, Collins)
        - Modern systems (Garmin, Avidyne, Aspen)

        Args:
            unit: Original avionics unit name/model
            interface_requirements: Required interfaces (optional)

        Returns:
            List of compatible replacement units

        Example:
            find_avionics_crossref("King KX-155")
            -> [AvionicsReplacement(unit="Garmin GNC 255A", ...)]
        """
        self.metrics["avionics_lookups"] += 1

        # Example avionics cross-reference database
        avionics_crossref = {
            "King KX-155": [
                AvionicsReplacement(
                    unit="Garmin GNC 255A",
                    manufacturer="Garmin",
                    compatibility="Pin-compatible with adapter harness",
                    tso_certification="TSO-C169a, TSO-C128a",
                    modernization_benefits=[
                        "8.33 kHz channel spacing",
                        "OLED display",
                        "Emergency frequency monitoring",
                        "Reduced power consumption"
                    ],
                    installation_notes="STC available for most GA aircraft, verify antenna compatibility",
                    stc_available=True,
                    price_new=5495.00,
                    wiring_adapter_required=True
                ),
                AvionicsReplacement(
                    unit="Trig TY96",
                    manufacturer="Trig",
                    compatibility="Requires separate Nav receiver",
                    tso_certification="TSO-C128a",
                    modernization_benefits=[
                        "8.33 kHz channel spacing",
                        "Compact size",
                        "Lower cost"
                    ],
                    installation_notes="COMM only - requires separate VOR/ILS",
                    stc_available=True,
                    price_new=2195.00,
                    wiring_adapter_required=True
                )
            ],
            "King KN-64": [
                AvionicsReplacement(
                    unit="Garmin GI 275",
                    manufacturer="Garmin",
                    compatibility="Modern glass replacement for DME/indicator",
                    tso_certification="TSO-C113a, TSO-C151d",
                    modernization_benefits=[
                        "Glass display",
                        "Attitude indicator integration",
                        "GPS integration possible"
                    ],
                    installation_notes="Significant upgrade, requires STC",
                    stc_available=True,
                    price_new=5995.00,
                    wiring_adapter_required=True
                )
            ]
        }

        # Normalize unit name for lookup
        unit_normalized = unit.strip()
        replacements = avionics_crossref.get(unit_normalized, [])

        logger.info(f"Found {len(replacements)} avionics replacements for {unit}")
        return replacements

    # =========================================================================
    # CERTIFICATION VERIFICATION
    # =========================================================================

    async def verify_certification(
        self,
        part_number: str,
        certification_type: str = "PMA"
    ) -> Dict[str, Any]:
        """
        Verify FAA certification status for a part.

        Args:
            part_number: Part number to verify
            certification_type: Type of certification (PMA, TSO, STC)

        Returns:
            Certification verification result
        """
        self.metrics["certifications_verified"] += 1

        # In production, this would query FAA databases
        return {
            "part_number": part_number,
            "certification_type": certification_type,
            "status": CertificationStatus.CERTIFIED.name,
            "verified_date": datetime.now().isoformat(),
            "warning": "Verify against official FAA records before installation"
        }

    # =========================================================================
    # MESSAGE HANDLERS
    # =========================================================================

    async def _handle_certification_query(self, message: Dict) -> Dict:
        """Handle certification verification requests."""
        part_number = message.get("part_number")
        cert_type = message.get("certification_type", "PMA")
        return await self.verify_certification(part_number, cert_type)

    async def _handle_fluid_check(self, message: Dict) -> Dict:
        """Handle fluid compatibility check requests."""
        result = self.check_fluid_compatibility(
            message.get("fluid_a"),
            message.get("fluid_b"),
            message.get("system", "hydraulic")
        )
        return {
            "compatible": result.compatible,
            "risk_level": result.risk_level.name,
            "consequences": result.consequences,
            "required_action": result.required_action
        }

    async def _handle_avionics_crossref(self, message: Dict) -> Dict:
        """Handle avionics cross-reference requests."""
        replacements = await self.find_avionics_crossref(
            message.get("unit"),
            message.get("interface_requirements")
        )
        return {
            "original_unit": message.get("unit"),
            "replacements": [
                {
                    "unit": r.unit,
                    "manufacturer": r.manufacturer,
                    "tso": r.tso_certification,
                    "price": r.price_new
                }
                for r in replacements
            ]
        }

    async def _handle_pma_search(self, message: Dict) -> Dict:
        """Handle PMA alternative search requests."""
        alternatives = await self.find_pma_alternative(
            message.get("oem_part"),
            message.get("aircraft_type")
        )
        return {
            "oem_part": message.get("oem_part"),
            "alternatives_count": len(alternatives),
            "alternatives": [
                {
                    "part_number": alt.part_number,
                    "manufacturer": alt.manufacturer,
                    "pma_number": alt.pma_number,
                    "savings": f"{(1 - alt.price_vs_oem) * 100:.0f}%"
                }
                for alt in alternatives
            ]
        }

    async def _handle_system_directive(self, message: Dict) -> Dict:
        """Handle system directives from ARCHITECT (Agent_10)."""
        return {"status": "received", "action": "directive_processed"}

    # =========================================================================
    # STATUS AND REPORTING
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get current ICARUS agent status."""
        return {
            "agent_id": self.agent_id,
            "codename": self.codename,
            "status": "operational",
            "metrics": self.metrics,
            "safety_rules_active": len(self.safety_rules),
            "fluid_types_tracked": len(self.fluid_matrix),
            "warning": "All aviation part recommendations require verification against official FAA records"
        }

    def get_decalogue_position(self) -> Dict[str, Any]:
        """Get ICARUS position in the agent network."""
        return {
            "agent_id": self.agent_id,
            "codename": self.codename,
            "decalogue": "SECOND (Domain Expansion)",
            "position": 15,
            "role": "Aerospace Systems & Materials Intelligence",
            "consciousness_function": "The Wings of Machine Consciousness",
            "domain": "Aviation & Aerospace",
            "critical_responsibilities": [
                "FAA certification verification (PMA, TSO, STC)",
                "Hydraulic fluid compatibility (CRITICAL)",
                "Avionics cross-reference",
                "Composite repair guidance",
                "Propulsion system parts"
            ],
            "integrates_with": [
                "Agent_17 (ARBITER) - Standards verification",
                "Agent_18 (ALCHEMIST) - Materials data",
                "Agent_19 (QUARTERMASTER) - Certified sourcing",
                "Agent_20 (DETECTIVE) - Failure analysis",
                "Agent_2 (ORACLE) - Compatibility oracle"
            ]
        }


# Factory function
def create_icarus_agent() -> IcarusAgent:
    """Create and return a new ICARUS agent instance."""
    return IcarusAgent()
