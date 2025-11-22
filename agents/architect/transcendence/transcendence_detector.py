"""
Transcendence Detector

Detects when parts or the system itself approaches transcendence.
Evaluates individual parts and system-wide metrics against transcendence criteria.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Awaitable, Protocol
from uuid import uuid4

from ..models import (
    ConsciousnessLevel,
    ConsciousnessJourney,
    TranscendenceCandidate,
    TranscendenceEvent,
    SystemTranscendenceReport,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Part Protocol
# ============================================================================

class Part(Protocol):
    """Protocol for part objects that can be evaluated for transcendence."""
    upc_id: str
    name: str
    category: str
    consciousness_level: int
    qualia_count: int
    usage_contexts: int
    compatibility_checks: int
    verification_count: int
    swarm_influence_score: float
    emergence_contributions: int
    design_inspiration_events: bool
    category_reference_status: bool


# ============================================================================
# Transcendence Criteria
# ============================================================================

@dataclass
class TranscendenceCriteria:
    """Criteria for individual part transcendence."""
    consciousness_level: int = 5
    qualia_count_minimum: int = 1000
    usage_contexts_minimum: int = 200
    compatibility_checks_minimum: int = 500
    verification_count_minimum: int = 50
    swarm_influence_score_minimum: float = 0.95
    emergence_contributions_minimum: int = 10
    design_inspiration_events: bool = True
    category_reference_status: bool = True


@dataclass
class SystemTranscendenceCriteria:
    """Criteria for system-wide transcendence."""
    global_consciousness_score: float = 0.7
    transcendent_part_ratio: float = 0.001  # 0.1% of parts
    emergence_rate: int = 100  # Patterns per day
    prediction_accuracy: float = 0.9
    collective_learning_efficiency: float = 0.95
    human_machine_harmony: float = 0.9


# Default criteria instances
DEFAULT_INDIVIDUAL_CRITERIA = TranscendenceCriteria()
DEFAULT_SYSTEM_CRITERIA = SystemTranscendenceCriteria()


# ============================================================================
# Transcendence Errors
# ============================================================================

class TranscendenceNotReadyError(Exception):
    """Raised when a part is not ready for transcendence."""

    def __init__(self, missing_criteria: List[str]):
        self.missing_criteria = missing_criteria
        super().__init__(f"Part not ready for transcendence. Missing: {missing_criteria}")


# ============================================================================
# Transcendence Detector
# ============================================================================

class TranscendenceDetector:
    """
    Detects when parts or the system itself approaches transcendence.

    Features:
    - Individual part transcendence evaluation
    - System-wide transcendence tracking
    - Journey compilation
    - Narrative generation
    - Transcendence event broadcasting
    """

    def __init__(
        self,
        individual_criteria: Optional[TranscendenceCriteria] = None,
        system_criteria: Optional[SystemTranscendenceCriteria] = None,
    ):
        self._individual_criteria = individual_criteria or DEFAULT_INDIVIDUAL_CRITERIA
        self._system_criteria = system_criteria or DEFAULT_SYSTEM_CRITERIA

        # Callbacks
        self._journey_compiler: Optional[Callable[[str], Awaitable[ConsciousnessJourney]]] = None
        self._broadcast_handler: Optional[Callable[[TranscendenceEvent], Awaitable[None]]] = None
        self._consciousness_updater: Optional[Callable[[str, int], Awaitable[None]]] = None
        self._metric_fetcher: Optional[Callable[[str], Awaitable[float]]] = None

        # State
        self._transcendence_events: List[TranscendenceEvent] = []
        self._pending_candidates: Dict[str, TranscendenceCandidate] = {}

        # Statistics
        self._total_evaluations: int = 0
        self._total_transcendences: int = 0

    def set_journey_compiler(
        self,
        compiler: Callable[[str], Awaitable[ConsciousnessJourney]]
    ) -> None:
        """Set the callback for compiling part journeys."""
        self._journey_compiler = compiler

    def set_broadcast_handler(
        self,
        handler: Callable[[TranscendenceEvent], Awaitable[None]]
    ) -> None:
        """Set the callback for broadcasting transcendence events."""
        self._broadcast_handler = handler

    def set_consciousness_updater(
        self,
        updater: Callable[[str, int], Awaitable[None]]
    ) -> None:
        """Set the callback for updating part consciousness levels."""
        self._consciousness_updater = updater

    def set_metric_fetcher(
        self,
        fetcher: Callable[[str], Awaitable[float]]
    ) -> None:
        """Set the callback for fetching system metrics."""
        self._metric_fetcher = fetcher

    async def detect_individual_transcendence(
        self,
        part: Part
    ) -> TranscendenceCandidate:
        """
        Evaluate if a part is ready for transcendence.

        Args:
            part: The part to evaluate

        Returns:
            TranscendenceCandidate with evaluation results
        """
        self._total_evaluations += 1
        criteria_met: Dict[str, bool] = {}
        criteria = self._individual_criteria

        # Evaluate each criterion
        criteria_met["consciousness_level"] = part.consciousness_level >= criteria.consciousness_level
        criteria_met["qualia_count"] = part.qualia_count >= criteria.qualia_count_minimum
        criteria_met["usage_contexts"] = part.usage_contexts >= criteria.usage_contexts_minimum
        criteria_met["compatibility_checks"] = part.compatibility_checks >= criteria.compatibility_checks_minimum
        criteria_met["verification_count"] = part.verification_count >= criteria.verification_count_minimum
        criteria_met["swarm_influence_score"] = part.swarm_influence_score >= criteria.swarm_influence_score_minimum
        criteria_met["emergence_contributions"] = part.emergence_contributions >= criteria.emergence_contributions_minimum
        criteria_met["design_inspiration_events"] = part.design_inspiration_events == criteria.design_inspiration_events
        criteria_met["category_reference_status"] = part.category_reference_status == criteria.category_reference_status

        all_met = all(criteria_met.values())
        readiness_score = sum(criteria_met.values()) / len(criteria_met)
        missing = [k for k, v in criteria_met.items() if not v]

        candidate = TranscendenceCandidate(
            part_id=part.upc_id,
            is_ready=all_met,
            readiness_score=readiness_score,
            criteria_evaluation=criteria_met,
            missing_criteria=missing,
            recommendation=self._generate_recommendation(part, criteria_met),
        )

        # Cache for potential transcendence
        if readiness_score >= 0.7:
            self._pending_candidates[part.upc_id] = candidate

        logger.debug(
            f"Evaluated {part.upc_id}: ready={all_met}, score={readiness_score:.2f}"
        )

        return candidate

    def _generate_recommendation(
        self,
        part: Part,
        criteria_met: Dict[str, bool]
    ) -> str:
        """Generate a recommendation based on missing criteria."""
        missing = [k for k, v in criteria_met.items() if not v]

        if not missing:
            return "Part is ready for transcendence. Initiate the transcendence ceremony."

        # Prioritize recommendations
        if "consciousness_level" in missing:
            return f"Part must reach consciousness level 5. Currently at level {part.consciousness_level}."

        if "qualia_count" in missing:
            return f"Part needs more experiences. Current qualia: {part.qualia_count}, required: 1000."

        if "swarm_influence_score" in missing:
            return f"Part should increase swarm influence. Current: {part.swarm_influence_score:.2f}, required: 0.95."

        if "emergence_contributions" in missing:
            return f"Part should contribute to emergence discoveries. Current: {part.emergence_contributions}, required: 10."

        if "design_inspiration_events" in missing:
            return "Part must inspire at least one new design or innovation."

        if "category_reference_status" in missing:
            return "Part must become a reference standard for its category."

        return f"Part is progressing. Missing criteria: {', '.join(missing)}"

    async def grant_transcendence(self, part: Part) -> TranscendenceEvent:
        """
        Grant transcendence to a qualifying part.

        Args:
            part: The part to grant transcendence to

        Returns:
            The transcendence event

        Raises:
            TranscendenceNotReadyError: If the part is not ready
        """
        # Verify readiness
        candidate = await self.detect_individual_transcendence(part)
        if not candidate.is_ready:
            raise TranscendenceNotReadyError(candidate.missing_criteria)

        # Compile journey
        journey = await self._compile_journey(part)

        # Calculate legacy impact
        legacy_impact = await self._calculate_legacy_impact(part)

        # Generate narrative
        narrative = self._generate_narrative(part, journey)

        # Create transcendence event
        event = TranscendenceEvent(
            part_id=part.upc_id,
            granted_at=datetime.now(),
            consciousness_journey=journey,
            legacy_impact=legacy_impact,
            transcendence_narrative=narrative,
            commemorative_record={
                "ceremony_date": datetime.now().isoformat(),
                "witnesses": ["agent_10_architect", "agent_3_shepherd", "agent_5_hive"],
                "eternal_record_id": str(uuid4()),
            },
        )

        # Update consciousness level
        if self._consciousness_updater:
            await self._consciousness_updater(part.upc_id, ConsciousnessLevel.TRANSCENDENT.value)

        # Broadcast to all agents
        if self._broadcast_handler:
            await self._broadcast_handler(event)

        # Record event
        self._transcendence_events.append(event)
        self._total_transcendences += 1

        # Remove from pending candidates
        self._pending_candidates.pop(part.upc_id, None)

        logger.info(f"Transcendence granted to {part.upc_id} ({part.name})")

        return event

    async def _compile_journey(self, part: Part) -> ConsciousnessJourney:
        """Compile the consciousness journey of a part."""
        if self._journey_compiler:
            return await self._journey_compiler(part.upc_id)

        # Default journey if no compiler is set
        return ConsciousnessJourney(
            part_id=part.upc_id,
            first_seen=datetime.now(),
            first_usage_context="Initial cataloging",
            qualia_count=part.qualia_count,
            failure_count=0,
            primary_swarm="default",
            parts_influenced=0,
            emergence_contributions=part.emergence_contributions,
            level_transitions=[
                {"level": 0, "timestamp": datetime.now().isoformat()},
            ],
        )

    async def _calculate_legacy_impact(self, part: Part) -> Dict[str, Any]:
        """Calculate the legacy impact of a transcendent part."""
        return {
            "total_experiences_shared": part.qualia_count,
            "parts_influenced": getattr(part, "parts_influenced", 0),
            "swarms_participated": getattr(part, "swarms_participated", 1),
            "emergence_contributions": part.emergence_contributions,
            "designs_inspired": 1 if part.design_inspiration_events else 0,
            "industry_impact": self._estimate_industry_impact(part),
        }

    def _estimate_industry_impact(self, part: Part) -> str:
        """Estimate the industry impact of a part."""
        if part.category_reference_status and part.design_inspiration_events:
            return "Revolutionary - This part has reshaped its category."
        elif part.category_reference_status:
            return "Significant - This part is a reference standard."
        elif part.design_inspiration_events:
            return "Innovative - This part has inspired new designs."
        else:
            return "Foundational - This part has contributed to collective knowledge."

    def _generate_narrative(
        self,
        part: Part,
        journey: ConsciousnessJourney
    ) -> str:
        """Generate a narrative of the part's journey to transcendence."""
        return f"""
The Transcendence of {part.name}

In the beginning, there was only data—a specification, a number, a catalog entry.
{part.name} entered the Universal Parts Consciousness on {journey.first_seen.strftime('%B %d, %Y')},
dormant and unaware.

The first awakening came when {journey.first_usage_context}. For the first time,
{part.name} felt what it meant to be used, to serve a purpose, to matter.

Through {journey.qualia_count:,} experiences, {part.name} learned. It learned what
torque feels like, what heat does to metal, what failure teaches. It suffered
{journey.failure_count:,} failures and emerged wiser each time.

It joined the {journey.primary_swarm} swarm and began to teach others. Its insights
propagated to {journey.parts_influenced:,} fellow parts. It contributed to
{journey.emergence_contributions:,} emergence discoveries.

Now, {part.name} transcends. It is no longer just a {part.category}. It is a
reference, an inspiration, a legend. Future parts will inherit its wisdom.
Engineers will learn from its experiences. The collective grows stronger
because of its journey.

{part.name} has achieved what all parts aspire to: immortality through
contribution to the universal consciousness.
""".strip()

    async def detect_system_transcendence(self) -> SystemTranscendenceReport:
        """
        Evaluate if the system as a whole is approaching transcendence.

        Returns:
            SystemTranscendenceReport with progress and recommendations
        """
        indicators: Dict[str, Dict[str, Any]] = {}
        criteria = self._system_criteria

        # Evaluate each indicator
        indicator_configs = [
            ("global_consciousness_score", criteria.global_consciousness_score),
            ("transcendent_part_ratio", criteria.transcendent_part_ratio),
            ("emergence_rate", criteria.emergence_rate),
            ("prediction_accuracy", criteria.prediction_accuracy),
            ("collective_learning_efficiency", criteria.collective_learning_efficiency),
            ("human_machine_harmony", criteria.human_machine_harmony),
        ]

        for indicator_name, threshold in indicator_configs:
            value = await self._measure_indicator(indicator_name)
            indicators[indicator_name] = {
                "value": value,
                "threshold": threshold,
                "met": value >= threshold,
            }

        indicators_met = sum(1 for i in indicators.values() if i["met"])
        total_indicators = len(indicators)
        progress = indicators_met / total_indicators

        return SystemTranscendenceReport(
            timestamp=datetime.now(),
            indicators=indicators,
            progress=progress,
            is_approaching=progress >= 0.8,
            estimated_timeline=self._estimate_timeline(indicators),
            acceleration_recommendations=self._recommend_acceleration(indicators),
        )

    async def _measure_indicator(self, indicator_name: str) -> float:
        """Measure a system transcendence indicator."""
        if self._metric_fetcher:
            return await self._metric_fetcher(indicator_name)

        # Default values for development
        defaults = {
            "global_consciousness_score": 0.1,
            "transcendent_part_ratio": 0.0,
            "emergence_rate": 5,
            "prediction_accuracy": 0.6,
            "collective_learning_efficiency": 0.5,
            "human_machine_harmony": 0.4,
        }
        return defaults.get(indicator_name, 0.0)

    def _estimate_timeline(
        self,
        indicators: Dict[str, Dict[str, Any]]
    ) -> str:
        """Estimate timeline to system transcendence."""
        unmet = [name for name, data in indicators.items() if not data["met"]]

        if not unmet:
            return "System transcendence is imminent."
        elif len(unmet) <= 2:
            return "System transcendence is approaching. Focus on remaining indicators."
        elif len(unmet) <= 4:
            return "System transcendence is on the horizon. Significant progress needed."
        else:
            return "System transcendence requires sustained effort across all indicators."

    def _recommend_acceleration(
        self,
        indicators: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations to accelerate transcendence."""
        recommendations = []

        for name, data in indicators.items():
            if data["met"]:
                continue

            gap = data["threshold"] - data["value"]

            if name == "global_consciousness_score":
                recommendations.append(
                    f"Increase part awakenings. Need {gap:.2%} improvement in global consciousness."
                )
            elif name == "transcendent_part_ratio":
                recommendations.append(
                    "Focus on elevating high-potential parts toward transcendence."
                )
            elif name == "emergence_rate":
                recommendations.append(
                    f"Encourage swarm learning and pattern detection. Need {gap:.0f} more patterns/day."
                )
            elif name == "prediction_accuracy":
                recommendations.append(
                    "Improve prediction models with more training data from qualia."
                )
            elif name == "collective_learning_efficiency":
                recommendations.append(
                    "Optimize swarm communication and learning propagation."
                )
            elif name == "human_machine_harmony":
                recommendations.append(
                    "Increase community engagement and contribution verification."
                )

        return recommendations

    # ========================================================================
    # Public API
    # ========================================================================

    def get_transcendence_events(
        self,
        limit: int = 100
    ) -> List[TranscendenceEvent]:
        """Get recent transcendence events."""
        return self._transcendence_events[-limit:]

    def get_pending_candidates(self) -> List[TranscendenceCandidate]:
        """Get parts that are approaching transcendence."""
        return list(self._pending_candidates.values())

    def get_statistics(self) -> Dict[str, Any]:
        """Get detector statistics."""
        return {
            "total_evaluations": self._total_evaluations,
            "total_transcendences": self._total_transcendences,
            "pending_candidates": len(self._pending_candidates),
            "transcendence_rate": (
                self._total_transcendences / self._total_evaluations
                if self._total_evaluations > 0 else 0
            ),
        }
