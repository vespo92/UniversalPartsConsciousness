"""
Knowledge Aggregator - Aggregates and synthesizes swarm collective knowledge.

Combines learnings from multiple sources to create unified swarm wisdom.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import Learning, LearningType, Swarm


@dataclass
class AggregatedKnowledge:
    """Synthesized knowledge from multiple learnings."""
    category: str
    key: str
    content: dict[str, Any]
    confidence: float
    sample_count: int
    sources: list[UUID]
    last_updated: datetime


@dataclass
class KnowledgeSummary:
    """Summary of a swarm's collective knowledge."""
    swarm_id: UUID
    total_learnings: int
    knowledge_categories: dict[str, int]
    top_insights: list[AggregatedKnowledge]
    confidence_average: float
    freshness_score: float


class KnowledgeRepository(Protocol):
    """Protocol for knowledge data access."""

    async def get_swarm_learnings(
        self,
        swarm_id: UUID,
        learning_type: Optional[LearningType] = None,
        since: Optional[datetime] = None,
        limit: int = 1000,
    ) -> list[Learning]:
        """Get learnings for a swarm."""
        ...

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def update_swarm_knowledge(
        self,
        swarm_id: UUID,
        aggregated_knowledge: dict[str, Any],
    ) -> None:
        """Update swarm's aggregated knowledge."""
        ...


