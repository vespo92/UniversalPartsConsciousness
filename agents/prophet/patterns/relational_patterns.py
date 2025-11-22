"""
Layer 3: Relational Pattern Detection
Detects compatibility networks, conflict detection, assembly archetypes, and supply chain patterns.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from ..types import DetectedPattern, PatternLayer, Assembly, SwarmKnowledge


logger = logging.getLogger(__name__)


@dataclass
class RelationalConfig:
    """Configuration for relational pattern detection"""
    min_co_occurrence: int = 5
    affinity_threshold: float = 0.6
    conflict_threshold: float = 0.3
    archetype_min_instances: int = 10


class RelationalPatternDetector:
    """
    Layer 3: Relational Pattern Detection

    Detects:
    - Compatibility networks (parts that work well together)
    - Conflict detection (parts that shouldn't be paired)
    - Assembly archetypes (successful combination patterns)
    - Supply chain insights (substitution patterns)
    """

    def __init__(self, config: Optional[RelationalConfig] = None):
        self.config = config or RelationalConfig()

    @property
    def layer(self) -> PatternLayer:
        return PatternLayer.RELATIONAL

    def detect(self, data: Dict[str, Any]) -> List[DetectedPattern]:
        """Detect relational patterns from assemblies"""
        patterns = []

        assemblies = data.get("assemblies", [])
        swarm_knowledge = data.get("swarm_knowledge", {})

        # Build compatibility network
        compatibility_patterns = self._build_compatibility_network(assemblies)
        patterns.extend(compatibility_patterns)

        # Detect conflicts
        conflict_patterns = self._detect_conflicts(assemblies)
        patterns.extend(conflict_patterns)

        # Identify assembly archetypes
        archetype_patterns = self._identify_archetypes(assemblies)
        patterns.extend(archetype_patterns)

        # Analyze substitution patterns
        substitution_patterns = self._analyze_substitutions(assemblies, swarm_knowledge)
        patterns.extend(substitution_patterns)

        return patterns

    def _build_compatibility_network(
        self,
        assemblies: List[Assembly],
    ) -> List[DetectedPattern]:
        """Build network of parts that work well together"""
        patterns = []

        if len(assemblies) < 10:
            return patterns

        # Count co-occurrences and success rates
        pair_stats: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "failure": 0}
        )

        for assembly in assemblies:
            parts = sorted(set(assembly.parts))
            for i, p1 in enumerate(parts):
                for p2 in parts[i + 1:]:
                    key = (p1, p2)
                    if assembly.success:
                        pair_stats[key]["success"] += 1
                    else:
                        pair_stats[key]["failure"] += 1

        # Find high-affinity pairs
        affinities = []
        for pair, stats in pair_stats.items():
            total = stats["success"] + stats["failure"]
            if total >= self.config.min_co_occurrence:
                affinity = stats["success"] / total
                affinities.append((pair, affinity, total))

        # Sort by affinity
        affinities.sort(key=lambda x: x[1], reverse=True)

        # Create patterns for top affinities
        for pair, affinity, total in affinities[:20]:
            if affinity >= self.config.affinity_threshold:
                pattern = DetectedPattern(
                    layer=PatternLayer.RELATIONAL,
                    pattern_type="compatibility_pair",
                    category="compatibility",
                    name=f"Compatibility: {pair[0][:15]} + {pair[1][:15]}",
                    description=(
                        f"Parts {pair[0]} and {pair[1]} have {affinity:.0%} "
                        f"success rate when used together ({total} instances)"
                    ),
                    significance_score=Decimal(str(affinity)),
                    evidence={
                        "part_1": pair[0],
                        "part_2": pair[1],
                        "affinity": affinity,
                        "success_count": pair_stats[pair]["success"],
                        "failure_count": pair_stats[pair]["failure"],
                        "total_instances": total,
                    },
                    sample_size=total,
                    confidence=Decimal(str(min(affinity * 0.95, 0.95))),
                )
                patterns.append(pattern)

        # Build network summary
        if affinities:
            network_density = len([a for a in affinities if a[1] >= self.config.affinity_threshold]) / len(affinities)
            network_pattern = DetectedPattern(
                layer=PatternLayer.RELATIONAL,
                pattern_type="compatibility_network",
                category="network",
                name="Part Compatibility Network",
                description=(
                    f"Analyzed {len(affinities)} part relationships, "
                    f"found {network_density:.0%} high-compatibility pairs"
                ),
                significance_score=Decimal(str(network_density)),
                evidence={
                    "total_pairs_analyzed": len(affinities),
                    "high_compatibility_pairs": len([a for a in affinities if a[1] >= self.config.affinity_threshold]),
                    "network_density": network_density,
                },
                sample_size=len(assemblies),
                confidence=Decimal("0.85"),
            )
            patterns.append(network_pattern)

        return patterns

    def _detect_conflicts(
        self,
        assemblies: List[Assembly],
    ) -> List[DetectedPattern]:
        """Detect parts that shouldn't be used together"""
        patterns = []

        if len(assemblies) < 10:
            return patterns

        # Find pairs with high failure rates
        pair_stats: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "failure": 0}
        )

        for assembly in assemblies:
            parts = sorted(set(assembly.parts))
            for i, p1 in enumerate(parts):
                for p2 in parts[i + 1:]:
                    key = (p1, p2)
                    if assembly.success:
                        pair_stats[key]["success"] += 1
                    else:
                        pair_stats[key]["failure"] += 1

        # Find conflicting pairs
        conflicts = []
        for pair, stats in pair_stats.items():
            total = stats["success"] + stats["failure"]
            if total >= self.config.min_co_occurrence:
                failure_rate = stats["failure"] / total
                if failure_rate >= (1 - self.config.conflict_threshold):
                    conflicts.append((pair, failure_rate, total))

        for pair, failure_rate, total in conflicts[:10]:
            pattern = DetectedPattern(
                layer=PatternLayer.RELATIONAL,
                pattern_type="conflict_pair",
                category="conflict",
                name=f"Conflict: {pair[0][:15]} + {pair[1][:15]}",
                description=(
                    f"Parts {pair[0]} and {pair[1]} have {failure_rate:.0%} "
                    f"failure rate when combined ({total} instances)"
                ),
                significance_score=Decimal(str(failure_rate)),
                evidence={
                    "part_1": pair[0],
                    "part_2": pair[1],
                    "failure_rate": failure_rate,
                    "success_count": pair_stats[pair]["success"],
                    "failure_count": pair_stats[pair]["failure"],
                    "warning": "These parts should not be used together",
                },
                sample_size=total,
                confidence=Decimal(str(min(failure_rate * 0.9, 0.95))),
            )
            patterns.append(pattern)

        return patterns

    def _identify_archetypes(
        self,
        assemblies: List[Assembly],
    ) -> List[DetectedPattern]:
        """Identify common assembly archetypes"""
        patterns = []

        if len(assemblies) < self.config.archetype_min_instances:
            return patterns

        # Group successful assemblies by part composition signature
        signatures: Dict[str, List[Assembly]] = defaultdict(list)

        for assembly in assemblies:
            if assembly.success:
                # Create signature from sorted parts
                sig = "|".join(sorted(set(assembly.parts)))
                signatures[sig].append(assembly)

        # Find archetypes (common patterns)
        archetypes = []
        for sig, sig_assemblies in signatures.items():
            if len(sig_assemblies) >= self.config.archetype_min_instances:
                parts = sig.split("|")
                avg_lifespan = sum(
                    a.lifespan_hours for a in sig_assemblies if a.lifespan_hours
                ) / max(len([a for a in sig_assemblies if a.lifespan_hours]), 1)

                archetypes.append({
                    "signature": sig,
                    "parts": parts,
                    "count": len(sig_assemblies),
                    "avg_lifespan": avg_lifespan,
                    "domains": list(set(a.domain for a in sig_assemblies)),
                })

        archetypes.sort(key=lambda x: x["count"], reverse=True)

        for i, archetype in enumerate(archetypes[:10]):
            pattern = DetectedPattern(
                layer=PatternLayer.RELATIONAL,
                pattern_type="assembly_archetype",
                category="archetype",
                name=f"Archetype #{i+1}: {archetype['domains'][0]} Assembly",
                description=(
                    f"Common assembly pattern with {len(archetype['parts'])} parts, "
                    f"seen {archetype['count']} times with avg lifespan "
                    f"{archetype['avg_lifespan']:.0f} hours"
                ),
                significance_score=Decimal(str(min(archetype["count"] / 100, 1.0))),
                evidence={
                    "archetype_rank": i + 1,
                    "parts": archetype["parts"],
                    "instance_count": archetype["count"],
                    "average_lifespan_hours": archetype["avg_lifespan"],
                    "domains": archetype["domains"],
                },
                sample_size=archetype["count"],
                confidence=Decimal(str(min(0.5 + archetype["count"] / 200, 0.95))),
            )
            patterns.append(pattern)

        return patterns

    def _analyze_substitutions(
        self,
        assemblies: List[Assembly],
        swarm_knowledge: Dict[str, SwarmKnowledge],
    ) -> List[DetectedPattern]:
        """Analyze part substitution patterns"""
        patterns = []

        if len(assemblies) < 20:
            return patterns

        # Group assemblies by application
        by_application: Dict[str, List[Assembly]] = defaultdict(list)
        for assembly in assemblies:
            by_application[assembly.application].append(assembly)

        # For each application, find parts used interchangeably
        substitution_groups: Dict[str, List[Set[str]]] = {}

        for app, app_assemblies in by_application.items():
            if len(app_assemblies) < 10:
                continue

            # Find parts that appear in similar roles
            successful = [a for a in app_assemblies if a.success]
            if len(successful) < 5:
                continue

            # Parts that appear in mutually exclusive fashion with similar success
            all_parts = set()
            for a in successful:
                all_parts.update(a.parts)

            # Find substitution pairs (parts that don't co-occur but fill same role)
            substitutes: List[Tuple[str, str, float]] = []

            part_list = list(all_parts)
            for i, p1 in enumerate(part_list):
                for p2 in part_list[i + 1:]:
                    # Check if they co-occur
                    co_occur = sum(
                        1 for a in successful if p1 in a.parts and p2 in a.parts
                    )
                    p1_only = sum(
                        1 for a in successful if p1 in a.parts and p2 not in a.parts
                    )
                    p2_only = sum(
                        1 for a in successful if p2 in a.parts and p1 not in a.parts
                    )

                    # If rarely co-occur but both appear frequently, likely substitutes
                    if co_occur < 2 and p1_only >= 5 and p2_only >= 5:
                        substitutes.append((p1, p2, (p1_only + p2_only) / len(successful)))

            if substitutes:
                substitution_groups[app] = substitutes

        # Create patterns for substitution groups
        for app, subs in substitution_groups.items():
            for p1, p2, coverage in subs[:5]:
                pattern = DetectedPattern(
                    layer=PatternLayer.RELATIONAL,
                    pattern_type="substitution_pair",
                    category="supply_chain",
                    name=f"Substitutes: {p1[:15]} <-> {p2[:15]}",
                    description=(
                        f"Parts {p1} and {p2} are interchangeable for {app} "
                        f"applications (coverage: {coverage:.0%})"
                    ),
                    significance_score=Decimal(str(coverage)),
                    evidence={
                        "part_1": p1,
                        "part_2": p2,
                        "application": app,
                        "coverage": coverage,
                        "substitution_type": "functional_equivalent",
                    },
                    sample_size=int(coverage * len(by_application[app])),
                    confidence=Decimal(str(min(coverage, 0.85))),
                )
                patterns.append(pattern)

        return patterns
