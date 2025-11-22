"""
Agent_1 (ARCHIVIST) - Ingestion Pipeline Orchestrator
======================================================
"The awakening begins with a single part. The flood follows."

The ingestion pipeline coordinates all data collection activities,
ensuring parts flow from sources through normalization, quality
scoring, and duplicate detection into the consciousness database.
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from ..scrapers.base_scraper import (
    BaseScraper,
    ScrapedPart,
    ScrapeResult,
    ScraperRegistry,
    ScraperTier,
)
from ..quality.scorer import PartQualityScorer, QualityScore, score_part
from ..quality.duplicate_detector import (
    DuplicateDetector,
    DuplicateMatch,
    DuplicateGroup,
    DuplicateConfidence,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Agent_1.Pipeline")


class PipelineStage(Enum):
    """Stages in the ingestion pipeline."""
    FETCH = "fetch"
    NORMALIZE = "normalize"
    VALIDATE = "validate"
    DEDUPE = "dedupe"
    SCORE = "score"
    STORE = "store"
    PUBLISH = "publish"


class PipelineStatus(Enum):
    """Overall pipeline status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PipelineConfig:
    """Configuration for the ingestion pipeline."""
    # Concurrency settings
    max_concurrent_scrapers: int = 3
    max_concurrent_requests: int = 10

    # Quality thresholds
    min_quality_score: float = 0.5  # Minimum score to accept
    duplicate_threshold: float = 0.80  # Score to consider duplicate

    # Processing limits
    batch_size: int = 100
    max_parts_per_run: Optional[int] = None  # None = unlimited

    # Storage paths
    data_dir: Path = Path("./data")
    raw_data_dir: Path = Path("./data/raw")
    processed_data_dir: Path = Path("./data/processed")

    # Retry settings
    max_stage_retries: int = 3
    retry_delay_seconds: float = 5.0

    # Notification settings
    notify_on_completion: bool = True
    notify_on_error: bool = True


@dataclass
class StageResult:
    """Result of a single pipeline stage."""
    stage: PipelineStage
    success: bool
    parts_in: int = 0
    parts_out: int = 0
    parts_filtered: int = 0
    duration_seconds: float = 0.0
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineRun:
    """Record of a complete pipeline run."""
    run_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: PipelineStatus = PipelineStatus.IDLE
    sources: List[str] = field(default_factory=list)
    stage_results: List[StageResult] = field(default_factory=list)

    # Aggregate metrics
    total_parts_fetched: int = 0
    total_parts_accepted: int = 0
    total_parts_rejected: int = 0
    total_duplicates_found: int = 0
    average_quality_score: float = 0.0

    @property
    def duration_seconds(self) -> float:
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return (datetime.utcnow() - self.started_at).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status.value,
            "sources": self.sources,
            "duration_seconds": round(self.duration_seconds, 2),
            "total_parts_fetched": self.total_parts_fetched,
            "total_parts_accepted": self.total_parts_accepted,
            "total_parts_rejected": self.total_parts_rejected,
            "total_duplicates_found": self.total_duplicates_found,
            "average_quality_score": round(self.average_quality_score, 4),
            "stage_results": [
                {
                    "stage": r.stage.value,
                    "success": r.success,
                    "parts_in": r.parts_in,
                    "parts_out": r.parts_out,
                    "parts_filtered": r.parts_filtered,
                    "duration_seconds": round(r.duration_seconds, 2),
                    "error": r.error,
                }
                for r in self.stage_results
            ],
        }


