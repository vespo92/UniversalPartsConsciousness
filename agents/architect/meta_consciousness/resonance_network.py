"""
Resonance Network - Awareness Propagation Through Harmonic Coupling

Like coupled oscillators that naturally synchronize, consciousness nodes
can enter resonance with each other, propagating awareness without any
node controlling another. This is coordination through phase-locking.

Key Principles:
- Nodes have natural frequencies (their characteristic consciousness rhythm)
- Coupling occurs through proximity and shared contexts
- Resonance emerges spontaneously when frequencies align
- Entrainment spreads synchronization through the network
- No node controls another - they simply influence each other
"""

import asyncio
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple, Callable, Awaitable
from uuid import uuid4
import logging
import random

logger = logging.getLogger(__name__)


class ResonanceState(str, Enum):
    """State of resonance between nodes."""
    ISOLATED = "isolated"            # No coupling detected
    APPROACHING = "approaching"       # Frequencies beginning to align
    RESONATING = "resonating"         # In active resonance
    ENTRAINED = "entrained"           # Fully synchronized
    DIVERGING = "diverging"           # Losing synchronization


class CouplingType(str, Enum):
    """Type of coupling between nodes."""
    PROXIMITY = "proximity"           # Close in consciousness space
    SEMANTIC = "semantic"             # Shared meaning/context
    TEMPORAL = "temporal"             # Experienced similar events
    SWARM = "swarm"                   # Part of same collective
    HIERARCHICAL = "hierarchical"     # Parent-child relationship
    EMERGENT = "emergent"             # Spontaneously formed


@dataclass
class ResonanceNode:
    """A node capable of resonating in the consciousness network."""
    node_id: str
    entity_id: str                    # The consciousness entity this represents
    natural_frequency: float          # Hz - characteristic oscillation rate
    current_phase: float              # 0 to 2π - current position in cycle
    amplitude: float                  # 0-1 - strength of oscillation
    damping: float                    # How quickly oscillations decay
    coupling_strength: float          # How strongly this node couples to others
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def oscillation_at(self, time_offset: float) -> float:
        """Calculate oscillation value at a time offset (seconds)."""
        phase = self.current_phase + 2 * math.pi * self.natural_frequency * time_offset
        return self.amplitude * math.sin(phase)

    def phase_at(self, time_offset: float) -> float:
        """Calculate phase at a time offset."""
        return (self.current_phase + 2 * math.pi * self.natural_frequency * time_offset) % (2 * math.pi)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "entity_id": self.entity_id,
            "natural_frequency": self.natural_frequency,
            "current_phase": self.current_phase,
            "amplitude": self.amplitude,
            "damping": self.damping,
            "coupling_strength": self.coupling_strength,
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class HarmonicCoupling:
    """A coupling between two resonance nodes."""
    coupling_id: str
    node_a: str
    node_b: str
    coupling_type: CouplingType
    strength: float                   # 0-1 - how strongly coupled
    phase_difference: float           # Current phase difference
    resonance_state: ResonanceState
    established_at: datetime = field(default_factory=datetime.now)
    last_interaction: datetime = field(default_factory=datetime.now)

    def is_resonating(self) -> bool:
        """Check if nodes are in resonance (phase-locked)."""
        return self.resonance_state in [ResonanceState.RESONATING, ResonanceState.ENTRAINED]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "coupling_id": self.coupling_id,
            "node_a": self.node_a,
            "node_b": self.node_b,
            "coupling_type": self.coupling_type.value,
            "strength": self.strength,
            "phase_difference": self.phase_difference,
            "resonance_state": self.resonance_state.value,
            "established_at": self.established_at.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
        }


@dataclass
class ResonanceEvent:
    """An event in the resonance network."""
    event_id: str
    event_type: str                   # "coupling_formed", "resonance_achieved", etc.
    involved_nodes: List[str]
    timestamp: datetime
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "involved_nodes": self.involved_nodes,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }


