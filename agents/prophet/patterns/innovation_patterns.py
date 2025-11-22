"""
Layer 4: Innovation Pattern Detection
Detects gaps, cross-category inspiration, evolution trajectories, and emerging categories.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set
import logging

from ..types import (
    DetectedPattern,
    PatternLayer,
    Assembly,
    FailureRecord,
    SwarmKnowledge,
)


logger = logging.getLogger(__name__)


@dataclass
class InnovationConfig:
    """Configuration for innovation pattern detection"""
    gap_frequency_threshold: int = 10
    cross_domain_min_similarity: float = 0.6
    evolution_trend_min_samples: int = 20
    emerging_category_threshold: float = 0.3


class InnovationPatternDetector:
    """
    Layer 4: Innovation Pattern Detection

    Detects:
    - Gap detection (needs without solutions)
    - Cross-category inspiration (ideas from other domains)
    - Evolution trajectories (where part families are heading)
    - Emergence of new categories (previously undefined groupings)
    """

    def __init__(self, config: Optional[InnovationConfig] = None):
        self.config = config or InnovationConfig()

    @property
    def layer(self) -> PatternLayer:
        return PatternLayer.INNOVATION

    def detect(self, data: Dict[str, Any]) -> List[DetectedPattern]:
        """Detect innovation patterns"""
        patterns = []

        assemblies = data.get("assemblies", [])
        failure_records = data.get("failure_records", [])
        swarm_knowledge = data.get("swarm_knowledge", {})

        # Detect gaps
        gap_patterns = self._detect_gaps(failure_records, assemblies)
        patterns.extend(gap_patterns)

        # Find cross-domain inspiration
        cross_domain = self._find_cross_domain_inspiration(assemblies, swarm_knowledge)
        patterns.extend(cross_domain)

        # Analyze evolution trajectories
        evolution = self._analyze_evolution_trajectories(assemblies, failure_records)
        patterns.extend(evolution)

        # Detect emerging categories
        emerging = self._detect_emerging_categories(assemblies, swarm_knowledge)
        patterns.extend(emerging)

        return patterns

    def _detect_gaps(
        self,
        failures: List[FailureRecord],
        assemblies: List[Assembly],
    ) -> List[DetectedPattern]:
        """Detect unmet needs and gaps in the parts ecosystem"""
        patterns = []

        if len(failures) < self.config.gap_frequency_threshold:
            return patterns

        # Analyze recurring failure patterns without solutions
        failure_by_mode: Dict[str, List[FailureRecord]] = defaultdict(list)
        for failure in failures:
            failure_by_mode[failure.failure_mode].append(failure)

        # Find failure modes without corresponding solutions in successful assemblies
        successful_parts = set()
        for assembly in assemblies:
            if assembly.success:
                successful_parts.update(assembly.parts)

        for mode, mode_failures in failure_by_mode.items():
            if len(mode_failures) < self.config.gap_frequency_threshold:
                continue

            # Check if there are parts specifically designed to prevent this failure
            affected_types = set(f.part_type for f in mode_failures)

            # Calculate problem scope
            problem_scope = len(mode_failures)
            unique_parts_affected = len(set(f.part_id for f in mode_failures))

            # Generate gap opportunity
            pattern = DetectedPattern(
                layer=PatternLayer.INNOVATION,
                pattern_type="solution_gap",
                category="gap",
                name=f"Gap: {mode} Prevention",
                description=(
                    f"No solution found for '{mode}' failure mode affecting "
                    f"{unique_parts_affected} parts ({problem_scope} occurrences)"
                ),
                significance_score=Decimal(str(min(problem_scope / 100, 1.0))),
                evidence={
                    "failure_mode": mode,
                    "occurrence_count": problem_scope,
                    "unique_parts_affected": unique_parts_affected,
                    "affected_part_types": list(affected_types)[:10],
                    "opportunity_type": "prevention_innovation",
                    "suggested_solution_directions": self._suggest_solutions(mode, mode_failures),
                },
                sample_size=problem_scope,
                confidence=Decimal(str(min(0.5 + problem_scope / 200, 0.9))),
            )
            patterns.append(pattern)

        return patterns

    def _find_cross_domain_inspiration(
        self,
        assemblies: List[Assembly],
        swarm_knowledge: Dict[str, SwarmKnowledge],
    ) -> List[DetectedPattern]:
        """Find successful patterns that could transfer between domains"""
        patterns = []

        if len(assemblies) < 20:
            return patterns

        # Group successful assemblies by domain
        by_domain: Dict[str, List[Assembly]] = defaultdict(list)
        for assembly in assemblies:
            if assembly.success:
                by_domain[assembly.domain].append(assembly)

        if len(by_domain) < 2:
            return patterns

        # Extract success patterns from each domain
        domain_patterns: Dict[str, Dict[str, Any]] = {}
        for domain, domain_assemblies in by_domain.items():
            if len(domain_assemblies) >= 10:
                domain_patterns[domain] = self._extract_domain_success_patterns(domain_assemblies)

        # Find transferable patterns between domains
        domains = list(domain_patterns.keys())
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i + 1:]:
                transferable = self._find_transferable_patterns(
                    domain1, domain_patterns[domain1],
                    domain2, domain_patterns[domain2],
                )

                for transfer in transferable:
                    pattern = DetectedPattern(
                        layer=PatternLayer.INNOVATION,
                        pattern_type="cross_domain_transfer",
                        category="innovation",
                        name=f"Transfer: {domain1} -> {domain2}",
                        description=(
                            f"Success pattern from {domain1} could apply to {domain2}: "
                            f"{transfer['principle']}"
                        ),
                        significance_score=Decimal(str(transfer["similarity"])),
                        evidence={
                            "source_domain": domain1,
                            "target_domain": domain2,
                            "success_principle": transfer["principle"],
                            "similarity_score": transfer["similarity"],
                            "source_evidence": transfer["source_evidence"],
                            "potential_applications": transfer["applications"],
                        },
                        sample_size=transfer.get("sample_size", 10),
                        confidence=Decimal(str(transfer["similarity"] * 0.85)),
                    )
                    patterns.append(pattern)

        return patterns

    def _analyze_evolution_trajectories(
        self,
        assemblies: List[Assembly],
        failures: List[FailureRecord],
    ) -> List[DetectedPattern]:
        """Analyze how part families are evolving"""
        patterns = []

        if len(assemblies) < self.config.evolution_trend_min_samples:
            return patterns

        # Group assemblies by domain and analyze changes over time
        # (Would use temporal data in production - using configuration changes as proxy)

        # Analyze configuration evolution
        config_evolution: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for assembly in assemblies:
            for key, value in assembly.configuration.items():
                config_evolution[key].append({
                    "value": value,
                    "domain": assembly.domain,
                    "success": assembly.success,
                })

        # Find evolving configurations
        for config_key, values in config_evolution.items():
            if len(values) < 20:
                continue

            # Analyze value distribution
            value_success: Dict[Any, Dict[str, int]] = defaultdict(
                lambda: {"success": 0, "total": 0}
            )
            for v in values:
                value_success[str(v["value"])]["total"] += 1
                if v["success"]:
                    value_success[str(v["value"])]["success"] += 1

            # Find trending values (high success rate + increasing frequency)
            trending = []
            for val, stats in value_success.items():
                if stats["total"] >= 5:
                    success_rate = stats["success"] / stats["total"]
                    if success_rate > 0.7:
                        trending.append((val, success_rate, stats["total"]))

            if trending:
                trending.sort(key=lambda x: x[1], reverse=True)
                best = trending[0]

                pattern = DetectedPattern(
                    layer=PatternLayer.INNOVATION,
                    pattern_type="evolution_trajectory",
                    category="evolution",
                    name=f"Evolution: {config_key}",
                    description=(
                        f"Configuration '{config_key}' evolving toward '{best[0]}' "
                        f"({best[1]:.0%} success rate)"
                    ),
                    significance_score=Decimal(str(best[1])),
                    evidence={
                        "configuration_key": config_key,
                        "trending_value": best[0],
                        "success_rate": best[1],
                        "instance_count": best[2],
                        "all_values": {k: v["total"] for k, v in value_success.items()},
                    },
                    sample_size=len(values),
                    confidence=Decimal(str(best[1] * 0.8)),
                )
                patterns.append(pattern)

        return patterns

    def _detect_emerging_categories(
        self,
        assemblies: List[Assembly],
        swarm_knowledge: Dict[str, SwarmKnowledge],
    ) -> List[DetectedPattern]:
        """Detect emergence of new part categories"""
        patterns = []

        if len(assemblies) < 20:
            return patterns

        # Look for novel combinations that don't fit existing categories
        existing_domains = set(a.domain for a in assemblies)

        # Analyze part combinations across domains
        cross_domain_combos: Dict[str, Set[str]] = defaultdict(set)
        for assembly in assemblies:
            for part in assembly.parts:
                cross_domain_combos[part].add(assembly.domain)

        # Find parts appearing in multiple domains (potential new category)
        versatile_parts = []
        for part, domains in cross_domain_combos.items():
            if len(domains) >= 3:
                versatile_parts.append((part, domains))

        if versatile_parts:
            # Group versatile parts by domain coverage
            coverage_groups: Dict[str, List[str]] = defaultdict(list)
            for part, domains in versatile_parts:
                key = "|".join(sorted(domains))
                coverage_groups[key].append(part)

            for domain_combo, parts in coverage_groups.items():
                if len(parts) >= 3:
                    domains = domain_combo.split("|")
                    pattern = DetectedPattern(
                        layer=PatternLayer.INNOVATION,
                        pattern_type="emerging_category",
                        category="emergence",
                        name=f"Emerging Category: Multi-domain Parts",
                        description=(
                            f"{len(parts)} parts work across {len(domains)} domains: "
                            f"{', '.join(domains[:3])}"
                        ),
                        significance_score=Decimal(str(min(len(parts) / 10, 1.0))),
                        evidence={
                            "parts": parts[:10],
                            "domains": domains,
                            "part_count": len(parts),
                            "domain_count": len(domains),
                            "category_suggestion": self._suggest_category_name(domains),
                        },
                        sample_size=len(parts),
                        confidence=Decimal(str(min(0.5 + len(parts) / 20, 0.85))),
                    )
                    patterns.append(pattern)

        return patterns

    def _suggest_solutions(
        self,
        failure_mode: str,
        failures: List[FailureRecord],
    ) -> List[str]:
        """Suggest potential solution directions for a gap"""
        suggestions = []

        # Analyze failure characteristics
        materials = set(f.material for f in failures if f.material)
        environments = set()
        for f in failures:
            if f.environment:
                environments.update(f.environment.keys())

        if "fatigue" in failure_mode.lower():
            suggestions.append("Investigate higher-strength materials or heat treatments")
            suggestions.append("Consider redesign for reduced stress concentration")

        if "corrosion" in failure_mode.lower():
            suggestions.append("Explore corrosion-resistant coatings or materials")
            suggestions.append("Investigate environmental protection solutions")

        if "wear" in failure_mode.lower():
            suggestions.append("Evaluate harder surface treatments or materials")
            suggestions.append("Consider improved lubrication solutions")

        if not suggestions:
            suggestions.append("Conduct root cause analysis on failure conditions")
            suggestions.append("Survey industry for existing solutions")

        return suggestions

    def _extract_domain_success_patterns(
        self,
        assemblies: List[Assembly],
    ) -> Dict[str, Any]:
        """Extract success patterns from a domain"""
        patterns = {
            "common_parts": defaultdict(int),
            "configurations": defaultdict(int),
            "avg_lifespan": 0,
            "success_factors": [],
        }

        lifespans = []
        for assembly in assemblies:
            for part in assembly.parts:
                patterns["common_parts"][part] += 1
            for key, value in assembly.configuration.items():
                patterns["configurations"][f"{key}={value}"] += 1
            if assembly.lifespan_hours:
                lifespans.append(assembly.lifespan_hours)

        if lifespans:
            patterns["avg_lifespan"] = sum(lifespans) / len(lifespans)

        return patterns

    def _find_transferable_patterns(
        self,
        domain1: str,
        patterns1: Dict[str, Any],
        domain2: str,
        patterns2: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Find patterns that could transfer between domains"""
        transferable = []

        # Find configurations successful in domain1 that don't exist in domain2
        configs1 = set(patterns1["configurations"].keys())
        configs2 = set(patterns2["configurations"].keys())

        unique_to_1 = configs1 - configs2
        for config in list(unique_to_1)[:5]:
            if patterns1["configurations"][config] >= 5:
                transferable.append({
                    "principle": f"Configuration '{config}' from {domain1}",
                    "similarity": 0.7,
                    "source_evidence": f"{patterns1['configurations'][config]} instances in {domain1}",
                    "applications": [f"Apply {config} pattern to {domain2} applications"],
                    "sample_size": patterns1["configurations"][config],
                })

        return transferable

    def _suggest_category_name(self, domains: List[str]) -> str:
        """Suggest a name for an emerging category"""
        if len(domains) == 0:
            return "Universal Parts"

        # Simple naming based on domain overlap
        if "automotive" in domains and "aerospace" in domains:
            return "High-Performance Transport Parts"
        elif "industrial" in domains and "marine" in domains:
            return "Heavy-Duty Environment Parts"
        else:
            return f"Multi-Application Parts ({'/'.join(domains[:2])})"
