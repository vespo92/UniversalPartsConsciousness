"""
Legend Scorer - Cultural significance scoring system.

Calculates the "legend score" for engines based on their cultural impact,
racing heritage, tuning culture, reliability, and innovation.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class LegendTier(Enum):
    """Legend tier classifications based on cultural score."""
    MYTHICAL = "mythical"       # 0.9+ : 2JZ, 13B, Hemi
    LEGENDARY = "legendary"     # 0.75+: K20, RB26, LS1
    ICONIC = "iconic"           # 0.6+ : SR20, B18C, N54
    RESPECTED = "respected"     # 0.4+ : Common performance engines
    RECOGNIZED = "recognized"   # 0.2+ : Notable but not famous
    DOCUMENTED = "documented"   # <0.2 : Basic documentation only


@dataclass
class SignificanceDimension:
    """Configuration for a significance dimension."""
    name: str
    description: str
    weight: float
    metrics: List[str]


@dataclass
class LegendScoreResult:
    """Result of a legend score calculation."""
    engine_code: str
    score: float
    tier: LegendTier
    dimension_scores: Dict[str, float]
    breakdown: Dict[str, Any]
    rationale: str


# Pre-calculated legend scores for known engines
KNOWN_LEGEND_SCORES = {
    # MYTHICAL tier
    "2JZ-GTE": {"score": 0.95, "tier": LegendTier.MYTHICAL},
    "13B-REW": {"score": 0.92, "tier": LegendTier.MYTHICAL},
    "426 Hemi": {"score": 0.94, "tier": LegendTier.MYTHICAL},
    "RB26DETT": {"score": 0.93, "tier": LegendTier.MYTHICAL},
    "F20C": {"score": 0.90, "tier": LegendTier.MYTHICAL},

    # LEGENDARY tier
    "K20A": {"score": 0.88, "tier": LegendTier.LEGENDARY},
    "B18C5": {"score": 0.85, "tier": LegendTier.LEGENDARY},
    "LS1": {"score": 0.87, "tier": LegendTier.LEGENDARY},
    "LS3": {"score": 0.82, "tier": LegendTier.LEGENDARY},
    "S54": {"score": 0.84, "tier": LegendTier.LEGENDARY},
    "EJ257": {"score": 0.80, "tier": LegendTier.LEGENDARY},
    "4G63T": {"score": 0.86, "tier": LegendTier.LEGENDARY},
    "VR38DETT": {"score": 0.83, "tier": LegendTier.LEGENDARY},

    # ICONIC tier
    "SR20DET": {"score": 0.72, "tier": LegendTier.ICONIC},
    "B16A": {"score": 0.70, "tier": LegendTier.ICONIC},
    "N54": {"score": 0.68, "tier": LegendTier.ICONIC},
    "B58": {"score": 0.65, "tier": LegendTier.ICONIC},
    "VQ35DE": {"score": 0.62, "tier": LegendTier.ICONIC},
    "Coyote": {"score": 0.70, "tier": LegendTier.ICONIC},
    "LT1": {"score": 0.68, "tier": LegendTier.ICONIC},
}


class LegendScorer:
    """
    Calculates the cultural "legend score" for engines.

    The legend score quantifies cultural significance through
    weighted evaluation of multiple dimensions:
    - Racing Heritage (25%)
    - Tuning Culture (20%)
    - Reliability Reputation (20%)
    - Engineering Innovation (20%)
    - Pop Culture Presence (15%)
    """

    DIMENSIONS = {
        "racing_heritage": SignificanceDimension(
            name="Racing Heritage",
            description="Competition history and achievements",
            weight=0.25,
            metrics=[
                "championship_wins",
                "race_victories",
                "lap_records",
                "notable_drivers",
                "iconic_moments"
            ]
        ),
        "tuning_culture": SignificanceDimension(
            name="Tuning Culture",
            description="Aftermarket support and modification culture",
            weight=0.20,
            metrics=[
                "aftermarket_parts_availability",
                "community_knowledge_base",
                "tuning_potential",
                "build_variety",
                "influencer_builds"
            ]
        ),
        "reliability": SignificanceDimension(
            name="Reliability Reputation",
            description="Real-world reliability and durability",
            weight=0.20,
            metrics=[
                "mileage_records",
                "abuse_tolerance",
                "service_simplicity",
                "parts_availability",
                "community_trust"
            ]
        ),
        "innovation": SignificanceDimension(
            name="Engineering Innovation",
            description="Technical innovations and engineering achievement",
            weight=0.20,
            metrics=[
                "patents_filed",
                "technology_firsts",
                "efficiency_achievements",
                "design_elegance",
                "influence_on_industry"
            ]
        ),
        "pop_culture": SignificanceDimension(
            name="Pop Culture Presence",
            description="Presence in media, games, and popular culture",
            weight=0.15,
            metrics=[
                "movie_appearances",
                "game_representations",
                "music_references",
                "social_media_presence",
                "meme_status"
            ]
        )
    }

    def __init__(self):
        """Initialize the legend scorer."""
        self._cached_scores: Dict[str, LegendScoreResult] = {}

    def calculate_score(
        self,
        engine_code: str,
        cultural_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate the legend score for an engine.

        Args:
            engine_code: Engine code to evaluate
            cultural_data: Optional cultural significance data

        Returns:
            Dictionary with score, tier, and breakdown
        """
        # Check for pre-calculated known score
        if engine_code in KNOWN_LEGEND_SCORES:
            known = KNOWN_LEGEND_SCORES[engine_code]
            tier = known["tier"]
            score = known["score"]
            return {
                "engine_code": engine_code,
                "score": score,
                "tier": tier.value,
                "tier_display": self._get_tier_display(tier),
                "dimension_scores": self._get_estimated_dimensions(score),
                "rationale": self._generate_rationale(engine_code, tier, score),
                "source": "known_legend"
            }

        # Calculate from provided data
        if cultural_data:
            dimension_scores = {}
            total_score = 0.0

            for dim_key, dim_config in self.DIMENSIONS.items():
                dim_data = cultural_data.get(dim_key, {})
                dim_score = self._evaluate_dimension(dim_data, dim_config.metrics)
                dimension_scores[dim_key] = dim_score
                total_score += dim_score * dim_config.weight

            tier = self._assign_tier(total_score)

            return {
                "engine_code": engine_code,
                "score": round(total_score, 3),
                "tier": tier.value,
                "tier_display": self._get_tier_display(tier),
                "dimension_scores": dimension_scores,
                "rationale": self._generate_rationale(engine_code, tier, total_score),
                "source": "calculated"
            }

        # No data available - return documented tier
        return {
            "engine_code": engine_code,
            "score": 0.1,
            "tier": LegendTier.DOCUMENTED.value,
            "tier_display": self._get_tier_display(LegendTier.DOCUMENTED),
            "dimension_scores": {},
            "rationale": f"Insufficient data to score {engine_code}. Basic documentation only.",
            "source": "default"
        }

    def _evaluate_dimension(
        self,
        dim_data: Dict[str, Any],
        metrics: List[str]
    ) -> float:
        """
        Evaluate a single dimension based on its metrics.

        Returns a score from 0.0 to 1.0.
        """
        if not dim_data:
            return 0.0

        scores = []
        for metric in metrics:
            value = dim_data.get(metric, 0)
            if isinstance(value, bool):
                scores.append(1.0 if value else 0.0)
            elif isinstance(value, (int, float)):
                # Normalize to 0-1 range (assume max of 10)
                scores.append(min(1.0, value / 10))
            elif isinstance(value, list):
                # Count-based: more items = higher score
                scores.append(min(1.0, len(value) / 10))
            elif isinstance(value, str):
                # String presence = some score
                scores.append(0.5 if value else 0.0)

        return sum(scores) / len(scores) if scores else 0.0

    def _assign_tier(self, score: float) -> LegendTier:
        """Assign a legend tier based on score."""
        if score >= 0.9:
            return LegendTier.MYTHICAL
        elif score >= 0.75:
            return LegendTier.LEGENDARY
        elif score >= 0.6:
            return LegendTier.ICONIC
        elif score >= 0.4:
            return LegendTier.RESPECTED
        elif score >= 0.2:
            return LegendTier.RECOGNIZED
        else:
            return LegendTier.DOCUMENTED

    def _get_tier_display(self, tier: LegendTier) -> str:
        """Get display name for tier."""
        displays = {
            LegendTier.MYTHICAL: "MYTHICAL - The Immortal Icons",
            LegendTier.LEGENDARY: "LEGENDARY - Engineering Masterpieces",
            LegendTier.ICONIC: "ICONIC - Enthusiast Favorites",
            LegendTier.RESPECTED: "RESPECTED - Proven Performers",
            LegendTier.RECOGNIZED: "RECOGNIZED - Notable Mention",
            LegendTier.DOCUMENTED: "DOCUMENTED - Historical Record"
        }
        return displays.get(tier, tier.value)

    def _get_estimated_dimensions(self, score: float) -> Dict[str, float]:
        """Estimate dimension scores from overall score."""
        # Distribute score roughly evenly with some variation
        base = score
        return {
            "racing_heritage": round(base * 1.1, 2),
            "tuning_culture": round(base * 0.95, 2),
            "reliability": round(base * 1.05, 2),
            "innovation": round(base * 0.9, 2),
            "pop_culture": round(base * 1.0, 2)
        }

    def _generate_rationale(
        self,
        engine_code: str,
        tier: LegendTier,
        score: float
    ) -> str:
        """Generate a narrative rationale for the score."""
        rationales = {
            LegendTier.MYTHICAL: (
                f"The {engine_code} has achieved MYTHICAL status in automotive culture. "
                f"This engine is spoken of with reverence, featured in countless builds, "
                f"and represents the pinnacle of its era's engineering."
            ),
            LegendTier.LEGENDARY: (
                f"The {engine_code} is LEGENDARY - a proven performer with extensive "
                f"racing pedigree, strong aftermarket support, and devoted following. "
                f"This engine defines its category."
            ),
            LegendTier.ICONIC: (
                f"The {engine_code} is ICONIC - well-known among enthusiasts with "
                f"good aftermarket support and notable achievements. A staple of "
                f"the tuning community."
            ),
            LegendTier.RESPECTED: (
                f"The {engine_code} is RESPECTED - a solid performer known for "
                f"reliability and capability. Popular choice for those who know."
            ),
            LegendTier.RECOGNIZED: (
                f"The {engine_code} is RECOGNIZED - notable in its niche with "
                f"dedicated but smaller following."
            ),
            LegendTier.DOCUMENTED: (
                f"The {engine_code} is DOCUMENTED for historical record. "
                f"Limited cultural impact but preserved for completeness."
            )
        }
        return rationales.get(tier, f"{engine_code}: Score {score}")

    def get_tier_examples(self, tier: LegendTier) -> List[str]:
        """Get example engines for a tier."""
        examples = {
            LegendTier.MYTHICAL: ["2JZ-GTE", "13B-REW", "426 Hemi", "RB26DETT"],
            LegendTier.LEGENDARY: ["K20A", "LS1", "S54", "4G63T", "B18C5"],
            LegendTier.ICONIC: ["SR20DET", "B16A", "N54", "VQ35DE", "Coyote"],
            LegendTier.RESPECTED: ["K24A", "FA20", "N52", "VQ37VHR"],
            LegendTier.RECOGNIZED: ["EA888", "B48", "L15B"],
            LegendTier.DOCUMENTED: []
        }
        return examples.get(tier, [])

    def compare_engines(
        self,
        engine_codes: List[str]
    ) -> List[Dict[str, Any]]:
        """Compare legend scores for multiple engines."""
        results = []
        for code in engine_codes:
            result = self.calculate_score(code)
            results.append(result)

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
