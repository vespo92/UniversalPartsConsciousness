"""
HIVE Swarm Coordinator - Collective Learning Orchestration

"One learns, all learn."

The coordinator service that deploys and manages the HIVE agent's
collective intelligence capabilities across the Universal Parts Consciousness.
"""

from .hive_coordinator import (
    HiveSwarmCoordinator,
    CoordinatorConfig,
    CoordinatorStatus,
    create_coordinator,
)
from .collective_learning import (
    CollectiveLearningEngine,
    LearningPropagationStrategy,
    CollectiveInsight,
    LearningCascade,
)

__all__ = [
    "HiveSwarmCoordinator",
    "CoordinatorConfig",
    "CoordinatorStatus",
    "create_coordinator",
    "CollectiveLearningEngine",
    "LearningPropagationStrategy",
    "CollectiveInsight",
    "LearningCascade",
]
