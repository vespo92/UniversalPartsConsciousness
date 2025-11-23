"""
Hydraulic Fluid Compatibility Matrix
====================================

CRITICAL: Aviation hydraulic fluids are NOT interchangeable.
Mixing incompatible fluids causes seal destruction and system failure.

This module provides the fluid compatibility intelligence that prevents
catastrophic mixing incidents. In aviation, a fluid compatibility error
can cause complete hydraulic system failure mid-flight.

Fluid Families:
- MIL-PRF-5606 (Red mineral oil) - GA piston aircraft
- MIL-PRF-83282 (Red synthetic) - Military aircraft
- MIL-PRF-87257 (Red synthetic, low temp) - Military cold weather
- Skydrol (Purple phosphate ester) - Commercial jets

THE RULE: NEVER mix fluids from different compatibility groups.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum, auto
import logging

logger = logging.getLogger(__name__)


class FluidType(Enum):
    """Hydraulic fluid type classification."""
    MINERAL = auto()           # Petroleum-based
    SYNTHETIC_HYDROCARBON = auto()  # Synthetic hydrocarbon
    PHOSPHATE_ESTER = auto()   # Skydrol family
    SILICONE = auto()          # Specialty applications


class CompatibilityGroup(Enum):
    """Fluid compatibility groupings."""
    GROUP_A = "A"  # MIL-PRF-5606 family (mineral oil)
    GROUP_B = "B"  # MIL-PRF-83282/87257 family (synthetic hydrocarbon)
    GROUP_C = "C"  # Skydrol family (phosphate ester)


class RiskLevel(Enum):
    """Risk level for fluid mixing."""
    SAFE = auto()              # Same fluid or fully compatible
    CAUTION = auto()           # Compatible but monitor
    WARNING = auto()           # Not recommended
    DANGER = auto()            # System damage likely
    CATASTROPHIC = auto()      # Complete system failure


@dataclass
class FluidFamily:
    """Aviation hydraulic fluid specification."""
    specification: str
    color: str
    fluid_type: FluidType
    compatibility_group: CompatibilityGroup
    typical_aircraft: List[str]
    temperature_range_c: Tuple[int, int]
    seal_materials: List[str]
    compatible_with: List[str]
    incompatible_with: List[str]
    cautions: List[str] = field(default_factory=list)
    supersedes: Optional[str] = None


@dataclass
class FluidCompatibility:
    """Result of fluid compatibility check."""
    fluid_a: str
    fluid_b: str
    compatible: bool
    risk_level: RiskLevel
    consequences: List[str] = field(default_factory=list)
    required_action: Optional[str] = None
    flush_procedure: Optional[str] = None
    seal_impact: Optional[str] = None
    historical_incidents: List[str] = field(default_factory=list)


@dataclass
class CompatibilityCheckResult:
    """Complete compatibility check result with guidance."""
    result: FluidCompatibility
    verification_notes: List[str]
    documentation_required: List[str]
    maintenance_actions: List[str]


class HydraulicFluidMatrix:
    """
    Aviation Hydraulic Fluid Compatibility Matrix.

    CRITICAL SAFETY COMPONENT: This matrix prevents catastrophic fluid
    mixing incidents. All compatibility checks MUST pass through this
    system before any fluid recommendations.

    The matrix tracks:
    - Fluid specifications and properties
    - Compatibility groupings
    - Seal material interactions
    - Historical incident data
    - Required flush procedures
    """

    def __init__(self):
        self._fluids: Dict[str, FluidFamily] = {}
        self._incident_history: List[Dict] = []

        self._initialize_fluid_database()
        logger.info("Hydraulic Fluid Matrix initialized - CRITICAL SAFETY SYSTEM")

    def _initialize_fluid_database(self):
        """Initialize the fluid compatibility database."""
        self._fluids = {
            "MIL-PRF-5606": FluidFamily(
                specification="MIL-PRF-5606",
                color="RED",
                fluid_type=FluidType.MINERAL,
                compatibility_group=CompatibilityGroup.GROUP_A,
                typical_aircraft=[
                    "Cessna 172/182/206/210",
                    "Piper PA-28/PA-32/PA-34",
                    "Beechcraft Bonanza/Baron",
                    "Most GA piston aircraft",
                    "Some older turboprops"
                ],
                temperature_range_c=(-54, 135),
                seal_materials=["Buna-N", "Neoprene", "Natural rubber"],
                compatible_with=["MIL-PRF-5606", "MIL-H-5606"],
                incompatible_with=[
                    "Skydrol_LD4", "Skydrol_5", "Skydrol_500B4",
                    "MIL-PRF-83282", "MIL-PRF-87257"
                ],
                supersedes="MIL-H-5606"
            ),
            "MIL-H-5606": FluidFamily(
                specification="MIL-H-5606",
                color="RED",
                fluid_type=FluidType.MINERAL,
                compatibility_group=CompatibilityGroup.GROUP_A,
                typical_aircraft=["Legacy aircraft", "Older systems"],
                temperature_range_c=(-54, 135),
                seal_materials=["Buna-N", "Neoprene"],
                compatible_with=["MIL-PRF-5606", "MIL-H-5606"],
                incompatible_with=[
                    "Skydrol_LD4", "Skydrol_5",
                    "MIL-PRF-83282", "MIL-PRF-87257"
                ],
                cautions=["Obsolete specification - use MIL-PRF-5606"]
            ),
            "MIL-PRF-83282": FluidFamily(
                specification="MIL-PRF-83282",
                color="RED",  # SAME COLOR AS 5606 - CRITICAL DANGER!
                fluid_type=FluidType.SYNTHETIC_HYDROCARBON,
                compatibility_group=CompatibilityGroup.GROUP_B,
                typical_aircraft=[
                    "F-15", "F-16", "F/A-18",
                    "C-130", "C-17",
                    "Some business jets",
                    "Military helicopters"
                ],
                temperature_range_c=(-40, 205),
                seal_materials=["EPR", "Butyl", "Ethylene propylene"],
                compatible_with=["MIL-PRF-83282", "MIL-PRF-87257"],
                incompatible_with=[
                    "MIL-PRF-5606", "MIL-H-5606",
                    "Skydrol_LD4", "Skydrol_5"
                ],
                cautions=[
                    "SAME RED COLOR as MIL-PRF-5606 - VERIFY BEFORE USE",
                    "Different seal requirements than 5606"
                ]
            ),
            "MIL-PRF-87257": FluidFamily(
                specification="MIL-PRF-87257",
                color="RED",
                fluid_type=FluidType.SYNTHETIC_HYDROCARBON,
                compatibility_group=CompatibilityGroup.GROUP_B,
                typical_aircraft=[
                    "Military aircraft in cold climates",
                    "Arctic operations"
                ],
                temperature_range_c=(-54, 205),
                seal_materials=["EPR", "Butyl"],
                compatible_with=["MIL-PRF-83282", "MIL-PRF-87257"],
                incompatible_with=[
                    "MIL-PRF-5606", "MIL-H-5606",
                    "Skydrol_LD4", "Skydrol_5"
                ],
                cautions=["Low temperature variant of 83282"]
            ),
            "Skydrol_LD4": FluidFamily(
                specification="Skydrol_LD4",
                color="PURPLE",
                fluid_type=FluidType.PHOSPHATE_ESTER,
                compatibility_group=CompatibilityGroup.GROUP_C,
                typical_aircraft=[
                    "Boeing 737/747/757/767/777/787",
                    "Airbus A320/A330/A340/A350/A380",
                    "Embraer regional jets",
                    "Large turboprops (ATR, Q400)"
                ],
                temperature_range_c=(-54, 107),
                seal_materials=["Butyl", "EPR", "Ethylene propylene"],
                compatible_with=["Skydrol_LD4", "Skydrol_5", "Skydrol_500B4"],
                incompatible_with=[
                    "MIL-PRF-5606", "MIL-H-5606",
                    "MIL-PRF-83282", "MIL-PRF-87257"
                ],
                cautions=[
                    "ATTACKS acrylic windows - protect during servicing",
                    "DISSOLVES paint - immediate cleanup required",
                    "Requires specific PPE - skin and eye irritant",
                    "Fire resistant but NOT fireproof"
                ]
            ),
            "Skydrol_5": FluidFamily(
                specification="Skydrol_5",
                color="PURPLE",
                fluid_type=FluidType.PHOSPHATE_ESTER,
                compatibility_group=CompatibilityGroup.GROUP_C,
                typical_aircraft=[
                    "Modern commercial jets",
                    "Boeing 787",
                    "Airbus A350/A380"
                ],
                temperature_range_c=(-54, 107),
                seal_materials=["Butyl", "EPR"],
                compatible_with=["Skydrol_LD4", "Skydrol_5", "Skydrol_500B4"],
                incompatible_with=[
                    "MIL-PRF-5606", "MIL-H-5606",
                    "MIL-PRF-83282", "MIL-PRF-87257"
                ],
                cautions=[
                    "Low density variant - weight savings",
                    "Same precautions as Skydrol LD-4"
                ]
            )
        }

        # Historical incidents for learning
        self._incident_history = [
            {
                "date": "documented",
                "fluids": ["MIL-PRF-5606", "Skydrol"],
                "consequence": "Complete brake system failure, gear collapse on landing",
                "root_cause": "Maintenance personnel unfamiliar with aircraft type"
            },
            {
                "date": "documented",
                "fluids": ["MIL-PRF-5606", "MIL-PRF-83282"],
                "consequence": "Gradual seal degradation, uncommanded flight control movement",
                "root_cause": "Both fluids are red - visual identification failed"
            }
        ]

    def check_compatibility(
        self,
        fluid_a: str,
        fluid_b: str
    ) -> FluidCompatibility:
        """
        Check compatibility between two hydraulic fluids.

        CRITICAL: This is a safety-critical function. The result determines
        whether fluids can be safely mixed or used in the same system.

        Args:
            fluid_a: First fluid specification
            fluid_b: Second fluid specification

        Returns:
            FluidCompatibility with risk assessment and required actions
        """
        # Normalize fluid names
        fluid_a_key = self._normalize_fluid_name(fluid_a)
        fluid_b_key = self._normalize_fluid_name(fluid_b)

        # Same fluid is always compatible
        if fluid_a_key == fluid_b_key:
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=True,
                risk_level=RiskLevel.SAFE,
                consequences=[],
                required_action=None
            )

        # Get fluid data
        fluid_a_data = self._fluids.get(fluid_a_key)
        fluid_b_data = self._fluids.get(fluid_b_key)

        if not fluid_a_data or not fluid_b_data:
            logger.warning(f"Unknown fluid: {fluid_a} or {fluid_b}")
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=False,
                risk_level=RiskLevel.WARNING,
                consequences=["Unknown fluid specification - cannot verify compatibility"],
                required_action="Identify fluid specifications before proceeding"
            )

        # Check if incompatible
        if fluid_b_key in fluid_a_data.incompatible_with:
            # Find relevant incidents
            relevant_incidents = [
                inc for inc in self._incident_history
                if fluid_a_key in inc["fluids"] or fluid_b_key in inc["fluids"]
            ]

            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=False,
                risk_level=RiskLevel.CATASTROPHIC,
                consequences=[
                    "IMMEDIATE seal degradation upon contact",
                    "Complete hydraulic system failure within hours",
                    "Flight control loss possible",
                    "Landing gear malfunction risk",
                    f"Seal materials incompatible: {fluid_a_data.seal_materials} vs {fluid_b_data.seal_materials}"
                ],
                required_action="DO NOT MIX UNDER ANY CIRCUMSTANCES",
                flush_procedure=(
                    f"If contaminated: Complete system drain, flush with approved solvent, "
                    f"replace ALL seals, refill with correct fluid per maintenance manual"
                ),
                seal_impact="ALL seals must be replaced after contamination",
                historical_incidents=[inc["consequence"] for inc in relevant_incidents]
            )

        # Check if compatible
        if fluid_b_key in fluid_a_data.compatible_with:
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=True,
                risk_level=RiskLevel.SAFE,
                consequences=[],
                required_action=None
            )

        # Same compatibility group but not explicitly listed
        if fluid_a_data.compatibility_group == fluid_b_data.compatibility_group:
            return FluidCompatibility(
                fluid_a=fluid_a,
                fluid_b=fluid_b,
                compatible=True,
                risk_level=RiskLevel.CAUTION,
                consequences=["Same fluid family - likely compatible"],
                required_action="Verify with aircraft maintenance manual"
            )

        # Different groups - treat as incompatible
        return FluidCompatibility(
            fluid_a=fluid_a,
            fluid_b=fluid_b,
            compatible=False,
            risk_level=RiskLevel.DANGER,
            consequences=["Different fluid families - incompatibility likely"],
            required_action="Do not mix - verify with maintenance manual"
        )

    def _normalize_fluid_name(self, fluid: str) -> str:
        """Normalize fluid name for database lookup."""
        # Common normalizations
        mappings = {
            "5606": "MIL-PRF-5606",
            "MIL-H-5606": "MIL-H-5606",
            "MIL-PRF-5606": "MIL-PRF-5606",
            "83282": "MIL-PRF-83282",
            "MIL-PRF-83282": "MIL-PRF-83282",
            "87257": "MIL-PRF-87257",
            "MIL-PRF-87257": "MIL-PRF-87257",
            "SKYDROL": "Skydrol_LD4",
            "SKYDROL LD-4": "Skydrol_LD4",
            "SKYDROL LD4": "Skydrol_LD4",
            "SKYDROL_LD4": "Skydrol_LD4",
            "SKYDROL 5": "Skydrol_5",
            "SKYDROL_5": "Skydrol_5",
        }

        normalized = fluid.upper().replace(" ", "_").replace("-", "_")

        # Try exact match first
        if fluid in self._fluids:
            return fluid

        # Try normalized match
        for key, value in mappings.items():
            if key.upper().replace(" ", "_").replace("-", "_") == normalized:
                return value

        return fluid

    def get_fluid_info(self, fluid: str) -> Optional[FluidFamily]:
        """
        Get detailed information about a hydraulic fluid.

        Args:
            fluid: Fluid specification

        Returns:
            FluidFamily data if found
        """
        fluid_key = self._normalize_fluid_name(fluid)
        return self._fluids.get(fluid_key)

    def get_compatible_fluids(self, fluid: str) -> List[str]:
        """
        Get list of fluids compatible with the specified fluid.

        Args:
            fluid: Fluid specification

        Returns:
            List of compatible fluid specifications
        """
        fluid_data = self.get_fluid_info(fluid)
        if fluid_data:
            return fluid_data.compatible_with
        return []

    def get_fluids_by_aircraft(self, aircraft: str) -> List[FluidFamily]:
        """
        Get recommended fluids for an aircraft type.

        Args:
            aircraft: Aircraft make/model

        Returns:
            List of applicable fluid families
        """
        aircraft_upper = aircraft.upper()
        return [
            fluid for fluid in self._fluids.values()
            if any(aircraft_upper in ac.upper() for ac in fluid.typical_aircraft)
        ]
