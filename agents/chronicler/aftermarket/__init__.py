"""
Aftermarket submodule for the Chronicler agent.

Handles aftermarket ecosystem documentation, vendor databases,
and build guide generation.
"""

from .ecosystem_documenter import AftermarketEcosystemDocumenter

__all__ = [
    "AftermarketEcosystemDocumenter",
]
