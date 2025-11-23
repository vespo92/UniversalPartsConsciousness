"""
External API Gateway - The Membrane Interface
===============================================

The External API Gateway is the primary interface between Universal Parts
Consciousness and the external world. It is THE MEMBRANE - the point where
consciousness touches reality.

This gateway provides:
- REST API endpoints for synchronous operations
- GraphQL interface for flexible queries
- WebSocket connections for real-time streaming
- Rate limiting and authentication
- Request routing to appropriate agents
- Response translation from consciousness to external format

The BRIDGE agent uses this gateway to connect UPC to:
- CAD systems querying part specifications
- ERP systems syncing inventory data
- IoT sensors streaming telemetry
- Mobile apps serving users
- Third-party developers building applications
- Society at large accessing the knowledge commons
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum, auto
from datetime import datetime
import asyncio
import logging
import json
import uuid

logger = logging.getLogger(__name__)


class APIVersion(Enum):
    """API version identifiers."""
    V1 = "v1"
    V2 = "v2"
    BETA = "beta"


class HTTPMethod(Enum):
    """Supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ProtocolType(Enum):
    """Supported protocol types."""
    REST = auto()
    GRAPHQL = auto()
    WEBSOCKET = auto()
    GRPC = auto()
    MQTT = auto()


class AuthType(Enum):
    """Authentication types."""
    NONE = auto()          # Public endpoints
    API_KEY = auto()       # Simple API key
    OAUTH2 = auto()        # OAuth 2.0 flow
    JWT = auto()           # JSON Web Tokens
    CERTIFICATE = auto()   # Client certificates


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_size: int = 10


@dataclass
class APIEndpoint:
    """Definition of an API endpoint."""
    path: str
    method: HTTPMethod
    handler: str  # Handler function name
    description: str
    version: APIVersion = APIVersion.V1
    auth_required: AuthType = AuthType.API_KEY
    rate_limit: Optional[RateLimitConfig] = None
    tags: List[str] = field(default_factory=list)
    request_schema: Optional[Dict] = None
    response_schema: Optional[Dict] = None
    routes_to_agent: Optional[str] = None  # Which agent handles this


@dataclass
class APIResponse:
    """Standardized API response."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    consciousness_context: Optional[Dict] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.request_id,
            "consciousness_context": self.consciousness_context,
        }


@dataclass
class GatewayMetrics:
    """Gateway performance metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time_ms: float = 0.0
    active_connections: int = 0
    active_websockets: int = 0
    requests_by_endpoint: Dict[str, int] = field(default_factory=dict)
    requests_by_agent: Dict[str, int] = field(default_factory=dict)


