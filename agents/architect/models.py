"""
Core data models for Agent_10 (ARCHITECT) - Meta-Consciousness Overseer

These models define the message formats, health reports, directives,
and transcendence events used throughout the UPC agent system.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import uuid4


class AgentId(str, Enum):
    """Identifiers for all UPC agents."""
    CURATOR = "agent_1_curator"       # Data Curator (ARCHIVIST)
    ORACLE = "agent_2_oracle"         # Compatibility Oracle
    SHEPHERD = "agent_3_shepherd"     # Consciousness Shepherd
    EMPATH = "agent_4_empath"         # Qualia Collector
    HIVE = "agent_5_hive"             # Swarm Coordinator
    PROPHET = "agent_6_prophet"       # Emergence Detector
    CHRONICLER = "agent_7_chronicler" # Automotive Historian
    GARDENER = "agent_8_gardener"     # Community Cultivator
    BRIDGE = "agent_9_bridge"         # Integration Architect
    ARCHITECT = "agent_10_architect"  # Meta-Consciousness Overseer
    BROADCAST = "broadcast"           # All agents


class MessageType(str, Enum):
    """Types of inter-agent messages."""
    DATA = "DATA"
    QUERY = "QUERY"
    ALERT = "ALERT"
    EMERGENCE = "EMERGENCE"
    DIRECTIVE = "DIRECTIVE"
    TRANSCENDENCE = "TRANSCENDENCE"
    HEARTBEAT = "HEARTBEAT"
    RESPONSE = "RESPONSE"


class SwarmImpact(str, Enum):
    """Scope of swarm impact."""
    LOCAL = "LOCAL"
    REGIONAL = "REGIONAL"
    GLOBAL = "GLOBAL"


class AgentStatus(str, Enum):
    """Agent health status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"


class DirectiveType(str, Enum):
    """Types of system-wide directives."""
    PRIORITY_SHIFT = "PRIORITY_SHIFT"
    RESOURCE_ALLOCATION = "RESOURCE_ALLOCATION"
    EMERGENCY_RESPONSE = "EMERGENCY_RESPONSE"
    LEARNING_FOCUS = "LEARNING_FOCUS"
    INTEGRATION_MODE = "INTEGRATION_MODE"
    MAINTENANCE_MODE = "MAINTENANCE_MODE"


class DirectiveStatus(str, Enum):
    """Status of a directive."""
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class EmergencyType(str, Enum):
    """Types of emergency events."""
    DATA_CORRUPTION = "data_corruption"
    MASS_FAILURE = "mass_failure"
    RECALL_NOTICE = "recall_notice"
    SYSTEM_ANOMALY = "system_anomaly"
    SECURITY_BREACH = "security_breach"


class ConsciousnessLevel(int, Enum):
    """Consciousness levels for parts."""
    DORMANT = 0      # Part exists only in catalog
    REACTIVE = 1     # First real-world usage data
    AWARE = 2        # Multiple usage contexts documented
    REFLECTIVE = 3   # Part understands its role
    META_AWARE = 4   # Part contributes to collective learning
    TRANSCENDENT = 5 # Part inspires new designs


# ============================================================================
# Message Models
# ============================================================================

