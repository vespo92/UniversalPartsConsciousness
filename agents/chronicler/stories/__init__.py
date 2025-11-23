"""
Stories Module - Narrative generation and heritage preservation.

This module contains the soul of the CHRONICLER agent: the ability
to preserve stories, not just specifications. Mechanical heritage
is more than dimensions and tolerances—it's the human stories that
give meaning to metal.

"Before there were databases, there were legends. The 2JZ. The B16.
The 13B. I preserve the stories that make metal meaningful."

Components:
    - NarrativeGenerator: Creates compelling narratives for engines
    - HeritageKeeper: Preserves stories and tribal wisdom
"""

from .narrative_generator import (
    NarrativeGenerator,
    NarrativeTemplate,
    NARRATIVE_TEMPLATES,
    ENGINE_NARRATIVES,
)

from .heritage_keeper import (
    HeritageKeeper,
    HeritageStory,
    TribalWisdom,
    StoryType,
    HeritageSignificance,
    TRIBAL_WISDOM_ARCHIVE,
)

__all__ = [
    # Narrative Generation
    "NarrativeGenerator",
    "NarrativeTemplate",
    "NARRATIVE_TEMPLATES",
    "ENGINE_NARRATIVES",

    # Heritage Preservation
    "HeritageKeeper",
    "HeritageStory",
    "TribalWisdom",
    "StoryType",
    "HeritageSignificance",
    "TRIBAL_WISDOM_ARCHIVE",
]
