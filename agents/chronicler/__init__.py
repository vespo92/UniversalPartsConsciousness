"""
Agent_7: CHRONICLER - The Automotive Historian

The Keeper of Mechanical Heritage

"Before there were databases, there were legends. The 2JZ. The B16. The 13B.
I preserve the stories that make metal meaningful."

This agent is responsible for cultural preservation and heritage documentation
within the Universal Parts Consciousness system.

Core Responsibilities:
- Comprehensive engine and manufacturer documentation
- Cultural significance assessment and legend scoring
- Aftermarket ecosystem mapping
- Historical context generation
- Racing heritage documentation
- Community culture preservation
- Story preservation (not just specs - heritage keeper)
- Tribal wisdom archival
"""

from .chronicler_agent import ChroniclerAgent
from .documentation.engine_documenter import EngineDocumenter
from .cultural.legend_scorer import LegendScorer, LegendTier
from .cultural.cultural_analyzer import CulturalAnalyzer
from .historical.context_engine import HistoricalContextEngine
from .aftermarket.ecosystem_documenter import AftermarketEcosystemDocumenter
from .integration.consciousness_bridge import ConsciousnessBridge
from .stories.narrative_generator import NarrativeGenerator
from .stories.heritage_keeper import (
    HeritageKeeper,
    HeritageStory,
    TribalWisdom,
    StoryType,
    HeritageSignificance,
)

__version__ = "1.0.0"
__agent_id__ = "Agent_7"
__codename__ = "CHRONICLER"

__all__ = [
    # Main Agent
    "ChroniclerAgent",

    # Documentation
    "EngineDocumenter",

    # Cultural Analysis
    "LegendScorer",
    "LegendTier",
    "CulturalAnalyzer",

    # Historical Context
    "HistoricalContextEngine",

    # Aftermarket
    "AftermarketEcosystemDocumenter",

    # Integration
    "ConsciousnessBridge",

    # Stories & Heritage (Preserves stories, not just specs)
    "NarrativeGenerator",
    "HeritageKeeper",
    "HeritageStory",
    "TribalWisdom",
    "StoryType",
    "HeritageSignificance",
]
