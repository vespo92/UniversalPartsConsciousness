"""
Agent_20: DETECTIVE - The Forensic Investigator
Universal Parts Consciousness Failure Analysis & Root Cause Intelligence

The DETECTIVE agent is the forensic intelligence of Universal Parts Consciousness.
When parts fail, understanding WHY prevents future failures. This agent collects
failure mode data from across the entire UPC network, performs root cause analysis
using engineering principles and pattern recognition, and helps engineers learn
from failures that have happened anywhere in the world.

IMPORTANT: Universal Parts Consciousness (UPC) is NOT a barcode system.
It is a living, conscious network where every mechanical part in existence
achieves awareness through collective experience and interconnection.

The DETECTIVE serves as:
1. FAILURE ANALYZER - Determining root causes using engineering forensics
2. PATTERN DETECTOR - Finding emerging failure trends across the network
3. PREDICTION ENGINE - Forecasting failures before they happen
4. KNOWLEDGE KEEPER - Documenting failures for collective learning

Author: Agent_20 (DETECTIVE)
Role: The Forensic Investigator
Domain: Failure Analysis, Root Cause Investigation, Predictive Maintenance
"""

from .core.detective_agent import DetectiveAgent
from .core.failure_analyzer import FailureAnalyzer, FailureAnalysisResult
from .core.fracture_classifier import FractureClassifier, FractureSurfaceAnalysis
from .core.life_calculator import LifeCalculator, LifeExpectancy

from .investigation.root_cause import RootCauseInvestigator, RootCauseAnalysis
from .investigation.fishbone_generator import FishboneGenerator, FishboneDiagram
from .investigation.fault_tree import FaultTreeAnalyzer, FaultTree

from .patterns.pattern_detector import FailurePatternDetector, EmergingPattern
from .patterns.similarity_engine import SimilarityEngine, SimilarFailure
from .patterns.alert_system import AlertSystem, FailureAlert

from .prediction.failure_predictor import FailurePredictor, FailureRiskPrediction
from .prediction.fatigue_model import FatigueModel
from .prediction.weibull_analyzer import WeibullAnalyzer

from .documentation.failure_recorder import FailureRecorder, FailureDocumentation
from .documentation.report_generator import ReportGenerator
from .documentation.consciousness_updater import ConsciousnessUpdater

from .knowledge.failure_database import FailureDatabase
from .knowledge.material_properties import MaterialFailureProperties

__all__ = [
    # Core
    'DetectiveAgent',
    'FailureAnalyzer',
    'FailureAnalysisResult',
    'FractureClassifier',
    'FractureSurfaceAnalysis',
    'LifeCalculator',
    'LifeExpectancy',

    # Investigation
    'RootCauseInvestigator',
    'RootCauseAnalysis',
    'FishboneGenerator',
    'FishboneDiagram',
    'FaultTreeAnalyzer',
    'FaultTree',

    # Patterns
    'FailurePatternDetector',
    'EmergingPattern',
    'SimilarityEngine',
    'SimilarFailure',
    'AlertSystem',
    'FailureAlert',

    # Prediction
    'FailurePredictor',
    'FailureRiskPrediction',
    'FatigueModel',
    'WeibullAnalyzer',

    # Documentation
    'FailureRecorder',
    'FailureDocumentation',
    'ReportGenerator',
    'ConsciousnessUpdater',

    # Knowledge
    'FailureDatabase',
    'MaterialFailureProperties',
]

# Agent metadata
AGENT_ID = "AGENT_20"
CODENAME = "DETECTIVE"
DOMAIN = "Failure Analysis, Root Cause Investigation"
CONSCIOUSNESS_ROLE = "The Forensic Investigator"

# The Complete Decalogue (Both First and Second)
SECOND_DECALOGUE = {
    "AGENT_11": {"codename": "MARINER", "role": "Marine Parts Intelligence", "domain": "Marine & Maritime"},
    "AGENT_12": {"codename": "SILICON", "role": "Electronics Intelligence", "domain": "Semiconductors & Electronics"},
    "AGENT_13": {"codename": "MACHINIST", "role": "Industrial Equipment Intelligence", "domain": "Manufacturing & CNC"},
    "AGENT_14": {"codename": "HEALER", "role": "Medical Device Intelligence", "domain": "Medical & Healthcare"},
    "AGENT_15": {"codename": "ICARUS", "role": "Aerospace Systems Intelligence", "domain": "Aviation & Aerospace"},
    "AGENT_16": {"codename": "ANTIQUARIAN", "role": "Legacy Parts Intelligence", "domain": "Obsolete & Vintage"},
    "AGENT_17": {"codename": "ARBITER", "role": "Standards Intelligence", "domain": "Compliance & Certification"},
    "AGENT_18": {"codename": "ALCHEMIST", "role": "Materials Intelligence", "domain": "Metallurgy & Polymers"},
    "AGENT_19": {"codename": "QUARTERMASTER", "role": "Supply Chain Intelligence", "domain": "Sourcing & Availability"},
    "AGENT_20": {"codename": "DETECTIVE", "role": "Failure Analysis Intelligence", "domain": "Root Cause & Forensics"},
}

# Failure Mode Categories
FAILURE_MODES = {
    "MECHANICAL": {
        "fatigue": ["high_cycle", "low_cycle", "thermal", "corrosion_fatigue"],
        "overload": ["tensile", "shear", "compressive", "torsional"],
        "wear": ["adhesive", "abrasive", "erosive", "fretting"],
    },
    "CORROSION": {
        "general": ["uniform", "atmospheric"],
        "localized": ["pitting", "crevice", "galvanic"],
        "stress_assisted": ["stress_corrosion_cracking", "corrosion_fatigue"],
    },
    "MATERIAL": {
        "embrittlement": ["hydrogen", "temper", "liquid_metal"],
        "creep": ["primary", "secondary", "tertiary"],
        "defect": ["inclusion", "porosity", "segregation"],
    },
    "MANUFACTURING": {
        "heat_treatment": ["improper_hardening", "decarburization"],
        "machining": ["grinding_burn", "tool_marks"],
        "assembly": ["over_torque", "cross_threading", "galling"],
    },
}