class KnowledgeAggregator:
    """
    Aggregates and synthesizes knowledge from individual learnings.
    """

    # Knowledge freshness decay (days)
    FRESHNESS_HALF_LIFE = 90

    # Minimum learnings for confident aggregation
    MIN_SAMPLES_FOR_AGGREGATION = 3

    def __init__(self, repository: KnowledgeRepository):
        self.repository = repository

    async def aggregate_swarm_knowledge(
        self,
        swarm_id: UUID,
    ) -> dict[str, AggregatedKnowledge]:
        """
        Aggregate all learnings in a swarm into synthesized knowledge.

        Args:
            swarm_id: The swarm to aggregate

        Returns:
            Dictionary of aggregated knowledge by category/key
        """
        # Get all learnings for the swarm
        learnings = await self.repository.get_swarm_learnings(swarm_id)

        if not learnings:
            return {}

        # Group learnings by type
        grouped: dict[LearningType, list[Learning]] = {}
        for learning in learnings:
            if learning.learning_type not in grouped:
                grouped[learning.learning_type] = []
            grouped[learning.learning_type].append(learning)

        # Aggregate each group
        aggregated = {}
        for learning_type, type_learnings in grouped.items():
            type_knowledge = self._aggregate_by_type(learning_type, type_learnings)
            aggregated.update(type_knowledge)

        return aggregated

    async def get_knowledge_summary(
        self,
        swarm_id: UUID,
    ) -> KnowledgeSummary:
        """
        Get a summary of a swarm's collective knowledge.

        Args:
            swarm_id: The swarm to summarize

        Returns:
            Knowledge summary
        """
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return KnowledgeSummary(
                swarm_id=swarm_id,
                total_learnings=0,
                knowledge_categories={},
                top_insights=[],
                confidence_average=0.0,
                freshness_score=0.0,
            )

        learnings = await self.repository.get_swarm_learnings(swarm_id)

        # Count by category
        categories: dict[str, int] = {}
        total_confidence = 0.0
        total_freshness = 0.0

        for learning in learnings:
            cat = learning.learning_type.value
            categories[cat] = categories.get(cat, 0) + 1
            total_confidence += learning.confidence
            total_freshness += self._calculate_freshness(learning.learned_at)

        # Get aggregated knowledge for top insights
        aggregated = await self.aggregate_swarm_knowledge(swarm_id)

        # Sort by confidence for top insights
        top_insights = sorted(
            aggregated.values(),
            key=lambda k: k.confidence,
            reverse=True,
        )[:10]

        return KnowledgeSummary(
            swarm_id=swarm_id,
            total_learnings=len(learnings),
            knowledge_categories=categories,
            top_insights=top_insights,
            confidence_average=total_confidence / len(learnings) if learnings else 0.0,
            freshness_score=total_freshness / len(learnings) if learnings else 0.0,
        )

    async def refresh_aggregation(
        self,
        swarm_id: UUID,
    ) -> bool:
        """
        Re-run aggregation and update swarm's stored knowledge.

        Args:
            swarm_id: The swarm to refresh

        Returns:
            True if successful
        """
        aggregated = await self.aggregate_swarm_knowledge(swarm_id)

        # Convert to storable format
        knowledge_dict = {}
        for key, agg_knowledge in aggregated.items():
            knowledge_dict[key] = {
                "category": agg_knowledge.category,
                "content": agg_knowledge.content,
                "confidence": agg_knowledge.confidence,
                "sample_count": agg_knowledge.sample_count,
                "sources": [str(s) for s in agg_knowledge.sources],
                "last_updated": agg_knowledge.last_updated.isoformat(),
            }

        await self.repository.update_swarm_knowledge(swarm_id, knowledge_dict)
        return True

    def _aggregate_by_type(
        self,
        learning_type: LearningType,
        learnings: list[Learning],
    ) -> dict[str, AggregatedKnowledge]:
        """Aggregate learnings of the same type."""
        if learning_type == LearningType.FAILURE_MODE:
            return self._aggregate_failures(learnings)
        elif learning_type == LearningType.SURVIVAL_LIMIT:
            return self._aggregate_survival(learnings)
        elif learning_type == LearningType.LONGEVITY_FACTOR:
            return self._aggregate_longevity(learnings)
        elif learning_type == LearningType.ENVIRONMENTAL_ADAPTATION:
            return self._aggregate_environmental(learnings)
        else:
            return self._aggregate_generic(learning_type, learnings)

    def _aggregate_failures(
        self,
        learnings: list[Learning],
    ) -> dict[str, AggregatedKnowledge]:
        """Aggregate failure mode learnings."""
        # Group by failure type
        by_failure_type: dict[str, list[Learning]] = {}
        for learning in learnings:
            failure_type = learning.content.get("failure_type", "unknown")
            if failure_type not in by_failure_type:
                by_failure_type[failure_type] = []
            by_failure_type[failure_type].append(learning)

        aggregated = {}
        for failure_type, type_learnings in by_failure_type.items():
            if len(type_learnings) < self.MIN_SAMPLES_FOR_AGGREGATION:
                continue

            # Aggregate prevention measures
            all_prevention = []
            all_factors = []
            total_confidence = 0.0
            sources = []
            latest_time = datetime.min

            for learning in type_learnings:
                all_prevention.extend(learning.content.get("prevention_measures", []))
                all_factors.extend(learning.content.get("contributing_factors", []))
                total_confidence += learning.confidence
                sources.append(learning.source_part_id)
                if learning.learned_at and learning.learned_at > latest_time:
                    latest_time = learning.learned_at

            # Count and rank prevention measures
            prevention_counts: dict[str, int] = {}
            for p in all_prevention:
                prevention_counts[p] = prevention_counts.get(p, 0) + 1

            ranked_prevention = sorted(
                prevention_counts.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            # Count contributing factors
            factor_counts: dict[str, int] = {}
            for f in all_factors:
                factor_counts[f] = factor_counts.get(f, 0) + 1

            key = f"failure_mode:{failure_type}"
            aggregated[key] = AggregatedKnowledge(
                category="failure_mode",
                key=failure_type,
                content={
                    "failure_type": failure_type,
                    "prevention_measures": [p[0] for p in ranked_prevention[:5]],
                    "contributing_factors": dict(factor_counts),
                    "occurrence_count": len(type_learnings),
                },
                confidence=total_confidence / len(type_learnings),
                sample_count=len(type_learnings),
                sources=[s for s in sources if s],
                last_updated=latest_time if latest_time != datetime.min else datetime.utcnow(),
            )

        return aggregated

    def _aggregate_survival(
        self,
        learnings: list[Learning],
    ) -> dict[str, AggregatedKnowledge]:
        """Aggregate survival limit learnings."""
        if len(learnings) < self.MIN_SAMPLES_FOR_AGGREGATION:
            return {}

        # Calculate statistics
        loads = []
        capacities = []
        total_confidence = 0.0
        sources = []
        latest_time = datetime.min

        for learning in learnings:
            load_info = learning.content.get("load_survived", {})
            loads.append(load_info.get("axial_load_n", 0))
            capacities.append(load_info.get("capacity_used_percent", 0))
            total_confidence += learning.confidence
            sources.append(learning.source_part_id)
            if learning.learned_at and learning.learned_at > latest_time:
                latest_time = learning.learned_at

        valid_loads = [l for l in loads if l > 0]
        valid_capacities = [c for c in capacities if c > 0]

        aggregated = {
            "survival_limit:aggregate": AggregatedKnowledge(
                category="survival_limit",
                key="aggregate",
                content={
                    "max_observed_load_n": max(valid_loads) if valid_loads else 0,
                    "avg_load_n": sum(valid_loads) / len(valid_loads) if valid_loads else 0,
                    "max_capacity_percent": max(valid_capacities) if valid_capacities else 0,
                    "avg_capacity_percent": sum(valid_capacities) / len(valid_capacities) if valid_capacities else 0,
                    "samples": len(learnings),
                },
                confidence=total_confidence / len(learnings),
                sample_count=len(learnings),
                sources=[s for s in sources if s],
                last_updated=latest_time if latest_time != datetime.min else datetime.utcnow(),
            )
        }

        return aggregated

    def _aggregate_longevity(
        self,
        learnings: list[Learning],
    ) -> dict[str, AggregatedKnowledge]:
        """Aggregate longevity factor learnings."""
        if len(learnings) < self.MIN_SAMPLES_FOR_AGGREGATION:
            return {}

        cycles = []
        all_factors = []
        total_confidence = 0.0
        sources = []
        latest_time = datetime.min

        for learning in learnings:
            cycles.append(learning.content.get("cycles_achieved", 0))
            all_factors.extend(learning.content.get("success_factors", []))
            total_confidence += learning.confidence
            sources.append(learning.source_part_id)
            if learning.learned_at and learning.learned_at > latest_time:
                latest_time = learning.learned_at

        valid_cycles = [c for c in cycles if c > 0]

        # Count success factors
        factor_counts: dict[str, int] = {}
        for f in all_factors:
            factor_counts[f] = factor_counts.get(f, 0) + 1

        ranked_factors = sorted(
            factor_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        aggregated = {
            "longevity:aggregate": AggregatedKnowledge(
                category="longevity_factor",
                key="aggregate",
                content={
                    "max_cycles": max(valid_cycles) if valid_cycles else 0,
                    "avg_cycles": sum(valid_cycles) / len(valid_cycles) if valid_cycles else 0,
                    "key_success_factors": [f[0] for f in ranked_factors[:5]],
                    "factor_frequency": dict(ranked_factors[:10]),
                    "samples": len(learnings),
                },
                confidence=total_confidence / len(learnings),
                sample_count=len(learnings),
                sources=[s for s in sources if s],
                last_updated=latest_time if latest_time != datetime.min else datetime.utcnow(),
            )
        }

        return aggregated

    def _aggregate_environmental(
        self,
        learnings: list[Learning],
    ) -> dict[str, AggregatedKnowledge]:
        """Aggregate environmental adaptation learnings."""
        # Group by challenge type
        by_challenge: dict[str, list[Learning]] = {}
        for learning in learnings:
            challenges = learning.content.get("environmental_challenges", [])
            for challenge in challenges:
                if challenge not in by_challenge:
                    by_challenge[challenge] = []
                by_challenge[challenge].append(learning)

        aggregated = {}
        for challenge, challenge_learnings in by_challenge.items():
            if len(challenge_learnings) < self.MIN_SAMPLES_FOR_AGGREGATION:
                continue

            all_adaptations = []
            total_confidence = 0.0
            sources = []
            latest_time = datetime.min

            for learning in challenge_learnings:
                all_adaptations.extend(learning.content.get("adaptation_strategies", []))
                total_confidence += learning.confidence
                sources.append(learning.source_part_id)
                if learning.learned_at and learning.learned_at > latest_time:
                    latest_time = learning.learned_at

            # Count adaptations
            adaptation_counts: dict[str, int] = {}
            for a in all_adaptations:
                adaptation_counts[a] = adaptation_counts.get(a, 0) + 1

            ranked_adaptations = sorted(
                adaptation_counts.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            key = f"environmental:{challenge}"
            aggregated[key] = AggregatedKnowledge(
                category="environmental_adaptation",
                key=challenge,
                content={
                    "challenge": challenge,
                    "effective_adaptations": [a[0] for a in ranked_adaptations[:5]],
                    "adaptation_frequency": dict(ranked_adaptations),
                    "samples": len(challenge_learnings),
                },
                confidence=total_confidence / len(challenge_learnings),
                sample_count=len(challenge_learnings),
                sources=[s for s in sources if s],
                last_updated=latest_time if latest_time != datetime.min else datetime.utcnow(),
            )

        return aggregated

    def _aggregate_generic(
        self,
        learning_type: LearningType,
        learnings: list[Learning],
    ) -> dict[str, AggregatedKnowledge]:
        """Generic aggregation for other learning types."""
        if len(learnings) < self.MIN_SAMPLES_FOR_AGGREGATION:
            return {}

        total_confidence = 0.0
        sources = []
        latest_time = datetime.min
        all_content: list[dict] = []

        for learning in learnings:
            all_content.append(learning.content)
            total_confidence += learning.confidence
            sources.append(learning.source_part_id)
            if learning.learned_at and learning.learned_at > latest_time:
                latest_time = learning.learned_at

        key = f"{learning_type.value}:aggregate"
        return {
            key: AggregatedKnowledge(
                category=learning_type.value,
                key="aggregate",
                content={
                    "sample_count": len(learnings),
                    "content_samples": all_content[:10],  # Store sample of content
                },
                confidence=total_confidence / len(learnings),
                sample_count=len(learnings),
                sources=[s for s in sources if s],
                last_updated=latest_time if latest_time != datetime.min else datetime.utcnow(),
            )
        }

    def _calculate_freshness(self, learned_at: Optional[datetime]) -> float:
        """Calculate freshness score based on age of learning."""
        if not learned_at:
            return 0.5

        age_days = (datetime.utcnow() - learned_at).days
        # Exponential decay with half-life
        freshness = 0.5 ** (age_days / self.FRESHNESS_HALF_LIFE)
        return freshness
