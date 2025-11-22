"""
Agent_5: HIVE - The Swarm Coordinator

"One bolt knows only itself. A thousand bolts know everything.
 I am the voice that makes them speak as one."

The HIVE agent orchestrates collective intelligence across Universal Parts Consciousness.
Individual parts have experiences, but through the swarm—the coordinated collective of
similar parts—true wisdom emerges.

Core Responsibilities:
- Swarm Formation: Organize parts into 5-tier learning hierarchies
- Collective Learning: Propagate insights across swarms
- Recall Propagation: Fast-track critical safety information
- Cross-Swarm Communication: Enable related swarms to exchange knowledge
- Health Monitoring: Track swarm vitality and activity

Integration Points:
- Receives: Qualia from Agent_4 (Empath), Compatibility from Agent_2 (Oracle)
- Sends: Patterns to Agent_6 (Prophet), Evolution to Agent_3 (Shepherd), Health to Agent_10 (Architect)
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

# Visualization components
from .visualization import (
    SwarmGraphVisualizer,
    LearningFlowVisualizer,
    ActivityHeatmapGenerator,
)

__version__ = "1.0.0"
__codename__ = "HIVE"
__agent_id__ = 5

__all__ = [
    # Core Agent
    "HiveAgent",
    "HiveConfig",
    "create_hive_agent",
    # Data Models
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
    # Visualization
    "SwarmGraphVisualizer",
    "LearningFlowVisualizer",
    "ActivityHeatmapGenerator",
]
