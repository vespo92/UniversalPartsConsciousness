"""
Marine Standards Database

Marine equipment must meet specific standards for safety and regulatory
compliance. This module tracks ABYC, USCG, ISO, Lloyd's, and other
marine standards.

Key Standards:
- SAE J1171: Ignition Protection
- ISO 8846: Electrical Ignition Protection
- ABYC E-11: AC and DC Electrical Systems
- ABYC H-27: Fuel Systems
- USCG 33 CFR 183: Safety Standards for Recreational Boats
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class StandardBody(Enum):
    """Standards organizations for marine equipment"""
    ABYC = "American Boat and Yacht Council"
    USCG = "United States Coast Guard"
    ISO = "International Organization for Standardization"
    SAE = "Society of Automotive Engineers"
    LLOYD = "Lloyd's Register"
    NMMA = "National Marine Manufacturers Association"
    CE = "European Conformity"
    DNV = "Det Norske Veritas"
    ABS = "American Bureau of Shipping"
    NFPA = "National Fire Protection Association"


class CertificationLevel(Enum):
    """Certification requirement levels"""
    MANDATORY = "mandatory"           # Required by law/regulation
    RECOMMENDED = "recommended"       # Industry best practice
    OPTIONAL = "optional"             # Available but not required
    VOLUNTARY = "voluntary"           # Self-certification


@dataclass
class MarineStandard:
    """A marine standard or specification"""
    designation: str           # e.g., "ABYC E-11"
    title: str
    body: StandardBody
    version: str
    year: int
    scope: str
    key_requirements: List[str]
    applies_to: List[str]      # Equipment types
    level: CertificationLevel
    related_standards: List[str]
    testing_required: List[str]


@dataclass
class MarineCertification:
    """Certification status for marine equipment"""
    standard: str
    certified: bool
    certification_number: Optional[str]
    testing_lab: Optional[str]
    expiration_date: Optional[str]
    scope_limitations: List[str]


@dataclass
class MarineFastener:
    """Marine-specific fastener specification with standards compliance"""
    designation: str             # "316SS 1/4-20 x 1 SHCS"
    material: str
    grade: str
    thread_spec: str
    length: str
    head_type: str

    # Material properties
    passivated: bool
    galvanic_position: float
    tensile_strength_psi: int
    proof_load_psi: int

    # Compatibility
    compatible_materials: List[str]
    incompatible_materials: List[str]

    # Certifications
    abyc_compliant: bool
    uscg_approved: bool
    iso_standard: Optional[str]
    mil_spec: Optional[str]

    # Application guidance
    max_immersion_depth_ft: Optional[int]
    torque_spec_ft_lbs: Optional[float]
    application_notes: str


class MarineStandardsDatabase:
    """
    Database of marine standards and compliance requirements.

    Covers:
    - Electrical standards (E-11, ignition protection)
    - Fuel system standards (H-27)
    - Fastener standards
    - Safety equipment standards
    - Hull and structure standards
    """

    def __init__(self):
        self.standards: Dict[str, MarineStandard] = self._build_standards_db()
        self.fasteners: Dict[str, MarineFastener] = self._build_fastener_db()

    def _build_standards_db(self) -> Dict[str, MarineStandard]:
        """Build the marine standards database"""
        return {
            "abyc_e11": MarineStandard(
                designation="ABYC E-11",
                title="AC and DC Electrical Systems on Boats",
                body=StandardBody.ABYC,
                version="2022",
                year=2022,
                scope="All AC and DC electrical systems on recreational boats",
                key_requirements=[
                    "Wire sizing based on ampacity and voltage drop",
                    "Overcurrent protection at source",
                    "Ignition protection in engine compartments",
                    "Proper grounding and bonding",
                    "Shore power inlet requirements",
                    "Battery installation requirements",
                ],
                applies_to=[
                    "Wiring and cables",
                    "Circuit breakers and fuses",
                    "Switches and panels",
                    "Batteries",
                    "Shore power systems",
                    "Generators",
                ],
                level=CertificationLevel.RECOMMENDED,
                related_standards=["ISO 13297", "USCG 33 CFR 183"],
                testing_required=["Continuity", "Insulation resistance", "Polarity"],
            ),

            "sae_j1171": MarineStandard(
                designation="SAE J1171",
                title="External Ignition Protection of Marine Electrical Devices",
                body=StandardBody.SAE,
                version="2020",
                year=2020,
                scope="Ignition protection for electrical devices in marine engine compartments",
                key_requirements=[
                    "No external sparking or arcing",
                    "Sealed construction for potential ignition sources",
                    "Temperature rise limits",
                    "Testing in flammable atmosphere",
                    "Marking requirements",
                ],
                applies_to=[
                    "Starters",
                    "Alternators",
                    "Distributors",
                    "Ignition coils",
                    "Electric fuel pumps",
                    "Blower motors",
                ],
                level=CertificationLevel.MANDATORY,
                related_standards=["ISO 8846", "USCG 33 CFR 183.410"],
                testing_required=[
                    "Explosive atmosphere test",
                    "Surface temperature test",
                    "Environmental cycling",
                ],
            ),

            "iso_8846": MarineStandard(
                designation="ISO 8846",
                title="Small craft - Electrical devices - Protection against ignition of surrounding flammable gases",
                body=StandardBody.ISO,
                version="1990",
                year=1990,
                scope="International standard for ignition protection",
                key_requirements=[
                    "Equivalent to SAE J1171",
                    "European CE marking basis",
                    "Testing requirements",
                ],
                applies_to=[
                    "All electrical devices in engine compartments",
                ],
                level=CertificationLevel.MANDATORY,
                related_standards=["SAE J1171"],
                testing_required=["Explosive gas atmosphere test"],
            ),

            "abyc_h27": MarineStandard(
                designation="ABYC H-27",
                title="Fuel Systems",
                body=StandardBody.ABYC,
                version="2021",
                year=2021,
                scope="Gasoline and diesel fuel systems on recreational boats",
                key_requirements=[
                    "Fuel tank construction and installation",
                    "Fuel line material and routing",
                    "Fuel system grounding/bonding",
                    "Vapor containment",
                    "Fuel fill and vent requirements",
                    "Carburetor flame arrestor requirement",
                ],
                applies_to=[
                    "Fuel tanks",
                    "Fuel lines and fittings",
                    "Carburetors",
                    "Fuel injection systems",
                    "Fuel pumps",
                ],
                level=CertificationLevel.MANDATORY,
                related_standards=["USCG 33 CFR 183.500"],
                testing_required=["Pressure testing", "Fire resistance"],
            ),

            "uscg_33cfr183": MarineStandard(
                designation="USCG 33 CFR 183",
                title="Boats and Associated Equipment - Safety Standards",
                body=StandardBody.USCG,
                version="Current",
                year=2023,
                scope="Federal safety requirements for recreational boats",
                key_requirements=[
                    "Electrical system requirements (Subpart I)",
                    "Fuel system requirements (Subpart J)",
                    "Flotation requirements",
                    "Capacity labeling",
                    "Navigation lights",
                    "Ventilation",
                ],
                applies_to=[
                    "All recreational boats sold in USA",
                    "Boat manufacturers",
                    "Marine equipment manufacturers",
                ],
                level=CertificationLevel.MANDATORY,
                related_standards=["ABYC E-11", "ABYC H-27"],
                testing_required=["Manufacturer certification required"],
            ),

            "abyc_h33": MarineStandard(
                designation="ABYC H-33",
                title="Diesel Engines",
                body=StandardBody.ABYC,
                version="2019",
                year=2019,
                scope="Diesel engine installation in recreational boats",
                key_requirements=[
                    "Fuel system requirements",
                    "Exhaust system requirements",
                    "Cooling system requirements",
                    "Ventilation",
                ],
                applies_to=[
                    "Diesel engines",
                    "Diesel fuel systems",
                ],
                level=CertificationLevel.RECOMMENDED,
                related_standards=["ISO 8178"],
                testing_required=["Installation inspection"],
            ),

            "abyc_a27": MarineStandard(
                designation="ABYC A-27",
                title="Alternating Current (AC) Electrical Systems on Boats",
                body=StandardBody.ABYC,
                version="2021",
                year=2021,
                scope="Shore power and generator AC systems",
                key_requirements=[
                    "GFCI/ELCI protection",
                    "Shore power inlet requirements",
                    "Isolation transformer options",
                    "Generator installation",
                ],
                applies_to=[
                    "Shore power systems",
                    "Generators",
                    "Inverters",
                ],
                level=CertificationLevel.RECOMMENDED,
                related_standards=["ABYC E-11"],
                testing_required=["Ground fault testing", "Polarity verification"],
            ),
        }

    def _build_fastener_db(self) -> Dict[str, MarineFastener]:
        """Build marine fastener specifications database"""
        return {
            "316ss_shcs_1/4-20": MarineFastener(
                designation="316SS 1/4-20 Socket Head Cap Screw",
                material="316 Stainless Steel",
                grade="ASTM F593 Group 2",
                thread_spec="1/4-20 UNC",
                length="Various",
                head_type="Socket Head Cap Screw",
                passivated=True,
                galvanic_position=0.05,
                tensile_strength_psi=75000,
                proof_load_psi=45000,
                compatible_materials=[
                    "316 Stainless Steel",
                    "Titanium",
                    "Monel",
                    "Fiberglass",
                    "Teak (with sealer)",
                ],
                incompatible_materials=[
                    "Aluminum (without isolation)",
                    "Zinc",
                    "Carbon steel",
                    "Graphite/carbon fiber (direct contact)",
                ],
                abyc_compliant=True,
                uscg_approved=True,
                iso_standard="ISO 3506-1",
                mil_spec=None,
                max_immersion_depth_ft=None,
                torque_spec_ft_lbs=6.25,
                application_notes="Standard marine fastener. MUST be passivated. Use anti-seize on threads. Isolate from aluminum with nylon washers.",
            ),

            "316ss_hex_bolt_3/8-16": MarineFastener(
                designation="316SS 3/8-16 Hex Bolt",
                material="316 Stainless Steel",
                grade="ASTM F593 Group 2",
                thread_spec="3/8-16 UNC",
                length="Various",
                head_type="Hex Head",
                passivated=True,
                galvanic_position=0.05,
                tensile_strength_psi=75000,
                proof_load_psi=45000,
                compatible_materials=[
                    "316 Stainless Steel",
                    "Titanium",
                    "Monel",
                    "Fiberglass",
                ],
                incompatible_materials=[
                    "Aluminum",
                    "Zinc",
                    "Carbon steel",
                ],
                abyc_compliant=True,
                uscg_approved=True,
                iso_standard="ISO 3506-1",
                mil_spec=None,
                max_immersion_depth_ft=None,
                torque_spec_ft_lbs=15,
                application_notes="General marine hardware. Hex head allows higher torque than socket head.",
            ),

            "silicon_bronze_wood_screw": MarineFastener(
                designation="Silicon Bronze Wood Screw",
                material="Silicon Bronze C65500",
                grade="ASTM B98",
                thread_spec="Wood screw threads",
                length="Various",
                head_type="Flat head or oval head",
                passivated=False,
                galvanic_position=-0.18,
                tensile_strength_psi=70000,
                proof_load_psi=None,
                compatible_materials=[
                    "Wood",
                    "Copper",
                    "Brass",
                    "Bronze",
                    "Fiberglass",
                ],
                incompatible_materials=[
                    "Aluminum",
                    "Stainless steel",
                    "Zinc",
                ],
                abyc_compliant=True,
                uscg_approved=True,
                iso_standard=None,
                mil_spec=None,
                max_immersion_depth_ft=None,
                torque_spec_ft_lbs=None,
                application_notes="Traditional marine fastener for wood construction. Compatible with copper anti-fouling paint. Pre-drill required.",
            ),

            "monel_k500_bolt": MarineFastener(
                designation="Monel K-500 Hex Bolt",
                material="Monel K-500",
                grade="AMS 4676",
                thread_spec="Various",
                length="Various",
                head_type="Hex Head",
                passivated=False,
                galvanic_position=0.10,
                tensile_strength_psi=145000,
                proof_load_psi=100000,
                compatible_materials=[
                    "Monel",
                    "316 Stainless Steel",
                    "Titanium",
                    "Inconel",
                ],
                incompatible_materials=[
                    "Aluminum",
                    "Zinc",
                    "Carbon steel",
                ],
                abyc_compliant=True,
                uscg_approved=True,
                iso_standard=None,
                mil_spec="QQ-N-286",
                max_immersion_depth_ft=1000,
                torque_spec_ft_lbs=None,
                application_notes="Premium marine fastener. Excellent corrosion resistance and strength. Used for propeller shafts and critical hardware.",
            ),

            "316ss_self_tapping": MarineFastener(
                designation="316SS Self-Tapping Screw",
                material="316 Stainless Steel",
                grade="ASTM F593",
                thread_spec="Self-tapping",
                length="Various",
                head_type="Pan head or flat head",
                passivated=True,
                galvanic_position=0.05,
                tensile_strength_psi=75000,
                proof_load_psi=None,
                compatible_materials=[
                    "Fiberglass",
                    "316 Stainless Steel",
                    "Aluminum (with isolation)",
                ],
                incompatible_materials=[
                    "Aluminum (direct)",
                    "Carbon steel",
                ],
                abyc_compliant=True,
                uscg_approved=True,
                iso_standard=None,
                mil_spec=None,
                max_immersion_depth_ft=None,
                torque_spec_ft_lbs=None,
                application_notes="For fiberglass and thin metal. Do not over-torque in fiberglass. Use backing plate for load-bearing.",
            ),
        }

    def get_standard(self, designation: str) -> Optional[MarineStandard]:
        """Get a standard by designation"""
        key = designation.lower().replace(" ", "_").replace("-", "_")
        return self.standards.get(key)

    def get_standards_for_equipment(
        self,
        equipment_type: str
    ) -> List[MarineStandard]:
        """Find all standards applicable to an equipment type"""
        matching = []
        equipment_lower = equipment_type.lower()

        for standard in self.standards.values():
            for applies in standard.applies_to:
                if equipment_lower in applies.lower() or applies.lower() in equipment_lower:
                    matching.append(standard)
                    break

        return matching

    def check_ignition_protection_required(
        self,
        component: str,
        location: str
    ) -> Dict:
        """
        Check if a component requires ignition protection.

        Ignition protection is required for electrical components
        in gasoline engine compartments.
        """
        requires_protection = False
        reason = ""
        standard = ""

        location_lower = location.lower()
        component_lower = component.lower()

        # Engine compartment requires ignition protection
        if any(loc in location_lower for loc in ["engine", "bilge", "fuel"]):
            # Check component type
            protected_components = [
                "starter", "alternator", "distributor", "coil",
                "fuel pump", "blower", "motor", "switch", "relay"
            ]

            for comp in protected_components:
                if comp in component_lower:
                    requires_protection = True
                    reason = f"{component} in {location} can create sparks that ignite fuel vapors"
                    standard = "SAE J1171 / ISO 8846 / USCG 33 CFR 183.410"
                    break

        if not requires_protection:
            # Outside engine compartment generally doesn't require
            reason = f"{component} in {location} typically does not require ignition protection"
            standard = "Verify with ABYC E-11 for specific requirements"

        return {
            "requires_ignition_protection": requires_protection,
            "reason": reason,
            "applicable_standard": standard,
            "certified_marking": "SAE J1171 or ISO 8846" if requires_protection else None,
            "consequences_of_non_compliance": "Fire or explosion risk from fuel vapors" if requires_protection else None,
        }

    def get_fastener(self, designation: str) -> Optional[MarineFastener]:
        """Get fastener specification by designation"""
        # Try exact match first
        for key, fastener in self.fasteners.items():
            if designation.lower() in fastener.designation.lower():
                return fastener
            if designation.lower() in key:
                return fastener
        return None

    def recommend_fastener_for_application(
        self,
        base_material: str,
        environment: str,
        load_type: str = "static"
    ) -> List[MarineFastener]:
        """
        Recommend fasteners for a specific application.

        Args:
            base_material: Material being fastened (aluminum, fiberglass, etc.)
            environment: saltwater, freshwater, etc.
            load_type: static, dynamic, vibration

        Returns:
            List of suitable fasteners sorted by suitability
        """
        suitable = []
        base_lower = base_material.lower()

        for fastener in self.fasteners.values():
            compatible = False

            # Check compatibility with base material
            for comp_mat in fastener.compatible_materials:
                if base_lower in comp_mat.lower() or comp_mat.lower() in base_lower:
                    compatible = True
                    break

            # Check it's not incompatible
            for incomp_mat in fastener.incompatible_materials:
                if base_lower in incomp_mat.lower():
                    compatible = False
                    break

            if compatible:
                suitable.append(fastener)

        return suitable

    def get_certification_requirements(
        self,
        product_type: str,
        market: str = "USA"
    ) -> Dict:
        """
        Get certification requirements for a marine product.

        Args:
            product_type: Type of product (electrical, fuel system, etc.)
            market: Target market (USA, EU, International)

        Returns:
            Dictionary of required certifications
        """
        requirements = {
            "mandatory": [],
            "recommended": [],
            "market": market,
            "product_type": product_type,
        }

        product_lower = product_type.lower()

        # Electrical products
        if any(term in product_lower for term in ["electrical", "starter", "alternator", "pump"]):
            if market == "USA":
                requirements["mandatory"].extend([
                    "USCG 33 CFR 183 (if in engine compartment)",
                    "SAE J1171 (ignition protection)",
                ])
                requirements["recommended"].extend([
                    "ABYC E-11 compliance",
                    "UL Marine listing",
                ])
            elif market == "EU":
                requirements["mandatory"].extend([
                    "CE Mark",
                    "ISO 8846 (ignition protection)",
                ])

        # Fuel system
        if any(term in product_lower for term in ["fuel", "tank", "carburetor"]):
            if market == "USA":
                requirements["mandatory"].extend([
                    "USCG 33 CFR 183 Subpart J",
                ])
                requirements["recommended"].extend([
                    "ABYC H-27 compliance",
                ])

        return requirements
