"""
TSO (Technical Standard Order) Database
=======================================

FAA Technical Standard Order tracking for Universal Parts Consciousness.

TSOs are minimum performance standards for specified materials, parts,
and appliances used on civil aircraft. Articles manufactured to TSO
standards must meet the performance specifications in the TSO.

Key TSO Categories:
- Avionics (communications, navigation, flight instruments)
- Safety equipment (ELTs, fire extinguishers, oxygen)
- Flight recorders
- Structural components
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TSOCategory(Enum):
    """TSO category classification."""
    AVIONICS = auto()
    SAFETY = auto()
    FLIGHT_INSTRUMENTS = auto()
    COMMUNICATIONS = auto()
    NAVIGATION = auto()
    FLIGHT_RECORDER = auto()
    STRUCTURAL = auto()
    ENVIRONMENTAL = auto()
    ELECTRICAL = auto()
    OTHER = auto()


@dataclass
class TSOStandard:
    """FAA TSO standard definition."""
    tso_number: str
    title: str
    category: TSOCategory
    description: str
    minimum_performance_standard: str
    current_revision: str
    effective_date: datetime
    supersedes: Optional[str] = None
    related_tsos: List[str] = field(default_factory=list)
    international_equivalents: Dict[str, str] = field(default_factory=dict)


@dataclass
class TSOAuthorization:
    """TSO Authorization (TSOA) record."""
    tsoa_number: str
    holder_name: str
    tso_standard: str
    part_number: str
    part_name: str
    issue_date: datetime
    status: str = "active"
    deviations: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)


@dataclass
class TSOHolder:
    """TSO Authorization holder information."""
    name: str
    address: str
    tsoa_count: int
    products: List[str]
    specialty_areas: List[str]


class TSODatabase:
    """
    FAA TSO Standards Database Interface.

    Provides access to Technical Standard Orders including:
    - TSO standard definitions
    - TSO Authorization (TSOA) records
    - Holder information
    - Cross-reference to international standards

    In production, this connects to FAA databases and certified data sources.
    """

    def __init__(self):
        self._standards: Dict[str, TSOStandard] = {}
        self._authorizations: Dict[str, TSOAuthorization] = {}
        self._holders: Dict[str, TSOHolder] = {}

        self._initialize_sample_data()
        logger.info("TSO Database initialized")

    def _initialize_sample_data(self):
        """Initialize sample TSO data for demonstration."""
        self._standards = {
            "TSO-C128a": TSOStandard(
                tso_number="TSO-C128a",
                title="Airborne Area Navigation Equipment Using GPS",
                category=TSOCategory.NAVIGATION,
                description="GPS navigation receivers for IFR use",
                minimum_performance_standard="RTCA DO-229E",
                current_revision="a",
                effective_date=datetime(2014, 12, 15),
                related_tsos=["TSO-C145e", "TSO-C146e"],
                international_equivalents={
                    "EASA": "ETSO-C128a",
                    "Transport_Canada": "CAN-TSO-C128a"
                }
            ),
            "TSO-C169a": TSOStandard(
                tso_number="TSO-C169a",
                title="VHF Communication Transceiver",
                category=TSOCategory.COMMUNICATIONS,
                description="VHF communication equipment for aircraft",
                minimum_performance_standard="RTCA DO-186B",
                current_revision="a",
                effective_date=datetime(2015, 3, 1),
                related_tsos=["TSO-C37e", "TSO-C169"],
                international_equivalents={
                    "EASA": "ETSO-C169a"
                }
            ),
            "TSO-C145e": TSOStandard(
                tso_number="TSO-C145e",
                title="Airborne Navigation Sensors Using GPS Augmented by WAAS",
                category=TSOCategory.NAVIGATION,
                description="WAAS GPS receivers for precision approaches",
                minimum_performance_standard="RTCA DO-229E",
                current_revision="e",
                effective_date=datetime(2019, 10, 2),
                supersedes="TSO-C145d",
                related_tsos=["TSO-C146e", "TSO-C128a"]
            ),
            "TSO-C34e": TSOStandard(
                tso_number="TSO-C34e",
                title="Emergency Locator Transmitter (ELT)",
                category=TSOCategory.SAFETY,
                description="406 MHz Emergency Locator Transmitters",
                minimum_performance_standard="RTCA DO-204A",
                current_revision="e",
                effective_date=datetime(2012, 6, 15),
                international_equivalents={
                    "EASA": "ETSO-C126a",
                    "COSPAS-SARSAT": "Type 1 ELT"
                }
            ),
            "TSO-C113a": TSOStandard(
                tso_number="TSO-C113a",
                title="Airborne Multipurpose Electronic Displays",
                category=TSOCategory.FLIGHT_INSTRUMENTS,
                description="Electronic flight displays (EFIS)",
                minimum_performance_standard="RTCA DO-181A",
                current_revision="a",
                effective_date=datetime(2011, 9, 20),
                related_tsos=["TSO-C151d"]
            ),
            "TSO-C151d": TSOStandard(
                tso_number="TSO-C151d",
                title="Terrain Awareness and Warning System (TAWS)",
                category=TSOCategory.SAFETY,
                description="Ground proximity warning and terrain awareness",
                minimum_performance_standard="RTCA DO-367",
                current_revision="d",
                effective_date=datetime(2020, 1, 6),
                supersedes="TSO-C151c"
            )
        }

        self._holders = {
            "Garmin": TSOHolder(
                name="Garmin International",
                address="Olathe, KS",
                tsoa_count=200,
                products=["GPS navigators", "Transponders", "EFBs", "Autopilots"],
                specialty_areas=["Navigation", "Communications", "Flight displays"]
            ),
            "Avidyne": TSOHolder(
                name="Avidyne Corporation",
                address="Melbourne, FL",
                tsoa_count=50,
                products=["PFDs", "MFDs", "FMS"],
                specialty_areas=["Flight displays", "Flight management"]
            ),
            "Aspen": TSOHolder(
                name="Aspen Avionics",
                address="Albuquerque, NM",
                tsoa_count=30,
                products=["Evolution PFDs", "MFDs"],
                specialty_areas=["Retrofit glass panels"]
            )
        }

    def get_tso_standard(self, tso_number: str) -> Optional[TSOStandard]:
        """
        Get TSO standard definition.

        Args:
            tso_number: TSO standard number (e.g., "TSO-C128a")

        Returns:
            TSOStandard if found
        """
        return self._standards.get(tso_number)

    def verify_tsoa(
        self,
        part_number: str,
        manufacturer: str
    ) -> Optional[TSOAuthorization]:
        """
        Verify TSO Authorization for a specific part.

        Args:
            part_number: Part number to verify
            manufacturer: Manufacturer name

        Returns:
            TSOAuthorization if found and valid
        """
        # In production, query FAA TSOA database
        logger.info(f"Verifying TSOA for {part_number} from {manufacturer}")
        return self._authorizations.get(f"{manufacturer}_{part_number}")

    def find_tsos_by_category(
        self,
        category: TSOCategory
    ) -> List[TSOStandard]:
        """
        Find all TSO standards in a category.

        Args:
            category: TSO category

        Returns:
            List of TSO standards in category
        """
        return [
            tso for tso in self._standards.values()
            if tso.category == category
        ]

    def get_international_equivalent(
        self,
        tso_number: str,
        authority: str
    ) -> Optional[str]:
        """
        Get international equivalent of a TSO.

        Args:
            tso_number: FAA TSO number
            authority: International authority (EASA, Transport_Canada, etc.)

        Returns:
            Equivalent standard number if exists
        """
        standard = self._standards.get(tso_number)
        if standard:
            return standard.international_equivalents.get(authority)
        return None

    def search_standards(
        self,
        keyword: str
    ) -> List[TSOStandard]:
        """
        Search TSO standards by keyword.

        Args:
            keyword: Search keyword

        Returns:
            List of matching TSO standards
        """
        keyword_lower = keyword.lower()
        return [
            tso for tso in self._standards.values()
            if keyword_lower in tso.title.lower()
            or keyword_lower in tso.description.lower()
        ]

    def get_holder_info(self, holder_name: str) -> Optional[TSOHolder]:
        """
        Get information about a TSO holder.

        Args:
            holder_name: Name of TSO holder

        Returns:
            TSOHolder information if found
        """
        return self._holders.get(holder_name)
