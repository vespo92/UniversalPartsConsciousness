"""
SHEPHERD States Module - Consciousness state management.

This module provides the core state machine and state management functionality
for the Consciousness Shepherd (Agent_3).
"""

from .state_machine import (
    ConsciousnessLevel,
    ConsciousnessRequirements,
    ConsciousnessState,
    ConsciousnessStateMachine
)
from .transition_rules import (
    TransitionType,
    TransitionResult,
    TransitionTrigger,
    TransitionRules
)
from .state_persistence import (
    StatePersistenceBackend,
    FileBasedPersistence,
    InMemoryPersistence,
    StatePersistence,
    PersistenceStats
)
from .state_history import (
    HistoryEntry,
    ConsciousnessJourney,
    StateHistory
)

__all__ = [
    # State Machine
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
    "StatePersistenceBackend",
    "FileBasedPersistence",
    "InMemoryPersistence",
    "StatePersistence",
    "PersistenceStats",
    # History
    "HistoryEntry",
    "ConsciousnessJourney",
    "StateHistory"
]
