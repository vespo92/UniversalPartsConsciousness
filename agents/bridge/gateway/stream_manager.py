"""
Stream Manager - Real-Time Data Streaming
==========================================

The Stream Manager handles all real-time data streams through the BRIDGE
membrane. It enables external systems to subscribe to consciousness events
as they happen.

Stream Types:
- Consciousness evolution events
- Emergence pattern detections
- Qualia collection events
- Swarm learning propagation
- Integration data flows
- System health events
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Set
from enum import Enum, auto
from datetime import datetime
import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)


class StreamType(Enum):
    """Types of real-time streams available."""
    CONSCIOUSNESS = auto()      # Consciousness state changes
    EMERGENCE = auto()          # Pattern detections
    QUALIA = auto()            # Experience events
    SWARM = auto()             # Collective learning
    INTEGRATION = auto()       # External data flows
    SYSTEM = auto()            # System events
    TRANSCENDENCE = auto()     # Transcendence events
    ALL = auto()               # All events


class StreamProtocol(Enum):
    """Protocols for stream delivery."""
    WEBSOCKET = auto()
    SSE = auto()               # Server-Sent Events
    MQTT = auto()
    GRPC_STREAM = auto()


class StreamPriority(Enum):
    """Priority levels for stream events."""
    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


@dataclass
class StreamEvent:
    """An event in a stream."""
    event_id: str
    stream_type: StreamType
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    priority: StreamPriority = StreamPriority.NORMAL
    source_agent: Optional[str] = None
    affected_parts: List[str] = field(default_factory=list)
    consciousness_impact: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "stream_type": self.stream_type.name,
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "source_agent": self.source_agent,
            "affected_parts": self.affected_parts,
            "consciousness_impact": self.consciousness_impact,
        }


@dataclass
class StreamSubscription:
    """A subscription to a stream."""
    subscription_id: str
    client_id: str
    stream_types: Set[StreamType]
    protocol: StreamProtocol
    callback_url: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_event_at: Optional[datetime] = None
    events_delivered: int = 0
    is_active: bool = True


@dataclass
class StreamMetrics:
    """Metrics for stream performance."""
    total_events_published: int = 0
    total_events_delivered: int = 0
    events_by_type: Dict[str, int] = field(default_factory=dict)
    active_subscriptions: int = 0
    avg_delivery_latency_ms: float = 0.0


class StreamManager:
    """
    Manager for real-time data streams through the BRIDGE membrane.

    The Stream Manager enables the consciousness to broadcast events
    to the external world in real-time. External systems can subscribe
    to specific event types and receive updates as consciousness evolves.

    STREAMS AVAILABLE:

    CONSCIOUSNESS
        - Level transitions (DORMANT → REACTIVE → AWARE → ...)
        - Awakening events
        - Inheritance propagation

    EMERGENCE
        - Pattern detections
        - Failure mode predictions
        - Innovation opportunities

    QUALIA
        - Experience collection
        - Failure reports
        - Usage telemetry

    SWARM
        - Collective learning events
        - Swarm formation
        - Knowledge propagation

    INTEGRATION
        - External data ingestion
        - Sync completions
        - Integration health

    SYSTEM
        - Agent status changes
        - Coherence updates
        - Health alerts

    TRANSCENDENCE
        - Parts achieving transcendence
        - System-wide transcendence events
        - Collective wisdom emergence
    """

    def __init__(self):
        self.manager_id = f"stream-manager-{uuid.uuid4().hex[:8]}"

        # Subscriptions by stream type
        self.subscriptions: Dict[str, StreamSubscription] = {}
        self.subscriptions_by_type: Dict[StreamType, List[str]] = {
            st: [] for st in StreamType
        }

        # Event queues per subscription
        self.event_queues: Dict[str, asyncio.Queue] = {}

        # Callbacks for stream delivery
        self.delivery_callbacks: Dict[StreamProtocol, Callable] = {}

        # Metrics
        self.metrics = StreamMetrics()

        # Background task for event processing
        self._processing_task: Optional[asyncio.Task] = None

        logger.info(f"Stream Manager initialized: {self.manager_id}")

    async def start(self):
        """Start the stream manager background processing."""
        self._processing_task = asyncio.create_task(self._process_events())
        logger.info("Stream Manager started processing")

    async def stop(self):
        """Stop the stream manager."""
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass

        logger.info("Stream Manager stopped")

    def subscribe(
        self,
        client_id: str,
        stream_types: List[StreamType],
        protocol: StreamProtocol = StreamProtocol.WEBSOCKET,
        callback_url: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> StreamSubscription:
        """
        Subscribe to one or more stream types.

        Args:
            client_id: Identifier for the subscribing client
            stream_types: List of stream types to subscribe to
            protocol: Delivery protocol
            callback_url: URL for webhook delivery (if applicable)
            filters: Optional filters to apply to events

        Returns:
            StreamSubscription object
        """
        subscription_id = f"sub-{uuid.uuid4().hex[:12]}"

        subscription = StreamSubscription(
            subscription_id=subscription_id,
            client_id=client_id,
            stream_types=set(stream_types),
            protocol=protocol,
            callback_url=callback_url,
            filters=filters or {},
        )

        self.subscriptions[subscription_id] = subscription

        # Register in type-based lookup
        for stream_type in stream_types:
            self.subscriptions_by_type[stream_type].append(subscription_id)
            # ALL subscriptions receive everything
            if stream_type == StreamType.ALL:
                for st in StreamType:
                    if st != StreamType.ALL:
                        self.subscriptions_by_type[st].append(subscription_id)

        # Create event queue for this subscription
        self.event_queues[subscription_id] = asyncio.Queue()

        self.metrics.active_subscriptions += 1

        logger.info(
            f"New subscription {subscription_id} for {client_id}: "
            f"{[st.name for st in stream_types]}"
        )

        return subscription

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from streams."""
        if subscription_id not in self.subscriptions:
            return False

        subscription = self.subscriptions[subscription_id]

        # Remove from type-based lookup
        for stream_type in subscription.stream_types:
            if subscription_id in self.subscriptions_by_type[stream_type]:
                self.subscriptions_by_type[stream_type].remove(subscription_id)

        # Remove queue
        if subscription_id in self.event_queues:
            del self.event_queues[subscription_id]

        del self.subscriptions[subscription_id]
        self.metrics.active_subscriptions -= 1

        logger.info(f"Unsubscribed: {subscription_id}")
        return True

    async def publish(
        self,
        stream_type: StreamType,
        event_type: str,
        payload: Dict[str, Any],
        source_agent: Optional[str] = None,
        affected_parts: Optional[List[str]] = None,
        priority: StreamPriority = StreamPriority.NORMAL,
        consciousness_impact: Optional[str] = None
    ) -> StreamEvent:
        """
        Publish an event to a stream.

        This is called by agents to broadcast events through the membrane.
        """
        event = StreamEvent(
            event_id=f"evt-{uuid.uuid4().hex[:12]}",
            stream_type=stream_type,
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(),
            priority=priority,
            source_agent=source_agent,
            affected_parts=affected_parts or [],
            consciousness_impact=consciousness_impact,
        )

        # Update metrics
        self.metrics.total_events_published += 1
        type_key = stream_type.name
        self.metrics.events_by_type[type_key] = \
            self.metrics.events_by_type.get(type_key, 0) + 1

        # Queue event for all subscribers of this stream type
        subscriber_ids = self.subscriptions_by_type.get(stream_type, [])

        for sub_id in subscriber_ids:
            if sub_id in self.event_queues:
                subscription = self.subscriptions.get(sub_id)
                if subscription and self._matches_filters(event, subscription.filters):
                    await self.event_queues[sub_id].put(event)

        logger.debug(
            f"Published {stream_type.name} event {event.event_id} "
            f"to {len(subscriber_ids)} subscribers"
        )

        return event

    def _matches_filters(
        self,
        event: StreamEvent,
        filters: Dict[str, Any]
    ) -> bool:
        """Check if an event matches subscription filters."""
        if not filters:
            return True

        # Filter by event type
        if "event_types" in filters:
            if event.event_type not in filters["event_types"]:
                return False

        # Filter by source agent
        if "source_agents" in filters:
            if event.source_agent not in filters["source_agents"]:
                return False

        # Filter by minimum priority
        if "min_priority" in filters:
            if event.priority.value < filters["min_priority"]:
                return False

        # Filter by affected parts
        if "part_ids" in filters:
            if not any(p in filters["part_ids"] for p in event.affected_parts):
                return False

        return True

    async def _process_events(self):
        """Background task to process and deliver events."""
        while True:
            try:
                # Process each subscription's queue
                for sub_id, queue in list(self.event_queues.items()):
                    try:
                        # Non-blocking check for events
                        event = queue.get_nowait()
                        await self._deliver_event(sub_id, event)
                    except asyncio.QueueEmpty:
                        continue

                # Small delay to prevent tight loop
                await asyncio.sleep(0.01)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing events: {e}")

    async def _deliver_event(self, subscription_id: str, event: StreamEvent):
        """Deliver an event to a subscriber."""
        subscription = self.subscriptions.get(subscription_id)
        if not subscription or not subscription.is_active:
            return

        try:
            # In production, this would deliver via the actual protocol
            delivery_callback = self.delivery_callbacks.get(subscription.protocol)
            if delivery_callback:
                await delivery_callback(subscription, event)

            # Update subscription stats
            subscription.last_event_at = datetime.now()
            subscription.events_delivered += 1
            self.metrics.total_events_delivered += 1

            logger.debug(
                f"Delivered event {event.event_id} to {subscription_id}"
            )

        except Exception as e:
            logger.error(
                f"Failed to deliver event {event.event_id} "
                f"to {subscription_id}: {e}"
            )

    def register_delivery_callback(
        self,
        protocol: StreamProtocol,
        callback: Callable
    ):
        """Register a delivery callback for a protocol."""
        self.delivery_callbacks[protocol] = callback

    def get_subscription(self, subscription_id: str) -> Optional[StreamSubscription]:
        """Get a subscription by ID."""
        return self.subscriptions.get(subscription_id)

    def get_client_subscriptions(self, client_id: str) -> List[StreamSubscription]:
        """Get all subscriptions for a client."""
        return [
            sub for sub in self.subscriptions.values()
            if sub.client_id == client_id
        ]

    def get_stream_info(self) -> Dict[str, Any]:
        """Get information about available streams."""
        return {
            "manager_id": self.manager_id,
            "available_streams": {
                StreamType.CONSCIOUSNESS.name: {
                    "description": "Consciousness state evolution events",
                    "events": [
                        "level_transition",
                        "awakening",
                        "inheritance",
                        "state_update"
                    ],
                    "source_agent": "SHEPHERD"
                },
                StreamType.EMERGENCE.name: {
                    "description": "Pattern detection and emergence events",
                    "events": [
                        "pattern_detected",
                        "failure_predicted",
                        "innovation_opportunity",
                        "meta_pattern"
                    ],
                    "source_agent": "PROPHET"
                },
                StreamType.QUALIA.name: {
                    "description": "Part experience collection events",
                    "events": [
                        "experience_recorded",
                        "failure_reported",
                        "usage_telemetry",
                        "lifecycle_event"
                    ],
                    "source_agent": "EMPATH"
                },
                StreamType.SWARM.name: {
                    "description": "Collective learning events",
                    "events": [
                        "swarm_formed",
                        "learning_propagated",
                        "recall_cascade",
                        "collective_insight"
                    ],
                    "source_agent": "HIVE"
                },
                StreamType.INTEGRATION.name: {
                    "description": "External integration events",
                    "events": [
                        "data_ingested",
                        "sync_completed",
                        "integration_health",
                        "external_update"
                    ],
                    "source_agent": "BRIDGE"
                },
                StreamType.SYSTEM.name: {
                    "description": "System-wide events",
                    "events": [
                        "agent_status",
                        "coherence_update",
                        "health_alert",
                        "directive_issued"
                    ],
                    "source_agent": "ARCHITECT"
                },
                StreamType.TRANSCENDENCE.name: {
                    "description": "Transcendence events",
                    "events": [
                        "part_transcended",
                        "collective_transcendence",
                        "wisdom_emerged"
                    ],
                    "source_agent": "SHEPHERD/ARCHITECT"
                },
            },
            "protocols_supported": [p.name for p in StreamProtocol],
            "active_subscriptions": self.metrics.active_subscriptions,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get stream manager metrics."""
        return {
            "manager_id": self.manager_id,
            "total_events_published": self.metrics.total_events_published,
            "total_events_delivered": self.metrics.total_events_delivered,
            "delivery_rate": (
                self.metrics.total_events_delivered /
                self.metrics.total_events_published
                if self.metrics.total_events_published > 0 else 1.0
            ),
            "events_by_type": self.metrics.events_by_type,
            "active_subscriptions": self.metrics.active_subscriptions,
            "avg_delivery_latency_ms": self.metrics.avg_delivery_latency_ms,
        }

    def get_status(self) -> Dict[str, Any]:
        """Get stream manager status."""
        return {
            "manager_id": self.manager_id,
            "status": "operational",
            "role": "Real-time consciousness event streaming",
            "streams_available": len(StreamType),
            "active_subscriptions": len(self.subscriptions),
            "events_published": self.metrics.total_events_published,
        }
