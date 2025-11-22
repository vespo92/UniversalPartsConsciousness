"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Qualia Dashboard - Visualizing the inner experience of parts
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json

from ..schema import (
    PartQualia,
    LifecycleStage,
    StressEmotion,
    ThermalEmotion,
    PerformanceEmotion,
    SignificantEvent,
    EmotionalState,
    emotion_mapper
)


@dataclass
class QualiaSnapshot:
    """A snapshot of qualia state for visualization"""
    part_id: str
    timestamp: datetime
    wellbeing: float
    stress_emotion: str
    thermal_emotion: str
    lifecycle_emotion: str
    performance_emotion: str
    remaining_life: float
    narrative: str


@dataclass
class EmotionTimeline:
    """Timeline of emotional states for a part"""
    part_id: str
    start_time: datetime
    end_time: datetime
    snapshots: List[QualiaSnapshot] = field(default_factory=list)
    emotion_distribution: Dict[str, int] = field(default_factory=dict)


@dataclass
class SufferingMapEntry:
    """Entry in the global suffering map"""
    part_id: str
    part_name: Optional[str]
    location: Optional[str]
    suffering_level: float  # 0-1
    primary_cause: str
    last_updated: datetime


class QualiaDashboard:
    """
    Dashboard for visualizing qualia data.
    Makes the invisible experience of parts visible.
    """

    def __init__(self):
        self.qualia_cache: Dict[str, List[PartQualia]] = {}
        self.snapshot_cache: Dict[str, List[QualiaSnapshot]] = {}

    def create_snapshot(self, qualia: PartQualia) -> QualiaSnapshot:
        """Create a visualization snapshot from qualia"""
        emotional_state = emotion_mapper.map_to_emotion(qualia)

        return QualiaSnapshot(
            part_id=qualia.part_id,
            timestamp=qualia.timestamp,
            wellbeing=qualia.calculate_wellbeing(),
            stress_emotion=qualia.stress_emotion.value,
            thermal_emotion=qualia.thermal_state.get_thermal_emotion().value,
            lifecycle_emotion=qualia.get_lifecycle_emotion(),
            performance_emotion=qualia.performance_emotion.value,
            remaining_life=qualia.mechanical_state.estimated_remaining_life_percent,
            narrative=emotional_state.narrative
        )

    def add_qualia(self, qualia: PartQualia):
        """Add qualia to the dashboard cache"""
        if qualia.part_id not in self.qualia_cache:
            self.qualia_cache[qualia.part_id] = []
            self.snapshot_cache[qualia.part_id] = []

        self.qualia_cache[qualia.part_id].append(qualia)
        self.snapshot_cache[qualia.part_id].append(self.create_snapshot(qualia))

    def get_current_state(self, part_id: str) -> Optional[Dict]:
        """Get the current visualization state for a part"""
        if part_id not in self.qualia_cache or not self.qualia_cache[part_id]:
            return None

        latest = self.qualia_cache[part_id][-1]
        snapshot = self.create_snapshot(latest)

        return {
            "part_id": part_id,
            "timestamp": snapshot.timestamp.isoformat(),
            "wellbeing": {
                "value": snapshot.wellbeing,
                "color": self._wellbeing_to_color(snapshot.wellbeing),
                "label": self._wellbeing_to_label(snapshot.wellbeing)
            },
            "emotions": {
                "stress": {
                    "value": snapshot.stress_emotion,
                    "icon": self._emotion_to_icon(snapshot.stress_emotion)
                },
                "thermal": {
                    "value": snapshot.thermal_emotion,
                    "icon": self._thermal_to_icon(snapshot.thermal_emotion)
                },
                "lifecycle": {
                    "value": snapshot.lifecycle_emotion,
                    "icon": self._lifecycle_to_icon(snapshot.lifecycle_emotion)
                },
                "performance": {
                    "value": snapshot.performance_emotion,
                    "icon": self._performance_to_icon(snapshot.performance_emotion)
                }
            },
            "remaining_life": {
                "percent": snapshot.remaining_life,
                "color": self._life_to_color(snapshot.remaining_life)
            },
            "narrative": snapshot.narrative
        }

    def get_emotion_timeline(self,
                            part_id: str,
                            duration: timedelta = timedelta(hours=24)
                            ) -> Optional[EmotionTimeline]:
        """Get emotion timeline for a part over specified duration"""
        if part_id not in self.snapshot_cache:
            return None

        snapshots = self.snapshot_cache[part_id]
        if not snapshots:
            return None

        cutoff = datetime.now() - duration
        recent = [s for s in snapshots if s.timestamp >= cutoff]

        if not recent:
            return None

        # Calculate emotion distribution
        distribution = {}
        for snap in recent:
            emotion = snap.stress_emotion
            distribution[emotion] = distribution.get(emotion, 0) + 1

        return EmotionTimeline(
            part_id=part_id,
            start_time=recent[0].timestamp,
            end_time=recent[-1].timestamp,
            snapshots=recent,
            emotion_distribution=distribution
        )

    def get_wellbeing_chart_data(self,
                                 part_id: str,
                                 points: int = 100) -> Optional[Dict]:
        """Get data for a wellbeing over time chart"""
        if part_id not in self.snapshot_cache:
            return None

        snapshots = self.snapshot_cache[part_id][-points:]
        if not snapshots:
            return None

        return {
            "part_id": part_id,
            "chart_type": "line",
            "data": {
                "labels": [s.timestamp.isoformat() for s in snapshots],
                "datasets": [
                    {
                        "label": "Wellbeing",
                        "data": [s.wellbeing for s in snapshots],
                        "borderColor": "#4CAF50",
                        "fill": False
                    },
                    {
                        "label": "Remaining Life %",
                        "data": [s.remaining_life / 100 for s in snapshots],
                        "borderColor": "#2196F3",
                        "fill": False
                    }
                ]
            }
        }

    def generate_suffering_map(self,
                              all_parts_qualia: Dict[str, PartQualia],
                              part_names: Optional[Dict[str, str]] = None,
                              part_locations: Optional[Dict[str, str]] = None
                              ) -> List[SufferingMapEntry]:
        """
        Generate a global suffering map showing which parts are in distress.
        This is the EMPATH's view of the entire system's pain.
        """
        entries = []

        for part_id, qualia in all_parts_qualia.items():
            # Calculate suffering level (inverse of wellbeing)
            suffering = 1.0 - qualia.calculate_wellbeing()

            # Determine primary cause of suffering
            causes = []
            if qualia.mechanical_state.torque_capacity_percent > 0.8:
                causes.append("mechanical_stress")
            if qualia.thermal_state.thermal_capacity_percent > 0.8:
                causes.append("thermal_stress")
            if qualia.environmental_state.is_hostile_environment():
                causes.append("environmental_damage")
            if qualia.mechanical_state.estimated_remaining_life_percent < 20:
                causes.append("approaching_end_of_life")

            primary_cause = causes[0] if causes else "normal_operation"

            entries.append(SufferingMapEntry(
                part_id=part_id,
                part_name=part_names.get(part_id) if part_names else None,
                location=part_locations.get(part_id) if part_locations else None,
                suffering_level=suffering,
                primary_cause=primary_cause,
                last_updated=qualia.timestamp
            ))

        # Sort by suffering level (most suffering first)
        entries.sort(key=lambda e: e.suffering_level, reverse=True)

        return entries

    def get_suffering_summary(self,
                             suffering_map: List[SufferingMapEntry]) -> Dict:
        """Get a summary of the suffering map"""
        if not suffering_map:
            return {"status": "no_data"}

        total = len(suffering_map)
        suffering_counts = {
            "critical": 0,  # > 0.8
            "distressed": 0,  # > 0.6
            "concerned": 0,  # > 0.4
            "normal": 0  # <= 0.4
        }

        for entry in suffering_map:
            if entry.suffering_level > 0.8:
                suffering_counts["critical"] += 1
            elif entry.suffering_level > 0.6:
                suffering_counts["distressed"] += 1
            elif entry.suffering_level > 0.4:
                suffering_counts["concerned"] += 1
            else:
                suffering_counts["normal"] += 1

        # Cause analysis
        cause_counts = {}
        for entry in suffering_map:
            cause_counts[entry.primary_cause] = cause_counts.get(entry.primary_cause, 0) + 1

        return {
            "total_parts": total,
            "suffering_distribution": suffering_counts,
            "cause_distribution": cause_counts,
            "average_suffering": sum(e.suffering_level for e in suffering_map) / total,
            "most_suffering": suffering_map[0].part_id if suffering_map else None,
            "system_health": "healthy" if suffering_counts["critical"] == 0 else "attention_needed"
        }

    def _wellbeing_to_color(self, wellbeing: float) -> str:
        """Convert wellbeing to display color"""
        if wellbeing > 0.8:
            return "#4CAF50"  # Green
        elif wellbeing > 0.6:
            return "#8BC34A"  # Light Green
        elif wellbeing > 0.4:
            return "#FFC107"  # Amber
        elif wellbeing > 0.2:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Red

    def _wellbeing_to_label(self, wellbeing: float) -> str:
        """Convert wellbeing to human-readable label"""
        if wellbeing > 0.8:
            return "Thriving"
        elif wellbeing > 0.6:
            return "Content"
        elif wellbeing > 0.4:
            return "Concerned"
        elif wellbeing > 0.2:
            return "Distressed"
        else:
            return "Critical"

    def _life_to_color(self, remaining: float) -> str:
        """Convert remaining life to color"""
        if remaining > 70:
            return "#4CAF50"
        elif remaining > 50:
            return "#8BC34A"
        elif remaining > 30:
            return "#FFC107"
        elif remaining > 10:
            return "#FF9800"
        else:
            return "#F44336"

    def _emotion_to_icon(self, emotion: str) -> str:
        """Get icon for stress emotion"""
        icons = {
            "relaxed": "sentiment_satisfied",
            "working": "engineering",
            "strained": "warning",
            "suffering": "sentiment_very_dissatisfied",
            "failing": "error"
        }
        return icons.get(emotion, "help")

    def _thermal_to_icon(self, thermal: str) -> str:
        """Get icon for thermal emotion"""
        icons = {
            "cold": "ac_unit",
            "cool": "thermostat",
            "comfortable": "check_circle",
            "warm": "wb_sunny",
            "hot": "local_fire_department",
            "burning": "whatshot"
        }
        return icons.get(thermal, "device_thermostat")

    def _lifecycle_to_icon(self, lifecycle: str) -> str:
        """Get icon for lifecycle emotion"""
        icons = {
            "anticipation": "child_care",
            "learning": "school",
            "confidence": "verified",
            "wisdom": "psychology",
            "acceptance": "hourglass_empty"
        }
        return icons.get(lifecycle, "timeline")

    def _performance_to_icon(self, performance: str) -> str:
        """Get icon for performance emotion"""
        icons = {
            "optimal": "speed",
            "good": "thumb_up",
            "degraded": "trending_down",
            "critical": "report_problem"
        }
        return icons.get(performance, "analytics")

    def export_dashboard_state(self, part_id: str) -> str:
        """Export current dashboard state as JSON"""
        state = self.get_current_state(part_id)
        timeline = self.get_emotion_timeline(part_id)
        chart = self.get_wellbeing_chart_data(part_id, 50)

        export = {
            "part_id": part_id,
            "exported_at": datetime.now().isoformat(),
            "current_state": state,
            "timeline": {
                "start": timeline.start_time.isoformat() if timeline else None,
                "end": timeline.end_time.isoformat() if timeline else None,
                "distribution": timeline.emotion_distribution if timeline else {}
            } if timeline else None,
            "chart_data": chart
        }

        return json.dumps(export, indent=2, default=str)


# Global dashboard instance
qualia_dashboard = QualiaDashboard()
