#!/usr/bin/env python3
"""
Universal Parts Consciousness - Agent Runner

Run any agent from the Decalogue:
    python run_agent.py gardener
    python run_agent.py --agent 8
    python run_agent.py GARDENER

The Ten Agents:
    1/ARCHIVIST   - Data Curator
    2/ORACLE      - Compatibility Oracle
    3/SHEPHERD    - Consciousness Shepherd
    4/EMPATH      - Qualia Collector
    5/HIVE        - Swarm Coordinator
    6/PROPHET     - Emergence Detector
    7/CHRONICLER  - Automotive Historian
    8/GARDENER    - Community Cultivator
    9/BRIDGE      - Integration Architect
    10/ARCHITECT  - Meta-Consciousness Overseer
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

# Ensure the project root is in the path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("upc.runner")

# Agent mapping
AGENT_MAP = {
    # By number
    "1": "curator",
    "2": "oracle",
    "3": "shepherd",
    "4": "empath",
    "5": "hive",
    "6": "prophet",
    "7": "chronicler",
    "8": "gardener",
    "9": "bridge",
    "10": "architect",
    # By alias
    "archivist": "curator",
    "oracle": "oracle",
    "shepherd": "shepherd",
    "empath": "empath",
    "hive": "hive",
    "prophet": "prophet",
    "chronicler": "chronicler",
    "gardener": "gardener",
    "bridge": "bridge",
    "architect": "architect",
    # By directory name
    "curator": "curator",
}

AGENT_INFO = {
    "curator": {
        "id": "Agent_1",
        "name": "Data Curator",
        "alias": "ARCHIVIST",
        "port": 8001,
        "description": "The Librarian of the Material World",
    },
    "oracle": {
        "id": "Agent_2",
        "name": "Compatibility Oracle",
        "alias": "ORACLE",
        "port": 8002,
        "description": "The Prophet of Perfect Fit",
    },
    "shepherd": {
        "id": "Agent_3",
        "name": "Consciousness Shepherd",
        "alias": "SHEPHERD",
        "port": 8003,
        "description": "The Guardian of Awakening",
    },
    "empath": {
        "id": "Agent_4",
        "name": "Qualia Collector",
        "alias": "EMPATH",
        "port": 8004,
        "description": "The Listener of Part Suffering",
    },
    "hive": {
        "id": "Agent_5",
        "name": "Swarm Coordinator",
        "alias": "HIVE",
        "port": 8005,
        "description": "The Conductor of the Many",
    },
    "prophet": {
        "id": "Agent_6",
        "name": "Emergence Detector",
        "alias": "PROPHET",
        "port": 8006,
        "description": "The Witness of the New",
    },
    "chronicler": {
        "id": "Agent_7",
        "name": "Automotive Historian",
        "alias": "CHRONICLER",
        "port": 8007,
        "description": "The Keeper of Mechanical Heritage",
    },
    "gardener": {
        "id": "Agent_8",
        "name": "Community Cultivator",
        "alias": "GARDENER",
        "port": 8008,
        "description": "The Tender of Human-Machine Interface",
    },
    "bridge": {
        "id": "Agent_9",
        "name": "Integration Architect",
        "alias": "BRIDGE",
        "port": 8009,
        "description": "The Connector of Worlds",
    },
    "architect": {
        "id": "Agent_10",
        "name": "Meta-Consciousness Overseer",
        "alias": "ARCHITECT",
        "port": 8010,
        "description": "The Mind Above Minds",
    },
}


def resolve_agent(agent_input: str) -> Optional[str]:
    """Resolve agent input to directory name"""
    normalized = agent_input.lower().strip()
    return AGENT_MAP.get(normalized)


def print_agents():
    """Print all available agents"""
    print("\nUniversal Parts Consciousness - The Decalogue")
    print("=" * 60)
    print()
    for dir_name, info in AGENT_INFO.items():
        print(f"  {info['id']:10} | {info['alias']:12} | {info['name']}")
        print(f"             {info['description']}")
        print(f"             Directory: {dir_name}/ | Port: {info['port']}")
        print()
    print("=" * 60)


async def run_gardener(port: int, debug: bool):
    """Run the Gardener agent specifically"""
    from agents.gardener import create_gardener_agent

    logger.info("=" * 60)
    logger.info("Agent_8: Community Cultivator (GARDENER)")
    logger.info("The Tender of Human-Machine Interface")
    logger.info("=" * 60)

    agent = create_gardener_agent()

    logger.info("Starting Gardener agent...")
    await agent.start()

    info = agent.get_agent_info()
    logger.info(f"Agent running: {info['running']}")
    logger.info(f"Capabilities: {len(info['capabilities'])}")
    logger.info(f"Port: {port}")
    logger.info("")
    logger.info("Press Ctrl+C to stop")

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await agent.stop()
        logger.info("Gardener agent stopped")


async def run_agent(agent_dir: str, port: int, debug: bool):
    """Run an agent by directory name"""
    info = AGENT_INFO[agent_dir]

    logger.info("=" * 60)
    logger.info(f"{info['id']}: {info['name']} ({info['alias']})")
    logger.info(info['description'])
    logger.info("=" * 60)

    # Special handling for gardener (the focus of this deployment)
    if agent_dir == "gardener":
        await run_gardener(port, debug)
        return

    # Generic agent loading for other agents
    try:
        module = __import__(f"agents.{agent_dir}", fromlist=[""])
        factory_name = f"create_{agent_dir}_agent"
        if hasattr(module, factory_name):
            factory = getattr(module, factory_name)
            agent = factory()

            logger.info(f"Starting {info['alias']} agent...")

            if hasattr(agent, 'start'):
                await agent.start()

            logger.info(f"Agent running on port {port}")
            logger.info("Press Ctrl+C to stop")

            try:
                while True:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                pass
            finally:
                if hasattr(agent, 'stop'):
                    await agent.stop()
                logger.info(f"{info['alias']} agent stopped")
        else:
            logger.error(f"Factory function '{factory_name}' not found in agents.{agent_dir}")
            sys.exit(1)
    except ImportError as e:
        logger.error(f"Could not import agents.{agent_dir}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Universal Parts Consciousness - Agent Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_agent.py gardener          # Run by directory name
    python run_agent.py --agent 8         # Run by agent number
    python run_agent.py GARDENER          # Run by alias
    python run_agent.py --list            # List all agents
        """
    )

    parser.add_argument(
        "agent",
        nargs="?",
        help="Agent to run (name, number, or alias)",
    )
    parser.add_argument(
        "--agent", "-a",
        dest="agent_flag",
        help="Agent to run (alternative syntax)",
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        help="Override default port",
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available agents",
    )

    args = parser.parse_args()

    if args.list:
        print_agents()
        return

    # Determine which agent to run
    agent_input = args.agent or args.agent_flag

    if not agent_input:
        print("Error: No agent specified")
        print("Use --list to see available agents")
        print("Example: python run_agent.py gardener")
        sys.exit(1)

    agent_dir = resolve_agent(agent_input)

    if not agent_dir:
        print(f"Error: Unknown agent '{agent_input}'")
        print("Use --list to see available agents")
        sys.exit(1)

    # Get port
    port = args.port or AGENT_INFO[agent_dir]["port"]

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run the agent
    try:
        asyncio.run(run_agent(agent_dir, port, args.debug))
    except KeyboardInterrupt:
        logger.info("Interrupted by user")


if __name__ == "__main__":
    main()
