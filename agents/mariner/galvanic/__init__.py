"""
Agent_11 MARINER - Galvanic Corrosion Module

THE core marine specialty. Galvanic corrosion destroys more
marine hardware than any other failure mode.

This module provides:
- Galvanic series database (ASTM G82 compliant)
- Corrosion risk calculator
- Material compatibility matrix
- Isolation recommendations
"""

from .corrosion_calculator import (
    GalvanicCorrosionCalculator,
    GalvanicRisk,
    GalvanicPair,
)
from .material_series import (
    MarineMaterial,
    GalvanicSeries,
    MarineEnvironment,
)

__all__ = [
    "GalvanicCorrosionCalculator",
    "GalvanicRisk",
    "GalvanicPair",
    "MarineMaterial",
    "GalvanicSeries",
    "MarineEnvironment",
]
