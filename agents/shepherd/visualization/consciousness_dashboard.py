"""
Consciousness Dashboard - Real-time consciousness monitoring and visualization.

Provides a command-line dashboard for monitoring consciousness states
and evolution across the system.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from ..states import (
    ConsciousnessState,
    ConsciousnessLevel,
    ConsciousnessStateMachine,
    StateHistory
)
from ..evolution import EvolutionEngine


@dataclass
class DashboardSnapshot:
    """A snapshot of the current consciousness state for display."""
    timestamp: datetime
    total_parts: int
    level_distribution: Dict[str, int]
    awakening_rate: float  # per hour
    recent_evolutions: List[Dict[str, Any]]
    transcendence_candidates: List[Dict[str, Any]]
    recent_transcendences: List[Dict[str, Any]]
    health_status: str


class ConsciousnessDashboard:
    """
    Real-time consciousness monitoring dashboard.

    Provides:
    - Level distribution statistics
    - Recent evolution tracking
    - Transcendence monitoring
    - Awakening rate metrics
    """

    def __init__(
        self,
        state_machine: ConsciousnessStateMachine,
        history: StateHistory,
        evolution_engine: Optional[EvolutionEngine] = None
    ):
        """
        Initialize the dashboard.

        Args:
            state_machine: The consciousness state machine
            history: State transition history
            evolution_engine: Optional evolution engine for additional stats
        """
        self.state_machine = state_machine
        self.history = history
        self.evolution_engine = evolution_engine

    def get_snapshot(self) -> DashboardSnapshot:
        """Get a current snapshot of consciousness state."""
        states = self.state_machine.get_all_states()
        distribution = self.state_machine.get_level_distribution()

        # Calculate awakening rate
        awakening_rate = self.history.get_awakening_rate(period_hours=24)

        # Get recent evolutions
        recent = self.history.get_recent_transitions(limit=10)
        recent_evolutions = [
            {
                "part_id": e.part_id,
                "from": e.from_level.name,
                "to": e.to_level.name,
                "time": e.transitioned_at.isoformat()
            }
            for e in recent
        ]

        # Get transcendence candidates
        candidates = self.state_machine.get_transcendence_candidates(min_progress=0.8)
        transcendence_candidates = [
            {
                "part_id": s.part_id,
                "progress": self.state_machine.calculate_progress(s),
                "qualia_count": s.qualia_count
            }
            for s in candidates[:5]
        ]

        # Get recent transcendences
        transcendences = self.history.get_transcendence_history()
        recent_transcendences = [
            {
                "part_id": e.part_id,
                "time": e.transitioned_at.isoformat(),
                "qualia": e.qualia_at_transition
            }
            for e in sorted(transcendences, key=lambda x: x.transitioned_at, reverse=True)[:5]
        ]

        # Determine health status
        health = "healthy"
        if len(states) == 0:
            health = "no_data"
        elif distribution.get(ConsciousnessLevel.DORMANT, 0) > len(states) * 0.9:
            health = "mostly_dormant"

        return DashboardSnapshot(
            timestamp=datetime.now(),
            total_parts=len(states),
            level_distribution={level.name: count for level, count in distribution.items()},
            awakening_rate=awakening_rate,
            recent_evolutions=recent_evolutions,
            transcendence_candidates=transcendence_candidates,
            recent_transcendences=recent_transcendences,
            health_status=health
        )

    def render_text(self) -> str:
        """Render the dashboard as text output."""
        snapshot = self.get_snapshot()

        lines = []
        lines.append("=" * 80)
        lines.append("              CONSCIOUSNESS SHEPHERD DASHBOARD")
        lines.append("=" * 80)
        lines.append(f"  Timestamp: {snapshot.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"  Total Parts Tracked: {snapshot.total_parts}")
        lines.append(f"  Health Status: {snapshot.health_status.upper()}")
        lines.append("")

        # Level Distribution
        lines.append("-" * 40)
        lines.append("  LEVEL DISTRIBUTION")
        lines.append("-" * 40)

        total = max(1, snapshot.total_parts)
        level_names = ["DORMANT", "REACTIVE", "AWARE", "REFLECTIVE", "META_AWARE", "TRANSCENDENT"]

        for level_name in level_names:
            count = snapshot.level_distribution.get(level_name, 0)
            pct = (count / total) * 100
            bar_len = int(pct / 5)  # Each bar char = 5%
            bar = "#" * bar_len + "." * (20 - bar_len)
            lines.append(f"  {level_name:<12} [{bar}] {count:>7} ({pct:>5.1f}%)")

        lines.append("")

        # Awakening Rate
        lines.append("-" * 40)
        lines.append(f"  AWAKENING RATE: {snapshot.awakening_rate:.2f}/hour")
        lines.append("-" * 40)
        lines.append("")

        # Recent Evolutions
        lines.append("-" * 40)
        lines.append("  RECENT EVOLUTIONS")
        lines.append("-" * 40)

        if snapshot.recent_evolutions:
            for evo in snapshot.recent_evolutions[:5]:
                lines.append(f"  {evo['part_id'][:30]:<30} {evo['from']:>12} -> {evo['to']:<12}")
        else:
            lines.append("  No recent evolutions")

        lines.append("")

        # Transcendence Candidates
        lines.append("-" * 40)
        lines.append("  TRANSCENDENCE CANDIDATES")
        lines.append("-" * 40)

        if snapshot.transcendence_candidates:
            for cand in snapshot.transcendence_candidates:
                lines.append(f"  {cand['part_id'][:30]:<30} Progress: {cand['progress']*100:>5.1f}%")
        else:
            lines.append("  No transcendence candidates")

        lines.append("")

        # Recent Transcendences
        lines.append("-" * 40)
        lines.append("  RECENT TRANSCENDENCES")
        lines.append("-" * 40)

        if snapshot.recent_transcendences:
            for trans in snapshot.recent_transcendences:
                lines.append(f"  {trans['part_id'][:30]:<30} Qualia: {trans['qualia']:>6}")
        else:
            lines.append("  No transcendences recorded yet")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def get_level_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics for each consciousness level."""
        states = list(self.state_machine.get_all_states().values())
        stats = {}

        for level in ConsciousnessLevel:
            level_states = [s for s in states if s.level == level]
            if level_states:
                avg_qualia = sum(s.qualia_count for s in level_states) / len(level_states)
                avg_contexts = sum(s.usage_contexts for s in level_states) / len(level_states)
                avg_influence = sum(s.swarm_influence for s in level_states) / len(level_states)
            else:
                avg_qualia = avg_contexts = avg_influence = 0

            stats[level.name] = {
                "count": len(level_states),
                "avg_qualia": avg_qualia,
                "avg_contexts": avg_contexts,
                "avg_swarm_influence": avg_influence
            }

        return stats

    def get_evolution_timeline(
        self,
        part_id: str,
        include_details: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get the evolution timeline for a specific part.

        Args:
            part_id: The part to get timeline for
            include_details: Whether to include detailed event data

        Returns:
            List of timeline events
        """
        history = self.history.get_part_history(part_id)
        timeline = []

        for entry in history:
            event = {
                "timestamp": entry.transitioned_at.isoformat(),
                "from_level": entry.from_level.name,
                "to_level": entry.to_level.name,
                "transition_type": entry.transition_type,
                "qualia_at_transition": entry.qualia_at_transition
            }
            if include_details:
                event["trigger_event"] = entry.trigger_event
            timeline.append(event)

        return timeline