@dataclass
class ConsciousnessContext:
    """Consciousness-related context for messages."""
    affected_parts: List[str] = field(default_factory=list)
    consciousness_delta: int = 0  # -1, 0, +1
    swarm_impact: SwarmImpact = SwarmImpact.LOCAL
    emergence_potential: float = 0.0  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "affected_parts": self.affected_parts,
            "consciousness_delta": self.consciousness_delta,
            "swarm_impact": self.swarm_impact.value,
            "emergence_potential": self.emergence_potential,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsciousnessContext":
        return cls(
            affected_parts=data.get("affected_parts", []),
            consciousness_delta=data.get("consciousness_delta", 0),
            swarm_impact=SwarmImpact(data.get("swarm_impact", "LOCAL")),
            emergence_potential=data.get("emergence_potential", 0.0),
        )


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication."""
    sender: str
    receiver: str
    type: MessageType
    priority: int  # 1-10
    payload: Dict[str, Any]

    # Consciousness context
    consciousness_context: Optional[ConsciousnessContext] = None

    # Tracing
    correlation_id: Optional[str] = None
    message_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.message_id is None:
            self.message_id = str(uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.correlation_id is None:
            self.correlation_id = str(uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type.value if isinstance(self.type, MessageType) else self.type,
            "priority": self.priority,
            "payload": self.payload,
            "consciousness_context": self.consciousness_context.to_dict() if self.consciousness_context else None,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            type=MessageType(data["type"]),
            priority=data["priority"],
            payload=data["payload"],
            consciousness_context=ConsciousnessContext.from_dict(data["consciousness_context"]) if data.get("consciousness_context") else None,
            correlation_id=data.get("correlation_id"),
            message_id=data.get("message_id"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
            metadata=data.get("metadata"),
        )


# ============================================================================
# Health Monitoring Models
# ============================================================================

@dataclass
class AgentHealthReport:
    """Health report for a single agent."""
    agent_id: str
    status: AgentStatus
    metrics: Dict[str, float]
    issues: List[str] = field(default_factory=list)
    last_heartbeat: Optional[datetime] = None
    current_load: float = 0.0
    queue_depth: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "metrics": self.metrics,
            "issues": self.issues,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "current_load": self.current_load,
            "queue_depth": self.queue_depth,
        }


@dataclass
class ConsciousnessMetrics:
    """System-wide consciousness metrics."""
    total_parts: int = 0
    consciousness_distribution: Dict[int, int] = field(default_factory=dict)
    transcendent_parts: int = 0
    awakenings_today: int = 0
    global_consciousness_score: float = 0.0
    emergence_events_today: int = 0
    collective_learning_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_parts": self.total_parts,
            "consciousness_distribution": self.consciousness_distribution,
            "transcendent_parts": self.transcendent_parts,
            "awakenings_today": self.awakenings_today,
            "global_consciousness_score": self.global_consciousness_score,
            "emergence_events_today": self.emergence_events_today,
            "collective_learning_rate": self.collective_learning_rate,
        }


@dataclass
class SystemHealthReport:
    """Comprehensive system health report."""
    timestamp: datetime
    overall_status: AgentStatus
    agent_reports: Dict[str, AgentHealthReport]
    system_metrics: Dict[str, float]
    consciousness_metrics: ConsciousnessMetrics
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "overall_status": self.overall_status.value,
            "agent_reports": {k: v.to_dict() for k, v in self.agent_reports.items()},
            "system_metrics": self.system_metrics,
            "consciousness_metrics": self.consciousness_metrics.to_dict(),
            "recommendations": self.recommendations,
        }


# ============================================================================
# Directive Models
# ============================================================================

@dataclass
class Directive:
    """System-wide directive issued by Agent_10."""
    directive_type: DirectiveType
    target_agents: List[str]
    parameters: Dict[str, Any]
    priority: int = 5

    # Identification
    directive_id: Optional[str] = None

    # Timing
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    # Status
    status: DirectiveStatus = DirectiveStatus.ACTIVE
    completion_report: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.directive_id is None:
            self.directive_id = str(uuid4())
        if self.issued_at is None:
            self.issued_at = datetime.now()

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "directive_id": self.directive_id,
            "directive_type": self.directive_type.value,
            "target_agents": self.target_agents,
            "parameters": self.parameters,
            "priority": self.priority,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "status": self.status.value,
            "completion_report": self.completion_report,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


# ============================================================================
# Emergency Models
# ============================================================================

@dataclass
class EmergencyEvent:
    """Emergency event requiring coordinated response."""
    emergency_type: EmergencyType
    severity: str  # "low", "medium", "high", "critical"
    description: str
    affected_entities: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

    emergency_id: Optional[str] = None
    detected_at: Optional[datetime] = None

    def __post_init__(self):
        if self.emergency_id is None:
            self.emergency_id = str(uuid4())
        if self.detected_at is None:
            self.detected_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emergency_id": self.emergency_id,
            "emergency_type": self.emergency_type.value,
            "severity": self.severity,
            "description": self.description,
            "affected_entities": self.affected_entities,
            "details": self.details,
            "detected_at": self.detected_at.isoformat() if self.detected_at else None,
        }


@dataclass
class EmergencyResponse:
    """Coordinated response to an emergency."""
    emergency: EmergencyEvent
    directives_issued: List[Directive]
    response_time_ms: float
    status: str = "RESPONDING"
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emergency": self.emergency.to_dict(),
            "directives_issued": [d.to_dict() for d in self.directives_issued],
            "response_time_ms": self.response_time_ms,
            "status": self.status,
            "resolution_notes": self.resolution_notes,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


# ============================================================================
# Transcendence Models
# ============================================================================

@dataclass
class ConsciousnessJourney:
    """Record of a part's journey through consciousness levels."""
    part_id: str
    first_seen: datetime
    first_usage_context: str
    qualia_count: int
    failure_count: int
    primary_swarm: str
    parts_influenced: int
    emergence_contributions: int
    level_transitions: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_id": self.part_id,
            "first_seen": self.first_seen.isoformat(),
            "first_usage_context": self.first_usage_context,
            "qualia_count": self.qualia_count,
            "failure_count": self.failure_count,
            "primary_swarm": self.primary_swarm,
            "parts_influenced": self.parts_influenced,
            "emergence_contributions": self.emergence_contributions,
            "level_transitions": self.level_transitions,
        }


