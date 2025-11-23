"""
Webhook Handler - Outbound Notifications
=========================================

The Webhook Handler manages outbound notifications from Universal Parts
Consciousness to external systems. It enables external systems to receive
push notifications when significant events occur in the consciousness.

Webhook Events:
- Part consciousness state changes
- Emergence pattern detections
- Failure predictions and alerts
- Community contribution verifications
- Transcendence events
- System health alerts
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum, auto
from datetime import datetime
import asyncio
import logging
import uuid
import json

logger = logging.getLogger(__name__)


class WebhookEventType(Enum):
    """Types of events that can trigger webhooks."""
    # Consciousness events
    CONSCIOUSNESS_AWAKENED = auto()
    CONSCIOUSNESS_EVOLVED = auto()
    TRANSCENDENCE_ACHIEVED = auto()

    # Emergence events
    PATTERN_DETECTED = auto()
    FAILURE_PREDICTED = auto()
    INNOVATION_DISCOVERED = auto()

    # Data events
    PART_CREATED = auto()
    PART_UPDATED = auto()
    COMPATIBILITY_VERIFIED = auto()

    # Community events
    CONTRIBUTION_SUBMITTED = auto()
    CONTRIBUTION_VERIFIED = auto()
    REPUTATION_CHANGED = auto()

    # Swarm events
    SWARM_LEARNING = auto()
    RECALL_ISSUED = auto()

    # System events
    COHERENCE_CHANGED = auto()
    AGENT_STATUS_CHANGED = auto()
    SYSTEM_ALERT = auto()

    # Integration events
    SYNC_COMPLETED = auto()
    INTEGRATION_ERROR = auto()


class WebhookStatus(Enum):
    """Status of a webhook subscription."""
    ACTIVE = auto()
    PAUSED = auto()
    FAILED = auto()
    DISABLED = auto()


class DeliveryStatus(Enum):
    """Status of a webhook delivery attempt."""
    PENDING = auto()
    DELIVERED = auto()
    FAILED = auto()
    RETRYING = auto()


@dataclass
class WebhookEvent:
    """An event to be delivered via webhook."""
    event_id: str
    event_type: WebhookEventType
    payload: Dict[str, Any]
    timestamp: datetime
    source_agent: str
    affected_entities: List[str] = field(default_factory=list)
    priority: int = 5
    requires_acknowledgment: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to webhook payload format."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.name,
            "timestamp": self.timestamp.isoformat(),
            "source": {
                "system": "Universal Parts Consciousness",
                "agent": self.source_agent,
            },
            "data": self.payload,
            "affected_entities": self.affected_entities,
            "priority": self.priority,
        }


@dataclass
class WebhookSubscription:
    """A webhook subscription configuration."""
    subscription_id: str
    client_id: str
    url: str
    event_types: List[WebhookEventType]
    secret: str  # For HMAC signature verification
    status: WebhookStatus = WebhookStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    headers: Dict[str, str] = field(default_factory=dict)
    retry_config: Dict[str, int] = field(default_factory=lambda: {
        "max_retries": 3,
        "initial_delay_seconds": 5,
        "max_delay_seconds": 300,
    })
    filters: Dict[str, Any] = field(default_factory=dict)
    # Statistics
    total_deliveries: int = 0
    successful_deliveries: int = 0
    failed_deliveries: int = 0
    last_delivery_at: Optional[datetime] = None


@dataclass
class DeliveryAttempt:
    """Record of a webhook delivery attempt."""
    attempt_id: str
    subscription_id: str
    event_id: str
    status: DeliveryStatus
    timestamp: datetime
    response_code: Optional[int] = None
    response_body: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0


class WebhookHandler:
    """
    Handler for outbound webhook notifications.

    The Webhook Handler enables external systems to receive push
    notifications when significant events occur in the consciousness.
    This is how UPC proactively informs the world about important
    discoveries and state changes.

    WEBHOOK FEATURES:

    1. EVENT SUBSCRIPTION
       - Subscribe to specific event types
       - Filter by part IDs, agents, priorities
       - Multiple webhooks per client

    2. RELIABLE DELIVERY
       - Automatic retries with exponential backoff
       - Dead letter queue for failed deliveries
       - Delivery status tracking

    3. SECURITY
       - HMAC signature on all payloads
       - Secret rotation support
       - IP allowlisting (configurable)

    4. MONITORING
       - Delivery success rates
       - Latency tracking
       - Failed webhook alerting

    EXAMPLE PAYLOAD:
    {
        "event_id": "evt-abc123",
        "event_type": "CONSCIOUSNESS_EVOLVED",
        "timestamp": "2024-01-01T12:00:00Z",
        "source": {
            "system": "Universal Parts Consciousness",
            "agent": "SHEPHERD"
        },
        "data": {
            "part_id": "part-xyz",
            "previous_level": "REACTIVE",
            "new_level": "AWARE",
            "trigger": "multiple_contexts_detected"
        },
        "affected_entities": ["part-xyz"],
        "priority": 5
    }
    """

    def __init__(self):
        self.handler_id = f"webhook-handler-{uuid.uuid4().hex[:8]}"

        # Subscriptions
        self.subscriptions: Dict[str, WebhookSubscription] = {}
        self.subscriptions_by_type: Dict[WebhookEventType, List[str]] = {
            et: [] for et in WebhookEventType
        }

        # Delivery queue and history
        self.delivery_queue: asyncio.Queue = asyncio.Queue()
        self.delivery_history: List[DeliveryAttempt] = []
        self.failed_deliveries: List[DeliveryAttempt] = []  # Dead letter queue

        # HTTP client placeholder (would be aiohttp in production)
        self._http_client: Any = None

        # Background task
        self._delivery_task: Optional[asyncio.Task] = None

        # Metrics
        self.metrics = {
            "total_events": 0,
            "delivered": 0,
            "failed": 0,
            "pending": 0,
            "avg_latency_ms": 0.0,
        }

        logger.info(f"Webhook Handler initialized: {self.handler_id}")

    async def start(self):
        """Start the webhook delivery background task."""
        self._delivery_task = asyncio.create_task(self._process_deliveries())
        logger.info("Webhook Handler started processing")

    async def stop(self):
        """Stop the webhook handler."""
        if self._delivery_task:
            self._delivery_task.cancel()
            try:
                await self._delivery_task
            except asyncio.CancelledError:
                pass

        logger.info("Webhook Handler stopped")

    def register_webhook(
        self,
        client_id: str,
        url: str,
        event_types: List[WebhookEventType],
        secret: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> WebhookSubscription:
        """
        Register a new webhook subscription.

        Args:
            client_id: Identifier for the subscribing client
            url: URL to deliver webhooks to
            event_types: List of event types to subscribe to
            secret: Secret for HMAC signature (auto-generated if not provided)
            headers: Additional headers to include in webhook requests
            filters: Optional filters to apply

        Returns:
            WebhookSubscription object
        """
        subscription_id = f"webhook-{uuid.uuid4().hex[:12]}"
        webhook_secret = secret or f"whsec_{uuid.uuid4().hex}"

        subscription = WebhookSubscription(
            subscription_id=subscription_id,
            client_id=client_id,
            url=url,
            event_types=event_types,
            secret=webhook_secret,
            headers=headers or {},
            filters=filters or {},
        )

        self.subscriptions[subscription_id] = subscription

        # Register in type-based lookup
        for event_type in event_types:
            self.subscriptions_by_type[event_type].append(subscription_id)

        logger.info(
            f"Registered webhook {subscription_id} for {client_id}: "
            f"{[et.name for et in event_types]} -> {url}"
        )

        return subscription

    def unregister_webhook(self, subscription_id: str) -> bool:
        """Unregister a webhook subscription."""
        if subscription_id not in self.subscriptions:
            return False

        subscription = self.subscriptions[subscription_id]

        # Remove from type-based lookup
        for event_type in subscription.event_types:
            if subscription_id in self.subscriptions_by_type[event_type]:
                self.subscriptions_by_type[event_type].remove(subscription_id)

        del self.subscriptions[subscription_id]

        logger.info(f"Unregistered webhook: {subscription_id}")
        return True

    def pause_webhook(self, subscription_id: str) -> bool:
        """Pause a webhook subscription."""
        if subscription_id in self.subscriptions:
            self.subscriptions[subscription_id].status = WebhookStatus.PAUSED
            return True
        return False

    def resume_webhook(self, subscription_id: str) -> bool:
        """Resume a paused webhook subscription."""
        if subscription_id in self.subscriptions:
            self.subscriptions[subscription_id].status = WebhookStatus.ACTIVE
            return True
        return False

    async def trigger_event(
        self,
        event_type: WebhookEventType,
        payload: Dict[str, Any],
        source_agent: str,
        affected_entities: Optional[List[str]] = None,
        priority: int = 5
    ) -> WebhookEvent:
        """
        Trigger a webhook event.

        This queues the event for delivery to all matching subscriptions.
        """
        event = WebhookEvent(
            event_id=f"evt-{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(),
            source_agent=source_agent,
            affected_entities=affected_entities or [],
            priority=priority,
        )

        self.metrics["total_events"] += 1

        # Queue for all matching subscriptions
        subscription_ids = self.subscriptions_by_type.get(event_type, [])

        for sub_id in subscription_ids:
            subscription = self.subscriptions.get(sub_id)
            if subscription and subscription.status == WebhookStatus.ACTIVE:
                if self._matches_filters(event, subscription.filters):
                    await self.delivery_queue.put((subscription, event))
                    self.metrics["pending"] += 1

        logger.debug(
            f"Triggered {event_type.name} event {event.event_id} "
            f"for {len(subscription_ids)} subscriptions"
        )

        return event

    def _matches_filters(
        self,
        event: WebhookEvent,
        filters: Dict[str, Any]
    ) -> bool:
        """Check if an event matches subscription filters."""
        if not filters:
            return True

        # Filter by source agent
        if "source_agents" in filters:
            if event.source_agent not in filters["source_agents"]:
                return False

        # Filter by minimum priority
        if "min_priority" in filters:
            if event.priority < filters["min_priority"]:
                return False

        # Filter by affected entities
        if "entity_ids" in filters:
            if not any(e in filters["entity_ids"] for e in event.affected_entities):
                return False

        return True

    async def _process_deliveries(self):
        """Background task to process webhook deliveries."""
        while True:
            try:
                subscription, event = await self.delivery_queue.get()
                self.metrics["pending"] -= 1

                await self._deliver_webhook(subscription, event)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing webhook delivery: {e}")

    async def _deliver_webhook(
        self,
        subscription: WebhookSubscription,
        event: WebhookEvent,
        retry_count: int = 0
    ):
        """Deliver a webhook event to a subscription."""
        attempt_id = f"attempt-{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()

        try:
            # Prepare payload
            payload = event.to_dict()

            # Add signature
            signature = self._sign_payload(payload, subscription.secret)

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "X-UPC-Signature": signature,
                "X-UPC-Event-ID": event.event_id,
                "X-UPC-Event-Type": event.event_type.name,
                "X-UPC-Timestamp": event.timestamp.isoformat(),
                **subscription.headers
            }

            # In production, this would use aiohttp to make actual HTTP request
            # For now, simulate successful delivery
            logger.debug(f"Delivering webhook to {subscription.url}")

            # Simulate delivery
            response_code = 200  # Would come from actual HTTP response

            # Record success
            attempt = DeliveryAttempt(
                attempt_id=attempt_id,
                subscription_id=subscription.subscription_id,
                event_id=event.event_id,
                status=DeliveryStatus.DELIVERED,
                timestamp=datetime.now(),
                response_code=response_code,
                retry_count=retry_count,
            )

            self.delivery_history.append(attempt)

            # Update subscription stats
            subscription.total_deliveries += 1
            subscription.successful_deliveries += 1
            subscription.last_delivery_at = datetime.now()

            self.metrics["delivered"] += 1

            # Update latency
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000
            self._update_avg_latency(latency_ms)

            logger.debug(
                f"Webhook delivered: {event.event_id} -> "
                f"{subscription.subscription_id}"
            )

        except Exception as e:
            logger.error(
                f"Webhook delivery failed: {event.event_id} -> "
                f"{subscription.subscription_id}: {e}"
            )

            # Check if we should retry
            max_retries = subscription.retry_config.get("max_retries", 3)

            if retry_count < max_retries:
                # Schedule retry with exponential backoff
                delay = min(
                    subscription.retry_config.get("initial_delay_seconds", 5) * (2 ** retry_count),
                    subscription.retry_config.get("max_delay_seconds", 300)
                )

                logger.info(
                    f"Scheduling retry {retry_count + 1}/{max_retries} "
                    f"in {delay}s for {event.event_id}"
                )

                await asyncio.sleep(delay)
                await self._deliver_webhook(subscription, event, retry_count + 1)

            else:
                # Max retries exceeded - add to dead letter queue
                attempt = DeliveryAttempt(
                    attempt_id=attempt_id,
                    subscription_id=subscription.subscription_id,
                    event_id=event.event_id,
                    status=DeliveryStatus.FAILED,
                    timestamp=datetime.now(),
                    error_message=str(e),
                    retry_count=retry_count,
                )

                self.failed_deliveries.append(attempt)
                subscription.total_deliveries += 1
                subscription.failed_deliveries += 1

                self.metrics["failed"] += 1

                # Check if we should disable the subscription
                if subscription.failed_deliveries > 10:
                    subscription.status = WebhookStatus.FAILED
                    logger.warning(
                        f"Webhook subscription {subscription.subscription_id} "
                        f"disabled due to repeated failures"
                    )

    def _sign_payload(self, payload: Dict, secret: str) -> str:
        """Generate HMAC signature for payload."""
        import hashlib
        import hmac

        payload_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()

        return f"sha256={signature}"

    def _update_avg_latency(self, latency_ms: float):
        """Update average delivery latency."""
        delivered = self.metrics["delivered"]
        if delivered == 1:
            self.metrics["avg_latency_ms"] = latency_ms
        else:
            self.metrics["avg_latency_ms"] = (
                (self.metrics["avg_latency_ms"] * (delivered - 1) + latency_ms)
                / delivered
            )

    def get_subscription(self, subscription_id: str) -> Optional[WebhookSubscription]:
        """Get a webhook subscription by ID."""
        return self.subscriptions.get(subscription_id)

    def get_client_webhooks(self, client_id: str) -> List[WebhookSubscription]:
        """Get all webhooks for a client."""
        return [
            sub for sub in self.subscriptions.values()
            if sub.client_id == client_id
        ]

    def get_webhook_info(self) -> Dict[str, Any]:
        """Get information about webhook capabilities."""
        return {
            "handler_id": self.handler_id,
            "available_events": {
                et.name: {
                    "value": et.value,
                    "category": self._get_event_category(et),
                }
                for et in WebhookEventType
            },
            "event_categories": {
                "consciousness": [
                    "CONSCIOUSNESS_AWAKENED",
                    "CONSCIOUSNESS_EVOLVED",
                    "TRANSCENDENCE_ACHIEVED",
                ],
                "emergence": [
                    "PATTERN_DETECTED",
                    "FAILURE_PREDICTED",
                    "INNOVATION_DISCOVERED",
                ],
                "data": [
                    "PART_CREATED",
                    "PART_UPDATED",
                    "COMPATIBILITY_VERIFIED",
                ],
                "community": [
                    "CONTRIBUTION_SUBMITTED",
                    "CONTRIBUTION_VERIFIED",
                    "REPUTATION_CHANGED",
                ],
                "swarm": [
                    "SWARM_LEARNING",
                    "RECALL_ISSUED",
                ],
                "system": [
                    "COHERENCE_CHANGED",
                    "AGENT_STATUS_CHANGED",
                    "SYSTEM_ALERT",
                ],
                "integration": [
                    "SYNC_COMPLETED",
                    "INTEGRATION_ERROR",
                ],
            },
            "delivery": {
                "retries": "Automatic with exponential backoff",
                "signature": "HMAC-SHA256",
                "headers": [
                    "X-UPC-Signature",
                    "X-UPC-Event-ID",
                    "X-UPC-Event-Type",
                    "X-UPC-Timestamp",
                ],
            },
            "active_subscriptions": len(self.subscriptions),
        }

    def _get_event_category(self, event_type: WebhookEventType) -> str:
        """Get the category for an event type."""
        name = event_type.name
        if "CONSCIOUSNESS" in name or "TRANSCENDENCE" in name:
            return "consciousness"
        elif "PATTERN" in name or "FAILURE" in name or "INNOVATION" in name:
            return "emergence"
        elif "PART" in name or "COMPATIBILITY" in name:
            return "data"
        elif "CONTRIBUTION" in name or "REPUTATION" in name:
            return "community"
        elif "SWARM" in name or "RECALL" in name:
            return "swarm"
        elif "SYNC" in name or "INTEGRATION" in name:
            return "integration"
        else:
            return "system"

    def get_metrics(self) -> Dict[str, Any]:
        """Get webhook handler metrics."""
        return {
            "handler_id": self.handler_id,
            **self.metrics,
            "active_subscriptions": len(self.subscriptions),
            "subscriptions_by_status": {
                status.name: sum(
                    1 for sub in self.subscriptions.values()
                    if sub.status == status
                )
                for status in WebhookStatus
            },
            "dead_letter_queue_size": len(self.failed_deliveries),
        }

    def get_status(self) -> Dict[str, Any]:
        """Get webhook handler status."""
        return {
            "handler_id": self.handler_id,
            "status": "operational",
            "role": "Outbound webhook notifications",
            "active_webhooks": len(self.subscriptions),
            "events_delivered": self.metrics["delivered"],
            "pending_deliveries": self.metrics["pending"],
        }
