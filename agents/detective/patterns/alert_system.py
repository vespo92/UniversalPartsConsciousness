"""
Alert System

Manages alerts and notifications for failure patterns.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts"""
    PATTERN_DETECTED = "pattern_detected"
    RECALL_WARNING = "recall_warning"
    SUPPLIER_QUALITY = "supplier_quality"
    SIMILAR_FAILURE = "similar_failure"
    TREND_DETECTED = "trend_detected"


@dataclass
class FailureAlert:
    """Alert for a failure pattern or event"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    description: str
    affected_parts: List[str]
    affected_users: int
    recommended_action: str
    created_at: datetime
    expires_at: Optional[datetime]
    acknowledged: bool


class AlertSystem:
    """
    Manages alerts and notifications for failure patterns.

    Handles:
    - Alert creation and routing
    - User notification
    - Alert acknowledgment
    - Alert escalation
    """

    def __init__(self):
        """Initialize the alert system."""
        self.active_alerts: List[FailureAlert] = []
        self.alert_history: List[FailureAlert] = []

    async def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        description: str,
        affected_parts: List[str],
        recommended_action: str
    ) -> FailureAlert:
        """
        Create a new alert.

        Args:
            alert_type: Type of alert
            severity: Severity level
            title: Alert title
            description: Detailed description
            affected_parts: List of affected part IDs
            recommended_action: Recommended user action

        Returns:
            Created alert
        """
        alert = FailureAlert(
            alert_id=self._generate_alert_id(),
            alert_type=alert_type,
            severity=severity,
            title=title,
            description=description,
            affected_parts=affected_parts,
            affected_users=self._estimate_affected_users(affected_parts),
            recommended_action=recommended_action,
            created_at=datetime.utcnow(),
            expires_at=None,
            acknowledged=False
        )

        self.active_alerts.append(alert)

        # Route alert to appropriate channels
        await self._route_alert(alert)

        return alert

    async def create_pattern_alert(
        self,
        pattern_id: str,
        description: str,
        affected_parts: List[str],
        confidence: float
    ) -> FailureAlert:
        """Create an alert for a detected pattern."""
        severity = AlertSeverity.HIGH if confidence > 0.8 else AlertSeverity.WARNING

        return await self.create_alert(
            alert_type=AlertType.PATTERN_DETECTED,
            severity=severity,
            title=f"Failure Pattern Detected: {pattern_id}",
            description=description,
            affected_parts=affected_parts,
            recommended_action="Review affected parts and consider preventive action"
        )

    async def create_supplier_alert(
        self,
        supplier: str,
        issue: str,
        affected_parts: List[str]
    ) -> FailureAlert:
        """Create an alert for supplier quality issues."""
        return await self.create_alert(
            alert_type=AlertType.SUPPLIER_QUALITY,
            severity=AlertSeverity.HIGH,
            title=f"Supplier Quality Alert: {supplier}",
            description=issue,
            affected_parts=affected_parts,
            recommended_action="Verify parts from this supplier, consider alternative sources"
        )

    async def create_recall_warning(
        self,
        parts: List[str],
        reason: str,
        scope: int
    ) -> FailureAlert:
        """Create a potential recall warning."""
        return await self.create_alert(
            alert_type=AlertType.RECALL_WARNING,
            severity=AlertSeverity.CRITICAL,
            title="Potential Recall Warning",
            description=f"{reason}. Estimated scope: {scope} units",
            affected_parts=parts,
            recommended_action="URGENT: Stop use of affected parts, contact manufacturer"
        )

    async def acknowledge_alert(self, alert_id: str, user_id: str) -> bool:
        """Acknowledge an alert."""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                return True
        return False

    async def get_active_alerts(
        self,
        severity_filter: Optional[AlertSeverity] = None,
        type_filter: Optional[AlertType] = None
    ) -> List[FailureAlert]:
        """Get active alerts with optional filtering."""
        alerts = self.active_alerts

        if severity_filter:
            alerts = [a for a in alerts if a.severity == severity_filter]

        if type_filter:
            alerts = [a for a in alerts if a.alert_type == type_filter]

        return alerts

    async def get_alerts_for_parts(
        self,
        part_ids: List[str]
    ) -> List[FailureAlert]:
        """Get all alerts affecting specified parts."""
        alerts = []
        for alert in self.active_alerts:
            if any(part in alert.affected_parts for part in part_ids):
                alerts.append(alert)
        return alerts

    def _generate_alert_id(self) -> str:
        """Generate unique alert ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        import random
        random_suffix = random.randint(100, 999)
        return f"ALERT-{timestamp}-{random_suffix}"

    def _estimate_affected_users(self, affected_parts: List[str]) -> int:
        """Estimate number of users affected by parts."""
        # Simulated - in production would query user database
        return len(affected_parts) * 100

    async def _route_alert(self, alert: FailureAlert) -> None:
        """Route alert to appropriate notification channels."""
        # Simulated routing logic
        if alert.severity == AlertSeverity.CRITICAL:
            # Send immediate notification
            await self._send_critical_notification(alert)
        elif alert.severity == AlertSeverity.HIGH:
            # Add to digest for affected users
            await self._queue_for_digest(alert)
        else:
            # Store for dashboard display
            pass

    async def _send_critical_notification(self, alert: FailureAlert) -> None:
        """Send immediate notification for critical alerts."""
        # Would integrate with notification service
        pass

    async def _queue_for_digest(self, alert: FailureAlert) -> None:
        """Queue alert for user digest."""
        # Would integrate with digest service
        pass
