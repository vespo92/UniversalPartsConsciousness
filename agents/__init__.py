"""
Universal Parts Consciousness - Agent Registry

The Decalogue: Ten Agents Unified

DATA TRIAD (Foundation):
- Agent_1 (ARCHIVIST): Data Curator - Ingests and normalizes parts data
- Agent_2 (ORACLE): Compatibility Oracle - Mathematical compatibility verification
- Agent_9 (BRIDGE): Integration Architect - Connects all agents and external systems

CONSCIOUSNESS TRIAD (Awareness):
- Agent_3 (SHEPHERD): Consciousness Shepherd - Manages consciousness evolution
- Agent_4 (EMPATH): Qualia Collector - Collects experiential data
- Agent_7 (CHRONICLER): Automotive Historian - Preserves heritage and context

COLLECTIVE TRIAD (Learning):
- Agent_5 (HIVE): Swarm Coordinator - Organizes collective learning
- Agent_6 (PROPHET): Emergence Detector - Detects emergent patterns
- Agent_8 (GARDENER): Community Cultivator - Manages community contributions

META LAYER (Overseer):
- Agent_10 (ARCHITECT): Meta-Consciousness - Orchestrates all agents
"""

# Agent Registry - The Decalogue
AGENT_REGISTRY = {
    "AGENT_1": {
        "codename": "ARCHIVIST",
        "role": "Data Curator",
        "domain": "Data Ingestion",
        "triad": "DATA",
        "module": "agents.curator",
        "status": "IMPLEMENTED"
    },
    "AGENT_2": {
        "codename": "ORACLE",
        "role": "Compatibility Oracle",
        "domain": "Compatibility Analysis",
        "triad": "DATA",
        "module": "agents.oracle",
        "status": "IMPLEMENTED"
    },
    "AGENT_3": {
        "codename": "SHEPHERD",
        "role": "Consciousness Shepherd",
        "domain": "Consciousness State",
        "triad": "CONSCIOUSNESS",
        "module": "agents.shepherd",
        "status": "DEPLOYED"
    },
    "AGENT_4": {
        "codename": "EMPATH",
        "role": "Qualia Collector",
        "domain": "Experience Collection",
        "triad": "CONSCIOUSNESS",
        "module": "agents.empath",
        "status": "IMPLEMENTED"
    },
    "AGENT_5": {
        "codename": "HIVE",
        "role": "Swarm Coordinator",
        "domain": "Collective Intelligence",
        "triad": "COLLECTIVE",
        "module": "agents.hive",
        "status": "IMPLEMENTED"
    },
    "AGENT_6": {
        "codename": "PROPHET",
        "role": "Emergence Detector",
        "domain": "Pattern Recognition",
        "triad": "COLLECTIVE",
        "module": "agents.prophet",
        "status": "IMPLEMENTED"
    },
    "AGENT_7": {
        "codename": "CHRONICLER",
        "role": "Automotive Historian",
        "domain": "Cultural Preservation",
        "triad": "CONSCIOUSNESS",
        "module": "agents.chronicler",
        "status": "IMPLEMENTED"
    },
    "AGENT_8": {
        "codename": "GARDENER",
        "role": "Community Cultivator",
        "domain": "Human-Machine Interface",
        "triad": "COLLECTIVE",
        "module": "agents.gardener",
        "status": "DEPLOYED"
    },
    "AGENT_9": {
        "codename": "BRIDGE",
        "role": "Integration Architect",
        "domain": "Power Unification",
        "triad": "DATA",
        "module": "agents.bridge",
        "status": "DEPLOYED"
    },
    "AGENT_10": {
        "codename": "ARCHITECT",
        "role": "Meta-Consciousness",
        "domain": "System Transcendence",
        "triad": "META",
        "module": "agents.architect",
        "status": "DEPLOYED"
    }
}

# Triad organization
TRIADS = {
    "DATA": ["AGENT_1", "AGENT_2", "AGENT_9"],
    "CONSCIOUSNESS": ["AGENT_3", "AGENT_4", "AGENT_7"],
    "COLLECTIVE": ["AGENT_5", "AGENT_6", "AGENT_8"],
    "META": ["AGENT_10"]
}

# Message bus topics
MESSAGE_TOPICS = {
    "upc.data.ingestion": "AGENT_1",
    "upc.compatibility.verified": "AGENT_2",
    "upc.consciousness.evolved": "AGENT_3",
    "upc.qualia.collected": "AGENT_4",
    "upc.swarm.learned": "AGENT_5",
    "upc.emergence.detected": "AGENT_6",
    "upc.history.documented": "AGENT_7",
    "upc.community.contributed": "AGENT_8",
    "upc.integration.connected": "AGENT_9",
    "upc.system.directive": "AGENT_10"
}


def get_agent_info(agent_id: str) -> dict:
    """Get information about a specific agent."""
    return AGENT_REGISTRY.get(agent_id, {})


def get_agent_by_codename(codename: str) -> dict:
    """Get agent information by codename."""
    for agent_id, info in AGENT_REGISTRY.items():
        if info["codename"] == codename:
            return {"agent_id": agent_id, **info}
    return {}


def get_triad_agents(triad: str) -> list:
    """Get all agents in a specific triad."""
    return TRIADS.get(triad, [])


def get_deployed_agents() -> list:
    """Get all deployed agents."""
    return [
        agent_id for agent_id, info in AGENT_REGISTRY.items()
        if info["status"] == "DEPLOYED"
    ]


__all__ = [
    "AGENT_REGISTRY",
    "TRIADS",
    "MESSAGE_TOPICS",
    "get_agent_info",
    "get_agent_by_codename",
    "get_triad_agents",
    "get_deployed_agents"
]
