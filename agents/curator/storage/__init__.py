"""
Agent_1 (ARCHIVIST) - Storage Module
=====================================
"Nothing is forgotten. Everything is accessible."

Data persistence and caching systems for the Universal Parts Consciousness.

Components:
- PartRepository: Core part data access layer with indexing and search
"""

from .part_repository import (
    PartRepository,
    PartIndex,
    RepositoryStats,
)


__all__ = [
    "PartRepository",
    "PartIndex",
    "RepositoryStats",
]
