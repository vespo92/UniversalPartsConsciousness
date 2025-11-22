"""
Learning Extractor - Extracts generalizable learnings from individual part experiences.

Transforms raw qualia (subjective experiences) into structured learnings
that can be propagated across swarms.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from ..models import Learning, LearningType


@dataclass
class PartQualia:
    """Representation of a part's subjective experience (from Agent_4)."""
    id: UUID
    part_id: UUID

    # Experience type
    experience_type: str  # "usage", "failure", "maintenance", "storage"

    # Mechanical state
    mechanical_state: dict[str, Any]
    # e.g., {"torque_applied": 45.0, "axial_load_n": 12000, "cycles": 50000,
    #        "torque_capacity_percent": 0.85, "wear_state": "good"}

    # Environmental state
    environmental_state: dict[str, Any]
    # e.g., {"temperature_c": 85, "humidity_percent": 40, "vibration_level": "high",
    #        "corrosive_exposure": False}

    # Lifecycle
    lifecycle_stage: str  # "new", "break_in", "service", "aged", "end_of_life"
    cumulative_cycles: int
    maintenance_history: list[dict[str, Any]]

    # Significant event (if any)
    significant_event: Optional[dict[str, Any]] = None
    # e.g., {"type": "failure", "failure_type": "fatigue_crack", "severity": "critical"}

    # Timestamp
    recorded_at: datetime = None


@dataclass
class SignificantEvent:
    """A notable event in a part's life."""
    event_type: str  # "failure", "overload", "exceptional_performance", "near_miss"
    severity: str  # "minor", "moderate", "significant", "critical"
    failure_type: Optional[str] = None
    description: str = ""
    contributing_factors: list[str] = None


