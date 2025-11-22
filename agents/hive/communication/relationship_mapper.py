"""
Relationship Mapper - Maps relationships between swarms.

Maintains the graph of swarm relationships for efficient
inter-swarm communication routing.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol
from uuid import UUID

from ..models import Swarm


@dataclass
class SwarmRelationship:
    """A relationship between two swarms."""
    source_swarm_id: UUID
    target_swarm_id: UUID
    relationship_type: str  # "mating", "compatible", "similar", "hierarchical"
    strength: float  # 0-1, how strong the relationship is
    bidirectional: bool
    last_communication: Optional[datetime] = None
    communication_count: int = 0


@dataclass
class RelationshipGraph:
    """Graph representation of swarm relationships."""
    swarms: dict[UUID, Swarm]
    relationships: list[SwarmRelationship]
    adjacency: dict[UUID, list[UUID]]


class RelationshipRepository(Protocol):
    """Protocol for relationship data operations."""

    async def get_relationships(
        self,
        swarm_id: UUID,
    ) -> list[SwarmRelationship]:
        """Get all relationships for a swarm."""
        ...

    async def add_relationship(
        self,
        relationship: SwarmRelationship,
    ) -> None:
        """Add a relationship."""
        ...

    async def update_relationship(
        self,
        relationship: SwarmRelationship,
    ) -> None:
        """Update a relationship."""
        ...

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def find_swarms_by_category(self, category: str) -> list[Swarm]:
        """Find swarms by category."""
        ...


class RelationshipMapper:
    """
    Maps and manages relationships between swarms.
    """

    # Standard relationship types
    RELATIONSHIP_MATING = "mating"        # Parts that mate together
    RELATIONSHIP_COMPATIBLE = "compatible" # Parts that can be used together
    RELATIONSHIP_SIMILAR = "similar"       # Similar parts
    RELATIONSHIP_HIERARCHICAL = "hierarchical"  # Parent/child swarms

    # Category relationships (what mates with what)
    MATING_CATEGORIES = {
        "bolts": ["nuts", "washers", "threaded_holes"],
        "nuts": ["bolts", "studs", "threaded_rods"],
        "bearings": ["shafts", "housings"],
        "shafts": ["bearings", "seals", "gears", "pulleys"],
        "seals": ["shafts", "housings", "pistons"],
        "gears": ["shafts", "bearings", "other_gears"],
        "pistons": ["rings", "pins", "cylinders"],
        "valves": ["springs", "seats", "guides"],
        "springs": ["valves", "fasteners", "mechanisms"],
        "gaskets": ["flanges", "manifolds", "covers"],
    }

    def __init__(self, repository: RelationshipRepository):
        self.repository = repository

    async def get_related_swarms(
        self,
        swarm_id: UUID,
        relationship_type: Optional[str] = None,
    ) -> list[Swarm]:
        """
        Get all swarms related to the given swarm.

        Args:
            swarm_id: The swarm to find relations for
            relationship_type: Optional filter by relationship type

        Returns:
            List of related swarms
        """
        relationships = await self.repository.get_relationships(swarm_id)

        if relationship_type:
            relationships = [r for r in relationships if r.relationship_type == relationship_type]

        related_swarms = []
        for rel in relationships:
            target_id = rel.target_swarm_id if rel.source_swarm_id == swarm_id else rel.source_swarm_id
            swarm = await self.repository.get_swarm(target_id)
            if swarm:
                related_swarms.append(swarm)

        return related_swarms

    async def get_mating_swarms(self, swarm_id: UUID) -> list[Swarm]:
        """Get swarms that mate with the given swarm."""
        return await self.get_related_swarms(swarm_id, self.RELATIONSHIP_MATING)

    async def get_compatible_swarms(self, swarm_id: UUID) -> list[Swarm]:
        """Get swarms compatible with the given swarm."""
        return await self.get_related_swarms(swarm_id, self.RELATIONSHIP_COMPATIBLE)

    async def create_relationship(
        self,
        source_swarm_id: UUID,
        target_swarm_id: UUID,
        relationship_type: str,
        strength: float = 0.5,
        bidirectional: bool = True,
    ) -> SwarmRelationship:
        """
        Create a relationship between two swarms.

        Args:
            source_swarm_id: Source swarm
            target_swarm_id: Target swarm
            relationship_type: Type of relationship
            strength: Relationship strength
            bidirectional: Whether relationship goes both ways

        Returns:
            Created relationship
        """
        relationship = SwarmRelationship(
            source_swarm_id=source_swarm_id,
            target_swarm_id=target_swarm_id,
            relationship_type=relationship_type,
            strength=strength,
            bidirectional=bidirectional,
        )

        await self.repository.add_relationship(relationship)

        # If bidirectional, create reverse relationship
        if bidirectional:
            reverse = SwarmRelationship(
                source_swarm_id=target_swarm_id,
                target_swarm_id=source_swarm_id,
                relationship_type=relationship_type,
                strength=strength,
                bidirectional=True,
            )
            await self.repository.add_relationship(reverse)

        return relationship

    async def discover_relationships(
        self,
        swarm: Swarm,
    ) -> list[SwarmRelationship]:
        """
        Discover potential relationships for a swarm based on its category.

        Args:
            swarm: The swarm to find relationships for

        Returns:
            List of discovered relationships
        """
        discovered = []
        category = swarm.category.lower()

        # Find mating categories
        mating_categories = self.MATING_CATEGORIES.get(category, [])

        for mating_category in mating_categories:
            # Find swarms in mating category
            mating_swarms = await self.repository.find_swarms_by_category(mating_category)

            for mating_swarm in mating_swarms:
                # Only relate swarms at similar tiers
                if abs(swarm.tier.value - mating_swarm.tier.value) <= 1:
                    relationship = SwarmRelationship(
                        source_swarm_id=swarm.id,
                        target_swarm_id=mating_swarm.id,
                        relationship_type=self.RELATIONSHIP_MATING,
                        strength=0.5,
                        bidirectional=True,
                    )
                    discovered.append(relationship)

        return discovered

    async def strengthen_relationship(
        self,
        source_swarm_id: UUID,
        target_swarm_id: UUID,
        increment: float = 0.1,
    ) -> None:
        """
        Strengthen a relationship after successful communication.

        Args:
            source_swarm_id: Source swarm
            target_swarm_id: Target swarm
            increment: Amount to increase strength
        """
        relationships = await self.repository.get_relationships(source_swarm_id)

        for rel in relationships:
            if rel.target_swarm_id == target_swarm_id:
                rel.strength = min(1.0, rel.strength + increment)
                rel.last_communication = datetime.utcnow()
                rel.communication_count += 1
                await self.repository.update_relationship(rel)
                break

    async def build_relationship_graph(
        self,
        root_swarm_id: UUID,
        depth: int = 2,
    ) -> RelationshipGraph:
        """
        Build a relationship graph starting from a swarm.

        Args:
            root_swarm_id: Starting swarm
            depth: How many levels to traverse

        Returns:
            Relationship graph
        """
        visited: set[UUID] = set()
        swarms: dict[UUID, Swarm] = {}
        all_relationships: list[SwarmRelationship] = []
        adjacency: dict[UUID, list[UUID]] = {}

        queue = [(root_swarm_id, 0)]

        while queue:
            swarm_id, level = queue.pop(0)

            if swarm_id in visited or level > depth:
                continue

            visited.add(swarm_id)

            swarm = await self.repository.get_swarm(swarm_id)
            if swarm:
                swarms[swarm_id] = swarm

            relationships = await self.repository.get_relationships(swarm_id)
            adjacency[swarm_id] = []

            for rel in relationships:
                all_relationships.append(rel)
                target_id = rel.target_swarm_id if rel.source_swarm_id == swarm_id else rel.source_swarm_id
                adjacency[swarm_id].append(target_id)

                if target_id not in visited:
                    queue.append((target_id, level + 1))

        return RelationshipGraph(
            swarms=swarms,
            relationships=all_relationships,
            adjacency=adjacency,
        )

    def find_shortest_path(
        self,
        graph: RelationshipGraph,
        source_id: UUID,
        target_id: UUID,
    ) -> Optional[list[UUID]]:
        """
        Find shortest path between two swarms in a graph.

        Args:
            graph: Relationship graph
            source_id: Starting swarm
            target_id: Target swarm

        Returns:
            List of swarm IDs in path, or None if no path
        """
        if source_id not in graph.adjacency:
            return None

        visited: set[UUID] = set()
        queue: list[list[UUID]] = [[source_id]]

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current == target_id:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in graph.adjacency.get(current, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append(new_path)

        return None
