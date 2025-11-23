"""
Agent_11 MARINER - Integration Module

Connects MARINER to the broader UPC agent network.

Integration Points:
- Agent_2 (ORACLE): Enhanced compatibility with galvanic data
- Agent_4 (EMPATH): Collect qualia from marine experiences
- Agent_9 (BRIDGE): Integration architecture
- Agent_18 (ALCHEMIST): Material science collaboration
- Agent_20 (DETECTIVE): Failure analysis for marine failures
"""

from .agent_bridge import (
    MarinerBridge,
    OracleIntegration,
    AlchemistIntegration,
)

__all__ = [
    "MarinerBridge",
    "OracleIntegration",
    "AlchemistIntegration",
]
