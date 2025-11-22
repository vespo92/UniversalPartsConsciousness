"""
Agent_8: Community Cultivator (GARDENER) - Data Models

Core data structures for the community contribution and verification system.
Bridges human expertise with machine learning through community contributions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


# ============================================================================
# Enums
# ============================================================================

class ContributionType(Enum):
    """Types of community contributions"""
    PART_DATA = "part_data"
    MEASUREMENT = "measurement"
    FAILURE_REPORT = "failure_report"
    CORRECTION = "correction"
    PHOTO = "photo"
    CAD_MODEL = "cad_model"
    APPLICATION_NOTE = "application_note"
    CROSS_REFERENCE = "cross_reference"
    TRIBAL_KNOWLEDGE = "tribal_knowledge"


class VerificationStatus(Enum):
    """Status of contribution verification"""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    NEEDS_REVIEW = "needs_review"
    NEEDS_EXPERT = "needs_expert"
    APPROVED = "approved"
    CONDITIONAL = "conditional"
    REJECTED = "rejected"
    MERGED = "merged"


class VerificationTier(Enum):
    """Verification tier levels"""
    AUTOMATED = 1
    PEER = 2
    EXPERT = 3


class ReviewDecision(Enum):
    """Possible review decisions"""
    APPROVE = "approve"
    REJECT = "reject"
    NEEDS_EXPERT = "needs_expert"
    NEEDS_REVISION = "needs_revision"


class UserStatus(Enum):
    """User account status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"


class ReputationLevel(Enum):
    """Reputation levels with their thresholds"""
    NEWCOMER = (0, 0)
    CONTRIBUTOR = (1, 100)
    TRUSTED = (2, 500)
    EXPERT = (3, 2000)
    MASTER = (4, 10000)
    ELDER = (5, 50000)

    def __init__(self, level: int, min_points: int):
        self._level = level
        self._min_points = min_points

    @property
    def level(self) -> int:
        return self._level

    @property
    def min_points(self) -> int:
        return self._min_points


class ExpertDomain(Enum):
    """Domain expertise areas"""
    FASTENERS = "fasteners"
    BEARINGS = "bearings"
    SEALS_GASKETS = "seals_gaskets"
    AUTOMOTIVE_ENGINES = "automotive_engines"
    AEROSPACE = "aerospace"
    MARINE = "marine"
    HEAVY_EQUIPMENT = "heavy_equipment"
    PRECISION_INSTRUMENTS = "precision_instruments"
    MATERIALS_SCIENCE = "materials_science"
    MANUFACTURING_PROCESSES = "manufacturing_processes"


# ============================================================================
# User Models
# ============================================================================

@dataclass
class CommunityUser:
    """Community user profile and statistics"""
    id: UUID = field(default_factory=uuid4)
    user_id: str = ""
    username: str = ""
    display_name: str = ""
    email: str = ""
    joined_at: datetime = field(default_factory=datetime.now)

    # Reputation
    lifetime_points: int = 0
    current_level: int = 0
    permissions: List[str] = field(default_factory=lambda: ["submit"])

    # Statistics
    contribution_count: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    review_count: int = 0
    accuracy_rate: Decimal = Decimal("1.000")

    # Activity
    last_contribution: Optional[datetime] = None
    last_review: Optional[datetime] = None
    last_login: Optional[datetime] = None
    streak_days: int = 0

    # Expertise
    expertise_categories: List[str] = field(default_factory=list)
    expert_domains: List[str] = field(default_factory=list)

    # Status
    status: UserStatus = UserStatus.ACTIVE
    verified: bool = False


@dataclass
class ReputationScore:
    """Calculated reputation score for a user"""
    lifetime_points: int
    effective_points: float
    level: ReputationLevel
    rank: int
    next_level_progress: float
    permissions: List[str] = field(default_factory=list)


@dataclass
class PointAward:
    """Record of points awarded to a user"""
    user_id: UUID
    action: str
    base_points: int
    multiplier: float
    final_points: int
    new_total: int
    awarded_at: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Contribution Models
# ============================================================================

@dataclass
class Contribution:
    """A community contribution submission"""
    id: UUID = field(default_factory=uuid4)
    contribution_id: str = ""

    # Contributor
    user_id: UUID = field(default_factory=uuid4)
    submitted_at: datetime = field(default_factory=datetime.now)

    # Content
    contribution_type: ContributionType = ContributionType.PART_DATA
    target_part_id: Optional[UUID] = None
    content: Dict[str, Any] = field(default_factory=dict)

    # Verification
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verification_tier: int = 0
    confidence_score: Optional[Decimal] = None

    # Review tracking
    peer_reviews: List["PeerReview"] = field(default_factory=list)
    expert_review: Optional["ExpertReview"] = None

    # Resolution
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None
    resolution_notes: str = ""

    def generate_contribution_id(self) -> str:
        """Generate a unique contribution ID"""
        prefix = self.contribution_type.value[:3].upper()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        short_uuid = str(self.id)[:8]
        self.contribution_id = f"{prefix}-{timestamp}-{short_uuid}"
        return self.contribution_id


