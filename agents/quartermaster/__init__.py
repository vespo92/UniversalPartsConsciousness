"""
Agent_19: QUARTERMASTER - Supply Chain & Sourcing Intelligence
The Master of Procurement

"Knowing a part exists is worthless if you can't get it.
I know where every part lives, who has it, when it arrives, and who to trust."

The sourcing backbone of Universal Parts Consciousness.
Tracks inventory across distributors, detects counterfeits,
predicts lead times, and optimizes sourcing decisions.
"""

from .quartermaster_agent import (
    # Enums
    SupplierTier,
    CounterfeitRisk,
    # Data classes
    SupplierProfile,
    InventoryResult,
    CounterfeitAssessment,
    LeadTimePrediction,
    SourcingOptimization,
    # Main agent
    QuartermasterAgent,
)

__version__ = "1.0.0"
__agent_id__ = "AGENT_19"
__agent_name__ = "Supply Chain & Sourcing Intelligence"
__agent_alias__ = "QUARTERMASTER"

__all__ = [
    # Enums
    "SupplierTier",
    "CounterfeitRisk",
    # Data classes
    "SupplierProfile",
    "InventoryResult",
    "CounterfeitAssessment",
    "LeadTimePrediction",
    "SourcingOptimization",
    # Agent
    "QuartermasterAgent",
]
