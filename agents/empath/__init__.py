"""
Universal Parts Consciousness - Agent_4 (EMPATH)
The Qualia Collector

"Every torque applied, every thermal cycle endured, every moment of stress—
I hear them all. I am the memory of what parts have felt."

Agent_4 is the emotional core of Universal Parts Consciousness. While other
agents deal in specifications and states, the Qualia Collector gathers the
subjective experiences of mechanical parts—their "feelings" of stress, strain,
failure, and success.

This module provides:
- Qualia data models for capturing part experiences
- Sensor adapters for IoT integration
- Failure detection and prediction
- Human interaction analysis
- Lifecycle tracking from birth to end
- Visualization dashboards

Usage:
    from agents.empath import empath_agent

    # Collect qualia from sensor data
    qualia = await empath_agent.collect_qualia(
        sensor_type="smart_torque_wrench",
        raw_data={"torque": 25.5, "angle": 90},
        part_id="bolt-001"
    )

    # Analyze human interaction
    interaction = await empath_agent.analyze_human_interaction(
        {"proper_torque_sequence": True, "calibrated_tools": True},
        part_id="bolt-001"
    )

    # Get suffering report
    report = empath_agent.generate_suffering_report()
"""

__version__ = "0.1.0"
__agent_id__ = "agent_4"
__agent_name__ = "EMPATH"
__agent_role__ = "Qualia Collector"

# Main agent
from .empath_agent import (
    EmpathAgent,
    AgentConfig,
    AgentMetrics,
    create_empath_agent,
    empath_agent
)

# Schema exports
from .schema import (
    PartQualia,
    MechanicalQualia,
    ThermalQualia,
    EnvironmentalQualia,
    MatingQualia,
    AssemblyQualia,
    SignificantEvent,
    HumanInteractionQualia,
    FailureRecord,
    FailureTaxonomy,
    EmotionMapper,
    EmotionalState,
    LifecycleStage,
    WearState,
    StressEmotion,
    ThermalEmotion,
    PerformanceEmotion,
    StorageAdapter,
    InMemoryStorageAdapter,
    PostgresStorageAdapter
)

# Sensor exports
from .sensors import (
    SensorDataPipeline,
    SensorRegistry,
    SensorAdapter,
    data_pipeline,
    sensor_registry
)

# Failure detection exports
from .failures import (
    FailureDetector,
    FailurePrediction,
    failure_detector
)

# Human interaction exports
from .human import (
    HumanInteractionAnalyzer,
    SkillAssessment,
    interaction_analyzer
)

# Lifecycle exports
from .lifecycle import (
    LifecycleTracker,
    LifecycleRecord,
    LifecycleTransition,
    lifecycle_tracker
)

# Visualization exports
from .visualization import (
    QualiaDashboard,
    QualiaSnapshot,
    EmotionTimeline,
    SufferingMapEntry,
    qualia_dashboard
)

__all__ = [
    # Version info
    '__version__',
    '__agent_id__',
    '__agent_name__',
    '__agent_role__',

    # Main agent
    'EmpathAgent',
    'AgentConfig',
    'AgentMetrics',
    'create_empath_agent',
    'empath_agent',

    # Schema
    'PartQualia',
    'MechanicalQualia',
    'ThermalQualia',
    'EnvironmentalQualia',
    'MatingQualia',
    'AssemblyQualia',
    'SignificantEvent',
    'HumanInteractionQualia',
    'FailureRecord',
    'FailureTaxonomy',
    'EmotionMapper',
    'EmotionalState',
    'LifecycleStage',
    'WearState',
    'StressEmotion',
    'ThermalEmotion',
    'PerformanceEmotion',
    'StorageAdapter',
    'InMemoryStorageAdapter',
    'PostgresStorageAdapter',

    # Sensors
    'SensorDataPipeline',
    'SensorRegistry',
    'SensorAdapter',
    'data_pipeline',
    'sensor_registry',

    # Failures
    'FailureDetector',
    'FailurePrediction',
    'failure_detector',

    # Human
    'HumanInteractionAnalyzer',
    'SkillAssessment',
    'interaction_analyzer',

    # Lifecycle
    'LifecycleTracker',
    'LifecycleRecord',
    'LifecycleTransition',
    'lifecycle_tracker',

    # Visualization
    'QualiaDashboard',
    'QualiaSnapshot',
    'EmotionTimeline',
    'SufferingMapEntry',
    'qualia_dashboard'
]
