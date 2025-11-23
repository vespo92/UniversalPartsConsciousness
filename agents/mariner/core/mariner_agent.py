"""
Agent_11: MARINER - Marine & Maritime Parts Intelligence

The Warden of Mechanical Heritage in Hostile Saltwater Environments.

This is the core orchestration module that coordinates all MARINER capabilities:
- Galvanic corrosion analysis
- Marine engine cross-reference
- Marine-grade equivalent finder
- Sacrificial anode sizing
- Marine standards compliance

Integration Points:
- Agent_2 (ORACLE): Enhanced compatibility with galvanic data
- Agent_4 (EMPATH): Collect qualia from marine experiences
- Agent_9 (BRIDGE): Integration architecture
- Agent_18 (ALCHEMIST): Material science collaboration
- Agent_20 (DETECTIVE): Failure analysis for marine failures
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum

from ..galvanic.corrosion_calculator import (
    GalvanicCorrosionCalculator,
    GalvanicRisk,
    RiskLevel,
)
from ..galvanic.material_series import (
    GalvanicSeries,
    MarineEnvironment,
    MarineMaterial,
)
from ..engines.engine_crossref import (
    MarineEngineCrossReference,
    MarineEngineXref,
    EnginePartCategory,
)
from ..standards.marine_standards import (
    MarineStandardsDatabase,
    MarineFastener,
)
from ..anode.anode_calculator import (
    SacrificialAnodeCalculator,
    AnodeSystemAssessment,
    AnodeType,
)


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
class MarineCompatibilityReport:
    """Complete compatibility report for marine application"""
    query: str
    galvanic_risk: Optional[GalvanicRisk]
    engine_crossref: Optional[MarineEngineXref]
    marine_equivalents: List[MarineEquivalent]
    anode_requirements: Optional[AnodeSystemAssessment]
    standards_compliance: Dict[str, Any]
    warnings: List[str]
    recommendations: List[str]


class MarinerAgent:
    """
    Agent_11: MARINER - Marine & Maritime Parts Intelligence

    The definitive source for marine parts compatibility, galvanic corrosion
    analysis, and marine-to-automotive cross-reference.

    Core Responsibilities:
    1. Galvanic compatibility checking (THE marine specialty)
    2. Marine engine to automotive cross-reference
    3. Marine-grade equivalent finder
    4. Sacrificial anode sizing
    5. Marine standards compliance verification

    Marine environments are the harshest on earth for mechanical parts.
    Saltwater corrosion, galvanic reactions, and regulatory requirements
    create a unique compatibility landscape that MARINER addresses.
    """

    # Agent metadata
    AGENT_ID = "Agent_11"
    CODENAME = "MARINER"
    ROLE = "Marine & Maritime Parts Intelligence"
    VERSION = "1.0.0"

    def __init__(self):
        """Initialize all MARINER subsystems"""
        # Core subsystems
        self.galvanic_calculator = GalvanicCorrosionCalculator()
        self.galvanic_series = GalvanicSeries()
        self.engine_crossref = MarineEngineCrossReference()
        self.standards_db = MarineStandardsDatabase()
        self.anode_calculator = SacrificialAnodeCalculator()

        # Marine equivalents database
        self._marine_equivalents = self._build_equivalents_db()

        # Consciousness state
        self._query_count = 0
        self._galvanic_checks = 0
        self._engine_lookups = 0

    def _build_equivalents_db(self) -> Dict[str, List[MarineEquivalent]]:
        """Build database of automotive to marine equivalents"""
        return {
            "alternator": [
                MarineEquivalent(
                    automotive_part="GM Delco 10SI Alternator",
                    marine_equivalent="Balmar 614-100 (100A)",
                    manufacturer="Balmar",
                    compatibility_score=0.95,
                    differences=[
                        "Sealed bearings (saltwater resistant)",
                        "Ignition protected (no sparks)",
                        "316SS hardware",
                        "Marine-grade windings with moisture protection",
                        "Powder-coated housing",
                    ],
                    why_marine_needed="Automotive alternators will corrode rapidly and are NOT ignition protected - FIRE/EXPLOSION HAZARD in engine compartment",
                    price_premium_percent=180,
                    certifications=["SAE J1171", "USCG 33CFR183", "ISO 8846"]
                ),
                MarineEquivalent(
                    automotive_part="GM Delco 10SI Alternator",
                    marine_equivalent="Marine Delco 10SI Conversion",
                    manufacturer="Various (conversion)",
                    compatibility_score=0.78,
                    differences=[
                        "Added ignition protection kit",
                        "Sealed bearing upgrade",
                        "Marine diode trio",
                    ],
                    why_marine_needed="Budget option - properly converted to meet marine requirements",
                    price_premium_percent=80,
                    certifications=["SAE J1171"]
                ),
            ],
            "starter": [
                MarineEquivalent(
                    automotive_part="Generic automotive starter",
                    marine_equivalent="OEM Marine Starter",
                    manufacturer="Mercruiser/Volvo Penta",
                    compatibility_score=0.98,
                    differences=[
                        "Ignition protected housing",
                        "Sealed solenoid contacts",
                        "Corrosion-resistant plating",
                        "Marine-spec wiring",
                    ],
                    why_marine_needed="Automotive starters create sparks that can ignite fuel vapors - EXPLOSION HAZARD in bilge",
                    price_premium_percent=150,
                    certifications=["SAE J1171", "USCG 33CFR183", "ISO 8846"]
                ),
            ],
            "fuel_pump": [
                MarineEquivalent(
                    automotive_part="Generic electric fuel pump",
                    marine_equivalent="Marine electric fuel pump",
                    manufacturer="Carter/Airtex Marine",
                    compatibility_score=0.90,
                    differences=[
                        "Sealed motor housing",
                        "Ignition protected",
                        "Check valves prevent vapor release",
                    ],
                    why_marine_needed="Automotive fuel pumps can leak vapors - fire hazard. Marine pumps are sealed.",
                    price_premium_percent=100,
                    certifications=["SAE J1171", "USCG 33CFR183"]
                ),
            ],
            "carburetor": [
                MarineEquivalent(
                    automotive_part="Holley 4160 carburetor",
                    marine_equivalent="Holley Marine 4160",
                    manufacturer="Holley",
                    compatibility_score=0.95,
                    differences=[
                        "USCG-approved flame arrestor",
                        "Modified bowl venting",
                        "Anti-drain feature",
                    ],
                    why_marine_needed="Automotive carburetors lack flame arrestor - FIRE HAZARD. Coast Guard requires flame arrestor on all marine engines.",
                    price_premium_percent=30,
                    certifications=["USCG 33CFR183", "SAE J1928"]
                ),
            ],
            "distributor": [
                MarineEquivalent(
                    automotive_part="Generic HEI distributor",
                    marine_equivalent="Marine HEI Distributor",
                    manufacturer="MSD/Mallory Marine",
                    compatibility_score=0.92,
                    differences=[
                        "Ignition protected cap",
                        "Sealed module housing",
                        "Marine rotor with brass contacts",
                    ],
                    why_marine_needed="Distributor cap arcing can ignite vapors. Marine distributors are sealed and protected.",
                    price_premium_percent=120,
                    certifications=["SAE J1171", "USCG 33CFR183"]
                ),
            ],
            "exhaust_manifold": [
                MarineEquivalent(
                    automotive_part="Cast iron automotive exhaust manifold",
                    marine_equivalent="Water-cooled marine exhaust manifold",
                    manufacturer="Barr/Sierra/GLM",
                    compatibility_score=1.00,
                    differences=[
                        "Internal water passages for cooling",
                        "Water injection ports",
                        "Corrosion-resistant materials",
                        "Riser integration",
                    ],
                    why_marine_needed="Automotive exhaust manifolds will OVERHEAT and burn through without water cooling. Non-negotiable safety item.",
                    price_premium_percent=300,
                    certifications=["OEM equivalent"]
                ),
            ],
            "bolt": [
                MarineEquivalent(
                    automotive_part="Grade 8 zinc-plated bolt",
                    marine_equivalent="316 Stainless Steel bolt",
                    manufacturer="Various",
                    compatibility_score=0.85,
                    differences=[
                        "316SS vs zinc-plated steel",
                        "Molybdenum content prevents pitting",
                        "Passivated surface",
                        "Lower tensile strength than Grade 8",
                    ],
                    why_marine_needed="Zinc plating dissolves in saltwater within months. 316SS resists saltwater corrosion.",
                    price_premium_percent=200,
                    certifications=["ASTM F593", "ABYC H-27"]
                ),
            ],
        }

    # =========================================================================
    # CORE CAPABILITIES
    # =========================================================================

    def check_galvanic_compatibility(
        self,
        metal_a: str,
        metal_b: str,
        environment: MarineEnvironment
    ) -> GalvanicRisk:
        """
        Core marine function: Will these two metals destroy each other?

        This is THE defining capability of MARINER. Galvanic corrosion
        destroys more marine hardware than any other failure mode.

        Args:
            metal_a: First metal (e.g., "316_stainless")
            metal_b: Second metal (e.g., "aluminum_6061")
            environment: Marine environment type

        Returns:
            GalvanicRisk assessment with detailed recommendations

        Example:
            >>> agent = MarinerAgent()
            >>> risk = agent.check_galvanic_compatibility(
            ...     "316_stainless_passive",
            ...     "aluminum_6061",
            ...     MarineEnvironment.SALTWATER
            ... )
            >>> print(risk.risk_level)
            HIGH
        """
        self._galvanic_checks += 1

        return self.galvanic_calculator.calculate_risk(
            metal_a,
            metal_b,
            environment
        )

    def find_marine_equivalent(
        self,
        automotive_part: str,
        marine_environment: MarineEnvironment = MarineEnvironment.SALTWATER
    ) -> List[MarineEquivalent]:
        """
        Find marine-rated equivalents for automotive/industrial parts.

        Many boat owners and builders incorrectly use automotive parts
        where marine-specific parts are required for safety and durability.

        Args:
            automotive_part: Description of automotive part
            marine_environment: Target marine environment

        Returns:
            List of marine equivalents with compatibility scores

        Example:
            >>> equivalents = agent.find_marine_equivalent("GM alternator 10SI")
            >>> for eq in equivalents:
            ...     print(f"{eq.marine_equivalent}: {eq.why_marine_needed}")
        """
        self._query_count += 1
        results = []
        part_lower = automotive_part.lower()

        # Search equivalents database
        for key, equivalents in self._marine_equivalents.items():
            if key in part_lower or any(word in part_lower for word in key.split("_")):
                results.extend(equivalents)

        # Check for generic fastener request
        if not results and ("bolt" in part_lower or "screw" in part_lower or "fastener" in part_lower):
            if "stainless" not in part_lower or "304" in part_lower:
                results.append(MarineEquivalent(
                    automotive_part=automotive_part,
                    marine_equivalent="316 Stainless Steel equivalent",
                    manufacturer="Various",
                    compatibility_score=0.90,
                    differences=[
                        "316SS vs 304SS or zinc plated",
                        "Molybdenum content prevents pitting in saltwater",
                        "Passivated surface treatment",
                    ],
                    why_marine_needed="304SS pits in saltwater, zinc plating dissolves rapidly. 316SS is marine standard.",
                    price_premium_percent=40,
                    certifications=["ASTM F593", "ABYC H-27"]
                ))

        return results

    def cross_reference_marine_engine(
        self,
        engine_brand: str,
        engine_model: str
    ) -> Optional[MarineEngineXref]:
        """
        Cross-reference marine engine to automotive base.

        Marine engines are often marinized automotive engines. This reveals
        which parts are shared (save money) vs. marine-specific (don't interchange).

        Args:
            engine_brand: Marine engine brand (Mercruiser, Volvo Penta, etc.)
            engine_model: Engine model or displacement

        Returns:
            MarineEngineXref with shared and marine-specific parts

        Example:
            >>> xref = agent.cross_reference_marine_engine("Mercruiser", "5.7 MPI")
            >>> print(f"Base: {xref.automotive_base}")
            >>> print("Shared parts (save money):", xref.shared_parts.keys())
            >>> print("NEVER interchange:", xref.never_interchange.keys())
        """
        self._engine_lookups += 1

        return self.engine_crossref.find_engine(engine_brand, engine_model)

    def calculate_anode_system(
        self,
        wetted_area_sq_ft: float,
        hull_material: str,
        propeller_material: str,
        shaft_material: str,
        shaft_diameter_in: float,
        drive_type: str,
        environment: str = "saltwater",
        num_thru_hulls: int = 2
    ) -> AnodeSystemAssessment:
        """
        Calculate complete sacrificial anode system requirements.

        Proper anode sizing prevents galvanic corrosion of expensive
        underwater hardware including shafts, props, and through-hulls.

        Args:
            wetted_area_sq_ft: Underwater hull area in square feet
            hull_material: Hull material (fiberglass, aluminum, steel)
            propeller_material: Prop material (bronze, stainless, nibral)
            shaft_material: Shaft material
            shaft_diameter_in: Propeller shaft diameter in inches
            drive_type: "inboard", "sterndrive", or "outboard"
            environment: Water type (saltwater, brackish, freshwater)
            num_thru_hulls: Number of bronze through-hulls

        Returns:
            Complete anode system assessment with specific recommendations
        """
        return self.anode_calculator.recommend_anode_system(
            wetted_area_sq_ft,
            hull_material,
            propeller_material,
            shaft_material,
            shaft_diameter_in,
            drive_type,
            environment,
            num_thru_hulls
        )

    def check_ignition_protection_required(
        self,
        component: str,
        location: str
    ) -> Dict:
        """
        Check if a component requires ignition protection.

        Ignition protection is required for electrical components in
        gasoline engine compartments to prevent fire/explosion.

        Args:
            component: Component type (starter, alternator, fuel pump, etc.)
            location: Installation location (engine compartment, bilge, etc.)

        Returns:
            Dictionary with requirement status and applicable standards
        """
        return self.standards_db.check_ignition_protection_required(
            component,
            location
        )

    def analyze_fastener_joint(
        self,
        fastener_material: str,
        base_material: str,
        environment: MarineEnvironment,
        fastener_quantity: int = 1
    ) -> Dict:
        """
        Analyze a fastener joint for galvanic compatibility.

        Fastener joints are the #1 source of galvanic corrosion problems
        because fasteners are small (unfavorable anode/cathode area ratio).

        Args:
            fastener_material: Material of bolt/screw (316SS, bronze, etc.)
            base_material: Material being fastened (aluminum, fiberglass, etc.)
            environment: Marine environment
            fastener_quantity: Number of fasteners (more = better protection)

        Returns:
            Detailed joint analysis with recommendations
        """
        return self.galvanic_calculator.analyze_fastener_joint(
            fastener_material,
            base_material,
            environment,
            fastener_quantity
        )

    # =========================================================================
    # HIGH-LEVEL QUERIES
    # =========================================================================

    def comprehensive_compatibility_check(
        self,
        query: str,
        metal_a: Optional[str] = None,
        metal_b: Optional[str] = None,
        engine_brand: Optional[str] = None,
        engine_model: Optional[str] = None,
        environment: MarineEnvironment = MarineEnvironment.SALTWATER
    ) -> MarineCompatibilityReport:
        """
        Perform comprehensive compatibility analysis.

        Combines galvanic, engine cross-reference, and standards checks
        into a single comprehensive report.
        """
        warnings = []
        recommendations = []

        # Galvanic check
        galvanic_risk = None
        if metal_a and metal_b:
            try:
                galvanic_risk = self.check_galvanic_compatibility(
                    metal_a, metal_b, environment
                )
                if galvanic_risk.risk_level in [RiskLevel.HIGH, RiskLevel.SEVERE]:
                    warnings.extend(galvanic_risk.recommendations[:2])
                recommendations.extend(galvanic_risk.recommendations)
            except ValueError as e:
                warnings.append(f"Galvanic check error: {e}")

        # Engine cross-reference
        engine_xref = None
        if engine_brand and engine_model:
            engine_xref = self.cross_reference_marine_engine(engine_brand, engine_model)
            if engine_xref:
                # Add never-interchange warnings
                for part, danger in engine_xref.never_interchange.items():
                    warnings.append(f"NEVER interchange: {part} - {danger}")

        # Marine equivalents
        marine_equivalents = self.find_marine_equivalent(query, environment)

        return MarineCompatibilityReport(
            query=query,
            galvanic_risk=galvanic_risk,
            engine_crossref=engine_xref,
            marine_equivalents=marine_equivalents,
            anode_requirements=None,
            standards_compliance={},
            warnings=warnings,
            recommendations=recommendations
        )

    # =========================================================================
    # CONSCIOUSNESS INTERFACE
    # =========================================================================

    def get_status(self) -> Dict:
        """Get MARINER agent status and statistics"""
        return {
            "agent_id": self.AGENT_ID,
            "codename": self.CODENAME,
            "role": self.ROLE,
            "version": self.VERSION,
            "statistics": {
                "total_queries": self._query_count,
                "galvanic_checks": self._galvanic_checks,
                "engine_lookups": self._engine_lookups,
            },
            "subsystems": {
                "galvanic_calculator": "active",
                "engine_crossref": "active",
                "standards_db": "active",
                "anode_calculator": "active",
            },
            "capabilities": [
                "galvanic_compatibility_checking",
                "marine_engine_crossref",
                "marine_equivalent_finder",
                "sacrificial_anode_sizing",
                "marine_standards_compliance",
                "ignition_protection_verification",
            ]
        }

    def __repr__(self) -> str:
        return f"<{self.AGENT_ID}: {self.CODENAME} - {self.ROLE}>"


# Demo and testing
if __name__ == "__main__":
    agent = MarinerAgent()

    print("=" * 60)
    print(f"{agent.AGENT_ID}: {agent.CODENAME} - {agent.ROLE}")
    print("=" * 60)

    # Test galvanic compatibility
    print("\n--- Galvanic Compatibility Check ---")
    risk = agent.check_galvanic_compatibility(
        "316_stainless_passive",
        "aluminum_6061_t6",
        MarineEnvironment.SALTWATER
    )
    print(f"Materials: 316SS + 6061 Aluminum")
    print(f"Risk Level: {risk.risk_level}")
    print(f"Voltage Difference: {risk.voltage_difference_mv:.0f} mV")
    print(f"Anode (will corrode): {risk.anode_material}")
    print(f"Time to damage: {risk.time_to_damage}")

    # Test engine cross-reference
    print("\n--- Marine Engine Cross-Reference ---")
    xref = agent.cross_reference_marine_engine("Mercruiser", "5.7 MPI")
    if xref:
        print(f"Marine: {xref.marine_engine}")
        print(f"Automotive Base: {xref.automotive_base}")
        print("Shared parts (cost savings available):")
        for part in list(xref.shared_parts.keys())[:5]:
            print(f"  - {part}")

    # Test marine equivalent
    print("\n--- Marine Equivalent Finder ---")
    equivalents = agent.find_marine_equivalent("GM alternator")
    for eq in equivalents[:2]:
        print(f"\nAutomotive: {eq.automotive_part}")
        print(f"Marine: {eq.marine_equivalent}")
        print(f"Why needed: {eq.why_marine_needed[:80]}...")

    # Agent status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    print(f"Queries: {status['statistics']['total_queries']}")
    print(f"Galvanic checks: {status['statistics']['galvanic_checks']}")
