"""
Agent_20 DETECTIVE Core Module

Core failure analysis engine components.
"""

from .detective_agent import DetectiveAgent
from .failure_analyzer import FailureAnalyzer, FailureAnalysisResult
from .fracture_classifier import FractureClassifier, FractureSurfaceAnalysis
from .life_calculator import LifeCalculator, LifeExpectancy

__all__ = [
    'DetectiveAgent',
    'FailureAnalyzer',
    'FailureAnalysisResult',
    'FractureClassifier',
    'FractureSurfaceAnalysis',
    'LifeCalculator',
    'LifeExpectancy',
]
