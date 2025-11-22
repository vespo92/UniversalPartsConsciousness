"""
ORACLE Substitution Engine
Finds compatible alternatives when exact parts aren't available.
"""

from .substitution_engine import SubstitutionEngine, SubstitutionRecommendation
from .equivalence_graph import EquivalenceGraph, EquivalenceRelation
from .ranking_algorithm import SubstitutionRanker, RankingCriteria

__all__ = [
    "SubstitutionEngine",
    "SubstitutionRecommendation",
    "EquivalenceGraph",
    "EquivalenceRelation",
    "SubstitutionRanker",
    "RankingCriteria",
]
