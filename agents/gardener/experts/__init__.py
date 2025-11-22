"""
Expert panel management subsystem for Agent_8 (Gardener).

Expert management functionality is primarily in verification/expert_review.py.
This module provides additional expert panel utilities and credential verification.
"""

from ..verification.expert_review import (
    ExpertReviewSystem,
    ExpertProfile,
    ExpertReviewRequest,
)

__all__ = [
    "ExpertReviewSystem",
    "ExpertProfile",
    "ExpertReviewRequest",
]
