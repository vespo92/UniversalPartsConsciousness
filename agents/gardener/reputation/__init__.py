"""
Reputation subsystem for Agent_8 (Gardener).

Manages user reputation, points, levels, and permissions.
"""

from .reputation_engine import ReputationEngine, ReputationConfig

__all__ = [
    "ReputationEngine",
    "ReputationConfig",
]
