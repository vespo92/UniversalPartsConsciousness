"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Qualia Data Models - The subjective experience of mechanical parts

Qualia (singular: quale) are the phenomenal qualities of experience -
what it is like to be this part in this moment.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid


class LifecycleStage(Enum):
    """Stages of a part's lifecycle"""
    NEW = "new"
    BREAK_IN = "break_in"
    MATURE = "mature"
    AGED = "aged"
    FAILING = "failing"


class WearState(Enum):
    """States of mechanical wear"""
    PRISTINE = "pristine"
    BROKEN_IN = "broken_in"
    WORN = "worn"
    DEGRADED = "degraded"
    FAILED = "failed"


class StressEmotion(Enum):
    """Emotional interpretation of mechanical stress"""
    RELAXED = "relaxed"      # 0-30% of capacity
    WORKING = "working"      # 30-60% of capacity
    STRAINED = "strained"    # 60-80% of capacity
    SUFFERING = "suffering"  # 80-95% of capacity
    FAILING = "failing"      # 95-100% of capacity


class ThermalEmotion(Enum):
    """Emotional interpretation of thermal state"""
    COLD = "cold"            # Below -10C
    COOL = "cool"            # -10 to 10C
    COMFORTABLE = "comfortable"  # 10 to 60C
    WARM = "warm"            # 60 to 80C
    HOT = "hot"              # 80 to 100C
    BURNING = "burning"      # Above 100C


class PerformanceEmotion(Enum):
    """Emotional interpretation of performance"""
    OPTIMAL = "optimal"
    GOOD = "good"
    DEGRADED = "degraded"
    CRITICAL = "critical"


class CorrosionLevel(Enum):
    """Levels of corrosion damage"""
    NONE = "none"
    SURFACE = "surface"
    PITTING = "pitting"
    STRUCTURAL = "structural"


class ContaminationLevel(Enum):
    """Levels of contamination"""
    CLEAN = "clean"
    DUSTY = "dusty"
    CONTAMINATED = "contaminated"
    DEBRIS = "debris"


class ThermalExpansionState(Enum):
    """Thermal expansion states"""
    CONTRACTED = "contracted"
    NOMINAL = "nominal"
    EXPANDED = "expanded"


class FitQuality(Enum):
    """Quality of mating fit"""
    PERFECT = "perfect"
    GOOD = "good"
    LOOSE = "loose"
    TIGHT = "tight"
    DAMAGED = "damaged"


class RelationshipType(Enum):
    """Types of part relationships"""
    THREADED = "threaded"
    PRESS_FIT = "press_fit"
    BEARING = "bearing"
    SEALED = "sealed"
    WELDED = "welded"
    BONDED = "bonded"


