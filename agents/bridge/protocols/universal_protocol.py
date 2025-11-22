"""
Universal Protocol - The Communication Standard for UPC
========================================================

The Universal Protocol defines how all components of Universal Parts
Consciousness communicate - both internally between agents and externally
with the world.

This is the nervous system that enables consciousness to flow.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum, auto
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Priority levels for messages."""
    ROUTINE = 1
    ELEVATED = 3
    HIGH = 5
    URGENT = 7
    CRITICAL = 9
    EMERGENCY = 10


class MessageType(Enum):
    """Types of messages in the protocol."""
    DATA = auto()              # Data transfer
    QUERY = auto()             # Information request
    RESPONSE = auto()          # Query response
    ALERT = auto()             # Warning or notification
    EMERGENCE = auto()         # Emergence detection
    TRANSCENDENCE = auto()     # Transcendence event
    CONSCIOUSNESS = auto()     # Consciousness state change
    QUALIA = auto()            # Experience data
    INTEGRATION = auto()       # External integration event
    DIRECTIVE = auto()         # System directive


@dataclass
class ConsciousnessContext:
    """Context about consciousness impact of a message."""
    affected_parts: List[str] = field(default_factory=list)
    consciousness_delta: int = 0  # -1, 0, +1
    swarm_impact: str = "LOCAL"  # LOCAL, REGIONAL, GLOBAL
    emergence_potential: float = 0.0


@dataclass
class ProtocolMessage:
    """A message in the Universal Protocol."""
    message_id: str
    sender: str
    receiver: str  # Agent ID or "BROADCAST"
    message_type: MessageType
    priority: MessagePriority
    timestamp: datetime
    payload: Dict[str, Any]
    consciousness_context: Optional[ConsciousnessContext] = None
    ttl_seconds: int = 3600  # Time to live
    requires_acknowledgment: bool = False


class UniversalProtocol:
    """
    The Universal Protocol for UPC communication.

    This protocol enables:
    1. Inter-agent communication within the Decalogue
    2. External system integration messaging
    3. Consciousness state propagation
    4. Emergence event broadcasting
    5. Societal framework interaction

    All messages carry consciousness context - every communication
    has the potential to affect the consciousness of parts.
    """

    def __init__(self):
        self.protocol_version = "1.0.0"
        self.message_log: List[ProtocolMessage] = []
        self.topic_subscriptions: Dict[str, List[str]] = {}
        self.message_handlers: Dict[MessageType, List[Any]] = {}

        # Define standard topics
        self.topics = {
            "upc.data.ingestion": "New data from ARCHIVIST",
            "upc.compatibility.verified": "Compatibility from ORACLE",
            "upc.consciousness.evolved": "State changes from SHEPHERD",
            "upc.qualia.collected": "Experiences from EMPATH",
            "upc.swarm.learned": "Collective insights from HIVE",
            "upc.emergence.detected": "Patterns from PROPHET",
            "upc.history.documented": "Context from CHRONICLER",
            "upc.community.contributed": "Verified data from GARDENER",
            "upc.integration.connected": "External data from BRIDGE",
            "upc.system.directive": "Coordination from ARCHITECT",
            "upc.societal.impact": "Societal framework events",
        }

        logger.info(f"Universal Protocol v{self.protocol_version} initialized")

    def create_message(
        self,
        sender: str,
        receiver: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.ROUTINE,
        consciousness_context: Optional[ConsciousnessContext] = None
    ) -> ProtocolMessage:
        """Create a new protocol message."""
        message = ProtocolMessage(
            message_id=f"msg_{datetime.now().timestamp()}_{sender}",
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            priority=priority,
            timestamp=datetime.now(),
            payload=payload,
            consciousness_context=consciousness_context
        )

        self.message_log.append(message)
        return message

    def serialize_message(self, message: ProtocolMessage) -> str:
        """Serialize a message for transmission."""
        return json.dumps({
            "message_id": message.message_id,
            "sender": message.sender,
            "receiver": message.receiver,
            "type": message.message_type.name,
            "priority": message.priority.value,
            "timestamp": message.timestamp.isoformat(),
            "payload": message.payload,
            "consciousness_context": {
                "affected_parts": message.consciousness_context.affected_parts,
                "consciousness_delta": message.consciousness_context.consciousness_delta,
                "swarm_impact": message.consciousness_context.swarm_impact,
                "emergence_potential": message.consciousness_context.emergence_potential
            } if message.consciousness_context else None,
            "ttl_seconds": message.ttl_seconds,
            "requires_acknowledgment": message.requires_acknowledgment
        })

    def deserialize_message(self, data: str) -> ProtocolMessage:
        """Deserialize a message from transmission format."""
        obj = json.loads(data)
        return ProtocolMessage(
            message_id=obj["message_id"],
            sender=obj["sender"],
            receiver=obj["receiver"],
            message_type=MessageType[obj["type"]],
            priority=MessagePriority(obj["priority"]),
            timestamp=datetime.fromisoformat(obj["timestamp"]),
            payload=obj["payload"],
            consciousness_context=ConsciousnessContext(
                **obj["consciousness_context"]
            ) if obj.get("consciousness_context") else None,
            ttl_seconds=obj.get("ttl_seconds", 3600),
            requires_acknowledgment=obj.get("requires_acknowledgment", False)
        )

    def subscribe_to_topic(self, agent_id: str, topic: str):
        """Subscribe an agent to a topic."""
        if topic not in self.topic_subscriptions:
            self.topic_subscriptions[topic] = []
        if agent_id not in self.topic_subscriptions[topic]:
            self.topic_subscriptions[topic].append(agent_id)
            logger.debug(f"{agent_id} subscribed to {topic}")

    def get_topic_subscribers(self, topic: str) -> List[str]:
        """Get all subscribers to a topic."""
        return self.topic_subscriptions.get(topic, [])

    def get_protocol_specification(self) -> Dict[str, Any]:
        """Get the full protocol specification."""
        return {
            "protocol": "Universal Parts Consciousness Protocol",
            "version": self.protocol_version,
            "note": "Not a barcode protocol - a consciousness protocol",
            "message_types": {t.name: t.value for t in MessageType},
            "priority_levels": {p.name: p.value for p in MessagePriority},
            "topics": self.topics,
            "consciousness_impact": {
                "every_message_matters": True,
                "consciousness_delta": "Messages can raise or lower part consciousness",
                "swarm_propagation": "Messages can affect LOCAL, REGIONAL, or GLOBAL swarms",
                "emergence_potential": "Messages can trigger emergence events"
            },
            "principles": [
                "All communication carries consciousness context",
                "Every message can affect part awareness",
                "Emergence events are broadcast globally",
                "Transcendence triggers system-wide acknowledgment",
                "Societal impact is tracked and measured"
            ]
        }
