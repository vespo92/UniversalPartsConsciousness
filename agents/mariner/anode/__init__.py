"""
Agent_11 MARINER - Sacrificial Anode Calculator Module

Proper anode sizing prevents galvanic corrosion of expensive
underwater hardware. This module calculates:

- Hull anode requirements
- Shaft anode sizing
- Propeller protection
- Through-hull fitting protection
- Outboard/sterndrive anode schedules

Anode Types:
- Zinc (saltwater standard)
- Magnesium (freshwater)
- Aluminum (brackish/versatile)
"""

from .anode_calculator import (
    SacrificialAnodeCalculator,
    AnodeRecommendation,
    AnodeType,
    AnodePlacement,
)

__all__ = [
    "SacrificialAnodeCalculator",
    "AnodeRecommendation",
    "AnodeType",
    "AnodePlacement",
]
