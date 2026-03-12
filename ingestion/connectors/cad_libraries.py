"""
CAD Library Connectors
=======================
"3D models are the physical truth of a part.
If a spec sheet lies, the model never does."

Connectors for 3D model repositories where parts live as
downloadable CAD files — the spatial consciousness layer.

Supported libraries:
  - GrabCAD Community Library (2.8M+ free CAD models)
  - TraceParts (100M+ 2D/3D models from certified suppliers)
  - 3D ContentCentral (free supplier-certified models)
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any, Dict, List, Optional

from .base import (
    ConnectorRegistry,
    DataSourceConnector,
    FetchedPart,
    FetchResult,
    SourceConfig,
    SourceTier,
    SourceType,
)

logger = logging.getLogger("UPC.Connector.CADLibrary")

try:
    import aiohttp
except ImportError:
    aiohttp = None


# ============================================================
# GRABCAD
# ============================================================

GRABCAD_CONFIG = SourceConfig(
    source_id="grabcad",
    name="GrabCAD Community Library",
    source_type=SourceType.CAD_LIBRARY,
    tier=SourceTier.TIER_3_MANUFACTURER,
    base_url="https://grabcad.com",
    requests_per_second=0.5,  # Respectful rate limiting
    max_concurrent=2,
    batch_size=20,
)


@ConnectorRegistry.register("grabcad")
class GrabCADConnector(DataSourceConnector):
    """
    GrabCAD Community Library connector.

    GrabCAD hosts 2.8M+ free CAD models from a community of 9M+ engineers.
    Models come in native CAD formats (SolidWorks, Inventor, CATIA, etc.)
    plus universal formats (STEP, IGES, STL).

    Note: GrabCAD does not have an official public API.
    This connector uses their public search pages.
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config or GRABCAD_CONFIG)

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        """Search GrabCAD library for CAD models."""
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        # GrabCAD search URL pattern
        params = {
            "utf8": "✓",
            "query": query,
            "page": page,
        }
        if category:
            params["category"] = category
        if filters:
            if "software" in filters:
                params["softwares"] = filters["software"]
            if "sort" in filters:
                params["sort"] = filters["sort"]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.base_url}/library",
                    params=params,
                    headers={
                        "User-Agent": (
                            "UniversalPartsConsciousness/1.0 "
                            "(CAD Library Indexer; Research)"
                        ),
                        "Accept": "application/json, text/html",
                    },
                ) as resp:
                    if resp.status == 200:
                        content_type = resp.headers.get("Content-Type", "")
                        if "json" in content_type:
                            data = await resp.json()
                            parts = self._transform_json_results(data)
                        else:
                            html = await resp.text()
                            parts = self._parse_search_results(html)

                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=parts,
                            page=page,
                            has_more=len(parts) >= page_size,
                        )
                    else:
                        return FetchResult(
                            success=False, source_id=self.source_id,
                            error=f"HTTP {resp.status}",
                        )
        except Exception as e:
            return FetchResult(
                success=False, source_id=self.source_id, error=str(e),
            )

    async def fetch_part(self, part_id: str) -> FetchResult:
        """Fetch a specific GrabCAD model by ID or URL slug."""
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        url = (
            f"{self.config.base_url}/library/{part_id}"
            if not part_id.startswith("http")
            else part_id
        )

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers={"User-Agent": "UniversalPartsConsciousness/1.0"},
                ) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        part = self._parse_model_page(html, url)
                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=[part] if part else [],
                        )
                    else:
                        return FetchResult(
                            success=False, source_id=self.source_id,
                            error=f"HTTP {resp.status}",
                        )
        except Exception as e:
            return FetchResult(
                success=False, source_id=self.source_id, error=str(e),
            )

    async def fetch_category(
        self, category: str, page: int = 1, page_size: int = 20,
    ) -> FetchResult:
        return await self.search("", category=category, page=page, page_size=page_size)

    def _transform_json_results(self, data: Dict) -> List[FetchedPart]:
        """Transform JSON search results."""
        parts = []
        for item in data.get("models", data.get("results", [])):
            parts.append(FetchedPart(
                source_id=str(item.get("id", "")),
                source_name="GrabCAD",
                raw_data=item,
                name=item.get("name", item.get("title", "")),
                description=item.get("description", ""),
                image_url=item.get("thumbnail", item.get("preview_image", "")),
                cad_models={
                    fmt: url for fmt, url in item.get("files", {}).items()
                },
                specifications={
                    "software": item.get("software", []),
                    "tags": item.get("tags", []),
                    "downloads": item.get("download_count", 0),
                    "likes": item.get("like_count", 0),
                },
            ))
        return parts

    def _parse_search_results(self, html: str) -> List[FetchedPart]:
        """Parse search results from HTML (fallback)."""
        parts = []

        # Extract model cards using regex
        card_pattern = re.compile(
            r'<a[^>]*href="/library/([^"]+)"[^>]*>.*?'
            r'<img[^>]*src="([^"]*)".*?'
            r'class="card-title[^"]*"[^>]*>([^<]+)',
            re.DOTALL
        )

        for match in card_pattern.finditer(html):
            slug, thumbnail, title = match.groups()
            parts.append(FetchedPart(
                source_id=slug,
                source_name="GrabCAD",
                raw_data={"slug": slug, "url": f"{self.config.base_url}/library/{slug}"},
                name=title.strip(),
                image_url=thumbnail,
            ))

        return parts

    def _parse_model_page(self, html: str, url: str) -> Optional[FetchedPart]:
        """Parse a single model page for detailed info."""
        title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        desc_match = re.search(
            r'class="description[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL
        )
        author_match = re.search(r'class="author[^"]*"[^>]*>([^<]+)', html)

        # Find download formats
        formats = {}
        format_pattern = re.compile(r'data-format="([^"]+)"[^>]*data-url="([^"]+)"')
        for fmt_match in format_pattern.finditer(html):
            fmt, download_url = fmt_match.groups()
            formats[fmt.upper()] = download_url

        if not title_match:
            return None

        return FetchedPart(
            source_id=url.split("/library/")[-1] if "/library/" in url else url,
            source_name="GrabCAD",
            raw_data={"url": url},
            name=title_match.group(1).strip(),
            description=desc_match.group(1).strip() if desc_match else "",
            manufacturer=author_match.group(1).strip() if author_match else "",
            cad_models=formats,
        )


