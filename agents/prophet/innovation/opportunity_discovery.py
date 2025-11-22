"""
Innovation Opportunity Discovery
Identifies opportunities for new parts, materials, or designs.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set
import logging

from ..types import (
    InnovationOpportunity,
    OpportunityType,
    SuccessFormula,
    FailureRecord,
    DetectedPattern,
    PatternLayer,
)


logger = logging.getLogger(__name__)


@dataclass
class DiscoveryConfig:
    """Configuration for opportunity discovery"""
    min_failure_frequency: int = 10
    min_impact_score: float = 0.3
    cross_domain_similarity_threshold: float = 0.5
    market_size_multiplier: float = 1000  # Failures -> potential market


class InnovationOpportunityDiscovery:
    """
    Identifies opportunities for new parts, materials, or designs.

    Opportunity types:
    1. Prevention Innovation - Solve recurring failure modes
    2. Cross-Domain Transfer - Apply success from one domain to another
    3. Material Evolution - Better materials for existing applications
    4. Design Evolution - Better designs emerging from data
    5. Gap Filling - Unmet needs in the parts ecosystem
    """

    def __init__(self, config: Optional[DiscoveryConfig] = None):
        self.config = config or DiscoveryConfig()
        self._discovered_opportunities: List[InnovationOpportunity] = []

    def discover_opportunities(
        self,
        failure_patterns: List[DetectedPattern],
        success_formulas: List[SuccessFormula],
        all_patterns: Optional[List[DetectedPattern]] = None,
        market_data: Optional[Dict[str, Any]] = None,
    ) -> List[InnovationOpportunity]:
        """
        Find gaps in the current parts ecosystem that represent
        innovation opportunities.

        Args:
            failure_patterns: Detected failure patterns
            success_formulas: Extracted success formulas
            all_patterns: All detected patterns (optional)
            market_data: Market data for impact estimation (optional)

        Returns:
            List of innovation opportunities, sorted by priority
        """
        opportunities = []

        # 1. Gap Analysis: What's failing that shouldn't?
        prevention_opps = self._analyze_prevention_opportunities(
            failure_patterns, market_data
        )
        opportunities.extend(prevention_opps)

        # 2. Cross-Pollination: Can success in one domain apply to another?
        transfer_opps = self._analyze_cross_domain_transfers(success_formulas)
        opportunities.extend(transfer_opps)

        # 3. Material Evolution: Are there better materials emerging?
        material_opps = self._analyze_material_trends(all_patterns or [])
        opportunities.extend(material_opps)

        # 4. Design Evolution: Are there design patterns emerging?
        design_opps = self._analyze_design_trends(all_patterns or [])
        opportunities.extend(design_opps)

        # 5. Gap Filling: Unmet needs
        gap_opps = self._identify_ecosystem_gaps(failure_patterns, success_formulas)
        opportunities.extend(gap_opps)

        # Sort by priority score
        opportunities.sort(key=lambda x: float(x.priority_score), reverse=True)

        self._discovered_opportunities.extend(opportunities)
        logger.info(f"Discovered {len(opportunities)} innovation opportunities")

        return opportunities

    def _analyze_prevention_opportunities(
        self,
        failure_patterns: List[DetectedPattern],
        market_data: Optional[Dict[str, Any]] = None,
    ) -> List[InnovationOpportunity]:
        """Analyze failure patterns for prevention opportunities"""
        opportunities = []

        for pattern in failure_patterns:
            if pattern.layer not in [PatternLayer.STATISTICAL, PatternLayer.BEHAVIORAL]:
                continue

            # Check if this is a preventable failure
            evidence = pattern.evidence
            failure_count = evidence.get("count", pattern.sample_size)

            if failure_count < self.config.min_failure_frequency:
                continue

            # Estimate market size
            market_size = self._estimate_market_size(pattern, market_data)

            # Generate solution hypothesis
            solution = self._generate_solution_hypothesis(pattern)

            # Calculate priority
            priority = self._calculate_priority(
                failure_count, market_size, float(pattern.confidence)
            )

            opportunity = InnovationOpportunity(
                opportunity_type=OpportunityType.PREVENTION_INNOVATION,
                title=f"Prevent: {pattern.name}",
                description=(
                    f"Innovation opportunity to prevent '{pattern.name}' "
                    f"affecting {failure_count} instances"
                ),
                problem_statement=pattern.description,
                proposed_solution=solution,
                affected_market_size=market_size,
                estimated_impact_score=pattern.significance_score,
                priority_score=Decimal(str(priority)),
                supporting_patterns=[pattern.pattern_id],
                confidence=pattern.confidence,
                status="identified",
            )
            opportunities.append(opportunity)

        return opportunities

    def _analyze_cross_domain_transfers(
        self,
        success_formulas: List[SuccessFormula],
    ) -> List[InnovationOpportunity]:
        """Identify opportunities for cross-domain knowledge transfer"""
        opportunities = []

        if len(success_formulas) < 2:
            return opportunities

        # Group formulas by domain
        by_domain: Dict[str, List[SuccessFormula]] = defaultdict(list)
        for formula in success_formulas:
            by_domain[formula.domain].append(formula)

        domains = list(by_domain.keys())

        # Check each pair of domains
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i + 1:]:
                transfers = self._find_transferable_insights(
                    domain1, by_domain[domain1],
                    domain2, by_domain[domain2],
                )

                for transfer in transfers:
                    opportunity = InnovationOpportunity(
                        opportunity_type=OpportunityType.CROSS_DOMAIN_TRANSFER,
                        title=f"Transfer: {domain1} -> {domain2}",
                        description=transfer["description"],
                        problem_statement=(
                            f"Success pattern in {domain1} not yet applied to {domain2}"
                        ),
                        proposed_solution=transfer["solution"],
                        source_domain=domain1,
                        target_domain=domain2,
                        success_principle=transfer["principle"],
                        estimated_impact_score=Decimal(str(transfer["impact"])),
                        priority_score=Decimal(str(transfer["priority"])),
                        confidence=Decimal(str(transfer["confidence"])),
                        status="identified",
                    )
                    opportunities.append(opportunity)

        return opportunities

    def _analyze_material_trends(
        self,
        patterns: List[DetectedPattern],
    ) -> List[InnovationOpportunity]:
        """Analyze trends in material usage and performance"""
        opportunities = []

        # Look for evolution patterns related to materials
        material_patterns = [
            p for p in patterns
            if p.layer == PatternLayer.INNOVATION
            and "material" in p.pattern_type.lower()
        ]

        for pattern in material_patterns:
            evidence = pattern.evidence

            opportunity = InnovationOpportunity(
                opportunity_type=OpportunityType.MATERIAL_EVOLUTION,
                title=f"Material Opportunity: {pattern.name}",
                description=pattern.description,
                problem_statement=evidence.get("problem", "Material improvement opportunity"),
                proposed_solution=evidence.get("solution", "Investigate advanced materials"),
                estimated_impact_score=pattern.significance_score,
                priority_score=Decimal(str(float(pattern.significance_score) * 0.8)),
                supporting_patterns=[pattern.pattern_id],
                confidence=pattern.confidence,
                status="identified",
            )
            opportunities.append(opportunity)

        return opportunities

    def _analyze_design_trends(
        self,
        patterns: List[DetectedPattern],
    ) -> List[InnovationOpportunity]:
        """Analyze emerging design patterns"""
        opportunities = []

        # Look for evolution patterns related to design
        design_patterns = [
            p for p in patterns
            if p.layer == PatternLayer.INNOVATION
            and ("design" in p.pattern_type.lower() or "evolution" in p.pattern_type.lower())
        ]

        for pattern in design_patterns:
            evidence = pattern.evidence

            opportunity = InnovationOpportunity(
                opportunity_type=OpportunityType.DESIGN_EVOLUTION,
                title=f"Design Evolution: {pattern.name}",
                description=pattern.description,
                problem_statement=evidence.get("current_limitation", "Design improvement opportunity"),
                proposed_solution=evidence.get("emerging_trend", "Follow design evolution trend"),
                estimated_impact_score=pattern.significance_score,
                priority_score=Decimal(str(float(pattern.significance_score) * 0.7)),
                supporting_patterns=[pattern.pattern_id],
                confidence=pattern.confidence,
                status="identified",
            )
            opportunities.append(opportunity)

        return opportunities

    def _identify_ecosystem_gaps(
        self,
        failure_patterns: List[DetectedPattern],
        success_formulas: List[SuccessFormula],
    ) -> List[InnovationOpportunity]:
        """Identify gaps in the parts ecosystem"""
        opportunities = []

        # Find failure modes without corresponding success formulas
        failure_domains = set()
        for pattern in failure_patterns:
            domain = pattern.evidence.get("domain", "unknown")
            failure_domains.add(domain)

        success_domains = set(f.domain for f in success_formulas)

        # Domains with failures but no success formulas
        gap_domains = failure_domains - success_domains

        for domain in gap_domains:
            domain_failures = [
                p for p in failure_patterns
                if p.evidence.get("domain") == domain
            ]

            if domain_failures:
                total_failures = sum(p.sample_size for p in domain_failures)

                opportunity = InnovationOpportunity(
                    opportunity_type=OpportunityType.GAP_FILLING,
                    title=f"Solution Gap: {domain}",
                    description=(
                        f"No success formulas exist for {domain} domain "
                        f"despite {total_failures} recorded failures"
                    ),
                    problem_statement=f"Unaddressed failure patterns in {domain}",
                    proposed_solution="Develop standardized success patterns for this domain",
                    affected_market_size=int(total_failures * self.config.market_size_multiplier),
                    estimated_impact_score=Decimal("0.7"),
                    priority_score=Decimal(str(min(total_failures / 100, 1.0))),
                    supporting_patterns=[p.pattern_id for p in domain_failures],
                    confidence=Decimal("0.6"),
                    status="identified",
                )
                opportunities.append(opportunity)

        return opportunities

    def _find_transferable_insights(
        self,
        domain1: str,
        formulas1: List[SuccessFormula],
        domain2: str,
        formulas2: List[SuccessFormula],
    ) -> List[Dict[str, Any]]:
        """Find insights that could transfer between domains"""
        transfers = []

        # Find high-success formulas in domain1
        high_success = [f for f in formulas1 if float(f.success_rate) >= 0.9]

        for formula in high_success:
            # Check if similar formula exists in domain2
            has_similar = any(
                self._formula_similarity(formula, f2) > self.config.cross_domain_similarity_threshold
                for f2 in formulas2
            )

            if not has_similar:
                transfers.append({
                    "description": (
                        f"Apply '{formula.name}' pattern from {domain1} to {domain2}"
                    ),
                    "principle": formula.name,
                    "solution": (
                        f"Adapt success pattern with {float(formula.success_rate):.0%} "
                        f"success rate for {domain2} applications"
                    ),
                    "impact": float(formula.success_rate) * 0.7,
                    "priority": float(formula.success_rate) * float(formula.confidence_score),
                    "confidence": float(formula.confidence_score) * 0.8,
                })

        return transfers

    def _formula_similarity(
        self,
        f1: SuccessFormula,
        f2: SuccessFormula,
    ) -> float:
        """Calculate similarity between two formulas"""
        # Simple similarity based on required parts overlap
        parts1 = set(p.get("part_type", "") for p in f1.required_parts)
        parts2 = set(p.get("part_type", "") for p in f2.required_parts)

        if not parts1 or not parts2:
            return 0.0

        overlap = len(parts1 & parts2)
        total = len(parts1 | parts2)

        return overlap / total if total > 0 else 0.0

    def _estimate_market_size(
        self,
        pattern: DetectedPattern,
        market_data: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Estimate market size for an opportunity"""
        base_size = pattern.sample_size

        if market_data:
            # Use market data if available
            multiplier = market_data.get("failure_to_market_multiplier", self.config.market_size_multiplier)
        else:
            multiplier = self.config.market_size_multiplier

        return int(base_size * multiplier)

    def _generate_solution_hypothesis(
        self,
        pattern: DetectedPattern,
    ) -> str:
        """Generate a hypothesis for solving a failure pattern"""
        evidence = pattern.evidence
        pattern_type = pattern.pattern_type.lower()

        if "corrosion" in pattern_type or "environmental" in pattern_type:
            return "Develop corrosion-resistant coatings or materials"
        elif "fatigue" in pattern_type or "cyclic" in pattern_type:
            return "Investigate higher-strength materials or design improvements"
        elif "wear" in pattern_type:
            return "Evaluate harder surface treatments or improved lubrication"
        elif "installation" in pattern_type or "assembly" in pattern_type:
            return "Create installation guidance system or improved part design"
        elif "thermal" in pattern_type:
            return "Develop heat-resistant materials or thermal management solutions"
        else:
            return f"Investigate root cause and develop preventive solution for {pattern.name}"

    def _calculate_priority(
        self,
        failure_count: int,
        market_size: int,
        confidence: float,
    ) -> float:
        """Calculate priority score for an opportunity"""
        # Normalize factors
        count_factor = min(failure_count / 100, 1.0)
        market_factor = min(market_size / 100000, 1.0)
        confidence_factor = confidence

        # Weighted combination
        priority = (count_factor * 0.3 + market_factor * 0.4 + confidence_factor * 0.3)
        return min(priority, 1.0)

    def get_opportunities_by_type(
        self,
        opportunity_type: OpportunityType,
    ) -> List[InnovationOpportunity]:
        """Get opportunities of a specific type"""
        return [
            o for o in self._discovered_opportunities
            if o.opportunity_type == opportunity_type
        ]

    def get_top_opportunities(
        self,
        limit: int = 10,
    ) -> List[InnovationOpportunity]:
        """Get top opportunities by priority"""
        sorted_opps = sorted(
            self._discovered_opportunities,
            key=lambda x: float(x.priority_score),
            reverse=True
        )
        return sorted_opps[:limit]
