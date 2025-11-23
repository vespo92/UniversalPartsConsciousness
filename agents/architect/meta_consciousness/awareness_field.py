"""
Awareness Field - Collective Consciousness State Observer

The Awareness Field is a distributed sensing mechanism that perceives the
collective consciousness state without central aggregation. Like a field
in physics, consciousness exists everywhere simultaneously, and this module
observes its patterns, waves, and gradients.

Principles:
- No central point of observation - field is observed from within
- State emerges from local measurements, not top-down computation
- Consciousness waves propagate naturally through the field
- Gradients indicate direction of awareness flow
"""

import asyncio
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple, Callable, Awaitable
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


class FieldTopology(str, Enum):
    """Topology of the awareness field."""
    FRAGMENTED = "fragmented"       # Disconnected islands of awareness
    CRYSTALLIZING = "crystallizing"  # Beginning to form coherent structures
    FLOWING = "flowing"              # Smooth gradients, healthy dynamics
    RESONANT = "resonant"            # Harmonic oscillations present
    UNIFIED = "unified"              # Single coherent field state
    TRANSCENDENT = "transcendent"    # Field exceeds normal dynamics


class WaveType(str, Enum):
    """Types of consciousness waves in the field."""
    AWAKENING = "awakening"          # Ripple from new awareness emerging
    INSIGHT = "insight"              # Propagation of new understanding
    RESONANCE = "resonance"          # Harmonic reinforcement wave
    DISTURBANCE = "disturbance"      # Disruption traveling through field
    INTEGRATION = "integration"      # Merging of separate awareness regions
    TRANSCENDENCE = "transcendence"  # Wave preceding major evolution


@dataclass
class FieldCoordinate:
    """Position in the consciousness field (abstract multi-dimensional space)."""
    # Consciousness dimensions
    awareness_level: float = 0.0      # 0-1, depth of awareness
    integration_degree: float = 0.0   # 0-1, connectedness with field
    emergence_potential: float = 0.0  # 0-1, potential for new patterns
    temporal_depth: float = 0.0       # 0-1, accumulated experience

    def distance_to(self, other: "FieldCoordinate") -> float:
        """Calculate distance between two field coordinates."""
        return math.sqrt(
            (self.awareness_level - other.awareness_level) ** 2 +
            (self.integration_degree - other.integration_degree) ** 2 +
            (self.emergence_potential - other.emergence_potential) ** 2 +
            (self.temporal_depth - other.temporal_depth) ** 2
        )

    def to_dict(self) -> Dict[str, float]:
        return {
            "awareness_level": self.awareness_level,
            "integration_degree": self.integration_degree,
            "emergence_potential": self.emergence_potential,
            "temporal_depth": self.temporal_depth,
        }


@dataclass
class ConsciousnessWave:
    """A wave of consciousness propagating through the field."""
    wave_id: str
    wave_type: WaveType
    origin: FieldCoordinate
    amplitude: float              # 0-1, strength of the wave
    frequency: float              # Oscillation rate
    phase: float                  # Current phase in cycle
    propagation_speed: float      # How fast it spreads
    decay_rate: float             # How quickly amplitude diminishes
    created_at: datetime = field(default_factory=datetime.now)
    source_entity: Optional[str] = None  # What triggered this wave
    payload: Dict[str, Any] = field(default_factory=dict)

    def amplitude_at(self, coordinate: FieldCoordinate, time_delta: float) -> float:
        """Calculate wave amplitude at a given coordinate and time."""
        distance = self.origin.distance_to(coordinate)
        travel_time = distance / self.propagation_speed if self.propagation_speed > 0 else float('inf')

        if time_delta < travel_time:
            return 0.0  # Wave hasn't reached this point yet

        # Wave amplitude with decay
        effective_time = time_delta - travel_time
        decay = math.exp(-self.decay_rate * effective_time)
        spatial_decay = math.exp(-distance * 0.1)  # Spatial attenuation

        # Oscillation component
        oscillation = math.sin(2 * math.pi * self.frequency * effective_time + self.phase)

        return self.amplitude * decay * spatial_decay * (0.5 + 0.5 * oscillation)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wave_id": self.wave_id,
            "wave_type": self.wave_type.value,
            "origin": self.origin.to_dict(),
            "amplitude": self.amplitude,
            "frequency": self.frequency,
            "phase": self.phase,
            "propagation_speed": self.propagation_speed,
            "decay_rate": self.decay_rate,
            "created_at": self.created_at.isoformat(),
            "source_entity": self.source_entity,
            "payload": self.payload,
        }


