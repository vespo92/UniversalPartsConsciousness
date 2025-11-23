"""
Agent_11: MARINER - Marine & Maritime Parts Intelligence

Marine environments are the harshest on earth for mechanical parts.
Saltwater corrosion, galvanic reactions, and regulatory requirements
create a unique compatibility landscape.

Domains:
- Recreational boats (outboard, inboard, stern drive)
- Commercial marine (workboats, fishing vessels)
- Yacht systems (navigation, electrical, plumbing)
- Marine fasteners (316SS, Monel, bronze compatibility)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class MarineEnvironment(Enum):
    """Marine environment classifications"""
    FRESHWATER = "freshwater"         # Lakes, rivers
    BRACKISH = "brackish"             # Estuaries, river mouths
    SALTWATER = "saltwater"           # Ocean, coastal
    SPLASH_ZONE = "splash_zone"       # Above waterline, constant spray
    SUBMERGED = "submerged"           # Continuous submersion


class MarineMaterial(Enum):
    """Marine-grade materials with galvanic positions"""
    MAGNESIUM = ("magnesium", -1.60, "Sacrificial anode only")
    ZINC = ("zinc", -1.10, "Sacrificial anode, galvanizing")
    ALUMINUM_5052 = ("aluminum_5052", -0.85, "Marine grade aluminum")
    ALUMINUM_6061 = ("aluminum_6061", -0.75, "Structural aluminum")
    CADMIUM = ("cadmium", -0.70, "Obsolete, toxic")
    CARBON_STEEL = ("carbon_steel", -0.60, "Requires protection")
    CAST_IRON = ("cast_iron", -0.55, "Engine blocks")
    STAINLESS_304 = ("304_stainless", -0.08, "Interior, freshwater")
    STAINLESS_316 = ("316_stainless", 0.05, "Marine standard")
    MONEL = ("monel_400", 0.08, "Premium marine")
    BRONZE = ("silicon_bronze", -0.18, "Traditional marine fastener")
    COPPER = ("copper", -0.20, "Plumbing, anti-fouling")
    TITANIUM = ("titanium", 0.10, "Racing, aerospace marine")


@dataclass
class GalvanicRisk:
    """Assessment of galvanic corrosion risk"""
    risk_level: str              # "MINIMAL", "LOW", "MODERATE", "HIGH", "SEVERE"
    voltage_difference_mv: float
    anode_material: str          # Will corrode
    cathode_material: str        # Will be protected
    corrosion_rate: str          # Qualitative rate
    recommendations: List[str]
    zinc_specification: Optional[str]


@dataclass
class MarineFastener:
    """Marine-specific fastener specification"""
    designation: str             # "316SS 1/4-20 x 1"
    material: str
    passivated: bool             # Critical for stainless
    galvanic_position: float
    compatible_materials: List[str]
    incompatible_materials: List[str]
    abyc_compliant: bool
    uscg_approved: bool
    application_notes: str


@dataclass
class MarineEquivalent:
    """Marine equivalent to an automotive/industrial part"""
    automotive_part: str
    marine_equivalent: str
    manufacturer: str
    compatibility_score: float
    differences: List[str]
    why_marine_needed: str
    price_premium_percent: int
    certifications: List[str]


@dataclass
class MarineEngineXref:
    """Cross-reference between marine and automotive engines"""
    marine_engine: str
    manufacturer: str
    base_automotive_engine: str
    shared_parts: List[str]
    marine_specific_parts: List[str]
    never_interchange: List[str]
    notes: str


class MarinerAgent:
    """
    Agent_11: MARINER - Marine & Maritime Parts Intelligence

    Core responsibilities:
    1. Galvanic compatibility checking (THE marine specialty)
    2. Marine engine to automotive cross-reference
    3. Marine-grade equivalent finder
    4. Sacrificial anode sizing
    5. Marine fastener selection
    """

    def __init__(self):
        self.galvanic_series = self._initialize_galvanic_series()
        self.marine_engines = self._initialize_engine_xref()
        self.marine_fasteners = self._initialize_fasteners()

    def _initialize_galvanic_series(self) -> Dict[str, float]:
        """
        Initialize galvanic series for seawater (ASTM G82).
        More negative = more anodic (will corrode first).
        """
        return {
            "magnesium": -1.60,
            "zinc": -1.10,
            "aluminum_5052": -0.85,
            "aluminum_6061": -0.75,
            "cadmium": -0.70,
            "carbon_steel": -0.60,
            "cast_iron": -0.55,
            "304_stainless_active": -0.50,
            "lead": -0.45,
            "tin": -0.40,
            "nickel_active": -0.35,
            "brass": -0.30,
            "copper": -0.20,
            "silicon_bronze": -0.18,
            "90_10_cupronickel": -0.15,
            "70_30_cupronickel": -0.10,
            "304_stainless_passive": -0.08,
            "316_stainless_passive": 0.05,
            "monel_400": 0.08,
            "titanium": 0.10,
            "hastelloy_c": 0.12,
            "silver": 0.15,
            "graphite": 0.25,
            "gold": 0.35,
            "platinum": 0.40,
        }

    def _initialize_engine_xref(self) -> Dict[str, MarineEngineXref]:
        """Initialize marine-to-automotive engine cross-references"""
        return {
            "mercruiser_5.7_mpi": MarineEngineXref(
                marine_engine="Mercruiser 5.7L MPI",
                manufacturer="Mercury Marine",
                base_automotive_engine="GM Vortec 5700 (1996-2002 truck)",
                shared_parts=[
                    "Pistons (identical)",
                    "Connecting rods (identical)",
                    "Crankshaft (identical)",
                    "Cylinder heads (cores)",
                    "Block (identical casting)",
                    "Timing chain/gears",
                    "Oil pump",
                    "Lifters"
                ],
                marine_specific_parts=[
                    "Intake manifold (marine specific)",
                    "Exhaust manifolds (water cooled)",
                    "Water pump (raw water)",
                    "Alternator (ignition protected)",
                    "Starter (ignition protected)",
                    "Carburetor/EFI (marine calibration)",
                    "Distributor (ignition protected)",
                    "Flame arrestor"
                ],
                never_interchange=[
                    "Starter - automotive not ignition protected, FIRE HAZARD",
                    "Alternator - automotive not sealed, will corrode",
                    "Distributor - automotive not ignition protected",
                    "Exhaust manifolds - automotive will BURN through"
                ],
                notes="5.7L MPI uses same block, heads, and rotating assembly as truck 5.7. Save money on internal parts, NEVER on ignition/electrical."
            ),
            "volvo_penta_5.0_gxi": MarineEngineXref(
                marine_engine="Volvo Penta 5.0L GXi",
                manufacturer="Volvo Penta",
                base_automotive_engine="GM L30 5000 Vortec (1999-2007)",
                shared_parts=[
                    "Block (identical)",
                    "Crankshaft",
                    "Pistons/rods",
                    "Cylinder heads (identical)"
                ],
                marine_specific_parts=[
                    "Complete fuel system",
                    "Cooling system",
                    "Electrical system",
                    "Drive adapter"
                ],
                never_interchange=[
                    "Any electrical component",
                    "Fuel system components"
                ],
                notes="Volvo uses Volvo-specific EFI and drive coupling. Internal engine is GM."
            ),
        }

    def _initialize_fasteners(self) -> Dict[str, MarineFastener]:
        """Initialize marine fastener database"""
        return {
            "316ss_shcs": MarineFastener(
                designation="316 Stainless Socket Head Cap Screw",
                material="316_stainless_passive",
                passivated=True,
                galvanic_position=0.05,
                compatible_materials=["316_stainless", "titanium", "monel_400", "fiberglass", "teak"],
                incompatible_materials=["aluminum", "zinc", "carbon_steel"],
                abyc_compliant=True,
                uscg_approved=True,
                application_notes="Standard marine fastener. MUST be passivated. Avoid contact with aluminum without isolation."
            ),
            "silicon_bronze": MarineFastener(
                designation="Silicon Bronze Wood Screw",
                material="silicon_bronze",
                passivated=False,
                galvanic_position=-0.18,
                compatible_materials=["silicon_bronze", "brass", "copper", "wood", "fiberglass"],
                incompatible_materials=["aluminum", "stainless_steel"],
                abyc_compliant=True,
                uscg_approved=True,
                application_notes="Traditional marine fastener for wood. Compatible with copper bottom paint."
            ),
            "monel_bolt": MarineFastener(
                designation="Monel 400 Hex Bolt",
                material="monel_400",
                passivated=False,
                galvanic_position=0.08,
                compatible_materials=["monel_400", "316_stainless", "titanium", "inconel"],
                incompatible_materials=["aluminum", "zinc", "carbon_steel"],
                abyc_compliant=True,
                uscg_approved=True,
                application_notes="Premium marine fastener. Expensive but excellent corrosion resistance."
            ),
        }

    def check_galvanic_compatibility(
        self,
        metal_a: str,
        metal_b: str,
        environment: MarineEnvironment
    ) -> GalvanicRisk:
        """
        Core marine function: Will these two metals destroy each other?

        Args:
            metal_a: First metal (e.g., "316_stainless_passive")
            metal_b: Second metal (e.g., "aluminum_6061")
            environment: Marine environment type

        Returns:
            GalvanicRisk assessment with recommendations
        """
        # Normalize metal names
        metal_a_key = metal_a.lower().replace(" ", "_").replace("-", "_")
        metal_b_key = metal_b.lower().replace(" ", "_").replace("-", "_")

        pos_a = self.galvanic_series.get(metal_a_key, 0.0)
        pos_b = self.galvanic_series.get(metal_b_key, 0.0)

        voltage_diff = abs(pos_a - pos_b) * 1000  # mV

        # Determine anode (more negative = will corrode)
        if pos_a < pos_b:
            anode, cathode = metal_a, metal_b
        else:
            anode, cathode = metal_b, metal_a

        # Environment factor
        env_factors = {
            MarineEnvironment.FRESHWATER: 0.3,
            MarineEnvironment.BRACKISH: 0.6,
            MarineEnvironment.SALTWATER: 1.0,
            MarineEnvironment.SPLASH_ZONE: 1.2,
            MarineEnvironment.SUBMERGED: 0.8,  # Less oxygen
        }
        env_factor = env_factors.get(environment, 1.0)
        effective_voltage = voltage_diff * env_factor

        # Risk assessment
        if effective_voltage < 100:
            risk_level = "MINIMAL"
            corrosion_rate = "Negligible"
        elif effective_voltage < 200:
            risk_level = "LOW"
            corrosion_rate = "Slow, years to notice"
        elif effective_voltage < 350:
            risk_level = "MODERATE"
            corrosion_rate = "Noticeable within 1-2 years"
        elif effective_voltage < 500:
            risk_level = "HIGH"
            corrosion_rate = "Significant within months"
        else:
            risk_level = "SEVERE"
            corrosion_rate = "Rapid destruction within weeks"

        # Recommendations based on risk
        recommendations = []
        zinc_spec = None

        if effective_voltage > 100:
            recommendations.append(f"Isolate {anode} from {cathode} with nylon/plastic washer")
            recommendations.append("Apply dielectric grease to joint")

        if effective_voltage > 200:
            recommendations.append("Consider using same material family for both parts")
            zinc_spec = "MIL-A-18001K (mil-spec zinc anode)"

        if effective_voltage > 350:
            recommendations.append(f"STRONGLY recommend replacing {anode} with material closer to {cathode}")
            recommendations.append("Install sacrificial zinc anode near joint")
            zinc_spec = "MIL-A-18001K Type II (high-capacity zinc)"

        if effective_voltage > 500:
            recommendations.insert(0, "WARNING: This combination will cause RAPID corrosion")
            recommendations.append("Do NOT use these materials together in marine environment")

        return GalvanicRisk(
            risk_level=risk_level,
            voltage_difference_mv=voltage_diff,
            anode_material=anode,
            cathode_material=cathode,
            corrosion_rate=corrosion_rate,
            recommendations=recommendations,
            zinc_specification=zinc_spec
        )

    def find_marine_equivalent(
        self,
        automotive_part: str,
        marine_environment: MarineEnvironment = MarineEnvironment.SALTWATER
    ) -> List[MarineEquivalent]:
        """
        Find marine-rated equivalents for automotive/industrial parts.

        Many boat builders use automotive parts where they shouldn't.
        This finds the proper marine-rated alternative.
        """
        results = []
        part_lower = automotive_part.lower()

        # Alternator
        if "alternator" in part_lower:
            results.append(MarineEquivalent(
                automotive_part=automotive_part,
                marine_equivalent="Balmar 614-100 (100A)",
                manufacturer="Balmar",
                compatibility_score=0.95,
                differences=[
                    "Sealed bearings",
                    "Ignition protected (no sparks)",
                    "316SS hardware",
                    "Marine-grade windings"
                ],
                why_marine_needed="Automotive alternators will corrode and are NOT ignition protected - FIRE HAZARD in engine compartment",
                price_premium_percent=180,
                certifications=["SAE J1171", "USCG 33CFR183"]
            ))
            results.append(MarineEquivalent(
                automotive_part=automotive_part,
                marine_equivalent="Delco 10SI Marine Conversion",
                manufacturer="Various",
                compatibility_score=0.75,
                differences=[
                    "Converted automotive unit",
                    "Added ignition protection",
                    "Marine bearings"
                ],
                why_marine_needed="Budget option, properly converted to meet marine requirements",
                price_premium_percent=80,
                certifications=["SAE J1171"]
            ))

        # Starter
        elif "starter" in part_lower:
            results.append(MarineEquivalent(
                automotive_part=automotive_part,
                marine_equivalent="Marine Power Starter",
                manufacturer="Mercruiser/Volvo OEM",
                compatibility_score=0.98,
                differences=[
                    "Ignition protected",
                    "Corrosion-resistant housing",
                    "Sealed connections"
                ],
                why_marine_needed="Automotive starters can create sparks - EXPLOSION HAZARD with fuel vapors in bilge",
                price_premium_percent=150,
                certifications=["SAE J1171", "USCG 33CFR183", "ISO 8846"]
            ))

        # Generic fastener
        elif "bolt" in part_lower or "screw" in part_lower or "fastener" in part_lower:
            if "stainless" not in part_lower or "304" in part_lower:
                results.append(MarineEquivalent(
                    automotive_part=automotive_part,
                    marine_equivalent="316 Stainless equivalent",
                    manufacturer="Various",
                    compatibility_score=0.90,
                    differences=[
                        "316SS vs 304SS or zinc plated",
                        "Molybdenum content prevents pitting",
                        "Passivated surface"
                    ],
                    why_marine_needed="304SS pits in saltwater, zinc plating dissolves rapidly",
                    price_premium_percent=40,
                    certifications=["ABYC H-27"]
                ))

        return results

    def cross_reference_marine_engine(
        self,
        engine_brand: str,
        engine_model: str
    ) -> Optional[MarineEngineXref]:
        """
        Cross-reference marine engine to automotive base.
        Reveals shared parts for cost savings.
        """
        key = f"{engine_brand.lower()}_{engine_model.lower().replace(' ', '_').replace('.', '_')}"

        # Try to find exact match
        if key in self.marine_engines:
            return self.marine_engines[key]

        # Try partial match
        for db_key, xref in self.marine_engines.items():
            if engine_brand.lower() in db_key and any(
                part in engine_model.lower()
                for part in ["5.7", "5.0", "4.3", "350", "305"]
            ):
                return xref

        return None

    def calculate_zinc_anode_size(
        self,
        hull_material: str,
        wetted_area_sqft: float,
        propeller_material: str,
        shaft_material: str,
        environment: MarineEnvironment
    ) -> Dict:
        """
        Calculate required sacrificial zinc anode sizing.

        Proper anode sizing prevents galvanic corrosion of
        expensive underwater hardware.
        """
        # Base zinc area required (1% rule for aluminum, 2% for steel)
        if "aluminum" in hull_material.lower():
            required_zinc_sqin = wetted_area_sqft * 144 * 0.01  # 1% for aluminum
            hull_note = "Aluminum hulls require careful anode sizing"
        else:
            required_zinc_sqin = wetted_area_sqft * 144 * 0.02  # 2% for fiberglass/steel
            hull_note = "Standard zinc sizing for fiberglass/steel"

        # Environment factor
        env_factors = {
            MarineEnvironment.FRESHWATER: 0.3,
            MarineEnvironment.BRACKISH: 0.7,
            MarineEnvironment.SALTWATER: 1.0,
        }
        env_factor = env_factors.get(environment, 1.0)
        required_zinc_sqin *= env_factor

        # Propeller/shaft considerations
        prop_note = ""
        if "bronze" in propeller_material.lower():
            required_zinc_sqin *= 1.2
            prop_note = "Bronze propeller requires additional zinc"
        elif "stainless" in propeller_material.lower():
            required_zinc_sqin *= 1.3
            prop_note = "Stainless propeller requires more zinc than bronze"

        # Standard anode sizes
        anodes = {
            "small_hull": {"size": "1 lb hull zinc", "area_sqin": 12, "part": "CM-821629"},
            "medium_hull": {"size": "2.5 lb hull zinc", "area_sqin": 28, "part": "CM-821630"},
            "large_hull": {"size": "5 lb hull zinc", "area_sqin": 45, "part": "CM-821631"},
            "shaft_1": {"size": "1\" shaft zinc", "area_sqin": 8, "part": "CM-55989"},
            "prop_nut": {"size": "Prop nut zinc", "area_sqin": 6, "part": "Various"},
        }

        # Calculate number of anodes needed
        recommended = []
        remaining = required_zinc_sqin

        # Shaft anode (always recommended)
        recommended.append({
            "type": "Shaft zinc",
            "quantity": 1,
            "part": "CM-55989 or equivalent",
            "notes": "Replace when 50% depleted"
        })
        remaining -= 8

        # Hull anodes
        if remaining > 0:
            large_count = int(remaining / 45)
            remaining -= large_count * 45
            if large_count > 0:
                recommended.append({
                    "type": "5 lb hull zinc",
                    "quantity": large_count,
                    "part": "CM-821631",
                    "notes": "Mount on hull below waterline"
                })

            medium_count = int(remaining / 28)
            remaining -= medium_count * 28
            if medium_count > 0:
                recommended.append({
                    "type": "2.5 lb hull zinc",
                    "quantity": medium_count,
                    "part": "CM-821630",
                    "notes": "Mount on hull below waterline"
                })

            if remaining > 0:
                recommended.append({
                    "type": "1 lb hull zinc",
                    "quantity": max(1, int(remaining / 12)),
                    "part": "CM-821629",
                    "notes": "Trim tab or small area"
                })

        return {
            "required_zinc_area_sqin": round(required_zinc_sqin, 1),
            "environment": environment.value,
            "hull_notes": hull_note,
            "propeller_notes": prop_note,
            "recommended_anodes": recommended,
            "inspection_interval": "Monthly in saltwater, quarterly in freshwater",
            "replacement_threshold": "Replace when 50% depleted"
        }


# Demo usage
if __name__ == "__main__":
    agent = MarinerAgent()

    print("=" * 60)
    print("Agent_11: MARINER - Marine Parts Intelligence")
    print("=" * 60)

    # Test galvanic compatibility
    print("\n--- Galvanic Compatibility Check ---")
    risk = agent.check_galvanic_compatibility(
        "316_stainless_passive",
        "aluminum_6061",
        MarineEnvironment.SALTWATER
    )
    print(f"Materials: 316SS + 6061 Aluminum")
    print(f"Risk Level: {risk.risk_level}")
    print(f"Voltage Difference: {risk.voltage_difference_mv:.0f} mV")
    print(f"Anode (will corrode): {risk.anode_material}")
    print(f"Corrosion Rate: {risk.corrosion_rate}")
    print("Recommendations:")
    for rec in risk.recommendations:
        print(f"  - {rec}")

    # Test marine engine cross-reference
    print("\n--- Marine Engine Cross-Reference ---")
    xref = agent.cross_reference_marine_engine("Mercruiser", "5.7 MPI")
    if xref:
        print(f"Marine: {xref.marine_engine}")
        print(f"Automotive Base: {xref.base_automotive_engine}")
        print("Shared parts (save money):")
        for part in xref.shared_parts[:5]:
            print(f"  - {part}")
        print("NEVER interchange:")
        for part in xref.never_interchange[:3]:
            print(f"  - {part}")

    # Test marine equivalent finder
    print("\n--- Marine Equivalent Finder ---")
    equivalents = agent.find_marine_equivalent("GM alternator 10SI")
    for eq in equivalents:
        print(f"\nAutomotive: {eq.automotive_part}")
        print(f"Marine equivalent: {eq.marine_equivalent}")
        print(f"Why needed: {eq.why_marine_needed}")
        print(f"Price premium: +{eq.price_premium_percent}%")

    # Test zinc anode calculation
    print("\n--- Zinc Anode Sizing ---")
    zinc = agent.calculate_zinc_anode_size(
        hull_material="fiberglass",
        wetted_area_sqft=150,
        propeller_material="bronze",
        shaft_material="stainless",
        environment=MarineEnvironment.SALTWATER
    )
    print(f"Required zinc area: {zinc['required_zinc_area_sqin']} sq.in")
    print("Recommended anodes:")
    for anode in zinc['recommended_anodes']:
        print(f"  - {anode['quantity']}x {anode['type']}: {anode['part']}")