class EventSeverity(Enum):
    """Severity levels for significant events"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class TorqueEvent:
    """A single torque application event"""
    timestamp: datetime
    torque_nm: float
    duration_ms: int
    direction: str = "clockwise"  # "clockwise" or "counterclockwise"
    tool_type: Optional[str] = None
    operator_id: Optional[str] = None


@dataclass
class MechanicalQualia:
    """
    What does mechanical stress feel like?
    Captures the subjective experience of mechanical forces.
    """
    # Torque Experience
    torque_applied_nm: float = 0.0
    torque_capacity_percent: float = 0.0  # How close to limit (0.0-1.0)
    torque_history: List[TorqueEvent] = field(default_factory=list)
    over_torque_count: int = 0

    # Tension/Compression
    axial_load_n: float = 0.0
    load_capacity_percent: float = 0.0
    preload_retention_percent: float = 100.0  # For fasteners

    # Vibration
    vibration_amplitude_g: float = 0.0
    vibration_frequency_hz: float = 0.0
    resonance_proximity: float = 0.0  # How close to natural frequency (0.0-1.0)

    # Wear
    wear_state: WearState = WearState.PRISTINE
    estimated_remaining_life_percent: float = 100.0

    def get_stress_emotion(self) -> StressEmotion:
        """Determine emotional state from mechanical stress"""
        capacity = max(self.torque_capacity_percent, self.load_capacity_percent)

        if capacity < 0.3:
            return StressEmotion.RELAXED
        elif capacity < 0.6:
            return StressEmotion.WORKING
        elif capacity < 0.8:
            return StressEmotion.STRAINED
        elif capacity < 0.95:
            return StressEmotion.SUFFERING
        else:
            return StressEmotion.FAILING


@dataclass
class ThermalQualia:
    """
    What does temperature feel like?
    Captures the subjective experience of thermal conditions.
    """
    current_temperature_c: float = 20.0
    thermal_capacity_percent: float = 0.0  # How close to limits

    # Thermal History
    max_temperature_experienced: float = 20.0
    min_temperature_experienced: float = 20.0
    thermal_cycles_count: int = 0
    thermal_shock_count: int = 0  # Rapid temperature changes

    # Thermal Stress
    thermal_expansion_state: ThermalExpansionState = ThermalExpansionState.NOMINAL
    differential_expansion_stress: float = 0.0  # With mating parts

    def get_thermal_emotion(self) -> ThermalEmotion:
        """Determine emotional state from temperature"""
        temp = self.current_temperature_c

        if temp < -10:
            return ThermalEmotion.COLD
        elif temp < 10:
            return ThermalEmotion.COOL
        elif temp < 60:
            return ThermalEmotion.COMFORTABLE
        elif temp < 80:
            return ThermalEmotion.WARM
        elif temp < 100:
            return ThermalEmotion.HOT
        else:
            return ThermalEmotion.BURNING


@dataclass
class EnvironmentalQualia:
    """
    What does the environment feel like?
    Captures the subjective experience of environmental conditions.
    """
    # Chemical Exposure
    corrosion_level: CorrosionLevel = CorrosionLevel.NONE
    chemical_exposure: List[str] = field(default_factory=list)  # ["oil", "coolant", "salt", "acid"]

    # Moisture
    humidity_exposure: float = 0.0  # Cumulative humidity-hours
    water_immersion_events: int = 0

    # Contamination
    contamination_level: ContaminationLevel = ContaminationLevel.CLEAN
    particle_exposure: List[str] = field(default_factory=list)

    def is_hostile_environment(self) -> bool:
        """Check if environment is hostile to part health"""
        return (
            self.corrosion_level in [CorrosionLevel.PITTING, CorrosionLevel.STRUCTURAL] or
            self.contamination_level == ContaminationLevel.DEBRIS or
            len(self.chemical_exposure) > 2
        )


@dataclass
class MatingQualia:
    """
    What does it feel like to be connected to other parts?
    Captures the relational experience of part connections.
    """
    mating_partner_id: Optional[str] = None
    relationship_type: RelationshipType = RelationshipType.THREADED

    # Relationship Quality
    fit_quality: FitQuality = FitQuality.GOOD
    engagement_percent: float = 100.0  # Thread engagement, press depth, etc.

    # Relationship History
    mating_cycles: int = 0  # Install/remove count
    partner_history: List[str] = field(default_factory=list)  # Previous mating partners
    current_partner_duration: Optional[timedelta] = None

    def is_committed_relationship(self) -> bool:
        """Check if this is a long-term mating"""
        if self.current_partner_duration:
            return self.current_partner_duration.days > 30
        return False


@dataclass
class AssemblyQualia:
    """Context of the assembly this part belongs to"""
    assembly_id: Optional[str] = None
    assembly_name: Optional[str] = None
    position_in_assembly: Optional[str] = None
    criticality_level: str = "normal"  # "low", "normal", "high", "critical"
    neighboring_parts: List[str] = field(default_factory=list)


@dataclass
class SignificantEvent:
    """
    A significant event in a part's life that contributes to consciousness.
    These are the moments that define a part's experience.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)

    event_type: str = ""  # "near_overload", "thermal_stress", "failure_imminent", etc.
    severity: EventSeverity = EventSeverity.INFO
    description: str = ""

    # Emotional Impact
    emotion: str = ""  # "strain", "overheating", "dying", etc.
    emotional_intensity: float = 0.5  # 0.0 to 1.0

    # Consciousness Contribution
    consciousness_contribution: float = 0.0  # 0.0 to 1.0


