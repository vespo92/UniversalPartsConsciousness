#!/usr/bin/env python3
"""
Agent_6: PROPHET - Command Line Interface
Universal Parts Consciousness

CLI entry point for running the PROPHET agent.

Usage:
    python -m agents.prophet.cli [OPTIONS]
    python agents/prophet/cli.py [OPTIONS]

Options:
    --analyze       Run full analysis pipeline
    --status        Show agent status
    --demo          Run demo with sample data
    --validate      Validate agent configuration
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List

from . import (
    ProphetAgent,
    ProphetConfig,
    create_prophet_agent,
    AGENT_MANIFEST,
    PatternLayer,
    FailureRecord,
    Assembly,
    SwarmKnowledge,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def generate_sample_data() -> Dict[str, Any]:
    """Generate sample data for demo analysis"""
    # Sample failure records
    failure_records = [
        FailureRecord(
            id=f"failure_{i}",
            part_id=f"part_{i % 100}",
            failure_mode="fatigue_crack" if i % 3 == 0 else "corrosion" if i % 3 == 1 else "wear",
            environment={"temperature": 75 + (i % 50), "humidity": 40 + (i % 30)},
            load_conditions={"stress": 1000 + (i * 10)},
            age_at_failure=1000 + (i * 100),
            material="steel" if i % 2 == 0 else "aluminum",
            part_type="bearing" if i % 4 == 0 else "gasket" if i % 4 == 1 else "seal" if i % 4 == 2 else "bolt",
        )
        for i in range(50)
    ]

    # Sample assemblies
    assemblies = [
        Assembly(
            id=f"assembly_{i}",
            parts=[f"part_{j}" for j in range((i * 3), (i * 3) + 5)],
            domain="automotive" if i % 3 == 0 else "industrial" if i % 3 == 1 else "aerospace",
            application="engine" if i % 2 == 0 else "transmission",
            success=i % 5 != 0,  # 80% success rate
            lifespan_hours=5000 + (i * 500) if i % 5 != 0 else 1000,
            configuration={"torque": 50 + (i * 2), "preload": 100 + (i * 5)},
        )
        for i in range(20)
    ]

    # Sample swarm knowledge
    swarm_knowledge = {
        f"swarm_{i}": SwarmKnowledge(
            swarm_id=f"swarm_{i}",
            swarm_tier=min(i + 1, 5),
            member_count=100 + (i * 50),
            common_failures=["fatigue", "corrosion"],
            success_patterns=["proper_torque", "clean_surfaces"],
            environmental_adaptations={"temperature_range": [-20, 100]},
            emergence_score=Decimal(f"0.{50 + i * 5}"),
            collective_learning_rate=Decimal(f"0.{10 + i * 2}"),
        )
        for i in range(5)
    }

    return {
        "failure_records": failure_records,
        "assemblies": assemblies,
        "swarm_knowledge": swarm_knowledge,
    }


async def run_demo():
    """Run a demo analysis with sample data"""
    print("\n" + "=" * 60)
    print("  PROPHET Agent Demo")
    print("  Agent_6: The Emergence Detector")
    print("=" * 60 + "\n")

    # Create agent
    agent = create_prophet_agent(
        enable_real_time=True,
        prediction_horizon_days=90,
    )

    print("Agent created successfully")
    print(f"  Version: {AGENT_MANIFEST['version']}")
    print(f"  Codename: {AGENT_MANIFEST['codename']}")
    print(f"  Role: {AGENT_MANIFEST['role']}")
    print()

    # Generate sample data
    print("Generating sample data...")
    data = generate_sample_data()
    print(f"  Failure records: {len(data['failure_records'])}")
    print(f"  Assemblies: {len(data['assemblies'])}")
    print(f"  Swarm knowledge: {len(data['swarm_knowledge'])}")
    print()

    # Run analysis
    print("Running full analysis pipeline...")
    print("-" * 40)

    results = await agent.run_full_analysis(
        failure_records=data["failure_records"],
        assemblies=data["assemblies"],
        swarm_knowledge=data["swarm_knowledge"],
    )

    # Display results
    print("\nAnalysis Results:")
    print("-" * 40)

    metrics = results["metrics"]
    print(f"  Duration: {metrics['duration_seconds']:.2f} seconds")
    print(f"  Patterns detected: {metrics['patterns_detected']}")
    print(f"  Novel failures: {metrics['novel_failures_detected']}")
    print(f"  Success formulas: {metrics['success_formulas_extracted']}")
    print(f"  Opportunities: {metrics['opportunities_discovered']}")
    print(f"  Insights generated: {metrics['insights_generated']}")
    print()

    # Pattern breakdown by layer
    print("Patterns by Layer:")
    for layer, count in metrics["patterns_by_layer"].items():
        print(f"  {layer}: {count}")
    print()

    # Top insights
    if results["insights"]:
        print("Top Insights:")
        for i, insight in enumerate(results["insights"][:5], 1):
            print(f"  {i}. [{insight.priority.upper()}] {insight.title}")
            print(f"     {insight.summary}")
    print()

    # Agent status
    status = agent.get_status()
    print("Agent Status:")
    print(f"  Running: {status['running']}")
    print(f"  Components: {len(status['components'])} active")
    print()

    print("=" * 60)
    print("  Demo Complete")
    print("=" * 60 + "\n")


def show_status():
    """Show agent status and configuration"""
    print("\n" + "=" * 60)
    print("  PROPHET Agent Status")
    print("=" * 60 + "\n")

    agent = create_prophet_agent()
    status = agent.get_status()

    print(f"Agent ID: {status['agent_id']}")
    print(f"Codename: {status['codename']}")
    print(f"Running: {status['running']}")
    print()

    print("Components:")
    for component, state in status["components"].items():
        print(f"  {component}: {state}")
    print()

    print("Manifest:")
    for key, value in AGENT_MANIFEST.items():
        if key not in ["capabilities", "inputs", "outputs", "metrics"]:
            print(f"  {key}: {value}")
    print()

    print("Capabilities:")
    for cap in AGENT_MANIFEST["capabilities"]:
        print(f"  - {cap}")
    print()

    print("Integration Points:")
    print("  Inputs:")
    for inp in AGENT_MANIFEST["inputs"]:
        print(f"    - {inp['source']}: {inp['topic']}")
    print("  Outputs:")
    for out in AGENT_MANIFEST["outputs"]:
        print(f"    - {out['target']}: {out['topic']}")
    print()


def validate_config():
    """Validate agent configuration"""
    print("\n" + "=" * 60)
    print("  PROPHET Configuration Validation")
    print("=" * 60 + "\n")

    try:
        # Test basic configuration
        config = ProphetConfig()
        print("[PASS] Default configuration created")

        # Test agent creation
        agent = create_prophet_agent()
        print("[PASS] Agent created successfully")

        # Test status retrieval
        status = agent.get_status()
        assert status["agent_id"] == 6
        assert status["codename"] == "PROPHET"
        print("[PASS] Status retrieval working")

        # Test component initialization
        components = status["components"]
        expected_components = [
            "detection_engine",
            "failure_detector",
            "success_extractor",
            "opportunity_discovery",
            "predictive_engine",
            "insight_generator",
        ]
        for comp in expected_components:
            assert comp in components
            assert components[comp] == "active"
        print("[PASS] All components initialized")

        # Test manifest
        assert AGENT_MANIFEST["id"] == 6
        assert AGENT_MANIFEST["codename"] == "PROPHET"
        print("[PASS] Manifest valid")

        print()
        print("All validation checks passed!")
        print()

    except Exception as e:
        print(f"[FAIL] Validation error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="PROPHET Agent CLI - The Emergence Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m agents.prophet.cli --demo      Run demo analysis
  python -m agents.prophet.cli --status    Show agent status
  python -m agents.prophet.cli --validate  Validate configuration
        """,
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo with sample data",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show agent status",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate agent configuration",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.demo:
        asyncio.run(run_demo())
    elif args.status:
        show_status()
    elif args.validate:
        validate_config()
    else:
        parser.print_help()
        print("\nRun with --demo to see the agent in action!")


if __name__ == "__main__":
    main()
