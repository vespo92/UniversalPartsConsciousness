"""
Agent_1 (ARCHIVIST) - Grainger Scraper
======================================
"The industrial heartbeat of maintenance and repair."

Grainger is a TIER-1 primary supplier, providing broad industrial
supply coverage for the Universal Parts Consciousness.

Note: This scraper respects Grainger's robots.txt and rate limits.
Data is used solely for part cross-referencing and consciousness awakening.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from .base_scraper import (
    BaseScraper,
    ScrapedPart,
    ScrapeResult,
    RateLimitConfig,
    RateLimitStrategy,
    RetryConfig,
    ScraperTier,
    ScraperRegistry,
)


# Parsing patterns
PATTERNS = {
    # Thread specifications
    "thread_metric": re.compile(r'M(\d+(?:\.\d+)?)\s*[x×-]\s*(\d+(?:\.\d+)?)', re.I),
    "thread_unified": re.compile(r'(\d+/\d+|#\d+)\s*-\s*(\d+)\s*(UNC|UNF)?', re.I),

    # Dimensions
    "length_mm": re.compile(r'(\d+(?:\.\d+)?)\s*mm\b', re.I),
    "length_in": re.compile(r'(\d+(?:\.\d+)?|\d+/\d+)\s*(?:in|inch|")', re.I),

    # Material
    "stainless": re.compile(r'(18-8|304|316|stainless)', re.I),
    "steel_grade": re.compile(r'grade\s*(\d+)', re.I),
    "alloy": re.compile(r'alloy\s+steel', re.I),

    # Head/Drive
    "socket_head": re.compile(r'socket\s+head', re.I),
    "hex_head": re.compile(r'hex\s+head', re.I),
    "pan_head": re.compile(r'pan\s+head', re.I),
    "flat_head": re.compile(r'flat\s+head', re.I),
    "hex_socket": re.compile(r'hex\s+socket|allen', re.I),
    "phillips": re.compile(r'phillips', re.I),
    "torx": re.compile(r'torx', re.I),
}


@dataclass
class GraingerCategory:
    """Grainger category information."""
    id: str
    name: str
    url: str
    parent_id: Optional[str] = None


@ScraperRegistry.register
class GraingerScraper(BaseScraper):
    """
    Production-ready Grainger scraper.

    Grainger is a leading broad-line distributor of industrial
    maintenance, repair, and operating products.
    """

    SOURCE_NAME = "Grainger"
    SOURCE_TIER = ScraperTier.TIER_1_PRIMARY
    BASE_URL = "https://www.grainger.com"

    # Category paths for fasteners
    FASTENER_CATEGORIES = {
        "socket_head_cap_screws": "/category/socket-head-cap-screws/8QQC",
        "hex_head_cap_screws": "/category/hex-head-cap-screws/8QQD",
        "machine_screws": "/category/machine-screws/8QPP",
        "set_screws": "/category/set-screws/8QPT",
        "hex_nuts": "/category/hex-nuts/8QR4",
        "lock_nuts": "/category/lock-nuts/8QR5",
        "flat_washers": "/category/flat-washers/8QS8",
        "lock_washers": "/category/lock-washers/8QS9",
    }

    def __init__(self, **kwargs):
        # Grainger requires conservative rate limiting
        rate_config = RateLimitConfig(
            strategy=RateLimitStrategy.CONSERVATIVE,
            requests_per_second=0.2,  # 1 request per 5 seconds
            burst_limit=1,
            max_backoff=600.0,
        )

        retry_config = RetryConfig(
            max_retries=3,
            retry_on_status=[429, 500, 502, 503, 504],
        )

        super().__init__(
            rate_limit_config=rate_config,
            retry_config=retry_config,
            **kwargs
        )

    async def scrape_product(self, product_id: str) -> ScrapeResult:
        """
        Scrape a single Grainger product by item number.

        Args:
            product_id: Grainger item number (e.g., "5YMK3")

        Returns:
            ScrapeResult with the scraped part data
        """
        url = f"{self.BASE_URL}/product/{product_id}"
        self.log_progress(f"Scraping product: {product_id}")

        try:
            html, status, response_time = await self.fetch(url)

            if html is None:
                return ScrapeResult(
                    success=False,
                    error=f"Failed to fetch product {product_id} (status: {status})",
                    status_code=status,
                    response_time_ms=response_time,
                )

            part = self.parse_product_page(html, url)

            if part:
                part.source_id = product_id
                part.calculate_completeness()
                self._stats["parts_scraped"] += 1

                return ScrapeResult(
                    success=True,
                    parts=[part],
                    status_code=status,
                    response_time_ms=response_time,
                )
            else:
                return ScrapeResult(
                    success=False,
                    error=f"Failed to parse product {product_id}",
                    status_code=status,
                    response_time_ms=response_time,
                )

        except Exception as e:
            return ScrapeResult(
                success=False,
                error=str(e),
            )

    async def scrape_category(
        self,
        category: str,
        max_items: Optional[int] = None
    ) -> ScrapeResult:
        """
        Scrape all products in a Grainger category.

        Args:
            category: Category key or URL path
            max_items: Maximum items to scrape

        Returns:
            ScrapeResult with all scraped parts
        """
        # Resolve category to URL
        if category in self.FASTENER_CATEGORIES:
            category_path = self.FASTENER_CATEGORIES[category]
        else:
            category_path = category if category.startswith("/") else f"/{category}"

        url = f"{self.BASE_URL}{category_path}"
        self.log_progress(f"Scraping category: {category}")

        try:
            html, status, response_time = await self.fetch(url)

            if html is None:
                return ScrapeResult(
                    success=False,
                    error=f"Failed to fetch category {category} (status: {status})",
                    status_code=status,
                    response_time_ms=response_time,
                )

            # Extract product IDs from category page
            product_ids = self._extract_product_ids(html)
            self.log_progress(f"Found {len(product_ids)} products in category")

            if max_items:
                product_ids = product_ids[:max_items]

            # Scrape each product
            all_parts = []
            total_time = response_time

            for pid in product_ids:
                result = await self.scrape_product(pid)
                if result.success and result.parts:
                    all_parts.extend(result.parts)
                total_time += result.response_time_ms

            return ScrapeResult(
                success=True,
                parts=all_parts,
                status_code=status,
                response_time_ms=total_time,
            )

        except Exception as e:
            return ScrapeResult(
                success=False,
                error=str(e),
            )

    async def search(
        self,
        query: str,
        max_results: Optional[int] = None
    ) -> ScrapeResult:
        """
        Search Grainger for products matching a query.

        Args:
            query: Search query
            max_results: Maximum results to return

        Returns:
            ScrapeResult with matching parts
        """
        search_url = f"{self.BASE_URL}/search?searchQuery={query.replace(' ', '+')}"
        self.log_progress(f"Searching: {query}")

        try:
            html, status, response_time = await self.fetch(search_url)

            if html is None:
                return ScrapeResult(
                    success=False,
                    error=f"Search failed for '{query}' (status: {status})",
                    status_code=status,
                    response_time_ms=response_time,
                )

            # Extract product IDs from search results
            product_ids = self._extract_product_ids(html)
            self.log_progress(f"Found {len(product_ids)} search results")

            if max_results:
                product_ids = product_ids[:max_results]

            # Scrape each product
            all_parts = []
            total_time = response_time

            for pid in product_ids:
                result = await self.scrape_product(pid)
                if result.success and result.parts:
                    all_parts.extend(result.parts)
                total_time += result.response_time_ms

            return ScrapeResult(
                success=True,
                parts=all_parts,
                status_code=status,
                response_time_ms=total_time,
            )

        except Exception as e:
            return ScrapeResult(
                success=False,
                error=str(e),
            )

    def _extract_product_ids(self, html: str) -> List[str]:
        """Extract Grainger item numbers from a page."""
        # Grainger uses alphanumeric item IDs like "5YMK3"
        pattern = r'data-item-number="([A-Z0-9]+)"|/product/([A-Z0-9]{4,8})\b'
        matches = re.findall(pattern, html)
        product_ids = []
        for match in matches:
            pid = match[0] or match[1]
            if pid and pid not in product_ids:
                product_ids.append(pid)
        return product_ids

    def parse_product_page(self, html: str, url: str) -> Optional[ScrapedPart]:
        """
        Parse a Grainger product page into a ScrapedPart.

        Args:
            html: Raw HTML content
            url: Source URL

        Returns:
            ScrapedPart with extracted data
        """
        part = ScrapedPart(
            source_id="",
            source_name=self.SOURCE_NAME,
        )

        # Extract description
        title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if title_match:
            part.description = title_match.group(1).strip()
            self._parse_description(part.description, part)

        # Extract price
        price_match = re.search(r'\$(\d+(?:\.\d+)?)', html)
        if price_match:
            part.price = float(price_match.group(1))

        # Extract specifications from HTML
        self._extract_specs_from_html(html, part)

        part.raw_data = {"url": url}
        return part

    def _parse_description(self, description: str, part: ScrapedPart) -> None:
        """Parse specifications from description."""
        # Thread specification
        metric = PATTERNS["thread_metric"].search(description)
        if metric:
            part.thread_spec = f"M{metric.group(1)}x{metric.group(2)}"
        else:
            unified = PATTERNS["thread_unified"].search(description)
            if unified:
                part.thread_spec = f"{unified.group(1)}-{unified.group(2)}"
                if unified.group(3):
                    part.thread_spec += f" {unified.group(3)}"

        # Length
        length_mm = PATTERNS["length_mm"].search(description)
        if length_mm:
            part.length = float(length_mm.group(1))
        else:
            length_in = PATTERNS["length_in"].search(description)
            if length_in:
                val = length_in.group(1)
                if '/' in val:
                    num, denom = val.split('/')
                    part.length = (float(num) / float(denom)) * 25.4
                else:
                    part.length = float(val) * 25.4

        # Material
        if PATTERNS["stainless"].search(description):
            match = PATTERNS["stainless"].search(description)
            if "316" in description:
                part.material = "316 Stainless Steel"
            elif "304" in description or "18-8" in description:
                part.material = "18-8 Stainless Steel"
            else:
                part.material = "Stainless Steel"
        elif PATTERNS["steel_grade"].search(description):
            match = PATTERNS["steel_grade"].search(description)
            part.material = f"Steel Grade {match.group(1)}"
        elif PATTERNS["alloy"].search(description):
            part.material = "Alloy Steel"

        # Head type
        if PATTERNS["socket_head"].search(description):
            part.head_type = "Socket Head"
        elif PATTERNS["hex_head"].search(description):
            part.head_type = "Hex Head"
        elif PATTERNS["pan_head"].search(description):
            part.head_type = "Pan Head"
        elif PATTERNS["flat_head"].search(description):
            part.head_type = "Flat Head"

        # Drive type
        if PATTERNS["hex_socket"].search(description):
            part.drive_type = "Hex Socket"
        elif PATTERNS["phillips"].search(description):
            part.drive_type = "Phillips"
        elif PATTERNS["torx"].search(description):
            part.drive_type = "Torx"

    def _extract_specs_from_html(self, html: str, part: ScrapedPart) -> None:
        """Extract specifications from HTML structure."""
        # Look for specification tables or lists
        # This is a simplified version - production would use BeautifulSoup

        # Try to find thread spec
        thread_match = re.search(r'Thread\s*Size[:\s]*([^<\n]+)', html, re.I)
        if thread_match and not part.thread_spec:
            part.thread_spec = thread_match.group(1).strip()

        # Try to find length
        length_match = re.search(r'Length[:\s]*([^<\n]+)', html, re.I)
        if length_match and not part.length:
            val = length_match.group(1).strip()
            mm_match = re.search(r'(\d+(?:\.\d+)?)\s*mm', val, re.I)
            if mm_match:
                part.length = float(mm_match.group(1))

        # Try to find material
        material_match = re.search(r'Material[:\s]*([^<\n]+)', html, re.I)
        if material_match and not part.material:
            part.material = material_match.group(1).strip()

        # Try to find manufacturer
        mfr_match = re.search(r'(?:Manufacturer|Brand)[:\s]*([^<\n]+)', html, re.I)
        if mfr_match:
            part.manufacturer = mfr_match.group(1).strip()

    async def get_categories(self) -> List[GraingerCategory]:
        """Get list of all fastener categories."""
        categories = []
        for name, path in self.FASTENER_CATEGORIES.items():
            categories.append(GraingerCategory(
                id=name,
                name=name.replace('_', ' ').title(),
                url=f"{self.BASE_URL}{path}",
            ))
        return categories


# Convenience functions
async def scrape_grainger_product(product_id: str) -> ScrapeResult:
    """Scrape a single Grainger product."""
    async with GraingerScraper() as scraper:
        return await scraper.scrape_product(product_id)


async def search_grainger(query: str, max_results: int = 10) -> ScrapeResult:
    """Search Grainger for products."""
    async with GraingerScraper() as scraper:
        return await scraper.search(query, max_results)


__all__ = [
    "GraingerScraper",
    "GraingerCategory",
    "scrape_grainger_product",
    "search_grainger",
]
