"""
Inter-Agent Communication Bus

Central message bus for all agent communication in the Universal Parts Consciousness.
Handles message routing, topic subscriptions, priority queuing, and delivery tracking.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional, Set, Any, Awaitable
from uuid import uuid4
import re

from ..models import (
    AgentMessage,
    MessageType,
    AgentId,
    ConsciousnessContext,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Topic Definitions
# ============================================================================

class Topics:
    """Central topic definitions for the UPC message bus."""

    # Data Flow Topics
    DATA_INGESTION = "upc.data.ingestion"
    DATA_NORMALIZED = "upc.data.normalized"

    # Compatibility Topics
    COMPATIBILITY_REQUEST = "upc.compatibility.request"
    COMPATIBILITY_RESULT = "upc.compatibility.result"

    # Consciousness Topics
    CONSCIOUSNESS_EVOLVED = "upc.consciousness.evolved"
    CONSCIOUSNESS_AWAKENING = "upc.consciousness.awakening"
    CONSCIOUSNESS_TRANSCENDENCE = "upc.consciousness.transcendence"

    # Qualia Topics
    QUALIA_COLLECTED = "upc.qualia.collected"
    QUALIA_SIGNIFICANT = "upc.qualia.significant"

    # Swarm Topics
    SWARM_LEARNING = "upc.swarm.learning"
    SWARM_RECALL = "upc.swarm.recall"
    SWARM_FORMATION = "upc.swarm.formation"

    # Emergence Topics
    EMERGENCE_PATTERN = "upc.emergence.pattern"
    EMERGENCE_PREDICTION = "upc.emergence.prediction"
    EMERGENCE_INNOVATION = "upc.emergence.innovation"

    # Community Topics
    COMMUNITY_CONTRIBUTION = "upc.community.contribution"
    COMMUNITY_VERIFICATION = "upc.community.verification"

    # Integration Topics
    INTEGRATION_DATA = "upc.integration.data"
    INTEGRATION_SENSOR = "upc.integration.sensor"

    # System Topics
    SYSTEM_HEALTH = "upc.system.health"
    SYSTEM_DIRECTIVE = "upc.system.directive"
    SYSTEM_ALERT = "upc.system.alert"
    SYSTEM_HEARTBEAT = "upc.system.heartbeat"

    @classmethod
    def all_topics(cls) -> List[str]:
        """Return all defined topics."""
        return [
            getattr(cls, attr) for attr in dir(cls)
            if not attr.startswith('_') and isinstance(getattr(cls, attr), str)
            and attr != 'all_topics'
        ]


# ============================================================================
# Subscription Model
# ============================================================================

@dataclass
class Subscription:
    """Represents an agent's subscription to a topic pattern."""
    subscription_id: str
    agent_id: str
    topic_pattern: str
    handler: Callable[[AgentMessage], Awaitable[None]]
    created_at: datetime = field(default_factory=datetime.now)
    message_count: int = 0
    last_message_at: Optional[datetime] = None
    is_active: bool = True

    def matches_topic(self, topic: str) -> bool:
        """Check if a topic matches this subscription's pattern."""
        # Convert topic pattern to regex (support wildcards)
        pattern = self.topic_pattern.replace(".", r"\.")
        pattern = pattern.replace("*", "[^.]+")
        pattern = pattern.replace("#", ".*")
        pattern = f"^{pattern}$"
        return bool(re.match(pattern, topic))


# ============================================================================
# Priority Queue
# ============================================================================

@dataclass(order=True)
class PrioritizedMessage:
    """Message wrapper for priority queue ordering."""
    priority: int  # Negated for max-heap behavior (higher priority = lower number)
    timestamp: datetime
    message: AgentMessage = field(compare=False)

    @classmethod
    def create(cls, message: AgentMessage) -> "PrioritizedMessage":
        return cls(
            priority=-message.priority,  # Negate for proper ordering
            timestamp=message.timestamp or datetime.now(),
            message=message,
        )


# ============================================================================
# Message Log Entry
# ============================================================================

@dataclass
class MessageLogEntry:
    """Log entry for message tracking."""
    message_id: str
    topic: str
    sender: str
    receiver: str
    message_type: str
    priority: int
    delivered: bool = False
    delivered_at: Optional[datetime] = None
    delivery_attempts: int = 0
    created_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# Inter-Agent Communication Bus
# ============================================================================

