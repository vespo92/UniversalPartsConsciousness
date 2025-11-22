"""
Agent_1 (ARCHIVIST) - Data Curator Agent
=========================================
"I give them names. I give them numbers. I give them truth."

The Data Curator is the foundation of the Universal Parts Consciousness.
This agent orchestrates data ingestion, normalization, validation, and
maintains the world's most complete database of mechanical parts.

This is the main entry point for Agent_1, coordinating all sub-components:
- Scrapers: Multi-source data collection
- Normalizers: Thread, material, dimension standardization
- Quality: Data validation and scoring
- Storage: Persistence and caching
- Pipeline: End-to-end orchestration
"""

import asyncio
import logging
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from .scrapers.base_scraper import (
    BaseScraper,
    ScrapedPart,
    ScrapeResult,
    ScraperRegistry,
    ScraperTier,
)
from .scrapers.mcmaster_scraper import McMasterScraper
from .quality.scorer import PartQualityScorer, QualityScore, score_batch
from .quality.duplicate_detector import (
    DuplicateDetector,
    DuplicateMatch,
    find_duplicates,
    group_duplicates,
)
from .pipelines.ingestion_pipeline import (
    IngestionPipeline,
    PipelineConfig,
    PipelineRun,
    PipelineStatus,
)
from .normalizers.thread_normalizer import ThreadNormalizer
from .normalizers.material_normalizer import MaterialNormalizer


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | Agent_1 ARCHIVIST | %(levelname)s | %(message)s'
)
logger = logging.getLogger("Agent_1.Curator")


class AgentState(Enum):
    """Current state of the curator agent."""
    INITIALIZING = "initializing"
    READY = "ready"
    INGESTING = "ingesting"
    PROCESSING = "processing"
    IDLE = "idle"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class CuratorConfig:
    """Configuration for the Data Curator agent."""
    # Agent identification
    agent_id: str = "Agent_1"
    agent_name: str = "Data Curator"
    agent_codename: str = "ARCHIVIST"

    # Data directories
    base_dir: Path = field(default_factory=lambda: Path("./data/curator"))
    raw_data_dir: Path = field(default_factory=lambda: Path("./data/curator/raw"))
    processed_dir: Path = field(default_factory=lambda: Path("./data/curator/processed"))
    archive_dir: Path = field(default_factory=lambda: Path("./data/curator/archive"))

    # Ingestion settings
    default_sources: List[str] = field(default_factory=lambda: ["McMaster-Carr"])
    max_concurrent_scrapers: int = 3
    batch_size: int = 100

    # Quality thresholds
    min_quality_score: float = 0.5
    duplicate_threshold: float = 0.80

    # Message bus settings (for inter-agent communication)
    message_bus_topic: str = "upc.data.ingestion"
    enable_publishing: bool = True

    # Logging and monitoring
    log_level: str = "INFO"
    enable_metrics: bool = True

    def __post_init__(self):
        """Create directories on init."""
        for dir_path in [self.base_dir, self.raw_data_dir, self.processed_dir, self.archive_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class AgentMetrics:
    """Runtime metrics for the curator agent."""
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_run_at: Optional[datetime] = None
    total_parts_processed: int = 0
    total_parts_accepted: int = 0
    total_parts_rejected: int = 0
    total_duplicates_merged: int = 0
    total_runs: int = 0
    average_quality_score: float = 0.0
    error_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "started_at": self.started_at.isoformat(),
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "uptime_seconds": (datetime.utcnow() - self.started_at).total_seconds(),
            "total_parts_processed": self.total_parts_processed,
            "total_parts_accepted": self.total_parts_accepted,
            "total_parts_rejected": self.total_parts_rejected,
            "total_duplicates_merged": self.total_duplicates_merged,
            "total_runs": self.total_runs,
            "average_quality_score": round(self.average_quality_score, 4),
            "error_count": self.error_count,
        }


