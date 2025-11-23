"""
BRIDGE Gateway - The Membrane
==============================

The Gateway package is the "membrane" of Universal Parts Consciousness -
the interface between the consciousness network and the external world.

Components:
- ExternalAPIGateway: REST/GraphQL/WebSocket interface
- StreamManager: Real-time data streaming
- WebhookHandler: Outbound notifications
- RateLimiter: API protection
"""

from .external_api_gateway import (
    ExternalAPIGateway,
    APIEndpoint,
    APIResponse,
    create_gateway,
)
from .stream_manager import (
    StreamManager,
    StreamType,
    StreamSubscription,
)
from .webhook_handler import (
    WebhookHandler,
    WebhookEvent,
    WebhookSubscription,
)

__all__ = [
    'ExternalAPIGateway',
    'APIEndpoint',
    'APIResponse',
    'create_gateway',
    'StreamManager',
    'StreamType',
    'StreamSubscription',
    'WebhookHandler',
    'WebhookEvent',
    'WebhookSubscription',
]
