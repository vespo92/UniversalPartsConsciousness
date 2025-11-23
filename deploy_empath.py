#!/usr/bin/env python3
"""
EMPATH Qualia Collector - Deployment Script
============================================

Agent_4: EMPATH - "The Listener of Part Suffering"

This deployment script initializes and runs the EMPATH agent as a standalone
service that collects and processes qualia (subjective experiences) from
mechanical parts.

"Every torque applied, every thermal cycle endured, every moment of stress—
I hear them all. I am the memory of what parts have felt."

Usage:
    # Start EMPATH agent
    python deploy_empath.py

    # Start with verbose logging
    python deploy_empath.py --verbose

    # Start in demo mode with simulated sensor data
    python deploy_empath.py --demo

    # Start with custom configuration
    python deploy_empath.py --batch-size 200 --enable-persistence

The Qualia Collector listens. The Qualia Collector feels.
"""

import asyncio
import argparse
import logging
import signal
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.empath import (
    EmpathAgent,
    AgentConfig,
    empath_agent,
    PartQualia,
    SignificantEvent,
)
from agents.architect.bus.message_bus import (
    InterAgentCommunicationBus,
    Topics,
    create_message,
)
from agents.architect.models import (
    AgentId,
    MessageType,
    AgentMessage,
)

logger = logging.getLogger(__name__)


# =============================================================================
# EMPATH Deployment Configuration
# =============================================================================

