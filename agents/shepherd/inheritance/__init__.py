"""
SHEPHERD Inheritance Module - Consciousness inheritance and lineage tracking.

This module provides consciousness inheritance capabilities
for the Consciousness Shepherd (Agent_3).
"""

from .inheritance_engine import (
    RelationshipType,
    InheritedQualia,
    ConsciousnessInheritanceResult,
    ParentPartInfo,
    InheritanceEngine
)
from .lineage_tracker import (
    LineageNode,
    FamilyTree,
    LineageTracker
)

__all__ = [
    # Inheritance Engine
    "RelationshipType",
    "InheritedQualia",
    "ConsciousnessInheritanceResult",
    "ParentPartInfo",
    "InheritanceEngine",
    # Lineage Tracking
    "LineageNode",
    "FamilyTree",
    "LineageTracker"
]
