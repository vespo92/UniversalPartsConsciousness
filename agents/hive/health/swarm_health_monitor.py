"""
Swarm Health Monitor - Monitors and reports on swarm vitality.

Tracks activity, learning velocity, and overall health of swarms.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from uuid import UUID

from ..models import Swarm, SwarmHealth, SwarmHealthStatus


@dataclass
class HealthThresholds:
    """Configurable thresholds for health assessment."""
    activity_healthy: float = 0.7
    activity_declining: float = 0.4
    activity_stagnant: float = 0.1
    elder_ratio_healthy: float = 0.1
    learning_velocity_healthy: float = 1.0  # per day
    propagation_latency_healthy_ms: float = 500


@dataclass
class SwarmHealthReport:
    """Comprehensive health report for a swarm."""
    swarm_id: UUID
    swarm_name: str
    health: SwarmHealth
    issues: list[str]
    recommendations: list[str]
    trend: str  # "improving", "stable", "declining"
    report_time: datetime


class HealthRepository(Protocol):
    """Protocol for health data operations."""

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def get_swarm_activity_count(
        self,
        swarm_id: UUID,
        since: datetime,
    ) -> int:
        """Get activity count for swarm since time."""
        ...

    async def get_swarm_learning_count(
        self,
        swarm_id: UUID,
        since: datetime,
    ) -> int:
        """Get learning count for swarm since time."""
        ...

    async def get_average_propagation_latency(
        self,
        swarm_id: UUID,
        since: datetime,
    ) -> float:
        """Get average propagation latency in ms."""
        ...

    async def get_previous_health(
        self,
        swarm_id: UUID,
    ) -> Optional[SwarmHealth]:
        """Get previous health measurement."""
        ...

    async def save_health(
        self,
        health: SwarmHealth,
    ) -> None:
        """Save health measurement."""
        ...


class SwarmHealthMonitor:
    """
    Monitors swarm health and generates reports.
    """

    def __init__(
        self,
        repository: HealthRepository,
        thresholds: Optional[HealthThresholds] = None,
    ):
        self.repository = repository
        self.thresholds = thresholds or HealthThresholds()

    async def measure_health(
        self,
        swarm_id: UUID,
    ) -> SwarmHealth:
        """
        Measure current health of a swarm.

        Args:
            swarm_id: The swarm to measure

        Returns:
            Current health metrics
        """
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return SwarmHealth(swarm_id=swarm_id, health_status=SwarmHealthStatus.DORMANT)

        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)

        # Calculate activity metrics
        daily_activity = await self.repository.get_swarm_activity_count(swarm_id, day_ago)
        weekly_activity = await self.repository.get_swarm_activity_count(swarm_id, week_ago)

        # Learning velocity (learnings per day)
        daily_learnings = await self.repository.get_swarm_learning_count(swarm_id, day_ago)
        weekly_learnings = await self.repository.get_swarm_learning_count(swarm_id, week_ago)
        learning_velocity = weekly_learnings / 7.0 if weekly_learnings > 0 else 0

        # Propagation latency
        avg_latency = await self.repository.get_average_propagation_latency(swarm_id, week_ago)

        # Calculate ratios
        total_members = swarm.member_count or 1
        active_ratio = swarm.active_member_count / total_members if total_members > 0 else 0
        elder_ratio = swarm.elder_count / swarm.active_member_count if swarm.active_member_count > 0 else 0
        contribution_rate = weekly_activity / swarm.active_member_count if swarm.active_member_count > 0 else 0

        # Calculate activity score (0-1)
        activity_score = self._calculate_activity_score(
            daily_activity,
            weekly_activity,
            active_ratio,
            learning_velocity,
        )

        # Determine health status
        health_status = self._determine_status(activity_score)

        # Calculate knowledge metrics
        knowledge_depth = swarm.learning_count
        knowledge_freshness = self._calculate_freshness(swarm.last_learning_at)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            activity_score,
            elder_ratio,
            learning_velocity,
            avg_latency,
        )

        # Calculate composite health score
        health_score = self._calculate_health_score(
            activity_score,
            elder_ratio,
            learning_velocity,
            avg_latency,
            knowledge_freshness,
        )

        health = SwarmHealth(
            swarm_id=swarm_id,
            activity_score=activity_score,
            learning_velocity=learning_velocity,
            propagation_latency_ms=avg_latency,
            active_member_ratio=active_ratio,
            elder_ratio=elder_ratio,
            contribution_rate=contribution_rate,
            knowledge_depth=knowledge_depth,
            knowledge_breadth=len(swarm.collective_knowledge),
            knowledge_freshness=knowledge_freshness,
            health_status=health_status,
            health_score=health_score,
            recommendations=recommendations,
            measured_at=now,
        )

        # Save measurement
        await self.repository.save_health(health)

        return health

    async def generate_report(
        self,
        swarm_id: UUID,
    ) -> SwarmHealthReport:
        """
        Generate a comprehensive health report.

        Args:
            swarm_id: The swarm to report on

        Returns:
            Health report
        """
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return SwarmHealthReport(
                swarm_id=swarm_id,
                swarm_name="Unknown",
                health=SwarmHealth(swarm_id=swarm_id),
                issues=["Swarm not found"],
                recommendations=[],
                trend="unknown",
                report_time=datetime.utcnow(),
            )

        current_health = await self.measure_health(swarm_id)
        previous_health = await self.repository.get_previous_health(swarm_id)

        # Identify issues
        issues = self._identify_issues(current_health)

        # Determine trend
        trend = self._determine_trend(current_health, previous_health)

        return SwarmHealthReport(
            swarm_id=swarm_id,
            swarm_name=swarm.name,
            health=current_health,
            issues=issues,
            recommendations=current_health.recommendations,
            trend=trend,
            report_time=datetime.utcnow(),
        )

    def _calculate_activity_score(
        self,
        daily_activity: int,
        weekly_activity: int,
        active_ratio: float,
        learning_velocity: float,
    ) -> float:
        """Calculate overall activity score (0-1)."""
        # Weight recent activity more
        daily_factor = min(daily_activity / 100, 1.0) * 0.3
        weekly_factor = min(weekly_activity / 500, 1.0) * 0.2
        active_factor = active_ratio * 0.3
        learning_factor = min(learning_velocity / 5, 1.0) * 0.2

        return round(daily_factor + weekly_factor + active_factor + learning_factor, 3)

    def _determine_status(self, activity_score: float) -> SwarmHealthStatus:
        """Determine health status from activity score."""
        if activity_score >= self.thresholds.activity_healthy:
            return SwarmHealthStatus.THRIVING
        elif activity_score >= self.thresholds.activity_declining:
            return SwarmHealthStatus.HEALTHY
        elif activity_score >= self.thresholds.activity_stagnant:
            return SwarmHealthStatus.DECLINING
        elif activity_score > 0:
            return SwarmHealthStatus.STAGNANT
        else:
            return SwarmHealthStatus.DORMANT

    def _calculate_freshness(
        self,
        last_learning: Optional[datetime],
    ) -> float:
        """Calculate knowledge freshness (0-1)."""
        if not last_learning:
            return 0.0

        days_since = (datetime.utcnow() - last_learning).days
        # Exponential decay with 30-day half-life
        return 0.5 ** (days_since / 30)

    def _calculate_health_score(
        self,
        activity_score: float,
        elder_ratio: float,
        learning_velocity: float,
        latency_ms: float,
        freshness: float,
    ) -> float:
        """Calculate composite health score (0-1)."""
        # Normalize components
        activity_component = activity_score * 0.3
        elder_component = min(elder_ratio / self.thresholds.elder_ratio_healthy, 1.0) * 0.15
        learning_component = min(learning_velocity / self.thresholds.learning_velocity_healthy, 1.0) * 0.25
        latency_component = (1 - min(latency_ms / 1000, 1.0)) * 0.15  # Lower latency = better
        freshness_component = freshness * 0.15

        return round(
            activity_component + elder_component + learning_component +
            latency_component + freshness_component,
            3
        )

    def _generate_recommendations(
        self,
        activity_score: float,
        elder_ratio: float,
        learning_velocity: float,
        latency_ms: float,
    ) -> list[str]:
        """Generate recommendations for improving health."""
        recommendations = []

        if activity_score < self.thresholds.activity_declining:
            recommendations.append("Increase member engagement through targeted learning propagation")

        if elder_ratio < self.thresholds.elder_ratio_healthy / 2:
            recommendations.append("Nurture experienced members to develop more elders")

        if learning_velocity < self.thresholds.learning_velocity_healthy / 2:
            recommendations.append("Encourage more qualia collection from swarm members")

        if latency_ms > self.thresholds.propagation_latency_healthy_ms * 2:
            recommendations.append("Optimize propagation pathways to reduce latency")

        if not recommendations:
            recommendations.append("Swarm is healthy - continue current patterns")

        return recommendations

    def _identify_issues(self, health: SwarmHealth) -> list[str]:
        """Identify specific issues with swarm health."""
        issues = []

        if health.activity_score < self.thresholds.activity_stagnant:
            issues.append("Critically low activity - swarm may become dormant")

        if health.elder_ratio < 0.01:
            issues.append("No elder members - swarm lacks experienced guidance")

        if health.learning_velocity < 0.1:
            issues.append("Very low learning velocity - knowledge is not growing")

        if health.propagation_latency_ms > 2000:
            issues.append("High propagation latency affecting knowledge spread")

        if health.knowledge_freshness < 0.2:
            issues.append("Stale knowledge - no recent learnings")

        return issues

    def _determine_trend(
        self,
        current: SwarmHealth,
        previous: Optional[SwarmHealth],
    ) -> str:
        """Determine health trend compared to previous measurement."""
        if not previous:
            return "unknown"

        score_diff = current.health_score - previous.health_score

        if score_diff > 0.05:
            return "improving"
        elif score_diff < -0.05:
            return "declining"
        else:
            return "stable"
