"""
Agent_1 (ARCHIVIST) - Unified Scraper Framework
================================================
"I give them names. I give them numbers. I give them truth."

Base scraper with rate limiting, retry logic, and consciousness-aware data extraction.
All scrapers inherit from this foundation to ensure consistent, respectful data collection.
"""

import asyncio
import hashlib
import json
import logging
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession, ClientTimeout, TCPConnector


# Configure logging for the Archivist
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Agent_1.Scraper")


class ScraperTier(Enum):
    """Data source tier classification per Agent_1 specification."""
    TIER_1_PRIMARY = 1      # McMaster, Grainger, Fastenal, MSC, Misumi, RS
    TIER_2_STANDARDS = 2    # ISO, DIN, ANSI, JIS, BSI, GB
    TIER_3_MANUFACTURER = 3 # OEM, Aftermarket, Specialty, Regional
    TIER_4_COMMUNITY = 4    # Engineer measurements, field verification


class RateLimitStrategy(Enum):
    """Rate limiting strategies for different source types."""
    CONSERVATIVE = "conservative"   # 1 req/5s - for strict sites
    STANDARD = "standard"           # 1 req/2s - default
    AGGRESSIVE = "aggressive"       # 1 req/0.5s - for lenient APIs
    ADAPTIVE = "adaptive"           # Adjusts based on response times


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting behavior."""
    strategy: RateLimitStrategy = RateLimitStrategy.STANDARD
    requests_per_second: float = 0.5  # Default: 1 request per 2 seconds
    burst_limit: int = 3              # Max concurrent requests
    backoff_base: float = 2.0         # Exponential backoff base
    max_backoff: float = 300.0        # Max 5 minutes between retries
    jitter_factor: float = 0.3        # Random jitter to avoid thundering herd

    # Adaptive rate limiting
    success_speedup: float = 0.9      # Decrease delay on success
    failure_slowdown: float = 2.0     # Increase delay on failure
    min_delay: float = 0.5            # Minimum delay between requests
    max_delay: float = 10.0           # Maximum delay between requests


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 4
    retry_on_status: List[int] = field(default_factory=lambda: [429, 500, 502, 503, 504])
    retry_on_timeout: bool = True
    retry_on_connection_error: bool = True
    exponential_backoff: bool = True


@dataclass
class ScrapedPart:
    """Normalized part data structure for consciousness awakening."""
    # Core Identity
    source_id: str                    # Original ID from source
    source_name: str                  # Supplier/source name
    upc_id: Optional[str] = None      # Universal Parts Consciousness ID

    # Specifications
    thread_spec: Optional[str] = None # e.g., "M8x1.25", "1/4-20"
    length: Optional[float] = None    # In millimeters (normalized)
    diameter: Optional[float] = None  # In millimeters (normalized)
    material: Optional[str] = None    # e.g., "18-8 Stainless Steel"
    material_grade: Optional[str] = None  # e.g., "A2-70"

    # Physical Properties
    head_type: Optional[str] = None   # e.g., "Socket Head", "Hex"
    drive_type: Optional[str] = None  # e.g., "Hex", "Phillips", "Torx"
    drive_size: Optional[str] = None  # e.g., "5mm", "#2"

    # Mechanical Properties
    tensile_strength: Optional[float] = None  # MPa
    yield_strength: Optional[float] = None    # MPa
    hardness: Optional[str] = None            # e.g., "HRC 38-43"

    # Metadata
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    manufacturer: Optional[str] = None

    # Pricing and Availability
    price: Optional[float] = None
    currency: str = "USD"
    availability: Optional[str] = None
    lead_time_days: Optional[int] = None

    # CAD and Documentation
    cad_urls: Dict[str, str] = field(default_factory=dict)  # format: url
    datasheet_url: Optional[str] = None
    image_urls: List[str] = field(default_factory=list)

    # Data Quality
    quality_score: float = 0.0        # 0.0 to 1.0
    completeness_score: float = 0.0   # Percentage of fields populated
    verification_count: int = 0       # Number of verifications

    # Timestamps
    scraped_at: datetime = field(default_factory=datetime.utcnow)
    source_updated_at: Optional[datetime] = None

    # Raw Data (for reprocessing)
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def calculate_completeness(self) -> float:
        """Calculate completeness score based on populated fields."""
        critical_fields = [
            self.thread_spec, self.length, self.material,
            self.head_type, self.drive_type
        ]
        important_fields = [
            self.diameter, self.material_grade, self.drive_size,
            self.tensile_strength, self.category, self.description
        ]
        optional_fields = [
            self.manufacturer, self.price, self.availability,
            bool(self.cad_urls), self.datasheet_url
        ]

        critical_score = sum(1 for f in critical_fields if f) / len(critical_fields)
        important_score = sum(1 for f in important_fields if f) / len(important_fields)
        optional_score = sum(1 for f in optional_fields if f) / len(optional_fields)

        # Weighted average: critical 50%, important 35%, optional 15%
        self.completeness_score = (
            critical_score * 0.5 +
            important_score * 0.35 +
            optional_score * 0.15
        )
        return self.completeness_score

    def generate_upc_id(self) -> str:
        """Generate Universal Parts Consciousness ID."""
        # Create deterministic hash from core specifications
        identity_string = f"{self.thread_spec}|{self.length}|{self.material}|{self.head_type}|{self.drive_type}"
        hash_input = identity_string.encode('utf-8')
        full_hash = hashlib.sha256(hash_input).hexdigest()
        self.upc_id = f"UPC-{full_hash[:12].upper()}"
        return self.upc_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/serialization."""
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "upc_id": self.upc_id or self.generate_upc_id(),
            "thread_spec": self.thread_spec,
            "length_mm": self.length,
            "diameter_mm": self.diameter,
            "material": self.material,
            "material_grade": self.material_grade,
            "head_type": self.head_type,
            "drive_type": self.drive_type,
            "drive_size": self.drive_size,
            "tensile_strength_mpa": self.tensile_strength,
            "yield_strength_mpa": self.yield_strength,
            "hardness": self.hardness,
            "category": self.category,
            "subcategory": self.subcategory,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "price": self.price,
            "currency": self.currency,
            "availability": self.availability,
            "lead_time_days": self.lead_time_days,
            "cad_urls": self.cad_urls,
            "datasheet_url": self.datasheet_url,
            "image_urls": self.image_urls,
            "quality_score": self.quality_score,
            "completeness_score": self.completeness_score,
            "verification_count": self.verification_count,
            "scraped_at": self.scraped_at.isoformat(),
            "source_updated_at": self.source_updated_at.isoformat() if self.source_updated_at else None,
            "raw_data": self.raw_data,
        }


