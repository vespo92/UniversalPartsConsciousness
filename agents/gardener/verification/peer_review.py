"""
Peer Review System - Tier 2 community-based verification

Manages assignment and processing of peer reviews for contributions
that require human verification.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID

from ..models import (
    Contribution,
    ContributionType,
    CommunityUser,
    PeerReview,
    ReviewDecision,
    ReputationLevel,
)


@dataclass
class ReviewRequest:
    """A request for peer review"""
    contribution_id: str
    contribution: Contribution
    required_reviews: int = 2
    assigned_reviewers: List[UUID] = field(default_factory=list)
    completed_reviews: List[PeerReview] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    deadline: datetime = None
    priority: int = 0  # Higher = more urgent

    def __post_init__(self):
        if self.deadline is None:
            self.deadline = datetime.now() + timedelta(hours=48)


@dataclass
class ReviewerMatch:
    """Match between reviewer and contribution"""
    reviewer: CommunityUser
    match_score: float
    reasons: List[str] = field(default_factory=list)


class PeerReviewSystem:
    """
    Tier 2 peer review verification system.

    Responsibilities:
    - Match contributions with qualified reviewers
    - Manage review assignments
    - Process completed reviews
    - Calculate review consensus
    - Track reviewer performance
    """

    # Review requirements
    DEFAULT_REQUIRED_REVIEWS = 2
    MAX_REVIEWER_QUEUE = 5  # Max pending reviews per reviewer
    REVIEW_TIMEOUT_HOURS = 48

    # Minimum reputation for peer review
    MIN_REVIEW_REPUTATION = 500  # Trusted level

    def __init__(self, db_connection=None, notification_service=None):
        self.db = db_connection
        self.notifications = notification_service

        # Active review requests
        self._active_requests: Dict[str, ReviewRequest] = {}

        # Reviewer availability
        self._reviewer_queues: Dict[UUID, List[str]] = {}

    async def request_reviews(
        self,
        contribution: Contribution,
        required_count: int = DEFAULT_REQUIRED_REVIEWS
    ) -> ReviewRequest:
        """
        Request peer reviews for a contribution.

        Args:
            contribution: The contribution needing review
            required_count: Number of reviews required

        Returns:
            ReviewRequest with assignment details
        """
        request = ReviewRequest(
            contribution_id=contribution.contribution_id,
            contribution=contribution,
            required_reviews=required_count,
            priority=self._calculate_priority(contribution)
        )

        self._active_requests[contribution.contribution_id] = request

        # Find and assign reviewers
        reviewers = await self._find_qualified_reviewers(contribution, required_count)

        for reviewer_match in reviewers:
            await self._assign_reviewer(request, reviewer_match.reviewer)

        return request

    async def _find_qualified_reviewers(
        self,
        contribution: Contribution,
        count: int
    ) -> List[ReviewerMatch]:
        """Find qualified reviewers for a contribution"""
        qualified = []

        # Get all eligible reviewers
        candidates = await self._get_eligible_reviewers()

        for candidate in candidates:
            # Skip if this is the contributor
            if candidate.id == contribution.user_id:
                continue

            # Calculate match score
            match = self._calculate_reviewer_match(candidate, contribution)
            if match.match_score > 0.5:  # Minimum match threshold
                qualified.append(match)

        # Sort by match score and current queue size
        qualified.sort(key=lambda m: (
            m.match_score,
            -len(self._reviewer_queues.get(m.reviewer.id, []))
        ), reverse=True)

        return qualified[:count * 2]  # Return extra in case some decline

    def _calculate_reviewer_match(
        self,
        reviewer: CommunityUser,
        contribution: Contribution
    ) -> ReviewerMatch:
        """Calculate how well a reviewer matches a contribution"""
        score = 0.5  # Base score
        reasons = []

        # Category expertise
        category = self._get_contribution_category(contribution)
        if category in reviewer.expertise_categories:
            score += 0.2
            reasons.append(f"Expert in {category}")

        # Experience with contribution type
        # (would check from DB in production)
        score += 0.1
        reasons.append("Has reviewed similar contributions")

        # Accuracy rate bonus
        if reviewer.accuracy_rate > Decimal("0.95"):
            score += 0.1
            reasons.append("High accuracy reviewer")

        # Penalize heavy queue
        queue_size = len(self._reviewer_queues.get(reviewer.id, []))
        if queue_size > 3:
            score -= 0.1 * (queue_size - 3)

        return ReviewerMatch(
            reviewer=reviewer,
            match_score=min(1.0, max(0.0, score)),
            reasons=reasons
        )

    async def _assign_reviewer(
        self,
        request: ReviewRequest,
        reviewer: CommunityUser
    ) -> bool:
        """Assign a reviewer to a review request"""
        # Check if reviewer is at capacity
        current_queue = self._reviewer_queues.get(reviewer.id, [])
        if len(current_queue) >= self.MAX_REVIEWER_QUEUE:
            return False

        # Add to request
        request.assigned_reviewers.append(reviewer.id)

        # Add to reviewer's queue
        if reviewer.id not in self._reviewer_queues:
            self._reviewer_queues[reviewer.id] = []
        self._reviewer_queues[reviewer.id].append(request.contribution_id)

        # Send notification
        await self._notify_reviewer(reviewer, request)

        return True

    async def submit_review(
        self,
        contribution_id: str,
        reviewer_id: UUID,
        decision: ReviewDecision,
        confidence: float,
        comments: str = "",
        corrections: Dict[str, Any] = None
    ) -> PeerReview:
        """
        Submit a completed peer review.

        Args:
            contribution_id: The contribution being reviewed
            reviewer_id: The reviewer's ID
            decision: The review decision
            confidence: Reviewer's confidence (0-1)
            comments: Optional comments
            corrections: Optional suggested corrections

        Returns:
            The completed PeerReview
        """
        request = self._active_requests.get(contribution_id)
        if not request:
            raise ValueError(f"No active review request for {contribution_id}")

        if reviewer_id not in request.assigned_reviewers:
            raise ValueError("Reviewer not assigned to this contribution")

        # Create review
        review = PeerReview(
            contribution_id=request.contribution.id,
            reviewer_id=reviewer_id,
            decision=decision,
            confidence=Decimal(str(confidence)),
            comments=comments,
            corrections=corrections or {}
        )

        # Add to completed reviews
        request.completed_reviews.append(review)

        # Remove from reviewer's queue
        if reviewer_id in self._reviewer_queues:
            queue = self._reviewer_queues[reviewer_id]
            if contribution_id in queue:
                queue.remove(contribution_id)

        # Check if we have enough reviews
        if len(request.completed_reviews) >= request.required_reviews:
            await self._finalize_review(request)

        return review

    async def _finalize_review(self, request: ReviewRequest):
        """Finalize review when all reviews are complete"""
        # Calculate consensus
        consensus = self._calculate_consensus(request.completed_reviews)

        # Remove from active requests
        del self._active_requests[request.contribution_id]

        # Trigger workflow callback (handled by WorkflowEngine)
        # The WorkflowEngine should be notified via event/callback

    def _calculate_consensus(
        self,
        reviews: List[PeerReview]
    ) -> Dict[str, Any]:
        """Calculate consensus from peer reviews"""
        if not reviews:
            return {"decision": "pending", "confidence": 0}

        decisions = [r.decision for r in reviews]
        confidences = [float(r.confidence) for r in reviews]

        # Count decisions
        approve_count = sum(1 for d in decisions if d == ReviewDecision.APPROVE)
        reject_count = sum(1 for d in decisions if d == ReviewDecision.REJECT)
        expert_count = sum(1 for d in decisions if d == ReviewDecision.NEEDS_EXPERT)

        total = len(reviews)
        avg_confidence = sum(confidences) / total

        # Expert request takes precedence
        if expert_count > 0:
            return {
                "decision": "needs_expert",
                "confidence": avg_confidence,
                "vote_counts": {
                    "approve": approve_count,
                    "reject": reject_count,
                    "expert": expert_count
                }
            }

        # Clear majority for approve
        if approve_count > reject_count and approve_count >= 2:
            return {
                "decision": "approve",
                "confidence": avg_confidence,
                "vote_counts": {
                    "approve": approve_count,
                    "reject": reject_count,
                    "expert": expert_count
                }
            }

        # Clear majority for reject
        if reject_count >= 2:
            return {
                "decision": "reject",
                "confidence": avg_confidence,
                "vote_counts": {
                    "approve": approve_count,
                    "reject": reject_count,
                    "expert": expert_count
                }
            }

        # Split decision - escalate to expert
        return {
            "decision": "needs_expert",
            "confidence": avg_confidence,
            "reason": "Split peer review decision",
            "vote_counts": {
                "approve": approve_count,
                "reject": reject_count,
                "expert": expert_count
            }
        }

    def _calculate_priority(self, contribution: Contribution) -> int:
        """Calculate review priority for a contribution"""
        priority = 0

        # Higher priority for important types
        priority_types = {
            ContributionType.CORRECTION: 3,
            ContributionType.FAILURE_REPORT: 2,
            ContributionType.PART_DATA: 1,
        }
        priority += priority_types.get(contribution.contribution_type, 0)

        return priority

    def _get_contribution_category(self, contribution: Contribution) -> str:
        """Extract category from contribution content"""
        content = contribution.content
        return content.get("category", "general")

    async def get_reviewer_queue(self, reviewer_id: UUID) -> List[ReviewRequest]:
        """Get pending reviews for a reviewer"""
        contribution_ids = self._reviewer_queues.get(reviewer_id, [])
        return [
            self._active_requests[cid]
            for cid in contribution_ids
            if cid in self._active_requests
        ]

    async def decline_review(
        self,
        contribution_id: str,
        reviewer_id: UUID,
        reason: str = ""
    ):
        """Allow a reviewer to decline a review assignment"""
        request = self._active_requests.get(contribution_id)
        if not request:
            return

        # Remove from assignment
        if reviewer_id in request.assigned_reviewers:
            request.assigned_reviewers.remove(reviewer_id)

        # Remove from queue
        if reviewer_id in self._reviewer_queues:
            queue = self._reviewer_queues[reviewer_id]
            if contribution_id in queue:
                queue.remove(contribution_id)

        # Find replacement reviewer
        replacements = await self._find_qualified_reviewers(
            request.contribution, count=1
        )
        if replacements:
            await self._assign_reviewer(request, replacements[0].reviewer)

    async def _notify_reviewer(self, reviewer: CommunityUser, request: ReviewRequest):
        """Send notification to reviewer about new assignment"""
        if not self.notifications:
            return

        await self.notifications.send(
            user_id=reviewer.id,
            notification_type="review_assigned",
            title="New peer review assigned",
            message=f"Please review contribution {request.contribution_id}",
            data={
                "contribution_id": request.contribution_id,
                "type": request.contribution.contribution_type.value,
                "deadline": request.deadline.isoformat()
            }
        )

    async def _get_eligible_reviewers(self) -> List[CommunityUser]:
        """Get all users eligible for peer review"""
        # In production, query database for users with sufficient reputation
        # and peer_review permission
        return []

    def get_pending_reviews_count(self) -> int:
        """Get total count of pending reviews"""
        return len(self._active_requests)

    async def check_timeouts(self):
        """Check for timed out review requests"""
        now = datetime.now()
        timed_out = []

        for contribution_id, request in self._active_requests.items():
            if now > request.deadline:
                timed_out.append(contribution_id)

        # Handle timed out requests
        for contribution_id in timed_out:
            request = self._active_requests[contribution_id]
            # If we have at least one review, finalize with what we have
            if request.completed_reviews:
                await self._finalize_review(request)
            # Otherwise escalate to expert


# Import Decimal at module level
from decimal import Decimal
