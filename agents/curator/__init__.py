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
    from agents.curator import CuratorAgent

    async def main():
        agent = CuratorAgent()
        result = await agent.ingest(categories=["socket_head_cap_screws"])
        print(f"Ingested {result.total_parts_accepted} parts")
        await agent.shutdown()

    # Or use the convenience function:
    from agents.curator import run_curator
    result = await run_curator(categories=["socket_head_cap_screws"])
"""

# Core agent
from .curator_agent import (
    CuratorAgent,
    CuratorConfig,
    AgentState,
    AgentMetrics,
    run_curator,
)

# Scraper framework
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

# Tier 1 Scrapers
from .scrapers.mcmaster_scraper import (
    McMasterScraper,
    McMasterCategory,
)

from .scrapers.grainger_scraper import (
    GraingerScraper,
    GraingerCategory,
)

# Normalizers
from .normalizers.thread_normalizer import (
    ThreadNormalizer,
    NormalizedThread,
    ThreadStandard,
    ThreadType,
    normalize_thread,
    threads_compatible,
)

from .normalizers.material_normalizer import (
    MaterialNormalizer,
    NormalizedMaterial,
    MaterialCategory,
    MaterialProperties,
    FinishType,
    normalize_material,
    materials_equivalent,
)

# Quality scoring
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

# Duplicate detection
from .quality.duplicate_detector import (
    DuplicateDetector,
    DuplicateMatch,
    DuplicateGroup,
    DuplicateConfidence,
    MatchFactor,
    find_duplicates,
    group_duplicates,
)

# Pipeline
from .pipelines.ingestion_pipeline import (
    IngestionPipeline,
    PipelineConfig,
    PipelineRun,
    PipelineStage,
    PipelineStatus,
    StageResult,
    run_ingestion,
)

# Storage
from .storage.part_repository import (
    StorageConfig,
    StoredPart,
    PartRepository,
    FileRepository,
    create_repository,
)


__version__ = "1.0.0"
__agent_id__ = "Agent_1"
__agent_name__ = "Data Curator"
__agent_codename__ = "ARCHIVIST"

__all__ = [
    # Core agent
    "CuratorAgent",
    "CuratorConfig",
    "AgentState",
    "AgentMetrics",
    "run_curator",
    # Scraper framework
    "BaseScraper",
    "ScrapedPart",
    "ScrapeResult",
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitStrategy",
    "RetryConfig",
    "ScraperTier",
    "ScraperRegistry",
    # Tier 1 scrapers
    "McMasterScraper",
    "McMasterCategory",
    "GraingerScraper",
    "GraingerCategory",
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
    # Storage
    "StorageConfig",
    "StoredPart",
    "PartRepository",
    "FileRepository",
    "create_repository",
]
