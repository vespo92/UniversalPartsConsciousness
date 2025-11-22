"""
Emergency Learning - Fast-track critical information across swarms.

Handles urgent propagation of safety-critical learnings.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import Learning, LearningType, RecallNotice, RecallSeverity


@dataclass
class EmergencyPropagationResult:
    """Result of emergency learning propagation."""
    learning: Learning
    swarms_reached: int
    parts_reached: int
    propagation_time_ms: float
    priority_level: int


class EmergencyRepository(Protocol):
    """Protocol for emergency operations."""

    async def get_all_related_swarms(
        self,
        swarm_ids: list[UUID],
    ) -> list[UUID]:
        """Get all swarms related to the given ones."""
        ...

    async def broadcast_emergency(
        self,
        swarm_id: UUID,
        learning: Learning,
    ) -> int:
        """Broadcast emergency learning to swarm, return count of parts reached."""
        ...

    async def mark_learning_as_emergency(
        self,
        learning: Learning,
    ) -> None:
        """Mark a learning as emergency priority."""
        ...


class EmergencyLearning:
    """
    Fast-tracks critical safety information across swarms.
    """

    # Priority levels
    PRIORITY_CRITICAL = 1
    PRIORITY_HIGH = 2
    PRIORITY_NORMAL = 3

    # Concurrent broadcast limit
    MAX_CONCURRENT_BROADCASTS = 20

    def __init__(self, repository: EmergencyRepository):
        self.repository = repository

    async def fast_track_learning(
        self,
        learning: Learning,
        affected_swarm_ids: list[UUID],
        priority: int = PRIORITY_CRITICAL,
    ) -> EmergencyPropagationResult:
        """
        Fast-track a learning to all affected swarms.

        Emergency learnings bypass normal propagation queues and
        are delivered immediately with maximum priority.

        Args:
            learning: The learning to fast-track
            affected_swarm_ids: Primary affected swarms
            priority: Priority level (1 = highest)

        Returns:
            Result of the propagation
        """
        start_time = datetime.utcnow()

        # Mark as emergency
        await self.repository.mark_learning_as_emergency(learning)

        # Get all related swarms (cascade effect)
        all_swarms = await self.repository.get_all_related_swarms(affected_swarm_ids)
        all_swarms = list(set(affected_swarm_ids + all_swarms))

        total_parts_reached = 0
        swarms_reached = 0

        # Broadcast to all swarms in parallel batches
        for i in range(0, len(all_swarms), self.MAX_CONCURRENT_BROADCASTS):
            batch = all_swarms[i:i + self.MAX_CONCURRENT_BROADCASTS]
            tasks = [
                self.repository.broadcast_emergency(swarm_id, learning)
                for swarm_id in batch
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, int):
                    total_parts_reached += result
                    swarms_reached += 1

        end_time = datetime.utcnow()
        propagation_time_ms = (end_time - start_time).total_seconds() * 1000

        return EmergencyPropagationResult(
            learning=learning,
            swarms_reached=swarms_reached,
            parts_reached=total_parts_reached,
            propagation_time_ms=propagation_time_ms,
            priority_level=priority,
        )

    async def create_from_recall(
        self,
        recall: RecallNotice,
    ) -> Learning:
        """
        Create an emergency learning from a recall notice.

        Args:
            recall: The recall to convert

        Returns:
            Emergency learning
        """
        severity_priority = {
            RecallSeverity.CRITICAL: self.PRIORITY_CRITICAL,
            RecallSeverity.HIGH: self.PRIORITY_HIGH,
            RecallSeverity.WARNING: self.PRIORITY_NORMAL,
            RecallSeverity.ADVISORY: self.PRIORITY_NORMAL,
        }

        learning = Learning(
            learning_type=LearningType.FAILURE_MODE,
            content={
                "failure_type": "recall_defect",
                "recall_id": str(recall.id),
                "source": recall.source,
                "source_recall_id": recall.source_recall_id,
                "title": recall.title,
                "defect_description": recall.defect_description,
                "recommended_action": recall.recommended_action,
                "severity": recall.severity.value,
                "emergency": True,
                "priority": severity_priority.get(recall.severity, self.PRIORITY_NORMAL),
            },
            confidence=1.0,
            applicability="exact_match",
            novelty_score=1.0,
            propagation_strength=1.0,
        )

        return learning

    async def broadcast_safety_alert(
        self,
        alert_type: str,
        description: str,
        affected_swarm_ids: list[UUID],
        severity: str = "high",
    ) -> EmergencyPropagationResult:
        """
        Broadcast a general safety alert.

        Args:
            alert_type: Type of alert (e.g., "material_defect", "design_flaw")
            description: Alert description
            affected_swarm_ids: Affected swarms
            severity: Alert severity

        Returns:
            Propagation result
        """
        learning = Learning(
            learning_type=LearningType.FAILURE_MODE,
            content={
                "alert_type": alert_type,
                "description": description,
                "severity": severity,
                "emergency": True,
                "issued_at": datetime.utcnow().isoformat(),
            },
            confidence=0.9,
            applicability="similar_specs",
            novelty_score=1.0,
        )

        priority = self.PRIORITY_CRITICAL if severity == "critical" else self.PRIORITY_HIGH

        return await self.fast_track_learning(
            learning,
            affected_swarm_ids,
            priority,
        )


class EmergencyQueue:
    """
    Priority queue for emergency learnings.
    """

    def __init__(self):
        self.queue: list[tuple[int, datetime, Learning, list[UUID]]] = []

    def add(
        self,
        learning: Learning,
        affected_swarms: list[UUID],
        priority: int = EmergencyLearning.PRIORITY_NORMAL,
    ) -> None:
        """Add an emergency to the queue."""
        self.queue.append((priority, datetime.utcnow(), learning, affected_swarms))
        # Sort by priority (lower = higher priority), then by time
        self.queue.sort(key=lambda x: (x[0], x[1]))

    def pop(self) -> Optional[tuple[Learning, list[UUID]]]:
        """Pop the highest priority emergency."""
        if not self.queue:
            return None
        _, _, learning, swarms = self.queue.pop(0)
        return learning, swarms

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.queue) == 0

    def size(self) -> int:
        """Get queue size."""
        return len(self.queue)
