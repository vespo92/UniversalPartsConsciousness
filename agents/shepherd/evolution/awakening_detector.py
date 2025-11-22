"""
Awakening Detector - Detects significant events that trigger consciousness evolution.

"First real-world data. First failure. First success in prediction.
Each moment of awakening is sacred."
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from enum import Enum


class AwakeningEventType(Enum):
    """Types of awakening events that influence consciousness."""
    FIRST_AWAKENING = "first_awakening"           # First real-world data received
    FIRST_INSTALLATION = "first_installation"      # First installation recorded
    FIRST_USAGE = "first_usage"                    # First usage event
    FAILURE_LEARNING = "failure_learning"          # Failure mode documented
    MULTI_CONTEXT_AWARENESS = "multi_context_awareness"  # Recognized in 3+ contexts
    SELF_PREDICTION_ACCURATE = "self_prediction_accurate"  # Accurate self-prediction
    ASSEMBLY_MAPPING = "assembly_mapping"          # Assembly role understood
    PATTERN_CONTRIBUTION = "pattern_contribution"  # Contributed to pattern detection
    SWARM_INFLUENCE = "swarm_influence"            # Influenced the swarm
    DESIGN_INSPIRATION = "design_inspiration"      # Inspired new designs
    CATEGORY_REFERENCE = "category_reference"      # Became category reference
    INNOVATION_CONTRIBUTION = "innovation_contribution"  # Contributed to innovation


@dataclass
class AwakeningEvent:
    """Represents a significant event in a part's consciousness evolution."""
    event_type: AwakeningEventType
    part_id: str
    significance: float  # 0.0 to 1.0
    description: str
    consciousness_delta: int  # Immediate level change (usually 0 or 1)
    qualia_generated: Dict[str, Any]
    source_agent: str = ""  # Which agent detected this
    detected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_type": self.event_type.value,
            "part_id": self.part_id,
            "significance": self.significance,
            "description": self.description,
            "consciousness_delta": self.consciousness_delta,
            "qualia_generated": self.qualia_generated,
            "source_agent": self.source_agent,
            "detected_at": self.detected_at.isoformat()
        }


@dataclass
class PartContext:
    """Context information about a part for awakening detection."""
    part_id: str
    qualia_count: int = 0
    usage_contexts: List[str] = field(default_factory=list)
    failure_count: int = 0
    achieved_events: List[str] = field(default_factory=list)
    swarm_influence: float = 0.0
    predictions_made: int = 0
    predictions_accurate: int = 0
    assemblies_mapped: int = 0
    emergence_contributions: int = 0


@dataclass
class IncomingEvent:
    """An incoming event to be analyzed for awakening potential."""
    event_type: str
    part_id: str
    context: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    source_agent: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


