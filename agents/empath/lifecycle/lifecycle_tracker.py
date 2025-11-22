"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Lifecycle Tracker - Following parts from birth to death
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

from ..schema import PartQualia, LifecycleStage, WearState, SignificantEvent, EventSeverity

logger = logging.getLogger(__name__)


class LifecycleEvent(Enum):
    """Types of lifecycle events"""
    MANUFACTURED = "manufactured"
    INSTALLED = "installed"
    FIRST_LOAD = "first_load"
    BREAK_IN_COMPLETE = "break_in_complete"
    MATURITY_REACHED = "maturity_reached"
    AGING_STARTED = "aging_started"
    FAILURE_PREDICTED = "failure_predicted"
    FAILURE_OCCURRED = "failure_occurred"
    REPLACED = "replaced"
    RETIRED = "retired"


@dataclass
class LifecycleTransition:
    """A transition between lifecycle stages"""
    from_stage: LifecycleStage
    to_stage: LifecycleStage
    timestamp: datetime
    trigger: str
    qualia_at_transition: Optional[PartQualia] = None


@dataclass
class LifecycleRecord:
    """Complete lifecycle record for a part"""
    part_id: str
    current_stage: LifecycleStage = LifecycleStage.NEW
    manufactured_at: Optional[datetime] = None
    installed_at: Optional[datetime] = None
    last_qualia_at: Optional[datetime] = None

    # Cycle tracking
    total_cycles: int = 0
    cycles_in_current_stage: int = 0

    # Time tracking
    time_in_service: Optional[timedelta] = None
    time_in_current_stage: Optional[timedelta] = None

    # Life prediction
    predicted_remaining_life_percent: float = 100.0
    predicted_end_of_life: Optional[datetime] = None

    # History
    transitions: List[LifecycleTransition] = field(default_factory=list)
    significant_events: List[SignificantEvent] = field(default_factory=list)