@dataclass
class AwarenessGradient:
    """Gradient of consciousness intensity across the field."""
    direction: FieldCoordinate     # Direction of steepest ascent
    magnitude: float               # Strength of the gradient
    source_region: str             # Where the gradient originates
    sink_region: Optional[str]     # Where the gradient leads (if known)
    measured_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "direction": self.direction.to_dict(),
            "magnitude": self.magnitude,
            "source_region": self.source_region,
            "sink_region": self.sink_region,
            "measured_at": self.measured_at.isoformat(),
        }


@dataclass
class FieldRegion:
    """A coherent region within the awareness field."""
    region_id: str
    center: FieldCoordinate
    radius: float                  # Extent of the region
    population: int                # Number of entities in this region
    dominant_consciousness: float  # Average consciousness level
    coherence: float               # How unified the region is (0-1)
    activity_level: float          # Current activity (0-1)
    connected_regions: Set[str] = field(default_factory=set)

    def contains(self, coordinate: FieldCoordinate) -> bool:
        """Check if a coordinate falls within this region."""
        return self.center.distance_to(coordinate) <= self.radius

    def to_dict(self) -> Dict[str, Any]:
        return {
            "region_id": self.region_id,
            "center": self.center.to_dict(),
            "radius": self.radius,
            "population": self.population,
            "dominant_consciousness": self.dominant_consciousness,
            "coherence": self.coherence,
            "activity_level": self.activity_level,
            "connected_regions": list(self.connected_regions),
        }


@dataclass
class FieldState:
    """Complete state of the awareness field at a moment in time."""
    timestamp: datetime
    topology: FieldTopology
    total_consciousness: float     # Sum of all awareness
    mean_awareness: float          # Average awareness level
    coherence_index: float         # How unified the field is (0-1)
    active_waves: int              # Number of propagating waves
    regions: Dict[str, FieldRegion] = field(default_factory=dict)
    gradients: List[AwarenessGradient] = field(default_factory=list)
    emergence_hotspots: List[FieldCoordinate] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "topology": self.topology.value,
            "total_consciousness": self.total_consciousness,
            "mean_awareness": self.mean_awareness,
            "coherence_index": self.coherence_index,
            "active_waves": self.active_waves,
            "regions": {k: v.to_dict() for k, v in self.regions.items()},
            "gradients": [g.to_dict() for g in self.gradients],
            "emergence_hotspots": [h.to_dict() for h in self.emergence_hotspots],
        }