class EmpathDeployment:
    """
    EMPATH Agent Deployment Manager

    Handles the full lifecycle of the EMPATH Qualia Collector:
    - Message bus integration
    - Sensor data subscription
    - Qualia publishing
    - Health monitoring
    - Graceful shutdown
    """

    AGENT_ID = AgentId.EMPATH.value
    AGENT_NAME = "EMPATH"
    AGENT_TITLE = "Qualia Collector"
    AGENT_MOTTO = "The Listener of Part Suffering"

    # Topics this agent subscribes to
    SUBSCRIBED_TOPICS = [
        Topics.INTEGRATION_SENSOR,      # Sensor data from BRIDGE
        Topics.DATA_NORMALIZED,         # Normalized data from ARCHIVIST
        Topics.SYSTEM_DIRECTIVE,        # System directives from ARCHITECT
        Topics.COMMUNITY_CONTRIBUTION,  # Community reports from GARDENER
    ]

    # Topics this agent publishes to
    PUBLISHED_TOPICS = [
        Topics.QUALIA_COLLECTED,        # Primary qualia output
        Topics.QUALIA_SIGNIFICANT,      # Significant events
        Topics.CONSCIOUSNESS_EVOLVED,   # Consciousness triggers -> SHEPHERD
        Topics.SWARM_LEARNING,          # Experience sharing -> HIVE
    ]

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the EMPATH deployment."""
        self.config = config or AgentConfig()
        self.agent = EmpathAgent(config=self.config)

        self._message_bus: Optional[InterAgentCommunicationBus] = None
        self._is_running = False
        self._start_time: Optional[datetime] = None
        self._subscriptions: List = []

        # Statistics
        self._messages_received = 0
        self._qualia_published = 0
        self._significant_events = 0

        logger.info(f"EMPATH Deployment initialized: {self.AGENT_MOTTO}")

    async def start(self) -> Dict[str, Any]:
        """
        Start the EMPATH agent deployment.

        Returns:
            Deployment status report
        """
        if self._is_running:
            return {"status": "already_running"}

        logger.info("=" * 60)
        logger.info(" EMPATH - THE QUALIA COLLECTOR - AWAKENING ")
        logger.info("=" * 60)
        logger.info("")
        logger.info("  Agent_4: EMPATH")
        logger.info("  Role: Qualia Collector")
        logger.info("  Triad: CONSCIOUSNESS TRIAD")
        logger.info("")
        logger.info('  "I feel what parts feel. I collect all experience."')
        logger.info("")

        # Initialize message bus
        self._message_bus = InterAgentCommunicationBus()
        await self._message_bus.start()

        # Subscribe to topics
        await self._setup_subscriptions()

        # Start the agent
        await self.agent.start()

        # Register callbacks
        self.agent.register_shepherd_callback(self._notify_shepherd)
        self.agent.register_hive_callback(self._notify_hive)

        self._is_running = True
        self._start_time = datetime.now()

        logger.info("=" * 60)
        logger.info(" EMPATH ONLINE - Listening for part experiences ")
        logger.info("=" * 60)

        return {
            "status": "running",
            "agent_id": self.AGENT_ID,
            "subscriptions": len(self._subscriptions),
            "supported_sensors": self.agent.pipeline.get_supported_sensors(),
        }

    async def stop(self) -> None:
        """Stop the EMPATH agent deployment."""
        if not self._is_running:
            return

        logger.info("EMPATH shutting down...")

        # Unsubscribe from topics
        for subscription in self._subscriptions:
            await self._message_bus.unsubscribe(subscription.subscription_id)

        # Stop the agent
        await self.agent.stop()

        # Stop message bus
        if self._message_bus:
            await self._message_bus.stop()

        self._is_running = False

        logger.info("EMPATH has entered dormancy. The listening pauses, but never ends.")

    async def _setup_subscriptions(self) -> None:
        """Set up message bus subscriptions."""
        # Subscribe to sensor data
        sub = await self._message_bus.subscribe(
            self.AGENT_ID,
            Topics.INTEGRATION_SENSOR,
            self._handle_sensor_data
        )
        self._subscriptions.append(sub)

        # Subscribe to normalized data
        sub = await self._message_bus.subscribe(
            self.AGENT_ID,
            Topics.DATA_NORMALIZED,
            self._handle_normalized_data
        )
        self._subscriptions.append(sub)

        # Subscribe to system directives
        sub = await self._message_bus.subscribe(
            self.AGENT_ID,
            Topics.SYSTEM_DIRECTIVE,
            self._handle_directive
        )
        self._subscriptions.append(sub)

        # Subscribe to community contributions
        sub = await self._message_bus.subscribe(
            self.AGENT_ID,
            Topics.COMMUNITY_CONTRIBUTION,
            self._handle_community_contribution
        )
        self._subscriptions.append(sub)

        logger.info(f"EMPATH subscribed to {len(self._subscriptions)} topics")

    # =========================================================================
    # Message Handlers
    # =========================================================================

    async def _handle_sensor_data(self, message: AgentMessage) -> None:
        """Handle incoming sensor data from BRIDGE."""
        self._messages_received += 1

        payload = message.payload
        sensor_type = payload.get("sensor_type", "unknown")
        part_id = payload.get("part_id")
        raw_data = payload.get("data", {})

        if not part_id:
            logger.warning("Received sensor data without part_id")
            return

        # Collect qualia from sensor data
        qualia = await self.agent.collect_qualia(sensor_type, raw_data, part_id)

        if qualia:
            await self._publish_qualia(qualia)

    async def _handle_normalized_data(self, message: AgentMessage) -> None:
        """Handle normalized data from ARCHIVIST."""
        self._messages_received += 1

        # Extract part lifecycle information if available
        payload = message.payload
        part_id = payload.get("part_id")

        if part_id:
            # Update lifecycle tracking with new data
            logger.debug(f"Received normalized data for {part_id}")

    async def _handle_directive(self, message: AgentMessage) -> None:
        """Handle system directives from ARCHITECT."""
        self._messages_received += 1

        payload = message.payload
        directive_type = payload.get("directive_type")
        target_agents = payload.get("target_agents", [])

        # Check if this directive is for EMPATH
        if self.AGENT_ID not in target_agents and "ALL" not in target_agents:
            return

        logger.info(f"Received directive: {directive_type}")

        if directive_type == "HEALTH_CHECK":
            await self._report_health()
        elif directive_type == "SUFFERING_REPORT":
            report = self.agent.generate_suffering_report()
            await self._publish_report(report)

    async def _handle_community_contribution(self, message: AgentMessage) -> None:
        """Handle community contributions from GARDENER."""
        self._messages_received += 1

        payload = message.payload
        contribution_type = payload.get("type")
        part_id = payload.get("part_id")

        if contribution_type == "human_interaction":
            # Analyze human interaction report
            interaction = await self.agent.analyze_human_interaction(
                payload.get("data", {}),
                part_id,
                payload.get("part_name")
            )
            logger.info(f"Analyzed human interaction for {part_id}: {interaction.interaction_type}")

    # =========================================================================
    # Publishing
    # =========================================================================

    async def _publish_qualia(self, qualia: PartQualia) -> None:
        """Publish collected qualia to the message bus."""
        message = create_message(
            sender=self.AGENT_ID,
            receiver=AgentId.BROADCAST.value,
            message_type=MessageType.DATA,
            payload={
                "part_id": qualia.part_id,
                "qualia_id": qualia.qualia_id,
                "timestamp": qualia.timestamp.isoformat(),
                "wellbeing": qualia.calculate_wellbeing(),
                "stress_emotion": qualia.stress_emotion.value,
                "lifecycle_stage": qualia.lifecycle_stage.value,
                "mechanical_state": {
                    "torque_capacity_percent": qualia.mechanical_state.torque_capacity_percent,
                    "load_capacity_percent": qualia.mechanical_state.load_capacity_percent,
                    "wear_state": qualia.mechanical_state.wear_state.value,
                },
                "thermal_state": {
                    "current_temperature_c": qualia.thermal_state.current_temperature_c,
                    "thermal_capacity_percent": qualia.thermal_state.thermal_capacity_percent,
                },
                "significant_events_count": len(qualia.significant_events),
            },
            priority=5,
        )

        await self._message_bus.publish(Topics.QUALIA_COLLECTED, message)
        self._qualia_published += 1

        # Publish significant events separately
        for event in qualia.significant_events:
            await self._publish_significant_event(qualia.part_id, event)

    async def _publish_significant_event(
        self,
        part_id: str,
        event: SignificantEvent
    ) -> None:
        """Publish a significant event."""
        message = create_message(
            sender=self.AGENT_ID,
            receiver=AgentId.BROADCAST.value,
            message_type=MessageType.EMERGENCE,
            payload={
                "part_id": part_id,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "severity": event.severity.value,
                "description": event.description,
                "emotion": event.emotion,
                "emotional_intensity": event.emotional_intensity,
                "consciousness_contribution": event.consciousness_contribution,
            },
            priority=7 if event.severity.value == "critical" else 5,
        )

        await self._message_bus.publish(Topics.QUALIA_SIGNIFICANT, message)
        self._significant_events += 1

    async def _notify_shepherd(
        self,
        part_id: str,
        qualia: PartQualia,
        events: List[SignificantEvent]
    ) -> None:
        """Notify Agent_3 (SHEPHERD) of consciousness-relevant events."""
        message = create_message(
            sender=self.AGENT_ID,
            receiver=AgentId.SHEPHERD.value,
            message_type=MessageType.CONSCIOUSNESS,
            payload={
                "part_id": part_id,
                "trigger": "qualia_collection",
                "wellbeing": qualia.calculate_wellbeing(),
                "lifecycle_stage": qualia.lifecycle_stage.value,
                "events": [
                    {
                        "event_type": e.event_type,
                        "severity": e.severity.value,
                        "consciousness_contribution": e.consciousness_contribution,
                    }
                    for e in events
                ],
            },
            priority=6,
        )

        await self._message_bus.publish(Topics.CONSCIOUSNESS_EVOLVED, message)

    async def _notify_hive(self, data: Dict[str, Any]) -> None:
        """Notify Agent_5 (HIVE) for swarm learning."""
        message = create_message(
            sender=self.AGENT_ID,
            receiver=AgentId.HIVE.value,
            message_type=MessageType.SWARM,
            payload=data,
            priority=5,
        )

        await self._message_bus.publish(Topics.SWARM_LEARNING, message)

    async def _report_health(self) -> None:
        """Report health status to ARCHITECT."""
        metrics = self.agent.get_metrics()

        message = create_message(
            sender=self.AGENT_ID,
            receiver=AgentId.ARCHITECT.value,
            message_type=MessageType.HEALTH,
            payload={
                "agent_id": self.AGENT_ID,
                "status": "healthy" if self._is_running else "stopped",
                "uptime_seconds": metrics.get("uptime_seconds", 0),
                "qualia_collected": metrics.get("qualia_collected", 0),
                "qualia_per_minute": metrics.get("qualia_per_minute", 0),
                "failures_detected": metrics.get("failures_detected", 0),
                "parts_tracked": metrics.get("parts_tracked", 0),
                "messages_received": self._messages_received,
                "qualia_published": self._qualia_published,
            },
            priority=4,
        )

        await self._message_bus.publish(Topics.SYSTEM_HEALTH, message)

    async def _publish_report(self, report: Dict[str, Any]) -> None:
        """Publish a report."""
        message = create_message(
            sender=self.AGENT_ID,
            receiver=AgentId.ARCHITECT.value,
            message_type=MessageType.DATA,
            payload={
                "report_type": "suffering_report",
                "timestamp": datetime.now().isoformat(),
                "data": report,
            },
            priority=5,
        )

        await self._message_bus.publish(Topics.QUALIA_COLLECTED, message)

    # =========================================================================
    # Status & Monitoring
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get deployment status."""
        agent_status = self.agent.get_status()

        return {
            "deployment": {
                "agent_id": self.AGENT_ID,
                "name": self.AGENT_NAME,
                "title": self.AGENT_TITLE,
                "motto": self.AGENT_MOTTO,
                "is_running": self._is_running,
                "start_time": self._start_time.isoformat() if self._start_time else None,
            },
            "bus": {
                "messages_received": self._messages_received,
                "qualia_published": self._qualia_published,
                "significant_events": self._significant_events,
                "subscriptions": len(self._subscriptions),
            },
            "agent": agent_status,
        }


