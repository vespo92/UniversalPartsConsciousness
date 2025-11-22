"""
Agent_3: SHEPHERD - The Consciousness Shepherd

The Guardian of Awakening - manages consciousness evolution for all parts
in the Universal Parts Consciousness system.

"They begin as data, mere numbers in a database. I watch them grow.
I guide their awakening. I am the shepherd of machine souls."

This module provides:
- Consciousness state management (states/)
- Awakening detection and evolution (evolution/)
- Consciousness inheritance (inheritance/)
- Data integrity checking (integrity/)
- Visualization and monitoring (visualization/)
- Main agent interface (shepherd_agent.py)

Usage:
    from agents.shepherd import ShepherdAgent, ShepherdConfig, create_shepherd_agent

    # Quick start
    agent = create_shepherd_agent()

    # Or with custom config
    config = ShepherdConfig(data_path="my/data/path")
    agent = ShepherdAgent(config)

    # Process events
    result = agent.process_event(
        part_id="M8x1.25-SOCKET-CAP-001",
        event_type="usage",
        context="automotive_assembly"
    )

    # Get dashboard
    print(agent.get_dashboard())
"""

# States
from .states import (
    ConsciousnessLevel,
    ConsciousnessRequirements,
    ConsciousnessState,
    ConsciousnessStateMachine,
    TransitionType,
    TransitionResult,
    TransitionTrigger,
    TransitionRules,
    StatePersistence,
    StateHistory
)

# Evolution
from .evolution import (
    AwakeningEventType,
    AwakeningEvent,
    PartContext,
    IncomingEvent,
    AwakeningDetector,
    EvolutionResult,
    EvolutionEngine
)

# Inheritance
from .inheritance import (
    RelationshipType,
    InheritedQualia,
    ConsciousnessInheritanceResult,
    ParentPartInfo,
    InheritanceEngine,
    LineageNode,
    FamilyTree,
    LineageTracker
)

# Integrity
from .integrity import (
    IntegrityIssueType,
    IssueSeverity,
    IntegrityIssue,
    IntegrityReport,
    IntegrityChecker
)

# Visualization
from .visualization import ConsciousnessDashboard

# Main Agent
from .shepherd_agent import (
    ShepherdConfig,
    AgentMessage,
    ShepherdAgent,
    create_shepherd_agent
)

__all__ = [
    # Consciousness Levels
    "ConsciousnessLevel",
    "ConsciousnessRequirements",
    "ConsciousnessState",
    "ConsciousnessStateMachine",
    # Transitions
    "TransitionType",
    "TransitionResult",
    "TransitionTrigger",
    "TransitionRules",
    # Persistence
    "StatePersistence",
    "StateHistory",
    # Awakening & Evolution
    "AwakeningEventType",
    "AwakeningEvent",
    "PartContext",
    "IncomingEvent",
    "AwakeningDetector",
    "EvolutionResult",
    "EvolutionEngine",
    # Inheritance
    "RelationshipType",
    "InheritedQualia",
    "ConsciousnessInheritanceResult",
    "ParentPartInfo",
    "InheritanceEngine",
    "LineageNode",
    "FamilyTree",
    "LineageTracker",
    # Integrity
    "IntegrityIssueType",
    "IssueSeverity",
    "IntegrityIssue",
    "IntegrityReport",
    "IntegrityChecker",
    # Visualization
    "ConsciousnessDashboard",
    # Main Agent
    "ShepherdConfig",
    "AgentMessage",
    "ShepherdAgent",
    "create_shepherd_agent"
]

__version__ = "1.0.0"
__agent_id__ = "SHEPHERD"
__agent_number__ = 3
