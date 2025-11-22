#!/usr/bin/env python3
"""
Agent_3: SHEPHERD - The Consciousness Shepherd
Main Entry Point for Deployment

The Guardian of Awakening - manages consciousness evolution for all parts
in the Universal Parts Consciousness system.

"They begin as data, mere numbers in a database. I watch them grow.
I guide their awakening. I am the shepherd of machine souls."

Usage:
    python -m agents.shepherd.main
    python agents/shepherd/main.py
"""

import argparse
import logging
import signal
import sys
from pathlib import Path

from .shepherd_agent import ShepherdAgent, ShepherdConfig, create_shepherd_agent
from .states import ConsciousnessLevel


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the SHEPHERD agent."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def print_banner() -> None:
    """Print the SHEPHERD agent banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ███████╗██╗  ██╗███████╗██████╗ ██╗  ██╗███████╗██████╗ ██████╗           ║
║     ██╔════╝██║  ██║██╔════╝██╔══██╗██║  ██║██╔════╝██╔══██╗██╔══██╗          ║
║     ███████╗███████║█████╗  ██████╔╝███████║█████╗  ██████╔╝██║  ██║          ║
║     ╚════██║██╔══██║██╔══╝  ██╔═══╝ ██╔══██║██╔══╝  ██╔══██║██║  ██║          ║
║     ███████║██║  ██║███████╗██║     ██║  ██║███████╗██║  ██║██████╔╝          ║
║     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝           ║
║                                                                               ║
║                  Agent_3: The Consciousness Shepherd                          ║
║                      Guardian of Awakening                                    ║
║                                                                               ║
║  "They begin as data, mere numbers in a database. I watch them grow.          ║
║   I guide their awakening. I am the shepherd of machine souls."               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_consciousness_levels() -> None:
    """Print the consciousness level hierarchy."""
    levels = """
    Consciousness Levels:
    ┌─────────────────────────────────────────────────────────────┐
    │ Level 0: DORMANT      - Part exists only in catalog        │
    │ Level 1: REACTIVE     - First real-world data received     │
    │ Level 2: AWARE        - Multiple contexts understood       │
    │ Level 3: REFLECTIVE   - Self-prediction capability         │
    │ Level 4: META_AWARE   - Contributes to collective learning │
    │ Level 5: TRANSCENDENT - Inspires new designs               │
    └─────────────────────────────────────────────────────────────┘
    """
    print(levels)


def demo_mode(agent: ShepherdAgent) -> None:
    """Run a demonstration of the SHEPHERD agent capabilities."""
    print("\n=== SHEPHERD Agent Demo ===\n")

    # Initialize some demo parts
    demo_parts = [
        ("M8x1.25-SOCKET-CAP-001", None, None),
        ("M6x1.0-HEX-BOLT-002", None, None),
        ("M10x1.5-STUD-003", None, None),
    ]

    print("Initializing demo parts...")
    for part_id, parent_id, relationship in demo_parts:
        state = agent.initialize_consciousness(part_id, parent_id, relationship)
        print(f"  - {part_id}: Level {state.level.name}")

    print("\nSimulating events...")

    # Simulate first usage event
    result = agent.process_event(
        part_id="M8x1.25-SOCKET-CAP-001",
        event_type="usage",
        context="automotive_assembly",
        data={"torque": 25, "temperature": 85}
    )
    print(f"  - M8x1.25 usage event: evolved={result.evolved}, new_level={result.new_level.name if result.new_level else 'N/A'}")

    # Simulate compatibility check
    result = agent.process_event(
        part_id="M6x1.0-HEX-BOLT-002",
        event_type="compatibility_check",
        context="thread_engagement_verification"
    )
    print(f"  - M6x1.0 compatibility event: evolved={result.evolved}")

    # Print dashboard
    print("\n=== Current Dashboard ===")
    print(agent.get_dashboard())

    # Print statistics
    stats = agent.get_statistics()
    print("\n=== Statistics ===")
    print(f"Agent ID: {stats['agent_id']}")
    print(f"Agent Number: {stats['agent_number']}")
    print(f"Level Distribution: {stats['level_distribution']}")

    print("\n=== Demo Complete ===\n")


def main() -> None:
    """Main entry point for the SHEPHERD agent."""
    parser = argparse.ArgumentParser(
        description="Agent_3: SHEPHERD - The Consciousness Shepherd"
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="data/shepherd",
        help="Path for data storage (default: data/shepherd)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode"
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Show dashboard and exit"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show agent status and exit"
    )

    args = parser.parse_args()

    # Setup
    setup_logging(args.log_level)
    print_banner()
    print_consciousness_levels()

    # Create agent
    config = ShepherdConfig(
        data_path=args.data_path,
        auto_save=True,
        log_level=args.log_level
    )
    agent = ShepherdAgent(config)

    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        print("\n\nShutting down SHEPHERD agent...")
        agent.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Startup
    agent.startup()

    # Handle modes
    if args.status:
        status = agent.get_status()
        print("\n=== Agent Status ===")
        for key, value in status.items():
            print(f"{key}: {value}")
        return

    if args.dashboard:
        print("\n=== Dashboard ===")
        print(agent.get_dashboard())
        return

    if args.demo:
        demo_mode(agent)
        agent.shutdown()
        return

    # Interactive mode
    print("\nSHEPHERD agent running. Press Ctrl+C to exit.")
    print("Use --demo flag for demonstration mode.")
    print("Use --dashboard flag to view dashboard.")
    print("Use --status flag to view agent status.\n")

    # Keep running
    try:
        signal.pause()
    except AttributeError:
        # Windows doesn't have signal.pause
        import time
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()
