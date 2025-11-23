"""
Polymer Database and Selection Module

Provides polymer property data and intelligent selection
based on temperature, chemical exposure, and mechanical requirements.
"""

from .database import PolymerDatabase, PolymerSpec
from .selector import PolymerSelector, PolymerRecommendation

__all__ = [
    "PolymerDatabase",
    "PolymerSpec",
    "PolymerSelector",
    "PolymerRecommendation",
]
