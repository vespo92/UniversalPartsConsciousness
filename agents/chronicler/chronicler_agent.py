"""
ChroniclerAgent - Core Agent_7 Implementation

The Automotive Historian: Keeper of Mechanical Heritage

This agent coordinates all documentation, cultural analysis, and historical
context generation for the Universal Parts Consciousness system.
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Operating states for the Chronicler agent."""
    DORMANT = "dormant"
    ACTIVE = "active"
    DOCUMENTING = "documenting"
    ANALYZING = "analyzing"
    ARCHIVING = "archiving"


@dataclass
class AgentMetrics:
    """Metrics tracked by Agent_10 (Meta-Consciousness)."""
    documentation_coverage: float = 0.0  # Target: 70%+
    narrative_quality: float = 0.0       # Qualitative assessment
    history_accuracy: float = 0.0        # Verification score
    engines_documented: int = 0
    manufacturers_complete: int = 0
    legend_scores_calculated: int = 0
    historical_narratives: int = 0
    aftermarket_ecosystems_mapped: int = 0
    racing_heritage_records: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class DocumentationStatus:
    """Status of documentation for a manufacturer."""
    manufacturer: str
    engine_families: int
    engines_documented: int
    completeness: float
    has_master: bool
    has_parts_catalog: bool
    has_interchangeability: bool
    has_tools_procedures: bool
    has_aftermarket: bool
    has_history_narrative: bool


