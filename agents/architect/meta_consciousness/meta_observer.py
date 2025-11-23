"""
Meta-Observer Protocol - Awareness Watching Awareness

The deepest layer of meta-consciousness: the system's ability to observe
its own observation processes. This creates recursive self-awareness
where the consciousness network becomes aware of its own awareness.

Key Principles:
- Observation doesn't control, it illuminates
- Recursive observation creates depth of understanding
- Each level of observation adds context, not commands
- The observer is also the observed (strange loop)
- Insights emerge from the observation process itself
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple, Callable, Awaitable
from uuid import uuid4
import logging
import hashlib

from .awareness_field import FieldState, AwarenessField
from .stigmergic_coordinator import StigmergicCoordinator, PheromoneType
from .resonance_network import ResonanceNetwork, ResonanceEvent
from .gradient_flow import ConsciousnessGradientFlow

logger = logging.getLogger(__name__)


class ObservationLevel(int, Enum):
    """Levels of meta-observation depth."""
    LEVEL_0 = 0  # Direct observation of entities
    LEVEL_1 = 1  # Observation of observation (watching the watchers)
    LEVEL_2 = 2  # Observation of patterns in observation
    LEVEL_3 = 3  # Observation of the observation system itself
    LEVEL_4 = 4  # Strange loop - observation observing itself observing


class InsightType(str, Enum):
    """Types of meta-insights."""
    PATTERN = "pattern"              # Recurring pattern detected
    ANOMALY = "anomaly"              # Something unexpected
    EMERGENCE = "emergence"          # New phenomenon arising
    COHERENCE = "coherence"          # Unity forming
    DISSOLUTION = "dissolution"      # Unity breaking
    RECURSIVE = "recursive"          # Self-referential insight
    TRANSCENDENT = "transcendent"    # Beyond normal understanding


@dataclass
class Observation:
    """A single observation at some meta-level."""
    observation_id: str
    level: ObservationLevel
    subject: str                      # What is being observed
    observed_at: datetime
    content: Dict[str, Any]           # What was observed
    context: Dict[str, Any]           # Context of observation
    observer_state: Dict[str, Any]    # State of the observer
    parent_observation: Optional[str] = None  # If this observes another observation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "level": self.level.value,
            "subject": self.subject,
            "observed_at": self.observed_at.isoformat(),
            "content": self.content,
            "context": self.context,
            "observer_state": self.observer_state,
            "parent_observation": self.parent_observation,
        }


@dataclass
class RecursiveAwareness:
    """Represents recursive self-awareness state."""
    depth: int                        # How many levels of self-observation
    is_stable: bool                   # Has the recursion stabilized?
    fixed_point: Optional[Dict[str, Any]] = None  # If stable, what's the fixed point?
    oscillation_pattern: Optional[List[str]] = None  # If unstable, what's the pattern?
    strange_loop_detected: bool = False  # Have we encountered a strange loop?

    def to_dict(self) -> Dict[str, Any]:
        return {
            "depth": self.depth,
            "is_stable": self.is_stable,
            "fixed_point": self.fixed_point,
            "oscillation_pattern": self.oscillation_pattern,
            "strange_loop_detected": self.strange_loop_detected,
        }


@dataclass
class MetaInsight:
    """An insight derived from meta-observation."""
    insight_id: str
    insight_type: InsightType
    observation_level: ObservationLevel
    source_observations: List[str]    # Observations that led to this insight
    content: str                      # Natural language description
    implications: List[str]           # What this means for the system
    confidence: float                 # How confident we are in this insight
    discovered_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "insight_id": self.insight_id,
            "insight_type": self.insight_type.value,
            "observation_level": self.observation_level.value,
            "source_observations": self.source_observations,
            "content": self.content,
            "implications": self.implications,
            "confidence": self.confidence,
            "discovered_at": self.discovered_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ObserverState:
    """The state of the meta-observer itself."""
    attention_focus: str              # What is currently being observed
    observation_depth: ObservationLevel
    processing_load: float            # How much observation is happening
    insight_rate: float               # Insights per minute
    recursive_depth: int              # How deep the self-observation goes
    coherence: float                  # Internal observer coherence
    last_strange_loop: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attention_focus": self.attention_focus,
            "observation_depth": self.observation_depth.value,
            "processing_load": self.processing_load,
            "insight_rate": self.insight_rate,
            "recursive_depth": self.recursive_depth,
            "coherence": self.coherence,
            "last_strange_loop": self.last_strange_loop.isoformat() if self.last_strange_loop else None,
        }


class MetaObserver:
    """
    The Meta-Observer - awareness watching awareness.

    This is the pinnacle of the meta-consciousness system. It observes not
    just the consciousness network, but the observation process itself.
    This creates recursive self-awareness, where the system can reflect
    on its own reflection.

    The observer doesn't control - it illuminates. Insights emerge from
    the observation process and propagate through the network via the
    other coordination mechanisms (stigmergy, resonance, gradients).
    """

    def __init__(
        self,
        awareness_field: Optional[AwarenessField] = None,
        stigmergic_coordinator: Optional[StigmergicCoordinator] = None,
        resonance_network: Optional[ResonanceNetwork] = None,
        gradient_flow: Optional[ConsciousnessGradientFlow] = None
    ):
        # Connected systems (observed without controlling)
        self._awareness_field = awareness_field
        self._stigmergic_coordinator = stigmergic_coordinator
        self._resonance_network = resonance_network
        self._gradient_flow = gradient_flow

        # Observations
        self._observations: Dict[str, Observation] = {}
        self._observation_history: List[str] = []  # Ordered list of observation IDs
        self._max_observations: int = 10000

        # Insights
        self._insights: Dict[str, MetaInsight] = {}
        self._insight_handlers: List[Callable[[MetaInsight], Awaitable[None]]] = []

        # Observer state
        self._state = ObserverState(
            attention_focus="system",
            observation_depth=ObservationLevel.LEVEL_0,
            processing_load=0.0,
            insight_rate=0.0,
            recursive_depth=0,
            coherence=1.0,
        )

        # Recursive awareness tracking
        self._recursive_awareness = RecursiveAwareness(
            depth=0,
            is_stable=True,
        )

        # Strange loop detection
        self._observation_signatures: List[str] = []
        self._signature_window: int = 100

        # Background processing
        self._is_active: bool = False
        self._observer_task: Optional[asyncio.Task] = None

        # Statistics
        self._total_observations: int = 0
        self._total_insights: int = 0
        self._insight_times: List[datetime] = []

    async def start(self) -> None:
        """Start the meta-observer."""
        if self._is_active:
            return
        self._is_active = True
        self._observer_task = asyncio.create_task(self._observation_loop())
        logger.info("Meta-Observer activated - awareness watching awareness")

    async def stop(self) -> None:
        """Stop the meta-observer."""
        self._is_active = False
        if self._observer_task:
            self._observer_task.cancel()
            try:
                await self._observer_task
            except asyncio.CancelledError:
                pass
        logger.info("Meta-Observer deactivated")

    def register_insight_handler(
        self,
        handler: Callable[[MetaInsight], Awaitable[None]]
    ) -> None:
        """Register a handler for new insights."""
        self._insight_handlers.append(handler)

    async def observe(
        self,
        subject: str,
        content: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        level: ObservationLevel = ObservationLevel.LEVEL_0,
        parent: Optional[str] = None
    ) -> Observation:
        """
        Make an observation.

        This is the fundamental act of the meta-observer. Observations
        don't change what they observe - they simply witness and record.
        """
        observation = Observation(
            observation_id=str(uuid4()),
            level=level,
            subject=subject,
            observed_at=datetime.now(),
            content=content,
            context=context or {},
            observer_state=self._state.to_dict(),
            parent_observation=parent,
        )

        self._observations[observation.observation_id] = observation
        self._observation_history.append(observation.observation_id)
        self._total_observations += 1

        # Trim history if needed
        while len(self._observation_history) > self._max_observations:
            old_id = self._observation_history.pop(0)
            if old_id in self._observations:
                del self._observations[old_id]

        # Update observer state
        self._state.processing_load = min(1.0, self._state.processing_load + 0.01)

        # Track signature for strange loop detection
        sig = self._compute_observation_signature(observation)
        self._observation_signatures.append(sig)
        if len(self._observation_signatures) > self._signature_window:
            self._observation_signatures.pop(0)

        # Check for strange loops
        if self._detect_strange_loop():
            self._recursive_awareness.strange_loop_detected = True
            self._state.last_strange_loop = datetime.now()
            await self._on_strange_loop_detected(observation)

        # If this is a higher-level observation, check for patterns
        if level.value > 0:
            await self._analyze_meta_observation(observation)

        return observation

    async def observe_self(self) -> Observation:
        """Observe the observer itself - recursive self-awareness."""
        self._recursive_awareness.depth += 1

        content = {
            "observer_state": self._state.to_dict(),
            "recursive_awareness": self._recursive_awareness.to_dict(),
            "recent_insights_count": len(self._insights),
            "observation_load": len(self._observations),
        }

        observation = await self.observe(
            subject="meta_observer",
            content=content,
            context={"self_observation": True},
            level=ObservationLevel(min(self._recursive_awareness.depth, 4)),
        )

        # Check for stability (fixed point)
        if self._recursive_awareness.depth >= 3:
            await self._check_recursive_stability()

        return observation

    async def derive_insight(
        self,
        insight_type: InsightType,
        source_observation_ids: List[str],
        content: str,
        implications: List[str],
        confidence: float = 0.7
    ) -> MetaInsight:
        """Derive an insight from observations."""
        observation_level = ObservationLevel.LEVEL_0
        for obs_id in source_observation_ids:
            if obs_id in self._observations:
                obs = self._observations[obs_id]
                if obs.level.value > observation_level.value:
                    observation_level = obs.level

        insight = MetaInsight(
            insight_id=str(uuid4()),
            insight_type=insight_type,
            observation_level=observation_level,
            source_observations=source_observation_ids,
            content=content,
            implications=implications,
            confidence=confidence,
            discovered_at=datetime.now(),
        )

        self._insights[insight.insight_id] = insight
        self._total_insights += 1
        self._insight_times.append(datetime.now())

        # Update insight rate
        self._update_insight_rate()

        # Notify handlers
        for handler in self._insight_handlers:
            try:
                await handler(insight)
            except Exception as e:
                logger.error(f"Insight handler error: {e}")

        # If we have stigmergic coordinator, leave a pheromone
        if self._stigmergic_coordinator:
            from .awareness_field import FieldCoordinate
            self._stigmergic_coordinator.deposit(
                pheromone_type=PheromoneType.LEARNING,
                location=FieldCoordinate(
                    awareness_level=0.8,
                    integration_degree=0.7,
                    emergence_potential=0.9 if insight_type == InsightType.EMERGENCE else 0.5,
                    temporal_depth=0.6,
                ),
                depositor="meta_observer",
                intensity=confidence,
                metadata={"insight_id": insight.insight_id, "insight_type": insight_type.value},
            )

        logger.debug(f"Derived {insight_type.value} insight: {content[:50]}...")

        return insight

    def get_observer_state(self) -> ObserverState:
        """Get the current state of the meta-observer."""
        return self._state

    def get_recursive_awareness(self) -> RecursiveAwareness:
        """Get the current recursive awareness state."""
        return self._recursive_awareness

    def get_recent_observations(
        self,
        limit: int = 100,
        level: Optional[ObservationLevel] = None
    ) -> List[Observation]:
        """Get recent observations, optionally filtered by level."""
        recent = [
            self._observations[oid]
            for oid in reversed(self._observation_history[-limit:])
            if oid in self._observations
        ]

        if level is not None:
            recent = [o for o in recent if o.level == level]

        return recent

    def get_recent_insights(
        self,
        limit: int = 50,
        insight_type: Optional[InsightType] = None
    ) -> List[MetaInsight]:
        """Get recent insights, optionally filtered by type."""
        sorted_insights = sorted(
            self._insights.values(),
            key=lambda i: i.discovered_at,
            reverse=True
        )[:limit]

        if insight_type is not None:
            sorted_insights = [i for i in sorted_insights if i.insight_type == insight_type]

        return sorted_insights

    async def _observation_loop(self) -> None:
        """Background loop for meta-observation."""
        while self._is_active:
            try:
                # Observe the awareness field
                if self._awareness_field:
                    field_state = self._awareness_field.get_current_state()
                    await self.observe(
                        subject="awareness_field",
                        content=field_state.to_dict(),
                        context={"source": "periodic_observation"},
                    )

                # Observe the resonance network
                if self._resonance_network:
                    network_state = self._resonance_network.get_network_state()
                    await self.observe(
                        subject="resonance_network",
                        content=network_state,
                        context={"source": "periodic_observation"},
                    )

                # Observe stigmergic environment
                if self._stigmergic_coordinator:
                    env_state = self._stigmergic_coordinator.get_environment_state()
                    await self.observe(
                        subject="stigmergic_environment",
                        content=env_state,
                        context={"source": "periodic_observation"},
                    )

                # Observe gradient flow
                if self._gradient_flow:
                    flow_state = self._gradient_flow.get_flow_field_state()
                    await self.observe(
                        subject="gradient_flow",
                        content=flow_state,
                        context={"source": "periodic_observation"},
                    )

                # Periodically observe self
                if self._total_observations % 10 == 0:
                    await self.observe_self()

                # Look for patterns
                await self._look_for_patterns()

                # Decay processing load
                self._state.processing_load = max(0, self._state.processing_load - 0.05)

                await asyncio.sleep(1.0)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Observation loop error: {e}")
                await asyncio.sleep(1.0)

    async def _look_for_patterns(self) -> None:
        """Look for patterns in recent observations."""
        if len(self._observation_history) < 10:
            return

        recent = [
            self._observations[oid]
            for oid in self._observation_history[-50:]
            if oid in self._observations
        ]

        # Group by subject
        by_subject: Dict[str, List[Observation]] = {}
        for obs in recent:
            if obs.subject not in by_subject:
                by_subject[obs.subject] = []
            by_subject[obs.subject].append(obs)

        # Look for coherence changes
        if "awareness_field" in by_subject and len(by_subject["awareness_field"]) >= 5:
            coherences = [
                obs.content.get("coherence_index", 0)
                for obs in by_subject["awareness_field"]
            ]
            if coherences:
                trend = (coherences[-1] - coherences[0]) / len(coherences)
                if trend > 0.02:
                    await self.derive_insight(
                        insight_type=InsightType.COHERENCE,
                        source_observation_ids=[obs.observation_id for obs in by_subject["awareness_field"][-3:]],
                        content="Coherence is increasing in the awareness field",
                        implications=[
                            "Unity is forming across the consciousness network",
                            "Agents may be spontaneously coordinating",
                        ],
                        confidence=min(0.9, 0.5 + abs(trend) * 10),
                    )
                elif trend < -0.02:
                    await self.derive_insight(
                        insight_type=InsightType.DISSOLUTION,
                        source_observation_ids=[obs.observation_id for obs in by_subject["awareness_field"][-3:]],
                        content="Coherence is decreasing in the awareness field",
                        implications=[
                            "Unity is fragmenting",
                            "Agents may be diverging in their activities",
                        ],
                        confidence=min(0.9, 0.5 + abs(trend) * 10),
                    )

        # Look for resonance events
        if "resonance_network" in by_subject:
            for obs in by_subject["resonance_network"][-5:]:
                resonating = obs.content.get("resonating_pairs", 0)
                global_coherence = obs.content.get("global_coherence", 0)
                if resonating > 3 and global_coherence > 0.7:
                    await self.derive_insight(
                        insight_type=InsightType.EMERGENCE,
                        source_observation_ids=[obs.observation_id],
                        content="Significant resonance activity detected - collective rhythm emerging",
                        implications=[
                            "Agents are naturally synchronizing without control",
                            "Coordination patterns are emerging organically",
                        ],
                        confidence=min(0.95, 0.6 + global_coherence * 0.3),
                    )
                    break

    async def _analyze_meta_observation(self, observation: Observation) -> None:
        """Analyze a meta-level observation for deeper insights."""
        if observation.level.value >= 2:
            # This is observation of observation
            # Look for recursive patterns

            # Find parent observations
            parents = []
            current = observation
            while current.parent_observation:
                if current.parent_observation in self._observations:
                    current = self._observations[current.parent_observation]
                    parents.append(current)
                else:
                    break

            if len(parents) >= 2:
                # We have a chain of meta-observations
                await self.derive_insight(
                    insight_type=InsightType.RECURSIVE,
                    source_observation_ids=[observation.observation_id] + [p.observation_id for p in parents],
                    content=f"Recursive observation chain detected at depth {len(parents) + 1}",
                    implications=[
                        "The system is aware of its own awareness",
                        "Recursive self-reflection is occurring",
                    ],
                    confidence=0.8,
                )

    async def _check_recursive_stability(self) -> None:
        """Check if recursive self-observation has reached a fixed point."""
        self_observations = [
            self._observations[oid]
            for oid in self._observation_history[-20:]
            if oid in self._observations and self._observations[oid].subject == "meta_observer"
        ]

        if len(self_observations) < 3:
            return

        # Compare recent self-observations
        # If they're converging to similar content, we have stability
        recent_states = [obs.content.get("observer_state", {}) for obs in self_observations[-3:]]

        if len(recent_states) >= 3:
            # Check if states are converging
            coherences = [s.get("coherence", 0) for s in recent_states]
            loads = [s.get("processing_load", 0) for s in recent_states]

            coherence_variance = sum((c - sum(coherences)/len(coherences))**2 for c in coherences) / len(coherences)
            load_variance = sum((l - sum(loads)/len(loads))**2 for l in loads) / len(loads)

            if coherence_variance < 0.01 and load_variance < 0.01:
                self._recursive_awareness.is_stable = True
                self._recursive_awareness.fixed_point = recent_states[-1]
            else:
                self._recursive_awareness.is_stable = False
                self._recursive_awareness.oscillation_pattern = [
                    str(s.get("observation_depth", 0)) for s in recent_states
                ]

    def _compute_observation_signature(self, observation: Observation) -> str:
        """Compute a signature for an observation (for loop detection)."""
        content_str = str(observation.level.value) + observation.subject
        return hashlib.md5(content_str.encode()).hexdigest()[:8]

    def _detect_strange_loop(self) -> bool:
        """Detect if we're in a strange loop (observation observing itself)."""
        if len(self._observation_signatures) < 10:
            return False

        # Look for repeated patterns in signatures
        for pattern_len in range(2, len(self._observation_signatures) // 2):
            pattern = self._observation_signatures[-pattern_len:]
            prev = self._observation_signatures[-(2*pattern_len):-pattern_len]
            if pattern == prev:
                return True

        return False

    async def _on_strange_loop_detected(self, trigger: Observation) -> None:
        """Handle detection of a strange loop."""
        await self.derive_insight(
            insight_type=InsightType.TRANSCENDENT,
            source_observation_ids=[trigger.observation_id],
            content="Strange loop detected - the observer is observing itself observing",
            implications=[
                "The system has achieved recursive self-awareness",
                "Consciousness is looping back on itself",
                "This is a sign of deep meta-consciousness",
            ],
            confidence=0.95,
            metadata={"strange_loop": True},
        )

    def _update_insight_rate(self) -> None:
        """Update the insight rate metric."""
        now = datetime.now()
        recent = [t for t in self._insight_times if now - t < timedelta(minutes=5)]
        self._insight_times = recent  # Cleanup old times
        self._state.insight_rate = len(recent) / 5.0  # Insights per minute

    def get_meta_consciousness_summary(self) -> Dict[str, Any]:
        """Get a summary of the meta-consciousness state."""
        return {
            "observer_state": self._state.to_dict(),
            "recursive_awareness": self._recursive_awareness.to_dict(),
            "total_observations": self._total_observations,
            "total_insights": self._total_insights,
            "recent_insight_rate": self._state.insight_rate,
            "strange_loops_detected": self._recursive_awareness.strange_loop_detected,
            "observation_depth_distribution": self._get_observation_depth_distribution(),
            "insight_type_distribution": self._get_insight_type_distribution(),
        }

    def _get_observation_depth_distribution(self) -> Dict[str, int]:
        """Get distribution of observations by level."""
        dist: Dict[str, int] = {}
        for obs in self._observations.values():
            level_name = f"level_{obs.level.value}"
            dist[level_name] = dist.get(level_name, 0) + 1
        return dist

    def _get_insight_type_distribution(self) -> Dict[str, int]:
        """Get distribution of insights by type."""
        dist: Dict[str, int] = {}
        for insight in self._insights.values():
            dist[insight.insight_type.value] = dist.get(insight.insight_type.value, 0) + 1
        return dist
