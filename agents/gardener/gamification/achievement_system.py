"""
Achievement System - Tracks and awards user achievements

Manages the achievement and badge system to incentivize quality contributions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID

from ..models import (
    Achievement,
    UserAchievement,
    CommunityUser,
    ContributionType,
    GardenerMessage,
    GardenerTopics,
)


@dataclass
class AchievementProgress:
    """Progress towards an achievement"""
    achievement: Achievement
    current: int
    target: int
    progress_pct: float
    unlocked: bool


class AchievementSystem:
    """
    Achievement and badge system.

    Tracks user progress towards achievements and awards
    badges when milestones are reached.
    """

    # Achievement definitions
    ACHIEVEMENTS = {
        # Contribution Achievements
        "first_contribution": Achievement(
            id="first_contribution",
            name="First Step",
            description="Submit your first contribution",
            points=10,
            badge="first_step",
            category="contribution",
            requirement={"type": "contribution_count", "value": 1}
        ),
        "ten_contributions": Achievement(
            id="ten_contributions",
            name="Getting Started",
            description="Submit 10 approved contributions",
            points=50,
            badge="getting_started",
            category="contribution",
            requirement={"type": "approved_count", "value": 10}
        ),
        "hundred_contributions": Achievement(
            id="hundred_contributions",
            name="Century",
            description="Submit 100 approved contributions",
            points=500,
            badge="century",
            category="contribution",
            requirement={"type": "approved_count", "value": 100}
        ),
        "thousand_contributions": Achievement(
            id="thousand_contributions",
            name="Prolific Contributor",
            description="Submit 1000 approved contributions",
            points=2000,
            badge="prolific",
            category="contribution",
            requirement={"type": "approved_count", "value": 1000}
        ),

        # Streak Achievements
        "perfect_streak_7": Achievement(
            id="perfect_streak_7",
            name="Lucky Seven",
            description="7 consecutive approved contributions",
            points=100,
            badge="lucky_seven",
            category="streak",
            requirement={"type": "approval_streak", "value": 7}
        ),
        "perfect_streak_30": Achievement(
            id="perfect_streak_30",
            name="Unstoppable",
            description="30 consecutive approved contributions",
            points=500,
            badge="unstoppable",
            category="streak",
            requirement={"type": "approval_streak", "value": 30}
        ),
        "daily_streak_7": Achievement(
            id="daily_streak_7",
            name="Week Warrior",
            description="Contribute 7 days in a row",
            points=50,
            badge="week_warrior",
            category="streak",
            requirement={"type": "daily_streak", "value": 7}
        ),
        "daily_streak_30": Achievement(
            id="daily_streak_30",
            name="Monthly Dedication",
            description="Contribute 30 days in a row",
            points=200,
            badge="monthly_dedication",
            category="streak",
            requirement={"type": "daily_streak", "value": 30}
        ),

        # Expertise Achievements
        "fastener_expert": Achievement(
            id="fastener_expert",
            name="Fastener Master",
            description="100 approved fastener contributions",
            points=300,
            badge="fastener_master",
            category="expertise",
            requirement={"type": "category_count", "category": "fasteners", "value": 100}
        ),
        "bearing_expert": Achievement(
            id="bearing_expert",
            name="Bearing Specialist",
            description="100 approved bearing contributions",
            points=300,
            badge="bearing_specialist",
            category="expertise",
            requirement={"type": "category_count", "category": "bearings", "value": 100}
        ),
        "automotive_historian": Achievement(
            id="automotive_historian",
            name="Automotive Historian",
            description="50 automotive history contributions",
            points=400,
            badge="historian",
            category="expertise",
            requirement={"type": "category_count", "category": "automotive", "value": 50}
        ),
        "measurement_guru": Achievement(
            id="measurement_guru",
            name="Measurement Guru",
            description="200 verified measurements",
            points=300,
            badge="measurement_guru",
            category="expertise",
            requirement={"type": "contribution_type_count", "contribution_type": "measurement", "value": 200}
        ),

        # Community Achievements
        "helpful_reviewer": Achievement(
            id="helpful_reviewer",
            name="Helpful Eye",
            description="Complete 50 peer reviews",
            points=200,
            badge="helpful_eye",
            category="community",
            requirement={"type": "review_count", "value": 50}
        ),
        "review_champion": Achievement(
            id="review_champion",
            name="Review Champion",
            description="Complete 500 peer reviews",
            points=1000,
            badge="review_champion",
            category="community",
            requirement={"type": "review_count", "value": 500}
        ),
        "mentor": Achievement(
            id="mentor",
            name="Mentor",
            description="Help 10 newcomers get their first contribution approved",
            points=500,
            badge="mentor",
            category="community",
            requirement={"type": "mentored_users", "value": 10}
        ),
        "myth_buster": Achievement(
            id="myth_buster",
            name="Myth Buster",
            description="Correct 25 pieces of misinformation",
            points=400,
            badge="myth_buster",
            category="community",
            requirement={"type": "corrections_accepted", "value": 25}
        ),

        # Special Achievements
        "legendary_find": Achievement(
            id="legendary_find",
            name="Legendary Find",
            description="Document a previously unknown part",
            points=1000,
            badge="legendary_find",
            category="special",
            requirement={"type": "new_part_documented", "value": 1}
        ),
        "failure_prophet": Achievement(
            id="failure_prophet",
            name="Failure Prophet",
            description="Report a failure mode that gets documented",
            points=750,
            badge="failure_prophet",
            category="special",
            requirement={"type": "failure_documented", "value": 1}
        ),
        "data_savior": Achievement(
            id="data_savior",
            name="Data Savior",
            description="Improve accuracy of 100 part records",
            points=800,
            badge="data_savior",
            category="special",
            requirement={"type": "accuracy_improvements", "value": 100}
        ),
        "tribal_elder": Achievement(
            id="tribal_elder",
            name="Tribal Elder",
            description="Contribute 50 pieces of tribal knowledge",
            points=600,
            badge="tribal_elder",
            category="special",
            requirement={"type": "tribal_knowledge_count", "value": 50}
        ),

        # Reputation Achievements
        "trusted_status": Achievement(
            id="trusted_status",
            name="Trusted Member",
            description="Reach Trusted reputation level",
            points=100,
            badge="trusted",
            category="reputation",
            requirement={"type": "reputation_level", "value": 2}
        ),
        "expert_status": Achievement(
            id="expert_status",
            name="Expert Status",
            description="Reach Expert reputation level",
            points=200,
            badge="expert_badge",
            category="reputation",
            requirement={"type": "reputation_level", "value": 3}
        ),
        "master_status": Achievement(
            id="master_status",
            name="Master Status",
            description="Reach Master reputation level",
            points=500,
            badge="master_badge",
            category="reputation",
            requirement={"type": "reputation_level", "value": 4}
        ),
        "elder_status": Achievement(
            id="elder_status",
            name="Elder Status",
            description="Reach Elder reputation level",
            points=1000,
            badge="elder_badge",
            category="reputation",
            requirement={"type": "reputation_level", "value": 5}
        ),
    }

    def __init__(
        self,
        db_connection=None,
        reputation_engine=None,
        message_bus=None
    ):
        self.db = db_connection
        self.reputation_engine = reputation_engine
        self.message_bus = message_bus

        # User achievement cache
        self._user_achievements: Dict[UUID, List[str]] = {}

        # Progress trackers
        self._progress_trackers: Dict[str, Callable] = {
            "contribution_count": self._track_contribution_count,
            "approved_count": self._track_approved_count,
            "approval_streak": self._track_approval_streak,
            "daily_streak": self._track_daily_streak,
            "category_count": self._track_category_count,
            "contribution_type_count": self._track_type_count,
            "review_count": self._track_review_count,
            "mentored_users": self._track_mentored_users,
            "corrections_accepted": self._track_corrections,
            "reputation_level": self._track_reputation_level,
            "new_part_documented": self._track_new_parts,
            "failure_documented": self._track_failure_reports,
            "accuracy_improvements": self._track_accuracy_improvements,
            "tribal_knowledge_count": self._track_tribal_knowledge,
        }

    async def check_achievements(
        self,
        user: CommunityUser,
        trigger_event: str = None,
        context: Dict[str, Any] = None
    ) -> List[UserAchievement]:
        """
        Check and award any new achievements for a user.

        Args:
            user: The user to check
            trigger_event: Optional event that triggered the check
            context: Optional context data

        Returns:
            List of newly unlocked achievements
        """
        context = context or {}
        newly_unlocked = []

        # Get user's current achievements
        current = await self._get_user_achievements(user.id)
        current_ids = {a.achievement_id for a in current}

        # Check each achievement
        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            # Skip if already earned
            if achievement_id in current_ids:
                continue

            # Check if earned
            if await self._check_achievement_earned(user, achievement, context):
                # Award achievement
                user_achievement = await self._award_achievement(user, achievement)
                newly_unlocked.append(user_achievement)

        return newly_unlocked

    async def _check_achievement_earned(
        self,
        user: CommunityUser,
        achievement: Achievement,
        context: Dict[str, Any]
    ) -> bool:
        """Check if user has earned an achievement"""
        requirement = achievement.requirement
        req_type = requirement.get("type")
        target_value = requirement.get("value", 0)

        # Get tracker for requirement type
        tracker = self._progress_trackers.get(req_type)
        if not tracker:
            return False

        # Get current progress
        current_value = await tracker(user, requirement, context)

        return current_value >= target_value

    async def _award_achievement(
        self,
        user: CommunityUser,
        achievement: Achievement
    ) -> UserAchievement:
        """Award an achievement to a user"""
        user_achievement = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id,
            points_awarded=achievement.points
        )

        # Award reputation points
        if self.reputation_engine:
            self.reputation_engine.award_points(
                user,
                "achievement_earned",
                {"achievement": achievement.id, "points": achievement.points}
            )

        # Update cache
        if user.id not in self._user_achievements:
            self._user_achievements[user.id] = []
        self._user_achievements[user.id].append(achievement.id)

        # Persist to database
        await self._save_user_achievement(user_achievement)

        # Send notification
        await self._notify_achievement(user, achievement)

        return user_achievement

    async def _notify_achievement(self, user: CommunityUser, achievement: Achievement):
        """Notify user and system of achievement"""
        if self.message_bus:
            await self.message_bus.publish(GardenerMessage(
                topic=GardenerTopics.ACHIEVEMENT_EARNED,
                message_type="achievement_unlocked",
                payload={
                    "user_id": str(user.id),
                    "achievement_id": achievement.id,
                    "achievement_name": achievement.name,
                    "badge": achievement.badge,
                    "points": achievement.points
                }
            ))

    def get_user_progress(
        self,
        user: CommunityUser
    ) -> List[AchievementProgress]:
        """Get progress towards all achievements"""
        progress_list = []

        current_ids = self._user_achievements.get(user.id, [])

        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            unlocked = achievement_id in current_ids

            if unlocked:
                progress_list.append(AchievementProgress(
                    achievement=achievement,
                    current=achievement.requirement.get("value", 0),
                    target=achievement.requirement.get("value", 0),
                    progress_pct=100.0,
                    unlocked=True
                ))
            else:
                # Calculate progress
                current, target = self._get_progress_values(user, achievement)
                progress_pct = (current / target * 100) if target > 0 else 0

                progress_list.append(AchievementProgress(
                    achievement=achievement,
                    current=current,
                    target=target,
                    progress_pct=min(100.0, progress_pct),
                    unlocked=False
                ))

        return progress_list

    def _get_progress_values(
        self,
        user: CommunityUser,
        achievement: Achievement
    ) -> tuple:
        """Get current and target values for achievement progress"""
        requirement = achievement.requirement
        target = requirement.get("value", 0)

        # Estimate current based on user stats
        req_type = requirement.get("type")

        if req_type == "contribution_count":
            current = user.contribution_count
        elif req_type == "approved_count":
            current = user.approved_count
        elif req_type == "daily_streak":
            current = user.streak_days
        elif req_type == "review_count":
            current = user.review_count
        elif req_type == "reputation_level":
            current = user.current_level
        else:
            current = 0

        return current, target

    # Progress trackers
    async def _track_contribution_count(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return user.contribution_count

    async def _track_approved_count(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return user.approved_count

    async def _track_approval_streak(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        # Would track consecutive approvals
        return context.get("approval_streak", 0)

    async def _track_daily_streak(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return user.streak_days

    async def _track_category_count(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        category = requirement.get("category")
        # Would query DB for category-specific count
        return context.get(f"category_{category}_count", 0)

    async def _track_type_count(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        contribution_type = requirement.get("contribution_type")
        # Would query DB for type-specific count
        return context.get(f"type_{contribution_type}_count", 0)

    async def _track_review_count(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return user.review_count

    async def _track_mentored_users(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        # Would query DB for mentored users
        return context.get("mentored_count", 0)

    async def _track_corrections(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        # Would query DB for accepted corrections
        return context.get("corrections_count", 0)

    async def _track_reputation_level(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return user.current_level

    async def _track_new_parts(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return context.get("new_parts_documented", 0)

    async def _track_failure_reports(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return context.get("failure_reports_documented", 0)

    async def _track_accuracy_improvements(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return context.get("accuracy_improvements", 0)

    async def _track_tribal_knowledge(
        self,
        user: CommunityUser,
        requirement: Dict,
        context: Dict
    ) -> int:
        return context.get("tribal_knowledge_count", 0)

    async def _get_user_achievements(self, user_id: UUID) -> List[UserAchievement]:
        """Get all achievements for a user"""
        # Would query from database
        return []

    async def _save_user_achievement(self, achievement: UserAchievement):
        """Save user achievement to database"""
        pass

    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get achievement definition by ID"""
        return self.ACHIEVEMENTS.get(achievement_id)

    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        """Get all achievements in a category"""
        return [
            a for a in self.ACHIEVEMENTS.values()
            if a.category == category
        ]
