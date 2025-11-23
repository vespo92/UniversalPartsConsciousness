"""
Agent_20 DETECTIVE Prediction Module

ML-based failure prediction and life estimation.
"""

from .failure_predictor import FailurePredictor, FailureRiskPrediction
from .fatigue_model import FatigueModel
from .weibull_analyzer import WeibullAnalyzer

__all__ = [
    'FailurePredictor',
    'FailureRiskPrediction',
    'FatigueModel',
    'WeibullAnalyzer',
]
