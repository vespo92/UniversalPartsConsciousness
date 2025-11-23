"""
Root Cause Investigator

Systematic root cause investigation using engineering methods.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum


class InvestigationMethod(Enum):
    """Available investigation methods"""
    FIVE_WHY = "5_why"
    FISHBONE = "fishbone"
    FAULT_TREE = "fault_tree"
    FMEA = "fmea"
    PHYSICS_OF_FAILURE = "physics_of_failure"


@dataclass
class RootCauseAnalysis:
    """Result of root cause investigation"""
    method: str
    chain: List[str]
    root_cause: str
    category: str
    contributing_factors: List[str]
    systemic_issue: bool
    recommended_actions: List[str]
    prevention_measures: List[str]
    confidence: float


class RootCauseInvestigator:
    """
    Systematic root cause investigation using engineering methods.

    Available methods:
    - 5 Why: Progressive questioning to find root cause
    - Fishbone: Ishikawa diagram for cause categorization
    - Fault Tree: Top-down logical failure analysis
    - FMEA: Failure Mode and Effects Analysis
    - Physics of Failure: First-principles failure mechanics
    """

    CAUSE_CATEGORIES = {
        "design": [
            "Inadequate safety factor",
            "Material selection error",
            "Stress concentration",
            "Insufficient fatigue life",
            "Missing load case",
            "Tolerance stack-up",
        ],
        "material": [
            "Out-of-spec material",
            "Material defect (inclusion, porosity)",
            "Wrong heat treatment",
            "Counterfeit/substandard material",
            "Material degradation",
        ],
        "manufacturing": [
            "Machining damage",
            "Heat treatment error",
            "Surface finish issues",
            "Assembly damage",
            "Contamination",
            "Process variation",
        ],
        "operation": [
            "Overload",
            "Undertorque/Overtorque",
            "Wrong lubricant",
            "Exceeded duty cycle",
            "Environmental exposure",
            "Misuse",
        ],
        "maintenance": [
            "Missed inspection",
            "Wrong replacement part",
            "Improper installation",
            "Exceeded service interval",
            "Inadequate repair",
        ],
    }

    def __init__(self):
        """Initialize the root cause investigator."""
        pass

    async def investigate(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any,
        method: str = "physics_of_failure"
    ) -> RootCauseAnalysis:
        """
        Perform systematic root cause investigation.

        Args:
            failed_part: Report of the failed part
            evidence: Physical evidence from failure
            failure_mode: Determined failure mode
            method: Investigation method to use

        Returns:
            Complete root cause analysis
        """
        if method == "5_why":
            return await self._five_why_analysis(failed_part, evidence, failure_mode)
        elif method == "fishbone":
            return await self._fishbone_analysis(failed_part, evidence, failure_mode)
        elif method == "fault_tree":
            return await self._fault_tree_analysis(failed_part, evidence, failure_mode)
        else:
            return await self._physics_of_failure_analysis(failed_part, evidence, failure_mode)

    async def _five_why_analysis(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any
    ) -> RootCauseAnalysis:
        """Perform 5-Why root cause analysis."""
        failure_mode_str = str(failure_mode.value if hasattr(failure_mode, 'value') else failure_mode)

        # Build why chain based on failure mode
        why_chains = {
            "high_cycle_fatigue": [
                f"Why did the part fail? -> {failure_mode_str}",
                "Why fatigue? -> Cyclic loading exceeded fatigue limit",
                "Why exceeded limit? -> Insufficient preload or design margin",
                "Why insufficient? -> Specification or assembly error",
                "Why error? -> Process control gap or design oversight",
            ],
            "hydrogen_embrittlement": [
                f"Why did the part fail? -> {failure_mode_str}",
                "Why hydrogen embrittlement? -> Hydrogen trapped in material",
                "Why hydrogen trapped? -> Inadequate baking after plating",
                "Why inadequate baking? -> Supplier process control failure",
                "Why process failure? -> No verification of bake cycle",
            ],
            "galvanic_corrosion": [
                f"Why did the part fail? -> {failure_mode_str}",
                "Why galvanic corrosion? -> Dissimilar metals in contact",
                "Why dissimilar metals? -> Material specification gap",
                "Why specification gap? -> Design review missed compatibility",
                "Why missed? -> No galvanic compatibility checklist",
            ],
        }

        chain = why_chains.get(failure_mode_str, [
            f"Why did the part fail? -> {failure_mode_str}",
            "Why this mode? -> Operating conditions exceeded capability",
            "Why exceeded? -> Design/specification mismatch",
            "Why mismatch? -> Incomplete requirements analysis",
            "Why incomplete? -> Process or knowledge gap",
        ])

        # Extract root cause from chain
        root_cause = chain[-1].split("->")[-1].strip() if chain else "Unknown"

        # Determine category
        category = self._categorize_root_cause(root_cause, failure_mode_str)

        return RootCauseAnalysis(
            method="5_why",
            chain=chain,
            root_cause=root_cause,
            category=category,
            contributing_factors=self._extract_contributing_factors(chain),
            systemic_issue=self._is_systemic(chain),
            recommended_actions=self._generate_actions(root_cause, category),
            prevention_measures=self._generate_prevention(root_cause, category),
            confidence=0.75
        )

    async def _physics_of_failure_analysis(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any
    ) -> RootCauseAnalysis:
        """Perform physics-of-failure based analysis."""
        failure_mode_str = str(failure_mode.value if hasattr(failure_mode, 'value') else failure_mode)

        # Physics-based root cause determination
        physics_causes = {
            "high_cycle_fatigue": {
                "root_cause": "Cyclic stress amplitude exceeded material endurance limit at critical location",
                "chain": [
                    "Stress concentration at geometric feature",
                    "Cyclic loading from operation",
                    "Crack initiation at stress raiser",
                    "Stable crack propagation under cycling",
                    "Final fast fracture when critical crack size reached",
                ],
                "factors": [
                    "Stress concentration factor (Kt)",
                    "Load amplitude and mean stress",
                    "Material fatigue properties",
                    "Surface condition",
                ],
            },
            "hydrogen_embrittlement": {
                "root_cause": "Hydrogen diffusion to triaxial stress field causing cleavage fracture",
                "chain": [
                    "Hydrogen introduced during processing (plating/cleaning)",
                    "Hydrogen diffuses to high stress regions",
                    "Hydrogen reduces cohesive strength at grain boundaries",
                    "Crack initiates under sustained load",
                    "Time-delayed brittle fracture",
                ],
                "factors": [
                    "Hydrogen source (plating, acid cleaning)",
                    "Material susceptibility (strength level)",
                    "Stress level and distribution",
                    "Time under load",
                ],
            },
            "galvanic_corrosion": {
                "root_cause": "Electrochemical potential difference driving anodic dissolution",
                "chain": [
                    "Two dissimilar metals in electrical contact",
                    "Electrolyte (moisture, humidity) present",
                    "Galvanic cell established",
                    "Anodic material (less noble) corrodes preferentially",
                    "Material loss leads to failure",
                ],
                "factors": [
                    "Galvanic series position difference",
                    "Area ratio (anode to cathode)",
                    "Electrolyte conductivity",
                    "Environmental exposure",
                ],
            },
        }

        physics = physics_causes.get(failure_mode_str, {
            "root_cause": f"Material or loading exceeded design capability for {failure_mode_str}",
            "chain": ["Applied load/environment exceeded material capability"],
            "factors": ["Load conditions", "Material properties", "Environmental factors"],
        })

        category = self._categorize_root_cause(physics["root_cause"], failure_mode_str)

        return RootCauseAnalysis(
            method="physics_of_failure",
            chain=physics["chain"],
            root_cause=physics["root_cause"],
            category=category,
            contributing_factors=physics["factors"],
            systemic_issue=False,
            recommended_actions=self._generate_actions(physics["root_cause"], category),
            prevention_measures=self._generate_prevention(physics["root_cause"], category),
            confidence=0.85
        )

    async def _fishbone_analysis(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any
    ) -> RootCauseAnalysis:
        """Generate fishbone (Ishikawa) analysis."""
        from .fishbone_generator import FishboneGenerator
        generator = FishboneGenerator()
        diagram = await generator.generate(failed_part, evidence, failure_mode)

        # Extract root cause from most significant branch
        root_cause = diagram.primary_cause if hasattr(diagram, 'primary_cause') else "Multi-factor failure"
        category = self._categorize_root_cause(root_cause, str(failure_mode))

        return RootCauseAnalysis(
            method="fishbone",
            chain=[f"{cat}: {', '.join(causes)}" for cat, causes in diagram.causes.items()],
            root_cause=root_cause,
            category=category,
            contributing_factors=self._flatten_causes(diagram.causes),
            systemic_issue=len(diagram.causes) > 3,
            recommended_actions=self._generate_actions(root_cause, category),
            prevention_measures=self._generate_prevention(root_cause, category),
            confidence=0.70
        )

    async def _fault_tree_analysis(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any
    ) -> RootCauseAnalysis:
        """Perform fault tree analysis."""
        from .fault_tree import FaultTreeAnalyzer
        analyzer = FaultTreeAnalyzer()
        tree = await analyzer.analyze(failed_part, evidence, failure_mode)

        root_cause = tree.minimal_cut_sets[0] if tree.minimal_cut_sets else "Unknown"
        category = self._categorize_root_cause(root_cause, str(failure_mode))

        return RootCauseAnalysis(
            method="fault_tree",
            chain=tree.event_chain,
            root_cause=root_cause,
            category=category,
            contributing_factors=tree.basic_events,
            systemic_issue=len(tree.minimal_cut_sets) > 1,
            recommended_actions=self._generate_actions(root_cause, category),
            prevention_measures=self._generate_prevention(root_cause, category),
            confidence=0.80
        )

    def _categorize_root_cause(self, root_cause: str, failure_mode: str) -> str:
        """Categorize root cause into standard categories."""
        root_cause_lower = root_cause.lower()

        if any(word in root_cause_lower for word in ["plating", "heat treat", "machining", "process"]):
            return "manufacturing"
        if any(word in root_cause_lower for word in ["material", "alloy", "composition", "defect"]):
            return "material"
        if any(word in root_cause_lower for word in ["design", "stress", "geometry", "tolerance"]):
            return "design"
        if any(word in root_cause_lower for word in ["torque", "load", "overload", "operation"]):
            return "operation"
        if any(word in root_cause_lower for word in ["maintenance", "inspection", "service"]):
            return "maintenance"

        # Default based on failure mode
        mode_categories = {
            "hydrogen_embrittlement": "manufacturing",
            "galvanic_corrosion": "design",
            "high_cycle_fatigue": "design",
            "overload": "operation",
        }
        return mode_categories.get(failure_mode, "unknown")

    def _extract_contributing_factors(self, chain: List[str]) -> List[str]:
        """Extract contributing factors from why chain."""
        factors = []
        for item in chain[1:-1]:  # Skip first and last
            if "->" in item:
                factor = item.split("->")[-1].strip()
                factors.append(factor)
        return factors

    def _is_systemic(self, chain: List[str]) -> bool:
        """Determine if root cause indicates systemic issue."""
        systemic_keywords = ["process", "system", "control", "verification", "checklist", "specification"]
        for item in chain:
            if any(keyword in item.lower() for keyword in systemic_keywords):
                return True
        return False

    def _flatten_causes(self, causes: Dict[str, List[str]]) -> List[str]:
        """Flatten cause dictionary to list."""
        flat = []
        for category_causes in causes.values():
            flat.extend(category_causes)
        return flat

    def _generate_actions(self, root_cause: str, category: str) -> List[str]:
        """Generate recommended actions based on root cause."""
        category_actions = {
            "manufacturing": [
                "Audit supplier manufacturing process",
                "Implement incoming quality inspection",
                "Require process certification documentation",
            ],
            "material": [
                "Verify material certification",
                "Implement material testing protocol",
                "Source from certified suppliers only",
            ],
            "design": [
                "Review and update design calculations",
                "Add design review checklist item",
                "Update design guidelines",
            ],
            "operation": [
                "Update operating procedures",
                "Implement operating limits monitoring",
                "Provide operator training",
            ],
            "maintenance": [
                "Update maintenance procedures",
                "Reduce maintenance intervals",
                "Implement condition monitoring",
            ],
        }
        return category_actions.get(category, ["Conduct detailed investigation"])

    def _generate_prevention(self, root_cause: str, category: str) -> List[str]:
        """Generate prevention measures."""
        prevention = {
            "manufacturing": [
                "Supplier qualification program",
                "Incoming inspection requirements",
                "Process capability verification",
            ],
            "material": [
                "Material traceability requirements",
                "Specification tightening",
                "Alternative material evaluation",
            ],
            "design": [
                "Design review process enhancement",
                "Analysis checklist addition",
                "Lessons learned database update",
            ],
            "operation": [
                "Operating procedure update",
                "Training program enhancement",
                "Monitoring system implementation",
            ],
            "maintenance": [
                "Maintenance procedure revision",
                "Inspection interval adjustment",
                "Predictive maintenance implementation",
            ],
        }
        return prevention.get(category, ["Document lesson learned"])
