"""
Opportunity Ranker
Ranks and prioritizes innovation opportunities.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional
import logging

from ..types import InnovationOpportunity, OpportunityType


logger = logging.getLogger(__name__)


@dataclass
class RankingWeights:
    """Weights for ranking factors"""
    impact_weight: float = 0.3
    confidence_weight: float = 0.25
    market_size_weight: float = 0.25
    urgency_weight: float = 0.2


@dataclass
class RankingConfig:
    """Configuration for opportunity ranking"""
    weights: RankingWeights = None
    type_multipliers: Dict[OpportunityType, float] = None

    def __post_init__(self):
        if self.weights is None:
            self.weights = RankingWeights()
        if self.type_multipliers is None:
            self.type_multipliers = {
                OpportunityType.PREVENTION_INNOVATION: 1.2,
                OpportunityType.CROSS_DOMAIN_TRANSFER: 1.0,
                OpportunityType.MATERIAL_EVOLUTION: 0.9,
                OpportunityType.DESIGN_EVOLUTION: 0.9,
                OpportunityType.GAP_FILLING: 0.8,
            }


class OpportunityRanker:
    """
    Ranks innovation opportunities by potential impact and feasibility.

    Ranking factors:
    - Estimated impact score
    - Confidence in the opportunity
    - Affected market size
    - Urgency (based on failure rates)
    - Opportunity type preference
    """

    def __init__(self, config: Optional[RankingConfig] = None):
        self.config = config or RankingConfig()

    def rank_opportunities(
        self,
        opportunities: List[InnovationOpportunity],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[InnovationOpportunity]:
        """
        Rank opportunities by calculated priority.

        Args:
            opportunities: List of opportunities to rank
            context: Optional context for ranking adjustments

        Returns:
            List of opportunities sorted by rank
        """
        if not opportunities:
            return []

        # Calculate scores for each opportunity
        scored = []
        for opp in opportunities:
            score = self._calculate_score(opp, context)
            scored.append((opp, score))

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        # Update priority scores
        ranked = []
        for opp, score in scored:
            opp.priority_score = Decimal(str(round(score, 4)))
            ranked.append(opp)

        return ranked

    def _calculate_score(
        self,
        opportunity: InnovationOpportunity,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Calculate ranking score for an opportunity"""
        weights = self.config.weights

        # Impact score (0-1)
        impact = float(opportunity.estimated_impact_score)

        # Confidence score (0-1)
        confidence = float(opportunity.confidence)

        # Market size score (normalized)
        market_score = self._normalize_market_size(opportunity.affected_market_size)

        # Urgency score (derived from supporting patterns)
        urgency = self._calculate_urgency(opportunity)

        # Base score
        base_score = (
            impact * weights.impact_weight +
            confidence * weights.confidence_weight +
            market_score * weights.market_size_weight +
            urgency * weights.urgency_weight
        )

        # Apply type multiplier
        type_multiplier = self.config.type_multipliers.get(
            opportunity.opportunity_type, 1.0
        )
        score = base_score * type_multiplier

        # Apply context adjustments
        if context:
            score = self._apply_context_adjustments(score, opportunity, context)

        return min(score, 1.0)

    def _normalize_market_size(self, market_size: int) -> float:
        """Normalize market size to 0-1 scale"""
        if market_size <= 0:
            return 0.0

        # Log scale normalization
        # Assume max market size of 10M
        import math
        max_size = 10_000_000
        normalized = math.log10(market_size + 1) / math.log10(max_size + 1)
        return min(normalized, 1.0)

    def _calculate_urgency(self, opportunity: InnovationOpportunity) -> float:
        """Calculate urgency based on opportunity type and context"""
        # Prevention innovations are more urgent
        if opportunity.opportunity_type == OpportunityType.PREVENTION_INNOVATION:
            return 0.8

        # Gap filling has moderate urgency
        if opportunity.opportunity_type == OpportunityType.GAP_FILLING:
            return 0.6

        # Evolution opportunities are less urgent
        if opportunity.opportunity_type in [
            OpportunityType.MATERIAL_EVOLUTION,
            OpportunityType.DESIGN_EVOLUTION,
        ]:
            return 0.4

        return 0.5

    def _apply_context_adjustments(
        self,
        score: float,
        opportunity: InnovationOpportunity,
        context: Dict[str, Any],
    ) -> float:
        """Apply context-based adjustments to score"""
        adjusted = score

        # Boost opportunities in priority domains
        priority_domains = context.get("priority_domains", [])
        if opportunity.source_domain in priority_domains or opportunity.target_domain in priority_domains:
            adjusted *= 1.2

        # Boost opportunities with high supporting pattern count
        pattern_count = len(opportunity.supporting_patterns)
        if pattern_count > 5:
            adjusted *= 1.1

        # Apply resource constraints
        if context.get("limited_resources", False):
            # Prefer high-confidence opportunities
            adjusted *= (0.7 + float(opportunity.confidence) * 0.3)

        return adjusted

    def filter_by_threshold(
        self,
        opportunities: List[InnovationOpportunity],
        threshold: float = 0.5,
    ) -> List[InnovationOpportunity]:
        """Filter opportunities by minimum priority score"""
        return [
            opp for opp in opportunities
            if float(opp.priority_score) >= threshold
        ]

    def group_by_type(
        self,
        opportunities: List[InnovationOpportunity],
    ) -> Dict[OpportunityType, List[InnovationOpportunity]]:
        """Group opportunities by type"""
        groups: Dict[OpportunityType, List[InnovationOpportunity]] = {}

        for opp in opportunities:
            if opp.opportunity_type not in groups:
                groups[opp.opportunity_type] = []
            groups[opp.opportunity_type].append(opp)

        return groups

    def get_actionable_recommendations(
        self,
        opportunities: List[InnovationOpportunity],
        max_recommendations: int = 5,
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations from top opportunities"""
        top = opportunities[:max_recommendations]

        recommendations = []
        for i, opp in enumerate(top, 1):
            recommendations.append({
                "rank": i,
                "title": opp.title,
                "type": opp.opportunity_type.value,
                "priority_score": float(opp.priority_score),
                "action": opp.proposed_solution,
                "expected_impact": float(opp.estimated_impact_score),
                "confidence": float(opp.confidence),
                "status": opp.status,
            })

        return recommendations
