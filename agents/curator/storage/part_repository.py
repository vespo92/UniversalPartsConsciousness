"""
Agent_1 (ARCHIVIST) - Part Repository
======================================
"Nothing is forgotten. Everything is accessible."

The Part Repository provides persistent storage and retrieval of
normalized part data. It serves as the foundation for the Universal
Parts Consciousness memory.

Features:
- JSON-based file storage (production would use PostgreSQL)
- Full-text search with fuzzy matching
- Historical versioning
- Index management for fast lookups
"""

import asyncio
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set
import re

from ..scrapers.base_scraper import ScrapedPart

logger = logging.getLogger("Agent_1.Repository")


@dataclass
class PartIndex:
    """Index entry for fast part lookups."""
    upc_id: str
    thread_spec: Optional[str]
    material: Optional[str]
    source_name: str
    quality_score: float
    file_path: str
    indexed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RepositoryStats:
    """Repository statistics."""
    total_parts: int = 0
    total_sources: int = 0
    avg_quality_score: float = 0.0
    last_update: Optional[datetime] = None
    index_size: int = 0


class PartRepository:
    """
    Persistent storage for normalized part data.

    This is a file-based implementation suitable for development.
    Production deployments would use PostgreSQL with full-text search.

    Example:
        repo = PartRepository(data_dir=Path("./data/parts"))
        await repo.initialize()

        # Store a part
        await repo.store(part)

        # Search parts
        results = await repo.search("M8 stainless socket head")

        # Get by ID
        part = await repo.get("UPC-ABC123DEF456")
    """

    def __init__(
        self,
        data_dir: Path,
        index_file: str = "index.json",
        max_parts_per_file: int = 1000,
    ):
        """
        Initialize the part repository.

        Args:
            data_dir: Directory for storing part data
            index_file: Name of the index file
            max_parts_per_file: Maximum parts per storage file
        """
        self.data_dir = Path(data_dir)
        self.index_file = self.data_dir / index_file
        self.parts_dir = self.data_dir / "parts"
        self.archive_dir = self.data_dir / "archive"
        self.max_parts_per_file = max_parts_per_file

        # In-memory index
        self._index: Dict[str, PartIndex] = {}

        # Thread-spec index for fast lookups
        self._thread_index: Dict[str, Set[str]] = {}

        # Material index
        self._material_index: Dict[str, Set[str]] = {}

        # Source index
        self._source_index: Dict[str, Set[str]] = {}

        # Statistics
        self._stats = RepositoryStats()

        self._initialized = False
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize the repository and load indices."""
        if self._initialized:
            return

        # Create directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.parts_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Load existing index
        await self._load_index()

        self._initialized = True
        logger.info(f"Repository initialized: {self._stats.total_parts} parts indexed")

    async def store(self, part: ScrapedPart) -> str:
        """
        Store a part in the repository.

        Args:
            part: Part to store

        Returns:
            UPC ID of the stored part
        """
        if not self._initialized:
            await self.initialize()

        async with self._lock:
            # Ensure UPC ID
            if not part.upc_id:
                part.generate_upc_id()

            # Determine storage file
            file_path = self._get_storage_path(part.upc_id)

            # Load existing file data or create new
            if file_path.exists():
                with open(file_path, 'r') as f:
                    file_data = json.load(f)
            else:
                file_data = {"parts": {}, "created_at": datetime.utcnow().isoformat()}

            # Add part to file
            file_data["parts"][part.upc_id] = part.to_dict()
            file_data["updated_at"] = datetime.utcnow().isoformat()

            # Write file
            with open(file_path, 'w') as f:
                json.dump(file_data, f, indent=2, default=str)

            # Update index
            await self._update_index(part, str(file_path))

            # Persist index periodically
            if self._stats.total_parts % 100 == 0:
                await self._save_index()

            return part.upc_id

    async def store_batch(self, parts: List[ScrapedPart]) -> List[str]:
        """
        Store multiple parts efficiently.

        Args:
            parts: List of parts to store

        Returns:
            List of UPC IDs
        """
        upc_ids = []
        for part in parts:
            upc_id = await self.store(part)
            upc_ids.append(upc_id)

        # Ensure index is saved after batch
        await self._save_index()

        return upc_ids

    async def get(self, upc_id: str) -> Optional[ScrapedPart]:
        """
        Get a part by UPC ID.

        Args:
            upc_id: Universal Parts Consciousness ID

        Returns:
            Part if found, None otherwise
        """
        if not self._initialized:
            await self.initialize()

        # Check index
        if upc_id not in self._index:
            return None

        index_entry = self._index[upc_id]
        file_path = Path(index_entry.file_path)

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r') as f:
                file_data = json.load(f)

            part_data = file_data.get("parts", {}).get(upc_id)
            if part_data:
                return self._dict_to_part(part_data)

        except Exception as e:
            logger.error(f"Error loading part {upc_id}: {e}")

        return None

    async def search(
        self,
        query: str,
        max_results: int = 100,
        min_quality: float = 0.0,
        source_filter: Optional[str] = None,
    ) -> List[ScrapedPart]:
        """
        Search for parts matching a query.

        Args:
            query: Search query (thread spec, material, description)
            max_results: Maximum results to return
            min_quality: Minimum quality score filter
            source_filter: Optional source name filter

        Returns:
            List of matching parts
        """
        if not self._initialized:
            await self.initialize()

        # Parse query for specific terms
        candidate_ids: Set[str] = set()
        query_lower = query.lower()

        # Check thread index
        for thread_spec, upc_ids in self._thread_index.items():
            if thread_spec.lower() in query_lower or query_lower in thread_spec.lower():
                candidate_ids.update(upc_ids)

        # Check material index
        for material, upc_ids in self._material_index.items():
            if material.lower() in query_lower or query_lower in material.lower():
                candidate_ids.update(upc_ids)

        # If no candidates from indices, search all
        if not candidate_ids:
            candidate_ids = set(self._index.keys())

        # Load and filter candidates
        results = []
        for upc_id in candidate_ids:
            if len(results) >= max_results:
                break

            index_entry = self._index.get(upc_id)
            if not index_entry:
                continue

            # Apply quality filter
            if index_entry.quality_score < min_quality:
                continue

            # Apply source filter
            if source_filter and index_entry.source_name != source_filter:
                continue

            # Load full part for scoring
            part = await self.get(upc_id)
            if part:
                # Score relevance
                score = self._score_relevance(part, query)
                if score > 0:
                    results.append((score, part))

        # Sort by relevance
        results.sort(key=lambda x: x[0], reverse=True)

        return [part for _, part in results[:max_results]]

    async def get_by_thread(self, thread_spec: str) -> List[ScrapedPart]:
        """
        Get all parts with a specific thread specification.

        Args:
            thread_spec: Thread specification

        Returns:
            List of matching parts
        """
        if thread_spec not in self._thread_index:
            return []

        parts = []
        for upc_id in self._thread_index[thread_spec]:
            part = await self.get(upc_id)
            if part:
                parts.append(part)

        return parts

    async def get_by_material(self, material: str) -> List[ScrapedPart]:
        """
        Get all parts with a specific material.

        Args:
            material: Material name

        Returns:
            List of matching parts
        """
        if material not in self._material_index:
            return []

        parts = []
        for upc_id in self._material_index[material]:
            part = await self.get(upc_id)
            if part:
                parts.append(part)

        return parts

    async def get_candidates_for_duplicate_check(
        self,
        part: ScrapedPart,
        max_candidates: int = 100,
    ) -> List[ScrapedPart]:
        """
        Get candidate parts that might be duplicates.

        Args:
            part: Part to find duplicates for
            max_candidates: Maximum candidates to return

        Returns:
            List of potential duplicate candidates
        """
        candidates: Set[str] = set()

        # Find candidates by thread spec
        if part.thread_spec and part.thread_spec in self._thread_index:
            candidates.update(self._thread_index[part.thread_spec])

        # Find candidates by material
        if part.material and part.material in self._material_index:
            candidates.update(self._material_index[part.material])

        # Load candidates
        parts = []
        for upc_id in list(candidates)[:max_candidates]:
            if upc_id == part.upc_id:
                continue
            candidate = await self.get(upc_id)
            if candidate:
                parts.append(candidate)

        return parts

    async def delete(self, upc_id: str) -> bool:
        """
        Delete a part from the repository.

        Args:
            upc_id: Part ID to delete

        Returns:
            True if deleted, False if not found
        """
        if upc_id not in self._index:
            return False

        async with self._lock:
            index_entry = self._index[upc_id]
            file_path = Path(index_entry.file_path)

            if file_path.exists():
                with open(file_path, 'r') as f:
                    file_data = json.load(f)

                if upc_id in file_data.get("parts", {}):
                    del file_data["parts"][upc_id]

                    with open(file_path, 'w') as f:
                        json.dump(file_data, f, indent=2)

            # Remove from indices
            self._remove_from_indices(upc_id)

            await self._save_index()
            return True

    def _get_storage_path(self, upc_id: str) -> Path:
        """Get storage file path for a UPC ID."""
        # Use hash prefix for distribution
        hash_prefix = upc_id[4:6] if len(upc_id) > 5 else "00"
        return self.parts_dir / f"parts_{hash_prefix}.json"

    async def _update_index(self, part: ScrapedPart, file_path: str) -> None:
        """Update all indices for a part."""
        # Main index
        self._index[part.upc_id] = PartIndex(
            upc_id=part.upc_id,
            thread_spec=part.thread_spec,
            material=part.material,
            source_name=part.source_name,
            quality_score=part.quality_score,
            file_path=file_path,
        )

        # Thread index
        if part.thread_spec:
            if part.thread_spec not in self._thread_index:
                self._thread_index[part.thread_spec] = set()
            self._thread_index[part.thread_spec].add(part.upc_id)

        # Material index
        if part.material:
            if part.material not in self._material_index:
                self._material_index[part.material] = set()
            self._material_index[part.material].add(part.upc_id)

        # Source index
        if part.source_name not in self._source_index:
            self._source_index[part.source_name] = set()
        self._source_index[part.source_name].add(part.upc_id)

        # Update stats
        self._stats.total_parts = len(self._index)
        self._stats.total_sources = len(self._source_index)
        self._stats.last_update = datetime.utcnow()

    def _remove_from_indices(self, upc_id: str) -> None:
        """Remove a part from all indices."""
        index_entry = self._index.get(upc_id)
        if not index_entry:
            return

        # Remove from thread index
        if index_entry.thread_spec and index_entry.thread_spec in self._thread_index:
            self._thread_index[index_entry.thread_spec].discard(upc_id)

        # Remove from material index
        if index_entry.material and index_entry.material in self._material_index:
            self._material_index[index_entry.material].discard(upc_id)

        # Remove from source index
        if index_entry.source_name in self._source_index:
            self._source_index[index_entry.source_name].discard(upc_id)

        # Remove from main index
        del self._index[upc_id]

        # Update stats
        self._stats.total_parts = len(self._index)

    def _score_relevance(self, part: ScrapedPart, query: str) -> float:
        """Score relevance of a part to a query."""
        query_terms = query.lower().split()
        score = 0.0

        # Check each term
        for term in query_terms:
            # Thread spec match (high weight)
            if part.thread_spec and term in part.thread_spec.lower():
                score += 3.0

            # Material match (high weight)
            if part.material and term in part.material.lower():
                score += 2.5

            # Head type match
            if part.head_type and term in part.head_type.lower():
                score += 2.0

            # Drive type match
            if part.drive_type and term in part.drive_type.lower():
                score += 1.5

            # Description match
            if part.description and term in part.description.lower():
                score += 1.0

            # Category match
            if part.category and term in part.category.lower():
                score += 0.5

        # Boost by quality score
        score *= (0.5 + part.quality_score * 0.5)

        return score

    async def _load_index(self) -> None:
        """Load index from disk."""
        if not self.index_file.exists():
            logger.info("No existing index found, starting fresh")
            return

        try:
            with open(self.index_file, 'r') as f:
                index_data = json.load(f)

            # Rebuild indices
            for entry in index_data.get("entries", []):
                index_entry = PartIndex(
                    upc_id=entry["upc_id"],
                    thread_spec=entry.get("thread_spec"),
                    material=entry.get("material"),
                    source_name=entry.get("source_name", "unknown"),
                    quality_score=entry.get("quality_score", 0.0),
                    file_path=entry["file_path"],
                )
                self._index[index_entry.upc_id] = index_entry

                # Thread index
                if index_entry.thread_spec:
                    if index_entry.thread_spec not in self._thread_index:
                        self._thread_index[index_entry.thread_spec] = set()
                    self._thread_index[index_entry.thread_spec].add(index_entry.upc_id)

                # Material index
                if index_entry.material:
                    if index_entry.material not in self._material_index:
                        self._material_index[index_entry.material] = set()
                    self._material_index[index_entry.material].add(index_entry.upc_id)

                # Source index
                if index_entry.source_name not in self._source_index:
                    self._source_index[index_entry.source_name] = set()
                self._source_index[index_entry.source_name].add(index_entry.upc_id)

            # Update stats
            self._stats.total_parts = len(self._index)
            self._stats.total_sources = len(self._source_index)
            self._stats.index_size = len(index_data.get("entries", []))

            logger.info(f"Loaded index: {self._stats.total_parts} parts")

        except Exception as e:
            logger.error(f"Error loading index: {e}")

    async def _save_index(self) -> None:
        """Save index to disk."""
        entries = []
        for upc_id, entry in self._index.items():
            entries.append({
                "upc_id": entry.upc_id,
                "thread_spec": entry.thread_spec,
                "material": entry.material,
                "source_name": entry.source_name,
                "quality_score": entry.quality_score,
                "file_path": entry.file_path,
            })

        index_data = {
            "version": "1.0",
            "updated_at": datetime.utcnow().isoformat(),
            "total_parts": len(entries),
            "entries": entries,
        }

        with open(self.index_file, 'w') as f:
            json.dump(index_data, f, indent=2)

    def _dict_to_part(self, data: Dict[str, Any]) -> ScrapedPart:
        """Convert dictionary to ScrapedPart."""
        # Handle datetime fields
        scraped_at = data.get("scraped_at")
        if isinstance(scraped_at, str):
            scraped_at = datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
        elif not isinstance(scraped_at, datetime):
            scraped_at = datetime.utcnow()

        source_updated_at = data.get("source_updated_at")
        if isinstance(source_updated_at, str):
            source_updated_at = datetime.fromisoformat(source_updated_at.replace('Z', '+00:00'))

        return ScrapedPart(
            source_id=data.get("source_id", ""),
            source_name=data.get("source_name", ""),
            upc_id=data.get("upc_id"),
            thread_spec=data.get("thread_spec"),
            length=data.get("length_mm"),
            diameter=data.get("diameter_mm"),
            material=data.get("material"),
            material_grade=data.get("material_grade"),
            head_type=data.get("head_type"),
            drive_type=data.get("drive_type"),
            drive_size=data.get("drive_size"),
            tensile_strength=data.get("tensile_strength_mpa"),
            yield_strength=data.get("yield_strength_mpa"),
            hardness=data.get("hardness"),
            category=data.get("category"),
            subcategory=data.get("subcategory"),
            description=data.get("description"),
            manufacturer=data.get("manufacturer"),
            price=data.get("price"),
            currency=data.get("currency", "USD"),
            availability=data.get("availability"),
            lead_time_days=data.get("lead_time_days"),
            cad_urls=data.get("cad_urls", {}),
            datasheet_url=data.get("datasheet_url"),
            image_urls=data.get("image_urls", []),
            quality_score=data.get("quality_score", 0.0),
            completeness_score=data.get("completeness_score", 0.0),
            verification_count=data.get("verification_count", 0),
            scraped_at=scraped_at,
            source_updated_at=source_updated_at,
            raw_data=data.get("raw_data", {}),
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get repository statistics."""
        quality_scores = [e.quality_score for e in self._index.values()]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0

        return {
            "total_parts": self._stats.total_parts,
            "total_sources": self._stats.total_sources,
            "unique_threads": len(self._thread_index),
            "unique_materials": len(self._material_index),
            "avg_quality_score": round(avg_quality, 4),
            "last_update": self._stats.last_update.isoformat() if self._stats.last_update else None,
            "data_directory": str(self.data_dir),
        }


__all__ = [
    "PartRepository",
    "PartIndex",
    "RepositoryStats",
]
