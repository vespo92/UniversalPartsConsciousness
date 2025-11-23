"""
Alloy Database and Cross-Reference Module

Provides comprehensive alloy data and cross-referencing
across international standards (AA, AISI, ASTM, EN, DIN, JIS, GB).
"""

from .database import AlloyDatabase, AlloySpec
from .cross_reference import CrossReferenceEngine, StandardsMapping

__all__ = [
    "AlloyDatabase",
    "AlloySpec",
    "CrossReferenceEngine",
    "StandardsMapping",
]
