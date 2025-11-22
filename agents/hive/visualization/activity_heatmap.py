"""
Activity Heatmap - Visualizes swarm activity patterns.

Shows activity intensity across:
- Swarms
- Time periods
- Categories
- Tiers
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import Swarm, SwarmTier, SwarmHealthStatus


class HeatmapDimension(Enum):
    """Dimensions for heatmap aggregation."""
    CATEGORY = "category"
    TIER = "tier"
    TIME_HOUR = "time_hour"
    TIME_DAY = "time_day"
    SWARM = "swarm"


class ActivityMetric(Enum):
    """Metrics to visualize in heatmap."""
    LEARNING_COUNT = "learning_count"
    MEMBER_ACTIVITY = "member_activity"
    PROPAGATION_VOLUME = "propagation_volume"
    HEALTH_SCORE = "health_score"
    MESSAGES_SENT = "messages_sent"


@dataclass
class SwarmActivityCell:
    """A cell in the activity heatmap."""
    row_key: str
    col_key: str

    # Metrics
    value: float = 0.0
    raw_count: int = 0

    # Swarms in this cell
    swarm_count: int = 0
    swarm_ids: list[str] = field(default_factory=list)

    # Color
    color: str = "#E2E8F0"
    intensity: float = 0.0  # 0-1


@dataclass
class ActivityTimeSeries:
    """Time series of activity for a swarm or category."""
    entity_id: str
    entity_name: str

    # Data points
    timestamps: list[str] = field(default_factory=list)
    values: list[float] = field(default_factory=list)

    # Aggregates
    avg_value: float = 0.0
    max_value: float = 0.0
    min_value: float = 0.0
    trend: str = "stable"  # "increasing", "decreasing", "stable"


class ActivityRepository(Protocol):
    """Protocol for activity data access."""

    async def get_all_swarms(self) -> list[Swarm]:
        """Get all swarms."""
        ...

    async def get_swarm_activity(
        self,
        swarm_id: UUID,
        metric: ActivityMetric,
        since: datetime,
    ) -> list[tuple[datetime, float]]:
        """Get activity time series for a swarm."""
        ...

    async def get_category_activity(
        self,
        category: str,
        metric: ActivityMetric,
        since: datetime,
    ) -> list[tuple[datetime, float]]:
        """Get aggregated activity for a category."""
        ...

    async def get_hourly_activity(
        self,
        since: datetime,
    ) -> dict[int, float]:
        """Get activity by hour of day."""
        ...


class ActivityHeatmapGenerator:
    """
    Generates activity heatmaps for swarm visualization.
    """

    # Color gradients
    GRADIENT_BLUE = [
        "#EBF8FF", "#BEE3F8", "#90CDF4", "#63B3ED",
        "#4299E1", "#3182CE", "#2B6CB0", "#2C5282", "#1A365D",
    ]

    GRADIENT_GREEN = [
        "#F0FFF4", "#C6F6D5", "#9AE6B4", "#68D391",
        "#48BB78", "#38A169", "#2F855A", "#276749", "#1C4532",
    ]

    GRADIENT_RED = [
        "#FFF5F5", "#FED7D7", "#FEB2B2", "#FC8181",
        "#F56565", "#E53E3E", "#C53030", "#9B2C2C", "#742A2A",
    ]

    def __init__(self, repository: ActivityRepository):
        self.repository = repository

    async def generate_heatmap(
        self,
        row_dimension: HeatmapDimension = HeatmapDimension.CATEGORY,
        col_dimension: HeatmapDimension = HeatmapDimension.TIME_DAY,
        metric: ActivityMetric = ActivityMetric.LEARNING_COUNT,
        time_range_days: int = 7,
        normalize: bool = True,
    ) -> dict[str, Any]:
        """
        Generate an activity heatmap.

        Args:
            row_dimension: What to show on rows
            col_dimension: What to show on columns
            metric: Which metric to visualize
            time_range_days: Days of data to include
            normalize: Whether to normalize values 0-1

        Returns:
            Heatmap data structure
        """
        since = datetime.utcnow() - timedelta(days=time_range_days)
        swarms = await self.repository.get_all_swarms()

        # Get row and column keys
        row_keys = self._get_dimension_keys(swarms, row_dimension, since)
        col_keys = self._get_dimension_keys(swarms, col_dimension, since)

        # Build cell matrix
        cells: list[list[SwarmActivityCell]] = []
        max_value = 0.0

        for row_key in row_keys:
            row = []
            for col_key in col_keys:
                cell = await self._calculate_cell(
                    swarms, row_dimension, row_key, col_dimension, col_key, metric, since
                )
                row.append(cell)
                max_value = max(max_value, cell.value)
            cells.append(row)

        # Normalize and colorize
        if normalize and max_value > 0:
            for row in cells:
                for cell in row:
                    cell.intensity = cell.value / max_value
                    cell.color = self._intensity_to_color(cell.intensity)

        return {
            "type": "heatmap",
            "row_dimension": row_dimension.value,
            "col_dimension": col_dimension.value,
            "metric": metric.value,
            "row_labels": row_keys,
            "col_labels": col_keys,
            "cells": [
                [
                    {
                        "value": cell.value,
                        "raw_count": cell.raw_count,
                        "swarm_count": cell.swarm_count,
                        "intensity": round(cell.intensity, 3),
                        "color": cell.color,
                    }
                    for cell in row
                ]
                for row in cells
            ],
            "metadata": {
                "max_value": max_value,
                "time_range_days": time_range_days,
                "normalized": normalize,
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def generate_activity_timeline(
        self,
        entity_type: str = "category",  # "category", "tier", "swarm"
        entity_id: Optional[str] = None,
        metric: ActivityMetric = ActivityMetric.LEARNING_COUNT,
        time_range_days: int = 7,
        granularity: str = "hour",  # "hour", "day"
    ) -> dict[str, Any]:
        """
        Generate activity time series for an entity.

        Args:
            entity_type: Type of entity
            entity_id: Specific entity ID (or None for all)
            metric: Metric to track
            time_range_days: Days of data
            granularity: Time granularity

        Returns:
            Time series data
        """
        since = datetime.utcnow() - timedelta(days=time_range_days)
        swarms = await self.repository.get_all_swarms()

        series_list = []

        if entity_type == "category":
            categories = set(s.category for s in swarms)
            if entity_id:
                categories = {entity_id}

            for category in categories:
                activity = await self.repository.get_category_activity(
                    category, metric, since
                )
                series = self._build_time_series(category, category, activity)
                series_list.append(series)

        elif entity_type == "tier":
            tiers = [t for t in SwarmTier]
            for tier in tiers:
                if entity_id and tier.name != entity_id:
                    continue
                tier_swarms = [s for s in swarms if s.tier == tier]
                # Aggregate activity
                activity = await self._aggregate_swarm_activity(
                    tier_swarms, metric, since
                )
                series = self._build_time_series(
                    str(tier.value), tier.name, activity
                )
                series_list.append(series)

        elif entity_type == "swarm":
            target_swarms = swarms
            if entity_id:
                target_swarms = [s for s in swarms if str(s.id) == entity_id]

            for swarm in target_swarms[:10]:  # Limit to 10 swarms
                activity = await self.repository.get_swarm_activity(
                    swarm.id, metric, since
                )
                series = self._build_time_series(
                    str(swarm.id), swarm.name, activity
                )
                series_list.append(series)

        return {
            "type": "timeline",
            "entity_type": entity_type,
            "metric": metric.value,
            "granularity": granularity,
            "series": [
                {
                    "id": s.entity_id,
                    "name": s.entity_name,
                    "timestamps": s.timestamps,
                    "values": s.values,
                    "stats": {
                        "avg": round(s.avg_value, 2),
                        "max": round(s.max_value, 2),
                        "min": round(s.min_value, 2),
                        "trend": s.trend,
                    },
                }
                for s in series_list
            ],
            "metadata": {
                "time_range_days": time_range_days,
                "series_count": len(series_list),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def generate_health_dashboard(self) -> dict[str, Any]:
        """
        Generate a health overview dashboard.

        Shows:
        - Health distribution by tier
        - Activity trends
        - Stagnant swarm alerts
        """
        swarms = await self.repository.get_all_swarms()

        # Health distribution
        health_by_status = {}
        health_by_tier = {}

        for swarm in swarms:
            # By status
            status = swarm.health_status.value
            health_by_status[status] = health_by_status.get(status, 0) + 1

            # By tier
            tier = swarm.tier.name
            if tier not in health_by_tier:
                health_by_tier[tier] = {"healthy": 0, "unhealthy": 0}

            if swarm.health_status in [SwarmHealthStatus.THRIVING, SwarmHealthStatus.HEALTHY]:
                health_by_tier[tier]["healthy"] += 1
            else:
                health_by_tier[tier]["unhealthy"] += 1

        # Stagnant swarms (need attention)
        stagnant_swarms = [
            {
                "id": str(s.id),
                "name": s.name,
                "tier": s.tier.name,
                "health_status": s.health_status.value,
                "activity_score": s.activity_score,
                "member_count": s.member_count,
            }
            for s in swarms
            if s.health_status in [SwarmHealthStatus.STAGNANT, SwarmHealthStatus.DORMANT]
        ][:20]

        # Top performing swarms
        top_swarms = sorted(swarms, key=lambda s: s.activity_score, reverse=True)[:10]

        return {
            "health_distribution": health_by_status,
            "health_by_tier": health_by_tier,
            "stagnant_swarms": stagnant_swarms,
            "top_performing": [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "tier": s.tier.name,
                    "activity_score": s.activity_score,
                    "learning_count": s.learning_count,
                }
                for s in top_swarms
            ],
            "summary": {
                "total_swarms": len(swarms),
                "healthy_percentage": (
                    health_by_status.get("thriving", 0) +
                    health_by_status.get("healthy", 0)
                ) / max(len(swarms), 1) * 100,
                "avg_activity_score": sum(s.activity_score for s in swarms) / max(len(swarms), 1),
            },
            "generated_at": datetime.utcnow().isoformat(),
        }

    def _get_dimension_keys(
        self,
        swarms: list[Swarm],
        dimension: HeatmapDimension,
        since: datetime,
    ) -> list[str]:
        """Get keys for a dimension."""
        if dimension == HeatmapDimension.CATEGORY:
            return sorted(set(s.category for s in swarms))

        elif dimension == HeatmapDimension.TIER:
            return [t.name for t in SwarmTier]

        elif dimension == HeatmapDimension.TIME_DAY:
            days = []
            current = since
            while current <= datetime.utcnow():
                days.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)
            return days

        elif dimension == HeatmapDimension.TIME_HOUR:
            return [f"{h:02d}:00" for h in range(24)]

        elif dimension == HeatmapDimension.SWARM:
            # Top 20 swarms by activity
            sorted_swarms = sorted(
                swarms, key=lambda s: s.activity_score, reverse=True
            )[:20]
            return [s.name for s in sorted_swarms]

        return []

    async def _calculate_cell(
        self,
        swarms: list[Swarm],
        row_dim: HeatmapDimension,
        row_key: str,
        col_dim: HeatmapDimension,
        col_key: str,
        metric: ActivityMetric,
        since: datetime,
    ) -> SwarmActivityCell:
        """Calculate value for a heatmap cell."""
        # Filter swarms matching row dimension
        matching_swarms = self._filter_swarms_by_dimension(
            swarms, row_dim, row_key
        )

        # Calculate metric value
        if metric == ActivityMetric.LEARNING_COUNT:
            value = sum(s.learning_count for s in matching_swarms)
        elif metric == ActivityMetric.MEMBER_ACTIVITY:
            total = sum(s.active_member_count for s in matching_swarms)
            total_members = sum(s.member_count for s in matching_swarms)
            value = total / max(total_members, 1)
        elif metric == ActivityMetric.HEALTH_SCORE:
            scores = [s.activity_score for s in matching_swarms]
            value = sum(scores) / max(len(scores), 1)
        else:
            value = len(matching_swarms)

        return SwarmActivityCell(
            row_key=row_key,
            col_key=col_key,
            value=value,
            raw_count=len(matching_swarms),
            swarm_count=len(matching_swarms),
            swarm_ids=[str(s.id) for s in matching_swarms],
        )

    def _filter_swarms_by_dimension(
        self,
        swarms: list[Swarm],
        dimension: HeatmapDimension,
        key: str,
    ) -> list[Swarm]:
        """Filter swarms by dimension value."""
        if dimension == HeatmapDimension.CATEGORY:
            return [s for s in swarms if s.category == key]
        elif dimension == HeatmapDimension.TIER:
            return [s for s in swarms if s.tier.name == key]
        elif dimension == HeatmapDimension.SWARM:
            return [s for s in swarms if s.name == key]
        return swarms

    async def _aggregate_swarm_activity(
        self,
        swarms: list[Swarm],
        metric: ActivityMetric,
        since: datetime,
    ) -> list[tuple[datetime, float]]:
        """Aggregate activity across multiple swarms."""
        aggregated: dict[datetime, float] = {}

        for swarm in swarms:
            activity = await self.repository.get_swarm_activity(
                swarm.id, metric, since
            )
            for ts, value in activity:
                # Round to hour
                ts_hour = ts.replace(minute=0, second=0, microsecond=0)
                aggregated[ts_hour] = aggregated.get(ts_hour, 0) + value

        return sorted(aggregated.items())

    def _build_time_series(
        self,
        entity_id: str,
        entity_name: str,
        activity: list[tuple[datetime, float]],
    ) -> ActivityTimeSeries:
        """Build a time series object from raw data."""
        if not activity:
            return ActivityTimeSeries(
                entity_id=entity_id,
                entity_name=entity_name,
            )

        timestamps = [ts.isoformat() for ts, _ in activity]
        values = [v for _, v in activity]

        # Calculate trend
        if len(values) >= 2:
            first_half = sum(values[:len(values)//2])
            second_half = sum(values[len(values)//2:])
            if second_half > first_half * 1.1:
                trend = "increasing"
            elif second_half < first_half * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "stable"

        return ActivityTimeSeries(
            entity_id=entity_id,
            entity_name=entity_name,
            timestamps=timestamps,
            values=values,
            avg_value=sum(values) / len(values),
            max_value=max(values),
            min_value=min(values),
            trend=trend,
        )

    def _intensity_to_color(self, intensity: float) -> str:
        """Convert intensity (0-1) to a color from the gradient."""
        gradient = self.GRADIENT_BLUE
        index = int(intensity * (len(gradient) - 1))
        return gradient[min(index, len(gradient) - 1)]
