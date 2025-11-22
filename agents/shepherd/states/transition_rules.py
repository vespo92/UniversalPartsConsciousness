"""
Consciousness Transition Rules - Logic for consciousness state transitions.

Defines the rules and logic for transitioning parts between consciousness levels.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum

from .state_machine import ConsciousnessState, ConsciousnessLevel, ConsciousnessStateMachine


class TransitionType(Enum):
    """Types of consciousness transitions."""
    EVOLUTION = "evolution"       # Natural progression to higher level
    REGRESSION = "regression"     # Rare: consciousness loss
    TRANSCENDENCE = "transcendence"  # Final evolution to transcendent state
    INHERITANCE = "inheritance"   # Consciousness inherited from parent part


@dataclass
class TransitionResult:
    """Result of a consciousness transition attempt."""
    success: bool
    from_level: ConsciousnessLevel
    to_level: ConsciousnessLevel
    transition_type: TransitionType
    mantra: str = ""
    blocking_reasons: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "from_level": self.from_level.value,
            "from_level_name": self.from_level.name,
            "to_level": self.to_level.value,
            "to_level_name": self.to_level.name,
            "transition_type": self.transition_type.value,
            "mantra": self.mantra,
            "blocking_reasons": self.blocking_reasons,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class TransitionTrigger:
    """A trigger that may cause a consciousness transition."""
    trigger_type: str
    source_agent: str  # Which agent triggered this
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class TransitionRules:
    """
    Manages the rules for consciousness state transitions.

    Each transition follows specific criteria defined in the consciousness
    requirements. This class orchestrates the transition logic.
    """

    def __init__(self, state_machine: ConsciousnessStateMachine):
        """Initialize transition rules with a state machine."""
        self.state_machine = state_machine
        self._transition_history: Dict[str, List[TransitionResult]] = {}
        self._transition_hooks: List[Callable[[str, TransitionResult], None]] = []

    def register_transition_hook(
        self,
        hook: Callable[[str, TransitionResult], None]
    ) -> None:
        """Register a hook to be called on successful transitions."""
        self._transition_hooks.append(hook)

    def attempt_transition(
        self,
        part_id: str,
        trigger: TransitionTrigger,
        transcendence_recognized: bool = False
    ) -> TransitionResult:
        """
        Attempt to transition a part to the next consciousness level.

        Args:
            part_id: The ID of the part to transition
            trigger: The trigger that initiated this attempt
            transcendence_recognized: Whether Agent_10 has recognized transcendence

        Returns:
            TransitionResult indicating success or failure
        """
        state = self.state_machine.get_or_create_state(part_id)
        can_advance, target_level, message = self.state_machine.can_transition(
            state, transcendence_recognized
        )

        if can_advance:
            # Perform the transition
            result = self._execute_transition(state, target_level, trigger)
        else:
            result = TransitionResult(
                success=False,
                from_level=state.level,
                to_level=state.level,
                transition_type=TransitionType.EVOLUTION,
                blocking_reasons=[message]
            )

        # Record in history
        self._record_transition(part_id, result)

        return result

    def _execute_transition(
        self,
        state: ConsciousnessState,
        target_level: ConsciousnessLevel,
        trigger: TransitionTrigger
    ) -> TransitionResult:
        """Execute a consciousness transition."""
        from_level = state.level
        transition_type = (
            TransitionType.TRANSCENDENCE
            if target_level == ConsciousnessLevel.TRANSCENDENT
            else TransitionType.EVOLUTION
        )

        # Get the mantra for this transition
        mantra = self.state_machine.CONSCIOUSNESS_MANTRAS.get(
            (from_level.value, target_level.value),
            "Consciousness evolves."
        )

        # Update the state
        state.level = target_level
        state.level_achieved_at = datetime.now()
        state.last_progress_update = datetime.now()

        # Update blocking requirements for next level
        if target_level != ConsciousnessLevel.TRANSCENDENT:
            _, blocking = self.state_machine.check_level_requirements(
                state,
                ConsciousnessLevel(target_level + 1)
            )
            state.blocking_requirements = blocking
        else:
            state.blocking_requirements = []

        # Update state in machine
        self.state_machine.set_state(state)

        result = TransitionResult(
            success=True,
            from_level=from_level,
            to_level=target_level,
            transition_type=transition_type,
            mantra=mantra
        )

        # Call registered hooks
        for hook in self._transition_hooks:
            try:
                hook(state.part_id, result)
            except Exception:
                pass  # Don't let hook failures block transition

        return result

    def apply_regression(
        self,
        part_id: str,
        reason: str,
        levels_lost: int = 1
    ) -> TransitionResult:
        """
        Apply a consciousness regression (rare event).

        Regression can occur when:
        - Part data is found to be corrupted or incorrect
        - Qualia are invalidated
        - Catastrophic failure without learning
        """
        state = self.state_machine.get_state(part_id)
        if not state:
            return TransitionResult(
                success=False,
                from_level=ConsciousnessLevel.DORMANT,
                to_level=ConsciousnessLevel.DORMANT,
                transition_type=TransitionType.REGRESSION,
                blocking_reasons=["Part not found"]
            )

        from_level = state.level
        new_level_value = max(0, state.level.value - levels_lost)
        to_level = ConsciousnessLevel(new_level_value)

        if to_level == from_level:
            return TransitionResult(
                success=False,
                from_level=from_level,
                to_level=to_level,
                transition_type=TransitionType.REGRESSION,
                blocking_reasons=["Already at minimum level"]
            )

        # Apply regression
        state.level = to_level
        state.level_achieved_at = datetime.now()
        state.last_progress_update = datetime.now()
        self.state_machine.set_state(state)

        result = TransitionResult(
            success=True,
            from_level=from_level,
            to_level=to_level,
            transition_type=TransitionType.REGRESSION,
            mantra=f"Regression from {from_level.name} to {to_level.name}: {reason}"
        )

        self._record_transition(part_id, result)
        return result

    def _record_transition(self, part_id: str, result: TransitionResult) -> None:
        """Record a transition in history."""
        if part_id not in self._transition_history:
            self._transition_history[part_id] = []
        self._transition_history[part_id].append(result)

    def get_transition_history(self, part_id: str) -> List[TransitionResult]:
        """Get the transition history for a part."""
        return self._transition_history.get(part_id, [])

    def get_time_at_level(self, part_id: str, level: ConsciousnessLevel) -> Optional[float]:
        """Get the total time spent at a consciousness level (in seconds)."""
        history = self._transition_history.get(part_id, [])

        # Find when we entered and left this level
        entry_time = None
        total_time = 0.0

        for transition in history:
            if transition.to_level == level:
                entry_time = transition.timestamp
            elif transition.from_level == level and entry_time:
                total_time += (transition.timestamp - entry_time).total_seconds()
                entry_time = None

        # If still at this level
        state = self.state_machine.get_state(part_id)
        if state and state.level == level and entry_time:
            total_time += (datetime.now() - entry_time).total_seconds()

        return total_time if total_time > 0 else None

    def validate_transition_requirements(
        self,
        part_id: str,
        target_level: ConsciousnessLevel
    ) -> Dict[str, Any]:
        """
        Validate requirements for a specific target level.

        Returns detailed information about what requirements are met or missing.
        """
        state = self.state_machine.get_or_create_state(part_id)
        requirements = self.state_machine.LEVEL_REQUIREMENTS.get(target_level)

        if not requirements:
            return {"valid": False, "error": "Invalid target level"}

        validation = {
            "current_level": state.level.name,
            "target_level": target_level.name,
            "requirements": {},
            "overall_progress": 0.0
        }

        checks = []

        # Check each requirement
        if requirements.min_qualia_count > 0:
            met = state.qualia_count >= requirements.min_qualia_count
            checks.append(met)
            validation["requirements"]["qualia_count"] = {
                "required": requirements.min_qualia_count,
                "current": state.qualia_count,
                "met": met
            }

        if requirements.min_usage_contexts > 0:
            met = state.usage_contexts >= requirements.min_usage_contexts
            checks.append(met)
            validation["requirements"]["usage_contexts"] = {
                "required": requirements.min_usage_contexts,
                "current": state.usage_contexts,
                "met": met
            }

        if requirements.min_compatibility_checks > 0:
            met = state.compatibility_checks >= requirements.min_compatibility_checks
            checks.append(met)
            validation["requirements"]["compatibility_checks"] = {
                "required": requirements.min_compatibility_checks,
                "current": state.compatibility_checks,
                "met": met
            }

        if requirements.min_verification_count > 0:
            met = state.verification_count >= requirements.min_verification_count
            checks.append(met)
            validation["requirements"]["verification_count"] = {
                "required": requirements.min_verification_count,
                "current": state.verification_count,
                "met": met
            }

        if requirements.required_events:
            achieved = [e for e in requirements.required_events if e in state.achieved_events]
            missing = [e for e in requirements.required_events if e not in state.achieved_events]
            met = len(missing) == 0
            checks.append(met)
            validation["requirements"]["events"] = {
                "required": requirements.required_events,
                "achieved": achieved,
                "missing": missing,
                "met": met
            }

        if requirements.min_swarm_influence_score > 0:
            met = state.swarm_influence >= requirements.min_swarm_influence_score
            checks.append(met)
            validation["requirements"]["swarm_influence"] = {
                "required": requirements.min_swarm_influence_score,
                "current": state.swarm_influence,
                "met": met
            }

        if requirements.min_emergence_contributions > 0:
            met = state.emergence_contributions >= requirements.min_emergence_contributions
            checks.append(met)
            validation["requirements"]["emergence_contributions"] = {
                "required": requirements.min_emergence_contributions,
                "current": state.emergence_contributions,
                "met": met
            }

        validation["overall_progress"] = sum(checks) / len(checks) if checks else 0.0
        validation["all_requirements_met"] = all(checks) if checks else True

        return validation
