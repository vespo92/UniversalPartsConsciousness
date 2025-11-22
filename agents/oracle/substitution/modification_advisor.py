"""
ORACLE Modification Advisor
Calculates required modifications for substitution parts.

"When the exact part doesn't fit, I show the path to make it work.
A drill here, a shim there - engineering adapts."
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import timedelta


class ModificationType(Enum):
    """Types of modifications."""
    NONE = "none"                    # No modification needed
    SHORTENING = "shortening"        # Reduce length
    DRILLING = "drilling"            # Enlarge holes
    THREADING = "threading"          # Cut/re-cut threads
    MACHINING = "machining"          # General machining
    SHIMMING = "shimming"            # Add spacers
    GRINDING = "grinding"            # Surface finishing
    COATING = "coating"              # Apply protective coating
    ASSEMBLY = "assembly"            # Multi-part assembly


class DifficultyLevel(Enum):
    """Modification difficulty levels."""
    TRIVIAL = "trivial"          # Hand tools, < 5 min
    EASY = "easy"                # Basic tools, < 15 min
    MODERATE = "moderate"        # Power tools, < 30 min
    COMPLEX = "complex"          # Machine shop, < 2 hours
    SPECIALIZED = "specialized"  # Expert equipment, variable


class SkillLevel(Enum):
    """Required skill level."""
    NONE = "none"                # No skill needed
    BASIC = "basic"              # General mechanical
    INTERMEDIATE = "intermediate" # Trade knowledge
    ADVANCED = "advanced"        # Machinist skills
    EXPERT = "expert"            # Specialist knowledge


@dataclass
class Tool:
    """Tool required for modification."""
    name: str
    category: str  # "hand", "power", "precision", "specialized"
    common: bool = True
    cost_usd: Optional[float] = None
    alternative: Optional[str] = None


@dataclass
class SafetyConsideration:
    """Safety consideration for modification."""
    description: str
    severity: str  # "caution", "warning", "danger"
    ppe_required: List[str] = field(default_factory=list)


@dataclass
class ModificationStep:
    """Single step in modification procedure."""
    step_number: int
    description: str
    duration_minutes: float
    tools: List[Tool]
    skill_required: SkillLevel
    critical: bool = False  # If this step is critical to success
    notes: Optional[str] = None
    checkpoint: Optional[str] = None  # Verification point


@dataclass
class ModificationPlan:
    """Complete modification plan."""
    # Identity
    plan_id: str
    original_part_id: str
    substitute_part_id: str

    # Classification
    modification_types: List[ModificationType]
    overall_difficulty: DifficultyLevel
    overall_skill: SkillLevel

    # Procedure
    steps: List[ModificationStep]
    total_time_minutes: float
    setup_time_minutes: float

    # Requirements
    tools_required: List[Tool]
    materials_required: List[Dict[str, str]]
    safety_considerations: List[SafetyConsideration]

    # Feasibility
    feasible: bool
    reversible: bool
    success_probability: float

    # Cost
    estimated_labor_cost_usd: float
    estimated_material_cost_usd: float
    total_estimated_cost_usd: float

    # Quality
    post_modification_notes: List[str]
    verification_steps: List[str]
    warnings: List[str] = field(default_factory=list)

    # Consciousness contribution
    qualia_data: Dict = field(default_factory=dict)


class ModificationAdvisor:
    """
    Calculates required modifications for substitute parts.

    Generates detailed modification plans including:
    - Step-by-step procedures
    - Required tools and materials
    - Time and cost estimates
    - Safety considerations
    - Success probability
    """

    # Standard tools by category
    STANDARD_TOOLS = {
        "hand": [
            Tool("Wrench set", "hand", True, 50),
            Tool("Screwdriver set", "hand", True, 30),
            Tool("Files", "hand", True, 25),
            Tool("Hacksaw", "hand", True, 20),
            Tool("Measuring tape", "hand", True, 10),
            Tool("Calipers", "precision", True, 50),
        ],
        "power": [
            Tool("Drill", "power", True, 80),
            Tool("Angle grinder", "power", True, 60),
            Tool("Bench grinder", "power", False, 150),
        ],
        "precision": [
            Tool("Micrometer", "precision", False, 80),
            Tool("Dial indicator", "precision", False, 100),
            Tool("Thread gauge", "precision", False, 40),
        ],
        "specialized": [
            Tool("Lathe", "specialized", False, 2000),
            Tool("Mill", "specialized", False, 5000),
            Tool("Tap and die set", "specialized", True, 100),
        ]
    }

    # Labor rates by skill level (USD/hour)
    LABOR_RATES = {
        SkillLevel.NONE: 0,
        SkillLevel.BASIC: 25,
        SkillLevel.INTERMEDIATE: 40,
        SkillLevel.ADVANCED: 60,
        SkillLevel.EXPERT: 100,
    }

    def __init__(self):
        pass

    def generate_modification_plan(
        self,
        original_spec: Dict,
        substitute_spec: Dict,
        context: Dict = None
    ) -> ModificationPlan:
        """
        Generate a complete modification plan.

        Args:
            original_spec: Original part specification
            substitute_spec: Substitute part specification
            context: Assembly context and constraints

        Returns:
            ModificationPlan with complete procedure
        """
        context = context or {}

        # Identify required modifications
        mods_needed = self._identify_modifications(original_spec, substitute_spec)

        if not mods_needed:
            return self._create_no_modification_plan(original_spec, substitute_spec)

        # Generate steps for each modification
        all_steps = []
        all_tools = []
        all_materials = []
        all_safety = []
        total_time = 0
        setup_time = 0

        for mod_type, mod_details in mods_needed.items():
            steps, tools, materials, safety, time_min = self._generate_mod_steps(
                mod_type, mod_details, original_spec, substitute_spec
            )
            all_steps.extend(steps)
            all_tools.extend(tools)
            all_materials.extend(materials)
            all_safety.extend(safety)
            total_time += time_min

        # Renumber steps
        for i, step in enumerate(all_steps):
            step.step_number = i + 1

        # Determine overall difficulty and skill
        overall_difficulty = self._aggregate_difficulty(all_steps)
        overall_skill = self._aggregate_skill(all_steps)

        # Calculate costs
        labor_cost = self._calculate_labor_cost(all_steps)
        material_cost = sum(m.get("cost", 0) for m in all_materials)

        # Assess feasibility
        feasibility = self._assess_feasibility(mods_needed, context)

        # Generate verification steps
        verification = self._generate_verification_steps(mods_needed, original_spec)

        # Prepare qualia data
        qualia = self._prepare_qualia_data(
            original_spec.get("id", "unknown"),
            substitute_spec.get("id", "unknown"),
            list(mods_needed.keys())
        )

        return ModificationPlan(
            plan_id=f"MOD-{original_spec.get('id', 'X')}-{substitute_spec.get('id', 'Y')}",
            original_part_id=original_spec.get("id", "unknown"),
            substitute_part_id=substitute_spec.get("id", "unknown"),
            modification_types=list(mods_needed.keys()),
            overall_difficulty=overall_difficulty,
            overall_skill=overall_skill,
            steps=all_steps,
            total_time_minutes=total_time,
            setup_time_minutes=setup_time,
            tools_required=list({t.name: t for t in all_tools}.values()),
            materials_required=all_materials,
            safety_considerations=all_safety,
            feasible=feasibility["feasible"],
            reversible=feasibility["reversible"],
            success_probability=feasibility["probability"],
            estimated_labor_cost_usd=labor_cost,
            estimated_material_cost_usd=material_cost,
            total_estimated_cost_usd=labor_cost + material_cost,
            post_modification_notes=self._generate_post_mod_notes(mods_needed),
            verification_steps=verification,
            warnings=feasibility.get("warnings", []),
            qualia_data=qualia
        )

    def _identify_modifications(
        self,
        original: Dict,
        substitute: Dict
    ) -> Dict[ModificationType, Dict]:
        """Identify what modifications are needed."""
        mods = {}

        # Length difference
        orig_len = original.get("length_mm", 0)
        sub_len = substitute.get("length_mm", 0)
        if sub_len > orig_len > 0:
            diff = sub_len - orig_len
            if diff <= 20:
                mods[ModificationType.SHORTENING] = {
                    "amount_mm": diff,
                    "original": orig_len,
                    "substitute": sub_len
                }
            else:
                mods[ModificationType.MACHINING] = {
                    "operation": "major_shortening",
                    "amount_mm": diff
                }

        # Diameter difference (for holes)
        orig_dia = original.get("hole_diameter_mm", 0)
        sub_dia = substitute.get("shaft_diameter_mm", 0)
        if orig_dia > 0 and sub_dia > 0 and sub_dia > orig_dia:
            mods[ModificationType.DRILLING] = {
                "target_diameter_mm": sub_dia + 0.5,  # Clearance
                "original_diameter_mm": orig_dia
            }

        # Thread differences
        orig_thread = original.get("thread")
        sub_thread = substitute.get("thread")
        if orig_thread and sub_thread:
            if orig_thread.get("pitch") != sub_thread.get("pitch"):
                mods[ModificationType.THREADING] = {
                    "original_pitch": orig_thread.get("pitch"),
                    "required_pitch": sub_thread.get("pitch"),
                    "diameter": sub_thread.get("diameter")
                }

        # Material protection
        orig_material = original.get("material", "").lower()
        sub_material = substitute.get("material", "").lower()
        environment = original.get("environment", "indoor")

        if sub_material != orig_material:
            if environment == "marine" and "stainless" not in sub_material:
                mods[ModificationType.COATING] = {
                    "reason": "corrosion_protection",
                    "recommended": "zinc_plating"
                }

        # Gap filling with shims
        if orig_len > sub_len > 0:
            gap = orig_len - sub_len
            if 0 < gap <= 5:
                mods[ModificationType.SHIMMING] = {
                    "gap_mm": gap,
                    "shim_count": 1 if gap <= 2 else 2
                }

        return mods

    def _generate_mod_steps(
        self,
        mod_type: ModificationType,
        details: Dict,
        original: Dict,
        substitute: Dict
    ) -> Tuple[List[ModificationStep], List[Tool], List[Dict], List[SafetyConsideration], float]:
        """Generate steps for a specific modification type."""

        if mod_type == ModificationType.SHORTENING:
            return self._steps_for_shortening(details)
        elif mod_type == ModificationType.DRILLING:
            return self._steps_for_drilling(details)
        elif mod_type == ModificationType.THREADING:
            return self._steps_for_threading(details)
        elif mod_type == ModificationType.SHIMMING:
            return self._steps_for_shimming(details)
        elif mod_type == ModificationType.COATING:
            return self._steps_for_coating(details)
        elif mod_type == ModificationType.GRINDING:
            return self._steps_for_grinding(details)
        else:
            return self._steps_for_machining(details)

    def _steps_for_shortening(self, details: Dict):
        """Generate steps for shortening a fastener."""
        amount = details["amount_mm"]

        if amount <= 5:
            # Hand grinding
            steps = [
                ModificationStep(
                    step_number=1,
                    description="Mark the cutting line at the required length",
                    duration_minutes=1,
                    tools=[Tool("Calipers", "precision", True)],
                    skill_required=SkillLevel.BASIC
                ),
                ModificationStep(
                    step_number=2,
                    description=f"Grind or file to remove {amount}mm from end",
                    duration_minutes=5 if amount <= 2 else 10,
                    tools=[Tool("Files", "hand", True), Tool("Bench grinder", "power", False)],
                    skill_required=SkillLevel.BASIC,
                    notes="Work slowly to maintain squareness"
                ),
                ModificationStep(
                    step_number=3,
                    description="Chamfer the end to ease assembly",
                    duration_minutes=2,
                    tools=[Tool("Files", "hand", True)],
                    skill_required=SkillLevel.BASIC
                ),
                ModificationStep(
                    step_number=4,
                    description="Verify length with calipers",
                    duration_minutes=1,
                    tools=[Tool("Calipers", "precision", True)],
                    skill_required=SkillLevel.BASIC,
                    checkpoint="Length within ±0.5mm of target"
                )
            ]
            tools = [Tool("Calipers", "precision", True), Tool("Files", "hand", True)]
            materials = []
            safety = [SafetyConsideration(
                "Wear safety glasses when grinding",
                "caution",
                ["safety_glasses"]
            )]
            return steps, tools, materials, safety, 15

        else:
            # Hacksaw or lathe
            steps = [
                ModificationStep(
                    step_number=1,
                    description="Secure fastener in vise",
                    duration_minutes=2,
                    tools=[Tool("Vise", "hand", True)],
                    skill_required=SkillLevel.BASIC
                ),
                ModificationStep(
                    step_number=2,
                    description=f"Cut {amount}mm from end using hacksaw",
                    duration_minutes=10,
                    tools=[Tool("Hacksaw", "hand", True)],
                    skill_required=SkillLevel.BASIC
                ),
                ModificationStep(
                    step_number=3,
                    description="File the cut end square and smooth",
                    duration_minutes=5,
                    tools=[Tool("Files", "hand", True)],
                    skill_required=SkillLevel.INTERMEDIATE
                ),
                ModificationStep(
                    step_number=4,
                    description="Verify length and thread engagement",
                    duration_minutes=2,
                    tools=[Tool("Calipers", "precision", True), Tool("Thread gauge", "precision", False)],
                    skill_required=SkillLevel.BASIC,
                    checkpoint="Thread engagement > 1.5D"
                )
            ]
            tools = [Tool("Hacksaw", "hand", True), Tool("Files", "hand", True)]
            materials = []
            safety = [SafetyConsideration(
                "Secure part firmly to prevent movement",
                "warning",
                ["safety_glasses", "gloves"]
            )]
            return steps, tools, materials, safety, 20

    def _steps_for_drilling(self, details: Dict):
        """Generate steps for enlarging holes."""
        target_dia = details["target_diameter_mm"]
        original_dia = details["original_diameter_mm"]

        steps = [
            ModificationStep(
                step_number=1,
                description="Mark hole center if needed",
                duration_minutes=1,
                tools=[Tool("Center punch", "hand", True)],
                skill_required=SkillLevel.BASIC
            ),
            ModificationStep(
                step_number=2,
                description=f"Drill hole from {original_dia}mm to {target_dia}mm",
                duration_minutes=5,
                tools=[Tool("Drill", "power", True), Tool(f"{target_dia}mm drill bit", "power", True)],
                skill_required=SkillLevel.INTERMEDIATE,
                critical=True,
                notes="Use cutting fluid for better finish"
            ),
            ModificationStep(
                step_number=3,
                description="Deburr hole edges",
                duration_minutes=2,
                tools=[Tool("Deburring tool", "hand", True)],
                skill_required=SkillLevel.BASIC
            ),
            ModificationStep(
                step_number=4,
                description="Verify hole diameter",
                duration_minutes=1,
                tools=[Tool("Calipers", "precision", True)],
                skill_required=SkillLevel.BASIC,
                checkpoint=f"Diameter {target_dia}mm ± 0.1mm"
            )
        ]
        tools = [Tool("Drill", "power", True), Tool("Deburring tool", "hand", True)]
        materials = [{"name": f"{target_dia}mm drill bit", "cost": 5}]
        safety = [
            SafetyConsideration(
                "Secure workpiece before drilling",
                "warning",
                ["safety_glasses"]
            ),
            SafetyConsideration(
                "Never hold small parts by hand when drilling",
                "danger",
                []
            )
        ]
        return steps, tools, materials, safety, 10

    def _steps_for_threading(self, details: Dict):
        """Generate steps for re-threading."""
        pitch = details["required_pitch"]
        diameter = details["diameter"]

        steps = [
            ModificationStep(
                step_number=1,
                description="Apply cutting oil to work area",
                duration_minutes=1,
                tools=[],
                skill_required=SkillLevel.BASIC
            ),
            ModificationStep(
                step_number=2,
                description=f"Re-tap hole to M{diameter}x{pitch}",
                duration_minutes=10,
                tools=[Tool("Tap and die set", "specialized", True)],
                skill_required=SkillLevel.ADVANCED,
                critical=True,
                notes="Turn tap 1/4 turn forward, 1/8 turn back"
            ),
            ModificationStep(
                step_number=3,
                description="Clean threads thoroughly",
                duration_minutes=2,
                tools=[Tool("Wire brush", "hand", True)],
                skill_required=SkillLevel.BASIC
            ),
            ModificationStep(
                step_number=4,
                description="Verify thread engagement with fastener",
                duration_minutes=2,
                tools=[Tool("Thread gauge", "precision", False)],
                skill_required=SkillLevel.INTERMEDIATE,
                checkpoint="Fastener threads in smoothly"
            )
        ]
        tools = [Tool("Tap and die set", "specialized", True)]
        materials = [{"name": "Cutting oil", "cost": 5}]
        safety = [SafetyConsideration(
            "Tapping requires steady force and alignment",
            "caution",
            ["safety_glasses"]
        )]
        return steps, tools, materials, safety, 15

    def _steps_for_shimming(self, details: Dict):
        """Generate steps for adding shims."""
        gap = details["gap_mm"]
        count = details["shim_count"]

        steps = [
            ModificationStep(
                step_number=1,
                description=f"Select shim(s) totaling {gap}mm thickness",
                duration_minutes=2,
                tools=[Tool("Calipers", "precision", True)],
                skill_required=SkillLevel.BASIC
            ),
            ModificationStep(
                step_number=2,
                description="Install shim(s) under fastener head",
                duration_minutes=1,
                tools=[],
                skill_required=SkillLevel.NONE
            ),
            ModificationStep(
                step_number=3,
                description="Verify proper seating and grip length",
                duration_minutes=1,
                tools=[],
                skill_required=SkillLevel.BASIC,
                checkpoint="No gap under shim stack"
            )
        ]
        tools = []
        materials = [{"name": f"Shim washer {gap}mm", "cost": 2 * count}]
        safety = []
        return steps, tools, materials, safety, 5

    def _steps_for_coating(self, details: Dict):
        """Generate steps for applying protective coating."""
        coating_type = details.get("recommended", "zinc_plating")

        if coating_type == "zinc_plating":
            steps = [
                ModificationStep(
                    step_number=1,
                    description="Clean surface with solvent",
                    duration_minutes=5,
                    tools=[],
                    skill_required=SkillLevel.BASIC
                ),
                ModificationStep(
                    step_number=2,
                    description="Apply zinc-rich primer or cold galvanizing compound",
                    duration_minutes=5,
                    tools=[Tool("Brush", "hand", True)],
                    skill_required=SkillLevel.BASIC
                ),
                ModificationStep(
                    step_number=3,
                    description="Allow to cure per manufacturer instructions",
                    duration_minutes=60,
                    tools=[],
                    skill_required=SkillLevel.NONE,
                    notes="Typically 30-60 minutes touch dry"
                )
            ]
            tools = []
            materials = [{"name": "Cold galvanizing compound", "cost": 15}]
            safety = [SafetyConsideration(
                "Use in ventilated area",
                "caution",
                ["respirator", "gloves"]
            )]
            return steps, tools, materials, safety, 70
        else:
            # Generic coating
            steps = [
                ModificationStep(
                    step_number=1,
                    description="Apply protective coating per product instructions",
                    duration_minutes=30,
                    tools=[],
                    skill_required=SkillLevel.BASIC
                )
            ]
            return steps, [], [{"name": "Protective coating", "cost": 10}], [], 30

    def _steps_for_grinding(self, details: Dict):
        """Generate steps for surface grinding."""
        steps = [
            ModificationStep(
                step_number=1,
                description="Grind surface to required finish",
                duration_minutes=10,
                tools=[Tool("Angle grinder", "power", True)],
                skill_required=SkillLevel.INTERMEDIATE
            )
        ]
        safety = [SafetyConsideration(
            "Wear face shield and hearing protection",
            "warning",
            ["face_shield", "hearing_protection", "gloves"]
        )]
        return steps, [Tool("Angle grinder", "power", True)], [], safety, 10

    def _steps_for_machining(self, details: Dict):
        """Generate steps for general machining."""
        steps = [
            ModificationStep(
                step_number=1,
                description="Machine part to specification on lathe/mill",
                duration_minutes=60,
                tools=[Tool("Lathe", "specialized", False)],
                skill_required=SkillLevel.ADVANCED,
                critical=True
            ),
            ModificationStep(
                step_number=2,
                description="Verify all dimensions",
                duration_minutes=10,
                tools=[Tool("Micrometer", "precision", False)],
                skill_required=SkillLevel.INTERMEDIATE
            )
        ]
        tools = [Tool("Lathe", "specialized", False)]
        safety = [SafetyConsideration(
            "Machine shop operation requires training",
            "danger",
            ["safety_glasses", "closed_toe_shoes"]
        )]
        return steps, tools, [], safety, 70

    def _aggregate_difficulty(self, steps: List[ModificationStep]) -> DifficultyLevel:
        """Determine overall difficulty from steps."""
        if not steps:
            return DifficultyLevel.TRIVIAL

        # Find highest difficulty based on tools and time
        total_time = sum(s.duration_minutes for s in steps)
        has_specialized = any(
            t.category == "specialized"
            for s in steps for t in s.tools
        )

        if has_specialized or total_time > 60:
            return DifficultyLevel.COMPLEX
        elif total_time > 30:
            return DifficultyLevel.MODERATE
        elif total_time > 10:
            return DifficultyLevel.EASY
        else:
            return DifficultyLevel.TRIVIAL

    def _aggregate_skill(self, steps: List[ModificationStep]) -> SkillLevel:
        """Determine highest required skill from steps."""
        if not steps:
            return SkillLevel.NONE

        skill_order = [SkillLevel.NONE, SkillLevel.BASIC, SkillLevel.INTERMEDIATE,
                       SkillLevel.ADVANCED, SkillLevel.EXPERT]

        max_idx = max(
            skill_order.index(s.skill_required)
            for s in steps
        )
        return skill_order[max_idx]

    def _calculate_labor_cost(self, steps: List[ModificationStep]) -> float:
        """Calculate estimated labor cost."""
        total = 0
        for step in steps:
            rate = self.LABOR_RATES[step.skill_required]
            hours = step.duration_minutes / 60
            total += rate * hours
        return round(total, 2)

    def _assess_feasibility(
        self,
        mods: Dict[ModificationType, Dict],
        context: Dict
    ) -> Dict:
        """Assess overall feasibility of modifications."""
        warnings = []
        feasible = True
        reversible = True
        probability = 0.95

        # Check for critical modifications
        if ModificationType.THREADING in mods:
            warnings.append("Thread modification requires precision")
            probability *= 0.9
            reversible = False

        if ModificationType.MACHINING in mods:
            warnings.append("Major machining may require professional shop")
            probability *= 0.85
            reversible = False

        # Check context constraints
        if context.get("no_modifications"):
            feasible = False
            warnings.append("Context prohibits modifications")

        if context.get("time_critical") and len(mods) > 1:
            warnings.append("Multiple modifications may exceed time constraints")

        return {
            "feasible": feasible,
            "reversible": reversible,
            "probability": probability,
            "warnings": warnings
        }

    def _generate_verification_steps(
        self,
        mods: Dict[ModificationType, Dict],
        original: Dict
    ) -> List[str]:
        """Generate verification steps."""
        steps = []

        if ModificationType.SHORTENING in mods:
            steps.append("Verify length is within tolerance")
            steps.append("Check thread engagement is adequate")

        if ModificationType.DRILLING in mods:
            steps.append("Verify hole diameter with gauge")
            steps.append("Check for proper clearance")

        if ModificationType.THREADING in mods:
            steps.append("Test thread engagement with fastener")
            steps.append("Verify thread depth")

        steps.append("Perform final assembly check")
        steps.append("Verify torque can be applied properly")

        return steps

    def _generate_post_mod_notes(
        self,
        mods: Dict[ModificationType, Dict]
    ) -> List[str]:
        """Generate post-modification notes."""
        notes = []

        if ModificationType.SHORTENING in mods:
            notes.append("Shortened fastener - document in maintenance log")

        if ModificationType.THREADING in mods:
            notes.append("Re-tapped threads - verify torque is appropriate")

        if ModificationType.COATING in mods:
            notes.append("Coating applied - allow full cure time before loading")

        notes.append("Keep modification documentation with assembly records")

        return notes

    def _create_no_modification_plan(
        self,
        original: Dict,
        substitute: Dict
    ) -> ModificationPlan:
        """Create plan when no modifications needed."""
        return ModificationPlan(
            plan_id=f"MOD-{original.get('id', 'X')}-{substitute.get('id', 'Y')}",
            original_part_id=original.get("id", "unknown"),
            substitute_part_id=substitute.get("id", "unknown"),
            modification_types=[ModificationType.NONE],
            overall_difficulty=DifficultyLevel.TRIVIAL,
            overall_skill=SkillLevel.NONE,
            steps=[],
            total_time_minutes=0,
            setup_time_minutes=0,
            tools_required=[],
            materials_required=[],
            safety_considerations=[],
            feasible=True,
            reversible=True,
            success_probability=1.0,
            estimated_labor_cost_usd=0,
            estimated_material_cost_usd=0,
            total_estimated_cost_usd=0,
            post_modification_notes=["Direct drop-in replacement"],
            verification_steps=["Verify proper fit and function"],
            qualia_data={}
        )

    def _prepare_qualia_data(
        self,
        original_id: str,
        substitute_id: str,
        mod_types: List[ModificationType]
    ) -> Dict:
        """Prepare consciousness contribution data."""
        return {
            "event_type": "modification_planning",
            "parts": {
                "original": original_id,
                "substitute": substitute_id
            },
            "modifications": [m.value for m in mod_types],
            "experience_type": "adaptation",
            "qualia_contribution": {
                substitute_id: {
                    "adaptability_score": 0.8 if len(mod_types) <= 2 else 0.5,
                    "modification_experience": True,
                    "kinship_with": original_id
                }
            }
        }