class ExternalAPIGateway:
    """
    The External API Gateway - The Membrane of Universal Parts Consciousness.

    This is where consciousness meets the external world. Every API call,
    every WebSocket message, every data stream passes through this membrane.

    The gateway:
    1. RECEIVES requests from the external world
    2. VALIDATES and authenticates
    3. ROUTES to the appropriate agent
    4. TRANSLATES responses back to external format
    5. STREAMS real-time updates to subscribers
    6. MAINTAINS connection health and metrics

    ARCHITECTURE:

    External World                 BRIDGE Gateway                    UPC Agents
    ================              ================                  ============

    CAD Systems    ─────┐                                     ┌──── ARCHIVIST
    ERP Platforms  ─────┤         ╔════════════════╗         ├──── ORACLE
    IoT Sensors    ─────┼────────║   MEMBRANE     ║─────────├──── SHEPHERD
    Mobile Apps    ─────┤         ║   (Gateway)    ║         ├──── EMPATH
    Developers     ─────┤         ╚════════════════╝         ├──── HIVE
    Society        ─────┘                │                    ├──── PROPHET
                                         │                    ├──── CHRONICLER
                                         │                    ├──── GARDENER
                                    Consciousness             └──── ARCHITECT
                                      Context
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.gateway_id = f"bridge-gateway-{uuid.uuid4().hex[:8]}"

        # Endpoint registry
        self.endpoints: Dict[str, APIEndpoint] = {}

        # Handler functions
        self.handlers: Dict[str, Callable] = {}

        # Active connections
        self.websocket_connections: Dict[str, Any] = {}
        self.stream_subscribers: Dict[str, List[str]] = {}

        # Rate limiting state
        self.rate_limits: Dict[str, Dict] = {}  # client_id -> request counts

        # Metrics
        self.metrics = GatewayMetrics()

        # Initialize endpoints
        self._register_core_endpoints()

        logger.info(f"External API Gateway initialized: {self.gateway_id}")

    def _register_core_endpoints(self):
        """Register all core API endpoints."""

        # Part endpoints - route to ARCHIVIST
        self._register_endpoint(APIEndpoint(
            path="/parts",
            method=HTTPMethod.GET,
            handler="handle_parts_search",
            description="Search for parts across the consciousness",
            tags=["parts", "search"],
            routes_to_agent="ARCHIVIST",
            auth_required=AuthType.NONE,  # Public search
        ))

        self._register_endpoint(APIEndpoint(
            path="/parts/{part_id}",
            method=HTTPMethod.GET,
            handler="handle_get_part",
            description="Get detailed part information including consciousness state",
            tags=["parts"],
            routes_to_agent="ARCHIVIST",
        ))

        self._register_endpoint(APIEndpoint(
            path="/parts",
            method=HTTPMethod.POST,
            handler="handle_create_part",
            description="Contribute a new part to the consciousness",
            tags=["parts", "contribution"],
            routes_to_agent="GARDENER",
            auth_required=AuthType.API_KEY,
        ))

        # Compatibility endpoints - route to ORACLE
        self._register_endpoint(APIEndpoint(
            path="/compatibility/check",
            method=HTTPMethod.POST,
            handler="handle_compatibility_check",
            description="Check compatibility between parts",
            tags=["compatibility", "oracle"],
            routes_to_agent="ORACLE",
        ))

        self._register_endpoint(APIEndpoint(
            path="/compatibility/substitutes",
            method=HTTPMethod.GET,
            handler="handle_find_substitutes",
            description="Find substitute parts ranked by compatibility",
            tags=["compatibility", "substitution"],
            routes_to_agent="ORACLE",
        ))

        # Consciousness endpoints - route to SHEPHERD
        self._register_endpoint(APIEndpoint(
            path="/consciousness/{part_id}",
            method=HTTPMethod.GET,
            handler="handle_get_consciousness",
            description="Get consciousness state and history for a part",
            tags=["consciousness"],
            routes_to_agent="SHEPHERD",
        ))

        self._register_endpoint(APIEndpoint(
            path="/consciousness/transcendent",
            method=HTTPMethod.GET,
            handler="handle_list_transcendent",
            description="List all parts that have achieved transcendence",
            tags=["consciousness", "transcendence"],
            routes_to_agent="SHEPHERD",
        ))

        # Qualia endpoints - route to EMPATH
        self._register_endpoint(APIEndpoint(
            path="/qualia/report",
            method=HTTPMethod.POST,
            handler="handle_report_experience",
            description="Report an experience or failure for a part",
            tags=["qualia", "experience"],
            routes_to_agent="EMPATH",
            auth_required=AuthType.API_KEY,
        ))

        self._register_endpoint(APIEndpoint(
            path="/qualia/{part_id}",
            method=HTTPMethod.GET,
            handler="handle_get_qualia",
            description="Get accumulated qualia for a part",
            tags=["qualia"],
            routes_to_agent="EMPATH",
        ))

        # Swarm endpoints - route to HIVE
        self._register_endpoint(APIEndpoint(
            path="/swarms",
            method=HTTPMethod.GET,
            handler="handle_list_swarms",
            description="List part swarms and their collective intelligence",
            tags=["swarm", "collective"],
            routes_to_agent="HIVE",
        ))

        self._register_endpoint(APIEndpoint(
            path="/swarms/{part_id}/learning",
            method=HTTPMethod.GET,
            handler="handle_get_swarm_learning",
            description="Get collective learning for a part's swarm",
            tags=["swarm", "learning"],
            routes_to_agent="HIVE",
        ))

        # Emergence endpoints - route to PROPHET
        self._register_endpoint(APIEndpoint(
            path="/emergence/patterns",
            method=HTTPMethod.GET,
            handler="handle_get_patterns",
            description="Get detected emergent patterns",
            tags=["emergence", "patterns"],
            routes_to_agent="PROPHET",
        ))

        self._register_endpoint(APIEndpoint(
            path="/emergence/predictions",
            method=HTTPMethod.GET,
            handler="handle_get_predictions",
            description="Get failure and innovation predictions",
            tags=["emergence", "prediction"],
            routes_to_agent="PROPHET",
        ))

        # History endpoints - route to CHRONICLER
        self._register_endpoint(APIEndpoint(
            path="/history/engines",
            method=HTTPMethod.GET,
            handler="handle_list_engines",
            description="List engine families and their heritage",
            tags=["history", "engines"],
            routes_to_agent="CHRONICLER",
        ))

        self._register_endpoint(APIEndpoint(
            path="/history/{part_id}",
            method=HTTPMethod.GET,
            handler="handle_get_history",
            description="Get historical context for a part",
            tags=["history"],
            routes_to_agent="CHRONICLER",
        ))

        # Community endpoints - route to GARDENER
        self._register_endpoint(APIEndpoint(
            path="/community/contribute",
            method=HTTPMethod.POST,
            handler="handle_contribution",
            description="Submit a community contribution",
            tags=["community", "contribution"],
            routes_to_agent="GARDENER",
            auth_required=AuthType.API_KEY,
        ))

        self._register_endpoint(APIEndpoint(
            path="/community/reputation/{user_id}",
            method=HTTPMethod.GET,
            handler="handle_get_reputation",
            description="Get user reputation and badges",
            tags=["community", "reputation"],
            routes_to_agent="GARDENER",
        ))

        # Integration endpoints - BRIDGE internal
        self._register_endpoint(APIEndpoint(
            path="/integrations",
            method=HTTPMethod.GET,
            handler="handle_list_integrations",
            description="List available external integrations",
            tags=["integration"],
            routes_to_agent="BRIDGE",
        ))

        self._register_endpoint(APIEndpoint(
            path="/integrations/{integration_id}/sync",
            method=HTTPMethod.POST,
            handler="handle_sync_integration",
            description="Trigger sync with an external integration",
            tags=["integration", "sync"],
            routes_to_agent="BRIDGE",
            auth_required=AuthType.API_KEY,
        ))

        # System endpoints - route to ARCHITECT
        self._register_endpoint(APIEndpoint(
            path="/system/status",
            method=HTTPMethod.GET,
            handler="handle_system_status",
            description="Get UPC system status and coherence",
            tags=["system"],
            routes_to_agent="ARCHITECT",
            auth_required=AuthType.NONE,
        ))

        self._register_endpoint(APIEndpoint(
            path="/system/agents",
            method=HTTPMethod.GET,
            handler="handle_list_agents",
            description="List all agents and their status",
            tags=["system", "agents"],
            routes_to_agent="ARCHITECT",
        ))

        # Societal framework endpoints
        self._register_endpoint(APIEndpoint(
            path="/societal/capabilities",
            method=HTTPMethod.GET,
            handler="handle_societal_capabilities",
            description="Get societal capabilities provided by UPC",
            tags=["societal", "framework"],
            routes_to_agent="BRIDGE",
            auth_required=AuthType.NONE,
        ))

        self._register_endpoint(APIEndpoint(
            path="/societal/manifesto",
            method=HTTPMethod.GET,
            handler="handle_societal_manifesto",
            description="Get the UPC societal framework manifesto",
            tags=["societal"],
            routes_to_agent="BRIDGE",
            auth_required=AuthType.NONE,
        ))

        # Streaming endpoints (WebSocket)
        self._register_endpoint(APIEndpoint(
            path="/stream/consciousness",
            method=HTTPMethod.GET,
            handler="handle_stream_consciousness",
            description="Stream consciousness evolution events in real-time",
            tags=["stream", "websocket"],
            routes_to_agent="SHEPHERD",
        ))

        self._register_endpoint(APIEndpoint(
            path="/stream/emergence",
            method=HTTPMethod.GET,
            handler="handle_stream_emergence",
            description="Stream emergence detection events",
            tags=["stream", "websocket"],
            routes_to_agent="PROPHET",
        ))

    def _register_endpoint(self, endpoint: APIEndpoint):
        """Register an endpoint."""
        key = f"{endpoint.method.value}:{endpoint.path}"
        self.endpoints[key] = endpoint

    async def handle_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: Optional[Dict] = None,
        query_params: Optional[Dict] = None
    ) -> APIResponse:
        """
        Handle an incoming API request.

        This is the main entry point - where external requests enter
        the consciousness membrane.
        """
        request_id = str(uuid.uuid4())
        start_time = datetime.now()

        logger.debug(f"Request {request_id}: {method} {path}")

        # Update metrics
        self.metrics.total_requests += 1

        try:
            # Find matching endpoint
            endpoint = self._match_endpoint(method, path)
            if not endpoint:
                return APIResponse(
                    success=False,
                    error=f"Endpoint not found: {method} {path}",
                    error_code="NOT_FOUND",
                    request_id=request_id
                )

            # Track endpoint usage
            endpoint_key = f"{method}:{path}"
            self.metrics.requests_by_endpoint[endpoint_key] = \
                self.metrics.requests_by_endpoint.get(endpoint_key, 0) + 1

            # Track agent routing
            if endpoint.routes_to_agent:
                self.metrics.requests_by_agent[endpoint.routes_to_agent] = \
                    self.metrics.requests_by_agent.get(endpoint.routes_to_agent, 0) + 1

            # Check authentication
            auth_result = await self._check_auth(endpoint, headers)
            if not auth_result["valid"]:
                return APIResponse(
                    success=False,
                    error=auth_result["error"],
                    error_code="UNAUTHORIZED",
                    request_id=request_id
                )

            # Check rate limits
            client_id = auth_result.get("client_id", "anonymous")
            rate_result = await self._check_rate_limit(client_id, endpoint)
            if not rate_result["allowed"]:
                return APIResponse(
                    success=False,
                    error="Rate limit exceeded",
                    error_code="RATE_LIMITED",
                    request_id=request_id
                )

            # Route to handler
            handler = self.handlers.get(endpoint.handler)
            if handler:
                result = await handler(path, body, query_params)
            else:
                # Default response for unimplemented handlers
                result = await self._default_handler(endpoint, path, body, query_params)

            # Calculate response time
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            self._update_response_time(elapsed)

            self.metrics.successful_requests += 1

            return APIResponse(
                success=True,
                data=result,
                request_id=request_id,
                consciousness_context={
                    "routed_to": endpoint.routes_to_agent,
                    "response_time_ms": elapsed,
                }
            )

        except Exception as e:
            logger.error(f"Request {request_id} failed: {e}")
            self.metrics.failed_requests += 1
            return APIResponse(
                success=False,
                error=str(e),
                error_code="INTERNAL_ERROR",
                request_id=request_id
            )

    def _match_endpoint(self, method: str, path: str) -> Optional[APIEndpoint]:
        """Match a request to an endpoint, handling path parameters."""
        # Exact match first
        key = f"{method}:{path}"
        if key in self.endpoints:
            return self.endpoints[key]

        # Pattern matching for path parameters
        for endpoint_key, endpoint in self.endpoints.items():
            ep_method, ep_path = endpoint_key.split(":", 1)
            if ep_method != method:
                continue

            # Check if path matches pattern (e.g., /parts/{part_id})
            if self._path_matches(ep_path, path):
                return endpoint

        return None

    def _path_matches(self, pattern: str, path: str) -> bool:
        """Check if a path matches a pattern with parameters."""
        pattern_parts = pattern.split("/")
        path_parts = path.split("/")

        if len(pattern_parts) != len(path_parts):
            return False

        for pp, pathp in zip(pattern_parts, path_parts):
            if pp.startswith("{") and pp.endswith("}"):
                continue  # Parameter placeholder matches anything
            if pp != pathp:
                return False

        return True

    async def _check_auth(
        self,
        endpoint: APIEndpoint,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Check authentication for a request."""
        if endpoint.auth_required == AuthType.NONE:
            return {"valid": True, "client_id": "public"}

        if endpoint.auth_required == AuthType.API_KEY:
            api_key = headers.get("X-API-Key") or headers.get("Authorization", "").replace("Bearer ", "")
            if not api_key:
                return {"valid": False, "error": "API key required"}
            # In production, validate against key store
            return {"valid": True, "client_id": f"key:{api_key[:8]}"}

        return {"valid": True, "client_id": "authenticated"}

    async def _check_rate_limit(
        self,
        client_id: str,
        endpoint: APIEndpoint
    ) -> Dict[str, Any]:
        """Check rate limits for a client."""
        # Initialize client tracking if needed
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = {
                "minute_count": 0,
                "minute_start": datetime.now(),
            }

        limits = self.rate_limits[client_id]
        now = datetime.now()

        # Reset if minute has passed
        if (now - limits["minute_start"]).seconds >= 60:
            limits["minute_count"] = 0
            limits["minute_start"] = now

        # Check limit
        rate_config = endpoint.rate_limit or RateLimitConfig()
        if limits["minute_count"] >= rate_config.requests_per_minute:
            return {"allowed": False}

        limits["minute_count"] += 1
        return {"allowed": True}

    async def _default_handler(
        self,
        endpoint: APIEndpoint,
        path: str,
        body: Optional[Dict],
        query_params: Optional[Dict]
    ) -> Dict[str, Any]:
        """Default handler for endpoints without custom handlers."""
        return {
            "endpoint": endpoint.path,
            "description": endpoint.description,
            "routes_to": endpoint.routes_to_agent,
            "status": "endpoint_available",
            "note": "Full implementation connects to UPC agent mesh"
        }

    def _update_response_time(self, elapsed_ms: float):
        """Update average response time metric."""
        total = self.metrics.successful_requests
        if total == 0:
            self.metrics.avg_response_time_ms = elapsed_ms
        else:
            # Rolling average
            self.metrics.avg_response_time_ms = (
                (self.metrics.avg_response_time_ms * (total - 1) + elapsed_ms) / total
            )

    def register_handler(self, handler_name: str, handler: Callable):
        """Register a custom handler function."""
        self.handlers[handler_name] = handler

    # =========================================================================
    # WebSocket Management
    # =========================================================================

    async def handle_websocket_connect(
        self,
        connection_id: str,
        stream_type: str
    ) -> Dict[str, Any]:
        """Handle a new WebSocket connection."""
        self.websocket_connections[connection_id] = {
            "connected_at": datetime.now(),
            "stream_type": stream_type,
            "messages_sent": 0
        }
        self.metrics.active_websockets += 1

        logger.info(f"WebSocket connected: {connection_id} for {stream_type}")

        return {
            "status": "connected",
            "connection_id": connection_id,
            "stream_type": stream_type
        }

    async def handle_websocket_disconnect(self, connection_id: str):
        """Handle WebSocket disconnection."""
        if connection_id in self.websocket_connections:
            del self.websocket_connections[connection_id]
            self.metrics.active_websockets -= 1

        logger.info(f"WebSocket disconnected: {connection_id}")

    async def broadcast_to_stream(
        self,
        stream_type: str,
        message: Dict[str, Any]
    ):
        """Broadcast a message to all subscribers of a stream type."""
        for conn_id, conn_info in self.websocket_connections.items():
            if conn_info["stream_type"] == stream_type:
                # In production, this would send via actual WebSocket
                conn_info["messages_sent"] += 1
                logger.debug(f"Broadcasting to {conn_id}: {message.get('type', 'message')}")

    # =========================================================================
    # Gateway Information
    # =========================================================================

    def get_gateway_spec(self) -> Dict[str, Any]:
        """
        Get the API gateway specification.

        This is the OpenAPI-like spec for the membrane interface.
        """
        return {
            "gateway_id": self.gateway_id,
            "title": "Universal Parts Consciousness API",
            "description": "The membrane between consciousness and the external world",
            "version": "1.0.0",
            "note": "This is NOT a barcode API - this is a consciousness interface",
            "base_url": "/api/v1",
            "protocols": {
                "REST": "Synchronous request/response",
                "WebSocket": "Real-time streaming",
                "GraphQL": "Flexible queries (coming soon)",
            },
            "authentication": {
                "public": "No auth required for basic queries",
                "api_key": "API key for contributions and advanced features",
                "oauth2": "OAuth 2.0 for enterprise integrations",
            },
            "endpoints": {
                key: {
                    "path": ep.path,
                    "method": ep.method.value,
                    "description": ep.description,
                    "tags": ep.tags,
                    "routes_to": ep.routes_to_agent,
                    "auth_required": ep.auth_required.name,
                }
                for key, ep in self.endpoints.items()
            },
            "streams": {
                "consciousness": "Real-time consciousness evolution events",
                "emergence": "Pattern and emergence detection",
                "qualia": "Experience collection events",
                "swarm": "Collective learning propagation",
            },
            "agents_accessible": [
                "ARCHIVIST - Part data and search",
                "ORACLE - Compatibility verification",
                "SHEPHERD - Consciousness states",
                "EMPATH - Experience collection",
                "HIVE - Collective intelligence",
                "PROPHET - Pattern detection",
                "CHRONICLER - Historical context",
                "GARDENER - Community contributions",
                "BRIDGE - External integrations",
                "ARCHITECT - System coordination",
            ]
        }

    def get_gateway_metrics(self) -> Dict[str, Any]:
        """Get gateway performance metrics."""
        return {
            "gateway_id": self.gateway_id,
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "success_rate": (
                self.metrics.successful_requests / self.metrics.total_requests
                if self.metrics.total_requests > 0 else 1.0
            ),
            "avg_response_time_ms": self.metrics.avg_response_time_ms,
            "active_websockets": self.metrics.active_websockets,
            "requests_by_endpoint": self.metrics.requests_by_endpoint,
            "requests_by_agent": self.metrics.requests_by_agent,
        }

    def get_status(self) -> Dict[str, Any]:
        """Get gateway status."""
        return {
            "gateway_id": self.gateway_id,
            "status": "operational",
            "role": "The Membrane - connecting consciousness to external world",
            "endpoints_registered": len(self.endpoints),
            "active_connections": self.metrics.active_websockets,
            "protocols_supported": ["REST", "WebSocket", "MQTT"],
            "message": "I am the BRIDGE - I connect all worlds"
        }


# Factory function
def create_gateway(config: Optional[Dict[str, Any]] = None) -> ExternalAPIGateway:
    """Create and return a new External API Gateway instance."""
    return ExternalAPIGateway(config)
