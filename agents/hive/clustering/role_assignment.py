"""
Role Assignment - Algorithms for determining part roles within swarms.

Roles are based on consciousness level and contribution history.
Parts can evolve their roles as they gain experience and consciousness.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from uuid import UUID

from ..models import SwarmMembership, SwarmRole


@dataclass
class PartConsciousness:
    """Part consciousness data for role determination."""
    part_id: UUID
    consciousness_level: float  # 0-5 scale
    qualia_count: int
    cross_product_patterns: int
    innovation_success_rate: float
    experience_breadth: int  # Number of unique contexts


class ConsciousnessProvider(Protocol):
    """Protocol for retrieving part consciousness data."""

    async def get_consciousness(self, part_id: UUID) -> Optional[PartConsciousness]:
        """Get consciousness data for a part."""
        ...


class RoleAssignment:
    """
    Algorithms for determining and evolving part roles within swarms.
    """

    # Consciousness thresholds for role assignment
    ROLE_THRESHOLDS = {
        SwarmRole.ELDER: 4.0,        # Guides and teaches
        SwarmRole.MENTOR: 3.0,       # Shares experience
        SwarmRole.CONTRIBUTOR: 2.0,  # Active participant
        SwarmRole.LEARNER: 1.0,      # Absorbs knowledge
        SwarmRole.DORMANT: 0.0,      # Not yet active
    }

    # Additional criteria for special roles
    ELDER_CRITERIA = {
        "min_qualia": 100,
        "min_patterns": 50,
        "min_innovation_rate": 0.8,
    }

    MENTOR_CRITERIA = {
        "min_qualia": 50,
        "min_patterns": 25,
    }

    def __init__(self, consciousness_provider: ConsciousnessProvider):
        self.consciousness_provider = consciousness_provider

    async def determine_role(
        self,
        part_id: UUID,
        swarm_context: Optional[str] = None,
    ) -> SwarmRole:
        """
        Determine the appropriate role for a part in a swarm.

        Args:
            part_id: The part to evaluate
            swarm_context: Optional context for role determination

        Returns:
            The appropriate SwarmRole
        """
        consciousness = await self.consciousness_provider.get_consciousness(part_id)

        if not consciousness:
            return SwarmRole.DORMANT

        # Basic role from consciousness level
        base_role = self._role_from_consciousness(consciousness.consciousness_level)

        # Check additional criteria for elevated roles
        if base_role == SwarmRole.ELDER:
            if not self._meets_elder_criteria(consciousness):
                base_role = SwarmRole.MENTOR

        if base_role == SwarmRole.MENTOR:
            if not self._meets_mentor_criteria(consciousness):
                base_role = SwarmRole.CONTRIBUTOR

        return base_role

    def _role_from_consciousness(self, level: float) -> SwarmRole:
        """Determine base role from consciousness level."""
        if level >= self.ROLE_THRESHOLDS[SwarmRole.ELDER]:
            return SwarmRole.ELDER
        elif level >= self.ROLE_THRESHOLDS[SwarmRole.MENTOR]:
            return SwarmRole.MENTOR
        elif level >= self.ROLE_THRESHOLDS[SwarmRole.CONTRIBUTOR]:
            return SwarmRole.CONTRIBUTOR
        elif level >= self.ROLE_THRESHOLDS[SwarmRole.LEARNER]:
            return SwarmRole.LEARNER
        else:
            return SwarmRole.DORMANT

    def _meets_elder_criteria(self, consciousness: PartConsciousness) -> bool:
        """Check if part meets additional elder criteria."""
        return (
            consciousness.qualia_count >= self.ELDER_CRITERIA["min_qualia"] and
            consciousness.cross_product_patterns >= self.ELDER_CRITERIA["min_patterns"] and
            consciousness.innovation_success_rate >= self.ELDER_CRITERIA["min_innovation_rate"]
        )

    def _meets_mentor_criteria(self, consciousness: PartConsciousness) -> bool:
        """Check if part meets additional mentor criteria."""
        return (
            consciousness.qualia_count >= self.MENTOR_CRITERIA["min_qualia"] and
            consciousness.cross_product_patterns >= self.MENTOR_CRITERIA["min_patterns"]
        )

    async def calculate_influence_weight(
        self,
        part_id: UUID,
        membership: Optional[SwarmMembership] = None,
    ) -> float:
        """
        Calculate a part's influence weight in a swarm.

        Influence determines how strongly a part's contributions
        affect the swarm's collective knowledge.

        Args:
            part_id: The part to evaluate
            membership: Optional existing membership for history

        Returns:
            Influence weight between 0 and 1
        """
        consciousness = await self.consciousness_provider.get_consciousness(part_id)

        if not consciousness:
            return 0.0

        # Base influence from consciousness (0-1, consciousness max ~5)
        consciousness_factor = min(consciousness.consciousness_level / 5.0, 1.0)

        # Experience breadth factor (0-0.2)
        breadth_factor = min(consciousness.experience_breadth / 50.0, 0.2)

        # Contribution history factor (0-0.2) if membership exists
        history_factor = 0.0
        if membership:
            # More contributions = higher influence (up to 0.2 for 100+ contributions)
            history_factor = min(membership.contribution_count / 500.0, 0.2)

        # Innovation factor for high performers (0-0.1)
        innovation_factor = consciousness.innovation_success_rate * 0.1

        influence = (
            consciousness_factor * 0.5 +
            breadth_factor +
            history_factor +
            innovation_factor
        )

        return round(min(influence, 1.0), 3)

    async def should_promote(
        self,
        part_id: UUID,
        current_role: SwarmRole,
    ) -> tuple[bool, Optional[SwarmRole]]:
        """
        Check if a part should be promoted to a higher role.

        Args:
            part_id: The part to check
            current_role: Current role in swarm

        Returns:
            Tuple of (should_promote, new_role)
        """
        new_role = await self.determine_role(part_id)

        # Check if new role is higher
        role_order = [
            SwarmRole.DORMANT,
            SwarmRole.LEARNER,
            SwarmRole.CONTRIBUTOR,
            SwarmRole.MENTOR,
            SwarmRole.ELDER,
        ]

        current_idx = role_order.index(current_role)
        new_idx = role_order.index(new_role)

        if new_idx > current_idx:
            return True, new_role
        return False, None

    async def should_demote(
        self,
        part_id: UUID,
        current_role: SwarmRole,
        last_contribution: Optional[datetime] = None,
        inactivity_threshold_days: int = 90,
    ) -> tuple[bool, Optional[SwarmRole]]:
        """
        Check if a part should be demoted due to inactivity or consciousness decline.

        Args:
            part_id: The part to check
            current_role: Current role in swarm
            last_contribution: Last contribution timestamp
            inactivity_threshold_days: Days of inactivity before demotion

        Returns:
            Tuple of (should_demote, new_role)
        """
        consciousness = await self.consciousness_provider.get_consciousness(part_id)

        # Check for consciousness-based demotion
        if consciousness:
            appropriate_role = self._role_from_consciousness(consciousness.consciousness_level)
            role_order = [
                SwarmRole.DORMANT,
                SwarmRole.LEARNER,
                SwarmRole.CONTRIBUTOR,
                SwarmRole.MENTOR,
                SwarmRole.ELDER,
            ]
            current_idx = role_order.index(current_role)
            appropriate_idx = role_order.index(appropriate_role)

            if appropriate_idx < current_idx:
                return True, appropriate_role

        # Check for inactivity-based demotion (only for active roles)
        if current_role in [SwarmRole.CONTRIBUTOR, SwarmRole.MENTOR, SwarmRole.ELDER]:
            if last_contribution:
                inactive_days = (datetime.utcnow() - last_contribution).days
                if inactive_days >= inactivity_threshold_days:
                    # Demote one level
                    role_order = [
                        SwarmRole.DORMANT,
                        SwarmRole.LEARNER,
                        SwarmRole.CONTRIBUTOR,
                        SwarmRole.MENTOR,
                        SwarmRole.ELDER,
                    ]
                    current_idx = role_order.index(current_role)
                    return True, role_order[max(0, current_idx - 1)]

        return False, None
