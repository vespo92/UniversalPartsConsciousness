"""
Layer 2: Behavioral Pattern Detection
Extracts success formulas, failure mode clustering, longevity factors, and outliers.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import math

from ..types import (
    DetectedPattern,
    PatternLayer,
    FailureRecord,
    Assembly,
    SuccessFormula,
)


logger = logging.getLogger(__name__)


@dataclass
class BehavioralConfig:
    """Configuration for behavioral pattern detection"""
    min_cluster_size: int = 5
    similarity_threshold: float = 0.75
    success_rate_threshold: float = 0.85
    outlier_z_threshold: float = 2.0
    longevity_percentile: float = 0.9


class BehavioralPatternDetector:
    """
    Layer 2: Behavioral Pattern Detection

    Detects:
    - Success formula extraction (what makes things work)
    - Failure mode clustering (common ways things break)
    - Longevity factors (what makes parts last)
    - Performance outliers (unexpectedly good/bad performers)
    """

    def __init__(self, config: Optional[BehavioralConfig] = None):
        self.config = config or BehavioralConfig()

    @property
    def layer(self) -> PatternLayer:
        return PatternLayer.BEHAVIORAL

    def detect(self, data: Dict[str, Any]) -> List[DetectedPattern]:
        """Detect behavioral patterns from assemblies and failures"""
        patterns = []

        assemblies = data.get("assemblies", [])
        failure_records = data.get("failure_records", [])
        swarm_knowledge = data.get("swarm_knowledge", {})

        # Extract success formulas
        success_patterns = self._extract_success_formulas(assemblies)
        patterns.extend(success_patterns)

        # Cluster failure modes
        failure_clusters = self._cluster_failure_modes(failure_records)
        patterns.extend(failure_clusters)

        # Identify longevity factors
        longevity_patterns = self._identify_longevity_factors(assemblies, failure_records)
        patterns.extend(longevity_patterns)

        # Find performance outliers
        outliers = self._detect_performance_outliers(assemblies, failure_records)
        patterns.extend(outliers)

        return patterns

    def _extract_success_formulas(
        self,
        assemblies: List[Assembly],
    ) -> List[DetectedPattern]:
        """Extract patterns from successful assemblies"""
        patterns = []

        if len(assemblies) < 10:
            return patterns

        # Separate successful and failed assemblies
        successful = [a for a in assemblies if a.success]
        failed = [a for a in assemblies if not a.success]

        if len(successful) < 5:
            return patterns

        # Group by domain
        by_domain: Dict[str, List[Assembly]] = defaultdict(list)
        for assembly in successful:
            by_domain[assembly.domain].append(assembly)

        for domain, domain_assemblies in by_domain.items():
            if len(domain_assemblies) < 5:
                continue

            # Find common part combinations
            formulas = self._find_common_combinations(domain_assemblies, failed)

            for formula in formulas:
                success_rate = formula["success_rate"]
                if success_rate >= self.config.success_rate_threshold:
                    pattern = DetectedPattern(
                        layer=PatternLayer.BEHAVIORAL,
                        pattern_type="success_formula",
                        category="success",
                        name=f"The {domain.replace('_', ' ').title()} Formula",
                        description=(
                            f"Success formula for {domain}: "
                            f"{success_rate:.0%} success rate with "
                            f"{len(formula['required_parts'])} key components"
                        ),
                        significance_score=Decimal(str(success_rate)),
                        evidence={
                            "domain": domain,
                            "required_parts": formula["required_parts"],
                            "optional_parts": formula.get("optional_parts", []),
                            "forbidden_parts": formula.get("forbidden_parts", []),
                            "success_rate": success_rate,
                            "sample_size": formula["sample_size"],
                            "average_lifespan": formula.get("average_lifespan"),
                        },
                        sample_size=formula["sample_size"],
                        confidence=Decimal(str(min(success_rate, 0.95))),
                    )
                    patterns.append(pattern)

        return patterns

    def _cluster_failure_modes(
        self,
        failures: List[FailureRecord],
    ) -> List[DetectedPattern]:
        """Cluster failures into common failure modes"""
        patterns = []

        if len(failures) < 10:
            return patterns

        # Group by failure mode
        by_mode: Dict[str, List[FailureRecord]] = defaultdict(list)
        for failure in failures:
            by_mode[failure.failure_mode].append(failure)

        # Analyze each cluster
        for mode, mode_failures in by_mode.items():
            if len(mode_failures) < self.config.min_cluster_size:
                continue

            # Find common characteristics
            characteristics = self._extract_cluster_characteristics(mode_failures)

            # Calculate cluster coherence
            coherence = self._calculate_cluster_coherence(mode_failures)

            if coherence > self.config.similarity_threshold:
                pattern = DetectedPattern(
                    layer=PatternLayer.BEHAVIORAL,
                    pattern_type="failure_cluster",
                    category="failure",
                    name=f"Failure Cluster: {mode}",
                    description=(
                        f"Identified {len(mode_failures)} failures with mode '{mode}' "
                        f"sharing {len(characteristics)} common characteristics"
                    ),
                    significance_score=Decimal(str(coherence)),
                    evidence={
                        "failure_mode": mode,
                        "count": len(mode_failures),
                        "common_characteristics": characteristics,
                        "coherence": coherence,
                        "affected_part_types": list(set(
                            f.part_type for f in mode_failures
                        )),
                    },
                    sample_size=len(mode_failures),
                    confidence=Decimal(str(coherence * 0.9)),
                )
                patterns.append(pattern)

        return patterns

    def _identify_longevity_factors(
        self,
        assemblies: List[Assembly],
        failures: List[FailureRecord],
    ) -> List[DetectedPattern]:
        """Identify factors that contribute to long part life"""
        patterns = []

        # Get parts with known lifespans
        lifespans: Dict[str, List[int]] = defaultdict(list)
        for assembly in assemblies:
            if assembly.lifespan_hours:
                for part in assembly.parts:
                    lifespans[part].append(assembly.lifespan_hours)

        if not lifespans:
            return patterns

        # Calculate lifespan statistics
        all_lifespans = [ls for lss in lifespans.values() for ls in lss]
        if not all_lifespans:
            return patterns

        avg_lifespan = sum(all_lifespans) / len(all_lifespans)
        long_life_threshold = sorted(all_lifespans)[
            int(len(all_lifespans) * self.config.longevity_percentile)
        ]

        # Find factors common in long-lived assemblies
        long_lived = [
            a for a in assemblies
            if a.lifespan_hours and a.lifespan_hours >= long_life_threshold
        ]

        if len(long_lived) >= 5:
            # Extract common factors
            factors = self._extract_longevity_factors(long_lived, assemblies)

            for factor_name, factor_data in factors.items():
                if factor_data["effect_size"] > 0.2:
                    pattern = DetectedPattern(
                        layer=PatternLayer.BEHAVIORAL,
                        pattern_type="longevity_factor",
                        category="success",
                        name=f"Longevity Factor: {factor_name}",
                        description=(
                            f"Factor '{factor_name}' associated with "
                            f"{factor_data['effect_size']:.0%} longer lifespan"
                        ),
                        significance_score=Decimal(str(factor_data["effect_size"])),
                        evidence={
                            "factor": factor_name,
                            "effect_size": factor_data["effect_size"],
                            "present_in_long_lived": factor_data["presence_rate"],
                            "avg_lifespan_with": factor_data["avg_lifespan_with"],
                            "avg_lifespan_without": factor_data["avg_lifespan_without"],
                        },
                        sample_size=len(long_lived),
                        confidence=Decimal(str(min(factor_data["effect_size"], 0.9))),
                    )
                    patterns.append(pattern)

        return patterns

    def _detect_performance_outliers(
        self,
        assemblies: List[Assembly],
        failures: List[FailureRecord],
    ) -> List[DetectedPattern]:
        """Detect parts that perform unexpectedly well or poorly"""
        patterns = []

        # Calculate expected vs actual performance
        performance_by_part: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"success": 0, "failure": 0, "total_lifespan": 0, "count": 0}
        )

        for assembly in assemblies:
            for part in assembly.parts:
                if assembly.success:
                    performance_by_part[part]["success"] += 1
                else:
                    performance_by_part[part]["failure"] += 1
                if assembly.lifespan_hours:
                    performance_by_part[part]["total_lifespan"] += assembly.lifespan_hours
                    performance_by_part[part]["count"] += 1

        if len(performance_by_part) < 5:
            return patterns

        # Calculate statistics
        success_rates = []
        for part_id, stats in performance_by_part.items():
            total = stats["success"] + stats["failure"]
            if total >= 5:
                rate = stats["success"] / total
                success_rates.append((part_id, rate, total))

        if len(success_rates) < 5:
            return patterns

        # Calculate mean and std
        rates = [r for _, r, _ in success_rates]
        mean_rate = sum(rates) / len(rates)
        variance = sum((r - mean_rate) ** 2 for r in rates) / len(rates)
        std_rate = math.sqrt(variance) if variance > 0 else 0.01

        # Find outliers
        for part_id, rate, total in success_rates:
            z_score = (rate - mean_rate) / std_rate if std_rate > 0 else 0

            if abs(z_score) > self.config.outlier_z_threshold:
                outlier_type = "positive" if z_score > 0 else "negative"
                pattern = DetectedPattern(
                    layer=PatternLayer.BEHAVIORAL,
                    pattern_type="performance_outlier",
                    category="outlier",
                    name=f"Performance Outlier: {part_id[:20]}...",
                    description=(
                        f"Part {part_id} is a {outlier_type} outlier with "
                        f"{rate:.0%} success rate (mean: {mean_rate:.0%})"
                    ),
                    significance_score=Decimal(str(min(abs(z_score) / 5, 1.0))),
                    evidence={
                        "part_id": part_id,
                        "success_rate": rate,
                        "mean_success_rate": mean_rate,
                        "z_score": z_score,
                        "outlier_type": outlier_type,
                        "sample_size": total,
                    },
                    sample_size=total,
                    confidence=Decimal(str(min(abs(z_score) / 4, 0.95))),
                )
                patterns.append(pattern)

        return patterns

    def _find_common_combinations(
        self,
        successful: List[Assembly],
        failed: List[Assembly],
    ) -> List[Dict[str, Any]]:
        """Find part combinations common in successful assemblies"""
        formulas = []

        # Count part co-occurrences in successful assemblies
        pair_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        part_counts: Dict[str, int] = defaultdict(int)

        for assembly in successful:
            parts = sorted(set(assembly.parts))
            for part in parts:
                part_counts[part] += 1
            for i, p1 in enumerate(parts):
                for p2 in parts[i + 1:]:
                    pair_counts[(p1, p2)] += 1

        # Find frequent part sets
        min_support = len(successful) * 0.3
        frequent_parts = {
            part for part, count in part_counts.items()
            if count >= min_support
        }

        # Check failure rate for assemblies with/without these parts
        for part in frequent_parts:
            with_part = [a for a in successful + failed if part in a.parts]
            success_with = sum(1 for a in with_part if a.success)

            if len(with_part) >= 5:
                success_rate = success_with / len(with_part)
                avg_lifespan = sum(
                    a.lifespan_hours for a in with_part
                    if a.success and a.lifespan_hours
                ) / max(success_with, 1)

                formulas.append({
                    "required_parts": [part],
                    "success_rate": success_rate,
                    "sample_size": len(with_part),
                    "average_lifespan": avg_lifespan,
                })

        return sorted(formulas, key=lambda x: x["success_rate"], reverse=True)[:10]

    def _extract_cluster_characteristics(
        self,
        failures: List[FailureRecord],
    ) -> Dict[str, Any]:
        """Extract common characteristics from a failure cluster"""
        characteristics = {}

        # Common materials
        materials = [f.material for f in failures if f.material]
        if materials:
            material_counts = defaultdict(int)
            for m in materials:
                material_counts[m] += 1
            common_material = max(material_counts.items(), key=lambda x: x[1])
            if common_material[1] / len(failures) > 0.5:
                characteristics["common_material"] = common_material[0]

        # Common part types
        types = [f.part_type for f in failures if f.part_type]
        if types:
            type_counts = defaultdict(int)
            for t in types:
                type_counts[t] += 1
            common_type = max(type_counts.items(), key=lambda x: x[1])
            if common_type[1] / len(failures) > 0.5:
                characteristics["common_part_type"] = common_type[0]

        # Age range
        ages = [f.age_at_failure for f in failures if f.age_at_failure]
        if ages:
            characteristics["age_range"] = {
                "min": min(ages),
                "max": max(ages),
                "mean": sum(ages) / len(ages),
            }

        return characteristics

    def _calculate_cluster_coherence(
        self,
        failures: List[FailureRecord],
    ) -> float:
        """Calculate how coherent (similar) failures in a cluster are"""
        if len(failures) < 2:
            return 1.0

        # Compare characteristics pairwise
        similarities = []

        for i, f1 in enumerate(failures[:10]):  # Sample for efficiency
            for f2 in failures[i + 1:10]:
                similarity = self._calculate_failure_similarity(f1, f2)
                similarities.append(similarity)

        return sum(similarities) / len(similarities) if similarities else 0.0

    def _calculate_failure_similarity(
        self,
        f1: FailureRecord,
        f2: FailureRecord,
    ) -> float:
        """Calculate similarity between two failure records"""
        score = 0.0
        factors = 0

        # Same material
        if f1.material and f2.material:
            factors += 1
            if f1.material == f2.material:
                score += 1.0

        # Same part type
        if f1.part_type and f2.part_type:
            factors += 1
            if f1.part_type == f2.part_type:
                score += 1.0

        # Similar age
        if f1.age_at_failure and f2.age_at_failure:
            factors += 1
            age_diff_ratio = abs(f1.age_at_failure - f2.age_at_failure) / max(
                f1.age_at_failure, f2.age_at_failure
            )
            score += max(0, 1 - age_diff_ratio)

        return score / factors if factors > 0 else 0.0

    def _extract_longevity_factors(
        self,
        long_lived: List[Assembly],
        all_assemblies: List[Assembly],
    ) -> Dict[str, Dict[str, Any]]:
        """Extract factors that correlate with long life"""
        factors = {}

        # Analyze configuration differences
        long_lived_configs = [a.configuration for a in long_lived]
        all_configs = [a.configuration for a in all_assemblies]

        # Find keys present more often in long-lived
        all_keys: Set[str] = set()
        for config in all_configs:
            all_keys.update(config.keys())

        for key in all_keys:
            in_long = sum(1 for c in long_lived_configs if key in c)
            in_all = sum(1 for c in all_configs if key in c)

            if in_all >= 5:
                presence_in_long = in_long / len(long_lived)
                presence_in_all = in_all / len(all_assemblies)

                if presence_in_long > presence_in_all * 1.2:
                    # This factor is more common in long-lived assemblies
                    with_factor = [a for a in all_assemblies if key in a.configuration]
                    without_factor = [a for a in all_assemblies if key not in a.configuration]

                    avg_with = sum(
                        a.lifespan_hours for a in with_factor if a.lifespan_hours
                    ) / max(len([a for a in with_factor if a.lifespan_hours]), 1)

                    avg_without = sum(
                        a.lifespan_hours for a in without_factor if a.lifespan_hours
                    ) / max(len([a for a in without_factor if a.lifespan_hours]), 1)

                    if avg_without > 0:
                        effect_size = (avg_with - avg_without) / avg_without
                        factors[key] = {
                            "effect_size": effect_size,
                            "presence_rate": presence_in_long,
                            "avg_lifespan_with": avg_with,
                            "avg_lifespan_without": avg_without,
                        }

        return factors
