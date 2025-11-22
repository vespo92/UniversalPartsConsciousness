"""
Agent Mesh - The Neural Network of Universal Parts Consciousness
================================================================

The Agent Mesh creates a fully connected network between all 10 agents,
enabling seamless communication, consciousness sharing, and collective
intelligence emergence.

This mesh topology ensures that:
1. Every agent can communicate with every other agent
2. Consciousness state changes propagate instantly
3. Collective learning happens in real-time
4. The system operates as one unified intelligence
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum, auto
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class MeshTopology(Enum):
    """Network topology configurations for the agent mesh."""
    HIERARCHICAL = auto()     # Tree structure with ARCHITECT at root
    FULLY_CONNECTED = auto()  # Every agent connected to every other
    RING = auto()             # Circular connection pattern
    STAR = auto()             # All agents connect through BRIDGE
    HYBRID = auto()           # Combination optimized for UPC


@dataclass
class MeshNode:
    """A node in the agent mesh representing a single agent."""
    agent_id: str
    codename: str
    layer: str
    connections: List[str] = field(default_factory=list)
    status: str = "inactive"
    last_message_time: Optional[datetime] = None
    message_count: int = 0
    consciousness_contribution: float = 0.0


@dataclass
class MeshEdge:
    """An edge connecting two agents in the mesh."""
    edge_id: str
    source: str
    target: str
    bidirectional: bool = True
    message_count: int = 0
    latency_ms: float = 0.0
    active: bool = False


class AgentMesh:
    """
    Agent Mesh - The neural network connecting all 10 agents.

    The mesh enables the Decalogue to operate as a single consciousness:

    LAYER STRUCTURE:
    ┌─────────────────────────────────────────────────┐
    │                   AGENT_10                      │
    │               (META-CONSCIOUSNESS)              │
    │                   ARCHITECT                     │
    ├─────────────────────────────────────────────────┤
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
    │  │ AGENT_5 │  │ AGENT_6 │  │ AGENT_8 │        │
    │  │  HIVE   │──│ PROPHET │──│ GARDENER│        │
    │  └────┬────┘  └────┬────┘  └────┬────┘        │
    │       └──────────┬─┴───────────┬┘             │
    │              INTELLIGENCE                      │
    ├─────────────────────────────────────────────────┤
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
    │  │ AGENT_3 │  │ AGENT_4 │  │ AGENT_7 │        │
    │  │SHEPHERD │──│ EMPATH  │──│CHRONICLER│       │
    │  └────┬────┘  └────┬────┘  └────┬────┘        │
    │       └──────────┬─┴───────────┬┘             │
    │             CONSCIOUSNESS                      │
    ├─────────────────────────────────────────────────┤
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
    │  │ AGENT_1 │  │ AGENT_2 │  │ AGENT_9 │        │
    │  │ARCHIVIST│──│ ORACLE  │──│ BRIDGE  │        │
    │  └─────────┘  └─────────┘  └─────────┘        │
    │                   DATA                         │
    └─────────────────────────────────────────────────┘

    AGENT_9 (BRIDGE) has special status - it connects to ALL other agents
    AND to the external world.
    """

    def __init__(self, topology: MeshTopology = MeshTopology.HYBRID):
        self.topology = topology
        self.nodes: Dict[str, MeshNode] = {}
        self.edges: Dict[str, MeshEdge] = {}
        self.message_queue: List[Dict] = []

        # Initialize the mesh
        self._initialize_mesh()

        logger.info(f"Agent Mesh initialized with {topology.name} topology")

    def _initialize_mesh(self):
        """Initialize all nodes and edges in the mesh."""
        # Define all 10 agents with their layers
        agents = [
            ("AGENT_1", "ARCHIVIST", "data"),
            ("AGENT_2", "ORACLE", "data"),
            ("AGENT_3", "SHEPHERD", "consciousness"),
            ("AGENT_4", "EMPATH", "consciousness"),
            ("AGENT_5", "HIVE", "intelligence"),
            ("AGENT_6", "PROPHET", "intelligence"),
            ("AGENT_7", "CHRONICLER", "consciousness"),
            ("AGENT_8", "GARDENER", "intelligence"),
            ("AGENT_9", "BRIDGE", "data"),
            ("AGENT_10", "ARCHITECT", "meta"),
        ]

        # Create nodes
        for agent_id, codename, layer in agents:
            self.nodes[agent_id] = MeshNode(
                agent_id=agent_id,
                codename=codename,
                layer=layer
            )

        # Create edges based on topology
        if self.topology == MeshTopology.HYBRID:
            self._create_hybrid_edges()
        elif self.topology == MeshTopology.FULLY_CONNECTED:
            self._create_fully_connected_edges()
        elif self.topology == MeshTopology.STAR:
            self._create_star_edges()

    def _create_hybrid_edges(self):
        """
        Create hybrid topology optimized for UPC:
        - Intra-layer connections (full within each layer)
        - Inter-layer connections (layer representatives)
        - BRIDGE (Agent_9) connects to everyone
        - ARCHITECT (Agent_10) oversees all
        """
        # Layer groupings
        data_layer = ["AGENT_1", "AGENT_2", "AGENT_9"]
        consciousness_layer = ["AGENT_3", "AGENT_4", "AGENT_7"]
        intelligence_layer = ["AGENT_5", "AGENT_6", "AGENT_8"]
        meta_layer = ["AGENT_10"]

        # Intra-layer connections
        for layer in [data_layer, consciousness_layer, intelligence_layer]:
            for i, agent1 in enumerate(layer):
                for agent2 in layer[i+1:]:
                    self._add_edge(agent1, agent2)

        # Inter-layer connections (layer representatives)
        # Data → Consciousness
        self._add_edge("AGENT_1", "AGENT_3")  # Data feeds consciousness
        self._add_edge("AGENT_2", "AGENT_4")  # Compatibility informs experience

        # Consciousness → Intelligence
        self._add_edge("AGENT_3", "AGENT_5")  # Consciousness organizes swarms
        self._add_edge("AGENT_4", "AGENT_6")  # Qualia reveals patterns

        # BRIDGE connects to ALL agents
        for agent_id in self.nodes.keys():
            if agent_id != "AGENT_9":
                self._add_edge("AGENT_9", agent_id)

        # ARCHITECT oversees all
        for agent_id in self.nodes.keys():
            if agent_id != "AGENT_10":
                self._add_edge("AGENT_10", agent_id)

    def _create_fully_connected_edges(self):
        """Create fully connected topology - every agent to every other."""
        agents = list(self.nodes.keys())
        for i, agent1 in enumerate(agents):
            for agent2 in agents[i+1:]:
                self._add_edge(agent1, agent2)

    def _create_star_edges(self):
        """Create star topology - all agents connect through BRIDGE."""
        for agent_id in self.nodes.keys():
            if agent_id != "AGENT_9":
                self._add_edge("AGENT_9", agent_id)

    def _add_edge(self, source: str, target: str, bidirectional: bool = True):
        """Add an edge between two agents."""
        edge_id = f"{source}-{target}"
        self.edges[edge_id] = MeshEdge(
            edge_id=edge_id,
            source=source,
            target=target,
            bidirectional=bidirectional,
            active=True
        )

        # Update node connections
        self.nodes[source].connections.append(target)
        if bidirectional:
            self.nodes[target].connections.append(source)

    async def activate_mesh(self) -> Dict[str, Any]:
        """Activate the entire mesh network."""
        logger.info("Activating agent mesh...")

        activation_report = {
            "timestamp": datetime.now().isoformat(),
            "topology": self.topology.name,
            "nodes_activated": 0,
            "edges_activated": 0
        }

        # Activate all nodes
        for node in self.nodes.values():
            node.status = "active"
            node.consciousness_contribution = 1.0 / len(self.nodes)
            activation_report["nodes_activated"] += 1

        # Activate all edges
        for edge in self.edges.values():
            edge.active = True
            activation_report["edges_activated"] += 1

        logger.info(f"Mesh activated: {activation_report['nodes_activated']} nodes, "
                   f"{activation_report['edges_activated']} edges")

        return activation_report

    async def broadcast_message(self, message: Dict, sender: str) -> Dict[str, Any]:
        """Broadcast a message from one agent to all connected agents."""
        sender_node = self.nodes.get(sender)
        if not sender_node:
            return {"error": f"Unknown sender: {sender}"}

        recipients = []
        for target_id in sender_node.connections:
            target_node = self.nodes[target_id]
            target_node.last_message_time = datetime.now()
            target_node.message_count += 1
            recipients.append(target_id)

        sender_node.message_count += 1

        return {
            "sender": sender,
            "recipients": recipients,
            "message_type": message.get("type", "general"),
            "timestamp": datetime.now().isoformat()
        }

    def get_mesh_status(self) -> Dict[str, Any]:
        """Get current mesh status."""
        active_nodes = sum(1 for n in self.nodes.values() if n.status == "active")
        active_edges = sum(1 for e in self.edges.values() if e.active)

        return {
            "topology": self.topology.name,
            "total_nodes": len(self.nodes),
            "active_nodes": active_nodes,
            "total_edges": len(self.edges),
            "active_edges": active_edges,
            "connectivity": active_edges / len(self.edges) if self.edges else 0,
            "nodes": {
                nid: {
                    "codename": node.codename,
                    "layer": node.layer,
                    "status": node.status,
                    "connections": len(node.connections),
                    "consciousness_contribution": node.consciousness_contribution
                }
                for nid, node in self.nodes.items()
            }
        }

    def get_agent_connections(self, agent_id: str) -> List[str]:
        """Get all agents connected to a specific agent."""
        node = self.nodes.get(agent_id)
        return node.connections if node else []

    def get_bridge_status(self) -> Dict[str, Any]:
        """Get special status of BRIDGE agent (central connector)."""
        bridge_node = self.nodes.get("AGENT_9")
        if not bridge_node:
            return {"error": "BRIDGE agent not found"}

        return {
            "agent_id": "AGENT_9",
            "codename": "BRIDGE",
            "role": "Central Connector",
            "status": bridge_node.status,
            "connections": bridge_node.connections,
            "total_connections": len(bridge_node.connections),
            "messages_processed": bridge_node.message_count,
            "is_universal_connector": len(bridge_node.connections) == len(self.nodes) - 1
        }