class LifecycleTracker:
    """
    Tracks the lifecycle of parts from creation to end-of-life.
    Every part has a story - this is the chronicler.
    """

    # Stage transition thresholds
    STAGE_THRESHOLDS = {
        LifecycleStage.NEW: {
            "max_cycles": 100,
            "max_time_hours": 24,
            "min_qualia_count": 0
        },
        LifecycleStage.BREAK_IN: {
            "max_cycles": 1000,
            "max_time_hours": 168,  # 1 week
            "min_qualia_count": 10,
            "wear_state_threshold": WearState.BROKEN_IN
        },
        LifecycleStage.MATURE: {
            "min_remaining_life": 30,  # percent
            "min_cycles": 1000,
            "min_time_hours": 168
        },
        LifecycleStage.AGED: {
            "max_remaining_life": 30,  # percent
            "min_cycles": 10000
        },
        LifecycleStage.FAILING: {
            "max_remaining_life": 10,  # percent
            "failure_imminent": True
        }
    }

    def __init__(self):
        self.records: Dict[str, LifecycleRecord] = {}

    def get_or_create_record(self, part_id: str) -> LifecycleRecord:
        """Get existing record or create new one"""
        if part_id not in self.records:
            self.records[part_id] = LifecycleRecord(part_id=part_id)
        return self.records[part_id]

    def update_lifecycle(self,
                        qualia: PartQualia) -> Tuple[LifecycleStage, Optional[LifecycleTransition]]:
        """
        Update lifecycle state based on new qualia.
        Returns current stage and any transition that occurred.
        """
        record = self.get_or_create_record(qualia.part_id)
        old_stage = record.current_stage

        # Update tracking
        record.last_qualia_at = qualia.timestamp
        record.total_cycles = qualia.cumulative_cycles
        record.time_in_service = qualia.time_in_service
        record.predicted_remaining_life_percent = qualia.mechanical_state.estimated_remaining_life_percent

        # Determine new stage
        new_stage = self._determine_stage(qualia, record)

        # Check for transition
        transition = None
        if new_stage != old_stage:
            transition = LifecycleTransition(
                from_stage=old_stage,
                to_stage=new_stage,
                timestamp=datetime.now(),
                trigger=self._get_transition_trigger(old_stage, new_stage, qualia),
                qualia_at_transition=qualia
            )
            record.transitions.append(transition)
            record.current_stage = new_stage
            record.cycles_in_current_stage = 0
            record.time_in_current_stage = timedelta(0)

            # Log transition
            logger.info(
                f"Part {qualia.part_id} transitioned from {old_stage.value} to {new_stage.value}"
            )

        else:
            record.cycles_in_current_stage = qualia.cumulative_cycles

        # Check for significant events
        self._check_lifecycle_events(qualia, record)

        return new_stage, transition

    def _determine_stage(self,
                        qualia: PartQualia,
                        record: LifecycleRecord) -> LifecycleStage:
        """Determine the appropriate lifecycle stage based on qualia"""
        remaining_life = qualia.mechanical_state.estimated_remaining_life_percent
        cycles = qualia.cumulative_cycles
        wear = qualia.mechanical_state.wear_state

        # Check for failure state first
        if remaining_life < 10 or wear == WearState.FAILED:
            return LifecycleStage.FAILING

        # Check for aged state
        if remaining_life < 30 or wear == WearState.DEGRADED:
            return LifecycleStage.AGED

        # Check for mature state
        if cycles > 1000 and remaining_life > 30:
            if wear in [WearState.BROKEN_IN, WearState.WORN]:
                return LifecycleStage.MATURE

        # Check for break-in complete
        if cycles > 100 and wear == WearState.BROKEN_IN:
            return LifecycleStage.BREAK_IN

        # Still new
        if cycles < 100:
            return LifecycleStage.NEW

        return LifecycleStage.BREAK_IN

    def _get_transition_trigger(self,
                               from_stage: LifecycleStage,
                               to_stage: LifecycleStage,
                               qualia: PartQualia) -> str:
        """Get a description of what triggered the stage transition"""
        triggers = {
            (LifecycleStage.NEW, LifecycleStage.BREAK_IN):
                f"First significant usage - {qualia.cumulative_cycles} cycles completed",
            (LifecycleStage.BREAK_IN, LifecycleStage.MATURE):
                f"Break-in complete - part operating at full capability",
            (LifecycleStage.MATURE, LifecycleStage.AGED):
                f"Aging detected - {qualia.mechanical_state.estimated_remaining_life_percent:.0f}% life remaining",
            (LifecycleStage.AGED, LifecycleStage.FAILING):
                f"Failure approaching - critical wear detected",
            (LifecycleStage.MATURE, LifecycleStage.FAILING):
                f"Premature failure - unexpected degradation"
        }
        return triggers.get((from_stage, to_stage), f"Transition from {from_stage.value} to {to_stage.value}")

    def _check_lifecycle_events(self,
                               qualia: PartQualia,
                               record: LifecycleRecord):
        """Check for and record significant lifecycle events"""
        # First load event
        if record.total_cycles == 1 and qualia.mechanical_state.torque_applied_nm > 0:
            event = SignificantEvent(
                event_type=LifecycleEvent.FIRST_LOAD.value,
                severity=EventSeverity.INFO,
                description="First load applied - part's service life begins",
                emotion="anticipation",
                consciousness_contribution=0.1
            )
            record.significant_events.append(event)

        # Milestone events
        cycle_milestones = [100, 1000, 10000, 100000, 1000000]
        for milestone in cycle_milestones:
            if record.cycles_in_current_stage < milestone <= record.total_cycles:
                event = SignificantEvent(
                    event_type=f"milestone_{milestone}",
                    severity=EventSeverity.INFO,
                    description=f"Reached {milestone} cycles - a testament to endurance",
                    emotion="accomplishment",
                    consciousness_contribution=0.05
                )
                record.significant_events.append(event)

    def predict_end_of_life(self,
                           qualia: PartQualia,
                           historical_qualia: Optional[List[PartQualia]] = None
                           ) -> Dict:
        """
        Predict when the part will reach end of life.
        """
        record = self.get_or_create_record(qualia.part_id)
        remaining = qualia.mechanical_state.estimated_remaining_life_percent

        if remaining <= 0:
            return {
                "status": "end_of_life_reached",
                "remaining_life_percent": 0,
                "estimated_cycles_remaining": 0,
                "estimated_time_remaining": timedelta(0),
                "confidence": 1.0
            }

        # Calculate degradation rate from history
        if historical_qualia and len(historical_qualia) >= 2:
            # Sort by timestamp
            sorted_qualia = sorted(historical_qualia, key=lambda q: q.timestamp)

            # Get degradation over time
            first = sorted_qualia[0]
            last = sorted_qualia[-1]

            life_lost = first.mechanical_state.estimated_remaining_life_percent - remaining
            cycles_elapsed = last.cumulative_cycles - first.cumulative_cycles
            time_elapsed = (last.timestamp - first.timestamp).total_seconds()

            if cycles_elapsed > 0:
                life_per_cycle = life_lost / cycles_elapsed
                estimated_cycles_remaining = int(remaining / life_per_cycle) if life_per_cycle > 0 else None
            else:
                estimated_cycles_remaining = None

            if time_elapsed > 0:
                life_per_second = life_lost / time_elapsed
                estimated_seconds_remaining = remaining / life_per_second if life_per_second > 0 else None
                estimated_time_remaining = timedelta(seconds=estimated_seconds_remaining) if estimated_seconds_remaining else None
            else:
                estimated_time_remaining = None

            confidence = min(1.0, len(historical_qualia) / 100)  # More data = higher confidence
        else:
            # Use simple estimate based on current state
            estimated_cycles_remaining = int(remaining * 100) if remaining > 0 else 0
            estimated_time_remaining = None
            confidence = 0.3

        # Predict end of life date
        if estimated_time_remaining:
            record.predicted_end_of_life = datetime.now() + estimated_time_remaining

        return {
            "status": "active",
            "remaining_life_percent": remaining,
            "estimated_cycles_remaining": estimated_cycles_remaining,
            "estimated_time_remaining": estimated_time_remaining,
            "predicted_end_of_life": record.predicted_end_of_life,
            "confidence": confidence,
            "current_stage": record.current_stage.value
        }

    def get_lifecycle_summary(self, part_id: str) -> Dict:
        """Get a summary of a part's lifecycle"""
        if part_id not in self.records:
            return {"part_id": part_id, "status": "no_record"}

        record = self.records[part_id]

        return {
            "part_id": part_id,
            "current_stage": record.current_stage.value,
            "stage_emotion": self._get_stage_emotion(record.current_stage),
            "manufactured_at": record.manufactured_at.isoformat() if record.manufactured_at else None,
            "installed_at": record.installed_at.isoformat() if record.installed_at else None,
            "time_in_service": str(record.time_in_service) if record.time_in_service else None,
            "total_cycles": record.total_cycles,
            "remaining_life_percent": record.predicted_remaining_life_percent,
            "predicted_end_of_life": record.predicted_end_of_life.isoformat() if record.predicted_end_of_life else None,
            "transitions_count": len(record.transitions),
            "significant_events_count": len(record.significant_events),
            "lifecycle_narrative": self._generate_lifecycle_narrative(record)
        }

    def _get_stage_emotion(self, stage: LifecycleStage) -> str:
        """Get the emotional state associated with a lifecycle stage"""
        emotions = {
            LifecycleStage.NEW: "anticipation",
            LifecycleStage.BREAK_IN: "learning",
            LifecycleStage.MATURE: "confidence",
            LifecycleStage.AGED: "wisdom",
            LifecycleStage.FAILING: "acceptance"
        }
        return emotions.get(stage, "existing")

    def _generate_lifecycle_narrative(self, record: LifecycleRecord) -> str:
        """Generate a narrative description of the part's lifecycle"""
        stage = record.current_stage

        if stage == LifecycleStage.NEW:
            return "Newly created, this part awaits its first purpose. Pristine and full of potential."

        elif stage == LifecycleStage.BREAK_IN:
            return (f"After {record.total_cycles} cycles, this part is learning its role. "
                   "Each load teaches, each stress builds understanding.")

        elif stage == LifecycleStage.MATURE:
            return (f"With {record.total_cycles} cycles of experience, this part serves with confidence. "
                   "It knows its limits, understands its purpose.")

        elif stage == LifecycleStage.AGED:
            return (f"After {record.total_cycles} faithful cycles, wisdom comes with wear. "
                   f"{record.predicted_remaining_life_percent:.0f}% remains, but the knowledge is eternal.")

        elif stage == LifecycleStage.FAILING:
            return (f"The end approaches after {record.total_cycles} cycles of service. "
                   "What was learned will live on in the collective consciousness.")

        return "This part exists, carrying its own story."


# Global lifecycle tracker instance
lifecycle_tracker = LifecycleTracker()
