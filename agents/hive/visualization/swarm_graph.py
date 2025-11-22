"""
Swarm Graph Visualization - Visualizes swarm relationships and hierarchy.

Creates interactive graph representations showing:
- Swarm hierarchy across 5 tiers
- Inter-swarm relationships
- Member counts and health status
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import Swarm, SwarmTier, SwarmHealthStatus


class GraphFormat(Enum):
    """Output formats for graph visualization."""
    JSON = "json"
    DOT = "dot"  # GraphViz format
    CYTOSCAPE = "cytoscape"
    D3 = "d3"


@dataclass
class SwarmNode:
    """A node in the swarm relationship graph."""
    id: str
    swarm_id: UUID
    name: str
    tier: SwarmTier
    category: str

    # Metrics
    member_count: int = 0
    active_member_count: int = 0
    learning_count: int = 0

    # Health
    health_status: SwarmHealthStatus = SwarmHealthStatus.HEALTHY
    health_score: float = 0.0
    activity_score: float = 0.0

    # Visual properties
    size: float = 1.0  # Relative node size
    color: str = "#4A90D9"  # Default blue
    position_x: Optional[float] = None
    position_y: Optional[float] = None


@dataclass
class SwarmEdge:
    """An edge connecting two swarms."""
    id: str
    source_id: str
    target_id: str

    # Relationship
    relationship_type: str = "related"  # "related", "parent_child", "cross_swarm"
    strength: float = 0.5  # 0-1, strength of relationship

    # Communication metrics
    messages_exchanged: int = 0
    last_communication: Optional[datetime] = None

    # Visual properties
    width: float = 1.0
    color: str = "#888888"
    style: str = "solid"  # "solid", "dashed", "dotted"


class SwarmRepository(Protocol):
    """Protocol for swarm data access."""

    async def get_all_swarms(self) -> list[Swarm]:
        """Get all swarms."""
        ...

    async def get_swarm_relationships(self, swarm_id: UUID) -> list[UUID]:
        """Get related swarm IDs."""
        ...

    async def get_communication_count(
        self, swarm1_id: UUID, swarm2_id: UUID
    ) -> int:
        """Get message count between swarms."""
        ...


class SwarmGraphVisualizer:
    """
    Generates visual graph representations of swarm relationships.
    """

    # Color scheme by tier
    TIER_COLORS = {
        SwarmTier.GLOBAL: "#1A365D",     # Deep blue
        SwarmTier.FAMILY: "#2C5282",     # Medium blue
        SwarmTier.SPEC: "#3182CE",       # Light blue
        SwarmTier.CONTEXT: "#63B3ED",    # Cyan
        SwarmTier.EXPERIENCE: "#90CDF4", # Light cyan
    }

    # Color scheme by health
    HEALTH_COLORS = {
        SwarmHealthStatus.THRIVING: "#48BB78",   # Green
        SwarmHealthStatus.HEALTHY: "#68D391",    # Light green
        SwarmHealthStatus.DECLINING: "#ECC94B",  # Yellow
        SwarmHealthStatus.STAGNANT: "#ED8936",   # Orange
        SwarmHealthStatus.DORMANT: "#A0AEC0",    # Gray
    }

    def __init__(self, repository: SwarmRepository):
        self.repository = repository

    async def generate_graph(
        self,
        format: GraphFormat = GraphFormat.JSON,
        filter_tier: Optional[SwarmTier] = None,
        filter_category: Optional[str] = None,
        min_members: int = 0,
        include_dormant: bool = False,
        color_by: str = "tier",  # "tier", "health", "activity"
    ) -> dict[str, Any]:
        """
        Generate a graph visualization of swarm relationships.

        Args:
            format: Output format
            filter_tier: Only include swarms of this tier
            filter_category: Only include swarms of this category
            min_members: Minimum member count to include
            include_dormant: Include dormant swarms
            color_by: How to color nodes

        Returns:
            Graph data in specified format
        """
        # Get all swarms
        all_swarms = await self.repository.get_all_swarms()

        # Apply filters
        swarms = self._filter_swarms(
            all_swarms,
            filter_tier,
            filter_category,
            min_members,
            include_dormant,
        )

        # Build nodes
        nodes = [self._swarm_to_node(s, color_by) for s in swarms]

        # Build edges
        edges = await self._build_edges(swarms)

        # Format output
        if format == GraphFormat.JSON:
            return self._to_json(nodes, edges)
        elif format == GraphFormat.DOT:
            return {"dot": self._to_dot(nodes, edges)}
        elif format == GraphFormat.CYTOSCAPE:
            return self._to_cytoscape(nodes, edges)
        elif format == GraphFormat.D3:
            return self._to_d3(nodes, edges)
        else:
            return self._to_json(nodes, edges)

    async def generate_hierarchy_view(
        self,
        category: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Generate a hierarchical tree view of swarms.

        Shows the 5-tier hierarchy for a category.
        """
        all_swarms = await self.repository.get_all_swarms()

        if category:
            swarms = [s for s in all_swarms if s.category == category]
        else:
            swarms = all_swarms

        # Organize by tier
        hierarchy = {
            "tier_1_global": [],
            "tier_2_family": [],
            "tier_3_spec": [],
            "tier_4_context": [],
            "tier_5_experience": [],
        }

        for swarm in swarms:
            tier_key = f"tier_{swarm.tier.value}_{swarm.tier.name.lower()}"
            if tier_key in hierarchy:
                hierarchy[tier_key].append({
                    "id": str(swarm.id),
                    "name": swarm.name,
                    "member_count": swarm.member_count,
                    "health": swarm.health_status.value,
                })

        return {
            "category": category or "all",
            "hierarchy": hierarchy,
            "total_swarms": len(swarms),
        }

    def _filter_swarms(
        self,
        swarms: list[Swarm],
        filter_tier: Optional[SwarmTier],
        filter_category: Optional[str],
        min_members: int,
        include_dormant: bool,
    ) -> list[Swarm]:
        """Apply filters to swarm list."""
        result = swarms

        if filter_tier:
            result = [s for s in result if s.tier == filter_tier]

        if filter_category:
            result = [s for s in result if s.category == filter_category]

        if min_members > 0:
            result = [s for s in result if s.member_count >= min_members]

        if not include_dormant:
            result = [s for s in result if s.health_status != SwarmHealthStatus.DORMANT]

        return result

    def _swarm_to_node(self, swarm: Swarm, color_by: str) -> SwarmNode:
        """Convert a swarm to a graph node."""
        # Determine color
        if color_by == "tier":
            color = self.TIER_COLORS.get(swarm.tier, "#4A90D9")
        elif color_by == "health":
            color = self.HEALTH_COLORS.get(swarm.health_status, "#4A90D9")
        elif color_by == "activity":
            # Gradient from red (inactive) to green (active)
            activity = swarm.activity_score
            if activity >= 0.7:
                color = "#48BB78"
            elif activity >= 0.4:
                color = "#ECC94B"
            else:
                color = "#FC8181"
        else:
            color = "#4A90D9"

        # Size based on member count (log scale)
        import math
        size = 1 + math.log10(max(swarm.member_count, 1)) * 0.3

        return SwarmNode(
            id=str(swarm.id),
            swarm_id=swarm.id,
            name=swarm.name,
            tier=swarm.tier,
            category=swarm.category,
            member_count=swarm.member_count,
            active_member_count=swarm.active_member_count,
            learning_count=swarm.learning_count,
            health_status=swarm.health_status,
            health_score=swarm.activity_score,  # Using activity as health proxy
            activity_score=swarm.activity_score,
            size=size,
            color=color,
        )

    async def _build_edges(self, swarms: list[Swarm]) -> list[SwarmEdge]:
        """Build edges between related swarms."""
        edges = []
        swarm_ids = {str(s.id) for s in swarms}
        processed = set()

        for swarm in swarms:
            for related_id in swarm.related_swarm_ids:
                related_str = str(related_id)

                # Only include if target is in our filtered set
                if related_str not in swarm_ids:
                    continue

                # Avoid duplicates
                edge_key = tuple(sorted([str(swarm.id), related_str]))
                if edge_key in processed:
                    continue
                processed.add(edge_key)

                # Get communication count
                msg_count = await self.repository.get_communication_count(
                    swarm.id, related_id
                )

                # Determine relationship type
                if swarm.parent_swarm_id == related_id or related_id in [str(c) for c in swarm.child_swarm_ids]:
                    rel_type = "parent_child"
                    style = "solid"
                else:
                    rel_type = "cross_swarm"
                    style = "dashed"

                edges.append(SwarmEdge(
                    id=f"{swarm.id}-{related_id}",
                    source_id=str(swarm.id),
                    target_id=related_str,
                    relationship_type=rel_type,
                    strength=min(msg_count / 100, 1.0),
                    messages_exchanged=msg_count,
                    width=1 + msg_count / 50,
                    style=style,
                ))

        return edges

    def _to_json(
        self,
        nodes: list[SwarmNode],
        edges: list[SwarmEdge],
    ) -> dict[str, Any]:
        """Convert to JSON format."""
        return {
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "tier": n.tier.value,
                    "tier_name": n.tier.name,
                    "category": n.category,
                    "member_count": n.member_count,
                    "active_member_count": n.active_member_count,
                    "learning_count": n.learning_count,
                    "health_status": n.health_status.value,
                    "health_score": n.health_score,
                    "activity_score": n.activity_score,
                    "visual": {
                        "size": n.size,
                        "color": n.color,
                    },
                }
                for n in nodes
            ],
            "edges": [
                {
                    "id": e.id,
                    "source": e.source_id,
                    "target": e.target_id,
                    "relationship_type": e.relationship_type,
                    "strength": e.strength,
                    "messages_exchanged": e.messages_exchanged,
                    "visual": {
                        "width": e.width,
                        "color": e.color,
                        "style": e.style,
                    },
                }
                for e in edges
            ],
            "metadata": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    def _to_dot(
        self,
        nodes: list[SwarmNode],
        edges: list[SwarmEdge],
    ) -> str:
        """Convert to GraphViz DOT format."""
        lines = ["digraph SwarmGraph {"]
        lines.append("  rankdir=TB;")
        lines.append("  node [shape=circle];")
        lines.append("")

        # Add nodes grouped by tier
        for tier in SwarmTier:
            tier_nodes = [n for n in nodes if n.tier == tier]
            if tier_nodes:
                lines.append(f"  subgraph cluster_{tier.name} {{")
                lines.append(f'    label="{tier.name}";')
                for node in tier_nodes:
                    label = node.name[:20]
                    lines.append(
                        f'    "{node.id}" [label="{label}", '
                        f'fillcolor="{node.color}", style=filled];'
                    )
                lines.append("  }")
                lines.append("")

        # Add edges
        for edge in edges:
            style = "solid" if edge.style == "solid" else "dashed"
            lines.append(
                f'  "{edge.source_id}" -> "{edge.target_id}" '
                f'[style={style}, penwidth={edge.width}];'
            )

        lines.append("}")
        return "\n".join(lines)

    def _to_cytoscape(
        self,
        nodes: list[SwarmNode],
        edges: list[SwarmEdge],
    ) -> dict[str, Any]:
        """Convert to Cytoscape.js format."""
        elements = []

        for node in nodes:
            elements.append({
                "group": "nodes",
                "data": {
                    "id": node.id,
                    "label": node.name,
                    "tier": node.tier.value,
                    "category": node.category,
                    "member_count": node.member_count,
                },
                "style": {
                    "background-color": node.color,
                    "width": node.size * 50,
                    "height": node.size * 50,
                },
            })

        for edge in edges:
            elements.append({
                "group": "edges",
                "data": {
                    "id": edge.id,
                    "source": edge.source_id,
                    "target": edge.target_id,
                    "weight": edge.strength,
                },
                "style": {
                    "width": edge.width,
                    "line-color": edge.color,
                    "line-style": edge.style,
                },
            })

        return {"elements": elements}

    def _to_d3(
        self,
        nodes: list[SwarmNode],
        edges: list[SwarmEdge],
    ) -> dict[str, Any]:
        """Convert to D3.js force-directed graph format."""
        return {
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "group": n.tier.value,
                    "size": n.size * 10,
                    "color": n.color,
                }
                for n in nodes
            ],
            "links": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "value": e.strength,
                }
                for e in edges
            ],
        }
