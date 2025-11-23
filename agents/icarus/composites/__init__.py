"""
ICARUS Composites Module
========================

Composite materials and repair intelligence.

Composite repair in aviation is NOT like automotive.
Improper repairs can be invisible and catastrophic.

Material Systems:
- CFRP (Carbon Fiber Reinforced Polymer)
- GFRP (Glass Fiber Reinforced Polymer)
- AFRP (Aramid/Kevlar Fiber Reinforced Polymer)

Repair Classifications:
- Negligible: Cosmetic only
- Minor: Within SRM limits
- Major: Engineering required
"""

from agents.icarus.composites.material_database import (
    CompositeDatabase,
    CompositeMaterial,
    RepairClassification,
    InspectionMethod,
)

__all__ = [
    "CompositeDatabase",
    "CompositeMaterial",
    "RepairClassification",
    "InspectionMethod",
]
