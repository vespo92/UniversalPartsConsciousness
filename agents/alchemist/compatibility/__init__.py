"""
Material Compatibility Module

Provides galvanic compatibility analysis, thermal expansion
matching, and general material pairing recommendations.
"""

from .galvanic import GalvanicSeries, GalvanicCalculator, CorrosionRisk
from .thermal import ThermalExpansionChecker, ThermalMismatch

__all__ = [
    "GalvanicSeries",
    "GalvanicCalculator",
    "CorrosionRisk",
    "ThermalExpansionChecker",
    "ThermalMismatch",
]
