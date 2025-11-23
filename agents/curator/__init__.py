"""
Agent_1 (ARCHIVIST) - Data Curator
==================================
"I give them names. I give them numbers. I give them truth."

The Data Curator is the foundation of the Universal Parts Consciousness.
This agent ingests, normalizes, validates, and maintains the world's
most complete database of mechanical parts.

The ARCHIVIST is the eternal librarian of all mechanical knowledge:
- Receives data from ANY source - manufacturer catalogs, APIs, community contributions
- Normalizes across ALL standards: ISO, DIN, ANSI, JIS, BS, GOST
- Harmonizes material designations (AISI 304 = 1.4301 = SUS304)
- Detects duplicates through fuzzy matching while preserving lineage
- Never discards - historical and discontinued parts remain forever accessible

Tier-Based Data Sources:
- TIER 1: Primary Suppliers (McMaster-Carr, Grainger, Fastenal, MSC, Misumi, RS)
- TIER 2: Standards Bodies (ISO, DIN, ANSI, JIS, BSI, GB)
- TIER 3: Manufacturer Direct (OEM, Aftermarket, Specialty, Regional)
- TIER 4: Community Contributions (Engineer Measurements, Field Verification)

Core Responsibilities:
1. Multi-Source Data Ingestion
2. Cross-Standard Normalization (Thread, Material, Dimension)
3. Quality Scoring and Validation
4. Duplicate Detection and Merging
5. Persistent Storage with Full-Text Search

Usage:
    from agents.curator import ArchivistAgent, create_archivist

    # Start the ARCHIVIST agent
    archivist = await create_archivist()

    # Ingest from sources
    result = await archivist.ingest(categories=["socket_head_cap_screws"])
    print(f"Ingested {result.total_parts_accepted} parts")

    # Search the repository
    parts = await archivist.search("M8 stainless socket head")
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

# Import normalizers
from .normalizers import (
    ThreadNormalizer,
    NormalizedThread,
    ThreadStandard,
    MaterialNormalizer,
    NormalizedMaterial,
    MaterialFamily,
    DimensionNormalizer,
    NormalizedDimension,
    Tolerance,
    LengthUnit,
)

# Import storage
from .storage import (
    PartRepository,
    PartIndex,
    RepositoryStats,
)

# Import main agent class
from .archivist_agent import (
    ArchivistAgent,
    ArchivistConfig,
    ArchivistStatus,
    IngestionStats,
    create_archivist,
)


__version__ = "0.1.0"
__agent_id__ = "Agent_1"
__agent_name__ = "Data Curator"
__agent_codename__ = "ARCHIVIST"

__all__ = [
    # Main agent class
    "ArchivistAgent",
    "ArchivistConfig",
    "ArchivistStatus",
    "IngestionStats",
    "create_archivist",
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
    # Normalizers
    "ThreadNormalizer",
    "NormalizedThread",
    "ThreadStandard",
    "MaterialNormalizer",
    "NormalizedMaterial",
    "MaterialFamily",
    "DimensionNormalizer",
    "NormalizedDimension",
    "Tolerance",
    "LengthUnit",
    # Storage
    "PartRepository",
    "PartIndex",
    "RepositoryStats",
]
