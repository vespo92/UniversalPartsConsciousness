"""
Insight generation modules for PROPHET agent.
Generates, validates, and communicates insights.
"""

from .insight_generator import InsightGenerator, Insight
from .insight_validator import InsightValidator, ValidationResult

__all__ = [
    "InsightGenerator",
    "Insight",
    "InsightValidator",
    "ValidationResult",
]