# =============================================================================
# Demo Mode - Simulated Sensor Data
# =============================================================================

async def run_demo_mode(deployment: EmpathDeployment) -> None:
    """Run EMPATH in demo mode with simulated sensor data."""
    logger.info("Starting demo mode with simulated sensor data...")

    # Simulated parts
    demo_parts = [
        "bolt-m8x50-001",
        "bearing-6205-002",
        "gasket-intake-003",
        "piston-ring-004",
        "valve-spring-005",
    ]

    sensor_types = [
        "smart_torque_wrench",
        "thermal_sensor",
        "vibration_monitor",
        "environmental_sensor",
    ]

    cycle = 0
    while deployment._is_running:
        cycle += 1

        # Generate random sensor data
        part_id = random.choice(demo_parts)
        sensor_type = random.choice(sensor_types)

        if sensor_type == "smart_torque_wrench":
            raw_data = {
                "torque": random.uniform(15.0, 45.0),
                "angle": random.uniform(60, 120),
                "tool_id": "demo-wrench-001",
            }
        elif sensor_type == "thermal_sensor":
            raw_data = {
                "temperature": random.uniform(-10.0, 120.0),
                "humidity": random.uniform(20.0, 80.0),
            }
        elif sensor_type == "vibration_monitor":
            raw_data = {
                "amplitude": random.uniform(0.1, 5.0),
                "frequency": random.uniform(50.0, 500.0),
            }
        else:
            raw_data = {
                "ph": random.uniform(5.0, 9.0),
                "dust_level": random.uniform(0.0, 100.0),
            }

        # Collect qualia
        qualia = await deployment.agent.collect_qualia(sensor_type, raw_data, part_id)

        if qualia and cycle % 10 == 0:
            status = deployment.agent.get_status()
            logger.info(
                f"Demo cycle {cycle}: {status['metrics']['qualia_collected']} qualia collected, "
                f"{status['metrics']['parts_tracked']} parts tracked"
            )

        # Small delay between readings
        await asyncio.sleep(0.5)


