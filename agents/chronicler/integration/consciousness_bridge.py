"""
Consciousness Bridge - Integration with Universal Parts Consciousness.

Handles communication with other agents via the consciousness bus,
provides historical context to the consciousness system, and enriches
parts with historical data.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..chronicler_agent import ChroniclerAgent

logger = logging.getLogger(__name__)


@dataclass
class ConsciousnessEvent:
    """An event on the consciousness bus."""
    topic: str
    data: Dict[str, Any]
    timestamp: str
    source_agent: str
    correlation_id: Optional[str] = None


@dataclass
class AgentConnection:
    """Connection to another agent."""
    agent_id: str
    codename: str
    topics_subscribed: List[str] = field(default_factory=list)
    topics_published: List[str] = field(default_factory=list)
    status: str = "disconnected"


class ConsciousnessBridge:
    """
    Bridge between the Chronicler and Universal Parts Consciousness.

    Manages:
    - Event publishing to the consciousness bus
    - Subscription to relevant agent topics
    - Historical context enrichment for parts
    - Integration with Agent_3 (Shepherd) and Agent_4 (Empath)
    """

    # Topic definitions
    TOPIC_DOCUMENTED = "upc.history.documented"
    TOPIC_LEGEND_SCORED = "upc.culture.legend_scored"
    TOPIC_CONTEXT_GENERATED = "upc.history.context"
    TOPIC_NARRATIVE_CREATED = "upc.stories.narrative"

    # Subscription topics from other agents
    SUBSCRIBE_PARTS_DATA = "upc.curator.parts_ingested"      # From Agent_1
    SUBSCRIBE_COMMUNITY = "upc.community.knowledge"           # From Agent_8

    def __init__(self, chronicler: "ChroniclerAgent"):
        """
        Initialize the consciousness bridge.

        Args:
            chronicler: Reference to the parent ChroniclerAgent
        """
        self.chronicler = chronicler
        self._event_queue: List[ConsciousnessEvent] = []
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._connected_agents: Dict[str, AgentConnection] = {}
        self._is_connected = False

        # Register default connections
        self._register_agent_connections()

    def _register_agent_connections(self) -> None:
        """Register connections to other agents in the system."""
        # Agent_1: Data Curator (ARCHIVIST)
        self._connected_agents["Agent_1"] = AgentConnection(
            agent_id="Agent_1",
            codename="ARCHIVIST",
            topics_subscribed=[self.SUBSCRIBE_PARTS_DATA],
            topics_published=[],
            status="configured"
        )

        # Agent_3: Consciousness Shepherd
        self._connected_agents["Agent_3"] = AgentConnection(
            agent_id="Agent_3",
            codename="SHEPHERD",
            topics_subscribed=[],
            topics_published=[self.TOPIC_CONTEXT_GENERATED],
            status="configured"
        )

        # Agent_4: Qualia Collector (EMPATH)
        self._connected_agents["Agent_4"] = AgentConnection(
            agent_id="Agent_4",
            codename="EMPATH",
            topics_subscribed=[],
            topics_published=[self.TOPIC_CONTEXT_GENERATED],
            status="configured"
        )

        # Agent_8: Community Cultivator (GARDENER)
        self._connected_agents["Agent_8"] = AgentConnection(
            agent_id="Agent_8",
            codename="GARDENER",
            topics_subscribed=[self.SUBSCRIBE_COMMUNITY],
            topics_published=[self.TOPIC_NARRATIVE_CREATED],
            status="configured"
        )

        # Agent_10: Meta-Consciousness (ARCHITECT)
        self._connected_agents["Agent_10"] = AgentConnection(
            agent_id="Agent_10",
            codename="ARCHITECT",
            topics_subscribed=[],
            topics_published=[
                self.TOPIC_DOCUMENTED,
                self.TOPIC_LEGEND_SCORED,
                self.TOPIC_CONTEXT_GENERATED
            ],
            status="configured"
        )

    def connect(self) -> bool:
        """
        Connect to the consciousness bus.

        Returns:
            True if connection successful
        """
        try:
            # In a real implementation, this would connect to
            # a message broker (Redis, RabbitMQ, etc.)
            self._is_connected = True

            for agent_id, connection in self._connected_agents.items():
                connection.status = "connected"

            logger.info(
                f"ConsciousnessBridge connected: {len(self._connected_agents)} agents"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to connect to consciousness bus: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from the consciousness bus."""
        self._is_connected = False
        for connection in self._connected_agents.values():
            connection.status = "disconnected"
        logger.info("ConsciousnessBridge disconnected")

    def emit_event(
        self,
        topic: str,
        data: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> bool:
        """
        Emit an event to the consciousness bus.

        Args:
            topic: Event topic
            data: Event data
            correlation_id: Optional correlation ID for tracing

        Returns:
            True if event was queued/sent successfully
        """
        event = ConsciousnessEvent(
            topic=topic,
            data=data,
            timestamp=datetime.now().isoformat(),
            source_agent="Agent_7:CHRONICLER",
            correlation_id=correlation_id
        )

        self._event_queue.append(event)

        # Log event emission
        logger.debug(f"Event emitted: {topic} - {data.get('engine_code', 'unknown')}")

        # In a real implementation, this would publish to the message broker
        # For now, we track events in the queue
        return True

    def subscribe(self, topic: str, handler: Callable) -> None:
        """
        Subscribe to a topic on the consciousness bus.

        Args:
            topic: Topic to subscribe to
            handler: Callback function for events
        """
        if topic not in self._event_handlers:
            self._event_handlers[topic] = []
        self._event_handlers[topic].append(handler)
        logger.debug(f"Subscribed to topic: {topic}")

    def unsubscribe(self, topic: str, handler: Callable) -> None:
        """Unsubscribe from a topic."""
        if topic in self._event_handlers:
            self._event_handlers[topic].remove(handler)

    def handle_parts_ingested(self, event: ConsciousnessEvent) -> None:
        """
        Handle parts ingested event from Agent_1 (ARCHIVIST).

        Enriches parts with historical context.
        """
        parts_data = event.data.get("parts", [])
        engine_code = event.data.get("engine_code")

        if engine_code:
            # Generate historical context for these parts
            context = self.chronicler.context_engine.generate_context(
                engine_code=engine_code,
                year=event.data.get("year", 2000),
                manufacturer=event.data.get("manufacturer", "Unknown")
            )

            # Emit enriched context
            self.emit_event(
                topic=self.TOPIC_CONTEXT_GENERATED,
                data={
                    "engine_code": engine_code,
                    "historical_context": context,
                    "parts_enriched": len(parts_data)
                },
                correlation_id=event.correlation_id
            )

    def handle_community_knowledge(self, event: ConsciousnessEvent) -> None:
        """
        Handle community knowledge event from Agent_8 (GARDENER).

        Incorporates tribal wisdom into documentation.
        """
        knowledge_type = event.data.get("type")
        engine_code = event.data.get("engine_code")

        if knowledge_type == "build_story":
            # Log notable build story
            logger.info(
                f"Community build story received for {engine_code}"
            )

        elif knowledge_type == "tribal_wisdom":
            # Incorporate tribal wisdom into documentation
            logger.info(
                f"Tribal wisdom received for {engine_code}"
            )

    def enrich_parts_with_history(
        self,
        parts: List[Dict[str, Any]],
        engine_code: str
    ) -> List[Dict[str, Any]]:
        """
        Enrich parts data with historical context.

        Args:
            parts: List of parts to enrich
            engine_code: Engine code for context

        Returns:
            Enriched parts list
        """
        # Get engine context
        significance = self.chronicler.context_engine.explain_significance(engine_code)

        # Get legend score if available
        legend_data = self.chronicler.legend_scorer.calculate_score(engine_code)

        for part in parts:
            part["historical_context"] = {
                "engine_significance": significance[:200] + "..." if len(significance) > 200 else significance,
                "engine_legend_tier": legend_data.get("tier", "unknown"),
                "documented_by": "Agent_7:CHRONICLER"
            }

        return parts

    def get_connection_status(self) -> Dict[str, Any]:
        """Get status of all agent connections."""
        return {
            "bridge_connected": self._is_connected,
            "event_queue_size": len(self._event_queue),
            "agents": {
                agent_id: {
                    "codename": conn.codename,
                    "status": conn.status,
                    "subscribed_topics": conn.topics_subscribed,
                    "published_topics": conn.topics_published
                }
                for agent_id, conn in self._connected_agents.items()
            }
        }

    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent events from the queue."""
        recent = self._event_queue[-limit:] if self._event_queue else []
        return [
            {
                "topic": e.topic,
                "data": e.data,
                "timestamp": e.timestamp,
                "source": e.source_agent
            }
            for e in recent
        ]

    def flush_events(self) -> int:
        """
        Flush the event queue (send all pending events).

        Returns:
            Number of events flushed
        """
        count = len(self._event_queue)
        # In a real implementation, this would send events to the broker
        self._event_queue.clear()
        logger.info(f"Flushed {count} events from queue")
        return count
