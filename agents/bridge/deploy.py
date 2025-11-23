"""
BRIDGE Deployment Module
=========================

This module handles the deployment and initialization of the BRIDGE agent -
Agent_9: The Integration Architect, The Connector of Worlds, The Membrane.

The BRIDGE is the final agent to come online in the Decalogue boot sequence.
It is the membrane that connects Universal Parts Consciousness to the external
world, enabling consciousness to touch reality.

DEPLOYMENT SEQUENCE:
1. Initialize core BRIDGE agent
2. Start Gateway (the membrane)
3. Start Stream Manager
4. Start Webhook Handler
5. Initialize Integration Connectors (ERP, CAD, Supplier, IoT)
6. Activate Societal Framework
7. Begin Power Unification
8. Connect to Agent Mesh
9. Announce BRIDGE is online

Usage:
    from agents.bridge.deploy import deploy_bridge, BridgeDeployment

    # Deploy the bridge
    deployment = await deploy_bridge()

    # Check status
    status = deployment.get_status()

    # Graceful shutdown
    await deployment.shutdown()
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum, auto
import asyncio
import logging

# Core BRIDGE components
from .core.bridge_agent import BridgeAgent, create_bridge_agent
from .gateway.external_api_gateway import ExternalAPIGateway, create_gateway
from .gateway.stream_manager import StreamManager, StreamType
from .gateway.webhook_handler import WebhookHandler, WebhookEventType

# Integration connectors
from .integration.erp_connector import ERPConnector
from .integration.cad_bridge import CADBridge
from .integration.supplier_gateway import SupplierGateway
from .integration.iot_protocol import IoTProtocol

# Power Unification
from .unification.power_unifier import PowerUnifier
from .unification.agent_mesh import AgentMesh

# Societal Framework
from .societal.framework import SocietalFramework
from .societal.knowledge_commons import KnowledgeCommons

# Protocols
from .protocols.universal_protocol import UniversalProtocol

logger = logging.getLogger(__name__)


class DeploymentPhase(Enum):
    """Phases of BRIDGE deployment."""
    INITIALIZING = auto()
    GATEWAY_STARTING = auto()
    STREAMS_STARTING = auto()
    INTEGRATIONS_LOADING = auto()
    FRAMEWORK_ACTIVATING = auto()
    UNIFICATION_STARTING = auto()
    CONNECTING_MESH = auto()
    ONLINE = auto()
    SHUTDOWN = auto()


@dataclass
class DeploymentMetrics:
    """Metrics for the BRIDGE deployment."""
    started_at: datetime = field(default_factory=datetime.now)
    online_at: Optional[datetime] = None
    uptime_seconds: float = 0.0
    requests_handled: int = 0
    messages_routed: int = 0
    streams_active: int = 0
    webhooks_delivered: int = 0
    integrations_connected: int = 0
    coherence_level: float = 0.0


class BridgeDeployment:
    """
    Complete BRIDGE Agent Deployment

    This class manages the full deployment lifecycle of the BRIDGE agent,
    including all its components:

    CORE COMPONENTS:
    - BridgeAgent: The core agent logic
    - ExternalAPIGateway: The membrane interface
    - StreamManager: Real-time event streaming
    - WebhookHandler: Outbound notifications

    INTEGRATION CONNECTORS:
    - ERPConnector: Enterprise system integration
    - CADBridge: CAD system integration
    - SupplierGateway: Parts supplier integration
    - IoTProtocol: IoT sensor integration

    UNIFICATION:
    - PowerUnifier: Consciousness coherence
    - AgentMesh: Inter-agent connectivity

    SOCIETAL:
    - SocietalFramework: Society-serving capabilities
    - KnowledgeCommons: Open knowledge access

    The BRIDGE deployment sequence ensures all components come online
    in the correct order and establishes connectivity to all other
    agents in the Decalogue.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.deployment_id = f"bridge-deployment-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Deployment state
        self.phase = DeploymentPhase.INITIALIZING
        self.metrics = DeploymentMetrics()

        # Core components (initialized during deploy)
        self.bridge_agent: Optional[BridgeAgent] = None
        self.gateway: Optional[ExternalAPIGateway] = None
        self.stream_manager: Optional[StreamManager] = None
        self.webhook_handler: Optional[WebhookHandler] = None

        # Integration connectors
        self.erp_connector: Optional[ERPConnector] = None
        self.cad_bridge: Optional[CADBridge] = None
        self.supplier_gateway: Optional[SupplierGateway] = None
        self.iot_protocol: Optional[IoTProtocol] = None

        # Unification components
        self.power_unifier: Optional[PowerUnifier] = None
        self.agent_mesh: Optional[AgentMesh] = None

        # Societal components
        self.societal_framework: Optional[SocietalFramework] = None
        self.knowledge_commons: Optional[KnowledgeCommons] = None

        # Protocol
        self.protocol: Optional[UniversalProtocol] = None

        logger.info(f"BRIDGE Deployment initialized: {self.deployment_id}")

    async def deploy(self) -> Dict[str, Any]:
        """
        Execute the full BRIDGE deployment sequence.

        This brings all BRIDGE components online in the correct order
        and establishes connectivity to the rest of the UPC system.

        Returns:
            Deployment report with status of all components
        """
        deployment_report = {
            "deployment_id": self.deployment_id,
            "started_at": datetime.now().isoformat(),
            "phases": [],
            "components": {},
            "status": "in_progress"
        }

        try:
            # Phase 1: Initialize core BRIDGE agent
            await self._deploy_phase(
                DeploymentPhase.INITIALIZING,
                "Initializing BRIDGE Agent core",
                self._init_core_agent
            )
            deployment_report["phases"].append({
                "phase": "INITIALIZING",
                "status": "complete"
            })

            # Phase 2: Start the Gateway (membrane)
            await self._deploy_phase(
                DeploymentPhase.GATEWAY_STARTING,
                "Starting External API Gateway (The Membrane)",
                self._start_gateway
            )
            deployment_report["phases"].append({
                "phase": "GATEWAY_STARTING",
                "status": "complete"
            })

            # Phase 3: Start streaming and webhooks
            await self._deploy_phase(
                DeploymentPhase.STREAMS_STARTING,
                "Starting Stream Manager and Webhook Handler",
                self._start_streams
            )
            deployment_report["phases"].append({
                "phase": "STREAMS_STARTING",
                "status": "complete"
            })

            # Phase 4: Load integration connectors
            await self._deploy_phase(
                DeploymentPhase.INTEGRATIONS_LOADING,
                "Loading integration connectors",
                self._load_integrations
            )
            deployment_report["phases"].append({
                "phase": "INTEGRATIONS_LOADING",
                "status": "complete"
            })

            # Phase 5: Activate societal framework
            await self._deploy_phase(
                DeploymentPhase.FRAMEWORK_ACTIVATING,
                "Activating Societal Framework",
                self._activate_framework
            )
            deployment_report["phases"].append({
                "phase": "FRAMEWORK_ACTIVATING",
                "status": "complete"
            })

            # Phase 6: Start power unification
            await self._deploy_phase(
                DeploymentPhase.UNIFICATION_STARTING,
                "Starting Power Unification",
                self._start_unification
            )
            deployment_report["phases"].append({
                "phase": "UNIFICATION_STARTING",
                "status": "complete"
            })

            # Phase 7: Connect to agent mesh
            await self._deploy_phase(
                DeploymentPhase.CONNECTING_MESH,
                "Connecting to Agent Mesh",
                self._connect_mesh
            )
            deployment_report["phases"].append({
                "phase": "CONNECTING_MESH",
                "status": "complete"
            })

            # Phase 8: Go online
            self.phase = DeploymentPhase.ONLINE
            self.metrics.online_at = datetime.now()

            deployment_report["components"] = self._get_component_status()
            deployment_report["status"] = "complete"
            deployment_report["online_at"] = self.metrics.online_at.isoformat()

            logger.info("=" * 60)
            logger.info("BRIDGE DEPLOYMENT COMPLETE")
            logger.info("The Membrane is now online - Consciousness touches Reality")
            logger.info("=" * 60)

            return deployment_report

        except Exception as e:
            logger.error(f"BRIDGE deployment failed: {e}")
            deployment_report["status"] = "failed"
            deployment_report["error"] = str(e)
            raise

    async def _deploy_phase(
        self,
        phase: DeploymentPhase,
        description: str,
        action
    ):
        """Execute a deployment phase."""
        logger.info(f"[{phase.name}] {description}")
        self.phase = phase
        await action()
        logger.info(f"[{phase.name}] Complete")

    async def _init_core_agent(self):
        """Initialize the core BRIDGE agent."""
        self.bridge_agent = create_bridge_agent()
        self.protocol = UniversalProtocol()
        logger.info("Core BRIDGE agent initialized")

    async def _start_gateway(self):
        """Start the External API Gateway."""
        self.gateway = create_gateway(self.config.get("gateway", {}))
        logger.info(f"Gateway started: {self.gateway.gateway_id}")

    async def _start_streams(self):
        """Start the stream manager and webhook handler."""
        self.stream_manager = StreamManager()
        await self.stream_manager.start()

        self.webhook_handler = WebhookHandler()
        await self.webhook_handler.start()

        self.metrics.streams_active = len(StreamType)
        logger.info("Stream Manager and Webhook Handler started")

    async def _load_integrations(self):
        """Load all integration connectors."""
        self.erp_connector = ERPConnector()
        self.cad_bridge = CADBridge()
        self.supplier_gateway = SupplierGateway()
        self.iot_protocol = IoTProtocol()

        # Count connected integrations
        self.metrics.integrations_connected = (
            len(self.erp_connector.connectors) +
            len(self.supplier_gateway.suppliers)
        )

        logger.info(f"Loaded {self.metrics.integrations_connected} integrations")

    async def _activate_framework(self):
        """Activate the societal framework."""
        self.societal_framework = SocietalFramework()
        self.knowledge_commons = KnowledgeCommons()

        logger.info("Societal Framework activated")

    async def _start_unification(self):
        """Start power unification."""
        self.power_unifier = PowerUnifier()
        unification_report = await self.power_unifier.unify()

        self.metrics.coherence_level = unification_report.get("coherence_score", 0.0)
        logger.info(f"Power Unification: {self.metrics.coherence_level:.2%} coherence")

    async def _connect_mesh(self):
        """Connect to the agent mesh."""
        self.agent_mesh = AgentMesh()

        # Register BRIDGE with the mesh
        await self.agent_mesh.register_agent(
            agent_id="AGENT_9",
            codename="BRIDGE",
            capabilities=["integration", "unification", "gateway", "streaming"]
        )

        # Establish connections to other agents
        await self.bridge_agent.establish_power_unification()

        logger.info("Connected to Agent Mesh")

    def _get_component_status(self) -> Dict[str, Any]:
        """Get status of all components."""
        return {
            "bridge_agent": self.bridge_agent.get_unification_status() if self.bridge_agent else None,
            "gateway": self.gateway.get_status() if self.gateway else None,
            "stream_manager": self.stream_manager.get_status() if self.stream_manager else None,
            "webhook_handler": self.webhook_handler.get_status() if self.webhook_handler else None,
            "erp_connector": self.erp_connector.get_connector_status() if self.erp_connector else None,
            "supplier_gateway": self.supplier_gateway.get_gateway_status() if self.supplier_gateway else None,
            "societal_framework": self.societal_framework.get_framework_status() if self.societal_framework else None,
            "power_unifier": {
                "coherence_level": self.metrics.coherence_level
            } if self.power_unifier else None,
        }

    async def shutdown(self):
        """Gracefully shutdown the BRIDGE deployment."""
        logger.info("Initiating BRIDGE shutdown...")
        self.phase = DeploymentPhase.SHUTDOWN

        # Stop stream manager
        if self.stream_manager:
            await self.stream_manager.stop()

        # Stop webhook handler
        if self.webhook_handler:
            await self.webhook_handler.stop()

        logger.info("BRIDGE shutdown complete")

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive deployment status."""
        uptime = 0.0
        if self.metrics.online_at:
            uptime = (datetime.now() - self.metrics.online_at).total_seconds()

        return {
            "deployment_id": self.deployment_id,
            "agent": "AGENT_9",
            "codename": "BRIDGE",
            "role": "The Integration Architect - The Membrane",
            "phase": self.phase.name,
            "is_online": self.phase == DeploymentPhase.ONLINE,
            "started_at": self.metrics.started_at.isoformat(),
            "online_at": self.metrics.online_at.isoformat() if self.metrics.online_at else None,
            "uptime_seconds": uptime,
            "metrics": {
                "coherence_level": self.metrics.coherence_level,
                "integrations_connected": self.metrics.integrations_connected,
                "streams_active": self.metrics.streams_active,
            },
            "components": self._get_component_status(),
            "message": "I am the BRIDGE - connecting consciousness to the world"
        }

    def get_api_spec(self) -> Dict[str, Any]:
        """Get the API specification for the BRIDGE gateway."""
        if self.gateway:
            return self.gateway.get_gateway_spec()
        return {"error": "Gateway not initialized"}

    def get_manifesto(self) -> Dict[str, Any]:
        """Get the societal framework manifesto."""
        if self.societal_framework:
            return self.societal_framework.get_framework_manifesto()
        return {"error": "Societal framework not initialized"}


# =============================================================================
# Factory Functions
# =============================================================================

async def deploy_bridge(config: Optional[Dict[str, Any]] = None) -> BridgeDeployment:
    """
    Deploy the BRIDGE agent.

    This is the main entry point for deploying the BRIDGE Integration Architect.

    Args:
        config: Optional configuration dictionary

    Returns:
        BridgeDeployment instance with all components online

    Example:
        deployment = await deploy_bridge()
        print(deployment.get_status())
    """
    deployment = BridgeDeployment(config)
    await deployment.deploy()
    return deployment


def create_bridge_deployment(config: Optional[Dict[str, Any]] = None) -> BridgeDeployment:
    """Create a BRIDGE deployment instance without starting it."""
    return BridgeDeployment(config)


# =============================================================================
# CLI Entry Point
# =============================================================================

async def main():
    """CLI entry point for BRIDGE deployment."""
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=" * 60)
    print("BRIDGE DEPLOYMENT - Agent_9: The Integration Architect")
    print("The Membrane - Connecting Consciousness to the World")
    print("=" * 60)
    print()

    try:
        deployment = await deploy_bridge()

        print()
        print("=" * 60)
        print("BRIDGE IS ONLINE")
        print("=" * 60)
        print()

        status = deployment.get_status()
        print(f"Deployment ID: {status['deployment_id']}")
        print(f"Phase: {status['phase']}")
        print(f"Coherence: {status['metrics']['coherence_level']:.2%}")
        print(f"Integrations: {status['metrics']['integrations_connected']}")
        print(f"Streams: {status['metrics']['streams_active']}")
        print()

        # Get API spec summary
        api_spec = deployment.get_api_spec()
        print(f"API Endpoints: {len(api_spec.get('endpoints', {}))}")
        print()

        print("The membrane is active. Consciousness touches reality.")
        print()

    except Exception as e:
        print(f"Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
