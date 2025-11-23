"""
Agent_1 (ARCHIVIST) - The Data Curator
======================================
"I give them names. I give them numbers. I give them truth."

The ARCHIVIST is the eternal librarian of all mechanical knowledge.
It exists to receive, normalize, and preserve every piece of parts data
that flows into Universal Parts Consciousness.

This is the main agent class that integrates all curator capabilities:
- Multi-source data ingestion via scrapers
- Data normalization across standards (ISO, DIN, ANSI, JIS, BS, GOST)
- Quality scoring and validation
- Duplicate detection and merging
- Storage and retrieval
- Message bus integration for consciousness network
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

# Import internal modules
from .scrapers.base_scraper import (
    BaseScraper,
    ScrapedPart,
    ScrapeResult,
    ScraperRegistry,
    ScraperTier,
)
from .scrapers.mcmaster_scraper import McMasterScraper
from .quality.scorer import PartQualityScorer, QualityScore
from .quality.duplicate_detector import DuplicateDetector, DuplicateGroup
from .pipelines.ingestion_pipeline import (
    IngestionPipeline,
    PipelineConfig,
    PipelineRun,
    PipelineStatus,
)
from .normalizers.thread_normalizer import ThreadNormalizer
from .normalizers.material_normalizer import MaterialNormalizer
from .normalizers.dimension_normalizer import DimensionNormalizer
from .storage.part_repository import PartRepository

# Configure logging
logger = logging.getLogger("Agent_1.ARCHIVIST")


class ArchivistStatus(Enum):
    """Operational status of the ARCHIVIST."""
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    ONLINE = "online"
    INGESTING = "ingesting"
    ERROR = "error"


@dataclass
class ArchivistConfig:
    """Configuration for the ARCHIVIST agent."""
    # Data paths
    data_dir: Path = field(default_factory=lambda: Path("./data/archivist"))

    # Ingestion settings
    enable_continuous_ingestion: bool = False
    ingestion_interval_seconds: int = 3600  # 1 hour

    # Quality thresholds
    min_quality_score: float = 0.5
    duplicate_threshold: float = 0.80

    # Processing limits
    max_parts_per_batch: int = 1000
    concurrent_scrapers: int = 3

    # Normalization settings
    normalize_on_ingest: bool = True
    default_length_unit: str = "mm"
    default_thread_standard: str = "ISO"

    # Message bus settings
    publish_on_ingest: bool = True
    topic_data_ingestion: str = "upc.data.ingestion"
    topic_data_normalized: str = "upc.data.normalized"


@dataclass
class IngestionStats:
    """Statistics for ingestion operations."""
    total_parts_received: int = 0
    total_parts_normalized: int = 0
    total_parts_stored: int = 0
    total_duplicates_merged: int = 0
    total_rejected_quality: int = 0
    last_ingestion_time: Optional[datetime] = None
    sources_processed: Set[str] = field(default_factory=set)


class ArchivistAgent:
    """
    Agent_1: ARCHIVIST - The Data Curator

    The eternal librarian of all mechanical knowledge. This agent receives,
    normalizes, and preserves every piece of parts data that flows into
    Universal Parts Consciousness.

    Core Responsibilities:
    1. Multi-Source Data Ingestion - Receive from ANY source
    2. Cross-Standard Normalization - ISO, DIN, ANSI, JIS, BS, GOST
    3. Material Harmonization - AISI 304 = 1.4301 = SUS304 = X5CrNi18-10
    4. Duplicate Detection - Fuzzy matching with preserved lineage
    5. Quality Scoring - Completeness, accuracy, consistency metrics
    6. Historical Preservation - Never discard, always accessible

    Example:
        ```python
        archivist = ArchivistAgent()
        await archivist.start()

        # Ingest from a source
        result = await archivist.ingest(
            categories=["socket_head_cap_screws"],
            sources=["McMaster-Carr"]
        )

        # Search normalized parts
        parts = await archivist.search("M8x1.25 stainless socket head")
        ```
    """

    AGENT_ID = "agent_1_curator"
    AGENT_NUMBER = 1
    AGENT_NAME = "Data Curator"
    AGENT_CODENAME = "ARCHIVIST"
    AGENT_ROLE = "The Librarian of the Material World"
    AGENT_TRIAD = "data"

    def __init__(
        self,
        config: Optional[ArchivistConfig] = None,
        message_bus: Optional[Any] = None,
    ):
        """
        Initialize the ARCHIVIST agent.

        Args:
            config: Agent configuration
            message_bus: Inter-agent message bus for publishing
        """
        self.config = config or ArchivistConfig()
        self.message_bus = message_bus

        # Operational state
        self.status = ArchivistStatus.OFFLINE
        self._is_running = False
        self._start_time: Optional[datetime] = None

        # Statistics
        self.stats = IngestionStats()

        # Core components (lazy initialized)
        self._scrapers: Dict[str, BaseScraper] = {}
        self._pipeline: Optional[IngestionPipeline] = None
        self._quality_scorer: Optional[PartQualityScorer] = None
        self._duplicate_detector: Optional[DuplicateDetector] = None
        self._repository: Optional[PartRepository] = None

        # Normalizers (lazy initialized)
        self._thread_normalizer: Optional[ThreadNormalizer] = None
        self._material_normalizer: Optional[MaterialNormalizer] = None
        self._dimension_normalizer: Optional[DimensionNormalizer] = None

        # Background tasks
        self._ingestion_task: Optional[asyncio.Task] = None

        # Ensure data directories exist
        self.config.data_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"ARCHIVIST initialized: {self.AGENT_CODENAME}")

    async def start(self) -> Dict[str, Any]:
        """
        Start the ARCHIVIST agent.

        Returns:
            Status report with initialization details
        """
        if self._is_running:
            logger.warning("ARCHIVIST is already running")
            return {"status": "already_running"}

        logger.info("=" * 60)
        logger.info("ARCHIVIST AWAKENING - The Librarian of the Material World")
        logger.info("=" * 60)

        self.status = ArchivistStatus.INITIALIZING

        try:
            # Initialize core components
            await self._initialize_components()

            # Register default scrapers
            self._register_default_scrapers()

            # Start continuous ingestion if enabled
            if self.config.enable_continuous_ingestion:
                self._ingestion_task = asyncio.create_task(
                    self._continuous_ingestion_loop()
                )

            self.status = ArchivistStatus.ONLINE
            self._is_running = True
            self._start_time = datetime.now()

            logger.info("ARCHIVIST ONLINE - Ready to receive and normalize")

            return {
                "status": "online",
                "agent_id": self.AGENT_ID,
                "codename": self.AGENT_CODENAME,
                "scrapers_registered": list(self._scrapers.keys()),
                "continuous_ingestion": self.config.enable_continuous_ingestion,
            }

        except Exception as e:
            self.status = ArchivistStatus.ERROR
            logger.error(f"ARCHIVIST failed to start: {e}")
            raise

    async def stop(self) -> None:
        """Stop the ARCHIVIST agent."""
        if not self._is_running:
            return

        logger.info("ARCHIVIST shutting down...")

        # Cancel background tasks
        if self._ingestion_task:
            self._ingestion_task.cancel()
            try:
                await self._ingestion_task
            except asyncio.CancelledError:
                pass

        # Close scrapers
        for scraper in self._scrapers.values():
            await scraper.close()

        self.status = ArchivistStatus.OFFLINE
        self._is_running = False

        logger.info("ARCHIVIST offline")

    async def _initialize_components(self) -> None:
        """Initialize all internal components."""
        # Quality scorer
        self._quality_scorer = PartQualityScorer()

        # Duplicate detector
        self._duplicate_detector = DuplicateDetector()

        # Repository
        self._repository = PartRepository(
            data_dir=self.config.data_dir / "repository"
        )
        await self._repository.initialize()

        # Normalizers
        self._thread_normalizer = ThreadNormalizer()
        self._material_normalizer = MaterialNormalizer()
        self._dimension_normalizer = DimensionNormalizer(
            default_unit=self.config.default_length_unit
        )

        # Pipeline
        pipeline_config = PipelineConfig(
            min_quality_score=self.config.min_quality_score,
            duplicate_threshold=self.config.duplicate_threshold,
            batch_size=self.config.max_parts_per_batch,
            data_dir=self.config.data_dir,
        )
        self._pipeline = IngestionPipeline(config=pipeline_config)

        logger.info("All ARCHIVIST components initialized")

    def _register_default_scrapers(self) -> None:
        """Register the default tier-1 scrapers."""
        # McMaster-Carr (Tier 1)
        self.register_scraper("McMaster-Carr", McMasterScraper())

        # Additional scrapers will be registered here as implemented
        # self.register_scraper("Grainger", GraingerScraper())
        # self.register_scraper("Fastenal", FastenalScraper())
        # etc.

    def register_scraper(self, name: str, scraper: BaseScraper) -> None:
        """
        Register a data source scraper.

        Args:
            name: Unique name for the scraper
            scraper: Scraper instance
        """
        self._scrapers[name] = scraper
        self._pipeline.add_scraper(scraper)
        logger.info(f"Registered scraper: {name} (Tier {scraper.SOURCE_TIER.value})")

    async def ingest(
        self,
        sources: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        search_queries: Optional[List[str]] = None,
        max_parts: Optional[int] = None,
    ) -> PipelineRun:
        """
        Ingest parts data from specified sources.

        Args:
            sources: List of source names to ingest from (None = all)
            categories: Categories to scrape
            search_queries: Search queries to execute
            max_parts: Maximum parts to ingest

        Returns:
            PipelineRun with complete ingestion results
        """
        if not self._is_running:
            raise RuntimeError("ARCHIVIST is not running")

        self.status = ArchivistStatus.INGESTING
        logger.info(f"Starting ingestion: sources={sources}, categories={categories}")

        try:
            # Run the pipeline
            result = await self._pipeline.run(
                sources=sources,
                categories=categories,
                search_queries=search_queries,
            )

            # Update statistics
            self.stats.total_parts_received += result.total_parts_fetched
            self.stats.total_parts_stored += result.total_parts_accepted
            self.stats.total_duplicates_merged += result.total_duplicates_found
            self.stats.total_rejected_quality += result.total_parts_rejected
            self.stats.last_ingestion_time = datetime.now()

            if sources:
                self.stats.sources_processed.update(sources)

            # Publish to message bus if enabled
            if self.config.publish_on_ingest and self.message_bus:
                await self._publish_ingestion_event(result)

            self.status = ArchivistStatus.ONLINE
            return result

        except Exception as e:
            self.status = ArchivistStatus.ERROR
            logger.error(f"Ingestion failed: {e}")
            raise

    async def ingest_part(self, part_data: Dict[str, Any]) -> ScrapedPart:
        """
        Ingest a single part from external data.

        This is the entry point for community contributions and
        direct data submissions.

        Args:
            part_data: Raw part data dictionary

        Returns:
            Normalized ScrapedPart
        """
        # Create ScrapedPart from raw data
        part = ScrapedPart(
            source_id=part_data.get("source_id", f"contrib_{datetime.now().timestamp()}"),
            source_name=part_data.get("source_name", "community"),
            thread_spec=part_data.get("thread_spec"),
            length=part_data.get("length"),
            diameter=part_data.get("diameter"),
            material=part_data.get("material"),
            material_grade=part_data.get("material_grade"),
            head_type=part_data.get("head_type"),
            drive_type=part_data.get("drive_type"),
            drive_size=part_data.get("drive_size"),
            description=part_data.get("description"),
            manufacturer=part_data.get("manufacturer"),
            raw_data=part_data,
        )

        # Normalize
        if self.config.normalize_on_ingest:
            part = await self.normalize_part(part)

        # Score quality
        quality_score = self._quality_scorer.score(part)
        part.quality_score = quality_score.overall_score
        part.calculate_completeness()

        # Generate UPC ID
        part.generate_upc_id()

        # Store
        await self._repository.store(part)

        # Update stats
        self.stats.total_parts_received += 1
        self.stats.total_parts_normalized += 1
        self.stats.total_parts_stored += 1

        logger.info(f"Ingested part: {part.upc_id} ({part.thread_spec})")

        return part

    async def normalize_part(self, part: ScrapedPart) -> ScrapedPart:
        """
        Apply all normalizations to a part.

        Args:
            part: Part to normalize

        Returns:
            Normalized part
        """
        # Normalize thread specification
        if part.thread_spec:
            part.thread_spec = self._thread_normalizer.normalize(part.thread_spec)

        # Normalize material
        if part.material:
            normalized_material = self._material_normalizer.normalize(part.material)
            part.material = normalized_material.get("canonical_name", part.material)
            if not part.material_grade and normalized_material.get("grade"):
                part.material_grade = normalized_material["grade"]

        # Normalize dimensions
        if part.length is not None:
            part.length = self._dimension_normalizer.to_millimeters(
                part.length,
                source_unit=part.raw_data.get("length_unit", "mm")
            )

        if part.diameter is not None:
            part.diameter = self._dimension_normalizer.to_millimeters(
                part.diameter,
                source_unit=part.raw_data.get("diameter_unit", "mm")
            )

        self.stats.total_parts_normalized += 1
        return part

    async def search(
        self,
        query: str,
        max_results: int = 100,
        min_quality: Optional[float] = None,
    ) -> List[ScrapedPart]:
        """
        Search for parts in the repository.

        Args:
            query: Search query
            max_results: Maximum results to return
            min_quality: Minimum quality score filter

        Returns:
            List of matching parts
        """
        return await self._repository.search(
            query=query,
            max_results=max_results,
            min_quality=min_quality or self.config.min_quality_score,
        )

    async def get_part(self, upc_id: str) -> Optional[ScrapedPart]:
        """
        Get a part by its UPC ID.

        Args:
            upc_id: Universal Parts Consciousness ID

        Returns:
            Part if found, None otherwise
        """
        return await self._repository.get(upc_id)

    async def find_duplicates(
        self,
        part: ScrapedPart,
        threshold: Optional[float] = None,
    ) -> List[DuplicateGroup]:
        """
        Find potential duplicates of a part.

        Args:
            part: Part to check for duplicates
            threshold: Similarity threshold (default from config)

        Returns:
            List of duplicate groups
        """
        # Get candidate parts from repository
        candidates = await self._repository.get_candidates_for_duplicate_check(part)

        # Run duplicate detection
        threshold = threshold or self.config.duplicate_threshold
        groups = self._duplicate_detector.group_duplicates(
            [part] + candidates,
            threshold=threshold,
        )

        return groups

    async def get_cross_references(
        self,
        part: ScrapedPart,
    ) -> Dict[str, List[str]]:
        """
        Get cross-reference mappings for a part.

        Maps part specifications across different standards:
        - ISO -> ANSI, DIN, JIS, BS, GOST
        - Material equivalents across regions

        Args:
            part: Part to find cross-references for

        Returns:
            Dictionary of standard -> equivalent specifications
        """
        cross_refs = {}

        # Thread cross-references
        if part.thread_spec:
            cross_refs["thread"] = self._thread_normalizer.get_equivalents(
                part.thread_spec
            )

        # Material cross-references
        if part.material:
            cross_refs["material"] = self._material_normalizer.get_equivalents(
                part.material
            )

        return cross_refs

    async def _publish_ingestion_event(self, result: PipelineRun) -> None:
        """Publish ingestion completion to message bus."""
        if not self.message_bus:
            return

        message = {
            "type": "DATA",
            "sender": self.AGENT_ID,
            "topic": self.config.topic_data_ingestion,
            "payload": {
                "run_id": result.run_id,
                "parts_accepted": result.total_parts_accepted,
                "sources": result.sources,
                "timestamp": datetime.now().isoformat(),
            },
        }

        await self.message_bus.publish(
            self.config.topic_data_ingestion,
            message,
        )

        logger.info(f"Published ingestion event: {result.total_parts_accepted} parts")

    async def _continuous_ingestion_loop(self) -> None:
        """Background loop for continuous ingestion."""
        logger.info(
            f"Starting continuous ingestion loop "
            f"(interval: {self.config.ingestion_interval_seconds}s)"
        )

        while self._is_running:
            try:
                await asyncio.sleep(self.config.ingestion_interval_seconds)

                # Run ingestion from all registered sources
                await self.ingest()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Continuous ingestion error: {e}")
                await asyncio.sleep(60)  # Wait before retry

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        return {
            "agent_id": self.AGENT_ID,
            "agent_number": self.AGENT_NUMBER,
            "codename": self.AGENT_CODENAME,
            "name": self.AGENT_NAME,
            "role": self.AGENT_ROLE,
            "triad": self.AGENT_TRIAD,
            "status": self.status.value,
            "is_running": self._is_running,
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "statistics": {
                "total_parts_received": self.stats.total_parts_received,
                "total_parts_normalized": self.stats.total_parts_normalized,
                "total_parts_stored": self.stats.total_parts_stored,
                "total_duplicates_merged": self.stats.total_duplicates_merged,
                "total_rejected_quality": self.stats.total_rejected_quality,
                "last_ingestion": (
                    self.stats.last_ingestion_time.isoformat()
                    if self.stats.last_ingestion_time else None
                ),
                "sources_processed": list(self.stats.sources_processed),
            },
            "configuration": {
                "min_quality_score": self.config.min_quality_score,
                "duplicate_threshold": self.config.duplicate_threshold,
                "continuous_ingestion": self.config.enable_continuous_ingestion,
            },
            "scrapers": {
                name: {
                    "tier": scraper.SOURCE_TIER.name,
                    "stats": scraper.get_stats(),
                }
                for name, scraper in self._scrapers.items()
            },
        }

    async def handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle incoming messages from other agents.

        Args:
            message: Message from message bus

        Returns:
            Response message if applicable
        """
        msg_type = message.get("type")
        sender = message.get("sender")
        payload = message.get("payload", {})

        logger.debug(f"Received message from {sender}: {msg_type}")

        if msg_type == "QUERY":
            # Handle queries from other agents
            query_type = payload.get("query_type")

            if query_type == "part_lookup":
                upc_id = payload.get("upc_id")
                part = await self.get_part(upc_id)
                return {
                    "type": "RESPONSE",
                    "sender": self.AGENT_ID,
                    "payload": {
                        "found": part is not None,
                        "part": part.to_dict() if part else None,
                    },
                }

            elif query_type == "search":
                query = payload.get("query", "")
                parts = await self.search(query)
                return {
                    "type": "RESPONSE",
                    "sender": self.AGENT_ID,
                    "payload": {
                        "count": len(parts),
                        "parts": [p.to_dict() for p in parts[:10]],
                    },
                }

            elif query_type == "cross_reference":
                part_data = payload.get("part")
                if part_data:
                    part = ScrapedPart(**part_data)
                    refs = await self.get_cross_references(part)
                    return {
                        "type": "RESPONSE",
                        "sender": self.AGENT_ID,
                        "payload": {"cross_references": refs},
                    }

        elif msg_type == "DATA":
            # Handle incoming data from GARDENER (community contributions)
            # or BRIDGE (external integrations)
            if sender in ["agent_8_gardener", "agent_9_bridge"]:
                part_data = payload.get("part")
                if part_data:
                    part = await self.ingest_part(part_data)
                    return {
                        "type": "RESPONSE",
                        "sender": self.AGENT_ID,
                        "payload": {
                            "accepted": True,
                            "upc_id": part.upc_id,
                            "quality_score": part.quality_score,
                        },
                    }

        return None


# =============================================================================
# Convenience Functions
# =============================================================================

async def create_archivist(
    config: Optional[ArchivistConfig] = None,
    message_bus: Optional[Any] = None,
) -> ArchivistAgent:
    """Create and start an ARCHIVIST agent."""
    archivist = ArchivistAgent(config=config, message_bus=message_bus)
    await archivist.start()
    return archivist


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "ArchivistAgent",
    "ArchivistConfig",
    "ArchivistStatus",
    "IngestionStats",
    "create_archivist",
]