# ============================================================
# TRACEPARTS
# ============================================================

TRACEPARTS_CONFIG = SourceConfig(
    source_id="traceparts",
    name="TraceParts",
    source_type=SourceType.CAD_LIBRARY,
    tier=SourceTier.TIER_1_PRIMARY,
    base_url="https://www.traceparts.com/en",
    api_key_env_var="TRACEPARTS_API_KEY",
    requests_per_second=1.0,
    max_concurrent=3,
    batch_size=50,
    extra={
        "api_base": "https://ws.traceparts.com/tpapi",
    },
)


@ConnectorRegistry.register("traceparts")
class TracePartsConnector(DataSourceConnector):
    """
    TraceParts connector.

    TraceParts provides 100M+ 2D and 3D supplier-certified CAD models
    from thousands of manufacturers. These are official manufacturer models,
    making them the gold standard for dimensional accuracy.

    API: TraceParts Web Services (TPAPI)
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config or TRACEPARTS_CONFIG)
        self._api_key = os.environ.get(self.config.api_key_env_var or "", "")

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        """Search TraceParts catalog."""
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        api_base = self.config.extra.get("api_base", "")

        params = {
            "apikey": self._api_key,
            "query": query,
            "offset": (page - 1) * page_size,
            "limit": page_size,
        }
        if category:
            params["classification"] = category
        if filters:
            params.update(filters)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{api_base}/search",
                    params=params,
                    headers={"Accept": "application/json"},
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        parts = self._transform_results(data)
                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=parts,
                            total_available=data.get("TotalCount", data.get("totalResults")),
                            page=page,
                            has_more=len(parts) >= page_size,
                        )
                    elif resp.status == 401:
                        return FetchResult(
                            success=False, source_id=self.source_id,
                            error="Auth failed. Set TRACEPARTS_API_KEY env var.",
                        )
                    else:
                        return FetchResult(
                            success=False, source_id=self.source_id,
                            error=f"API error: {resp.status}",
                        )
        except Exception as e:
            return FetchResult(
                success=False, source_id=self.source_id, error=str(e),
            )

    async def fetch_part(self, part_id: str) -> FetchResult:
        """Fetch a specific TraceParts model."""
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        api_base = self.config.extra.get("api_base", "")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{api_base}/parts/{part_id}",
                    params={"apikey": self._api_key},
                    headers={"Accept": "application/json"},
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        part = self._transform_part(data)
                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=[part] if part else [],
                        )
                    else:
                        return FetchResult(
                            success=False, source_id=self.source_id,
                            error=f"API error: {resp.status}",
                        )
        except Exception as e:
            return FetchResult(
                success=False, source_id=self.source_id, error=str(e),
            )

    async def fetch_category(
        self, category: str, page: int = 1, page_size: int = 50,
    ) -> FetchResult:
        return await self.search("*", category=category, page=page, page_size=page_size)

    def _transform_results(self, data: Dict) -> List[FetchedPart]:
        parts = []
        for item in data.get("Results", data.get("parts", [])):
            part = self._transform_part(item)
            if part:
                parts.append(part)
        return parts

    def _transform_part(self, item: Dict) -> Optional[FetchedPart]:
        if not item:
            return None

        # Extract available CAD formats
        cad_models = {}
        for fmt in item.get("AvailableFormats", item.get("formats", [])):
            if isinstance(fmt, dict):
                cad_models[fmt.get("Name", "")] = fmt.get("DownloadUrl", "")
            elif isinstance(fmt, str):
                cad_models[fmt] = ""

        # Extract specifications from properties
        specs = {}
        for prop in item.get("Properties", item.get("parameters", [])):
            if isinstance(prop, dict):
                specs[prop.get("Name", "")] = prop.get("Value", "")

        return FetchedPart(
            source_id=item.get("PartNumber", item.get("id", "")),
            source_name="TraceParts",
            raw_data=item,
            name=item.get("Description", item.get("name", "")),
            part_number=item.get("PartNumber", item.get("partNumber", "")),
            manufacturer=item.get("Manufacturer", item.get("supplier", "")),
            description=item.get("Description", ""),
            category=item.get("Classification", item.get("category", "")),
            image_url=item.get("ThumbnailUrl", item.get("imageUrl", "")),
            cad_models=cad_models,
            specifications=specs,
        )
