"""
SHEPHERD Integrity Module - Consciousness data validation.

This module provides integrity checking capabilities
for the Consciousness Shepherd (Agent_3).
"""

from .integrity_checker import (
    IntegrityIssueType,
    IssueSeverity,
    IntegrityIssue,
    IntegrityReport,
    IntegrityChecker
)

__all__ = [
    "IntegrityIssueType",
    "IssueSeverity",
    "IntegrityIssue",
    "IntegrityReport",
    "IntegrityChecker"
]
