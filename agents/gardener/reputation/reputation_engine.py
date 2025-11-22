"""
Reputation Engine - Core reputation calculation and management

Calculates user reputation scores based on contribution quality,
community engagement, and verification accuracy.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from ..models import (
    CommunityUser,
    ReputationScore,
    ReputationLevel,
    PointAward,
    GardenerMessage,
    GardenerTopics,
)


@dataclass
class ReputationConfig:
    """Configuration for reputation calculations"""
    # Decay settings
    decay_start_days: int = 30  # Start decay after 30 days inactive
    decay_rate_per_day: float = 0.01  # 1% per day after threshold
    min_decay_factor: float = 0.5  # Never decay below 50%

    # Activity boost settings
    max_activity_boost: float = 0.20  # Max 20% boost
    activity_boost_per_contribution: float = 0.01  # 1% per contribution in last 30 days

    # Category expertise threshold
    expertise_threshold: int = 50  # Contributions needed for expertise


class ReputationEngine:
    """
    Core reputation calculation engine.

    Calculates effective reputation considering:
    - Lifetime points earned
    - Activity decay for inactivity
    - Recent activity boost
    - Category expertise multipliers
    """

    REPUTATION_LEVELS = {
        0: {"name": "Newcomer", "min_points": 0, "permissions": ["submit"]},
        1: {"name": "Contributor", "min_points": 100, "permissions": ["submit", "comment"]},
        2: {"name": "Trusted", "min_points": 500, "permissions": ["submit", "comment", "peer_review"]},
        3: {"name": "Expert", "min_points": 2000, "permissions": ["submit", "comment", "peer_review", "edit"]},
        4: {"name": "Master", "min_points": 10000, "permissions": ["submit", "comment", "peer_review", "edit", "expert_review"]},
        5: {"name": "Elder", "min_points": 50000, "permissions": ["all", "moderate", "ban"]}
    }

    POINT_AWARDS = {
        # Contribution Points
        "part_submission_approved": 10,
        "measurement_verified": 5,
        "failure_report_useful": 15,
        "correction_accepted": 20,
        "photo_contribution": 5,
        "cad_model_contribution": 30,

        # Review Points
        "peer_review_completed": 3,
        "expert_review_completed": 10,
        "review_consensus_correct": 5,

        # Community Points
        "helpful_comment": 2,
        "question_answered": 5,
        "guide_written": 50,

        # Quality Bonuses
        "streak_bonus_7_days": 50,
        "streak_bonus_30_days": 200,
        "first_in_category": 100,
        "data_improved_accuracy": 25
    }

    POINT_PENALTIES = {
        "submission_rejected_poor_quality": -5,
        "submission_rejected_spam": -50,
        "review_incorrect": -10,
        "community_report_upheld": -100,
        "ban_issued": -1000
    }

    def __init__(
        self,
        db_connection=None,
        config: ReputationConfig = None,
        message_bus=None
    ):
        self.db = db_connection
        self.config = config or ReputationConfig()
        self.message_bus = message_bus

        # Cache for performance
        self._reputation_cache: Dict[UUID, Tuple[ReputationScore, datetime]] = {}
        self._cache_ttl = timedelta(minutes=5)

    def calculate_reputation(self, user: CommunityUser) -> ReputationScore:
        """
        Calculate current reputation score for a user.

        Considers lifetime points, activity decay, and boosts.

        Args:
            user: The user to calculate reputation for

        Returns:
            ReputationScore with detailed breakdown
        """
        # Check cache
        cached = self._get_cached_reputation(user.id)
        if cached:
            return cached

        base_score = user.lifetime_points

        # Calculate decay factor
        decay_factor = self._calculate_decay_factor(user)

        # Calculate activity boost
        activity_boost = self._calculate_activity_boost(user)

        # Calculate effective score
        effective_score = base_score * decay_factor * (1 + activity_boost)

        # Determine level
        level = self._determine_level(effective_score)

        # Calculate rank (would query DB in production)
        rank = self._calculate_rank(user.id, effective_score)

        # Progress to next level
        progress = self._progress_to_next_level(effective_score, level)

        # Get permissions for level
        level_info = self.REPUTATION_LEVELS.get(level.level, self.REPUTATION_LEVELS[0])
        permissions = level_info["permissions"]

        reputation = ReputationScore(
            lifetime_points=base_score,
            effective_points=effective_score,
            level=level,
            rank=rank,
            next_level_progress=progress,
            permissions=permissions
        )

        # Cache result
        self._cache_reputation(user.id, reputation)

        return reputation

    def _calculate_decay_factor(self, user: CommunityUser) -> float:
        """Calculate reputation decay for inactivity"""
        if not user.last_contribution:
            return self.config.min_decay_factor

        days_inactive = (datetime.now() - user.last_contribution).days

        if days_inactive <= self.config.decay_start_days:
            return 1.0

        # Calculate decay
        decay_days = days_inactive - self.config.decay_start_days
        decay = 1 - (decay_days * self.config.decay_rate_per_day)

        return max(self.config.min_decay_factor, decay)

    def _calculate_activity_boost(self, user: CommunityUser) -> float:
        """Calculate activity boost from recent contributions"""
        # In production, query recent contribution count from DB
        recent_count = self._count_recent_contributions(user, days=30)

        boost = recent_count * self.config.activity_boost_per_contribution
        return min(self.config.max_activity_boost, boost)

    def _count_recent_contributions(self, user: CommunityUser, days: int) -> int:
        """Count contributions in the last N days"""
        # Placeholder - would query DB in production
        return user.streak_days  # Use streak as approximation

    def _determine_level(self, effective_score: float) -> ReputationLevel:
        """Determine reputation level from score"""
        current_level = ReputationLevel.NEWCOMER

        for level in ReputationLevel:
            if effective_score >= level.min_points:
                current_level = level

        return current_level

    def _calculate_rank(self, user_id: UUID, effective_score: float) -> int:
        """Calculate user's rank among all users"""
        # Placeholder - would query DB for rank
        return 0

    def _progress_to_next_level(
        self,
        effective_score: float,
        current_level: ReputationLevel
    ) -> float:
        """Calculate progress towards next level (0-1)"""
        # Find next level
        next_level = None
        for level in ReputationLevel:
            if level.level == current_level.level + 1:
                next_level = level
                break

        if not next_level:
            return 1.0  # Max level

        current_min = current_level.min_points
        next_min = next_level.min_points

        points_in_level = effective_score - current_min
        points_needed = next_min - current_min

        return min(1.0, points_in_level / points_needed)

    def award_points(
        self,
        user: CommunityUser,
        action: str,
        context: Optional[Dict[str, Any]] = None
    ) -> PointAward:
        """
        Award points for a user action.

        Args:
            user: The user to award points to
            action: The action being rewarded (from POINT_AWARDS)
            context: Optional context for multipliers

        Returns:
            PointAward with details of the award
        """
        context = context or {}
        base_points = self.POINT_AWARDS.get(action, 0)

        if base_points == 0 and action in self.POINT_PENALTIES:
            base_points = self.POINT_PENALTIES[action]

        # Calculate multiplier
        multiplier = self._calculate_multiplier(user, action, context)

        # Calculate final points
        final_points = int(base_points * multiplier)

        # Check for level up before applying
        old_reputation = self.calculate_reputation(user)

        # Update user
        user.lifetime_points = max(0, user.lifetime_points + final_points)
        user.last_contribution = datetime.now()

        # Clear cache
        self._invalidate_cache(user.id)

        # Check for level up
        new_reputation = self.calculate_reputation(user)
        if new_reputation.level.level > old_reputation.level.level:
            self._handle_level_up(user, old_reputation.level, new_reputation.level)

        award = PointAward(
            user_id=user.id,
            action=action,
            base_points=base_points,
            multiplier=multiplier,
            final_points=final_points,
            new_total=user.lifetime_points,
            context=context
        )

        # Persist award
        self._save_point_award(award)

        return award

    def _calculate_multiplier(
        self,
        user: CommunityUser,
        action: str,
        context: Dict[str, Any]
    ) -> float:
        """Calculate point multiplier based on context"""
        multiplier = 1.0

        # Category expertise bonus
        category = context.get("category")
        if category and category in user.expertise_categories:
            multiplier *= 1.5

        # Quality score bonus
        quality = context.get("quality_score", 0)
        if quality > 0.9:
            multiplier *= 1.25
        elif quality > 0.8:
            multiplier *= 1.1

        # Verification count bonus
        verifications = context.get("verification_count", 0)
        if verifications > 3:
            multiplier *= 1.1

        # First contribution in category bonus
        if context.get("first_in_category"):
            multiplier *= 2.0

        return multiplier

    def apply_penalty(
        self,
        user: CommunityUser,
        action: str,
        reason: str = ""
    ) -> PointAward:
        """
        Apply a point penalty to a user.

        Args:
            user: The user to penalize
            action: The penalty action
            reason: Reason for penalty

        Returns:
            PointAward (with negative points)
        """
        return self.award_points(user, action, {"reason": reason})

    async def _handle_level_up(
        self,
        user: CommunityUser,
        old_level: ReputationLevel,
        new_level: ReputationLevel
    ):
        """Handle user level up event"""
        # Update user permissions
        level_info = self.REPUTATION_LEVELS.get(new_level.level, {})
        user.permissions = level_info.get("permissions", ["submit"])
        user.current_level = new_level.level

        # Send notification via message bus
        if self.message_bus:
            await self.message_bus.publish(GardenerMessage(
                topic=GardenerTopics.USER_LEVEL_UP,
                message_type="level_up",
                payload={
                    "user_id": str(user.id),
                    "old_level": old_level.name,
                    "new_level": new_level.name,
                    "new_permissions": user.permissions
                }
            ))

    def update_expertise(self, user: CommunityUser, category: str, count: int):
        """Update category expertise based on contribution count"""
        if count >= self.config.expertise_threshold:
            if category not in user.expertise_categories:
                user.expertise_categories.append(category)

    def _get_cached_reputation(self, user_id: UUID) -> Optional[ReputationScore]:
        """Get cached reputation if valid"""
        if user_id in self._reputation_cache:
            reputation, cached_at = self._reputation_cache[user_id]
            if datetime.now() - cached_at < self._cache_ttl:
                return reputation
        return None

    def _cache_reputation(self, user_id: UUID, reputation: ReputationScore):
        """Cache reputation score"""
        self._reputation_cache[user_id] = (reputation, datetime.now())

    def _invalidate_cache(self, user_id: UUID):
        """Invalidate cached reputation for user"""
        if user_id in self._reputation_cache:
            del self._reputation_cache[user_id]

    def _save_point_award(self, award: PointAward):
        """Save point award to database"""
        # In production, persist to database
        pass

    def get_point_history(
        self,
        user_id: UUID,
        limit: int = 50
    ) -> List[PointAward]:
        """Get point award history for a user"""
        # In production, query from database
        return []

    def recalculate_all_reputations(self):
        """Recalculate all user reputations (for maintenance)"""
        # Clear cache
        self._reputation_cache.clear()
        # In production, batch recalculate from DB

    def get_leaderboard(
        self,
        limit: int = 100,
        category: Optional[str] = None
    ) -> List[Tuple[CommunityUser, ReputationScore]]:
        """Get top users by reputation"""
        # In production, query DB ordered by effective points
        return []
