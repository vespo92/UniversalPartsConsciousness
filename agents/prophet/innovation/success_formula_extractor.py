"""
Success Formula Extractor
Identifies what makes assemblies and part combinations successful.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from ..types import Assembly, SuccessFormula, SwarmKnowledge


logger = logging.getLogger(__name__)


@dataclass
class ExtractionConfig:
    """Configuration for success formula extraction"""
    min_success_rate: float = 0.85
    min_sample_size: int = 10
    min_lifespan_improvement: float = 0.2
    confidence_threshold: float = 0.7


class SuccessFormulaExtractor:
    """
    Identifies what makes assemblies and part combinations successful.

    Analyzes:
    - Common patterns in successful assemblies
    - Part combinations with high success rates
    - Configuration parameters that correlate with success
    - Environmental conditions that favor success
    """

    def __init__(self, config: Optional[ExtractionConfig] = None):
        self.config = config or ExtractionConfig()
        self._extracted_formulas: List[SuccessFormula] = []

    def extract_success_formulas(
        self,
        successful_assemblies: List[Assembly],
        all_assemblies: Optional[List[Assembly]] = None,
        swarm_knowledge: Optional[Dict[str, SwarmKnowledge]] = None,
    ) -> List[SuccessFormula]:
        """
        Analyze successful assemblies to find repeatable patterns.

        Args:
            successful_assemblies: List of assemblies that succeeded
            all_assemblies: All assemblies for comparison (optional)
            swarm_knowledge: Knowledge from part swarms (optional)

        Returns:
            List of extracted success formulas
        """
        formulas = []

        if len(successful_assemblies) < self.config.min_sample_size:
            return formulas

        # Group assemblies by application domain
        domains = self._group_by_domain(successful_assemblies)

        for domain, domain_assemblies in domains.items():
            if len(domain_assemblies) < 5:
                continue

            # Find common patterns in successful assemblies
            patterns = self._find_common_patterns(domain_assemblies, all_assemblies)

            for pattern in patterns:
                formula = self._create_formula(domain, pattern, domain_assemblies)
                if formula.success_rate >= Decimal(str(self.config.min_success_rate)):
                    formulas.append(formula)
                    self._extracted_formulas.append(formula)

        # Incorporate swarm knowledge if available
        if swarm_knowledge:
            swarm_formulas = self._extract_from_swarm_knowledge(swarm_knowledge)
            formulas.extend(swarm_formulas)

        logger.info(f"Extracted {len(formulas)} success formulas")
        return formulas

    def _group_by_domain(
        self,
        assemblies: List[Assembly],
    ) -> Dict[str, List[Assembly]]:
        """Group assemblies by their application domain"""
        domains: Dict[str, List[Assembly]] = defaultdict(list)
        for assembly in assemblies:
            domains[assembly.domain].append(assembly)
        return domains

    def _find_common_patterns(
        self,
        successful: List[Assembly],
        all_assemblies: Optional[List[Assembly]] = None,
    ) -> List[Dict[str, Any]]:
        """Find patterns common across successful assemblies"""
        patterns = []

        # Count part occurrences
        part_counts: Dict[str, int] = defaultdict(int)
        pair_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        config_counts: Dict[str, Dict[Any, int]] = defaultdict(lambda: defaultdict(int))

        for assembly in successful:
            parts = sorted(set(assembly.parts))
            for part in parts:
                part_counts[part] += 1

            # Count pairs
            for i, p1 in enumerate(parts):
                for p2 in parts[i + 1:]:
                    pair_counts[(p1, p2)] += 1

            # Count configurations
            for key, value in assembly.configuration.items():
                config_counts[key][str(value)] += 1

        total = len(successful)

        # Find frequent parts (>50% occurrence)
        frequent_parts = {
            part for part, count in part_counts.items()
            if count / total >= 0.5
        }

        # Find frequent pairs
        frequent_pairs = {
            pair for pair, count in pair_counts.items()
            if count / total >= 0.4
        }

        # Find frequent configurations
        frequent_configs = {}
        for key, value_counts in config_counts.items():
            for value, count in value_counts.items():
                if count / total >= 0.5:
                    frequent_configs[key] = value

        # Build pattern
        if frequent_parts or frequent_configs:
            # Calculate success rate vs baseline
            success_rate = 1.0  # All are successful by definition
            failure_reduction = 0.0

            if all_assemblies:
                # Calculate how this pattern performs across all assemblies
                matching = self._find_matching_assemblies(
                    all_assemblies, frequent_parts, frequent_configs
                )
                if matching:
                    success_rate = sum(1 for a in matching if a.success) / len(matching)
                    baseline = sum(1 for a in all_assemblies if a.success) / len(all_assemblies)
                    failure_reduction = (success_rate - baseline) / (1 - baseline) if baseline < 1 else 0

            # Calculate average lifespan
            lifespans = [a.lifespan_hours for a in successful if a.lifespan_hours]
            avg_lifespan = sum(lifespans) / len(lifespans) if lifespans else 0

            patterns.append({
                "required_parts": list(frequent_parts),
                "frequent_pairs": list(frequent_pairs),
                "configurations": frequent_configs,
                "success_rate": success_rate,
                "failure_reduction": failure_reduction,
                "avg_lifespan": avg_lifespan,
                "sample_size": total,
            })

        return patterns

    def _find_matching_assemblies(
        self,
        assemblies: List[Assembly],
        required_parts: Set[str],
        required_configs: Dict[str, Any],
    ) -> List[Assembly]:
        """Find assemblies matching the pattern"""
        matching = []
        for assembly in assemblies:
            # Check parts
            if required_parts and not required_parts.issubset(set(assembly.parts)):
                continue

            # Check configurations
            config_match = True
            for key, value in required_configs.items():
                if str(assembly.configuration.get(key)) != value:
                    config_match = False
                    break

            if config_match:
                matching.append(assembly)

        return matching

    def _create_formula(
        self,
        domain: str,
        pattern: Dict[str, Any],
        assemblies: List[Assembly],
    ) -> SuccessFormula:
        """Create a SuccessFormula from a pattern"""
        # Generate a memorable name
        name = self._generate_formula_name(domain, pattern)

        # Extract material requirements
        materials = self._extract_material_requirements(assemblies)

        # Extract environmental limits
        env_limits = self._extract_environmental_limits(assemblies)

        # Find optional and forbidden parts
        optional_parts = self._find_optional_parts(assemblies, set(pattern["required_parts"]))
        forbidden_parts = self._find_forbidden_parts(assemblies)

        return SuccessFormula(
            name=name,
            domain=domain,
            required_parts=[{"part_type": p} for p in pattern["required_parts"]],
            optional_parts=[{"part_type": p} for p in optional_parts],
            forbidden_parts=[{"part_type": p} for p in forbidden_parts],
            configuration=pattern["configurations"],
            material_requirements=materials,
            environmental_limits=env_limits,
            success_rate=Decimal(str(pattern["success_rate"])),
            average_lifespan_hours=int(pattern["avg_lifespan"]),
            failure_reduction_percent=Decimal(str(pattern["failure_reduction"] * 100)),
            sample_size=pattern["sample_size"],
            confidence_score=self._calculate_confidence(pattern),
            example_assemblies=[a.id for a in assemblies[:10]],
            status="proposed",
        )

    def _generate_formula_name(
        self,
        domain: str,
        pattern: Dict[str, Any],
    ) -> str:
        """Generate a memorable name for the success formula"""
        domain_name = domain.replace("_", " ").title()

        # Find key differentiator
        if pattern["required_parts"]:
            key_part = pattern["required_parts"][0]
            key_name = key_part.split("_")[0].title() if "_" in key_part else key_part[:10].title()
        else:
            key_name = "Standard"

        return f"The {domain_name} {key_name} Formula"

    def _extract_material_requirements(
        self,
        assemblies: List[Assembly],
    ) -> List[str]:
        """Extract common material requirements"""
        materials: Dict[str, int] = defaultdict(int)

        for assembly in assemblies:
            for material in assembly.configuration.get("materials", []):
                materials[material] += 1

        # Return materials present in >50% of assemblies
        threshold = len(assemblies) * 0.5
        return [m for m, c in materials.items() if c >= threshold]

    def _extract_environmental_limits(
        self,
        assemblies: List[Assembly],
    ) -> Dict[str, Any]:
        """Extract environmental limits from successful assemblies"""
        limits = {}

        temps = []
        pressures = []

        for assembly in assemblies:
            env = assembly.configuration.get("environment", {})
            if "max_temp" in env:
                temps.append(env["max_temp"])
            if "max_pressure" in env:
                pressures.append(env["max_pressure"])

        if temps:
            limits["max_temperature"] = max(temps)
            limits["min_temperature"] = min(temps)
        if pressures:
            limits["max_pressure"] = max(pressures)

        return limits

    def _find_optional_parts(
        self,
        assemblies: List[Assembly],
        required: Set[str],
    ) -> List[str]:
        """Find parts that appear often but aren't required"""
        part_counts: Dict[str, int] = defaultdict(int)

        for assembly in assemblies:
            for part in assembly.parts:
                if part not in required:
                    part_counts[part] += 1

        # Optional = present in 20-50% of assemblies
        total = len(assemblies)
        return [
            p for p, c in part_counts.items()
            if 0.2 <= c / total < 0.5
        ]

    def _find_forbidden_parts(
        self,
        assemblies: List[Assembly],
    ) -> List[str]:
        """Find parts that are never present in successful assemblies"""
        # Would need access to failed assemblies to identify
        # For now, return empty
        return []

    def _calculate_confidence(
        self,
        pattern: Dict[str, Any],
    ) -> Decimal:
        """Calculate confidence score for the formula"""
        sample_factor = min(pattern["sample_size"] / 50, 1.0)
        success_factor = pattern["success_rate"]
        reduction_factor = min(pattern["failure_reduction"] * 2, 1.0) if pattern["failure_reduction"] > 0 else 0.5

        confidence = (sample_factor * 0.3 + success_factor * 0.4 + reduction_factor * 0.3)
        return Decimal(str(min(confidence, 0.95)))

    def _extract_from_swarm_knowledge(
        self,
        swarm_knowledge: Dict[str, SwarmKnowledge],
    ) -> List[SuccessFormula]:
        """Extract formulas from collective swarm knowledge"""
        formulas = []

        for swarm_id, knowledge in swarm_knowledge.items():
            if knowledge.success_patterns:
                for pattern_desc in knowledge.success_patterns[:3]:
                    formula = SuccessFormula(
                        name=f"Swarm {swarm_id[:8]} Pattern",
                        domain="swarm_derived",
                        required_parts=[],
                        success_rate=Decimal(str(0.8)),  # Estimated
                        sample_size=knowledge.member_count,
                        confidence_score=Decimal(str(float(knowledge.emergence_score) * 0.8)),
                        status="proposed",
                    )
                    formulas.append(formula)

        return formulas

    def get_formulas_by_domain(
        self,
        domain: str,
    ) -> List[SuccessFormula]:
        """Get extracted formulas for a specific domain"""
        return [f for f in self._extracted_formulas if f.domain == domain]

    def validate_formula(
        self,
        formula_id: str,
        validation_data: Dict[str, Any],
    ) -> bool:
        """Validate a formula against new data"""
        for formula in self._extracted_formulas:
            if formula.id == formula_id:
                formula.status = "validated"
                return True
        return False
