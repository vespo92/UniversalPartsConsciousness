"""
Supplier API Connectors
========================
"The supply chain is the nervous system. These connectors are the synapses."

Connectors for major industrial and electronic component suppliers.
Each connector handles authentication, pagination, and field mapping
for its specific API.

Supported suppliers:
  - Grainger (industrial supply)
  - DigiKey (electronic components)
  - Mouser (electronic components)
  - Fastenal (fasteners & industrial)
  - MSC Industrial (metalworking & industrial)
  - RS Components (global electronics & industrial)
"""

from __future__ import annotations

import logging
import os
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

logger = logging.getLogger("UPC.Connector.Supplier")

try:
    import aiohttp
except ImportError:
    aiohttp = None


# ============================================================
# GRAINGER
# ============================================================

GRAINGER_CONFIG = SourceConfig(
    source_id="grainger",
    name="Grainger",
    source_type=SourceType.SUPPLIER_API,
    tier=SourceTier.TIER_1_PRIMARY,
    base_url="https://api.grainger.com/v1",
    api_key_env_var="GRAINGER_API_KEY",
    requests_per_second=2.0,
    max_concurrent=3,
    batch_size=100,
)


@ConnectorRegistry.register("grainger")
class GraingerConnector(DataSourceConnector):
    """
    Grainger API connector.

    Grainger is one of North America's largest industrial supply companies
    with 1.5M+ products across safety, tools, fasteners, plumbing, and more.

    API Documentation: https://developer.grainger.com/
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config or GRAINGER_CONFIG)
        self._api_key = os.environ.get(self.config.api_key_env_var or "", "")

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required for API calls",
            )

        params = {
            "searchQuery": query,
            "pageSize": min(page_size, 100),
            "startIndex": (page - 1) * page_size,
        }
        if category:
            params["categoryId"] = category
        if filters:
            params.update(filters)

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.base_url}/search/products",
                    params=params,
                    headers=headers,
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        parts = self._transform_results(data)
                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=parts,
                            total_available=data.get("totalCount"),
                            page=page,
                            has_more=len(parts) >= page_size,
                        )
                    elif resp.status == 401:
                        return FetchResult(
                            success=False, source_id=self.source_id,
                            error="Authentication failed. Set GRAINGER_API_KEY env var.",
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
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.base_url}/products/{part_id}",
                    headers=headers,
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        part = self._transform_product(data)
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
        return await self.search("", category=category, page=page, page_size=page_size)

    def _transform_results(self, data: Dict) -> List[FetchedPart]:
        """Transform Grainger API response to FetchedPart list."""
        parts = []
        for item in data.get("products", data.get("results", [])):
            part = self._transform_product(item)
            if part:
                parts.append(part)
        return parts

    def _transform_product(self, item: Dict) -> Optional[FetchedPart]:
        """Transform a single Grainger product to FetchedPart."""
        if not item:
            return None

        return FetchedPart(
            source_id=item.get("itemNumber", item.get("id", "")),
            source_name="Grainger",
            raw_data=item,
            name=item.get("name", item.get("description", "")),
            part_number=item.get("itemNumber", item.get("manufacturerNumber", "")),
            manufacturer=item.get("brandName", item.get("manufacturer", "")),
            description=item.get("description", ""),
            category=item.get("categoryName", ""),
            material=item.get("material", ""),
            price=item.get("price", item.get("listPrice")),
            image_url=item.get("imageUrl", ""),
            specifications=item.get("specifications", {}),
        )


# ============================================================
# DIGIKEY
# ============================================================

DIGIKEY_CONFIG = SourceConfig(
    source_id="digikey",
    name="DigiKey",
    source_type=SourceType.SUPPLIER_API,
    tier=SourceTier.TIER_1_PRIMARY,
    base_url="https://api.digikey.com/products/v4",
    api_key_env_var="DIGIKEY_CLIENT_ID",
    requests_per_second=5.0,
    max_concurrent=5,
    batch_size=50,
    extra={
        "client_secret_env": "DIGIKEY_CLIENT_SECRET",
        "oauth_url": "https://api.digikey.com/v1/oauth2/token",
    },
)


@ConnectorRegistry.register("digikey")
class DigiKeyConnector(DataSourceConnector):
    """
    DigiKey API connector.

    DigiKey is one of the world's largest electronic component distributors
    with 13M+ products from 2,300+ manufacturers.

    API Documentation: https://developer.digikey.com/
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config or DIGIKEY_CONFIG)
        self._client_id = os.environ.get(self.config.api_key_env_var or "", "")
        self._client_secret = os.environ.get(
            self.config.extra.get("client_secret_env", ""), ""
        )
        self._access_token: Optional[str] = None

    async def _authenticate(self) -> bool:
        """Get OAuth2 access token."""
        if not aiohttp or not self._client_id:
            return False

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.extra.get("oauth_url", ""),
                    data={
                        "client_id": self._client_id,
                        "client_secret": self._client_secret,
                        "grant_type": "client_credentials",
                    },
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self._access_token = data.get("access_token")
                        return True
        except Exception as e:
            logger.error(f"DigiKey auth failed: {e}")
        return False

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        await self._rate_limit()

        if not self._access_token:
            await self._authenticate()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "X-DIGIKEY-Client-Id": self._client_id,
            "Accept": "application/json",
        }

        body = {
            "Keywords": query,
            "RecordCount": min(page_size, 50),
            "RecordStartPosition": (page - 1) * page_size,
            "ExcludeMarketPlaceProducts": True,
        }
        if category:
            body["CategoryFilter"] = {"Id": category}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.base_url}/search/keyword",
                    json=body,
                    headers=headers,
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        parts = self._transform_results(data)
                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=parts,
                            total_available=data.get("ProductsCount"),
                            page=page,
                            has_more=len(parts) >= page_size,
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
        await self._rate_limit()

        if not self._access_token:
            await self._authenticate()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "X-DIGIKEY-Client-Id": self._client_id,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config.base_url}/search/{part_id}/productdetails",
                    headers=headers,
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        part = self._transform_product(data.get("Product", data))
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
        for item in data.get("Products", []):
            part = self._transform_product(item)
            if part:
                parts.append(part)
        return parts

    def _transform_product(self, item: Dict) -> Optional[FetchedPart]:
        if not item:
            return None

        # Extract specs from parameters
        specs = {}
        for param in item.get("Parameters", []):
            specs[param.get("Parameter", "")] = param.get("Value", "")

        return FetchedPart(
            source_id=item.get("DigiKeyPartNumber", ""),
            source_name="DigiKey",
            raw_data=item,
            name=item.get("ProductDescription", item.get("DetailedDescription", "")),
            part_number=item.get("ManufacturerPartNumber", ""),
            manufacturer=item.get("Manufacturer", {}).get("Name", ""),
            description=item.get("DetailedDescription", ""),
            category=item.get("Category", {}).get("Name", ""),
            price=item.get("UnitPrice"),
            datasheet_url=item.get("DatasheetUrl", item.get("PrimaryDatasheet", "")),
            image_url=item.get("PrimaryPhoto", ""),
            specifications=specs,
        )


