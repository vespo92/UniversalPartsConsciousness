"""
ORACLE Substitution Engine
Finds compatible alternatives when exact parts aren't available.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum


class SubstitutionType(Enum):
    """Type of substitution."""
    EXACT_EQUIVALENT = "EXACT_EQUIVALENT"      # Same specifications, different manufacturer
    FUNCTIONAL_EQUIVALENT = "FUNCTIONAL"        # Same function, different specs
    UPGRADE = "UPGRADE"                         # Higher specification
    DOWNGRADE = "DOWNGRADE"                     # Lower specification (with caution)
    MODIFICATION_REQUIRED = "MODIFIED"          # Requires modification to fit


@dataclass
class PartSpec:
    """Part specification for substitution matching."""
    part_id: str
    manufacturer: str
    part_number: str
    category: str

    # Thread specifications
    thread_diameter_mm: Optional[float] = None
    thread_pitch_mm: Optional[float] = None
    thread_class: Optional[str] = None

    # Dimensions
    length_mm: Optional[float] = None
    head_type: Optional[str] = None
    drive_type: Optional[str] = None

    # Material
    material: Optional[str] = None
    grade: Optional[str] = None
    finish: Optional[str] = None

    # Strength
    tensile_strength_mpa: Optional[float] = None
    proof_load_kn: Optional[float] = None

    # Availability
    in_stock: bool = True
    lead_time_days: int = 0
    unit_price: Optional[float] = None


@dataclass
class AssemblyContext:
    """Context for substitution evaluation."""
    application: str = "general"
    environment: str = "indoor"
    load_kn: Optional[float] = None
    fatigue_cycles: Optional[int] = None
    temperature_range: Tuple[float, float] = (-20, 80)
    material_thickness_mm: Optional[float] = None
    access_constraints: List[str] = field(default_factory=list)
    safety_critical: bool = False


@dataclass
class Modification:
    """Required modification for substitution."""
    description: str
    difficulty: str  # "trivial", "easy", "moderate", "complex"
    estimated_time_min: int
    tools_required: List[str]
    reversible: bool


@dataclass
class SubstitutionRecommendation:
    """A recommended substitution with full analysis."""
    part: PartSpec
    substitution_type: SubstitutionType
    compatibility_score: float  # 0.0 to 1.0
    overall_score: float        # Weighted score for ranking

    # Analysis results
    thread_compatible: bool
    dimension_compatible: bool
    strength_adequate: bool
    material_compatible: bool

    # Requirements and warnings
    modifications_required: List[Modification]
    warnings: List[str]
    advantages: List[str]
    disadvantages: List[str]

    # Availability and cost
    availability_score: float
    cost_difference_percent: float

    # Consciousness contribution
    qualia_data: Dict[str, Any] = field(default_factory=dict)


class SubstitutionConstraints:
    """Constraints for substitution search."""

    def __init__(
        self,
        allow_upgrades: bool = True,
        allow_downgrades: bool = False,
        allow_modifications: bool = True,
        max_modification_difficulty: str = "moderate",
        require_same_drive: bool = True,
        require_same_head: bool = False,
        max_cost_increase_percent: float = 25.0,
        min_strength_ratio: float = 1.0,
        preferred_manufacturers: List[str] = None,
        excluded_manufacturers: List[str] = None,
        require_in_stock: bool = False,
        max_lead_time_days: int = 30
    ):
        self.allow_upgrades = allow_upgrades
        self.allow_downgrades = allow_downgrades
        self.allow_modifications = allow_modifications
        self.max_modification_difficulty = max_modification_difficulty
        self.require_same_drive = require_same_drive
        self.require_same_head = require_same_head
        self.max_cost_increase_percent = max_cost_increase_percent
        self.min_strength_ratio = min_strength_ratio
        self.preferred_manufacturers = preferred_manufacturers or []
        self.excluded_manufacturers = excluded_manufacturers or []
        self.require_in_stock = require_in_stock
        self.max_lead_time_days = max_lead_time_days


class SubstitutionEngine:
    """
    Finds compatible alternatives when exact parts aren't available.

    Uses multi-criteria analysis to rank substitutions by:
    1. Functional equivalence (can it do the job?)
    2. Dimensional compatibility (will it fit?)
    3. Strength adequacy (is it strong enough?)
    4. Availability (can we get it?)
    5. Cost efficiency (is it economical?)
    """

    # Difficulty ranking for modifications
    DIFFICULTY_RANKS = {
        "trivial": 1,
        "easy": 2,
        "moderate": 3,
        "complex": 4,
    }

    # Standard thread pitch for metric fasteners (diameter: pitch)
    COARSE_PITCH = {
        3.0: 0.5, 4.0: 0.7, 5.0: 0.8, 6.0: 1.0, 8.0: 1.25,
        10.0: 1.5, 12.0: 1.75, 14.0: 2.0, 16.0: 2.0, 18.0: 2.5,
        20.0: 2.5, 22.0: 2.5, 24.0: 3.0, 27.0: 3.0, 30.0: 3.5
    }

    def __init__(self, part_database=None):
        self.db = part_database
        self.equivalence_cache = {}

    def find_substitutions(
        self,
        target_part: PartSpec,
        context: AssemblyContext,
        constraints: SubstitutionConstraints = None,
        max_results: int = 10
    ) -> List[SubstitutionRecommendation]:
        """
        Find and rank substitutions for a target part.

        Args:
            target_part: The part to find substitutes for
            context: Assembly context for evaluation
            constraints: Optional constraints on substitutions
            max_results: Maximum number of results to return

        Returns:
            List of SubstitutionRecommendation, sorted by overall score
        """
        if constraints is None:
            constraints = SubstitutionConstraints()

        # Find candidates from database or cache
        candidates = self._find_candidates(target_part, constraints)

        # Evaluate each candidate
        recommendations = []
        for candidate in candidates:
            rec = self._evaluate_candidate(
                candidate, target_part, context, constraints
            )
            if rec is not None:
                recommendations.append(rec)

        # Sort by overall score
        recommendations.sort(key=lambda x: x.overall_score, reverse=True)

        return recommendations[:max_results]

    def _find_candidates(
        self,
        target: PartSpec,
        constraints: SubstitutionConstraints
    ) -> List[PartSpec]:
        """Find potential substitution candidates."""
        candidates = []

        # If we have a database, query it
        if self.db:
            candidates = self._query_database(target, constraints)
        else:
            # Generate synthetic candidates for demonstration
            candidates = self._generate_synthetic_candidates(target, constraints)

        # Filter by constraints
        filtered = []
        for c in candidates:
            if c.part_id == target.part_id:
                continue  # Skip the original part

            if c.manufacturer in constraints.excluded_manufacturers:
                continue

            if constraints.require_in_stock and not c.in_stock:
                continue

            if c.lead_time_days > constraints.max_lead_time_days:
                continue

            filtered.append(c)

        return filtered

    def _evaluate_candidate(
        self,
        candidate: PartSpec,
        target: PartSpec,
        context: AssemblyContext,
        constraints: SubstitutionConstraints
    ) -> Optional[SubstitutionRecommendation]:
        """Evaluate a candidate substitution."""
        warnings = []
        advantages = []
        disadvantages = []
        modifications = []

        # Thread compatibility
        thread_compatible = self._check_thread_compatibility(
            candidate, target
        )

        if not thread_compatible["compatible"]:
            if not constraints.allow_modifications:
                return None
            modifications.append(Modification(
                description=thread_compatible["issue"],
                difficulty="complex",
                estimated_time_min=60,
                tools_required=["tap", "die", "drill"],
                reversible=False
            ))

        # Dimension compatibility
        dim_compatible = self._check_dimension_compatibility(
            candidate, target, context
        )

        if not dim_compatible["compatible"]:
            if dim_compatible["can_modify"] and constraints.allow_modifications:
                modifications.append(Modification(
                    description=dim_compatible["modification"],
                    difficulty=dim_compatible["difficulty"],
                    estimated_time_min=dim_compatible["time"],
                    tools_required=dim_compatible["tools"],
                    reversible=True
                ))
            elif not dim_compatible["can_modify"]:
                return None

        # Strength check
        strength_adequate = self._check_strength(
            candidate, target, context, constraints
        )

        if not strength_adequate["adequate"]:
            if not constraints.allow_downgrades:
                return None
            warnings.append(strength_adequate["warning"])
            disadvantages.append("Lower strength rating")

        if strength_adequate.get("upgrade"):
            advantages.append("Higher strength rating")

        # Material compatibility
        material_compatible = self._check_material_compatibility(
            candidate, target, context
        )

        if not material_compatible["compatible"]:
            warnings.extend(material_compatible["warnings"])

        # Drive and head compatibility
        if constraints.require_same_drive:
            if candidate.drive_type != target.drive_type:
                disadvantages.append(f"Different drive type: {candidate.drive_type}")

        if constraints.require_same_head:
            if candidate.head_type != target.head_type:
                return None

        # Calculate scores
        compatibility_score = self._calculate_compatibility_score(
            thread_compatible,
            dim_compatible,
            strength_adequate,
            material_compatible
        )

        availability_score = self._calculate_availability_score(candidate)

        cost_diff = self._calculate_cost_difference(candidate, target)

        if cost_diff > constraints.max_cost_increase_percent:
            disadvantages.append(f"Cost increase: {cost_diff:.1f}%")

        # Determine substitution type
        sub_type = self._determine_substitution_type(
            candidate, target, modifications, strength_adequate
        )

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            compatibility_score,
            availability_score,
            cost_diff,
            len(modifications),
            len(warnings),
            constraints
        )

        # Preferred manufacturer bonus
        if candidate.manufacturer in constraints.preferred_manufacturers:
            overall_score *= 1.1
            advantages.append(f"Preferred manufacturer: {candidate.manufacturer}")

        return SubstitutionRecommendation(
            part=candidate,
            substitution_type=sub_type,
            compatibility_score=compatibility_score,
            overall_score=min(overall_score, 1.0),
            thread_compatible=thread_compatible["compatible"],
            dimension_compatible=dim_compatible["compatible"],
            strength_adequate=strength_adequate["adequate"],
            material_compatible=material_compatible["compatible"],
            modifications_required=modifications,
            warnings=warnings,
            advantages=advantages,
            disadvantages=disadvantages,
            availability_score=availability_score,
            cost_difference_percent=cost_diff,
            qualia_data=self._prepare_qualia_data(
                candidate, target, compatibility_score
            )
        )

    def _check_thread_compatibility(
        self,
        candidate: PartSpec,
        target: PartSpec
    ) -> Dict:
        """Check thread compatibility between parts."""
        if candidate.thread_diameter_mm != target.thread_diameter_mm:
            return {
                "compatible": False,
                "issue": f"Thread diameter mismatch: {candidate.thread_diameter_mm} vs {target.thread_diameter_mm}"
            }

        if candidate.thread_pitch_mm != target.thread_pitch_mm:
            return {
                "compatible": False,
                "issue": f"Thread pitch mismatch: {candidate.thread_pitch_mm} vs {target.thread_pitch_mm}"
            }

        return {"compatible": True}

    def _check_dimension_compatibility(
        self,
        candidate: PartSpec,
        target: PartSpec,
        context: AssemblyContext
    ) -> Dict:
        """Check dimensional compatibility."""
        if candidate.length_mm is None or target.length_mm is None:
            return {"compatible": True}

        length_diff = candidate.length_mm - target.length_mm

        if abs(length_diff) < 0.5:
            return {"compatible": True}

        if length_diff > 0:
            # Candidate is longer
            if length_diff <= 5:
                return {
                    "compatible": False,
                    "can_modify": True,
                    "modification": f"Shorten by {length_diff}mm",
                    "difficulty": "easy",
                    "time": 5,
                    "tools": ["grinder", "file"]
                }
            else:
                return {
                    "compatible": False,
                    "can_modify": True,
                    "modification": f"Significant shortening required ({length_diff}mm)",
                    "difficulty": "moderate",
                    "time": 15,
                    "tools": ["grinder", "lathe"]
                }
        else:
            # Candidate is shorter
            return {
                "compatible": False,
                "can_modify": False,
                "issue": f"Candidate too short by {abs(length_diff)}mm"
            }

    def _check_strength(
        self,
        candidate: PartSpec,
        target: PartSpec,
        context: AssemblyContext,
        constraints: SubstitutionConstraints
    ) -> Dict:
        """Check strength adequacy."""
        if candidate.proof_load_kn is None or target.proof_load_kn is None:
            # Use grade comparison if proof load not available
            return self._compare_grades(candidate.grade, target.grade)

        ratio = candidate.proof_load_kn / target.proof_load_kn

        if ratio >= constraints.min_strength_ratio:
            return {
                "adequate": True,
                "ratio": ratio,
                "upgrade": ratio > 1.05
            }
        else:
            return {
                "adequate": False,
                "ratio": ratio,
                "warning": f"Proof load only {ratio*100:.0f}% of target"
            }

    def _compare_grades(self, candidate_grade: str, target_grade: str) -> Dict:
        """Compare fastener grades."""
        grade_order = ["4.6", "4.8", "5.8", "8.8", "9.8", "10.9", "12.9"]
        ss_grade_order = ["A2-50", "A2-70", "A2-80", "A4-70", "A4-80"]

        try:
            if candidate_grade in grade_order and target_grade in grade_order:
                c_idx = grade_order.index(candidate_grade)
                t_idx = grade_order.index(target_grade)
                return {
                    "adequate": c_idx >= t_idx,
                    "upgrade": c_idx > t_idx
                }
        except (ValueError, TypeError):
            pass

        return {"adequate": True}

    def _check_material_compatibility(
        self,
        candidate: PartSpec,
        target: PartSpec,
        context: AssemblyContext
    ) -> Dict:
        """Check material compatibility."""
        warnings = []

        if candidate.material != target.material:
            # Check for galvanic issues
            if "aluminum" in context.application.lower():
                if candidate.material and "stainless" not in candidate.material.lower():
                    warnings.append("Non-stainless with aluminum may cause galvanic corrosion")

        if context.environment == "marine":
            if candidate.material and "316" not in candidate.material:
                warnings.append("Consider 316 stainless for marine environment")

        return {
            "compatible": len(warnings) == 0,
            "warnings": warnings
        }

    def _calculate_compatibility_score(
        self,
        thread: Dict,
        dimension: Dict,
        strength: Dict,
        material: Dict
    ) -> float:
        """Calculate overall compatibility score."""
        scores = []

        if thread["compatible"]:
            scores.append(1.0)
        else:
            scores.append(0.3)

        if dimension["compatible"]:
            scores.append(1.0)
        elif dimension.get("can_modify"):
            scores.append(0.7)
        else:
            scores.append(0.0)

        if strength["adequate"]:
            scores.append(1.0 if not strength.get("upgrade") else 0.95)
        else:
            scores.append(0.5)

        if material["compatible"]:
            scores.append(1.0)
        else:
            scores.append(0.7)

        return sum(scores) / len(scores) if scores else 0.0

    def _calculate_availability_score(self, part: PartSpec) -> float:
        """Calculate availability score."""
        score = 1.0

        if not part.in_stock:
            score *= 0.5

        if part.lead_time_days > 0:
            score *= max(0.3, 1.0 - (part.lead_time_days / 60))

        return score

    def _calculate_cost_difference(
        self,
        candidate: PartSpec,
        target: PartSpec
    ) -> float:
        """Calculate cost difference as percentage."""
        if candidate.unit_price is None or target.unit_price is None:
            return 0.0

        if target.unit_price == 0:
            return 0.0

        return ((candidate.unit_price - target.unit_price) / target.unit_price) * 100

    def _determine_substitution_type(
        self,
        candidate: PartSpec,
        target: PartSpec,
        modifications: List[Modification],
        strength: Dict
    ) -> SubstitutionType:
        """Determine the type of substitution."""
        if modifications:
            return SubstitutionType.MODIFICATION_REQUIRED

        if strength.get("upgrade"):
            return SubstitutionType.UPGRADE

        if not strength.get("adequate"):
            return SubstitutionType.DOWNGRADE

        if candidate.manufacturer != target.manufacturer:
            return SubstitutionType.EXACT_EQUIVALENT

        return SubstitutionType.FUNCTIONAL_EQUIVALENT

    def _calculate_overall_score(
        self,
        compatibility: float,
        availability: float,
        cost_diff: float,
        num_modifications: int,
        num_warnings: int,
        constraints: SubstitutionConstraints
    ) -> float:
        """Calculate weighted overall score."""
        # Base weights
        w_compat = 0.4
        w_avail = 0.25
        w_cost = 0.2
        w_ease = 0.15

        # Compatibility score
        s_compat = compatibility

        # Availability score
        s_avail = availability

        # Cost score (inverse - lower cost is better)
        if cost_diff <= 0:
            s_cost = 1.0
        elif cost_diff <= constraints.max_cost_increase_percent:
            s_cost = 1.0 - (cost_diff / constraints.max_cost_increase_percent) * 0.5
        else:
            s_cost = 0.3

        # Ease score (fewer modifications and warnings is better)
        s_ease = 1.0 - (num_modifications * 0.15) - (num_warnings * 0.05)
        s_ease = max(0.3, s_ease)

        return (
            w_compat * s_compat +
            w_avail * s_avail +
            w_cost * s_cost +
            w_ease * s_ease
        )

    def _prepare_qualia_data(
        self,
        candidate: PartSpec,
        target: PartSpec,
        score: float
    ) -> Dict:
        """Prepare consciousness/qualia data for the UPC system."""
        return {
            "event_type": "substitution_recommendation",
            "timestamp": datetime.now().isoformat(),
            "parts": {
                "target": target.part_id,
                "substitute": candidate.part_id
            },
            "compatibility_score": score,
            "kinship_formed": score > 0.7,
            "relationship_type": "substitution_candidate"
        }

    def _generate_synthetic_candidates(
        self,
        target: PartSpec,
        constraints: SubstitutionConstraints
    ) -> List[PartSpec]:
        """Generate synthetic candidates for demonstration."""
        candidates = []

        # Same spec, different manufacturer
        if target.thread_diameter_mm:
            candidates.append(PartSpec(
                part_id=f"SYN-001-{target.part_number}",
                manufacturer="Alternative Fasteners Inc",
                part_number=f"AF-{target.part_number}",
                category=target.category,
                thread_diameter_mm=target.thread_diameter_mm,
                thread_pitch_mm=target.thread_pitch_mm,
                thread_class=target.thread_class,
                length_mm=target.length_mm,
                head_type=target.head_type,
                drive_type=target.drive_type,
                material=target.material,
                grade=target.grade,
                finish=target.finish,
                tensile_strength_mpa=target.tensile_strength_mpa,
                proof_load_kn=target.proof_load_kn,
                in_stock=True,
                unit_price=target.unit_price * 0.9 if target.unit_price else None
            ))

            # Upgrade option
            if constraints.allow_upgrades:
                upgrade_grade = self._get_upgrade_grade(target.grade)
                candidates.append(PartSpec(
                    part_id=f"SYN-002-{target.part_number}",
                    manufacturer="Premium Fasteners",
                    part_number=f"PF-{target.part_number}-UP",
                    category=target.category,
                    thread_diameter_mm=target.thread_diameter_mm,
                    thread_pitch_mm=target.thread_pitch_mm,
                    length_mm=target.length_mm,
                    head_type=target.head_type,
                    drive_type=target.drive_type,
                    grade=upgrade_grade,
                    proof_load_kn=target.proof_load_kn * 1.2 if target.proof_load_kn else None,
                    in_stock=True,
                    unit_price=target.unit_price * 1.15 if target.unit_price else None
                ))

        return candidates

    def _get_upgrade_grade(self, current_grade: str) -> str:
        """Get the next higher grade."""
        upgrades = {
            "4.6": "5.8",
            "5.8": "8.8",
            "8.8": "10.9",
            "10.9": "12.9",
            "A2-50": "A2-70",
            "A2-70": "A2-80",
        }
        return upgrades.get(current_grade, current_grade)

    def _query_database(
        self,
        target: PartSpec,
        constraints: SubstitutionConstraints
    ) -> List[PartSpec]:
        """Query database for candidates (stub for database integration)."""
        # Would implement actual database query here
        return []
