"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Sensors Module - IoT sensor integration for qualia collection
"""

from .sensor_registry import (
    SensorRegistry,
    SensorAdapter,
    SensorSpec,
    SensorCapability,
    SensorCategory,
    sensor_registry
)

from .data_pipeline import (
    SensorDataPipeline,
    PipelineConfig,
    QualiaUpdate,
    data_pipeline
)

from .adapters import (
    SmartTorqueWrenchAdapter,
    StrainGaugeAdapter,
    TorqueTransducerAdapter,
    ThermocoupleAdapter,
    IRThermometerAdapter,
    ThermalCameraAdapter,
    AccelerometerAdapter,
    VibrationAnalyzerAdapter,
    HumiditySensorAdapter,
    ChemicalDetectorAdapter,
    CorrosionSensorAdapter,
    VisualInspectionAdapter
)

__all__ = [
    # Registry
    'SensorRegistry',
    'SensorAdapter',
    'SensorSpec',
    'SensorCapability',
    'SensorCategory',
    'sensor_registry',
    # Pipeline
    'SensorDataPipeline',
    'PipelineConfig',
    'QualiaUpdate',
    'data_pipeline',
    # Adapters
    'SmartTorqueWrenchAdapter',
    'StrainGaugeAdapter',
    'TorqueTransducerAdapter',
    'ThermocoupleAdapter',
    'IRThermometerAdapter',
    'ThermalCameraAdapter',
    'AccelerometerAdapter',
    'VibrationAnalyzerAdapter',
    'HumiditySensorAdapter',
    'ChemicalDetectorAdapter',
    'CorrosionSensorAdapter',
    'VisualInspectionAdapter'
]
