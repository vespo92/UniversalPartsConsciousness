"""
Broadcast Engine - Handles broadcast messaging to multiple swarms.

Efficient delivery of messages to large numbers of swarms.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import SwarmMessage, Swarm


@dataclass
class BroadcastResult:
    """Result of a broadcast operation."""
    message_id: UUID
    total_targets: int
    successful_deliveries: int
    failed_deliveries: int
    total_time_ms: float
    errors: list[str]


@dataclass
class BroadcastFilter:
    """Filter for broadcast targeting."""
    categories: Optional[list[str]] = None
    tiers: Optional[list[int]] = None
    min_members: Optional[int] = None
    max_members: Optional[int] = None
    health_status: Optional[list[str]] = None
    exclude_swarm_ids: Optional[list[UUID]] = None


class BroadcastRepository(Protocol):
    """Protocol for broadcast operations."""

    async def get_swarms_by_filter(
        self,
        filter: BroadcastFilter,
    ) -> list[Swarm]:
        """Get swarms matching the filter."""
        ...

    async def deliver_message(
        self,
        swarm_id: UUID,
        message: SwarmMessage,
    ) -> bool:
        """Deliver message to a swarm."""
        ...


class BroadcastEngine:
    """
    Handles efficient broadcast messaging to multiple swarms.
    """

    # Concurrent delivery limit
    MAX_CONCURRENT_DELIVERIES = 50

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY_MS = 100

    def __init__(self, repository: BroadcastRepository):
        self.repository = repository

    async def broadcast(
        self,
        message: SwarmMessage,
        filter: Optional[BroadcastFilter] = None,
        target_swarm_ids: Optional[list[UUID]] = None,
    ) -> BroadcastResult:
        """
        Broadcast a message to multiple swarms.

        Args:
            message: The message to broadcast
            filter: Optional filter for target selection
            target_swarm_ids: Explicit target list (overrides filter)

        Returns:
            Broadcast result
        """
        start_time = datetime.utcnow()
        errors: list[str] = []

        # Determine targets
        if target_swarm_ids:
            targets = target_swarm_ids
        elif filter:
            swarms = await self.repository.get_swarms_by_filter(filter)
            targets = [s.id for s in swarms]
        else:
            errors.append("No targets specified")
            return BroadcastResult(
                message_id=message.id,
                total_targets=0,
                successful_deliveries=0,
                failed_deliveries=0,
                total_time_ms=0,
                errors=errors,
            )

        # Exclude any specified swarms
        if filter and filter.exclude_swarm_ids:
            targets = [t for t in targets if t not in filter.exclude_swarm_ids]

        # Deliver in parallel batches
        successful = 0
        failed = 0

        for i in range(0, len(targets), self.MAX_CONCURRENT_DELIVERIES):
            batch = targets[i:i + self.MAX_CONCURRENT_DELIVERIES]
            tasks = [self._deliver_with_retry(swarm_id, message) for swarm_id in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for j, result in enumerate(results):
                if isinstance(result, Exception):
                    failed += 1
                    errors.append(f"Swarm {batch[j]}: {str(result)}")
                elif result:
                    successful += 1
                else:
                    failed += 1

        end_time = datetime.utcnow()
        total_time = (end_time - start_time).total_seconds() * 1000

        return BroadcastResult(
            message_id=message.id,
            total_targets=len(targets),
            successful_deliveries=successful,
            failed_deliveries=failed,
            total_time_ms=total_time,
            errors=errors[:10],  # Limit error list size
        )

    async def _deliver_with_retry(
        self,
        swarm_id: UUID,
        message: SwarmMessage,
    ) -> bool:
        """Deliver message with retry logic."""
        for attempt in range(self.MAX_RETRIES):
            try:
                result = await self.repository.deliver_message(swarm_id, message)
                if result:
                    return True
            except Exception:
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY_MS / 1000)
                continue

        return False

    async def broadcast_to_category(
        self,
        message: SwarmMessage,
        category: str,
        min_tier: int = 1,
        max_tier: int = 5,
    ) -> BroadcastResult:
        """
        Broadcast to all swarms in a category.

        Args:
            message: The message
            category: Target category
            min_tier: Minimum swarm tier
            max_tier: Maximum swarm tier

        Returns:
            Broadcast result
        """
        filter = BroadcastFilter(
            categories=[category],
            tiers=list(range(min_tier, max_tier + 1)),
        )

        return await self.broadcast(message, filter=filter)

    async def broadcast_to_related(
        self,
        message: SwarmMessage,
        source_swarm: Swarm,
        relationship_types: Optional[list[str]] = None,
    ) -> BroadcastResult:
        """
        Broadcast to all swarms related to the source.

        Args:
            message: The message
            source_swarm: Source swarm
            relationship_types: Optional filter by relationship type

        Returns:
            Broadcast result
        """
        # Would use RelationshipMapper to find related swarms
        # For now, exclude the source swarm
        filter = BroadcastFilter(
            exclude_swarm_ids=[source_swarm.id],
        )

        return await self.broadcast(message, filter=filter)

    async def emergency_broadcast(
        self,
        message: SwarmMessage,
    ) -> BroadcastResult:
        """
        Emergency broadcast to all swarms.

        Used for critical safety alerts. Bypasses normal filtering.

        Args:
            message: Emergency message

        Returns:
            Broadcast result
        """
        # Set highest priority
        message.priority = 1

        # Get all active swarms
        filter = BroadcastFilter(
            health_status=["thriving", "healthy", "declining"],  # Exclude dormant
        )

        return await self.broadcast(message, filter=filter)


class ScheduledBroadcast:
    """
    Scheduled broadcast management.
    """

    def __init__(self, engine: BroadcastEngine):
        self.engine = engine
        self.scheduled: list[tuple[datetime, SwarmMessage, BroadcastFilter]] = []

    def schedule(
        self,
        message: SwarmMessage,
        filter: BroadcastFilter,
        scheduled_time: datetime,
    ) -> None:
        """Schedule a broadcast for later."""
        self.scheduled.append((scheduled_time, message, filter))
        self.scheduled.sort(key=lambda x: x[0])

    async def process_due(self) -> list[BroadcastResult]:
        """Process all due broadcasts."""
        now = datetime.utcnow()
        results = []

        while self.scheduled and self.scheduled[0][0] <= now:
            scheduled_time, message, filter = self.scheduled.pop(0)
            result = await self.engine.broadcast(message, filter)
            results.append(result)

        return results

    def get_pending_count(self) -> int:
        """Get count of pending broadcasts."""
        return len(self.scheduled)
