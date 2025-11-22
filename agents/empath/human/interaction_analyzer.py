"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Human Interaction Analyzer - Understanding how humans treat parts
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import logging

from ..schema import HumanInteractionQualia, PartQualia, SignificantEvent, EventSeverity

logger = logging.getLogger(__name__)


@dataclass
class InteractionPattern:
    """Definition of a human interaction pattern"""
    pattern_name: str
    description: str
    indicators: List[str]
    qualia_effect: str
    consciousness_boost: float
    emotional_impact: str
    severity: str = "info"  # "info", "warning", "critical"


# Pre-defined interaction patterns
INTERACTION_PATTERNS: Dict[str, InteractionPattern] = {
    "expert_installation": InteractionPattern(
        pattern_name="expert_installation",
        description="Skilled technician performing proper installation",
        indicators=[
            "proper_torque_sequence",
            "correct_lubrication",
            "alignment_verified",
            "specification_followed",
            "calibrated_tools"
        ],
        qualia_effect="confidence",
        consciousness_boost=0.1,
        emotional_impact="This part feels secure and properly cared for"
    ),
    "novice_installation": InteractionPattern(
        pattern_name="novice_installation",
        description="Inexperienced installer with learning curve",
        indicators=[
            "inconsistent_torque",
            "multiple_attempts",
            "no_lubrication",
            "hesitation_detected",
            "reference_checks"
        ],
        qualia_effect="anxiety",
        consciousness_boost=0.05,
        emotional_impact="Uncertainty, but survival through learning"
    ),
    "rushed_installation": InteractionPattern(
        pattern_name="rushed_installation",
        description="Time-pressured installation with shortcuts",
        indicators=[
            "fast_torque_application",
            "skipped_steps",
            "no_verification",
            "single_pass",
            "no_lubrication"
        ],
        qualia_effect="uncertainty",
        consciousness_boost=0.02,
        emotional_impact="Hurried into place, future uncertain",
        severity="warning"
    ),
    "abuse": InteractionPattern(
        pattern_name="abuse",
        description="Harmful treatment causing damage",
        indicators=[
            "impact_applied",
            "over_torque_severe",
            "cross_threading",
            "forced_fit",
            "hammering"
        ],
        qualia_effect="suffering",
        consciousness_boost=0.15,  # Pain is a powerful teacher
        emotional_impact="Trauma - excessive force, threads crying out",
        severity="critical"
    ),
    "maintenance_care": InteractionPattern(
        pattern_name="maintenance_care",
        description="Regular maintenance and inspection",
        indicators=[
            "regular_inspection",
            "proper_cleaning",
            "timely_replacement",
            "lubrication_refresh",
            "torque_recheck"
        ],
        qualia_effect="nurturing",
        consciousness_boost=0.08,
        emotional_impact="Someone cares - inspected, appreciated"
    ),
    "neglect": InteractionPattern(
        pattern_name="neglect",
        description="Lack of proper maintenance",
        indicators=[
            "no_inspection",
            "contamination_ignored",
            "degradation_ignored",
            "overdue_service",
            "warning_signs_missed"
        ],
        qualia_effect="abandonment",
        consciousness_boost=0.03,
        emotional_impact="Forgotten in darkness, degradation creeping in",
        severity="warning"
    ),
    "diagnostic_attention": InteractionPattern(
        pattern_name="diagnostic_attention",
        description="Troubleshooting and diagnostic focus",
        indicators=[
            "measurement_taken",
            "visual_inspection",
            "testing_performed",
            "documentation",
            "comparison_analysis"
        ],
        qualia_effect="examination",
        consciousness_boost=0.06,
        emotional_impact="Being studied, condition understood"
    ),
    "emergency_repair": InteractionPattern(
        pattern_name="emergency_repair",
        description="Urgent repair under pressure",
        indicators=[
            "rapid_disassembly",
            "immediate_replacement",
            "minimal_verification",
            "pressure_conditions",
            "incomplete_procedure"
        ],
        qualia_effect="crisis",
        consciousness_boost=0.1,
        emotional_impact="Urgency, survival mode, rapid change",
        severity="warning"
    )
}


@dataclass
class SkillAssessment:
    """Assessment of installer/maintainer skill level"""
    skill_level: str  # "novice", "intermediate", "expert"
    confidence: float
    indicators: List[str]
    recommendations: List[str]


