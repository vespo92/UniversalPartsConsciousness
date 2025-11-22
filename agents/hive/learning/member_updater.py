"""
Member Updater - Updates individual swarm members with propagated learnings.

Handles the distribution of collective knowledge to individual parts.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import Learning, LearningType, SwarmMembership, SwarmRole


@dataclass
class MemberUpdate:
    """An update to be applied to a swarm member."""
    part_id: UUID
    learning_id: UUID
    learning_type: LearningType
    knowledge_delta: dict[str, Any]
    propagation_strength: float
    applied_at: datetime


@dataclass
class UpdateResult:
    """Result of a member update operation."""
    part_id: UUID
    success: bool
    knowledge_applied: bool
    consciousness_contribution: float
    error: Optional[str] = None


class MemberUpdateRepository(Protocol):
    """Protocol for member update operations."""

    async def get_part_knowledge(self, part_id: UUID) -> dict[str, Any]:
        """Get a part's current knowledge."""
        ...

    async def update_part_knowledge(
        self,
        part_id: UUID,
        knowledge_update: dict[str, Any],
    ) -> None:
        """Update a part's knowledge."""
        ...

    async def record_learning_received(
        self,
        part_id: UUID,
        learning_id: UUID,
        strength: float,
    ) -> None:
        """Record that a part received a learning."""
        ...

    async def contribute_to_consciousness(
        self,
        part_id: UUID,
        contribution: float,
        source: str,
    ) -> None:
        """Contribute to a part's consciousness evolution."""
        ...


