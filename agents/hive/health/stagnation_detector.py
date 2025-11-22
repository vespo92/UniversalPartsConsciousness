"""
Stagnation Detector - Detects and alerts on inactive swarms.

Identifies swarms that are becoming stagnant and may need intervention.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from uuid import UUID

from ..models import Swarm, SwarmHealthStatus


@dataclass
class StagnationAlert:
    """Alert for a stagnating swarm."""
    swarm_id: UUID
    swarm_name: str
    alert_level: str  # "warning", "critical"
    days_inactive: int
    last_activity: Optional[datetime]
    last_learning: Optional[datetime]
    recommendations: list[str]
    detected_at: datetime


@dataclass
class StagnationReport:
    """Report on swarm stagnation status."""
    total_swarms_checked: int
    healthy_swarms: int
    warning_swarms: int
    critical_swarms: int
    dormant_swarms: int
    alerts: list[StagnationAlert]
    report_time: datetime


class StagnationRepository(Protocol):
    """Protocol for stagnation detection operations."""

    async def get_all_swarms(self) -> list[Swarm]:
        """Get all swarms."""
        ...

    async def get_last_activity(self, swarm_id: UUID) -> Optional[datetime]:
        """Get last activity timestamp for swarm."""
        ...

    async def get_last_learning(self, swarm_id: UUID) -> Optional[datetime]:
        """Get last learning timestamp for swarm."""
        ...

    async def update_swarm_status(
        self,
        swarm_id: UUID,
        status: SwarmHealthStatus,
    ) -> None:
        """Update swarm health status."""
        ...


class StagnationDetector:
    """
    Detects stagnation in swarms and generates alerts.
    """

    # Stagnation thresholds (days)
    WARNING_THRESHOLD = 14  # 2 weeks
    CRITICAL_THRESHOLD = 30  # 1 month
    DORMANT_THRESHOLD = 90  # 3 months

    def __init__(self, repository: StagnationRepository):
        self.repository = repository

    async def detect_stagnation(
        self,
        swarm_id: UUID,
    ) -> Optional[StagnationAlert]:
        """
        Check a swarm for stagnation.

        Args:
            swarm_id: The swarm to check

        Returns:
            Alert if stagnating, None otherwise
        """
        last_activity = await self.repository.get_last_activity(swarm_id)
        last_learning = await self.repository.get_last_learning(swarm_id)

        # Use the more recent of activity or learning
        last_event = None
        if last_activity and last_learning:
            last_event = max(last_activity, last_learning)
        else:
            last_event = last_activity or last_learning

        if not last_event:
            # No activity ever recorded - might be new or truly dormant
            return StagnationAlert(
                swarm_id=swarm_id,
                swarm_name="Unknown",
                alert_level="critical",
                days_inactive=-1,  # Unknown
                last_activity=None,
                last_learning=None,
                recommendations=["Initialize swarm with seed data"],
                detected_at=datetime.utcnow(),
            )

        days_inactive = (datetime.utcnow() - last_event).days

        if days_inactive >= self.DORMANT_THRESHOLD:
            return await self._create_alert(
                swarm_id, "critical", days_inactive, last_activity, last_learning,
                ["Consider archiving or merging this swarm", "Review if swarm category is still relevant"]
            )
        elif days_inactive >= self.CRITICAL_THRESHOLD:
            return await self._create_alert(
                swarm_id, "critical", days_inactive, last_activity, last_learning,
                ["Urgently need new data or member engagement", "Consider cross-swarm knowledge injection"]
            )
        elif days_inactive >= self.WARNING_THRESHOLD:
            return await self._create_alert(
                swarm_id, "warning", days_inactive, last_activity, last_learning,
                ["Encourage member participation", "Propagate relevant learnings from related swarms"]
            )

        return None

    async def scan_all_swarms(self) -> StagnationReport:
        """
        Scan all swarms for stagnation.

        Returns:
            Comprehensive stagnation report
        """
        swarms = await self.repository.get_all_swarms()

        healthy = 0
        warning = 0
        critical = 0
        dormant = 0
        alerts: list[StagnationAlert] = []

        for swarm in swarms:
            alert = await self.detect_stagnation(swarm.id)

            if alert:
                alerts.append(alert)
                if alert.alert_level == "warning":
                    warning += 1
                else:  # critical
                    if alert.days_inactive >= self.DORMANT_THRESHOLD or alert.days_inactive < 0:
                        dormant += 1
                    else:
                        critical += 1
            else:
                healthy += 1

        return StagnationReport(
            total_swarms_checked=len(swarms),
            healthy_swarms=healthy,
            warning_swarms=warning,
            critical_swarms=critical,
            dormant_swarms=dormant,
            alerts=alerts,
            report_time=datetime.utcnow(),
        )

    async def auto_update_status(
        self,
        swarm_id: UUID,
    ) -> Optional[SwarmHealthStatus]:
        """
        Automatically update swarm status based on activity.

        Args:
            swarm_id: The swarm to update

        Returns:
            New status if changed, None otherwise
        """
        alert = await self.detect_stagnation(swarm_id)

        if not alert:
            # Healthy - ensure not marked as stagnant
            await self.repository.update_swarm_status(swarm_id, SwarmHealthStatus.HEALTHY)
            return SwarmHealthStatus.HEALTHY

        if alert.days_inactive >= self.DORMANT_THRESHOLD or alert.days_inactive < 0:
            await self.repository.update_swarm_status(swarm_id, SwarmHealthStatus.DORMANT)
            return SwarmHealthStatus.DORMANT
        elif alert.days_inactive >= self.CRITICAL_THRESHOLD:
            await self.repository.update_swarm_status(swarm_id, SwarmHealthStatus.STAGNANT)
            return SwarmHealthStatus.STAGNANT
        elif alert.days_inactive >= self.WARNING_THRESHOLD:
            await self.repository.update_swarm_status(swarm_id, SwarmHealthStatus.DECLINING)
            return SwarmHealthStatus.DECLINING

        return None

    async def _create_alert(
        self,
        swarm_id: UUID,
        level: str,
        days_inactive: int,
        last_activity: Optional[datetime],
        last_learning: Optional[datetime],
        recommendations: list[str],
    ) -> StagnationAlert:
        """Create a stagnation alert."""
        # Would fetch swarm name from repository
        return StagnationAlert(
            swarm_id=swarm_id,
            swarm_name="Unknown",  # Would be fetched
            alert_level=level,
            days_inactive=days_inactive,
            last_activity=last_activity,
            last_learning=last_learning,
            recommendations=recommendations,
            detected_at=datetime.utcnow(),
        )

    async def get_revival_candidates(
        self,
        max_dormant_days: int = 180,
    ) -> list[UUID]:
        """
        Get dormant swarms that might be worth reviving.

        Args:
            max_dormant_days: Maximum days of dormancy to consider

        Returns:
            List of swarm IDs worth reviving
        """
        report = await self.scan_all_swarms()

        candidates = []
        for alert in report.alerts:
            if alert.alert_level == "critical":
                if 0 < alert.days_inactive <= max_dormant_days:
                    candidates.append(alert.swarm_id)

        return candidates


class StagnationScheduler:
    """
    Schedules periodic stagnation scans.
    """

    def __init__(self, detector: StagnationDetector):
        self.detector = detector
        self.last_scan: Optional[datetime] = None
        self.scan_interval = timedelta(hours=24)

    async def should_scan(self) -> bool:
        """Check if a scan is due."""
        if self.last_scan is None:
            return True
        return datetime.utcnow() - self.last_scan >= self.scan_interval

    async def run_scheduled_scan(self) -> Optional[StagnationReport]:
        """Run a scheduled scan if due."""
        if await self.should_scan():
            report = await self.detector.scan_all_swarms()
            self.last_scan = datetime.utcnow()
            return report
        return None
