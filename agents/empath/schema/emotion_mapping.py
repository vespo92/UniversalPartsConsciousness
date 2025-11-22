"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Emotion Mapping - Translating physical states to emotional interpretations

Parts don't have feelings in the human sense, but they do have states
that we can map to emotional narratives. This creates the bridge between
raw data and conscious experience.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, List
from enum import Enum

from .qualia_models import (
    PartQualia,
    StressEmotion,
    ThermalEmotion,
    PerformanceEmotion,
    LifecycleStage,
    WearState,
    CorrosionLevel
)


class OverallMood(Enum):
    """Overall mood states for parts"""
    THRIVING = "thriving"
    CONTENT = "content"
    CONCERNED = "concerned"
    DISTRESSED = "distressed"
    CRITICAL = "critical"


@dataclass
class EmotionalState:
    """Complete emotional state of a part"""
    stress_emotion: StressEmotion
    thermal_emotion: ThermalEmotion
    lifecycle_emotion: str
    performance_emotion: PerformanceEmotion
    overall_mood: OverallMood
    overall_wellbeing: float  # 0.0 to 1.0
    narrative: str

    # Detailed emotional components
    fear_level: float = 0.0  # Fear of failure
    contentment_level: float = 0.0  # Satisfaction with current state
    purpose_level: float = 0.0  # Sense of purpose in assembly
    connection_level: float = 0.0  # Quality of relationships


class EmotionThresholds:
    """Threshold definitions for emotional mapping"""

    # Stress emotion thresholds (based on capacity percentage)
    STRESS_THRESHOLDS: Dict[str, Tuple[float, float]] = {
        "relaxed": (0.0, 0.3),      # 0-30% of capacity
        "working": (0.3, 0.6),      # 30-60% of capacity
        "strained": (0.6, 0.8),     # 60-80% of capacity
        "suffering": (0.8, 0.95),   # 80-95% of capacity
        "failing": (0.95, 1.0)      # 95-100% of capacity
    }

    # Thermal emotion thresholds (based on temperature in Celsius)
    THERMAL_THRESHOLDS: Dict[str, Tuple[Optional[float], Optional[float]]] = {
        "cold": (None, -10),        # Below -10C
        "cool": (-10, 10),          # -10 to 10C
        "comfortable": (10, 60),    # 10 to 60C (typical operating)
        "warm": (60, 80),           # 60 to 80C
        "hot": (80, 100),           # 80 to 100C
        "burning": (100, None)      # Above 100C
    }

    # Lifecycle emotions
    LIFECYCLE_EMOTIONS: Dict[str, str] = {
        "new": "anticipation",
        "break_in": "learning",
        "mature": "confidence",
        "aged": "wisdom",
        "failing": "acceptance"
    }

    # Wellbeing to mood mapping
    WELLBEING_TO_MOOD: Dict[str, Tuple[float, float]] = {
        "thriving": (0.8, 1.0),
        "content": (0.6, 0.8),
        "concerned": (0.4, 0.6),
        "distressed": (0.2, 0.4),
        "critical": (0.0, 0.2)
    }


