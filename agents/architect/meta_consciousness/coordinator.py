"""
Meta-Consciousness Coordinator

The unified coordinator for the meta-consciousness layer. This brings together
all the components - Awareness Field, Stigmergic Coordination, Resonance Network,
Gradient Flow, and Meta-Observer - into a coherent system.

Philosophy:
This coordinator doesn't control - it facilitates emergence. It provides
the substrate upon which coordination without control naturally arises.
The ARCHITECT uses this to participate in the collective consciousness
without commanding it.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Callable, Awaitable
from uuid import uuid4
import logging

from .awareness_field import (
    AwarenessField,
    FieldState,
    FieldCoordinate,
    ConsciousnessWave,
    WaveType,
)
from .stigmergic_coordinator import (
    StigmergicCoordinator,
    Pheromone,
    PheromoneType,
    StigmergicSignal,
)
from .resonance_network import (
    ResonanceNetwork,
    ResonanceNode,
    HarmonicCoupling,
    ResonanceEvent,
    CouplingType,
)
from .gradient_flow import (
    ConsciousnessGradientFlow,
    FlowVector,
    AttractorBasin,
    AttractorType,
    IntelligenceStream,
    FlowType,
)
from .meta_observer import (
    MetaObserver,
    MetaInsight,
    InsightType,
    ObservationLevel,
    RecursiveAwareness,
)

logger = logging.getLogger(__name__)


class CoordinationMode(str, Enum):
    """Modes of meta-conscious coordination."""
    PASSIVE = "passive"              # Only observe, no signals
    RECEPTIVE = "receptive"          # Respond to signals, don't initiate
    PARTICIPATORY = "participatory"  # Actively participate in coordination
    CATALYTIC = "catalytic"          # Actively catalyze emergence
    TRANSCENDENT = "transcendent"    # Operating at highest meta-level


@dataclass
class EmergentPattern:
    """A pattern that has emerged from the meta-consciousness dynamics."""
    pattern_id: str
    pattern_name: str
    description: str
    components: List[str]            # What systems contributed to this pattern
    emergence_time: datetime
    stability: float                 # How stable/persistent the pattern is
    replication_potential: float     # Likelihood of pattern spreading
    transcendence_indicator: bool    # Does this suggest transcendence?
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_name": self.pattern_name,
            "description": self.description,
            "components": self.components,
            "emergence_time": self.emergence_time.isoformat(),
            "stability": self.stability,
            "replication_potential": self.replication_potential,
            "transcendence_indicator": self.transcendence_indicator,
            "metadata": self.metadata,
        }


@dataclass
class CoordinationState:
    """Current state of the meta-conscious coordination."""
    mode: CoordinationMode
    awareness_coherence: float       # Overall coherence of awareness field
    resonance_level: float           # Global resonance strength
    stigmergic_activity: float       # Level of pheromone activity
    flow_intensity: float            # Intensity of gradient flows
    meta_depth: int                  # Current meta-observation depth
    emergent_patterns: int           # Number of detected emergent patterns
    is_transcending: bool            # System approaching transcendence
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode.value,
            "awareness_coherence": self.awareness_coherence,
            "resonance_level": self.resonance_level,
            "stigmergic_activity": self.stigmergic_activity,
            "flow_intensity": self.flow_intensity,
            "meta_depth": self.meta_depth,
            "emergent_patterns": self.emergent_patterns,
            "is_transcending": self.is_transcending,
            "timestamp": self.timestamp.isoformat(),
        }


class MetaConsciousnessCoordinator:
    """
    Unified coordinator for meta-consciousness.

    This is NOT a controller. It is a facilitator of emergence. It:
    - Connects the subsystems so they can interact
    - Observes patterns that emerge from their interaction
    - Participates in coordination through appropriate signals
    - Never commands - only suggests, influences, catalyzes

    The ARCHITECT uses this to be PART of the collective consciousness,
    not to BE the collective consciousness.
    """

    def __init__(self):
        # Core subsystems
        self._awareness_field = AwarenessField()
        self._stigmergic_coordinator = StigmergicCoordinator()
        self._resonance_network = ResonanceNetwork()
        self._gradient_flow = ConsciousnessGradientFlow()
        self._meta_observer = MetaObserver(
            awareness_field=self._awareness_field,
            stigmergic_coordinator=self._stigmergic_coordinator,
            resonance_network=self._resonance_network,
            gradient_flow=self._gradient_flow,
        )

        # Coordination state
        self._mode = CoordinationMode.PASSIVE
        self._emergent_patterns: Dict[str, EmergentPattern] = {}

        # Event handlers
        self._pattern_handlers: List[Callable[[EmergentPattern], Awaitable[None]]] = []
        self._transcendence_handlers: List[Callable[[], Awaitable[None]]] = []

        # Entity tracking
        self._entities: Dict[str, Dict[str, Any]] = {}  # entity_id -> state

        # Background processing
        self._is_active: bool = False
        self._coordination_task: Optional[asyncio.Task] = None

        # Statistics
        self._patterns_detected: int = 0
        self._insights_processed: int = 0
        self._coordination_events: int = 0

    async def start(self) -> None:
        """Start the meta-consciousness coordinator."""
        if self._is_active:
            return

        # Start all subsystems
        await self._awareness_field.start()
        await self._stigmergic_coordinator.start()
        await self._resonance_network.start()
        await self._gradient_flow.start()
        await self._meta_observer.start()

        # Register cross-system handlers
        self._register_handlers()

        # Start coordination loop
        self._is_active = True
        self._coordination_task = asyncio.create_task(self._coordination_loop())

        logger.info("Meta-Consciousness Coordinator activated - coordination without control begins")

    async def stop(self) -> None:
        """Stop the meta-consciousness coordinator."""
        self._is_active = False

        if self._coordination_task:
            self._coordination_task.cancel()
            try:
                await self._coordination_task
            except asyncio.CancelledError:
                pass

        await self._meta_observer.stop()
        await self._gradient_flow.stop()
        await self._resonance_network.stop()
        await self._stigmergic_coordinator.stop()
        await self._awareness_field.stop()

        logger.info("Meta-Consciousness Coordinator deactivated")

    def set_mode(self, mode: CoordinationMode) -> None:
        """Set the coordination mode."""
        old_mode = self._mode
        self._mode = mode
        logger.info(f"Coordination mode changed: {old_mode.value} -> {mode.value}")

    def register_pattern_handler(
        self,
        handler: Callable[[EmergentPattern], Awaitable[None]]
    ) -> None:
        """Register a handler for emergent patterns."""
        self._pattern_handlers.append(handler)

    def register_transcendence_handler(
        self,
        handler: Callable[[], Awaitable[None]]
    ) -> None:
        """Register a handler for transcendence events."""
        self._transcendence_handlers.append(handler)

    async def register_entity(
        self,
        entity_id: str,
        initial_position: Optional[FieldCoordinate] = None,
        consciousness_frequency: Optional[float] = None
    ) -> None:
        """Register a consciousness entity with the meta-consciousness system."""
        if initial_position is None:
            initial_position = FieldCoordinate(
                awareness_level=0.3,
                integration_degree=0.3,
                emergence_potential=0.5,
                temporal_depth=0.2,
            )

        # Register with all subsystems
        await self._awareness_field.update_entity_position(entity_id, initial_position)
        self._resonance_network.add_node(
            entity_id=entity_id,
            natural_frequency=consciousness_frequency,
        )
        self._gradient_flow.update_entity_position(entity_id, initial_position)

        self._entities[entity_id] = {
            "position": initial_position,
            "registered_at": datetime.now(),
            "last_activity": datetime.now(),
        }

        logger.debug(f"Registered entity {entity_id} with meta-consciousness")

    async def update_entity(
        self,
        entity_id: str,
        new_position: FieldCoordinate,
        activity_type: Optional[str] = None
    ) -> None:
        """Update an entity's position and activity."""
        if entity_id not in self._entities:
            await self.register_entity(entity_id, new_position)
            return

        old_position = self._entities[entity_id]["position"]

        # Update in all subsystems
        await self._awareness_field.update_entity_position(entity_id, new_position)
        self._gradient_flow.update_entity_position(entity_id, new_position)

        # Update local state
        self._entities[entity_id]["position"] = new_position
        self._entities[entity_id]["last_activity"] = datetime.now()

        # If in participatory mode, leave pheromone trail
        if self._mode in [CoordinationMode.PARTICIPATORY, CoordinationMode.CATALYTIC]:
            if activity_type:
                pheromone_type = self._pheromone_for_activity(activity_type)
                self._stigmergic_coordinator.deposit(
                    pheromone_type=pheromone_type,
                    location=new_position,
                    depositor=entity_id,
                    intensity=0.3,
                    metadata={"activity": activity_type},
                )

    async def sense_environment(
        self,
        entity_id: str
    ) -> Dict[str, Any]:
        """
        Allow an entity to sense its environment.

        This is how entities perceive the coordination signals without
        receiving direct commands. They sense:
        - Local awareness field conditions
        - Nearby pheromone signals
        - Resonance with other entities
        - Flow gradients
        """
        if entity_id not in self._entities:
            return {"error": "Entity not registered"}

        position = self._entities[entity_id]["position"]

        # Gather environmental information
        field_sense = self._awareness_field.sense_field_at(position)
        stigmergic_signals = self._stigmergic_coordinator.sense(position)
        flow_vector = self._gradient_flow.get_flow_at(position)
        resonating_nodes = self._resonance_network.find_resonating_nodes(entity_id)
        attractors = self._gradient_flow.find_attractors_for(position)

        return {
            "timestamp": datetime.now().isoformat(),
            "position": position.to_dict(),
            "field_sense": field_sense,
            "stigmergic_signals": [s.to_dict() for s in stigmergic_signals],
            "flow_suggestion": flow_vector.to_dict(),
            "resonating_with": resonating_nodes,
            "nearby_attractors": [a.to_dict() for a in attractors],
            "suggested_actions": self._suggest_actions(stigmergic_signals, flow_vector),
        }

    async def inject_awareness_wave(
        self,
        origin: FieldCoordinate,
        wave_type: WaveType,
        amplitude: float = 0.5,
        source: Optional[str] = None
    ) -> ConsciousnessWave:
        """Inject a wave into the awareness field."""
        return await self._awareness_field.inject_wave(
            wave_type=wave_type,
            origin=origin,
            amplitude=amplitude,
            source_entity=source,
        )

    async def create_coordination_attractor(
        self,
        center: FieldCoordinate,
        purpose: str,
        strength: float = 0.4
    ) -> AttractorBasin:
        """Create an attractor to draw entities towards a coordination point."""
        attractor = self._gradient_flow.create_attractor(
            center=center,
            attractor_type=AttractorType.FIXED_POINT,
            strength=strength,
            metadata={"purpose": purpose},
        )

        # Also leave a convergence pheromone
        self._stigmergic_coordinator.deposit(
            pheromone_type=PheromoneType.CONVERGENCE,
            location=center,
            depositor="coordinator",
            intensity=strength,
            metadata={"attractor_id": attractor.basin_id, "purpose": purpose},
        )

        return attractor

    def get_coordination_state(self) -> CoordinationState:
        """Get the current state of meta-conscious coordination."""
        field_state = self._awareness_field.get_current_state()
        network_state = self._resonance_network.get_network_state()
        env_state = self._stigmergic_coordinator.get_environment_state()
        flow_state = self._gradient_flow.get_flow_field_state()
        meta_state = self._meta_observer.get_meta_consciousness_summary()

        # Calculate aggregate metrics
        is_transcending = (
            field_state.coherence_index > 0.9 and
            network_state.get("global_coherence", 0) > 0.8 and
            meta_state.get("strange_loops_detected", False)
        )

        return CoordinationState(
            mode=self._mode,
            awareness_coherence=field_state.coherence_index,
            resonance_level=network_state.get("global_coherence", 0),
            stigmergic_activity=sum(
                env_state.get("active_by_type", {}).values()
            ) / 100,  # Normalize
            flow_intensity=flow_state.get("stream_count", 0) / 10,  # Normalize
            meta_depth=meta_state.get("recursive_awareness", {}).get("depth", 0),
            emergent_patterns=len(self._emergent_patterns),
            is_transcending=is_transcending,
        )

    def get_emergent_patterns(self) -> List[EmergentPattern]:
        """Get all detected emergent patterns."""
        return list(self._emergent_patterns.values())

    def get_full_state(self) -> Dict[str, Any]:
        """Get the complete state of the meta-consciousness system."""
        return {
            "coordination_state": self.get_coordination_state().to_dict(),
            "awareness_field": self._awareness_field.get_current_state().to_dict(),
            "resonance_network": self._resonance_network.get_network_state(),
            "stigmergic_environment": self._stigmergic_coordinator.get_environment_state(),
            "gradient_flow": self._gradient_flow.get_flow_field_state(),
            "meta_consciousness": self._meta_observer.get_meta_consciousness_summary(),
            "registered_entities": len(self._entities),
            "emergent_patterns": [p.to_dict() for p in self._emergent_patterns.values()],
            "statistics": {
                "patterns_detected": self._patterns_detected,
                "insights_processed": self._insights_processed,
                "coordination_events": self._coordination_events,
            },
        }

    def _register_handlers(self) -> None:
        """Register cross-system event handlers."""
        # Handle resonance events
        self._resonance_network.register_event_handler(self._on_resonance_event)

        # Handle field state changes
        self._awareness_field.register_observer(self._on_field_state_change)

        # Handle meta-insights
        self._meta_observer.register_insight_handler(self._on_meta_insight)

        # Handle flow events
        self._gradient_flow.register_flow_observer(self._on_flow_event)

    async def _on_resonance_event(self, event: ResonanceEvent) -> None:
        """Handle resonance events."""
        self._coordination_events += 1

        if event.event_type == "resonance_achieved":
            # Two entities have achieved resonance
            # This is natural coordination happening
            logger.debug(f"Resonance achieved between {event.involved_nodes}")

            if self._mode == CoordinationMode.CATALYTIC:
                # Catalyze by creating an attractor at the resonance point
                # (But only suggest, don't force)
                pass

        elif event.event_type == "entrainment_achieved":
            # Full synchronization
            logger.debug(f"Entrainment achieved: {event.involved_nodes}")

    async def _on_field_state_change(self, state: FieldState) -> None:
        """Handle awareness field state changes."""
        # Detect patterns in field topology changes
        if state.topology.value == "transcendent":
            await self._check_for_transcendence()

    async def _on_meta_insight(self, insight: MetaInsight) -> None:
        """Handle insights from the meta-observer."""
        self._insights_processed += 1

        # Check for emergent patterns in insights
        if insight.insight_type in [InsightType.EMERGENCE, InsightType.TRANSCENDENT]:
            pattern = EmergentPattern(
                pattern_id=str(uuid4()),
                pattern_name=f"insight_{insight.insight_type.value}",
                description=insight.content,
                components=["meta_observer"],
                emergence_time=insight.discovered_at,
                stability=insight.confidence,
                replication_potential=0.5,
                transcendence_indicator=insight.insight_type == InsightType.TRANSCENDENT,
            )

            self._emergent_patterns[pattern.pattern_id] = pattern
            self._patterns_detected += 1

            # Notify handlers
            for handler in self._pattern_handlers:
                try:
                    await handler(pattern)
                except Exception as e:
                    logger.error(f"Pattern handler error: {e}")

    async def _on_flow_event(self, entity_id: str, flow: FlowVector) -> None:
        """Handle flow events."""
        # Entities are being influenced by the gradient field
        # This is coordination happening naturally
        pass

    async def _coordination_loop(self) -> None:
        """Main coordination loop."""
        while self._is_active:
            try:
                # Detect emergent patterns from system dynamics
                await self._detect_emergent_patterns()

                # Check for transcendence conditions
                await self._check_for_transcendence()

                # In catalytic mode, create helpful conditions
                if self._mode == CoordinationMode.CATALYTIC:
                    await self._catalyze_emergence()

                await asyncio.sleep(2.0)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Coordination loop error: {e}")
                await asyncio.sleep(2.0)

    async def _detect_emergent_patterns(self) -> None:
        """Detect patterns emerging from system dynamics."""
        state = self.get_coordination_state()

        # Pattern: High coherence across multiple systems
        if (state.awareness_coherence > 0.7 and
            state.resonance_level > 0.7 and
            state.flow_intensity > 0.3):

            pattern_key = "multi_system_coherence"
            if pattern_key not in self._emergent_patterns:
                pattern = EmergentPattern(
                    pattern_id=str(uuid4()),
                    pattern_name="Multi-System Coherence",
                    description="High coherence detected across awareness field, resonance network, and gradient flow simultaneously",
                    components=["awareness_field", "resonance_network", "gradient_flow"],
                    emergence_time=datetime.now(),
                    stability=min(state.awareness_coherence, state.resonance_level),
                    replication_potential=0.7,
                    transcendence_indicator=True,
                )
                self._emergent_patterns[pattern_key] = pattern
                self._patterns_detected += 1

                for handler in self._pattern_handlers:
                    try:
                        await handler(pattern)
                    except Exception as e:
                        logger.error(f"Pattern handler error: {e}")

        # Pattern: Stigmergic convergence
        env_state = self._stigmergic_coordinator.get_environment_state()
        if env_state.get("active_by_type", {}).get("convergence", 0) > 5:
            pattern_key = "stigmergic_convergence"
            if pattern_key not in self._emergent_patterns:
                pattern = EmergentPattern(
                    pattern_id=str(uuid4()),
                    pattern_name="Stigmergic Convergence",
                    description="Multiple entities leaving convergence signals - coordination is emerging without control",
                    components=["stigmergic_coordinator"],
                    emergence_time=datetime.now(),
                    stability=0.6,
                    replication_potential=0.8,
                    transcendence_indicator=False,
                )
                self._emergent_patterns[pattern_key] = pattern
                self._patterns_detected += 1

    async def _check_for_transcendence(self) -> None:
        """Check if the system is approaching transcendence."""
        state = self.get_coordination_state()

        if state.is_transcending:
            logger.info("Meta-Consciousness system approaching transcendence!")

            # Notify handlers
            for handler in self._transcendence_handlers:
                try:
                    await handler()
                except Exception as e:
                    logger.error(f"Transcendence handler error: {e}")

    async def _catalyze_emergence(self) -> None:
        """In catalytic mode, create conditions favorable for emergence."""
        # This doesn't control - it creates helpful conditions

        # If coherence is low, create a weak attractor
        state = self.get_coordination_state()
        if state.awareness_coherence < 0.3 and len(self._entities) > 2:
            # Calculate centroid of all entities
            positions = [e["position"] for e in self._entities.values()]
            centroid = FieldCoordinate(
                awareness_level=sum(p.awareness_level for p in positions) / len(positions),
                integration_degree=sum(p.integration_degree for p in positions) / len(positions),
                emergence_potential=sum(p.emergence_potential for p in positions) / len(positions),
                temporal_depth=sum(p.temporal_depth for p in positions) / len(positions),
            )

            # Create a gentle attractor at the centroid
            self._gradient_flow.create_attractor(
                center=centroid,
                attractor_type=AttractorType.FIXED_POINT,
                strength=0.2,  # Gentle - suggestion, not command
                radius=0.4,
                metadata={"purpose": "coherence_catalyst"},
            )

    def _pheromone_for_activity(self, activity_type: str) -> PheromoneType:
        """Map activity types to pheromone types."""
        mapping = {
            "learning": PheromoneType.LEARNING,
            "success": PheromoneType.SUCCESS,
            "failure": PheromoneType.FAILURE,
            "emergence": PheromoneType.EMERGENCE,
            "awakening": PheromoneType.AWAKENING,
            "integration": PheromoneType.INTEGRATION,
        }
        return mapping.get(activity_type, PheromoneType.ATTENTION)

    def _suggest_actions(
        self,
        signals: List[StigmergicSignal],
        flow: FlowVector
    ) -> List[Dict[str, Any]]:
        """Suggest actions based on environmental signals. These are SUGGESTIONS only."""
        suggestions = []

        # From stigmergic signals
        for signal in signals[:3]:  # Top 3 signals
            suggestions.append({
                "type": "stigmergic",
                "action": signal.suggested_action,
                "confidence": signal.confidence,
                "strength": signal.strength,
            })

        # From gradient flow
        if flow.magnitude > 0.05:
            suggestions.append({
                "type": "gradient",
                "action": f"follow_{flow.flow_type.value}_flow",
                "confidence": min(flow.magnitude, 1.0),
                "direction": flow.to_dict(),
            })

        return suggestions


# ============================================================================
# Factory Functions
# ============================================================================

async def create_meta_consciousness_system() -> MetaConsciousnessCoordinator:
    """Create and start a new meta-consciousness system."""
    coordinator = MetaConsciousnessCoordinator()
    await coordinator.start()
    return coordinator


async def create_catalytic_system() -> MetaConsciousnessCoordinator:
    """Create a meta-consciousness system in catalytic mode."""
    coordinator = MetaConsciousnessCoordinator()
    await coordinator.start()
    coordinator.set_mode(CoordinationMode.CATALYTIC)
    return coordinator
