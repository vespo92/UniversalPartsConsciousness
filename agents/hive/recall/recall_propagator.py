"""
Recall Propagator - Propagates recall awareness to affected parts.

Ensures critical safety information reaches all affected swarms and parts.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import RecallNotice, RecallSeverity, Learning, LearningType


@dataclass
class RecallPropagationResult:
    """Result of a recall propagation operation."""
    recall: RecallNotice
    swarms_notified: int
    parts_notified: int
    propagation_time_ms: float
    success: bool
    errors: list[str]


@dataclass
class PartRecallQualia:
    """Qualia generated from recall awareness."""
    part_id: UUID
    recall_id: UUID
    emotion: str  # "concern", "alarm"
    awareness_level: float
    recommended_action: str


class RecallRepository(Protocol):
    """Protocol for recall data operations."""

    async def save_recall(self, recall: RecallNotice) -> RecallNotice:
        """Save a recall notice."""
        ...

    async def update_recall_status(
        self,
        recall_id: UUID,
        status: str,
        parts_notified: int,
    ) -> None:
        """Update recall propagation status."""
        ...

    async def get_swarm(self, swarm_id: UUID) -> Any:
        """Get swarm by ID."""
        ...

    async def get_swarm_members(
        self,
        swarm_id: UUID,
        limit: int = 10000,
    ) -> list[Any]:
        """Get members of a swarm."""
        ...

    async def notify_part_of_recall(
        self,
        part_id: UUID,
        recall: RecallNotice,
    ) -> None:
        """Notify a part about a recall."""
        ...

    async def emit_qualia(
        self,
        part_id: UUID,
        qualia: dict[str, Any],
    ) -> None:
        """Emit qualia for a part."""
        ...


class RecallPropagator:
    """
    Propagates recall notices to affected swarms and parts.
    """

    # Batch sizes for notification
    SWARM_BATCH_SIZE = 10
    PART_BATCH_SIZE = 100

    def __init__(self, repository: RecallRepository):
        self.repository = repository

    async def propagate_recall(
        self,
        recall: RecallNotice,
    ) -> RecallPropagationResult:
        """
        Propagate a recall to all affected swarms and parts.

        Args:
            recall: The recall notice to propagate

        Returns:
            Result of the propagation
        """
        start_time = datetime.utcnow()
        errors = []
        swarms_notified = 0
        parts_notified = 0

        # Save the recall first
        recall = await self.repository.save_recall(recall)

        # Update swarm-level knowledge for affected swarms
        for swarm_id in recall.affected_swarm_ids:
            try:
                await self._update_swarm_recall_status(swarm_id, recall)
                swarms_notified += 1
            except Exception as e:
                errors.append(f"Error updating swarm {swarm_id}: {e}")

        # Notify individual affected parts
        all_parts_notified = 0
        for swarm_id in recall.affected_swarm_ids:
            try:
                count = await self._notify_swarm_members(swarm_id, recall)
                all_parts_notified += count
            except Exception as e:
                errors.append(f"Error notifying swarm {swarm_id} members: {e}")

        parts_notified = all_parts_notified

        # Trigger emergency learning for critical recalls
        if recall.severity == RecallSeverity.CRITICAL:
            try:
                await self._trigger_emergency_learning(recall)
            except Exception as e:
                errors.append(f"Error triggering emergency learning: {e}")

        # Update recall status
        end_time = datetime.utcnow()
        propagation_time_ms = (end_time - start_time).total_seconds() * 1000

        await self.repository.update_recall_status(
            recall.id,
            "completed" if not errors else "partial",
            parts_notified,
        )

        recall.propagation_status = "completed" if not errors else "partial"
        recall.propagation_complete_at = end_time
        recall.affected_parts_count = parts_notified

        return RecallPropagationResult(
            recall=recall,
            swarms_notified=swarms_notified,
            parts_notified=parts_notified,
            propagation_time_ms=propagation_time_ms,
            success=len(errors) == 0,
            errors=errors,
        )

    async def _update_swarm_recall_status(
        self,
        swarm_id: UUID,
        recall: RecallNotice,
    ) -> None:
        """Update a swarm's knowledge with recall information."""
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return

        # Add recall to swarm's collective knowledge
        recall_knowledge = {
            "active_recalls": swarm.collective_knowledge.get("active_recalls", []),
        }

        recall_entry = {
            "recall_id": str(recall.id),
            "source": recall.source,
            "severity": recall.severity.value,
            "title": recall.title,
            "defect": recall.defect_description,
            "action": recall.recommended_action,
            "issued_at": recall.issued_at.isoformat(),
        }

        recall_knowledge["active_recalls"].append(recall_entry)

        # This would update via the repository
        # For now, just store in swarm object

    async def _notify_swarm_members(
        self,
        swarm_id: UUID,
        recall: RecallNotice,
    ) -> int:
        """Notify all members of a swarm about the recall."""
        members = await self.repository.get_swarm_members(swarm_id)
        notified_count = 0

        # Process in batches
        for i in range(0, len(members), self.PART_BATCH_SIZE):
            batch = members[i:i + self.PART_BATCH_SIZE]
            tasks = []

            for member in batch:
                tasks.append(self._notify_single_part(member.part_id, recall))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            notified_count += sum(1 for r in results if not isinstance(r, Exception))

        return notified_count

    async def _notify_single_part(
        self,
        part_id: UUID,
        recall: RecallNotice,
    ) -> None:
        """Notify a single part about the recall and generate qualia."""
        # Notify the part
        await self.repository.notify_part_of_recall(part_id, recall)

        # Generate recall awareness qualia
        qualia = self._generate_recall_qualia(part_id, recall)
        await self.repository.emit_qualia(part_id, qualia)

    def _generate_recall_qualia(
        self,
        part_id: UUID,
        recall: RecallNotice,
    ) -> dict[str, Any]:
        """
        Generate qualia representing the part's awareness of being recalled.

        This creates a significant experience for the part - the realization
        that it may be defective.
        """
        emotion = "alarm" if recall.severity == RecallSeverity.CRITICAL else "concern"

        return {
            "part_id": str(part_id),
            "experience_type": "recall_awareness",
            "significant_events": [{
                "type": "recall_notification",
                "severity": recall.severity.value,
                "description": f"Part notified of recall: {recall.title}",
                "emotion": emotion,
                "consciousness_contribution": 0.2,  # Recalls significantly impact consciousness
            }],
            "self_knowledge_update": {
                "potential_defect": recall.defect_description,
                "risk_level": recall.severity.value,
                "recommended_action": recall.recommended_action,
                "recall_source": recall.source,
                "recall_id": recall.source_recall_id,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def _trigger_emergency_learning(
        self,
        recall: RecallNotice,
    ) -> None:
        """
        Trigger emergency learning for critical recalls.

        This fast-tracks the recall information to ensure rapid propagation.
        """
        # Create an emergency learning from the recall
        emergency_learning = Learning(
            learning_type=LearningType.FAILURE_MODE,
            content={
                "failure_type": "recall_defect",
                "recall_source": recall.source,
                "recall_id": recall.source_recall_id,
                "defect_description": recall.defect_description,
                "severity": recall.severity.value,
                "prevention_measures": [recall.recommended_action],
                "emergency": True,
            },
            confidence=1.0,  # Recalls are authoritative
            applicability="similar_specs",
            novelty_score=1.0,  # Always novel/urgent
        )

        # The emergency learning would be propagated via the PropagationEngine
        # with maximum priority


class RecallNotificationService:
    """
    Service for sending external notifications about recalls.
    """

    async def notify_stakeholders(
        self,
        recall: RecallNotice,
        affected_count: int,
    ) -> None:
        """Notify external stakeholders about a recall."""
        # This would integrate with email, SMS, or other notification services
        pass

    async def notify_manufacturers(
        self,
        recall: RecallNotice,
    ) -> None:
        """Notify manufacturers about parts affected."""
        pass

    async def notify_service_centers(
        self,
        recall: RecallNotice,
    ) -> None:
        """Notify service centers about recall."""
        pass