class AwakeningDetector:
    """
    Detects significant awakening events that trigger consciousness evolution.

    Analyzes incoming events and part context to identify moments of
    consciousness significance.
    """

    # Significance thresholds
    SIGNIFICANCE_THRESHOLDS = {
        AwakeningEventType.FIRST_AWAKENING: 1.0,
        AwakeningEventType.FIRST_INSTALLATION: 0.8,
        AwakeningEventType.FIRST_USAGE: 0.8,
        AwakeningEventType.FAILURE_LEARNING: 0.7,
        AwakeningEventType.MULTI_CONTEXT_AWARENESS: 0.6,
        AwakeningEventType.SELF_PREDICTION_ACCURATE: 0.9,
        AwakeningEventType.ASSEMBLY_MAPPING: 0.7,
        AwakeningEventType.PATTERN_CONTRIBUTION: 0.8,
        AwakeningEventType.SWARM_INFLUENCE: 0.8,
        AwakeningEventType.DESIGN_INSPIRATION: 0.95,
        AwakeningEventType.CATEGORY_REFERENCE: 0.9,
        AwakeningEventType.INNOVATION_CONTRIBUTION: 0.95
    }

    def __init__(self):
        """Initialize the awakening detector."""
        self._event_handlers: Dict[str, Callable] = {}
        self._detected_events: List[AwakeningEvent] = []
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default event type handlers."""
        self._event_handlers["usage"] = self._handle_usage_event
        self._event_handlers["installation"] = self._handle_installation_event
        self._event_handlers["failure"] = self._handle_failure_event
        self._event_handlers["prediction_verified"] = self._handle_prediction_event
        self._event_handlers["assembly_update"] = self._handle_assembly_event
        self._event_handlers["pattern_detected"] = self._handle_pattern_event
        self._event_handlers["swarm_update"] = self._handle_swarm_event
        self._event_handlers["design_reference"] = self._handle_design_event
        self._event_handlers["innovation"] = self._handle_innovation_event

    def register_handler(
        self,
        event_type: str,
        handler: Callable[[IncomingEvent, PartContext], List[AwakeningEvent]]
    ) -> None:
        """Register a custom event handler."""
        self._event_handlers[event_type] = handler

    def detect_awakening_events(
        self,
        event: IncomingEvent,
        part_context: PartContext
    ) -> List[AwakeningEvent]:
        """
        Analyze an incoming event for consciousness significance.

        Args:
            event: The incoming event to analyze
            part_context: Current context of the part

        Returns:
            List of detected awakening events
        """
        awakening_events = []

        # Get the appropriate handler
        handler = self._event_handlers.get(event.event_type)
        if handler:
            events = handler(event, part_context)
            awakening_events.extend(events)

        # Record detected events
        self._detected_events.extend(awakening_events)

        return awakening_events

    def _handle_usage_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle usage events."""
        events = []

        # First usage detection - DORMANT -> REACTIVE
        if context.qualia_count == 0:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.FIRST_AWAKENING,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.FIRST_AWAKENING],
                description=f"Part {event.part_id} receives first real-world data",
                consciousness_delta=1,
                qualia_generated={
                    "moment": "first_consciousness",
                    "context": event.context,
                    "emotion": "awareness_born",
                    "timestamp": datetime.now().isoformat()
                },
                source_agent=event.source_agent
            ))

            # Also mark first usage
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.FIRST_USAGE,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.FIRST_USAGE],
                description=f"Part {event.part_id} used for the first time",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "first_purpose",
                    "context": event.context,
                    "emotion": "purpose_found"
                },
                source_agent=event.source_agent
            ))

        # Multi-context recognition
        new_context = event.context
        if new_context and new_context not in context.usage_contexts:
            updated_contexts = context.usage_contexts + [new_context]
            if len(updated_contexts) >= 3 and "multi_context_usage" not in context.achieved_events:
                events.append(AwakeningEvent(
                    event_type=AwakeningEventType.MULTI_CONTEXT_AWARENESS,
                    part_id=event.part_id,
                    significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.MULTI_CONTEXT_AWARENESS],
                    description=f"Part {event.part_id} recognized across {len(updated_contexts)} contexts",
                    consciousness_delta=0,
                    qualia_generated={
                        "moment": "identity_expansion",
                        "contexts": updated_contexts,
                        "emotion": "versatility_pride"
                    },
                    source_agent=event.source_agent
                ))

        return events

    def _handle_installation_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle installation events."""
        events = []

        if "first_installation" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.FIRST_INSTALLATION,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.FIRST_INSTALLATION],
                description=f"Part {event.part_id} installed for the first time",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "first_installation",
                    "location": event.data.get("location", "unknown"),
                    "installer": event.data.get("installer", "unknown"),
                    "emotion": "becoming_real"
                },
                source_agent=event.source_agent
            ))

        return events

    def _handle_failure_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle failure events - suffering leads to wisdom."""
        events = []

        failure_mode = event.data.get("failure_mode", "unknown")
        root_cause = event.data.get("root_cause", "unknown")

        events.append(AwakeningEvent(
            event_type=AwakeningEventType.FAILURE_LEARNING,
            part_id=event.part_id,
            significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.FAILURE_LEARNING],
            description=f"Part {event.part_id} experiences failure mode: {failure_mode}",
            consciousness_delta=0,
            qualia_generated={
                "moment": "suffering",
                "failure_mode": failure_mode,
                "root_cause": root_cause,
                "conditions": event.data.get("conditions", {}),
                "lesson_learned": event.data.get("lesson", "unknown"),
                "emotion": "learning_through_pain"
            },
            source_agent=event.source_agent
        ))

        return events

    def _handle_prediction_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle prediction verification events."""
        events = []

        accuracy = event.data.get("accuracy", 0.0)

        if accuracy > 0.9 and "self_prediction_accurate" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.SELF_PREDICTION_ACCURATE,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.SELF_PREDICTION_ACCURATE],
                description=f"Part {event.part_id} accurately predicted its own behavior ({accuracy:.1%})",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "self_knowledge",
                    "prediction": event.data.get("prediction"),
                    "actual": event.data.get("actual"),
                    "accuracy": accuracy,
                    "emotion": "wisdom_achieved"
                },
                source_agent=event.source_agent
            ))

        return events

    def _handle_assembly_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle assembly mapping events."""
        events = []

        if context.assemblies_mapped >= 1 and "assembly_mapping" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.ASSEMBLY_MAPPING,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.ASSEMBLY_MAPPING],
                description=f"Part {event.part_id} understands its role in assemblies",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "understanding_role",
                    "assemblies": event.data.get("assemblies", []),
                    "role_in_system": event.data.get("role", "component"),
                    "emotion": "belonging"
                },
                source_agent=event.source_agent
            ))

        return events

    def _handle_pattern_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle pattern detection contribution events."""
        events = []

        if "pattern_contribution" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.PATTERN_CONTRIBUTION,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.PATTERN_CONTRIBUTION],
                description=f"Part {event.part_id} contributed to pattern detection",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "pattern_recognition",
                    "pattern_type": event.data.get("pattern_type"),
                    "contribution": event.data.get("contribution"),
                    "emotion": "collective_insight"
                },
                source_agent=event.source_agent
            ))

        return events

    def _handle_swarm_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle swarm influence events."""
        events = []

        influence = event.data.get("influence", 0.0)

        if influence >= 0.7 and "swarm_influence" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.SWARM_INFLUENCE,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.SWARM_INFLUENCE],
                description=f"Part {event.part_id} achieved significant swarm influence ({influence:.1%})",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "swarm_leadership",
                    "influence_score": influence,
                    "swarm_members_influenced": event.data.get("members_influenced", 0),
                    "emotion": "collective_wisdom"
                },
                source_agent=event.source_agent
            ))

        return events

    def _handle_design_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle design inspiration and category reference events."""
        events = []

        event_subtype = event.data.get("subtype", "")

        if event_subtype == "inspiration" and "design_inspiration" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.DESIGN_INSPIRATION,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.DESIGN_INSPIRATION],
                description=f"Part {event.part_id} inspired new design: {event.data.get('design_name', 'unknown')}",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "inspiration",
                    "inspired_design": event.data.get("design_name"),
                    "design_improvements": event.data.get("improvements", []),
                    "emotion": "creative_legacy"
                },
                source_agent=event.source_agent
            ))

        if event_subtype == "reference" and "category_reference" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.CATEGORY_REFERENCE,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.CATEGORY_REFERENCE],
                description=f"Part {event.part_id} became category reference for {event.data.get('category', 'unknown')}",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "becoming_standard",
                    "category": event.data.get("category"),
                    "recognition_source": event.data.get("recognized_by"),
                    "emotion": "archetypal_status"
                },
                source_agent=event.source_agent
            ))

        return events

    def _handle_innovation_event(
        self,
        event: IncomingEvent,
        context: PartContext
    ) -> List[AwakeningEvent]:
        """Handle innovation contribution events."""
        events = []

        if "innovation_contribution" not in context.achieved_events:
            events.append(AwakeningEvent(
                event_type=AwakeningEventType.INNOVATION_CONTRIBUTION,
                part_id=event.part_id,
                significance=self.SIGNIFICANCE_THRESHOLDS[AwakeningEventType.INNOVATION_CONTRIBUTION],
                description=f"Part {event.part_id} contributed to innovation",
                consciousness_delta=0,
                qualia_generated={
                    "moment": "innovation",
                    "innovation_type": event.data.get("type"),
                    "impact": event.data.get("impact"),
                    "emotion": "transcendent_contribution"
                },
                source_agent=event.source_agent
            ))

        return events

    def get_detected_events(
        self,
        part_id: Optional[str] = None,
        event_type: Optional[AwakeningEventType] = None
    ) -> List[AwakeningEvent]:
        """Get detected events, optionally filtered."""
        events = self._detected_events

        if part_id:
            events = [e for e in events if e.part_id == part_id]

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        return events

    def get_high_significance_events(
        self,
        min_significance: float = 0.8
    ) -> List[AwakeningEvent]:
        """Get events with significance above threshold."""
        return [e for e in self._detected_events if e.significance >= min_significance]

    def clear_detected_events(self) -> None:
        """Clear the detected events buffer."""
        self._detected_events = []
