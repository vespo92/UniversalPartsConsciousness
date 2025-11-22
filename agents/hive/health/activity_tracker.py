"""
Activity Tracker - Tracks swarm activity levels over time.

Monitors contributions, learnings, and interactions within swarms.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Optional, Protocol
from uuid import UUID


@dataclass
class ActivityEvent:
    """A recorded activity event."""
    event_id: UUID
    swarm_id: UUID
    event_type: str  # "contribution", "learning", "communication", "membership"
    part_id: Optional[UUID]
    details: dict[str, Any]
    timestamp: datetime


@dataclass
class ActivitySummary:
    """Summary of activity for a time period."""
    swarm_id: UUID
    period_start: datetime
    period_end: datetime
    total_events: int
    events_by_type: dict[str, int]
    unique_participants: int
    peak_hour: int
    trend: str  # "increasing", "stable", "decreasing"


@dataclass
class ActivityTimeSeries:
    """Time series of activity data."""
    swarm_id: UUID
    timestamps: list[datetime]
    counts: list[int]
    interval: str  # "hour", "day", "week"


class ActivityRepository(Protocol):
    """Protocol for activity data operations."""

    async def record_event(self, event: ActivityEvent) -> None:
        """Record an activity event."""
        ...

    async def get_events(
        self,
        swarm_id: UUID,
        since: datetime,
        event_type: Optional[str] = None,
    ) -> list[ActivityEvent]:
        """Get events for a swarm."""
        ...

    async def get_unique_participants(
        self,
        swarm_id: UUID,
        since: datetime,
    ) -> int:
        """Get count of unique participants."""
        ...

    async def get_hourly_counts(
        self,
        swarm_id: UUID,
        since: datetime,
    ) -> dict[int, int]:
        """Get event counts by hour."""
        ...


class ActivityTracker:
    """
    Tracks and analyzes swarm activity patterns.
    """

    def __init__(self, repository: ActivityRepository):
        self.repository = repository

    async def record_activity(
        self,
        swarm_id: UUID,
        event_type: str,
        part_id: Optional[UUID] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> ActivityEvent:
        """
        Record an activity event.

        Args:
            swarm_id: The swarm where activity occurred
            event_type: Type of activity
            part_id: Part involved (if any)
            details: Additional details

        Returns:
            Recorded event
        """
        from uuid import uuid4

        event = ActivityEvent(
            event_id=uuid4(),
            swarm_id=swarm_id,
            event_type=event_type,
            part_id=part_id,
            details=details or {},
            timestamp=datetime.utcnow(),
        )

        await self.repository.record_event(event)
        return event

    async def get_activity_summary(
        self,
        swarm_id: UUID,
        period_days: int = 7,
    ) -> ActivitySummary:
        """
        Get activity summary for a time period.

        Args:
            swarm_id: The swarm to analyze
            period_days: Number of days to look back

        Returns:
            Activity summary
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=period_days)

        events = await self.repository.get_events(swarm_id, start_time)

        # Count by type
        events_by_type: dict[str, int] = {}
        for event in events:
            events_by_type[event.event_type] = events_by_type.get(event.event_type, 0) + 1

        # Get unique participants
        unique_participants = await self.repository.get_unique_participants(swarm_id, start_time)

        # Find peak hour
        hourly_counts = await self.repository.get_hourly_counts(swarm_id, start_time)
        peak_hour = max(hourly_counts.items(), key=lambda x: x[1])[0] if hourly_counts else 0

        # Determine trend
        trend = await self._calculate_trend(swarm_id, period_days)

        return ActivitySummary(
            swarm_id=swarm_id,
            period_start=start_time,
            period_end=end_time,
            total_events=len(events),
            events_by_type=events_by_type,
            unique_participants=unique_participants,
            peak_hour=peak_hour,
            trend=trend,
        )

    async def get_time_series(
        self,
        swarm_id: UUID,
        period_days: int = 30,
        interval: str = "day",
    ) -> ActivityTimeSeries:
        """
        Get activity time series data.

        Args:
            swarm_id: The swarm to analyze
            period_days: Number of days
            interval: Aggregation interval (hour, day, week)

        Returns:
            Time series data
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=period_days)

        events = await self.repository.get_events(swarm_id, start_time)

        # Aggregate by interval
        timestamps: list[datetime] = []
        counts: list[int] = []

        if interval == "hour":
            delta = timedelta(hours=1)
        elif interval == "day":
            delta = timedelta(days=1)
        elif interval == "week":
            delta = timedelta(weeks=1)
        else:
            delta = timedelta(days=1)

        current = start_time
        while current <= end_time:
            next_time = current + delta
            period_count = sum(
                1 for e in events
                if current <= e.timestamp < next_time
            )
            timestamps.append(current)
            counts.append(period_count)
            current = next_time

        return ActivityTimeSeries(
            swarm_id=swarm_id,
            timestamps=timestamps,
            counts=counts,
            interval=interval,
        )

    async def _calculate_trend(
        self,
        swarm_id: UUID,
        period_days: int,
    ) -> str:
        """Calculate activity trend."""
        now = datetime.utcnow()
        half_period = timedelta(days=period_days // 2)

        # Compare first half to second half
        recent_start = now - half_period
        older_start = now - timedelta(days=period_days)

        recent_events = await self.repository.get_events(swarm_id, recent_start)
        older_events = await self.repository.get_events(swarm_id, older_start)
        older_events = [e for e in older_events if e.timestamp < recent_start]

        recent_count = len(recent_events)
        older_count = len(older_events)

        if older_count == 0:
            return "new" if recent_count > 0 else "dormant"

        change_rate = (recent_count - older_count) / older_count

        if change_rate > 0.1:
            return "increasing"
        elif change_rate < -0.1:
            return "decreasing"
        else:
            return "stable"

    async def record_contribution(
        self,
        swarm_id: UUID,
        part_id: UUID,
        contribution_type: str,
        value: Any = None,
    ) -> ActivityEvent:
        """Record a contribution event."""
        return await self.record_activity(
            swarm_id,
            "contribution",
            part_id,
            {"type": contribution_type, "value": value},
        )

    async def record_learning(
        self,
        swarm_id: UUID,
        learning_id: UUID,
        learning_type: str,
    ) -> ActivityEvent:
        """Record a learning event."""
        return await self.record_activity(
            swarm_id,
            "learning",
            None,
            {"learning_id": str(learning_id), "type": learning_type},
        )

    async def record_communication(
        self,
        source_swarm_id: UUID,
        target_swarm_id: UUID,
        message_type: str,
    ) -> ActivityEvent:
        """Record an inter-swarm communication event."""
        return await self.record_activity(
            source_swarm_id,
            "communication",
            None,
            {"target_swarm_id": str(target_swarm_id), "message_type": message_type},
        )

    async def record_membership_change(
        self,
        swarm_id: UUID,
        part_id: UUID,
        change_type: str,  # "joined", "left", "promoted", "demoted"
        new_role: Optional[str] = None,
    ) -> ActivityEvent:
        """Record a membership change event."""
        return await self.record_activity(
            swarm_id,
            "membership",
            part_id,
            {"change_type": change_type, "new_role": new_role},
        )
