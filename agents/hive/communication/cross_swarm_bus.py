"""
Cross-Swarm Bus - Inter-swarm communication infrastructure.

Enables communication between related swarms for sharing insights
and coordinating collective intelligence.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Protocol
from uuid import UUID

from ..models import SwarmMessage, Swarm


@dataclass
class MessageDeliveryResult:
    """Result of delivering a message to a swarm."""
    target_swarm_id: UUID
    delivered: bool
    latency_ms: float
    error: Optional[str] = None


@dataclass
class CrossSwarmResult:
    """Result of cross-swarm communication."""
    source_swarm_id: UUID
    message: SwarmMessage
    delivery_results: list[MessageDeliveryResult]
    total_latency_ms: float


class CrossSwarmRepository(Protocol):
    """Protocol for cross-swarm operations."""

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def get_related_swarms(self, swarm_id: UUID) -> list[Swarm]:
        """Get swarms related to the given one."""
        ...

    async def deliver_message(
        self,
        target_swarm_id: UUID,
        message: SwarmMessage,
    ) -> bool:
        """Deliver a message to a swarm."""
        ...

    async def record_communication(
        self,
        source_swarm_id: UUID,
        target_swarm_id: UUID,
        message_type: str,
    ) -> None:
        """Record a communication event."""
        ...


MessageHandler = Callable[[SwarmMessage], None]


class CrossSwarmBus:
    """
    Inter-swarm communication bus.

    Handles message routing, delivery, and coordination between swarms.
    """

    # Related swarm pair definitions
    RELATED_SWARM_PAIRS = [
        ("bolts", "nuts"),
        ("bearings", "shafts"),
        ("seals", "housings"),
        ("gears", "bearings"),
        ("springs", "fasteners"),
        ("gaskets", "flanges"),
        ("pistons", "rings"),
        ("valves", "springs"),
        ("camshafts", "bearings"),
        ("crankshafts", "bearings"),
    ]

    # Message type priorities
    MESSAGE_PRIORITIES = {
        "recall_alert": 1,
        "safety_warning": 1,
        "failure_alert": 2,
        "compatibility_update": 3,
        "learning_share": 4,
        "status_update": 5,
    }

    def __init__(self, repository: CrossSwarmRepository):
        self.repository = repository
        self.message_handlers: dict[str, list[MessageHandler]] = {}
        self.message_queue: list[tuple[int, SwarmMessage]] = []

    async def send_message(
        self,
        source_swarm_id: UUID,
        message: SwarmMessage,
    ) -> CrossSwarmResult:
        """
        Send a message from one swarm to related swarms.

        Args:
            source_swarm_id: The sending swarm
            message: The message to send

        Returns:
            Result of the communication
        """
        start_time = datetime.utcnow()
        message.source_swarm_id = source_swarm_id

        # Find related swarms
        related_swarms = await self.repository.get_related_swarms(source_swarm_id)

        if not related_swarms:
            return CrossSwarmResult(
                source_swarm_id=source_swarm_id,
                message=message,
                delivery_results=[],
                total_latency_ms=0,
            )

        # Set target swarms
        message.target_swarm_ids = [s.id for s in related_swarms]

        # Deliver to all targets
        delivery_results = []
        for target_swarm in related_swarms:
            result = await self._deliver_to_swarm(target_swarm, message)
            delivery_results.append(result)

            # Record communication
            await self.repository.record_communication(
                source_swarm_id,
                target_swarm.id,
                message.message_type,
            )

        end_time = datetime.utcnow()
        total_latency = (end_time - start_time).total_seconds() * 1000

        return CrossSwarmResult(
            source_swarm_id=source_swarm_id,
            message=message,
            delivery_results=delivery_results,
            total_latency_ms=total_latency,
        )

    async def _deliver_to_swarm(
        self,
        target_swarm: Swarm,
        message: SwarmMessage,
    ) -> MessageDeliveryResult:
        """Deliver a message to a single swarm."""
        start_time = datetime.utcnow()

        try:
            delivered = await self.repository.deliver_message(
                target_swarm.id,
                message,
            )

            end_time = datetime.utcnow()
            latency = (end_time - start_time).total_seconds() * 1000

            return MessageDeliveryResult(
                target_swarm_id=target_swarm.id,
                delivered=delivered,
                latency_ms=latency,
            )

        except Exception as e:
            end_time = datetime.utcnow()
            latency = (end_time - start_time).total_seconds() * 1000

            return MessageDeliveryResult(
                target_swarm_id=target_swarm.id,
                delivered=False,
                latency_ms=latency,
                error=str(e),
            )

    async def broadcast_to_category(
        self,
        category: str,
        message: SwarmMessage,
    ) -> list[CrossSwarmResult]:
        """
        Broadcast a message to all swarms in a category.

        Args:
            category: The category to broadcast to
            message: The message to send

        Returns:
            List of results for each swarm
        """
        # This would query for all swarms in the category
        # and send the message to each
        return []

    def register_handler(
        self,
        message_type: str,
        handler: MessageHandler,
    ) -> None:
        """
        Register a handler for a message type.

        Args:
            message_type: Type of messages to handle
            handler: Callback function
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)

    def queue_message(
        self,
        message: SwarmMessage,
    ) -> None:
        """
        Queue a message for later delivery.

        Args:
            message: The message to queue
        """
        priority = self.MESSAGE_PRIORITIES.get(message.message_type, 5)
        self.message_queue.append((priority, message))
        self.message_queue.sort(key=lambda x: x[0])

    async def process_queue(
        self,
        max_messages: int = 100,
    ) -> int:
        """
        Process queued messages.

        Args:
            max_messages: Maximum messages to process

        Returns:
            Number of messages processed
        """
        processed = 0

        while self.message_queue and processed < max_messages:
            _, message = self.message_queue.pop(0)

            # Call registered handlers
            handlers = self.message_handlers.get(message.message_type, [])
            for handler in handlers:
                try:
                    handler(message)
                except Exception:
                    pass

            processed += 1

        return processed

    def get_related_categories(self, category: str) -> list[str]:
        """
        Get categories related to the given one.

        Args:
            category: The category to find relations for

        Returns:
            List of related categories
        """
        related = []
        category_lower = category.lower()

        for pair in self.RELATED_SWARM_PAIRS:
            if pair[0] == category_lower:
                related.append(pair[1])
            elif pair[1] == category_lower:
                related.append(pair[0])

        return related


