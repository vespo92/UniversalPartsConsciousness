"""
Recall Tracker - Tracks recall resolution and compliance.

Monitors the lifecycle of recalls from detection to resolution.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import RecallNotice, RecallSeverity


@dataclass
class RecallStatus:
    """Current status of a recall."""
    recall_id: UUID
    status: str  # "active", "resolved", "expired", "superseded"
    parts_affected: int
    parts_remediated: int
    remediation_rate: float
    days_since_issued: int
    last_activity: datetime


@dataclass
class RecallMetrics:
    """Aggregate metrics for recalls."""
    total_active: int
    total_resolved: int
    avg_remediation_rate: float
    avg_time_to_resolution_days: float
    by_severity: dict[str, int]


class RecallTrackerRepository(Protocol):
    """Protocol for recall tracking operations."""

    async def get_recall(self, recall_id: UUID) -> Optional[RecallNotice]:
        """Get recall by ID."""
        ...

    async def get_active_recalls(self) -> list[RecallNotice]:
        """Get all active recalls."""
        ...

    async def update_recall(self, recall: RecallNotice) -> None:
        """Update recall."""
        ...

    async def get_remediation_count(self, recall_id: UUID) -> int:
        """Get count of remediated parts for a recall."""
        ...

    async def record_remediation(
        self,
        part_id: UUID,
        recall_id: UUID,
        remediation_type: str,
    ) -> None:
        """Record that a part was remediated."""
        ...


class RecallTracker:
    """
    Tracks recall lifecycle and compliance.
    """

    # Resolution thresholds
    RESOLUTION_THRESHOLD = 0.99  # 99% remediation for resolution
    EXPIRY_DAYS = 365  # Recalls expire after 1 year if not resolved

    def __init__(self, repository: RecallTrackerRepository):
        self.repository = repository

    async def get_recall_status(
        self,
        recall_id: UUID,
    ) -> Optional[RecallStatus]:
        """
        Get the current status of a recall.

        Args:
            recall_id: The recall to check

        Returns:
            Current recall status
        """
        recall = await self.repository.get_recall(recall_id)
        if not recall:
            return None

        remediated_count = await self.repository.get_remediation_count(recall_id)
        total_affected = recall.affected_parts_count

        remediation_rate = (
            remediated_count / total_affected
            if total_affected > 0
            else 0.0
        )

        days_since_issued = (datetime.utcnow() - recall.issued_at).days

        # Determine status
        if remediation_rate >= self.RESOLUTION_THRESHOLD:
            status = "resolved"
        elif days_since_issued > self.EXPIRY_DAYS:
            status = "expired"
        else:
            status = "active"

        return RecallStatus(
            recall_id=recall_id,
            status=status,
            parts_affected=total_affected,
            parts_remediated=remediated_count,
            remediation_rate=remediation_rate,
            days_since_issued=days_since_issued,
            last_activity=recall.propagation_complete_at or recall.received_at,
        )

    async def record_part_remediation(
        self,
        part_id: UUID,
        recall_id: UUID,
        remediation_type: str = "replaced",
    ) -> bool:
        """
        Record that a part has been remediated for a recall.

        Args:
            part_id: The remediated part
            recall_id: The recall being addressed
            remediation_type: Type of remediation (replaced, repaired, inspected)

        Returns:
            True if recorded successfully
        """
        try:
            await self.repository.record_remediation(
                part_id,
                recall_id,
                remediation_type,
            )
            return True
        except Exception:
            return False

    async def get_recall_metrics(self) -> RecallMetrics:
        """
        Get aggregate metrics for all recalls.

        Returns:
            Recall metrics
        """
        active_recalls = await self.repository.get_active_recalls()

        total_active = 0
        total_resolved = 0
        total_remediation = 0.0
        total_resolution_days = 0.0
        resolved_count = 0
        by_severity: dict[str, int] = {}

        for recall in active_recalls:
            status = await self.get_recall_status(recall.id)
            if not status:
                continue

            if status.status == "active":
                total_active += 1
            elif status.status == "resolved":
                total_resolved += 1
                resolved_count += 1
                total_resolution_days += status.days_since_issued
            else:
                total_resolved += 1  # Count expired as resolved

            total_remediation += status.remediation_rate

            # Count by severity
            severity = recall.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1

        total_recalls = len(active_recalls)
        avg_remediation = total_remediation / total_recalls if total_recalls > 0 else 0.0
        avg_resolution_days = total_resolution_days / resolved_count if resolved_count > 0 else 0.0

        return RecallMetrics(
            total_active=total_active,
            total_resolved=total_resolved,
            avg_remediation_rate=avg_remediation,
            avg_time_to_resolution_days=avg_resolution_days,
            by_severity=by_severity,
        )

    async def get_outstanding_parts(
        self,
        recall_id: UUID,
    ) -> list[UUID]:
        """
        Get parts that have not been remediated for a recall.

        Args:
            recall_id: The recall to check

        Returns:
            List of part IDs awaiting remediation
        """
        # This would query for parts that:
        # 1. Were notified of the recall
        # 2. Have not been marked as remediated
        # Implementation depends on repository
        return []

    async def check_auto_resolution(
        self,
        recall_id: UUID,
    ) -> bool:
        """
        Check if a recall should be auto-resolved.

        Args:
            recall_id: The recall to check

        Returns:
            True if auto-resolved
        """
        status = await self.get_recall_status(recall_id)
        if not status:
            return False

        if status.remediation_rate >= self.RESOLUTION_THRESHOLD:
            recall = await self.repository.get_recall(recall_id)
            if recall:
                recall.propagation_status = "resolved"
                await self.repository.update_recall(recall)
                return True

        return False

    async def generate_compliance_report(
        self,
        recall_id: UUID,
    ) -> dict[str, Any]:
        """
        Generate a compliance report for a recall.

        Args:
            recall_id: The recall to report on

        Returns:
            Compliance report data
        """
        recall = await self.repository.get_recall(recall_id)
        status = await self.get_recall_status(recall_id)

        if not recall or not status:
            return {"error": "Recall not found"}

        outstanding = await self.get_outstanding_parts(recall_id)

        return {
            "recall_id": str(recall_id),
            "source": recall.source,
            "source_recall_id": recall.source_recall_id,
            "title": recall.title,
            "severity": recall.severity.value,
            "issued_at": recall.issued_at.isoformat(),
            "status": status.status,
            "compliance": {
                "parts_affected": status.parts_affected,
                "parts_remediated": status.parts_remediated,
                "remediation_rate": f"{status.remediation_rate:.1%}",
                "outstanding_count": len(outstanding),
            },
            "timeline": {
                "days_since_issued": status.days_since_issued,
                "last_activity": status.last_activity.isoformat(),
            },
            "generated_at": datetime.utcnow().isoformat(),
        }
