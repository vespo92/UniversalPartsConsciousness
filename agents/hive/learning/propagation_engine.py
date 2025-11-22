"""
Propagation Engine - Propagates learnings across swarms.

When a part learns something, this engine determines which swarms
should receive the learning and updates their collective knowledge.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import (
    Learning,
    LearningType,
    PropagationResult,
    Swarm,
    SwarmMembership,
)


@dataclass
class SwarmKnowledgeDelta:
    """Change to swarm's collective knowledge from a learning."""
    swarm_id: UUID
    learning_id: UUID
    knowledge_key: str
    old_value: Any
    new_value: Any
    confidence_change: float


class PropagationRepository(Protocol):
    """Protocol for propagation data access."""

    async def get_part_swarms(self, part_id: UUID) -> list[Swarm]:
        """Get all swarms a part belongs to."""
        ...

    async def get_swarm_members(
        self,
        swarm_id: UUID,
        exclude_part_id: Optional[UUID] = None,
        limit: int = 1000,
    ) -> list[SwarmMembership]:
        """Get members of a swarm."""
        ...

    async def update_swarm_knowledge(
        self,
        swarm_id: UUID,
        knowledge_update: dict[str, Any],
    ) -> None:
        """Update a swarm's collective knowledge."""
        ...

    async def record_learning(
        self,
        swarm_id: UUID,
        learning: Learning,
        propagation_strength: float,
    ) -> None:
        """Record that a learning was propagated to a swarm."""
        ...

    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        """Get swarm by ID."""
        ...

    async def notify_part(
        self,
        part_id: UUID,
        learning: Learning,
        propagation_strength: float,
    ) -> None:
        """Notify a part about a propagated learning."""
        ...


