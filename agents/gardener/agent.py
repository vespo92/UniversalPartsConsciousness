"""
Agent_8: Community Cultivator (GARDENER)

The main orchestrator for the Gardener agent, bridging human expertise
with machine learning through community contributions.

"Data comes from sensors. Wisdom comes from humans. I cultivate the garden
where engineers share their knowledge, and the machine learns from the masters."
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID

from .models import (
    Contribution,
    ContributionType,
    CommunityUser,
    VerificationStatus,
    GardenerMessage,
    GardenerTopics,
    PeerReview,
    ExpertReview,
    ReviewDecision,
)

from .contributions import (
    ContributionHandler,
    WorkflowEngine,
    IntegrationHandler,
)

from .verification import (
    AutoVerifier,
    PeerReviewSystem,
    ExpertReviewSystem,
)

from .reputation import ReputationEngine

from .gamification import (
    AchievementSystem,
    LeaderboardSystem,
)

from .analytics import AnalyticsDashboard


@dataclass
class GardenerConfig:
    """Configuration for the Gardener agent"""
    # Verification settings
    auto_approve_trusted_users: bool = True
    trusted_user_threshold: int = 2000  # Points needed
    require_peer_review_for_new_users: bool = True
    new_user_threshold: int = 100  # Points threshold

    # Workflow settings
    peer_review_timeout_hours: int = 48
    expert_review_timeout_hours: int = 72
    max_pending_reviews_per_user: int = 5

    # Gamification settings
    enable_achievements: bool = True
    enable_leaderboards: bool = True

    # Integration settings
    notify_other_agents: bool = True


class GardenerAgent:
    """
    Agent_8: Community Cultivator (GARDENER)

    Main orchestrator that coordinates all community cultivation subsystems:
    - Contribution submission and validation
    - 3-tier verification workflow
    - Reputation and point management
    - Gamification (achievements, challenges, leaderboards)
    - Expert panel management
    - Inter-agent communication

    Integration Points:
    - Receives: Content needing community review (from all agents)
    - Sends to Agent_1 (Curator): Verified contributions → data
    - Sends to Agent_4 (Empath): Community experiences → qualia
    - Sends to Agent_7 (Chronicler): Tribal knowledge → history
    """

    AGENT_ID = "Agent_8"
    AGENT_NAME = "Community Cultivator"
    AGENT_ALIAS = "GARDENER"

    def __init__(
        self,
        config: GardenerConfig = None,
        db_connection=None,
        message_bus=None,
        notification_service=None
    ):
        self.config = config or GardenerConfig()
        self.db = db_connection
        self.message_bus = message_bus
        self.notifications = notification_service

        # Initialize subsystems
        self._init_subsystems()

        # Register event handlers
        self._setup_event_handlers()

        # Agent state
        self._running = False
        self._background_tasks: List[asyncio.Task] = []

    def _init_subsystems(self):
        """Initialize all subsystems"""
        # Core systems
        self.contribution_handler = ContributionHandler(
            db_connection=self.db,
            message_bus=self.message_bus
        )

        self.auto_verifier = AutoVerifier(
            db_connection=self.db
        )

        self.peer_review_system = PeerReviewSystem(
            db_connection=self.db,
            notification_service=self.notifications
        )

        self.expert_review_system = ExpertReviewSystem(
            db_connection=self.db,
            notification_service=self.notifications
        )

        self.integration_handler = IntegrationHandler(
            db_connection=self.db,
            message_bus=self.message_bus
        )

        self.workflow_engine = WorkflowEngine(
            auto_verifier=self.auto_verifier,
            peer_review_system=self.peer_review_system,
            expert_review_system=self.expert_review_system,
            integration_handler=self.integration_handler,
            message_bus=self.message_bus
        )

        # Reputation and gamification
        self.reputation_engine = ReputationEngine(
            db_connection=self.db,
            message_bus=self.message_bus
        )

        self.achievement_system = AchievementSystem(
            db_connection=self.db,
            reputation_engine=self.reputation_engine,
            message_bus=self.message_bus
        )

        self.leaderboard_system = LeaderboardSystem(
            db_connection=self.db,
            reputation_engine=self.reputation_engine
        )

        # Analytics
        self.analytics = AnalyticsDashboard(
            db_connection=self.db
        )

    def _setup_event_handlers(self):
        """Setup event handlers for workflow events"""
        # Workflow events
        self.workflow_engine.on_event("approved", self._on_contribution_approved)
        self.workflow_engine.on_event("rejected", self._on_contribution_rejected)
        self.workflow_engine.on_event("tier2_started", self._on_peer_review_started)
        self.workflow_engine.on_event("tier3_started", self._on_expert_review_started)

    async def start(self):
        """Start the Gardener agent"""
        self._running = True

        # Start background tasks
        self._background_tasks.append(
            asyncio.create_task(self._timeout_check_loop())
        )
        self._background_tasks.append(
            asyncio.create_task(self._leaderboard_update_loop())
        )

        # Subscribe to message bus
        if self.message_bus:
            await self.message_bus.subscribe(
                GardenerTopics.REVIEW_REQUEST,
                self._handle_review_request
            )

    async def stop(self):
        """Stop the Gardener agent"""
        self._running = False

        # Cancel background tasks
        for task in self._background_tasks:
            task.cancel()

        await asyncio.gather(*self._background_tasks, return_exceptions=True)
        self._background_tasks.clear()

    # =========================================================================
    # Public API - Contribution Management
    # =========================================================================

    async def submit_contribution(
        self,
        user: CommunityUser,
        contribution_type: ContributionType,
        content: Dict[str, Any],
        target_part_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Submit a new contribution from a community member.

        Args:
            user: The submitting user
            contribution_type: Type of contribution
            content: Contribution content/data
            target_part_id: Optional target part UUID

        Returns:
            Result dict with contribution details and status
        """
        # Submit via handler
        result = self.contribution_handler.submit_contribution(
            user=user,
            contribution_type=contribution_type,
            content=content,
            target_part_id=target_part_id
        )

        if not result.success:
            return {
                "success": False,
                "errors": result.errors
            }

        # Start verification workflow
        await self.workflow_engine.start_workflow(result.contribution)

        return {
            "success": True,
            "contribution_id": result.contribution_id,
            "status": "submitted",
            "next_steps": result.next_steps
        }

    async def submit_peer_review(
        self,
        contribution_id: str,
        reviewer_id: UUID,
        decision: str,
        confidence: float,
        comments: str = "",
        corrections: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Submit a peer review for a contribution"""
        try:
            review_decision = ReviewDecision(decision)
        except ValueError:
            return {"success": False, "error": f"Invalid decision: {decision}"}

        review = await self.peer_review_system.submit_review(
            contribution_id=contribution_id,
            reviewer_id=reviewer_id,
            decision=review_decision,
            confidence=confidence,
            comments=comments,
            corrections=corrections
        )

        # Award review points
        reviewer = await self._get_user(reviewer_id)
        if reviewer:
            self.reputation_engine.award_points(
                reviewer,
                "peer_review_completed",
                {"contribution_id": contribution_id}
            )

        # Process in workflow
        await self.workflow_engine.process_peer_review(contribution_id, review)

        return {
            "success": True,
            "review_id": str(review.id)
        }

    async def submit_expert_review(
        self,
        contribution_id: str,
        expert_id: UUID,
        decision: str,
        assessment: str,
        confidence: float,
        conditions: List[str] = None
    ) -> Dict[str, Any]:
        """Submit an expert review for a contribution"""
        try:
            review_decision = ReviewDecision(decision)
        except ValueError:
            return {"success": False, "error": f"Invalid decision: {decision}"}

        review = await self.expert_review_system.submit_review(
            contribution_id=contribution_id,
            expert_id=expert_id,
            decision=review_decision,
            assessment=assessment,
            confidence=confidence,
            conditions=conditions
        )

        # Award review points
        expert = await self._get_user(expert_id)
        if expert:
            self.reputation_engine.award_points(
                expert,
                "expert_review_completed",
                {"contribution_id": contribution_id}
            )

        # Process in workflow
        await self.workflow_engine.process_expert_review(contribution_id, review)

        return {
            "success": True,
            "review_id": str(review.id)
        }

    # =========================================================================
    # Public API - User Management
    # =========================================================================

    async def get_user_profile(self, user_id: UUID) -> Dict[str, Any]:
        """Get complete user profile with reputation and stats"""
        user = await self._get_user(user_id)
        if not user:
            return {"error": "User not found"}

        reputation = self.reputation_engine.calculate_reputation(user)
        achievements = self.achievement_system.get_user_progress(user)

        return {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "display_name": user.display_name,
                "joined_at": user.joined_at.isoformat(),
                "status": user.status.value,
            },
            "reputation": {
                "lifetime_points": reputation.lifetime_points,
                "effective_points": reputation.effective_points,
                "level": reputation.level.name,
                "rank": reputation.rank,
                "next_level_progress": reputation.next_level_progress,
                "permissions": reputation.permissions,
            },
            "stats": {
                "contribution_count": user.contribution_count,
                "approved_count": user.approved_count,
                "accuracy_rate": float(user.accuracy_rate),
                "review_count": user.review_count,
                "streak_days": user.streak_days,
            },
            "expertise": {
                "categories": user.expertise_categories,
                "expert_domains": user.expert_domains,
            },
            "achievements": [
                {
                    "id": a.achievement.id,
                    "name": a.achievement.name,
                    "unlocked": a.unlocked,
                    "progress_pct": a.progress_pct,
                }
                for a in achievements[:10]  # Top 10
            ],
        }

    async def get_user_contributions(
        self,
        user_id: UUID,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get contributions by a user"""
        status_filter = None
        if status:
            try:
                status_filter = VerificationStatus(status)
            except ValueError:
                pass

        contributions = self.contribution_handler.get_user_contributions(
            user_id=user_id,
            status=status_filter,
            limit=limit
        )

        return [
            {
                "id": str(c.id),
                "contribution_id": c.contribution_id,
                "type": c.contribution_type.value,
                "status": c.verification_status.value,
                "submitted_at": c.submitted_at.isoformat(),
                "confidence_score": float(c.confidence_score) if c.confidence_score else None,
            }
            for c in contributions
        ]

    async def get_pending_reviews(self, user_id: UUID) -> Dict[str, Any]:
        """Get pending reviews assigned to a user"""
        peer_reviews = await self.peer_review_system.get_reviewer_queue(user_id)

        return {
            "peer_reviews": [
                {
                    "contribution_id": r.contribution_id,
                    "type": r.contribution.contribution_type.value,
                    "deadline": r.deadline.isoformat(),
                    "priority": r.priority,
                }
                for r in peer_reviews
            ],
            "count": len(peer_reviews),
        }

    # =========================================================================
    # Public API - Gamification
    # =========================================================================

    async def get_leaderboard(
        self,
        leaderboard_type: str = "all_time",
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get leaderboard rankings"""
        leaderboard = await self.leaderboard_system.get_leaderboard(
            leaderboard_type=leaderboard_type,
            category=category
        )

        return {
            "type": leaderboard.leaderboard_type,
            "category": leaderboard.category,
            "generated_at": leaderboard.generated_at.isoformat(),
            "entries": [
                {
                    "rank": e.rank,
                    "username": e.username,
                    "display_name": e.display_name,
                    "points": e.points,
                    "level": e.level,
                    "badges": e.badges,
                }
                for e in leaderboard.entries
            ],
        }

    async def get_achievements(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get user's achievements and progress"""
        user = await self._get_user(user_id)
        if not user:
            return []

        progress = self.achievement_system.get_user_progress(user)

        return [
            {
                "id": a.achievement.id,
                "name": a.achievement.name,
                "description": a.achievement.description,
                "badge": a.achievement.badge,
                "points": a.achievement.points,
                "category": a.achievement.category,
                "current": a.current,
                "target": a.target,
                "progress_pct": a.progress_pct,
                "unlocked": a.unlocked,
            }
            for a in progress
        ]

    # =========================================================================
    # Public API - Analytics
    # =========================================================================

    async def get_community_metrics(self) -> Dict[str, Any]:
        """Get community health metrics"""
        metrics = await self.analytics.get_community_metrics()

        return {
            "users": {
                "total": metrics.total_users,
                "active_30d": metrics.active_users_30d,
                "active_7d": metrics.active_users_7d,
                "new_30d": metrics.new_users_30d,
            },
            "contributions": {
                "total": metrics.total_contributions,
                "last_30d": metrics.contributions_30d,
                "last_7d": metrics.contributions_7d,
                "approval_rate": metrics.approval_rate,
                "avg_verification_hours": metrics.avg_verification_time_hours,
            },
            "reviews": {
                "pending_peer": metrics.pending_peer_reviews,
                "pending_expert": metrics.pending_expert_reviews,
            },
            "experts": {
                "active": metrics.active_experts,
                "capacity_pct": metrics.expert_capacity_pct,
            },
            "generated_at": metrics.generated_at.isoformat(),
        }

    # =========================================================================
    # Event Handlers
    # =========================================================================

    async def _on_contribution_approved(
        self,
        contribution: Contribution,
        state,
        result
    ):
        """Handle contribution approval"""
        # Get contributor
        user = await self._get_user(contribution.user_id)
        if not user:
            return

        # Award points based on contribution type
        action = self._get_point_action(contribution.contribution_type)
        context = {
            "contribution_id": contribution.contribution_id,
            "quality_score": float(contribution.confidence_score or 0),
            "category": contribution.content.get("category"),
        }

        self.reputation_engine.award_points(user, action, context)

        # Check for achievements
        if self.config.enable_achievements:
            await self.achievement_system.check_achievements(
                user,
                trigger_event="contribution_approved",
                context=context
            )

        # Update leaderboards
        if self.config.enable_leaderboards:
            self.leaderboard_system.invalidate_cache()

    async def _on_contribution_rejected(
        self,
        contribution: Contribution,
        state,
        result
    ):
        """Handle contribution rejection"""
        user = await self._get_user(contribution.user_id)
        if not user:
            return

        # Apply penalty for poor quality (not spam)
        if "spam" not in result.reason.lower():
            self.reputation_engine.apply_penalty(
                user,
                "submission_rejected_poor_quality",
                result.reason
            )
        else:
            self.reputation_engine.apply_penalty(
                user,
                "submission_rejected_spam",
                result.reason
            )

    async def _on_peer_review_started(self, contribution: Contribution, state):
        """Handle peer review stage start"""
        pass  # Logging/metrics

    async def _on_expert_review_started(self, contribution: Contribution, state):
        """Handle expert review stage start"""
        pass  # Logging/metrics

    async def _handle_review_request(self, message: GardenerMessage):
        """Handle incoming review requests from other agents"""
        # Process review request from message bus
        pass

    # =========================================================================
    # Background Tasks
    # =========================================================================

    async def _timeout_check_loop(self):
        """Periodically check for timed out reviews"""
        while self._running:
            try:
                await self.workflow_engine.check_timeouts()
                await self.peer_review_system.check_timeouts()
                await self.expert_review_system.process_pending_queue()
            except Exception:
                pass  # Log error

            await asyncio.sleep(300)  # Every 5 minutes

    async def _leaderboard_update_loop(self):
        """Periodically snapshot leaderboards"""
        while self._running:
            try:
                await self.leaderboard_system.record_leaderboard_snapshot()
            except Exception:
                pass  # Log error

            await asyncio.sleep(3600)  # Every hour

    # =========================================================================
    # Helpers
    # =========================================================================

    def _get_point_action(self, contribution_type: ContributionType) -> str:
        """Map contribution type to point action"""
        action_map = {
            ContributionType.PART_DATA: "part_submission_approved",
            ContributionType.MEASUREMENT: "measurement_verified",
            ContributionType.FAILURE_REPORT: "failure_report_useful",
            ContributionType.CORRECTION: "correction_accepted",
            ContributionType.PHOTO: "photo_contribution",
            ContributionType.CAD_MODEL: "cad_model_contribution",
        }
        return action_map.get(contribution_type, "part_submission_approved")

    async def _get_user(self, user_id: UUID) -> Optional[CommunityUser]:
        """Get user by ID (placeholder for DB lookup)"""
        # In production, query database
        return None

    # =========================================================================
    # Agent Info
    # =========================================================================

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information and status"""
        return {
            "id": self.AGENT_ID,
            "name": self.AGENT_NAME,
            "alias": self.AGENT_ALIAS,
            "running": self._running,
            "mission": (
                "Bridge the gap between human expertise and machine learning. "
                "Cultivate the community that provides invaluable real-world knowledge, "
                "verifies accuracy, and enriches the collective consciousness."
            ),
            "capabilities": [
                "Contribution submission and validation",
                "3-tier verification workflow (Auto, Peer, Expert)",
                "Reputation and point management",
                "Achievement and gamification system",
                "Expert panel management",
                "Community analytics",
            ],
            "integrations": {
                "receives_from": ["All Agents - Content needing review"],
                "sends_to": [
                    "Agent_1 (Curator) - Verified contributions",
                    "Agent_4 (Empath) - Community experiences",
                    "Agent_7 (Chronicler) - Tribal knowledge",
                ],
            },
        }


# Convenience function to create configured agent
def create_gardener_agent(
    db_connection=None,
    message_bus=None,
    notification_service=None,
    **config_kwargs
) -> GardenerAgent:
    """Create a configured Gardener agent instance"""
    config = GardenerConfig(**config_kwargs)
    return GardenerAgent(
        config=config,
        db_connection=db_connection,
        message_bus=message_bus,
        notification_service=notification_service
    )
