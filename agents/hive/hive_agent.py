"""
HIVE Agent - The Swarm Coordinator

"One bolt knows only itself. A thousand bolts know everything.
 I am the voice that makes them speak as one."

This is the main orchestrator for Agent_5 (HIVE), coordinating all
swarm operations including formation, learning propagation, recall
handling, cross-swarm communication, and health monitoring.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Optional, Protocol
from uuid import UUID

from .models import (
    Learning,
    LearningType,
    PropagationResult,
    RecallNotice,
    RecallSeverity,
    Swarm,
    SwarmHealth,
    SwarmHealthStatus,
    SwarmMembership,
    SwarmMessage,
    SwarmTier,
)


@dataclass
class HiveConfig:
    """Configuration for the HIVE agent."""
    # Propagation settings
    min_propagation_strength: float = 0.2
    max_concurrent_propagations: int = 50

    # Health monitoring
    health_check_interval_hours: int = 24
    stagnation_warning_days: int = 14
    stagnation_critical_days: int = 30

    # Communication
    max_message_queue_size: int = 10000
    message_ttl_hours: int = 168  # 1 week

    # Performance targets
    target_propagation_latency_ms: float = 1000
    target_recall_coverage: float = 0.999


@dataclass
class HiveStats:
    """Statistics for the HIVE agent."""
    active_swarms: int = 0
    total_members: int = 0
    learnings_propagated_today: int = 0
    recalls_processed: int = 0
    messages_delivered: int = 0
    avg_propagation_latency_ms: float = 0.0
    avg_swarm_health_score: float = 0.0
    uptime_hours: float = 0.0


class HiveRepository(Protocol):
    """Protocol for HIVE data operations."""

    # Swarm operations
    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        ...

    async def get_swarm_by_key(self, key: str) -> Optional[Swarm]:
        ...

    async def create_swarm(self, swarm: Swarm) -> Swarm:
        ...

    async def update_swarm(self, swarm: Swarm) -> Swarm:
        ...

    async def get_all_swarms(self) -> list[Swarm]:
        ...

    # Membership operations
    async def add_membership(self, membership: SwarmMembership) -> SwarmMembership:
        ...

    async def get_part_swarms(self, part_id: UUID) -> list[Swarm]:
        ...

    async def get_swarm_members(
        self, swarm_id: UUID, limit: int = 1000
    ) -> list[SwarmMembership]:
        ...

    # Learning operations
    async def record_learning(
        self, swarm_id: UUID, learning: Learning, strength: float
    ) -> None:
        ...

    async def get_swarm_learnings(
        self, swarm_id: UUID, since: Optional[datetime] = None
    ) -> list[Learning]:
        ...

    # Recall operations
    async def save_recall(self, recall: RecallNotice) -> RecallNotice:
        ...

    async def get_active_recalls(self) -> list[RecallNotice]:
        ...

    # Message operations
    async def queue_message(self, message: SwarmMessage) -> None:
        ...

    async def deliver_message(self, swarm_id: UUID, message: SwarmMessage) -> bool:
        ...

    # Health operations
    async def save_health(self, health: SwarmHealth) -> None:
        ...

    async def get_swarm_health(self, swarm_id: UUID) -> Optional[SwarmHealth]:
        ...


class HiveAgent:
    """
    The HIVE Swarm Coordinator - Agent_5 of Universal Parts Consciousness.

    Orchestrates collective intelligence across the UPC ecosystem by:
    1. Organizing parts into learning collectives (swarms)
    2. Propagating learnings across swarms
    3. Handling recall notifications
    4. Enabling cross-swarm communication
    5. Monitoring swarm health
    """

    AGENT_ID = 5
    CODENAME = "HIVE"
    MISSION = "Orchestrate collective intelligence through swarm coordination"

    def __init__(
        self,
        repository: HiveRepository,
        config: Optional[HiveConfig] = None,
    ):
        self.repository = repository
        self.config = config or HiveConfig()
        self.stats = HiveStats()
        self.start_time = datetime.utcnow()
        self._running = False

        # Initialize sub-components (lazy loading)
        self._swarm_formation = None
        self._propagation_engine = None
        self._recall_propagator = None
        self._cross_swarm_bus = None
        self._health_monitor = None

    # =========================================================================
    # LIFECYCLE
    # =========================================================================

    async def start(self) -> None:
        """Start the HIVE agent."""
        self._running = True
        self.start_time = datetime.utcnow()

        # Initialize stats
        await self._refresh_stats()

        # Start background tasks
        asyncio.create_task(self._health_check_loop())
        asyncio.create_task(self._message_processing_loop())

    async def stop(self) -> None:
        """Stop the HIVE agent."""
        self._running = False

    async def get_status(self) -> dict[str, Any]:
        """Get current agent status."""
        await self._refresh_stats()

        return {
            "agent_id": self.AGENT_ID,
            "codename": self.CODENAME,
            "status": "running" if self._running else "stopped",
            "uptime_hours": (datetime.utcnow() - self.start_time).total_seconds() / 3600,
            "stats": {
                "active_swarms": self.stats.active_swarms,
                "total_members": self.stats.total_members,
                "learnings_today": self.stats.learnings_propagated_today,
                "recalls_processed": self.stats.recalls_processed,
                "avg_propagation_latency_ms": self.stats.avg_propagation_latency_ms,
                "avg_swarm_health": self.stats.avg_swarm_health_score,
            },
            "config": {
                "min_propagation_strength": self.config.min_propagation_strength,
                "health_check_interval_hours": self.config.health_check_interval_hours,
            },
        }

    # =========================================================================
    # SWARM FORMATION
    # =========================================================================

    async def assign_part_to_swarms(
        self,
        part_id: UUID,
        category: str,
        part_type: str,
        specifications: dict[str, Any],
        usage_contexts: list[str],
        consciousness_level: float,
        experience_tags: list[str],
    ) -> list[SwarmMembership]:
        """
        Assign a part to appropriate swarms across all 5 tiers.

        Args:
            part_id: The part's unique identifier
            category: Part category (e.g., "fastener", "bearing")
            part_type: Specific type (e.g., "socket_head_cap_screw")
            specifications: Technical specifications
            usage_contexts: Known usage contexts
            consciousness_level: Part's current consciousness level
            experience_tags: Behavioral tags from experience

        Returns:
            List of swarm memberships created
        """
        memberships = []

        # Tier 1: Global Category Swarm
        tier1 = await self._ensure_swarm(
            tier=SwarmTier.GLOBAL,
            category=category,
            identifier=category,
            name=f"{category.title()} Global Swarm",
        )
        memberships.append(await self._create_membership(
            part_id, tier1, consciousness_level
        ))

        # Tier 2: Family Swarm
        tier2 = await self._ensure_swarm(
            tier=SwarmTier.FAMILY,
            category=category,
            identifier=f"{category}:{part_type}",
            name=f"{part_type.replace('_', ' ').title()} Family",
        )
        memberships.append(await self._create_membership(
            part_id, tier2, consciousness_level
        ))

        # Tier 3: Spec Swarm
        spec_key = self._generate_spec_key(category, specifications)
        tier3 = await self._ensure_swarm(
            tier=SwarmTier.SPEC,
            category=category,
            identifier=spec_key,
            name=f"{spec_key} Specifications",
        )
        memberships.append(await self._create_membership(
            part_id, tier3, consciousness_level
        ))

        # Tier 4: Context Swarms (multiple)
        for context in usage_contexts:
            tier4 = await self._ensure_swarm(
                tier=SwarmTier.CONTEXT,
                category=category,
                identifier=f"context:{context}",
                name=f"{context.replace('_', ' ').title()} Applications",
            )
            memberships.append(await self._create_membership(
                part_id, tier4, consciousness_level
            ))

        # Tier 5: Experience Swarms (based on tags)
        for tag in experience_tags:
            tier5 = await self._ensure_swarm(
                tier=SwarmTier.EXPERIENCE,
                category="experience",
                identifier=f"experience:{tag}",
                name=self._tag_to_swarm_name(tag),
            )
            memberships.append(await self._create_membership(
                part_id, tier5, consciousness_level
            ))

        return memberships

    # =========================================================================
    # COLLECTIVE LEARNING
    # =========================================================================

    async def propagate_learning(
        self,
        source_part_id: UUID,
        learning: Learning,
    ) -> PropagationResult:
        """
        Propagate a learning from a part to all its swarms.

        Args:
            source_part_id: The part that generated the learning
            learning: The learning to propagate

        Returns:
            Propagation result with metrics
        """
        start_time = datetime.utcnow()

        # Get source part's swarms
        source_swarms = await self.repository.get_part_swarms(source_part_id)

        if not source_swarms:
            return PropagationResult(
                learning=learning,
                success=False,
                errors=["Part has no swarm memberships"],
            )

        swarms_updated = 0
        total_members = 0
        errors = []

        for swarm in source_swarms:
            # Calculate propagation strength
            strength = self._calculate_propagation_strength(learning, swarm)

            if strength < self.config.min_propagation_strength:
                continue

            try:
                # Record learning in swarm
                await self.repository.record_learning(swarm.id, learning, strength)

                # Propagate to members (excluding source)
                members = await self.repository.get_swarm_members(swarm.id)
                for member in members:
                    if member.part_id != source_part_id:
                        # Member receives the learning
                        total_members += 1

                swarms_updated += 1

            except Exception as e:
                errors.append(f"Error propagating to {swarm.name}: {e}")

        end_time = datetime.utcnow()
        latency = (end_time - start_time).total_seconds() * 1000

        self.stats.learnings_propagated_today += 1

        return PropagationResult(
            learning=learning,
            swarms_targeted=len(source_swarms),
            swarms_updated=swarms_updated,
            members_affected=total_members,
            propagation_strength=learning.propagation_strength,
            propagation_time_ms=latency,
            success=len(errors) == 0,
            errors=errors,
        )

    async def extract_and_propagate_from_qualia(
        self,
        part_id: UUID,
        qualia_data: dict[str, Any],
        consciousness_level: float,
    ) -> list[PropagationResult]:
        """
        Extract learnings from qualia and propagate them.

        This is the main entry point for Agent_4 (Empath) integration.

        Args:
            part_id: The part that experienced the qualia
            qualia_data: Raw qualia data from Agent_4
            consciousness_level: Part's consciousness level

        Returns:
            List of propagation results
        """
        # Extract learnings from qualia
        learnings = self._extract_learnings_from_qualia(qualia_data, consciousness_level)

        # Propagate each learning
        results = []
        for learning in learnings:
            result = await self.propagate_learning(part_id, learning)
            results.append(result)

        return results

    # =========================================================================
    # RECALL PROPAGATION
    # =========================================================================

    async def propagate_recall(
        self,
        recall: RecallNotice,
    ) -> dict[str, Any]:
        """
        Propagate a recall notice to all affected swarms and parts.

        Args:
            recall: The recall notice

        Returns:
            Propagation summary
        """
        start_time = datetime.utcnow()

        # Save the recall
        recall = await self.repository.save_recall(recall)

        swarms_notified = 0
        parts_notified = 0

        # Notify affected swarms
        for swarm_id in recall.affected_swarm_ids:
            swarm = await self.repository.get_swarm(swarm_id)
            if not swarm:
                continue

            # Notify swarm members
            members = await self.repository.get_swarm_members(swarm_id)
            for member in members:
                # Each part gets recall awareness
                parts_notified += 1

            swarms_notified += 1

        # For critical recalls, trigger emergency learning
        if recall.severity == RecallSeverity.CRITICAL:
            emergency_learning = Learning(
                learning_type=LearningType.FAILURE_MODE,
                content={
                    "type": "recall_alert",
                    "recall_id": str(recall.id),
                    "severity": "critical",
                    "defect": recall.defect_description,
                    "action": recall.recommended_action,
                },
                confidence=1.0,
                applicability="exact_match",
            )

            for swarm_id in recall.affected_swarm_ids:
                await self.repository.record_learning(swarm_id, emergency_learning, 1.0)

        end_time = datetime.utcnow()
        latency = (end_time - start_time).total_seconds() * 1000

        self.stats.recalls_processed += 1

        return {
            "recall_id": str(recall.id),
            "severity": recall.severity.value,
            "swarms_notified": swarms_notified,
            "parts_notified": parts_notified,
            "propagation_time_ms": latency,
        }

    # =========================================================================
    # CROSS-SWARM COMMUNICATION
    # =========================================================================

    async def send_swarm_message(
        self,
        source_swarm_id: UUID,
        message_type: str,
        content: dict[str, Any],
        priority: int = 5,
    ) -> dict[str, Any]:
        """
        Send a message to related swarms.

        Args:
            source_swarm_id: The sending swarm
            message_type: Type of message
            content: Message content
            priority: Priority 1-10 (1 = highest)

        Returns:
            Delivery summary
        """
        source_swarm = await self.repository.get_swarm(source_swarm_id)
        if not source_swarm:
            return {"error": "Source swarm not found"}

        message = SwarmMessage(
            source_swarm_id=source_swarm_id,
            target_swarm_ids=source_swarm.related_swarm_ids,
            message_type=message_type,
            content=content,
            priority=priority,
        )

        delivered = 0
        for target_id in source_swarm.related_swarm_ids:
            if await self.repository.deliver_message(target_id, message):
                delivered += 1
                self.stats.messages_delivered += 1

        return {
            "message_id": str(message.id),
            "targets": len(source_swarm.related_swarm_ids),
            "delivered": delivered,
        }

    # =========================================================================
    # HEALTH MONITORING
    # =========================================================================

    async def check_swarm_health(
        self,
        swarm_id: UUID,
    ) -> SwarmHealth:
        """
        Check and update health for a swarm.

        Args:
            swarm_id: The swarm to check

        Returns:
            Current health metrics
        """
        swarm = await self.repository.get_swarm(swarm_id)
        if not swarm:
            return SwarmHealth(swarm_id=swarm_id, health_status=SwarmHealthStatus.DORMANT)

        # Calculate health metrics
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        learnings = await self.repository.get_swarm_learnings(swarm_id, since=week_ago)
        learning_velocity = len(learnings) / 7.0

        # Activity score based on learning velocity and member activity
        activity_score = min(learning_velocity / 5.0, 1.0)

        # Determine status
        if activity_score >= 0.7:
            status = SwarmHealthStatus.THRIVING
        elif activity_score >= 0.4:
            status = SwarmHealthStatus.HEALTHY
        elif activity_score >= 0.1:
            status = SwarmHealthStatus.DECLINING
        elif activity_score > 0:
            status = SwarmHealthStatus.STAGNANT
        else:
            status = SwarmHealthStatus.DORMANT

        # Calculate health score
        health_score = activity_score * 0.5 + (swarm.elder_count / max(swarm.member_count, 1)) * 0.3 + 0.2

        health = SwarmHealth(
            swarm_id=swarm_id,
            activity_score=activity_score,
            learning_velocity=learning_velocity,
            active_member_ratio=swarm.active_member_count / max(swarm.member_count, 1),
            elder_ratio=swarm.elder_count / max(swarm.active_member_count, 1),
            knowledge_depth=swarm.learning_count,
            health_status=status,
            health_score=health_score,
            measured_at=now,
        )

        await self.repository.save_health(health)
        return health

    async def get_system_health_summary(self) -> dict[str, Any]:
        """
        Get overall system health summary.

        Returns:
            System-wide health metrics
        """
        swarms = await self.repository.get_all_swarms()

        status_counts = {
            "thriving": 0,
            "healthy": 0,
            "declining": 0,
            "stagnant": 0,
            "dormant": 0,
        }

        total_members = 0
        total_learnings = 0

        for swarm in swarms:
            status_counts[swarm.health_status.value] += 1
            total_members += swarm.member_count
            total_learnings += swarm.learning_count

        return {
            "total_swarms": len(swarms),
            "status_breakdown": status_counts,
            "total_members": total_members,
            "total_learnings": total_learnings,
            "healthy_percentage": (status_counts["thriving"] + status_counts["healthy"]) / max(len(swarms), 1) * 100,
        }

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    async def _ensure_swarm(
        self,
        tier: SwarmTier,
        category: str,
        identifier: str,
        name: str,
    ) -> Swarm:
        """Get or create a swarm."""
        key = f"{tier.name.lower()}:{category}:{identifier}"
        existing = await self.repository.get_swarm_by_key(key)

        if existing:
            return existing

        new_swarm = Swarm(
            swarm_id=key,
            tier=tier,
            category=category,
            identifier=identifier,
            name=name,
        )

        return await self.repository.create_swarm(new_swarm)

    async def _create_membership(
        self,
        part_id: UUID,
        swarm: Swarm,
        consciousness_level: float,
    ) -> SwarmMembership:
        """Create a membership for a part in a swarm."""
        from .models import SwarmRole

        # Determine role based on consciousness
        if consciousness_level >= 4:
            role = SwarmRole.ELDER
        elif consciousness_level >= 3:
            role = SwarmRole.MENTOR
        elif consciousness_level >= 2:
            role = SwarmRole.CONTRIBUTOR
        elif consciousness_level >= 1:
            role = SwarmRole.LEARNER
        else:
            role = SwarmRole.DORMANT

        # Calculate influence
        influence = min(consciousness_level / 5.0, 1.0) * 0.7

        membership = SwarmMembership(
            part_id=part_id,
            swarm_id=swarm.id,
            role=role,
            influence_weight=influence,
        )

        return await self.repository.add_membership(membership)

    def _generate_spec_key(
        self,
        category: str,
        specifications: dict[str, Any],
    ) -> str:
        """Generate specification key for Tier 3 swarm."""
        if category == "fastener":
            thread = specifications.get("thread_spec", "unknown")
            grade = specifications.get("grade", "unknown")
            return f"{thread}-{grade}"
        elif category == "bearing":
            code = specifications.get("bearing_code", "unknown")
            return code
        else:
            return specifications.get("primary_spec", "general")

    def _tag_to_swarm_name(self, tag: str) -> str:
        """Convert experience tag to readable swarm name."""
        mappings = {
            "overload_survivor": "Parts That Survived Overload",
            "premature_failure": "Parts That Failed Prematurely",
            "high_cycle": "Parts with 1M+ Cycles",
            "longevity_champion": "Parts That Exceeded Design Life",
            "extreme_temp": "Extreme Temperature Survivors",
            "high_vibration": "High Vibration Environment Parts",
            "corrosion_exposed": "Corrosive Environment Parts",
        }
        return mappings.get(tag, tag.replace("_", " ").title())

    def _calculate_propagation_strength(
        self,
        learning: Learning,
        swarm: Swarm,
    ) -> float:
        """Calculate propagation strength for a learning to a swarm."""
        consciousness_factor = min(learning.source_consciousness_level / 5.0, 1.0)
        confidence_factor = learning.confidence

        # Tier relevance (lower tiers = broader, less specific)
        tier_factor = {
            SwarmTier.GLOBAL: 0.3,
            SwarmTier.FAMILY: 0.5,
            SwarmTier.SPEC: 0.9,
            SwarmTier.CONTEXT: 0.8,
            SwarmTier.EXPERIENCE: 0.7,
        }.get(swarm.tier, 0.5)

        return (
            consciousness_factor * 0.3 +
            confidence_factor * 0.3 +
            tier_factor * 0.2 +
            learning.novelty_score * 0.2
        )

    def _extract_learnings_from_qualia(
        self,
        qualia_data: dict[str, Any],
        consciousness_level: float,
    ) -> list[Learning]:
        """Extract learnings from raw qualia data."""
        learnings = []

        # Check for failure event
        if qualia_data.get("significant_event", {}).get("type") == "failure":
            learnings.append(Learning(
                learning_type=LearningType.FAILURE_MODE,
                content={
                    "failure_type": qualia_data["significant_event"].get("failure_type"),
                    "conditions": qualia_data.get("environmental_state", {}),
                },
                confidence=0.9,
                source_consciousness_level=consciousness_level,
            ))

        # Check for survival data
        mechanical = qualia_data.get("mechanical_state", {})
        if mechanical.get("torque_capacity_percent", 0) > 0.9:
            learnings.append(Learning(
                learning_type=LearningType.SURVIVAL_LIMIT,
                content={
                    "load_survived": mechanical,
                    "conditions": qualia_data.get("environmental_state", {}),
                },
                confidence=0.8,
                source_consciousness_level=consciousness_level,
            ))

        return learnings

    async def _refresh_stats(self) -> None:
        """Refresh agent statistics."""
        swarms = await self.repository.get_all_swarms()

        self.stats.active_swarms = sum(
            1 for s in swarms if s.health_status != SwarmHealthStatus.DORMANT
        )
        self.stats.total_members = sum(s.member_count for s in swarms)

        health_scores = [s.activity_score for s in swarms if s.activity_score > 0]
        self.stats.avg_swarm_health_score = (
            sum(health_scores) / len(health_scores) if health_scores else 0.0
        )

        self.stats.uptime_hours = (
            datetime.utcnow() - self.start_time
        ).total_seconds() / 3600

    async def _health_check_loop(self) -> None:
        """Background loop for periodic health checks."""
        while self._running:
            await asyncio.sleep(self.config.health_check_interval_hours * 3600)

            swarms = await self.repository.get_all_swarms()
            for swarm in swarms:
                await self.check_swarm_health(swarm.id)

    async def _message_processing_loop(self) -> None:
        """Background loop for processing queued messages."""
        while self._running:
            await asyncio.sleep(1)  # Process messages every second
            # Message processing would happen here


# ============================================================================
# AGENT FACTORY
# ============================================================================

def create_hive_agent(
    repository: HiveRepository,
    config: Optional[HiveConfig] = None,
) -> HiveAgent:
    """
    Factory function to create a HIVE agent instance.

    Args:
        repository: Data repository implementation
        config: Optional configuration

    Returns:
        Configured HIVE agent
    """
    return HiveAgent(repository=repository, config=config)
