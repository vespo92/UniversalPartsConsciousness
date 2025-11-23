"""
HIVE Swarm Coordinator Service Entry Point

This module provides the deployment entry point for the HIVE Swarm Coordinator.
It can be run as a standalone service or integrated into the larger UPC system.

Usage:
    # As standalone service
    python -m agents.hive.coordinator.service

    # With custom config
    python -m agents.hive.coordinator.service --config config.json

    # In the UPC system
    from agents.hive.coordinator.service import deploy_hive_coordinator
    coordinator = await deploy_hive_coordinator()
"""

import argparse
import asyncio
import json
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .hive_coordinator import (
    HiveSwarmCoordinator,
    CoordinatorConfig,
    CoordinatorStatus,
    create_coordinator,
)
from ..hive_agent import HiveConfig, HiveRepository
from ..models import (
    Learning,
    LearningType,
    PropagationResult,
    RecallNotice,
    RecallSeverity,
    Swarm,
    SwarmHealth,
    SwarmHealthStatus,
    SwarmMembership,
    SwarmMessage,
    SwarmRole,
    SwarmTier,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("hive.coordinator.service")


# ============================================================================
# IN-MEMORY REPOSITORY (for standalone operation)
# ============================================================================

class InMemoryHiveRepository:
    """
    In-memory implementation of HiveRepository for standalone operation.

    This is used when running the coordinator without a database connection.
    For production, replace with a persistent repository implementation.
    """

    def __init__(self):
        self._swarms: dict[UUID, Swarm] = {}
        self._swarm_keys: dict[str, UUID] = {}
        self._memberships: dict[UUID, SwarmMembership] = {}
        self._part_memberships: dict[UUID, list[UUID]] = {}
        self._learnings: dict[UUID, list[tuple[Learning, float, datetime]]] = {}
        self._recalls: dict[UUID, RecallNotice] = {}
        self._messages: dict[UUID, list[SwarmMessage]] = {}
        self._health: dict[UUID, SwarmHealth] = {}

    # Swarm operations
    async def get_swarm(self, swarm_id: UUID) -> Optional[Swarm]:
        return self._swarms.get(swarm_id)

    async def get_swarm_by_key(self, key: str) -> Optional[Swarm]:
        swarm_id = self._swarm_keys.get(key)
        if swarm_id:
            return self._swarms.get(swarm_id)
        return None

    async def create_swarm(self, swarm: Swarm) -> Swarm:
        self._swarms[swarm.id] = swarm
        self._swarm_keys[swarm.get_swarm_key()] = swarm.id
        self._learnings[swarm.id] = []
        self._messages[swarm.id] = []
        return swarm

    async def update_swarm(self, swarm: Swarm) -> Swarm:
        swarm.updated_at = datetime.utcnow()
        self._swarms[swarm.id] = swarm
        return swarm

    async def get_all_swarms(self) -> list[Swarm]:
        return list(self._swarms.values())

    # Membership operations
    async def add_membership(self, membership: SwarmMembership) -> SwarmMembership:
        self._memberships[membership.id] = membership

        # Track by part
        if membership.part_id not in self._part_memberships:
            self._part_memberships[membership.part_id] = []
        self._part_memberships[membership.part_id].append(membership.id)

        # Update swarm stats
        swarm = self._swarms.get(membership.swarm_id)
        if swarm:
            swarm.member_count += 1
            if membership.role == SwarmRole.ELDER:
                swarm.elder_count += 1
            elif membership.role == SwarmRole.MENTOR:
                swarm.mentor_count += 1
            swarm.active_member_count += 1

        return membership

    async def get_part_swarms(self, part_id: UUID) -> list[Swarm]:
        membership_ids = self._part_memberships.get(part_id, [])
        swarms = []
        for mid in membership_ids:
            membership = self._memberships.get(mid)
            if membership:
                swarm = self._swarms.get(membership.swarm_id)
                if swarm:
                    swarms.append(swarm)
        return swarms

    async def get_swarm_members(
        self, swarm_id: UUID, limit: int = 1000
    ) -> list[SwarmMembership]:
        return [
            m for m in self._memberships.values()
            if m.swarm_id == swarm_id
        ][:limit]

    # Learning operations
    async def record_learning(
        self, swarm_id: UUID, learning: Learning, strength: float
    ) -> None:
        if swarm_id not in self._learnings:
            self._learnings[swarm_id] = []
        self._learnings[swarm_id].append((learning, strength, datetime.utcnow()))

        swarm = self._swarms.get(swarm_id)
        if swarm:
            swarm.learning_count += 1
            swarm.last_learning_at = datetime.utcnow()

    async def get_swarm_learnings(
        self, swarm_id: UUID, since: Optional[datetime] = None
    ) -> list[Learning]:
        learnings = self._learnings.get(swarm_id, [])
        if since:
            return [l for l, s, t in learnings if t >= since]
        return [l for l, s, t in learnings]

    # Recall operations
    async def save_recall(self, recall: RecallNotice) -> RecallNotice:
        recall.received_at = datetime.utcnow()
        self._recalls[recall.id] = recall
        return recall

    async def get_active_recalls(self) -> list[RecallNotice]:
        return [
            r for r in self._recalls.values()
            if r.propagation_status != "complete"
        ]

    # Message operations
    async def queue_message(self, message: SwarmMessage) -> None:
        for target_id in message.target_swarm_ids:
            if target_id not in self._messages:
                self._messages[target_id] = []
            self._messages[target_id].append(message)

    async def deliver_message(self, swarm_id: UUID, message: SwarmMessage) -> bool:
        if swarm_id not in self._messages:
            self._messages[swarm_id] = []
        self._messages[swarm_id].append(message)
        message.delivered_to.append(swarm_id)
        return True

    # Health operations
    async def save_health(self, health: SwarmHealth) -> None:
        self._health[health.swarm_id] = health

    async def get_swarm_health(self, swarm_id: UUID) -> Optional[SwarmHealth]:
        return self._health.get(swarm_id)


# ============================================================================
# SERVICE DEPLOYMENT
# ============================================================================

async def deploy_hive_coordinator(
    config: Optional[CoordinatorConfig] = None,
    repository: Optional[HiveRepository] = None,
) -> HiveSwarmCoordinator:
    """
    Deploy the HIVE Swarm Coordinator.

    This is the main entry point for deploying the coordinator service.

    Args:
        config: Optional coordinator configuration
        repository: Optional repository implementation (uses in-memory if not provided)

    Returns:
        Running HiveSwarmCoordinator instance
    """
    logger.info("=" * 60)
    logger.info("HIVE SWARM COORDINATOR")
    logger.info("\"One learns, all learn.\"")
    logger.info("=" * 60)

    # Use in-memory repository if none provided
    if repository is None:
        logger.info("Using in-memory repository")
        repository = InMemoryHiveRepository()

    # Create coordinator
    config = config or CoordinatorConfig()
    coordinator = create_coordinator(
        repository=repository,
        config=config,
    )

    # Start the coordinator
    logger.info("Starting HIVE Swarm Coordinator...")
    await coordinator.start()

    status = await coordinator.get_status()
    logger.info(f"Coordinator status: {status['coordinator']['status']}")
    logger.info(f"Agent ID: {coordinator.AGENT_ID}")
    logger.info(f"Codename: {coordinator.CODENAME}")
    logger.info(f"Role: {coordinator.ROLE}")

    return coordinator


async def run_service(config_path: Optional[str] = None) -> None:
    """
    Run the HIVE Swarm Coordinator as a standalone service.

    Args:
        config_path: Optional path to configuration file
    """
    # Load configuration
    config = CoordinatorConfig()
    if config_path:
        with open(config_path) as f:
            config_data = json.load(f)
            # Apply configuration overrides
            if "coordinator_id" in config_data:
                config.coordinator_id = config_data["coordinator_id"]
            if "coordinator_name" in config_data:
                config.coordinator_name = config_data["coordinator_name"]

    # Deploy coordinator
    coordinator = await deploy_hive_coordinator(config=config)

    # Set up signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    shutdown_event = asyncio.Event()

    def signal_handler():
        logger.info("Received shutdown signal")
        shutdown_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    logger.info("HIVE Swarm Coordinator is running. Press Ctrl+C to stop.")

    # Print initial status
    status = await coordinator.get_status()
    logger.info(f"Initial stats: {status['stats']}")

    # Wait for shutdown
    await shutdown_event.wait()

    # Graceful shutdown
    logger.info("Shutting down HIVE Swarm Coordinator...")
    await coordinator.stop()
    logger.info("Coordinator stopped. Goodbye!")


def print_banner():
    """Print the HIVE Swarm Coordinator banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     ██╗  ██╗██╗██╗   ██╗███████╗                             ║
    ║     ██║  ██║██║██║   ██║██╔════╝                             ║
    ║     ███████║██║██║   ██║█████╗                               ║
    ║     ██╔══██║██║╚██╗ ██╔╝██╔══╝                               ║
    ║     ██║  ██║██║ ╚████╔╝ ███████╗                             ║
    ║     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝                             ║
    ║                                                               ║
    ║           S W A R M   C O O R D I N A T O R                  ║
    ║                                                               ║
    ║     "One bolt knows only itself. A thousand bolts know       ║
    ║      everything. I am the voice that makes them speak        ║
    ║      as one."                                                ║
    ║                                                               ║
    ║                    ONE LEARNS, ALL LEARN                     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point for the HIVE Swarm Coordinator service."""
    parser = argparse.ArgumentParser(
        description="HIVE Swarm Coordinator - Organizes Collective Learning"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress banner output",
    )

    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    try:
        asyncio.run(run_service(config_path=args.config))
    except KeyboardInterrupt:
        logger.info("Service interrupted")
        sys.exit(0)


if __name__ == "__main__":
    main()
