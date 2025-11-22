"""
Core data models for the HIVE Swarm Coordinator.

These models define the structure of swarms, memberships, learnings,
and all data types used for collective intelligence orchestration.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Optional
from uuid import UUID, uuid4


class SwarmTier(Enum):
    """
    5-tier hierarchy for swarm organization.
    Parts typically belong to 5-15 swarms across tiers.
    """
    GLOBAL = 1       # Category-level (e.g., "Fasteners Swarm" - 50M+ members)
    FAMILY = 2       # Type-level (e.g., "Socket Head Cap Screws")
    SPEC = 3         # Size/Material-level (e.g., "M8x1.25 Grade 12.9")
    CONTEXT = 4      # Application-level (e.g., "Automotive Engine Fasteners")
    EXPERIENCE = 5   # Behavioral-level (e.g., "Parts That Survived Overload")


class SwarmRole(Enum):
    """
    Role of a part within a swarm based on consciousness level.
    """
    ELDER = "elder"             # Consciousness >= 4: Guides and teaches
    MENTOR = "mentor"           # Consciousness >= 3: Shares experience
    CONTRIBUTOR = "contributor" # Consciousness >= 2: Active participant
    LEARNER = "learner"         # Consciousness >= 1: Absorbs knowledge
    DORMANT = "dormant"         # Consciousness < 1: Not yet active


class LearningType(Enum):
    """Types of learnings that can be extracted and propagated."""
    FAILURE_MODE = "failure_mode"
    SURVIVAL_LIMIT = "survival_limit"
    LONGEVITY_FACTOR = "longevity_factor"
    COMPATIBILITY_INSIGHT = "compatibility_insight"
    USAGE_PATTERN = "usage_pattern"
    ENVIRONMENTAL_ADAPTATION = "environmental_adaptation"
    MAINTENANCE_WISDOM = "maintenance_wisdom"


class RecallSeverity(Enum):
    """Severity levels for recall notices."""
    CRITICAL = "critical"   # Immediate safety risk
    HIGH = "high"           # Significant defect
    WARNING = "warning"     # Potential issue
    ADVISORY = "advisory"   # Informational


class SwarmHealthStatus(Enum):
    """Health status of a swarm."""
    THRIVING = "thriving"       # High activity, good learning
    HEALTHY = "healthy"         # Normal operation
    DECLINING = "declining"     # Reduced activity
    STAGNANT = "stagnant"       # No recent learning
    DORMANT = "dormant"         # Inactive


@dataclass
class Swarm:
    """
    A learning collective of similar parts.
    """
    id: UUID = field(default_factory=uuid4)
    swarm_id: str = ""              # Unique identifier (e.g., "fasteners:global")

    # Classification
    tier: SwarmTier = SwarmTier.GLOBAL
    category: str = ""
    identifier: str = ""
    name: str = ""

    # Statistics
    member_count: int = 0
    active_member_count: int = 0
    elder_count: int = 0
    mentor_count: int = 0

    # Knowledge
    collective_knowledge: dict[str, Any] = field(default_factory=dict)
    learning_count: int = 0

    # Health
    activity_score: float = 0.0
    health_status: SwarmHealthStatus = SwarmHealthStatus.HEALTHY
    last_learning_at: Optional[datetime] = None

    # Relationships
    related_swarm_ids: list[UUID] = field(default_factory=list)
    parent_swarm_id: Optional[UUID] = None
    child_swarm_ids: list[UUID] = field(default_factory=list)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def get_swarm_key(self) -> str:
        """Generate unique swarm key based on tier and identifier."""
        return f"{self.tier.name.lower()}:{self.category}:{self.identifier}"


@dataclass
class SwarmMembership:
    """
    Represents a part's membership in a swarm.
    """
    id: UUID = field(default_factory=uuid4)
    part_id: UUID = field(default_factory=uuid4)
    swarm_id: UUID = field(default_factory=uuid4)

    # Role
    role: SwarmRole = SwarmRole.LEARNER
    influence_weight: float = 0.0

    # Activity tracking
    last_contribution_at: Optional[datetime] = None
    contribution_count: int = 0
    learnings_received: int = 0
    learnings_propagated: int = 0

    # Timestamps
    joined_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Learning:
    """
    A generalizable insight extracted from individual experience.
    """
    id: UUID = field(default_factory=uuid4)
    learning_type: LearningType = LearningType.USAGE_PATTERN

    # Content
    content: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    applicability: str = "similar_specs"  # How broadly this applies

    # Source
    source_part_id: Optional[UUID] = None
    source_qualia_id: Optional[UUID] = None
    source_consciousness_level: float = 0.0

    # Propagation tracking
    propagation_strength: float = 0.0
    swarms_affected: int = 0
    members_affected: int = 0

    # Novelty
    novelty_score: float = 0.5  # How new/unique this learning is

    # Timestamps
    learned_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RecallNotice:
    """
    An industry recall or safety notice.
    """
    id: UUID = field(default_factory=uuid4)

    # Source
    source: str = ""            # NHTSA, manufacturer, etc.
    source_recall_id: str = ""  # Original recall ID

    # Details
    severity: RecallSeverity = RecallSeverity.WARNING
    title: str = ""
    description: str = ""
    defect_description: str = ""
    recommended_action: str = ""

    # Affected parts criteria
    affected_criteria: dict[str, Any] = field(default_factory=dict)
    # e.g., {"manufacturer": "XYZ", "part_numbers": ["A123", "A124"], "date_range": ["2020-01", "2021-06"]}

    # Propagation tracking
    affected_swarm_ids: list[UUID] = field(default_factory=list)
    affected_parts_count: int = 0
    propagation_status: str = "pending"
    propagation_complete_at: Optional[datetime] = None

    # Timestamps
    issued_at: datetime = field(default_factory=datetime.utcnow)
    received_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SwarmMessage:
    """
    A message for inter-swarm communication.
    """
    id: UUID = field(default_factory=uuid4)

    # Routing
    source_swarm_id: UUID = field(default_factory=uuid4)
    target_swarm_ids: list[UUID] = field(default_factory=list)

    # Content
    message_type: str = ""  # "compatibility_update", "failure_alert", "learning_share"
    content: dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1-10, higher = more urgent

    # Delivery tracking
    delivered_to: list[UUID] = field(default_factory=list)
    delivery_status: str = "pending"

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


@dataclass
class SwarmHealth:
    """
    Health metrics for a swarm.
    """
    swarm_id: UUID = field(default_factory=uuid4)

    # Activity metrics
    activity_score: float = 0.0         # 0-1, based on recent activity
    learning_velocity: float = 0.0      # Learnings per day
    propagation_latency_ms: float = 0.0 # Average propagation time

    # Engagement metrics
    active_member_ratio: float = 0.0    # Active / Total members
    elder_ratio: float = 0.0            # Elders / Active members
    contribution_rate: float = 0.0      # Contributions per active member

    # Knowledge metrics
    knowledge_depth: int = 0            # Total learnings
    knowledge_breadth: int = 0          # Unique learning types
    knowledge_freshness: float = 0.0    # Recency of learnings

    # Overall status
    health_status: SwarmHealthStatus = SwarmHealthStatus.HEALTHY
    health_score: float = 0.0           # Composite 0-1 score

    # Recommendations
    recommendations: list[str] = field(default_factory=list)

    # Timestamp
    measured_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PropagationResult:
    """
    Result of a learning propagation operation.
    """
    learning: Learning = field(default_factory=Learning)

    # Scope
    swarms_targeted: int = 0
    swarms_updated: int = 0
    members_affected: int = 0

    # Metrics
    propagation_strength: float = 0.0
    propagation_time_ms: float = 0.0

    # Status
    success: bool = True
    errors: list[str] = field(default_factory=list)

    # Knowledge delta
    swarm_knowledge_deltas: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def aggregate(results: list["PropagationResult"]) -> "PropagationResult":
        """Aggregate multiple propagation results into one."""
        if not results:
            return PropagationResult()

        return PropagationResult(
            learning=results[0].learning,
            swarms_targeted=sum(r.swarms_targeted for r in results),
            swarms_updated=sum(r.swarms_updated for r in results),
            members_affected=sum(r.members_affected for r in results),
            propagation_strength=sum(r.propagation_strength for r in results) / len(results),
            propagation_time_ms=max(r.propagation_time_ms for r in results),
            success=all(r.success for r in results),
            errors=[e for r in results for e in r.errors],
        )


@dataclass
class CrossSwarmResult:
    """
    Result of cross-swarm communication.
    """
    source_swarm_id: UUID = field(default_factory=uuid4)
    target_swarm_ids: list[UUID] = field(default_factory=list)

    # Results per target
    delivery_results: dict[str, bool] = field(default_factory=dict)
    translation_applied: bool = False

    # Metrics
    latency_ms: float = 0.0

    # Compatibility updates
    compatibility_updates: list[dict[str, Any]] = field(default_factory=list)


# Type aliases for clarity
PartId = UUID
SwarmId = UUID
QualiaId = UUID
