"""
Workflow Engine - Manages contribution verification workflow

Orchestrates the 3-tier verification process from submission to integration.
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
    VerificationStatus,
    VerificationResult,
    VerificationTier,
    PeerReview,
    ExpertReview,
    GardenerMessage,
    GardenerTopics,
)


@dataclass
class WorkflowState:
    """Current state of a contribution's workflow"""
    contribution_id: str
    current_tier: VerificationTier
    status: VerificationStatus
    started_at: datetime = field(default_factory=datetime.now)
    tier_started_at: datetime = field(default_factory=datetime.now)
    retry_count: int = 0
    escalation_reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowTransition:
    """A transition in the workflow state machine"""
    from_status: VerificationStatus
    to_status: VerificationStatus
    trigger: str
    timestamp: datetime = field(default_factory=datetime.now)
    actor: str = ""  # User ID or "system"
    notes: str = ""


class WorkflowEngine:
    """
    Manages the contribution verification workflow.

    State Machine:
    PENDING -> IN_REVIEW (Tier 1: Automated)
           -> APPROVED (auto-approve)
           -> NEEDS_REVIEW (escalate to Tier 2)
           -> REJECTED

    NEEDS_REVIEW -> IN_REVIEW (Tier 2: Peer)
                 -> APPROVED (peer consensus)
                 -> NEEDS_EXPERT (escalate to Tier 3)
                 -> REJECTED

    NEEDS_EXPERT -> IN_REVIEW (Tier 3: Expert)
                 -> APPROVED
                 -> CONDITIONAL
                 -> REJECTED

    APPROVED/CONDITIONAL -> MERGED (integrated into main database)
    """

    # Workflow configuration
    PEER_REVIEW_THRESHOLD = 2  # Reviews needed for consensus
    PEER_REVIEW_TIMEOUT_HOURS = 48
    EXPERT_REVIEW_TIMEOUT_HOURS = 72
    MAX_RETRY_COUNT = 3

    # Contribution types that skip peer review (go straight to auto-approve if passed)
    AUTO_APPROVE_TYPES = [
        ContributionType.PHOTO,
    ]

    # Contribution types that always need expert review
    EXPERT_REQUIRED_TYPES = [
        ContributionType.CAD_MODEL,
        ContributionType.FAILURE_REPORT,
    ]

    def __init__(
        self,
        auto_verifier=None,
        peer_review_system=None,
        expert_review_system=None,
        integration_handler=None,
        message_bus=None
    ):
        self.auto_verifier = auto_verifier
        self.peer_review_system = peer_review_system
        self.expert_review_system = expert_review_system
        self.integration_handler = integration_handler
        self.message_bus = message_bus

        # Active workflow states
        self._workflows: Dict[str, WorkflowState] = {}
        self._transition_history: Dict[str, List[WorkflowTransition]] = {}

        # Callbacks for workflow events
        self._event_handlers: Dict[str, List[Callable]] = {}

    async def start_workflow(self, contribution: Contribution) -> WorkflowState:
        """
        Start verification workflow for a contribution.

        Args:
            contribution: The contribution to verify

        Returns:
            Initial workflow state
        """
        # Create workflow state
        state = WorkflowState(
            contribution_id=contribution.contribution_id,
            current_tier=VerificationTier.AUTOMATED,
            status=VerificationStatus.IN_REVIEW,
        )

        self._workflows[contribution.contribution_id] = state
        self._transition_history[contribution.contribution_id] = []

        # Record initial transition
        self._record_transition(
            contribution.contribution_id,
            VerificationStatus.PENDING,
            VerificationStatus.IN_REVIEW,
            "workflow_started",
            "system"
        )

        # Start automated verification
        await self._run_tier1_verification(contribution, state)

        return state

    async def _run_tier1_verification(
        self,
        contribution: Contribution,
        state: WorkflowState
    ):
        """Run Tier 1 automated verification"""
        if self.auto_verifier is None:
            # Skip to peer review if no auto-verifier
            await self._escalate_to_tier2(contribution, state, "No auto-verifier configured")
            return

        result = await self.auto_verifier.verify(contribution)

        if result.status == "APPROVED":
            # Check if auto-approve is allowed for this type
            if contribution.contribution_type in self.AUTO_APPROVE_TYPES:
                await self._approve_contribution(contribution, state, result)
            else:
                # Still escalate to peer review for quality assurance
                await self._escalate_to_tier2(
                    contribution, state,
                    "Auto-verification passed, proceeding to peer review"
                )

        elif result.status == "NEEDS_REVIEW":
            await self._escalate_to_tier2(contribution, state, result.reason)

        elif result.status == "REJECTED":
            await self._reject_contribution(contribution, state, result)

    async def _escalate_to_tier2(
        self,
        contribution: Contribution,
        state: WorkflowState,
        reason: str
    ):
        """Escalate to Tier 2 peer review"""
        state.current_tier = VerificationTier.PEER
        state.status = VerificationStatus.NEEDS_REVIEW
        state.tier_started_at = datetime.now()
        state.escalation_reason = reason

        self._record_transition(
            contribution.contribution_id,
            VerificationStatus.IN_REVIEW,
            VerificationStatus.NEEDS_REVIEW,
            "escalate_to_peer",
            "system",
            reason
        )

        # Request peer reviews
        if self.peer_review_system:
            await self.peer_review_system.request_reviews(
                contribution,
                required_count=self.PEER_REVIEW_THRESHOLD
            )

        # Fire event
        await self._fire_event("tier2_started", contribution, state)

    async def process_peer_review(
        self,
        contribution_id: str,
        review: PeerReview
    ):
        """Process a completed peer review"""
        state = self._workflows.get(contribution_id)
        if not state or state.current_tier != VerificationTier.PEER:
            return

        contribution = await self._get_contribution(contribution_id)
        if not contribution:
            return

        # Add review to contribution
        contribution.peer_reviews.append(review)

        # Check if we have enough reviews for consensus
        if len(contribution.peer_reviews) >= self.PEER_REVIEW_THRESHOLD:
            consensus = self._calculate_peer_consensus(contribution.peer_reviews)

            if consensus["decision"] == "approve":
                await self._approve_contribution(
                    contribution, state,
                    VerificationResult(
                        status="APPROVED",
                        tier_reached=2,
                        confidence=consensus["confidence"],
                        reviewer_comments=[r.comments for r in contribution.peer_reviews]
                    )
                )

            elif consensus["decision"] == "needs_expert":
                await self._escalate_to_tier3(
                    contribution, state,
                    "Peer reviewers requested expert review"
                )

            elif consensus["decision"] == "reject":
                await self._reject_contribution(
                    contribution, state,
                    VerificationResult(
                        status="REJECTED",
                        tier_reached=2,
                        reason=consensus["reason"],
                        reviewer_comments=[r.comments for r in contribution.peer_reviews]
                    )
                )

    def _calculate_peer_consensus(
        self,
        reviews: List[PeerReview]
    ) -> Dict[str, Any]:
        """Calculate consensus from peer reviews"""
        approve_count = sum(1 for r in reviews if r.decision.value == "approve")
        reject_count = sum(1 for r in reviews if r.decision.value == "reject")
        expert_count = sum(1 for r in reviews if r.decision.value == "needs_expert")

        total = len(reviews)
        avg_confidence = sum(float(r.confidence) for r in reviews) / total if total > 0 else 0

        if expert_count > 0:
            return {
                "decision": "needs_expert",
                "confidence": avg_confidence,
                "reason": "Peer reviewer requested expert review"
            }

        if approve_count > reject_count and approve_count >= self.PEER_REVIEW_THRESHOLD:
            return {
                "decision": "approve",
                "confidence": avg_confidence,
                "reason": "Peer consensus: approved"
            }

        if reject_count >= self.PEER_REVIEW_THRESHOLD // 2 + 1:
            return {
                "decision": "reject",
                "confidence": avg_confidence,
                "reason": "Peer consensus: rejected"
            }

        # No clear consensus yet
        return {
            "decision": "pending",
            "confidence": avg_confidence,
            "reason": "Awaiting more reviews"
        }

    async def _escalate_to_tier3(
        self,
        contribution: Contribution,
        state: WorkflowState,
        reason: str
    ):
        """Escalate to Tier 3 expert review"""
        state.current_tier = VerificationTier.EXPERT
        state.status = VerificationStatus.NEEDS_EXPERT
        state.tier_started_at = datetime.now()
        state.escalation_reason = reason

        self._record_transition(
            contribution.contribution_id,
            VerificationStatus.NEEDS_REVIEW,
            VerificationStatus.NEEDS_EXPERT,
            "escalate_to_expert",
            "system",
            reason
        )

        # Request expert review
        if self.expert_review_system:
            await self.expert_review_system.assign_expert(contribution)

        # Fire event
        await self._fire_event("tier3_started", contribution, state)

    async def process_expert_review(
        self,
        contribution_id: str,
        review: ExpertReview
    ):
        """Process a completed expert review"""
        state = self._workflows.get(contribution_id)
        if not state or state.current_tier != VerificationTier.EXPERT:
            return

        contribution = await self._get_contribution(contribution_id)
        if not contribution:
            return

        contribution.expert_review = review

        if review.decision.value == "approve":
            await self._approve_contribution(
                contribution, state,
                VerificationResult(
                    status="APPROVED",
                    tier_reached=3,
                    confidence=review.confidence,
                    expert_assessment=review.assessment
                )
            )

        elif review.decision.value == "reject":
            await self._reject_contribution(
                contribution, state,
                VerificationResult(
                    status="REJECTED",
                    tier_reached=3,
                    reason="Expert rejected contribution",
                    expert_assessment=review.assessment
                )
            )

        elif review.decision.value == "needs_revision":
            # Return to contributor for revision
            state.status = VerificationStatus.PENDING
            state.retry_count += 1

            if state.retry_count >= self.MAX_RETRY_COUNT:
                await self._reject_contribution(
                    contribution, state,
                    VerificationResult(
                        status="REJECTED",
                        tier_reached=3,
                        reason="Maximum revision attempts exceeded"
                    )
                )

    async def _approve_contribution(
        self,
        contribution: Contribution,
        state: WorkflowState,
        result: VerificationResult
    ):
        """Approve and integrate contribution"""
        state.status = VerificationStatus.APPROVED
        contribution.verification_status = VerificationStatus.APPROVED
        contribution.confidence_score = result.confidence
        contribution.resolved_at = datetime.now()
        contribution.resolution = "approved"

        self._record_transition(
            contribution.contribution_id,
            state.status,
            VerificationStatus.APPROVED,
            "approved",
            "system",
            result.notes
        )

        # Integrate into main database
        if self.integration_handler:
            await self.integration_handler.integrate(contribution)

        # Fire events
        await self._fire_event("approved", contribution, state, result)

        # Send to other agents
        await self._notify_agents(contribution, "approved")

    async def _reject_contribution(
        self,
        contribution: Contribution,
        state: WorkflowState,
        result: VerificationResult
    ):
        """Reject contribution"""
        state.status = VerificationStatus.REJECTED
        contribution.verification_status = VerificationStatus.REJECTED
        contribution.resolved_at = datetime.now()
        contribution.resolution = "rejected"
        contribution.resolution_notes = result.reason

        self._record_transition(
            contribution.contribution_id,
            state.status,
            VerificationStatus.REJECTED,
            "rejected",
            "system",
            result.reason
        )

        # Fire event
        await self._fire_event("rejected", contribution, state, result)

    async def _notify_agents(self, contribution: Contribution, event: str):
        """Notify other agents about contribution events"""
        if not self.message_bus:
            return

        # Notify Agent_1 (Data Curator) for verified data
        if contribution.contribution_type in [
            ContributionType.PART_DATA,
            ContributionType.MEASUREMENT,
            ContributionType.CROSS_REFERENCE,
        ]:
            await self.message_bus.publish(GardenerMessage(
                target_agent="Agent_1_Curator",
                topic=GardenerTopics.VERIFIED_CONTRIBUTION,
                message_type="contribution_verified",
                payload={
                    "contribution_id": contribution.contribution_id,
                    "type": contribution.contribution_type.value,
                    "content": contribution.content,
                    "confidence": float(contribution.confidence_score or 0)
                }
            ))

        # Notify Agent_4 (Qualia Collector) for experiences
        if contribution.contribution_type in [
            ContributionType.FAILURE_REPORT,
            ContributionType.APPLICATION_NOTE,
        ]:
            await self.message_bus.publish(GardenerMessage(
                target_agent="Agent_4_Empath",
                topic=GardenerTopics.COMMUNITY_EXPERIENCE,
                message_type="experience_submitted",
                payload={
                    "contribution_id": contribution.contribution_id,
                    "type": contribution.contribution_type.value,
                    "content": contribution.content,
                    "user_id": str(contribution.user_id)
                }
            ))

        # Notify Agent_7 (Chronicler) for tribal knowledge
        if contribution.contribution_type == ContributionType.TRIBAL_KNOWLEDGE:
            await self.message_bus.publish(GardenerMessage(
                target_agent="Agent_7_Chronicler",
                topic=GardenerTopics.TRIBAL_KNOWLEDGE,
                message_type="tribal_knowledge_verified",
                payload={
                    "contribution_id": contribution.contribution_id,
                    "content": contribution.content,
                    "category": contribution.content.get("category"),
                }
            ))

    def _record_transition(
        self,
        contribution_id: str,
        from_status: VerificationStatus,
        to_status: VerificationStatus,
        trigger: str,
        actor: str,
        notes: str = ""
    ):
        """Record a workflow transition"""
        transition = WorkflowTransition(
            from_status=from_status,
            to_status=to_status,
            trigger=trigger,
            actor=actor,
            notes=notes
        )

        if contribution_id not in self._transition_history:
            self._transition_history[contribution_id] = []

        self._transition_history[contribution_id].append(transition)

    def get_workflow_history(self, contribution_id: str) -> List[WorkflowTransition]:
        """Get full workflow history for a contribution"""
        return self._transition_history.get(contribution_id, [])

    async def _fire_event(self, event_name: str, *args, **kwargs):
        """Fire workflow event to registered handlers"""
        handlers = self._event_handlers.get(event_name, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(*args, **kwargs)
                else:
                    handler(*args, **kwargs)
            except Exception:
                pass  # Log error in production

    def on_event(self, event_name: str, handler: Callable):
        """Register event handler"""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    async def _get_contribution(self, contribution_id: str) -> Optional[Contribution]:
        """Get contribution by ID (placeholder for DB lookup)"""
        # In production, fetch from database
        return None

    async def check_timeouts(self):
        """Check for timed-out reviews and escalate if needed"""
        now = datetime.now()

        for contribution_id, state in self._workflows.items():
            if state.status == VerificationStatus.NEEDS_REVIEW:
                elapsed = (now - state.tier_started_at).total_seconds() / 3600
                if elapsed > self.PEER_REVIEW_TIMEOUT_HOURS:
                    # Escalate to expert review
                    contribution = await self._get_contribution(contribution_id)
                    if contribution:
                        await self._escalate_to_tier3(
                            contribution, state,
                            "Peer review timed out"
                        )

            elif state.status == VerificationStatus.NEEDS_EXPERT:
                elapsed = (now - state.tier_started_at).total_seconds() / 3600
                if elapsed > self.EXPERT_REVIEW_TIMEOUT_HOURS:
                    # Flag for admin attention
                    state.metadata["timeout_flagged"] = True
                    await self._fire_event("expert_timeout", contribution_id, state)
