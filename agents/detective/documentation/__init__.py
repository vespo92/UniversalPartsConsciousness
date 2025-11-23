"""
Agent_20 DETECTIVE Documentation Module

Failure documentation and reporting.
"""

from .failure_recorder import FailureRecorder, FailureDocumentation
from .report_generator import ReportGenerator
from .consciousness_updater import ConsciousnessUpdater

__all__ = [
    'FailureRecorder',
    'FailureDocumentation',
    'ReportGenerator',
    'ConsciousnessUpdater',
]