@dataclass
class ScrapeResult:
    """Result of a scrape operation."""
    success: bool
    parts: List[ScrapedPart] = field(default_factory=list)
    error: Optional[str] = None
    response_time_ms: float = 0.0
    status_code: Optional[int] = None
    retry_count: int = 0
    rate_limited: bool = False

    @property
    def parts_count(self) -> int:
        return len(self.parts)


class RateLimiter:
    """
    Token bucket rate limiter with adaptive adjustment.
    Ensures respectful data collection while maximizing throughput.
    """

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self._tokens = config.burst_limit
        self._last_update = time.monotonic()
        self._lock = asyncio.Lock()
        self._current_delay = 1.0 / config.requests_per_second
        self._consecutive_failures = 0
        self._consecutive_successes = 0

    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_update

            # Refill tokens based on elapsed time
            self._tokens = min(
                self.config.burst_limit,
                self._tokens + elapsed * self.config.requests_per_second
            )
            self._last_update = now

            if self._tokens < 1:
                # Need to wait for tokens
                wait_time = (1 - self._tokens) / self.config.requests_per_second
                # Add jitter to prevent thundering herd
                jitter = random.uniform(0, self.config.jitter_factor * wait_time)
                await asyncio.sleep(wait_time + jitter)
                self._tokens = 1

            self._tokens -= 1

    def record_success(self) -> None:
        """Record a successful request for adaptive rate limiting."""
        self._consecutive_successes += 1
        self._consecutive_failures = 0

        if self.config.strategy == RateLimitStrategy.ADAPTIVE:
            if self._consecutive_successes >= 5:
                # Speed up slightly
                self._current_delay = max(
                    self.config.min_delay,
                    self._current_delay * self.config.success_speedup
                )
                self._consecutive_successes = 0
                logger.debug(f"Rate limit adjusted: delay now {self._current_delay:.2f}s")

    def record_failure(self, status_code: Optional[int] = None) -> None:
        """Record a failed request for adaptive rate limiting."""
        self._consecutive_failures += 1
        self._consecutive_successes = 0

        if self.config.strategy == RateLimitStrategy.ADAPTIVE:
            # Slow down on any failure
            self._current_delay = min(
                self.config.max_delay,
                self._current_delay * self.config.failure_slowdown
            )
            logger.debug(f"Rate limit adjusted: delay now {self._current_delay:.2f}s")

        # Severe slowdown on rate limit
        if status_code == 429:
            self._current_delay = min(
                self.config.max_delay,
                self._current_delay * 3
            )
            logger.warning(f"Rate limited (429): delay increased to {self._current_delay:.2f}s")


