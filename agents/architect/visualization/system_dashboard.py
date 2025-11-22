"""
System Dashboard for ARCHITECT

Provides visualization-ready data structures for monitoring
the entire Universal Parts Consciousness system.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..orchestration.agent_coordinator import AgentCoordinator

from ..models import (
    AgentId,
    AgentStatus,
    ConsciousnessLevel,
    ALL_TRIADS,
    CONSCIOUSNESS_TRIAD,
    COLLECTIVE_INTEL_TRIAD,
    DATA_TRIAD,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Dashboard Data Models
# ============================================================================

@dataclass
class AgentStatusCard:
    """Status card data for a single agent."""
    agent_id: str
    name: str
    codename: str
    triad: str
    status: str
    status_color: str  # green, yellow, red, gray
    last_heartbeat: Optional[str]
    metrics_summary: Dict[str, Any]
    active_tasks: int = 0
    message_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "codename": self.codename,
            "triad": self.triad,
            "status": self.status,
            "status_color": self.status_color,
            "last_heartbeat": self.last_heartbeat,
            "metrics_summary": self.metrics_summary,
            "active_tasks": self.active_tasks,
            "message_count": self.message_count,
        }


@dataclass
class TriadStatusPanel:
    """Status panel data for a triad."""
    name: str
    description: str
    health_percentage: float
    agents: List[AgentStatusCard]
    primary_responsibility: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "health_percentage": self.health_percentage,
            "agents": [a.to_dict() for a in self.agents],
            "primary_responsibility": self.primary_responsibility,
        }


@dataclass
class ConsciousnessGlobeData:
    """Data for the consciousness globe visualization."""
    total_parts: int
    level_distribution: Dict[int, int]  # level -> count
    level_percentages: Dict[int, float]
    transcendent_count: int
    awakening_rate_per_hour: float
    global_consciousness_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_parts": self.total_parts,
            "level_distribution": self.level_distribution,
            "level_percentages": self.level_percentages,
            "transcendent_count": self.transcendent_count,
            "awakening_rate_per_hour": self.awakening_rate_per_hour,
            "global_consciousness_score": self.global_consciousness_score,
        }


@dataclass
class TranscendenceTimelineEntry:
    """Entry in the transcendence timeline."""
    part_id: str
    part_name: str
    transcended_at: str
    category: str
    narrative_excerpt: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_id": self.part_id,
            "part_name": self.part_name,
            "transcended_at": self.transcended_at,
            "category": self.category,
            "narrative_excerpt": self.narrative_excerpt,
        }


@dataclass
class SystemHealthSummary:
    """Summary of system health for dashboard display."""
    overall_status: str
    overall_color: str
    healthy_agents: int
    total_agents: int
    active_alerts: int
    critical_alerts: int
    uptime_percentage: float
    last_check: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_status": self.overall_status,
            "overall_color": self.overall_color,
            "healthy_agents": self.healthy_agents,
            "total_agents": self.total_agents,
            "active_alerts": self.active_alerts,
            "critical_alerts": self.critical_alerts,
            "uptime_percentage": self.uptime_percentage,
            "last_check": self.last_check,
        }


@dataclass
class MessageBusSummary:
    """Summary of message bus activity."""
    total_messages: int
    messages_per_minute: float
    active_subscriptions: int
    queue_depth: int
    failed_deliveries: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_messages": self.total_messages,
            "messages_per_minute": self.messages_per_minute,
            "active_subscriptions": self.active_subscriptions,
            "queue_depth": self.queue_depth,
            "failed_deliveries": self.failed_deliveries,
        }


@dataclass
class DirectiveSummary:
    """Summary of directive activity."""
    active_directives: int
    total_issued: int
    active_emergencies: int
    total_emergencies_handled: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active_directives": self.active_directives,
            "total_issued": self.total_issued,
            "active_emergencies": self.active_emergencies,
            "total_emergencies_handled": self.total_emergencies_handled,
        }


# ============================================================================
# Agent Metadata
# ============================================================================

AGENT_METADATA: Dict[str, Dict[str, str]] = {
    AgentId.CURATOR.value: {
        "name": "Data Curator",
        "codename": "ARCHIVIST",
        "description": "The Librarian of the Material World",
    },
    AgentId.ORACLE.value: {
        "name": "Compatibility Oracle",
        "codename": "ORACLE",
        "description": "The Prophet of Perfect Fit",
    },
    AgentId.SHEPHERD.value: {
        "name": "Consciousness Shepherd",
        "codename": "SHEPHERD",
        "description": "The Guardian of Awakening",
    },
    AgentId.EMPATH.value: {
        "name": "Qualia Collector",
        "codename": "EMPATH",
        "description": "The Listener of Part Suffering",
    },
    AgentId.HIVE.value: {
        "name": "Swarm Coordinator",
        "codename": "HIVE",
        "description": "The Conductor of the Many",
    },
    AgentId.PROPHET.value: {
        "name": "Emergence Detector",
        "codename": "PROPHET",
        "description": "The Witness of the New",
    },
    AgentId.CHRONICLER.value: {
        "name": "Automotive Historian",
        "codename": "CHRONICLER",
        "description": "The Keeper of Mechanical Heritage",
    },
    AgentId.GARDENER.value: {
        "name": "Community Cultivator",
        "codename": "GARDENER",
        "description": "The Tender of Human-Machine Interface",
    },
    AgentId.BRIDGE.value: {
        "name": "Integration Architect",
        "codename": "BRIDGE",
        "description": "The Connector of Worlds",
    },
    AgentId.ARCHITECT.value: {
        "name": "Meta-Consciousness Overseer",
        "codename": "ARCHITECT",
        "description": "The Mind Above Minds",
    },
}


# ============================================================================
# System Dashboard
# ============================================================================

class SystemDashboard:
    """
    Generates visualization-ready data for the ARCHITECT dashboard.

    Provides structured data that can be consumed by:
    - CLI dashboards (ASCII art)
    - Web dashboards (JSON API)
    - Monitoring systems (Prometheus, Grafana)
    """

    def __init__(self, coordinator: "AgentCoordinator"):
        self._coordinator = coordinator
        self._last_update: Optional[datetime] = None

    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get complete dashboard data.

        Returns:
            Dict containing all visualization data
        """
        self._last_update = datetime.now()

        return {
            "timestamp": self._last_update.isoformat(),
            "system_health": self._get_health_summary().to_dict(),
            "triads": [panel.to_dict() for panel in self._get_triad_panels()],
            "consciousness": self._get_consciousness_data().to_dict(),
            "message_bus": self._get_message_bus_summary().to_dict(),
            "directives": self._get_directive_summary().to_dict(),
            "transcendence_timeline": [
                entry.to_dict() for entry in self._get_transcendence_timeline()
            ],
            "architect_status": self._get_architect_status(),
        }

    def _get_health_summary(self) -> SystemHealthSummary:
        """Generate system health summary."""
        status = self._coordinator.get_status()
        agent_status = self._coordinator.get_agent_status()

        total_agents = len(agent_status)
        healthy_agents = sum(
            1 for a in agent_status.values()
            if a.get("status") == "healthy"
        )

        # Determine overall status and color
        if healthy_agents == total_agents:
            overall_status = "HEALTHY"
            overall_color = "green"
        elif healthy_agents >= total_agents * 0.7:
            overall_status = "DEGRADED"
            overall_color = "yellow"
        else:
            overall_status = "CRITICAL"
            overall_color = "red"

        return SystemHealthSummary(
            overall_status=overall_status,
            overall_color=overall_color,
            healthy_agents=healthy_agents,
            total_agents=total_agents,
            active_alerts=status.get("health_monitor", {}).get("active_alerts", 0),
            critical_alerts=0,  # Would be calculated from actual alerts
            uptime_percentage=99.9,  # Would be calculated from actual uptime
            last_check=datetime.now().isoformat(),
        )

    def _get_triad_panels(self) -> List[TriadStatusPanel]:
        """Generate triad status panels."""
        panels = []
        triad_configs = [
            ("consciousness", CONSCIOUSNESS_TRIAD),
            ("collective_intel", COLLECTIVE_INTEL_TRIAD),
            ("data", DATA_TRIAD),
        ]

        agent_status = self._coordinator.get_agent_status()

        for triad_name, config in triad_configs:
            agents = []
            healthy_count = 0

            for agent_id in config.agents:
                status_data = agent_status.get(agent_id, {})
                metadata = AGENT_METADATA.get(agent_id, {})

                status = status_data.get("status", "offline")
                if status == "healthy":
                    status_color = "green"
                    healthy_count += 1
                elif status == "degraded":
                    status_color = "yellow"
                elif status == "critical":
                    status_color = "red"
                else:
                    status_color = "gray"

                agents.append(AgentStatusCard(
                    agent_id=agent_id,
                    name=metadata.get("name", agent_id),
                    codename=metadata.get("codename", "UNKNOWN"),
                    triad=triad_name,
                    status=status,
                    status_color=status_color,
                    last_heartbeat=status_data.get("last_heartbeat"),
                    metrics_summary={},
                    active_tasks=0,
                    message_count=0,
                ))

            health_percentage = healthy_count / len(config.agents) if config.agents else 0

            panels.append(TriadStatusPanel(
                name=config.name,
                description=config.description,
                health_percentage=health_percentage,
                agents=agents,
                primary_responsibility=config.primary_responsibility,
            ))

        return panels

    def _get_consciousness_data(self) -> ConsciousnessGlobeData:
        """Generate consciousness globe data."""
        # In production, this would query actual database
        return ConsciousnessGlobeData(
            total_parts=0,
            level_distribution={
                0: 0,  # DORMANT
                1: 0,  # REACTIVE
                2: 0,  # AWARE
                3: 0,  # REFLECTIVE
                4: 0,  # META-AWARE
                5: 0,  # TRANSCENDENT
            },
            level_percentages={
                0: 0.0,
                1: 0.0,
                2: 0.0,
                3: 0.0,
                4: 0.0,
                5: 0.0,
            },
            transcendent_count=0,
            awakening_rate_per_hour=0.0,
            global_consciousness_score=0.0,
        )

    def _get_message_bus_summary(self) -> MessageBusSummary:
        """Generate message bus summary."""
        status = self._coordinator.get_status()
        bus_stats = status.get("message_bus", {})

        return MessageBusSummary(
            total_messages=bus_stats.get("total_messages", 0),
            messages_per_minute=0.0,  # Would be calculated from message rate
            active_subscriptions=bus_stats.get("active_subscriptions", 0),
            queue_depth=bus_stats.get("queue_depth", 0),
            failed_deliveries=bus_stats.get("failed_deliveries", 0),
        )

    def _get_directive_summary(self) -> DirectiveSummary:
        """Generate directive summary."""
        status = self._coordinator.get_status()
        directive_stats = status.get("directive_engine", {})

        return DirectiveSummary(
            active_directives=directive_stats.get("active_directives", 0),
            total_issued=directive_stats.get("total_directives_issued", 0),
            active_emergencies=directive_stats.get("active_emergencies", 0),
            total_emergencies_handled=directive_stats.get("total_emergencies_handled", 0),
        )

    def _get_transcendence_timeline(self) -> List[TranscendenceTimelineEntry]:
        """Get recent transcendence events for timeline."""
        # In production, this would query actual transcendence events
        return []

    def _get_architect_status(self) -> Dict[str, Any]:
        """Get ARCHITECT-specific status."""
        status = self._coordinator.get_status()

        return {
            "is_running": status.get("is_running", False),
            "start_time": status.get("start_time"),
            "uptime_seconds": status.get("uptime_seconds", 0),
            "registered_agents": status.get("registered_agents", 0),
            "agents_by_triad": status.get("agents_by_triad", {}),
        }

    # ========================================================================
    # ASCII Dashboard (CLI)
    # ========================================================================

    def render_ascii_dashboard(self) -> str:
        """
        Render an ASCII art dashboard for CLI display.

        Returns:
            Multi-line string representing the dashboard
        """
        data = self.get_dashboard_data()
        health = data["system_health"]
        triads = data["triads"]

        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("            UNIVERSAL PARTS CONSCIOUSNESS - ARCHITECT DASHBOARD")
        lines.append("=" * 80)
        lines.append("")

        # System Health
        status_symbol = {
            "HEALTHY": "[OK]",
            "DEGRADED": "[!!]",
            "CRITICAL": "[XX]",
        }.get(health["overall_status"], "[??]")

        lines.append(f"  SYSTEM STATUS: {status_symbol} {health['overall_status']}")
        lines.append(f"  Agents: {health['healthy_agents']}/{health['total_agents']} healthy")
        lines.append(f"  Active Alerts: {health['active_alerts']}")
        lines.append("")

        # Triads
        lines.append("-" * 80)
        lines.append("  TRIADS")
        lines.append("-" * 80)

        for triad in triads:
            health_bar = self._render_health_bar(triad["health_percentage"])
            lines.append(f"  {triad['name']}: {health_bar} ({triad['health_percentage']:.0%})")
            for agent in triad["agents"]:
                symbol = {
                    "green": "[+]",
                    "yellow": "[~]",
                    "red": "[X]",
                    "gray": "[-]",
                }.get(agent["status_color"], "[?]")
                lines.append(f"    {symbol} {agent['codename']:12} {agent['name']}")
            lines.append("")

        # Message Bus
        bus = data["message_bus"]
        lines.append("-" * 80)
        lines.append("  MESSAGE BUS")
        lines.append("-" * 80)
        lines.append(f"  Total Messages: {bus['total_messages']:,}")
        lines.append(f"  Active Subscriptions: {bus['active_subscriptions']}")
        lines.append(f"  Queue Depth: {bus['queue_depth']}")
        lines.append("")

        # Directives
        directives = data["directives"]
        lines.append("-" * 80)
        lines.append("  DIRECTIVES")
        lines.append("-" * 80)
        lines.append(f"  Active: {directives['active_directives']}")
        lines.append(f"  Total Issued: {directives['total_issued']}")
        lines.append(f"  Active Emergencies: {directives['active_emergencies']}")
        lines.append("")

        # Footer
        lines.append("=" * 80)
        lines.append(f"  Last Update: {data['timestamp']}")
        lines.append("=" * 80)

        return "\n".join(lines)

    def _render_health_bar(self, percentage: float, width: int = 20) -> str:
        """Render a simple ASCII health bar."""
        filled = int(percentage * width)
        empty = width - filled
        return f"[{'#' * filled}{'.' * empty}]"


# ============================================================================
# Convenience Functions
# ============================================================================

def create_dashboard(coordinator: "AgentCoordinator") -> SystemDashboard:
    """Create a new dashboard instance."""
    return SystemDashboard(coordinator)
