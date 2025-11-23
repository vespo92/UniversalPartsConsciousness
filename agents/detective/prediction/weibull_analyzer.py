"""
Weibull Distribution Analyzer

Reliability statistics using Weibull analysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import math


@dataclass
class WeibullParameters:
    """Weibull distribution parameters"""
    beta: float  # Shape parameter
    eta: float   # Scale parameter (characteristic life)
    gamma: float  # Location parameter (minimum life)


@dataclass
class WeibullAnalysisResult:
    """Result of Weibull analysis"""
    parameters: WeibullParameters
    b10_life: float
    b50_life: float
    mean_life: float
    failure_mode_indication: str
    confidence: float


class WeibullAnalyzer:
    """
    Weibull distribution analysis for reliability prediction.

    The Weibull distribution is fundamental to reliability engineering:
    - Beta < 1: Infant mortality (decreasing failure rate)
    - Beta = 1: Random failures (constant failure rate, exponential)
    - Beta > 1: Wear-out failures (increasing failure rate)
    """

    # Typical beta values for different failure modes
    TYPICAL_BETA_VALUES = {
        "infant_mortality": 0.5,      # Manufacturing defects
        "random": 1.0,                 # Random failures
        "early_wear": 1.5,            # Early wear-out
        "fatigue": 2.5,               # Typical fatigue
        "ball_bearing_fatigue": 1.5,  # Ball bearing fatigue
        "roller_bearing_fatigue": 1.1,  # Roller bearing
        "corrosion": 2.0,             # Corrosion
        "stress_rupture": 3.0,        # Creep/stress rupture
    }

    def __init__(self):
        """Initialize the Weibull analyzer."""
        pass

    def analyze_failure_data(
        self,
        failure_times: List[float],
        censored_times: Optional[List[float]] = None
    ) -> WeibullAnalysisResult:
        """
        Analyze failure time data to estimate Weibull parameters.

        Args:
            failure_times: List of times to failure
            censored_times: Optional list of censored (suspended) times

        Returns:
            Weibull analysis results
        """
        if not failure_times:
            raise ValueError("At least one failure time required")

        # Use median rank regression for parameter estimation
        n = len(failure_times)
        sorted_times = sorted(failure_times)

        # Calculate median ranks (Bernard's approximation)
        ranks = [(i - 0.3) / (n + 0.4) for i in range(1, n + 1)]

        # Linearize: ln(ln(1/(1-F))) vs ln(t)
        # y = beta * x - beta * ln(eta)
        x_values = [math.log(t) for t in sorted_times]
        y_values = [math.log(math.log(1 / (1 - r))) for r in ranks]

        # Linear regression
        beta, ln_eta = self._linear_regression(x_values, y_values)
        eta = math.exp(ln_eta / beta) if beta != 0 else sorted_times[-1]

        # Assume gamma = 0 (2-parameter Weibull)
        gamma = 0

        params = WeibullParameters(beta=beta, eta=eta, gamma=gamma)

        # Calculate characteristic lives
        b10 = self._calculate_bx_life(params, 0.10)
        b50 = self._calculate_bx_life(params, 0.50)
        mean = eta * math.gamma(1 + 1/beta) if beta > 0 else eta

        # Interpret beta
        failure_indication = self._interpret_beta(beta)

        return WeibullAnalysisResult(
            parameters=params,
            b10_life=b10,
            b50_life=b50,
            mean_life=mean,
            failure_mode_indication=failure_indication,
            confidence=0.80 if n >= 10 else 0.60
        )

    def predict_reliability(
        self,
        params: WeibullParameters,
        time: float
    ) -> float:
        """
        Predict reliability at a given time.

        R(t) = exp(-((t-gamma)/eta)^beta)

        Args:
            params: Weibull parameters
            time: Time at which to calculate reliability

        Returns:
            Reliability (0-1)
        """
        if time <= params.gamma:
            return 1.0

        t_adjusted = time - params.gamma
        reliability = math.exp(-((t_adjusted / params.eta) ** params.beta))

        return reliability

    def predict_failure_probability(
        self,
        params: WeibullParameters,
        time: float
    ) -> float:
        """
        Predict cumulative failure probability at a given time.

        F(t) = 1 - R(t)

        Args:
            params: Weibull parameters
            time: Time at which to calculate probability

        Returns:
            Failure probability (0-1)
        """
        return 1 - self.predict_reliability(params, time)

    def calculate_hazard_rate(
        self,
        params: WeibullParameters,
        time: float
    ) -> float:
        """
        Calculate instantaneous hazard (failure) rate.

        h(t) = (beta/eta) * ((t-gamma)/eta)^(beta-1)

        Args:
            params: Weibull parameters
            time: Time at which to calculate hazard rate

        Returns:
            Hazard rate (failures per unit time)
        """
        if time <= params.gamma:
            return 0.0 if params.beta > 1 else float('inf') if params.beta < 1 else 1/params.eta

        t_adjusted = time - params.gamma
        hazard = (params.beta / params.eta) * ((t_adjusted / params.eta) ** (params.beta - 1))

        return hazard

    def estimate_from_l10_life(
        self,
        l10_life: float,
        failure_mode: str = "fatigue"
    ) -> WeibullParameters:
        """
        Estimate Weibull parameters from L10 life and typical beta.

        Args:
            l10_life: B10 (L10) life
            failure_mode: Type of failure for beta estimation

        Returns:
            Estimated Weibull parameters
        """
        beta = self.TYPICAL_BETA_VALUES.get(failure_mode, 2.0)

        # B10 life corresponds to 10% failure probability
        # F(B10) = 0.10 = 1 - exp(-(B10/eta)^beta)
        # Solving for eta: eta = B10 / (-ln(0.90))^(1/beta)
        eta = l10_life / ((-math.log(0.90)) ** (1 / beta))

        return WeibullParameters(beta=beta, eta=eta, gamma=0)

    def _calculate_bx_life(
        self,
        params: WeibullParameters,
        x: float
    ) -> float:
        """
        Calculate Bx (x% failure) life.

        Args:
            params: Weibull parameters
            x: Failure fraction (e.g., 0.10 for B10)

        Returns:
            Life at x% failure probability
        """
        # F(t) = x = 1 - exp(-(t/eta)^beta)
        # t = eta * (-ln(1-x))^(1/beta)
        return params.eta * ((-math.log(1 - x)) ** (1 / params.beta)) + params.gamma

    def _interpret_beta(self, beta: float) -> str:
        """Interpret beta value for failure mode indication."""
        if beta < 0.8:
            return "Infant mortality - early failures, check manufacturing quality"
        elif beta < 1.2:
            return "Random failures - constant failure rate, external causes likely"
        elif beta < 2.0:
            return "Early wear-out - gradual degradation beginning"
        elif beta < 4.0:
            return "Normal wear-out - fatigue or wear mechanism dominant"
        else:
            return "Rapid wear-out - aggressive degradation mechanism"

    def _linear_regression(
        self,
        x: List[float],
        y: List[float]
    ) -> Tuple[float, float]:
        """
        Simple linear regression: y = mx + b

        Returns: (slope m, intercept b)
        """
        n = len(x)
        if n < 2:
            return (2.0, 0.0)  # Default values

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)

        denom = n * sum_x2 - sum_x ** 2
        if abs(denom) < 1e-10:
            return (2.0, 0.0)

        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n

        return (slope, intercept)
