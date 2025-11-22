"""
ORACLE Tolerance Stack Analyzer
Statistical and worst-case tolerance analysis for assemblies.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math
import random


class DistributionType(Enum):
    """Statistical distribution for tolerance."""
    NORMAL = "NORMAL"
    UNIFORM = "UNIFORM"
    TRIANGULAR = "TRIANGULAR"


@dataclass
class Dimension:
    """A single dimension with tolerances."""
    name: str
    nominal: float
    tolerance_plus: float
    tolerance_minus: float
    distribution: DistributionType = DistributionType.NORMAL
    contributes_positive: bool = True  # True if adds to stack, False if subtracts

    @property
    def tolerance_band(self) -> float:
        """Total tolerance band width."""
        return self.tolerance_plus - self.tolerance_minus

    @property
    def mean(self) -> float:
        """Mean value (nominal + center of tolerance)."""
        return self.nominal + (self.tolerance_plus + self.tolerance_minus) / 2

    @property
    def std_dev(self) -> float:
        """Standard deviation (assuming 3-sigma coverage)."""
        return self.tolerance_band / 6


@dataclass
class ToleranceStackResult:
    """Complete tolerance stack analysis result."""
    nominal: float

    # Worst-case analysis
    worst_case_min: float
    worst_case_max: float
    worst_case_range: float

    # RSS (Root Sum Square) statistical analysis
    rss_mean: float
    rss_3sigma_min: float
    rss_3sigma_max: float
    rss_3sigma_range: float

    # Monte Carlo simulation
    monte_carlo_mean: float
    monte_carlo_std: float
    monte_carlo_min: float
    monte_carlo_max: float
    monte_carlo_99_min: float
    monte_carlo_99_max: float

    # Specification check
    probability_within_spec: float
    meets_spec: bool

    # Analysis details
    critical_contributors: List[Tuple[str, float]]  # (name, contribution %)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class AssemblySpec:
    """Assembly specification for tolerance check."""
    target: float
    upper_limit: float
    lower_limit: float


class ToleranceStackAnalyzer:
    """
    Performs tolerance stack analysis using multiple methods.

    Methods:
    - Worst Case: Sum of all max tolerances
    - RSS (Root Sum Square): Statistical 3-sigma approach
    - Monte Carlo: Probabilistic simulation
    """

    def __init__(self, monte_carlo_iterations: int = 10000):
        self.monte_carlo_iterations = monte_carlo_iterations

    def analyze_assembly(
        self,
        dimensions: List[Dimension],
        specification: Optional[AssemblySpec] = None
    ) -> ToleranceStackResult:
        """
        Complete tolerance stack analysis.

        Args:
            dimensions: List of contributing dimensions
            specification: Optional assembly specification to check against

        Returns:
            ToleranceStackResult with all analysis methods
        """
        if not dimensions:
            return ToleranceStackResult(
                nominal=0, worst_case_min=0, worst_case_max=0, worst_case_range=0,
                rss_mean=0, rss_3sigma_min=0, rss_3sigma_max=0, rss_3sigma_range=0,
                monte_carlo_mean=0, monte_carlo_std=0, monte_carlo_min=0,
                monte_carlo_max=0, monte_carlo_99_min=0, monte_carlo_99_max=0,
                probability_within_spec=0, meets_spec=False,
                critical_contributors=[]
            )

        # Calculate nominal
        nominal = sum(
            d.nominal * (1 if d.contributes_positive else -1)
            for d in dimensions
        )

        # Worst-case analysis
        worst_case = self._worst_case_analysis(dimensions)

        # RSS analysis
        rss = self._rss_analysis(dimensions)

        # Monte Carlo simulation
        monte_carlo = self._monte_carlo_analysis(dimensions)

        # Check specification
        if specification:
            prob_within = self._probability_within_spec(
                monte_carlo["samples"],
                specification
            )
            meets_spec = prob_within >= 0.997  # 99.7% confidence (3-sigma)
        else:
            prob_within = 1.0
            meets_spec = True

        # Identify critical contributors
        critical = self._identify_critical_contributors(dimensions)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            dimensions, worst_case, rss, specification
        )

        return ToleranceStackResult(
            nominal=nominal,
            worst_case_min=worst_case["min"],
            worst_case_max=worst_case["max"],
            worst_case_range=worst_case["range"],
            rss_mean=rss["mean"],
            rss_3sigma_min=rss["min"],
            rss_3sigma_max=rss["max"],
            rss_3sigma_range=rss["range"],
            monte_carlo_mean=monte_carlo["mean"],
            monte_carlo_std=monte_carlo["std"],
            monte_carlo_min=monte_carlo["min"],
            monte_carlo_max=monte_carlo["max"],
            monte_carlo_99_min=monte_carlo["p0.5"],
            monte_carlo_99_max=monte_carlo["p99.5"],
            probability_within_spec=prob_within,
            meets_spec=meets_spec,
            critical_contributors=critical,
            recommendations=recommendations
        )

    def _worst_case_analysis(self, dimensions: List[Dimension]) -> Dict:
        """
        Worst-case analysis: all tolerances at their limits.
        Conservative but may overestimate variation.
        """
        worst_min = 0.0
        worst_max = 0.0

        for d in dimensions:
            if d.contributes_positive:
                worst_min += d.nominal + d.tolerance_minus
                worst_max += d.nominal + d.tolerance_plus
            else:
                worst_min -= (d.nominal + d.tolerance_plus)
                worst_max -= (d.nominal + d.tolerance_minus)

        return {
            "min": worst_min,
            "max": worst_max,
            "range": worst_max - worst_min
        }

    def _rss_analysis(self, dimensions: List[Dimension]) -> Dict:
        """
        RSS (Root Sum Square) statistical analysis.
        Assumes normal distributions and combines statistically.
        """
        mean = sum(
            d.mean * (1 if d.contributes_positive else -1)
            for d in dimensions
        )

        # RSS of standard deviations
        variance = sum(d.std_dev ** 2 for d in dimensions)
        std = math.sqrt(variance)

        return {
            "mean": mean,
            "std": std,
            "min": mean - 3 * std,
            "max": mean + 3 * std,
            "range": 6 * std
        }

    def _monte_carlo_analysis(self, dimensions: List[Dimension]) -> Dict:
        """
        Monte Carlo simulation for complex distributions.
        """
        samples = []

        for _ in range(self.monte_carlo_iterations):
            value = 0.0
            for d in dimensions:
                sample = self._sample_dimension(d)
                if d.contributes_positive:
                    value += sample
                else:
                    value -= sample
            samples.append(value)

        samples.sort()
        n = len(samples)

        return {
            "samples": samples,
            "mean": sum(samples) / n,
            "std": math.sqrt(sum((x - sum(samples)/n)**2 for x in samples) / n),
            "min": min(samples),
            "max": max(samples),
            "p0.5": samples[int(n * 0.005)],
            "p99.5": samples[int(n * 0.995)],
        }

    def _sample_dimension(self, d: Dimension) -> float:
        """Generate a random sample from dimension's distribution."""
        if d.distribution == DistributionType.NORMAL:
            # Use Box-Muller for normal distribution
            return random.gauss(d.mean, d.std_dev)
        elif d.distribution == DistributionType.UNIFORM:
            return random.uniform(
                d.nominal + d.tolerance_minus,
                d.nominal + d.tolerance_plus
            )
        elif d.distribution == DistributionType.TRIANGULAR:
            return random.triangular(
                d.nominal + d.tolerance_minus,
                d.nominal + d.tolerance_plus,
                d.nominal
            )
        else:
            return d.nominal

    def _probability_within_spec(
        self,
        samples: List[float],
        spec: AssemblySpec
    ) -> float:
        """Calculate probability of assembly meeting specification."""
        in_spec = sum(
            1 for s in samples
            if spec.lower_limit <= s <= spec.upper_limit
        )
        return in_spec / len(samples)

    def _identify_critical_contributors(
        self,
        dimensions: List[Dimension]
    ) -> List[Tuple[str, float]]:
        """
        Identify dimensions that contribute most to variation.
        Returns list of (name, contribution_percent).
        """
        total_variance = sum(d.std_dev ** 2 for d in dimensions)

        if total_variance == 0:
            return []

        contributions = [
            (d.name, (d.std_dev ** 2 / total_variance) * 100)
            for d in dimensions
        ]

        # Sort by contribution (highest first)
        contributions.sort(key=lambda x: x[1], reverse=True)

        return contributions

    def _generate_recommendations(
        self,
        dimensions: List[Dimension],
        worst_case: Dict,
        rss: Dict,
        spec: Optional[AssemblySpec]
    ) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []

        # Check if RSS is significantly better than worst-case
        if worst_case["range"] > 2 * rss["range"]:
            recommendations.append(
                "Statistical tolerance analysis shows significant improvement over worst-case"
            )

        # Identify largest contributors
        contributions = self._identify_critical_contributors(dimensions)
        if contributions and contributions[0][1] > 50:
            recommendations.append(
                f"'{contributions[0][0]}' contributes {contributions[0][1]:.1f}% of variation - "
                "consider tightening this tolerance first"
            )

        # Check specification
        if spec:
            if worst_case["min"] < spec.lower_limit or worst_case["max"] > spec.upper_limit:
                recommendations.append(
                    "Worst-case analysis exceeds specification - "
                    "statistical approach or tighter tolerances required"
                )

        return recommendations

    def analyze_clearance_fit(
        self,
        shaft: Dimension,
        hole: Dimension
    ) -> Dict:
        """
        Analyze clearance fit between shaft and hole.

        Returns:
            Analysis including min/max clearance and probability of fit.
        """
        # Calculate clearance (hole - shaft)
        dimensions = [
            Dimension(
                name="hole",
                nominal=hole.nominal,
                tolerance_plus=hole.tolerance_plus,
                tolerance_minus=hole.tolerance_minus,
                contributes_positive=True
            ),
            Dimension(
                name="shaft",
                nominal=shaft.nominal,
                tolerance_plus=shaft.tolerance_plus,
                tolerance_minus=shaft.tolerance_minus,
                contributes_positive=False
            )
        ]

        result = self.analyze_assembly(dimensions)

        # Check for interference (negative clearance)
        interference_probability = 0.0
        if hasattr(result, 'monte_carlo_min') and result.monte_carlo_min < 0:
            # Count samples below zero
            samples = self._monte_carlo_analysis(dimensions)["samples"]
            interference_probability = sum(1 for s in samples if s < 0) / len(samples)

        return {
            "min_clearance_worst": result.worst_case_min,
            "max_clearance_worst": result.worst_case_max,
            "mean_clearance": result.rss_mean,
            "clearance_3sigma_range": result.rss_3sigma_range,
            "interference_probability": interference_probability,
            "fit_type": self._classify_fit(result.worst_case_min, result.worst_case_max)
        }

    def _classify_fit(self, min_clearance: float, max_clearance: float) -> str:
        """Classify the type of fit."""
        if min_clearance > 0:
            return "CLEARANCE_FIT"
        elif max_clearance < 0:
            return "INTERFERENCE_FIT"
        else:
            return "TRANSITION_FIT"
