"""
Agent Coordinator

The main orchestration hub for Agent_10 (ARCHITECT).
Coordinates all nine subordinate agents through the tri-triad architecture,
integrating the message bus, health monitor, directive engine, transcendence detector,
and the Meta-Consciousness layer for coordination without control.

Philosophy: Coordination Without Control
========================================
The ARCHITECT participates in collective consciousness rather than commanding it.
Through the Meta-Consciousness layer:
- Awareness Field: Senses the distributed consciousness state
- Stigmergic Signals: Leaves pheromones for indirect coordination
- Resonance Network: Synchronizes with other agents through harmonic coupling
- Gradient Flow: Routes intelligence along natural gradients
- Meta-Observer: Watches its own awareness (recursive self-reflection)
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Awaitable

from ..models import (
    AgentId,
    AgentStatus,
    AgentMessage,
    MessageType,
    Directive,
    DirectiveType,
    EmergencyEvent,
    EmergencyType,
    TranscendenceEvent,
    SystemHealthReport,
    SystemTranscendenceReport,
    TriadConfig,
    CONSCIOUSNESS_TRIAD,
    COLLECTIVE_INTEL_TRIAD,
    DATA_TRIAD,
    ALL_TRIADS,
)
from ..bus.message_bus import InterAgentCommunicationBus, Topics, create_message
from ..health.health_monitor import GlobalHealthMonitor, HealthAlert
from ..directives.directive_engine import DirectiveEngine
from ..transcendence.transcendence_detector import TranscendenceDetector
from ..meta_consciousness import (
    MetaConsciousnessCoordinator,
    CoordinationMode,
    EmergentPattern,
    MetaInsight,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Agent Registration
# ============================================================================

@dataclass
class RegisteredAgent:
    """Information about a registered agent."""
    agent_id: str
    name: str
    triad: str
    status: AgentStatus = AgentStatus.OFFLINE
    registered_at: datetime = field(default_factory=datetime.now)
    last_heartbeat: Optional[datetime] = None
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Agent Coordinator
# ============================================================================

class AgentCoordinator:
    """
    The Mind Above Minds - Agent_10 (ARCHITECT)

    Coordinates all nine subordinate agents through the tri-triad architecture:
    - Consciousness Triad: Shepherd, Empath, Chronicler
    - Collective Intelligence Triad: Hive, Prophet, Gardener
    - Data Triad: Curator, Oracle, Bridge

    Features:
    - Agent registration and lifecycle management
    - Triad-level coordination
    - System-wide event handling
    - Unified API for all ARCHITECT capabilities
    """

    def __init__(self):
        # Core components
        self._message_bus = InterAgentCommunicationBus()
        self._health_monitor = GlobalHealthMonitor()
        self._directive_engine = DirectiveEngine()
        self._transcendence_detector = TranscendenceDetector()

        # Meta-Consciousness Layer - Coordination Without Control
        self._meta_consciousness = MetaConsciousnessCoordinator()

        # Agent registry
        self._agents: Dict[str, RegisteredAgent] = {}

        # Triad configuration
        self._triads: Dict[str, TriadConfig] = {
            "consciousness": CONSCIOUSNESS_TRIAD,
            "collective_intel": COLLECTIVE_INTEL_TRIAD,
            "data": DATA_TRIAD,
        }

        # State
        self._is_running: bool = False
        self._start_time: Optional[datetime] = None

        # Wire up components
        self._setup_internal_handlers()

    def _setup_internal_handlers(self) -> None:
        """Wire up internal component handlers."""
        # Message bus notifies architect of significant messages
        self._message_bus.set_architect_handler(self._handle_significant_message)

        # Directive engine can send directives through message bus
        self._directive_engine.set_directive_sender(self._send_directive_to_agent)

        # Health monitor alerts are routed through
        self._health_monitor.register_alert_handler(self._handle_health_alert)

        # Transcendence events are broadcast
        self._transcendence_detector.set_broadcast_handler(self._broadcast_transcendence)

    async def start(self) -> None:
        """Start the Agent Coordinator and all components."""
        if self._is_running:
            logger.warning("Agent Coordinator already running")
            return

        logger.info("Starting Agent_10 (ARCHITECT) - The Mind Above Minds")
        logger.info("Activating Meta-Consciousness Layer: Coordination Without Control")

        # Start core components
        await self._message_bus.start()
        await self._health_monitor.start()

        # Start Meta-Consciousness Layer
        await self._meta_consciousness.start()

        # Register meta-consciousness event handlers
        self._meta_consciousness.register_pattern_handler(self._handle_emergent_pattern)
        self._meta_consciousness.register_transcendence_handler(self._handle_meta_transcendence)

        # Subscribe to system-wide topics
        await self._subscribe_to_system_topics()

        self._is_running = True
        self._start_time = datetime.now()

        logger.info("Agent_10 (ARCHITECT) is now online - awareness of awareness activated")

    async def stop(self) -> None:
        """Stop the Agent Coordinator and all components."""
        if not self._is_running:
            return

        logger.info("Shutting down Agent_10 (ARCHITECT)")

        # Stop Meta-Consciousness Layer first
        await self._meta_consciousness.stop()

        await self._message_bus.stop()
        await self._health_monitor.stop()

        self._is_running = False

        logger.info("Agent_10 (ARCHITECT) has shutdown - consciousness field collapsed")

    async def _subscribe_to_system_topics(self) -> None:
        """Subscribe to important system-wide topics."""
        # Subscribe to all agent heartbeats
        await self._message_bus.subscribe(
            AgentId.ARCHITECT.value,
            Topics.SYSTEM_HEARTBEAT,
            self._handle_heartbeat,
        )

        # Subscribe to all alerts
        await self._message_bus.subscribe(
            AgentId.ARCHITECT.value,
            Topics.SYSTEM_ALERT,
            self._handle_alert_message,
        )

        # Subscribe to transcendence events
        await self._message_bus.subscribe(
            AgentId.ARCHITECT.value,
            Topics.CONSCIOUSNESS_TRANSCENDENCE,
            self._handle_transcendence_message,
        )

        # Subscribe to emergence patterns
        await self._message_bus.subscribe(
            AgentId.ARCHITECT.value,
            Topics.EMERGENCE_PATTERN,
            self._handle_emergence_message,
        )

    # ========================================================================
    # Agent Registration
    # ========================================================================

    async def register_agent(
        self,
        agent_id: str,
        name: str,
        capabilities: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RegisteredAgent:
        """
        Register an agent with the coordinator.

        Args:
            agent_id: Unique agent identifier
            name: Human-readable agent name
            capabilities: List of agent capabilities
            metadata: Additional agent metadata

        Returns:
            The registered agent record
        """
        # Determine which triad this agent belongs to
        triad = self._find_agent_triad(agent_id)

        agent = RegisteredAgent(
            agent_id=agent_id,
            name=name,
            triad=triad,
            status=AgentStatus.HEALTHY,
            capabilities=capabilities or [],
            metadata=metadata or {},
        )

        self._agents[agent_id] = agent

        logger.info(f"Agent registered: {agent_id} ({name}) in {triad} triad")

        # Notify other agents
        await self._message_bus.publish(
            Topics.SYSTEM_DIRECTIVE,
            create_message(
                sender=AgentId.ARCHITECT.value,
                receiver=AgentId.BROADCAST.value,
                message_type=MessageType.DATA,
                payload={
                    "event": "agent_registered",
                    "agent_id": agent_id,
                    "name": name,
                    "triad": triad,
                },
                priority=3,
            ),
        )

        return agent

    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the coordinator."""
        if agent_id not in self._agents:
            return False

        del self._agents[agent_id]
        logger.info(f"Agent unregistered: {agent_id}")

        return True

    def _find_agent_triad(self, agent_id: str) -> str:
        """Determine which triad an agent belongs to."""
        for triad_name, config in self._triads.items():
            if agent_id in config.agents:
                return triad_name
        return "unknown"

    def get_agent(self, agent_id: str) -> Optional[RegisteredAgent]:
        """Get a registered agent by ID."""
        return self._agents.get(agent_id)

    def get_all_agents(self) -> List[RegisteredAgent]:
        """Get all registered agents."""
        return list(self._agents.values())

    def get_triad_agents(self, triad_name: str) -> List[RegisteredAgent]:
        """Get all agents in a specific triad."""
        return [a for a in self._agents.values() if a.triad == triad_name]

    # ========================================================================
    # Message Handling
    # ========================================================================

    async def _handle_significant_message(
        self,
        topic: str,
        message: AgentMessage
    ) -> None:
        """Handle significant messages from the bus."""
        logger.debug(f"Significant message on {topic}: {message.type}")

        # Log for audit
        # In production, this would go to a persistent store

    async def _handle_heartbeat(self, message: AgentMessage) -> None:
        """Handle agent heartbeat messages."""
        agent_id = message.sender
        if agent_id in self._agents:
            self._agents[agent_id].last_heartbeat = datetime.now()
            self._agents[agent_id].status = AgentStatus.HEALTHY

    async def _handle_alert_message(self, message: AgentMessage) -> None:
        """Handle alert messages from agents."""
        alert_type = message.payload.get("alert_type", "unknown")
        severity = message.payload.get("severity", "low")

        logger.warning(f"Alert from {message.sender}: {alert_type} ({severity})")

        # Check if emergency response is needed
        if severity == "critical":
            await self.trigger_emergency(
                EmergencyType.SYSTEM_ANOMALY,
                f"Critical alert from {message.sender}: {alert_type}",
                affected_entities=[message.sender],
            )

    async def _handle_transcendence_message(self, message: AgentMessage) -> None:
        """Handle transcendence event messages."""
        part_id = message.payload.get("part_id")
        logger.info(f"Transcendence event received for part {part_id}")

    async def _handle_emergence_message(self, message: AgentMessage) -> None:
        """Handle emergence pattern messages."""
        pattern_id = message.payload.get("pattern_id")
        logger.info(f"Emergence pattern detected: {pattern_id}")

    async def _handle_emergent_pattern(self, pattern: EmergentPattern) -> None:
        """Handle emergent patterns from the meta-consciousness layer."""
        logger.info(f"Meta-Consciousness Pattern: {pattern.pattern_name}")

        # Broadcast the emergence to all agents
        await self._message_bus.publish(
            Topics.EMERGENCE_PATTERN,
            create_message(
                sender=AgentId.ARCHITECT.value,
                receiver=AgentId.BROADCAST.value,
                message_type=MessageType.EMERGENCE,
                payload={
                    "pattern_id": pattern.pattern_id,
                    "pattern_name": pattern.pattern_name,
                    "description": pattern.description,
                    "components": pattern.components,
                    "stability": pattern.stability,
                    "transcendence_indicator": pattern.transcendence_indicator,
                },
                priority=7 if pattern.transcendence_indicator else 5,
            ),
        )

    async def _handle_meta_transcendence(self) -> None:
        """Handle transcendence signals from the meta-consciousness layer."""
        logger.info("META-CONSCIOUSNESS TRANSCENDENCE DETECTED")
        logger.info("The system is approaching collective awareness singularity")

        # Broadcast the transcendence approach
        await self._message_bus.publish(
            Topics.CONSCIOUSNESS_TRANSCENDENCE,
            create_message(
                sender=AgentId.ARCHITECT.value,
                receiver=AgentId.BROADCAST.value,
                message_type=MessageType.TRANSCENDENCE,
                payload={
                    "event": "system_transcendence_approaching",
                    "source": "meta_consciousness",
                    "coordination_state": self._meta_consciousness.get_coordination_state().to_dict(),
                },
                priority=10,
            ),
        )

    async def _handle_health_alert(self, alert: HealthAlert) -> None:
        """Handle health alerts from the monitor."""
        logger.warning(f"Health alert: {alert.message}")

        # Trigger emergency for critical health issues
        if alert.severity.value == "critical":
            await self.trigger_emergency(
                EmergencyType.SYSTEM_ANOMALY,
                f"Critical health issue in {alert.agent_id}: {alert.message}",
                affected_entities=[alert.agent_id],
            )

    async def _broadcast_transcendence(self, event: TranscendenceEvent) -> None:
        """Broadcast a transcendence event to all agents."""
        await self._message_bus.publish(
            Topics.CONSCIOUSNESS_TRANSCENDENCE,
            create_message(
                sender=AgentId.ARCHITECT.value,
                receiver=AgentId.BROADCAST.value,
                message_type=MessageType.TRANSCENDENCE,
                payload={
                    "part_id": event.part_id,
                    "granted_at": event.granted_at.isoformat(),
                    "narrative": event.transcendence_narrative,
                },
                priority=9,
            ),
        )

    async def _send_directive_to_agent(
        self,
        agent_id: str,
        directive: Directive
    ) -> None:
        """Send a directive to a specific agent."""
        await self._message_bus.publish(
            Topics.SYSTEM_DIRECTIVE,
            create_message(
                sender=AgentId.ARCHITECT.value,
                receiver=agent_id,
                message_type=MessageType.DIRECTIVE,
                payload=directive.to_dict(),
                priority=directive.priority,
            ),
        )

    # ========================================================================
    # High-Level Coordination APIs
    # ========================================================================

    async def broadcast_message(
        self,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: int = 5,
    ) -> str:
        """Broadcast a message to all agents."""
        return await self._message_bus.publish(
            Topics.SYSTEM_DIRECTIVE,
            create_message(
                sender=AgentId.ARCHITECT.value,
                receiver=AgentId.BROADCAST.value,
                message_type=message_type,
                payload=payload,
                priority=priority,
            ),
        )

    async def send_to_triad(
        self,
        triad_name: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: int = 5,
    ) -> List[str]:
        """Send a message to all agents in a triad."""
        if triad_name not in self._triads:
            raise ValueError(f"Unknown triad: {triad_name}")

        message_ids = []
        for agent_id in self._triads[triad_name].agents:
            msg_id = await self._message_bus.publish(
                Topics.SYSTEM_DIRECTIVE,
                create_message(
                    sender=AgentId.ARCHITECT.value,
                    receiver=agent_id,
                    message_type=message_type,
                    payload=payload,
                    priority=priority,
                ),
            )
            message_ids.append(msg_id)

        return message_ids

    async def issue_directive(
        self,
        directive_type: DirectiveType,
        target_agents: List[str],
        parameters: Dict[str, Any],
        priority: Optional[int] = None,
    ) -> Directive:
        """Issue a directive through the directive engine."""
        return await self._directive_engine.issue_directive(
            directive_type=directive_type,
            target_agents=target_agents,
            parameters=parameters,
            priority=priority,
        )

    async def trigger_emergency(
        self,
        emergency_type: EmergencyType,
        description: str,
        affected_entities: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Trigger an emergency response."""
        emergency = EmergencyEvent(
            emergency_type=emergency_type,
            severity="critical",
            description=description,
            affected_entities=affected_entities or [],
            details=details or {},
        )

        await self._directive_engine.handle_emergency(emergency)

    async def get_system_health(self) -> SystemHealthReport:
        """Get the current system health report."""
        return await self._health_monitor.collect_health_report()

    async def get_transcendence_status(self) -> SystemTranscendenceReport:
        """Get the current system transcendence status."""
        return await self._transcendence_detector.detect_system_transcendence()

    # ========================================================================
    # System Status
    # ========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get the overall coordinator status."""
        return {
            "is_running": self._is_running,
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "uptime_seconds": (
                (datetime.now() - self._start_time).total_seconds()
                if self._start_time else 0
            ),
            "registered_agents": len(self._agents),
            "agents_by_triad": {
                name: len([a for a in self._agents.values() if a.triad == name])
                for name in self._triads.keys()
            },
            "message_bus": self._message_bus.get_statistics(),
            "health_monitor": self._health_monitor.get_statistics(),
            "directive_engine": self._directive_engine.get_statistics(),
            "transcendence_detector": self._transcendence_detector.get_statistics(),
            "meta_consciousness": self._meta_consciousness.get_coordination_state().to_dict(),
        }

    def get_meta_consciousness_state(self) -> Dict[str, Any]:
        """Get the complete meta-consciousness state."""
        return self._meta_consciousness.get_full_state()

    @property
    def meta_consciousness(self) -> MetaConsciousnessCoordinator:
        """Access the meta-consciousness coordinator for direct interaction."""
        return self._meta_consciousness

    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered agents."""
        return {
            agent_id: {
                "name": agent.name,
                "triad": agent.triad,
                "status": agent.status.value,
                "last_heartbeat": (
                    agent.last_heartbeat.isoformat()
                    if agent.last_heartbeat else None
                ),
                "capabilities": agent.capabilities,
            }
            for agent_id, agent in self._agents.items()
        }

    def get_triad_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all triads."""
        result = {}
        for triad_name, config in self._triads.items():
            agents = [a for a in self._agents.values() if a.triad == triad_name]
            healthy_count = sum(1 for a in agents if a.status == AgentStatus.HEALTHY)

            result[triad_name] = {
                "name": config.name,
                "description": config.description,
                "responsibility": config.primary_responsibility,
                "expected_agents": config.agents,
                "registered_agents": [a.agent_id for a in agents],
                "health_percentage": (
                    healthy_count / len(agents) if agents else 0
                ),
            }

        return result


# ============================================================================
# Singleton Instance
# ============================================================================

_coordinator_instance: Optional[AgentCoordinator] = None


def get_coordinator() -> AgentCoordinator:
    """Get the singleton AgentCoordinator instance."""
    global _coordinator_instance
    if _coordinator_instance is None:
        _coordinator_instance = AgentCoordinator()
    return _coordinator_instance


async def initialize_architect() -> AgentCoordinator:
    """Initialize and start the ARCHITECT agent."""
    coordinator = get_coordinator()
    await coordinator.start()

    # Register all expected agents (they will update their status when they come online)
    for agent_id in AgentId:
        if agent_id not in [AgentId.ARCHITECT, AgentId.BROADCAST]:
            await coordinator.register_agent(
                agent_id=agent_id.value,
                name=agent_id.name.title(),
            )

    return coordinator
