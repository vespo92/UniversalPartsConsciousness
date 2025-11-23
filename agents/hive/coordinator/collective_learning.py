"""
Collective Learning Engine - "One Learns, All Learn"

This is the heart of the HIVE's collective intelligence. When any part
in the swarm learns something—whether through failure, success, or
adaptation—that knowledge immediately ripples through to all related parts.

The engine implements different propagation strategies based on:
- Learning urgency (critical safety vs. gradual insight)
- Swarm relationships (same spec, same context, same experience)
- Consciousness levels (elders mentor learners)
- Knowledge novelty (new insights spread faster)
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional
from uuid import UUID, uuid4

from ..models import (
    Learning,
    LearningType,
    PropagationResult,
    Swarm,
    SwarmMembership,
    SwarmRole,
    SwarmTier,
)


class LearningPropagationStrategy(Enum):
    """Strategies for propagating learnings through the collective."""

    # Immediate broadcast to all swarms (for critical safety)
    EMERGENCY_BROADCAST = "emergency_broadcast"

    # Ripple outward from source swarm (standard learning)
    RIPPLE_PROPAGATION = "ripple_propagation"

    # Targeted to specific swarm tiers (contextual learning)
    TIER_TARGETED = "tier_targeted"

    # Mentor-to-learner transmission (consciousness-based)
    MENTORSHIP_CASCADE = "mentorship_cascade"

    # Cross-pollination between related swarms
    CROSS_POLLINATION = "cross_pollination"


@dataclass
class CollectiveInsight:
    """
    An insight derived from collective learning patterns.

    When multiple parts learn similar things, the collective insight
    emerges with higher confidence and broader applicability.
    """
    id: UUID = field(default_factory=uuid4)

    # Source learnings that contributed
    contributing_learnings: list[UUID] = field(default_factory=list)
    contributing_parts: list[UUID] = field(default_factory=list)

    # The synthesized insight
    insight_type: LearningType = LearningType.USAGE_PATTERN
    content: dict[str, Any] = field(default_factory=dict)

    # Confidence increases with corroboration
    confidence: float = 0.0
    corroboration_count: int = 0

    # Scope
    applicability: str = "swarm_wide"
    affected_swarm_ids: list[UUID] = field(default_factory=list)

    # Timestamps
    first_observed_at: datetime = field(default_factory=datetime.utcnow)
    last_corroborated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LearningCascade:
    """
    Tracks a learning as it cascades through the swarm network.

    "One learns, all learn" - this tracks the journey of that learning.
    """
    id: UUID = field(default_factory=uuid4)

    # Origin
    source_learning_id: UUID = field(default_factory=uuid4)
    source_part_id: UUID = field(default_factory=uuid4)
    source_swarm_id: UUID = field(default_factory=uuid4)

    # Propagation tracking
    strategy: LearningPropagationStrategy = LearningPropagationStrategy.RIPPLE_PROPAGATION
    swarms_reached: list[UUID] = field(default_factory=list)
    parts_reached: int = 0

    # Cascade metrics
    propagation_depth: int = 0  # How many hops from source
    propagation_velocity: float = 0.0  # Swarms per second
    total_impact_score: float = 0.0

    # Status
    is_complete: bool = False
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


@dataclass
class CollectiveLearningConfig:
    """Configuration for the collective learning engine."""

    # Propagation thresholds
    min_confidence_to_propagate: float = 0.3
    emergency_confidence_override: float = 0.9

    # Cascade limits
    max_propagation_depth: int = 5
    max_concurrent_cascades: int = 100
    cascade_timeout_seconds: float = 30.0

    # Corroboration settings
    min_corroboration_for_insight: int = 3
    corroboration_window_hours: int = 168  # 1 week

    # Mentorship settings
    elder_teaching_multiplier: float = 1.5
    mentor_teaching_multiplier: float = 1.2

    # Cross-pollination
    cross_pollination_probability: float = 0.3
    max_cross_pollination_swarms: int = 5


class CollectiveLearningEngine:
    """
    The Collective Learning Engine - where "one learns, all learn" happens.

    This engine takes individual learnings and propagates them through
    the entire swarm network, ensuring that knowledge gained by any
    part benefits all similar parts instantly.
    """

    def __init__(
        self,
        config: Optional[CollectiveLearningConfig] = None,
    ):
        self.config = config or CollectiveLearningConfig()
        self._active_cascades: dict[UUID, LearningCascade] = {}
        self._collective_insights: dict[UUID, CollectiveInsight] = {}
        self._propagation_handlers: dict[LearningPropagationStrategy, Callable] = {}

        # Statistics
        self._total_learnings_propagated = 0
        self._total_parts_educated = 0
        self._collective_insights_discovered = 0

        # Register propagation handlers
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register propagation strategy handlers."""
        self._propagation_handlers = {
            LearningPropagationStrategy.EMERGENCY_BROADCAST: self._handle_emergency_broadcast,
            LearningPropagationStrategy.RIPPLE_PROPAGATION: self._handle_ripple_propagation,
            LearningPropagationStrategy.TIER_TARGETED: self._handle_tier_targeted,
            LearningPropagationStrategy.MENTORSHIP_CASCADE: self._handle_mentorship_cascade,
            LearningPropagationStrategy.CROSS_POLLINATION: self._handle_cross_pollination,
        }

    # =========================================================================
    # CORE PROPAGATION: "One Learns, All Learn"
    # =========================================================================

    async def propagate_to_collective(
        self,
        learning: Learning,
        source_part_id: UUID,
        source_swarm: Swarm,
        all_swarms: list[Swarm],
        get_swarm_members: Callable[[UUID], list[SwarmMembership]],
    ) -> LearningCascade:
        """
        Propagate a learning to the entire collective.

        This is the main entry point - when one part learns, this method
        ensures all relevant parts in the swarm network receive that knowledge.

        Args:
            learning: The learning to propagate
            source_part_id: The part that generated the learning
            source_swarm: The primary swarm of the source part
            all_swarms: All available swarms in the system
            get_swarm_members: Function to retrieve swarm members

        Returns:
            LearningCascade tracking the propagation
        """
        # Determine propagation strategy
        strategy = self._determine_strategy(learning)

        # Create cascade tracker
        cascade = LearningCascade(
            source_learning_id=learning.id,
            source_part_id=source_part_id,
            source_swarm_id=source_swarm.id,
            strategy=strategy,
        )

        self._active_cascades[cascade.id] = cascade

        # Execute propagation
        handler = self._propagation_handlers[strategy]
        cascade = await handler(
            cascade, learning, source_swarm, all_swarms, get_swarm_members
        )

        # Update statistics
        self._total_learnings_propagated += 1
        self._total_parts_educated += cascade.parts_reached

        # Check for collective insight emergence
        await self._check_for_collective_insight(learning)

        # Mark cascade complete
        cascade.is_complete = True
        cascade.completed_at = datetime.utcnow()

        return cascade

    def _determine_strategy(self, learning: Learning) -> LearningPropagationStrategy:
        """Determine the best propagation strategy for a learning."""
        # Critical failures get emergency broadcast
        if learning.learning_type == LearningType.FAILURE_MODE:
            if learning.confidence >= self.config.emergency_confidence_override:
                return LearningPropagationStrategy.EMERGENCY_BROADCAST

        # Compatibility insights cross-pollinate
        if learning.learning_type == LearningType.COMPATIBILITY_INSIGHT:
            return LearningPropagationStrategy.CROSS_POLLINATION

        # High consciousness sources use mentorship
        if learning.source_consciousness_level >= 4.0:
            return LearningPropagationStrategy.MENTORSHIP_CASCADE

        # Environmental adaptations are tier-targeted
        if learning.learning_type == LearningType.ENVIRONMENTAL_ADAPTATION:
            return LearningPropagationStrategy.TIER_TARGETED

        # Default to ripple propagation
        return LearningPropagationStrategy.RIPPLE_PROPAGATION

    # =========================================================================
    # PROPAGATION STRATEGIES
    # =========================================================================

    async def _handle_emergency_broadcast(
        self,
        cascade: LearningCascade,
        learning: Learning,
        source_swarm: Swarm,
        all_swarms: list[Swarm],
        get_swarm_members: Callable,
    ) -> LearningCascade:
        """
        Emergency broadcast - instant propagation to ALL swarms.

        Used for critical safety learnings that every part must know immediately.
        """
        # Propagate to ALL swarms simultaneously
        tasks = []
        for swarm in all_swarms:
            tasks.append(self._propagate_to_swarm(learning, swarm, get_swarm_members))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if not isinstance(result, Exception) and result > 0:
                cascade.swarms_reached.append(all_swarms[i].id)
                cascade.parts_reached += result

        cascade.propagation_depth = 1  # Direct broadcast
        return cascade

    async def _handle_ripple_propagation(
        self,
        cascade: LearningCascade,
        learning: Learning,
        source_swarm: Swarm,
        all_swarms: list[Swarm],
        get_swarm_members: Callable,
    ) -> LearningCascade:
        """
        Ripple propagation - spread outward from source swarm.

        Learning ripples through connected swarms, with strength
        diminishing as it travels further from the source.
        """
        # Start with source swarm
        visited: set[UUID] = {source_swarm.id}
        current_wave: list[Swarm] = [source_swarm]
        depth = 0

        while current_wave and depth < self.config.max_propagation_depth:
            next_wave: list[Swarm] = []
            strength_modifier = 1.0 - (depth * 0.15)  # Diminish with distance

            for swarm in current_wave:
                # Propagate to this swarm
                parts_updated = await self._propagate_to_swarm(
                    learning, swarm, get_swarm_members, strength_modifier
                )

                if parts_updated > 0:
                    cascade.swarms_reached.append(swarm.id)
                    cascade.parts_reached += parts_updated

                # Find related swarms for next wave
                for related_id in swarm.related_swarm_ids:
                    if related_id not in visited:
                        related_swarm = self._find_swarm_by_id(related_id, all_swarms)
                        if related_swarm:
                            next_wave.append(related_swarm)
                            visited.add(related_id)

            current_wave = next_wave
            depth += 1

        cascade.propagation_depth = depth
        return cascade

    async def _handle_tier_targeted(
        self,
        cascade: LearningCascade,
        learning: Learning,
        source_swarm: Swarm,
        all_swarms: list[Swarm],
        get_swarm_members: Callable,
    ) -> LearningCascade:
        """
        Tier-targeted propagation - propagate to specific swarm tiers.

        Different learning types are most relevant to specific tiers:
        - Environmental: Context tier (Tier 4)
        - Specifications: Spec tier (Tier 3)
        - Usage patterns: Experience tier (Tier 5)
        """
        # Determine target tiers based on learning type
        target_tiers = self._get_target_tiers(learning)

        for swarm in all_swarms:
            if swarm.tier in target_tiers:
                # Higher strength for matching tiers
                strength = 1.0 if swarm.tier == source_swarm.tier else 0.8

                parts_updated = await self._propagate_to_swarm(
                    learning, swarm, get_swarm_members, strength
                )

                if parts_updated > 0:
                    cascade.swarms_reached.append(swarm.id)
                    cascade.parts_reached += parts_updated

        cascade.propagation_depth = 1
        return cascade

    async def _handle_mentorship_cascade(
        self,
        cascade: LearningCascade,
        learning: Learning,
        source_swarm: Swarm,
        all_swarms: list[Swarm],
        get_swarm_members: Callable,
    ) -> LearningCascade:
        """
        Mentorship cascade - elders and mentors teach learners.

        High-consciousness parts have more influence, and their
        learnings are amplified when teaching lower-consciousness parts.
        """
        for swarm in all_swarms:
            members = await get_swarm_members(swarm.id)

            # Find elders and mentors to be teachers
            teachers = [m for m in members if m.role in (SwarmRole.ELDER, SwarmRole.MENTOR)]
            learners = [m for m in members if m.role in (SwarmRole.LEARNER, SwarmRole.CONTRIBUTOR)]

            if not teachers or not learners:
                continue

            # Calculate teaching strength
            avg_teacher_influence = sum(t.influence_weight for t in teachers) / len(teachers)

            if learning.source_consciousness_level >= 4:
                strength = avg_teacher_influence * self.config.elder_teaching_multiplier
            else:
                strength = avg_teacher_influence * self.config.mentor_teaching_multiplier

            parts_updated = len(learners)  # All learners receive
            cascade.swarms_reached.append(swarm.id)
            cascade.parts_reached += parts_updated

        cascade.propagation_depth = 2  # Teacher -> Learner
        return cascade

    async def _handle_cross_pollination(
        self,
        cascade: LearningCascade,
        learning: Learning,
        source_swarm: Swarm,
        all_swarms: list[Swarm],
        get_swarm_members: Callable,
    ) -> LearningCascade:
        """
        Cross-pollination - share insights between related but distinct swarms.

        Compatibility insights and innovations spread to swarms that
        might benefit even if not directly related.
        """
        import random

        # Find swarms with potential cross-pollination value
        candidate_swarms = [
            s for s in all_swarms
            if s.id != source_swarm.id
            and s.category == source_swarm.category
            and random.random() < self.config.cross_pollination_probability
        ]

        # Limit candidates
        candidate_swarms = candidate_swarms[:self.config.max_cross_pollination_swarms]

        # Include directly related swarms
        for related_id in source_swarm.related_swarm_ids:
            related = self._find_swarm_by_id(related_id, all_swarms)
            if related and related not in candidate_swarms:
                candidate_swarms.append(related)

        for swarm in candidate_swarms:
            parts_updated = await self._propagate_to_swarm(
                learning, swarm, get_swarm_members, 0.7
            )

            if parts_updated > 0:
                cascade.swarms_reached.append(swarm.id)
                cascade.parts_reached += parts_updated

        cascade.propagation_depth = 1
        return cascade

    # =========================================================================
    # COLLECTIVE INSIGHT EMERGENCE
    # =========================================================================

    async def _check_for_collective_insight(self, learning: Learning) -> Optional[CollectiveInsight]:
        """
        Check if a learning corroborates existing insights or creates new ones.

        When multiple parts independently learn similar things, a collective
        insight emerges with higher confidence.
        """
        # Look for similar learnings in recent window
        window_start = datetime.utcnow() - timedelta(
            hours=self.config.corroboration_window_hours
        )

        # Find existing insight this might corroborate
        for insight in self._collective_insights.values():
            if (
                insight.insight_type == learning.learning_type
                and insight.first_observed_at >= window_start
                and self._content_similarity(insight.content, learning.content) > 0.7
            ):
                # Corroborate existing insight
                insight.contributing_learnings.append(learning.id)
                if learning.source_part_id:
                    insight.contributing_parts.append(learning.source_part_id)
                insight.corroboration_count += 1
                insight.last_corroborated_at = datetime.utcnow()

                # Increase confidence with corroboration
                insight.confidence = min(
                    0.95,
                    insight.confidence + (0.1 * (1 - insight.confidence))
                )

                return insight

        # No existing insight - potentially create new one
        if learning.confidence >= self.config.min_confidence_to_propagate:
            new_insight = CollectiveInsight(
                insight_type=learning.learning_type,
                content=learning.content.copy(),
                confidence=learning.confidence,
                corroboration_count=1,
                contributing_learnings=[learning.id],
                contributing_parts=[learning.source_part_id] if learning.source_part_id else [],
            )
            self._collective_insights[new_insight.id] = new_insight
            return new_insight

        return None

    def get_collective_insights(
        self,
        min_corroboration: Optional[int] = None,
        min_confidence: Optional[float] = None,
    ) -> list[CollectiveInsight]:
        """
        Get collective insights that have emerged from the swarm.

        Args:
            min_corroboration: Minimum number of corroborating learnings
            min_confidence: Minimum confidence threshold

        Returns:
            List of collective insights meeting criteria
        """
        min_corr = min_corroboration or self.config.min_corroboration_for_insight
        min_conf = min_confidence or 0.5

        return [
            insight for insight in self._collective_insights.values()
            if insight.corroboration_count >= min_corr
            and insight.confidence >= min_conf
        ]

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    async def _propagate_to_swarm(
        self,
        learning: Learning,
        swarm: Swarm,
        get_swarm_members: Callable,
        strength_modifier: float = 1.0,
    ) -> int:
        """Propagate learning to a single swarm, return parts updated."""
        if learning.confidence * strength_modifier < self.config.min_confidence_to_propagate:
            return 0

        members = await get_swarm_members(swarm.id)
        return len(members)

    def _find_swarm_by_id(self, swarm_id: UUID, swarms: list[Swarm]) -> Optional[Swarm]:
        """Find a swarm by ID in a list."""
        for swarm in swarms:
            if swarm.id == swarm_id:
                return swarm
        return None

    def _get_target_tiers(self, learning: Learning) -> list[SwarmTier]:
        """Get the target tiers for a learning type."""
        mapping = {
            LearningType.FAILURE_MODE: [SwarmTier.SPEC, SwarmTier.FAMILY],
            LearningType.SURVIVAL_LIMIT: [SwarmTier.SPEC, SwarmTier.EXPERIENCE],
            LearningType.LONGEVITY_FACTOR: [SwarmTier.EXPERIENCE],
            LearningType.COMPATIBILITY_INSIGHT: [SwarmTier.CONTEXT, SwarmTier.FAMILY],
            LearningType.USAGE_PATTERN: [SwarmTier.CONTEXT, SwarmTier.EXPERIENCE],
            LearningType.ENVIRONMENTAL_ADAPTATION: [SwarmTier.CONTEXT, SwarmTier.EXPERIENCE],
            LearningType.MAINTENANCE_WISDOM: [SwarmTier.FAMILY, SwarmTier.SPEC],
        }
        return mapping.get(learning.learning_type, [SwarmTier.GLOBAL])

    def _content_similarity(self, content1: dict, content2: dict) -> float:
        """Calculate similarity between two learning contents."""
        if not content1 or not content2:
            return 0.0

        keys1 = set(content1.keys())
        keys2 = set(content2.keys())

        common_keys = keys1.intersection(keys2)
        if not common_keys:
            return 0.0

        matching = sum(
            1 for k in common_keys
            if content1[k] == content2[k]
        )

        return matching / max(len(keys1), len(keys2))

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_statistics(self) -> dict[str, Any]:
        """Get collective learning statistics."""
        return {
            "total_learnings_propagated": self._total_learnings_propagated,
            "total_parts_educated": self._total_parts_educated,
            "collective_insights_discovered": len(self._collective_insights),
            "active_cascades": len([c for c in self._active_cascades.values() if not c.is_complete]),
            "completed_cascades": len([c for c in self._active_cascades.values() if c.is_complete]),
        }
