"""
Swarm Lifecycle - Management of swarm creation, evolution, and dissolution.

Responsibilities:
- Create new swarms when needed
- Merge similar/overlapping swarms
- Split large swarms for better granularity
- Archive/dissolve inactive swarms
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from uuid import UUID

from ..models import Swarm, SwarmTier, SwarmHealthStatus


@dataclass
class SwarmMergeResult:
    """Result of a swarm merge operation."""
    primary_swarm: Swarm
    merged_swarm_ids: list[UUID]
    members_migrated: int
    learnings_consolidated: int
    success: bool
    message: str = ""


@dataclass
class SwarmSplitResult:
    """Result of a swarm split operation."""
    original_swarm: Swarm
    new_swarms: list[Swarm]
    members_redistributed: int
    success: bool
    message: str = ""


class SwarmLifecycleRepository(Protocol):
    """Protocol for swarm lifecycle operations."""

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def create_swarm(self, swarm: Swarm) -> Swarm:
        """Create a new swarm."""
        ...

    async def update_swarm(self, swarm: Swarm) -> Swarm:
        """Update swarm."""
        ...

    async def delete_swarm(self, swarm_id: UUID) -> bool:
        """Delete a swarm."""
        ...

    async def get_swarm_members_count(self, swarm_id: UUID) -> int:
        """Get member count for a swarm."""
        ...

    async def migrate_members(self, from_swarm_id: UUID, to_swarm_id: UUID) -> int:
        """Move all members from one swarm to another."""
        ...

    async def migrate_learnings(self, from_swarm_id: UUID, to_swarm_id: UUID) -> int:
        """Move all learnings from one swarm to another."""
        ...

    async def get_similar_swarms(
        self,
        swarm: Swarm,
        similarity_threshold: float,
    ) -> list[Swarm]:
        """Find swarms similar to the given one."""
        ...

    async def get_inactive_swarms(
        self,
        inactive_since: datetime,
    ) -> list[Swarm]:
        """Get swarms with no activity since the given time."""
        ...


class SwarmLifecycle:
    """
    Manages the lifecycle of swarms: creation, evolution, and dissolution.
    """

    # Thresholds for lifecycle operations
    MERGE_SIMILARITY_THRESHOLD = 0.85  # How similar swarms must be to merge
    SPLIT_MEMBER_THRESHOLD = 100000    # Split swarms larger than this
    INACTIVE_DAYS_THRESHOLD = 180      # Archive swarms inactive this long
    MIN_MEMBERS_FOR_VIABILITY = 10     # Minimum members for a viable swarm

    def __init__(self, repository: SwarmLifecycleRepository):
        self.repository = repository

    async def create_swarm(
        self,
        tier: SwarmTier,
        category: str,
        identifier: str,
        name: str,
        parent_swarm_id: Optional[UUID] = None,
    ) -> Swarm:
        """
        Create a new swarm.

        Args:
            tier: The swarm tier
            category: Category classification
            identifier: Unique identifier within category
            name: Human-readable name
            parent_swarm_id: Optional parent swarm for hierarchy

        Returns:
            The created swarm
        """
        swarm_id = f"{tier.name.lower()}:{category}:{identifier}"

        swarm = Swarm(
            swarm_id=swarm_id,
            tier=tier,
            category=category,
            identifier=identifier,
            name=name,
            parent_swarm_id=parent_swarm_id,
        )

        created_swarm = await self.repository.create_swarm(swarm)

        # Update parent if exists
        if parent_swarm_id:
            parent = await self.repository.get_swarm(parent_swarm_id)
            if parent:
                parent.child_swarm_ids.append(created_swarm.id)
                await self.repository.update_swarm(parent)

        return created_swarm

    async def merge_swarms(
        self,
        primary_swarm_id: UUID,
        secondary_swarm_ids: list[UUID],
    ) -> SwarmMergeResult:
        """
        Merge multiple swarms into one.

        The primary swarm absorbs all members and learnings from secondary swarms.
        Secondary swarms are then archived.

        Args:
            primary_swarm_id: The swarm to merge into
            secondary_swarm_ids: Swarms to be merged

        Returns:
            Result of the merge operation
        """
        primary = await self.repository.get_swarm(primary_swarm_id)
        if not primary:
            return SwarmMergeResult(
                primary_swarm=Swarm(),
                merged_swarm_ids=[],
                members_migrated=0,
                learnings_consolidated=0,
                success=False,
                message=f"Primary swarm {primary_swarm_id} not found",
            )

        total_members_migrated = 0
        total_learnings_consolidated = 0
        merged_ids = []

        for secondary_id in secondary_swarm_ids:
            secondary = await self.repository.get_swarm(secondary_id)
            if not secondary:
                continue

            # Migrate members
            members_migrated = await self.repository.migrate_members(
                secondary_id, primary_swarm_id
            )
            total_members_migrated += members_migrated

            # Migrate learnings
            learnings_migrated = await self.repository.migrate_learnings(
                secondary_id, primary_swarm_id
            )
            total_learnings_consolidated += learnings_migrated

            # Update primary swarm counts
            primary.member_count += secondary.member_count
            primary.active_member_count += secondary.active_member_count
            primary.elder_count += secondary.elder_count
            primary.mentor_count += secondary.mentor_count
            primary.learning_count += secondary.learning_count

            # Merge related swarms
            for related_id in secondary.related_swarm_ids:
                if related_id not in primary.related_swarm_ids:
                    primary.related_swarm_ids.append(related_id)

            # Archive secondary swarm
            secondary.health_status = SwarmHealthStatus.DORMANT
            secondary.updated_at = datetime.utcnow()
            await self.repository.update_swarm(secondary)

            merged_ids.append(secondary_id)

        # Update primary
        primary.updated_at = datetime.utcnow()
        await self.repository.update_swarm(primary)

        return SwarmMergeResult(
            primary_swarm=primary,
            merged_swarm_ids=merged_ids,
            members_migrated=total_members_migrated,
            learnings_consolidated=total_learnings_consolidated,
            success=True,
            message=f"Merged {len(merged_ids)} swarms into {primary.name}",
        )

    async def split_swarm(
        self,
        swarm_id: UUID,
        split_criteria: dict,
    ) -> SwarmSplitResult:
        """
        Split a large swarm into multiple smaller swarms.

        Args:
            swarm_id: The swarm to split
            split_criteria: Criteria for splitting (e.g., by material, size, context)

        Returns:
            Result of the split operation
        """
        original = await self.repository.get_swarm(swarm_id)
        if not original:
            return SwarmSplitResult(
                original_swarm=Swarm(),
                new_swarms=[],
                members_redistributed=0,
                success=False,
                message=f"Swarm {swarm_id} not found",
            )

        # Check if split is warranted
        member_count = await self.repository.get_swarm_members_count(swarm_id)
        if member_count < self.SPLIT_MEMBER_THRESHOLD:
            return SwarmSplitResult(
                original_swarm=original,
                new_swarms=[],
                members_redistributed=0,
                success=False,
                message=f"Swarm has {member_count} members, below split threshold",
            )

        # Create new sub-swarms based on criteria
        new_swarms = []
        split_key = split_criteria.get("key", "material")
        split_values = split_criteria.get("values", [])

        for value in split_values:
            new_swarm = await self.create_swarm(
                tier=SwarmTier(original.tier.value + 1) if original.tier.value < 5 else original.tier,
                category=original.category,
                identifier=f"{original.identifier}:{value}",
                name=f"{original.name} - {value}",
                parent_swarm_id=original.id,
            )
            new_swarms.append(new_swarm)

        # Note: Actual member redistribution would require more complex logic
        # based on part attributes matching split criteria

        original.child_swarm_ids.extend([s.id for s in new_swarms])
        original.updated_at = datetime.utcnow()
        await self.repository.update_swarm(original)

        return SwarmSplitResult(
            original_swarm=original,
            new_swarms=new_swarms,
            members_redistributed=0,  # Would be calculated by redistribution logic
            success=True,
            message=f"Split {original.name} into {len(new_swarms)} sub-swarms",
        )

    async def archive_inactive_swarms(
        self,
        inactive_days: int = INACTIVE_DAYS_THRESHOLD,
    ) -> list[UUID]:
        """
        Archive swarms that have been inactive for too long.

        Args:
            inactive_days: Days of inactivity before archiving

        Returns:
            List of archived swarm IDs
        """
        inactive_since = datetime.utcnow() - timedelta(days=inactive_days)
        inactive_swarms = await self.repository.get_inactive_swarms(inactive_since)

        archived_ids = []
        for swarm in inactive_swarms:
            # Don't archive swarms with minimum viable membership
            member_count = await self.repository.get_swarm_members_count(swarm.id)
            if member_count >= self.MIN_MEMBERS_FOR_VIABILITY:
                # Just mark as stagnant, don't archive
                swarm.health_status = SwarmHealthStatus.STAGNANT
            else:
                # Archive truly inactive small swarms
                swarm.health_status = SwarmHealthStatus.DORMANT

            swarm.updated_at = datetime.utcnow()
            await self.repository.update_swarm(swarm)
            archived_ids.append(swarm.id)

        return archived_ids

    async def find_merge_candidates(
        self,
        swarm_id: UUID,
    ) -> list[Swarm]:
        """
        Find swarms that could be merged with the given swarm.

        Args:
            swarm_id: The swarm to find merge candidates for

        Returns:
            List of candidate swarms
        """
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return []

        return await self.repository.get_similar_swarms(
            swarm,
            self.MERGE_SIMILARITY_THRESHOLD,
        )

    async def check_viability(self, swarm_id: UUID) -> tuple[bool, str]:
        """
        Check if a swarm is viable (should continue to exist).

        Args:
            swarm_id: The swarm to check

        Returns:
            Tuple of (is_viable, reason)
        """
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return False, "Swarm not found"

        member_count = await self.repository.get_swarm_members_count(swarm_id)

        # Check member count
        if member_count < self.MIN_MEMBERS_FOR_VIABILITY:
            return False, f"Only {member_count} members, below minimum of {self.MIN_MEMBERS_FOR_VIABILITY}"

        # Check health status
        if swarm.health_status == SwarmHealthStatus.DORMANT:
            return False, "Swarm is dormant"

        # Check activity
        if swarm.last_learning_at:
            days_since_learning = (datetime.utcnow() - swarm.last_learning_at).days
            if days_since_learning > self.INACTIVE_DAYS_THRESHOLD:
                return False, f"No learning activity for {days_since_learning} days"

        return True, "Swarm is viable"
