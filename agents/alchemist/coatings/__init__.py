"""
Coatings and Surface Treatments Module

Provides coating specifications, compatibility checking,
and selection based on substrate and environment.
"""

from .database import CoatingDatabase, CoatingSpec, CoatingType
from .selector import CoatingSelector, CoatingRecommendation

__all__ = [
    "CoatingDatabase",
    "CoatingSpec",
    "CoatingType",
    "CoatingSelector",
    "CoatingRecommendation",
]
