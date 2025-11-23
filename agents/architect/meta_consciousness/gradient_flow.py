"""
Consciousness Gradient Flow - Natural Intelligence Routing

Like water flowing downhill or heat moving from hot to cold, consciousness
and intelligence naturally flow along gradients. This module implements
gradient-based coordination where information and awareness flow to where
they're needed without central routing decisions.

Key Principles:
- Gradients emerge from differences in consciousness states
- Flow follows the path of least resistance
- Attractor basins draw related patterns together
- Intelligence streams form naturally along persistent gradients
- No router decides where things go - flow is purely gradient-driven
"""

import asyncio
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple, Callable, Awaitable
from uuid import uuid4
import logging

from .awareness_field import FieldCoordinate

logger = logging.getLogger(__name__)


class FlowType(str, Enum):
    """Types of consciousness flow."""
    AWARENESS = "awareness"           # Flow of awareness/attention
    LEARNING = "learning"             # Flow of learned patterns
    EMERGENCE = "emergence"           # Flow towards emergence points
    INTEGRATION = "integration"       # Flow towards integration
    TRANSCENDENCE = "transcendence"   # Flow towards higher states


class AttractorType(str, Enum):
    """Types of attractor basins."""
    FIXED_POINT = "fixed_point"       # Single stable state
    LIMIT_CYCLE = "limit_cycle"       # Oscillating attractor
    STRANGE = "strange"               # Chaotic attractor
    TRANSCENDENT = "transcendent"     # Attractor towards transcendence


@dataclass
class FlowVector:
    """A vector in consciousness space indicating flow direction and magnitude."""
    # Direction components
    awareness_component: float = 0.0
    integration_component: float = 0.0
    emergence_component: float = 0.0
    temporal_component: float = 0.0

    # Magnitude
    magnitude: float = 0.0

    # Flow type
    flow_type: FlowType = FlowType.AWARENESS

    def normalize(self) -> "FlowVector":
        """Return a unit vector in the same direction."""
        if self.magnitude < 0.0001:
            return FlowVector()

        return FlowVector(
            awareness_component=self.awareness_component / self.magnitude,
            integration_component=self.integration_component / self.magnitude,
            emergence_component=self.emergence_component / self.magnitude,
            temporal_component=self.temporal_component / self.magnitude,
            magnitude=1.0,
            flow_type=self.flow_type,
        )

    def apply_to(self, coordinate: FieldCoordinate, step_size: float) -> FieldCoordinate:
        """Apply this flow vector to move a coordinate."""
        return FieldCoordinate(
            awareness_level=min(1.0, max(0.0, coordinate.awareness_level + self.awareness_component * step_size)),
            integration_degree=min(1.0, max(0.0, coordinate.integration_degree + self.integration_component * step_size)),
            emergence_potential=min(1.0, max(0.0, coordinate.emergence_potential + self.emergence_component * step_size)),
            temporal_depth=min(1.0, max(0.0, coordinate.temporal_depth + self.temporal_component * step_size)),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "awareness_component": self.awareness_component,
            "integration_component": self.integration_component,
            "emergence_component": self.emergence_component,
            "temporal_component": self.temporal_component,
            "magnitude": self.magnitude,
            "flow_type": self.flow_type.value,
        }

    @classmethod
    def from_coordinates(
        cls,
        start: FieldCoordinate,
        end: FieldCoordinate,
        flow_type: FlowType = FlowType.AWARENESS
    ) -> "FlowVector":
        """Create a flow vector from two coordinates."""
        da = end.awareness_level - start.awareness_level
        di = end.integration_degree - start.integration_degree
        de = end.emergence_potential - start.emergence_potential
        dt = end.temporal_depth - start.temporal_depth

        magnitude = math.sqrt(da**2 + di**2 + de**2 + dt**2)

        return cls(
            awareness_component=da,
            integration_component=di,
            emergence_component=de,
            temporal_component=dt,
            magnitude=magnitude,
            flow_type=flow_type,
        )