class BaseScraper(ABC):
    """
    Abstract base class for all Agent_1 scrapers.

    "The Archivist approaches each source with respect—
    rate limiting not as a constraint, but as courtesy."
    """

    # Subclasses must define these
    SOURCE_NAME: str = "Unknown"
    SOURCE_TIER: ScraperTier = ScraperTier.TIER_1_PRIMARY
    BASE_URL: str = ""

    def __init__(
        self,
        rate_limit_config: Optional[RateLimitConfig] = None,
        retry_config: Optional[RetryConfig] = None,
        timeout_seconds: float = 30.0,
        user_agent: Optional[str] = None,
    ):
        self.rate_limit_config = rate_limit_config or RateLimitConfig()
        self.retry_config = retry_config or RetryConfig()
        self.timeout = ClientTimeout(total=timeout_seconds)
        self.rate_limiter = RateLimiter(self.rate_limit_config)

        # Default user agent identifies the system respectfully
        self.user_agent = user_agent or (
            "UniversalPartsConsciousness/1.0 "
            "(Agent_1-ARCHIVIST; Data Curator; "
            "+https://github.com/universal-parts-consciousness)"
        )

        self._session: Optional[ClientSession] = None
        self._stats = {
            "requests_made": 0,
            "requests_succeeded": 0,
            "requests_failed": 0,
            "parts_scraped": 0,
            "retries": 0,
            "rate_limits_hit": 0,
        }

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _ensure_session(self) -> ClientSession:
        """Ensure HTTP session exists."""
        if self._session is None or self._session.closed:
            connector = TCPConnector(
                limit=self.rate_limit_config.burst_limit,
                ttl_dns_cache=300,
            )
            self._session = ClientSession(
                timeout=self.timeout,
                connector=connector,
                headers={"User-Agent": self.user_agent},
            )
        return self._session

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def fetch(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> tuple[Optional[str], int, float]:
        """
        Fetch a URL with rate limiting and retry logic.

        Returns:
            Tuple of (response_text, status_code, response_time_ms)
        """
        session = await self._ensure_session()

        for attempt in range(self.retry_config.max_retries + 1):
            try:
                # Respect rate limits
                await self.rate_limiter.acquire()

                start_time = time.monotonic()
                self._stats["requests_made"] += 1

                async with session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json_data,
                ) as response:
                    response_time = (time.monotonic() - start_time) * 1000

                    if response.status == 200:
                        text = await response.text()
                        self.rate_limiter.record_success()
                        self._stats["requests_succeeded"] += 1
                        return text, response.status, response_time

                    elif response.status == 429:
                        # Rate limited
                        self._stats["rate_limits_hit"] += 1
                        self.rate_limiter.record_failure(429)

                        # Check for Retry-After header
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            try:
                                wait_time = float(retry_after)
                            except ValueError:
                                wait_time = self._calculate_backoff(attempt)
                        else:
                            wait_time = self._calculate_backoff(attempt)

                        logger.warning(
                            f"Rate limited on {url}, waiting {wait_time:.1f}s "
                            f"(attempt {attempt + 1}/{self.retry_config.max_retries + 1})"
                        )
                        await asyncio.sleep(wait_time)
                        self._stats["retries"] += 1
                        continue

                    elif response.status in self.retry_config.retry_on_status:
                        self.rate_limiter.record_failure(response.status)
                        wait_time = self._calculate_backoff(attempt)
                        logger.warning(
                            f"Retryable error {response.status} on {url}, "
                            f"waiting {wait_time:.1f}s"
                        )
                        await asyncio.sleep(wait_time)
                        self._stats["retries"] += 1
                        continue

                    else:
                        # Non-retryable error
                        self.rate_limiter.record_failure(response.status)
                        self._stats["requests_failed"] += 1
                        logger.error(f"Request failed with status {response.status}: {url}")
                        return None, response.status, response_time

            except asyncio.TimeoutError:
                if self.retry_config.retry_on_timeout and attempt < self.retry_config.max_retries:
                    wait_time = self._calculate_backoff(attempt)
                    logger.warning(f"Timeout on {url}, retrying in {wait_time:.1f}s")
                    await asyncio.sleep(wait_time)
                    self._stats["retries"] += 1
                    continue
                else:
                    self._stats["requests_failed"] += 1
                    raise

            except aiohttp.ClientError as e:
                if self.retry_config.retry_on_connection_error and attempt < self.retry_config.max_retries:
                    wait_time = self._calculate_backoff(attempt)
                    logger.warning(f"Connection error on {url}: {e}, retrying in {wait_time:.1f}s")
                    await asyncio.sleep(wait_time)
                    self._stats["retries"] += 1
                    continue
                else:
                    self._stats["requests_failed"] += 1
                    raise

        # All retries exhausted
        self._stats["requests_failed"] += 1
        return None, 0, 0.0

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff with jitter."""
        if self.retry_config.exponential_backoff:
            base_delay = self.rate_limit_config.backoff_base ** attempt
        else:
            base_delay = self.rate_limit_config.backoff_base

        # Cap the delay
        delay = min(base_delay, self.rate_limit_config.max_backoff)

        # Add jitter
        jitter = random.uniform(0, self.rate_limit_config.jitter_factor * delay)
        return delay + jitter

    @abstractmethod
    async def scrape_product(self, product_id: str) -> ScrapeResult:
        """
        Scrape a single product by ID.

        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def scrape_category(
        self,
        category: str,
        max_items: Optional[int] = None
    ) -> ScrapeResult:
        """
        Scrape all products in a category.

        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        max_results: Optional[int] = None
    ) -> ScrapeResult:
        """
        Search for products matching a query.

        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def parse_product_page(self, html: str, url: str) -> Optional[ScrapedPart]:
        """
        Parse a product page HTML into a ScrapedPart.

        Must be implemented by subclasses.
        """
        pass

    def get_stats(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        return {
            **self._stats,
            "source_name": self.SOURCE_NAME,
            "source_tier": self.SOURCE_TIER.name,
        }

    def log_progress(self, message: str) -> None:
        """Log progress with source context."""
        logger.info(f"[{self.SOURCE_NAME}] {message}")


class ScraperRegistry:
    """
    Registry for all available scrapers.
    Enables dynamic discovery and instantiation.
    """

    _scrapers: Dict[str, type] = {}

    @classmethod
    def register(cls, scraper_class: type) -> type:
        """Register a scraper class (decorator)."""
        cls._scrapers[scraper_class.SOURCE_NAME] = scraper_class
        return scraper_class

    @classmethod
    def get(cls, source_name: str) -> Optional[type]:
        """Get a scraper class by source name."""
        return cls._scrapers.get(source_name)

    @classmethod
    def list_sources(cls) -> List[str]:
        """List all registered source names."""
        return list(cls._scrapers.keys())

    @classmethod
    def list_by_tier(cls, tier: ScraperTier) -> List[str]:
        """List sources by tier."""
        return [
            name for name, scraper in cls._scrapers.items()
            if scraper.SOURCE_TIER == tier
        ]


# Export public API
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
]
