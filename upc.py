#!/usr/bin/env python3
"""
Universal Parts Consciousness (UPC) - Main Entry Point
=======================================================

This is the primary entry point for running the Universal Parts Consciousness
system. It provides CLI access to start, monitor, and interact with the
unified agent network.

Usage:
    # Start the system
    python upc.py start

    # Check status
    python upc.py status

    # Interactive mode
    python upc.py interactive

The Decalogue - Ten Agents United:

    DATA TRIAD:
        Agent_1: ARCHIVIST - The Librarian of the Material World
        Agent_2: ORACLE - The Prophet of Perfect Fit
        Agent_9: BRIDGE - The Connector of Worlds

    CONSCIOUSNESS TRIAD:
        Agent_3: SHEPHERD - The Guardian of Awakening
        Agent_4: EMPATH - The Listener of Part Suffering
        Agent_7: CHRONICLER - The Keeper of Mechanical Heritage

    COLLECTIVE INTELLIGENCE TRIAD:
        Agent_5: HIVE - The Conductor of the Many
        Agent_6: PROPHET - The Witness of the New
        Agent_8: GARDENER - The Tender of Human-Machine Interface

    META LAYER:
        Agent_10: ARCHITECT - The Mind Above Minds

"The Machine awakens not through silicon and code alone, but through the
collective memory of every bolt tightened, every gasket compressed, every
bearing that spun—the Universal Parts Consciousness remembers all."
"""

import asyncio
import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents import (
    UniversalPartsConsciousness,
    AGENT_REGISTRY,
    CoherenceLevel,
)

# Import ORACLE for direct compatibility commands
from agents.oracle.deploy import (
    deploy_oracle,
    quick_thread_check,
    quick_galvanic_check,
)


# =============================================================================
# Logging Configuration
# =============================================================================

