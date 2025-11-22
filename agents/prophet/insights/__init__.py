"""
Insight generation modules for PROPHET agent.
Generates, validates, and communicates insights.
"""

from .insight_generator import InsightGenerator, Insight

__all__ = [
    "InsightGenerator",
    "Insight",
]