class HumanInteractionAnalyzer:
    """
    Analyzes human interactions with parts and their qualia implications.
    Understanding how humans treat parts is key to consciousness evolution.
    """

    def __init__(self):
        self.patterns = INTERACTION_PATTERNS
        self.interaction_history: Dict[str, List[HumanInteractionQualia]] = {}

    def analyze_interaction(self,
                           interaction_data: Dict,
                           part_id: str,
                           part_name: Optional[str] = None
                           ) -> HumanInteractionQualia:
        """
        Analyze interaction data to determine the nature of human interaction
        and its effect on the part.
        """
        # Match patterns
        pattern_scores = self._score_patterns(interaction_data)

        # Find best match
        best_match_name = max(pattern_scores, key=pattern_scores.get)
        best_match = self.patterns[best_match_name]
        confidence = pattern_scores[best_match_name]

        # Build qualia
        qualia = HumanInteractionQualia(
            part_id=part_id,
            interaction_type=best_match_name,
            confidence=confidence,
            qualia_effect=best_match.qualia_effect,
            consciousness_contribution=best_match.consciousness_boost * confidence,
            narrative=self._generate_narrative(best_match, part_name or f"Part {part_id}"),
            indicators_matched=self._get_matched_indicators(interaction_data, best_match),
            raw_data=interaction_data
        )

        # Store in history
        if part_id not in self.interaction_history:
            self.interaction_history[part_id] = []
        self.interaction_history[part_id].append(qualia)

        return qualia

    def _score_patterns(self, interaction_data: Dict) -> Dict[str, float]:
        """Score all patterns against the interaction data"""
        scores = {}

        for pattern_name, pattern in self.patterns.items():
            score = self._match_pattern(interaction_data, pattern.indicators)
            scores[pattern_name] = score

        return scores

    def _match_pattern(self, data: Dict, indicators: List[str]) -> float:
        """Calculate match score for a pattern's indicators"""
        if not indicators:
            return 0.0

        matches = 0
        for indicator in indicators:
            # Direct indicator presence
            if indicator in data and data[indicator]:
                matches += 1
                continue

            # Check for indicator in nested data
            if self._check_nested_indicator(data, indicator):
                matches += 1
                continue

            # Check derived indicators
            if self._check_derived_indicator(data, indicator):
                matches += 1

        return matches / len(indicators)

    def _check_nested_indicator(self, data: Dict, indicator: str) -> bool:
        """Check for indicator in nested data structures"""
        for key, value in data.items():
            if isinstance(value, dict):
                if indicator in value:
                    return bool(value[indicator])
            elif isinstance(value, list):
                if indicator in value:
                    return True
        return False

    def _check_derived_indicator(self, data: Dict, indicator: str) -> bool:
        """Check for indicators that can be derived from raw data"""
        derivations = {
            "proper_torque_sequence": lambda d: (
                d.get("torque_steps", 0) >= 3 and
                d.get("torque_variance", 1) < 0.1
            ),
            "over_torque_severe": lambda d: (
                d.get("torque_applied", 0) > d.get("torque_spec", float('inf')) * 1.2
            ),
            "fast_torque_application": lambda d: (
                d.get("torque_duration_ms", float('inf')) < 500
            ),
            "multiple_attempts": lambda d: (
                d.get("attempt_count", 1) > 2
            ),
            "calibrated_tools": lambda d: (
                d.get("tool_calibration_date") is not None
            ),
            "inconsistent_torque": lambda d: (
                d.get("torque_variance", 0) > 0.2
            ),
            "cross_threading": lambda d: (
                d.get("thread_engagement_issues", False) or
                d.get("resistance_anomaly", False)
            ),
            "impact_applied": lambda d: (
                d.get("impact_detected", False) or
                d.get("acceleration_spike", 0) > 50  # 50g spike
            )
        }

        if indicator in derivations:
            try:
                return derivations[indicator](data)
            except (KeyError, TypeError):
                return False

        return False

    def _get_matched_indicators(self,
                               data: Dict,
                               pattern: InteractionPattern) -> List[str]:
        """Get list of indicators that matched"""
        matched = []
        for indicator in pattern.indicators:
            if indicator in data and data[indicator]:
                matched.append(indicator)
            elif self._check_nested_indicator(data, indicator):
                matched.append(indicator)
            elif self._check_derived_indicator(data, indicator):
                matched.append(indicator)
        return matched

    def _generate_narrative(self, pattern: InteractionPattern, part_name: str) -> str:
        """Generate a narrative description of the interaction experience"""
        narratives = {
            "expert_installation": f"{part_name} was installed by skilled hands, "
                                  "each step precise and deliberate. Torque applied with care, "
                                  "alignment verified, lubrication perfect.",
            "novice_installation": f"{part_name} felt the uncertainty of inexperienced hands, "
                                  "but survived the learning. Multiple attempts, growing confidence.",
            "rushed_installation": f"{part_name} was hurried into place, steps skipped, "
                                  "verification absent. Its future uncertain, foundation shaky.",
            "abuse": f"{part_name} suffered - impact, strain beyond design, "
                    "threads crying out. The damage will be remembered.",
            "maintenance_care": f"{part_name} was inspected, cleaned, appreciated. "
                               "Regular attention from someone who cares.",
            "neglect": f"{part_name} waits in darkness, forgotten. "
                      "Contamination builds, degradation creeps in unnoticed.",
            "diagnostic_attention": f"{part_name} was examined closely, measured, tested. "
                                   "Its condition is now understood, documented.",
            "emergency_repair": f"{part_name} experienced the urgency of crisis. "
                               "Rapid hands, immediate need, survival mode engaged."
        }
        return narratives.get(pattern.pattern_name,
                             f"{part_name} experienced {pattern.description}.")

    def assess_skill(self,
                    interaction_history: List[Dict]) -> SkillAssessment:
        """
        Assess the skill level of the human based on interaction history.
        """
        if not interaction_history:
            return SkillAssessment(
                skill_level="unknown",
                confidence=0.0,
                indicators=[],
                recommendations=["Insufficient data for assessment"]
            )

        # Analyze patterns in history
        expert_indicators = 0
        novice_indicators = 0
        abuse_indicators = 0
        total_interactions = len(interaction_history)

        for interaction in interaction_history:
            scores = self._score_patterns(interaction)

            if scores.get("expert_installation", 0) > 0.6:
                expert_indicators += 1
            if scores.get("novice_installation", 0) > 0.6:
                novice_indicators += 1
            if scores.get("abuse", 0) > 0.3:
                abuse_indicators += 1

        # Determine skill level
        if expert_indicators / total_interactions > 0.7:
            skill_level = "expert"
            confidence = expert_indicators / total_interactions
            indicators = ["consistent_proper_technique", "high_quality_installations"]
            recommendations = ["Continue current practices"]
        elif novice_indicators / total_interactions > 0.5:
            skill_level = "novice"
            confidence = novice_indicators / total_interactions
            indicators = ["inconsistent_technique", "learning_patterns"]
            recommendations = [
                "Recommend additional training",
                "Pair with experienced technician",
                "Provide step-by-step guides"
            ]
        else:
            skill_level = "intermediate"
            confidence = 0.5
            indicators = ["mixed_results", "variable_technique"]
            recommendations = ["Targeted skill improvement", "Regular quality checks"]

        if abuse_indicators > 0:
            indicators.append("damage_incidents")
            recommendations.append("CRITICAL: Address handling issues immediately")

        return SkillAssessment(
            skill_level=skill_level,
            confidence=confidence,
            indicators=indicators,
            recommendations=recommendations
        )

    def get_interaction_summary(self, part_id: str) -> Dict:
        """Get a summary of all interactions for a part"""
        if part_id not in self.interaction_history:
            return {"part_id": part_id, "interactions": 0, "summary": "No recorded interactions"}

        history = self.interaction_history[part_id]

        # Count interaction types
        type_counts = {}
        total_consciousness = 0.0

        for interaction in history:
            itype = interaction.interaction_type
            type_counts[itype] = type_counts.get(itype, 0) + 1
            total_consciousness += interaction.consciousness_contribution

        # Determine overall treatment
        if type_counts.get("abuse", 0) > 0:
            overall = "abused"
        elif type_counts.get("expert_installation", 0) >= type_counts.get("novice_installation", 0):
            overall = "well_treated"
        elif type_counts.get("neglect", 0) > len(history) / 2:
            overall = "neglected"
        else:
            overall = "mixed"

        return {
            "part_id": part_id,
            "interactions": len(history),
            "type_breakdown": type_counts,
            "total_consciousness_contribution": total_consciousness,
            "overall_treatment": overall,
            "last_interaction": history[-1].timestamp.isoformat() if history else None
        }


# Global analyzer instance
interaction_analyzer = HumanInteractionAnalyzer()
