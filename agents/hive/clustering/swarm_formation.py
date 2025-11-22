"""
Swarm Formation - Algorithms for organizing parts into learning collectives.

Parts are organized into a 5-tier hierarchy:
- Tier 1: Global category swarms (50M+ members)
- Tier 2: Family swarms (type-level)
- Tier 3: Spec swarms (size/material-level)
- Tier 4: Context swarms (application-level)
- Tier 5: Experience swarms (behavioral-level)
"""

from dataclasses import dataclass
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import (
    Swarm,
    SwarmMembership,
    SwarmRole,
    SwarmTier,
)


@dataclass
class Part:
    """Minimal part representation for swarm formation."""
    id: UUID
    category: str
    part_type: str
    specifications: dict[str, Any]
    usage_contexts: list[str]
    consciousness_level: float
    experience_tags: list[str]

    # Optional detailed specs
    material: Optional[str] = None
    thread_spec: Optional[str] = None
    size_spec: Optional[str] = None


class SwarmRepository(Protocol):
    """Protocol for swarm data access."""

    async def get_swarm_by_key(self, key: str) -> Optional[Swarm]:
        """Retrieve swarm by unique key."""
        ...

    async def create_swarm(self, swarm: Swarm) -> Swarm:
        """Create a new swarm."""
        ...

    async def update_swarm(self, swarm: Swarm) -> Swarm:
        """Update existing swarm."""
        ...

    async def add_membership(self, membership: SwarmMembership) -> SwarmMembership:
        """Add part to swarm."""
        ...


