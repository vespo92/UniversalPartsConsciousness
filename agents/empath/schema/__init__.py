"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Schema Module - Core data structures for qualia processing
"""

from .qualia_models import (
    PartQualia,
    MechanicalQualia,
    ThermalQualia,
    EnvironmentalQualia,
    MatingQualia,
    AssemblyQualia,
    SignificantEvent,
    HumanInteractionQualia,
    TorqueEvent,
    LifecycleStage,
    WearState,
    StressEmotion,
    ThermalEmotion,
    PerformanceEmotion,
    CorrosionLevel,
    ContaminationLevel,
    FitQuality,
    RelationshipType,
    EventSeverity
)

from .failure_taxonomy import (
    FailureRecord,
    FailureTaxonomy,
    FailureCategory,
    FailureSignature,
    ContributingFactor,
    PreventiveMeasure,
    MechanicalFailureType,
    FatigueSubtype,
    OverloadSubtype,
    WearSubtype,
    CorrosionSubtype
)

from .emotion_mapping import (
    EmotionMapper,
    EmotionalState,
    OverallMood,
    emotion_mapper
)

from .storage_adapter import (
    StorageAdapter,
    PostgresStorageAdapter,
    InMemoryStorageAdapter
)

__all__ = [
    # Qualia Models
    'PartQualia',
    'MechanicalQualia',
    'ThermalQualia',
    'EnvironmentalQualia',
    'MatingQualia',
    'AssemblyQualia',
    'SignificantEvent',
    'HumanInteractionQualia',
    'TorqueEvent',
    # Enums
    'LifecycleStage',
    'WearState',
    'StressEmotion',
    'ThermalEmotion',
    'PerformanceEmotion',
    'CorrosionLevel',
    'ContaminationLevel',
    'FitQuality',
    'RelationshipType',
    'EventSeverity',
    # Failure Taxonomy
    'FailureRecord',
    'FailureTaxonomy',
    'FailureCategory',
    'FailureSignature',
    'ContributingFactor',
    'PreventiveMeasure',
    'MechanicalFailureType',
    'FatigueSubtype',
    'OverloadSubtype',
    'WearSubtype',
    'CorrosionSubtype',
    # Emotion Mapping
    'EmotionMapper',
    'EmotionalState',
    'OverallMood',
    'emotion_mapper',
    # Storage
    'StorageAdapter',
    'PostgresStorageAdapter',
    'InMemoryStorageAdapter'
]
