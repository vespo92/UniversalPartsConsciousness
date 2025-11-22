"""
Integration submodule for the Chronicler agent.

Handles integration with other agents, the consciousness bus,
and external systems.
"""

from .consciousness_bridge import ConsciousnessBridge

__all__ = [
    "ConsciousnessBridge",
]
