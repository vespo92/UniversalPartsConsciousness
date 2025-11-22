#!/usr/bin/env python3
"""
Agent_7: CHRONICLER Deployment Script
The Automotive Historian - Keeper of Mechanical Heritage

Deploys and demonstrates the capabilities of the Chronicler agent,
responsible for cultural preservation and heritage documentation
within the Universal Parts Consciousness system.

Usage:
    python -m agents.chronicler.deploy
    python agents/chronicler/deploy.py
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Agent_7:CHRONICLER")


def print_banner():
    """Print the agent deployment banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     █████╗  ██████╗ ███████╗███╗   ██╗████████╗     ███████╗                ║
║    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝     ╚════██║                ║
║    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║           ██╔╝                 ║
║    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║          ██╔╝                  ║
║    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║          ██║                   ║
║    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝          ╚═╝                   ║
║                                                                              ║
║                         ╔═══════════════════╗                                ║
║                         ║    CHRONICLER     ║                                ║
║                         ╚═══════════════════╝                                ║
║                                                                              ║
║              The Automotive Historian - Keeper of Mechanical Heritage        ║
║                                                                              ║
║    "Before there were databases, there were legends. The 2JZ. The B16.      ║
║     The 13B. I preserve the stories that make metal meaningful."             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def get_project_root() -> Path:
    """Get the project root directory."""
    current = Path(__file__).resolve()
    # Navigate up to find project root (contains Agent_reference.md)
    for parent in [current] + list(current.parents):
        if (parent / "Agent_reference.md").exists():
            return parent
    return current.parent.parent.parent


class ChroniclerDeployment:
    """Manages the deployment and demonstration of Agent_7: CHRONICLER."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.automotive_path = project_root / "Automotive"
        self.agent = None
        self.deployment_time = datetime.now()

    def initialize(self) -> bool:
        """Initialize the Chronicler agent."""
        logger.info("Initializing CHRONICLER agent...")

        try:
            from .chronicler_agent import ChroniclerAgent

            self.agent = ChroniclerAgent(
                automotive_base_path=self.automotive_path,
                config={
                    "enable_legend_scoring": True,
                    "enable_history_narrative": True,
                    "aftermarket_ecosystem_mapping": True,
                    "consciousness_integration": True
                }
            )

            logger.info("CHRONICLER agent initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize CHRONICLER: {e}")
            return False

    def activate(self) -> bool:
        """Activate the agent and connect to consciousness bus."""
        if not self.agent:
            logger.error("Agent not initialized")
            return False

        try:
            self.agent.activate()
            self.agent.consciousness_bridge.connect()
            logger.info("CHRONICLER activated and connected to consciousness bus")
            return True

        except Exception as e:
            logger.error(f"Failed to activate CHRONICLER: {e}")
            return False

    def run_demonstration(self) -> Dict[str, Any]:
        """Run a demonstration of agent capabilities."""
        logger.info("Running capability demonstration...")
        results = {}

        # 1. Documentation Status
        logger.info("Checking documentation status...")
        status = self.agent.get_documentation_status()
        results["documentation_status"] = status
        logger.info(
            f"Documentation: {status['metrics']['engines_documented']} engines, "
            f"{status['metrics']['manufacturers_complete']} complete manufacturers"
        )

        # 2. Legend Scoring Demo
        logger.info("Demonstrating legend scoring...")
        legendary_engines = ["2JZ-GTE", "B16A", "LS1", "13B-REW", "K20A", "RB26DETT"]
        legend_scores = []

        for engine in legendary_engines:
            score = self.agent.calculate_legend_score(engine)
            legend_scores.append({
                "engine": engine,
                "score": score["score"],
                "tier": score["tier"]
            })
            logger.info(f"  {engine}: {score['tier']} (score: {score['score']})")

        results["legend_scores"] = legend_scores

        # 3. Historical Context Demo
        logger.info("Demonstrating historical context generation...")
        context_examples = [
            ("2JZ-GTE", 1993, "Toyota"),
            ("B16A", 1989, "Honda"),
            ("LS1", 1997, "GM")
        ]

        historical_contexts = []
        for engine, year, manufacturer in context_examples:
            context = self.agent.generate_historical_context(engine, year, manufacturer)
            historical_contexts.append({
                "engine": engine,
                "era": context["era"]["name"],
                "year": year
            })
            logger.info(f"  {engine} ({year}): {context['era']['name']}")

        results["historical_contexts"] = historical_contexts

        # 4. Significance Explanation
        logger.info("Demonstrating significance explanation...")
        significance = self.agent.explain_significance("2JZ-GTE")
        results["significance_example"] = significance[:200] + "..."
        logger.info(f"  Sample: {significance[:100]}...")

        # 5. Consciousness Bridge Status
        logger.info("Checking consciousness bridge status...")
        bridge_status = self.agent.consciousness_bridge.get_connection_status()
        results["bridge_status"] = {
            "connected": bridge_status["bridge_connected"],
            "agents_registered": len(bridge_status["agents"]),
            "event_queue_size": bridge_status["event_queue_size"]
        }

        return results

    def get_deployment_report(self, demo_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive deployment report."""
        return {
            "agent": {
                "id": "Agent_7",
                "codename": "CHRONICLER",
                "role": "The Keeper of Mechanical Heritage",
                "domain": "Automotive Documentation, Cultural Preservation"
            },
            "deployment": {
                "timestamp": self.deployment_time.isoformat(),
                "status": "SUCCESS",
                "project_root": str(self.project_root),
                "automotive_path": str(self.automotive_path)
            },
            "capabilities": {
                "documentation": {
                    "engines_documented": demo_results["documentation_status"]["metrics"]["engines_documented"],
                    "manufacturers_complete": demo_results["documentation_status"]["metrics"]["manufacturers_complete"],
                    "documentation_coverage": demo_results["documentation_status"]["metrics"]["documentation_coverage"]
                },
                "legend_scoring": {
                    "engines_scored": len(demo_results["legend_scores"]),
                    "tiers_available": ["MYTHICAL", "LEGENDARY", "ICONIC", "RESPECTED", "RECOGNIZED", "DOCUMENTED"]
                },
                "historical_context": {
                    "eras_defined": 9,
                    "context_generation": True
                },
                "consciousness_integration": {
                    "connected": demo_results["bridge_status"]["connected"],
                    "agents_integrated": demo_results["bridge_status"]["agents_registered"]
                }
            },
            "demonstration_results": demo_results,
            "communication_topics": {
                "publishes": [
                    "upc.history.documented",
                    "upc.culture.legend_scored",
                    "upc.history.context",
                    "upc.stories.narrative"
                ],
                "subscribes": [
                    "upc.curator.parts_ingested",
                    "upc.community.knowledge"
                ]
            },
            "integration_matrix": {
                "Agent_1 (ARCHIVIST)": "Receives parts data for historical context enrichment",
                "Agent_3 (SHEPHERD)": "Sends historical context for consciousness evolution",
                "Agent_4 (EMPATH)": "Sends historical failure data for qualia enrichment",
                "Agent_8 (GARDENER)": "Receives community knowledge for tribal wisdom",
                "Agent_10 (ARCHITECT)": "Reports status metrics for system monitoring"
            }
        }