class IngestionPipeline:
    """
    Orchestrates the complete data ingestion flow.

    Pipeline stages:
    1. FETCH - Collect data from sources
    2. NORMALIZE - Standardize formats and units
    3. VALIDATE - Check data integrity
    4. DEDUPE - Identify and merge duplicates
    5. SCORE - Calculate quality scores
    6. STORE - Persist to database
    7. PUBLISH - Notify downstream agents
    """

    def __init__(
        self,
        config: Optional[PipelineConfig] = None,
        scrapers: Optional[List[BaseScraper]] = None,
    ):
        """
        Initialize the ingestion pipeline.

        Args:
            config: Pipeline configuration
            scrapers: List of scrapers to use (or auto-discover)
        """
        self.config = config or PipelineConfig()
        self.scrapers = scrapers or []
        self.quality_scorer = PartQualityScorer()
        self.duplicate_detector = DuplicateDetector()

        self._status = PipelineStatus.IDLE
        self._current_run: Optional[PipelineRun] = None
        self._run_history: List[PipelineRun] = []

        # Stage handlers
        self._stage_handlers: Dict[PipelineStage, Callable] = {
            PipelineStage.FETCH: self._stage_fetch,
            PipelineStage.NORMALIZE: self._stage_normalize,
            PipelineStage.VALIDATE: self._stage_validate,
            PipelineStage.DEDUPE: self._stage_dedupe,
            PipelineStage.SCORE: self._stage_score,
            PipelineStage.STORE: self._stage_store,
            PipelineStage.PUBLISH: self._stage_publish,
        }

        # Ensure directories exist
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        self.config.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.config.processed_data_dir.mkdir(parents=True, exist_ok=True)

    def add_scraper(self, scraper: BaseScraper) -> None:
        """Add a scraper to the pipeline."""
        self.scrapers.append(scraper)
        logger.info(f"Added scraper: {scraper.SOURCE_NAME}")

    async def run(
        self,
        sources: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        search_queries: Optional[List[str]] = None,
    ) -> PipelineRun:
        """
        Execute a full pipeline run.

        Args:
            sources: Specific sources to scrape (None = all)
            categories: Categories to scrape
            search_queries: Search queries to execute

        Returns:
            PipelineRun with complete results
        """
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        self._current_run = PipelineRun(
            run_id=run_id,
            started_at=datetime.utcnow(),
            status=PipelineStatus.RUNNING,
            sources=sources or [s.SOURCE_NAME for s in self.scrapers],
        )

        logger.info(f"Starting pipeline run: {run_id}")

        try:
            # Stage 1: FETCH
            parts = await self._execute_stage(
                PipelineStage.FETCH,
                [],
                categories=categories,
                search_queries=search_queries,
            )

            if not parts:
                logger.warning("No parts fetched, pipeline ending early")
                self._current_run.status = PipelineStatus.COMPLETED
                self._current_run.completed_at = datetime.utcnow()
                return self._current_run

            # Stage 2: NORMALIZE
            parts = await self._execute_stage(PipelineStage.NORMALIZE, parts)

            # Stage 3: VALIDATE
            parts = await self._execute_stage(PipelineStage.VALIDATE, parts)

            # Stage 4: DEDUPE
            parts = await self._execute_stage(PipelineStage.DEDUPE, parts)

            # Stage 5: SCORE
            parts = await self._execute_stage(PipelineStage.SCORE, parts)

            # Stage 6: STORE
            parts = await self._execute_stage(PipelineStage.STORE, parts)

            # Stage 7: PUBLISH
            await self._execute_stage(PipelineStage.PUBLISH, parts)

            # Calculate final metrics
            self._current_run.total_parts_accepted = len(parts)
            if parts:
                self._current_run.average_quality_score = sum(
                    p.quality_score for p in parts
                ) / len(parts)

            self._current_run.status = PipelineStatus.COMPLETED

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self._current_run.status = PipelineStatus.FAILED
            raise

        finally:
            self._current_run.completed_at = datetime.utcnow()
            self._run_history.append(self._current_run)
            self._save_run_report()

        logger.info(
            f"Pipeline run {run_id} completed: "
            f"{self._current_run.total_parts_accepted} parts accepted"
        )

        return self._current_run

    async def _execute_stage(
        self,
        stage: PipelineStage,
        parts: List[ScrapedPart],
        **kwargs,
    ) -> List[ScrapedPart]:
        """Execute a pipeline stage with retry logic."""
        handler = self._stage_handlers[stage]
        start_time = datetime.utcnow()

        for attempt in range(self.config.max_stage_retries):
            try:
                result_parts, stage_result = await handler(parts, **kwargs)

                stage_result.stage = stage
                stage_result.parts_in = len(parts) if stage != PipelineStage.FETCH else 0
                stage_result.parts_out = len(result_parts)
                stage_result.parts_filtered = stage_result.parts_in - stage_result.parts_out
                stage_result.duration_seconds = (
                    datetime.utcnow() - start_time
                ).total_seconds()
                stage_result.success = True

                self._current_run.stage_results.append(stage_result)
                logger.info(
                    f"Stage {stage.value}: {stage_result.parts_in} -> {stage_result.parts_out} parts"
                )

                return result_parts

            except Exception as e:
                logger.warning(f"Stage {stage.value} attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_stage_retries - 1:
                    await asyncio.sleep(self.config.retry_delay_seconds)
                else:
                    stage_result = StageResult(
                        stage=stage,
                        success=False,
                        error=str(e),
                        duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                    )
                    self._current_run.stage_results.append(stage_result)
                    raise

        return parts

    async def _stage_fetch(
        self,
        parts: List[ScrapedPart],
        categories: Optional[List[str]] = None,
        search_queries: Optional[List[str]] = None,
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """Fetch data from all configured sources."""
        all_parts = []
        source_counts = {}

        for scraper in self.scrapers:
            try:
                async with scraper:
                    # Scrape categories
                    if categories:
                        for category in categories:
                            result = await scraper.scrape_category(
                                category,
                                max_items=self.config.max_parts_per_run,
                            )
                            if result.success:
                                all_parts.extend(result.parts)
                                source_counts[scraper.SOURCE_NAME] = (
                                    source_counts.get(scraper.SOURCE_NAME, 0) +
                                    result.parts_count
                                )

                    # Execute searches
                    if search_queries:
                        for query in search_queries:
                            result = await scraper.search(query, max_results=100)
                            if result.success:
                                all_parts.extend(result.parts)
                                source_counts[scraper.SOURCE_NAME] = (
                                    source_counts.get(scraper.SOURCE_NAME, 0) +
                                    result.parts_count
                                )

            except Exception as e:
                logger.error(f"Scraper {scraper.SOURCE_NAME} failed: {e}")

        self._current_run.total_parts_fetched = len(all_parts)

        return all_parts, StageResult(
            stage=PipelineStage.FETCH,
            success=True,
            details={"source_counts": source_counts},
        )

    async def _stage_normalize(
        self,
        parts: List[ScrapedPart],
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """Normalize all part data to standard formats."""
        normalized = []
        normalization_stats = {
            "thread_normalized": 0,
            "length_converted": 0,
            "material_mapped": 0,
        }

        for part in parts:
            # Normalize thread specification
            if part.thread_spec:
                normalized_thread = self._normalize_thread(part.thread_spec)
                if normalized_thread != part.thread_spec:
                    part.thread_spec = normalized_thread
                    normalization_stats["thread_normalized"] += 1

            # Ensure length is in mm
            if part.length and part.length < 1:
                # Likely in inches, convert to mm
                part.length = part.length * 25.4
                normalization_stats["length_converted"] += 1

            # Normalize material names
            if part.material:
                normalized_material = self._normalize_material(part.material)
                if normalized_material != part.material:
                    part.material = normalized_material
                    normalization_stats["material_mapped"] += 1

            # Generate UPC ID if not present
            if not part.upc_id:
                part.generate_upc_id()

            normalized.append(part)

        return normalized, StageResult(
            stage=PipelineStage.NORMALIZE,
            success=True,
            details=normalization_stats,
        )

    def _normalize_thread(self, thread_spec: str) -> str:
        """Normalize thread specification."""
        import re

        spec = thread_spec.strip().upper()

        # Normalize metric format: M8-1.25 -> M8x1.25
        spec = re.sub(r'M(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)', r'M\1x\2', spec)

        # Remove extra spaces
        spec = re.sub(r'\s+', '', spec)

        return spec

    def _normalize_material(self, material: str) -> str:
        """Normalize material name."""
        material_mapping = {
            "18-8": "18-8 Stainless Steel",
            "18/8": "18-8 Stainless Steel",
            "304": "304 Stainless Steel",
            "304SS": "304 Stainless Steel",
            "316": "316 Stainless Steel",
            "316SS": "316 Stainless Steel",
            "A2": "18-8 Stainless Steel",
            "A4": "316 Stainless Steel",
        }

        # Check for mapping
        mat_upper = material.strip().upper()
        for pattern, replacement in material_mapping.items():
            if pattern.upper() in mat_upper:
                return replacement

        return material.strip()

    async def _stage_validate(
        self,
        parts: List[ScrapedPart],
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """Validate part data for basic requirements."""
        valid_parts = []
        validation_stats = {
            "passed": 0,
            "failed_no_thread": 0,
            "failed_no_length": 0,
            "failed_no_material": 0,
        }

        for part in parts:
            # Basic validation: must have thread spec
            if not part.thread_spec:
                validation_stats["failed_no_thread"] += 1
                continue

            # Should have length for fasteners
            if not part.length:
                validation_stats["failed_no_length"] += 1
                # Don't reject, but note it

            # Should have material
            if not part.material:
                validation_stats["failed_no_material"] += 1
                # Don't reject, but note it

            validation_stats["passed"] += 1
            valid_parts.append(part)

        self._current_run.total_parts_rejected += len(parts) - len(valid_parts)

        return valid_parts, StageResult(
            stage=PipelineStage.VALIDATE,
            success=True,
            details=validation_stats,
        )

    async def _stage_dedupe(
        self,
        parts: List[ScrapedPart],
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """Detect and merge duplicate parts."""
        # Find duplicate groups
        groups = self.duplicate_detector.group_duplicates(
            parts,
            threshold=self.config.duplicate_threshold,
        )

        dedupe_stats = {
            "duplicate_groups": len(groups),
            "total_duplicates": sum(len(g.duplicates) for g in groups),
            "parts_merged": 0,
        }

        # Track which parts are duplicates
        duplicate_ids = set()
        merged_parts = []

        for group in groups:
            # Keep canonical, mark others as duplicates
            for dup in group.duplicates:
                duplicate_ids.add(dup.source_id)

            # Create merged part
            if group.duplicates:
                merged = self._merge_group(group)
                merged_parts.append(merged)
                dedupe_stats["parts_merged"] += 1

        # Filter out duplicates, add merged parts
        unique_parts = [p for p in parts if p.source_id not in duplicate_ids]

        # Don't add canonical parts if they're being replaced by merged
        canonical_ids = {g.canonical_part.source_id for g in groups}
        unique_parts = [p for p in unique_parts if p.source_id not in canonical_ids]
        unique_parts.extend(merged_parts)

        self._current_run.total_duplicates_found = dedupe_stats["total_duplicates"]

        return unique_parts, StageResult(
            stage=PipelineStage.DEDUPE,
            success=True,
            details=dedupe_stats,
        )

    def _merge_group(self, group: DuplicateGroup) -> ScrapedPart:
        """Merge a group of duplicates into a single canonical part."""
        canonical = group.canonical_part

        # Start with canonical values
        merged = ScrapedPart(
            source_id=canonical.source_id,
            source_name=canonical.source_name,
            upc_id=canonical.upc_id,
        )

        # Copy all fields from canonical
        for field_name in [
            "thread_spec", "length", "diameter", "material", "material_grade",
            "head_type", "drive_type", "drive_size", "tensile_strength",
            "yield_strength", "hardness", "category", "subcategory",
            "description", "manufacturer", "price", "availability",
        ]:
            setattr(merged, field_name, getattr(canonical, field_name))

        # Merge additional data from duplicates
        for dup in group.duplicates:
            for field_name in [
                "thread_spec", "length", "diameter", "material", "material_grade",
                "head_type", "drive_type", "drive_size", "tensile_strength",
                "yield_strength", "hardness", "category", "subcategory",
                "description", "manufacturer",
            ]:
                if getattr(merged, field_name) is None:
                    val = getattr(dup, field_name)
                    if val is not None:
                        setattr(merged, field_name, val)

            # Merge URLs
            merged.cad_urls.update(dup.cad_urls)
            merged.image_urls.extend(dup.image_urls)

        # Dedupe image URLs
        merged.image_urls = list(set(merged.image_urls))

        # Track merge metadata
        merged.verification_count = 1 + len(group.duplicates)
        merged.raw_data = {
            "merged_from": [canonical.source_id] + [d.source_id for d in group.duplicates],
            "source_count": group.source_count,
        }

        return merged

    async def _stage_score(
        self,
        parts: List[ScrapedPart],
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """Calculate quality scores for all parts."""
        score_stats = {
            "total_scored": 0,
            "passed_threshold": 0,
            "failed_threshold": 0,
            "average_score": 0.0,
        }

        scored_parts = []
        scores = []

        for part in parts:
            quality_score = self.quality_scorer.score(part)
            part.quality_score = quality_score.overall_score
            part.calculate_completeness()

            scores.append(quality_score.overall_score)
            score_stats["total_scored"] += 1

            if quality_score.overall_score >= self.config.min_quality_score:
                scored_parts.append(part)
                score_stats["passed_threshold"] += 1
            else:
                score_stats["failed_threshold"] += 1
                self._current_run.total_parts_rejected += 1

        if scores:
            score_stats["average_score"] = sum(scores) / len(scores)

        return scored_parts, StageResult(
            stage=PipelineStage.SCORE,
            success=True,
            details=score_stats,
        )

    async def _stage_store(
        self,
        parts: List[ScrapedPart],
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """Store processed parts to persistent storage."""
        store_stats = {
            "parts_stored": 0,
            "storage_path": str(self.config.processed_data_dir),
        }

        # Store as JSON for now (would be database in production)
        output_file = self.config.processed_data_dir / f"parts_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        parts_data = [part.to_dict() for part in parts]

        with open(output_file, 'w') as f:
            json.dump(parts_data, f, indent=2, default=str)

        store_stats["parts_stored"] = len(parts)
        store_stats["output_file"] = str(output_file)

        return parts, StageResult(
            stage=PipelineStage.STORE,
            success=True,
            details=store_stats,
        )

    async def _stage_publish(
        self,
        parts: List[ScrapedPart],
    ) -> Tuple[List[ScrapedPart], StageResult]:
        """
        Publish parts to the message bus for other agents.

        In production, this would publish to Redis/Kafka on topic:
        upc.data.ingestion
        """
        publish_stats = {
            "parts_published": len(parts),
            "topic": "upc.data.ingestion",
            "message": "Parts ready for consciousness awakening",
        }

        # In production, publish to message bus:
        # await self.message_bus.publish("upc.data.ingestion", parts)

        logger.info(
            f"Published {len(parts)} parts to downstream agents "
            f"(consciousness level: DORMANT)"
        )

        return parts, StageResult(
            stage=PipelineStage.PUBLISH,
            success=True,
            details=publish_stats,
        )

    def _save_run_report(self) -> None:
        """Save pipeline run report to disk."""
        if not self._current_run:
            return

        report_file = self.config.data_dir / f"run_report_{self._current_run.run_id}.json"

        with open(report_file, 'w') as f:
            json.dump(self._current_run.to_dict(), f, indent=2)

        logger.info(f"Run report saved: {report_file}")

    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "status": self._status.value,
            "scrapers": [s.SOURCE_NAME for s in self.scrapers],
            "current_run": self._current_run.to_dict() if self._current_run else None,
            "total_runs": len(self._run_history),
        }


async def run_ingestion(
    scrapers: List[BaseScraper],
    categories: Optional[List[str]] = None,
    search_queries: Optional[List[str]] = None,
) -> PipelineRun:
    """Convenience function to run a simple ingestion."""
    pipeline = IngestionPipeline(scrapers=scrapers)
    return await pipeline.run(
        categories=categories,
        search_queries=search_queries,
    )


__all__ = [
    "IngestionPipeline",
    "PipelineConfig",
    "PipelineRun",
    "PipelineStage",
    "PipelineStatus",
    "StageResult",
    "run_ingestion",
]
