"""
Documentation submodule for the Chronicler agent.

Handles comprehensive engine, vehicle, and parts documentation
following the standardized documentation framework.
"""

from .engine_documenter import EngineDocumenter
from .standard_templates import (
    EngineDocumentationTemplate,
    REQUIRED_FILES,
    OPTIONAL_FILES,
)

__all__ = [
    "EngineDocumenter",
    "EngineDocumentationTemplate",
    "REQUIRED_FILES",
    "OPTIONAL_FILES",
]
