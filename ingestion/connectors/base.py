"""
Data Source Connector Base
===========================
"Every data source speaks a different language.
The connectors are the translators."

Abstract base for all data source connectors.
Each connector knows how to authenticate, paginate, rate-limit,
and transform data from a specific external source.
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional, Type

logger = logging.getLogger("UPC.Connector")


class SourceType(str, Enum):
    SUPPLIER_API = "supplier_api"        # McMaster, Grainger, DigiKey
    STANDARDS_DB = "standards_db"        # ISO, DIN, ANSI databases
    CAD_LIBRARY = "cad_library"          # GrabCAD, TraceParts, 3D ContentCentral
    MANUFACTURER = "manufacturer"        # Direct from OEM
    COMMUNITY = "community"             # User contributions, forums
    GOVERNMENT = "government"           # NIST, FDA, military specs
    FILE_IMPORT = "file_import"         # CSV, JSON, Excel uploads


class SourceTier(int, Enum):
    TIER_1_PRIMARY = 1          # Gold standard: McMaster, Grainger, DigiKey
    TIER_2_STANDARDS = 2        # Official standards: ISO, DIN, ANSI
    TIER_3_MANUFACTURER = 3     # OEM data, aftermarket catalogs
    TIER_4_COMMUNITY = 4        # Field measurements, community contributions


@dataclass
class SourceConfig:
    """Configuration for a data source connector."""
    source_id: str                         # Unique identifier
    name: str                              # Display name
    source_type: SourceType
    tier: SourceTier

    # Connection
    base_url: Optional[str] = None
    api_key: Optional[str] = None          # Set via environment variable
    api_key_env_var: Optional[str] = None  # e.g., "GRAINGER_API_KEY"

    # Rate limiting
    requests_per_second: float = 1.0
    max_concurrent: int = 3
    retry_count: int = 3

    # Ingestion
    batch_size: int = 100
    max_items_per_run: Optional[int] = None

    # Custom config
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FetchedPart:
    """A part record fetched from a data source, pre-normalization."""
    source_id: str                # ID in source system
    source_name: str              # Name of source
    raw_data: Dict[str, Any]      # Complete raw data from source
    fetched_at: datetime = field(default_factory=datetime.utcnow)

    # Pre-mapped fields (optional, connector can pre-map known fields)
    name: Optional[str] = None
    part_number: Optional[str] = None
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    price: Optional[float] = None
    currency: str = "USD"
    image_url: Optional[str] = None
    datasheet_url: Optional[str] = None
    cad_models: Dict[str, str] = field(default_factory=dict)

    # Dimensions (in mm)
    specifications: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FetchResult:
    """Result of a fetch/search operation."""
    success: bool
    source_id: str
    parts: List[FetchedPart] = field(default_factory=list)
    total_available: Optional[int] = None  # Total matching items at source
    page: int = 1
    has_more: bool = False
    error: Optional[str] = None
    response_time_ms: float = 0.0


class DataSourceConnector(ABC):
    """
    Abstract base class for all data source connectors.

    Subclasses implement the specifics of authenticating with,
    searching, and fetching data from a particular source.
    """

    def __init__(self, config: SourceConfig):
        self.config = config
        self._last_request_time = 0.0
        self._request_count = 0
        self._semaphore = asyncio.Semaphore(config.max_concurrent)

    @property
    def source_id(self) -> str:
        return self.config.source_id

    @property
    def name(self) -> str:
        return self.config.name

    @abstractmethod
    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        """
        Search the data source for parts matching a query.

        Args:
            query: Search text
            category: Optional category filter
            page: Page number (1-indexed)
            page_size: Results per page
            filters: Source-specific filters

        Returns:
            FetchResult with matching parts
        """
        pass

    @abstractmethod
    async def fetch_part(self, part_id: str) -> FetchResult:
        """
        Fetch a single part by its source-specific ID.

        Args:
            part_id: Part identifier in the source system

        Returns:
            FetchResult with the part data
        """
        pass

    @abstractmethod
    async def fetch_category(
        self,
        category: str,
        page: int = 1,
        page_size: int = 50,
    ) -> FetchResult:
        """
        Fetch all parts in a category.

        Args:
            category: Category identifier or path
            page: Page number
            page_size: Results per page

        Returns:
            FetchResult with parts in the category
        """
        pass

    async def fetch_all(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        max_items: Optional[int] = None,
    ) -> AsyncIterator[FetchedPart]:
        """
        Fetch all matching parts with automatic pagination.

        Yields individual FetchedPart objects.
        """
        page = 1
        total_fetched = 0
        max_items = max_items or self.config.max_items_per_run

        while True:
            if query:
                result = await self.search(query, category, page=page)
            elif category:
                result = await self.fetch_category(category, page=page)
            else:
                break

            if not result.success or not result.parts:
                break

            for part in result.parts:
                yield part
                total_fetched += 1
                if max_items and total_fetched >= max_items:
                    return

            if not result.has_more:
                break

            page += 1

    async def health_check(self) -> bool:
        """Check if the data source is reachable and responding."""
        try:
            result = await self.search("test", page_size=1)
            return result.success
        except Exception:
            return False

    async def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        async with self._semaphore:
            now = time.monotonic()
            min_interval = 1.0 / self.config.requests_per_second
            elapsed = now - self._last_request_time
            if elapsed < min_interval:
                await asyncio.sleep(min_interval - elapsed)
            self._last_request_time = time.monotonic()
            self._request_count += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get connector statistics."""
        return {
            "source_id": self.config.source_id,
            "name": self.config.name,
            "type": self.config.source_type.value,
            "tier": self.config.tier.value,
            "requests_made": self._request_count,
        }


class ConnectorRegistry:
    """
    Registry of all available data source connectors.

    Usage:
        @ConnectorRegistry.register("grainger")
        class GraingerConnector(DataSourceConnector):
            ...

        connector = ConnectorRegistry.create("grainger", config)
    """

    _connectors: Dict[str, Type[DataSourceConnector]] = {}

    @classmethod
    def register(cls, source_id: str):
        """Decorator to register a connector class."""
        def decorator(connector_class: Type[DataSourceConnector]):
            cls._connectors[source_id] = connector_class
            return connector_class
        return decorator

    @classmethod
    def create(cls, source_id: str, config: SourceConfig) -> DataSourceConnector:
        """Create a connector instance by source ID."""
        connector_class = cls._connectors.get(source_id)
        if not connector_class:
            raise ValueError(
                f"Unknown data source: {source_id}. "
                f"Available: {list(cls._connectors.keys())}"
            )
        return connector_class(config)

    @classmethod
    def list_sources(cls) -> List[str]:
        """List all registered source IDs."""
        return list(cls._connectors.keys())

    @classmethod
    def get_class(cls, source_id: str) -> Optional[Type[DataSourceConnector]]:
        """Get the connector class for a source."""
        return cls._connectors.get(source_id)