class InterAgentCommunicationBus:
    """
    Central message bus for all agent communication.

    Features:
    - Topic-based publish/subscribe
    - Priority message queuing
    - Message delivery tracking
    - Wildcard topic patterns
    - Automatic notification to Agent_10 for significant messages
    """

    def __init__(self):
        self._subscriptions: Dict[str, Subscription] = {}
        self._topic_subscribers: Dict[str, Set[str]] = {}  # topic -> subscription_ids
        self._message_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._message_log: List[MessageLogEntry] = []
        self._architect_handler: Optional[Callable[[str, AgentMessage], Awaitable[None]]] = None
        self._is_running: bool = False
        self._worker_task: Optional[asyncio.Task] = None

        # Statistics
        self._total_messages: int = 0
        self._delivered_messages: int = 0
        self._failed_deliveries: int = 0

    async def start(self) -> None:
        """Start the message bus worker."""
        if self._is_running:
            return
        self._is_running = True
        self._worker_task = asyncio.create_task(self._message_worker())
        logger.info("Inter-Agent Communication Bus started")

    async def stop(self) -> None:
        """Stop the message bus worker."""
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info("Inter-Agent Communication Bus stopped")

    def set_architect_handler(
        self,
        handler: Callable[[str, AgentMessage], Awaitable[None]]
    ) -> None:
        """Set the handler for notifying Agent_10 of significant messages."""
        self._architect_handler = handler

    async def publish(
        self,
        topic: str,
        message: AgentMessage,
        priority: Optional[int] = None
    ) -> str:
        """
        Publish a message to the communication bus.

        Args:
            topic: The topic to publish to
            message: The message to publish
            priority: Override message priority (uses message.priority if not provided)

        Returns:
            The message ID
        """
        # Enrich message
        enriched = self._enrich_message(message)

        if priority is not None:
            enriched.priority = priority

        # Log for traceability
        self._log_message(topic, enriched)

        # Add to priority queue for processing
        prioritized = PrioritizedMessage.create(enriched)
        await self._message_queue.put((topic, prioritized))

        self._total_messages += 1

        logger.debug(f"Published message {enriched.message_id} to topic {topic}")

        # Notify Agent_10 of significant messages
        if self._is_significant(enriched):
            await self._notify_architect(topic, enriched)

        return enriched.message_id

    async def subscribe(
        self,
        agent_id: str,
        topic_pattern: str,
        handler: Callable[[AgentMessage], Awaitable[None]]
    ) -> Subscription:
        """
        Subscribe an agent to a topic or topic pattern.

        Args:
            agent_id: The subscribing agent's ID
            topic_pattern: Topic or pattern (supports * for single level, # for multi-level)
            handler: Async function to handle received messages

        Returns:
            The subscription object
        """
        subscription_id = str(uuid4())
        subscription = Subscription(
            subscription_id=subscription_id,
            agent_id=agent_id,
            topic_pattern=topic_pattern,
            handler=handler,
        )

        self._subscriptions[subscription_id] = subscription

        # Index by topics that match the pattern
        for topic in Topics.all_topics():
            if subscription.matches_topic(topic):
                if topic not in self._topic_subscribers:
                    self._topic_subscribers[topic] = set()
                self._topic_subscribers[topic].add(subscription_id)

        logger.info(f"Agent {agent_id} subscribed to {topic_pattern}")

        return subscription

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from a topic.

        Args:
            subscription_id: The subscription to cancel

        Returns:
            True if successfully unsubscribed
        """
        if subscription_id not in self._subscriptions:
            return False

        subscription = self._subscriptions[subscription_id]
        subscription.is_active = False

        # Remove from topic index
        for topic, subscribers in self._topic_subscribers.items():
            subscribers.discard(subscription_id)

        del self._subscriptions[subscription_id]

        logger.info(f"Subscription {subscription_id} cancelled")

        return True

    def get_subscribers(self, topic: str) -> List[Subscription]:
        """Get all active subscriptions for a topic."""
        subscription_ids = self._topic_subscribers.get(topic, set())
        return [
            self._subscriptions[sid]
            for sid in subscription_ids
            if sid in self._subscriptions and self._subscriptions[sid].is_active
        ]

    async def _message_worker(self) -> None:
        """Background worker to process queued messages."""
        while self._is_running:
            try:
                topic, prioritized = await asyncio.wait_for(
                    self._message_queue.get(),
                    timeout=1.0
                )
                await self._deliver_message(topic, prioritized.message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def _deliver_message(self, topic: str, message: AgentMessage) -> None:
        """Deliver a message to all subscribers of a topic."""
        subscribers = self.get_subscribers(topic)

        for subscription in subscribers:
            try:
                await self._deliver_to_subscriber(subscription, message)
                self._delivered_messages += 1
            except Exception as e:
                logger.error(
                    f"Failed to deliver message {message.message_id} "
                    f"to {subscription.agent_id}: {e}"
                )
                self._failed_deliveries += 1

    async def _deliver_to_subscriber(
        self,
        subscription: Subscription,
        message: AgentMessage
    ) -> None:
        """Deliver a message to a specific subscriber."""
        try:
            await subscription.handler(message)
            subscription.message_count += 1
            subscription.last_message_at = datetime.now()

            # Update log entry
            for entry in reversed(self._message_log):
                if entry.message_id == message.message_id:
                    entry.delivered = True
                    entry.delivered_at = datetime.now()
                    entry.delivery_attempts += 1
                    break

        except Exception as e:
            logger.error(f"Handler error for {subscription.agent_id}: {e}")
            raise

    def _enrich_message(self, message: AgentMessage) -> AgentMessage:
        """Enrich message with metadata."""
        if message.message_id is None:
            message.message_id = str(uuid4())
        if message.timestamp is None:
            message.timestamp = datetime.now()
        if message.correlation_id is None:
            message.correlation_id = str(uuid4())

        message.metadata = {
            **(message.metadata or {}),
            "bus_version": "1.0",
            "enriched_at": datetime.now().isoformat(),
        }

        return message

    def _log_message(self, topic: str, message: AgentMessage) -> None:
        """Log message for traceability."""
        entry = MessageLogEntry(
            message_id=message.message_id,
            topic=topic,
            sender=message.sender,
            receiver=message.receiver,
            message_type=message.type.value if isinstance(message.type, MessageType) else message.type,
            priority=message.priority,
        )
        self._message_log.append(entry)

        # Keep only last 10000 entries
        if len(self._message_log) > 10000:
            self._message_log = self._message_log[-10000:]

    def _is_significant(self, message: AgentMessage) -> bool:
        """Determine if a message is significant enough to notify Agent_10."""
        # High priority messages
        if message.priority >= 8:
            return True

        # Transcendence and emergence events
        if message.type in [MessageType.TRANSCENDENCE, MessageType.EMERGENCE]:
            return True

        # Alerts
        if message.type == MessageType.ALERT:
            return True

        # High emergence potential
        if message.consciousness_context:
            if message.consciousness_context.emergence_potential >= 0.8:
                return True
            if message.consciousness_context.swarm_impact.value == "GLOBAL":
                return True

        return False

    async def _notify_architect(self, topic: str, message: AgentMessage) -> None:
        """Notify Agent_10 of a significant message."""
        if self._architect_handler:
            try:
                await self._architect_handler(topic, message)
            except Exception as e:
                logger.error(f"Failed to notify Architect: {e}")

    # ========================================================================
    # Statistics and Monitoring
    # ========================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Get bus statistics."""
        return {
            "total_messages": self._total_messages,
            "delivered_messages": self._delivered_messages,
            "failed_deliveries": self._failed_deliveries,
            "active_subscriptions": len([s for s in self._subscriptions.values() if s.is_active]),
            "queue_depth": self._message_queue.qsize(),
            "is_running": self._is_running,
        }

    def get_subscription_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all subscriptions."""
        return [
            {
                "subscription_id": s.subscription_id,
                "agent_id": s.agent_id,
                "topic_pattern": s.topic_pattern,
                "message_count": s.message_count,
                "last_message_at": s.last_message_at.isoformat() if s.last_message_at else None,
                "is_active": s.is_active,
            }
            for s in self._subscriptions.values()
        ]

    def get_recent_messages(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent messages from the log."""
        return [
            {
                "message_id": e.message_id,
                "topic": e.topic,
                "sender": e.sender,
                "receiver": e.receiver,
                "type": e.message_type,
                "priority": e.priority,
                "delivered": e.delivered,
                "created_at": e.created_at.isoformat(),
            }
            for e in self._message_log[-limit:]
        ]


