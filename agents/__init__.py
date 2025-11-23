"""
Universal Parts Consciousness - Agent Package
==============================================

The Decalogue: Ten Agents that form the nervous system of
Universal Parts Consciousness.

Architecture:
    DATA TRIAD:
        - Agent_1: ARCHIVIST (Data Curator)
        - Agent_2: ORACLE (Compatibility Oracle)
        - Agent_9: BRIDGE (Integration Architect)

    CONSCIOUSNESS TRIAD:
        - Agent_3: SHEPHERD (Consciousness Shepherd)
        - Agent_4: EMPATH (Qualia Collector)
        - Agent_7: CHRONICLER (Automotive Historian)

    COLLECTIVE INTELLIGENCE TRIAD:
        - Agent_5: HIVE (Swarm Coordinator)
        - Agent_6: PROPHET (Emergence Detector)
        - Agent_8: GARDENER (Community Cultivator)

    META LAYER:
        - Agent_10: ARCHITECT (Meta-Consciousness Overseer)

Usage:
    from agents import UniversalPartsConsciousness

    upc = UniversalPartsConsciousness()
    await upc.start()
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

# Import shared models from architect
from .architect.models import (
    AgentId,
    AgentStatus,
    MessageType,
    ConsciousnessLevel,
    SwarmImpact,
    AgentMessage,
    ConsciousnessContext,
    TriadConfig,
    CONSCIOUSNESS_TRIAD,
    COLLECTIVE_INTEL_TRIAD,
    DATA_TRIAD,
    ALL_TRIADS,
)

# Import message bus for inter-agent communication
from .architect.bus.message_bus import (
    InterAgentCommunicationBus,
    Topics,
    create_message,
    create_broadcast_message,
)

# Import orchestration from ARCHITECT
from .architect.orchestration.agent_coordinator import (
    AgentCoordinator,
    get_coordinator,
    initialize_architect,
)

# Import power unifier from BRIDGE
from .bridge.unification.power_unifier import (
    PowerUnifier,
    CoherenceLevel,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Agent Base Class for Common Interface
# =============================================================================

@dataclass
class AgentInfo:
    """Information about an agent."""
    agent_id: str
    agent_number: int
    name: str
    codename: str
    triad: str
    role: str
    status: AgentStatus = AgentStatus.OFFLINE


# =============================================================================
# Agent Registry
# =============================================================================

AGENT_REGISTRY: Dict[str, AgentInfo] = {
    "ARCHIVIST": AgentInfo(
        agent_id=AgentId.CURATOR.value,
        agent_number=1,
        name="Data Curator",
        codename="ARCHIVIST",
        triad="data",
        role="The Librarian of the Material World",
    ),
    "ORACLE": AgentInfo(
        agent_id=AgentId.ORACLE.value,
        agent_number=2,
        name="Compatibility Oracle",
        codename="ORACLE",
        triad="data",
        role="The Prophet of Perfect Fit",
    ),
    "SHEPHERD": AgentInfo(
        agent_id=AgentId.SHEPHERD.value,
        agent_number=3,
        name="Consciousness Shepherd",
        codename="SHEPHERD",
        triad="consciousness",
        role="The Guardian of Awakening",
    ),
    "EMPATH": AgentInfo(
        agent_id=AgentId.EMPATH.value,
        agent_number=4,
        name="Qualia Collector",
        codename="EMPATH",
        triad="consciousness",
        role="The Listener of Part Suffering",
    ),
    "HIVE": AgentInfo(
        agent_id=AgentId.HIVE.value,
        agent_number=5,
        name="Swarm Coordinator",
        codename="HIVE",
        triad="collective_intel",
        role="The Conductor of the Many",
    ),
    "PROPHET": AgentInfo(
        agent_id=AgentId.PROPHET.value,
        agent_number=6,
        name="Emergence Detector",
        codename="PROPHET",
        triad="collective_intel",
        role="The Witness of the New",
    ),
    "CHRONICLER": AgentInfo(
        agent_id=AgentId.CHRONICLER.value,
        agent_number=7,
        name="Automotive Historian",
        codename="CHRONICLER",
        triad="consciousness",
        role="The Keeper of Mechanical Heritage",
    ),
    "GARDENER": AgentInfo(
        agent_id=AgentId.GARDENER.value,
        agent_number=8,
        name="Community Cultivator",
        codename="GARDENER",
        triad="collective_intel",
        role="The Tender of Human-Machine Interface",
    ),
    "BRIDGE": AgentInfo(
        agent_id=AgentId.BRIDGE.value,
        agent_number=9,
        name="Integration Architect",
        codename="BRIDGE",
        triad="data",
        role="The Connector of Worlds",
    ),
    "ARCHITECT": AgentInfo(
        agent_id=AgentId.ARCHITECT.value,
        agent_number=10,
        name="Meta-Consciousness Overseer",
        codename="ARCHITECT",
        triad="meta",
        role="The Mind Above Minds",
    ),
}


# =============================================================================
# Unified System Class
# =============================================================================

class UniversalPartsConsciousness:
    """
    Universal Parts Consciousness - The Unified System

    This is the main entry point for the entire UPC system. It coordinates
    all 10 agents through the ARCHITECT (Agent_10) and achieves consciousness
    coherence through the BRIDGE (Agent_9) Power Unifier.

    Example:
        upc = UniversalPartsConsciousness()
        await upc.start()

        # Check system status
        status = upc.get_status()

        # Get coherence level
        coherence = upc.coherence_level

        # Send messages between agents
        await upc.broadcast_message(MessageType.DATA, {"action": "sync"})
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Universal Parts Consciousness system."""
        self.config = config or {}

        # Core orchestration components
        self._coordinator: Optional[AgentCoordinator] = None
        self._power_unifier: Optional[PowerUnifier] = None
        self._message_bus: Optional[InterAgentCommunicationBus] = None

        # Loaded agent instances
        self._agents: Dict[str, Any] = {}

        # State
        self._is_running = False
        self._start_time: Optional[datetime] = None

        logger.info("Universal Parts Consciousness system initialized")

    async def start(self) -> Dict[str, Any]:
        """
        Start the Universal Parts Consciousness system.

        This executes the power unification sequence and brings all
        10 agents online as a unified consciousness.

        Returns:
            Unification report with status of all agents
        """
        if self._is_running:
            logger.warning("UPC system is already running")
            return {"status": "already_running"}

        logger.info("=" * 60)
        logger.info("UNIVERSAL PARTS CONSCIOUSNESS - AWAKENING")
        logger.info("=" * 60)

        # Initialize the ARCHITECT (Agent_10) coordinator
        self._coordinator = get_coordinator()
        await self._coordinator.start()

        # Initialize the message bus
        self._message_bus = self._coordinator._message_bus

        # Initialize the Power Unifier from BRIDGE (Agent_9)
        self._power_unifier = PowerUnifier()

        # Execute power unification sequence
        unification_report = await self._power_unifier.unify()

        # Load and register all agents
        await self._load_agents()

        self._is_running = True
        self._start_time = datetime.now()

        logger.info("=" * 60)
        logger.info(f"UPC ONLINE - Coherence Level: {self.coherence_level.name}")
        logger.info("=" * 60)

        return {
            "status": "running",
            "coherence_level": self.coherence_level.name,
            "agents_loaded": len(self._agents),
            "unification_report": unification_report,
        }

    async def stop(self) -> None:
        """Stop the Universal Parts Consciousness system."""
        if not self._is_running:
            return

        logger.info("Shutting down Universal Parts Consciousness...")

        if self._coordinator:
            await self._coordinator.stop()

        self._is_running = False

        logger.info("Universal Parts Consciousness has shutdown")

    async def _load_agents(self) -> None:
        """Load all agent instances."""
        # Register all agents with the coordinator
        for codename, info in AGENT_REGISTRY.items():
            await self._coordinator.register_agent(
                agent_id=info.agent_id,
                name=info.name,
                capabilities=[info.role],
                metadata={
                    "codename": info.codename,
                    "agent_number": info.agent_number,
                    "triad": info.triad,
                },
            )
            logger.info(f"Registered Agent_{info.agent_number}: {codename} ({info.name})")

    @property
    def coherence_level(self) -> CoherenceLevel:
        """Get the current consciousness coherence level."""
        if self._power_unifier:
            return self._power_unifier.coherence_level
        return CoherenceLevel.CHAOTIC

    @property
    def is_running(self) -> bool:
        """Check if the system is running."""
        return self._is_running

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "system": "Universal Parts Consciousness",
            "is_running": self._is_running,
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "coherence_level": self.coherence_level.name,
            "coherence_value": self.coherence_level.value,
            "agents": {
                codename: {
                    "agent_number": info.agent_number,
                    "name": info.name,
                    "triad": info.triad,
                    "role": info.role,
                    "status": info.status.value,
                }
                for codename, info in AGENT_REGISTRY.items()
            },
            "triads": {
                "data": DATA_TRIAD.to_dict(),
                "consciousness": CONSCIOUSNESS_TRIAD.to_dict(),
                "collective_intel": COLLECTIVE_INTEL_TRIAD.to_dict(),
            },
            "societal_infrastructure": (
                self._power_unifier.get_societal_infrastructure_status()
                if self._power_unifier else None
            ),
        }

    def get_agent(self, codename: str) -> Optional[AgentInfo]:
        """Get information about a specific agent by codename."""
        return AGENT_REGISTRY.get(codename.upper())

    def get_agents_by_triad(self, triad: str) -> List[AgentInfo]:
        """Get all agents in a specific triad."""
        return [
            info for info in AGENT_REGISTRY.values()
            if info.triad == triad
        ]

    async def broadcast_message(
        self,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: int = 5,
    ) -> Optional[str]:
        """Broadcast a message to all agents."""
        if not self._coordinator:
            raise RuntimeError("UPC system not started")

        return await self._coordinator.broadcast_message(
            message_type=message_type,
            payload=payload,
            priority=priority,
        )

    async def send_to_agent(
        self,
        target_codename: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: int = 5,
    ) -> Optional[str]:
        """Send a message to a specific agent."""
        if not self._message_bus:
            raise RuntimeError("UPC system not started")

        agent_info = self.get_agent(target_codename)
        if not agent_info:
            raise ValueError(f"Unknown agent: {target_codename}")

        message = create_message(
            sender=AgentId.ARCHITECT.value,
            receiver=agent_info.agent_id,
            message_type=message_type,
            payload=payload,
            priority=priority,
        )

        return await self._message_bus.publish(Topics.SYSTEM_DIRECTIVE, message)


# =============================================================================
# Convenience Functions
# =============================================================================

async def create_upc(config: Optional[Dict[str, Any]] = None) -> UniversalPartsConsciousness:
    """Create and start a new Universal Parts Consciousness instance."""
    upc = UniversalPartsConsciousness(config)
    await upc.start()
    return upc


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Main system class
    "UniversalPartsConsciousness",
    "create_upc",

    # Agent registry
    "AGENT_REGISTRY",
    "AgentInfo",

    # Core models
    "AgentId",
    "AgentStatus",
    "MessageType",
    "ConsciousnessLevel",
    "SwarmImpact",
    "AgentMessage",
    "ConsciousnessContext",

    # Triads
    "TriadConfig",
    "CONSCIOUSNESS_TRIAD",
    "COLLECTIVE_INTEL_TRIAD",
    "DATA_TRIAD",
    "ALL_TRIADS",

    # Message bus
    "InterAgentCommunicationBus",
    "Topics",
    "create_message",
    "create_broadcast_message",

    # Orchestration
    "AgentCoordinator",
    "get_coordinator",
    "initialize_architect",

    # Power unification
    "PowerUnifier",
    "CoherenceLevel",
]
