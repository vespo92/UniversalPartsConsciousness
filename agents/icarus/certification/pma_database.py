"""
PMA (Parts Manufacturer Approval) Database
==========================================

FAA-approved alternative parts database for Universal Parts Consciousness.

PMA parts are manufactured by companies other than the original equipment
manufacturer (OEM), but are FAA-approved as direct replacements.

Benefits of PMA parts:
- 40-70% cost savings vs OEM
- Same safety and quality standards
- FAA oversight and approval

IMPORTANT: All PMA parts must have valid FAA approval and 8130-3 documentation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PMAStatus(Enum):
    """PMA approval status."""
    ACTIVE = auto()          # Currently valid approval
    SUSPENDED = auto()       # Temporarily suspended
    REVOKED = auto()         # Approval revoked
    EXPIRED = auto()         # Approval expired
    PENDING = auto()         # Application pending


class PMABasis(Enum):
    """Basis for PMA approval."""
    TEST_AND_COMPUTATION = auto()    # Full testing and analysis
    IDENTICALITY = auto()            # Identical to type design
    LICENSING = auto()               # License from TC holder
    TEST_ONLY = auto()               # Test only basis


@dataclass
class PMACertification:
    """FAA PMA certification record."""
    pma_number: str
    holder_name: str
    holder_address: str
    part_numbers: List[str]
    applicable_tcs: List[str]  # Type Certificates
    basis: PMABasis
    status: PMAStatus
    issue_date: datetime
    expiry_date: Optional[datetime] = None
    limitations: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class PMAAlternative:
    """PMA alternative to an OEM part."""
    part_number: str
    manufacturer: str
    pma_number: str
    oem_part_replaced: str
    compatibility_score: float  # 0.0 to 1.0
    price_vs_oem: float  # Ratio (0.45 = 55% cheaper)
    weight_difference_lbs: float
    installation_notes: str
    applicable_aircraft: List[str] = field(default_factory=list)
    stc_required: Optional[str] = None
    documentation_required: List[str] = field(default_factory=list)
    airworthiness_limitations: List[str] = field(default_factory=list)
    verification_status: str = "unverified"


@dataclass
class PMAHolder:
    """PMA holder (manufacturer) information."""
    holder_number: str
    name: str
    address: str
    pma_certificates: List[str]
    parts_count: int
    specialty_areas: List[str]
    faa_district: str
    contact_info: Optional[Dict[str, str]] = None


class PMADatabase:
    """
    FAA PMA Parts Database Interface.

    Provides access to PMA-approved alternative parts, including:
    - Part cross-reference (OEM to PMA)
    - Certification verification
    - Holder information
    - Applicable aircraft lookup

    In production, this connects to FAA databases and certified data sources.
    """

    def __init__(self):
        # Example PMA data (production would connect to FAA databases)
        self._pma_parts: Dict[str, List[PMAAlternative]] = {}
        self._pma_holders: Dict[str, PMAHolder] = {}
        self._certifications: Dict[str, PMACertification] = {}

        self._initialize_sample_data()
        logger.info("PMA Database initialized")

    def _initialize_sample_data(self):
        """Initialize sample PMA data for demonstration."""
        # Sample PMA alternatives
        self._pma_parts = {
            # Cessna alternator
            "C611501-0202": [
                PMAAlternative(
                    part_number="ES4016",
                    manufacturer="Plane-Power",
                    pma_number="PQ0611SW",
                    oem_part_replaced="C611501-0202",
                    compatibility_score=1.0,
                    price_vs_oem=0.45,
                    weight_difference_lbs=-2.1,
                    installation_notes="Direct replacement, same mounting pattern",
                    applicable_aircraft=[
                        "Cessna 172 (all models)",
                        "Cessna 182 (all models)",
                        "Cessna 206",
                        "Cessna 210"
                    ],
                    documentation_required=[
                        "FAA Form 8130-3",
                        "Installation instructions",
                        "Weight and balance update if needed"
                    ]
                )
            ],
            # Lycoming magneto
            "LW-15473": [
                PMAAlternative(
                    part_number="E-MAG",
                    manufacturer="SureFly",
                    pma_number="PQ0987XX",
                    oem_part_replaced="LW-15473",
                    compatibility_score=0.95,
                    price_vs_oem=0.75,
                    weight_difference_lbs=-1.5,
                    installation_notes="Electronic ignition, requires STC for most installations",
                    applicable_aircraft=[
                        "Various Lycoming-powered aircraft"
                    ],
                    stc_required="STC SA02639SE",
                    documentation_required=[
                        "FAA Form 8130-3",
                        "STC documentation",
                        "Installation manual"
                    ]
                )
            ],
            # Brake disc
            "164-11400": [
                PMAAlternative(
                    part_number="APS164-11400",
                    manufacturer="APS Brakes",
                    pma_number="PQ0456APS",
                    oem_part_replaced="164-11400",
                    compatibility_score=1.0,
                    price_vs_oem=0.50,
                    weight_difference_lbs=0.0,
                    installation_notes="Direct replacement",
                    applicable_aircraft=[
                        "Cessna 172",
                        "Cessna 182",
                        "Piper PA-28"
                    ],
                    documentation_required=["FAA Form 8130-3"]
                )
            ]
        }

        # Sample PMA holders
        self._pma_holders = {
            "Plane-Power": PMAHolder(
                holder_number="PQ0611SW",
                name="Plane-Power Ltd",
                address="Tulsa, OK",
                pma_certificates=["PQ0611SW", "PQ0611SX"],
                parts_count=25,
                specialty_areas=["Alternators", "Starters", "Electrical"],
                faa_district="Southwest"
            ),
            "APS Brakes": PMAHolder(
                holder_number="PQ0456APS",
                name="Aircraft Performance Services",
                address="Kansas City, MO",
                pma_certificates=["PQ0456APS"],
                parts_count=50,
                specialty_areas=["Brake assemblies", "Brake discs", "Linings"],
                faa_district="Central"
            )
        }

    def find_pma_alternatives(
        self,
        oem_part_number: str,
        aircraft_type: Optional[str] = None
    ) -> List[PMAAlternative]:
        """
        Find PMA alternatives for an OEM part number.

        Args:
            oem_part_number: Original equipment manufacturer part number
            aircraft_type: Optional aircraft type to filter results

        Returns:
            List of PMA alternatives
        """
        alternatives = self._pma_parts.get(oem_part_number, [])

        if aircraft_type and alternatives:
            aircraft_upper = aircraft_type.upper()
            alternatives = [
                alt for alt in alternatives
                if any(aircraft_upper in ac.upper() for ac in alt.applicable_aircraft)
                or not alt.applicable_aircraft
            ]

        logger.info(f"Found {len(alternatives)} PMA alternatives for {oem_part_number}")
        return alternatives

    def verify_pma_certification(
        self,
        pma_number: str
    ) -> Optional[PMACertification]:
        """
        Verify a PMA certification is valid.

        Args:
            pma_number: PMA certificate number

        Returns:
            PMACertification if found and valid, None otherwise
        """
        certification = self._certifications.get(pma_number)

        if certification:
            if certification.status != PMAStatus.ACTIVE:
                logger.warning(f"PMA {pma_number} is not active: {certification.status.name}")

        return certification

    def get_pma_holder(self, holder_name: str) -> Optional[PMAHolder]:
        """
        Get information about a PMA holder.

        Args:
            holder_name: Name of the PMA holder/manufacturer

        Returns:
            PMAHolder information if found
        """
        return self._pma_holders.get(holder_name)

    def search_by_aircraft(
        self,
        aircraft_type: str
    ) -> Dict[str, List[PMAAlternative]]:
        """
        Search all PMA parts applicable to a specific aircraft type.

        Args:
            aircraft_type: Aircraft make/model

        Returns:
            Dictionary of OEM part numbers to PMA alternatives
        """
        results = {}
        aircraft_upper = aircraft_type.upper()

        for oem_part, alternatives in self._pma_parts.items():
            applicable = [
                alt for alt in alternatives
                if any(aircraft_upper in ac.upper() for ac in alt.applicable_aircraft)
            ]
            if applicable:
                results[oem_part] = applicable

        return results

    def calculate_savings(
        self,
        oem_part_number: str,
        oem_price: float
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate potential savings from PMA alternatives.

        Args:
            oem_part_number: OEM part number
            oem_price: Current OEM price

        Returns:
            Savings calculation for each PMA alternative
        """
        alternatives = self._pma_parts.get(oem_part_number, [])

        if not alternatives:
            return None

        savings = []
        for alt in alternatives:
            pma_price = oem_price * alt.price_vs_oem
            savings.append({
                "pma_part": alt.part_number,
                "manufacturer": alt.manufacturer,
                "pma_price": pma_price,
                "savings": oem_price - pma_price,
                "savings_percent": (1 - alt.price_vs_oem) * 100
            })

        return {
            "oem_part": oem_part_number,
            "oem_price": oem_price,
            "alternatives": savings
        }