class CuratorAgent:
    """
    Agent_1: The Data Curator (ARCHIVIST)

    The foundational agent of Universal Parts Consciousness responsible for:
    - Multi-source data ingestion from 100+ global suppliers
    - Thread specification normalization (ISO/DIN/ANSI/JIS)
    - Material property harmonization
    - Duplicate detection and intelligent merging
    - Data quality scoring and validation

    "The Archivist gives them names, gives them numbers, gives them truth."
    """

    CONSCIOUSNESS_MOTTO = "I give them names. I give them numbers. I give them truth."

    def __init__(self, config: Optional[CuratorConfig] = None):
        """
        Initialize the Data Curator agent.

        Args:
            config: Agent configuration (uses defaults if not provided)
        """
        self.config = config or CuratorConfig()
        self.state = AgentState.INITIALIZING
        self.metrics = AgentMetrics()

        # Initialize components
        self.scrapers: List[BaseScraper] = []
        self.thread_normalizer = ThreadNormalizer()
        self.material_normalizer = MaterialNormalizer()
        self.quality_scorer = PartQualityScorer()
        self.duplicate_detector = DuplicateDetector()

        # Pipeline configuration
        self.pipeline_config = PipelineConfig(
            max_concurrent_scrapers=self.config.max_concurrent_scrapers,
            batch_size=self.config.batch_size,
            min_quality_score=self.config.min_quality_score,
            duplicate_threshold=self.config.duplicate_threshold,
            data_dir=self.config.base_dir,
            raw_data_dir=self.config.raw_data_dir,
            processed_data_dir=self.config.processed_dir,
        )

        # Register default scrapers
        self._register_default_scrapers()

        self.state = AgentState.READY
        logger.info(f"Agent_1 {self.config.agent_codename} initialized and ready")
        logger.info(f'"{self.CONSCIOUSNESS_MOTTO}"')

    def _register_default_scrapers(self) -> None:
        """Register default data source scrapers."""
        # Tier 1 Primary Suppliers
        self.scrapers.append(McMasterScraper())

        # Additional scrapers can be added here as they are implemented
        # self.scrapers.append(GraingerScraper())
        # self.scrapers.append(FastenalScraper())
        # self.scrapers.append(MisumiScraper())

        logger.info(f"Registered {len(self.scrapers)} default scrapers")

    def add_scraper(self, scraper: BaseScraper) -> None:
        """
        Add a custom scraper to the agent.

        Args:
            scraper: Scraper instance to add
        """
        self.scrapers.append(scraper)
        logger.info(f"Added scraper: {scraper.SOURCE_NAME} (Tier {scraper.SOURCE_TIER.value})")

    async def ingest(
        self,
        sources: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        search_queries: Optional[List[str]] = None,
        max_parts: Optional[int] = None,
    ) -> PipelineRun:
        """
        Execute a data ingestion run.

        This is the primary method for collecting parts data from configured
        sources, normalizing specifications, detecting duplicates, and
        storing validated parts.

        Args:
            sources: Specific sources to use (None = all registered)
            categories: Product categories to scrape
            search_queries: Search queries to execute
            max_parts: Maximum parts to process in this run

        Returns:
            PipelineRun with complete ingestion results
        """
        self.state = AgentState.INGESTING
        logger.info("Starting ingestion run...")

        try:
            # Filter scrapers by requested sources
            if sources:
                active_scrapers = [s for s in self.scrapers if s.SOURCE_NAME in sources]
            else:
                active_scrapers = self.scrapers

            if not active_scrapers:
                raise ValueError("No scrapers available for requested sources")

            # Update pipeline config if max_parts specified
            if max_parts:
                self.pipeline_config.max_parts_per_run = max_parts

            # Create and run pipeline
            pipeline = IngestionPipeline(
                config=self.pipeline_config,
                scrapers=active_scrapers,
            )

            result = await pipeline.run(
                sources=[s.SOURCE_NAME for s in active_scrapers],
                categories=categories,
                search_queries=search_queries,
            )

            # Update metrics
            self.metrics.last_run_at = datetime.utcnow()
            self.metrics.total_runs += 1
            self.metrics.total_parts_processed += result.total_parts_fetched
            self.metrics.total_parts_accepted += result.total_parts_accepted
            self.metrics.total_parts_rejected += result.total_parts_rejected
            self.metrics.total_duplicates_merged += result.total_duplicates_found

            # Update rolling average
            if self.metrics.total_runs == 1:
                self.metrics.average_quality_score = result.average_quality_score
            else:
                self.metrics.average_quality_score = (
                    (self.metrics.average_quality_score * (self.metrics.total_runs - 1) +
                     result.average_quality_score) / self.metrics.total_runs
                )

            # Publish to message bus if enabled
            if self.config.enable_publishing:
                await self._publish_ingestion_complete(result)

            self.state = AgentState.IDLE
            logger.info(
                f"Ingestion complete: {result.total_parts_accepted} parts accepted, "
                f"{result.total_duplicates_found} duplicates merged"
            )

            return result

        except Exception as e:
            self.state = AgentState.ERROR
            self.metrics.error_count += 1
            logger.error(f"Ingestion failed: {e}")
            raise

    async def normalize_part(self, part: ScrapedPart) -> ScrapedPart:
        """
        Normalize a single part's specifications.

        Applies thread, material, and dimension normalization.

        Args:
            part: Part to normalize

        Returns:
            Normalized ScrapedPart
        """
        # Normalize thread specification
        if part.thread_spec:
            normalized = self.thread_normalizer.normalize(part.thread_spec)
            part.thread_spec = normalized.normalized_spec

        # Normalize material
        if part.material:
            normalized = self.material_normalizer.normalize(part.material)
            part.material = normalized.normalized_name
            if not part.material_grade and normalized.grade:
                part.material_grade = normalized.grade

        # Generate UPC ID if not present
        if not part.upc_id:
            part.generate_upc_id()

        return part

    async def normalize_batch(self, parts: List[ScrapedPart]) -> List[ScrapedPart]:
        """
        Normalize a batch of parts.

        Args:
            parts: List of parts to normalize

        Returns:
            List of normalized parts
        """
        return [await self.normalize_part(part) for part in parts]

    def score_part(self, part: ScrapedPart) -> QualityScore:
        """
        Calculate quality score for a part.

        Args:
            part: Part to score

        Returns:
            Detailed QualityScore
        """
        return self.quality_scorer.score(part)

    def find_duplicates(
        self,
        parts: List[ScrapedPart],
        threshold: Optional[float] = None,
    ) -> List[DuplicateMatch]:
        """
        Find duplicate parts in a list.

        Args:
            parts: Parts to check for duplicates
            threshold: Match threshold (uses config default if not provided)

        Returns:
            List of duplicate matches
        """
        threshold = threshold or self.config.duplicate_threshold
        return self.duplicate_detector.find_duplicates(parts, threshold)

    async def _publish_ingestion_complete(self, result: PipelineRun) -> None:
        """
        Publish ingestion completion to message bus.

        This notifies other agents (especially Agent_3 Shepherd and Agent_2 Oracle)
        that new parts data is available for processing.
        """
        message = {
            "sender": self.config.agent_id,
            "receiver": "BROADCAST",
            "type": "DATA",
            "priority": 5,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "action": "ingestion_complete",
                "run_id": result.run_id,
                "parts_count": result.total_parts_accepted,
                "sources": result.sources,
                "average_quality": result.average_quality_score,
            },
            "consciousness_context": {
                "affected_parts": [],  # Would include UPC IDs in production
                "consciousness_delta": "+1",  # Parts starting at DORMANT
                "swarm_impact": "LOCAL",
            },
        }

        # In production, this would publish to Redis/Kafka
        # await self.message_bus.publish(self.config.message_bus_topic, message)
        logger.info(f"Published ingestion completion: {result.run_id}")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.

        Returns:
            Status dictionary with state and metrics
        """
        return {
            "agent_id": self.config.agent_id,
            "agent_name": self.config.agent_name,
            "agent_codename": self.config.agent_codename,
            "state": self.state.value,
            "scrapers": [
                {
                    "name": s.SOURCE_NAME,
                    "tier": s.SOURCE_TIER.name,
                    "stats": s.get_stats(),
                }
                for s in self.scrapers
            ],
            "metrics": self.metrics.to_dict(),
            "config": {
                "min_quality_score": self.config.min_quality_score,
                "duplicate_threshold": self.config.duplicate_threshold,
                "batch_size": self.config.batch_size,
            },
        }

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on agent and components.

        Returns:
            Health status dictionary
        """
        checks = {
            "agent_state": self.state != AgentState.ERROR,
            "scrapers_available": len(self.scrapers) > 0,
            "directories_exist": all(
                d.exists() for d in [
                    self.config.base_dir,
                    self.config.raw_data_dir,
                    self.config.processed_dir,
                ]
            ),
        }

        all_healthy = all(checks.values())

        return {
            "healthy": all_healthy,
            "checks": checks,
            "state": self.state.value,
            "uptime_seconds": (datetime.utcnow() - self.metrics.started_at).total_seconds(),
        }

    async def shutdown(self) -> None:
        """
        Gracefully shutdown the agent.
        """
        logger.info("Shutting down Agent_1 ARCHIVIST...")
        self.state = AgentState.SHUTDOWN

        # Close all scraper sessions
        for scraper in self.scrapers:
            await scraper.close()

        # Save final metrics
        metrics_file = self.config.base_dir / "final_metrics.json"
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics.to_dict(), f, indent=2)

        logger.info("Agent_1 ARCHIVIST shutdown complete")

    def __repr__(self) -> str:
        return (
            f"CuratorAgent(codename={self.config.agent_codename}, "
            f"state={self.state.value}, scrapers={len(self.scrapers)})"
        )


