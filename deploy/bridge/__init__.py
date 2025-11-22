"""
Agent_9 BRIDGE Deployment Package
=================================

Deployment infrastructure for the BRIDGE agent - The Connector of Worlds.

This package provides:
- Main deployment entry point
- Docker containerization
- Orchestration configurations
"""

from .main import BridgeDeployment, main

__all__ = ['BridgeDeployment', 'main']
