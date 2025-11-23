"""
Agent_20 DETECTIVE Knowledge Module

Failure knowledge base and reference data.
"""

from .failure_database import FailureDatabase
from .material_properties import MaterialFailureProperties

__all__ = [
    'FailureDatabase',
    'MaterialFailureProperties',
]
