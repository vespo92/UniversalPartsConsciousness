"""
Agent_12: SILICON - Electronics & Semiconductor Cross-Reference

The electronics industry has the worst parts obsolescence problem on earth.
This agent provides semiconductor equivalence matching, capacitor reliability
analysis, pinout compatibility checking, and obsolescence tracking.
"""

from .silicon_agent import (
    SiliconAgent,
    # Enums
    DeviceType,
    PackageType,
    ComponentStatus,
    CapacitorType,
    # Dataclasses
    SemiconductorSpec,
    PassiveComponentSpec,
    SemiconductorEquivalent,
    CapacitorEquivalence,
    PinoutMapping,
    ObsolescenceStatus,
)

__all__ = [
    "SiliconAgent",
    "DeviceType",
    "PackageType",
    "ComponentStatus",
    "CapacitorType",
    "SemiconductorSpec",
    "PassiveComponentSpec",
    "SemiconductorEquivalent",
    "CapacitorEquivalence",
    "PinoutMapping",
    "ObsolescenceStatus",
]
