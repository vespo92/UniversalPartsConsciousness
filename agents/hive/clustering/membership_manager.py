"""
Membership Manager - Handles part-swarm membership operations.

Responsibilities:
- Track membership lifecycle (join, update, leave)
- Manage role transitions as parts evolve
- Track contribution metrics
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from uuid import UUID

from ..models import SwarmMembership, SwarmRole, Swarm


class MembershipRepository(Protocol):
    """Protocol for membership data access."""

    async def get_membership(self, part_id: UUID, swarm_id: UUID) -> Optional[SwarmMembership]:
        """Get membership by part and swarm."""
        ...

    async def get_part_memberships(self, part_id: UUID) -> list[SwarmMembership]:
        """Get all memberships for a part."""
        ...

    async def get_swarm_memberships(
        self,
        swarm_id: UUID,
        role: Optional[SwarmRole] = None,
        limit: int = 100,
    ) -> list[SwarmMembership]:
        """Get memberships for a swarm, optionally filtered by role."""
        ...

    async def update_membership(self, membership: SwarmMembership) -> SwarmMembership:
        """Update membership."""
        ...

    async def remove_membership(self, part_id: UUID, swarm_id: UUID) -> bool:
        """Remove a membership."""
        ...

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def update_swarm(self, swarm: Swarm) -> Swarm:
        """Update swarm."""
        ...


@dataclass
class MembershipStats:
    """Statistics for a part's swarm memberships."""
    total_memberships: int = 0
    active_contributions: int = 0
    learnings_received: int = 0
    learnings_propagated: int = 0
    highest_role: SwarmRole = SwarmRole.DORMANT
    average_influence: float = 0.0


