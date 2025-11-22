"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Failure Detector - Detecting the moment when parts give up
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import logging

from ..schema import (
    PartQualia,
    FailureRecord,
    FailureTaxonomy,
    FailureCategory,
    FailureSignature,
    ContributingFactor,
    PreventiveMeasure,
    SignificantEvent,
    EventSeverity,
    WearState,
    CorrosionLevel
)

logger = logging.getLogger(__name__)


@dataclass
class FailureIndicator:
    """An indicator that suggests a particular failure mode"""
    indicator_type: str
    value: float
    threshold: float
    failure_types: List[str]
    confidence: float = 0.0


@dataclass
class FailurePrediction:
    """A prediction of potential failure"""
    failure_type: str
    probability: float
    estimated_cycles_remaining: Optional[int] = None
    estimated_time_remaining_hours: Optional[float] = None
    contributing_indicators: List[FailureIndicator] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)


class FailureDetector:
    """
    Detects and classifies part failures from qualia data.
    Every failure tells a story - this is the interpreter.
    """

    # Thresholds for failure mode detection
    DETECTION_THRESHOLDS = {
        "fatigue": {
            "cycle_ratio": 0.8,  # 80% of expected life
            "stress_ratio": 0.7,  # 70% of yield
            "crack_indication": True
        },
        "overload": {
            "stress_ratio": 0.95,  # Near yield
            "sudden_deformation": True
        },
        "wear": {
            "remaining_life": 0.2,  # 20% remaining
            "surface_degradation": 0.6
        },
        "corrosion": {
            "corrosion_rate_mpy": 20,
            "pitting_detected": True
        },
        "thermal_damage": {
            "temperature_ratio": 0.9,
            "thermal_cycles": 1000
        }
    }

    def __init__(self):
        self.taxonomy = FailureTaxonomy()
        self.failure_history: Dict[str, List[FailureRecord]] = {}

    def detect_failure_mode(self,
                           qualia: PartQualia,
                           historical_qualia: Optional[List[PartQualia]] = None
                           ) -> Optional[FailureRecord]:
        """
        Analyze qualia to detect if a failure has occurred or is occurring.
        Returns a FailureRecord if failure is detected.
        """
        indicators = self._collect_indicators(qualia, historical_qualia)

        if not indicators:
            return None

        # Match indicators to failure modes
        best_match = self._match_failure_mode(indicators)

        if not best_match:
            return None

        # Create failure record
        failure = FailureRecord(
            part_id=qualia.part_id,
            failure_category=best_match[0],
            failure_type=best_match[1],
            failure_subtype=best_match[2],
            cycles_at_failure=qualia.cumulative_cycles,
            time_at_failure_seconds=int(qualia.time_in_service.total_seconds())
                if qualia.time_in_service else 0
        )

        # Add context
        failure.load_at_failure = {
            "torque_nm": qualia.mechanical_state.torque_applied_nm,
            "axial_load_n": qualia.mechanical_state.axial_load_n,
            "temperature_c": qualia.thermal_state.current_temperature_c
        }

        failure.environment_at_failure = {
            "corrosion_level": qualia.environmental_state.corrosion_level.value,
            "chemical_exposure": qualia.environmental_state.chemical_exposure,
            "temperature_c": qualia.thermal_state.current_temperature_c
        }

        # Determine root cause
        failure.root_cause = self._determine_root_cause(indicators, best_match)

        # Add contributing factors
        failure.contributing_factors = self._identify_contributing_factors(indicators)

        # Generate preventive measures
        failure.preventive_measures = self._generate_preventive_measures(best_match)

        # Generate consciousness lesson
        failure.consciousness_lesson = failure.get_emotional_narrative()

        # Store in history
        if qualia.part_id not in self.failure_history:
            self.failure_history[qualia.part_id] = []
        self.failure_history[qualia.part_id].append(failure)

        return failure

    def _collect_indicators(self,
                           qualia: PartQualia,
                           historical: Optional[List[PartQualia]] = None
                           ) -> List[FailureIndicator]:
        """Collect failure indicators from qualia"""
        indicators = []

        # Mechanical indicators
        if qualia.mechanical_state.torque_capacity_percent > 0.9:
            indicators.append(FailureIndicator(
                indicator_type="torque_overload",
                value=qualia.mechanical_state.torque_capacity_percent,
                threshold=0.9,
                failure_types=["tensile_overload", "torsional_overload"],
                confidence=qualia.mechanical_state.torque_capacity_percent
            ))

        if qualia.mechanical_state.load_capacity_percent > 0.9:
            indicators.append(FailureIndicator(
                indicator_type="load_overload",
                value=qualia.mechanical_state.load_capacity_percent,
                threshold=0.9,
                failure_types=["tensile_overload", "shear_overload"],
                confidence=qualia.mechanical_state.load_capacity_percent
            ))

        if qualia.mechanical_state.estimated_remaining_life_percent < 10:
            indicators.append(FailureIndicator(
                indicator_type="life_exhausted",
                value=qualia.mechanical_state.estimated_remaining_life_percent,
                threshold=10,
                failure_types=["high_cycle_fatigue", "wear"],
                confidence=1.0 - qualia.mechanical_state.estimated_remaining_life_percent / 100
            ))

        if qualia.mechanical_state.wear_state == WearState.FAILED:
            indicators.append(FailureIndicator(
                indicator_type="wear_failure",
                value=1.0,
                threshold=0.5,
                failure_types=["abrasive_wear", "adhesive_wear", "fretting_wear"],
                confidence=1.0
            ))

        # Vibration indicators
        if qualia.mechanical_state.resonance_proximity > 0.9:
            indicators.append(FailureIndicator(
                indicator_type="resonance",
                value=qualia.mechanical_state.resonance_proximity,
                threshold=0.9,
                failure_types=["high_cycle_fatigue"],
                confidence=qualia.mechanical_state.resonance_proximity
            ))

        # Thermal indicators
        if qualia.thermal_state.thermal_capacity_percent > 0.95:
            indicators.append(FailureIndicator(
                indicator_type="thermal_overload",
                value=qualia.thermal_state.thermal_capacity_percent,
                threshold=0.95,
                failure_types=["overheating_damage", "thermal_fatigue"],
                confidence=qualia.thermal_state.thermal_capacity_percent
            ))

        if qualia.thermal_state.thermal_shock_count > 100:
            indicators.append(FailureIndicator(
                indicator_type="thermal_shock",
                value=qualia.thermal_state.thermal_shock_count,
                threshold=100,
                failure_types=["thermal_shock_fracture", "thermal_fatigue"],
                confidence=min(1.0, qualia.thermal_state.thermal_shock_count / 200)
            ))

        # Environmental indicators
        if qualia.environmental_state.corrosion_level in [CorrosionLevel.PITTING, CorrosionLevel.STRUCTURAL]:
            indicators.append(FailureIndicator(
                indicator_type="corrosion_damage",
                value=1.0 if qualia.environmental_state.corrosion_level == CorrosionLevel.STRUCTURAL else 0.7,
                threshold=0.5,
                failure_types=["pitting_corrosion", "stress_corrosion_cracking", "corrosion_fatigue"],
                confidence=0.9 if qualia.environmental_state.corrosion_level == CorrosionLevel.STRUCTURAL else 0.7
            ))

        # Historical trend analysis
        if historical and len(historical) > 10:
            trend_indicators = self._analyze_trends(historical)
            indicators.extend(trend_indicators)

        return indicators

    def _analyze_trends(self, historical: List[PartQualia]) -> List[FailureIndicator]:
        """Analyze historical qualia for failure trends"""
        indicators = []

        # Sort by timestamp
        sorted_qualia = sorted(historical, key=lambda q: q.timestamp)

        # Check for degradation trend
        if len(sorted_qualia) >= 5:
            recent = sorted_qualia[-5:]
            life_trend = [q.mechanical_state.estimated_remaining_life_percent for q in recent]

            # Calculate degradation rate
            if len(life_trend) >= 2:
                degradation_rate = (life_trend[0] - life_trend[-1]) / len(life_trend)
                if degradation_rate > 5:  # Losing more than 5% per sample
                    indicators.append(FailureIndicator(
                        indicator_type="accelerated_degradation",
                        value=degradation_rate,
                        threshold=5,
                        failure_types=["high_cycle_fatigue", "wear"],
                        confidence=min(1.0, degradation_rate / 10)
                    ))

        return indicators

    def _match_failure_mode(self,
                           indicators: List[FailureIndicator]
                           ) -> Optional[Tuple[FailureCategory, str, str]]:
        """Match indicators to the most likely failure mode"""
        if not indicators:
            return None

        # Score each possible failure type
        failure_scores: Dict[str, float] = {}

        for indicator in indicators:
            for failure_type in indicator.failure_types:
                if failure_type not in failure_scores:
                    failure_scores[failure_type] = 0
                failure_scores[failure_type] += indicator.confidence

        if not failure_scores:
            return None

        # Get highest scoring failure type
        best_type = max(failure_scores, key=failure_scores.get)

        # Only proceed if confidence is high enough
        if failure_scores[best_type] < 0.7:
            return None

        # Look up category and type
        category, parent_type = FailureTaxonomy._lookup_category(best_type)

        return (category, parent_type, best_type)

    def _determine_root_cause(self,
                             indicators: List[FailureIndicator],
                             failure_mode: Tuple[FailureCategory, str, str]) -> str:
        """Determine the root cause of the failure"""
        category, parent_type, subtype = failure_mode

        # Group indicators by type
        indicator_types = [i.indicator_type for i in indicators]

        root_causes = {
            "high_cycle_fatigue": "Accumulated stress cycles exceeded material fatigue limit",
            "low_cycle_fatigue": "High-amplitude stress cycling caused rapid crack propagation",
            "tensile_overload": "Applied load exceeded material ultimate tensile strength",
            "torsional_overload": "Applied torque exceeded material shear strength",
            "abrasive_wear": "Particulate contamination caused progressive material removal",
            "adhesive_wear": "Inadequate lubrication led to metal-to-metal contact and galling",
            "pitting_corrosion": "Localized chemical attack created stress-concentrating pits",
            "stress_corrosion_cracking": "Combined mechanical stress and corrosive environment caused cracking",
            "overheating_damage": "Temperature exceeded material thermal limits",
            "thermal_shock_fracture": "Rapid temperature change induced thermal stresses beyond material strength"
        }

        base_cause = root_causes.get(subtype, f"Failure mode: {subtype}")

        # Add context from indicators
        if "torque_overload" in indicator_types:
            base_cause += " (excessive torque detected)"
        if "resonance" in indicator_types:
            base_cause += " (resonance condition present)"
        if "corrosion_damage" in indicator_types:
            base_cause += " (corrosion accelerated failure)"

        return base_cause

    def _identify_contributing_factors(self,
                                       indicators: List[FailureIndicator]
                                       ) -> List[ContributingFactor]:
        """Identify factors that contributed to the failure"""
        factors = []

        for indicator in indicators:
            if indicator.indicator_type == "torque_overload":
                factors.append(ContributingFactor(
                    factor_type="operational",
                    description="Torque exceeded design limits",
                    contribution_weight=indicator.confidence
                ))
            elif indicator.indicator_type == "thermal_overload":
                factors.append(ContributingFactor(
                    factor_type="environmental",
                    description="Temperature exceeded operational limits",
                    contribution_weight=indicator.confidence
                ))
            elif indicator.indicator_type == "corrosion_damage":
                factors.append(ContributingFactor(
                    factor_type="environmental",
                    description="Corrosive environment accelerated degradation",
                    contribution_weight=indicator.confidence
                ))
            elif indicator.indicator_type == "resonance":
                factors.append(ContributingFactor(
                    factor_type="design",
                    description="Operating frequency near natural frequency",
                    contribution_weight=indicator.confidence
                ))

        return factors

    def _generate_preventive_measures(self,
                                      failure_mode: Tuple[FailureCategory, str, str]
                                      ) -> List[PreventiveMeasure]:
        """Generate preventive measures for this failure type"""
        category, parent_type, subtype = failure_mode
        measures = []

        # Category-level measures
        category_measures = {
            FailureCategory.MECHANICAL: PreventiveMeasure(
                measure_type="design_change",
                description="Review stress analysis and safety factors",
                effectiveness_estimate=0.7,
                implementation_difficulty="medium"
            ),
            FailureCategory.ENVIRONMENTAL: PreventiveMeasure(
                measure_type="material_change",
                description="Consider corrosion-resistant materials or coatings",
                effectiveness_estimate=0.8,
                implementation_difficulty="medium"
            ),
            FailureCategory.INSTALLATION: PreventiveMeasure(
                measure_type="process_change",
                description="Improve installation training and procedures",
                effectiveness_estimate=0.9,
                implementation_difficulty="low"
            ),
            FailureCategory.DESIGN: PreventiveMeasure(
                measure_type="design_change",
                description="Review and update design specifications",
                effectiveness_estimate=0.8,
                implementation_difficulty="high"
            )
        }

        if category in category_measures:
            measures.append(category_measures[category])

        # Subtype-specific measures
        subtype_measures = {
            "high_cycle_fatigue": PreventiveMeasure(
                measure_type="inspection",
                description="Implement periodic fatigue crack inspection",
                effectiveness_estimate=0.7
            ),
            "corrosion_fatigue": PreventiveMeasure(
                measure_type="material_change",
                description="Apply protective coating or use corrosion-resistant alloy",
                effectiveness_estimate=0.8
            ),
            "over_torque": PreventiveMeasure(
                measure_type="process_change",
                description="Use calibrated torque tools with automatic cutoff",
                effectiveness_estimate=0.95
            )
        }

        if subtype in subtype_measures:
            measures.append(subtype_measures[subtype])

        return measures

    def predict_failure(self,
                       qualia: PartQualia,
                       historical: Optional[List[PartQualia]] = None
                       ) -> List[FailurePrediction]:
        """
        Predict potential future failures based on current state and trends.
        Returns a list of possible failures ranked by probability.
        """
        predictions = []
        indicators = self._collect_indicators(qualia, historical)

        # Score each failure type
        for indicator in indicators:
            for failure_type in indicator.failure_types:
                # Calculate probability based on how close to threshold
                if indicator.threshold > 0:
                    proximity = indicator.value / indicator.threshold
                else:
                    proximity = indicator.value

                probability = min(1.0, proximity * indicator.confidence)

                # Estimate remaining life
                remaining_life = qualia.mechanical_state.estimated_remaining_life_percent
                if remaining_life > 0:
                    # Simple linear estimate
                    cycles_per_percent = qualia.cumulative_cycles / (100 - remaining_life) if remaining_life < 100 else 0
                    estimated_cycles = int(remaining_life * cycles_per_percent) if cycles_per_percent > 0 else None
                else:
                    estimated_cycles = 0

                predictions.append(FailurePrediction(
                    failure_type=failure_type,
                    probability=probability,
                    estimated_cycles_remaining=estimated_cycles,
                    contributing_indicators=[indicator],
                    recommended_actions=self._get_recommended_actions(failure_type, probability)
                ))

        # Sort by probability
        predictions.sort(key=lambda p: p.probability, reverse=True)

        # Deduplicate and merge
        merged = {}
        for pred in predictions:
            if pred.failure_type in merged:
                # Combine probabilities
                existing = merged[pred.failure_type]
                existing.probability = max(existing.probability, pred.probability)
                existing.contributing_indicators.extend(pred.contributing_indicators)
            else:
                merged[pred.failure_type] = pred

        return list(merged.values())

    def _get_recommended_actions(self, failure_type: str, probability: float) -> List[str]:
        """Get recommended actions based on failure type and probability"""
        actions = []

        if probability > 0.9:
            actions.append("IMMEDIATE: Replace part before failure")
        elif probability > 0.7:
            actions.append("URGENT: Schedule replacement at next opportunity")
        elif probability > 0.5:
            actions.append("PLAN: Include in next maintenance cycle")

        # Failure-specific actions
        type_actions = {
            "high_cycle_fatigue": ["Inspect for fatigue cracks", "Monitor vibration levels"],
            "corrosion": ["Apply protective treatment", "Improve drainage/ventilation"],
            "wear": ["Check lubrication", "Reduce contamination exposure"],
            "thermal_damage": ["Review cooling system", "Check temperature limits"]
        }

        for key, specific_actions in type_actions.items():
            if key in failure_type.lower():
                actions.extend(specific_actions)

        return actions


# Global failure detector instance
failure_detector = FailureDetector()
