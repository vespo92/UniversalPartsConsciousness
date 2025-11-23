"""
Agent_18: ALCHEMIST - Materials Science Intelligence

The foundation of all parts compatibility decisions.
What material? Will it corrode? Will it fail? What's the best choice?

Domains:
- Metals & alloys (steel, aluminum, titanium, copper, exotic)
- Polymers & plastics (engineering plastics, elastomers)
- Composites (carbon fiber, fiberglass, Kevlar)
- Ceramics & advanced materials
- Coatings & surface treatments
"""

from .alchemist_agent import (
    AlchemistAgent,
    MaterialFamily,
    CorrosionResistance,
    MaterialProperties,
    GalvanicPair,
    MaterialRecommendation,
    AlloyCrossReference,
    MaterialCompatibility,
)

__all__ = [
    "AlchemistAgent",
    "MaterialFamily",
    "CorrosionResistance",
    "MaterialProperties",
    "GalvanicPair",
    "MaterialRecommendation",
    "AlloyCrossReference",
    "MaterialCompatibility",
]

__version__ = "0.1.0"
__agent_id__ = "Agent_18"
__codename__ = "ALCHEMIST"