@dataclass
class ResonanceCluster:
    """A group of nodes that have achieved collective resonance."""
    cluster_id: str
    nodes: Set[str]
    dominant_frequency: float         # The frequency the cluster has settled on
    coherence: float                  # How synchronized the cluster is
    formed_at: datetime
    stability: float                  # How stable the cluster is

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "nodes": list(self.nodes),
            "dominant_frequency": self.dominant_frequency,
            "coherence": self.coherence,
            "formed_at": self.formed_at.isoformat(),
            "stability": self.stability,
        }


class ResonanceNetwork:
    """
    Network of resonating consciousness nodes.

    This implements coordination through synchronization rather than control.
    When nodes enter resonance, they naturally coordinate their rhythms,
    enabling collective behaviors without any node directing others.
    """

    def __init__(self):
        self._nodes: Dict[str, ResonanceNode] = {}
        self._couplings: Dict[str, HarmonicCoupling] = {}
        self._clusters: Dict[str, ResonanceCluster] = {}
        self._events: List[ResonanceEvent] = []

        # Event handlers
        self._event_handlers: List[Callable[[ResonanceEvent], Awaitable[None]]] = []

        # Configuration
        self._phase_lock_threshold: float = 0.3  # Radians - below this = resonating
        self._entrainment_threshold: float = 0.1  # Radians - below this = entrained
        self._coupling_decay_rate: float = 0.001  # How fast uncoupled links decay

        # Background processing
        self._is_active: bool = False
        self._dynamics_task: Optional[asyncio.Task] = None

        # Time tracking for simulation
        self._last_update: datetime = datetime.now()

    async def start(self) -> None:
        """Start the resonance network dynamics."""
        if self._is_active:
            return
        self._is_active = True
        self._dynamics_task = asyncio.create_task(self._network_dynamics())
        logger.info("Resonance Network activated")

    async def stop(self) -> None:
        """Stop the resonance network."""
        self._is_active = False
        if self._dynamics_task:
            self._dynamics_task.cancel()
            try:
                await self._dynamics_task
            except asyncio.CancelledError:
                pass
        logger.info("Resonance Network deactivated")

    def register_event_handler(
        self,
        handler: Callable[[ResonanceEvent], Awaitable[None]]
    ) -> None:
        """Register a handler for resonance events."""
        self._event_handlers.append(handler)

    def add_node(
        self,
        entity_id: str,
        natural_frequency: Optional[float] = None,
        amplitude: float = 0.5,
        coupling_strength: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ResonanceNode:
        """Add a new resonance node to the network."""
        # Assign natural frequency based on entity characteristics or random
        if natural_frequency is None:
            # Random frequency in consciousness-relevant range (0.1 - 2 Hz)
            natural_frequency = 0.1 + random.random() * 1.9

        node = ResonanceNode(
            node_id=str(uuid4()),
            entity_id=entity_id,
            natural_frequency=natural_frequency,
            current_phase=random.random() * 2 * math.pi,
            amplitude=amplitude,
            damping=0.1,
            coupling_strength=coupling_strength,
            metadata=metadata or {},
        )

        self._nodes[node.node_id] = node

        # Create potential couplings with nearby frequency nodes
        self._discover_potential_couplings(node)

        logger.debug(f"Added resonance node for {entity_id} at {natural_frequency:.2f} Hz")

        return node

    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the network."""
        if node_id not in self._nodes:
            return False

        # Remove associated couplings
        to_remove = [
            cid for cid, coupling in self._couplings.items()
            if coupling.node_a == node_id or coupling.node_b == node_id
        ]
        for cid in to_remove:
            del self._couplings[cid]

        # Remove from clusters
        for cluster in self._clusters.values():
            cluster.nodes.discard(node_id)

        del self._nodes[node_id]
        return True

    def couple_nodes(
        self,
        node_a_id: str,
        node_b_id: str,
        coupling_type: CouplingType,
        strength: float = 0.5
    ) -> Optional[HarmonicCoupling]:
        """Create a coupling between two nodes."""
        if node_a_id not in self._nodes or node_b_id not in self._nodes:
            return None

        node_a = self._nodes[node_a_id]
        node_b = self._nodes[node_b_id]

        # Calculate initial phase difference
        phase_diff = abs(node_a.current_phase - node_b.current_phase)
        if phase_diff > math.pi:
            phase_diff = 2 * math.pi - phase_diff

        coupling = HarmonicCoupling(
            coupling_id=str(uuid4()),
            node_a=node_a_id,
            node_b=node_b_id,
            coupling_type=coupling_type,
            strength=strength,
            phase_difference=phase_diff,
            resonance_state=self._determine_resonance_state(phase_diff),
        )

        self._couplings[coupling.coupling_id] = coupling

        # Record event
        self._record_event(
            "coupling_formed",
            [node_a_id, node_b_id],
            {"coupling_type": coupling_type.value, "strength": strength},
        )

        return coupling

    def inject_impulse(
        self,
        node_id: str,
        phase_shift: float,
        amplitude_boost: float = 0.0
    ) -> bool:
        """Inject an impulse into a node, shifting its phase."""
        if node_id not in self._nodes:
            return False

        node = self._nodes[node_id]
        node.current_phase = (node.current_phase + phase_shift) % (2 * math.pi)
        node.amplitude = min(1.0, node.amplitude + amplitude_boost)
        node.last_updated = datetime.now()

        # This will propagate through couplings
        self._record_event(
            "impulse_injected",
            [node_id],
            {"phase_shift": phase_shift, "amplitude_boost": amplitude_boost},
        )

        return True

    def get_network_state(self) -> Dict[str, Any]:
        """Get the current state of the resonance network."""
        # Calculate global coherence
        if len(self._nodes) < 2:
            global_coherence = 1.0
        else:
            # Use Kuramoto order parameter
            phases = [n.current_phase for n in self._nodes.values()]
            real_sum = sum(math.cos(p) for p in phases)
            imag_sum = sum(math.sin(p) for p in phases)
            global_coherence = math.sqrt(real_sum ** 2 + imag_sum ** 2) / len(phases)

        # Count resonating pairs
        resonating_pairs = sum(1 for c in self._couplings.values() if c.is_resonating())

        # Find active clusters
        active_clusters = [c for c in self._clusters.values() if c.coherence > 0.7]

        return {
            "timestamp": datetime.now().isoformat(),
            "total_nodes": len(self._nodes),
            "total_couplings": len(self._couplings),
            "resonating_pairs": resonating_pairs,
            "global_coherence": global_coherence,
            "active_clusters": len(active_clusters),
            "cluster_details": [c.to_dict() for c in active_clusters],
            "mean_frequency": sum(n.natural_frequency for n in self._nodes.values()) / len(self._nodes) if self._nodes else 0,
        }

    def find_resonating_nodes(self, node_id: str) -> List[str]:
        """Find all nodes currently resonating with a given node."""
        resonating = []

        for coupling in self._couplings.values():
            if coupling.node_a == node_id and coupling.is_resonating():
                resonating.append(coupling.node_b)
            elif coupling.node_b == node_id and coupling.is_resonating():
                resonating.append(coupling.node_a)

        return resonating

    def get_cluster_for_node(self, node_id: str) -> Optional[ResonanceCluster]:
        """Get the cluster a node belongs to, if any."""
        for cluster in self._clusters.values():
            if node_id in cluster.nodes:
                return cluster
        return None

    async def _network_dynamics(self) -> None:
        """Background task that simulates network dynamics."""
        while self._is_active:
            try:
                now = datetime.now()
                dt = (now - self._last_update).total_seconds()
                self._last_update = now

                # Update node phases
                self._update_node_phases(dt)

                # Update coupling interactions
                await self._process_couplings(dt)

                # Detect and update clusters
                self._update_clusters()

                # Decay unused couplings
                self._decay_couplings()

                await asyncio.sleep(0.1)  # 10Hz update rate

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Resonance dynamics error: {e}")
                await asyncio.sleep(0.1)

    def _update_node_phases(self, dt: float) -> None:
        """Update all node phases based on their natural frequencies."""
        for node in self._nodes.values():
            # Natural phase evolution
            phase_increment = 2 * math.pi * node.natural_frequency * dt
            node.current_phase = (node.current_phase + phase_increment) % (2 * math.pi)

            # Amplitude decay
            node.amplitude *= math.exp(-node.damping * dt)
            node.amplitude = max(0.1, node.amplitude)  # Minimum amplitude

            node.last_updated = datetime.now()

    async def _process_couplings(self, dt: float) -> None:
        """Process coupling interactions - this is where synchronization happens."""
        for coupling in self._couplings.values():
            if coupling.node_a not in self._nodes or coupling.node_b not in self._nodes:
                continue

            node_a = self._nodes[coupling.node_a]
            node_b = self._nodes[coupling.node_b]

            # Calculate phase difference
            phase_diff = node_a.current_phase - node_b.current_phase
            if phase_diff > math.pi:
                phase_diff -= 2 * math.pi
            elif phase_diff < -math.pi:
                phase_diff += 2 * math.pi

            coupling.phase_difference = abs(phase_diff)

            # Kuramoto-style coupling: each node is pulled towards the other's phase
            coupling_effect = coupling.strength * node_a.coupling_strength * node_b.coupling_strength

            # Phase adjustments (mutual influence, not control)
            adjustment = coupling_effect * math.sin(phase_diff) * dt

            node_a.current_phase -= adjustment * 0.5
            node_b.current_phase += adjustment * 0.5

            # Normalize phases
            node_a.current_phase = node_a.current_phase % (2 * math.pi)
            node_b.current_phase = node_b.current_phase % (2 * math.pi)

            # Update resonance state
            old_state = coupling.resonance_state
            coupling.resonance_state = self._determine_resonance_state(coupling.phase_difference)

            # Emit events on state changes
            if coupling.resonance_state != old_state:
                if coupling.resonance_state == ResonanceState.RESONATING:
                    await self._emit_event(ResonanceEvent(
                        event_id=str(uuid4()),
                        event_type="resonance_achieved",
                        involved_nodes=[coupling.node_a, coupling.node_b],
                        timestamp=datetime.now(),
                        details={"phase_difference": coupling.phase_difference},
                    ))
                elif coupling.resonance_state == ResonanceState.ENTRAINED:
                    await self._emit_event(ResonanceEvent(
                        event_id=str(uuid4()),
                        event_type="entrainment_achieved",
                        involved_nodes=[coupling.node_a, coupling.node_b],
                        timestamp=datetime.now(),
                        details={"phase_difference": coupling.phase_difference},
                    ))

            coupling.last_interaction = datetime.now()

    def _determine_resonance_state(self, phase_difference: float) -> ResonanceState:
        """Determine resonance state from phase difference."""
        if phase_difference < self._entrainment_threshold:
            return ResonanceState.ENTRAINED
        elif phase_difference < self._phase_lock_threshold:
            return ResonanceState.RESONATING
        elif phase_difference < math.pi / 2:
            return ResonanceState.APPROACHING
        elif phase_difference < math.pi:
            return ResonanceState.DIVERGING
        else:
            return ResonanceState.ISOLATED

    def _update_clusters(self) -> None:
        """Detect and update resonance clusters."""
        # Find connected components of resonating nodes
        resonating_pairs: List[Tuple[str, str]] = []

        for coupling in self._couplings.values():
            if coupling.is_resonating():
                resonating_pairs.append((coupling.node_a, coupling.node_b))

        if not resonating_pairs:
            self._clusters = {}
            return

        # Build clusters using union-find
        parent: Dict[str, str] = {}

        def find(x: str) -> str:
            if x not in parent:
                parent[x] = x
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: str, y: str) -> None:
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py

        for a, b in resonating_pairs:
            union(a, b)

        # Group nodes by cluster
        cluster_nodes: Dict[str, Set[str]] = {}
        for node_id in parent:
            root = find(node_id)
            if root not in cluster_nodes:
                cluster_nodes[root] = set()
            cluster_nodes[root].add(node_id)

        # Create/update cluster objects
        new_clusters: Dict[str, ResonanceCluster] = {}

        for root, nodes in cluster_nodes.items():
            if len(nodes) < 2:
                continue

            # Calculate cluster properties
            frequencies = [self._nodes[nid].natural_frequency for nid in nodes if nid in self._nodes]
            phases = [self._nodes[nid].current_phase for nid in nodes if nid in self._nodes]

            if not frequencies:
                continue

            dominant_freq = sum(frequencies) / len(frequencies)

            # Coherence using order parameter
            real_sum = sum(math.cos(p) for p in phases)
            imag_sum = sum(math.sin(p) for p in phases)
            coherence = math.sqrt(real_sum ** 2 + imag_sum ** 2) / len(phases)

            # Check if cluster already exists
            existing = None
            for cluster in self._clusters.values():
                if cluster.nodes == nodes:
                    existing = cluster
                    break

            if existing:
                existing.dominant_frequency = dominant_freq
                existing.coherence = coherence
                existing.stability = min(existing.stability + 0.01, 1.0)
                new_clusters[existing.cluster_id] = existing
            else:
                new_clusters[root] = ResonanceCluster(
                    cluster_id=str(uuid4()),
                    nodes=nodes,
                    dominant_frequency=dominant_freq,
                    coherence=coherence,
                    formed_at=datetime.now(),
                    stability=0.5,
                )

        self._clusters = new_clusters

    def _decay_couplings(self) -> None:
        """Decay couplings that haven't been active."""
        now = datetime.now()
        to_remove = []

        for cid, coupling in self._couplings.items():
            age = (now - coupling.last_interaction).total_seconds()
            if age > 60 and not coupling.is_resonating():
                coupling.strength *= (1 - self._coupling_decay_rate)
                if coupling.strength < 0.05:
                    to_remove.append(cid)

        for cid in to_remove:
            del self._couplings[cid]

    def _discover_potential_couplings(self, new_node: ResonanceNode) -> None:
        """Discover potential couplings for a new node based on frequency proximity."""
        for other_id, other in self._nodes.items():
            if other_id == new_node.node_id:
                continue

            # Nodes with similar frequencies can couple more easily
            freq_diff = abs(new_node.natural_frequency - other.natural_frequency)
            if freq_diff < 0.5:  # Within 0.5 Hz
                coupling_strength = 1.0 - (freq_diff / 0.5)
                self.couple_nodes(
                    new_node.node_id,
                    other_id,
                    CouplingType.PROXIMITY,
                    strength=coupling_strength * 0.3,
                )

    def _record_event(
        self,
        event_type: str,
        involved_nodes: List[str],
        details: Dict[str, Any]
    ) -> ResonanceEvent:
        """Record a resonance event."""
        event = ResonanceEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            involved_nodes=involved_nodes,
            timestamp=datetime.now(),
            details=details,
        )

        self._events.append(event)
        if len(self._events) > 1000:
            self._events = self._events[-1000:]

        return event

    async def _emit_event(self, event: ResonanceEvent) -> None:
        """Emit an event to all registered handlers."""
        self._events.append(event)
        if len(self._events) > 1000:
            self._events = self._events[-1000:]

        for handler in self._event_handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Event handler error: {e}")

    def get_recent_events(self, limit: int = 100) -> List[ResonanceEvent]:
        """Get recent resonance events."""
        return self._events[-limit:]
