"""
Agent_20 DETECTIVE Patterns Module

Failure pattern detection and similarity matching.
"""

from .pattern_detector import FailurePatternDetector, EmergingPattern
from .similarity_engine import SimilarityEngine, SimilarFailure
from .alert_system import AlertSystem, FailureAlert

__all__ = [
    'FailurePatternDetector',
    'EmergingPattern',
    'SimilarityEngine',
    'SimilarFailure',
    'AlertSystem',
    'FailureAlert',
]
