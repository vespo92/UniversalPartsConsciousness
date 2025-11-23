"""
Failure Pattern Detector

Detects patterns across failure reports in the UPC network.
This is where collective learning happens.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


@dataclass
class EmergingPattern:
    """An emerging failure pattern detected in the network"""
    pattern_id: str
    description: str
    affected_parts: List[str]
    failure_count: int
    time_window_days: int
    geographic_distribution: List[str]
    common_factors: List[str]
    confidence: float
    severity: str
    recommended_action: str
    potential_recall_scope: Optional[int]
    first_detected: datetime


@dataclass
class SimilarFailure:
    """A similar failure from the network"""
    failure_id: str
    similarity_score: float
    part_type: str
    part_specification: str
    application: str
    failure_mode: str
    root_cause: str
    resolution: str
    reporter_type: str
    verification_status: str


class FailurePatternDetector:
    """
    Detects patterns across failure reports in the UPC network.

    This is where collective learning happens - identifying:
    - Similar failures for learning
    - Emerging patterns that might indicate recalls
    - Trends over time
    - Geographic clusters
    """

    def __init__(self):
        """Initialize pattern detector."""
        self.pattern_history = []
        self.similar_failure_cache = {}

    async def find_similar_failures(
        self,
        part_type: str,
        failure_mode: Any,
        application: Optional[str] = None,
        similarity_threshold: float = 0.7
    ) -> List[SimilarFailure]:
        """
        Find similar failures reported across the UPC network.

        Args:
            part_type: Type of part that failed
            failure_mode: Mode of failure
            application: Optional application context
            similarity_threshold: Minimum similarity score

        Returns:
            List of similar failures sorted by similarity
        """
        failure_mode_str = str(failure_mode.value if hasattr(failure_mode, 'value') else failure_mode)

        # Simulated similar failures database
        # In production, this would query the actual network database
        similar_failures_db = self._get_simulated_failures(part_type, failure_mode_str)

        # Filter and score by similarity
        results = []
        for failure in similar_failures_db:
            score = self._calculate_similarity(
                part_type,
                failure_mode_str,
                application,
                failure
            )
            if score >= similarity_threshold:
                results.append(SimilarFailure(
                    failure_id=failure["id"],
                    similarity_score=score,
                    part_type=failure["part_type"],
                    part_specification=failure["part_spec"],
                    application=failure["application"],
                    failure_mode=failure["failure_mode"],
                    root_cause=failure["root_cause"],
                    resolution=failure["resolution"],
                    reporter_type=failure["reporter_type"],
                    verification_status=failure["verified"]
                ))

        # Sort by similarity score
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:10]  # Return top 10

    async def detect_emerging_patterns(
        self,
        time_window_days: int = 30
    ) -> List[EmergingPattern]:
        """
        Detect emerging failure patterns that might indicate systemic issues.

        This is how we catch recalls before they happen.

        Args:
            time_window_days: Time window to analyze

        Returns:
            List of emerging patterns with severity ratings
        """
        # Simulated pattern detection
        # In production, this would run ML models on the failure database
        patterns = [
            EmergingPattern(
                pattern_id="PATTERN-2024-001",
                description="Hydrogen embrittlement in zinc-plated 10.9 bolts",
                affected_parts=["M8x25-10.9-ZN", "M10x30-10.9-ZN", "M10x40-10.9-ZN"],
                failure_count=12,
                time_window_days=time_window_days,
                geographic_distribution=["California", "Texas", "Michigan"],
                common_factors=[
                    "All zinc electroplated",
                    "All Grade 10.9",
                    "All failed within 1000 service hours",
                    "Common supplier suspected",
                ],
                confidence=0.85,
                severity="HIGH",
                recommended_action="Alert users with similar parts, investigate supplier",
                potential_recall_scope=50000,
                first_detected=datetime.utcnow() - timedelta(days=5)
            ),
        ]

        return patterns

    async def detect_trend(
        self,
        failure_mode: str,
        time_range_days: int = 90
    ) -> Dict[str, Any]:
        """
        Detect trends in failure occurrence over time.

        Args:
            failure_mode: Failure mode to analyze
            time_range_days: Time range to analyze

        Returns:
            Trend analysis results
        """
        return {
            "failure_mode": failure_mode,
            "time_range_days": time_range_days,
            "trend": "increasing",  # or "decreasing", "stable"
            "rate_change_percent": 15,
            "total_failures": 47,
            "geographic_hotspots": ["California", "Texas"],
            "common_applications": ["Automotive", "Industrial"],
            "recommendation": "Monitor closely, potential systemic issue",
        }

    def _get_simulated_failures(
        self,
        part_type: str,
        failure_mode: str
    ) -> List[Dict]:
        """Get simulated similar failures for demonstration."""
        base_failures = [
            {
                "id": "FAIL-2024-8891",
                "part_type": "Socket head cap screw",
                "part_spec": "M10x40 SHCS 10.9",
                "application": "CNC spindle mount",
                "failure_mode": "high_cycle_fatigue",
                "root_cause": "Insufficient preload + vibration",
                "resolution": "Upgraded to 12.9 + Nord-Lock washers",
                "reporter_type": "verified_engineer",
                "verified": "Verified",
            },
            {
                "id": "FAIL-2024-7234",
                "part_type": "Socket head cap screw",
                "part_spec": "M10x30 SHCS 10.9",
                "application": "Motor mount",
                "failure_mode": "high_cycle_fatigue",
                "root_cause": "Preload relaxation over time",
                "resolution": "Added Belleville washers, re-torque schedule",
                "reporter_type": "oem_engineer",
                "verified": "Verified",
            },
            {
                "id": "FAIL-2024-6543",
                "part_type": "Hex bolt",
                "part_spec": "M8x25 8.8 Zinc",
                "application": "Suspension bracket",
                "failure_mode": "hydrogen_embrittlement",
                "root_cause": "No bake after zinc plating",
                "resolution": "Switched to Geomet coating",
                "reporter_type": "professional",
                "verified": "Verified",
            },
            {
                "id": "FAIL-2024-5678",
                "part_type": "Socket head cap screw",
                "part_spec": "M8x20 SHCS 12.9",
                "application": "Engine mount",
                "failure_mode": "high_cycle_fatigue",
                "root_cause": "Thread root stress concentration",
                "resolution": "Used rolled thread bolts",
                "reporter_type": "professional",
                "verified": "Pending",
            },
        ]

        # Filter by relevance to query
        return [f for f in base_failures
                if failure_mode in f["failure_mode"] or
                part_type.lower() in f["part_type"].lower()]

    def _calculate_similarity(
        self,
        query_part_type: str,
        query_failure_mode: str,
        query_application: Optional[str],
        candidate: Dict
    ) -> float:
        """Calculate similarity score between query and candidate."""
        score = 0.0

        # Part type similarity (40% weight)
        if query_part_type.lower() in candidate["part_type"].lower():
            score += 0.4
        elif any(word in candidate["part_type"].lower()
                for word in query_part_type.lower().split()):
            score += 0.2

        # Failure mode match (40% weight)
        if query_failure_mode == candidate["failure_mode"]:
            score += 0.4
        elif query_failure_mode in candidate["failure_mode"]:
            score += 0.2

        # Application match (20% weight)
        if query_application:
            if query_application.lower() in candidate["application"].lower():
                score += 0.2
            elif any(word in candidate["application"].lower()
                    for word in query_application.lower().split()):
                score += 0.1

        return min(score, 1.0)
