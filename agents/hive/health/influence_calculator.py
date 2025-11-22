"""
Influence Calculator - Calculates part influence weights within swarms.

Influence determines how strongly a part's contributions affect
the swarm's collective knowledge.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from uuid import UUID


@dataclass
class InfluenceFactors:
    """Factors contributing to influence calculation."""
    consciousness_factor: float  # From part's consciousness level
    contribution_factor: float   # From contribution history
    seniority_factor: float      # From time in swarm
    quality_factor: float        # From learning quality/acceptance
    network_factor: float        # From connections to other parts


@dataclass
class InfluenceResult:
    """Result of influence calculation."""
    part_id: UUID
    swarm_id: UUID
    influence_weight: float
    factors: InfluenceFactors
    rank_in_swarm: int
    percentile: float


class InfluenceRepository(Protocol):
    """Protocol for influence data operations."""

    async def get_part_consciousness(self, part_id: UUID) -> float:
        """Get part's consciousness level."""
        ...

    async def get_contribution_count(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> int:
        """Get contribution count for part in swarm."""
        ...

    async def get_join_date(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> Optional[datetime]:
        """Get when part joined swarm."""
        ...

    async def get_learning_acceptance_rate(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> float:
        """Get rate at which part's learnings are accepted."""
        ...

    async def get_connection_count(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> int:
        """Get count of connections to other parts."""
        ...

    async def get_all_influences(
        self,
        swarm_id: UUID,
    ) -> list[tuple[UUID, float]]:
        """Get all part influences in a swarm."""
        ...


class InfluenceCalculator:
    """
    Calculates influence weights for parts within swarms.
    """

    # Weight factors for influence calculation
    CONSCIOUSNESS_WEIGHT = 0.35
    CONTRIBUTION_WEIGHT = 0.25
    SENIORITY_WEIGHT = 0.15
    QUALITY_WEIGHT = 0.15
    NETWORK_WEIGHT = 0.10

    # Normalization constants
    MAX_CONSCIOUSNESS = 5.0
    CONTRIBUTION_SATURATION = 100  # Contributions beyond this have diminishing returns
    SENIORITY_SATURATION_DAYS = 365
    NETWORK_SATURATION = 50

    def __init__(self, repository: InfluenceRepository):
        self.repository = repository

    async def calculate_influence(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> InfluenceResult:
        """
        Calculate influence weight for a part in a swarm.

        Args:
            part_id: The part to calculate for
            swarm_id: The swarm context

        Returns:
            Influence calculation result
        """
        # Get all factors
        consciousness = await self.repository.get_part_consciousness(part_id)
        contributions = await self.repository.get_contribution_count(part_id, swarm_id)
        join_date = await self.repository.get_join_date(part_id, swarm_id)
        acceptance_rate = await self.repository.get_learning_acceptance_rate(part_id, swarm_id)
        connections = await self.repository.get_connection_count(part_id, swarm_id)

        # Calculate individual factors
        consciousness_factor = min(consciousness / self.MAX_CONSCIOUSNESS, 1.0)

        contribution_factor = self._diminishing_returns(
            contributions, self.CONTRIBUTION_SATURATION
        )

        seniority_factor = 0.0
        if join_date:
            days_in_swarm = (datetime.utcnow() - join_date).days
            seniority_factor = self._diminishing_returns(
                days_in_swarm, self.SENIORITY_SATURATION_DAYS
            )

        quality_factor = acceptance_rate  # Already 0-1

        network_factor = self._diminishing_returns(
            connections, self.NETWORK_SATURATION
        )

        # Combine factors
        factors = InfluenceFactors(
            consciousness_factor=consciousness_factor,
            contribution_factor=contribution_factor,
            seniority_factor=seniority_factor,
            quality_factor=quality_factor,
            network_factor=network_factor,
        )

        influence_weight = (
            consciousness_factor * self.CONSCIOUSNESS_WEIGHT +
            contribution_factor * self.CONTRIBUTION_WEIGHT +
            seniority_factor * self.SENIORITY_WEIGHT +
            quality_factor * self.QUALITY_WEIGHT +
            network_factor * self.NETWORK_WEIGHT
        )

        influence_weight = round(min(influence_weight, 1.0), 4)

        # Get rank
        rank, percentile = await self._get_rank(swarm_id, part_id, influence_weight)

        return InfluenceResult(
            part_id=part_id,
            swarm_id=swarm_id,
            influence_weight=influence_weight,
            factors=factors,
            rank_in_swarm=rank,
            percentile=percentile,
        )

    async def recalculate_swarm_influences(
        self,
        swarm_id: UUID,
    ) -> list[InfluenceResult]:
        """
        Recalculate influences for all members of a swarm.

        Args:
            swarm_id: The swarm to recalculate

        Returns:
            List of influence results
        """
        # This would get all members and recalculate
        # Implementation depends on getting member list
        return []

    async def get_top_influencers(
        self,
        swarm_id: UUID,
        limit: int = 10,
    ) -> list[InfluenceResult]:
        """
        Get top influencers in a swarm.

        Args:
            swarm_id: The swarm
            limit: Number of top influencers

        Returns:
            List of top influencers
        """
        all_influences = await self.repository.get_all_influences(swarm_id)
        sorted_influences = sorted(all_influences, key=lambda x: x[1], reverse=True)

        results = []
        for i, (part_id, weight) in enumerate(sorted_influences[:limit]):
            result = await self.calculate_influence(part_id, swarm_id)
            results.append(result)

        return results

    def _diminishing_returns(self, value: int, saturation: int) -> float:
        """
        Apply diminishing returns curve.

        Uses 1 - e^(-value/saturation) for smooth saturation.
        """
        import math
        return 1 - math.exp(-value / saturation)

    async def _get_rank(
        self,
        swarm_id: UUID,
        part_id: UUID,
        influence: float,
    ) -> tuple[int, float]:
        """Get rank and percentile for a part's influence."""
        all_influences = await self.repository.get_all_influences(swarm_id)

        if not all_influences:
            return 1, 100.0

        sorted_influences = sorted(
            [(pid, weight) for pid, weight in all_influences],
            key=lambda x: x[1],
            reverse=True,
        )

        rank = 1
        for pid, weight in sorted_influences:
            if pid == part_id:
                break
            rank += 1

        percentile = (1 - (rank - 1) / len(sorted_influences)) * 100

        return rank, round(percentile, 1)


class InfluenceDecay:
    """
    Handles influence decay for inactive parts.
    """

    DECAY_RATE_PER_DAY = 0.01  # 1% decay per day of inactivity

    async def apply_decay(
        self,
        part_id: UUID,
        swarm_id: UUID,
        current_influence: float,
        last_activity: datetime,
    ) -> float:
        """
        Apply decay to influence based on inactivity.

        Args:
            part_id: The part
            swarm_id: The swarm
            current_influence: Current influence weight
            last_activity: Last activity timestamp

        Returns:
            Decayed influence weight
        """
        import math

        days_inactive = (datetime.utcnow() - last_activity).days

        if days_inactive <= 0:
            return current_influence

        # Exponential decay
        decay_factor = math.exp(-self.DECAY_RATE_PER_DAY * days_inactive)
        decayed_influence = current_influence * decay_factor

        # Minimum influence floor
        return max(decayed_influence, 0.01)