@dataclass
class VerificationCheck:
    """Result of a single verification check"""
    name: str
    passed: bool
    critical: bool = False
    warning: bool = False
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AutoVerificationResult:
    """Result of automated verification"""
    status: str  # APPROVED, NEEDS_REVIEW, REJECTED
    confidence: Decimal = Decimal("0")
    reason: str = ""
    notes: str = ""
    checks: List[VerificationCheck] = field(default_factory=list)
    concerns: List[VerificationCheck] = field(default_factory=list)
    warnings: List[VerificationCheck] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """Overall verification result"""
    status: str  # APPROVED, REJECTED, CONDITIONAL
    tier_reached: int
    confidence: Decimal = Decimal("0")
    reason: str = ""
    notes: str = ""
    reviewer_comments: List[str] = field(default_factory=list)
    expert_assessment: str = ""
    conditions: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


# ============================================================================
# Review Models
# ============================================================================

@dataclass
class PeerReview:
    """A peer review of a contribution"""
    id: UUID = field(default_factory=uuid4)
    contribution_id: UUID = field(default_factory=uuid4)
    reviewer_id: UUID = field(default_factory=uuid4)

    # Review
    decision: ReviewDecision = ReviewDecision.APPROVE
    confidence: Decimal = Decimal("0.8")
    comments: str = ""
    corrections: Dict[str, Any] = field(default_factory=dict)

    reviewed_at: datetime = field(default_factory=datetime.now)


@dataclass
class ExpertReview:
    """An expert review of a contribution"""
    id: UUID = field(default_factory=uuid4)
    contribution_id: UUID = field(default_factory=uuid4)
    expert_id: UUID = field(default_factory=uuid4)

    # Assignment
    assigned_at: Optional[datetime] = None
    deadline: Optional[datetime] = None

    # Review
    decision: Optional[ReviewDecision] = None
    assessment: str = ""
    conditions: List[str] = field(default_factory=list)
    confidence: Decimal = Decimal("0")

    # Completion
    completed_at: Optional[datetime] = None
    compensation_paid: bool = False
    compensation_amount: Decimal = Decimal("0")


@dataclass
class ExpertAssignment:
    """Assignment of contribution to an expert"""
    status: str  # ASSIGNED, QUEUED, UNAVAILABLE
    expert: Optional[CommunityUser] = None
    contribution: Optional[Contribution] = None
    deadline: Optional[datetime] = None
    compensation: Decimal = Decimal("0")
    estimated_wait_time: Optional[int] = None  # hours


@dataclass
class ExpertApplication:
    """Application for expert status"""
    status: str  # PENDING_REVIEW, APPROVED, REJECTED
    user: Optional[CommunityUser] = None
    domain: str = ""
    reason: str = ""
    stats: Dict[str, Any] = field(default_factory=dict)
    next_step: str = ""


# ============================================================================
# Gamification Models
# ============================================================================

@dataclass
class Achievement:
    """An achievement that can be earned"""
    id: str
    name: str
    description: str
    points: int
    badge: str
    category: str = "general"
    requirement: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserAchievement:
    """An achievement earned by a user"""
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    achievement_id: str = ""
    earned_at: datetime = field(default_factory=datetime.now)
    points_awarded: int = 0


@dataclass
class Challenge:
    """A time-limited challenge"""
    id: str
    name: str
    description: str
    reward_points: int
    duration_days: int
    requirement: Dict[str, Any] = field(default_factory=dict)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class UserChallenge:
    """User's participation in a challenge"""
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    challenge_id: str = ""
    started_at: datetime = field(default_factory=datetime.now)
    progress: Dict[str, Any] = field(default_factory=dict)
    completed: bool = False
    completed_at: Optional[datetime] = None


@dataclass
class LeaderboardEntry:
    """An entry in a leaderboard"""
    rank: int
    user_id: UUID
    username: str
    display_name: str
    points: int
    level: int
    contribution_count: int
    badges: List[str] = field(default_factory=list)


@dataclass
class Leaderboard:
    """A complete leaderboard"""
    leaderboard_type: str  # all_time, monthly, weekly, category
    category: Optional[str] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    entries: List[LeaderboardEntry] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# Message Bus Models (Inter-Agent Communication)
# ============================================================================

@dataclass
class GardenerMessage:
    """Message for inter-agent communication"""
    id: UUID = field(default_factory=uuid4)
    source_agent: str = "Agent_8_Gardener"
    target_agent: str = ""
    topic: str = ""
    message_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[UUID] = None


# Message topics used by Gardener
class GardenerTopics:
    """Topics for Gardener inter-agent communication"""
    # Outgoing to Agent_1 (Data Curator)
    VERIFIED_CONTRIBUTION = "upc.community.contribution.verified"

    # Outgoing to Agent_4 (Qualia Collector)
    COMMUNITY_EXPERIENCE = "upc.community.experience.submitted"

    # Outgoing to Agent_7 (Automotive Historian)
    TRIBAL_KNOWLEDGE = "upc.community.tribal_knowledge.verified"

    # Incoming from all agents
    REVIEW_REQUEST = "upc.community.review.requested"

    # Internal events
    USER_LEVEL_UP = "upc.community.user.level_up"
    ACHIEVEMENT_EARNED = "upc.community.achievement.earned"
    EXPERT_ASSIGNED = "upc.community.expert.assigned"
