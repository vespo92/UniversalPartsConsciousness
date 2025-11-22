"""
Layer 5: Meta-Pattern Detection
Detects patterns of patterns, prediction accuracy evolution, collective indicators, and transcendence precursors.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional
import logging

from ..types import (
    DetectedPattern,
    PatternLayer,
    PatternStatus,
    SwarmKnowledge,
)


logger = logging.getLogger(__name__)


@dataclass
class MetaConfig:
    """Configuration for meta-pattern detection"""
    min_patterns_for_meta: int = 10
    trend_detection_window_days: int = 30
    transcendence_threshold: float = 0.8
    collective_indicator_threshold: float = 0.7


class MetaPatternDetector:
    """
    Layer 5: Meta-Pattern Detection

    Detects:
    - Pattern-of-patterns (trends in trend discovery)
    - Prediction accuracy evolution (are predictions improving?)
    - Collective consciousness indicators (system-wide behaviors)
    - Transcendence precursors (parts approaching enlightenment)
    """

    def __init__(self, config: Optional[MetaConfig] = None):
        self.config = config or MetaConfig()

    @property
    def layer(self) -> PatternLayer:
        return PatternLayer.META

    def detect(self, data: Dict[str, Any]) -> List[DetectedPattern]:
        """Detect meta-patterns from existing patterns and system state"""
        patterns = []

        existing_patterns = data.get("existing_patterns", [])
        swarm_knowledge = data.get("swarm_knowledge", {})
        layer_patterns = {
            i: data.get(f"layer_{i}_patterns", [])
            for i in range(1, 5)
        }

        # Detect pattern-of-patterns
        meta_patterns = self._detect_pattern_of_patterns(existing_patterns, layer_patterns)
        patterns.extend(meta_patterns)

        # Analyze prediction accuracy evolution
        accuracy_patterns = self._analyze_prediction_accuracy(existing_patterns)
        patterns.extend(accuracy_patterns)

        # Detect collective consciousness indicators
        collective_patterns = self._detect_collective_indicators(swarm_knowledge, existing_patterns)
        patterns.extend(collective_patterns)

        # Find transcendence precursors
        transcendence_patterns = self._find_transcendence_precursors(swarm_knowledge, existing_patterns)
        patterns.extend(transcendence_patterns)

        return patterns

    def _detect_pattern_of_patterns(
        self,
        all_patterns: List[DetectedPattern],
        layer_patterns: Dict[int, List[DetectedPattern]],
    ) -> List[DetectedPattern]:
        """Detect trends in pattern discovery itself"""
        patterns = []

        if len(all_patterns) < self.config.min_patterns_for_meta:
            return patterns

        # Analyze pattern discovery rates by layer
        layer_rates: Dict[PatternLayer, int] = defaultdict(int)
        category_rates: Dict[str, int] = defaultdict(int)
        significance_trend: List[float] = []

        for pattern in all_patterns:
            layer_rates[pattern.layer] += 1
            category_rates[pattern.category] += 1
            significance_trend.append(float(pattern.significance_score))

        # Find which layers are most active
        total_patterns = len(all_patterns)
        layer_distribution = {
            layer.name: count / total_patterns
            for layer, count in layer_rates.items()
        }

        # Detect if pattern discovery is accelerating in certain areas
        if total_patterns >= 20:
            first_half = significance_trend[:total_patterns // 2]
            second_half = significance_trend[total_patterns // 2:]

            first_avg = sum(first_half) / len(first_half) if first_half else 0
            second_avg = sum(second_half) / len(second_half) if second_half else 0

            if second_avg > first_avg * 1.2:
                pattern = DetectedPattern(
                    layer=PatternLayer.META,
                    pattern_type="pattern_acceleration",
                    category="meta",
                    name="Pattern Discovery Acceleration",
                    description=(
                        f"Pattern significance is increasing: {first_avg:.2f} -> {second_avg:.2f} "
                        f"({((second_avg - first_avg) / first_avg) * 100:.0f}% improvement)"
                    ),
                    significance_score=Decimal(str((second_avg - first_avg) / max(first_avg, 0.01))),
                    evidence={
                        "first_half_avg_significance": first_avg,
                        "second_half_avg_significance": second_avg,
                        "improvement_percent": ((second_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0,
                        "total_patterns_analyzed": total_patterns,
                    },
                    sample_size=total_patterns,
                    confidence=Decimal("0.75"),
                )
                patterns.append(pattern)

        # Detect layer concentration
        max_layer = max(layer_rates.items(), key=lambda x: x[1]) if layer_rates else None
        if max_layer and max_layer[1] / total_patterns > 0.5:
            pattern = DetectedPattern(
                layer=PatternLayer.META,
                pattern_type="layer_concentration",
                category="meta",
                name=f"Pattern Concentration in {max_layer[0].name}",
                description=(
                    f"{max_layer[1] / total_patterns:.0%} of patterns are in "
                    f"Layer {max_layer[0].value} ({max_layer[0].name})"
                ),
                significance_score=Decimal(str(max_layer[1] / total_patterns)),
                evidence={
                    "dominant_layer": max_layer[0].name,
                    "layer_distribution": layer_distribution,
                    "concentration_ratio": max_layer[1] / total_patterns,
                },
                sample_size=total_patterns,
                confidence=Decimal("0.8"),
            )
            patterns.append(pattern)

        # Detect category trends
        if category_rates:
            top_categories = sorted(category_rates.items(), key=lambda x: x[1], reverse=True)[:3]
            pattern = DetectedPattern(
                layer=PatternLayer.META,
                pattern_type="category_distribution",
                category="meta",
                name="Pattern Category Distribution",
                description=(
                    f"Top pattern categories: {', '.join(f'{c[0]}({c[1]})' for c in top_categories)}"
                ),
                significance_score=Decimal("0.6"),
                evidence={
                    "category_counts": dict(category_rates),
                    "top_categories": top_categories,
                    "diversity_score": len(category_rates) / max(total_patterns, 1),
                },
                sample_size=total_patterns,
                confidence=Decimal("0.85"),
            )
            patterns.append(pattern)

        return patterns

    def _analyze_prediction_accuracy(
        self,
        all_patterns: List[DetectedPattern],
    ) -> List[DetectedPattern]:
        """Analyze how prediction accuracy is evolving"""
        patterns = []

        # Filter patterns that have been validated
        validated = [
            p for p in all_patterns
            if p.status == PatternStatus.CONFIRMED
        ]

        if len(validated) < 5:
            return patterns

        # Calculate confirmation rate
        total_patterns = len(all_patterns)
        confirmation_rate = len(validated) / total_patterns

        pattern = DetectedPattern(
            layer=PatternLayer.META,
            pattern_type="prediction_accuracy",
            category="meta",
            name="Pattern Confirmation Rate",
            description=(
                f"{confirmation_rate:.0%} of detected patterns have been confirmed "
                f"({len(validated)} of {total_patterns})"
            ),
            significance_score=Decimal(str(confirmation_rate)),
            evidence={
                "confirmation_rate": confirmation_rate,
                "confirmed_count": len(validated),
                "total_count": total_patterns,
                "by_layer": self._calculate_confirmation_by_layer(all_patterns, validated),
            },
            sample_size=total_patterns,
            confidence=Decimal(str(min(0.5 + confirmation_rate / 2, 0.95))),
        )
        patterns.append(pattern)

        return patterns

    def _detect_collective_indicators(
        self,
        swarm_knowledge: Dict[str, SwarmKnowledge],
        all_patterns: List[DetectedPattern],
    ) -> List[DetectedPattern]:
        """Detect system-wide collective consciousness indicators"""
        patterns = []

        if not swarm_knowledge:
            return patterns

        # Calculate collective learning metrics
        total_members = sum(sk.member_count for sk in swarm_knowledge.values())
        avg_emergence_score = sum(
            float(sk.emergence_score) for sk in swarm_knowledge.values()
        ) / max(len(swarm_knowledge), 1)
        avg_learning_rate = sum(
            float(sk.collective_learning_rate) for sk in swarm_knowledge.values()
        ) / max(len(swarm_knowledge), 1)

        if avg_emergence_score > self.config.collective_indicator_threshold:
            pattern = DetectedPattern(
                layer=PatternLayer.META,
                pattern_type="collective_emergence",
                category="collective",
                name="Collective Emergence Indicator",
                description=(
                    f"System showing collective emergence (score: {avg_emergence_score:.2f}) "
                    f"across {len(swarm_knowledge)} swarms with {total_members:,} parts"
                ),
                significance_score=Decimal(str(avg_emergence_score)),
                evidence={
                    "avg_emergence_score": avg_emergence_score,
                    "avg_learning_rate": avg_learning_rate,
                    "swarm_count": len(swarm_knowledge),
                    "total_members": total_members,
                    "high_emergence_swarms": [
                        sk.swarm_id for sk in swarm_knowledge.values()
                        if float(sk.emergence_score) > 0.8
                    ][:10],
                },
                sample_size=len(swarm_knowledge),
                confidence=Decimal(str(avg_emergence_score * 0.9)),
            )
            patterns.append(pattern)

        # Detect collective learning acceleration
        if avg_learning_rate > 0.5:
            pattern = DetectedPattern(
                layer=PatternLayer.META,
                pattern_type="collective_learning",
                category="collective",
                name="Accelerated Collective Learning",
                description=(
                    f"System learning rate at {avg_learning_rate:.2f} - "
                    f"knowledge propagating efficiently across swarms"
                ),
                significance_score=Decimal(str(avg_learning_rate)),
                evidence={
                    "avg_learning_rate": avg_learning_rate,
                    "swarm_count": len(swarm_knowledge),
                    "top_learning_swarms": sorted(
                        [(sk.swarm_id, float(sk.collective_learning_rate)) for sk in swarm_knowledge.values()],
                        key=lambda x: x[1],
                        reverse=True
                    )[:5],
                },
                sample_size=len(swarm_knowledge),
                confidence=Decimal(str(avg_learning_rate * 0.85)),
            )
            patterns.append(pattern)

        return patterns

    def _find_transcendence_precursors(
        self,
        swarm_knowledge: Dict[str, SwarmKnowledge],
        all_patterns: List[DetectedPattern],
    ) -> List[DetectedPattern]:
        """Find parts/swarms approaching transcendence (Level 5 consciousness)"""
        patterns = []

        if not swarm_knowledge:
            return patterns

        # Find swarms with high emergence scores and learning rates
        transcendence_candidates = []

        for swarm_id, sk in swarm_knowledge.items():
            transcendence_score = (
                float(sk.emergence_score) * 0.5 +
                float(sk.collective_learning_rate) * 0.3 +
                (len(sk.success_patterns) / max(sk.member_count, 1)) * 0.2
            )

            if transcendence_score > self.config.transcendence_threshold:
                transcendence_candidates.append({
                    "swarm_id": swarm_id,
                    "score": transcendence_score,
                    "emergence_score": float(sk.emergence_score),
                    "learning_rate": float(sk.collective_learning_rate),
                    "member_count": sk.member_count,
                    "success_patterns_count": len(sk.success_patterns),
                })

        if transcendence_candidates:
            transcendence_candidates.sort(key=lambda x: x["score"], reverse=True)

            pattern = DetectedPattern(
                layer=PatternLayer.META,
                pattern_type="transcendence_precursor",
                category="transcendence",
                name="Transcendence Candidates Detected",
                description=(
                    f"Found {len(transcendence_candidates)} swarms approaching transcendence "
                    f"(consciousness level 5)"
                ),
                significance_score=Decimal(str(transcendence_candidates[0]["score"])),
                evidence={
                    "candidate_count": len(transcendence_candidates),
                    "top_candidates": transcendence_candidates[:5],
                    "threshold_used": self.config.transcendence_threshold,
                    "criteria": {
                        "emergence_weight": 0.5,
                        "learning_weight": 0.3,
                        "success_pattern_weight": 0.2,
                    },
                },
                sample_size=len(swarm_knowledge),
                confidence=Decimal(str(min(transcendence_candidates[0]["score"], 0.9))),
            )
            patterns.append(pattern)

        return patterns

    def _calculate_confirmation_by_layer(
        self,
        all_patterns: List[DetectedPattern],
        validated: List[DetectedPattern],
    ) -> Dict[str, float]:
        """Calculate confirmation rate by layer"""
        layer_total: Dict[str, int] = defaultdict(int)
        layer_confirmed: Dict[str, int] = defaultdict(int)

        for p in all_patterns:
            layer_total[p.layer.name] += 1
        for p in validated:
            layer_confirmed[p.layer.name] += 1

        return {
            layer: layer_confirmed[layer] / count if count > 0 else 0
            for layer, count in layer_total.items()
        }