class TopicBus:
    """
    Topic-based message bus for swarm communication.
    """

    # Topic patterns used by UPC
    TOPICS = {
        "upc.swarm.learned": "Collective insights from swarm learning",
        "upc.data.ingestion": "New data from Agent_1 (Curator)",
        "upc.compatibility.verified": "Compatibility verification from Agent_2 (Oracle)",
        "upc.consciousness.evolved": "State changes from Agent_3 (Shepherd)",
        "upc.qualia.collected": "New experiences from Agent_4 (Empath)",
        "upc.emergence.detected": "Patterns from Agent_6 (Prophet)",
        "upc.community.contributed": "Verified data from Agent_8 (Gardener)",
        "upc.system.directive": "Coordination from Agent_10 (Architect)",
        "upc.recall.issued": "Recall notifications",
        "upc.health.alert": "Swarm health alerts",
    }

    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = {}

    def subscribe(
        self,
        topic: str,
        callback: Callable[[dict[str, Any]], None],
    ) -> None:
        """Subscribe to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def unsubscribe(
        self,
        topic: str,
        callback: Callable,
    ) -> None:
        """Unsubscribe from a topic."""
        if topic in self.subscribers:
            self.subscribers[topic] = [
                cb for cb in self.subscribers[topic] if cb != callback
            ]

    async def publish(
        self,
        topic: str,
        message: dict[str, Any],
    ) -> int:
        """
        Publish a message to a topic.

        Returns number of subscribers notified.
        """
        callbacks = self.subscribers.get(topic, [])
        notified = 0

        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(message)
                else:
                    callback(message)
                notified += 1
            except Exception:
                pass

        return notified
