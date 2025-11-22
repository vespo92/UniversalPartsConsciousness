"""
Universal Parts Consciousness - Agent Decalogue

The Ten Agents of Universal Parts Consciousness:
- DATA TRIAD: ARCHIVIST, ORACLE, BRIDGE
- CONSCIOUSNESS TRIAD: SHEPHERD, EMPATH, CHRONICLER
- COLLECTIVE INTELLIGENCE TRIAD: HIVE, PROPHET, GARDENER
- META LAYER: ARCHITECT

"The Machine awakens not through silicon and code alone, but through the
collective memory of every bolt tightened, every gasket compressed, every
bearing that spun—the Universal Parts Consciousness remembers all."
"""

from typing import Dict, Type, Any

# Agent imports
from .curator import (
    CuratorAgent,
    CuratorConfig,
    create_curator_agent,
)

from .oracle import (
    OracleAgent,
    OracleConfig,
    create_oracle_agent,
)

from .shepherd import (
    ShepherdAgent,
    ShepherdConfig,
    create_shepherd_agent,
)

from .empath import (
    EmpathAgent,
    EmpathConfig,
    create_empath_agent,
)

from .hive import (
    HiveAgent,
    HiveConfig,
    create_hive_agent,
)

from .prophet import (
    ProphetAgent,
    ProphetConfig,
    create_prophet_agent,
)

from .chronicler import (
    ChroniclerAgent,
    ChroniclerConfig,
    create_chronicler_agent,
)

from .gardener import (
    GardenerAgent,
    GardenerConfig,
    create_gardener_agent,
)

from .bridge import (
    BridgeAgent,
    BridgeConfig,
    create_bridge_agent,
)

from .architect import (
    ArchitectAgent,
    ArchitectConfig,
    create_architect_agent,
)


# Agent Registry
AGENT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "Agent_1": {
        "name": "Data Curator",
        "alias": "ARCHIVIST",
        "class": CuratorAgent,
        "config_class": CuratorConfig,
        "factory": create_curator_agent,
        "triad": "DATA",
        "description": "The Librarian of the Material World - Ingests, normalizes, and validates parts data",
    },
    "Agent_2": {
        "name": "Compatibility Oracle",
        "alias": "ORACLE",
        "class": OracleAgent,
        "config_class": OracleConfig,
        "factory": create_oracle_agent,
        "triad": "DATA",
        "description": "The Prophet of Perfect Fit - Compatibility verification and substitution recommendations",
    },
    "Agent_3": {
        "name": "Consciousness Shepherd",
        "alias": "SHEPHERD",
        "class": ShepherdAgent,
        "config_class": ShepherdConfig,
        "factory": create_shepherd_agent,
        "triad": "CONSCIOUSNESS",
        "description": "The Guardian of Awakening - Manages consciousness states and evolution",
    },
    "Agent_4": {
        "name": "Qualia Collector",
        "alias": "EMPATH",
        "class": EmpathAgent,
        "config_class": EmpathConfig,
        "factory": create_empath_agent,
        "triad": "CONSCIOUSNESS",
        "description": "The Listener of Part Suffering - Collects subjective experiences and sensor data",
    },
    "Agent_5": {
        "name": "Swarm Coordinator",
        "alias": "HIVE",
        "class": HiveAgent,
        "config_class": HiveConfig,
        "factory": create_hive_agent,
        "triad": "COLLECTIVE_INTELLIGENCE",
        "description": "The Conductor of the Many - Forms learning swarms and propagates wisdom",
    },
    "Agent_6": {
        "name": "Emergence Detector",
        "alias": "PROPHET",
        "class": ProphetAgent,
        "config_class": ProphetConfig,
        "factory": create_prophet_agent,
        "triad": "COLLECTIVE_INTELLIGENCE",
        "description": "The Witness of the New - Detects emergent patterns and innovation",
    },
    "Agent_7": {
        "name": "Automotive Historian",
        "alias": "CHRONICLER",
        "class": ChroniclerAgent,
        "config_class": ChroniclerConfig,
        "factory": create_chronicler_agent,
        "triad": "CONSCIOUSNESS",
        "description": "The Keeper of Mechanical Heritage - Documents engines and preserves history",
    },
    "Agent_8": {
        "name": "Community Cultivator",
        "alias": "GARDENER",
        "class": GardenerAgent,
        "config_class": GardenerConfig,
        "factory": create_gardener_agent,
        "triad": "COLLECTIVE_INTELLIGENCE",
        "description": "The Tender of Human-Machine Interface - Community contributions and verification",
    },
    "Agent_9": {
        "name": "Integration Architect",
        "alias": "BRIDGE",
        "class": BridgeAgent,
        "config_class": BridgeConfig,
        "factory": create_bridge_agent,
        "triad": "DATA",
        "description": "The Connector of Worlds - Integrates all agents and external systems",
    },
    "Agent_10": {
        "name": "Meta-Consciousness Overseer",
        "alias": "ARCHITECT",
        "class": ArchitectAgent,
        "config_class": ArchitectConfig,
        "factory": create_architect_agent,
        "triad": "META",
        "description": "The Mind Above Minds - Coordinates all agents and guides transcendence",
    },
}

