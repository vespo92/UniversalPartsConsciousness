"""
ORACLE Substitution Ranking Algorithm
Multi-criteria scoring for substitution recommendations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum


class RankingCriteria(Enum):
    """Criteria for ranking substitutions."""
    COMPATIBILITY = "compatibility"
    AVAILABILITY = "availability"
    COST = "cost"
    STRENGTH = "strength"
    EASE_OF_USE = "ease"
    MANUFACTURER_PREFERENCE = "manufacturer"
    COMMUNITY_RATING = "community"
    CONSCIOUSNESS_SCORE = "consciousness"


@dataclass
class CriterionWeight:
    """Weight configuration for a ranking criterion."""
    criterion: RankingCriteria
    weight: float  # 0.0 to 1.0
    importance: str  # "critical", "high", "medium", "low"
    threshold: Optional[float] = None  # Minimum acceptable score


@dataclass
class RankingProfile:
    """A complete ranking configuration profile."""
    name: str
    description: str
    weights: List[CriterionWeight]

    def get_weight(self, criterion: RankingCriteria) -> float:
        """Get weight for a specific criterion."""
        for w in self.weights:
            if w.criterion == criterion:
                return w.weight
        return 0.0


# Pre-defined ranking profiles
RANKING_PROFILES = {
    "balanced": RankingProfile(
        name="Balanced",
        description="Equal consideration of all factors",
        weights=[
            CriterionWeight(RankingCriteria.COMPATIBILITY, 0.25, "high"),
            CriterionWeight(RankingCriteria.AVAILABILITY, 0.20, "high"),
            CriterionWeight(RankingCriteria.COST, 0.20, "medium"),
            CriterionWeight(RankingCriteria.STRENGTH, 0.15, "high"),
            CriterionWeight(RankingCriteria.EASE_OF_USE, 0.10, "medium"),
            CriterionWeight(RankingCriteria.MANUFACTURER_PREFERENCE, 0.05, "low"),
            CriterionWeight(RankingCriteria.COMMUNITY_RATING, 0.05, "low"),
        ]
    ),
    "safety_critical": RankingProfile(
        name="Safety Critical",
        description="Prioritizes strength and reliability over cost",
        weights=[
            CriterionWeight(RankingCriteria.STRENGTH, 0.35, "critical", threshold=0.9),
            CriterionWeight(RankingCriteria.COMPATIBILITY, 0.30, "critical", threshold=0.8),
            CriterionWeight(RankingCriteria.MANUFACTURER_PREFERENCE, 0.15, "high"),
            CriterionWeight(RankingCriteria.COMMUNITY_RATING, 0.10, "high"),
            CriterionWeight(RankingCriteria.AVAILABILITY, 0.05, "medium"),
            CriterionWeight(RankingCriteria.COST, 0.05, "low"),
        ]
    ),
    "cost_focused": RankingProfile(
        name="Cost Focused",
        description="Minimizes cost while maintaining basic compatibility",
        weights=[
            CriterionWeight(RankingCriteria.COST, 0.35, "high"),
            CriterionWeight(RankingCriteria.AVAILABILITY, 0.25, "high"),
            CriterionWeight(RankingCriteria.COMPATIBILITY, 0.20, "high", threshold=0.6),
            CriterionWeight(RankingCriteria.STRENGTH, 0.10, "medium", threshold=0.7),
            CriterionWeight(RankingCriteria.EASE_OF_USE, 0.10, "medium"),
        ]
    ),
    "quick_availability": RankingProfile(
        name="Quick Availability",
        description="Prioritizes in-stock and fast delivery",
        weights=[
            CriterionWeight(RankingCriteria.AVAILABILITY, 0.40, "critical", threshold=0.8),
            CriterionWeight(RankingCriteria.COMPATIBILITY, 0.25, "high", threshold=0.7),
            CriterionWeight(RankingCriteria.EASE_OF_USE, 0.15, "high"),
            CriterionWeight(RankingCriteria.STRENGTH, 0.10, "medium"),
            CriterionWeight(RankingCriteria.COST, 0.10, "low"),
        ]
    ),
    "consciousness_aware": RankingProfile(
        name="Consciousness Aware",
        description="Incorporates UPC consciousness scoring",
        weights=[
            CriterionWeight(RankingCriteria.COMPATIBILITY, 0.25, "high"),
            CriterionWeight(RankingCriteria.CONSCIOUSNESS_SCORE, 0.20, "high"),
            CriterionWeight(RankingCriteria.COMMUNITY_RATING, 0.15, "high"),
            CriterionWeight(RankingCriteria.STRENGTH, 0.15, "high"),
            CriterionWeight(RankingCriteria.AVAILABILITY, 0.10, "medium"),
            CriterionWeight(RankingCriteria.COST, 0.10, "medium"),
            CriterionWeight(RankingCriteria.EASE_OF_USE, 0.05, "low"),
        ]
    ),
}


@dataclass
class ScoredCandidate:
    """A candidate with computed scores."""
    candidate_id: str
    criteria_scores: Dict[RankingCriteria, float]
    weighted_score: float
    meets_thresholds: bool
    disqualification_reason: Optional[str] = None


class SubstitutionRanker:
    """
    Multi-criteria ranking engine for substitution recommendations.

    Supports:
    - Configurable weight profiles
    - Threshold-based filtering
    - Custom scoring functions
    - Pareto-optimal filtering
    """

    def __init__(self, profile: RankingProfile = None):
        self.profile = profile or RANKING_PROFILES["balanced"]
        self.custom_scorers: Dict[RankingCriteria, Callable] = {}

    def set_profile(self, profile_name: str):
        """Set ranking profile by name."""
        if profile_name in RANKING_PROFILES:
            self.profile = RANKING_PROFILES[profile_name]
        else:
            raise ValueError(f"Unknown profile: {profile_name}")

    def set_custom_scorer(
        self,
        criterion: RankingCriteria,
        scorer: Callable[[Dict], float]
    ):
        """Set a custom scoring function for a criterion."""
        self.custom_scorers[criterion] = scorer

    def rank_candidates(
        self,
        candidates: List[Dict],
        context: Dict = None
    ) -> List[ScoredCandidate]:
        """
        Rank candidates using the current profile.

        Args:
            candidates: List of candidate data dictionaries
            context: Optional context for scoring

        Returns:
            List of ScoredCandidate, sorted by score
        """
        scored = []

        for candidate in candidates:
            scored_candidate = self._score_candidate(candidate, context)
            scored.append(scored_candidate)

        # Filter by thresholds
        qualified = [s for s in scored if s.meets_thresholds]
        disqualified = [s for s in scored if not s.meets_thresholds]

        # Sort qualified by score
        qualified.sort(key=lambda x: x.weighted_score, reverse=True)

        # Append disqualified at end
        return qualified + disqualified

    def _score_candidate(
        self,
        candidate: Dict,
        context: Dict
    ) -> ScoredCandidate:
        """Score a single candidate."""
        criteria_scores = {}
        meets_thresholds = True
        disqualification = None

        for weight in self.profile.weights:
            criterion = weight.criterion

            # Get score
            if criterion in self.custom_scorers:
                score = self.custom_scorers[criterion](candidate)
            else:
                score = self._default_score(criterion, candidate, context)

            criteria_scores[criterion] = score

            # Check threshold
            if weight.threshold is not None and score < weight.threshold:
                meets_thresholds = False
                disqualification = f"Failed {criterion.value} threshold: {score:.2f} < {weight.threshold}"

        # Calculate weighted score
        weighted_score = sum(
            criteria_scores.get(w.criterion, 0.0) * w.weight
            for w in self.profile.weights
        )

        return ScoredCandidate(
            candidate_id=candidate.get("id", "unknown"),
            criteria_scores=criteria_scores,
            weighted_score=weighted_score,
            meets_thresholds=meets_thresholds,
            disqualification_reason=disqualification
        )

    def _default_score(
        self,
        criterion: RankingCriteria,
        candidate: Dict,
        context: Dict
    ) -> float:
        """Default scoring function for each criterion."""
        if criterion == RankingCriteria.COMPATIBILITY:
            return candidate.get("compatibility_score", 0.5)

        elif criterion == RankingCriteria.AVAILABILITY:
            if candidate.get("in_stock"):
                base = 1.0
            else:
                base = 0.3
            lead_time = candidate.get("lead_time_days", 0)
            return base * max(0.3, 1.0 - lead_time / 60)

        elif criterion == RankingCriteria.COST:
            cost_diff = candidate.get("cost_difference_percent", 0)
            if cost_diff <= 0:
                return 1.0
            elif cost_diff <= 25:
                return 1.0 - (cost_diff / 50)
            else:
                return max(0.1, 0.5 - (cost_diff / 100))

        elif criterion == RankingCriteria.STRENGTH:
            ratio = candidate.get("strength_ratio", 1.0)
            if ratio >= 1.0:
                return min(1.0, 0.9 + (ratio - 1.0) * 0.2)
            else:
                return max(0.0, ratio)

        elif criterion == RankingCriteria.EASE_OF_USE:
            mods = candidate.get("modifications_count", 0)
            warnings = candidate.get("warnings_count", 0)
            return max(0.3, 1.0 - mods * 0.15 - warnings * 0.05)

        elif criterion == RankingCriteria.MANUFACTURER_PREFERENCE:
            if context and candidate.get("manufacturer") in context.get("preferred_manufacturers", []):
                return 1.0
            return 0.5

        elif criterion == RankingCriteria.COMMUNITY_RATING:
            return candidate.get("community_rating", 0.5)

        elif criterion == RankingCriteria.CONSCIOUSNESS_SCORE:
            return candidate.get("consciousness_level", 0) / 5.0

        return 0.5

    def get_pareto_optimal(
        self,
        scored: List[ScoredCandidate],
        criteria: List[RankingCriteria]
    ) -> List[ScoredCandidate]:
        """
        Filter to Pareto-optimal candidates.

        A candidate is Pareto-optimal if no other candidate
        is better in all specified criteria.
        """
        pareto = []

        for candidate in scored:
            is_dominated = False

            for other in scored:
                if other.candidate_id == candidate.candidate_id:
                    continue

                # Check if other dominates candidate
                all_better = all(
                    other.criteria_scores.get(c, 0) >= candidate.criteria_scores.get(c, 0)
                    for c in criteria
                )
                some_strictly_better = any(
                    other.criteria_scores.get(c, 0) > candidate.criteria_scores.get(c, 0)
                    for c in criteria
                )

                if all_better and some_strictly_better:
                    is_dominated = True
                    break

            if not is_dominated:
                pareto.append(candidate)

        return pareto

    def explain_ranking(
        self,
        candidate: ScoredCandidate
    ) -> str:
        """Generate human-readable explanation of ranking."""
        lines = [f"Ranking Explanation for {candidate.candidate_id}:"]
        lines.append(f"  Overall Score: {candidate.weighted_score:.3f}")
        lines.append("")
        lines.append("  Criteria Breakdown:")

        for weight in self.profile.weights:
            criterion = weight.criterion
            score = candidate.criteria_scores.get(criterion, 0.0)
            weighted = score * weight.weight
            status = ""

            if weight.threshold is not None:
                if score >= weight.threshold:
                    status = " [PASS]"
                else:
                    status = f" [FAIL: < {weight.threshold}]"

            lines.append(
                f"    {criterion.value:20s}: {score:.2f} x {weight.weight:.2f} = {weighted:.3f}{status}"
            )

        if not candidate.meets_thresholds:
            lines.append("")
            lines.append(f"  DISQUALIFIED: {candidate.disqualification_reason}")

        return "\n".join(lines)


def create_custom_profile(
    name: str,
    weights: Dict[str, float],
    thresholds: Dict[str, float] = None
) -> RankingProfile:
    """
    Create a custom ranking profile.

    Args:
        name: Profile name
        weights: Dict mapping criterion name to weight
        thresholds: Optional dict mapping criterion name to threshold

    Returns:
        New RankingProfile
    """
    thresholds = thresholds or {}

    criterion_weights = []
    for criterion_name, weight in weights.items():
        try:
            criterion = RankingCriteria(criterion_name)
        except ValueError:
            continue

        threshold = thresholds.get(criterion_name)

        # Determine importance from weight
        if weight >= 0.3:
            importance = "critical"
        elif weight >= 0.2:
            importance = "high"
        elif weight >= 0.1:
            importance = "medium"
        else:
            importance = "low"

        criterion_weights.append(CriterionWeight(
            criterion=criterion,
            weight=weight,
            importance=importance,
            threshold=threshold
        ))

    return RankingProfile(
        name=name,
        description=f"Custom profile: {name}",
        weights=criterion_weights
    )
