"""
Similarity Engine

Calculates similarity between failures for pattern matching.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import math


@dataclass
class SimilarityResult:
    """Result of similarity calculation"""
    overall_score: float
    part_similarity: float
    mode_similarity: float
    condition_similarity: float
    application_similarity: float
    matching_factors: List[str]


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


class SimilarityEngine:
    """
    Calculates similarity between failures for pattern matching.

    Similarity factors:
    - Part type and specifications
    - Failure mode
    - Operating conditions
    - Application context
    - Time-to-failure
    """

    # Weights for different similarity components
    WEIGHTS = {
        "part_type": 0.25,
        "part_spec": 0.15,
        "failure_mode": 0.25,
        "application": 0.15,
        "conditions": 0.10,
        "time_to_failure": 0.10,
    }

    # Part type synonyms for fuzzy matching
    PART_SYNONYMS = {
        "bolt": ["screw", "fastener", "cap screw", "stud"],
        "screw": ["bolt", "fastener", "cap screw"],
        "bearing": ["bushing", "sleeve"],
        "seal": ["o-ring", "gasket"],
    }

    def __init__(self):
        """Initialize similarity engine."""
        pass

    def calculate_similarity(
        self,
        failure_a: Dict[str, Any],
        failure_b: Dict[str, Any]
    ) -> SimilarityResult:
        """
        Calculate overall similarity between two failures.

        Args:
            failure_a: First failure record
            failure_b: Second failure record

        Returns:
            Detailed similarity result
        """
        # Calculate component similarities
        part_sim = self._part_type_similarity(
            failure_a.get("part_type", ""),
            failure_b.get("part_type", "")
        )

        spec_sim = self._specification_similarity(
            failure_a.get("part_spec", ""),
            failure_b.get("part_spec", "")
        )

        mode_sim = self._failure_mode_similarity(
            failure_a.get("failure_mode", ""),
            failure_b.get("failure_mode", "")
        )

        app_sim = self._application_similarity(
            failure_a.get("application", ""),
            failure_b.get("application", "")
        )

        cond_sim = self._conditions_similarity(
            failure_a.get("conditions", {}),
            failure_b.get("conditions", {})
        )

        time_sim = self._time_to_failure_similarity(
            failure_a.get("time_to_failure", 0),
            failure_b.get("time_to_failure", 0)
        )

        # Calculate weighted overall score
        overall = (
            part_sim * self.WEIGHTS["part_type"] +
            spec_sim * self.WEIGHTS["part_spec"] +
            mode_sim * self.WEIGHTS["failure_mode"] +
            app_sim * self.WEIGHTS["application"] +
            cond_sim * self.WEIGHTS["conditions"] +
            time_sim * self.WEIGHTS["time_to_failure"]
        )

        # Identify matching factors
        matching_factors = []
        if part_sim > 0.8:
            matching_factors.append("Same part type")
        if mode_sim > 0.9:
            matching_factors.append("Same failure mode")
        if app_sim > 0.7:
            matching_factors.append("Similar application")

        return SimilarityResult(
            overall_score=overall,
            part_similarity=part_sim,
            mode_similarity=mode_sim,
            condition_similarity=cond_sim,
            application_similarity=app_sim,
            matching_factors=matching_factors
        )

    def find_most_similar(
        self,
        target: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        threshold: float = 0.5,
        max_results: int = 10
    ) -> List[tuple[Dict[str, Any], SimilarityResult]]:
        """
        Find most similar failures from a list of candidates.

        Args:
            target: Target failure to match
            candidates: List of candidate failures
            threshold: Minimum similarity threshold
            max_results: Maximum results to return

        Returns:
            List of (candidate, similarity_result) tuples, sorted by score
        """
        results = []

        for candidate in candidates:
            similarity = self.calculate_similarity(target, candidate)
            if similarity.overall_score >= threshold:
                results.append((candidate, similarity))

        # Sort by overall score descending
        results.sort(key=lambda x: x[1].overall_score, reverse=True)

        return results[:max_results]

    def _part_type_similarity(self, type_a: str, type_b: str) -> float:
        """Calculate part type similarity with fuzzy matching."""
        if not type_a or not type_b:
            return 0.0

        type_a = type_a.lower()
        type_b = type_b.lower()

        # Exact match
        if type_a == type_b:
            return 1.0

        # Check synonyms
        for base_type, synonyms in self.PART_SYNONYMS.items():
            a_match = type_a == base_type or type_a in synonyms
            b_match = type_b == base_type or type_b in synonyms
            if a_match and b_match:
                return 0.9

        # Partial word match
        words_a = set(type_a.split())
        words_b = set(type_b.split())
        intersection = words_a & words_b
        union = words_a | words_b

        if union:
            return len(intersection) / len(union)

        return 0.0

    def _specification_similarity(self, spec_a: str, spec_b: str) -> float:
        """Calculate specification similarity."""
        if not spec_a or not spec_b:
            return 0.0

        spec_a = spec_a.lower()
        spec_b = spec_b.lower()

        # Exact match
        if spec_a == spec_b:
            return 1.0

        # Extract key spec components
        def extract_components(spec):
            components = {}
            # Look for metric sizes (M8, M10, etc.)
            import re
            size_match = re.search(r'm(\d+)', spec.lower())
            if size_match:
                components['size'] = int(size_match.group(1))
            # Look for grades (8.8, 10.9, 12.9)
            grade_match = re.search(r'(\d+\.\d+)', spec)
            if grade_match:
                components['grade'] = float(grade_match.group(1))
            return components

        comp_a = extract_components(spec_a)
        comp_b = extract_components(spec_b)

        score = 0.0
        count = 0

        # Compare sizes
        if 'size' in comp_a and 'size' in comp_b:
            count += 1
            if comp_a['size'] == comp_b['size']:
                score += 1.0
            elif abs(comp_a['size'] - comp_b['size']) <= 2:
                score += 0.7

        # Compare grades
        if 'grade' in comp_a and 'grade' in comp_b:
            count += 1
            if comp_a['grade'] == comp_b['grade']:
                score += 1.0
            elif abs(comp_a['grade'] - comp_b['grade']) <= 2:
                score += 0.6

        return score / max(count, 1)

    def _failure_mode_similarity(self, mode_a: str, mode_b: str) -> float:
        """Calculate failure mode similarity."""
        if not mode_a or not mode_b:
            return 0.0

        mode_a = mode_a.lower()
        mode_b = mode_b.lower()

        # Exact match
        if mode_a == mode_b:
            return 1.0

        # Related modes
        related_modes = {
            "high_cycle_fatigue": ["fatigue", "cyclic", "vibration"],
            "low_cycle_fatigue": ["fatigue", "thermal_fatigue"],
            "hydrogen_embrittlement": ["brittle", "embrittlement", "delayed_fracture"],
            "galvanic_corrosion": ["corrosion", "electrochemical"],
            "stress_corrosion_cracking": ["corrosion", "cracking", "scc"],
        }

        for mode, related in related_modes.items():
            if (mode in mode_a or any(r in mode_a for r in related)) and \
               (mode in mode_b or any(r in mode_b for r in related)):
                return 0.8

        # Check if modes share any words
        words_a = set(mode_a.replace("_", " ").split())
        words_b = set(mode_b.replace("_", " ").split())
        if words_a & words_b:
            return 0.5

        return 0.0

    def _application_similarity(self, app_a: str, app_b: str) -> float:
        """Calculate application similarity."""
        if not app_a or not app_b:
            return 0.0

        app_a = app_a.lower()
        app_b = app_b.lower()

        # Exact match
        if app_a == app_b:
            return 1.0

        # Related applications
        app_groups = {
            "automotive": ["engine", "suspension", "drivetrain", "vehicle", "car", "truck"],
            "industrial": ["cnc", "machine", "equipment", "manufacturing", "factory"],
            "aerospace": ["aircraft", "aviation", "flight", "aerospace"],
            "marine": ["boat", "ship", "marine", "nautical"],
        }

        for group, keywords in app_groups.items():
            a_match = any(k in app_a for k in keywords)
            b_match = any(k in app_b for k in keywords)
            if a_match and b_match:
                return 0.7

        return 0.0

    def _conditions_similarity(
        self,
        cond_a: Dict[str, Any],
        cond_b: Dict[str, Any]
    ) -> float:
        """Calculate operating conditions similarity."""
        if not cond_a or not cond_b:
            return 0.5  # Neutral if no data

        score = 0.0
        count = 0

        # Compare temperature ranges
        if 'temperature_c' in cond_a and 'temperature_c' in cond_b:
            count += 1
            diff = abs(cond_a['temperature_c'] - cond_b['temperature_c'])
            score += max(0, 1.0 - diff / 100)

        # Compare vibration levels
        if 'vibration_level' in cond_a and 'vibration_level' in cond_b:
            count += 1
            if cond_a['vibration_level'] == cond_b['vibration_level']:
                score += 1.0

        # Compare load conditions
        if 'load' in cond_a and 'load' in cond_b:
            count += 1
            if cond_a['load'] == cond_b['load']:
                score += 1.0

        return score / max(count, 1)

    def _time_to_failure_similarity(
        self,
        time_a: float,
        time_b: float
    ) -> float:
        """Calculate time-to-failure similarity."""
        if time_a <= 0 or time_b <= 0:
            return 0.5  # Neutral if no data

        # Use logarithmic scale for comparison
        log_a = math.log10(max(time_a, 1))
        log_b = math.log10(max(time_b, 1))

        diff = abs(log_a - log_b)

        # Within same order of magnitude is similar
        if diff < 0.3:
            return 1.0
        elif diff < 0.5:
            return 0.8
        elif diff < 1.0:
            return 0.5
        else:
            return 0.2