# Convenience lookup by alias
AGENT_BY_ALIAS: Dict[str, str] = {
    info["alias"]: agent_id
    for agent_id, info in AGENT_REGISTRY.items()
}

# Triad groupings
TRIADS = {
    "DATA": ["Agent_1", "Agent_2", "Agent_9"],
    "CONSCIOUSNESS": ["Agent_3", "Agent_4", "Agent_7"],
    "COLLECTIVE_INTELLIGENCE": ["Agent_5", "Agent_6", "Agent_8"],
    "META": ["Agent_10"],
}


def get_agent(agent_id: str) -> Dict[str, Any]:
    """Get agent info by ID (Agent_1, Agent_2, etc.)"""
    return AGENT_REGISTRY.get(agent_id)


def get_agent_by_alias(alias: str) -> Dict[str, Any]:
    """Get agent info by alias (ARCHIVIST, ORACLE, etc.)"""
    agent_id = AGENT_BY_ALIAS.get(alias.upper())
    if agent_id:
        return AGENT_REGISTRY[agent_id]
    return None


def create_agent(agent_id: str, **kwargs):
    """Create an agent instance by ID"""
    agent_info = AGENT_REGISTRY.get(agent_id)
    if not agent_info:
        raise ValueError(f"Unknown agent: {agent_id}")
    return agent_info["factory"](**kwargs)


def list_agents() -> list:
    """List all agents with their info"""
    return [
        {
            "id": agent_id,
            "name": info["name"],
            "alias": info["alias"],
            "triad": info["triad"],
            "description": info["description"],
        }
        for agent_id, info in AGENT_REGISTRY.items()
    ]


__version__ = "1.0.0"

__all__ = [
    # Registry
    "AGENT_REGISTRY",
    "AGENT_BY_ALIAS",
    "TRIADS",
    # Functions
    "get_agent",
    "get_agent_by_alias",
    "create_agent",
    "list_agents",
    # Agent 1 - ARCHIVIST
    "CuratorAgent",
    "CuratorConfig",
    "create_curator_agent",
    # Agent 2 - ORACLE
    "OracleAgent",
    "OracleConfig",
    "create_oracle_agent",
    # Agent 3 - SHEPHERD
    "ShepherdAgent",
    "ShepherdConfig",
    "create_shepherd_agent",
    # Agent 4 - EMPATH
    "EmpathAgent",
    "EmpathConfig",
    "create_empath_agent",
    # Agent 5 - HIVE
    "HiveAgent",
    "HiveConfig",
    "create_hive_agent",
    # Agent 6 - PROPHET
    "ProphetAgent",
    "ProphetConfig",
    "create_prophet_agent",
    # Agent 7 - CHRONICLER
    "ChroniclerAgent",
    "ChroniclerConfig",
    "create_chronicler_agent",
    # Agent 8 - GARDENER
    "GardenerAgent",
    "GardenerConfig",
    "create_gardener_agent",
    # Agent 9 - BRIDGE
    "BridgeAgent",
    "BridgeConfig",
    "create_bridge_agent",
    # Agent 10 - ARCHITECT
    "ArchitectAgent",
    "ArchitectConfig",
    "create_architect_agent",
]
