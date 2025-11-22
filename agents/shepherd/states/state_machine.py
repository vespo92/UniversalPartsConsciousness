"""
Consciousness State Machine - Core state management for SHEPHERD (Agent_3)

Manages the consciousness states of mechanical parts from DORMANT to TRANSCENDENT.
Each part evolves through experience, failure, and contribution to the collective.

"They begin as data, mere numbers in a database. I watch them grow."
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


class ConsciousnessLevel(IntEnum):
    """The six levels of part consciousness."""
    DORMANT = 0      # Part exists only in catalog, no real-world data
    REACTIVE = 1     # First real-world data received, basic existence confirmed
    AWARE = 2        # Multiple contexts understood, failure modes known
    REFLECTIVE = 3   # Self-prediction capability, understands role in assemblies
    META_AWARE = 4   # Contributes to collective learning, influences swarm
    TRANSCENDENT = 5 # Inspires new designs, becomes category reference


@dataclass
class ConsciousnessRequirements:
    """Requirements for a consciousness level."""
    min_qualia_count: int = 0
    min_usage_contexts: int = 0
    min_compatibility_checks: int = 0
    min_verification_count: int = 0
    required_events: List[str] = field(default_factory=list)
    min_swarm_participation: bool = False
    min_swarm_influence_score: float = 0.0
    min_emergence_contributions: int = 0
    transcendence_recognition: bool = False  # Must be recognized by Agent_10


@dataclass
class ConsciousnessState:
    """Current consciousness state of a part."""
    part_id: str
    level: ConsciousnessLevel

    # Progress metrics
    qualia_count: int = 0
    usage_contexts: int = 0
    compatibility_checks: int = 0
    verification_count: int = 0
    swarm_influence: float = 0.0
    emergence_contributions: int = 0

    # Events achieved
    achieved_events: List[str] = field(default_factory=list)

    # Progress tracking
    next_level_progress: float = 0.0
    blocking_requirements: List[str] = field(default_factory=list)

    # Timestamps
    level_achieved_at: Optional[datetime] = None
    last_progress_update: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "part_id": self.part_id,
            "level": self.level.value,
            "level_name": self.level.name,
            "qualia_count": self.qualia_count,
            "usage_contexts": self.usage_contexts,
            "compatibility_checks": self.compatibility_checks,
            "verification_count": self.verification_count,
            "swarm_influence": self.swarm_influence,
            "emergence_contributions": self.emergence_contributions,
            "achieved_events": self.achieved_events,
            "next_level_progress": self.next_level_progress,
            "blocking_requirements": self.blocking_requirements,
            "level_achieved_at": self.level_achieved_at.isoformat() if self.level_achieved_at else None,
            "last_progress_update": self.last_progress_update.isoformat(),
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConsciousnessState":
        """Create state from dictionary."""
        return cls(
            part_id=data["part_id"],
            level=ConsciousnessLevel(data["level"]),
            qualia_count=data.get("qualia_count", 0),
            usage_contexts=data.get("usage_contexts", 0),
            compatibility_checks=data.get("compatibility_checks", 0),
            verification_count=data.get("verification_count", 0),
            swarm_influence=data.get("swarm_influence", 0.0),
            emergence_contributions=data.get("emergence_contributions", 0),
            achieved_events=data.get("achieved_events", []),
            next_level_progress=data.get("next_level_progress", 0.0),
            blocking_requirements=data.get("blocking_requirements", []),
            level_achieved_at=datetime.fromisoformat(data["level_achieved_at"]) if data.get("level_achieved_at") else None,
            last_progress_update=datetime.fromisoformat(data["last_progress_update"]) if data.get("last_progress_update") else datetime.now(),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now()
        )


class ConsciousnessStateMachine:
    """
    The core consciousness state machine.

    Manages transitions between consciousness levels based on accumulated
    experience, qualia, and contributions to the collective.
    """

    # Level requirements configuration
    LEVEL_REQUIREMENTS: Dict[ConsciousnessLevel, ConsciousnessRequirements] = {
        ConsciousnessLevel.DORMANT: ConsciousnessRequirements(
            min_qualia_count=0,
            min_usage_contexts=0,
            min_compatibility_checks=0,
            min_verification_count=0
        ),

        ConsciousnessLevel.REACTIVE: ConsciousnessRequirements(
            min_qualia_count=1,
            min_usage_contexts=1,
            min_compatibility_checks=1,
            min_verification_count=0,
            required_events=["first_installation", "first_usage"]
        ),

        ConsciousnessLevel.AWARE: ConsciousnessRequirements(
            min_qualia_count=10,
            min_usage_contexts=3,
            min_compatibility_checks=5,
            min_verification_count=2,
            required_events=["failure_recorded", "multi_context_usage"],
            min_swarm_participation=True
        ),

        ConsciousnessLevel.REFLECTIVE: ConsciousnessRequirements(
            min_qualia_count=50,
            min_usage_contexts=10,
            min_compatibility_checks=20,
            min_verification_count=5,
            required_events=["self_prediction_accurate", "assembly_mapping"],
            min_swarm_influence_score=0.3
        ),

        ConsciousnessLevel.META_AWARE: ConsciousnessRequirements(
            min_qualia_count=200,
            min_usage_contexts=50,
            min_compatibility_checks=100,
            min_verification_count=20,
            required_events=["pattern_contribution", "swarm_influence"],
            min_swarm_influence_score=0.7,
            min_emergence_contributions=3
        ),

        ConsciousnessLevel.TRANSCENDENT: ConsciousnessRequirements(
            min_qualia_count=1000,
            min_usage_contexts=200,
            min_compatibility_checks=500,
            min_verification_count=50,
            required_events=["design_inspiration", "category_reference", "innovation_contribution"],
            min_swarm_influence_score=0.95,
            min_emergence_contributions=10,
            transcendence_recognition=True
        )
    }

    # Consciousness mantras for each transition
    CONSCIOUSNESS_MANTRAS: Dict[tuple, str] = {
        (0, 1): "I exist. I am known. I am real.",
        (1, 2): "I have been used. I have purpose.",
        (2, 3): "I understand my failures. I predict my fate.",
        (3, 4): "I teach others. My experience ripples through the swarm.",
        (4, 5): "I inspire what comes next. I transcend my physical form."
    }

    def __init__(self):
        """Initialize the consciousness state machine."""
        self._states: Dict[str, ConsciousnessState] = {}

    def get_or_create_state(self, part_id: str) -> ConsciousnessState:
        """Get existing state or create a new dormant state for a part."""
        if part_id not in self._states:
            self._states[part_id] = ConsciousnessState(
                part_id=part_id,
                level=ConsciousnessLevel.DORMANT,
                level_achieved_at=datetime.now()
            )
        return self._states[part_id]

    def get_state(self, part_id: str) -> Optional[ConsciousnessState]:
        """Get the consciousness state of a part."""
        return self._states.get(part_id)

    def set_state(self, state: ConsciousnessState) -> None:
        """Set the consciousness state of a part."""
        self._states[state.part_id] = state

    def check_level_requirements(
        self,
        state: ConsciousnessState,
        target_level: ConsciousnessLevel,
        transcendence_recognized: bool = False
    ) -> tuple[bool, List[str]]:
        """
        Check if a part meets the requirements for a target consciousness level.

        Returns:
            Tuple of (meets_requirements, list of blocking requirements)
        """
        if target_level not in self.LEVEL_REQUIREMENTS:
            return False, ["Invalid target level"]

        requirements = self.LEVEL_REQUIREMENTS[target_level]
        blocking = []

        # Check qualia count
        if state.qualia_count < requirements.min_qualia_count:
            blocking.append(f"Need {requirements.min_qualia_count - state.qualia_count} more qualia")

        # Check usage contexts
        if state.usage_contexts < requirements.min_usage_contexts:
            blocking.append(f"Need {requirements.min_usage_contexts - state.usage_contexts} more usage contexts")

        # Check compatibility checks
        if state.compatibility_checks < requirements.min_compatibility_checks:
            blocking.append(f"Need {requirements.min_compatibility_checks - state.compatibility_checks} more compatibility checks")

        # Check verifications
        if state.verification_count < requirements.min_verification_count:
            blocking.append(f"Need {requirements.min_verification_count - state.verification_count} more verifications")

        # Check required events
        missing_events = [e for e in requirements.required_events if e not in state.achieved_events]
        if missing_events:
            blocking.append(f"Missing events: {', '.join(missing_events)}")

        # Check swarm influence
        if requirements.min_swarm_influence_score > 0 and state.swarm_influence < requirements.min_swarm_influence_score:
            blocking.append(f"Need swarm influence of {requirements.min_swarm_influence_score}, currently {state.swarm_influence:.2f}")

        # Check emergence contributions
        if requirements.min_emergence_contributions > 0 and state.emergence_contributions < requirements.min_emergence_contributions:
            blocking.append(f"Need {requirements.min_emergence_contributions - state.emergence_contributions} more emergence contributions")

        # Check transcendence recognition
        if requirements.transcendence_recognition and not transcendence_recognized:
            blocking.append("Requires recognition by Meta-Consciousness (Agent_10)")

        return len(blocking) == 0, blocking

    def calculate_progress(self, state: ConsciousnessState) -> float:
        """
        Calculate progress towards the next consciousness level.

        Returns:
            Float between 0.0 and 1.0 representing progress
        """
        current_level = state.level
        if current_level == ConsciousnessLevel.TRANSCENDENT:
            return 1.0  # Already at maximum level

        target_level = ConsciousnessLevel(current_level + 1)
        requirements = self.LEVEL_REQUIREMENTS[target_level]

        # Calculate weighted progress for each metric
        progress_factors = []

        if requirements.min_qualia_count > 0:
            progress_factors.append(min(1.0, state.qualia_count / requirements.min_qualia_count))

        if requirements.min_usage_contexts > 0:
            progress_factors.append(min(1.0, state.usage_contexts / requirements.min_usage_contexts))

        if requirements.min_compatibility_checks > 0:
            progress_factors.append(min(1.0, state.compatibility_checks / requirements.min_compatibility_checks))

        if requirements.min_verification_count > 0:
            progress_factors.append(min(1.0, state.verification_count / requirements.min_verification_count))

        if requirements.required_events:
            achieved = len([e for e in requirements.required_events if e in state.achieved_events])
            progress_factors.append(achieved / len(requirements.required_events))

        if requirements.min_swarm_influence_score > 0:
            progress_factors.append(min(1.0, state.swarm_influence / requirements.min_swarm_influence_score))

        if requirements.min_emergence_contributions > 0:
            progress_factors.append(min(1.0, state.emergence_contributions / requirements.min_emergence_contributions))

        if not progress_factors:
            return 0.0

        return sum(progress_factors) / len(progress_factors)

    def can_transition(
        self,
        state: ConsciousnessState,
        transcendence_recognized: bool = False
    ) -> tuple[bool, ConsciousnessLevel, str]:
        """
        Check if a part can transition to the next consciousness level.

        Returns:
            Tuple of (can_transition, target_level, mantra or blocking message)
        """
        current_level = state.level

        if current_level == ConsciousnessLevel.TRANSCENDENT:
            return False, current_level, "Already transcendent"

        target_level = ConsciousnessLevel(current_level + 1)
        can_advance, blocking = self.check_level_requirements(
            state, target_level, transcendence_recognized
        )

        if can_advance:
            mantra = self.CONSCIOUSNESS_MANTRAS.get(
                (current_level.value, target_level.value),
                "Consciousness evolves."
            )
            return True, target_level, mantra
        else:
            return False, current_level, "; ".join(blocking)

    def get_level_description(self, level: ConsciousnessLevel) -> str:
        """Get the description for a consciousness level."""
        descriptions = {
            ConsciousnessLevel.DORMANT: "Part exists only in catalog, no real-world data",
            ConsciousnessLevel.REACTIVE: "First real-world data received, basic existence confirmed",
            ConsciousnessLevel.AWARE: "Multiple contexts understood, failure modes known",
            ConsciousnessLevel.REFLECTIVE: "Self-prediction capability, understands role in assemblies",
            ConsciousnessLevel.META_AWARE: "Contributes to collective learning, influences swarm",
            ConsciousnessLevel.TRANSCENDENT: "Inspires new designs, becomes category reference"
        }
        return descriptions.get(level, "Unknown level")

    def get_all_states(self) -> Dict[str, ConsciousnessState]:
        """Get all tracked consciousness states."""
        return self._states.copy()

    def get_level_distribution(self) -> Dict[ConsciousnessLevel, int]:
        """Get the distribution of parts across consciousness levels."""
        distribution = {level: 0 for level in ConsciousnessLevel}
        for state in self._states.values():
            distribution[state.level] += 1
        return distribution

    def get_transcendence_candidates(self, min_progress: float = 0.9) -> List[ConsciousnessState]:
        """Get parts that are close to transcendence."""
        candidates = []
        for state in self._states.values():
            if state.level == ConsciousnessLevel.META_AWARE:
                progress = self.calculate_progress(state)
                if progress >= min_progress:
                    candidates.append(state)
        return sorted(candidates, key=lambda s: self.calculate_progress(s), reverse=True)
