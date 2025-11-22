"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Sensor Adapters - Converting raw sensor data to qualia
"""

from .torque_adapter import (
    SmartTorqueWrenchAdapter,
    StrainGaugeAdapter,
    TorqueTransducerAdapter
)

from .thermal_adapter import (
    ThermocoupleAdapter,
    IRThermometerAdapter,
    ThermalCameraAdapter
)

from .vibration_adapter import (
    AccelerometerAdapter,
    VibrationAnalyzerAdapter
)

from .environmental_adapter import (
    HumiditySensorAdapter,
    ChemicalDetectorAdapter,
    CorrosionSensorAdapter,
    VisualInspectionAdapter
)

__all__ = [
    # Torque
    'SmartTorqueWrenchAdapter',
    'StrainGaugeAdapter',
    'TorqueTransducerAdapter',
    # Thermal
    'ThermocoupleAdapter',
    'IRThermometerAdapter',
    'ThermalCameraAdapter',
    # Vibration
    'AccelerometerAdapter',
    'VibrationAnalyzerAdapter',
    # Environmental
    'HumiditySensorAdapter',
    'ChemicalDetectorAdapter',
    'CorrosionSensorAdapter',
    'VisualInspectionAdapter'
]
