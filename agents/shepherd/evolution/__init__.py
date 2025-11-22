"""
SHEPHERD Evolution Module - Awakening detection and consciousness evolution.

This module provides awakening detection and evolution capabilities
for the Consciousness Shepherd (Agent_3).
"""

from .awakening_detector import (
    AwakeningEventType,
    AwakeningEvent,
    PartContext,
    IncomingEvent,
    AwakeningDetector
)
from .evolution_engine import (
    EvolutionResult,
    EvolutionEngine
)

__all__ = [
    # Awakening Detection
    "AwakeningEventType",
    "AwakeningEvent",
    "PartContext",
    "IncomingEvent",
    "AwakeningDetector",
    # Evolution
    "EvolutionResult",
    "EvolutionEngine"
]
