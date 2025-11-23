"""
Agent_11 MARINER - Marine Engine Cross-Reference Module

Marine engines are often marinized automotive engines.
This module reveals the base engine for parts sourcing,
identifying what's shared vs. what's marine-specific.

Covered Manufacturers:
- Mercruiser (GM-based)
- Volvo Penta (GM and Volvo-based)
- OMC/Johnson/Evinrude
- Yamaha Marine
- Honda Marine
- Crusader (Ford-based)
- Indmar (GM-based)
- PCM (GM-based)
"""

from .engine_crossref import (
    MarineEngineCrossReference,
    MarineEngineXref,
    EnginePartCategory,
)

__all__ = [
    "MarineEngineCrossReference",
    "MarineEngineXref",
    "EnginePartCategory",
]
