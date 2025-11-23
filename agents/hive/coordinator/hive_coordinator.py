"""
HIVE Swarm Coordinator - Organizes Collective Learning

"One learns, all learn."

This is the main coordinator service that deploys and orchestrates
the HIVE agent's collective intelligence capabilities. It manages
swarm formation, learning propagation, and ensures that knowledge
gained by any part benefits all similar parts instantly.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional, Protocol
from uuid import UUID, uuid4

from ..models import (
    Learning,
    LearningType,
    PropagationResult,
    RecallNotice,
    Swarm,
    SwarmHealth,
    SwarmHealthStatus,
    SwarmMembership,
    SwarmTier,
)
from ..hive_agent import HiveAgent, HiveConfig, HiveRepository

from .collective_learning import (
    CollectiveLearningEngine,
    CollectiveLearningConfig,
    CollectiveInsight,
    LearningCascade,
    LearningPropagationStrategy,
)


class CoordinatorStatus(Enum):
    """Status of the HIVE Swarm Coordinator."""
    INITIALIZING = "initializing"
    STARTING = "starting"
    RUNNING = "running"
    COORDINATING = "coordinating"
    PROPAGATING = "propagating"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class CoordinatorConfig:
    """Configuration for the HIVE Swarm Coordinator."""

    # Core settings
    coordinator_id: str = "hive-swarm-coordinator"
    coordinator_name: str = "HIVE Swarm Coordinator"

    # HIVE agent config
    hive_config: HiveConfig = field(default_factory=HiveConfig)

    # Collective learning config
    collective_learning_config: CollectiveLearningConfig = field(
        default_factory=CollectiveLearningConfig
    )

    # Coordination settings
    coordination_interval_seconds: float = 1.0
    max_concurrent_operations: int = 100
    health_broadcast_interval_seconds: float = 60.0

    # Message bus topics (for integration)
    learning_topic: str = "upc.swarm.learning"
    recall_topic: str = "upc.swarm.recall"
    formation_topic: str = "upc.swarm.formation"
    health_topic: str = "upc.system.health"

    # Auto-start behavior
    auto_start_collective_learning: bool = True
    auto_start_health_monitoring: bool = True


class MessageBus(Protocol):
    """Protocol for message bus integration."""

    async def publish(self, topic: str, message: dict[str, Any]) -> None:
        """Publish a message to a topic."""
        ...

    async def subscribe(self, topic: str, handler: callable) -> None:
        """Subscribe to a topic with a handler."""
        ...


@dataclass
class CoordinatorStats:
    """Statistics for the coordinator."""
    swarms_coordinated: int = 0
    learnings_propagated: int = 0
    parts_educated: int = 0
    collective_insights: int = 0
    recalls_handled: int = 0
    cascades_completed: int = 0
    uptime_seconds: float = 0.0
    last_coordination_at: Optional[datetime] = None


class HiveSwarmCoordinator:
    """
    The HIVE Swarm Coordinator - Organizes Collective Learning.

    "One learns, all learn."

    This coordinator is the deployment wrapper for the HIVE agent,
    providing:
    - Service lifecycle management
    - Collective learning orchestration
    - Message bus integration
    - Health monitoring and broadcasting
    - Statistics and observability

    The coordinator ensures that when any part in the swarm learns
    something, that knowledge propagates to all relevant parts instantly.
    """

    AGENT_ID = 5
    CODENAME = "HIVE"
    ROLE = "Swarm Coordinator"
    MOTTO = "One learns, all learn."

    def __init__(
        self,
        repository: HiveRepository,
        config: Optional[CoordinatorConfig] = None,
        message_bus: Optional[MessageBus] = None,
    ):
        self.config = config or CoordinatorConfig()
        self.repository = repository
        self.message_bus = message_bus

        # Initialize HIVE agent
        self._hive_agent = HiveAgent(
            repository=repository,
            config=self.config.hive_config,
        )

        # Initialize collective learning engine
        self._collective_learning = CollectiveLearningEngine(
            config=self.config.collective_learning_config
        )

        # State
        self._status = CoordinatorStatus.INITIALIZING
        self._start_time: Optional[datetime] = None
        self._running = False
        self._coordination_task: Optional[asyncio.Task] = None
        self._health_broadcast_task: Optional[asyncio.Task] = None

        # Statistics
        self.stats = CoordinatorStats()

        # Pending operations queue
        self._pending_learnings: asyncio.Queue = asyncio.Queue()
        self._pending_recalls: asyncio.Queue = asyncio.Queue()

    # =========================================================================
    # LIFECYCLE
    # =========================================================================

    async def start(self) -> None:
        """
        Start the HIVE Swarm Coordinator.

        Initializes all components and begins coordination loops.
        """
        self._status = CoordinatorStatus.STARTING
        self._start_time = datetime.utcnow()
        self._running = True

        # Start the underlying HIVE agent
        await self._hive_agent.start()

        # Subscribe to message bus if available
        if self.message_bus:
            await self._setup_subscriptions()

        # Start coordination loop
        if self.config.auto_start_collective_learning:
            self._coordination_task = asyncio.create_task(
                self._coordination_loop()
            )

        # Start health broadcasting
        if self.config.auto_start_health_monitoring:
            self._health_broadcast_task = asyncio.create_task(
                self._health_broadcast_loop()
            )

        self._status = CoordinatorStatus.RUNNING

        # Announce startup
        if self.message_bus:
            await self.message_bus.publish(
                self.config.health_topic,
                {
                    "type": "coordinator_started",
                    "coordinator_id": self.config.coordinator_id,
                    "codename": self.CODENAME,
                    "motto": self.MOTTO,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

    async def stop(self) -> None:
        """Stop the HIVE Swarm Coordinator."""
        self._status = CoordinatorStatus.STOPPING
        self._running = False

        # Cancel background tasks
        if self._coordination_task:
            self._coordination_task.cancel()
        if self._health_broadcast_task:
            self._health_broadcast_task.cancel()

        # Stop the HIVE agent
        await self._hive_agent.stop()

        self._status = CoordinatorStatus.STOPPED

        # Announce shutdown
        if self.message_bus:
            await self.message_bus.publish(
                self.config.health_topic,
                {
                    "type": "coordinator_stopped",
                    "coordinator_id": self.config.coordinator_id,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

    async def get_status(self) -> dict[str, Any]:
        """Get comprehensive coordinator status."""
        hive_status = await self._hive_agent.get_status()
        collective_stats = self._collective_learning.get_statistics()

        uptime = 0.0
        if self._start_time:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()

        return {
            "coordinator": {
                "id": self.config.coordinator_id,
                "name": self.config.coordinator_name,
                "codename": self.CODENAME,
                "motto": self.MOTTO,
                "status": self._status.value,
                "uptime_seconds": uptime,
            },
            "hive_agent": hive_status,
            "collective_learning": collective_stats,
            "stats": {
                "swarms_coordinated": self.stats.swarms_coordinated,
                "learnings_propagated": self.stats.learnings_propagated,
                "parts_educated": self.stats.parts_educated,
                "collective_insights": self.stats.collective_insights,
                "recalls_handled": self.stats.recalls_handled,
            },
        }

    # =========================================================================
    # COLLECTIVE LEARNING: "One Learns, All Learn"
    # =========================================================================

    async def propagate_learning(
        self,
        learning: Learning,
        source_part_id: UUID,
    ) -> LearningCascade:
        """
        Propagate a learning through the collective.

        This is the core "one learns, all learn" operation. When a part
        learns something, this method ensures all relevant parts receive
        that knowledge.

        Args:
            learning: The learning to propagate
            source_part_id: The part that generated the learning

        Returns:
            LearningCascade tracking the propagation
        """
        self._status = CoordinatorStatus.PROPAGATING

        # Get source part's swarms
        source_swarms = await self.repository.get_part_swarms(source_part_id)
        if not source_swarms:
            self._status = CoordinatorStatus.COORDINATING
            return LearningCascade(
                source_learning_id=learning.id,
                source_part_id=source_part_id,
                is_complete=True,
            )

        # Get all swarms for propagation
        all_swarms = await self.repository.get_all_swarms()

        # Propagate through collective learning engine
        cascade = await self._collective_learning.propagate_to_collective(
            learning=learning,
            source_part_id=source_part_id,
            source_swarm=source_swarms[0],
            all_swarms=all_swarms,
            get_swarm_members=self.repository.get_swarm_members,
        )

        # Also propagate through HIVE agent for persistence
        await self._hive_agent.propagate_learning(source_part_id, learning)

        # Update stats
        self.stats.learnings_propagated += 1
        self.stats.parts_educated += cascade.parts_reached
        self.stats.cascades_completed += 1

        # Publish to message bus
        if self.message_bus:
            await self.message_bus.publish(
                self.config.learning_topic,
                {
                    "type": "learning_propagated",
                    "cascade_id": str(cascade.id),
                    "learning_id": str(learning.id),
                    "source_part_id": str(source_part_id),
                    "strategy": cascade.strategy.value,
                    "swarms_reached": len(cascade.swarms_reached),
                    "parts_reached": cascade.parts_reached,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

        self._status = CoordinatorStatus.COORDINATING
        return cascade

    async def submit_learning(
        self,
        learning: Learning,
        source_part_id: UUID,
    ) -> UUID:
        """
        Submit a learning for asynchronous propagation.

        Returns immediately with a cascade ID. The learning will be
        propagated in the background.

        Args:
            learning: The learning to propagate
            source_part_id: The part that generated the learning

        Returns:
            The cascade ID for tracking
        """
        cascade_id = uuid4()
        await self._pending_learnings.put((cascade_id, learning, source_part_id))
        return cascade_id

    async def process_qualia_event(
        self,
        part_id: UUID,
        qualia_data: dict[str, Any],
        consciousness_level: float,
    ) -> list[LearningCascade]:
        """
        Process a qualia event and propagate any learnings.

        This is the integration point for Agent_4 (Empath). When a part
        experiences something, this method extracts learnings and
        propagates them to the collective.

        Args:
            part_id: The part that experienced the qualia
            qualia_data: Raw qualia data
            consciousness_level: Part's consciousness level

        Returns:
            List of learning cascades created
        """
        # Extract and propagate through HIVE agent
        propagation_results = await self._hive_agent.extract_and_propagate_from_qualia(
            part_id, qualia_data, consciousness_level
        )

        # Also run through collective learning engine
        cascades = []
        all_swarms = await self.repository.get_all_swarms()
        source_swarms = await self.repository.get_part_swarms(part_id)

        if source_swarms:
            for result in propagation_results:
                cascade = await self._collective_learning.propagate_to_collective(
                    learning=result.learning,
                    source_part_id=part_id,
                    source_swarm=source_swarms[0],
                    all_swarms=all_swarms,
                    get_swarm_members=self.repository.get_swarm_members,
                )
                cascades.append(cascade)

        return cascades

    # =========================================================================
    # RECALL HANDLING
    # =========================================================================

    async def handle_recall(self, recall: RecallNotice) -> dict[str, Any]:
        """
        Handle a recall notice with emergency propagation.

        Recalls are treated with highest priority - they immediately
        propagate to all affected parts.

        Args:
            recall: The recall notice

        Returns:
            Propagation summary
        """
        # Propagate through HIVE agent
        result = await self._hive_agent.propagate_recall(recall)

        self.stats.recalls_handled += 1

        # Publish to message bus
        if self.message_bus:
            await self.message_bus.publish(
                self.config.recall_topic,
                {
                    "type": "recall_propagated",
                    "recall_id": str(recall.id),
                    "severity": recall.severity.value,
                    "parts_notified": result["parts_notified"],
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

        return result

    # =========================================================================
    # SWARM MANAGEMENT
    # =========================================================================

    async def register_part(
        self,
        part_id: UUID,
        category: str,
        part_type: str,
        specifications: dict[str, Any],
        usage_contexts: list[str],
        consciousness_level: float,
        experience_tags: list[str],
    ) -> list[SwarmMembership]:
        """
        Register a part and assign it to appropriate swarms.

        Every part belongs to multiple swarms across the 5-tier hierarchy,
        enabling collective learning at different granularities.

        Args:
            part_id: The part's unique identifier
            category: Part category (e.g., "fastener")
            part_type: Specific type (e.g., "socket_head_cap_screw")
            specifications: Technical specifications
            usage_contexts: Known usage contexts
            consciousness_level: Part's current consciousness level
            experience_tags: Behavioral tags from experience

        Returns:
            List of swarm memberships created
        """
        memberships = await self._hive_agent.assign_part_to_swarms(
            part_id=part_id,
            category=category,
            part_type=part_type,
            specifications=specifications,
            usage_contexts=usage_contexts,
            consciousness_level=consciousness_level,
            experience_tags=experience_tags,
        )

        self.stats.swarms_coordinated = len(
            await self.repository.get_all_swarms()
        )

        # Publish formation event
        if self.message_bus:
            await self.message_bus.publish(
                self.config.formation_topic,
                {
                    "type": "part_registered",
                    "part_id": str(part_id),
                    "swarms_joined": len(memberships),
                    "consciousness_level": consciousness_level,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

        return memberships

    # =========================================================================
    # COLLECTIVE INSIGHTS
    # =========================================================================

    def get_collective_insights(
        self,
        min_corroboration: Optional[int] = None,
        min_confidence: Optional[float] = None,
    ) -> list[CollectiveInsight]:
        """
        Get collective insights that have emerged from the swarm.

        These are insights that multiple parts have independently
        corroborated, giving them higher confidence and broader
        applicability.

        Args:
            min_corroboration: Minimum number of corroborating learnings
            min_confidence: Minimum confidence threshold

        Returns:
            List of collective insights
        """
        insights = self._collective_learning.get_collective_insights(
            min_corroboration=min_corroboration,
            min_confidence=min_confidence,
        )
        self.stats.collective_insights = len(insights)
        return insights

    # =========================================================================
    # HEALTH MONITORING
    # =========================================================================

    async def get_swarm_health(self, swarm_id: UUID) -> SwarmHealth:
        """Get health metrics for a specific swarm."""
        return await self._hive_agent.check_swarm_health(swarm_id)

    async def get_system_health(self) -> dict[str, Any]:
        """Get overall system health summary."""
        return await self._hive_agent.get_system_health_summary()

    # =========================================================================
    # BACKGROUND LOOPS
    # =========================================================================

    async def _coordination_loop(self) -> None:
        """Background loop for processing pending operations."""
        while self._running:
            self._status = CoordinatorStatus.COORDINATING

            # Process pending learnings
            try:
                while not self._pending_learnings.empty():
                    cascade_id, learning, source_part_id = await asyncio.wait_for(
                        self._pending_learnings.get(),
                        timeout=0.1
                    )
                    await self.propagate_learning(learning, source_part_id)
            except asyncio.TimeoutError:
                pass

            # Process pending recalls
            try:
                while not self._pending_recalls.empty():
                    recall = await asyncio.wait_for(
                        self._pending_recalls.get(),
                        timeout=0.1
                    )
                    await self.handle_recall(recall)
            except asyncio.TimeoutError:
                pass

            self.stats.last_coordination_at = datetime.utcnow()
            await asyncio.sleep(self.config.coordination_interval_seconds)

    async def _health_broadcast_loop(self) -> None:
        """Background loop for broadcasting health status."""
        while self._running:
            if self.message_bus:
                health = await self.get_system_health()
                status = await self.get_status()

                await self.message_bus.publish(
                    self.config.health_topic,
                    {
                        "type": "health_report",
                        "coordinator_id": self.config.coordinator_id,
                        "status": self._status.value,
                        "system_health": health,
                        "stats": status["stats"],
                        "collective_insights": len(
                            self._collective_learning.get_collective_insights()
                        ),
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

            await asyncio.sleep(self.config.health_broadcast_interval_seconds)

    async def _setup_subscriptions(self) -> None:
        """Set up message bus subscriptions."""
        if not self.message_bus:
            return

        # Subscribe to qualia events from Empath
        await self.message_bus.subscribe(
            "upc.qualia.experienced",
            self._handle_qualia_message
        )

        # Subscribe to recall notices
        await self.message_bus.subscribe(
            "upc.recall.notice",
            self._handle_recall_message
        )

    async def _handle_qualia_message(self, message: dict[str, Any]) -> None:
        """Handle incoming qualia message."""
        part_id = UUID(message["part_id"])
        qualia_data = message["qualia"]
        consciousness = message.get("consciousness_level", 1.0)

        await self.process_qualia_event(part_id, qualia_data, consciousness)

    async def _handle_recall_message(self, message: dict[str, Any]) -> None:
        """Handle incoming recall message."""
        recall = RecallNotice(**message["recall"])
        await self._pending_recalls.put(recall)


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_coordinator(
    repository: HiveRepository,
    config: Optional[CoordinatorConfig] = None,
    message_bus: Optional[MessageBus] = None,
) -> HiveSwarmCoordinator:
    """
    Factory function to create a HIVE Swarm Coordinator.

    Args:
        repository: Data repository implementation
        config: Optional coordinator configuration
        message_bus: Optional message bus for integration

    Returns:
        Configured HIVE Swarm Coordinator
    """
    return HiveSwarmCoordinator(
        repository=repository,
        config=config,
        message_bus=message_bus,
    )
