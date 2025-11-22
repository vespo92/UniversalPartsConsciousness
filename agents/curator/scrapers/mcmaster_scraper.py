"""
Agent_1 (ARCHIVIST) - McMaster-Carr Scraper
============================================
"The primary oracle of industrial specifications."

McMaster-Carr is a TIER-1 primary supplier, providing the foundation
for fastener consciousness in the Universal Parts database.

Note: This scraper respects McMaster-Carr's robots.txt and rate limits.
Data is used solely for part cross-referencing and consciousness awakening.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse, parse_qs

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


# Thread specification patterns for parsing
THREAD_PATTERNS = {
    # Metric: M3x0.5, M8-1.25, M10 x 1.5
    "metric": re.compile(
        r'M(\d+(?:\.\d+)?)\s*[x×-]\s*(\d+(?:\.\d+)?)',
        re.IGNORECASE
    ),
    # Unified: 1/4-20, 1/4"-20, #10-24, #8-32
    "unified": re.compile(
        r'(?:(\d+/\d+)|#(\d+))\s*["\']?\s*-\s*(\d+)',
        re.IGNORECASE
    ),
    # Metric coarse (no pitch): M3, M8
    "metric_coarse": re.compile(
        r'\bM(\d+(?:\.\d+)?)\b(?!\s*[x×-])',
        re.IGNORECASE
    ),
}

# Length patterns
LENGTH_PATTERNS = {
    # Metric: 20mm, 25 mm, 30-mm
    "metric_mm": re.compile(
        r'(\d+(?:\.\d+)?)\s*-?\s*mm\b',
        re.IGNORECASE
    ),
    # Imperial: 1", 1-1/2", 3/4"
    "imperial_inch": re.compile(
        r'(\d+(?:-\d+/\d+)?|\d+/\d+)\s*["\']',
        re.IGNORECASE
    ),
}

# Material patterns
MATERIAL_PATTERNS = {
    "stainless_18_8": re.compile(r'18-8\s+stainless', re.IGNORECASE),
    "stainless_316": re.compile(r'316\s+stainless', re.IGNORECASE),
    "stainless_304": re.compile(r'304\s+stainless', re.IGNORECASE),
    "alloy_steel": re.compile(r'alloy\s+steel', re.IGNORECASE),
    "grade_8": re.compile(r'grade\s*8\b', re.IGNORECASE),
    "grade_5": re.compile(r'grade\s*5\b', re.IGNORECASE),
    "brass": re.compile(r'\bbrass\b', re.IGNORECASE),
    "bronze": re.compile(r'\bbronze\b', re.IGNORECASE),
    "aluminum": re.compile(r'\baluminum\b', re.IGNORECASE),
    "titanium": re.compile(r'\btitanium\b', re.IGNORECASE),
    "nylon": re.compile(r'\bnylon\b', re.IGNORECASE),
    "zinc_plated": re.compile(r'zinc[- ]plated', re.IGNORECASE),
    "black_oxide": re.compile(r'black\s*oxide', re.IGNORECASE),
}

# Head type patterns
HEAD_TYPE_PATTERNS = {
    "socket_head": re.compile(r'socket\s+head', re.IGNORECASE),
    "button_head": re.compile(r'button\s+head', re.IGNORECASE),
    "flat_head": re.compile(r'flat\s+head', re.IGNORECASE),
    "pan_head": re.compile(r'pan\s+head', re.IGNORECASE),
    "hex_head": re.compile(r'hex\s+head', re.IGNORECASE),
    "hex_flange": re.compile(r'hex\s+flange', re.IGNORECASE),
    "truss_head": re.compile(r'truss\s+head', re.IGNORECASE),
    "round_head": re.compile(r'round\s+head', re.IGNORECASE),
    "oval_head": re.compile(r'oval\s+head', re.IGNORECASE),
    "fillister": re.compile(r'fillister', re.IGNORECASE),
}

# Drive type patterns
DRIVE_TYPE_PATTERNS = {
    "hex_socket": re.compile(r'hex\s*socket|allen', re.IGNORECASE),
    "phillips": re.compile(r'phillips', re.IGNORECASE),
    "slotted": re.compile(r'slotted', re.IGNORECASE),
    "torx": re.compile(r'torx|star', re.IGNORECASE),
    "square": re.compile(r'square\s+drive|robertson', re.IGNORECASE),
    "combo": re.compile(r'combo|combination', re.IGNORECASE),
    "hex_external": re.compile(r'external\s+hex|\bhex\b(?!\s*socket)', re.IGNORECASE),
}


@dataclass
class McMasterCategory:
    """McMaster-Carr category information."""
    id: str
    name: str
    url: str
    parent_id: Optional[str] = None
    product_count: Optional[int] = None


@ScraperRegistry.register
class McMasterScraper(BaseScraper):
    """
    Production-ready McMaster-Carr scraper.

    McMaster-Carr provides the most comprehensive industrial supply
    catalog in North America. Their specifications become the foundation
    for fastener consciousness.
    """

    SOURCE_NAME = "McMaster-Carr"
    SOURCE_TIER = ScraperTier.TIER_1_PRIMARY
    BASE_URL = "https://www.mcmaster.com"

    # Category URLs for fasteners
    FASTENER_CATEGORIES = {
        "socket_head_cap_screws": "/screws/socket-head-cap-screws",
        "button_head_cap_screws": "/screws/button-head-socket-cap-screws",
        "flat_head_cap_screws": "/screws/flat-head-socket-cap-screws",
        "hex_head_cap_screws": "/hex-head-cap-screws",
        "machine_screws": "/machine-screws",
        "set_screws": "/set-screws",
        "hex_nuts": "/hex-nuts",
        "lock_nuts": "/locknuts",
        "washers": "/washers",
        "lock_washers": "/lock-washers",
    }

    def __init__(self, **kwargs):
        # McMaster requires conservative rate limiting
        rate_config = RateLimitConfig(
            strategy=RateLimitStrategy.CONSERVATIVE,
            requests_per_second=0.2,  # 1 request per 5 seconds
            burst_limit=1,
            max_backoff=600.0,  # 10 minutes max
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
        Scrape a single McMaster-Carr product by part number.

        Args:
            product_id: McMaster-Carr part number (e.g., "91290A113")

        Returns:
            ScrapeResult with the scraped part data
        """
        url = f"{self.BASE_URL}/{product_id}"
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
        Scrape all products in a McMaster-Carr category.

        Args:
            category: Category key (from FASTENER_CATEGORIES) or URL path
            max_items: Maximum items to scrape (None for all)

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
        Search McMaster-Carr for products matching a query.

        Args:
            query: Search query (e.g., "M8 socket head cap screw")
            max_results: Maximum results to return

        Returns:
            ScrapeResult with matching parts
        """
        # McMaster uses path-based search
        search_url = f"{self.BASE_URL}/{query.replace(' ', '-')}"
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
        """Extract McMaster-Carr product IDs from a page."""
        if BeautifulSoup is None:
            # Fallback regex extraction
            pattern = r'data-part-number="(\d{8}[A-Z]\d{3})"'
            matches = re.findall(pattern, html)
            if not matches:
                # Try alternate pattern
                pattern = r'/(\d{8}[A-Z]\d{3})\b'
                matches = re.findall(pattern, html)
            return list(set(matches))

        soup = BeautifulSoup(html, 'html.parser')
        product_ids = []

        # Look for product links
        for link in soup.find_all('a', href=True):
            href = link['href']
            # McMaster product IDs are typically like "91290A113"
            match = re.search(r'/(\d{8}[A-Z]\d{3})\b', href)
            if match:
                product_ids.append(match.group(1))

        # Also check data attributes
        for elem in soup.find_all(attrs={'data-part-number': True}):
            product_ids.append(elem['data-part-number'])

        return list(set(product_ids))

    def parse_product_page(self, html: str, url: str) -> Optional[ScrapedPart]:
        """
        Parse a McMaster-Carr product page into a ScrapedPart.

        Args:
            html: Raw HTML content
            url: Source URL

        Returns:
            ScrapedPart with extracted data, or None if parsing fails
        """
        if BeautifulSoup is None:
            return self._parse_product_regex(html, url)

        try:
            soup = BeautifulSoup(html, 'html.parser')
            part = ScrapedPart(
                source_id="",  # Will be set by caller
                source_name=self.SOURCE_NAME,
            )

            # Extract title/description
            title_elem = soup.find('h1') or soup.find(class_='product-title')
            if title_elem:
                part.description = title_elem.get_text(strip=True)
                self._parse_description(part.description, part)

            # Extract specifications table
            spec_table = soup.find('table', class_='specs') or soup.find('table')
            if spec_table:
                self._parse_spec_table(spec_table, part)

            # Extract price
            price_elem = soup.find(class_='price') or soup.find('span', {'data-price': True})
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                if price_match:
                    part.price = float(price_match.group(1).replace(',', ''))

            # Extract CAD model URLs
            part.cad_urls = self._extract_cad_urls(soup)

            # Extract images
            for img in soup.find_all('img', class_='product-image'):
                if img.get('src'):
                    part.image_urls.append(urljoin(url, img['src']))

            # Store raw data for reprocessing
            part.raw_data = {
                "url": url,
                "title": part.description,
                "html_length": len(html),
            }

            return part

        except Exception as e:
            self.log_progress(f"Parse error: {e}")
            return self._parse_product_regex(html, url)

    def _parse_product_regex(self, html: str, url: str) -> Optional[ScrapedPart]:
        """Fallback regex-based parsing when BeautifulSoup is unavailable."""
        part = ScrapedPart(
            source_id="",
            source_name=self.SOURCE_NAME,
        )

        # Extract title
        title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if title_match:
            part.description = title_match.group(1).strip()
            self._parse_description(part.description, part)

        # Extract price
        price_match = re.search(r'\$?([\d,]+\.?\d*)\s*(?:each|per|/)', html, re.IGNORECASE)
        if price_match:
            part.price = float(price_match.group(1).replace(',', ''))

        # Extract specifications from various patterns
        self._extract_specs_regex(html, part)

        part.raw_data = {"url": url}
        return part

    def _parse_description(self, description: str, part: ScrapedPart) -> None:
        """Parse thread, material, and type info from description."""
        # Thread specification
        for pattern_name, pattern in THREAD_PATTERNS.items():
            match = pattern.search(description)
            if match:
                if pattern_name == "metric":
                    part.thread_spec = f"M{match.group(1)}x{match.group(2)}"
                elif pattern_name == "unified":
                    if match.group(1):  # Fractional
                        part.thread_spec = f"{match.group(1)}-{match.group(3)}"
                    else:  # Numbered
                        part.thread_spec = f"#{match.group(2)}-{match.group(3)}"
                elif pattern_name == "metric_coarse":
                    part.thread_spec = f"M{match.group(1)}"
                break

        # Material
        for mat_name, pattern in MATERIAL_PATTERNS.items():
            if pattern.search(description):
                material_map = {
                    "stainless_18_8": "18-8 Stainless Steel",
                    "stainless_316": "316 Stainless Steel",
                    "stainless_304": "304 Stainless Steel",
                    "alloy_steel": "Alloy Steel",
                    "grade_8": "Alloy Steel Grade 8",
                    "grade_5": "Steel Grade 5",
                    "brass": "Brass",
                    "bronze": "Bronze",
                    "aluminum": "Aluminum",
                    "titanium": "Titanium",
                    "nylon": "Nylon",
                    "zinc_plated": "Zinc-Plated Steel",
                    "black_oxide": "Black-Oxide Steel",
                }
                part.material = material_map.get(mat_name, mat_name)
                break

        # Head type
        for head_name, pattern in HEAD_TYPE_PATTERNS.items():
            if pattern.search(description):
                head_map = {
                    "socket_head": "Socket Head",
                    "button_head": "Button Head",
                    "flat_head": "Flat Head",
                    "pan_head": "Pan Head",
                    "hex_head": "Hex Head",
                    "hex_flange": "Hex Flange",
                    "truss_head": "Truss Head",
                    "round_head": "Round Head",
                    "oval_head": "Oval Head",
                    "fillister": "Fillister",
                }
                part.head_type = head_map.get(head_name, head_name)
                break

        # Drive type
        for drive_name, pattern in DRIVE_TYPE_PATTERNS.items():
            if pattern.search(description):
                drive_map = {
                    "hex_socket": "Hex Socket",
                    "phillips": "Phillips",
                    "slotted": "Slotted",
                    "torx": "Torx",
                    "square": "Square",
                    "combo": "Combo",
                    "hex_external": "External Hex",
                }
                part.drive_type = drive_map.get(drive_name, drive_name)
                break

        # Length
        for len_name, pattern in LENGTH_PATTERNS.items():
            match = pattern.search(description)
            if match:
                if len_name == "metric_mm":
                    part.length = float(match.group(1))
                elif len_name == "imperial_inch":
                    part.length = self._parse_imperial_length(match.group(1))
                break

    def _parse_imperial_length(self, length_str: str) -> float:
        """Convert imperial length string to millimeters."""
        total_inches = 0.0

        # Handle mixed fractions like "1-1/2"
        if '-' in length_str:
            parts = length_str.split('-')
            if len(parts) == 2:
                whole = float(parts[0]) if parts[0] else 0
                if '/' in parts[1]:
                    num, denom = parts[1].split('/')
                    total_inches = whole + float(num) / float(denom)
                else:
                    total_inches = whole
        elif '/' in length_str:
            num, denom = length_str.split('/')
            total_inches = float(num) / float(denom)
        else:
            total_inches = float(length_str)

        # Convert to mm
        return total_inches * 25.4

    def _parse_spec_table(self, table, part: ScrapedPart) -> None:
        """Parse specifications from a table element."""
        for row in table.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)

                if 'thread' in label:
                    part.thread_spec = value
                elif 'length' in label:
                    self._parse_length_value(value, part)
                elif 'material' in label:
                    part.material = value
                elif 'head' in label and 'type' in label:
                    part.head_type = value
                elif 'drive' in label:
                    if 'size' in label:
                        part.drive_size = value
                    else:
                        part.drive_type = value
                elif 'tensile' in label:
                    match = re.search(r'([\d,]+)', value)
                    if match:
                        part.tensile_strength = float(match.group(1).replace(',', ''))
                elif 'diameter' in label:
                    self._parse_diameter_value(value, part)

    def _parse_length_value(self, value: str, part: ScrapedPart) -> None:
        """Parse length from specification value."""
        # Try metric first
        mm_match = re.search(r'([\d.]+)\s*mm', value, re.IGNORECASE)
        if mm_match:
            part.length = float(mm_match.group(1))
            return

        # Try imperial
        inch_match = re.search(r'([\d.]+(?:-\d+/\d+)?|\d+/\d+)\s*["\']', value)
        if inch_match:
            part.length = self._parse_imperial_length(inch_match.group(1))

    def _parse_diameter_value(self, value: str, part: ScrapedPart) -> None:
        """Parse diameter from specification value."""
        mm_match = re.search(r'([\d.]+)\s*mm', value, re.IGNORECASE)
        if mm_match:
            part.diameter = float(mm_match.group(1))

    def _extract_cad_urls(self, soup) -> Dict[str, str]:
        """Extract CAD model download URLs."""
        cad_urls = {}
        cad_formats = ['step', 'stp', 'stl', 'dwg', 'dxf', 'iges', 'igs', 'pdf']

        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text(strip=True).lower()

            for fmt in cad_formats:
                if fmt in href or fmt in text:
                    cad_urls[fmt.upper()] = link['href']
                    break

        return cad_urls

    def _extract_specs_regex(self, html: str, part: ScrapedPart) -> None:
        """Extract specifications using regex patterns."""
        # Thread
        for pattern_name, pattern in THREAD_PATTERNS.items():
            match = pattern.search(html)
            if match and not part.thread_spec:
                if pattern_name == "metric":
                    part.thread_spec = f"M{match.group(1)}x{match.group(2)}"
                elif pattern_name == "unified":
                    if match.group(1):
                        part.thread_spec = f"{match.group(1)}-{match.group(3)}"
                    else:
                        part.thread_spec = f"#{match.group(2)}-{match.group(3)}"

        # Length
        for pattern_name, pattern in LENGTH_PATTERNS.items():
            match = pattern.search(html)
            if match and not part.length:
                if pattern_name == "metric_mm":
                    part.length = float(match.group(1))
                elif pattern_name == "imperial_inch":
                    part.length = self._parse_imperial_length(match.group(1))

    async def get_categories(self) -> List[McMasterCategory]:
        """
        Get list of all fastener categories.

        Returns:
            List of category information
        """
        categories = []
        for name, path in self.FASTENER_CATEGORIES.items():
            categories.append(McMasterCategory(
                id=name,
                name=name.replace('_', ' ').title(),
                url=f"{self.BASE_URL}{path}",
            ))
        return categories


# Convenience function for direct usage
async def scrape_mcmaster_product(product_id: str) -> ScrapeResult:
    """Scrape a single McMaster-Carr product."""
    async with McMasterScraper() as scraper:
        return await scraper.scrape_product(product_id)


async def search_mcmaster(query: str, max_results: int = 10) -> ScrapeResult:
    """Search McMaster-Carr for products."""
    async with McMasterScraper() as scraper:
        return await scraper.search(query, max_results)


__all__ = [
    "McMasterScraper",
    "McMasterCategory",
    "scrape_mcmaster_product",
    "search_mcmaster",
]
