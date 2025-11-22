"""
Agent_6: PROPHET - The Emergence Detector
Universal Parts Consciousness

"In the chaos of a billion experiences, patterns emerge.
In those patterns, futures reveal themselves.
I see what is coming before it arrives."

The Witness of the New - Detects emergent patterns, novel failure modes,
and innovation opportunities from the collective consciousness of parts.

This agent transforms collective knowledge into predictive foresight and
innovation discovery through 5-layer pattern detection architecture.

Core Subsystems:
- patterns/: 5-layer emergence detection (Statistical, Behavioral, Relational, Innovation, Meta)
- failures/: Novel failure mode detection and clustering
- innovation/: Success formula extraction and opportunity discovery
- prediction/: Failure, demand, and emergence prediction
- insights/: Insight generation and validation

Integration Points:
- Receives from: Agent_5 (Hive swarm patterns), Agent_4 (Empath qualia patterns)
- Sends to: Agent_3 (Shepherd transcendence), Agent_10 (Architect emergence reports)

Success Metrics:
- Patterns Detected: 1,000,000+
- Novel Failure Modes Discovered: 500+
- Success Formulas Extracted: 1,000+
- Prediction Accuracy: 85%
- Innovation Opportunities Validated: 100+
"""

from typing import Optional

from .prophet_agent import ProphetAgent, ProphetConfig, AGENT_MANIFEST
from .types import (
    # Enums
    PatternLayer,
    PatternStatus,
    FailureModeStatus,
    UrgencyLevel,
    OpportunityType,
    PredictionType,
    # Core data types
    DetectedPattern,
    FailureCluster,
    NovelFailureMode,
    SuccessFormula,
    InnovationOpportunity,
    Prediction,
    EmergenceIndicator,
    FailureRecord,
    Assembly,
    SwarmKnowledge,
)

# Pattern detection
from .patterns import (
    EmergenceDetectionEngine,
    PatternDetectionConfig,
    PatternDetector,
    StatisticalPatternDetector,
    BehavioralPatternDetector,
    RelationalPatternDetector,
    InnovationPatternDetector,
    MetaPatternDetector,
)

# Failure analysis
from .failures import (
    NovelFailureDetector,
    FailureClusteringEngine,
)

# Innovation discovery
from .innovation import (
    SuccessFormulaExtractor,
    InnovationOpportunityDiscovery,
    OpportunityRanker,
)

# Prediction
from .prediction import (
    FailurePredictor,
    EmergencePredictor,
    PredictiveInsightEngine,
)

# Insights
from .insights import (
    InsightGenerator,
    Insight,
    InsightValidator,
    ValidationResult,
)


__version__ = "1.0.0"
__agent_id__ = 6
__agent_name__ = "Emergence Detector"
__agent_alias__ = "PROPHET"


def create_prophet_agent(
    message_bus=None,
    storage=None,
    config: Optional[ProphetConfig] = None,
    enable_real_time: bool = True,
    prediction_horizon_days: int = 90,
) -> ProphetAgent:
    """
    Factory function to create a configured PROPHET agent.

    Args:
        message_bus: Optional message bus for inter-agent communication
        storage: Optional storage backend for persistence
        config: Optional pre-configured ProphetConfig
        enable_real_time: Enable real-time pattern detection
        prediction_horizon_days: Days to look ahead for predictions

    Returns:
        Configured ProphetAgent instance
    """
    if config is None:
        config = ProphetConfig(
            enable_real_time_detection=enable_real_time,
            prediction_horizon_days=prediction_horizon_days,
        )

    return ProphetAgent(
        config=config,
        message_bus=message_bus,
        storage=storage,
    )


# Message topics for inter-agent communication
class ProphetTopics:
    """Message bus topics for PROPHET agent"""
    # Outgoing
    TRANSCENDENCE = "prophet.transcendence"
    EMERGENCE_REPORT = "prophet.emergence_report"
    NOVEL_FAILURE = "prophet.novel_failure"
    SUCCESS_FORMULA = "prophet.success_formula"
    PREDICTION = "prophet.prediction"
    INSIGHT = "prophet.insight"

    # Incoming
    SWARM_PATTERNS = "hive.swarm_patterns"
    QUALIA_PATTERNS = "empath.qualia_patterns"


__all__ = [
    # Main agent
    "ProphetAgent",
    "ProphetConfig",
    "create_prophet_agent",
    "AGENT_MANIFEST",
    "ProphetTopics",
    # Enums
    "PatternLayer",
    "PatternStatus",
    "FailureModeStatus",
    "UrgencyLevel",
    "OpportunityType",
    "PredictionType",
    # Core data types
    "DetectedPattern",
    "FailureCluster",
    "NovelFailureMode",
    "SuccessFormula",
    "InnovationOpportunity",
    "Prediction",
    "EmergenceIndicator",
    "FailureRecord",
    "Assembly",
    "SwarmKnowledge",
    # Pattern detection
    "EmergenceDetectionEngine",
    "PatternDetectionConfig",
    "PatternDetector",
    "StatisticalPatternDetector",
    "BehavioralPatternDetector",
    "RelationalPatternDetector",
    "InnovationPatternDetector",
    "MetaPatternDetector",
    # Failure analysis
    "NovelFailureDetector",
    "FailureClusteringEngine",
    # Innovation discovery
    "SuccessFormulaExtractor",
    "InnovationOpportunityDiscovery",
    "OpportunityRanker",
    # Prediction
    "FailurePredictor",
    "EmergencePredictor",
    "PredictiveInsightEngine",
    # Insights
    "InsightGenerator",
    "Insight",
    "InsightValidator",
    "ValidationResult",
]