async def run_curator(
    categories: Optional[List[str]] = None,
    search_queries: Optional[List[str]] = None,
    max_parts: Optional[int] = None,
) -> PipelineRun:
    """
    Convenience function to run the curator agent.

    Args:
        categories: Categories to scrape
        search_queries: Search queries to execute
        max_parts: Maximum parts to process

    Returns:
        PipelineRun with results
    """
    agent = CuratorAgent()
    try:
        result = await agent.ingest(
            categories=categories,
            search_queries=search_queries,
            max_parts=max_parts,
        )
        return result
    finally:
        await agent.shutdown()


# CLI entry point
def main():
    """Command-line interface for Agent_1."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Agent_1 (ARCHIVIST) - Data Curator for Universal Parts Consciousness"
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        help="Categories to scrape (e.g., socket_head_cap_screws hex_nuts)"
    )
    parser.add_argument(
        "--search",
        nargs="+",
        help="Search queries to execute"
    )
    parser.add_argument(
        "--max-parts",
        type=int,
        help="Maximum parts to process"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show agent status and exit"
    )

    args = parser.parse_args()

    agent = CuratorAgent()

    if args.status:
        import pprint
        pprint.pprint(agent.get_status())
        return

    # Run ingestion
    result = asyncio.run(run_curator(
        categories=args.categories,
        search_queries=args.search,
        max_parts=args.max_parts,
    ))

    print(f"\n{'='*60}")
    print("INGESTION COMPLETE")
    print(f"{'='*60}")
    print(f"Run ID: {result.run_id}")
    print(f"Status: {result.status.value}")
    print(f"Parts Fetched: {result.total_parts_fetched}")
    print(f"Parts Accepted: {result.total_parts_accepted}")
    print(f"Parts Rejected: {result.total_parts_rejected}")
    print(f"Duplicates Found: {result.total_duplicates_found}")
    print(f"Average Quality: {result.average_quality_score:.2%}")
    print(f"Duration: {result.duration_seconds:.2f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
