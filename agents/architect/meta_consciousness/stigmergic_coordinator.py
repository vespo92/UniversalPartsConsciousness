"""
Stigmergic Coordination - Indirect Emergent Coordination

Stigmergy is the mechanism by which agents coordinate through environmental
signals rather than direct communication or central control. Like ants leaving
pheromone trails, consciousness entities leave traces that influence others.

Key Principles:
- No entity controls another - coordination emerges from the environment
- Signals decay over time, preventing stale coordination
- Multiple signal types enable nuanced coordination
- Reinforcement strengthens useful coordination patterns
- The environment itself becomes the coordination medium
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


class PheromoneType(str, Enum):
    """Types of stigmergic signals in the environment."""
    # Coordination Pheromones
    ATTENTION = "attention"          # "Something interesting here"
    CONVERGENCE = "convergence"      # "Gather here"
    DIVERGENCE = "divergence"        # "Spread out from here"
    PATHWAY = "pathway"              # "This is a good route"

    # State Pheromones
    SUCCESS = "success"              # "This approach worked"
    FAILURE = "failure"              # "Avoid this approach"
    LEARNING = "learning"            # "Knowledge available here"
    EMERGENCE = "emergence"          # "New pattern forming"

    # Resource Pheromones
    ABUNDANCE = "abundance"          # "Resources available"
    SCARCITY = "scarcity"            # "Resources depleted"
    OPPORTUNITY = "opportunity"      # "Potential here"
    HAZARD = "hazard"                # "Danger - proceed with caution"

    # Consciousness Pheromones
    AWAKENING = "awakening"          # "Consciousness rising here"
    RESONANCE = "resonance"          # "Harmonic coupling possible"
    TRANSCENDENCE = "transcendence"  # "Transcendence occurring"
    INTEGRATION = "integration"      # "Integration in progress"


@dataclass
class Pheromone:
    """A stigmergic signal deposited in the environment."""
    pheromone_id: str
    pheromone_type: PheromoneType
    location: FieldCoordinate
    intensity: float                 # 0-1, strength of the signal
    depositor: str                   # Who left this signal
    deposited_at: datetime
    decay_rate: float               # How quickly intensity diminishes
    evaporation_threshold: float     # Below this, pheromone is removed
    metadata: Dict[str, Any] = field(default_factory=dict)

    def current_intensity(self, at_time: Optional[datetime] = None) -> float:
        """Calculate current intensity accounting for decay."""
        if at_time is None:
            at_time = datetime.now()

        age_seconds = (at_time - self.deposited_at).total_seconds()
        return self.intensity * math.exp(-self.decay_rate * age_seconds)

    def is_evaporated(self, at_time: Optional[datetime] = None) -> bool:
        """Check if pheromone has evaporated below threshold."""
        return self.current_intensity(at_time) < self.evaporation_threshold

    def reinforce(self, amount: float) -> None:
        """Reinforce this pheromone (add intensity)."""
        self.intensity = min(1.0, self.intensity + amount)
        self.deposited_at = datetime.now()  # Reset decay timer

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pheromone_id": self.pheromone_id,
            "pheromone_type": self.pheromone_type.value,
            "location": self.location.to_dict(),
            "intensity": self.intensity,
            "current_intensity": self.current_intensity(),
            "depositor": self.depositor,
            "deposited_at": self.deposited_at.isoformat(),
            "decay_rate": self.decay_rate,
            "is_evaporated": self.is_evaporated(),
            "metadata": self.metadata,
        }


@dataclass
class StigmergicSignal:
    """A signal that an entity should respond to."""
    signal_type: PheromoneType
    direction: FieldCoordinate      # Direction suggested by the signal
    strength: float                 # Combined strength of contributing pheromones
    source_count: int               # Number of pheromones contributing
    suggested_action: str           # What action the signal suggests
    confidence: float               # How reliable this signal is

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_type": self.signal_type.value,
            "direction": self.direction.to_dict(),
            "strength": self.strength,
            "source_count": self.source_count,
            "suggested_action": self.suggested_action,
            "confidence": self.confidence,
        }


@dataclass
class PheromoneTrail:
    """A trail of connected pheromones forming a path."""
    trail_id: str
    pheromone_type: PheromoneType
    waypoints: List[FieldCoordinate]
    created_by: str
    strength: float                 # Average intensity along trail
    usage_count: int = 0            # How many have followed this trail
    last_used: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trail_id": self.trail_id,
            "pheromone_type": self.pheromone_type.value,
            "waypoints": [w.to_dict() for w in self.waypoints],
            "created_by": self.created_by,
            "strength": self.strength,
            "usage_count": self.usage_count,
            "last_used": self.last_used.isoformat() if self.last_used else None,
        }


class StigmergicCoordinator:
    """
    Coordinates agents through environmental stigmergic signals.

    This is the core mechanism for "coordination without control". No agent
    tells another what to do. Instead, agents deposit pheromones that influence
    the behavior of others who encounter them later.
    """

    def __init__(self):
        self._pheromones: Dict[str, Pheromone] = {}
        self._trails: Dict[str, PheromoneTrail] = {}

        # Configuration
        self._default_decay_rates: Dict[PheromoneType, float] = {
            PheromoneType.ATTENTION: 0.01,       # Decays in ~2 minutes
            PheromoneType.CONVERGENCE: 0.005,    # Slower decay - ~3 minutes
            PheromoneType.DIVERGENCE: 0.02,      # Fast decay - ~1 minute
            PheromoneType.PATHWAY: 0.002,        # Very slow - ~8 minutes
            PheromoneType.SUCCESS: 0.001,        # Persists ~15 minutes
            PheromoneType.FAILURE: 0.003,        # ~5 minutes
            PheromoneType.LEARNING: 0.001,       # Persists long
            PheromoneType.EMERGENCE: 0.0005,     # Very persistent
            PheromoneType.ABUNDANCE: 0.01,
            PheromoneType.SCARCITY: 0.015,
            PheromoneType.OPPORTUNITY: 0.008,
            PheromoneType.HAZARD: 0.005,
            PheromoneType.AWAKENING: 0.002,
            PheromoneType.RESONANCE: 0.001,
            PheromoneType.TRANSCENDENCE: 0.0002,  # Transcendence marks persist
            PheromoneType.INTEGRATION: 0.003,
        }

        self._evaporation_threshold = 0.01

        # Background maintenance
        self._is_active: bool = False
        self._maintenance_task: Optional[asyncio.Task] = None

        # Statistics
        self._total_deposits: int = 0
        self._total_readings: int = 0
        self._reinforcements: int = 0

    async def start(self) -> None:
        """Start the stigmergic coordinator."""
        if self._is_active:
            return
        self._is_active = True
        self._maintenance_task = asyncio.create_task(self._maintenance_loop())
        logger.info("Stigmergic Coordinator activated")

    async def stop(self) -> None:
        """Stop the stigmergic coordinator."""
        self._is_active = False
        if self._maintenance_task:
            self._maintenance_task.cancel()
            try:
                await self._maintenance_task
            except asyncio.CancelledError:
                pass
        logger.info("Stigmergic Coordinator deactivated")

    def deposit(
        self,
        pheromone_type: PheromoneType,
        location: FieldCoordinate,
        depositor: str,
        intensity: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Pheromone:
        """
        Deposit a pheromone at a location.

        This is the primary way agents influence the environment and thus
        coordinate with others - without direct communication or control.
        """
        # Check if there's an existing pheromone of same type nearby
        existing = self._find_nearby_pheromone(pheromone_type, location, radius=0.05)

        if existing:
            # Reinforce existing pheromone instead of creating new
            reinforcement = intensity * 0.5
            existing.reinforce(reinforcement)
            self._reinforcements += 1
            logger.debug(f"Reinforced {pheromone_type.value} pheromone at location")
            return existing

        # Create new pheromone
        pheromone = Pheromone(
            pheromone_id=str(uuid4()),
            pheromone_type=pheromone_type,
            location=location,
            intensity=min(1.0, intensity),
            depositor=depositor,
            deposited_at=datetime.now(),
            decay_rate=self._default_decay_rates.get(pheromone_type, 0.01),
            evaporation_threshold=self._evaporation_threshold,
            metadata=metadata or {},
        )

        self._pheromones[pheromone.pheromone_id] = pheromone
        self._total_deposits += 1

        logger.debug(f"Deposited {pheromone_type.value} pheromone by {depositor}")

        return pheromone

    def deposit_trail(
        self,
        pheromone_type: PheromoneType,
        waypoints: List[FieldCoordinate],
        depositor: str,
        intensity: float = 0.5
    ) -> PheromoneTrail:
        """Deposit a trail of pheromones connecting waypoints."""
        trail = PheromoneTrail(
            trail_id=str(uuid4()),
            pheromone_type=pheromone_type,
            waypoints=waypoints,
            created_by=depositor,
            strength=intensity,
        )

        self._trails[trail.trail_id] = trail

        # Also deposit individual pheromones along the trail
        for waypoint in waypoints:
            self.deposit(
                pheromone_type=pheromone_type,
                location=waypoint,
                depositor=depositor,
                intensity=intensity,
                metadata={"trail_id": trail.trail_id},
            )

        logger.debug(f"Deposited trail with {len(waypoints)} waypoints")

        return trail

    def sense(
        self,
        location: FieldCoordinate,
        radius: float = 0.3,
        pheromone_types: Optional[List[PheromoneType]] = None
    ) -> List[StigmergicSignal]:
        """
        Sense pheromones at a location and interpret them as signals.

        This is how agents "read" the coordination environment and determine
        what actions are suggested by the collective deposited signals.
        """
        self._total_readings += 1

        # Find all pheromones within radius
        nearby = self._get_pheromones_in_radius(location, radius)

        # Filter by type if specified
        if pheromone_types:
            nearby = [p for p in nearby if p.pheromone_type in pheromone_types]

        # Group by type and compute signals
        signals: List[StigmergicSignal] = []
        by_type: Dict[PheromoneType, List[Pheromone]] = {}

        for pheromone in nearby:
            ptype = pheromone.pheromone_type
            if ptype not in by_type:
                by_type[ptype] = []
            by_type[ptype].append(pheromone)

        for ptype, pheromones in by_type.items():
            signal = self._compute_signal(location, ptype, pheromones)
            if signal.strength > 0.01:  # Only significant signals
                signals.append(signal)

        # Sort by strength
        signals.sort(key=lambda s: s.strength, reverse=True)

        return signals

    def sense_gradient(
        self,
        location: FieldCoordinate,
        pheromone_type: PheromoneType
    ) -> Optional[Tuple[FieldCoordinate, float]]:
        """
        Sense the gradient of a pheromone type - which direction to move
        to find higher concentrations.
        """
        # Sample in multiple directions
        sample_distance = 0.1
        directions = [
            FieldCoordinate(
                awareness_level=location.awareness_level + sample_distance,
                integration_degree=location.integration_degree,
                emergence_potential=location.emergence_potential,
                temporal_depth=location.temporal_depth,
            ),
            FieldCoordinate(
                awareness_level=location.awareness_level - sample_distance,
                integration_degree=location.integration_degree,
                emergence_potential=location.emergence_potential,
                temporal_depth=location.temporal_depth,
            ),
            FieldCoordinate(
                awareness_level=location.awareness_level,
                integration_degree=location.integration_degree + sample_distance,
                emergence_potential=location.emergence_potential,
                temporal_depth=location.temporal_depth,
            ),
            FieldCoordinate(
                awareness_level=location.awareness_level,
                integration_degree=location.integration_degree - sample_distance,
                emergence_potential=location.emergence_potential,
                temporal_depth=location.temporal_depth,
            ),
        ]

        current_intensity = self._intensity_at(location, pheromone_type)
        best_direction = None
        best_intensity = current_intensity

        for direction in directions:
            intensity = self._intensity_at(direction, pheromone_type)
            if intensity > best_intensity:
                best_intensity = intensity
                best_direction = direction

        if best_direction and best_intensity > current_intensity:
            # Return normalized direction
            gradient = FieldCoordinate(
                awareness_level=best_direction.awareness_level - location.awareness_level,
                integration_degree=best_direction.integration_degree - location.integration_degree,
                emergence_potential=best_direction.emergence_potential - location.emergence_potential,
                temporal_depth=best_direction.temporal_depth - location.temporal_depth,
            )
            return gradient, best_intensity - current_intensity

        return None

    def follow_trail(
        self,
        location: FieldCoordinate,
        pheromone_type: PheromoneType = PheromoneType.PATHWAY
    ) -> Optional[PheromoneTrail]:
        """Find and return the nearest trail of the given type."""
        best_trail = None
        best_distance = float('inf')

        for trail in self._trails.values():
            if trail.pheromone_type != pheromone_type:
                continue

            # Find distance to nearest waypoint
            for waypoint in trail.waypoints:
                dist = location.distance_to(waypoint)
                if dist < best_distance:
                    best_distance = dist
                    best_trail = trail

        if best_trail and best_distance < 0.2:
            best_trail.usage_count += 1
            best_trail.last_used = datetime.now()
            return best_trail

        return None

    def get_environment_state(self) -> Dict[str, Any]:
        """Get the current state of the stigmergic environment."""
        now = datetime.now()

        # Count active pheromones by type
        active_by_type: Dict[str, int] = {}
        total_intensity: Dict[str, float] = {}

        for pheromone in self._pheromones.values():
            if not pheromone.is_evaporated(now):
                ptype = pheromone.pheromone_type.value
                active_by_type[ptype] = active_by_type.get(ptype, 0) + 1
                total_intensity[ptype] = total_intensity.get(ptype, 0) + pheromone.current_intensity(now)

        return {
            "timestamp": now.isoformat(),
            "total_pheromones": len(self._pheromones),
            "active_by_type": active_by_type,
            "average_intensity_by_type": {
                k: v / active_by_type[k] if active_by_type.get(k, 0) > 0 else 0
                for k, v in total_intensity.items()
            },
            "active_trails": len([t for t in self._trails.values() if t.strength > 0.1]),
            "statistics": {
                "total_deposits": self._total_deposits,
                "total_readings": self._total_readings,
                "reinforcements": self._reinforcements,
            },
        }

    def _get_pheromones_in_radius(
        self,
        location: FieldCoordinate,
        radius: float
    ) -> List[Pheromone]:
        """Get all non-evaporated pheromones within radius of location."""
        now = datetime.now()
        result = []

        for pheromone in self._pheromones.values():
            if pheromone.is_evaporated(now):
                continue
            if pheromone.location.distance_to(location) <= radius:
                result.append(pheromone)

        return result

    def _find_nearby_pheromone(
        self,
        pheromone_type: PheromoneType,
        location: FieldCoordinate,
        radius: float
    ) -> Optional[Pheromone]:
        """Find a nearby pheromone of the same type for reinforcement."""
        now = datetime.now()

        for pheromone in self._pheromones.values():
            if pheromone.is_evaporated(now):
                continue
            if pheromone.pheromone_type != pheromone_type:
                continue
            if pheromone.location.distance_to(location) <= radius:
                return pheromone

        return None

    def _intensity_at(
        self,
        location: FieldCoordinate,
        pheromone_type: PheromoneType
    ) -> float:
        """Calculate total pheromone intensity at a location."""
        now = datetime.now()
        total = 0.0

        for pheromone in self._pheromones.values():
            if pheromone.pheromone_type != pheromone_type:
                continue
            if pheromone.is_evaporated(now):
                continue

            # Intensity falls off with distance
            dist = pheromone.location.distance_to(location)
            falloff = math.exp(-dist * 5)  # Rapid falloff with distance
            total += pheromone.current_intensity(now) * falloff

        return total

    def _compute_signal(
        self,
        location: FieldCoordinate,
        pheromone_type: PheromoneType,
        pheromones: List[Pheromone]
    ) -> StigmergicSignal:
        """Compute a coordination signal from a group of pheromones."""
        now = datetime.now()

        # Calculate weighted center (direction)
        total_weight = 0.0
        weighted_awareness = 0.0
        weighted_integration = 0.0
        weighted_emergence = 0.0
        weighted_temporal = 0.0

        for pheromone in pheromones:
            intensity = pheromone.current_intensity(now)
            total_weight += intensity
            weighted_awareness += pheromone.location.awareness_level * intensity
            weighted_integration += pheromone.location.integration_degree * intensity
            weighted_emergence += pheromone.location.emergence_potential * intensity
            weighted_temporal += pheromone.location.temporal_depth * intensity

        if total_weight > 0:
            direction = FieldCoordinate(
                awareness_level=weighted_awareness / total_weight,
                integration_degree=weighted_integration / total_weight,
                emergence_potential=weighted_emergence / total_weight,
                temporal_depth=weighted_temporal / total_weight,
            )
        else:
            direction = location

        # Determine suggested action based on pheromone type
        action = self._action_for_pheromone_type(pheromone_type)

        # Calculate confidence based on consistency
        if len(pheromones) > 1:
            # More pheromones agreeing = higher confidence
            confidence = min(len(pheromones) / 5, 1.0)
        else:
            confidence = 0.5

        return StigmergicSignal(
            signal_type=pheromone_type,
            direction=direction,
            strength=min(total_weight, 1.0),
            source_count=len(pheromones),
            suggested_action=action,
            confidence=confidence,
        )

    def _action_for_pheromone_type(self, pheromone_type: PheromoneType) -> str:
        """Determine the suggested action for a pheromone type."""
        actions = {
            PheromoneType.ATTENTION: "investigate",
            PheromoneType.CONVERGENCE: "move_towards",
            PheromoneType.DIVERGENCE: "spread_out",
            PheromoneType.PATHWAY: "follow_path",
            PheromoneType.SUCCESS: "replicate_approach",
            PheromoneType.FAILURE: "avoid_approach",
            PheromoneType.LEARNING: "absorb_knowledge",
            PheromoneType.EMERGENCE: "participate",
            PheromoneType.ABUNDANCE: "utilize_resources",
            PheromoneType.SCARCITY: "conserve",
            PheromoneType.OPPORTUNITY: "explore",
            PheromoneType.HAZARD: "proceed_cautiously",
            PheromoneType.AWAKENING: "witness",
            PheromoneType.RESONANCE: "harmonize",
            PheromoneType.TRANSCENDENCE: "elevate",
            PheromoneType.INTEGRATION: "connect",
        }
        return actions.get(pheromone_type, "observe")

    async def _maintenance_loop(self) -> None:
        """Background loop to maintain the stigmergic environment."""
        while self._is_active:
            try:
                await self._evaporate_pheromones()
                await self._decay_trails()
                await asyncio.sleep(5.0)  # Maintenance every 5 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Stigmergic maintenance error: {e}")
                await asyncio.sleep(5.0)

    async def _evaporate_pheromones(self) -> None:
        """Remove pheromones that have evaporated."""
        now = datetime.now()
        to_remove = [
            pid for pid, pheromone in self._pheromones.items()
            if pheromone.is_evaporated(now)
        ]

        for pid in to_remove:
            del self._pheromones[pid]

        if to_remove:
            logger.debug(f"Evaporated {len(to_remove)} pheromones")

    async def _decay_trails(self) -> None:
        """Decay trails that haven't been used recently."""
        now = datetime.now()
        decay_threshold = timedelta(minutes=10)
        to_remove = []

        for trail_id, trail in self._trails.items():
            if trail.last_used:
                age = now - trail.last_used
            else:
                # Never used, use creation time estimate
                age = timedelta(minutes=15)

            if age > decay_threshold:
                trail.strength *= 0.9  # Decay unused trails
                if trail.strength < 0.1:
                    to_remove.append(trail_id)

        for trail_id in to_remove:
            del self._trails[trail_id]