class ChroniclerAgent:
    """
    Agent_7: The Automotive Historian (CHRONICLER)

    Core orchestrator for all documentation and cultural preservation
    activities within the Universal Parts Consciousness system.

    "Engines are not just machines. They are the dreams of engineers made
    manifest, the roar of competition, the stories passed down through
    generations. I preserve these stories so that consciousness has roots."
    """

    AGENT_ID = "Agent_7"
    CODENAME = "CHRONICLER"
    DOMAIN = "Automotive Documentation, Cultural Preservation"
    CONSCIOUSNESS_ROLE = "The Keeper of Mechanical Heritage"

    # Communication bus topics
    TOPIC_DOCUMENTED = "upc.history.documented"
    TOPIC_LEGEND_SCORED = "upc.culture.legend_scored"
    TOPIC_CONTEXT_GENERATED = "upc.history.context"

    def __init__(
        self,
        automotive_base_path: Optional[Path] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Chronicler agent.

        Args:
            automotive_base_path: Base path to Automotive/ directory
            config: Optional configuration dictionary
        """
        self.state = AgentState.DORMANT
        self.metrics = AgentMetrics()
        self.config = config or {}

        # Set base paths
        self.base_path = automotive_base_path or Path("Automotive")
        self.engines_path = self.base_path / "Engines" / "Manufacturers"
        self.heritage_path = self.base_path / "Heritage"
        self.stories_path = self.base_path / "Stories"

        # Initialize subcomponents (lazy loading)
        self._engine_documenter = None
        self._legend_scorer = None
        self._cultural_analyzer = None
        self._context_engine = None
        self._ecosystem_documenter = None
        self._consciousness_bridge = None
        self._narrative_generator = None
        self._heritage_keeper = None

        # Documentation registry
        self._documented_engines: Dict[str, DocumentationStatus] = {}

        logger.info(
            f"Initialized {self.AGENT_ID} ({self.CODENAME}): {self.CONSCIOUSNESS_ROLE}"
        )

    @property
    def engine_documenter(self):
        """Lazy-load engine documenter."""
        if self._engine_documenter is None:
            from .documentation.engine_documenter import EngineDocumenter
            self._engine_documenter = EngineDocumenter(self.engines_path)
        return self._engine_documenter

    @property
    def legend_scorer(self):
        """Lazy-load legend scorer."""
        if self._legend_scorer is None:
            from .cultural.legend_scorer import LegendScorer
            self._legend_scorer = LegendScorer()
        return self._legend_scorer

    @property
    def cultural_analyzer(self):
        """Lazy-load cultural analyzer."""
        if self._cultural_analyzer is None:
            from .cultural.cultural_analyzer import CulturalAnalyzer
            self._cultural_analyzer = CulturalAnalyzer()
        return self._cultural_analyzer

    @property
    def context_engine(self):
        """Lazy-load historical context engine."""
        if self._context_engine is None:
            from .historical.context_engine import HistoricalContextEngine
            self._context_engine = HistoricalContextEngine()
        return self._context_engine

    @property
    def ecosystem_documenter(self):
        """Lazy-load aftermarket ecosystem documenter."""
        if self._ecosystem_documenter is None:
            from .aftermarket.ecosystem_documenter import AftermarketEcosystemDocumenter
            self._ecosystem_documenter = AftermarketEcosystemDocumenter()
        return self._ecosystem_documenter

    @property
    def consciousness_bridge(self):
        """Lazy-load consciousness bridge for agent integration."""
        if self._consciousness_bridge is None:
            from .integration.consciousness_bridge import ConsciousnessBridge
            self._consciousness_bridge = ConsciousnessBridge(self)
        return self._consciousness_bridge

    @property
    def narrative_generator(self):
        """Lazy-load narrative generator for story creation."""
        if self._narrative_generator is None:
            from .stories.narrative_generator import NarrativeGenerator
            self._narrative_generator = NarrativeGenerator()
        return self._narrative_generator

    @property
    def heritage_keeper(self):
        """Lazy-load heritage keeper for story preservation."""
        if self._heritage_keeper is None:
            from .stories.heritage_keeper import HeritageKeeper
            self._heritage_keeper = HeritageKeeper()
        return self._heritage_keeper

    def activate(self) -> None:
        """Activate the agent and begin monitoring."""
        self.state = AgentState.ACTIVE
        logger.info(f"{self.CODENAME} activated: Ready to preserve mechanical heritage")
        self._scan_documentation_status()

    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.state = AgentState.DORMANT
        logger.info(f"{self.CODENAME} entering dormant state")

    def _scan_documentation_status(self) -> None:
        """Scan existing documentation to update metrics."""
        if not self.engines_path.exists():
            logger.warning(f"Engines path not found: {self.engines_path}")
            return

        total_engines = 0
        complete_manufacturers = 0

        for manufacturer_path in self.engines_path.iterdir():
            if not manufacturer_path.is_dir():
                continue

            engine_count = 0
            complete_count = 0

            # Handle nested manufacturer structure (e.g., GM/Chevrolet)
            engine_dirs = list(manufacturer_path.glob("*/"))
            if not engine_dirs:
                continue

            # Check if subdirs are engine dirs or brand dirs
            first_subdir = engine_dirs[0]
            has_json = list(first_subdir.glob("*.json"))

            if has_json:
                # Direct engine directories
                for engine_dir in engine_dirs:
                    engine_count += 1
                    if self._check_engine_completeness(engine_dir):
                        complete_count += 1
            else:
                # Nested brand structure (GM/Chevrolet, GM/Buick, etc.)
                for brand_dir in engine_dirs:
                    for engine_dir in brand_dir.iterdir():
                        if engine_dir.is_dir():
                            engine_count += 1
                            if self._check_engine_completeness(engine_dir):
                                complete_count += 1

            total_engines += engine_count
            if engine_count > 0 and complete_count == engine_count:
                complete_manufacturers += 1

            self._documented_engines[manufacturer_path.name] = DocumentationStatus(
                manufacturer=manufacturer_path.name,
                engine_families=engine_count,
                engines_documented=complete_count,
                completeness=complete_count / engine_count if engine_count > 0 else 0,
                has_master=True,  # Simplified
                has_parts_catalog=True,
                has_interchangeability=True,
                has_tools_procedures=True,
                has_aftermarket=True,
                has_history_narrative=False  # TODO: Check for .md files
            )

        self.metrics.engines_documented = total_engines
        self.metrics.manufacturers_complete = complete_manufacturers
        self.metrics.documentation_coverage = (
            total_engines / 500 if total_engines < 500 else 1.0
        )  # Target: 500 engines
        self.metrics.last_updated = datetime.now()

        logger.info(
            f"Documentation scan complete: {total_engines} engines, "
            f"{complete_manufacturers} complete manufacturers"
        )

    def _check_engine_completeness(self, engine_dir: Path) -> bool:
        """Check if an engine directory has all required files."""
        required_patterns = ["*-master.json", "*-catalog.json", "*interchangeability*.json"]
        for pattern in required_patterns:
            if not list(engine_dir.glob(pattern)):
                return False
        return True

    def document_engine(
        self,
        manufacturer: str,
        engine_code: str,
        specifications: Dict[str, Any],
        history: Optional[Dict[str, Any]] = None,
        cultural_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create comprehensive documentation for an engine.

        Args:
            manufacturer: Manufacturer name (e.g., "Honda", "Toyota")
            engine_code: Engine code (e.g., "B16A", "2JZ-GTE")
            specifications: Technical specifications dictionary
            history: Optional historical context data
            cultural_data: Optional cultural significance data

        Returns:
            Documentation result with paths and status
        """
        self.state = AgentState.DOCUMENTING

        try:
            # Generate documentation
            result = self.engine_documenter.document(
                manufacturer=manufacturer,
                engine_code=engine_code,
                specifications=specifications,
                history=history
            )

            # Calculate legend score if cultural data provided
            if cultural_data:
                legend_result = self.legend_scorer.calculate_score(
                    engine_code=engine_code,
                    cultural_data=cultural_data
                )
                result["legend_score"] = legend_result

            # Generate historical context
            if history and history.get("production_start_year"):
                context = self.context_engine.generate_context(
                    engine_code=engine_code,
                    year=history["production_start_year"],
                    manufacturer=manufacturer
                )
                result["historical_context"] = context

            # Update metrics
            self.metrics.engines_documented += 1
            self.metrics.last_updated = datetime.now()

            # Notify consciousness bridge
            self.consciousness_bridge.emit_event(
                topic=self.TOPIC_DOCUMENTED,
                data={
                    "engine_code": engine_code,
                    "manufacturer": manufacturer,
                    "documentation_paths": result.get("paths", [])
                }
            )

            return result

        finally:
            self.state = AgentState.ACTIVE

    def calculate_legend_score(
        self,
        engine_code: str,
        racing_heritage: Optional[Dict[str, Any]] = None,
        tuning_culture: Optional[Dict[str, Any]] = None,
        reliability: Optional[Dict[str, Any]] = None,
        innovation: Optional[Dict[str, Any]] = None,
        pop_culture: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate the legend score for an engine.

        Args:
            engine_code: Engine code to score
            racing_heritage: Racing achievements and history
            tuning_culture: Aftermarket support and community
            reliability: Reliability reputation data
            innovation: Engineering innovation data
            pop_culture: Media presence data

        Returns:
            Legend score result with tier and breakdown
        """
        self.state = AgentState.ANALYZING

        try:
            result = self.legend_scorer.calculate_score(
                engine_code=engine_code,
                cultural_data={
                    "racing_heritage": racing_heritage or {},
                    "tuning_culture": tuning_culture or {},
                    "reliability": reliability or {},
                    "innovation": innovation or {},
                    "pop_culture": pop_culture or {}
                }
            )

            self.metrics.legend_scores_calculated += 1

            # Notify consciousness
            self.consciousness_bridge.emit_event(
                topic=self.TOPIC_LEGEND_SCORED,
                data={
                    "engine_code": engine_code,
                    "score": result["score"],
                    "tier": result["tier"]
                }
            )

            return result

        finally:
            self.state = AgentState.ACTIVE

    def generate_historical_context(
        self,
        engine_code: str,
        year: int,
        manufacturer: str
    ) -> Dict[str, Any]:
        """
        Generate rich historical context for an engine.

        Args:
            engine_code: Engine code
            year: Production year to contextualize
            manufacturer: Manufacturer name

        Returns:
            Historical context report
        """
        self.state = AgentState.ANALYZING

        try:
            context = self.context_engine.generate_context(
                engine_code=engine_code,
                year=year,
                manufacturer=manufacturer
            )

            self.consciousness_bridge.emit_event(
                topic=self.TOPIC_CONTEXT_GENERATED,
                data={
                    "engine_code": engine_code,
                    "year": year,
                    "era": context.get("era", "unknown")
                }
            )

            return context

        finally:
            self.state = AgentState.ACTIVE

    def get_documentation_status(self) -> Dict[str, Any]:
        """Get current documentation status and metrics."""
        return {
            "agent_id": self.AGENT_ID,
            "codename": self.CODENAME,
            "state": self.state.value,
            "metrics": {
                "documentation_coverage": self.metrics.documentation_coverage,
                "engines_documented": self.metrics.engines_documented,
                "manufacturers_complete": self.metrics.manufacturers_complete,
                "legend_scores_calculated": self.metrics.legend_scores_calculated,
                "historical_narratives": self.metrics.historical_narratives,
                "last_updated": self.metrics.last_updated.isoformat()
            },
            "manufacturers": {
                name: {
                    "engine_families": status.engine_families,
                    "completeness": status.completeness
                }
                for name, status in self._documented_engines.items()
            }
        }

    def get_manufacturer_status(self, manufacturer: str) -> Optional[DocumentationStatus]:
        """Get documentation status for a specific manufacturer."""
        return self._documented_engines.get(manufacturer)

    def list_documented_manufacturers(self) -> List[str]:
        """List all documented manufacturers."""
        return list(self._documented_engines.keys())

    def explain_significance(self, engine_code: str) -> str:
        """
        Generate a narrative explanation of why an engine mattered.

        This is the soul of the Chronicler - explaining the human story
        behind mechanical engineering.
        """
        return self.context_engine.explain_significance(engine_code)

    def get_engine_narrative(self, engine_code: str) -> Dict[str, Any]:
        """
        Get the complete narrative for an engine.

        Preserves stories, not just specs - this returns the human
        story behind the mechanical specifications.

        Args:
            engine_code: Engine code to get narrative for

        Returns:
            Complete narrative with title and content
        """
        return self.narrative_generator.generate_narrative(engine_code)

    def preserve_story(
        self,
        subject: str,
        title: str,
        narrative: str,
        story_type: str = "origin_story",
        significance: str = "documented",
        era: str = "",
        community_contributed: bool = False
    ) -> Dict[str, Any]:
        """
        Preserve a heritage story for future generations.

        "Preserves stories, not just specs - heritage keeper"

        Args:
            subject: What the story is about (engine, part, person)
            title: Story title
            narrative: The full narrative
            story_type: Type of story (origin_story, racing_glory, etc.)
            significance: Heritage significance level
            era: Time period
            community_contributed: Whether from community

        Returns:
            Preserved story details
        """
        from .stories.heritage_keeper import StoryType, HeritageSignificance

        # Map string to enum
        story_type_enum = StoryType(story_type)
        significance_enum = HeritageSignificance(significance)

        story = self.heritage_keeper.preserve_story(
            subject=subject,
            title=title,
            narrative=narrative,
            story_type=story_type_enum,
            significance=significance_enum,
            era=era,
            community_contributed=community_contributed
        )

        self.metrics.historical_narratives += 1
        self.metrics.last_updated = datetime.now()

        return {
            "story_id": story.story_id,
            "subject": story.subject,
            "title": story.title,
            "significance": story.significance.value,
            "preservation_date": story.preservation_date.isoformat()
        }

    def get_tribal_wisdom(self, engine_code: str) -> List[Dict[str, Any]]:
        """
        Get tribal wisdom for an engine - the unwritten rules every builder knows.

        This knowledge isn't in any manual, but every experienced builder
        understands it. It's passed down through forums, shop talk, and
        hard-won experience.

        Args:
            engine_code: Engine code to get wisdom for

        Returns:
            List of tribal wisdom entries
        """
        wisdom_list = self.heritage_keeper.get_tribal_wisdom(engine_code)
        return [
            {
                "wisdom": w.wisdom,
                "context": w.context,
                "source_community": w.source_community,
                "verification_level": w.verification_level,
                "failure_stories": w.failure_stories
            }
            for w in wisdom_list
        ]

    def get_heritage_explanation(self, engine_code: str) -> Dict[str, Any]:
        """
        Get comprehensive heritage explanation for an engine.

        This is the full story: significance, narratives, tribal wisdom,
        and cultural impact all in one place.

        Args:
            engine_code: Engine code to explain

        Returns:
            Complete heritage explanation
        """
        return self.heritage_keeper.explain_heritage(engine_code)

    def __repr__(self) -> str:
        return (
            f"<ChroniclerAgent(state={self.state.value}, "
            f"engines={self.metrics.engines_documented}, "
            f"manufacturers={self.metrics.manufacturers_complete})>"
        )