# ============================================================
# MOUSER
# ============================================================

MOUSER_CONFIG = SourceConfig(
    source_id="mouser",
    name="Mouser Electronics",
    source_type=SourceType.SUPPLIER_API,
    tier=SourceTier.TIER_1_PRIMARY,
    base_url="https://api.mouser.com/api/v2",
    api_key_env_var="MOUSER_API_KEY",
    requests_per_second=3.0,
    max_concurrent=3,
    batch_size=50,
)


@ConnectorRegistry.register("mouser")
class MouserConnector(DataSourceConnector):
    """
    Mouser Electronics API connector.

    Mouser stocks 6.8M+ products from 1,200+ manufacturers.

    API Documentation: https://api.mouser.com/api/docs/ui/index
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config or MOUSER_CONFIG)
        self._api_key = os.environ.get(self.config.api_key_env_var or "", "")

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        await self._rate_limit()

        if not aiohttp:
            return FetchResult(
                success=False, source_id=self.source_id,
                error="aiohttp required",
            )

        body = {
            "SearchByKeywordRequest": {
                "keyword": query,
                "records": min(page_size, 50),
                "startingRecord": (page - 1) * page_size,
                "searchOptions": category or "",
            }
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.base_url}/search/keyword",
                    json=body,
                    params={"apiKey": self._api_key},
                    headers={"Content-Type": "application/json"},
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        search_results = data.get("SearchResults", {})
                        parts = self._transform_results(search_results)
                        return FetchResult(
                            success=True,
                            source_id=self.source_id,
                            parts=parts,
                            total_available=search_results.get("NumberOfResult"),
                            page=page,
                            has_more=len(parts) >= page_size,
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
        """Fetch by Mouser part number."""
        return await self.search(part_id, page_size=1)

    async def fetch_category(
        self, category: str, page: int = 1, page_size: int = 50,
    ) -> FetchResult:
        return await self.search("*", category=category, page=page, page_size=page_size)

    def _transform_results(self, data: Dict) -> List[FetchedPart]:
        parts = []
        for item in data.get("Parts", []):
            parts.append(FetchedPart(
                source_id=item.get("MouserPartNumber", ""),
                source_name="Mouser",
                raw_data=item,
                name=item.get("Description", ""),
                part_number=item.get("ManufacturerPartNumber", ""),
                manufacturer=item.get("Manufacturer", ""),
                description=item.get("Description", ""),
                category=item.get("Category", ""),
                price=self._parse_price(item.get("PriceBreaks", [])),
                datasheet_url=item.get("DataSheetUrl", ""),
                image_url=item.get("ImagePath", ""),
            ))
        return parts

    @staticmethod
    def _parse_price(price_breaks: List) -> Optional[float]:
        """Get unit price from price breaks (first break)."""
        if price_breaks:
            price_str = price_breaks[0].get("Price", "")
            try:
                return float(price_str.replace("$", "").replace(",", ""))
            except (ValueError, AttributeError):
                pass
        return None
