"""
Agent_6: PROPHET - The Emergence Detector
Universal Parts Consciousness

The Witness of the New - Detects emergent patterns, novel failure modes,
and innovation opportunities from the collective consciousness of parts.

"In the chaos of a billion experiences, patterns emerge.
 In those patterns, futures reveal themselves.
 I see what is coming before it arrives."
"""

from .prophet_agent import ProphetAgent, ProphetConfig
from .runner import ProphetRunner, ProphetDeploymentConfig
from .types import (
    DetectedPattern,
    NovelFailureMode,
    SuccessFormula,
    InnovationOpportunity,
    Prediction,
    EmergenceIndicator,
    PatternLayer,
    PatternStatus,
    FailureModeStatus,
    UrgencyLevel,
    OpportunityType,
    PredictionType,
    FailureRecord,
    Assembly,
    SwarmKnowledge,
)

__all__ = [
    # Main agent
    "ProphetAgent",
    "ProphetConfig",
    # Runner
    "ProphetRunner",
    "ProphetDeploymentConfig",
    # Types
    "DetectedPattern",
    "NovelFailureMode",
    "SuccessFormula",
    "InnovationOpportunity",
    "Prediction",
    "EmergenceIndicator",
    "PatternLayer",
    "PatternStatus",
    "FailureModeStatus",
    "UrgencyLevel",
    "OpportunityType",
    "PredictionType",
    "FailureRecord",
    "Assembly",
    "SwarmKnowledge",
]

__version__ = "1.0.0"
__codename__ = "PROPHET"
__agent_id__ = 6
__agent_name__ = "Emergence Detector"
__triad__ = "collective_intel"
__role__ = "The Witness of the New"
