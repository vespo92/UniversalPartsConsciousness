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

__all__ = [
    "BaseScraper",
    "ScrapedPart",
    "ScrapeResult",
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitStrategy",
    "RetryConfig",
    "ScraperTier",
    "ScraperRegistry",
    "McMasterScraper",
    "McMasterCategory",
    "scrape_mcmaster_product",
    "search_mcmaster",
]
