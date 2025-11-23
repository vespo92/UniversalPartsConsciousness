"""
Agent_16: ANTIQUARIAN - Legacy & Obsolete Parts Intelligence

When equipment outlives its parts, knowledge becomes survival.
This agent specializes in finding New Old Stock (NOS), identifying
modern replacements for obsolete components, tracking reproduction
parts, and connecting users with salvage networks.

Domains:
- Vintage automotive (pre-OBD)
- Legacy industrial equipment
- Retro computing and electronics
- Discontinued consumer products
- NOS (New Old Stock) sourcing

"Every part has a story. Some stories ended when production stopped.
I keep those stories alive, finding the parts that time forgot."
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime, date
from decimal import Decimal
import hashlib


class PartCondition(Enum):
    """Condition grades for vintage/used parts"""
    NOS = "nos"                         # New Old Stock - never used, original packaging
    NORS = "nors"                       # New Old Replacement Stock - aftermarket from era
    REBUILT = "rebuilt"                 # Professionally rebuilt to spec
    REFURBISHED = "refurbished"         # Cleaned, tested, ready to use
    USED_GOOD = "used_good"             # Used but good condition
    USED_FAIR = "used_fair"             # Functional but showing wear
    CORE = "core"                       # Rebuildable core
    FOR_PARTS = "for_parts"             # Parts donor only


class PartEra(Enum):
    """Historical eras for vintage parts"""
    PRE_WAR = "pre_war"                 # Before 1945
    POST_WAR = "post_war"               # 1945-1960
    MUSCLE_ERA = "muscle_era"           # 1960-1974
    MALAISE_ERA = "malaise_era"         # 1975-1985
    MODERN_CLASSIC = "modern_classic"   # 1986-2000
    RECENT_OBSOLETE = "recent_obsolete" # 2001-2015
    CURRENT = "current"                 # 2016+


class ObsolescenceReason(Enum):
    """Why a part became obsolete"""
    MANUFACTURER_DISCONTINUED = "manufacturer_discontinued"
    COMPANY_BANKRUPT = "company_bankrupt"
    SUPERSEDED = "superseded"           # Replaced by newer design
    REGULATION = "regulation"           # No longer meets regulations
    MATERIAL_UNAVAILABLE = "material_unavailable"
    LOW_DEMAND = "low_demand"
    TECHNOLOGY_CHANGE = "technology_change"
    MERGER_ACQUISITION = "merger_acquisition"


@dataclass
class NOSSource:
    """Source for New Old Stock parts"""
    source: str                         # Vendor name or platform
    source_type: str                    # "dealer", "ebay", "forum", "estate"
    condition: PartCondition
    price_usd: float
    quantity_available: int
    location: str
    seller_rating: Optional[float]      # 0-100 if applicable
    verification: str                   # How authenticity was verified
    date_code: Optional[str]            # Manufacturing date if known
    notes: str
    listing_url: Optional[str] = None
    shipping_available: bool = True
    international_shipping: bool = False


@dataclass
class ModernReplacement:
    """Modern part that can replace an obsolete one"""
    part_number: str
    manufacturer: str
    compatibility_score: float          # 0-1
    form_factor: str                    # "exact", "requires_modification", "different"
    improvements: List[str]             # How it's better than original
    differences: List[str]              # What's different
    price_usd: float
    availability: str                   # "in_stock", "special_order", etc.
    installation_notes: str
    verified_applications: List[str]    # Where it's been tested


@dataclass
class ReproductionPart:
    """Reproduction of an obsolete part"""
    manufacturer: str
    part_number: str
    quality_rating: str                 # "concours", "oem_quality", "functional", "budget"
    material: str                       # Material used (may differ from original)
    manufacturing_process: str          # "stamped", "cast", "3d_printed", etc.
    price_usd: float
    fit_notes: str
    country_of_origin: str
    includes_hardware: bool
    year_compatibility: str             # e.g., "1967-1969"
    reviews_summary: Optional[str] = None


@dataclass
class SalvageEstimate:
    """Estimate of finding part in salvage"""
    availability_score: float           # 0-1 likelihood of finding
    estimated_yards_with_part: int
    average_price_usd: float
    price_range: Tuple[float, float]
    condition_notes: str
    search_platforms: List[str]
    geographic_concentration: str       # Where most likely to find
    tips: List[str]


@dataclass
class ObsoletePartInfo:
    """Complete information about an obsolete part"""
    original_part_number: str
    manufacturer: str
    description: str
    era: PartEra
    obsolescence_reason: ObsolescenceReason
    last_production_year: Optional[int]
    original_price_usd: Optional[float]
    applications: List[str]
    nos_available: bool
    reproduction_available: bool
    modern_replacement_available: bool
    salvage_likelihood: float           # 0-1
    collector_interest: str             # "high", "medium", "low"


@dataclass
class CrossReferenceResult:
    """Result of cross-referencing obsolete parts"""
    original_part: str
    equivalent_parts: List[Dict]        # Other part numbers for same part
    supersession_chain: List[str]       # Part number evolution
    current_recommendation: str
    notes: str


class AntiquarianAgent:
    """
    Agent_16: ANTIQUARIAN - Legacy & Obsolete Parts Intelligence

    Core responsibilities:
    1. Locate NOS (New Old Stock) parts across multiple sources
    2. Identify modern replacements for obsolete components
    3. Track reproduction parts quality and availability
    4. Connect users with salvage yard networks
    5. Maintain obsolescence knowledge and supersession chains

    Integration Points:
    - Receives from Agent_2 (Oracle): Compatibility queries for vintage parts
    - Sends to Agent_4 (Empath): Historical qualia from vintage usage
    - Receives from Agent_19 (Quartermaster): Supply chain data
    - Sends to Agent_7 (Chronicler): Historical part documentation
    """

    AGENT_ID = "Agent_16"
    AGENT_NAME = "Legacy & Obsolete Parts Intelligence"
    AGENT_ALIAS = "ANTIQUARIAN"

    def __init__(self):
        self.nos_inventory = self._initialize_nos_inventory()
        self.reproduction_catalog = self._initialize_reproduction_catalog()
        self.obsolete_crossref = self._initialize_crossref()
        self.salvage_network = self._initialize_salvage_network()
        self.supersession_chains = self._initialize_supersessions()

    def _initialize_nos_inventory(self) -> Dict[str, List[NOSSource]]:
        """Initialize sample NOS inventory database"""
        return {
            "holley_1850": [
                NOSSource(
                    source="Vintage Carbs USA",
                    source_type="dealer",
                    condition=PartCondition.NOS,
                    price_usd=485.00,
                    quantity_available=3,
                    location="Ohio, USA",
                    seller_rating=98.5,
                    verification="Original box, date codes verified",
                    date_code="1972",
                    notes="Complete with original gaskets and instructions"
                ),
                NOSSource(
                    source="eBay",
                    source_type="ebay",
                    condition=PartCondition.REBUILT,
                    price_usd=350.00,
                    quantity_available=1,
                    location="California, USA",
                    seller_rating=99.2,
                    verification="Photos of rebuild process",
                    date_code=None,
                    notes="Factory rebuilt with modern gaskets, accelerator pump updated"
                ),
            ],
            "rifa_pme271": [
                NOSSource(
                    source="Electronic Goldmine",
                    source_type="dealer",
                    condition=PartCondition.NOS,
                    price_usd=2.50,
                    quantity_available=500,
                    location="Arizona, USA",
                    seller_rating=95.0,
                    verification="Lot purchase from factory closeout",
                    date_code="1985",
                    notes="WARNING: RIFA caps fail with age - recommend modern replacement"
                ),
            ],
            "delco_remy_1107916": [
                NOSSource(
                    source="NOS Parts Company",
                    source_type="dealer",
                    condition=PartCondition.NOS,
                    price_usd=275.00,
                    quantity_available=5,
                    location="Michigan, USA",
                    seller_rating=97.0,
                    verification="GM part number verified",
                    date_code="1969",
                    notes="Original AC Delco alternator for muscle car restoration"
                ),
            ],
        }

    def _initialize_reproduction_catalog(self) -> Dict[str, List[ReproductionPart]]:
        """Initialize reproduction parts catalog"""
        return {
            "1967_mustang_weatherstripping": [
                ReproductionPart(
                    manufacturer="Metro Moulded Parts",
                    part_number="LM 21-J",
                    quality_rating="oem_quality",
                    material="EPDM rubber (better than original neoprene)",
                    manufacturing_process="extruded",
                    price_usd=285.00,
                    fit_notes="Exact reproduction, includes clips. Better longevity than OE.",
                    country_of_origin="USA",
                    includes_hardware=True,
                    year_compatibility="1967-1968",
                    reviews_summary="4.8/5 stars - Excellent fit, premium quality"
                ),
                ReproductionPart(
                    manufacturer="Daniel Carpenter",
                    part_number="C7ZZ-6520530-A",
                    quality_rating="oem_quality",
                    material="EPDM rubber",
                    manufacturing_process="extruded",
                    price_usd=245.00,
                    fit_notes="Good reproduction, minor trimming may be needed",
                    country_of_origin="Taiwan",
                    includes_hardware=True,
                    year_compatibility="1967-1968",
                    reviews_summary="4.5/5 stars - Good value, slight fitment variation"
                ),
            ],
            "sbc_350_timing_chain": [
                ReproductionPart(
                    manufacturer="Cloyes",
                    part_number="9-3100",
                    quality_rating="oem_quality",
                    material="Steel with nylon-coated silent chain",
                    manufacturing_process="precision machined",
                    price_usd=45.00,
                    fit_notes="Direct replacement for all SBC engines 1955-1995",
                    country_of_origin="USA",
                    includes_hardware=False,
                    year_compatibility="1955-1995",
                    reviews_summary="Industry standard replacement"
                ),
            ],
        }

    def _initialize_crossref(self) -> Dict[str, CrossReferenceResult]:
        """Initialize obsolete part cross-references"""
        return {
            "ac_delco_r45ts": CrossReferenceResult(
                original_part="AC Delco R45TS",
                equivalent_parts=[
                    {"number": "Champion RC12YC", "manufacturer": "Champion"},
                    {"number": "NGK BPR6ES", "manufacturer": "NGK"},
                    {"number": "Autolite 3924", "manufacturer": "Autolite"},
                    {"number": "Bosch WR7DC+", "manufacturer": "Bosch"},
                ],
                supersession_chain=["R45T", "R45TS", "R45TSX", "41-110"],
                current_recommendation="AC Delco 41-110 or NGK BPR6ES",
                notes="Original equipment on GM V8s 1974-1995. All equivalents are exact cross."
            ),
            "gm_points_ignition": CrossReferenceResult(
                original_part="Delco-Remy Points/Condenser",
                equivalent_parts=[
                    {"number": "Pertronix Ignitor", "manufacturer": "Pertronix"},
                    {"number": "Crane XR-700", "manufacturer": "Crane"},
                ],
                supersession_chain=["Points", "HEI", "DIS", "Coil-on-plug"],
                current_recommendation="Pertronix Ignitor for stock appearance with electronic reliability",
                notes="Points obsolete since 1975 HEI transition. Pertronix fits inside original distributor."
            ),
        }

    def _initialize_salvage_network(self) -> Dict[str, Dict]:
        """Initialize salvage yard network data"""
        return {
            "car-part.com": {
                "coverage": "USA/Canada",
                "yards_connected": 3500,
                "specialties": ["All vehicles", "Best for common parts"],
                "url": "https://car-part.com"
            },
            "row52.com": {
                "coverage": "USA",
                "yards_connected": 500,
                "specialties": ["Self-service yards", "Pricing visible"],
                "url": "https://row52.com"
            },
            "benzworld_classifieds": {
                "coverage": "Worldwide",
                "yards_connected": None,
                "specialties": ["Mercedes-Benz parts", "Private sellers"],
                "url": "https://www.benzworld.org/classifieds"
            },
            "thesamba": {
                "coverage": "Worldwide",
                "yards_connected": None,
                "specialties": ["VW air-cooled", "Porsche 356/early 911"],
                "url": "https://www.thesamba.com/vw/classifieds"
            },
            "hemmings": {
                "coverage": "USA",
                "yards_connected": None,
                "specialties": ["Classic cars", "NOS parts", "High-end"],
                "url": "https://www.hemmings.com/classifieds"
            },
        }

    def _initialize_supersessions(self) -> Dict[str, List[str]]:
        """Initialize part number supersession chains"""
        return {
            # GM part number evolutions
            "3893010": ["3893010", "340220", "12368062", "19168050"],  # GM SBC oil pump
            "3927186": ["3927186", "10105531", "12561405"],  # GM water pump

            # Ford part number evolutions
            "D0AZ-6261-A": ["D0AZ-6261-A", "E0AZ-6261-A", "F0AZ-6261-A"],  # Ford timing chain

            # Mopar part number evolutions
            "3418858": ["3418858", "3830428", "4120863"],  # Mopar oil pump
        }

    def find_nos_sources(
        self,
        part_description: str,
        acceptable_conditions: Optional[List[PartCondition]] = None,
        max_price: Optional[float] = None
    ) -> List[NOSSource]:
        """
        Find New Old Stock or quality used parts.

        Args:
            part_description: Part name or number to search
            acceptable_conditions: List of acceptable conditions (default: NOS, REBUILT, NORS)
            max_price: Maximum price filter

        Returns:
            List of NOSSource options sorted by price
        """
        if acceptable_conditions is None:
            acceptable_conditions = [
                PartCondition.NOS,
                PartCondition.NORS,
                PartCondition.REBUILT
            ]

        results = []
        search_lower = part_description.lower()

        # Search inventory
        for part_key, sources in self.nos_inventory.items():
            if search_lower in part_key.lower() or part_key.lower() in search_lower:
                for source in sources:
                    if source.condition in acceptable_conditions:
                        if max_price is None or source.price_usd <= max_price:
                            results.append(source)

        # Sort by price
        results.sort(key=lambda x: x.price_usd)
        return results

    def find_modern_replacement(
        self,
        obsolete_part: str,
        critical_specs: Optional[Dict] = None
    ) -> List[ModernReplacement]:
        """
        Find modern parts that can replace obsolete ones.

        Args:
            obsolete_part: Description or part number of obsolete part
            critical_specs: Dict of specifications that must be matched

        Returns:
            List of modern replacement options
        """
        results = []
        part_lower = obsolete_part.lower()

        # RIFA capacitor replacement (famous failure mode)
        if "rifa" in part_lower or "pme271" in part_lower:
            results.append(ModernReplacement(
                part_number="MKP3386",
                manufacturer="Vishay",
                compatibility_score=0.98,
                form_factor="exact",
                improvements=[
                    "Self-healing design - won't explode",
                    "Extended temperature range",
                    "No aging failures",
                    "Meets modern safety standards"
                ],
                differences=["Slightly smaller physical size"],
                price_usd=1.50,
                availability="in_stock",
                installation_notes="Direct replacement for all RIFA PME271 X2 series. Same lead spacing.",
                verified_applications=["Commodore 64", "Amiga", "Apple II", "Various 1980s equipment"]
            ))

        # Generic electrolytic capacitor replacement
        if "electrolytic" in part_lower or "capacitor" in part_lower:
            results.append(ModernReplacement(
                part_number="Series varies",
                manufacturer="Nichicon, Panasonic, Rubycon",
                compatibility_score=0.95,
                form_factor="exact",
                improvements=[
                    "10x longer life (10000hr vs 2000hr)",
                    "Lower ESR",
                    "Better temperature tolerance"
                ],
                differences=["May be physically smaller"],
                price_usd=0.50,
                availability="in_stock",
                installation_notes="Match voltage and capacitance. Modern caps have better specs at same ratings.",
                verified_applications=["Vintage audio", "Computer power supplies", "CRT monitors"]
            ))

        # Points to electronic ignition
        if "points" in part_lower or "ignition" in part_lower:
            results.append(ModernReplacement(
                part_number="Ignitor",
                manufacturer="Pertronix",
                compatibility_score=0.92,
                form_factor="exact",
                improvements=[
                    "No more points adjustment",
                    "More consistent timing",
                    "Better high-RPM performance",
                    "Invisible installation"
                ],
                differences=["Requires 12V source", "Electronic vs mechanical"],
                price_usd=95.00,
                availability="in_stock",
                installation_notes="Fits inside original distributor. Stock appearance maintained.",
                verified_applications=["GM HEI-era vehicles", "Ford Duraspark", "Mopar electronic"]
            ))

        # Carburetor to EFI
        if "carburetor" in part_lower and critical_specs and critical_specs.get("prefer_efi"):
            results.append(ModernReplacement(
                part_number="Sniper EFI",
                manufacturer="Holley",
                compatibility_score=0.85,
                form_factor="requires_modification",
                improvements=[
                    "Self-tuning fuel injection",
                    "Better fuel economy",
                    "Easier starting",
                    "Altitude compensation"
                ],
                differences=[
                    "Requires fuel pump upgrade",
                    "Requires 12V switched power",
                    "Higher initial cost"
                ],
                price_usd=999.00,
                availability="in_stock",
                installation_notes="Bolts to standard 4150 flange. Requires return fuel line.",
                verified_applications=["SBC/BBC", "SBF/BBF", "Mopar"]
            ))

        return results

    def check_reproduction_availability(
        self,
        part_type: str,
        vehicle_or_equipment: str
    ) -> List[ReproductionPart]:
        """
        Check if quality reproductions are available.

        Args:
            part_type: Type of part needed
            vehicle_or_equipment: Application (e.g., "1967 Ford Mustang")

        Returns:
            List of available reproduction parts
        """
        results = []
        combined_search = f"{vehicle_or_equipment} {part_type}".lower()

        for key, repros in self.reproduction_catalog.items():
            if any(term in key.lower() for term in combined_search.split()):
                results.extend(repros)

        # Sort by quality rating
        quality_order = {"concours": 0, "oem_quality": 1, "functional": 2, "budget": 3}
        results.sort(key=lambda x: quality_order.get(x.quality_rating, 99))

        return results

    def estimate_salvage_availability(
        self,
        part: str,
        vehicle_or_equipment: str,
        location: Optional[str] = None
    ) -> SalvageEstimate:
        """
        Estimate likelihood of finding part in salvage network.

        Args:
            part: Part description
            vehicle_or_equipment: Source vehicle/equipment
            location: Geographic location for search

        Returns:
            SalvageEstimate with availability assessment
        """
        # Calculate availability score based on vehicle production numbers and age
        vehicle_lower = vehicle_or_equipment.lower()

        # Base availability - higher production = more salvage
        high_production = ["mustang", "camaro", "civic", "accord", "f150", "silverado", "corolla"]
        medium_production = ["corvette", "m3", "911", "miata"]
        low_production = ["nsx", "supra mkiv", "rx7", "ferrari"]

        if any(v in vehicle_lower for v in high_production):
            base_score = 0.75
            estimated_yards = 25
            avg_price = 150.00
        elif any(v in vehicle_lower for v in medium_production):
            base_score = 0.55
            estimated_yards = 10
            avg_price = 350.00
        elif any(v in vehicle_lower for v in low_production):
            base_score = 0.25
            estimated_yards = 3
            avg_price = 800.00
        else:
            base_score = 0.50
            estimated_yards = 8
            avg_price = 250.00

        # Part type affects availability
        part_lower = part.lower()
        rare_parts = ["ecu", "cluster", "body panel", "interior trim"]
        common_parts = ["alternator", "starter", "water pump", "brake caliper"]

        if any(p in part_lower for p in rare_parts):
            base_score *= 0.6
        elif any(p in part_lower for p in common_parts):
            base_score *= 1.2

        # Determine search platforms
        platforms = ["Car-Part.com"]
        if "bmw" in vehicle_lower or "mercedes" in vehicle_lower:
            platforms.append("BavarianBoard/BenzWorld Classifieds")
        if "vw" in vehicle_lower or "porsche" in vehicle_lower:
            platforms.append("TheSamba.com")
        if "mustang" in vehicle_lower or "corvette" in vehicle_lower:
            platforms.append("Hemmings")
        platforms.append("eBay Motors")
        platforms.append("Facebook Marketplace")

        # Generate tips
        tips = [
            "Call yards directly - not everything is listed online",
            "Check yards in similar climate (rust belt vs dry states)",
            "Ask about whole-car purchases if multiple parts needed"
        ]

        if "transmission" in part_lower or "engine" in part_lower:
            tips.append("Consider rebuilt vs used for drivetrain components")
        if "interior" in part_lower:
            tips.append("Check color code compatibility - fading varies")

        return SalvageEstimate(
            availability_score=min(base_score, 1.0),
            estimated_yards_with_part=estimated_yards,
            average_price_usd=avg_price,
            price_range=(avg_price * 0.5, avg_price * 1.5),
            condition_notes="Typical salvage: 100-200k miles, condition varies",
            search_platforms=platforms,
            geographic_concentration="Southwest US for rust-free, Midwest for higher mileage",
            tips=tips
        )

    def get_supersession_chain(
        self,
        part_number: str
    ) -> Optional[CrossReferenceResult]:
        """
        Get part number supersession history.

        Args:
            part_number: Original or current part number

        Returns:
            CrossReferenceResult with supersession chain if found
        """
        # Direct lookup
        if part_number in self.obsolete_crossref:
            return self.obsolete_crossref[part_number]

        # Search supersession chains
        for orig_part, chain in self.supersession_chains.items():
            if part_number in chain:
                return CrossReferenceResult(
                    original_part=orig_part,
                    equivalent_parts=[],
                    supersession_chain=chain,
                    current_recommendation=chain[-1],
                    notes=f"Part number evolved: {' -> '.join(chain)}"
                )

        return None

    def assess_obsolete_part(
        self,
        part_number: str,
        manufacturer: str,
        description: str
    ) -> ObsoletePartInfo:
        """
        Assess an obsolete part for sourcing options.

        Args:
            part_number: Original part number
            manufacturer: Original manufacturer
            description: Part description

        Returns:
            Complete assessment of sourcing options
        """
        # Check various availability sources
        nos_sources = self.find_nos_sources(part_number) or self.find_nos_sources(description)
        modern_replacements = self.find_modern_replacement(description)
        reproductions = self.check_reproduction_availability(description, "")

        # Determine era based on clues
        era = PartEra.MODERN_CLASSIC  # Default
        if "1960" in description or "muscle" in description.lower():
            era = PartEra.MUSCLE_ERA
        elif "1950" in description or "pre-war" in description.lower():
            era = PartEra.POST_WAR

        return ObsoletePartInfo(
            original_part_number=part_number,
            manufacturer=manufacturer,
            description=description,
            era=era,
            obsolescence_reason=ObsolescenceReason.MANUFACTURER_DISCONTINUED,
            last_production_year=None,
            original_price_usd=None,
            applications=["See application guide"],
            nos_available=len(nos_sources) > 0,
            reproduction_available=len(reproductions) > 0,
            modern_replacement_available=len(modern_replacements) > 0,
            salvage_likelihood=0.5,
            collector_interest="medium"
        )

    def get_agent_info(self) -> Dict:
        """Get agent information and status"""
        return {
            "id": self.AGENT_ID,
            "name": self.AGENT_NAME,
            "alias": self.AGENT_ALIAS,
            "mission": (
                "Preserve mechanical heritage by keeping obsolete parts findable. "
                "When production stops, I ensure knowledge survives - connecting "
                "restorers, collectors, and engineers with the parts time forgot."
            ),
            "capabilities": [
                "NOS (New Old Stock) inventory search across dealers and auctions",
                "Modern replacement identification for obsolete components",
                "Reproduction parts quality tracking and recommendations",
                "Salvage yard network connectivity and availability estimation",
                "Part number supersession chain tracking",
                "Cross-reference database for vintage applications"
            ],
            "domains": [
                "Vintage automotive (pre-OBD era)",
                "Classic muscle cars and imports",
                "Legacy industrial equipment",
                "Retro computing and electronics",
                "Discontinued consumer products"
            ],
            "integrations": {
                "receives_from": [
                    "Agent_2 (Oracle) - Compatibility queries for vintage",
                    "Agent_19 (Quartermaster) - Supply chain updates"
                ],
                "sends_to": [
                    "Agent_4 (Empath) - Historical usage qualia",
                    "Agent_7 (Chronicler) - Part heritage documentation"
                ]
            },
            "data_sources": [
                "NOS dealer networks",
                "Online auction aggregators",
                "Reproduction manufacturer catalogs",
                "Salvage yard databases (Car-Part, Row52)",
                "Enthusiast forums and communities",
                "Manufacturer supersession bulletins"
            ]
        }


# Demo usage
if __name__ == "__main__":
    agent = AntiquarianAgent()

    print("=" * 70)
    print("Agent_16: ANTIQUARIAN - Legacy & Obsolete Parts Intelligence")
    print("=" * 70)

    # Test NOS search
    print("\n--- NOS Search: Holley 1850 Carburetor ---")
    nos_results = agent.find_nos_sources("Holley 1850")
    for src in nos_results:
        print(f"\nSource: {src.source} ({src.source_type})")
        print(f"  Condition: {src.condition.value}")
        print(f"  Price: ${src.price_usd:.2f}")
        print(f"  Qty Available: {src.quantity_available}")
        print(f"  Verification: {src.verification}")
        print(f"  Notes: {src.notes}")

    # Test modern replacement
    print("\n--- Modern Replacement: RIFA Capacitor ---")
    replacements = agent.find_modern_replacement("RIFA PME271 capacitor")
    for rep in replacements:
        print(f"\nReplacement: {rep.manufacturer} {rep.part_number}")
        print(f"  Compatibility: {rep.compatibility_score:.0%}")
        print(f"  Price: ${rep.price_usd:.2f}")
        print("  Improvements:")
        for imp in rep.improvements[:3]:
            print(f"    - {imp}")
        print(f"  Install Notes: {rep.installation_notes}")

    # Test reproduction search
    print("\n--- Reproduction Parts: 1967 Mustang Weatherstripping ---")
    repros = agent.check_reproduction_availability("weatherstripping", "1967 Mustang")
    for repro in repros:
        print(f"\n{repro.manufacturer} {repro.part_number}")
        print(f"  Quality: {repro.quality_rating}")
        print(f"  Price: ${repro.price_usd:.2f}")
        print(f"  Material: {repro.material}")
        print(f"  Fit Notes: {repro.fit_notes}")

    # Test salvage estimate
    print("\n--- Salvage Estimate: E36 M3 Transmission ---")
    salvage = agent.estimate_salvage_availability(
        "5-speed transmission",
        "1995 BMW E36 M3",
        "California"
    )
    print(f"Availability Score: {salvage.availability_score:.0%}")
    print(f"Estimated Yards with Part: {salvage.estimated_yards_with_part}")
    print(f"Average Price: ${salvage.average_price_usd:.2f}")
    print("Search Platforms:")
    for platform in salvage.search_platforms:
        print(f"  - {platform}")
    print("Tips:")
    for tip in salvage.tips:
        print(f"  - {tip}")

    # Print agent info
    print("\n--- Agent Info ---")
    info = agent.get_agent_info()
    print(f"ID: {info['id']}")
    print(f"Alias: {info['alias']}")
    print(f"Mission: {info['mission']}")
