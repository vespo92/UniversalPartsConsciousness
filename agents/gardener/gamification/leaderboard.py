"""
Leaderboard System - Tracks and displays user rankings

Manages multiple leaderboard types with caching for performance.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..models import (
    CommunityUser,
    Leaderboard,
    LeaderboardEntry,
)


@dataclass
class LeaderboardConfig:
    """Configuration for a leaderboard type"""
    leaderboard_type: str
    period_days: Optional[int] = None  # None = all-time
    display_count: int = 100
    per_category: bool = False
    cache_ttl_minutes: int = 5


class LeaderboardSystem:
    """
    Leaderboard management system.

    Supports multiple leaderboard types:
    - All-time: Overall rankings by lifetime points
    - Monthly: Rankings for the current month
    - Weekly: Rankings for the current week
    - Category: Per-category rankings
    """

    LEADERBOARD_CONFIGS = {
        "all_time": LeaderboardConfig(
            leaderboard_type="all_time",
            period_days=None,
            display_count=100
        ),
        "monthly": LeaderboardConfig(
            leaderboard_type="monthly",
            period_days=30,
            display_count=50
        ),
        "weekly": LeaderboardConfig(
            leaderboard_type="weekly",
            period_days=7,
            display_count=25
        ),
        "category": LeaderboardConfig(
            leaderboard_type="category",
            period_days=None,
            display_count=10,
            per_category=True
        ),
    }

    CATEGORIES = [
        "fasteners",
        "bearings",
        "seals",
        "automotive",
        "aerospace",
        "marine",
        "materials",
        "manufacturing",
    ]

    def __init__(self, db_connection=None, reputation_engine=None):
        self.db = db_connection
        self.reputation_engine = reputation_engine

        # Leaderboard cache
        self._cache: Dict[str, Leaderboard] = {}
        self._cache_timestamps: Dict[str, datetime] = {}

    async def get_leaderboard(
        self,
        leaderboard_type: str,
        category: Optional[str] = None,
        force_refresh: bool = False
    ) -> Leaderboard:
        """
        Get a leaderboard, using cache if available.

        Args:
            leaderboard_type: Type of leaderboard (all_time, monthly, weekly, category)
            category: Category for category leaderboards
            force_refresh: Force refresh from database

        Returns:
            Leaderboard with rankings
        """
        config = self.LEADERBOARD_CONFIGS.get(leaderboard_type)
        if not config:
            raise ValueError(f"Unknown leaderboard type: {leaderboard_type}")

        cache_key = self._get_cache_key(leaderboard_type, category)

        # Check cache
        if not force_refresh:
            cached = self._get_from_cache(cache_key, config.cache_ttl_minutes)
            if cached:
                return cached

        # Generate leaderboard
        leaderboard = await self._generate_leaderboard(config, category)

        # Cache result
        self._cache[cache_key] = leaderboard
        self._cache_timestamps[cache_key] = datetime.now()

        return leaderboard

    async def _generate_leaderboard(
        self,
        config: LeaderboardConfig,
        category: Optional[str] = None
    ) -> Leaderboard:
        """Generate leaderboard from database"""
        # Calculate period
        period_start = None
        period_end = datetime.now()

        if config.period_days:
            period_start = datetime.now() - timedelta(days=config.period_days)

        # Get top users
        entries = await self._get_top_users(
            period_start=period_start,
            period_end=period_end,
            category=category,
            limit=config.display_count
        )

        return Leaderboard(
            leaderboard_type=config.leaderboard_type,
            category=category,
            period_start=period_start,
            period_end=period_end,
            entries=entries,
            generated_at=datetime.now()
        )

    async def _get_top_users(
        self,
        period_start: Optional[datetime],
        period_end: datetime,
        category: Optional[str],
        limit: int
    ) -> List[LeaderboardEntry]:
        """Get top users for leaderboard"""
        # In production, this would query the database
        # For now, return placeholder
        return []

    def _get_cache_key(
        self,
        leaderboard_type: str,
        category: Optional[str]
    ) -> str:
        """Generate cache key"""
        if category:
            return f"{leaderboard_type}:{category}"
        return leaderboard_type

    def _get_from_cache(
        self,
        cache_key: str,
        ttl_minutes: int
    ) -> Optional[Leaderboard]:
        """Get leaderboard from cache if valid"""
        if cache_key not in self._cache:
            return None

        cached_at = self._cache_timestamps.get(cache_key)
        if not cached_at:
            return None

        age = datetime.now() - cached_at
        if age > timedelta(minutes=ttl_minutes):
            return None

        return self._cache[cache_key]

    def invalidate_cache(self, leaderboard_type: Optional[str] = None):
        """Invalidate leaderboard cache"""
        if leaderboard_type:
            # Invalidate specific leaderboard
            keys_to_remove = [
                k for k in self._cache.keys()
                if k.startswith(leaderboard_type)
            ]
            for key in keys_to_remove:
                del self._cache[key]
                if key in self._cache_timestamps:
                    del self._cache_timestamps[key]
        else:
            # Invalidate all
            self._cache.clear()
            self._cache_timestamps.clear()

    async def get_user_rank(
        self,
        user_id: UUID,
        leaderboard_type: str = "all_time",
        category: Optional[str] = None
    ) -> Optional[int]:
        """Get a user's rank on a leaderboard"""
        leaderboard = await self.get_leaderboard(leaderboard_type, category)

        for entry in leaderboard.entries:
            if entry.user_id == user_id:
                return entry.rank

        # User not in top N, need to query for exact rank
        return await self._get_exact_rank(user_id, leaderboard_type, category)

    async def _get_exact_rank(
        self,
        user_id: UUID,
        leaderboard_type: str,
        category: Optional[str]
    ) -> Optional[int]:
        """Get exact rank for user not in top N"""
        # Would query database for count of users with more points
        return None

    async def get_surrounding_users(
        self,
        user_id: UUID,
        leaderboard_type: str = "all_time",
        context_count: int = 5
    ) -> Dict[str, Any]:
        """Get users around a specific user's rank"""
        rank = await self.get_user_rank(user_id, leaderboard_type)
        if not rank:
            return {"user_rank": None, "surrounding": []}

        # Get users above and below
        # Would query database for surrounding entries
        return {
            "user_rank": rank,
            "surrounding": []
        }

    async def get_category_leaders(self) -> Dict[str, LeaderboardEntry]:
        """Get the #1 user in each category"""
        leaders = {}

        for category in self.CATEGORIES:
            leaderboard = await self.get_leaderboard("category", category)
            if leaderboard.entries:
                leaders[category] = leaderboard.entries[0]

        return leaders

    async def record_leaderboard_snapshot(self):
        """Record current leaderboard state for historical tracking"""
        # Would save to database for historical analysis
        for leaderboard_type in self.LEADERBOARD_CONFIGS.keys():
            if leaderboard_type == "category":
                for category in self.CATEGORIES:
                    leaderboard = await self.get_leaderboard(leaderboard_type, category)
                    await self._save_snapshot(leaderboard)
            else:
                leaderboard = await self.get_leaderboard(leaderboard_type)
                await self._save_snapshot(leaderboard)

    async def _save_snapshot(self, leaderboard: Leaderboard):
        """Save leaderboard snapshot to database"""
        pass

    async def get_historical_rank(
        self,
        user_id: UUID,
        leaderboard_type: str,
        date: datetime
    ) -> Optional[int]:
        """Get user's historical rank at a specific date"""
        # Would query historical snapshots
        return None

    def get_rank_change(
        self,
        user_id: UUID,
        leaderboard_type: str = "all_time"
    ) -> Optional[int]:
        """Get rank change since last snapshot"""
        # Would compare current rank to previous snapshot
        return None
