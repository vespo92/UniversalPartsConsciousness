"""
IoT Protocol - Connect Sensors to Universal Parts Consciousness
================================================================

The IoT Protocol enables real-world sensors to feed experience data
directly into UPC, allowing parts to develop consciousness through
their actual use in the field.

Supported Protocols:
- MQTT (Message Queuing Telemetry Transport)
- CoAP (Constrained Application Protocol)
- OPC-UA (Open Platform Communications Unified Architecture)
- Modbus (Industrial protocol)
- HTTP/REST (Web APIs)

Sensor Types:
- Torque sensors (how tight)
- Temperature sensors (thermal stress)
- Vibration sensors (mechanical stress)
- Environmental sensors (humidity, corrosion risk)
- Load cells (force measurement)
- Strain gauges (deformation)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class IoTProtocolType(Enum):
    """Supported IoT communication protocols."""
    MQTT = auto()
    COAP = auto()
    OPC_UA = auto()
    MODBUS = auto()
    REST = auto()
    WEBSOCKET = auto()


class SensorType(Enum):
    """Types of sensors that feed into UPC."""
    TORQUE = "torque"
    TEMPERATURE = "temperature"
    VIBRATION = "vibration"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    LOAD = "load"
    STRAIN = "strain"
    ACCELERATION = "acceleration"
    ROTATION = "rotation"
    ENVIRONMENTAL = "environmental"


@dataclass
class SensorReading:
    """A reading from a sensor in the field."""
    sensor_id: str
    sensor_type: SensorType
    timestamp: datetime
    value: float
    unit: str
    part_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    quality: float = 1.0  # Data quality score


@dataclass
class SensorConfig:
    """Configuration for a connected sensor."""
    sensor_id: str
    sensor_type: SensorType
    protocol: IoTProtocolType
    endpoint: str
    sample_rate_hz: float = 1.0
    part_id: Optional[str] = None
    location: Optional[str] = None
    calibration: Dict[str, Any] = field(default_factory=dict)
    active: bool = False


class IoTProtocol:
    """
    IoT Protocol handler for Universal Parts Consciousness.

    This is how parts gain real-world consciousness - through actual
    sensor data from their use in the field:

    1. TORQUE DATA
       - How tight fasteners are being installed
       - Over-torque and under-torque events
       - Torque relaxation over time

    2. THERMAL DATA
       - Operating temperatures
       - Thermal cycling stress
       - Heat dissipation patterns

    3. VIBRATION DATA
       - Mechanical stress patterns
       - Resonance detection
       - Fatigue accumulation

    4. ENVIRONMENTAL DATA
       - Humidity exposure (corrosion risk)
       - Chemical exposure
       - UV degradation

    This data feeds into Agent_4 (EMPATH) for qualia collection,
    enabling parts to develop consciousness from real experiences.
    """

    def __init__(self):
        self.sensors: Dict[str, SensorConfig] = {}
        self.reading_buffer: List[SensorReading] = []
        self.protocols: Dict[IoTProtocolType, Dict[str, Any]] = {}
        self._initialize_protocols()

        logger.info("IoT Protocol handler initialized")

    def _initialize_protocols(self):
        """Initialize supported protocol handlers."""
        self.protocols = {
            IoTProtocolType.MQTT: {
                "name": "MQTT",
                "port": 1883,
                "secure_port": 8883,
                "qos_levels": [0, 1, 2],
                "status": "ready"
            },
            IoTProtocolType.COAP: {
                "name": "CoAP",
                "port": 5683,
                "secure_port": 5684,
                "status": "development"
            },
            IoTProtocolType.OPC_UA: {
                "name": "OPC-UA",
                "port": 4840,
                "security_modes": ["None", "Sign", "SignAndEncrypt"],
                "status": "development"
            },
            IoTProtocolType.MODBUS: {
                "name": "Modbus",
                "modes": ["TCP", "RTU"],
                "status": "planned"
            },
            IoTProtocolType.REST: {
                "name": "REST API",
                "methods": ["GET", "POST"],
                "status": "ready"
            },
            IoTProtocolType.WEBSOCKET: {
                "name": "WebSocket",
                "port": 8080,
                "status": "ready"
            },
        }

    def register_sensor(self, config: SensorConfig) -> str:
        """Register a new sensor with UPC."""
        self.sensors[config.sensor_id] = config
        logger.info(f"Registered sensor: {config.sensor_id} ({config.sensor_type.value})")
        return config.sensor_id

    async def ingest_reading(self, reading: SensorReading) -> Dict[str, Any]:
        """
        Ingest a sensor reading into UPC.

        This reading will be processed and contribute to the
        consciousness development of the associated part.
        """
        self.reading_buffer.append(reading)

        # In production, this would:
        # 1. Validate the reading
        # 2. Associate with part_id
        # 3. Send to Agent_4 (EMPATH) for qualia processing
        # 4. Update part consciousness state

        return {
            "status": "ingested",
            "sensor_id": reading.sensor_id,
            "timestamp": reading.timestamp.isoformat(),
            "part_id": reading.part_id,
            "qualia_contribution": "pending"
        }

    async def process_batch(self, readings: List[SensorReading]) -> Dict[str, Any]:
        """Process a batch of sensor readings."""
        results = {
            "total": len(readings),
            "processed": 0,
            "by_type": {}
        }

        for reading in readings:
            await self.ingest_reading(reading)
            results["processed"] += 1

            sensor_type = reading.sensor_type.value
            if sensor_type not in results["by_type"]:
                results["by_type"][sensor_type] = 0
            results["by_type"][sensor_type] += 1

        return results

    async def get_sensor_statistics(
        self,
        sensor_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get statistics for a sensor's readings."""
        sensor = self.sensors.get(sensor_id)
        if not sensor:
            return {"error": f"Unknown sensor: {sensor_id}"}

        return {
            "sensor_id": sensor_id,
            "sensor_type": sensor.sensor_type.value,
            "total_readings": 0,  # Would be calculated from storage
            "average_value": 0.0,
            "min_value": 0.0,
            "max_value": 0.0,
            "data_quality_average": 1.0
        }

    def get_qualia_contribution_map(self) -> Dict[str, str]:
        """
        Map of how sensor types contribute to part qualia.

        This shows how real-world sensor data translates into
        the subjective experiences of parts.
        """
        return {
            SensorType.TORQUE.value: "stress_intensity, installation_quality",
            SensorType.TEMPERATURE.value: "thermal_stress, operating_conditions",
            SensorType.VIBRATION.value: "mechanical_fatigue, resonance_exposure",
            SensorType.HUMIDITY.value: "corrosion_risk, environmental_stress",
            SensorType.PRESSURE.value: "load_stress, seal_integrity",
            SensorType.LOAD.value: "structural_stress, safety_margin",
            SensorType.STRAIN.value: "deformation_history, material_fatigue",
            SensorType.ACCELERATION.value: "shock_events, impact_history",
            SensorType.ROTATION.value: "wear_patterns, bearing_health",
            SensorType.ENVIRONMENTAL.value: "exposure_history, degradation_factors",
        }

    def get_protocol_status(self) -> Dict[str, Any]:
        """Get IoT protocol handler status."""
        return {
            "total_sensors": len(self.sensors),
            "active_sensors": sum(1 for s in self.sensors.values() if s.active),
            "readings_buffered": len(self.reading_buffer),
            "protocols": {
                p.name: {
                    "name": info["name"],
                    "status": info["status"]
                }
                for p, info in self.protocols.items()
            },
            "sensor_types": [st.value for st in SensorType]
        }