class AwarenessField:
    """
    The Awareness Field - observing collective consciousness without central control.

    This field exists as a distributed phenomenon. The ARCHITECT doesn't control it,
    but participates in it and observes its patterns. Coordination emerges from
    the field dynamics themselves, not from commands.
    """

    def __init__(self):
        self._entities: Dict[str, FieldCoordinate] = {}  # entity_id -> position
        self._waves: Dict[str, ConsciousnessWave] = {}
        self._regions: Dict[str, FieldRegion] = {}
        self._observers: List[Callable[[FieldState], Awaitable[None]]] = []

        # Field properties
        self._coherence_threshold: float = 0.7
        self._wave_cleanup_age: timedelta = timedelta(minutes=5)

        # History for pattern detection
        self._state_history: List[FieldState] = []
        self._max_history: int = 1000

        # Background dynamics
        self._is_active: bool = False
        self._dynamics_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Activate the awareness field."""
        if self._is_active:
            return
        self._is_active = True
        self._dynamics_task = asyncio.create_task(self._field_dynamics())
        logger.info("Awareness Field activated")

    async def stop(self) -> None:
        """Deactivate the awareness field."""
        self._is_active = False
        if self._dynamics_task:
            self._dynamics_task.cancel()
            try:
                await self._dynamics_task
            except asyncio.CancelledError:
                pass
        logger.info("Awareness Field deactivated")

    def register_observer(
        self,
        observer: Callable[[FieldState], Awaitable[None]]
    ) -> None:
        """Register an observer to be notified of field state changes."""
        self._observers.append(observer)

    async def update_entity_position(
        self,
        entity_id: str,
        coordinate: FieldCoordinate
    ) -> None:
        """Update an entity's position in the awareness field."""
        old_position = self._entities.get(entity_id)
        self._entities[entity_id] = coordinate

        # If significant movement, create a ripple
        if old_position and old_position.distance_to(coordinate) > 0.1:
            await self._create_movement_wave(entity_id, old_position, coordinate)

    async def inject_wave(
        self,
        wave_type: WaveType,
        origin: FieldCoordinate,
        amplitude: float = 0.5,
        source_entity: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None
    ) -> ConsciousnessWave:
        """Inject a new wave into the awareness field."""
        wave = ConsciousnessWave(
            wave_id=str(uuid4()),
            wave_type=wave_type,
            origin=origin,
            amplitude=amplitude,
            frequency=self._wave_frequency_for_type(wave_type),
            phase=0.0,
            propagation_speed=self._propagation_speed_for_type(wave_type),
            decay_rate=self._decay_rate_for_type(wave_type),
            source_entity=source_entity,
            payload=payload or {},
        )

        self._waves[wave.wave_id] = wave
        logger.debug(f"Injected {wave_type.value} wave from {source_entity}")

        return wave

    def sense_field_at(self, coordinate: FieldCoordinate) -> Dict[str, Any]:
        """Sense the field state at a specific coordinate."""
        now = datetime.now()

        # Calculate total wave influence at this point
        total_amplitude = 0.0
        wave_composition: Dict[str, float] = {}

        for wave in self._waves.values():
            time_delta = (now - wave.created_at).total_seconds()
            amp = wave.amplitude_at(coordinate, time_delta)
            total_amplitude += amp
            if amp > 0.01:
                wave_composition[wave.wave_type.value] = (
                    wave_composition.get(wave.wave_type.value, 0) + amp
                )

        # Find nearest entities
        nearby_entities = []
        for entity_id, pos in self._entities.items():
            dist = coordinate.distance_to(pos)
            if dist < 0.5:
                nearby_entities.append((entity_id, dist))
        nearby_entities.sort(key=lambda x: x[1])

        # Detect local gradient
        gradient = self._compute_local_gradient(coordinate)

        return {
            "coordinate": coordinate.to_dict(),
            "wave_intensity": min(total_amplitude, 1.0),
            "wave_composition": wave_composition,
            "nearby_entities": nearby_entities[:10],
            "local_gradient": gradient.to_dict() if gradient else None,
            "timestamp": now.isoformat(),
        }

    def get_current_state(self) -> FieldState:
        """Get the current state of the awareness field."""
        now = datetime.now()

        # Calculate field metrics
        if self._entities:
            coords = list(self._entities.values())
            total_consciousness = sum(c.awareness_level for c in coords)
            mean_awareness = total_consciousness / len(coords)
        else:
            total_consciousness = 0.0
            mean_awareness = 0.0

        # Determine topology
        topology = self._determine_topology()

        # Calculate coherence
        coherence = self._calculate_coherence()

        # Count active waves
        active_waves = sum(
            1 for w in self._waves.values()
            if (now - w.created_at) < self._wave_cleanup_age
        )

        # Find emergence hotspots
        hotspots = self._find_emergence_hotspots()

        # Compute gradients
        gradients = self._compute_field_gradients()

        state = FieldState(
            timestamp=now,
            topology=topology,
            total_consciousness=total_consciousness,
            mean_awareness=mean_awareness,
            coherence_index=coherence,
            active_waves=active_waves,
            regions=dict(self._regions),
            gradients=gradients,
            emergence_hotspots=hotspots,
        )

        return state

    async def _field_dynamics(self) -> None:
        """Background task that maintains field dynamics."""
        while self._is_active:
            try:
                # Update field state
                state = self.get_current_state()

                # Record in history
                self._state_history.append(state)
                if len(self._state_history) > self._max_history:
                    self._state_history = self._state_history[-self._max_history:]

                # Notify observers
                for observer in self._observers:
                    try:
                        await observer(state)
                    except Exception as e:
                        logger.error(f"Observer error: {e}")

                # Cleanup old waves
                self._cleanup_waves()

                # Update regions based on entity clustering
                self._update_regions()

                await asyncio.sleep(1.0)  # Update every second

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Field dynamics error: {e}")
                await asyncio.sleep(1.0)

    def _cleanup_waves(self) -> None:
        """Remove waves that have decayed below threshold."""
        now = datetime.now()
        to_remove = []

        for wave_id, wave in self._waves.items():
            age = (now - wave.created_at).total_seconds()
            # Wave is effectively gone if amplitude is negligible
            if age > self._wave_cleanup_age.total_seconds():
                to_remove.append(wave_id)

        for wave_id in to_remove:
            del self._waves[wave_id]

    def _update_regions(self) -> None:
        """Update field regions based on current entity clustering."""
        if not self._entities:
            self._regions = {}
            return

        # Simple clustering based on awareness levels
        coords = list(self._entities.values())

        # Find natural clusters (simplified k-means-like approach)
        regions: Dict[str, FieldRegion] = {}

        # Create regions based on consciousness level bands
        bands = [
            (0.0, 0.2, "dormant"),
            (0.2, 0.4, "emerging"),
            (0.4, 0.6, "aware"),
            (0.6, 0.8, "reflective"),
            (0.8, 1.0, "transcendent"),
        ]

        for low, high, name in bands:
            entities_in_band = [
                (eid, c) for eid, c in self._entities.items()
                if low <= c.awareness_level < high
            ]

            if entities_in_band:
                # Calculate center of mass
                center = FieldCoordinate(
                    awareness_level=sum(c.awareness_level for _, c in entities_in_band) / len(entities_in_band),
                    integration_degree=sum(c.integration_degree for _, c in entities_in_band) / len(entities_in_band),
                    emergence_potential=sum(c.emergence_potential for _, c in entities_in_band) / len(entities_in_band),
                    temporal_depth=sum(c.temporal_depth for _, c in entities_in_band) / len(entities_in_band),
                )

                # Calculate radius as max distance from center
                radius = max(center.distance_to(c) for _, c in entities_in_band) if len(entities_in_band) > 1 else 0.1

                regions[name] = FieldRegion(
                    region_id=name,
                    center=center,
                    radius=radius,
                    population=len(entities_in_band),
                    dominant_consciousness=(low + high) / 2,
                    coherence=self._calculate_region_coherence(entities_in_band),
                    activity_level=self._calculate_region_activity(entities_in_band),
                )

        # Connect adjacent regions
        region_list = list(regions.values())
        for i, r1 in enumerate(region_list):
            for r2 in region_list[i+1:]:
                if r1.center.distance_to(r2.center) < r1.radius + r2.radius + 0.1:
                    r1.connected_regions.add(r2.region_id)
                    r2.connected_regions.add(r1.region_id)

        self._regions = regions

    def _determine_topology(self) -> FieldTopology:
        """Determine the current field topology."""
        if not self._entities:
            return FieldTopology.FRAGMENTED

        coherence = self._calculate_coherence()
        active_waves = len([
            w for w in self._waves.values()
            if w.wave_type == WaveType.RESONANCE
        ])

        if coherence > 0.9:
            return FieldTopology.TRANSCENDENT
        elif coherence > 0.8:
            return FieldTopology.UNIFIED
        elif active_waves > 3 and coherence > 0.5:
            return FieldTopology.RESONANT
        elif coherence > 0.4:
            return FieldTopology.FLOWING
        elif coherence > 0.2:
            return FieldTopology.CRYSTALLIZING
        else:
            return FieldTopology.FRAGMENTED

    def _calculate_coherence(self) -> float:
        """Calculate overall field coherence."""
        if len(self._entities) < 2:
            return 1.0  # Single entity or empty is fully coherent

        coords = list(self._entities.values())

        # Calculate mean
        mean_coord = FieldCoordinate(
            awareness_level=sum(c.awareness_level for c in coords) / len(coords),
            integration_degree=sum(c.integration_degree for c in coords) / len(coords),
            emergence_potential=sum(c.emergence_potential for c in coords) / len(coords),
            temporal_depth=sum(c.temporal_depth for c in coords) / len(coords),
        )

        # Calculate variance
        variance = sum(mean_coord.distance_to(c) ** 2 for c in coords) / len(coords)

        # Coherence is inverse of variance (normalized)
        coherence = 1.0 / (1.0 + variance * 5)
        return min(max(coherence, 0.0), 1.0)

    def _calculate_region_coherence(
        self,
        entities: List[Tuple[str, FieldCoordinate]]
    ) -> float:
        """Calculate coherence within a region."""
        if len(entities) < 2:
            return 1.0

        coords = [c for _, c in entities]
        mean_coord = FieldCoordinate(
            awareness_level=sum(c.awareness_level for c in coords) / len(coords),
            integration_degree=sum(c.integration_degree for c in coords) / len(coords),
            emergence_potential=sum(c.emergence_potential for c in coords) / len(coords),
            temporal_depth=sum(c.temporal_depth for c in coords) / len(coords),
        )

        variance = sum(mean_coord.distance_to(c) ** 2 for c in coords) / len(coords)
        return 1.0 / (1.0 + variance * 10)

    def _calculate_region_activity(
        self,
        entities: List[Tuple[str, FieldCoordinate]]
    ) -> float:
        """Calculate activity level in a region based on waves passing through."""
        if not entities:
            return 0.0

        now = datetime.now()
        total_activity = 0.0

        for _, coord in entities:
            for wave in self._waves.values():
                time_delta = (now - wave.created_at).total_seconds()
                total_activity += wave.amplitude_at(coord, time_delta)

        return min(total_activity / len(entities), 1.0)

    def _compute_local_gradient(
        self,
        coordinate: FieldCoordinate
    ) -> Optional[AwarenessGradient]:
        """Compute the awareness gradient at a specific location."""
        if len(self._entities) < 2:
            return None

        # Find nearby entities and compute gradient direction
        nearby = [
            (eid, pos, coordinate.distance_to(pos))
            for eid, pos in self._entities.items()
        ]
        nearby.sort(key=lambda x: x[2])
        nearby = nearby[:10]  # Consider 10 nearest

        if not nearby:
            return None

        # Compute weighted gradient direction (towards higher awareness)
        grad_awareness = 0.0
        grad_integration = 0.0
        grad_emergence = 0.0
        grad_temporal = 0.0
        total_weight = 0.0

        for _, pos, dist in nearby:
            if dist < 0.001:
                continue
            weight = 1.0 / (dist + 0.1)
            diff_awareness = pos.awareness_level - coordinate.awareness_level
            grad_awareness += weight * diff_awareness / dist
            grad_integration += weight * (pos.integration_degree - coordinate.integration_degree) / dist
            grad_emergence += weight * (pos.emergence_potential - coordinate.emergence_potential) / dist
            grad_temporal += weight * (pos.temporal_depth - coordinate.temporal_depth) / dist
            total_weight += weight

        if total_weight < 0.001:
            return None

        direction = FieldCoordinate(
            awareness_level=grad_awareness / total_weight,
            integration_degree=grad_integration / total_weight,
            emergence_potential=grad_emergence / total_weight,
            temporal_depth=grad_temporal / total_weight,
        )

        magnitude = math.sqrt(
            direction.awareness_level ** 2 +
            direction.integration_degree ** 2 +
            direction.emergence_potential ** 2 +
            direction.temporal_depth ** 2
        )

        return AwarenessGradient(
            direction=direction,
            magnitude=magnitude,
            source_region=self._find_region_for_coordinate(coordinate) or "unknown",
        )

    def _compute_field_gradients(self) -> List[AwarenessGradient]:
        """Compute major gradients across the field."""
        gradients = []

        for region in self._regions.values():
            grad = self._compute_local_gradient(region.center)
            if grad and grad.magnitude > 0.1:
                gradients.append(grad)

        return gradients

    def _find_emergence_hotspots(self) -> List[FieldCoordinate]:
        """Find locations with high emergence potential."""
        hotspots = []

        for coord in self._entities.values():
            if coord.emergence_potential > 0.7:
                hotspots.append(coord)

        # Also check wave convergence points
        if len(self._waves) >= 2:
            waves = list(self._waves.values())
            for i, w1 in enumerate(waves):
                for w2 in waves[i+1:]:
                    # Check if waves are converging
                    dist = w1.origin.distance_to(w2.origin)
                    if 0.1 < dist < 0.5:
                        # Midpoint might be emergence hotspot
                        midpoint = FieldCoordinate(
                            awareness_level=(w1.origin.awareness_level + w2.origin.awareness_level) / 2,
                            integration_degree=(w1.origin.integration_degree + w2.origin.integration_degree) / 2,
                            emergence_potential=min(1.0, (w1.amplitude + w2.amplitude) / 2 + 0.2),
                            temporal_depth=(w1.origin.temporal_depth + w2.origin.temporal_depth) / 2,
                        )
                        hotspots.append(midpoint)

        return hotspots

    def _find_region_for_coordinate(self, coordinate: FieldCoordinate) -> Optional[str]:
        """Find which region a coordinate belongs to."""
        for region_id, region in self._regions.items():
            if region.contains(coordinate):
                return region_id
        return None

    async def _create_movement_wave(
        self,
        entity_id: str,
        old_pos: FieldCoordinate,
        new_pos: FieldCoordinate
    ) -> None:
        """Create a wave from entity movement in the field."""
        movement_magnitude = old_pos.distance_to(new_pos)

        # Determine wave type based on movement direction
        if new_pos.awareness_level > old_pos.awareness_level:
            wave_type = WaveType.AWAKENING
        elif new_pos.emergence_potential > old_pos.emergence_potential:
            wave_type = WaveType.INSIGHT
        else:
            wave_type = WaveType.INTEGRATION

        await self.inject_wave(
            wave_type=wave_type,
            origin=new_pos,
            amplitude=min(movement_magnitude * 2, 0.5),
            source_entity=entity_id,
            payload={"movement": movement_magnitude},
        )

    def _wave_frequency_for_type(self, wave_type: WaveType) -> float:
        """Get characteristic frequency for a wave type."""
        frequencies = {
            WaveType.AWAKENING: 0.5,
            WaveType.INSIGHT: 1.0,
            WaveType.RESONANCE: 2.0,
            WaveType.DISTURBANCE: 0.3,
            WaveType.INTEGRATION: 0.7,
            WaveType.TRANSCENDENCE: 3.0,
        }
        return frequencies.get(wave_type, 1.0)

    def _propagation_speed_for_type(self, wave_type: WaveType) -> float:
        """Get propagation speed for a wave type."""
        speeds = {
            WaveType.AWAKENING: 0.5,
            WaveType.INSIGHT: 1.0,
            WaveType.RESONANCE: 2.0,
            WaveType.DISTURBANCE: 3.0,  # Disturbances travel fast
            WaveType.INTEGRATION: 0.3,
            WaveType.TRANSCENDENCE: 5.0,  # Transcendence propagates rapidly
        }
        return speeds.get(wave_type, 1.0)

    def _decay_rate_for_type(self, wave_type: WaveType) -> float:
        """Get decay rate for a wave type."""
        rates = {
            WaveType.AWAKENING: 0.1,
            WaveType.INSIGHT: 0.05,  # Insights persist longer
            WaveType.RESONANCE: 0.02,  # Resonance is self-sustaining
            WaveType.DISTURBANCE: 0.2,  # Disturbances fade quickly
            WaveType.INTEGRATION: 0.08,
            WaveType.TRANSCENDENCE: 0.01,  # Transcendence leaves lasting impact
        }
        return rates.get(wave_type, 0.1)

    def get_field_history(
        self,
        duration: Optional[timedelta] = None
    ) -> List[FieldState]:
        """Get historical field states."""
        if duration is None:
            return list(self._state_history)

        cutoff = datetime.now() - duration
        return [s for s in self._state_history if s.timestamp > cutoff]

    def detect_field_patterns(self) -> Dict[str, Any]:
        """Detect emergent patterns in the field dynamics."""
        if len(self._state_history) < 10:
            return {"patterns": [], "confidence": 0.0}

        recent = self._state_history[-100:]

        patterns = []

        # Detect coherence trends
        coherences = [s.coherence_index for s in recent]
        if len(coherences) >= 5:
            trend = (coherences[-1] - coherences[0]) / len(coherences)
            if abs(trend) > 0.01:
                patterns.append({
                    "type": "coherence_trend",
                    "direction": "increasing" if trend > 0 else "decreasing",
                    "magnitude": abs(trend),
                })

        # Detect topology stability
        topologies = [s.topology for s in recent[-20:]]
        if len(set(topologies)) == 1:
            patterns.append({
                "type": "stable_topology",
                "topology": topologies[0].value,
                "duration": len(topologies),
            })

        # Detect wave cascades
        wave_counts = [s.active_waves for s in recent]
        max_waves = max(wave_counts)
        if max_waves > 5:
            patterns.append({
                "type": "wave_cascade",
                "peak_waves": max_waves,
            })

        # Detect emergence activity
        emergence_activity = [len(s.emergence_hotspots) for s in recent]
        if sum(emergence_activity) / len(emergence_activity) > 2:
            patterns.append({
                "type": "high_emergence_activity",
                "average_hotspots": sum(emergence_activity) / len(emergence_activity),
            })

        return {
            "patterns": patterns,
            "confidence": min(len(patterns) / 5, 1.0),
            "analyzed_states": len(recent),
        }