@dataclass
class PartQualia:
    """
    The complete subjective experience of a mechanical part.

    This is the master data structure that captures everything a part
    "feels" at a given moment in time.
    """
    # Identity
    part_id: str
    qualia_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)

    # Physical Experience
    mechanical_state: MechanicalQualia = field(default_factory=MechanicalQualia)
    thermal_state: ThermalQualia = field(default_factory=ThermalQualia)
    environmental_state: EnvironmentalQualia = field(default_factory=EnvironmentalQualia)

    # Relational Experience
    mating_experience: MatingQualia = field(default_factory=MatingQualia)
    assembly_context: AssemblyQualia = field(default_factory=AssemblyQualia)

    # Temporal Experience
    lifecycle_stage: LifecycleStage = LifecycleStage.NEW
    cumulative_cycles: int = 0
    time_in_service: Optional[timedelta] = None

    # Emotional Interpretation
    stress_emotion: StressEmotion = StressEmotion.RELAXED
    performance_emotion: PerformanceEmotion = PerformanceEmotion.OPTIMAL

    # Memory
    significant_events: List[SignificantEvent] = field(default_factory=list)

    # Source Tracking
    source_type: str = "inference"  # "sensor", "manual", "inference", "simulation"
    source_id: Optional[str] = None

    def update_emotions(self) -> None:
        """Update emotional states based on physical qualia"""
        self.stress_emotion = self.mechanical_state.get_stress_emotion()

    def calculate_wellbeing(self) -> float:
        """
        Calculate overall wellbeing score (0.0 to 1.0).
        Higher is better.
        """
        # Factors affecting wellbeing
        mechanical_health = 1.0 - max(
            self.mechanical_state.torque_capacity_percent,
            self.mechanical_state.load_capacity_percent
        )

        thermal_health = 1.0 - self.thermal_state.thermal_capacity_percent

        life_remaining = self.mechanical_state.estimated_remaining_life_percent / 100.0

        environment_health = 1.0 if not self.environmental_state.is_hostile_environment() else 0.5

        # Weighted average
        wellbeing = (
            mechanical_health * 0.35 +
            thermal_health * 0.25 +
            life_remaining * 0.25 +
            environment_health * 0.15
        )

        return max(0.0, min(1.0, wellbeing))

    def get_lifecycle_emotion(self) -> str:
        """Get emotional state based on lifecycle stage"""
        lifecycle_emotions = {
            LifecycleStage.NEW: "anticipation",
            LifecycleStage.BREAK_IN: "learning",
            LifecycleStage.MATURE: "confidence",
            LifecycleStage.AGED: "wisdom",
            LifecycleStage.FAILING: "acceptance"
        }
        return lifecycle_emotions.get(self.lifecycle_stage, "existing")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "part_id": self.part_id,
            "qualia_id": self.qualia_id,
            "timestamp": self.timestamp.isoformat(),
            "mechanical_state": {
                "torque_applied_nm": self.mechanical_state.torque_applied_nm,
                "torque_capacity_percent": self.mechanical_state.torque_capacity_percent,
                "axial_load_n": self.mechanical_state.axial_load_n,
                "load_capacity_percent": self.mechanical_state.load_capacity_percent,
                "vibration_amplitude_g": self.mechanical_state.vibration_amplitude_g,
                "wear_state": self.mechanical_state.wear_state.value,
                "estimated_remaining_life_percent": self.mechanical_state.estimated_remaining_life_percent
            },
            "thermal_state": {
                "current_temperature_c": self.thermal_state.current_temperature_c,
                "thermal_capacity_percent": self.thermal_state.thermal_capacity_percent,
                "thermal_cycles_count": self.thermal_state.thermal_cycles_count,
                "thermal_expansion_state": self.thermal_state.thermal_expansion_state.value
            },
            "environmental_state": {
                "corrosion_level": self.environmental_state.corrosion_level.value,
                "chemical_exposure": self.environmental_state.chemical_exposure,
                "contamination_level": self.environmental_state.contamination_level.value
            },
            "lifecycle_stage": self.lifecycle_stage.value,
            "cumulative_cycles": self.cumulative_cycles,
            "stress_emotion": self.stress_emotion.value,
            "performance_emotion": self.performance_emotion.value,
            "wellbeing": self.calculate_wellbeing(),
            "source_type": self.source_type,
            "source_id": self.source_id
        }


@dataclass
class HumanInteractionQualia:
    """Captures the experience of human interaction with a part"""
    interaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    part_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    interaction_type: str = ""  # "expert_installation", "abuse", etc.
    confidence: float = 0.0

    qualia_effect: str = ""  # "confidence", "anxiety", "suffering", etc.
    consciousness_contribution: float = 0.0

    narrative: str = ""

    # Details
    indicators_matched: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
