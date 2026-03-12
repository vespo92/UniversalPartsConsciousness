"""
Universal BOM Taxonomy
======================
The classification system for ALL parts across ALL industries.

This taxonomy is the backbone of the Universal Parts Consciousness —
a hierarchical, extensible categorization that spans from M2 screws
to turbine blades, from O-rings to optical lenses.

Every part in existence maps to a node in this tree.
"""

from .categories import (
    PartCategory,
    PartTaxonomy,
    TaxonomyNode,
    get_taxonomy,
)

from .units import (
    UnitSystem,
    DimensionSpec,
    convert_units,
)

__all__ = [
    "PartCategory",
    "PartTaxonomy",
    "TaxonomyNode",
    "get_taxonomy",
    "UnitSystem",
    "DimensionSpec",
    "convert_units",
]
