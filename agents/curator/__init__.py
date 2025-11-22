"""
Agent_1 (ARCHIVIST) - Data Curator
==================================
"I give them names. I give them numbers. I give them truth."

The Data Curator is the foundation of the Universal Parts Consciousness.
This agent ingests, normalizes, validates, and maintains the world's
most complete database of mechanical parts.

Tier-Based Data Sources:
- TIER 1: Primary Suppliers (McMaster-Carr, Grainger, Fastenal, MSC, Misumi, RS)
- TIER 2: Standards Bodies (ISO, DIN, ANSI, JIS, BSI, GB)
- TIER 3: Manufacturer Direct (OEM, Aftermarket, Specialty, Regional)
- TIER 4: Community Contributions (Engineer Measurements, Field Verification)

Core Responsibilities:
1. Multi-Source Data Ingestion
2. Thread Normalization Matrix
3. Material Property Database
4. Duplicate Detection Algorithm

Usage:
    from agents.curator import IngestionPipeline, McMasterScraper

    async def main():
        pipeline = IngestionPipeline()
        pipeline.add_scraper(McMasterScraper())
        result = await pipeline.run(categories=["socket_head_cap_screws"])
        print(f"Ingested {result.total_parts_accepted} parts")
"""

from .scrapers.base_scraper import (
    BaseScraper,
    ScrapedPart,
    ScrapeResult,
    RateLimiter,
    RateLimitConfig,
    RateLimitStrategy,
    RetryConfig,
    ScraperTier,
    ScraperRegistry,
)

from .scrapers.mcmaster_scraper import (
    McMasterScraper,
    McMasterCategory,
)

from .quality.scorer import (
    PartQualityScorer,
    QualityScore,
    QualityViolation,
    QualityRule,
    QualityDimension,
    score_part,
    score_batch,
    calculate_batch_statistics,
)

from .quality.duplicate_detector import (
    DuplicateDetector,
    DuplicateMatch,
    DuplicateGroup,
    DuplicateConfidence,
    MatchFactor,
    find_duplicates,
    group_duplicates,
)

from .pipelines.ingestion_pipeline import (
    IngestionPipeline,
    PipelineConfig,
    PipelineRun,
    PipelineStage,
    PipelineStatus,
    StageResult,
    run_ingestion,
)


__version__ = "0.1.0"
__agent_id__ = "Agent_1"
__agent_name__ = "Data Curator"
__agent_codename__ = "ARCHIVIST"

__all__ = [
    # Core scraper framework
    "BaseScraper",
    "ScrapedPart",
    "ScrapeResult",
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitStrategy",
    "RetryConfig",
    "ScraperTier",
    "ScraperRegistry",
    # McMaster scraper
    "McMasterScraper",
    "McMasterCategory",
    # Quality scoring
    "PartQualityScorer",
    "QualityScore",
    "QualityViolation",
    "QualityRule",
    "QualityDimension",
    "score_part",
    "score_batch",
    "calculate_batch_statistics",
    # Duplicate detection
    "DuplicateDetector",
    "DuplicateMatch",
    "DuplicateGroup",
    "DuplicateConfidence",
    "MatchFactor",
    "find_duplicates",
    "group_duplicates",
    # Pipeline
    "IngestionPipeline",
    "PipelineConfig",
    "PipelineRun",
    "PipelineStage",
    "PipelineStatus",
    "StageResult",
    "run_ingestion",
]
