"""
Agent_2: Compatibility Oracle (ORACLE)
The Prophet of Perfect Fit

"Will it fit? Will it hold? Will it fail?
These questions haunt every engineer. I am the answer that ends the doubt."

The mathematical core of Universal Parts Consciousness.
Deals in certainties: thread engagement, strength verification,
tolerance stack analysis, and compatibility determination.
"""

from .engine.compatibility_core import UniversalCompatibilityChecker, CompatibilityResult
from .engine.thread_calculator import ThreadEngagementCalculator, EngagementResult
from .engine.strength_calculator import StrengthCalculator, StrengthResult
from .engine.tolerance_analyzer import ToleranceStackAnalyzer, ToleranceStackResult
from .engine.material_compatibility import MaterialCompatibilityChecker, GalvanicRisk

from .substitution.substitution_engine import SubstitutionEngine, SubstitutionRecommendation
from .substitution.equivalence_graph import EquivalenceGraph
from .substitution.ranking_algorithm import SubstitutionRanker

from .prediction.failure_predictor import FailurePredictor, FailurePrediction
from .prediction.fatigue_analyzer import FatigueAnalyzer, FatigueResult
from .prediction.safety_factor_engine import SafetyFactorEngine

from .api.compatibility_api import CompatibilityAPI
from .api.batch_checker import BatchCompatibilityChecker
from .cache.compatibility_cache import CompatibilityCache

from .oracle_agent import OracleAgent, create_oracle_agent

__version__ = "1.0.0"
__agent_id__ = "AGENT_2"
__agent_name__ = "Compatibility Oracle"
__agent_alias__ = "ORACLE"

__all__ = [
    # Core Engine
    "UniversalCompatibilityChecker",
    "CompatibilityResult",
    "ThreadEngagementCalculator",
    "EngagementResult",
    "StrengthCalculator",
    "StrengthResult",
    "ToleranceStackAnalyzer",
    "ToleranceStackResult",
    "MaterialCompatibilityChecker",
    "GalvanicRisk",
    # Substitution
    "SubstitutionEngine",
    "SubstitutionRecommendation",
    "EquivalenceGraph",
    "SubstitutionRanker",
    # Prediction
    "FailurePredictor",
    "FailurePrediction",
    "FatigueAnalyzer",
    "FatigueResult",
    "SafetyFactorEngine",
    # API
    "CompatibilityAPI",
    "BatchCompatibilityChecker",
    "CompatibilityCache",
    # Agent
    "OracleAgent",
    "create_oracle_agent",
]