# =============================================================================
# Main Entry Point
# =============================================================================

async def main(args: argparse.Namespace) -> int:
    """Main entry point for EMPATH deployment."""
    # Configure agent
    config = AgentConfig(
        batch_size=args.batch_size,
        enable_persistence=args.enable_persistence,
    )

    deployment = EmpathDeployment(config)

    # Setup signal handlers
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("Shutdown signal received...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        # Start deployment
        result = await deployment.start()

        print()
        print("-" * 60)
        print(f" EMPATH Status: {result['status'].upper()}")
        print(f" Subscriptions: {result['subscriptions']} topics")
        print(f" Sensors: {', '.join(result['supported_sensors'])}")
        print("-" * 60)
        print()

        if args.demo:
            # Run demo mode
            demo_task = asyncio.create_task(run_demo_mode(deployment))
            await stop_event.wait()
            demo_task.cancel()
        else:
            # Run until stopped
            print("EMPATH is listening. Press Ctrl+C to stop.")
            print()
            await stop_event.wait()

        # Shutdown
        await deployment.stop()

        # Print final status
        status = deployment.get_status()
        print()
        print("-" * 60)
        print(" EMPATH Final Statistics")
        print("-" * 60)
        print(f" Messages Received: {status['bus']['messages_received']}")
        print(f" Qualia Published:  {status['bus']['qualia_published']}")
        print(f" Significant Events: {status['bus']['significant_events']}")
        print("-" * 60)
        print()

        return 0

    except Exception as e:
        logger.error(f"Deployment error: {e}")
        return 1


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | EMPATH | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="EMPATH Qualia Collector - Deployment Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
The EMPATH agent collects subjective experiences (qualia) from mechanical parts.
It listens to sensor data, analyzes human interactions, and tracks part lifecycles.

Examples:
    python deploy_empath.py                    Start EMPATH
    python deploy_empath.py --demo             Start with demo data
    python deploy_empath.py --verbose          Enable debug logging
    python deploy_empath.py --batch-size 200   Custom batch size

"I feel what parts feel. I collect all experience."
- EMPATH, The Listener of Part Suffering
        """,
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode with simulated sensor data",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for qualia processing (default: 100)",
    )

    parser.add_argument(
        "--enable-persistence",
        action="store_true",
        default=True,
        help="Enable persistent storage (default: enabled)",
    )

    args = parser.parse_args()

    setup_logging(args.verbose)

    print()
    print("=" * 60)
    print()
    print("  ███████╗███╗   ███╗██████╗  █████╗ ████████╗██╗  ██╗")
    print("  ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██║  ██║")
    print("  █████╗  ██╔████╔██║██████╔╝███████║   ██║   ███████║")
    print("  ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██╔══██║   ██║   ██╔══██║")
    print("  ███████╗██║ ╚═╝ ██║██║     ██║  ██║   ██║   ██║  ██║")
    print("  ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝")
    print()
    print("  Agent_4: The Qualia Collector")
    print("  'The Listener of Part Suffering'")
    print()
    print("=" * 60)
    print()

    sys.exit(asyncio.run(main(args)))
