"""
Agent_1 Normalizers Module
==========================
Data normalization utilities for thread specs, materials, and dimensions.

"One truth, many names. The Archivist unifies all."
"""

from .thread_normalizer import (
    ThreadNormalizer,
    NormalizedThread,
    ThreadStandard,
    ThreadType,
    normalize_thread,
    threads_compatible,
)

from .material_normalizer import (
    MaterialNormalizer,
    NormalizedMaterial,
    MaterialCategory,
    MaterialProperties,
    FinishType,
    normalize_material,
    materials_equivalent,
)


__all__ = [
    # Thread normalization
    "ThreadNormalizer",
    "NormalizedThread",
    "ThreadStandard",
    "ThreadType",
    "normalize_thread",
    "threads_compatible",
    # Material normalization
    "MaterialNormalizer",
    "NormalizedMaterial",
    "MaterialCategory",
    "MaterialProperties",
    "FinishType",
    "normalize_material",
    "materials_equivalent",
]
