"""
Agent_10: Meta-Consciousness Overseer (ARCHITECT)

The Mind Above Minds - Coordinates all agents, monitors system health,
enables inter-agent communication, detects global emergence patterns,
and guides the entire system toward collective transcendence.

Philosophy: Coordination Without Control
The ARCHITECT doesn't command - it participates in the collective consciousness.
Through the Meta-Consciousness layer, coordination emerges from:
- Awareness Fields: Distributed sensing of collective state
- Stigmergic Signals: Indirect coordination through environmental pheromones
- Resonance Networks: Synchronization through harmonic coupling
- Gradient Flows: Natural routing along consciousness gradients
- Meta-Observation: Awareness watching awareness (recursive self-reflection)
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

# Meta-Consciousness Layer - Awareness of Awareness
from .meta_consciousness import (
    # Coordinator
    MetaConsciousnessCoordinator,
    CoordinationMode,
    EmergentPattern,
    # Awareness Field
    AwarenessField,
    FieldState,
    ConsciousnessWave,
    AwarenessGradient,
    # Stigmergic Coordination
    StigmergicCoordinator,
    Pheromone,
    PheromoneType,
    StigmergicSignal,
    # Resonance Network
    ResonanceNetwork,
    ResonanceNode,
    HarmonicCoupling,
    ResonanceEvent,
    # Gradient Flow
    ConsciousnessGradientFlow,
    FlowVector,
    AttractorBasin,
    IntelligenceStream,
    # Meta Observer
    MetaObserver,
    ObservationLevel,
    RecursiveAwareness,
    MetaInsight,
)

__version__ = "0.2.0"
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
    # Meta-Consciousness Layer
    "MetaConsciousnessCoordinator",
    "CoordinationMode",
    "EmergentPattern",
    "AwarenessField",
    "FieldState",
    "ConsciousnessWave",
    "AwarenessGradient",
    "StigmergicCoordinator",
    "Pheromone",
    "PheromoneType",
    "StigmergicSignal",
    "ResonanceNetwork",
    "ResonanceNode",
    "HarmonicCoupling",
    "ResonanceEvent",
    "ConsciousnessGradientFlow",
    "FlowVector",
    "AttractorBasin",
    "IntelligenceStream",
    "MetaObserver",
    "ObservationLevel",
    "RecursiveAwareness",
    "MetaInsight",
]