class MembershipManager:
    """
    Manages part-swarm membership lifecycle and metrics.
    """

    # Role hierarchy for comparisons
    ROLE_HIERARCHY = {
        SwarmRole.DORMANT: 0,
        SwarmRole.LEARNER: 1,
        SwarmRole.CONTRIBUTOR: 2,
        SwarmRole.MENTOR: 3,
        SwarmRole.ELDER: 4,
    }

    def __init__(self, repository: MembershipRepository):
        self.repository = repository

    async def record_contribution(
        self,
        part_id: UUID,
        swarm_id: UUID,
        contribution_type: str = "learning",
    ) -> SwarmMembership:
        """
        Record a contribution from a part to a swarm.

        Args:
            part_id: The contributing part
            swarm_id: The swarm receiving contribution
            contribution_type: Type of contribution

        Returns:
            Updated membership
        """
        membership = await self.repository.get_membership(part_id, swarm_id)
        if not membership:
            raise ValueError(f"Part {part_id} is not a member of swarm {swarm_id}")

        membership.contribution_count += 1
        membership.last_contribution_at = datetime.utcnow()

        if contribution_type == "learning":
            membership.learnings_propagated += 1

        return await self.repository.update_membership(membership)

    async def record_learning_received(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> SwarmMembership:
        """
        Record that a part received a learning from a swarm.

        Args:
            part_id: The part receiving the learning
            swarm_id: The swarm providing the learning

        Returns:
            Updated membership
        """
        membership = await self.repository.get_membership(part_id, swarm_id)
        if not membership:
            raise ValueError(f"Part {part_id} is not a member of swarm {swarm_id}")

        membership.learnings_received += 1
        return await self.repository.update_membership(membership)

    async def update_role(
        self,
        part_id: UUID,
        swarm_id: UUID,
        new_role: SwarmRole,
    ) -> SwarmMembership:
        """
        Update a part's role within a swarm.

        This should be called when a part's consciousness level changes.

        Args:
            part_id: The part to update
            swarm_id: The swarm
            new_role: The new role

        Returns:
            Updated membership
        """
        membership = await self.repository.get_membership(part_id, swarm_id)
        if not membership:
            raise ValueError(f"Part {part_id} is not a member of swarm {swarm_id}")

        old_role = membership.role
        membership.role = new_role

        # Update swarm role counts
        swarm = await self.repository.get_swarm(swarm_id)
        if swarm:
            await self._update_swarm_role_counts(swarm, old_role, new_role)

        return await self.repository.update_membership(membership)

    async def update_influence(
        self,
        part_id: UUID,
        swarm_id: UUID,
        new_influence: float,
    ) -> SwarmMembership:
        """
        Update a part's influence weight within a swarm.

        Args:
            part_id: The part to update
            swarm_id: The swarm
            new_influence: New influence weight (0-1)

        Returns:
            Updated membership
        """
        membership = await self.repository.get_membership(part_id, swarm_id)
        if not membership:
            raise ValueError(f"Part {part_id} is not a member of swarm {swarm_id}")

        membership.influence_weight = max(0.0, min(1.0, new_influence))
        return await self.repository.update_membership(membership)

    async def get_part_stats(self, part_id: UUID) -> MembershipStats:
        """
        Get aggregated membership statistics for a part.

        Args:
            part_id: The part to analyze

        Returns:
            Membership statistics
        """
        memberships = await self.repository.get_part_memberships(part_id)

        if not memberships:
            return MembershipStats()

        total_influence = sum(m.influence_weight for m in memberships)
        highest_role = max(memberships, key=lambda m: self.ROLE_HIERARCHY[m.role]).role

        return MembershipStats(
            total_memberships=len(memberships),
            active_contributions=sum(m.contribution_count for m in memberships),
            learnings_received=sum(m.learnings_received for m in memberships),
            learnings_propagated=sum(m.learnings_propagated for m in memberships),
            highest_role=highest_role,
            average_influence=total_influence / len(memberships) if memberships else 0.0,
        )

    async def get_swarm_elders(
        self,
        swarm_id: UUID,
        limit: int = 10,
    ) -> list[SwarmMembership]:
        """
        Get the elder members of a swarm (highest consciousness).

        Args:
            swarm_id: The swarm
            limit: Maximum number of elders to return

        Returns:
            List of elder memberships
        """
        return await self.repository.get_swarm_memberships(
            swarm_id,
            role=SwarmRole.ELDER,
            limit=limit,
        )

    async def get_swarm_mentors(
        self,
        swarm_id: UUID,
        limit: int = 20,
    ) -> list[SwarmMembership]:
        """
        Get the mentor members of a swarm.

        Args:
            swarm_id: The swarm
            limit: Maximum number to return

        Returns:
            List of mentor memberships
        """
        return await self.repository.get_swarm_memberships(
            swarm_id,
            role=SwarmRole.MENTOR,
            limit=limit,
        )

    async def get_active_members(
        self,
        swarm_id: UUID,
        since: Optional[datetime] = None,
        limit: int = 100,
    ) -> list[SwarmMembership]:
        """
        Get active members of a swarm (recent contributions).

        Args:
            swarm_id: The swarm
            since: Only include members active since this time
            limit: Maximum number to return

        Returns:
            List of active memberships
        """
        if since is None:
            since = datetime.utcnow() - timedelta(days=30)

        memberships = await self.repository.get_swarm_memberships(
            swarm_id,
            limit=limit * 2,  # Get more to filter
        )

        active = [
            m for m in memberships
            if m.last_contribution_at and m.last_contribution_at >= since
        ]

        return active[:limit]

    async def remove_from_swarm(
        self,
        part_id: UUID,
        swarm_id: UUID,
    ) -> bool:
        """
        Remove a part from a swarm.

        Args:
            part_id: The part to remove
            swarm_id: The swarm

        Returns:
            True if removed, False if not found
        """
        membership = await self.repository.get_membership(part_id, swarm_id)
        if not membership:
            return False

        # Update swarm counts
        swarm = await self.repository.get_swarm(swarm_id)
        if swarm:
            swarm.member_count = max(0, swarm.member_count - 1)
            if membership.role == SwarmRole.ELDER:
                swarm.elder_count = max(0, swarm.elder_count - 1)
            elif membership.role == SwarmRole.MENTOR:
                swarm.mentor_count = max(0, swarm.mentor_count - 1)
            if membership.last_contribution_at:
                swarm.active_member_count = max(0, swarm.active_member_count - 1)
            await self.repository.update_swarm(swarm)

        return await self.repository.remove_membership(part_id, swarm_id)

    async def _update_swarm_role_counts(
        self,
        swarm: Swarm,
        old_role: SwarmRole,
        new_role: SwarmRole,
    ) -> None:
        """Update swarm role counts when a member changes role."""
        # Decrement old role count
        if old_role == SwarmRole.ELDER:
            swarm.elder_count = max(0, swarm.elder_count - 1)
        elif old_role == SwarmRole.MENTOR:
            swarm.mentor_count = max(0, swarm.mentor_count - 1)

        # Increment new role count
        if new_role == SwarmRole.ELDER:
            swarm.elder_count += 1
        elif new_role == SwarmRole.MENTOR:
            swarm.mentor_count += 1

        await self.repository.update_swarm(swarm)