class LearningExtractor:
    """
    Extracts generalizable learnings from individual part experiences.
    """

    # Thresholds for learning extraction
    HIGH_LOAD_THRESHOLD = 0.85  # % of capacity
    LOW_MARGIN_THRESHOLD = 0.1  # Remaining margin
    LONGEVITY_CYCLE_THRESHOLD = 1000000  # 1M cycles
    SURVIVAL_FACTOR = 0.9  # % capacity to count as survival

    def extract_learnings(
        self,
        qualia: PartQualia,
        source_consciousness_level: float = 1.0,
    ) -> list[Learning]:
        """
        Extract all applicable learnings from a qualia record.

        Args:
            qualia: The experience to analyze
            source_consciousness_level: Consciousness level of the source part

        Returns:
            List of extracted learnings
        """
        learnings = []

        # Extract failure learnings
        if qualia.significant_event:
            event = SignificantEvent(
                event_type=qualia.significant_event.get("type", "unknown"),
                severity=qualia.significant_event.get("severity", "unknown"),
                failure_type=qualia.significant_event.get("failure_type"),
                description=qualia.significant_event.get("description", ""),
                contributing_factors=qualia.significant_event.get("factors", []),
            )

            if event.event_type == "failure":
                learning = self._extract_failure_learning(qualia, event)
                if learning:
                    learning.source_consciousness_level = source_consciousness_level
                    learnings.append(learning)

        # Extract survival learning (high load survived)
        survival_learning = self._extract_survival_learning(qualia)
        if survival_learning:
            survival_learning.source_consciousness_level = source_consciousness_level
            learnings.append(survival_learning)

        # Extract longevity learning
        longevity_learning = self._extract_longevity_learning(qualia)
        if longevity_learning:
            longevity_learning.source_consciousness_level = source_consciousness_level
            learnings.append(longevity_learning)

        # Extract environmental adaptation learning
        env_learning = self._extract_environmental_learning(qualia)
        if env_learning:
            env_learning.source_consciousness_level = source_consciousness_level
            learnings.append(env_learning)

        # Extract usage pattern learning
        usage_learning = self._extract_usage_learning(qualia)
        if usage_learning:
            usage_learning.source_consciousness_level = source_consciousness_level
            learnings.append(usage_learning)

        return learnings

    def _extract_failure_learning(
        self,
        qualia: PartQualia,
        event: SignificantEvent,
    ) -> Optional[Learning]:
        """Extract learning from a failure event."""
        if event.event_type != "failure":
            return None

        # Infer prevention measures based on failure type
        prevention = self._infer_prevention(event, qualia)

        content = {
            "failure_type": event.failure_type,
            "severity": event.severity,
            "conditions": {
                "mechanical": qualia.mechanical_state,
                "environmental": qualia.environmental_state,
            },
            "lifecycle_stage": qualia.lifecycle_stage,
            "cycles_at_failure": qualia.cumulative_cycles,
            "prevention_measures": prevention,
            "contributing_factors": event.contributing_factors or [],
        }

        # Higher confidence for more severe failures (more memorable)
        confidence = 0.7 if event.severity in ["minor", "moderate"] else 0.9

        return Learning(
            learning_type=LearningType.FAILURE_MODE,
            content=content,
            confidence=confidence,
            applicability="similar_conditions",
            source_part_id=qualia.part_id,
            source_qualia_id=qualia.id,
        )

    def _extract_survival_learning(
        self,
        qualia: PartQualia,
    ) -> Optional[Learning]:
        """Extract learning from surviving high loads."""
        mechanical = qualia.mechanical_state
        capacity_percent = mechanical.get("torque_capacity_percent", 0)

        if capacity_percent < self.SURVIVAL_FACTOR:
            return None

        content = {
            "load_survived": {
                "axial_load_n": mechanical.get("axial_load_n"),
                "torque_applied": mechanical.get("torque_applied"),
                "capacity_used_percent": capacity_percent,
            },
            "conditions": qualia.environmental_state,
            "margin_remaining": 1 - capacity_percent,
            "wear_state_after": mechanical.get("wear_state", "unknown"),
        }

        return Learning(
            learning_type=LearningType.SURVIVAL_LIMIT,
            content=content,
            confidence=0.8,
            applicability="similar_specs",
            source_part_id=qualia.part_id,
            source_qualia_id=qualia.id,
        )

    def _extract_longevity_learning(
        self,
        qualia: PartQualia,
    ) -> Optional[Learning]:
        """Extract learning from long-lasting parts."""
        if qualia.lifecycle_stage not in ["aged", "end_of_life"]:
            return None

        mechanical = qualia.mechanical_state
        wear_state = mechanical.get("wear_state", "unknown")

        # Only learn from parts that lasted well
        if qualia.cumulative_cycles < self.LONGEVITY_CYCLE_THRESHOLD:
            return None

        if wear_state not in ["good", "acceptable"]:
            return None

        content = {
            "cycles_achieved": qualia.cumulative_cycles,
            "final_wear_state": wear_state,
            "operating_conditions": qualia.environmental_state,
            "maintenance_pattern": self._summarize_maintenance(qualia.maintenance_history),
            "success_factors": self._infer_longevity_factors(qualia),
        }

        return Learning(
            learning_type=LearningType.LONGEVITY_FACTOR,
            content=content,
            confidence=0.7,
            applicability="similar_usage",
            source_part_id=qualia.part_id,
            source_qualia_id=qualia.id,
        )

    def _extract_environmental_learning(
        self,
        qualia: PartQualia,
    ) -> Optional[Learning]:
        """Extract learning from environmental adaptation."""
        env = qualia.environmental_state
        mechanical = qualia.mechanical_state

        # Check for notable environmental conditions
        notable_conditions = []
        if env.get("temperature_c", 20) > 100:
            notable_conditions.append("high_temperature")
        if env.get("temperature_c", 20) < -20:
            notable_conditions.append("low_temperature")
        if env.get("humidity_percent", 50) > 90:
            notable_conditions.append("high_humidity")
        if env.get("vibration_level") == "extreme":
            notable_conditions.append("extreme_vibration")
        if env.get("corrosive_exposure"):
            notable_conditions.append("corrosive_environment")

        if not notable_conditions:
            return None

        content = {
            "environmental_challenges": notable_conditions,
            "conditions_detail": env,
            "performance_maintained": mechanical.get("wear_state") in ["good", "acceptable"],
            "adaptation_strategies": self._infer_adaptations(env, mechanical),
        }

        return Learning(
            learning_type=LearningType.ENVIRONMENTAL_ADAPTATION,
            content=content,
            confidence=0.75,
            applicability="similar_environment",
            source_part_id=qualia.part_id,
            source_qualia_id=qualia.id,
        )

    def _extract_usage_learning(
        self,
        qualia: PartQualia,
    ) -> Optional[Learning]:
        """Extract learning from usage patterns."""
        if qualia.experience_type != "usage":
            return None

        mechanical = qualia.mechanical_state

        content = {
            "usage_context": qualia.experience_type,
            "load_pattern": {
                "typical_load_percent": mechanical.get("torque_capacity_percent", 0) * 100,
                "cycles_per_period": qualia.cumulative_cycles,
            },
            "environmental_context": qualia.environmental_state,
            "lifecycle_stage": qualia.lifecycle_stage,
        }

        return Learning(
            learning_type=LearningType.USAGE_PATTERN,
            content=content,
            confidence=0.6,
            applicability="similar_application",
            source_part_id=qualia.part_id,
            source_qualia_id=qualia.id,
        )

    def _infer_prevention(
        self,
        event: SignificantEvent,
        qualia: PartQualia,
    ) -> list[str]:
        """Infer prevention measures based on failure type."""
        prevention = []

        failure_type = event.failure_type or ""

        if "fatigue" in failure_type.lower():
            prevention.extend([
                "Reduce cyclic loading frequency",
                "Consider higher fatigue-rated part",
                "Implement stress-relief design",
            ])

        if "corrosion" in failure_type.lower():
            prevention.extend([
                "Use corrosion-resistant material",
                "Apply protective coating",
                "Control environmental exposure",
            ])

        if "overload" in failure_type.lower():
            prevention.extend([
                "Increase safety factor",
                "Use higher strength grade",
                "Add load limiting mechanism",
            ])

        if "wear" in failure_type.lower():
            prevention.extend([
                "Improve lubrication",
                "Use harder surface treatment",
                "Reduce friction points",
            ])

        # Add environmental-specific prevention
        env = qualia.environmental_state
        if env.get("temperature_c", 20) > 100:
            prevention.append("Select high-temperature rated component")

        return prevention

    def _summarize_maintenance(
        self,
        history: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Summarize maintenance history for learning."""
        if not history:
            return {"maintenance_performed": False}

        return {
            "maintenance_performed": True,
            "maintenance_count": len(history),
            "maintenance_types": list(set(m.get("type", "unknown") for m in history)),
            "regular_interval": len(history) >= 3,  # Indicates scheduled maintenance
        }

    def _infer_longevity_factors(
        self,
        qualia: PartQualia,
    ) -> list[str]:
        """Infer factors that contributed to longevity."""
        factors = []

        env = qualia.environmental_state
        mechanical = qualia.mechanical_state

        # Low stress operation
        if mechanical.get("torque_capacity_percent", 1) < 0.5:
            factors.append("Conservative loading (under 50% capacity)")

        # Favorable environment
        temp = env.get("temperature_c", 20)
        if 10 <= temp <= 40:
            factors.append("Moderate operating temperature")

        if env.get("vibration_level") in ["low", "minimal"]:
            factors.append("Low vibration environment")

        if not env.get("corrosive_exposure"):
            factors.append("Non-corrosive environment")

        # Good maintenance
        if qualia.maintenance_history:
            factors.append("Regular maintenance performed")

        return factors

    def _infer_adaptations(
        self,
        env: dict[str, Any],
        mechanical: dict[str, Any],
    ) -> list[str]:
        """Infer environmental adaptations for successful operation."""
        adaptations = []

        if env.get("temperature_c", 20) > 100:
            adaptations.append("High-temperature rated materials")
            adaptations.append("Thermal expansion allowance in design")

        if env.get("vibration_level") in ["high", "extreme"]:
            adaptations.append("Vibration-dampening mounting")
            adaptations.append("Thread-locking compound")

        if env.get("corrosive_exposure"):
            adaptations.append("Corrosion-resistant coating")
            adaptations.append("Regular inspection schedule")

        if env.get("humidity_percent", 50) > 80:
            adaptations.append("Moisture-resistant sealing")

        return adaptations
