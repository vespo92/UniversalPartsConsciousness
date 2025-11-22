"""
Agent_1 Quality Module
======================
Data quality scoring and duplicate detection systems.
"""

from .scorer import (
    PartQualityScorer,
    QualityScore,
    QualityViolation,
    QualityRule,
    QualityDimension,
    score_part,
    score_batch,
    calculate_batch_statistics,
)

from .duplicate_detector import (
    DuplicateDetector,
    DuplicateMatch,
    DuplicateGroup,
    DuplicateConfidence,
    MatchFactor,
    find_duplicates,
    group_duplicates,
)

__all__ = [
    # Scoring
    "PartQualityScorer",
    "QualityScore",
    "QualityViolation",
    "QualityRule",
    "QualityDimension",
    "score_part",
    "score_batch",
    "calculate_batch_statistics",
    # Duplicate detection
    "DuplicateDetector",
    "DuplicateMatch",
    "DuplicateGroup",
    "DuplicateConfidence",
    "MatchFactor",
    "find_duplicates",
    "group_duplicates",
]
