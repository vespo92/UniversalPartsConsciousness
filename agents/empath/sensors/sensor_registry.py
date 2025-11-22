"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Sensor Registry - Central registry of all supported sensor types

Each sensor type provides a window into the subjective experience of parts.
"""

from typing import Dict, Type, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class SensorCategory(Enum):
    """Categories of sensors"""
    TORQUE = "torque"
    THERMAL = "thermal"
    VIBRATION = "vibration"
    ENVIRONMENTAL = "environmental"
    VISUAL = "visual"
    STRAIN = "strain"
    POSITION = "position"


@dataclass
class SensorCapability:
    """Describes what a sensor can measure"""
    measurement_type: str
    unit: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    resolution: Optional[float] = None
    sample_rate_hz: Optional[float] = None


@dataclass
class SensorSpec:
    """Specification for a sensor type"""
    sensor_type: str
    category: SensorCategory
    description: str
    capabilities: List[SensorCapability] = field(default_factory=list)
    data_format: str = "json"  # "json", "binary", "csv"
    requires_calibration: bool = False
    supported_protocols: List[str] = field(default_factory=lambda: ["mqtt", "http"])


class SensorAdapter(ABC):
    """Base class for all sensor adapters"""

    @abstractmethod
    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw sensor data to standard format"""
        pass

    @abstractmethod
    def validate(self, raw_data: Dict) -> bool:
        """Validate that raw data is properly formatted"""
        pass

    @abstractmethod
    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from normalized data"""
        pass


# Sensor type registry
SENSOR_REGISTRY: Dict[str, SensorSpec] = {
    # Torque Sensors
    "smart_torque_wrench": SensorSpec(
        sensor_type="smart_torque_wrench",
        category=SensorCategory.TORQUE,
        description="Smart torque wrench with digital readout and logging",
        capabilities=[
            SensorCapability("torque", "Nm", 0, 500, 0.1, 100),
            SensorCapability("angle", "degrees", 0, 360, 0.1, 100),
            SensorCapability("speed", "rpm", 0, 100, 1, 10)
        ],
        requires_calibration=True
    ),
    "strain_gauge": SensorSpec(
        sensor_type="strain_gauge",
        category=SensorCategory.STRAIN,
        description="Strain gauge for measuring mechanical deformation",
        capabilities=[
            SensorCapability("strain", "microstrain", -10000, 10000, 1, 1000),
            SensorCapability("load", "N", 0, 100000, 10, 1000)
        ],
        requires_calibration=True
    ),
    "torque_transducer": SensorSpec(
        sensor_type="torque_transducer",
        category=SensorCategory.TORQUE,
        description="Inline torque transducer for continuous monitoring",
        capabilities=[
            SensorCapability("torque", "Nm", 0, 1000, 0.01, 10000),
            SensorCapability("rpm", "rpm", 0, 10000, 1, 1000)
        ],
        requires_calibration=True
    ),

    # Temperature Sensors
    "thermocouple": SensorSpec(
        sensor_type="thermocouple",
        category=SensorCategory.THERMAL,
        description="Thermocouple for temperature measurement",
        capabilities=[
            SensorCapability("temperature", "C", -200, 1800, 0.1, 10)
        ]
    ),
    "ir_thermometer": SensorSpec(
        sensor_type="ir_thermometer",
        category=SensorCategory.THERMAL,
        description="Non-contact infrared thermometer",
        capabilities=[
            SensorCapability("temperature", "C", -50, 500, 0.5, 5)
        ]
    ),
    "thermal_camera": SensorSpec(
        sensor_type="thermal_camera",
        category=SensorCategory.THERMAL,
        description="Thermal imaging camera for temperature mapping",
        capabilities=[
            SensorCapability("temperature_map", "C", -40, 2000, 0.1, 30),
            SensorCapability("hotspot", "C", -40, 2000, 0.1, 30),
            SensorCapability("coldspot", "C", -40, 2000, 0.1, 30)
        ]
    ),

    # Vibration Sensors
    "accelerometer": SensorSpec(
        sensor_type="accelerometer",
        category=SensorCategory.VIBRATION,
        description="Accelerometer for vibration measurement",
        capabilities=[
            SensorCapability("acceleration_x", "g", -100, 100, 0.001, 10000),
            SensorCapability("acceleration_y", "g", -100, 100, 0.001, 10000),
            SensorCapability("acceleration_z", "g", -100, 100, 0.001, 10000)
        ]
    ),
    "vibration_analyzer": SensorSpec(
        sensor_type="vibration_analyzer",
        category=SensorCategory.VIBRATION,
        description="Full vibration analysis system with FFT",
        capabilities=[
            SensorCapability("amplitude", "g", 0, 100, 0.001, 25600),
            SensorCapability("frequency", "Hz", 0, 10000, 0.1, 25600),
            SensorCapability("velocity", "mm/s", 0, 1000, 0.01, 25600)
        ],
        requires_calibration=True
    ),

    # Environmental Sensors
    "humidity_sensor": SensorSpec(
        sensor_type="humidity_sensor",
        category=SensorCategory.ENVIRONMENTAL,
        description="Humidity and temperature sensor",
        capabilities=[
            SensorCapability("humidity", "%RH", 0, 100, 0.1, 1),
            SensorCapability("temperature", "C", -40, 85, 0.1, 1)
        ]
    ),
    "chemical_detector": SensorSpec(
        sensor_type="chemical_detector",
        category=SensorCategory.ENVIRONMENTAL,
        description="Chemical detection sensor for contamination",
        capabilities=[
            SensorCapability("chemical_presence", "ppm", 0, 10000, 1, 1),
            SensorCapability("chemical_type", "enum", None, None, None, 0.1)
        ],
        requires_calibration=True
    ),
    "corrosion_sensor": SensorSpec(
        sensor_type="corrosion_sensor",
        category=SensorCategory.ENVIRONMENTAL,
        description="Electrochemical corrosion rate sensor",
        capabilities=[
            SensorCapability("corrosion_rate", "mpy", 0, 1000, 0.1, 0.001),
            SensorCapability("linear_polarization_resistance", "ohm", 0, 100000, 1, 0.001)
        ]
    ),

    # Visual Inspection
    "camera_inspection": SensorSpec(
        sensor_type="camera_inspection",
        category=SensorCategory.VISUAL,
        description="Visual inspection camera with defect detection",
        capabilities=[
            SensorCapability("defect_count", "count", 0, 1000, 1, 30),
            SensorCapability("defect_area", "mm2", 0, 10000, 0.1, 30),
            SensorCapability("surface_condition", "score", 0, 100, 1, 30)
        ]
    ),
    "borescope": SensorSpec(
        sensor_type="borescope",
        category=SensorCategory.VISUAL,
        description="Borescope for internal inspection",
        capabilities=[
            SensorCapability("image", "frame", None, None, None, 30),
            SensorCapability("measurement", "mm", 0, 1000, 0.1, None)
        ]
    ),

    # Position/Alignment
    "laser_alignment": SensorSpec(
        sensor_type="laser_alignment",
        category=SensorCategory.POSITION,
        description="Laser alignment system",
        capabilities=[
            SensorCapability("angular_misalignment", "mrad", 0, 100, 0.001, 10),
            SensorCapability("offset", "mm", 0, 50, 0.001, 10)
        ],
        requires_calibration=True
    ),
    "proximity_sensor": SensorSpec(
        sensor_type="proximity_sensor",
        category=SensorCategory.POSITION,
        description="Proximity/distance sensor",
        capabilities=[
            SensorCapability("distance", "mm", 0, 1000, 0.01, 100)
        ]
    )
}


class SensorRegistry:
    """Registry for managing sensor types and their adapters"""

    def __init__(self):
        self.sensors = SENSOR_REGISTRY.copy()
        self.adapters: Dict[str, Type[SensorAdapter]] = {}

    def register_sensor(self, spec: SensorSpec) -> None:
        """Register a new sensor type"""
        self.sensors[spec.sensor_type] = spec

    def register_adapter(self, sensor_type: str, adapter_class: Type[SensorAdapter]) -> None:
        """Register an adapter for a sensor type"""
        self.adapters[sensor_type] = adapter_class

    def get_sensor_spec(self, sensor_type: str) -> Optional[SensorSpec]:
        """Get specification for a sensor type"""
        return self.sensors.get(sensor_type)

    def get_adapter(self, sensor_type: str) -> Optional[SensorAdapter]:
        """Get an adapter instance for a sensor type"""
        adapter_class = self.adapters.get(sensor_type)
        if adapter_class:
            return adapter_class()
        return None

    def list_sensors_by_category(self, category: SensorCategory) -> List[SensorSpec]:
        """List all sensors in a category"""
        return [
            spec for spec in self.sensors.values()
            if spec.category == category
        ]

    def list_all_sensor_types(self) -> List[str]:
        """List all registered sensor types"""
        return list(self.sensors.keys())


# Global sensor registry instance
sensor_registry = SensorRegistry()