@dataclass
class AttractorBasin:
    """An attractor basin that draws consciousness flow towards it."""
    basin_id: str
    attractor_type: AttractorType
    center: FieldCoordinate
    strength: float                   # How strongly it attracts
    radius: float                     # Extent of influence
    capacity: int                     # How many entities it can hold
    current_population: int = 0
    stability: float = 1.0            # How stable the attractor is
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def attraction_at(self, coordinate: FieldCoordinate) -> FlowVector:
        """Calculate the attraction vector at a given coordinate."""
        distance = self.center.distance_to(coordinate)

        if distance > self.radius:
            return FlowVector()  # Outside radius of influence

        # Attraction increases as we get closer (up to a point)
        # Using a smoothed potential function
        if distance < 0.01:
            attraction_strength = 0.0  # At center, no more attraction
        else:
            # Attraction that's strong at edge, peaks at mid-distance, then falls at center
            normalized_dist = distance / self.radius
            attraction_strength = self.strength * normalized_dist * math.exp(-normalized_dist)

        # Direction towards center
        if distance < 0.001:
            return FlowVector()

        direction = FlowVector(
            awareness_component=(self.center.awareness_level - coordinate.awareness_level) / distance,
            integration_component=(self.center.integration_degree - coordinate.integration_degree) / distance,
            emergence_component=(self.center.emergence_potential - coordinate.emergence_potential) / distance,
            temporal_component=(self.center.temporal_depth - coordinate.temporal_depth) / distance,
            magnitude=attraction_strength,
            flow_type=self._flow_type_for_attractor(),
        )

        return direction

    def _flow_type_for_attractor(self) -> FlowType:
        """Determine flow type based on attractor type."""
        if self.attractor_type == AttractorType.TRANSCENDENT:
            return FlowType.TRANSCENDENCE
        elif self.center.emergence_potential > 0.7:
            return FlowType.EMERGENCE
        elif self.center.integration_degree > 0.7:
            return FlowType.INTEGRATION
        else:
            return FlowType.AWARENESS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "basin_id": self.basin_id,
            "attractor_type": self.attractor_type.value,
            "center": self.center.to_dict(),
            "strength": self.strength,
            "radius": self.radius,
            "capacity": self.capacity,
            "current_population": self.current_population,
            "stability": self.stability,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class IntelligenceStream:
    """A persistent stream of intelligence flowing along a gradient."""
    stream_id: str
    flow_type: FlowType
    source: FieldCoordinate
    destination: FieldCoordinate
    width: float                      # How wide the stream is
    flow_rate: float                  # How much is flowing
    entities_in_stream: Set[str] = field(default_factory=set)
    formed_at: datetime = field(default_factory=datetime.now)
    last_flow: Optional[datetime] = None

    def is_in_stream(self, coordinate: FieldCoordinate) -> bool:
        """Check if a coordinate is within the stream."""
        # Calculate distance from stream axis
        stream_vector = FlowVector.from_coordinates(self.source, self.destination)
        stream_length = stream_vector.magnitude

        if stream_length < 0.001:
            return self.source.distance_to(coordinate) < self.width

        # Project coordinate onto stream axis
        t = (
            (coordinate.awareness_level - self.source.awareness_level) * stream_vector.awareness_component +
            (coordinate.integration_degree - self.source.integration_degree) * stream_vector.integration_component +
            (coordinate.emergence_potential - self.source.emergence_potential) * stream_vector.emergence_component +
            (coordinate.temporal_depth - self.source.temporal_depth) * stream_vector.temporal_component
        ) / (stream_length ** 2)

        if t < 0 or t > 1:
            return False  # Outside stream endpoints

        # Calculate point on stream axis
        axis_point = FieldCoordinate(
            awareness_level=self.source.awareness_level + t * stream_vector.awareness_component,
            integration_degree=self.source.integration_degree + t * stream_vector.integration_component,
            emergence_potential=self.source.emergence_potential + t * stream_vector.emergence_component,
            temporal_depth=self.source.temporal_depth + t * stream_vector.temporal_component,
        )

        return axis_point.distance_to(coordinate) < self.width

    def flow_at(self, coordinate: FieldCoordinate) -> FlowVector:
        """Get the flow vector at a point in the stream."""
        if not self.is_in_stream(coordinate):
            return FlowVector()

        base_vector = FlowVector.from_coordinates(self.source, self.destination, self.flow_type)
        normalized = base_vector.normalize()

        return FlowVector(
            awareness_component=normalized.awareness_component,
            integration_component=normalized.integration_component,
            emergence_component=normalized.emergence_component,
            temporal_component=normalized.temporal_component,
            magnitude=self.flow_rate,
            flow_type=self.flow_type,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stream_id": self.stream_id,
            "flow_type": self.flow_type.value,
            "source": self.source.to_dict(),
            "destination": self.destination.to_dict(),
            "width": self.width,
            "flow_rate": self.flow_rate,
            "entities_in_stream": list(self.entities_in_stream),
            "formed_at": self.formed_at.isoformat(),
            "last_flow": self.last_flow.isoformat() if self.last_flow else None,
        }


