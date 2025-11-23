"""
ORACLE Deployment - Agent_2: Compatibility Oracle
==================================================

Standalone deployment module for the Compatibility Oracle.
Answers "will it fit?" with mathematical truth.

"Compatibility is not subjective. It is physics. It is mathematics.
It is the relationship between dimensions, materials, and forces."

Usage:
    # As module
    from agents.oracle.deploy import deploy_oracle, oracle_query

    # Deploy the ORACLE
    oracle = deploy_oracle()

    # Query compatibility
    result = oracle_query(oracle, part_a, part_b)

    # Command line
    python -m agents.oracle.deploy --check M8x1.25 M8x1.25
"""

import asyncio
import json
from dataclasses import asdict
from decimal import Decimal
from typing import Dict, Any, Optional, List

from .oracle_agent import OracleAgent, create_oracle_agent
from .engine.compatibility_core import (
    UniversalCompatibilityChecker,
    Part,
    ThreadSpec,
    MaterialSpec,
    DimensionSpec,
    AssemblyContext,
    CompatibilityResult,
    CompatibilityType,
)
from .engine.material_compatibility import MaterialCompatibilityChecker, Environment
from .engine.thread_calculator import ThreadEngagementCalculator
from .engine.strength_calculator import StrengthCalculator
from .engine.tolerance_analyzer import ToleranceStackAnalyzer


