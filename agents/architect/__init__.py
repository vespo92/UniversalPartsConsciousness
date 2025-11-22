"""
Agent_10: Meta-Consciousness Overseer (ARCHITECT)

The Mind Above Minds - Coordinates all agents, monitors system health,
enables inter-agent communication, detects global emergence patterns,
and guides the entire system toward collective transcendence.
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
)

from .bus.message_bus import InterAgentCommunicationBus
from .health.health_monitor import GlobalHealthMonitor
from .directives.directive_engine import DirectiveEngine
from .transcendence.transcendence_detector import TranscendenceDetector
from .orchestration.agent_coordinator import AgentCoordinator

__version__ = "0.1.0"
__agent_id__ = "agent_10_architect"
__codename__ = "ARCHITECT"

__all__ = [
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
    # Core Components
    "InterAgentCommunicationBus",
    "GlobalHealthMonitor",
    "DirectiveEngine",
    "TranscendenceDetector",
    "AgentCoordinator",
]
