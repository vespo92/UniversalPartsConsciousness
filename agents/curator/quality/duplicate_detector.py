"""
Agent_1 (ARCHIVIST) - Duplicate Detection System
=================================================
"One truth, many names. The Archivist sees through illusion."

Multi-factor duplicate detection ensures the Universal Parts Consciousness
maintains a single, authoritative record for each unique part across
all data sources.
"""

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from ..scrapers.base_scraper import ScrapedPart


class DuplicateConfidence(Enum):
    """Confidence levels for duplicate detection."""
    DEFINITE = "definite"       # 95%+ match - auto-merge
    PROBABLE = "probable"       # 80-95% match - suggest merge
    POSSIBLE = "possible"       # 60-80% match - manual review
    UNLIKELY = "unlikely"       # 40-60% match - probably different
    DISTINCT = "distinct"       # <40% match - definitely different


@dataclass
class MatchFactor:
    """A single factor in duplicate matching."""
    name: str
    weight: float
    score: float  # 0.0 to 1.0
    matched_values: Tuple[Any, Any] = (None, None)
    details: str = ""

    @property
    def weighted_score(self) -> float:
        return self.weight * self.score


@dataclass
class DuplicateMatch:
    """Result of comparing two parts for duplication."""
    part_a: ScrapedPart
    part_b: ScrapedPart
    overall_score: float
    confidence: DuplicateConfidence
    factors: List[MatchFactor] = field(default_factory=list)
    recommended_action: str = "none"
    merged_part: Optional[ScrapedPart] = None

    @property
    def is_duplicate(self) -> bool:
        return self.confidence in [DuplicateConfidence.DEFINITE, DuplicateConfidence.PROBABLE]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_a_id": self.part_a.source_id,
            "part_b_id": self.part_b.source_id,
            "overall_score": round(self.overall_score, 4),
            "confidence": self.confidence.value,
            "factors": [
                {
                    "name": f.name,
                    "weight": f.weight,
                    "score": round(f.score, 4),
                    "weighted_score": round(f.weighted_score, 4),
                    "details": f.details,
                }
                for f in self.factors
            ],
            "recommended_action": self.recommended_action,
        }


@dataclass
class DuplicateGroup:
    """A group of parts identified as duplicates."""
    canonical_part: ScrapedPart  # The authoritative version
    duplicates: List[ScrapedPart] = field(default_factory=list)
    sources: Set[str] = field(default_factory=set)
    match_scores: Dict[str, float] = field(default_factory=dict)

    @property
    def source_count(self) -> int:
        return len(self.sources)

    def add_duplicate(self, part: ScrapedPart, score: float) -> None:
        self.duplicates.append(part)
        self.sources.add(part.source_name)
        self.match_scores[part.source_id] = score


