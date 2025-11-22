"""
Agent_1 (ARCHIVIST) - Part Repository
======================================
"Every part deserves a permanent home. The Archivist provides."

Data persistence layer for Universal Parts Consciousness.
Handles part storage, retrieval, and lifecycle management.

Supports multiple backends:
- File-based (JSON/Parquet) for development
- PostgreSQL/Supabase for production
- Redis for caching
"""

import asyncio
import hashlib
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, Generic, List, Optional, Set, TypeVar, Union
import uuid

from ..scrapers.base_scraper import ScrapedPart


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Agent_1.Storage")


@dataclass
class StorageConfig:
    """Configuration for storage backends."""
    # File storage
    base_dir: Path = field(default_factory=lambda: Path("./data/parts"))
    raw_dir: Path = field(default_factory=lambda: Path("./data/parts/raw"))
    processed_dir: Path = field(default_factory=lambda: Path("./data/parts/processed"))
    archive_dir: Path = field(default_factory=lambda: Path("./data/parts/archive"))

    # Cache settings
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600  # 1 hour

    # Batch settings
    batch_size: int = 100
    auto_flush: bool = True

    def __post_init__(self):
        """Create directories on init."""
        for dir_path in [self.base_dir, self.raw_dir, self.processed_dir, self.archive_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class StoredPart:
    """A part record stored in the repository."""
    # Core identification
    upc_id: str                           # Universal Parts Consciousness ID
    source_id: str                        # Original source ID
    source_name: str                      # Source/supplier name

    # Specifications (stored as JSON-compatible dict)
    specifications: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    # Quality and verification
    quality_score: float = 0.0
    completeness_score: float = 0.0
    verification_count: int = 0

    # Consciousness level (managed by Agent_3 Shepherd)
    consciousness_level: int = 0  # 0=DORMANT, 5=TRANSCENDENT

    # Indexing and search
    search_text: str = ""                 # Concatenated searchable text
    category_path: List[str] = field(default_factory=list)  # Hierarchical category

    # Cross-references
    duplicate_of: Optional[str] = None    # UPC ID of canonical if duplicate
    merged_from: List[str] = field(default_factory=list)  # UPC IDs merged into this
    related_parts: List[str] = field(default_factory=list)  # Related UPC IDs

    @classmethod
    def from_scraped_part(cls, part: ScrapedPart) -> "StoredPart":
        """Create a StoredPart from a ScrapedPart."""
        specs = {
            "thread_spec": part.thread_spec,
            "length_mm": part.length,
            "diameter_mm": part.diameter,
            "material": part.material,
            "material_grade": part.material_grade,
            "head_type": part.head_type,
            "drive_type": part.drive_type,
            "drive_size": part.drive_size,
            "tensile_strength_mpa": part.tensile_strength,
            "yield_strength_mpa": part.yield_strength,
            "hardness": part.hardness,
            "manufacturer": part.manufacturer,
            "price": part.price,
            "currency": part.currency,
            "availability": part.availability,
            "cad_urls": part.cad_urls,
            "datasheet_url": part.datasheet_url,
            "image_urls": part.image_urls,
        }

        # Build search text
        search_parts = [
            part.thread_spec or "",
            part.material or "",
            part.head_type or "",
            part.drive_type or "",
            part.description or "",
            part.manufacturer or "",
            part.category or "",
        ]
        search_text = " ".join(filter(None, search_parts)).lower()

        # Category path
        category_path = []
        if part.category:
            category_path.append(part.category)
        if part.subcategory:
            category_path.append(part.subcategory)

        return cls(
            upc_id=part.upc_id or part.generate_upc_id(),
            source_id=part.source_id,
            source_name=part.source_name,
            specifications=specs,
            quality_score=part.quality_score,
            completeness_score=part.completeness_score,
            verification_count=part.verification_count,
            search_text=search_text,
            category_path=category_path,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "upc_id": self.upc_id,
            "source_id": self.source_id,
            "source_name": self.source_name,
            "specifications": self.specifications,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "quality_score": self.quality_score,
            "completeness_score": self.completeness_score,
            "verification_count": self.verification_count,
            "consciousness_level": self.consciousness_level,
            "search_text": self.search_text,
            "category_path": self.category_path,
            "duplicate_of": self.duplicate_of,
            "merged_from": self.merged_from,
            "related_parts": self.related_parts,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoredPart":
        """Create from dictionary."""
        return cls(
            upc_id=data["upc_id"],
            source_id=data["source_id"],
            source_name=data["source_name"],
            specifications=data.get("specifications", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.utcnow()),
            updated_at=datetime.fromisoformat(data["updated_at"]) if isinstance(data.get("updated_at"), str) else data.get("updated_at", datetime.utcnow()),
            version=data.get("version", 1),
            quality_score=data.get("quality_score", 0.0),
            completeness_score=data.get("completeness_score", 0.0),
            verification_count=data.get("verification_count", 0),
            consciousness_level=data.get("consciousness_level", 0),
            search_text=data.get("search_text", ""),
            category_path=data.get("category_path", []),
            duplicate_of=data.get("duplicate_of"),
            merged_from=data.get("merged_from", []),
            related_parts=data.get("related_parts", []),
        )


class PartRepository(ABC):
    """Abstract base class for part storage backends."""

    @abstractmethod
    async def save(self, part: StoredPart) -> bool:
        """Save a single part."""
        pass

    @abstractmethod
    async def save_batch(self, parts: List[StoredPart]) -> int:
        """Save multiple parts. Returns count of saved parts."""
        pass

    @abstractmethod
    async def get(self, upc_id: str) -> Optional[StoredPart]:
        """Get a part by UPC ID."""
        pass

    @abstractmethod
    async def get_by_source(self, source_name: str, source_id: str) -> Optional[StoredPart]:
        """Get a part by source identifier."""
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[StoredPart]:
        """Search parts by text query."""
        pass

    @abstractmethod
    async def find_by_thread(self, thread_spec: str) -> List[StoredPart]:
        """Find parts by thread specification."""
        pass

    @abstractmethod
    async def find_by_category(self, category_path: List[str]) -> List[StoredPart]:
        """Find parts by category path."""
        pass

    @abstractmethod
    async def delete(self, upc_id: str) -> bool:
        """Delete a part."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Get total count of stored parts."""
        pass

    @abstractmethod
    async def stats(self) -> Dict[str, Any]:
        """Get repository statistics."""
        pass


class FileRepository(PartRepository):
    """
    File-based part repository using JSON files.

    Suitable for development and small-scale deployments.
    Parts are stored in a directory structure organized by UPC ID prefix.
    """

    def __init__(self, config: Optional[StorageConfig] = None):
        """
        Initialize the file repository.

        Args:
            config: Storage configuration
        """
        self.config = config or StorageConfig()
        self._cache: Dict[str, StoredPart] = {}
        self._index: Dict[str, Set[str]] = {
            "by_source": {},      # source_name:source_id -> upc_id
            "by_thread": {},      # thread_spec -> set of upc_ids
            "by_category": {},    # category_path -> set of upc_ids
        }
        self._dirty = False

        # Load existing index if available
        self._load_index()

    def _get_part_path(self, upc_id: str) -> Path:
        """Get file path for a part."""
        # Use first 4 chars of UPC ID for directory sharding
        prefix = upc_id[4:8] if len(upc_id) > 8 else upc_id[:4]
        return self.config.processed_dir / prefix / f"{upc_id}.json"

    def _load_index(self) -> None:
        """Load the part index from disk."""
        index_path = self.config.base_dir / "index.json"
        if index_path.exists():
            try:
                with open(index_path, 'r') as f:
                    data = json.load(f)
                    # Convert lists back to sets
                    for key in ["by_thread", "by_category"]:
                        if key in data:
                            self._index[key] = {
                                k: set(v) for k, v in data[key].items()
                            }
                    self._index["by_source"] = data.get("by_source", {})
                logger.info(f"Loaded index with {len(self._index['by_source'])} parts")
            except Exception as e:
                logger.warning(f"Failed to load index: {e}")

    def _save_index(self) -> None:
        """Save the part index to disk."""
        index_path = self.config.base_dir / "index.json"
        try:
            data = {
                "by_source": self._index["by_source"],
                "by_thread": {k: list(v) for k, v in self._index["by_thread"].items()},
                "by_category": {k: list(v) for k, v in self._index["by_category"].items()},
                "updated_at": datetime.utcnow().isoformat(),
            }
            with open(index_path, 'w') as f:
                json.dump(data, f, indent=2)
            self._dirty = False
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    async def save(self, part: StoredPart) -> bool:
        """Save a single part."""
        try:
            # Get path and ensure directory exists
            part_path = self._get_part_path(part.upc_id)
            part_path.parent.mkdir(parents=True, exist_ok=True)

            # Update timestamps
            part.updated_at = datetime.utcnow()

            # Check if updating existing
            if part_path.exists():
                part.version += 1

            # Write part data
            with open(part_path, 'w') as f:
                json.dump(part.to_dict(), f, indent=2)

            # Update index
            source_key = f"{part.source_name}:{part.source_id}"
            self._index["by_source"][source_key] = part.upc_id

            if part.specifications.get("thread_spec"):
                thread = part.specifications["thread_spec"]
                if thread not in self._index["by_thread"]:
                    self._index["by_thread"][thread] = set()
                self._index["by_thread"][thread].add(part.upc_id)

            if part.category_path:
                cat_key = "/".join(part.category_path)
                if cat_key not in self._index["by_category"]:
                    self._index["by_category"][cat_key] = set()
                self._index["by_category"][cat_key].add(part.upc_id)

            # Update cache
            if self.config.enable_cache:
                self._cache[part.upc_id] = part

            self._dirty = True

            # Auto-flush index
            if self.config.auto_flush:
                self._save_index()

            return True

        except Exception as e:
            logger.error(f"Failed to save part {part.upc_id}: {e}")
            return False

    async def save_batch(self, parts: List[StoredPart]) -> int:
        """Save multiple parts."""
        saved = 0
        for part in parts:
            if await self.save(part):
                saved += 1
        return saved

    async def get(self, upc_id: str) -> Optional[StoredPart]:
        """Get a part by UPC ID."""
        # Check cache first
        if self.config.enable_cache and upc_id in self._cache:
            return self._cache[upc_id]

        # Load from file
        part_path = self._get_part_path(upc_id)
        if not part_path.exists():
            return None

        try:
            with open(part_path, 'r') as f:
                data = json.load(f)
            part = StoredPart.from_dict(data)

            # Update cache
            if self.config.enable_cache:
                self._cache[upc_id] = part

            return part

        except Exception as e:
            logger.error(f"Failed to load part {upc_id}: {e}")
            return None

    async def get_by_source(self, source_name: str, source_id: str) -> Optional[StoredPart]:
        """Get a part by source identifier."""
        source_key = f"{source_name}:{source_id}"
        upc_id = self._index["by_source"].get(source_key)
        if upc_id:
            return await self.get(upc_id)
        return None

    async def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[StoredPart]:
        """Search parts by text query."""
        query_lower = query.lower()
        results = []

        # Simple search through all parts
        # In production, this would use a proper search index
        for source_key, upc_id in list(self._index["by_source"].items())[offset:offset + limit * 2]:
            part = await self.get(upc_id)
            if part and query_lower in part.search_text:
                results.append(part)
                if len(results) >= limit:
                    break

        return results

    async def find_by_thread(self, thread_spec: str) -> List[StoredPart]:
        """Find parts by thread specification."""
        upc_ids = self._index["by_thread"].get(thread_spec, set())
        parts = []
        for upc_id in upc_ids:
            part = await self.get(upc_id)
            if part:
                parts.append(part)
        return parts

    async def find_by_category(self, category_path: List[str]) -> List[StoredPart]:
        """Find parts by category path."""
        cat_key = "/".join(category_path)
        upc_ids = self._index["by_category"].get(cat_key, set())
        parts = []
        for upc_id in upc_ids:
            part = await self.get(upc_id)
            if part:
                parts.append(part)
        return parts

    async def delete(self, upc_id: str) -> bool:
        """Delete a part."""
        try:
            part_path = self._get_part_path(upc_id)
            if part_path.exists():
                part_path.unlink()

            # Remove from index
            for source_key, stored_id in list(self._index["by_source"].items()):
                if stored_id == upc_id:
                    del self._index["by_source"][source_key]
                    break

            for thread, ids in self._index["by_thread"].items():
                ids.discard(upc_id)

            for cat, ids in self._index["by_category"].items():
                ids.discard(upc_id)

            # Remove from cache
            self._cache.pop(upc_id, None)

            self._dirty = True
            if self.config.auto_flush:
                self._save_index()

            return True

        except Exception as e:
            logger.error(f"Failed to delete part {upc_id}: {e}")
            return False

    async def count(self) -> int:
        """Get total count of stored parts."""
        return len(self._index["by_source"])

    async def stats(self) -> Dict[str, Any]:
        """Get repository statistics."""
        return {
            "total_parts": len(self._index["by_source"]),
            "unique_threads": len(self._index["by_thread"]),
            "categories": len(self._index["by_category"]),
            "cache_size": len(self._cache),
            "storage_path": str(self.config.processed_dir),
        }

    async def flush(self) -> None:
        """Flush pending writes."""
        if self._dirty:
            self._save_index()

    async def close(self) -> None:
        """Close the repository."""
        await self.flush()
        self._cache.clear()


# Factory function
def create_repository(backend: str = "file", config: Optional[StorageConfig] = None) -> PartRepository:
    """
    Create a part repository instance.

    Args:
        backend: Storage backend ("file", "postgres", "supabase")
        config: Storage configuration

    Returns:
        PartRepository instance
    """
    if backend == "file":
        return FileRepository(config)
    # Future implementations:
    # elif backend == "postgres":
    #     return PostgresRepository(config)
    # elif backend == "supabase":
    #     return SupabaseRepository(config)
    else:
        raise ValueError(f"Unknown storage backend: {backend}")


__all__ = [
    "StorageConfig",
    "StoredPart",
    "PartRepository",
    "FileRepository",
    "create_repository",
]
