"""
Agent_5: HIVE - The Swarm Coordinator

"One bolt knows only itself. A thousand bolts know everything.
 I am the voice that makes them speak as one."

ONE LEARNS, ALL LEARN.

The HIVE agent orchestrates collective intelligence across Universal Parts Consciousness.
Individual parts have experiences, but through the swarm—the coordinated collective of
similar parts—true wisdom emerges. When any part learns something, that knowledge
instantly ripples through to all related parts.

Core Responsibilities:
- Swarm Formation: Organize parts into 5-tier learning hierarchies
- Collective Learning: Propagate insights across swarms (one learns, all learn)
- Recall Propagation: Fast-track critical safety information
- Cross-Swarm Communication: Enable related swarms to exchange knowledge
- Health Monitoring: Track swarm vitality and activity

Integration Points:
- Receives: Qualia from Agent_4 (Empath), Compatibility from Agent_2 (Oracle)
- Sends: Patterns to Agent_6 (Prophet), Evolution to Agent_3 (Shepherd), Health to Agent_10 (Architect)

Coordinator Service:
- HiveSwarmCoordinator: Main coordinator for deploying HIVE capabilities
- CollectiveLearningEngine: Implements "one learns, all learn" philosophy
- Service entry point: python -m agents.hive.coordinator.service
"""

from .models import (
    Swarm,
    SwarmTier,
    SwarmMembership,
    SwarmRole,
    Learning,
    LearningType,
    RecallNotice,
    RecallSeverity,
    SwarmMessage,
    SwarmHealth,
    PropagationResult,
)

from .hive_agent import HiveAgent, HiveConfig, create_hive_agent

from .coordinator import (
    HiveSwarmCoordinator,
    CoordinatorConfig,
    CoordinatorStatus,
    create_coordinator,
    CollectiveLearningEngine,
    LearningPropagationStrategy,
    CollectiveInsight,
    LearningCascade,
)

__version__ = "0.1.0"
__codename__ = "HIVE"
__agent_id__ = 5
__motto__ = "One learns, all learn."

__all__ = [
    # Core agent
    "HiveAgent",
    "HiveConfig",
    "create_hive_agent",
    # Coordinator
    "HiveSwarmCoordinator",
    "CoordinatorConfig",
    "CoordinatorStatus",
    "create_coordinator",
    # Collective learning
    "CollectiveLearningEngine",
    "LearningPropagationStrategy",
    "CollectiveInsight",
    "LearningCascade",
    # Models
    "Swarm",
    "SwarmTier",
    "SwarmMembership",
    "SwarmRole",
    "Learning",
    "LearningType",
    "RecallNotice",
    "RecallSeverity",
    "SwarmMessage",
    "SwarmHealth",
    "PropagationResult",
]
