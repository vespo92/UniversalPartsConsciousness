"""
ORACLE Prediction Engine
Failure prediction, fatigue analysis, wear estimation, and safety factor calculations.
"""

from .failure_predictor import FailurePredictor, FailurePrediction, FailureMode
from .fatigue_analyzer import FatigueAnalyzer, FatigueResult, LoadType
from .safety_factor_engine import SafetyFactorEngine, SafetyFactorResult
from .wear_estimator import WearEstimator, WearPrediction, WearMechanism, WearSeverity

__all__ = [
    "FailurePredictor",
    "FailurePrediction",
    "FailureMode",
    "FatigueAnalyzer",
    "FatigueResult",
    "LoadType",
    "SafetyFactorEngine",
    "SafetyFactorResult",
    "WearEstimator",
    "WearPrediction",
    "WearMechanism",
    "WearSeverity",
]