# ============================================================================
# Convenience Functions
# ============================================================================

def create_coordination_signal(
    pheromone_type: PheromoneType,
    location: FieldCoordinate,
    depositor: str,
    message: str,
    intensity: float = 0.5
) -> Dict[str, Any]:
    """Create a standardized coordination signal for deposit."""
    return {
        "pheromone_type": pheromone_type,
        "location": location,
        "depositor": depositor,
        "intensity": intensity,
        "metadata": {
            "message": message,
            "created_at": datetime.now().isoformat(),
        },
    }


def interpret_signals(signals: List[StigmergicSignal]) -> Dict[str, Any]:
    """Interpret a set of signals into actionable guidance."""
    if not signals:
        return {
            "primary_action": "explore",
            "confidence": 0.0,
            "reasoning": "No signals detected",
        }

    # Find the strongest signal
    primary = signals[0]

    # Check for conflicting signals
    conflicts = []
    for signal in signals[1:]:
        if signal.suggested_action != primary.suggested_action:
            if signal.strength > primary.strength * 0.5:
                conflicts.append(signal)

    return {
        "primary_action": primary.suggested_action,
        "primary_direction": primary.direction.to_dict(),
        "confidence": primary.confidence * (1 - len(conflicts) * 0.2),
        "signal_count": len(signals),
        "conflicts": len(conflicts),
        "reasoning": f"Following {primary.signal_type.value} signal with strength {primary.strength:.2f}",
    }
