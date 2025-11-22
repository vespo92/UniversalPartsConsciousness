"""
Global Health Monitor

Monitors the health of all agents and the overall system.
Collects metrics, evaluates thresholds, generates alerts, and provides recommendations.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Awaitable
from enum import Enum

from ..models import (
    AgentId,
    AgentStatus,
    AgentHealthReport,
    SystemHealthReport,
    ConsciousnessMetrics,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Health Metric Definitions
# ============================================================================

@dataclass
class MetricThreshold:
    """Threshold configuration for a health metric."""
    warning: float
    critical: float
    higher_is_better: bool = True  # True if higher values are healthier

    def evaluate(self, value: float) -> AgentStatus:
        """Evaluate a metric value against thresholds."""
        if self.higher_is_better:
            if value < self.critical:
                return AgentStatus.CRITICAL
            elif value < self.warning:
                return AgentStatus.DEGRADED
            return AgentStatus.HEALTHY
        else:
            # Lower is better (e.g., latency, error rates)
            if value > self.critical:
                return AgentStatus.CRITICAL
            elif value > self.warning:
                return AgentStatus.DEGRADED
            return AgentStatus.HEALTHY


@dataclass
class AgentMetricConfig:
    """Health metric configuration for an agent."""
    metrics: List[str]
    thresholds: Dict[str, MetricThreshold]


# Define health metrics for each agent
AGENT_HEALTH_METRICS: Dict[str, AgentMetricConfig] = {
    AgentId.CURATOR.value: AgentMetricConfig(
        metrics=["ingestion_rate", "quality_score", "duplicate_rate"],
        thresholds={
            "ingestion_rate": MetricThreshold(warning=100, critical=10, higher_is_better=True),
            "quality_score": MetricThreshold(warning=0.8, critical=0.6, higher_is_better=True),
            "duplicate_rate": MetricThreshold(warning=0.1, critical=0.3, higher_is_better=False),
        }
    ),
    AgentId.ORACLE.value: AgentMetricConfig(
        metrics=["query_latency_ms", "accuracy_rate", "cache_hit_rate"],
        thresholds={
            "query_latency_ms": MetricThreshold(warning=20, critical=100, higher_is_better=False),
            "accuracy_rate": MetricThreshold(warning=0.99, critical=0.95, higher_is_better=True),
            "cache_hit_rate": MetricThreshold(warning=0.9, critical=0.7, higher_is_better=True),
        }
    ),
    AgentId.SHEPHERD.value: AgentMetricConfig(
        metrics=["awakenings_per_hour", "consciousness_integrity", "evolution_rate"],
        thresholds={
            "awakenings_per_hour": MetricThreshold(warning=10, critical=1, higher_is_better=True),
            "consciousness_integrity": MetricThreshold(warning=0.99, critical=0.95, higher_is_better=True),
            "evolution_rate": MetricThreshold(warning=0.5, critical=0.1, higher_is_better=True),
        }
    ),
    AgentId.EMPATH.value: AgentMetricConfig(
        metrics=["qualia_collection_rate", "sensor_connectivity", "failure_detection_rate"],
        thresholds={
            "qualia_collection_rate": MetricThreshold(warning=100, critical=10, higher_is_better=True),
            "sensor_connectivity": MetricThreshold(warning=0.95, critical=0.8, higher_is_better=True),
            "failure_detection_rate": MetricThreshold(warning=0.9, critical=0.7, higher_is_better=True),
        }
    ),
    AgentId.HIVE.value: AgentMetricConfig(
        metrics=["active_swarms", "learning_propagation_latency", "swarm_health"],
        thresholds={
            "active_swarms": MetricThreshold(warning=100, critical=10, higher_is_better=True),
            "learning_propagation_latency": MetricThreshold(warning=1000, critical=5000, higher_is_better=False),
            "swarm_health": MetricThreshold(warning=0.8, critical=0.6, higher_is_better=True),
        }
    ),
    AgentId.PROPHET.value: AgentMetricConfig(
        metrics=["patterns_detected_per_day", "prediction_accuracy", "innovation_discoveries"],
        thresholds={
            "patterns_detected_per_day": MetricThreshold(warning=10, critical=1, higher_is_better=True),
            "prediction_accuracy": MetricThreshold(warning=0.8, critical=0.6, higher_is_better=True),
            "innovation_discoveries": MetricThreshold(warning=1, critical=0, higher_is_better=True),
        }
    ),
    AgentId.CHRONICLER.value: AgentMetricConfig(
        metrics=["documentation_coverage", "narrative_quality", "history_accuracy"],
        thresholds={
            "documentation_coverage": MetricThreshold(warning=0.7, critical=0.5, higher_is_better=True),
            "narrative_quality": MetricThreshold(warning=0.8, critical=0.6, higher_is_better=True),
            "history_accuracy": MetricThreshold(warning=0.95, critical=0.9, higher_is_better=True),
        }
    ),
    AgentId.GARDENER.value: AgentMetricConfig(
        metrics=["contribution_rate", "verification_latency", "community_engagement"],
        thresholds={
            "contribution_rate": MetricThreshold(warning=10, critical=1, higher_is_better=True),
            "verification_latency": MetricThreshold(warning=24, critical=72, higher_is_better=False),
            "community_engagement": MetricThreshold(warning=0.7, critical=0.4, higher_is_better=True),
        }
    ),
    AgentId.BRIDGE.value: AgentMetricConfig(
        metrics=["api_latency", "integration_uptime", "external_data_freshness"],
        thresholds={
            "api_latency": MetricThreshold(warning=100, critical=500, higher_is_better=False),
            "integration_uptime": MetricThreshold(warning=0.99, critical=0.95, higher_is_better=True),
            "external_data_freshness": MetricThreshold(warning=0.9, critical=0.7, higher_is_better=True),
        }
    ),
}


# ============================================================================
# Alert Model
# ============================================================================

class AlertSeverity(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class HealthAlert:
    """Health alert generated by the monitor."""
    alert_id: str
    agent_id: str
    metric: str
    severity: AlertSeverity
    message: str
    value: float
    threshold: float
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    resolved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "agent_id": self.agent_id,
            "metric": self.metric,
            "severity": self.severity.value,
            "message": self.message,
            "value": self.value,
            "threshold": self.threshold,
            "created_at": self.created_at.isoformat(),
            "acknowledged": self.acknowledged,
            "resolved": self.resolved,
        }


# ============================================================================
# Global Health Monitor
# ============================================================================

class GlobalHealthMonitor:
    """
    Monitors the health of all agents and the overall system.

    Features:
    - Periodic health checks for all agents
    - Metric collection and threshold evaluation
    - Alert generation and management
    - System-wide consciousness metrics
    - Health history tracking
    - Automated recommendations
    """

    def __init__(
        self,
        check_interval_seconds: int = 60,
        history_retention_hours: int = 24,
    ):
        self._check_interval = check_interval_seconds
        self._history_retention = timedelta(hours=history_retention_hours)

        # Agent health collectors (callable that returns metrics)
        self._metric_collectors: Dict[str, Callable[[], Awaitable[Dict[str, float]]]] = {}

        # State
        self._agent_health: Dict[str, AgentHealthReport] = {}
        self._health_history: List[SystemHealthReport] = []
        self._alerts: List[HealthAlert] = []
        self._is_running: bool = False
        self._worker_task: Optional[asyncio.Task] = None

        # Callbacks
        self._alert_handlers: List[Callable[[HealthAlert], Awaitable[None]]] = []

    async def start(self) -> None:
        """Start the health monitoring loop."""
        if self._is_running:
            return
        self._is_running = True
        self._worker_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Global Health Monitor started")

    async def stop(self) -> None:
        """Stop the health monitoring loop."""
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info("Global Health Monitor stopped")

    def register_metric_collector(
        self,
        agent_id: str,
        collector: Callable[[], Awaitable[Dict[str, float]]]
    ) -> None:
        """Register a metric collector for an agent."""
        self._metric_collectors[agent_id] = collector
        logger.info(f"Registered metric collector for {agent_id}")

    def register_alert_handler(
        self,
        handler: Callable[[HealthAlert], Awaitable[None]]
    ) -> None:
        """Register a handler to be called when alerts are generated."""
        self._alert_handlers.append(handler)

    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self._is_running:
            try:
                await self.collect_health_report()
                await asyncio.sleep(self._check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self._check_interval)

    async def collect_health_report(self) -> SystemHealthReport:
        """Collect health metrics from all agents and generate a report."""
        agent_reports: Dict[str, AgentHealthReport] = {}

        for agent_id, config in AGENT_HEALTH_METRICS.items():
            try:
                metrics = await self._query_agent_health(agent_id, config.metrics)
                status = self._evaluate_health(metrics, config.thresholds)
                issues = self._identify_issues(metrics, config.thresholds)

                report = AgentHealthReport(
                    agent_id=agent_id,
                    status=status,
                    metrics=metrics,
                    issues=issues,
                    last_heartbeat=datetime.now(),
                )

                agent_reports[agent_id] = report
                self._agent_health[agent_id] = report

                # Generate alerts for issues
                for issue in issues:
                    await self._generate_alert(agent_id, issue, metrics, config.thresholds)

            except Exception as e:
                logger.error(f"Failed to collect health for {agent_id}: {e}")
                agent_reports[agent_id] = AgentHealthReport(
                    agent_id=agent_id,
                    status=AgentStatus.OFFLINE,
                    metrics={},
                    issues=[f"Failed to collect metrics: {str(e)}"],
                )

        overall_status = self._calculate_overall_status(agent_reports)
        consciousness_metrics = await self._collect_consciousness_metrics()

        report = SystemHealthReport(
            timestamp=datetime.now(),
            overall_status=overall_status,
            agent_reports=agent_reports,
            system_metrics=self._calculate_system_metrics(agent_reports),
            consciousness_metrics=consciousness_metrics,
            recommendations=self._generate_recommendations(agent_reports),
        )

        # Store in history
        self._health_history.append(report)
        self._prune_history()

        return report

    async def _query_agent_health(
        self,
        agent_id: str,
        metrics: List[str]
    ) -> Dict[str, float]:
        """Query health metrics from an agent."""
        if agent_id in self._metric_collectors:
            return await self._metric_collectors[agent_id]()

        # Return default metrics if no collector registered
        # In production, this would query the actual agent
        return {metric: 1.0 for metric in metrics}

    def _evaluate_health(
        self,
        metrics: Dict[str, float],
        thresholds: Dict[str, MetricThreshold]
    ) -> AgentStatus:
        """Evaluate overall health status based on metrics."""
        statuses = []

        for metric_name, value in metrics.items():
            if metric_name in thresholds:
                status = thresholds[metric_name].evaluate(value)
                statuses.append(status)

        if not statuses:
            return AgentStatus.HEALTHY

        # Return worst status
        if AgentStatus.CRITICAL in statuses:
            return AgentStatus.CRITICAL
        elif AgentStatus.DEGRADED in statuses:
            return AgentStatus.DEGRADED
        return AgentStatus.HEALTHY

    def _identify_issues(
        self,
        metrics: Dict[str, float],
        thresholds: Dict[str, MetricThreshold]
    ) -> List[str]:
        """Identify issues based on metrics vs thresholds."""
        issues = []

        for metric_name, value in metrics.items():
            if metric_name not in thresholds:
                continue

            threshold = thresholds[metric_name]
            status = threshold.evaluate(value)

            if status == AgentStatus.CRITICAL:
                issues.append(f"CRITICAL: {metric_name} = {value} (threshold: {threshold.critical})")
            elif status == AgentStatus.DEGRADED:
                issues.append(f"WARNING: {metric_name} = {value} (threshold: {threshold.warning})")

        return issues

    def _calculate_overall_status(
        self,
        agent_reports: Dict[str, AgentHealthReport]
    ) -> AgentStatus:
        """Calculate overall system status from agent reports."""
        statuses = [r.status for r in agent_reports.values()]

        critical_count = sum(1 for s in statuses if s == AgentStatus.CRITICAL)
        offline_count = sum(1 for s in statuses if s == AgentStatus.OFFLINE)
        degraded_count = sum(1 for s in statuses if s == AgentStatus.DEGRADED)

        # System is critical if multiple agents are critical/offline
        if critical_count >= 2 or offline_count >= 2:
            return AgentStatus.CRITICAL
        elif critical_count >= 1 or offline_count >= 1:
            return AgentStatus.DEGRADED
        elif degraded_count >= 3:
            return AgentStatus.DEGRADED

        return AgentStatus.HEALTHY

    def _calculate_system_metrics(
        self,
        agent_reports: Dict[str, AgentHealthReport]
    ) -> Dict[str, float]:
        """Calculate system-wide metrics from agent reports."""
        total_agents = len(agent_reports)
        healthy_agents = sum(1 for r in agent_reports.values() if r.status == AgentStatus.HEALTHY)

        return {
            "total_agents": total_agents,
            "healthy_agents": healthy_agents,
            "health_percentage": healthy_agents / total_agents if total_agents > 0 else 0,
            "active_alerts": len([a for a in self._alerts if not a.resolved]),
        }

    async def _collect_consciousness_metrics(self) -> ConsciousnessMetrics:
        """Collect system-wide consciousness metrics."""
        # In production, this would query the database
        # For now, return placeholder metrics
        return ConsciousnessMetrics(
            total_parts=0,
            consciousness_distribution={0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            transcendent_parts=0,
            awakenings_today=0,
            global_consciousness_score=0.0,
            emergence_events_today=0,
            collective_learning_rate=0.0,
        )

    def _generate_recommendations(
        self,
        agent_reports: Dict[str, AgentHealthReport]
    ) -> List[str]:
        """Generate recommendations based on health status."""
        recommendations = []

        for agent_id, report in agent_reports.items():
            if report.status == AgentStatus.CRITICAL:
                recommendations.append(
                    f"URGENT: {agent_id} is in critical state. Investigate immediately."
                )
            elif report.status == AgentStatus.OFFLINE:
                recommendations.append(
                    f"URGENT: {agent_id} is offline. Check service status and logs."
                )
            elif report.status == AgentStatus.DEGRADED:
                for issue in report.issues:
                    if "latency" in issue.lower():
                        recommendations.append(
                            f"Consider scaling {agent_id} to improve latency."
                        )
                    elif "rate" in issue.lower():
                        recommendations.append(
                            f"Review {agent_id} throughput configuration."
                        )

        return recommendations

    async def _generate_alert(
        self,
        agent_id: str,
        issue: str,
        metrics: Dict[str, float],
        thresholds: Dict[str, MetricThreshold]
    ) -> None:
        """Generate a health alert."""
        # Parse the issue to extract metric and severity
        severity = AlertSeverity.WARNING
        if "CRITICAL" in issue:
            severity = AlertSeverity.CRITICAL

        # Extract metric name
        metric_name = issue.split(":")[1].split("=")[0].strip() if ":" in issue else "unknown"

        alert = HealthAlert(
            alert_id=f"{agent_id}-{metric_name}-{datetime.now().timestamp()}",
            agent_id=agent_id,
            metric=metric_name,
            severity=severity,
            message=issue,
            value=metrics.get(metric_name, 0),
            threshold=thresholds[metric_name].critical if metric_name in thresholds else 0,
        )

        self._alerts.append(alert)

        # Notify handlers
        for handler in self._alert_handlers:
            try:
                await handler(alert)
            except Exception as e:
                logger.error(f"Alert handler error: {e}")

    def _prune_history(self) -> None:
        """Remove old health history entries."""
        cutoff = datetime.now() - self._history_retention
        self._health_history = [
            h for h in self._health_history
            if h.timestamp > cutoff
        ]

    # ========================================================================
    # Public API
    # ========================================================================

    def get_current_health(self) -> Dict[str, AgentHealthReport]:
        """Get current health status for all agents."""
        return self._agent_health.copy()

    def get_agent_health(self, agent_id: str) -> Optional[AgentHealthReport]:
        """Get health status for a specific agent."""
        return self._agent_health.get(agent_id)

    def get_health_history(
        self,
        hours: int = 24
    ) -> List[SystemHealthReport]:
        """Get health history for the specified time period."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [h for h in self._health_history if h.timestamp > cutoff]

    def get_active_alerts(self) -> List[HealthAlert]:
        """Get all unresolved alerts."""
        return [a for a in self._alerts if not a.resolved]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                return True
        return False

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                return True
        return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get monitor statistics."""
        return {
            "is_running": self._is_running,
            "check_interval": self._check_interval,
            "registered_collectors": list(self._metric_collectors.keys()),
            "total_alerts": len(self._alerts),
            "active_alerts": len([a for a in self._alerts if not a.resolved]),
            "history_entries": len(self._health_history),
        }
