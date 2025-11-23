"""
Agent_17: ARBITER - Standards & Regulatory Compliance Intelligence

"The law is the public conscience." - Thomas Hobbes

When parts must meet standards, ARBITER is the authority.
Verifies compliance claims, maps equivalences between standards systems,
explains certification requirements, and ensures engineers understand
what "meets spec" really means.

Domains:
- Mechanical standards (ISO, ASTM, SAE, DIN, JIS)
- Electrical standards (UL, CSA, CE, IEC)
- Industry-specific (MIL-SPEC, AMS, FDA, ABYC)
- Quality certifications (ISO 9001, AS9100, IATF 16949)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
from decimal import Decimal


class StandardsBody(Enum):
    """Major standards organizations"""
    ISO = "iso"           # International Organization for Standardization
    ASTM = "astm"         # American Society for Testing and Materials
    SAE = "sae"           # Society of Automotive Engineers
    DIN = "din"           # Deutsches Institut fur Normung (German)
    JIS = "jis"           # Japanese Industrial Standards
    BS = "bs"             # British Standards
    UL = "ul"             # Underwriters Laboratories
    CSA = "csa"           # Canadian Standards Association
    CE = "ce"             # Conformite Europeenne (European)
    IEC = "iec"           # International Electrotechnical Commission
    MIL = "mil"           # Military Specifications
    AMS = "ams"           # Aerospace Material Specifications
    FDA = "fda"           # Food and Drug Administration
    ABYC = "abyc"         # American Boat and Yacht Council
    NEMA = "nema"         # National Electrical Manufacturers Association
    ANSI = "ansi"         # American National Standards Institute


class VerificationStatus(Enum):
    """Status of standards compliance verification"""
    VERIFIED = "verified"           # Confirmed compliant
    UNVERIFIABLE = "unverifiable"   # Cannot confirm
    NON_COMPLIANT = "non_compliant" # Confirmed non-compliant
    CONDITIONAL = "conditional"      # Compliant under certain conditions
    PENDING = "pending"              # Awaiting verification


class CertificationType(Enum):
    """Types of certifications"""
    PRODUCT = "product"              # Product certification (UL Listed)
    COMPONENT = "component"          # Component certification (UL Recognized)
    SYSTEM = "system"                # Quality management system (ISO 9001)
    MATERIAL = "material"            # Material certification (mill cert)
    PROCESS = "process"              # Process certification (Nadcap)
    FACILITY = "facility"            # Facility certification (AS9100)


class StandardsDomain(Enum):
    """Domain categories for standards"""
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    AEROSPACE = "aerospace"
    AUTOMOTIVE = "automotive"
    MARINE = "marine"
    MEDICAL = "medical"
    INDUSTRIAL = "industrial"
    CONSTRUCTION = "construction"


@dataclass
class StandardDefinition:
    """Definition of a standard specification"""
    standard_id: str              # e.g., "ISO 898-1"
    name: str                     # Full name
    body: StandardsBody           # Issuing organization
    domain: StandardsDomain       # Application domain
    version: str                  # Current version/year
    description: str              # What it covers
    key_requirements: List[str]   # Main requirements
    test_methods: List[str]       # Required tests
    supersedes: Optional[str]     # Previous standard it replaced
    harmonized_with: List[str]    # Equivalent/harmonized standards


@dataclass
class StandardsVerification:
    """Result of verifying a part against a claimed standard"""
    part_number: str
    claimed_standard: str
    manufacturer: str
    verification_status: VerificationStatus
    verified: bool
    concerns: List[str]
    evidence_reviewed: List[str]
    recommendation: str
    testing_required: List[str]
    confidence: float             # 0-1 confidence in assessment
    verification_date: datetime


@dataclass
class StandardsEquivalence:
    """Equivalence mapping between two standards"""
    standard_a: str
    standard_b: str
    equivalent: bool
    reason: str
    comparison: Dict[str, Dict[str, Any]]  # Property comparisons
    interchangeable_in_practice: bool
    notes: str
    exceptions: List[str]


@dataclass
class MarketCertification:
    """Certification requirements for a specific market"""
    market: str
    required_certifications: List[str]
    mandatory: bool
    typical_cost_usd: int
    typical_time_weeks: int
    testing_bodies: List[str]
    notes: str


@dataclass
class CertificationRequirements:
    """Complete certification requirements for target markets"""
    product_type: str
    markets: List[str]
    requirements_by_market: Dict[str, MarketCertification]
    harmonized_standards: List[str]
    estimated_total_cost_usd: int
    estimated_total_time_months: int
    strategy_recommendation: str


@dataclass
class CertificationExplanation:
    """Explanation of differences between certifications"""
    cert_a: str
    cert_b: str
    difference_level: str  # "Minor", "Significant", "Major"
    cert_a_details: Dict[str, str]
    cert_b_details: Dict[str, str]
    practical_implication: str
    common_confusion: str
    recommendation: str


@dataclass
class StandardsQuery:
    """Query for standards information"""
    query_type: str  # "compliance", "equivalence", "requirements", "explanation"
    parameters: Dict[str, Any]
    timestamp: datetime


class ArbiterAgent:
    """
    Agent_17: ARBITER - Standards & Regulatory Compliance Intelligence

    Core responsibilities:
    1. Verify that parts meet claimed standards
    2. Map equivalence between different standards systems
    3. Determine certification requirements for target markets
    4. Explain certification differences and implications
    5. Track standards updates and revisions
    """

    AGENT_ID = "AGENT_17"
    AGENT_NAME = "Standards & Regulatory Compliance"
    AGENT_ALIAS = "ARBITER"

    SUBSCRIBED_TOPICS = [
        "upc.standards.verify",
        "upc.standards.equivalence",
        "upc.standards.requirements",
        "upc.certification.explain",
        "upc.data.part_updated",       # From Agent_1
        "upc.system.directive",         # From Agent_10
    ]

    PUBLISHED_TOPICS = [
        "upc.standards.verified",
        "upc.standards.mapped",
        "upc.certification.required",
        "upc.compliance.alert",
        "upc.qualia.contribution",      # To Agent_4
    ]

    def __init__(self):
        self.standards_database = self._initialize_standards_db()
        self.certification_tracker = self._initialize_certifications()
        self.equivalence_mapper = self._initialize_equivalence_map()
        self.testing_requirements = self._initialize_testing_db()

    def _initialize_standards_db(self) -> Dict[str, StandardDefinition]:
        """Initialize database of known standards"""
        return {
            "ISO 898-1": StandardDefinition(
                standard_id="ISO 898-1",
                name="Mechanical properties of fasteners made of carbon steel and alloy steel - Bolts, screws and studs",
                body=StandardsBody.ISO,
                domain=StandardsDomain.MECHANICAL,
                version="2013",
                description="Specifies mechanical and physical properties of bolts, screws and studs with coarse pitch thread and fine pitch thread",
                key_requirements=[
                    "Tensile strength requirements by property class",
                    "Proof load specifications",
                    "Hardness requirements (HRC/HV)",
                    "Ductility requirements",
                    "Dimensional requirements per ISO 4759-1"
                ],
                test_methods=[
                    "Tensile test per ISO 898-1 Annex A",
                    "Proof load test",
                    "Hardness test per ISO 6508-1 or ISO 6507-1",
                    "Head soundness test",
                    "Surface discontinuity per ISO 6157-1 or ISO 6157-3"
                ],
                supersedes="ISO 898-1:2009",
                harmonized_with=["EN ISO 898-1", "DIN EN ISO 898-1"]
            ),
            "SAE J429": StandardDefinition(
                standard_id="SAE J429",
                name="Mechanical and Material Requirements for Externally Threaded Fasteners",
                body=StandardsBody.SAE,
                domain=StandardsDomain.AUTOMOTIVE,
                version="2014",
                description="Covers chemical, metallurgical, and mechanical requirements for steel externally threaded fasteners",
                key_requirements=[
                    "Grade-specific tensile strength",
                    "Proof load requirements",
                    "Core hardness requirements",
                    "Surface hardness limits",
                    "Decarburization limits"
                ],
                test_methods=[
                    "Tensile strength test",
                    "Proof load test",
                    "Wedge tensile test",
                    "Hardness test",
                    "Surface decarburization examination"
                ],
                supersedes="SAE J429:2011",
                harmonized_with=[]
            ),
            "ASTM F3125": StandardDefinition(
                standard_id="ASTM F3125",
                name="Standard Specification for High Strength Structural Bolts and Assemblies",
                body=StandardsBody.ASTM,
                domain=StandardsDomain.CONSTRUCTION,
                version="2019",
                description="Consolidated standard for structural bolts replacing ASTM A325 and A490",
                key_requirements=[
                    "Tensile strength per grade (Grade A325: 120ksi min, Grade A490: 150ksi min)",
                    "Proof load requirements",
                    "Rotational-capacity testing",
                    "Galvanizing requirements where applicable",
                    "Lot traceability"
                ],
                test_methods=[
                    "Tension testing per ASTM F606",
                    "Hardness testing",
                    "Proof load testing",
                    "Wedge testing",
                    "Rotational-capacity testing"
                ],
                supersedes="ASTM A325, ASTM A490",
                harmonized_with=[]
            ),
            "UL 1004-1": StandardDefinition(
                standard_id="UL 1004-1",
                name="Standard for Rotating Electrical Machines - General Requirements",
                body=StandardsBody.UL,
                domain=StandardsDomain.ELECTRICAL,
                version="2021",
                description="Safety requirements for rotating electrical machines",
                key_requirements=[
                    "Electrical insulation requirements",
                    "Temperature rise limits",
                    "Dielectric voltage-withstand",
                    "Mechanical endurance",
                    "Enclosure requirements"
                ],
                test_methods=[
                    "Dielectric voltage-withstand test",
                    "Temperature test",
                    "Locked-rotor test",
                    "Overload test",
                    "Rain test (where applicable)"
                ],
                supersedes=None,
                harmonized_with=["IEC 60034-1"]
            ),
            "MIL-STD-1312": StandardDefinition(
                standard_id="MIL-STD-1312",
                name="Fastener Test Methods",
                body=StandardsBody.MIL,
                domain=StandardsDomain.AEROSPACE,
                version="1984",
                description="Test methods for threaded fasteners used in military applications",
                key_requirements=[
                    "Tensile strength testing procedures",
                    "Double shear testing",
                    "Stress durability testing",
                    "Stress corrosion testing",
                    "Hydrogen embrittlement testing"
                ],
                test_methods=[
                    "Tensile test (Method 5)",
                    "Double shear test (Method 13)",
                    "Stress durability (Method 10)",
                    "Stress corrosion (Method 11)",
                    "Hydrogen embrittlement (Method 16)"
                ],
                supersedes=None,
                harmonized_with=[]
            ),
            "AS9100": StandardDefinition(
                standard_id="AS9100",
                name="Quality Management Systems - Requirements for Aviation, Space and Defense Organizations",
                body=StandardsBody.SAE,
                domain=StandardsDomain.AEROSPACE,
                version="Rev D (2016)",
                description="Quality management system requirements for aerospace industry",
                key_requirements=[
                    "ISO 9001 base requirements",
                    "Configuration management",
                    "Product safety requirements",
                    "Counterfeit parts prevention",
                    "Risk management",
                    "Special process control"
                ],
                test_methods=[
                    "Internal audit",
                    "Management review",
                    "Process verification",
                    "Product conformity verification",
                    "Supplier monitoring"
                ],
                supersedes="AS9100 Rev C",
                harmonized_with=["EN 9100", "JISQ 9100"]
            ),
        }

    def _initialize_certifications(self) -> Dict[str, Dict]:
        """Initialize certification database"""
        return {
            "UL Listed": {
                "type": CertificationType.PRODUCT,
                "body": "Underwriters Laboratories",
                "meaning": "Complete product tested and approved for safety",
                "mark": "UL in circle",
                "can_be_used": "As standalone product by end user",
                "scope": "Complete assembled product",
                "follow_up": "Factory inspections required",
                "typical_cost_range": (15000, 100000),
                "typical_time_weeks": (8, 16)
            },
            "UL Recognized": {
                "type": CertificationType.COMPONENT,
                "body": "Underwriters Laboratories",
                "meaning": "Component tested for use in larger Listed product",
                "mark": "Backwards UR (Recognized Component Mark)",
                "can_be_used": "Only as part of UL Listed end product",
                "scope": "Component or subassembly only",
                "follow_up": "Factory inspections required",
                "typical_cost_range": (5000, 30000),
                "typical_time_weeks": (4, 10)
            },
            "CE Mark": {
                "type": CertificationType.PRODUCT,
                "body": "European Commission (self-declared or Notified Body)",
                "meaning": "Product meets EU health, safety, and environmental requirements",
                "mark": "CE letters",
                "can_be_used": "Required for sale in European Economic Area",
                "scope": "Complete product per applicable directives",
                "follow_up": "Technical file must be maintained",
                "typical_cost_range": (5000, 50000),
                "typical_time_weeks": (6, 12)
            },
            "ISO 9001": {
                "type": CertificationType.SYSTEM,
                "body": "Accredited certification body",
                "meaning": "Quality management system meets ISO requirements",
                "mark": "Certification body logo + ISO 9001",
                "can_be_used": "Organization-level certification",
                "scope": "Quality management processes",
                "follow_up": "Annual surveillance audits, recertification every 3 years",
                "typical_cost_range": (10000, 50000),
                "typical_time_weeks": (12, 24)
            },
            "AS9100": {
                "type": CertificationType.FACILITY,
                "body": "Accredited aerospace certification body",
                "meaning": "Quality system meets aerospace industry requirements",
                "mark": "Certification body logo + AS9100",
                "can_be_used": "Required for aerospace supply chain",
                "scope": "Aviation, space, and defense operations",
                "follow_up": "Annual surveillance, recertification every 3 years",
                "typical_cost_range": (25000, 100000),
                "typical_time_weeks": (16, 32)
            },
            "IATF 16949": {
                "type": CertificationType.FACILITY,
                "body": "Accredited automotive certification body",
                "meaning": "Quality system meets automotive industry requirements",
                "mark": "Certification body logo + IATF 16949",
                "can_be_used": "Required for automotive OEM supply chain",
                "scope": "Automotive production and service parts",
                "follow_up": "Annual surveillance, recertification every 3 years",
                "typical_cost_range": (20000, 80000),
                "typical_time_weeks": (16, 28)
            },
            "CCC Mark": {
                "type": CertificationType.PRODUCT,
                "body": "China Certification Centre (CNCA)",
                "meaning": "Product meets China's compulsory safety requirements",
                "mark": "CCC letters",
                "can_be_used": "Required for sale in China (for covered products)",
                "scope": "Products in CCC catalog",
                "follow_up": "Factory inspections required",
                "typical_cost_range": (10000, 60000),
                "typical_time_weeks": (12, 20)
            },
        }

    def _initialize_equivalence_map(self) -> Dict[str, Dict]:
        """Initialize standards equivalence mappings"""
        return {
            ("ISO 898-1 Class 10.9", "SAE J429 Grade 8"): {
                "equivalent": False,
                "reason": "Similar but not identical specifications",
                "comparison": {
                    "tensile_strength_mpa": {"ISO 10.9": 1040, "SAE Grade 8": 1034},
                    "proof_load_mpa": {"ISO 10.9": 830, "SAE Grade 8": 827},
                    "hardness_hrc": {"ISO 10.9": "32-39", "SAE Grade 8": "33-39"},
                    "material": {"ISO 10.9": "Carbon/alloy steel", "SAE Grade 8": "Medium carbon alloy steel"},
                    "size_range": {"ISO 10.9": "M1.6-M39", "SAE Grade 8": "1/4\"-1-1/2\""}
                },
                "interchangeable_in_practice": True,
                "notes": "SAE Grade 8 has slightly lower minimum specs but practically equivalent for most applications"
            },
            ("ISO 898-1 Class 8.8", "SAE J429 Grade 5"): {
                "equivalent": False,
                "reason": "Different strength classes",
                "comparison": {
                    "tensile_strength_mpa": {"ISO 8.8": 800, "SAE Grade 5": 827},
                    "proof_load_mpa": {"ISO 8.8": 580, "SAE Grade 5": 586},
                    "hardness_hrc": {"ISO 8.8": "22-32", "SAE Grade 5": "25-34"},
                },
                "interchangeable_in_practice": True,
                "notes": "Grade 5 is slightly stronger but commonly used interchangeably"
            },
            ("DIN 931", "ISO 4014"): {
                "equivalent": True,
                "reason": "DIN 931 was harmonized with ISO 4014",
                "comparison": {
                    "thread_length": {"DIN 931": "Same as ISO", "ISO 4014": "Per formula"},
                    "head_dimensions": {"DIN 931": "Same as ISO", "ISO 4014": "Per ISO 4014"},
                },
                "interchangeable_in_practice": True,
                "notes": "DIN 931 is now identical to ISO 4014 for new production"
            },
            ("ASTM A325", "ASTM F3125 Grade A325"): {
                "equivalent": True,
                "reason": "ASTM A325 was consolidated into F3125",
                "comparison": {
                    "tensile_strength_ksi": {"A325": "120 min", "F3125 A325": "120 min"},
                    "specification": {"A325": "Withdrawn", "F3125 A325": "Current"},
                },
                "interchangeable_in_practice": True,
                "notes": "ASTM A325 specification was withdrawn and replaced by F3125 Grade A325"
            },
            ("IEC 60034-1", "NEMA MG-1"): {
                "equivalent": False,
                "reason": "Different regional standards with different test requirements",
                "comparison": {
                    "insulation_class": {"IEC": "Class F (155C)", "NEMA": "Class F (155C)"},
                    "efficiency_classes": {"IEC": "IE1-IE4", "NEMA": "Standard/Energy Efficient/Premium"},
                    "frame_sizes": {"IEC": "IEC frames", "NEMA": "NEMA frames"},
                    "test_methods": {"IEC": "IEC test procedures", "NEMA": "IEEE test procedures"},
                },
                "interchangeable_in_practice": False,
                "notes": "Motors must be designed and tested to each standard separately"
            },
        }

    def _initialize_testing_db(self) -> Dict[str, List[str]]:
        """Initialize testing requirements database"""
        return {
            "fastener_mechanical": [
                "Tensile test to determine ultimate tensile strength",
                "Proof load test to verify elastic behavior",
                "Hardness test (Rockwell C or Vickers)",
                "Wedge tensile test for head integrity",
                "Dimensional inspection per applicable standard"
            ],
            "fastener_coating": [
                "Coating thickness measurement",
                "Adhesion test (bend or impact)",
                "Salt spray test (hours per spec)",
                "Hydrogen embrittlement test for high-strength",
                "Coefficient of friction verification"
            ],
            "electrical_safety": [
                "Dielectric withstand test",
                "Insulation resistance test",
                "Ground continuity test",
                "Leakage current test",
                "Temperature rise test"
            ],
            "material_verification": [
                "Chemical analysis (spectrometry)",
                "Mechanical properties (tensile test)",
                "Microstructure examination",
                "Non-destructive testing (UT, MT, PT)",
                "Traceability verification"
            ],
        }

    def verify_standard_compliance(
        self,
        part_number: str,
        claimed_standard: str,
        manufacturer: str
    ) -> StandardsVerification:
        """
        Verify that a part actually meets claimed standards.

        Args:
            part_number: Part identifier
            claimed_standard: Standard the part claims to meet
            manufacturer: Part manufacturer

        Returns:
            StandardsVerification with verification status and concerns
        """
        concerns = []
        evidence_reviewed = []
        testing_required = []

        # Check if we know this standard
        standard_def = self.standards_database.get(claimed_standard.split()[0])

        # Assess manufacturer credibility
        manufacturer_lower = manufacturer.lower()
        unknown_manufacturer = any(term in manufacturer_lower for term in
            ["unknown", "generic", "unbranded", "china", "alibaba"])

        if unknown_manufacturer:
            concerns.append("Manufacturer origin may not have rigorous quality control")
            concerns.append("No traceable documentation likely available")
            testing_required.extend([
                "Independent material verification",
                "Full mechanical property testing"
            ])

        # Check for specific standards
        if "898" in claimed_standard or "J429" in claimed_standard:
            # Fastener mechanical standard
            evidence_reviewed.append("Fastener marking verification")

            if "10.9" in claimed_standard or "Grade 8" in claimed_standard:
                concerns.append("High-strength fastener requires traceable heat treatment")
                if unknown_manufacturer:
                    concerns.append("Head marking may be counterfeit - common with imported fasteners")
                    testing_required.append("Hardness test to verify heat treatment")
                    testing_required.append("Tensile test on sample")

            testing_required.extend([
                "Proof load test",
                "Head marking verification",
                "Dimensional check"
            ])

        elif "UL" in claimed_standard:
            # UL certification
            evidence_reviewed.append("UL file number lookup")
            testing_required.append("Verify UL file number on UL website")
            concerns.append("Must verify active UL listing with file number")

        elif "ASTM" in claimed_standard:
            evidence_reviewed.append("Mill certification review")
            testing_required.append("Request and verify mill test report")
            if unknown_manufacturer:
                concerns.append("Mill certification may be falsified")
                testing_required.append("Independent chemical analysis")

        # Determine verification status
        if not concerns:
            status = VerificationStatus.VERIFIED
            verified = True
            confidence = 0.9
            recommendation = "Part appears to meet claimed standard with available evidence"
        elif len(concerns) <= 2 and not unknown_manufacturer:
            status = VerificationStatus.CONDITIONAL
            verified = False
            confidence = 0.6
            recommendation = "Request documentation and verify before critical applications"
        else:
            status = VerificationStatus.UNVERIFIABLE
            verified = False
            confidence = 0.3
            recommendation = "Source from ISO 17025 certified supplier with full traceability"

        return StandardsVerification(
            part_number=part_number,
            claimed_standard=claimed_standard,
            manufacturer=manufacturer,
            verification_status=status,
            verified=verified,
            concerns=concerns,
            evidence_reviewed=evidence_reviewed,
            recommendation=recommendation,
            testing_required=list(set(testing_required)),  # Remove duplicates
            confidence=confidence,
            verification_date=datetime.now()
        )

    def map_standard_equivalence(
        self,
        standard_a: str,
        standard_b: str
    ) -> StandardsEquivalence:
        """
        Map equivalence between different standards systems.

        Args:
            standard_a: First standard
            standard_b: Second standard

        Returns:
            StandardsEquivalence with comparison details
        """
        # Check if we have a direct mapping
        mapping = self.equivalence_mapper.get((standard_a, standard_b))
        if not mapping:
            # Try reverse
            mapping = self.equivalence_mapper.get((standard_b, standard_a))
            if mapping:
                # Swap the comparison keys
                mapping = mapping.copy()

        if mapping:
            return StandardsEquivalence(
                standard_a=standard_a,
                standard_b=standard_b,
                equivalent=mapping["equivalent"],
                reason=mapping["reason"],
                comparison=mapping["comparison"],
                interchangeable_in_practice=mapping["interchangeable_in_practice"],
                notes=mapping["notes"],
                exceptions=[]
            )

        # Generate a generic comparison if no direct mapping
        return StandardsEquivalence(
            standard_a=standard_a,
            standard_b=standard_b,
            equivalent=False,
            reason="No direct equivalence mapping available",
            comparison={
                "note": {
                    standard_a: "Refer to standard document",
                    standard_b: "Refer to standard document"
                }
            },
            interchangeable_in_practice=False,
            notes="Consult both standards documents for detailed comparison. Contact ARBITER for analysis.",
            exceptions=["Application-specific requirements may affect interchangeability"]
        )

    def get_certification_requirements(
        self,
        product_type: str,
        markets: List[str]
    ) -> CertificationRequirements:
        """
        What certifications are needed for a product in target markets?

        Args:
            product_type: Type of product (e.g., "Industrial motor")
            markets: Target markets (e.g., ["USA", "EU", "China"])

        Returns:
            CertificationRequirements with comprehensive breakdown
        """
        requirements_by_market = {}
        total_cost = 0
        max_time = 0

        # Define market-specific requirements by product type
        product_lower = product_type.lower()

        for market in markets:
            market_upper = market.upper()

            if market_upper in ["USA", "US", "UNITED STATES"]:
                if "motor" in product_lower or "electrical" in product_lower:
                    cert = MarketCertification(
                        market="USA",
                        required_certifications=["UL Listed (UL 1004-1)", "NEMA MG-1 compliance"],
                        mandatory=True,
                        typical_cost_usd=35000,
                        typical_time_weeks=12,
                        testing_bodies=["UL", "CSA", "Intertek"],
                        notes="UL listing often required by insurance companies and AHJs"
                    )
                elif "fastener" in product_lower and "structural" in product_lower:
                    cert = MarketCertification(
                        market="USA",
                        required_certifications=["ASTM F3125 compliance", "Mill certification"],
                        mandatory=True,
                        typical_cost_usd=5000,
                        typical_time_weeks=2,
                        testing_bodies=["Independent testing labs"],
                        notes="AISC certified fabricators require F3125 compliance"
                    )
                else:
                    cert = MarketCertification(
                        market="USA",
                        required_certifications=["Product-specific (varies)"],
                        mandatory=False,
                        typical_cost_usd=20000,
                        typical_time_weeks=8,
                        testing_bodies=["UL", "CSA", "Intertek", "TUV"],
                        notes="Requirements vary by product category and industry"
                    )

            elif market_upper in ["EU", "EUROPE", "EUROPEAN UNION"]:
                if "motor" in product_lower or "electrical" in product_lower:
                    cert = MarketCertification(
                        market="EU",
                        required_certifications=["CE Mark", "EN 60034-1 (Low Voltage Directive)"],
                        mandatory=True,
                        typical_cost_usd=25000,
                        typical_time_weeks=10,
                        testing_bodies=["TUV", "SGS", "Bureau Veritas"],
                        notes="CE marking is mandatory; may self-declare for many products"
                    )
                else:
                    cert = MarketCertification(
                        market="EU",
                        required_certifications=["CE Mark", "Applicable EN standards"],
                        mandatory=True,
                        typical_cost_usd=15000,
                        typical_time_weeks=8,
                        testing_bodies=["Notified Bodies", "TUV", "SGS"],
                        notes="CE marking required; specific directives depend on product"
                    )

            elif market_upper in ["CHINA", "CN", "PRC"]:
                if "motor" in product_lower or "electrical" in product_lower:
                    cert = MarketCertification(
                        market="China",
                        required_certifications=["CCC Mark", "GB 755 compliance"],
                        mandatory=True,
                        typical_cost_usd=30000,
                        typical_time_weeks=16,
                        testing_bodies=["CQC", "CCIC"],
                        notes="CCC is compulsory for many electrical products"
                    )
                else:
                    cert = MarketCertification(
                        market="China",
                        required_certifications=["CCC Mark (if applicable)", "GB standards"],
                        mandatory=False,
                        typical_cost_usd=20000,
                        typical_time_weeks=14,
                        testing_bodies=["CQC", "CCIC"],
                        notes="Not all products require CCC; check catalog"
                    )

            else:
                cert = MarketCertification(
                    market=market,
                    required_certifications=["Market-specific requirements"],
                    mandatory=False,
                    typical_cost_usd=15000,
                    typical_time_weeks=10,
                    testing_bodies=["Regional certification bodies"],
                    notes=f"Contact local regulatory authority for {market} requirements"
                )

            requirements_by_market[market] = cert
            total_cost += cert.typical_cost_usd
            max_time = max(max_time, cert.typical_time_weeks)

        # Determine harmonized standards
        harmonized = []
        if "motor" in product_lower:
            harmonized.append("IEC 60034-1 covers most requirements across regions")
        if "fastener" in product_lower:
            harmonized.append("ISO standards generally accepted globally")

        return CertificationRequirements(
            product_type=product_type,
            markets=markets,
            requirements_by_market=requirements_by_market,
            harmonized_standards=harmonized,
            estimated_total_cost_usd=total_cost,
            estimated_total_time_months=max(1, max_time // 4),
            strategy_recommendation="Consider testing to harmonized international standards first to minimize regional retesting"
        )

    def explain_certification_difference(
        self,
        cert_a: str,
        cert_b: str
    ) -> CertificationExplanation:
        """
        Explain the practical difference between certifications.

        Args:
            cert_a: First certification
            cert_b: Second certification

        Returns:
            CertificationExplanation with detailed comparison
        """
        # Get certification details
        cert_a_data = self.certification_tracker.get(cert_a)
        cert_b_data = self.certification_tracker.get(cert_b)

        if not cert_a_data or not cert_b_data:
            return CertificationExplanation(
                cert_a=cert_a,
                cert_b=cert_b,
                difference_level="Unknown",
                cert_a_details={"note": "Certification not in database"},
                cert_b_details={"note": "Certification not in database"},
                practical_implication="Unable to compare - one or both certifications not found",
                common_confusion="Contact ARBITER for specific certification information",
                recommendation="Consult certification body documentation"
            )

        # Determine difference level
        if cert_a_data["type"] != cert_b_data["type"]:
            difference_level = "Significant"
        elif cert_a_data["body"] != cert_b_data["body"]:
            difference_level = "Moderate"
        else:
            difference_level = "Minor"

        # Handle UL Listed vs UL Recognized specifically
        if "UL Listed" in [cert_a, cert_b] and "UL Recognized" in [cert_a, cert_b]:
            return CertificationExplanation(
                cert_a=cert_a,
                cert_b=cert_b,
                difference_level="Significant",
                cert_a_details={
                    "meaning": cert_a_data["meaning"],
                    "can_be_used": cert_a_data["can_be_used"],
                    "mark_appearance": cert_a_data["mark"]
                },
                cert_b_details={
                    "meaning": cert_b_data["meaning"],
                    "can_be_used": cert_b_data["can_be_used"],
                    "mark_appearance": cert_b_data["mark"]
                },
                practical_implication="Recognized components MUST be installed in a Listed enclosure or system. They cannot be used as standalone products.",
                common_confusion="Many assume 'UL Recognized' means the same as 'UL Listed' - it does NOT",
                recommendation="If selling to end users, ensure product is UL Listed. Components can be UL Recognized if integrated into Listed end products."
            )

        return CertificationExplanation(
            cert_a=cert_a,
            cert_b=cert_b,
            difference_level=difference_level,
            cert_a_details={
                "type": cert_a_data["type"].value,
                "meaning": cert_a_data["meaning"],
                "scope": cert_a_data["scope"]
            },
            cert_b_details={
                "type": cert_b_data["type"].value,
                "meaning": cert_b_data["meaning"],
                "scope": cert_b_data["scope"]
            },
            practical_implication=f"{cert_a} and {cert_b} serve different purposes in the certification landscape",
            common_confusion="Different certification types address different aspects (product vs system vs component)",
            recommendation="Determine which certification type is required for your application"
        )

    def get_standard_info(self, standard_id: str) -> Optional[StandardDefinition]:
        """
        Get detailed information about a specific standard.

        Args:
            standard_id: Standard identifier (e.g., "ISO 898-1")

        Returns:
            StandardDefinition if found, None otherwise
        """
        # Try exact match first
        if standard_id in self.standards_database:
            return self.standards_database[standard_id]

        # Try partial match
        for key, value in self.standards_database.items():
            if standard_id.lower() in key.lower():
                return value

        return None

    def get_testing_requirements(
        self,
        part_type: str,
        standard: str
    ) -> List[str]:
        """
        Get testing requirements for verifying compliance.

        Args:
            part_type: Type of part
            standard: Standard to verify against

        Returns:
            List of required tests
        """
        tests = []

        part_lower = part_type.lower()
        standard_lower = standard.lower()

        # Determine test category
        if any(term in part_lower for term in ["fastener", "bolt", "screw", "nut"]):
            tests.extend(self.testing_requirements.get("fastener_mechanical", []))
            if any(term in part_lower for term in ["plated", "coated", "zinc", "galvanized"]):
                tests.extend(self.testing_requirements.get("fastener_coating", []))

        if any(term in part_lower for term in ["motor", "electrical", "switch", "relay"]):
            tests.extend(self.testing_requirements.get("electrical_safety", []))

        if any(term in standard_lower for term in ["material", "alloy", "steel"]):
            tests.extend(self.testing_requirements.get("material_verification", []))

        if not tests:
            tests = [
                "Visual inspection per applicable standard",
                "Dimensional verification",
                "Functional testing per specification",
                "Documentation review"
            ]

        return list(set(tests))  # Remove duplicates

    def check_substitution_compliance(
        self,
        original_standard: str,
        substitute_standard: str,
        application: str
    ) -> Dict[str, Any]:
        """
        Check if a substitution maintains standards compliance.

        Args:
            original_standard: Standard of original part
            substitute_standard: Standard of substitute part
            application: Application context

        Returns:
            Dict with compliance assessment
        """
        equivalence = self.map_standard_equivalence(original_standard, substitute_standard)

        result = {
            "original": original_standard,
            "substitute": substitute_standard,
            "application": application,
            "compliant": equivalence.interchangeable_in_practice,
            "equivalence": equivalence.equivalent,
            "notes": equivalence.notes,
            "warnings": []
        }

        # Add application-specific warnings
        application_lower = application.lower()

        if "structural" in application_lower or "safety" in application_lower:
            result["warnings"].append(
                "Safety-critical application: Verify substitution with qualified engineer"
            )
            result["compliant"] = result["compliant"] and equivalence.equivalent

        if "aerospace" in application_lower or "aviation" in application_lower:
            result["warnings"].append(
                "Aerospace application: May require FAA/DER approval for substitution"
            )
            result["compliant"] = False  # Requires specific approval

        if "medical" in application_lower:
            result["warnings"].append(
                "Medical device: FDA notification may be required for material changes"
            )

        return result


# Demo usage
if __name__ == "__main__":
    agent = ArbiterAgent()

    print("=" * 70)
    print("Agent_17: ARBITER - Standards & Regulatory Compliance Intelligence")
    print("=" * 70)

    # Test 1: Verify standard compliance
    print("\n--- Standards Compliance Verification ---")
    verification = agent.verify_standard_compliance(
        part_number="Generic M10x30 bolt",
        claimed_standard="ISO 898-1 Class 10.9",
        manufacturer="Unknown Chinese"
    )
    print(f"Part: {verification.part_number}")
    print(f"Claimed: {verification.claimed_standard}")
    print(f"Status: {verification.verification_status.value}")
    print(f"Verified: {verification.verified}")
    print(f"Confidence: {verification.confidence:.0%}")
    print("Concerns:")
    for concern in verification.concerns:
        print(f"  - {concern}")
    print(f"Recommendation: {verification.recommendation}")
    print("Testing required:")
    for test in verification.testing_required:
        print(f"  - {test}")

    # Test 2: Map standard equivalence
    print("\n--- Standards Equivalence Mapping ---")
    equivalence = agent.map_standard_equivalence(
        "ISO 898-1 Class 10.9",
        "SAE J429 Grade 8"
    )
    print(f"Comparing: {equivalence.standard_a} vs {equivalence.standard_b}")
    print(f"Equivalent: {equivalence.equivalent}")
    print(f"Reason: {equivalence.reason}")
    print("Property comparison:")
    for prop, values in equivalence.comparison.items():
        print(f"  {prop}:")
        for std, val in values.items():
            print(f"    {std}: {val}")
    print(f"Interchangeable in practice: {equivalence.interchangeable_in_practice}")
    print(f"Notes: {equivalence.notes}")

    # Test 3: Get certification requirements
    print("\n--- Certification Requirements ---")
    requirements = agent.get_certification_requirements(
        product_type="Industrial motor",
        markets=["USA", "EU", "China"]
    )
    print(f"Product: {requirements.product_type}")
    print(f"Markets: {', '.join(requirements.markets)}")
    for market, cert in requirements.requirements_by_market.items():
        print(f"\n{market}:")
        print(f"  Required: {', '.join(cert.required_certifications)}")
        print(f"  Mandatory: {cert.mandatory}")
        print(f"  Est. cost: ${cert.typical_cost_usd:,}")
        print(f"  Est. time: {cert.typical_time_weeks} weeks")
    print(f"\nTotal estimated cost: ${requirements.estimated_total_cost_usd:,}")
    print(f"Total estimated time: {requirements.estimated_total_time_months} months")
    print(f"Strategy: {requirements.strategy_recommendation}")

    # Test 4: Explain certification difference
    print("\n--- Certification Explanation ---")
    explanation = agent.explain_certification_difference(
        "UL Listed",
        "UL Recognized"
    )
    print(f"Comparing: {explanation.cert_a} vs {explanation.cert_b}")
    print(f"Difference level: {explanation.difference_level}")
    print(f"\n{explanation.cert_a}:")
    for key, value in explanation.cert_a_details.items():
        print(f"  {key}: {value}")
    print(f"\n{explanation.cert_b}:")
    for key, value in explanation.cert_b_details.items():
        print(f"  {key}: {value}")
    print(f"\nPractical implication: {explanation.practical_implication}")
    print(f"Common confusion: {explanation.common_confusion}")
    print(f"Recommendation: {explanation.recommendation}")

    # Test 5: Check substitution compliance
    print("\n--- Substitution Compliance Check ---")
    sub_check = agent.check_substitution_compliance(
        original_standard="ISO 898-1 Class 10.9",
        substitute_standard="SAE J429 Grade 8",
        application="Automotive suspension"
    )
    print(f"Original: {sub_check['original']}")
    print(f"Substitute: {sub_check['substitute']}")
    print(f"Application: {sub_check['application']}")
    print(f"Compliant: {sub_check['compliant']}")
    print(f"Notes: {sub_check['notes']}")
    if sub_check["warnings"]:
        print("Warnings:")
        for warning in sub_check["warnings"]:
            print(f"  - {warning}")