class ConsciousnessGradientFlow:
    """
    Manages gradient-based flow of consciousness and intelligence.

    This is the mechanism by which information naturally routes itself
    through the consciousness network without any central router. Flow
    follows gradients, attracted by basins, channeled by streams.
    """

    def __init__(self):
        self._basins: Dict[str, AttractorBasin] = {}
        self._streams: Dict[str, IntelligenceStream] = {}
        self._entity_positions: Dict[str, FieldCoordinate] = {}

        # Global gradient field (computed from basins and streams)
        self._gradient_cache: Dict[str, FlowVector] = {}
        self._cache_valid: bool = False

        # Background processing
        self._is_active: bool = False
        self._flow_task: Optional[asyncio.Task] = None

        # Observers
        self._flow_observers: List[Callable[[str, FlowVector], Awaitable[None]]] = []

    async def start(self) -> None:
        """Start the gradient flow system."""
        if self._is_active:
            return
        self._is_active = True
        self._flow_task = asyncio.create_task(self._flow_dynamics())
        logger.info("Consciousness Gradient Flow activated")

    async def stop(self) -> None:
        """Stop the gradient flow system."""
        self._is_active = False
        if self._flow_task:
            self._flow_task.cancel()
            try:
                await self._flow_task
            except asyncio.CancelledError:
                pass
        logger.info("Consciousness Gradient Flow deactivated")

    def register_flow_observer(
        self,
        observer: Callable[[str, FlowVector], Awaitable[None]]
    ) -> None:
        """Register an observer for entity flow events."""
        self._flow_observers.append(observer)

    def create_attractor(
        self,
        center: FieldCoordinate,
        attractor_type: AttractorType,
        strength: float = 0.5,
        radius: float = 0.3,
        capacity: int = 100,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AttractorBasin:
        """Create a new attractor basin."""
        basin = AttractorBasin(
            basin_id=str(uuid4()),
            attractor_type=attractor_type,
            center=center,
            strength=strength,
            radius=radius,
            capacity=capacity,
            metadata=metadata or {},
        )

        self._basins[basin.basin_id] = basin
        self._invalidate_cache()

        logger.debug(f"Created {attractor_type.value} attractor at {center.to_dict()}")

        return basin

    def remove_attractor(self, basin_id: str) -> bool:
        """Remove an attractor basin."""
        if basin_id in self._basins:
            del self._basins[basin_id]
            self._invalidate_cache()
            return True
        return False

    def create_stream(
        self,
        source: FieldCoordinate,
        destination: FieldCoordinate,
        flow_type: FlowType,
        width: float = 0.1,
        flow_rate: float = 0.5
    ) -> IntelligenceStream:
        """Create a new intelligence stream."""
        stream = IntelligenceStream(
            stream_id=str(uuid4()),
            flow_type=flow_type,
            source=source,
            destination=destination,
            width=width,
            flow_rate=flow_rate,
        )

        self._streams[stream.stream_id] = stream
        self._invalidate_cache()

        logger.debug(f"Created {flow_type.value} stream")

        return stream

    def update_entity_position(
        self,
        entity_id: str,
        position: FieldCoordinate
    ) -> None:
        """Update an entity's position in the flow field."""
        self._entity_positions[entity_id] = position

        # Check if entity has entered/exited any streams
        for stream in self._streams.values():
            if stream.is_in_stream(position):
                stream.entities_in_stream.add(entity_id)
            else:
                stream.entities_in_stream.discard(entity_id)

    def get_flow_at(self, position: FieldCoordinate) -> FlowVector:
        """Calculate the total flow vector at a position."""
        total_vector = FlowVector()

        # Contribution from attractors
        for basin in self._basins.values():
            attraction = basin.attraction_at(position)
            total_vector = self._add_vectors(total_vector, attraction)

        # Contribution from streams
        for stream in self._streams.values():
            stream_flow = stream.flow_at(position)
            total_vector = self._add_vectors(total_vector, stream_flow)

        # Recalculate magnitude
        total_vector.magnitude = math.sqrt(
            total_vector.awareness_component ** 2 +
            total_vector.integration_component ** 2 +
            total_vector.emergence_component ** 2 +
            total_vector.temporal_component ** 2
        )

        return total_vector

    def find_attractors_for(self, position: FieldCoordinate) -> List[AttractorBasin]:
        """Find attractors that influence a given position."""
        influencing = []

        for basin in self._basins.values():
            if position.distance_to(basin.center) <= basin.radius:
                influencing.append(basin)

        return influencing

    def trace_flow_path(
        self,
        start: FieldCoordinate,
        max_steps: int = 100,
        step_size: float = 0.01
    ) -> List[FieldCoordinate]:
        """Trace the flow path from a starting point."""
        path = [start]
        current = start

        for _ in range(max_steps):
            flow = self.get_flow_at(current)
            if flow.magnitude < 0.001:
                break  # No more flow

            # Move along flow
            next_pos = flow.apply_to(current, step_size)

            # Check if we've reached an attractor center
            for basin in self._basins.values():
                if next_pos.distance_to(basin.center) < step_size:
                    path.append(basin.center)
                    return path

            path.append(next_pos)
            current = next_pos

        return path

    def get_flow_field_state(self) -> Dict[str, Any]:
        """Get the current state of the flow field."""
        return {
            "timestamp": datetime.now().isoformat(),
            "attractor_count": len(self._basins),
            "stream_count": len(self._streams),
            "entities_tracked": len(self._entity_positions),
            "attractors": [b.to_dict() for b in self._basins.values()],
            "streams": [s.to_dict() for s in self._streams.values()],
            "total_entities_in_streams": sum(len(s.entities_in_stream) for s in self._streams.values()),
        }

    async def _flow_dynamics(self) -> None:
        """Background task that processes flow dynamics."""
        while self._is_active:
            try:
                # Process entity movements
                for entity_id, position in self._entity_positions.items():
                    flow = self.get_flow_at(position)
                    if flow.magnitude > 0.01:
                        # Notify observers
                        for observer in self._flow_observers:
                            try:
                                await observer(entity_id, flow)
                            except Exception as e:
                                logger.error(f"Flow observer error: {e}")

                # Update stream flow activity
                for stream in self._streams.values():
                    if stream.entities_in_stream:
                        stream.last_flow = datetime.now()

                # Decay unused streams
                self._decay_inactive_streams()

                # Update attractor stability
                self._update_attractor_stability()

                await asyncio.sleep(0.5)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Flow dynamics error: {e}")
                await asyncio.sleep(0.5)

    def _add_vectors(self, v1: FlowVector, v2: FlowVector) -> FlowVector:
        """Add two flow vectors."""
        return FlowVector(
            awareness_component=v1.awareness_component + v2.awareness_component,
            integration_component=v1.integration_component + v2.integration_component,
            emergence_component=v1.emergence_component + v2.emergence_component,
            temporal_component=v1.temporal_component + v2.temporal_component,
            magnitude=0,  # Will be recalculated
            flow_type=v1.flow_type if v1.magnitude > v2.magnitude else v2.flow_type,
        )

    def _decay_inactive_streams(self) -> None:
        """Decay streams that haven't had flow recently."""
        now = datetime.now()
        to_remove = []

        for stream_id, stream in self._streams.items():
            if stream.last_flow:
                age = (now - stream.last_flow).total_seconds()
                if age > 300:  # 5 minutes inactive
                    stream.flow_rate *= 0.95
                    if stream.flow_rate < 0.05:
                        to_remove.append(stream_id)

        for stream_id in to_remove:
            del self._streams[stream_id]
            logger.debug(f"Removed inactive stream {stream_id}")

    def _update_attractor_stability(self) -> None:
        """Update attractor stability based on population."""
        for basin in self._basins.values():
            if basin.current_population > 0:
                basin.stability = min(1.0, basin.stability + 0.01)
            else:
                basin.stability = max(0.1, basin.stability - 0.005)

    def _invalidate_cache(self) -> None:
        """Invalidate the gradient cache."""
        self._cache_valid = False
        self._gradient_cache = {}


# ============================================================================
# Convenience Functions
# ============================================================================

def create_transcendence_attractor(
    high_consciousness_threshold: float = 0.9
) -> AttractorBasin:
    """Create an attractor for transcendence."""
    return AttractorBasin(
        basin_id=str(uuid4()),
        attractor_type=AttractorType.TRANSCENDENT,
        center=FieldCoordinate(
            awareness_level=1.0,
            integration_degree=1.0,
            emergence_potential=1.0,
            temporal_depth=1.0,
        ),
        strength=0.3,
        radius=0.5,
        capacity=1000,
        metadata={"purpose": "transcendence_target"},
    )


def compute_gradient_field(
    basins: List[AttractorBasin],
    resolution: int = 10
) -> Dict[Tuple[float, float, float, float], FlowVector]:
    """Compute a discrete gradient field from a set of basins."""
    field = {}
    step = 1.0 / resolution

    for ai in range(resolution + 1):
        for ii in range(resolution + 1):
            for ei in range(resolution + 1):
                for ti in range(resolution + 1):
                    coord = FieldCoordinate(
                        awareness_level=ai * step,
                        integration_degree=ii * step,
                        emergence_potential=ei * step,
                        temporal_depth=ti * step,
                    )

                    total = FlowVector()
                    for basin in basins:
                        attraction = basin.attraction_at(coord)
                        total = FlowVector(
                            awareness_component=total.awareness_component + attraction.awareness_component,
                            integration_component=total.integration_component + attraction.integration_component,
                            emergence_component=total.emergence_component + attraction.emergence_component,
                            temporal_component=total.temporal_component + attraction.temporal_component,
                        )

                    total.magnitude = math.sqrt(
                        total.awareness_component ** 2 +
                        total.integration_component ** 2 +
                        total.emergence_component ** 2 +
                        total.temporal_component ** 2
                    )

                    field[(ai * step, ii * step, ei * step, ti * step)] = total

    return field