class DuplicateDetector:
    """
    Multi-factor duplicate detection using weighted scoring.

    Per Agent_1 specification:
    - Thread specification match: 30% weight
    - Dimensional tolerance overlap: 25% weight
    - Material composition match: 20% weight
    - Part number pattern analysis: 15% weight
    - Supplier cross-reference: 10% weight
    """

    # Default weights per specification
    DEFAULT_WEIGHTS = {
        "thread_spec": 0.30,
        "dimensions": 0.25,
        "material": 0.20,
        "part_number": 0.15,
        "cross_reference": 0.10,
    }

    # Confidence thresholds
    DEFINITE_THRESHOLD = 0.95
    PROBABLE_THRESHOLD = 0.80
    POSSIBLE_THRESHOLD = 0.60
    UNLIKELY_THRESHOLD = 0.40

    # Thread normalization patterns
    METRIC_PATTERN = re.compile(r'M(\d+(?:\.\d+)?)[x×-]?(\d+(?:\.\d+)?)?')
    UNIFIED_PATTERN = re.compile(r'(?:(\d+/\d+)|#(\d+))-(\d+)')

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        length_tolerance_pct: float = 0.02,  # 2% tolerance
        diameter_tolerance_pct: float = 0.02,
        use_fuzzy_matching: bool = True,
    ):
        """
        Initialize the duplicate detector.

        Args:
            weights: Custom factor weights (must sum to 1.0)
            length_tolerance_pct: Tolerance for length comparison
            diameter_tolerance_pct: Tolerance for diameter comparison
            use_fuzzy_matching: Enable fuzzy string matching
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self.length_tolerance_pct = length_tolerance_pct
        self.diameter_tolerance_pct = diameter_tolerance_pct
        self.use_fuzzy_matching = use_fuzzy_matching

        # Normalize weights
        total = sum(self.weights.values())
        if total != 1.0:
            self.weights = {k: v / total for k, v in self.weights.items()}

    def compare(self, part_a: ScrapedPart, part_b: ScrapedPart) -> DuplicateMatch:
        """
        Compare two parts for potential duplication.

        Args:
            part_a: First part to compare
            part_b: Second part to compare

        Returns:
            DuplicateMatch with detailed comparison results
        """
        factors = []

        # Factor 1: Thread specification match (30%)
        thread_factor = self._compare_thread_specs(part_a, part_b)
        factors.append(thread_factor)

        # Factor 2: Dimensional tolerance overlap (25%)
        dimension_factor = self._compare_dimensions(part_a, part_b)
        factors.append(dimension_factor)

        # Factor 3: Material composition match (20%)
        material_factor = self._compare_materials(part_a, part_b)
        factors.append(material_factor)

        # Factor 4: Part number pattern analysis (15%)
        part_number_factor = self._compare_part_numbers(part_a, part_b)
        factors.append(part_number_factor)

        # Factor 5: Supplier cross-reference (10%)
        cross_ref_factor = self._compare_cross_references(part_a, part_b)
        factors.append(cross_ref_factor)

        # Calculate overall score
        overall_score = sum(f.weighted_score for f in factors)

        # Determine confidence level
        if overall_score >= self.DEFINITE_THRESHOLD:
            confidence = DuplicateConfidence.DEFINITE
            action = "auto_merge"
        elif overall_score >= self.PROBABLE_THRESHOLD:
            confidence = DuplicateConfidence.PROBABLE
            action = "suggest_merge"
        elif overall_score >= self.POSSIBLE_THRESHOLD:
            confidence = DuplicateConfidence.POSSIBLE
            action = "manual_review"
        elif overall_score >= self.UNLIKELY_THRESHOLD:
            confidence = DuplicateConfidence.UNLIKELY
            action = "likely_distinct"
        else:
            confidence = DuplicateConfidence.DISTINCT
            action = "none"

        match = DuplicateMatch(
            part_a=part_a,
            part_b=part_b,
            overall_score=overall_score,
            confidence=confidence,
            factors=factors,
            recommended_action=action,
        )

        # Create merged part for definite duplicates
        if confidence == DuplicateConfidence.DEFINITE:
            match.merged_part = self._merge_parts(part_a, part_b)

        return match

    def _compare_thread_specs(self, part_a: ScrapedPart, part_b: ScrapedPart) -> MatchFactor:
        """Compare thread specifications."""
        weight = self.weights["thread_spec"]

        if not part_a.thread_spec or not part_b.thread_spec:
            return MatchFactor(
                name="thread_spec",
                weight=weight,
                score=0.0,
                matched_values=(part_a.thread_spec, part_b.thread_spec),
                details="One or both parts missing thread specification",
            )

        # Normalize thread specs
        norm_a = self._normalize_thread_spec(part_a.thread_spec)
        norm_b = self._normalize_thread_spec(part_b.thread_spec)

        if norm_a == norm_b:
            return MatchFactor(
                name="thread_spec",
                weight=weight,
                score=1.0,
                matched_values=(part_a.thread_spec, part_b.thread_spec),
                details=f"Exact match after normalization: {norm_a}",
            )

        # Check for equivalent threads (e.g., M6 coarse vs M6x1.0)
        equiv_score = self._check_thread_equivalence(norm_a, norm_b)
        if equiv_score > 0:
            return MatchFactor(
                name="thread_spec",
                weight=weight,
                score=equiv_score,
                matched_values=(part_a.thread_spec, part_b.thread_spec),
                details=f"Equivalent threads: {norm_a} ~ {norm_b}",
            )

        return MatchFactor(
            name="thread_spec",
            weight=weight,
            score=0.0,
            matched_values=(part_a.thread_spec, part_b.thread_spec),
            details=f"No match: {norm_a} vs {norm_b}",
        )

    def _normalize_thread_spec(self, thread_spec: str) -> str:
        """Normalize thread specification to standard format."""
        spec = thread_spec.strip().upper()

        # Try metric format
        metric_match = self.METRIC_PATTERN.search(spec)
        if metric_match:
            diameter = metric_match.group(1)
            pitch = metric_match.group(2)
            if pitch:
                return f"M{diameter}x{pitch}"
            return f"M{diameter}"

        # Try unified format
        unified_match = self.UNIFIED_PATTERN.search(spec)
        if unified_match:
            if unified_match.group(1):  # Fractional
                return f"{unified_match.group(1)}-{unified_match.group(3)}"
            else:  # Numbered
                return f"#{unified_match.group(2)}-{unified_match.group(3)}"

        # Return cleaned original
        return re.sub(r'\s+', '', spec)

    def _check_thread_equivalence(self, thread_a: str, thread_b: str) -> float:
        """Check if two threads are equivalent (e.g., M6 vs M6x1.0)."""
        # Metric coarse pitch equivalents
        metric_coarse_pitches = {
            "M1.6": "0.35", "M2": "0.4", "M2.5": "0.45", "M3": "0.5",
            "M4": "0.7", "M5": "0.8", "M6": "1.0", "M8": "1.25",
            "M10": "1.5", "M12": "1.75", "M16": "2.0", "M20": "2.5",
            "M24": "3.0", "M30": "3.5", "M36": "4.0",
        }

        # Check if one has pitch and other doesn't
        metric_a = self.METRIC_PATTERN.match(thread_a)
        metric_b = self.METRIC_PATTERN.match(thread_b)

        if metric_a and metric_b:
            dia_a = metric_a.group(1)
            dia_b = metric_b.group(1)
            pitch_a = metric_a.group(2)
            pitch_b = metric_b.group(2)

            if dia_a == dia_b:
                # Same diameter
                if pitch_a and pitch_b:
                    return 0.0  # Both have pitch but different
                elif pitch_a or pitch_b:
                    # One has pitch, check if it's coarse
                    pitch = pitch_a or pitch_b
                    coarse_pitch = metric_coarse_pitches.get(f"M{dia_a}")
                    if coarse_pitch and pitch == coarse_pitch:
                        return 0.95  # Very likely the same
                    return 0.7  # Possibly the same

        return 0.0

    def _compare_dimensions(self, part_a: ScrapedPart, part_b: ScrapedPart) -> MatchFactor:
        """Compare length and diameter dimensions."""
        weight = self.weights["dimensions"]
        scores = []
        details = []

        # Compare lengths
        if part_a.length is not None and part_b.length is not None:
            length_diff = abs(part_a.length - part_b.length)
            avg_length = (part_a.length + part_b.length) / 2
            tolerance = avg_length * self.length_tolerance_pct

            if length_diff <= tolerance:
                scores.append(1.0)
                details.append(f"Length match: {part_a.length}mm ~ {part_b.length}mm")
            elif length_diff <= tolerance * 2:
                scores.append(0.5)
                details.append(f"Length close: {part_a.length}mm vs {part_b.length}mm")
            else:
                scores.append(0.0)
                details.append(f"Length mismatch: {part_a.length}mm vs {part_b.length}mm")

        # Compare diameters
        if part_a.diameter is not None and part_b.diameter is not None:
            dia_diff = abs(part_a.diameter - part_b.diameter)
            avg_dia = (part_a.diameter + part_b.diameter) / 2
            tolerance = avg_dia * self.diameter_tolerance_pct

            if dia_diff <= tolerance:
                scores.append(1.0)
                details.append(f"Diameter match: {part_a.diameter}mm ~ {part_b.diameter}mm")
            elif dia_diff <= tolerance * 2:
                scores.append(0.5)
                details.append(f"Diameter close: {part_a.diameter}mm vs {part_b.diameter}mm")
            else:
                scores.append(0.0)
                details.append(f"Diameter mismatch: {part_a.diameter}mm vs {part_b.diameter}mm")

        if not scores:
            return MatchFactor(
                name="dimensions",
                weight=weight,
                score=0.0,
                matched_values=((part_a.length, part_a.diameter), (part_b.length, part_b.diameter)),
                details="Missing dimension data for comparison",
            )

        avg_score = sum(scores) / len(scores)
        return MatchFactor(
            name="dimensions",
            weight=weight,
            score=avg_score,
            matched_values=((part_a.length, part_a.diameter), (part_b.length, part_b.diameter)),
            details="; ".join(details),
        )

    def _compare_materials(self, part_a: ScrapedPart, part_b: ScrapedPart) -> MatchFactor:
        """Compare material compositions."""
        weight = self.weights["material"]

        if not part_a.material or not part_b.material:
            return MatchFactor(
                name="material",
                weight=weight,
                score=0.0,
                matched_values=(part_a.material, part_b.material),
                details="One or both parts missing material specification",
            )

        # Normalize materials
        mat_a = self._normalize_material(part_a.material)
        mat_b = self._normalize_material(part_b.material)

        if mat_a == mat_b:
            return MatchFactor(
                name="material",
                weight=weight,
                score=1.0,
                matched_values=(part_a.material, part_b.material),
                details=f"Exact material match: {mat_a}",
            )

        # Check for material equivalents
        equiv_score = self._check_material_equivalence(mat_a, mat_b)
        if equiv_score > 0:
            return MatchFactor(
                name="material",
                weight=weight,
                score=equiv_score,
                matched_values=(part_a.material, part_b.material),
                details=f"Equivalent materials: {mat_a} ~ {mat_b}",
            )

        # Check material grades
        if part_a.material_grade and part_b.material_grade:
            grade_a = part_a.material_grade.upper()
            grade_b = part_b.material_grade.upper()
            if grade_a == grade_b:
                return MatchFactor(
                    name="material",
                    weight=weight,
                    score=0.7,
                    matched_values=(part_a.material, part_b.material),
                    details=f"Grade match ({grade_a}) with different material names",
                )

        return MatchFactor(
            name="material",
            weight=weight,
            score=0.0,
            matched_values=(part_a.material, part_b.material),
            details=f"No match: {mat_a} vs {mat_b}",
        )

    def _normalize_material(self, material: str) -> str:
        """Normalize material name."""
        mat = material.strip().lower()

        # Common normalizations
        mat = re.sub(r'\s+', ' ', mat)
        mat = re.sub(r'stainless\s*steel', 'stainless', mat)
        mat = re.sub(r'alloy\s*steel', 'alloy', mat)
        mat = re.sub(r'carbon\s*steel', 'carbon', mat)

        return mat

    def _check_material_equivalence(self, mat_a: str, mat_b: str) -> float:
        """Check if two materials are equivalent."""
        # Material equivalence groups
        equivalents = {
            frozenset(["18-8 stainless", "304 stainless", "a2 stainless"]): 0.95,
            frozenset(["316 stainless", "a4 stainless"]): 0.95,
            frozenset(["grade 8", "alloy", "10.9"]): 0.9,
            frozenset(["grade 5", "8.8"]): 0.9,
            frozenset(["grade 2", "4.6", "low carbon"]): 0.85,
        }

        mat_a_lower = mat_a.lower()
        mat_b_lower = mat_b.lower()

        for equiv_group, score in equivalents.items():
            matches_a = any(e in mat_a_lower for e in equiv_group)
            matches_b = any(e in mat_b_lower for e in equiv_group)
            if matches_a and matches_b:
                return score

        # Partial match (same base material)
        if mat_a.split()[0] == mat_b.split()[0]:
            return 0.5

        return 0.0

    def _compare_part_numbers(self, part_a: ScrapedPart, part_b: ScrapedPart) -> MatchFactor:
        """Analyze part number patterns for similarity."""
        weight = self.weights["part_number"]

        # Extract numeric patterns
        nums_a = re.findall(r'\d+', part_a.source_id)
        nums_b = re.findall(r'\d+', part_b.source_id)

        if not nums_a or not nums_b:
            return MatchFactor(
                name="part_number",
                weight=weight,
                score=0.0,
                matched_values=(part_a.source_id, part_b.source_id),
                details="Cannot extract numeric patterns",
            )

        # Check for common sequence patterns
        common_nums = set(nums_a) & set(nums_b)
        if common_nums:
            # Significant number overlap
            overlap_ratio = len(common_nums) / max(len(nums_a), len(nums_b))
            if overlap_ratio >= 0.5:
                return MatchFactor(
                    name="part_number",
                    weight=weight,
                    score=0.6 + (overlap_ratio * 0.4),
                    matched_values=(part_a.source_id, part_b.source_id),
                    details=f"Common numeric patterns: {common_nums}",
                )

        # Check if same source with different variants
        if part_a.source_name == part_b.source_name:
            # Same supplier - check for variant patterns
            prefix_a = re.match(r'^([A-Z]+\d+)', part_a.source_id.upper())
            prefix_b = re.match(r'^([A-Z]+\d+)', part_b.source_id.upper())

            if prefix_a and prefix_b and prefix_a.group(1) == prefix_b.group(1):
                return MatchFactor(
                    name="part_number",
                    weight=weight,
                    score=0.5,
                    matched_values=(part_a.source_id, part_b.source_id),
                    details=f"Same product family prefix: {prefix_a.group(1)}",
                )

        return MatchFactor(
            name="part_number",
            weight=weight,
            score=0.0,
            matched_values=(part_a.source_id, part_b.source_id),
            details="No pattern similarity detected",
        )

    def _compare_cross_references(self, part_a: ScrapedPart, part_b: ScrapedPart) -> MatchFactor:
        """Check for cross-reference information."""
        weight = self.weights["cross_reference"]

        # Check if parts reference each other
        raw_a = part_a.raw_data
        raw_b = part_b.raw_data

        # Look for cross-reference fields
        xref_a = raw_a.get("cross_references", [])
        xref_b = raw_b.get("cross_references", [])

        if part_b.source_id in xref_a or part_a.source_id in xref_b:
            return MatchFactor(
                name="cross_reference",
                weight=weight,
                score=1.0,
                matched_values=(xref_a, xref_b),
                details="Direct cross-reference found",
            )

        # Check for common cross-references
        if xref_a and xref_b:
            common_refs = set(xref_a) & set(xref_b)
            if common_refs:
                return MatchFactor(
                    name="cross_reference",
                    weight=weight,
                    score=0.8,
                    matched_values=(xref_a, xref_b),
                    details=f"Common cross-references: {common_refs}",
                )

        # Check manufacturer match
        if part_a.manufacturer and part_b.manufacturer:
            if part_a.manufacturer.lower() == part_b.manufacturer.lower():
                return MatchFactor(
                    name="cross_reference",
                    weight=weight,
                    score=0.5,
                    matched_values=(part_a.manufacturer, part_b.manufacturer),
                    details=f"Same manufacturer: {part_a.manufacturer}",
                )

        return MatchFactor(
            name="cross_reference",
            weight=weight,
            score=0.0,
            matched_values=(None, None),
            details="No cross-reference data available",
        )

    def _merge_parts(self, part_a: ScrapedPart, part_b: ScrapedPart) -> ScrapedPart:
        """
        Merge two duplicate parts into a canonical record.

        Strategy: Prefer data from higher-quality source, combine unique info.
        """
        # Determine which part has higher quality
        primary = part_a if part_a.quality_score >= part_b.quality_score else part_b
        secondary = part_b if primary == part_a else part_a

        # Create merged part starting from primary
        merged = ScrapedPart(
            source_id=primary.source_id,
            source_name=primary.source_name,
            upc_id=primary.upc_id or primary.generate_upc_id(),
        )

        # Merge fields, preferring non-None values
        def prefer_primary(field_name: str):
            primary_val = getattr(primary, field_name)
            secondary_val = getattr(secondary, field_name)
            return primary_val if primary_val is not None else secondary_val

        merged.thread_spec = prefer_primary("thread_spec")
        merged.length = prefer_primary("length")
        merged.diameter = prefer_primary("diameter")
        merged.material = prefer_primary("material")
        merged.material_grade = prefer_primary("material_grade")
        merged.head_type = prefer_primary("head_type")
        merged.drive_type = prefer_primary("drive_type")
        merged.drive_size = prefer_primary("drive_size")
        merged.tensile_strength = prefer_primary("tensile_strength")
        merged.yield_strength = prefer_primary("yield_strength")
        merged.hardness = prefer_primary("hardness")
        merged.category = prefer_primary("category")
        merged.subcategory = prefer_primary("subcategory")
        merged.description = prefer_primary("description")
        merged.manufacturer = prefer_primary("manufacturer")
        merged.price = prefer_primary("price")
        merged.availability = prefer_primary("availability")
        merged.datasheet_url = prefer_primary("datasheet_url")

        # Merge lists/dicts
        merged.cad_urls = {**secondary.cad_urls, **primary.cad_urls}
        merged.image_urls = list(set(primary.image_urls + secondary.image_urls))

        # Increment verification count
        merged.verification_count = primary.verification_count + secondary.verification_count + 1

        # Store merge metadata
        merged.raw_data = {
            "merged_from": [primary.source_id, secondary.source_id],
            "merge_sources": [primary.source_name, secondary.source_name],
        }

        return merged

    def find_duplicates(
        self,
        parts: List[ScrapedPart],
        threshold: float = 0.80,
    ) -> List[DuplicateMatch]:
        """
        Find all duplicate pairs in a list of parts.

        Args:
            parts: List of parts to check
            threshold: Minimum score to consider as duplicate

        Returns:
            List of duplicate matches above threshold
        """
        duplicates = []

        for i, part_a in enumerate(parts):
            for part_b in parts[i + 1:]:
                match = self.compare(part_a, part_b)
                if match.overall_score >= threshold:
                    duplicates.append(match)

        # Sort by score descending
        duplicates.sort(key=lambda m: m.overall_score, reverse=True)
        return duplicates

    def group_duplicates(
        self,
        parts: List[ScrapedPart],
        threshold: float = 0.80,
    ) -> List[DuplicateGroup]:
        """
        Group parts into duplicate clusters.

        Args:
            parts: List of parts to cluster
            threshold: Minimum score for grouping

        Returns:
            List of duplicate groups
        """
        # Use union-find for grouping
        parent = {part.source_id: part.source_id for part in parts}
        parts_by_id = {part.source_id: part for part in parts}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py

        # Find all duplicate pairs
        for i, part_a in enumerate(parts):
            for part_b in parts[i + 1:]:
                match = self.compare(part_a, part_b)
                if match.overall_score >= threshold:
                    union(part_a.source_id, part_b.source_id)

        # Build groups
        groups_dict: Dict[str, DuplicateGroup] = {}

        for part in parts:
            root = find(part.source_id)
            if root not in groups_dict:
                groups_dict[root] = DuplicateGroup(
                    canonical_part=parts_by_id[root],
                )
                groups_dict[root].sources.add(parts_by_id[root].source_name)

            if part.source_id != root:
                match = self.compare(groups_dict[root].canonical_part, part)
                groups_dict[root].add_duplicate(part, match.overall_score)

        # Only return groups with duplicates
        return [g for g in groups_dict.values() if g.duplicates]


def find_duplicates(
    parts: List[ScrapedPart],
    threshold: float = 0.80,
) -> List[DuplicateMatch]:
    """Convenience function to find duplicates."""
    detector = DuplicateDetector()
    return detector.find_duplicates(parts, threshold)


def group_duplicates(
    parts: List[ScrapedPart],
    threshold: float = 0.80,
) -> List[DuplicateGroup]:
    """Convenience function to group duplicates."""
    detector = DuplicateDetector()
    return detector.group_duplicates(parts, threshold)


__all__ = [
    "DuplicateDetector",
    "DuplicateMatch",
    "DuplicateGroup",
    "DuplicateConfidence",
    "MatchFactor",
    "find_duplicates",
    "group_duplicates",
]