class SwarmFormation:
    """
    Algorithms for organizing parts into learning collectives.
    """

    # Experience swarm definitions
    EXPERIENCE_SWARM_CRITERIA = {
        "survived_overload": {
            "name": "Parts That Survived Overload",
            "condition": lambda p: "overload_survivor" in p.experience_tags,
        },
        "premature_failure": {
            "name": "Parts That Failed Prematurely",
            "condition": lambda p: "premature_failure" in p.experience_tags,
        },
        "million_cycles": {
            "name": "Parts with 1M+ Cycles",
            "condition": lambda p: "high_cycle" in p.experience_tags,
        },
        "exceeded_design_life": {
            "name": "Parts That Exceeded Design Life",
            "condition": lambda p: "longevity_champion" in p.experience_tags,
        },
        "extreme_temperature": {
            "name": "Parts Operating in Extreme Temperatures",
            "condition": lambda p: "extreme_temp" in p.experience_tags,
        },
        "high_vibration": {
            "name": "Parts in High Vibration Environments",
            "condition": lambda p: "high_vibration" in p.experience_tags,
        },
        "corrosive_environment": {
            "name": "Parts in Corrosive Environments",
            "condition": lambda p: "corrosion_exposed" in p.experience_tags,
        },
    }

    def __init__(self, repository: SwarmRepository):
        self.repository = repository

    async def assign_part_to_swarms(self, part: Part) -> list[SwarmMembership]:
        """
        Determine which swarms a part should belong to.
        Parts typically belong to 5-15 swarms across tiers.

        Args:
            part: The part to assign to swarms

        Returns:
            List of SwarmMembership objects representing memberships
        """
        memberships = []

        # Tier 1: Global Category Swarm
        tier1_membership = await self._assign_global_swarm(part)
        memberships.append(tier1_membership)

        # Tier 2: Family Swarm
        tier2_membership = await self._assign_family_swarm(part)
        memberships.append(tier2_membership)

        # Tier 3: Spec Swarm
        tier3_membership = await self._assign_spec_swarm(part)
        memberships.append(tier3_membership)

        # Tier 4: Context Swarms (multiple based on usage)
        tier4_memberships = await self._assign_context_swarms(part)
        memberships.extend(tier4_memberships)

        # Tier 5: Experience Swarms (based on behaviors)
        tier5_memberships = await self._assign_experience_swarms(part)
        memberships.extend(tier5_memberships)

        return memberships

    async def _assign_global_swarm(self, part: Part) -> SwarmMembership:
        """Assign part to Tier 1 Global Category Swarm."""
        swarm_key = f"global:{part.category}"

        swarm = await self._get_or_create_swarm(
            tier=SwarmTier.GLOBAL,
            category=part.category,
            identifier=part.category,
            name=f"{part.category} Global Swarm",
            swarm_key=swarm_key,
        )

        role = self._determine_role(part)
        influence = self._calculate_influence(part)

        membership = SwarmMembership(
            part_id=part.id,
            swarm_id=swarm.id,
            role=role,
            influence_weight=influence,
        )

        await self.repository.add_membership(membership)
        return membership

    async def _assign_family_swarm(self, part: Part) -> SwarmMembership:
        """Assign part to Tier 2 Family Swarm."""
        swarm_key = f"family:{part.category}:{part.part_type}"

        swarm = await self._get_or_create_swarm(
            tier=SwarmTier.FAMILY,
            category=part.category,
            identifier=f"{part.category}:{part.part_type}",
            name=f"{part.part_type} Family Swarm",
            swarm_key=swarm_key,
        )

        role = self._determine_role(part)
        influence = self._calculate_influence(part)

        membership = SwarmMembership(
            part_id=part.id,
            swarm_id=swarm.id,
            role=role,
            influence_weight=influence,
        )

        await self.repository.add_membership(membership)
        return membership

    async def _assign_spec_swarm(self, part: Part) -> SwarmMembership:
        """Assign part to Tier 3 Spec Swarm."""
        spec_key = self._generate_spec_key(part)
        swarm_key = f"spec:{spec_key}"

        swarm = await self._get_or_create_swarm(
            tier=SwarmTier.SPEC,
            category=part.category,
            identifier=spec_key,
            name=f"{spec_key} Spec Swarm",
            swarm_key=swarm_key,
        )

        role = self._determine_role(part)
        influence = self._calculate_influence(part)

        membership = SwarmMembership(
            part_id=part.id,
            swarm_id=swarm.id,
            role=role,
            influence_weight=influence,
        )

        await self.repository.add_membership(membership)
        return membership

    async def _assign_context_swarms(self, part: Part) -> list[SwarmMembership]:
        """Assign part to Tier 4 Context Swarms based on usage."""
        memberships = []

        for context in part.usage_contexts:
            swarm_key = f"context:{context}"

            swarm = await self._get_or_create_swarm(
                tier=SwarmTier.CONTEXT,
                category=part.category,
                identifier=context,
                name=f"{context} Context Swarm",
                swarm_key=swarm_key,
            )

            role = self._determine_role(part)
            influence = self._calculate_influence(part)

            membership = SwarmMembership(
                part_id=part.id,
                swarm_id=swarm.id,
                role=role,
                influence_weight=influence,
            )

            await self.repository.add_membership(membership)
            memberships.append(membership)

        return memberships

    async def _assign_experience_swarms(self, part: Part) -> list[SwarmMembership]:
        """Assign part to Tier 5 Experience Swarms based on behaviors."""
        memberships = []

        for swarm_id, criteria in self.EXPERIENCE_SWARM_CRITERIA.items():
            if criteria["condition"](part):
                swarm_key = f"experience:{swarm_id}"

                swarm = await self._get_or_create_swarm(
                    tier=SwarmTier.EXPERIENCE,
                    category="experience",
                    identifier=swarm_id,
                    name=criteria["name"],
                    swarm_key=swarm_key,
                )

                # Experience swarms always use "contributor" role
                membership = SwarmMembership(
                    part_id=part.id,
                    swarm_id=swarm.id,
                    role=SwarmRole.CONTRIBUTOR,
                    influence_weight=self._calculate_influence(part),
                )

                await self.repository.add_membership(membership)
                memberships.append(membership)

        return memberships

    async def _get_or_create_swarm(
        self,
        tier: SwarmTier,
        category: str,
        identifier: str,
        name: str,
        swarm_key: str,
    ) -> Swarm:
        """Get existing swarm or create a new one."""
        existing = await self.repository.get_swarm_by_key(swarm_key)
        if existing:
            return existing

        new_swarm = Swarm(
            swarm_id=swarm_key,
            tier=tier,
            category=category,
            identifier=identifier,
            name=name,
        )

        return await self.repository.create_swarm(new_swarm)

    def _determine_role(self, part: Part) -> SwarmRole:
        """
        Determine part's role within a swarm based on consciousness level.

        Consciousness Levels -> Roles:
        - >= 4: Elder (guides and teaches)
        - >= 3: Mentor (shares experience)
        - >= 2: Contributor (active participant)
        - >= 1: Learner (absorbs knowledge)
        - < 1: Dormant (not yet active)
        """
        if part.consciousness_level >= 4:
            return SwarmRole.ELDER
        elif part.consciousness_level >= 3:
            return SwarmRole.MENTOR
        elif part.consciousness_level >= 2:
            return SwarmRole.CONTRIBUTOR
        elif part.consciousness_level >= 1:
            return SwarmRole.LEARNER
        else:
            return SwarmRole.DORMANT

    def _calculate_influence(self, part: Part) -> float:
        """
        Calculate a part's influence weight within swarms.

        Factors:
        - Consciousness level (primary factor)
        - Experience breadth (number of contexts)
        - Unique experiences (tags)
        """
        # Base influence from consciousness (0-1 scale, consciousness max ~5)
        consciousness_factor = min(part.consciousness_level / 5.0, 1.0)

        # Context breadth bonus (max 0.2 for 5+ contexts)
        context_factor = min(len(part.usage_contexts) / 25.0, 0.2)

        # Experience uniqueness bonus (max 0.1 for 5+ experience tags)
        experience_factor = min(len(part.experience_tags) / 50.0, 0.1)

        influence = (
            consciousness_factor * 0.7 +
            context_factor +
            experience_factor
        )

        return round(min(influence, 1.0), 3)

    def _generate_spec_key(self, part: Part) -> str:
        """
        Generate a unique specification key for Tier 3 swarm.
        Format varies by category.
        """
        specs = part.specifications

        if part.category.lower() == "fastener":
            # Example: "M8x1.25-Grade12.9-SteelAlloy"
            thread = specs.get("thread_spec", part.thread_spec or "unknown")
            grade = specs.get("grade", "unknown")
            material = specs.get("material", part.material or "unknown")
            return f"{thread}-{grade}-{material}"

        elif part.category.lower() == "bearing":
            # Example: "6205-2RS-Chrome"
            bearing_code = specs.get("bearing_code", "unknown")
            seal_type = specs.get("seal_type", "unknown")
            material = specs.get("material", part.material or "unknown")
            return f"{bearing_code}-{seal_type}-{material}"

        elif part.category.lower() == "seal":
            # Example: "NBR-30x3mm-ShoreA70"
            material = specs.get("material", part.material or "unknown")
            size = specs.get("size", part.size_spec or "unknown")
            hardness = specs.get("hardness", "unknown")
            return f"{material}-{size}-{hardness}"

        else:
            # Generic: use part type and primary specs
            type_key = part.part_type
            primary_spec = specs.get("primary_spec", "unknown")
            return f"{type_key}-{primary_spec}"


async def batch_assign_parts(
    formation: SwarmFormation,
    parts: list[Part],
) -> dict[UUID, list[SwarmMembership]]:
    """
    Batch assign multiple parts to swarms.

    Args:
        formation: SwarmFormation instance
        parts: List of parts to assign

    Returns:
        Dictionary mapping part IDs to their memberships
    """
    results = {}
    for part in parts:
        memberships = await formation.assign_part_to_swarms(part)
        results[part.id] = memberships
    return results
