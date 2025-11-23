"""
Agent_1 (ARCHIVIST) - Normalizers Module
=========================================
"One truth, many names. The Archivist knows them all."

Data normalization utilities for transforming disparate data formats
into the canonical Universal Parts Consciousness format.

Normalizers:
- ThreadNormalizer: Thread specification normalization (ISO/ANSI/DIN/JIS/BSW)
- MaterialNormalizer: Material property normalization across standards
- DimensionNormalizer: Unit conversion and tolerance handling
"""

from .thread_normalizer import (
    ThreadNormalizer,
    NormalizedThread,
    ThreadStandard,
)

from .material_normalizer import (
    MaterialNormalizer,
    NormalizedMaterial,
    MaterialFamily,
    MaterialEquivalent,
    MATERIAL_EQUIVALENTS,
    GRADE_EQUIVALENTS,
)

from .dimension_normalizer import (
    DimensionNormalizer,
    NormalizedDimension,
    Tolerance,
    LengthUnit,
    AngularUnit,
)


__all__ = [
    # Thread normalizer
    "ThreadNormalizer",
    "NormalizedThread",
    "ThreadStandard",
    # Material normalizer
    "MaterialNormalizer",
    "NormalizedMaterial",
    "MaterialFamily",
    "MaterialEquivalent",
    "MATERIAL_EQUIVALENTS",
    "GRADE_EQUIVALENTS",
    # Dimension normalizer
    "DimensionNormalizer",
    "NormalizedDimension",
    "Tolerance",
    "LengthUnit",
    "AngularUnit",
]