class OracleDeployment:
    """
    Standalone ORACLE deployment for direct compatibility queries.

    The Prophet of Perfect Fit - Mathematical truth for "will it fit?"
    """

    VERSION = "1.0.0"
    AGENT_ID = "AGENT_2"
    AGENT_ALIAS = "ORACLE"

    def __init__(self, cache_config: Optional[Dict] = None):
        """
        Initialize the ORACLE deployment.

        Args:
            cache_config: Optional cache configuration
        """
        self.agent = create_oracle_agent(cache_config=cache_config or {})

        # Direct access to core engines for standalone use
        self.compatibility_checker = self.agent.compatibility_checker
        self.material_checker = self.agent.material_checker
        self.tolerance_analyzer = self.agent.tolerance_analyzer
        self.failure_predictor = self.agent.failure_predictor
        self.substitution_engine = self.agent.substitution_engine

        # Statistics
        self.queries_processed = 0
        self.cache_hits = 0

    def check_compatibility(
        self,
        part_a: Dict[str, Any],
        part_b: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Check compatibility between two parts.

        Args:
            part_a: First part specification (dict or Part object)
            part_b: Second part specification (dict or Part object)
            context: Optional assembly context

        Returns:
            Compatibility result with confidence and analysis
        """
        result = self.agent.check_compatibility(part_a, part_b, context)
        self.queries_processed += 1
        return result

    def check_thread_compatibility(
        self,
        external_thread: Dict[str, Any],
        internal_thread: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check thread compatibility between bolt and nut/hole.

        Args:
            external_thread: Bolt thread specification
            internal_thread: Nut/hole thread specification

        Returns:
            Thread compatibility analysis with engagement quality
        """
        ext = self._dict_to_thread(external_thread)
        int_ = self._dict_to_thread(internal_thread)

        result = self.compatibility_checker.check_thread_compatibility(ext, int_)

        return {
            "is_compatible": result.is_compatible,
            "pitch_match": result.pitch_match,
            "diameter_match": result.diameter_match,
            "class_compatible": result.class_compatible,
            "direction_match": result.direction_match,
            "clearance_min_mm": result.clearance_min,
            "clearance_max_mm": result.clearance_max,
            "engagement_quality": result.engagement_quality,
            "warnings": result.warnings,
        }

    def check_galvanic_risk(
        self,
        material_a: str,
        material_b: str,
        environment: str = "indoor"
    ) -> Dict[str, Any]:
        """
        Check galvanic corrosion risk between materials.

        Args:
            material_a: First material type
            material_b: Second material type
            environment: Operating environment

        Returns:
            Galvanic risk assessment
        """
        risk = self.agent.get_galvanic_risk(material_a, material_b, environment)

        risk_descriptions = {
            "SAFE": "No galvanic corrosion concern",
            "LOW": "Minor galvanic risk - acceptable for most applications",
            "MODERATE": "Moderate risk - consider isolation or coating",
            "SEVERE": "High galvanic risk - isolation required or avoid combination",
        }

        return {
            "material_a": material_a,
            "material_b": material_b,
            "environment": environment,
            "risk_level": risk,
            "description": risk_descriptions.get(risk, "Unknown risk level"),
            "recommendation": self._get_galvanic_recommendation(risk),
        }

    def calculate_safety_factor(
        self,
        proof_load_kn: float,
        applied_load_kn: float,
        load_type: str = "static"
    ) -> Dict[str, Any]:
        """
        Calculate safety factor for a fastener.

        Args:
            proof_load_kn: Fastener proof load in kN
            applied_load_kn: Applied load in kN
            load_type: Type of loading (static, cyclic, impact)

        Returns:
            Safety factor analysis
        """
        sf = proof_load_kn / applied_load_kn if applied_load_kn > 0 else float('inf')

        # Recommended minimums by load type
        minimums = {
            "static": 2.0,
            "cyclic": 3.0,
            "impact": 4.0,
        }
        min_sf = minimums.get(load_type, 2.0)

        return {
            "safety_factor": round(sf, 2),
            "proof_load_kn": proof_load_kn,
            "applied_load_kn": applied_load_kn,
            "load_type": load_type,
            "minimum_required": min_sf,
            "is_adequate": sf >= min_sf,
            "margin_percent": round((sf / min_sf - 1) * 100, 1) if sf >= min_sf else round((sf / min_sf - 1) * 100, 1),
        }

    def predict_failure(
        self,
        condition: Dict[str, Any],
        mission_hours: float = 10000
    ) -> Dict[str, Any]:
        """
        Predict failure probability for a joint.

        Args:
            condition: Joint condition specification
            mission_hours: Expected service hours

        Returns:
            Failure prediction with risk assessment
        """
        return self.agent.predict_failure(condition, mission_hours)

    def find_substitutions(
        self,
        target_part: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find substitution recommendations for a part.

        Args:
            target_part: Part to find substitutions for
            context: Assembly context
            max_results: Maximum results to return

        Returns:
            Ranked list of substitution recommendations
        """
        return self.agent.find_substitutions(target_part, context, max_results)

    def get_status(self) -> Dict[str, Any]:
        """Get ORACLE deployment status."""
        return {
            "agent_id": self.AGENT_ID,
            "agent_alias": self.AGENT_ALIAS,
            "version": self.VERSION,
            "status": "ACTIVE",
            "queries_processed": self.queries_processed,
            "cache_stats": {
                "hits": self.cache_hits,
            },
            "capabilities": [
                "thread_compatibility",
                "material_compatibility",
                "dimensional_compatibility",
                "strength_verification",
                "galvanic_risk_assessment",
                "tolerance_stack_analysis",
                "failure_prediction",
                "substitution_recommendation",
            ],
        }

    def _dict_to_thread(self, data: Dict) -> ThreadSpec:
        """Convert dict to ThreadSpec."""
        return ThreadSpec(
            nominal_diameter=Decimal(str(data.get("diameter", data.get("nominal_diameter", 8)))),
            pitch=Decimal(str(data.get("pitch", 1.25))),
            thread_class=data.get("class", data.get("thread_class", "6g")),
            major_dia_min=Decimal(str(data.get("major_dia_min", 7.76))),
            major_dia_max=Decimal(str(data.get("major_dia_max", 7.97))),
            pitch_dia_min=Decimal(str(data.get("pitch_dia_min", 7.16))),
            pitch_dia_max=Decimal(str(data.get("pitch_dia_max", 7.35))),
            minor_dia_min=Decimal(str(data.get("minor_dia_min", 6.65))),
            minor_dia_max=Decimal(str(data.get("minor_dia_max", 6.91))),
            direction=data.get("direction", "right"),
        )

    def _get_galvanic_recommendation(self, risk: str) -> str:
        """Get recommendation based on galvanic risk."""
        recommendations = {
            "SAFE": "No special precautions needed",
            "LOW": "Monitor periodically, especially in humid conditions",
            "MODERATE": "Use isolation washers, coating, or barrier sealant",
            "SEVERE": "Avoid this combination or use full isolation (nylon washers, coating both surfaces)",
        }
        return recommendations.get(risk, "Consult materials engineer")


def deploy_oracle(cache_config: Optional[Dict] = None) -> OracleDeployment:
    """
    Deploy a standalone ORACLE instance.

    Args:
        cache_config: Optional cache configuration

    Returns:
        Configured OracleDeployment instance
    """
    return OracleDeployment(cache_config)


def oracle_query(
    oracle: OracleDeployment,
    part_a: Dict[str, Any],
    part_b: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute a compatibility query on deployed ORACLE.

    Args:
        oracle: Deployed ORACLE instance
        part_a: First part specification
        part_b: Second part specification
        context: Optional assembly context

    Returns:
        Compatibility result
    """
    return oracle.check_compatibility(part_a, part_b, context)


def quick_thread_check(
    diameter: float,
    pitch: float,
    external_class: str = "6g",
    internal_class: str = "6H"
) -> Dict[str, Any]:
    """
    Quick thread compatibility check for common use case.

    Args:
        diameter: Nominal diameter in mm
        pitch: Thread pitch in mm
        external_class: External thread tolerance class
        internal_class: Internal thread tolerance class

    Returns:
        Quick compatibility assessment
    """
    oracle = deploy_oracle()

    # Standard ISO metric thread with given parameters
    external = {
        "diameter": diameter,
        "pitch": pitch,
        "class": external_class,
        "major_dia_min": diameter - 0.24,
        "major_dia_max": diameter - 0.03,
        "pitch_dia_min": diameter - pitch * 0.65,
        "pitch_dia_max": diameter - pitch * 0.54,
        "minor_dia_min": diameter - pitch * 1.35,
        "minor_dia_max": diameter - pitch * 1.09,
    }

    internal = {
        "diameter": diameter,
        "pitch": pitch,
        "class": internal_class,
        "major_dia_min": diameter,
        "major_dia_max": diameter + 0.3,
        "pitch_dia_min": diameter - pitch * 0.54,
        "pitch_dia_max": diameter - pitch * 0.44,
        "minor_dia_min": diameter - pitch * 1.09,
        "minor_dia_max": diameter - pitch * 0.92,
    }

    return oracle.check_thread_compatibility(external, internal)


def quick_galvanic_check(
    material_a: str,
    material_b: str,
    environment: str = "indoor"
) -> Dict[str, Any]:
    """
    Quick galvanic compatibility check.

    Args:
        material_a: First material
        material_b: Second material
        environment: Operating environment

    Returns:
        Galvanic risk assessment
    """
    oracle = deploy_oracle()
    return oracle.check_galvanic_risk(material_a, material_b, environment)


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ORACLE - The Compatibility Oracle (Agent_2)"
    )
    parser.add_argument(
        "--check-thread",
        nargs=2,
        metavar=("DIAMETER", "PITCH"),
        help="Check thread compatibility (e.g., --check-thread 8 1.25)"
    )
    parser.add_argument(
        "--check-galvanic",
        nargs=2,
        metavar=("MAT_A", "MAT_B"),
        help="Check galvanic risk (e.g., --check-galvanic steel aluminum)"
    )
    parser.add_argument(
        "--environment",
        default="indoor",
        choices=["indoor", "outdoor", "marine", "chemical"],
        help="Operating environment for galvanic check"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show ORACLE status"
    )

    args = parser.parse_args()

    oracle = deploy_oracle()

    if args.status:
        status = oracle.get_status()
        print(json.dumps(status, indent=2))

    elif args.check_thread:
        diameter, pitch = map(float, args.check_thread)
        result = quick_thread_check(diameter, pitch)
        print(f"\nThread Check: M{diameter}x{pitch}")
        print("-" * 40)
        print(f"Compatible: {result['is_compatible']}")
        print(f"Engagement Quality: {result['engagement_quality']}")
        print(f"Clearance: {result['clearance_min_mm']:.4f} - {result['clearance_max_mm']:.4f} mm")
        if result['warnings']:
            print(f"Warnings: {', '.join(result['warnings'])}")

    elif args.check_galvanic:
        mat_a, mat_b = args.check_galvanic
        result = quick_galvanic_check(mat_a, mat_b, args.environment)
        print(f"\nGalvanic Check: {mat_a} + {mat_b} ({args.environment})")
        print("-" * 40)
        print(f"Risk Level: {result['risk_level']}")
        print(f"Description: {result['description']}")
        print(f"Recommendation: {result['recommendation']}")

    else:
        # Demo mode
        print("\n" + "=" * 60)
        print(" ORACLE - Compatibility Oracle (Agent_2) DEPLOYED")
        print("=" * 60)
        print("\n\"Will it fit? Will it hold? Will it fail?")
        print("These questions haunt every engineer. I am the answer.\"\n")

        print("Status:", oracle.get_status()["status"])
        print("Capabilities:")
        for cap in oracle.get_status()["capabilities"]:
            print(f"  - {cap}")

        print("\nExample checks:")
        print("-" * 40)

        # Thread example
        result = quick_thread_check(8, 1.25)
        print(f"\nM8x1.25 Thread: {result['engagement_quality']} ({result['is_compatible']})")

        # Galvanic example
        result = quick_galvanic_check("steel", "aluminum")
        print(f"Steel + Aluminum: {result['risk_level']} risk")

        result = quick_galvanic_check("stainless_304", "stainless_316")
        print(f"304SS + 316SS: {result['risk_level']} risk")

        print("\n" + "=" * 60)
        print(" ORACLE IS LISTENING")
        print("=" * 60)
