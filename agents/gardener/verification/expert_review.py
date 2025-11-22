"""
Expert Review System - Tier 3 authoritative verification

Manages expert panel reviews for complex contributions requiring
domain expertise and authoritative verification.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..models import (
    Contribution,
    ContributionType,
    CommunityUser,
    ExpertReview,
    ExpertAssignment,
    ExpertDomain,
    ReviewDecision,
)


@dataclass
class ExpertProfile:
    """Extended profile for expert panelists"""
    user: CommunityUser
    domains: List[ExpertDomain]
    credentials: Dict[str, Any] = field(default_factory=dict)
    verification_date: Optional[datetime] = None
    active: bool = True
    max_queue_size: int = 5
    current_queue_size: int = 0
    specialties: List[str] = field(default_factory=list)
    review_count: int = 0
    avg_review_time_hours: float = 24.0
    compensation_rate: Decimal = Decimal("0")  # Per review
    volunteer: bool = True


@dataclass
class ExpertReviewRequest:
    """Request for expert review"""
    contribution_id: str
    contribution: Contribution
    domain: ExpertDomain
    assigned_expert: Optional[ExpertProfile] = None
    assignment: Optional[ExpertAssignment] = None
    created_at: datetime = field(default_factory=datetime.now)
    priority: int = 0
    urgency_reason: str = ""


class ExpertReviewSystem:
    """
    Tier 3 expert review verification system.

    Manages the expert panel for authoritative reviews of complex
    contributions that require domain expertise.

    Responsibilities:
    - Expert panel management
    - Expert matching and assignment
    - Review processing
    - Compensation tracking
    - Quality assurance
    """

    # Expert requirements (from Agent_8 spec)
    EXPERT_REQUIREMENTS = {
        "minimum_reputation": 10000,
        "minimum_contributions": 200,
        "domain_contributions": 50,
        "accuracy_rate": Decimal("0.95"),
    }

    # Review configuration
    DEFAULT_DEADLINE_DAYS = 3
    COMPENSATION_BASE = Decimal("25.00")  # Base compensation per review

    def __init__(self, db_connection=None, notification_service=None):
        self.db = db_connection
        self.notifications = notification_service

        # Expert panel
        self._experts: Dict[UUID, ExpertProfile] = {}

        # Active review requests
        self._pending_requests: Dict[str, ExpertReviewRequest] = {}
        self._assigned_requests: Dict[str, ExpertReviewRequest] = {}

        # Domain mapping for contributions
        self._domain_mappings: Dict[str, ExpertDomain] = {}

    async def assign_expert(
        self,
        contribution: Contribution
    ) -> ExpertAssignment:
        """
        Assign an expert to review a contribution.

        Args:
            contribution: The contribution needing expert review

        Returns:
            ExpertAssignment with assignment details
        """
        # Determine required domain
        domain = self._determine_domain(contribution)

        # Create review request
        request = ExpertReviewRequest(
            contribution_id=contribution.contribution_id,
            contribution=contribution,
            domain=domain,
            priority=self._calculate_priority(contribution)
        )

        # Find available expert
        expert = await self._find_best_expert(domain, contribution)

        if not expert:
            # Queue for later assignment
            self._pending_requests[contribution.contribution_id] = request
            return ExpertAssignment(
                status="QUEUED",
                estimated_wait_time=self._estimate_wait_time(domain)
            )

        # Calculate compensation
        compensation = self._calculate_compensation(contribution, expert)

        # Create assignment
        deadline = datetime.now() + timedelta(days=self.DEFAULT_DEADLINE_DAYS)
        assignment = ExpertAssignment(
            status="ASSIGNED",
            expert=expert.user,
            contribution=contribution,
            deadline=deadline,
            compensation=compensation
        )

        # Update tracking
        request.assigned_expert = expert
        request.assignment = assignment
        self._assigned_requests[contribution.contribution_id] = request

        # Update expert queue
        expert.current_queue_size += 1

        # Notify expert
        await self._notify_expert(expert, request)

        return assignment

    async def _find_best_expert(
        self,
        domain: ExpertDomain,
        contribution: Contribution
    ) -> Optional[ExpertProfile]:
        """Find the best available expert for a contribution"""
        # Get experts in domain
        domain_experts = [
            e for e in self._experts.values()
            if domain in e.domains and e.active
        ]

        if not domain_experts:
            return None

        # Filter by availability
        available = [
            e for e in domain_experts
            if e.current_queue_size < e.max_queue_size
        ]

        if not available:
            return None

        # Score experts
        scored = []
        for expert in available:
            score = self._score_expert_match(expert, contribution)
            scored.append((expert, score))

        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[0][0] if scored else None

    def _score_expert_match(
        self,
        expert: ExpertProfile,
        contribution: Contribution
    ) -> float:
        """Score how well an expert matches a contribution"""
        score = 0.5  # Base score

        # Specialty match
        category = contribution.content.get("category", "")
        if category in expert.specialties:
            score += 0.3

        # Availability bonus (less queue = higher score)
        availability = 1 - (expert.current_queue_size / expert.max_queue_size)
        score += availability * 0.2

        # Experience bonus
        if expert.review_count > 100:
            score += 0.1

        # Speed bonus (faster reviewers get slight preference)
        if expert.avg_review_time_hours < 24:
            score += 0.05

        return min(1.0, score)

    def _determine_domain(self, contribution: Contribution) -> ExpertDomain:
        """Determine the expert domain for a contribution"""
        content = contribution.content
        category = content.get("category", "").lower()

        # Map categories to domains
        domain_map = {
            "fastener": ExpertDomain.FASTENERS,
            "bolt": ExpertDomain.FASTENERS,
            "screw": ExpertDomain.FASTENERS,
            "nut": ExpertDomain.FASTENERS,
            "bearing": ExpertDomain.BEARINGS,
            "seal": ExpertDomain.SEALS_GASKETS,
            "gasket": ExpertDomain.SEALS_GASKETS,
            "engine": ExpertDomain.AUTOMOTIVE_ENGINES,
            "automotive": ExpertDomain.AUTOMOTIVE_ENGINES,
            "aerospace": ExpertDomain.AEROSPACE,
            "marine": ExpertDomain.MARINE,
            "heavy": ExpertDomain.HEAVY_EQUIPMENT,
            "precision": ExpertDomain.PRECISION_INSTRUMENTS,
            "material": ExpertDomain.MATERIALS_SCIENCE,
            "manufacturing": ExpertDomain.MANUFACTURING_PROCESSES,
        }

        for keyword, domain in domain_map.items():
            if keyword in category:
                return domain

        # Default based on contribution type
        if contribution.contribution_type == ContributionType.CAD_MODEL:
            return ExpertDomain.MANUFACTURING_PROCESSES
        if contribution.contribution_type == ContributionType.FAILURE_REPORT:
            return ExpertDomain.MATERIALS_SCIENCE

        return ExpertDomain.FASTENERS  # Default

    def _calculate_priority(self, contribution: Contribution) -> int:
        """Calculate review priority"""
        priority = 0

        # Failure reports are high priority
        if contribution.contribution_type == ContributionType.FAILURE_REPORT:
            priority += 3

        # CAD models are moderate priority
        if contribution.contribution_type == ContributionType.CAD_MODEL:
            priority += 2

        # Check for safety implications
        content = contribution.content
        if content.get("safety_critical"):
            priority += 5

        return priority

    def _calculate_compensation(
        self,
        contribution: Contribution,
        expert: ExpertProfile
    ) -> Decimal:
        """Calculate compensation for expert review"""
        if expert.volunteer:
            return Decimal("0")

        base = expert.compensation_rate or self.COMPENSATION_BASE

        # Complexity multiplier
        multiplier = Decimal("1.0")

        if contribution.contribution_type == ContributionType.CAD_MODEL:
            multiplier = Decimal("1.5")
        elif contribution.contribution_type == ContributionType.FAILURE_REPORT:
            multiplier = Decimal("1.25")

        return base * multiplier

    async def submit_review(
        self,
        contribution_id: str,
        expert_id: UUID,
        decision: ReviewDecision,
        assessment: str,
        confidence: float,
        conditions: List[str] = None
    ) -> ExpertReview:
        """
        Submit a completed expert review.

        Args:
            contribution_id: The contribution being reviewed
            expert_id: The expert's ID
            decision: The review decision
            assessment: Detailed expert assessment
            confidence: Expert's confidence (0-1)
            conditions: Optional conditions for conditional approval

        Returns:
            The completed ExpertReview
        """
        request = self._assigned_requests.get(contribution_id)
        if not request:
            raise ValueError(f"No assigned review for {contribution_id}")

        if not request.assigned_expert or request.assigned_expert.user.id != expert_id:
            raise ValueError("Expert not assigned to this contribution")

        # Create review
        review = ExpertReview(
            contribution_id=request.contribution.id,
            expert_id=expert_id,
            assigned_at=request.assignment.deadline - timedelta(days=self.DEFAULT_DEADLINE_DAYS),
            deadline=request.assignment.deadline,
            decision=decision,
            assessment=assessment,
            confidence=Decimal(str(confidence)),
            conditions=conditions or [],
            completed_at=datetime.now(),
            compensation_amount=request.assignment.compensation
        )

        # Update expert stats
        expert = request.assigned_expert
        expert.current_queue_size -= 1
        expert.review_count += 1

        # Calculate review time
        if review.assigned_at:
            review_hours = (review.completed_at - review.assigned_at).total_seconds() / 3600
            # Update rolling average
            expert.avg_review_time_hours = (
                expert.avg_review_time_hours * 0.9 + review_hours * 0.1
            )

        # Remove from assigned requests
        del self._assigned_requests[contribution_id]

        # Mark compensation as pending
        if review.compensation_amount > 0:
            await self._queue_compensation(expert, review)

        return review

    async def _queue_compensation(self, expert: ExpertProfile, review: ExpertReview):
        """Queue compensation for an expert review"""
        # In production, this would integrate with payment system
        pass

    async def _notify_expert(self, expert: ExpertProfile, request: ExpertReviewRequest):
        """Notify expert of new review assignment"""
        if not self.notifications:
            return

        await self.notifications.send(
            user_id=expert.user.id,
            notification_type="expert_review_assigned",
            title="Expert review assigned",
            message=f"Please review contribution {request.contribution_id}",
            data={
                "contribution_id": request.contribution_id,
                "type": request.contribution.contribution_type.value,
                "domain": request.domain.value,
                "deadline": request.assignment.deadline.isoformat(),
                "compensation": float(request.assignment.compensation)
            }
        )

    def _estimate_wait_time(self, domain: ExpertDomain) -> int:
        """Estimate wait time in hours for a domain"""
        # Count pending requests for domain
        pending_count = sum(
            1 for r in self._pending_requests.values()
            if r.domain == domain
        )

        # Get average review time for domain experts
        domain_experts = [
            e for e in self._experts.values()
            if domain in e.domains and e.active
        ]

        if not domain_experts:
            return 168  # 1 week if no experts

        avg_time = sum(e.avg_review_time_hours for e in domain_experts) / len(domain_experts)
        total_capacity = sum(e.max_queue_size - e.current_queue_size for e in domain_experts)

        if total_capacity <= 0:
            return int(avg_time * (pending_count + 1))

        return int(avg_time * (pending_count / total_capacity + 1))

    # Expert Panel Management

    async def add_expert(
        self,
        user: CommunityUser,
        domains: List[ExpertDomain],
        credentials: Dict[str, Any],
        specialties: List[str] = None,
        volunteer: bool = True,
        compensation_rate: Decimal = None
    ) -> ExpertProfile:
        """Add a new expert to the panel"""
        # Verify requirements
        if user.lifetime_points < self.EXPERT_REQUIREMENTS["minimum_reputation"]:
            raise ValueError("Insufficient reputation for expert status")

        if user.contribution_count < self.EXPERT_REQUIREMENTS["minimum_contributions"]:
            raise ValueError("Insufficient contribution count for expert status")

        if user.accuracy_rate < self.EXPERT_REQUIREMENTS["accuracy_rate"]:
            raise ValueError("Accuracy rate below expert threshold")

        profile = ExpertProfile(
            user=user,
            domains=domains,
            credentials=credentials,
            verification_date=datetime.now(),
            active=True,
            specialties=specialties or [],
            volunteer=volunteer,
            compensation_rate=compensation_rate or Decimal("0")
        )

        self._experts[user.id] = profile

        # Grant expert permissions
        if "expert_review" not in user.permissions:
            user.permissions.append("expert_review")

        return profile

    async def deactivate_expert(self, expert_id: UUID, reason: str = ""):
        """Deactivate an expert"""
        if expert_id in self._experts:
            self._experts[expert_id].active = False

            # Reassign pending reviews
            await self._reassign_expert_reviews(expert_id)

    async def _reassign_expert_reviews(self, expert_id: UUID):
        """Reassign reviews from a deactivated expert"""
        for contribution_id, request in list(self._assigned_requests.items()):
            if request.assigned_expert and request.assigned_expert.user.id == expert_id:
                # Return to pending queue
                del self._assigned_requests[contribution_id]
                self._pending_requests[contribution_id] = request
                request.assigned_expert = None
                request.assignment = None

                # Try to find new expert
                await self.assign_expert(request.contribution)

    def get_expert_panel(
        self,
        domain: Optional[ExpertDomain] = None,
        active_only: bool = True
    ) -> List[ExpertProfile]:
        """Get experts, optionally filtered by domain"""
        experts = list(self._experts.values())

        if active_only:
            experts = [e for e in experts if e.active]

        if domain:
            experts = [e for e in experts if domain in e.domains]

        return experts

    def get_expert_stats(self, expert_id: UUID) -> Dict[str, Any]:
        """Get statistics for an expert"""
        expert = self._experts.get(expert_id)
        if not expert:
            return {}

        return {
            "review_count": expert.review_count,
            "avg_review_time_hours": expert.avg_review_time_hours,
            "current_queue_size": expert.current_queue_size,
            "domains": [d.value for d in expert.domains],
            "active": expert.active,
            "volunteer": expert.volunteer
        }

    async def process_pending_queue(self):
        """Process pending requests when experts become available"""
        for contribution_id, request in list(self._pending_requests.items()):
            assignment = await self.assign_expert(request.contribution)
            if assignment.status == "ASSIGNED":
                del self._pending_requests[contribution_id]
