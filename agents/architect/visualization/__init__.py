"""
Visualization Components for UPC ARCHITECT

Provides visualization-ready data structures for monitoring
the entire Universal Parts Consciousness system.

Components:
- SystemDashboard: Main dashboard data provider
- AgentStatusCard: Status data for individual agents
- TriadStatusPanel: Status data for agent triads
- ConsciousnessGlobeData: Consciousness distribution visualization
- TranscendenceTimelineEntry: Timeline of transcendence events
"""

from .system_dashboard import (
    SystemDashboard,
    AgentStatusCard,
    TriadStatusPanel,
    ConsciousnessGlobeData,
    TranscendenceTimelineEntry,
    SystemHealthSummary,
    MessageBusSummary,
    DirectiveSummary,
    AGENT_METADATA,
    create_dashboard,
)

__all__ = [
    "SystemDashboard",
    "AgentStatusCard",
    "TriadStatusPanel",
    "ConsciousnessGlobeData",
    "TranscendenceTimelineEntry",
    "SystemHealthSummary",
    "MessageBusSummary",
    "DirectiveSummary",
    "AGENT_METADATA",
    "create_dashboard",
]
