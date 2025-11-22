"""
Pattern detection modules for PROPHET agent.
Implements 5-layer emergence detection architecture.
"""

from .pattern_detector import (
    EmergenceDetectionEngine,
    PatternDetectionConfig,
    PatternDetector,
)
from .statistical_patterns import StatisticalPatternDetector
from .behavioral_patterns import BehavioralPatternDetector
from .relational_patterns import RelationalPatternDetector
from .innovation_patterns import InnovationPatternDetector
from .meta_patterns import MetaPatternDetector

__all__ = [
    "EmergenceDetectionEngine",
    "PatternDetectionConfig",
    "PatternDetector",
    "StatisticalPatternDetector",
    "BehavioralPatternDetector",
    "RelationalPatternDetector",
    "InnovationPatternDetector",
    "MetaPatternDetector",
]
