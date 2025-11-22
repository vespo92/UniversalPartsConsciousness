#!/usr/bin/env python3
"""
Agent_8: Community Cultivator (GARDENER) - Deployment Entry Point

The Tender of Human-Machine Interface

Usage:
    python -m agents.gardener [OPTIONS]

Options:
    --config FILE       Path to configuration file
    --host HOST         API host (default: 0.0.0.0)
    --port PORT         API port (default: 8008)
    --debug             Enable debug mode
    --no-background     Disable background tasks
"""

import argparse
import asyncio
import json
import logging
import os
import signal
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.gardener import (
    GardenerAgent,
    GardenerConfig,
    create_gardener_agent,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger("gardener.deploy")


class GardenerDeployment:
    """
    Deployment wrapper for the Gardener agent.

    Handles:
    - Configuration loading
    - Signal handling for graceful shutdown
    - Health checks
    - Metrics collection
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        host: str = "0.0.0.0",
        port: int = 8008,
        debug: bool = False,
        enable_background: bool = True,
    ):
        self.host = host
        self.port = port
        self.debug = debug
        self.enable_background = enable_background

        # Load configuration
        self.config = self._load_config(config_path)

        # Create agent
        self.agent = create_gardener_agent(**self.config)

        # Shutdown event
        self._shutdown_event = asyncio.Event()

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or environment"""
        config = {}

        # Load from file if provided
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_path}")

        # Override with environment variables
        env_mappings = {
            "GARDENER_AUTO_APPROVE_TRUSTED": ("auto_approve_trusted_users", bool),
            "GARDENER_TRUSTED_THRESHOLD": ("trusted_user_threshold", int),
            "GARDENER_PEER_REVIEW_TIMEOUT": ("peer_review_timeout_hours", int),
            "GARDENER_EXPERT_REVIEW_TIMEOUT": ("expert_review_timeout_hours", int),
            "GARDENER_ENABLE_ACHIEVEMENTS": ("enable_achievements", bool),
            "GARDENER_ENABLE_LEADERBOARDS": ("enable_leaderboards", bool),
        }

        for env_var, (config_key, type_fn) in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                if type_fn == bool:
                    config[config_key] = value.lower() in ("true", "1", "yes")
                else:
                    config[config_key] = type_fn(value)

        return config

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        loop = asyncio.get_event_loop()

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self._handle_signal(s))
            )

    async def _handle_signal(self, sig: signal.Signals):
        """Handle shutdown signal"""
        logger.info(f"Received signal {sig.name}, initiating graceful shutdown...")
        self._shutdown_event.set()

    async def start(self):
        """Start the Gardener agent deployment"""
        logger.info("=" * 60)
        logger.info("Agent_8: Community Cultivator (GARDENER)")
        logger.info("The Tender of Human-Machine Interface")
        logger.info("=" * 60)
        logger.info("")
        logger.info('"Data comes from sensors. Wisdom comes from humans.')
        logger.info('I cultivate the garden where engineers share their knowledge,')
        logger.info('and the machine learns from the masters."')
        logger.info("")
        logger.info("=" * 60)

        # Setup signal handlers
        try:
            self._setup_signal_handlers()
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            logger.warning("Signal handlers not available on this platform")

        # Start the agent
        logger.info("Starting Gardener agent...")
        await self.agent.start()

        # Display agent info
        info = self.agent.get_agent_info()
        logger.info(f"Agent ID: {info['id']}")
        logger.info(f"Agent Name: {info['name']}")
        logger.info(f"Agent Alias: {info['alias']}")
        logger.info(f"Status: {'Running' if info['running'] else 'Stopped'}")
        logger.info("")
        logger.info("Capabilities:")
        for cap in info["capabilities"]:
            logger.info(f"  - {cap}")
        logger.info("")
        logger.info("Integration Points:")
        logger.info("  Receives from:")
        for recv in info["integrations"]["receives_from"]:
            logger.info(f"    - {recv}")
        logger.info("  Sends to:")
        for send in info["integrations"]["sends_to"]:
            logger.info(f"    - {send}")
        logger.info("")
        logger.info(f"Listening on {self.host}:{self.port}")
        logger.info("Press Ctrl+C to stop")
        logger.info("")

        # Wait for shutdown signal
        await self._shutdown_event.wait()

        # Graceful shutdown
        await self.stop()

    async def stop(self):
        """Stop the Gardener agent deployment"""
        logger.info("Stopping Gardener agent...")
        await self.agent.stop()
        logger.info("Gardener agent stopped")

    async def health_check(self) -> dict:
        """Perform health check"""
        return {
            "agent_id": self.agent.AGENT_ID,
            "agent_name": self.agent.AGENT_NAME,
            "agent_alias": self.agent.AGENT_ALIAS,
            "status": "healthy" if self.agent._running else "stopped",
            "background_tasks": len(self.agent._background_tasks),
        }


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Deploy Agent_8: Community Cultivator (GARDENER)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m agents.gardener
    python -m agents.gardener --port 9000
    python -m agents.gardener --config config/gardener.json --debug
        """
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="API host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8008,
        help="API port (default: 8008)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )
    parser.add_argument(
        "--no-background",
        action="store_true",
        help="Disable background tasks",
    )

    return parser.parse_args()


async def main():
    """Main entry point"""
    args = parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    deployment = GardenerDeployment(
        config_path=args.config,
        host=args.host,
        port=args.port,
        debug=args.debug,
        enable_background=not args.no_background,
    )

    await deployment.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
