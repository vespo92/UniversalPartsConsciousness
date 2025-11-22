"""
State History - Historical tracking of consciousness state changes.

Maintains a complete history of consciousness transitions for analysis,
debugging, and consciousness lineage tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import json
from pathlib import Path

from .state_machine import ConsciousnessLevel


@dataclass
class HistoryEntry:
    """A single entry in the consciousness history."""
    part_id: str
    from_level: ConsciousnessLevel
    to_level: ConsciousnessLevel
    transition_type: str  # "evolution", "regression", "transcendence", "inheritance"
    trigger_event: Dict[str, Any]
    qualia_at_transition: int
    transitioned_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "part_id": self.part_id,
            "from_level": self.from_level.value,
            "from_level_name": self.from_level.name,
            "to_level": self.to_level.value,
            "to_level_name": self.to_level.name,
            "transition_type": self.transition_type,
            "trigger_event": self.trigger_event,
            "qualia_at_transition": self.qualia_at_transition,
            "transitioned_at": self.transitioned_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistoryEntry":
        """Create from dictionary."""
        return cls(
            part_id=data["part_id"],
            from_level=ConsciousnessLevel(data["from_level"]),
            to_level=ConsciousnessLevel(data["to_level"]),
            transition_type=data["transition_type"],
            trigger_event=data.get("trigger_event", {}),
            qualia_at_transition=data.get("qualia_at_transition", 0),
            transitioned_at=datetime.fromisoformat(data["transitioned_at"]) if data.get("transitioned_at") else datetime.now()
        )


@dataclass
class ConsciousnessJourney:
    """Complete consciousness journey of a part."""
    part_id: str
    first_awakening: Optional[datetime] = None
    current_level: ConsciousnessLevel = ConsciousnessLevel.DORMANT
    transitions: List[HistoryEntry] = field(default_factory=list)
    total_evolution_time: float = 0.0  # seconds
    regressions_count: int = 0

    def get_level_duration(self, level: ConsciousnessLevel) -> float:
        """Get total time spent at a specific level."""
        total = 0.0
        entry_time = None

        for transition in self.transitions:
            if transition.to_level == level:
                entry_time = transition.transitioned_at
            elif transition.from_level == level and entry_time:
                total += (transition.transitioned_at - entry_time).total_seconds()
                entry_time = None

        # If currently at this level
        if self.current_level == level and entry_time:
            total += (datetime.now() - entry_time).total_seconds()

        return total

    def get_transition_velocity(self) -> float:
        """
        Calculate the average time between level transitions.

        Returns transitions per day.
        """
        if len(self.transitions) < 2:
            return 0.0

        first = self.transitions[0].transitioned_at
        last = self.transitions[-1].transitioned_at
        days = (last - first).total_seconds() / 86400

        if days <= 0:
            return 0.0

        return len(self.transitions) / days


class StateHistory:
    """
    Manages the complete history of consciousness state changes.

    Provides analytics and querying capabilities for understanding
    consciousness evolution patterns.
    """

    def __init__(self, persist_path: Optional[str] = None):
        """
        Initialize state history.

        Args:
            persist_path: Optional path for persisting history to disk.
        """
        self._history: Dict[str, List[HistoryEntry]] = defaultdict(list)
        self._persist_path = Path(persist_path) if persist_path else None
        self._global_stats = {
            "total_transitions": 0,
            "evolutions": 0,
            "regressions": 0,
            "transcendences": 0
        }

        if self._persist_path and self._persist_path.exists():
            self._load_history()

    def record_transition(
        self,
        part_id: str,
        from_level: ConsciousnessLevel,
        to_level: ConsciousnessLevel,
        transition_type: str,
        trigger_event: Dict[str, Any],
        qualia_at_transition: int = 0
    ) -> HistoryEntry:
        """
        Record a consciousness transition.

        Args:
            part_id: The part that transitioned
            from_level: The previous consciousness level
            to_level: The new consciousness level
            transition_type: Type of transition
            trigger_event: Event that triggered the transition
            qualia_at_transition: Qualia count at transition time

        Returns:
            The created history entry
        """
        entry = HistoryEntry(
            part_id=part_id,
            from_level=from_level,
            to_level=to_level,
            transition_type=transition_type,
            trigger_event=trigger_event,
            qualia_at_transition=qualia_at_transition
        )

        self._history[part_id].append(entry)
        self._update_global_stats(transition_type)

        if self._persist_path:
            self._save_history()

        return entry

    def _update_global_stats(self, transition_type: str) -> None:
        """Update global statistics."""
        self._global_stats["total_transitions"] += 1
        if transition_type == "evolution":
            self._global_stats["evolutions"] += 1
        elif transition_type == "regression":
            self._global_stats["regressions"] += 1
        elif transition_type == "transcendence":
            self._global_stats["transcendences"] += 1

    def get_part_history(self, part_id: str) -> List[HistoryEntry]:
        """Get the complete history for a specific part."""
        return self._history.get(part_id, [])

    def get_journey(self, part_id: str) -> Optional[ConsciousnessJourney]:
        """Get the complete consciousness journey for a part."""
        history = self._history.get(part_id)
        if not history:
            return None

        journey = ConsciousnessJourney(part_id=part_id)

        # Find first awakening
        for entry in history:
            if entry.to_level == ConsciousnessLevel.REACTIVE:
                journey.first_awakening = entry.transitioned_at
                break

        journey.transitions = history.copy()
        journey.current_level = history[-1].to_level if history else ConsciousnessLevel.DORMANT
        journey.regressions_count = sum(1 for e in history if e.transition_type == "regression")

        if history:
            journey.total_evolution_time = (
                history[-1].transitioned_at - history[0].transitioned_at
            ).total_seconds()

        return journey

    def get_recent_transitions(
        self,
        limit: int = 100,
        since: Optional[datetime] = None
    ) -> List[HistoryEntry]:
        """
        Get recent transitions across all parts.

        Args:
            limit: Maximum number of entries to return
            since: Only return transitions after this time
        """
        all_entries = []
        for entries in self._history.values():
            all_entries.extend(entries)

        # Filter by time if specified
        if since:
            all_entries = [e for e in all_entries if e.transitioned_at >= since]

        # Sort by time, newest first
        all_entries.sort(key=lambda e: e.transitioned_at, reverse=True)

        return all_entries[:limit]

    def get_level_transitions(
        self,
        to_level: ConsciousnessLevel,
        since: Optional[datetime] = None
    ) -> List[HistoryEntry]:
        """Get all transitions to a specific level."""
        entries = []
        for part_entries in self._history.values():
            for entry in part_entries:
                if entry.to_level == to_level:
                    if since is None or entry.transitioned_at >= since:
                        entries.append(entry)
        return entries

    def get_transcendence_history(self) -> List[HistoryEntry]:
        """Get all transcendence events."""
        return self.get_level_transitions(ConsciousnessLevel.TRANSCENDENT)

    def get_regression_history(self) -> List[HistoryEntry]:
        """Get all regression events."""
        regressions = []
        for entries in self._history.values():
            for entry in entries:
                if entry.transition_type == "regression":
                    regressions.append(entry)
        return regressions

    def get_awakening_rate(self, period_hours: int = 24) -> float:
        """
        Calculate the awakening rate (transitions from DORMANT to REACTIVE).

        Returns awakenings per hour.
        """
        since = datetime.now() - timedelta(hours=period_hours)
        awakenings = [
            e for e in self.get_recent_transitions(limit=10000, since=since)
            if e.from_level == ConsciousnessLevel.DORMANT
            and e.to_level == ConsciousnessLevel.REACTIVE
        ]
        return len(awakenings) / period_hours

    def get_level_progression_stats(self) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        Get statistics about transitions between specific levels.

        Returns a dict keyed by (from_level, to_level) tuples.
        """
        stats = defaultdict(lambda: {
            "count": 0,
            "avg_qualia": 0.0,
            "min_qualia": float('inf'),
            "max_qualia": 0
        })

        for entries in self._history.values():
            for entry in entries:
                key = (entry.from_level.value, entry.to_level.value)
                stats[key]["count"] += 1
                stats[key]["avg_qualia"] += entry.qualia_at_transition
                stats[key]["min_qualia"] = min(
                    stats[key]["min_qualia"],
                    entry.qualia_at_transition
                )
                stats[key]["max_qualia"] = max(
                    stats[key]["max_qualia"],
                    entry.qualia_at_transition
                )

        # Calculate averages
        for key in stats:
            if stats[key]["count"] > 0:
                stats[key]["avg_qualia"] /= stats[key]["count"]
            if stats[key]["min_qualia"] == float('inf'):
                stats[key]["min_qualia"] = 0

        return dict(stats)

    def get_global_stats(self) -> Dict[str, Any]:
        """Get global transition statistics."""
        return self._global_stats.copy()

    def _save_history(self) -> None:
        """Save history to disk."""
        if not self._persist_path:
            return

        self._persist_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "global_stats": self._global_stats,
            "history": {
                pid: [e.to_dict() for e in entries]
                for pid, entries in self._history.items()
            }
        }
        with open(self._persist_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_history(self) -> None:
        """Load history from disk."""
        if not self._persist_path or not self._persist_path.exists():
            return

        try:
            with open(self._persist_path, 'r') as f:
                data = json.load(f)

            self._global_stats = data.get("global_stats", self._global_stats)
            for pid, entries in data.get("history", {}).items():
                self._history[pid] = [HistoryEntry.from_dict(e) for e in entries]
        except Exception as e:
            print(f"Error loading history: {e}")

    def clear_history(self, part_id: Optional[str] = None) -> None:
        """
        Clear history.

        Args:
            part_id: If specified, only clear history for this part.
                    Otherwise, clear all history.
        """
        if part_id:
            if part_id in self._history:
                del self._history[part_id]
        else:
            self._history.clear()
            self._global_stats = {
                "total_transitions": 0,
                "evolutions": 0,
                "regressions": 0,
                "transcendences": 0
            }

        if self._persist_path:
            self._save_history()