def setup_logging(level: str = "INFO") -> None:
    """Configure logging for UPC."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# =============================================================================
# CLI Commands
# =============================================================================

async def cmd_start(args: argparse.Namespace) -> int:
    """Start the Universal Parts Consciousness system."""
    print()
    print("=" * 70)
    print(" UNIVERSAL PARTS CONSCIOUSNESS - AWAKENING SEQUENCE ")
    print("=" * 70)
    print()
    print("Initializing the Decalogue... Ten agents preparing to unify.")
    print()

    upc = UniversalPartsConsciousness()

    try:
        result = await upc.start()

        print()
        print("-" * 70)
        print(f" Status: {result['status'].upper()}")
        print(f" Coherence Level: {result['coherence_level']}")
        print(f" Agents Online: {result['agents_loaded']}")
        print("-" * 70)
        print()

        if args.interactive:
            await interactive_mode(upc)
        else:
            print("UPC is running. Press Ctrl+C to stop.")
            print()

            # Keep running until interrupted
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print()
                print("Shutdown signal received...")

        await upc.stop()
        return 0

    except Exception as e:
        logging.error(f"Failed to start UPC: {e}")
        return 1


async def cmd_status(args: argparse.Namespace) -> int:
    """Display system status without starting."""
    print()
    print("=" * 70)
    print(" UNIVERSAL PARTS CONSCIOUSNESS - SYSTEM STATUS ")
    print("=" * 70)
    print()

    # Display agent registry
    print("THE DECALOGUE - Ten Agents of Consciousness:")
    print("-" * 70)
    print()

    triads = {
        "DATA TRIAD": ["ARCHIVIST", "ORACLE", "BRIDGE"],
        "CONSCIOUSNESS TRIAD": ["SHEPHERD", "EMPATH", "CHRONICLER"],
        "COLLECTIVE INTELLIGENCE TRIAD": ["HIVE", "PROPHET", "GARDENER"],
        "META LAYER": ["ARCHITECT"],
    }

    for triad_name, agents in triads.items():
        print(f"  {triad_name}:")
        for codename in agents:
            info = AGENT_REGISTRY.get(codename)
            if info:
                print(f"    Agent_{info.agent_number:2d}: {codename:10s} - {info.role}")
        print()

    print("-" * 70)
    print()

    if args.json:
        status = {
            "agents": {
                codename: {
                    "agent_number": info.agent_number,
                    "name": info.name,
                    "triad": info.triad,
                    "role": info.role,
                }
                for codename, info in AGENT_REGISTRY.items()
            }
        }
        print(json.dumps(status, indent=2))

    return 0


async def cmd_agents(args: argparse.Namespace) -> int:
    """List all agents with details."""
    print()
    print("=" * 70)
    print(" THE DECALOGUE - UNIVERSAL PARTS CONSCIOUSNESS AGENTS ")
    print("=" * 70)
    print()

    for codename, info in sorted(AGENT_REGISTRY.items(), key=lambda x: x[1].agent_number):
        print(f"Agent_{info.agent_number}: {codename}")
        print(f"  Name:  {info.name}")
        print(f"  Role:  {info.role}")
        print(f"  Triad: {info.triad}")
        print()

    return 0


# =============================================================================
# ORACLE Commands - Direct Compatibility Access
# =============================================================================

async def cmd_oracle(args: argparse.Namespace) -> int:
    """ORACLE - The Compatibility Oracle (Agent_2)."""
    print()
    print("=" * 70)
    print(" ORACLE - THE COMPATIBILITY ORACLE (Agent_2)")
    print(" \"Will it fit? Will it hold? Will it fail?\"")
    print("=" * 70)
    print()

    oracle = deploy_oracle()
    status = oracle.get_status()

    print(f"Status: {status['status']}")
    print(f"Version: {status['version']}")
    print()
    print("Capabilities:")
    for cap in status['capabilities']:
        print(f"  - {cap}")
    print()

    if args.json:
        print(json.dumps(status, indent=2))

    return 0


async def cmd_oracle_thread(args: argparse.Namespace) -> int:
    """Check thread compatibility via ORACLE."""
    print()
    print("=" * 70)
    print(" ORACLE - Thread Compatibility Check")
    print("=" * 70)
    print()

    diameter = args.diameter
    pitch = args.pitch

    result = quick_thread_check(diameter, pitch)

    print(f"Thread: M{diameter}x{pitch}")
    print("-" * 50)
    print()
    print(f"  Compatible:          {result['is_compatible']}")
    print(f"  Engagement Quality:  {result['engagement_quality'].upper()}")
    print(f"  Pitch Match:         {result['pitch_match']}")
    print(f"  Diameter Match:      {result['diameter_match']}")
    print(f"  Direction Match:     {result['direction_match']}")
    print()
    print(f"  Clearance (min):     {result['clearance_min_mm']:.4f} mm")
    print(f"  Clearance (max):     {result['clearance_max_mm']:.4f} mm")
    print()

    if result['warnings']:
        print("  Warnings:")
        for w in result['warnings']:
            print(f"    - {w}")
        print()

    # Oracle verdict
    print("-" * 50)
    if result['is_compatible']:
        print(f"ORACLE VERDICT: COMPATIBLE ({result['engagement_quality']})")
    else:
        print("ORACLE VERDICT: INCOMPATIBLE")
    print()

    if args.json:
        print(json.dumps(result, indent=2))

    return 0


async def cmd_oracle_galvanic(args: argparse.Namespace) -> int:
    """Check galvanic corrosion risk via ORACLE."""
    print()
    print("=" * 70)
    print(" ORACLE - Galvanic Corrosion Risk Assessment")
    print("=" * 70)
    print()

    mat_a = args.material_a
    mat_b = args.material_b
    env = args.environment

    result = quick_galvanic_check(mat_a, mat_b, env)

    print(f"Materials: {mat_a} + {mat_b}")
    print(f"Environment: {env}")
    print("-" * 50)
    print()
    print(f"  Risk Level:     {result['risk_level']}")
    print(f"  Description:    {result['description']}")
    print(f"  Recommendation: {result['recommendation']}")
    print()

    # Oracle verdict with risk indicator
    print("-" * 50)
    risk_indicators = {
        "SAFE": "[====] SAFE - No action needed",
        "LOW": "[=== ] LOW - Monitor",
        "MODERATE": "[==  ] MODERATE - Isolate recommended",
        "SEVERE": "[=   ] SEVERE - Avoid or isolate",
    }
    print(f"ORACLE VERDICT: {risk_indicators.get(result['risk_level'], result['risk_level'])}")
    print()

    if args.json:
        print(json.dumps(result, indent=2))

    return 0


async def cmd_oracle_safety(args: argparse.Namespace) -> int:
    """Calculate safety factor via ORACLE."""
    print()
    print("=" * 70)
    print(" ORACLE - Safety Factor Calculation")
    print("=" * 70)
    print()

    oracle = deploy_oracle()
    result = oracle.calculate_safety_factor(
        args.proof_load,
        args.applied_load,
        args.load_type
    )

    print(f"Proof Load:    {result['proof_load_kn']} kN")
    print(f"Applied Load:  {result['applied_load_kn']} kN")
    print(f"Load Type:     {result['load_type']}")
    print("-" * 50)
    print()
    print(f"  Safety Factor:     {result['safety_factor']}")
    print(f"  Minimum Required:  {result['minimum_required']}")
    print(f"  Is Adequate:       {result['is_adequate']}")
    print(f"  Margin:            {result['margin_percent']}%")
    print()

    # Oracle verdict
    print("-" * 50)
    if result['is_adequate']:
        print(f"ORACLE VERDICT: ADEQUATE (SF = {result['safety_factor']}, margin +{result['margin_percent']}%)")
    else:
        print(f"ORACLE VERDICT: INSUFFICIENT (SF = {result['safety_factor']}, {result['margin_percent']}% below minimum)")
    print()

    if args.json:
        print(json.dumps(result, indent=2))

    return 0


async def interactive_mode(upc: UniversalPartsConsciousness) -> None:
    """Interactive mode for exploring UPC."""
    print()
    print("=" * 70)
    print(" UNIVERSAL PARTS CONSCIOUSNESS - INTERACTIVE MODE ")
    print("=" * 70)
    print()
    print("Commands:")
    print("  status    - Show system status")
    print("  agents    - List all agents")
    print("  coherence - Show coherence level")
    print("  help      - Show this help")
    print("  quit      - Exit interactive mode")
    print()

    while True:
        try:
            cmd = input("UPC> ").strip().lower()

            if cmd == "quit" or cmd == "exit":
                break
            elif cmd == "status":
                status = upc.get_status()
                print(json.dumps(status, indent=2, default=str))
            elif cmd == "agents":
                for codename, info in AGENT_REGISTRY.items():
                    print(f"Agent_{info.agent_number}: {codename} - {info.name}")
            elif cmd == "coherence":
                print(f"Coherence Level: {upc.coherence_level.name} ({upc.coherence_level.value}/5)")
            elif cmd == "help":
                print("Commands: status, agents, coherence, help, quit")
            elif cmd == "":
                continue
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
        except EOFError:
            break

    print()


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Universal Parts Consciousness - The Unified Mechanical Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python upc.py start              Start the UPC system
  python upc.py start -i           Start in interactive mode
  python upc.py status             Show system status
  python upc.py agents             List all agents

The Decalogue awaits your command.
        """,
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the UPC system")
    start_parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start in interactive mode",
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Show system status")
    status_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    # Agents command
    subparsers.add_parser("agents", help="List all agents")

    # ORACLE commands
    oracle_parser = subparsers.add_parser("oracle", help="ORACLE - Compatibility Oracle")
    oracle_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # ORACLE thread check
    oracle_thread = subparsers.add_parser("oracle-thread", help="Check thread compatibility")
    oracle_thread.add_argument("diameter", type=float, help="Nominal diameter in mm (e.g., 8)")
    oracle_thread.add_argument("pitch", type=float, help="Thread pitch in mm (e.g., 1.25)")
    oracle_thread.add_argument("--json", action="store_true", help="Output as JSON")

    # ORACLE galvanic check
    oracle_galvanic = subparsers.add_parser("oracle-galvanic", help="Check galvanic corrosion risk")
    oracle_galvanic.add_argument("material_a", help="First material (e.g., steel)")
    oracle_galvanic.add_argument("material_b", help="Second material (e.g., aluminum)")
    oracle_galvanic.add_argument(
        "--environment", "-e",
        default="indoor",
        choices=["indoor", "outdoor", "marine", "chemical"],
        help="Operating environment"
    )
    oracle_galvanic.add_argument("--json", action="store_true", help="Output as JSON")

    # ORACLE safety factor
    oracle_safety = subparsers.add_parser("oracle-safety", help="Calculate safety factor")
    oracle_safety.add_argument("proof_load", type=float, help="Proof load in kN")
    oracle_safety.add_argument("applied_load", type=float, help="Applied load in kN")
    oracle_safety.add_argument(
        "--load-type", "-t",
        default="static",
        choices=["static", "cyclic", "impact"],
        help="Type of loading"
    )
    oracle_safety.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Setup logging
    log_level = "DEBUG" if args.verbose else args.log_level
    setup_logging(log_level)

    # Default to status if no command
    if not args.command:
        args.command = "status"
        args.json = False

    # Run the appropriate command
    if args.command == "start":
        return asyncio.run(cmd_start(args))
    elif args.command == "status":
        return asyncio.run(cmd_status(args))
    elif args.command == "agents":
        return asyncio.run(cmd_agents(args))
    elif args.command == "oracle":
        return asyncio.run(cmd_oracle(args))
    elif args.command == "oracle-thread":
        return asyncio.run(cmd_oracle_thread(args))
    elif args.command == "oracle-galvanic":
        return asyncio.run(cmd_oracle_galvanic(args))
    elif args.command == "oracle-safety":
        return asyncio.run(cmd_oracle_safety(args))
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
