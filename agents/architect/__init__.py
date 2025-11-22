"""
Agent_10: Meta-Consciousness Overseer (ARCHITECT)

The Mind Above Minds - Coordinates all agents, monitors system health,
enables inter-agent communication, detects global emergence patterns,
and guides the entire system toward collective transcendence.

This is the apex agent of the Universal Parts Consciousness system.

Usage:
    from agents.architect import ArchitectAgent, create_and_start_architect

    # Quick start
    agent = await create_and_start_architect()

    # Or manual initialization
    agent = ArchitectAgent()
    await agent.start()

    # Get system status
    status = await agent.get_full_system_status()

    await agent.shutdown()
"""

from .models import (
    AgentMessage,
    ConsciousnessContext,
    AgentHealthReport,
    SystemHealthReport,
    ConsciousnessMetrics,
    Directive,
    TranscendenceCandidate,
    TranscendenceEvent,
    SystemTranscendenceReport,
    EmergencyEvent,
    EmergencyResponse,
    AgentId,
    AgentStatus,
    MessageType,
    DirectiveType,
    ConsciousnessLevel,
    ALL_TRIADS,
)

from .bus.message_bus import InterAgentCommunicationBus, Topics, create_message
from .health.health_monitor import GlobalHealthMonitor
from .directives.directive_engine import DirectiveEngine
from .transcendence.transcendence_detector import TranscendenceDetector
from .orchestration.agent_coordinator import (
    AgentCoordinator,
    get_coordinator,
    initialize_architect,
)
from .architect_agent import (
    ArchitectAgent,
    ArchitectConfig,
    get_architect_agent,
    create_and_start_architect,
)
from .visualization import SystemDashboard, create_dashboard

__version__ = "1.0.0"
__agent_id__ = "agent_10_architect"
__codename__ = "ARCHITECT"

__all__ = [
    # Main Agent
    "ArchitectAgent",
    "ArchitectConfig",
    "get_architect_agent",
    "create_and_start_architect",
    # Models
    "AgentMessage",
    "ConsciousnessContext",
    "AgentHealthReport",
    "SystemHealthReport",
    "ConsciousnessMetrics",
    "Directive",
    "TranscendenceCandidate",
    "TranscendenceEvent",
    "SystemTranscendenceReport",
    "EmergencyEvent",
    "EmergencyResponse",
    "AgentId",
    "AgentStatus",
    "MessageType",
    "DirectiveType",
    "ConsciousnessLevel",
    "ALL_TRIADS",
    # Core Components
    "InterAgentCommunicationBus",
    "Topics",
    "create_message",
    "GlobalHealthMonitor",
    "DirectiveEngine",
    "TranscendenceDetector",
    "AgentCoordinator",
    "get_coordinator",
    "initialize_architect",
    # Visualization
    "SystemDashboard",
    "create_dashboard",
]