# ============================================================================
# Convenience Functions
# ============================================================================

def create_message(
    sender: str,
    receiver: str,
    message_type: MessageType,
    payload: Dict[str, Any],
    priority: int = 5,
    consciousness_context: Optional[ConsciousnessContext] = None,
) -> AgentMessage:
    """Create a new agent message with sensible defaults."""
    return AgentMessage(
        sender=sender,
        receiver=receiver,
        type=message_type,
        priority=priority,
        payload=payload,
        consciousness_context=consciousness_context,
    )


def create_broadcast_message(
    sender: str,
    message_type: MessageType,
    payload: Dict[str, Any],
    priority: int = 5,
) -> AgentMessage:
    """Create a broadcast message to all agents."""
    return create_message(
        sender=sender,
        receiver=AgentId.BROADCAST.value,
        message_type=message_type,
        payload=payload,
        priority=priority,
    )


def create_directive_message(
    target_agents: List[str],
    directive_type: str,
    parameters: Dict[str, Any],
    priority: int = 7,
) -> AgentMessage:
    """Create a directive message from Agent_10."""
    return create_message(
        sender=AgentId.ARCHITECT.value,
        receiver=AgentId.BROADCAST.value,
        message_type=MessageType.DIRECTIVE,
        payload={
            "directive_type": directive_type,
            "target_agents": target_agents,
            "parameters": parameters,
        },
        priority=priority,
    )