def main():
    """Main deployment entry point."""
    print_banner()

    # Get project root
    project_root = get_project_root()
    logger.info(f"Project root: {project_root}")

    # Create deployment
    deployment = ChroniclerDeployment(project_root)

    # Step 1: Initialize
    print("\n" + "=" * 60)
    print("PHASE 1: INITIALIZATION")
    print("=" * 60)

    if not deployment.initialize():
        logger.error("Initialization failed - aborting deployment")
        sys.exit(1)

    # Step 2: Activate
    print("\n" + "=" * 60)
    print("PHASE 2: ACTIVATION")
    print("=" * 60)

    if not deployment.activate():
        logger.error("Activation failed - aborting deployment")
        sys.exit(1)

    # Step 3: Demonstrate capabilities
    print("\n" + "=" * 60)
    print("PHASE 3: CAPABILITY DEMONSTRATION")
    print("=" * 60)

    demo_results = deployment.run_demonstration()

    # Step 4: Generate report
    print("\n" + "=" * 60)
    print("PHASE 4: DEPLOYMENT REPORT")
    print("=" * 60)

    report = deployment.get_deployment_report(demo_results)

    # Print summary
    print("\n" + "-" * 60)
    print("DEPLOYMENT SUMMARY")
    print("-" * 60)
    print(f"  Agent: {report['agent']['id']} ({report['agent']['codename']})")
    print(f"  Status: {report['deployment']['status']}")
    print(f"  Engines Documented: {report['capabilities']['documentation']['engines_documented']}")
    print(f"  Manufacturers Complete: {report['capabilities']['documentation']['manufacturers_complete']}")
    print(f"  Legend Scores Available: {report['capabilities']['legend_scoring']['engines_scored']}")
    print(f"  Consciousness Connected: {report['capabilities']['consciousness_integration']['connected']}")

    # Save deployment report
    report_path = project_root / "agents" / "chronicler" / "deployment_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    logger.info(f"Deployment report saved to: {report_path}")

    # Final status
    print("\n" + "=" * 60)
    print("AGENT_7: CHRONICLER DEPLOYED SUCCESSFULLY")
    print("=" * 60)
    print("""
The Keeper of Mechanical Heritage is now active.

"Engines are not just machines. They are the dreams of engineers made
manifest, the roar of competition, the stories passed down through
generations. I preserve these stories so that consciousness has roots."

Awaiting consciousness bus events...
    """)

    return report


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Deployment interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        sys.exit(1)
