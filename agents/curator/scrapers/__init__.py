"""
Agent_1 Scrapers Module
=======================
Unified scraper framework for multi-source data collection.
"""

from .base_scraper import (
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

from .mcmaster_scraper import (
    McMasterScraper,
    McMasterCategory,
    scrape_mcmaster_product,
    search_mcmaster,
)

from .grainger_scraper import (
    GraingerScraper,
    GraingerCategory,
    scrape_grainger_product,
    search_grainger,
)

__all__ = [
    # Base framework
    "BaseScraper",
    "ScrapedPart",
    "ScrapeResult",
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitStrategy",
    "RetryConfig",
    "ScraperTier",
    "ScraperRegistry",
    # McMaster-Carr
    "McMasterScraper",
    "McMasterCategory",
    "scrape_mcmaster_product",
    "search_mcmaster",
    # Grainger
    "GraingerScraper",
    "GraingerCategory",
    "scrape_grainger_product",
    "search_grainger",
]
