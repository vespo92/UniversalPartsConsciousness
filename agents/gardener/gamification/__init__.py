"""
Gamification subsystem for Agent_8 (Gardener).

Manages achievements, challenges, leaderboards, and badges to
incentivize quality community contributions.
"""

from .achievement_system import AchievementSystem, AchievementProgress
from .leaderboard import LeaderboardSystem, LeaderboardConfig

__all__ = [
    "AchievementSystem",
    "AchievementProgress",
    "LeaderboardSystem",
    "LeaderboardConfig",
]