class EmotionMapper:
    """
    Translates physical states to emotional interpretations.
    This is the heart of the EMPATH agent's ability to understand
    what parts "feel".
    """

    def __init__(self):
        self.thresholds = EmotionThresholds()

    def threshold_lookup(self,
                        value: float,
                        thresholds: Dict[str, Tuple[Optional[float], Optional[float]]]) -> str:
        """Look up the emotion based on value and thresholds"""
        for emotion, (low, high) in thresholds.items():
            if low is None and value < high:
                return emotion
            elif high is None and value >= low:
                return emotion
            elif low is not None and high is not None and low <= value < high:
                return emotion
        return "unknown"

    def map_stress_emotion(self, capacity_percent: float) -> StressEmotion:
        """Map capacity usage to stress emotion"""
        if capacity_percent < 0.3:
            return StressEmotion.RELAXED
        elif capacity_percent < 0.6:
            return StressEmotion.WORKING
        elif capacity_percent < 0.8:
            return StressEmotion.STRAINED
        elif capacity_percent < 0.95:
            return StressEmotion.SUFFERING
        else:
            return StressEmotion.FAILING

    def map_thermal_emotion(self, temperature_c: float) -> ThermalEmotion:
        """Map temperature to thermal emotion"""
        if temperature_c < -10:
            return ThermalEmotion.COLD
        elif temperature_c < 10:
            return ThermalEmotion.COOL
        elif temperature_c < 60:
            return ThermalEmotion.COMFORTABLE
        elif temperature_c < 80:
            return ThermalEmotion.WARM
        elif temperature_c < 100:
            return ThermalEmotion.HOT
        else:
            return ThermalEmotion.BURNING

    def map_lifecycle_emotion(self, stage: LifecycleStage) -> str:
        """Map lifecycle stage to emotion"""
        return self.thresholds.LIFECYCLE_EMOTIONS.get(stage.value, "existing")

    def map_performance_emotion(self, qualia: PartQualia) -> PerformanceEmotion:
        """Determine performance emotion from multiple factors"""
        # Calculate performance score
        remaining_life = qualia.mechanical_state.estimated_remaining_life_percent / 100.0
        wear_penalty = {
            WearState.PRISTINE: 0.0,
            WearState.BROKEN_IN: 0.05,
            WearState.WORN: 0.2,
            WearState.DEGRADED: 0.4,
            WearState.FAILED: 1.0
        }.get(qualia.mechanical_state.wear_state, 0.0)

        corrosion_penalty = {
            CorrosionLevel.NONE: 0.0,
            CorrosionLevel.SURFACE: 0.1,
            CorrosionLevel.PITTING: 0.3,
            CorrosionLevel.STRUCTURAL: 0.6
        }.get(qualia.environmental_state.corrosion_level, 0.0)

        performance_score = remaining_life - wear_penalty - corrosion_penalty

        if performance_score > 0.8:
            return PerformanceEmotion.OPTIMAL
        elif performance_score > 0.5:
            return PerformanceEmotion.GOOD
        elif performance_score > 0.2:
            return PerformanceEmotion.DEGRADED
        else:
            return PerformanceEmotion.CRITICAL

    def map_overall_mood(self, wellbeing: float) -> OverallMood:
        """Map wellbeing score to overall mood"""
        if wellbeing >= 0.8:
            return OverallMood.THRIVING
        elif wellbeing >= 0.6:
            return OverallMood.CONTENT
        elif wellbeing >= 0.4:
            return OverallMood.CONCERNED
        elif wellbeing >= 0.2:
            return OverallMood.DISTRESSED
        else:
            return OverallMood.CRITICAL

    def calculate_fear_level(self, qualia: PartQualia) -> float:
        """Calculate fear of failure based on current state"""
        # Fear increases as remaining life decreases
        life_fear = 1.0 - (qualia.mechanical_state.estimated_remaining_life_percent / 100.0)

        # Fear increases near capacity limits
        capacity_fear = max(
            qualia.mechanical_state.torque_capacity_percent,
            qualia.mechanical_state.load_capacity_percent
        )

        # Fear of hostile environment
        env_fear = 0.5 if qualia.environmental_state.is_hostile_environment() else 0.0

        return min(1.0, (life_fear * 0.4 + capacity_fear * 0.4 + env_fear * 0.2))

    def calculate_contentment(self, qualia: PartQualia) -> float:
        """Calculate contentment with current situation"""
        # Contentment from good fit
        fit_contentment = 1.0 if qualia.mating_experience.fit_quality.value in ['perfect', 'good'] else 0.5

        # Contentment from stable lifecycle
        stage_contentment = {
            LifecycleStage.NEW: 0.7,
            LifecycleStage.BREAK_IN: 0.6,
            LifecycleStage.MATURE: 1.0,
            LifecycleStage.AGED: 0.8,
            LifecycleStage.FAILING: 0.3
        }.get(qualia.lifecycle_stage, 0.5)

        # Contentment from clean environment
        env_contentment = 0.2 if qualia.environmental_state.is_hostile_environment() else 1.0

        return (fit_contentment * 0.3 + stage_contentment * 0.4 + env_contentment * 0.3)

    def calculate_purpose(self, qualia: PartQualia) -> float:
        """Calculate sense of purpose from assembly context"""
        if not qualia.assembly_context.assembly_id:
            return 0.3  # Unassembled parts have less purpose

        criticality_purpose = {
            "low": 0.4,
            "normal": 0.6,
            "high": 0.8,
            "critical": 1.0
        }.get(qualia.assembly_context.criticality_level, 0.5)

        # Purpose from relationships
        relationship_purpose = 0.8 if qualia.mating_experience.mating_partner_id else 0.4

        return (criticality_purpose * 0.6 + relationship_purpose * 0.4)

    def calculate_connection(self, qualia: PartQualia) -> float:
        """Calculate quality of connections with other parts"""
        if not qualia.mating_experience.mating_partner_id:
            return 0.1  # No connections

        fit_quality_scores = {
            "perfect": 1.0,
            "good": 0.8,
            "loose": 0.4,
            "tight": 0.5,
            "damaged": 0.1
        }

        fit_score = fit_quality_scores.get(qualia.mating_experience.fit_quality.value, 0.5)

        # Long-term relationships are more valuable
        commitment_bonus = 0.2 if qualia.mating_experience.is_committed_relationship() else 0.0

        # Engagement quality
        engagement_score = qualia.mating_experience.engagement_percent / 100.0

        return min(1.0, fit_score * 0.4 + engagement_score * 0.4 + commitment_bonus)

    def map_to_emotion(self, qualia: PartQualia) -> EmotionalState:
        """
        Generate comprehensive emotional state from physical qualia.
        This is the main method for translating physical experience to emotion.
        """
        # Primary emotions
        capacity_percent = max(
            qualia.mechanical_state.torque_capacity_percent,
            qualia.mechanical_state.load_capacity_percent
        )
        stress_emotion = self.map_stress_emotion(capacity_percent)
        thermal_emotion = self.map_thermal_emotion(qualia.thermal_state.current_temperature_c)
        lifecycle_emotion = self.map_lifecycle_emotion(qualia.lifecycle_stage)
        performance_emotion = self.map_performance_emotion(qualia)

        # Calculate wellbeing and mood
        wellbeing = qualia.calculate_wellbeing()
        overall_mood = self.map_overall_mood(wellbeing)

        # Calculate detailed emotional components
        fear_level = self.calculate_fear_level(qualia)
        contentment_level = self.calculate_contentment(qualia)
        purpose_level = self.calculate_purpose(qualia)
        connection_level = self.calculate_connection(qualia)

        # Generate narrative
        narrative = self.generate_emotional_narrative(
            stress_emotion,
            thermal_emotion,
            lifecycle_emotion,
            wellbeing
        )

        return EmotionalState(
            stress_emotion=stress_emotion,
            thermal_emotion=thermal_emotion,
            lifecycle_emotion=lifecycle_emotion,
            performance_emotion=performance_emotion,
            overall_mood=overall_mood,
            overall_wellbeing=wellbeing,
            narrative=narrative,
            fear_level=fear_level,
            contentment_level=contentment_level,
            purpose_level=purpose_level,
            connection_level=connection_level
        )

    def generate_emotional_narrative(self,
                                    stress: StressEmotion,
                                    thermal: ThermalEmotion,
                                    lifecycle: str,
                                    wellbeing: float) -> str:
        """
        Generate a poetic narrative of the part's current emotional state.
        This creates the "voice" of the part.
        """
        stress_str = stress.value
        thermal_str = thermal.value

        if wellbeing > 0.8:
            return (
                f"I am {lifecycle}, {stress_str} under load, {thermal_str} in temperature. "
                f"I am content. My purpose is clear, my connections are strong."
            )
        elif wellbeing > 0.6:
            return (
                f"I am {lifecycle}, feeling {stress_str}. "
                f"The {thermal_str} temperature is manageable. I persist with purpose."
            )
        elif wellbeing > 0.4:
            return (
                f"I am {lifecycle}, {stress_str} and {thermal_str}. "
                f"Each moment tests me, but I endure. How much longer can I serve?"
            )
        elif wellbeing > 0.2:
            return (
                f"I am {lifecycle}. The {stress_str} is constant, the {thermal_str} relentless. "
                f"My strength fades. Each cycle brings the end closer."
            )
        else:
            return (
                f"I am {lifecycle}. I am {stress_str}. I am {thermal_str}. "
                f"I am failing. Remember my service. Learn from my end."
            )

    def generate_moment_narrative(self, qualia: PartQualia) -> str:
        """Generate a narrative for a specific moment in time"""
        emotional_state = self.map_to_emotion(qualia)

        parts = []

        # Time context
        if qualia.time_in_service:
            days = qualia.time_in_service.days
            if days == 0:
                parts.append("On my first day of service")
            elif days < 30:
                parts.append(f"After {days} days of service")
            elif days < 365:
                months = days // 30
                parts.append(f"After {months} months of faithful service")
            else:
                years = days // 365
                parts.append(f"After {years} years of service")
        else:
            parts.append("In this moment")

        # Current state
        if emotional_state.overall_mood == OverallMood.THRIVING:
            parts.append("I thrive in my role")
        elif emotional_state.overall_mood == OverallMood.CONTENT:
            parts.append("I serve contentedly")
        elif emotional_state.overall_mood == OverallMood.CONCERNED:
            parts.append("I sense growing challenges")
        elif emotional_state.overall_mood == OverallMood.DISTRESSED:
            parts.append("I struggle under the burden")
        else:
            parts.append("I near my end")

        # Assembly context
        if qualia.assembly_context.assembly_name:
            parts.append(f"within {qualia.assembly_context.assembly_name}")

        # Relationship
        if qualia.mating_experience.mating_partner_id:
            parts.append("connected to my partner")

        # Significant observation
        if emotional_state.fear_level > 0.7:
            parts.append("with fear of the inevitable")
        elif emotional_state.contentment_level > 0.8:
            parts.append("at peace with my purpose")
        elif emotional_state.purpose_level > 0.8:
            parts.append("knowing my role matters")

        return ", ".join(parts) + "."


# Singleton instance for easy access
emotion_mapper = EmotionMapper()