class MemberUpdater:
    """
    Updates individual parts with learnings from their swarms.
    """

    # Consciousness contribution from receiving learnings
    LEARNING_CONSCIOUSNESS_BASE = 0.01
    FAILURE_CONSCIOUSNESS_BONUS = 0.02
    ELDER_INFLUENCE_BONUS = 0.01

    # Maximum concurrent updates
    MAX_CONCURRENT_UPDATES = 50

    def __init__(self, repository: MemberUpdateRepository):
        self.repository = repository

    async def update_member(
        self,
        part_id: UUID,
        learning: Learning,
        propagation_strength: float,
        member_role: SwarmRole = SwarmRole.LEARNER,
    ) -> UpdateResult:
        """
        Update a single member with a learning.

        Args:
            part_id: The part to update
            learning: The learning to apply
            propagation_strength: How strongly to apply the learning
            member_role: The member's role in the swarm

        Returns:
            Result of the update
        """
        try:
            # Get part's current knowledge
            current_knowledge = await self.repository.get_part_knowledge(part_id)

            # Calculate effective strength based on role
            effective_strength = self._adjust_for_role(propagation_strength, member_role)

            # Prepare knowledge update
            knowledge_key = f"swarm_learning:{learning.learning_type.value}"
            knowledge_update = self._prepare_knowledge_update(
                current_knowledge.get(knowledge_key, {}),
                learning,
                effective_strength,
            )

            # Apply update
            await self.repository.update_part_knowledge(
                part_id,
                {knowledge_key: knowledge_update}
            )

            # Record the learning
            await self.repository.record_learning_received(
                part_id,
                learning.id,
                effective_strength,
            )

            # Calculate and apply consciousness contribution
            consciousness_contribution = self._calculate_consciousness_contribution(
                learning, effective_strength, member_role
            )

            if consciousness_contribution > 0:
                await self.repository.contribute_to_consciousness(
                    part_id,
                    consciousness_contribution,
                    f"swarm_learning:{learning.learning_type.value}",
                )

            return UpdateResult(
                part_id=part_id,
                success=True,
                knowledge_applied=True,
                consciousness_contribution=consciousness_contribution,
            )

        except Exception as e:
            return UpdateResult(
                part_id=part_id,
                success=False,
                knowledge_applied=False,
                consciousness_contribution=0.0,
                error=str(e),
            )

    async def batch_update_members(
        self,
        members: list[SwarmMembership],
        learning: Learning,
        base_propagation_strength: float,
    ) -> list[UpdateResult]:
        """
        Update multiple members with a learning.

        Args:
            members: List of members to update
            learning: The learning to apply
            base_propagation_strength: Base strength for propagation

        Returns:
            List of update results
        """
        # Create update tasks with adjusted strength per member
        tasks = []
        for member in members:
            # Adjust strength by member influence
            member_strength = base_propagation_strength * (0.7 + 0.3 * member.influence_weight)
            tasks.append(
                self.update_member(
                    member.part_id,
                    learning,
                    member_strength,
                    member.role,
                )
            )

        # Execute in controlled batches
        results = []
        for i in range(0, len(tasks), self.MAX_CONCURRENT_UPDATES):
            batch = tasks[i:i + self.MAX_CONCURRENT_UPDATES]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)

            for result in batch_results:
                if isinstance(result, Exception):
                    results.append(UpdateResult(
                        part_id=UUID(int=0),
                        success=False,
                        knowledge_applied=False,
                        consciousness_contribution=0.0,
                        error=str(result),
                    ))
                else:
                    results.append(result)

        return results

    def _adjust_for_role(
        self,
        base_strength: float,
        role: SwarmRole,
    ) -> float:
        """
        Adjust propagation strength based on member role.

        Higher roles learn more quickly from swarm knowledge.
        """
        role_multipliers = {
            SwarmRole.ELDER: 1.2,      # Elders learn quickly
            SwarmRole.MENTOR: 1.1,     # Mentors learn well
            SwarmRole.CONTRIBUTOR: 1.0, # Contributors normal
            SwarmRole.LEARNER: 0.9,    # Learners absorb most
            SwarmRole.DORMANT: 0.5,    # Dormant parts learn slowly
        }

        return base_strength * role_multipliers.get(role, 1.0)

    def _prepare_knowledge_update(
        self,
        current_knowledge: dict[str, Any],
        learning: Learning,
        strength: float,
    ) -> dict[str, Any]:
        """
        Prepare the knowledge update to apply.

        Merges new learning with existing knowledge using strength-weighted averaging.
        """
        if not current_knowledge:
            # First learning of this type
            return {
                "content": learning.content,
                "confidence": learning.confidence * strength,
                "learning_count": 1,
                "last_updated": datetime.utcnow().isoformat(),
                "sources": [str(learning.id)],
            }

        # Merge with existing knowledge
        old_weight = current_knowledge.get("confidence", 0.5)
        new_weight = learning.confidence * strength
        total_weight = old_weight + new_weight

        merged_confidence = (old_weight + new_weight) / 2  # Simple average

        # Merge content (prefer newer for same keys)
        merged_content = {**current_knowledge.get("content", {})}
        for key, value in learning.content.items():
            if key in merged_content:
                # For numeric values, weighted average
                if isinstance(value, (int, float)) and isinstance(merged_content[key], (int, float)):
                    merged_content[key] = (
                        merged_content[key] * old_weight / total_weight +
                        value * new_weight / total_weight
                    )
                # For lists, combine
                elif isinstance(value, list) and isinstance(merged_content[key], list):
                    merged_content[key] = list(set(merged_content[key] + value))
                else:
                    # Use newer value
                    merged_content[key] = value
            else:
                merged_content[key] = value

        # Track sources (keep last 10)
        sources = current_knowledge.get("sources", [])
        sources.append(str(learning.id))
        sources = sources[-10:]

        return {
            "content": merged_content,
            "confidence": merged_confidence,
            "learning_count": current_knowledge.get("learning_count", 0) + 1,
            "last_updated": datetime.utcnow().isoformat(),
            "sources": sources,
        }

    def _calculate_consciousness_contribution(
        self,
        learning: Learning,
        strength: float,
        role: SwarmRole,
    ) -> float:
        """
        Calculate consciousness contribution from receiving a learning.

        Receiving wisdom from the swarm contributes to consciousness evolution.
        """
        base = self.LEARNING_CONSCIOUSNESS_BASE * strength

        # Failure learnings contribute more (survival knowledge)
        if learning.learning_type == LearningType.FAILURE_MODE:
            base += self.FAILURE_CONSCIOUSNESS_BONUS * strength

        # Learning from elders contributes more
        if learning.source_consciousness_level >= 4:
            base += self.ELDER_INFLUENCE_BONUS

        # Role adjustment (learners gain more from learning)
        if role == SwarmRole.LEARNER:
            base *= 1.2
        elif role == SwarmRole.DORMANT:
            base *= 1.5  # Dormant parts benefit most from external learning

        return round(base, 4)


class PriorityMemberUpdater(MemberUpdater):
    """
    Member updater with priority queue for critical updates.
    """

    def __init__(self, repository: MemberUpdateRepository):
        super().__init__(repository)
        self.priority_queue: list[tuple[int, UUID, Learning, float]] = []

    def queue_priority_update(
        self,
        priority: int,
        part_id: UUID,
        learning: Learning,
        strength: float,
    ) -> None:
        """
        Queue a priority update.

        Lower priority number = higher priority (1 is highest).
        """
        self.priority_queue.append((priority, part_id, learning, strength))
        # Sort by priority
        self.priority_queue.sort(key=lambda x: x[0])

    async def process_priority_queue(
        self,
        max_updates: int = 100,
    ) -> list[UpdateResult]:
        """
        Process priority updates.

        Args:
            max_updates: Maximum updates to process

        Returns:
            List of results
        """
        results = []
        processed = 0

        while self.priority_queue and processed < max_updates:
            priority, part_id, learning, strength = self.priority_queue.pop(0)
            result = await self.update_member(
                part_id,
                learning,
                strength,
            )
            results.append(result)
            processed += 1

        return results