class PropagationEngine:
    """
    Propagates learnings from individual experiences to swarm collective knowledge.
    """

    # Weight factors for propagation strength calculation
    CONSCIOUSNESS_WEIGHT = 0.3
    CONFIDENCE_WEIGHT = 0.3
    RELEVANCE_WEIGHT = 0.2
    NOVELTY_WEIGHT = 0.2

    # Minimum threshold for propagation
    MIN_PROPAGATION_STRENGTH = 0.2

    def __init__(self, repository: PropagationRepository):
        self.repository = repository

    async def propagate_learning(
        self,
        source_part_id: UUID,
        learning: Learning,
    ) -> PropagationResult:
        """
        Propagate a learning from a source part to relevant swarms.

        Args:
            source_part_id: The part that generated the learning
            learning: The learning to propagate

        Returns:
            Result of the propagation
        """
        start_time = datetime.utcnow()

        # Get swarms the source part belongs to
        source_swarms = await self.repository.get_part_swarms(source_part_id)

        if not source_swarms:
            return PropagationResult(
                learning=learning,
                success=False,
                errors=["Source part has no swarm memberships"],
            )

        # Identify relevant swarms for this learning
        relevant_swarms = self._identify_relevant_swarms(source_swarms, learning)

        swarms_updated = 0
        total_members_affected = 0
        knowledge_deltas = {}
        errors = []

        # Propagate to each relevant swarm
        for swarm in relevant_swarms:
            try:
                # Calculate propagation strength for this swarm
                propagation_strength = self._calculate_propagation_strength(
                    learning, swarm
                )

                if propagation_strength < self.MIN_PROPAGATION_STRENGTH:
                    continue

                # Update swarm's collective knowledge
                delta = await self._update_swarm_knowledge(
                    swarm, learning, propagation_strength
                )
                if delta:
                    knowledge_deltas[str(swarm.id)] = delta

                # Record learning in swarm
                await self.repository.record_learning(
                    swarm.id, learning, propagation_strength
                )

                # Propagate to individual members
                members_affected = await self._propagate_to_members(
                    swarm, learning, propagation_strength, source_part_id
                )
                total_members_affected += members_affected

                swarms_updated += 1

            except Exception as e:
                errors.append(f"Error propagating to swarm {swarm.id}: {str(e)}")

        end_time = datetime.utcnow()
        propagation_time_ms = (end_time - start_time).total_seconds() * 1000

        return PropagationResult(
            learning=learning,
            swarms_targeted=len(relevant_swarms),
            swarms_updated=swarms_updated,
            members_affected=total_members_affected,
            propagation_strength=learning.propagation_strength,
            propagation_time_ms=propagation_time_ms,
            success=len(errors) == 0,
            errors=errors,
            swarm_knowledge_deltas=knowledge_deltas,
        )

    def _identify_relevant_swarms(
        self,
        swarms: list[Swarm],
        learning: Learning,
    ) -> list[Swarm]:
        """
        Identify which swarms should receive the learning.

        Some learnings apply broadly, others are more specific.
        """
        relevant = []

        for swarm in swarms:
            relevance = self._calculate_relevance(swarm, learning)
            if relevance > 0.3:  # Minimum relevance threshold
                relevant.append(swarm)

        # Sort by relevance (most relevant first)
        relevant.sort(
            key=lambda s: self._calculate_relevance(s, learning),
            reverse=True
        )

        return relevant

    def _calculate_relevance(
        self,
        swarm: Swarm,
        learning: Learning,
    ) -> float:
        """
        Calculate how relevant a learning is to a swarm.

        Different learning types have different relevance patterns.
        """
        applicability = learning.applicability
        learning_type = learning.learning_type

        # Base relevance by swarm tier (lower tiers = broader relevance)
        tier_factor = {
            1: 0.3,  # Global - low individual relevance
            2: 0.5,  # Family - moderate relevance
            3: 0.9,  # Spec - high relevance
            4: 0.8,  # Context - high relevance
            5: 0.7,  # Experience - moderate relevance
        }.get(swarm.tier.value, 0.5)

        # Adjust by applicability
        applicability_factor = {
            "similar_specs": 0.9 if swarm.tier.value >= 3 else 0.4,
            "similar_conditions": 0.7,
            "similar_usage": 0.8 if swarm.tier.value >= 4 else 0.5,
            "similar_environment": 0.7,
            "similar_application": 0.8,
        }.get(applicability, 0.5)

        # Adjust by learning type
        type_factor = {
            LearningType.FAILURE_MODE: 1.0,  # Failures are always relevant
            LearningType.SURVIVAL_LIMIT: 0.9,
            LearningType.LONGEVITY_FACTOR: 0.8,
            LearningType.ENVIRONMENTAL_ADAPTATION: 0.7,
            LearningType.USAGE_PATTERN: 0.6,
            LearningType.COMPATIBILITY_INSIGHT: 0.8,
            LearningType.MAINTENANCE_WISDOM: 0.7,
        }.get(learning_type, 0.5)

        return tier_factor * applicability_factor * type_factor

    def _calculate_propagation_strength(
        self,
        learning: Learning,
        swarm: Swarm,
    ) -> float:
        """
        Calculate how strongly a learning should propagate.

        Factors:
        - Source part consciousness level (higher = more trusted)
        - Learning confidence
        - Swarm relevance
        - Learning novelty
        """
        consciousness_factor = min(learning.source_consciousness_level / 5.0, 1.0)
        confidence_factor = learning.confidence
        relevance_factor = self._calculate_relevance(swarm, learning)
        novelty_factor = learning.novelty_score

        strength = (
            consciousness_factor * self.CONSCIOUSNESS_WEIGHT +
            confidence_factor * self.CONFIDENCE_WEIGHT +
            relevance_factor * self.RELEVANCE_WEIGHT +
            novelty_factor * self.NOVELTY_WEIGHT
        )

        return round(min(strength, 1.0), 3)

    async def _update_swarm_knowledge(
        self,
        swarm: Swarm,
        learning: Learning,
        propagation_strength: float,
    ) -> Optional[SwarmKnowledgeDelta]:
        """
        Update a swarm's collective knowledge with a learning.

        Uses weighted averaging to incorporate new knowledge.
        """
        learning_type = learning.learning_type.value
        knowledge_key = f"{learning_type}:{self._get_content_key(learning)}"

        # Get current knowledge
        current_knowledge = swarm.collective_knowledge.get(knowledge_key, {})

        # Merge new learning with existing knowledge
        if current_knowledge:
            # Weighted merge based on existing confidence and propagation strength
            old_weight = current_knowledge.get("confidence", 0.5)
            new_weight = propagation_strength * learning.confidence
            total_weight = old_weight + new_weight

            merged_confidence = (
                old_weight * current_knowledge.get("confidence", 0.5) +
                new_weight * learning.confidence
            ) / total_weight

            merged_content = self._merge_content(
                current_knowledge.get("content", {}),
                learning.content,
                old_weight / total_weight,
                new_weight / total_weight,
            )

            new_knowledge = {
                "content": merged_content,
                "confidence": merged_confidence,
                "sample_count": current_knowledge.get("sample_count", 0) + 1,
                "last_updated": datetime.utcnow().isoformat(),
            }
        else:
            # First learning of this type
            new_knowledge = {
                "content": learning.content,
                "confidence": learning.confidence * propagation_strength,
                "sample_count": 1,
                "last_updated": datetime.utcnow().isoformat(),
            }

        # Update swarm
        knowledge_update = {knowledge_key: new_knowledge}
        await self.repository.update_swarm_knowledge(swarm.id, knowledge_update)

        return SwarmKnowledgeDelta(
            swarm_id=swarm.id,
            learning_id=learning.id,
            knowledge_key=knowledge_key,
            old_value=current_knowledge,
            new_value=new_knowledge,
            confidence_change=new_knowledge["confidence"] - current_knowledge.get("confidence", 0),
        )

    def _get_content_key(self, learning: Learning) -> str:
        """Generate a key for the learning content."""
        content = learning.content

        if learning.learning_type == LearningType.FAILURE_MODE:
            return content.get("failure_type", "unknown")
        elif learning.learning_type == LearningType.SURVIVAL_LIMIT:
            return "survival_data"
        elif learning.learning_type == LearningType.LONGEVITY_FACTOR:
            return "longevity_data"
        elif learning.learning_type == LearningType.ENVIRONMENTAL_ADAPTATION:
            challenges = content.get("environmental_challenges", [])
            return "_".join(sorted(challenges)) if challenges else "general"
        else:
            return "general"

    def _merge_content(
        self,
        old_content: dict[str, Any],
        new_content: dict[str, Any],
        old_weight: float,
        new_weight: float,
    ) -> dict[str, Any]:
        """
        Merge two content dictionaries with weights.

        Numeric values are averaged, lists are combined, other types use the newer value.
        """
        merged = {}
        all_keys = set(old_content.keys()) | set(new_content.keys())

        for key in all_keys:
            old_val = old_content.get(key)
            new_val = new_content.get(key)

            if old_val is None:
                merged[key] = new_val
            elif new_val is None:
                merged[key] = old_val
            elif isinstance(old_val, (int, float)) and isinstance(new_val, (int, float)):
                # Weighted average for numbers
                merged[key] = old_val * old_weight + new_val * new_weight
            elif isinstance(old_val, list) and isinstance(new_val, list):
                # Combine and deduplicate lists
                combined = list(set(old_val + new_val))
                merged[key] = combined
            elif isinstance(old_val, dict) and isinstance(new_val, dict):
                # Recursive merge for nested dicts
                merged[key] = self._merge_content(old_val, new_val, old_weight, new_weight)
            else:
                # Use newer value for other types
                merged[key] = new_val

        return merged

    async def _propagate_to_members(
        self,
        swarm: Swarm,
        learning: Learning,
        propagation_strength: float,
        source_part_id: UUID,
    ) -> int:
        """
        Propagate learning to individual swarm members.

        Returns the number of members affected.
        """
        # Get members (excluding source)
        members = await self.repository.get_swarm_members(
            swarm.id,
            exclude_part_id=source_part_id,
            limit=1000,  # Limit batch size
        )

        if not members:
            return 0

        # Notify members asynchronously
        tasks = []
        for member in members:
            # Adjust strength by member's influence (higher influence = faster learning)
            member_strength = propagation_strength * (0.7 + 0.3 * member.influence_weight)
            tasks.append(
                self.repository.notify_part(
                    member.part_id,
                    learning,
                    member_strength,
                )
            )

        # Execute in batches to avoid overwhelming the system
        batch_size = 100
        affected_count = 0

        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            await asyncio.gather(*batch, return_exceptions=True)
            affected_count += len(batch)

        return affected_count


async def propagate_batch(
    engine: PropagationEngine,
    learnings: list[tuple[UUID, Learning]],
) -> list[PropagationResult]:
    """
    Propagate multiple learnings in batch.

    Args:
        engine: PropagationEngine instance
        learnings: List of (source_part_id, learning) tuples

    Returns:
        List of propagation results
    """
    tasks = [
        engine.propagate_learning(part_id, learning)
        for part_id, learning in learnings
    ]
    return await asyncio.gather(*tasks)
