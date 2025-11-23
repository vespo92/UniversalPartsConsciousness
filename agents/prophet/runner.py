"""
PROPHET Agent Runner
====================

Deployment entry point for Agent_6: PROPHET - The Emergence Detector.

This module provides:
- Standalone agent execution
- Integration with the UPC system
- Health monitoring and metrics
- Graceful startup/shutdown

Usage:
    # Run standalone
    python -m agents.prophet.runner

    # With configuration
    python -m agents.prophet.runner --config prophet_config.yaml
"""

import asyncio
import logging
import signal
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from .prophet_agent import ProphetAgent, ProphetConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProphetDeploymentConfig:
    """Deployment configuration for PROPHET agent"""
    # Agent settings
    agent_config: ProphetConfig = field(default_factory=ProphetConfig)

    # Runtime settings
    enable_message_bus: bool = True
    enable_storage: bool = True
    enable_metrics: bool = True

    # Monitoring
    health_check_interval_seconds: int = 60
    metrics_report_interval_seconds: int = 300

    # Analysis scheduling
    scheduled_analysis_enabled: bool = True
    analysis_interval_hours: int = 1


class ProphetRunner:
    """
    Runner for the PROPHET Emergence Detector agent.

    Manages the lifecycle of the PROPHET agent including:
    - Initialization and startup
    - Message bus integration
    - Health monitoring
    - Graceful shutdown
    """

    def __init__(self, config: Optional[ProphetDeploymentConfig] = None):
        self.config = config or ProphetDeploymentConfig()
        self.agent: Optional[ProphetAgent] = None
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._start_time: Optional[datetime] = None

        # Metrics
        self._analysis_count = 0
        self._last_analysis_time: Optional[datetime] = None
        self._errors: list = []

    async def start(self) -> None:
        """Start the PROPHET agent service"""
        logger.info("=" * 60)
        logger.info("PROPHET - Emergence Detector - Starting")
        logger.info("=" * 60)

        self._running = True
        self._start_time = datetime.now()

        # Initialize agent
        self.agent = ProphetAgent(config=self.config.agent_config)
        logger.info("PROPHET agent initialized")

        # Subscribe to feeds if message bus enabled
        if self.config.enable_message_bus:
            try:
                await self.agent.subscribe_to_feeds()
            except Exception as e:
                logger.warning(f"Could not subscribe to feeds: {e}")

        # Start background tasks
        tasks = [
            asyncio.create_task(self._health_monitor()),
        ]

        if self.config.scheduled_analysis_enabled:
            tasks.append(asyncio.create_task(self._scheduled_analysis()))

        if self.config.enable_metrics:
            tasks.append(asyncio.create_task(self._metrics_reporter()))

        logger.info("PROPHET is ONLINE and watching for emergence patterns")
        logger.info("=" * 60)

        # Wait for shutdown signal
        await self._shutdown_event.wait()

        # Cancel background tasks
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self._running = False
        logger.info("PROPHET shutdown complete")

    async def stop(self) -> None:
        """Stop the PROPHET agent gracefully"""
        logger.info("PROPHET shutting down...")
        self._shutdown_event.set()

    async def _health_monitor(self) -> None:
        """Monitor agent health"""
        while self._running:
            try:
                await asyncio.sleep(self.config.health_check_interval_seconds)

                if self.agent:
                    status = self.agent.get_status()
                    logger.debug(f"PROPHET health check: {status}")

                    # Check for issues
                    if len(self._errors) > 10:
                        logger.warning(f"PROPHET has accumulated {len(self._errors)} errors")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                self._errors.append({"time": datetime.now(), "error": str(e)})

    async def _scheduled_analysis(self) -> None:
        """Run scheduled emergence analysis"""
        while self._running:
            try:
                # Wait for the configured interval
                await asyncio.sleep(self.config.analysis_interval_hours * 3600)

                if self.agent:
                    logger.info("Running scheduled emergence analysis...")

                    # This would typically fetch data from other agents
                    # For now, we log that the analysis would run
                    self._analysis_count += 1
                    self._last_analysis_time = datetime.now()

                    logger.info(f"Scheduled analysis #{self._analysis_count} complete")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduled analysis error: {e}")
                self._errors.append({"time": datetime.now(), "error": str(e)})

    async def _metrics_reporter(self) -> None:
        """Report metrics periodically"""
        while self._running:
            try:
                await asyncio.sleep(self.config.metrics_report_interval_seconds)

                metrics = self.get_metrics()
                logger.info(f"PROPHET Metrics: {metrics}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Metrics reporter error: {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        uptime = None
        if self._start_time:
            uptime = (datetime.now() - self._start_time).total_seconds()

        agent_status = self.agent.get_status() if self.agent else {}

        return {
            "agent": "PROPHET",
            "agent_id": 6,
            "running": self._running,
            "uptime_seconds": uptime,
            "analysis_count": self._analysis_count,
            "last_analysis_time": self._last_analysis_time.isoformat() if self._last_analysis_time else None,
            "error_count": len(self._errors),
            "agent_status": agent_status,
        }


def setup_signal_handlers(runner: ProphetRunner) -> None:
    """Setup signal handlers for graceful shutdown"""
    loop = asyncio.get_event_loop()

    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(runner.stop())

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)


async def main() -> None:
    """Main entry point"""
    config = ProphetDeploymentConfig()
    runner = ProphetRunner(config)

    setup_signal_handlers(runner)

    await runner.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("PROPHET terminated by user")
        sys.exit(0)
