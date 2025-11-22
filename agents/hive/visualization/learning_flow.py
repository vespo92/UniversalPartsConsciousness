"""
Learning Flow Visualization - Visualizes knowledge propagation across swarms.

Shows how learnings flow from individual parts through swarms,
tracking propagation paths, strength, and impact.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import Learning, LearningType, Swarm, SwarmTier


class FlowVisualizationType(Enum):
    """Types of flow visualizations."""
    SANKEY = "sankey"       # Sankey diagram
    TIMELINE = "timeline"   # Temporal flow
    TREE = "tree"           # Propagation tree
    HEATMAP = "heatmap"     # Flow intensity heatmap


@dataclass
class PropagationPath:
    """A path that a learning took through swarms."""
    learning_id: UUID
    learning_type: LearningType

    # Source
    source_part_id: UUID
    source_swarm_id: UUID
    source_swarm_name: str

    # Path through swarms
    path_steps: list[dict[str, Any]] = field(default_factory=list)
    # Each step: {swarm_id, swarm_name, tier, strength, members_affected, timestamp}

    # Metrics
    total_swarms_reached: int = 0
    total_members_affected: int = 0
    propagation_time_ms: float = 0.0
    avg_strength: float = 0.0

    # Timestamps
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


@dataclass
class FlowAggregation:
    """Aggregated flow data between source and target."""
    source_id: str
    source_name: str
    target_id: str
    target_name: str

    # Metrics
    total_learnings: int = 0
    total_members_affected: int = 0
    avg_strength: float = 0.0

    # By type
    learnings_by_type: dict[str, int] = field(default_factory=dict)


class LearningFlowRepository(Protocol):
    """Protocol for learning flow data access."""

    async def get_propagation_paths(
        self,
        since: datetime,
        limit: int = 1000,
    ) -> list[PropagationPath]:
        """Get recent propagation paths."""
        ...

    async def get_learning_path(
        self,
        learning_id: UUID,
    ) -> Optional[PropagationPath]:
        """Get path for a specific learning."""
        ...

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def get_learnings_between(
        self,
        source_swarm_id: UUID,
        target_swarm_id: UUID,
        since: datetime,
    ) -> list[Learning]:
        """Get learnings that flowed between two swarms."""
        ...


class LearningFlowVisualizer:
    """
    Generates visualizations of learning propagation flows.
    """

    # Colors for learning types
    LEARNING_TYPE_COLORS = {
        LearningType.FAILURE_MODE: "#E53E3E",       # Red
        LearningType.SURVIVAL_LIMIT: "#38A169",     # Green
        LearningType.LONGEVITY_FACTOR: "#3182CE",   # Blue
        LearningType.COMPATIBILITY_INSIGHT: "#805AD5",  # Purple
        LearningType.USAGE_PATTERN: "#D69E2E",      # Yellow
        LearningType.ENVIRONMENTAL_ADAPTATION: "#00B5D8",  # Cyan
        LearningType.MAINTENANCE_WISDOM: "#ED8936", # Orange
    }

    def __init__(self, repository: LearningFlowRepository):
        self.repository = repository

    async def generate_flow_diagram(
        self,
        visualization_type: FlowVisualizationType = FlowVisualizationType.SANKEY,
        time_range_hours: int = 24,
        filter_type: Optional[LearningType] = None,
        min_strength: float = 0.0,
    ) -> dict[str, Any]:
        """
        Generate a flow visualization.

        Args:
            visualization_type: Type of visualization
            time_range_hours: Hours of data to include
            filter_type: Only include this learning type
            min_strength: Minimum propagation strength

        Returns:
            Visualization data in appropriate format
        """
        since = datetime.utcnow() - timedelta(hours=time_range_hours)
        paths = await self.repository.get_propagation_paths(since)

        # Filter paths
        if filter_type:
            paths = [p for p in paths if p.learning_type == filter_type]
        if min_strength > 0:
            paths = [p for p in paths if p.avg_strength >= min_strength]

        # Generate based on type
        if visualization_type == FlowVisualizationType.SANKEY:
            return await self._generate_sankey(paths)
        elif visualization_type == FlowVisualizationType.TIMELINE:
            return await self._generate_timeline(paths)
        elif visualization_type == FlowVisualizationType.TREE:
            return await self._generate_tree(paths)
        elif visualization_type == FlowVisualizationType.HEATMAP:
            return await self._generate_flow_heatmap(paths)
        else:
            return await self._generate_sankey(paths)

    async def get_learning_path_visualization(
        self,
        learning_id: UUID,
    ) -> dict[str, Any]:
        """
        Get visualization of a specific learning's propagation path.
        """
        path = await self.repository.get_learning_path(learning_id)
        if not path:
            return {"error": "Learning path not found"}

        return {
            "learning_id": str(learning_id),
            "learning_type": path.learning_type.value,
            "source": {
                "part_id": str(path.source_part_id),
                "swarm_id": str(path.source_swarm_id),
                "swarm_name": path.source_swarm_name,
            },
            "path": [
                {
                    "swarm_id": step["swarm_id"],
                    "swarm_name": step["swarm_name"],
                    "tier": step["tier"],
                    "strength": step["strength"],
                    "members_affected": step["members_affected"],
                    "timestamp": step["timestamp"],
                    "color": self._strength_to_color(step["strength"]),
                }
                for step in path.path_steps
            ],
            "metrics": {
                "total_swarms": path.total_swarms_reached,
                "total_members": path.total_members_affected,
                "propagation_time_ms": path.propagation_time_ms,
                "avg_strength": path.avg_strength,
            },
            "timestamps": {
                "started": path.started_at.isoformat(),
                "completed": path.completed_at.isoformat() if path.completed_at else None,
            },
        }

    async def _generate_sankey(
        self,
        paths: list[PropagationPath],
    ) -> dict[str, Any]:
        """
        Generate Sankey diagram data.

        Shows flows between tiers and swarms.
        """
        # Aggregate flows between swarms
        aggregations: dict[tuple[str, str], FlowAggregation] = {}

        for path in paths:
            prev_step = {
                "swarm_id": str(path.source_swarm_id),
                "swarm_name": path.source_swarm_name,
            }

            for step in path.path_steps:
                key = (prev_step["swarm_id"], step["swarm_id"])

                if key not in aggregations:
                    aggregations[key] = FlowAggregation(
                        source_id=prev_step["swarm_id"],
                        source_name=prev_step["swarm_name"],
                        target_id=step["swarm_id"],
                        target_name=step["swarm_name"],
                    )

                agg = aggregations[key]
                agg.total_learnings += 1
                agg.total_members_affected += step.get("members_affected", 0)
                agg.avg_strength = (
                    agg.avg_strength * (agg.total_learnings - 1) +
                    step.get("strength", 0)
                ) / agg.total_learnings

                lt = path.learning_type.value
                agg.learnings_by_type[lt] = agg.learnings_by_type.get(lt, 0) + 1

                prev_step = step

        # Build Sankey format
        nodes = set()
        links = []

        for (src, tgt), agg in aggregations.items():
            nodes.add((src, agg.source_name))
            nodes.add((tgt, agg.target_name))
            links.append({
                "source": src,
                "target": tgt,
                "value": agg.total_learnings,
                "members_affected": agg.total_members_affected,
                "avg_strength": round(agg.avg_strength, 3),
                "by_type": agg.learnings_by_type,
            })

        return {
            "type": "sankey",
            "nodes": [
                {"id": nid, "name": name}
                for nid, name in nodes
            ],
            "links": links,
            "metadata": {
                "total_paths": len(paths),
                "total_flows": len(links),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def _generate_timeline(
        self,
        paths: list[PropagationPath],
    ) -> dict[str, Any]:
        """
        Generate timeline visualization data.

        Shows learning propagation over time.
        """
        events = []

        for path in paths:
            # Source event
            events.append({
                "timestamp": path.started_at.isoformat(),
                "type": "source",
                "learning_id": str(path.learning_id),
                "learning_type": path.learning_type.value,
                "swarm_id": str(path.source_swarm_id),
                "swarm_name": path.source_swarm_name,
                "color": self.LEARNING_TYPE_COLORS.get(
                    path.learning_type, "#718096"
                ),
            })

            # Propagation events
            for step in path.path_steps:
                events.append({
                    "timestamp": step.get("timestamp", path.started_at.isoformat()),
                    "type": "propagation",
                    "learning_id": str(path.learning_id),
                    "learning_type": path.learning_type.value,
                    "swarm_id": step["swarm_id"],
                    "swarm_name": step["swarm_name"],
                    "strength": step.get("strength", 0),
                    "members_affected": step.get("members_affected", 0),
                    "color": self._strength_to_color(step.get("strength", 0)),
                })

        # Sort by timestamp
        events.sort(key=lambda e: e["timestamp"])

        return {
            "type": "timeline",
            "events": events,
            "metadata": {
                "total_paths": len(paths),
                "total_events": len(events),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def _generate_tree(
        self,
        paths: list[PropagationPath],
    ) -> dict[str, Any]:
        """
        Generate tree visualization data.

        Shows propagation as a tree from source outward.
        """
        trees = []

        for path in paths:
            tree = {
                "id": str(path.learning_id),
                "type": path.learning_type.value,
                "root": {
                    "id": str(path.source_swarm_id),
                    "name": path.source_swarm_name,
                    "type": "source",
                    "children": [],
                },
            }

            # Build tree structure
            current = tree["root"]
            for step in path.path_steps:
                child = {
                    "id": step["swarm_id"],
                    "name": step["swarm_name"],
                    "tier": step.get("tier"),
                    "strength": step.get("strength", 0),
                    "members": step.get("members_affected", 0),
                    "children": [],
                }
                current["children"].append(child)
                current = child

            trees.append(tree)

        return {
            "type": "tree",
            "trees": trees,
            "metadata": {
                "total_trees": len(trees),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def _generate_flow_heatmap(
        self,
        paths: list[PropagationPath],
    ) -> dict[str, Any]:
        """
        Generate heatmap of flow intensity.

        Shows which swarm pairs have most learning flow.
        """
        # Count flows between tier pairs
        tier_flows: dict[tuple[int, int], int] = {}
        swarm_flows: dict[tuple[str, str], int] = {}

        for path in paths:
            prev_tier = None
            prev_id = str(path.source_swarm_id)

            for step in path.path_steps:
                curr_tier = step.get("tier", 0)
                curr_id = step["swarm_id"]

                if prev_tier is not None:
                    tier_key = (prev_tier, curr_tier)
                    tier_flows[tier_key] = tier_flows.get(tier_key, 0) + 1

                swarm_key = (prev_id, curr_id)
                swarm_flows[swarm_key] = swarm_flows.get(swarm_key, 0) + 1

                prev_tier = curr_tier
                prev_id = curr_id

        # Convert to heatmap format
        tier_matrix = []
        for i in range(1, 6):
            row = []
            for j in range(1, 6):
                row.append(tier_flows.get((i, j), 0))
            tier_matrix.append(row)

        return {
            "type": "heatmap",
            "tier_matrix": {
                "labels": ["Global", "Family", "Spec", "Context", "Experience"],
                "values": tier_matrix,
            },
            "top_flows": sorted(
                [
                    {"source": src, "target": tgt, "count": count}
                    for (src, tgt), count in swarm_flows.items()
                ],
                key=lambda x: x["count"],
                reverse=True,
            )[:20],
            "metadata": {
                "total_paths": len(paths),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    def _strength_to_color(self, strength: float) -> str:
        """Convert propagation strength to a color."""
        if strength >= 0.8:
            return "#38A169"  # Green - strong
        elif strength >= 0.6:
            return "#68D391"  # Light green
        elif strength >= 0.4:
            return "#ECC94B"  # Yellow - moderate
        elif strength >= 0.2:
            return "#ED8936"  # Orange - weak
        else:
            return "#E53E3E"  # Red - very weak
