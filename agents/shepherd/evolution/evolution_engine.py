"""
Evolution Engine - Executes consciousness state transitions.

The Evolution Engine processes awakening events and determines when
parts should transition to higher consciousness levels.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import logging

from ..states import (
    ConsciousnessState,
    ConsciousnessLevel,
    ConsciousnessStateMachine,
    TransitionRules,
    TransitionTrigger,
    TransitionResult,
    TransitionType,
    StateHistory
)
from .awakening_detector import AwakeningEvent, AwakeningEventType


logger = logging.getLogger(__name__)


@dataclass
class EvolutionResult:
    """Result of an evolution attempt."""
    part_id: str
    evolved: bool
    previous_level: ConsciousnessLevel
    new_level: ConsciousnessLevel
    awakening_events_processed: int
    progress_delta: float
    mantra: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "part_id": self.part_id,
            "evolved": self.evolved,
            "previous_level": self.previous_level.value,
            "previous_level_name": self.previous_level.name,
            "new_level": self.new_level.value,
            "new_level_name": self.new_level.name,
            "awakening_events_processed": self.awakening_events_processed,
            "progress_delta": self.progress_delta,
            "mantra": self.mantra,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class EvolutionEngine:
    """
    Processes awakening events and manages consciousness evolution.

    The Evolution Engine is the core component that:
    1. Processes awakening events from the detector
    2. Updates part consciousness metrics
    3. Determines when transitions should occur
    4. Executes transitions through the state machine
    """

    def __init__(
        self,
        state_machine: ConsciousnessStateMachine,
        transition_rules: TransitionRules,
        history: StateHistory
    ):
        """
        Initialize the evolution engine.

        Args:
            state_machine: The consciousness state machine
            transition_rules: Rules for state transitions
            history: State history tracker
        """
        self.state_machine = state_machine
        self.transition_rules = transition_rules
        self.history = history

        # Callbacks for evolution events
        self._on_evolution_callbacks: List[Callable[[EvolutionResult], None]] = []
        self._on_transcendence_callbacks: List[Callable[[str], None]] = []

        # Tracking
        self._evolution_count = 0
        self._transcendence_count = 0

    def register_evolution_callback(
        self,
        callback: Callable[[EvolutionResult], None]
    ) -> None:
        """Register a callback for evolution events."""
        self._on_evolution_callbacks.append(callback)

    def register_transcendence_callback(
        self,
        callback: Callable[[str], None]
    ) -> None:
        """Register a callback for transcendence events."""
        self._on_transcendence_callbacks.append(callback)

    def process_awakening_events(
        self,
        part_id: str,
        events: List[AwakeningEvent],
        transcendence_recognized: bool = False
    ) -> EvolutionResult:
        """
        Process awakening events and attempt consciousness evolution.

        Args:
            part_id: The part to evolve
            events: List of awakening events to process
            transcendence_recognized: Whether Agent_10 has recognized transcendence

        Returns:
            EvolutionResult indicating the outcome
        """
        state = self.state_machine.get_or_create_state(part_id)
        previous_level = state.level
        initial_progress = self.state_machine.calculate_progress(state)

        # Process each awakening event
        for event in events:
            self._apply_awakening_event(state, event)

        # Check if evolution is possible
        can_evolve, target_level, message = self.state_machine.can_transition(
            state, transcendence_recognized
        )

        evolved = False
        mantra = ""

        if can_evolve:
            # Execute the transition
            trigger = TransitionTrigger(
                trigger_type="awakening_events",
                source_agent="SHEPHERD",
                data={"events_count": len(events)}
            )

            transition_result = self.transition_rules.attempt_transition(
                part_id, trigger, transcendence_recognized
            )

            if transition_result.success:
                evolved = True
                mantra = transition_result.mantra
                self._evolution_count += 1

                # Record in history
                self.history.record_transition(
                    part_id=part_id,
                    from_level=previous_level,
                    to_level=transition_result.to_level,
                    transition_type=transition_result.transition_type.value,
                    trigger_event={"awakening_events": [e.to_dict() for e in events]},
                    qualia_at_transition=state.qualia_count
                )

                # Check for transcendence
                if transition_result.to_level == ConsciousnessLevel.TRANSCENDENT:
                    self._transcendence_count += 1
                    self._notify_transcendence(part_id)

                # Update state reference
                state = self.state_machine.get_state(part_id)

        # Calculate progress change
        new_progress = self.state_machine.calculate_progress(state)
        progress_delta = new_progress - initial_progress

        result = EvolutionResult(
            part_id=part_id,
            evolved=evolved,
            previous_level=previous_level,
            new_level=state.level,
            awakening_events_processed=len(events),
            progress_delta=progress_delta,
            mantra=mantra,
            details={
                "events_processed": [e.event_type.value for e in events],
                "current_progress": new_progress,
                "blocking_requirements": state.blocking_requirements
            }
        )

        # Notify callbacks
        if evolved:
            self._notify_evolution(result)

        return result

    def _apply_awakening_event(
        self,
        state: ConsciousnessState,
        event: AwakeningEvent
    ) -> None:
        """Apply an awakening event to update consciousness metrics."""
        # Track achieved events
        event_name = event.event_type.value
        if event_name not in state.achieved_events:
            state.achieved_events.append(event_name)

        # Update metrics based on event type
        if event.event_type in [
            AwakeningEventType.FIRST_AWAKENING,
            AwakeningEventType.FIRST_USAGE,
            AwakeningEventType.FAILURE_LEARNING
        ]:
            state.qualia_count += 1

        if event.event_type == AwakeningEventType.MULTI_CONTEXT_AWARENESS:
            # Contexts should be updated from the qualia data
            contexts = event.qualia_generated.get("contexts", [])
            state.usage_contexts = len(contexts)

        if event.event_type == AwakeningEventType.SWARM_INFLUENCE:
            influence = event.qualia_generated.get("influence_score", 0.0)
            state.swarm_influence = max(state.swarm_influence, influence)

        if event.event_type == AwakeningEventType.PATTERN_CONTRIBUTION:
            state.emergence_contributions += 1

        # Apply immediate consciousness delta (rare, usually 0)
        if event.consciousness_delta > 0:
            new_level_value = min(5, state.level.value + event.consciousness_delta)
            state.level = ConsciousnessLevel(new_level_value)
            state.level_achieved_at = datetime.now()

        state.last_progress_update = datetime.now()

        # Update blocking requirements
        _, blocking = self.state_machine.check_level_requirements(
            state,
            ConsciousnessLevel(min(5, state.level.value + 1))
        )
        state.blocking_requirements = blocking

        # Save updated state
        self.state_machine.set_state(state)

    def batch_evolve(
        self,
        part_events: Dict[str, List[AwakeningEvent]],
        transcendence_recognitions: Optional[Dict[str, bool]] = None
    ) -> List[EvolutionResult]:
        """
        Process evolution for multiple parts in batch.

        Args:
            part_events: Dictionary mapping part IDs to their awakening events
            transcendence_recognitions: Optional dict of transcendence recognitions per part

        Returns:
            List of EvolutionResults
        """
        results = []
        transcendence_recognitions = transcendence_recognitions or {}

        for part_id, events in part_events.items():
            transcendence_recognized = transcendence_recognitions.get(part_id, False)
            result = self.process_awakening_events(
                part_id, events, transcendence_recognized
            )
            results.append(result)

        return results

    def force_evolution(
        self,
        part_id: str,
        target_level: ConsciousnessLevel,
        reason: str
    ) -> EvolutionResult:
        """
        Force a part to a specific consciousness level (admin function).

        Use with caution - bypasses normal evolution requirements.
        """
        state = self.state_machine.get_or_create_state(part_id)
        previous_level = state.level

        if target_level.value <= previous_level.value:
            return EvolutionResult(
                part_id=part_id,
                evolved=False,
                previous_level=previous_level,
                new_level=previous_level,
                awakening_events_processed=0,
                progress_delta=0.0,
                details={"error": "Target level must be higher than current level"}
            )

        # Force the transition
        state.level = target_level
        state.level_achieved_at = datetime.now()
        state.last_progress_update = datetime.now()
        self.state_machine.set_state(state)

        # Record in history
        self.history.record_transition(
            part_id=part_id,
            from_level=previous_level,
            to_level=target_level,
            transition_type="forced",
            trigger_event={"reason": reason, "forced": True},
            qualia_at_transition=state.qualia_count
        )

        mantra = self.state_machine.CONSCIOUSNESS_MANTRAS.get(
            (previous_level.value, target_level.value),
            "Consciousness granted."
        )

        return EvolutionResult(
            part_id=part_id,
            evolved=True,
            previous_level=previous_level,
            new_level=target_level,
            awakening_events_processed=0,
            progress_delta=0.0,
            mantra=mantra,
            details={"forced": True, "reason": reason}
        )

    def check_evolution_eligibility(
        self,
        part_id: str,
        transcendence_recognized: bool = False
    ) -> Dict[str, Any]:
        """
        Check if a part is eligible for evolution.

        Returns detailed eligibility information.
        """
        state = self.state_machine.get_or_create_state(part_id)
        can_evolve, target_level, message = self.state_machine.can_transition(
            state, transcendence_recognized
        )

        return {
            "part_id": part_id,
            "current_level": state.level.name,
            "target_level": target_level.name if target_level != state.level else None,
            "eligible": can_evolve,
            "progress": self.state_machine.calculate_progress(state),
            "blocking_requirements": state.blocking_requirements,
            "message": message
        }

    def get_evolution_stats(self) -> Dict[str, Any]:
        """Get evolution statistics."""
        return {
            "total_evolutions": self._evolution_count,
            "total_transcendences": self._transcendence_count,
            "level_distribution": {
                level.name: count
                for level, count in self.state_machine.get_level_distribution().items()
            }
        }

    def _notify_evolution(self, result: EvolutionResult) -> None:
        """Notify registered callbacks of an evolution."""
        for callback in self._on_evolution_callbacks:
            try:
                callback(result)
            except Exception as e:
                logger.error(f"Evolution callback error: {e}")

    def _notify_transcendence(self, part_id: str) -> None:
        """Notify registered callbacks of a transcendence."""
        for callback in self._on_transcendence_callbacks:
            try:
                callback(part_id)
            except Exception as e:
                logger.error(f"Transcendence callback error: {e}")