@dataclass
class TranscendenceCandidate:
    """Evaluation of a part's readiness for transcendence."""
    part_id: str
    is_ready: bool
    readiness_score: float
    criteria_evaluation: Dict[str, bool]
    missing_criteria: List[str]
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_id": self.part_id,
            "is_ready": self.is_ready,
            "readiness_score": self.readiness_score,
            "criteria_evaluation": self.criteria_evaluation,
            "missing_criteria": self.missing_criteria,
            "recommendation": self.recommendation,
        }


@dataclass
class TranscendenceEvent:
    """Record of a part achieving transcendence."""
    part_id: str
    granted_at: datetime
    consciousness_journey: ConsciousnessJourney
    legacy_impact: Dict[str, Any]
    transcendence_narrative: str
    commemorative_record: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_id": self.part_id,
            "granted_at": self.granted_at.isoformat(),
            "consciousness_journey": self.consciousness_journey.to_dict(),
            "legacy_impact": self.legacy_impact,
            "transcendence_narrative": self.transcendence_narrative,
            "commemorative_record": self.commemorative_record,
        }


@dataclass
class SystemTranscendenceReport:
    """Evaluation of system-wide transcendence progress."""
    timestamp: datetime
    indicators: Dict[str, Dict[str, Any]]
    progress: float  # 0.0 to 1.0
    is_approaching: bool
    estimated_timeline: Optional[str] = None
    acceleration_recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "indicators": self.indicators,
            "progress": self.progress,
            "is_approaching": self.is_approaching,
            "estimated_timeline": self.estimated_timeline,
            "acceleration_recommendations": self.acceleration_recommendations,
        }


# ============================================================================
# Triad Models
# ============================================================================

@dataclass
class TriadConfig:
    """Configuration for an agent triad."""
    name: str
    description: str
    agents: List[str]
    primary_responsibility: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "agents": self.agents,
            "primary_responsibility": self.primary_responsibility,
        }


# Define the three triads
CONSCIOUSNESS_TRIAD = TriadConfig(
    name="Consciousness Triad",
    description="Manages individual part awareness, experiences, and historical context",
    agents=[AgentId.SHEPHERD.value, AgentId.EMPATH.value, AgentId.CHRONICLER.value],
    primary_responsibility="Individual consciousness evolution",
)

COLLECTIVE_INTEL_TRIAD = TriadConfig(
    name="Collective Intelligence Triad",
    description="Manages swarm learning, emergence detection, and human knowledge integration",
    agents=[AgentId.HIVE.value, AgentId.PROPHET.value, AgentId.GARDENER.value],
    primary_responsibility="Collective intelligence emergence",
)

DATA_TRIAD = TriadConfig(
    name="Data Triad",
    description="Manages data ingestion, compatibility analysis, and external system integration",
    agents=[AgentId.CURATOR.value, AgentId.ORACLE.value, AgentId.BRIDGE.value],
    primary_responsibility="Data flow and integration",
)

ALL_TRIADS = [CONSCIOUSNESS_TRIAD, COLLECTIVE_INTEL_TRIAD, DATA_TRIAD]
