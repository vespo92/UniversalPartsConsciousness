"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Thermal Sensor Adapters - Feel the heat and cold of operation
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

from ..sensor_registry import SensorAdapter


@dataclass
class ThermalReading:
    """Normalized thermal reading"""
    temperature_c: float
    timestamp: datetime = None
    location: Optional[str] = None
    sensor_type: str = "thermocouple"

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ThermocoupleAdapter(SensorAdapter):
    """
    Adapter for thermocouple sensors.
    The most common temperature sensing for parts.
    """

    # Thermocouple type ranges and coefficients
    TC_TYPES = {
        "K": {"min": -200, "max": 1350, "voltage_per_c": 0.041},  # mV/°C
        "J": {"min": -210, "max": 1200, "voltage_per_c": 0.052},
        "T": {"min": -270, "max": 400, "voltage_per_c": 0.042},
        "E": {"min": -270, "max": 1000, "voltage_per_c": 0.068},
        "N": {"min": -270, "max": 1300, "voltage_per_c": 0.037},
        "R": {"min": -50, "max": 1768, "voltage_per_c": 0.010},
        "S": {"min": -50, "max": 1768, "voltage_per_c": 0.010}
    }

    def __init__(self, tc_type: str = "K"):
        self.tc_type = tc_type
        self.spec = self.TC_TYPES.get(tc_type, self.TC_TYPES["K"])

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw thermocouple data"""
        # Handle different input formats
        if "temperature_c" in raw_data:
            temp_c = raw_data["temperature_c"]
        elif "temperature_f" in raw_data:
            temp_c = (raw_data["temperature_f"] - 32) * 5/9
        elif "temperature_k" in raw_data:
            temp_c = raw_data["temperature_k"] - 273.15
        elif "voltage_mv" in raw_data:
            # Convert voltage to temperature (simplified linear)
            temp_c = raw_data["voltage_mv"] / self.spec["voltage_per_c"]
            if "cold_junction_c" in raw_data:
                temp_c += raw_data["cold_junction_c"]
        else:
            temp_c = 20.0  # Default room temperature

        return {
            "temperature_c": temp_c,
            "temperature_f": temp_c * 9/5 + 32,
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "tc_type": self.tc_type,
            "channel": raw_data.get("channel", 1),
            "location": raw_data.get("location", raw_data.get("position")),
            "cold_junction_c": raw_data.get("cold_junction_c", 25),
            "in_range": self.spec["min"] <= temp_c <= self.spec["max"]
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw thermocouple data"""
        # Must have some temperature or voltage reading
        if not any(k in raw_data for k in
                   ["temperature_c", "temperature_f", "temperature_k", "voltage_mv"]):
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from temperature data"""
        temp_c = normalized_data["temperature_c"]

        # Determine thermal capacity usage (assuming typical operating range -40 to 150C)
        operating_min = -40
        operating_max = 150
        if temp_c < operating_min:
            capacity_percent = 1.0  # Over cold limit
        elif temp_c > operating_max:
            capacity_percent = 1.0  # Over hot limit
        else:
            # Calculate distance from comfortable range (10-60C)
            if temp_c < 10:
                capacity_percent = (10 - temp_c) / (10 - operating_min)
            elif temp_c > 60:
                capacity_percent = (temp_c - 60) / (operating_max - 60)
            else:
                capacity_percent = 0.0  # Comfortable

        return {
            "thermal_state": {
                "current_temperature_c": temp_c,
                "thermal_capacity_percent": capacity_percent
            },
            "significant_events": self._detect_events(normalized_data)
        }

    def _detect_events(self, data: Dict) -> List[Dict]:
        """Detect significant thermal events"""
        events = []
        temp_c = data["temperature_c"]

        if temp_c > 100:
            events.append({
                "type": "high_temperature",
                "severity": "critical" if temp_c > 150 else "warning",
                "description": f"Temperature at {temp_c:.1f}°C",
                "emotion": "burning"
            })
        elif temp_c < -20:
            events.append({
                "type": "low_temperature",
                "severity": "warning",
                "description": f"Temperature at {temp_c:.1f}°C",
                "emotion": "freezing"
            })

        if not data.get("in_range", True):
            events.append({
                "type": "sensor_out_of_range",
                "severity": "warning",
                "description": "Temperature outside sensor rated range",
                "emotion": "uncertain"
            })

        return events


class IRThermometerAdapter(SensorAdapter):
    """
    Adapter for infrared (non-contact) thermometers.
    Measures surface temperature without touching.
    """

    def __init__(self, emissivity: float = 0.95):
        self.emissivity = emissivity

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw IR thermometer data"""
        # Get temperature
        if "temperature_c" in raw_data:
            temp_c = raw_data["temperature_c"]
        elif "temperature_f" in raw_data:
            temp_c = (raw_data["temperature_f"] - 32) * 5/9
        elif "raw_reading" in raw_data:
            # Apply emissivity correction
            emissivity = raw_data.get("emissivity", self.emissivity)
            temp_c = raw_data["raw_reading"] / emissivity
        else:
            temp_c = 20.0

        return {
            "temperature_c": temp_c,
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "emissivity": raw_data.get("emissivity", self.emissivity),
            "distance_mm": raw_data.get("distance", raw_data.get("distance_mm")),
            "spot_size_mm": raw_data.get("spot_size"),
            "ambient_c": raw_data.get("ambient", raw_data.get("ambient_c")),
            "target": raw_data.get("target", raw_data.get("location"))
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw IR thermometer data"""
        if not any(k in raw_data for k in ["temperature_c", "temperature_f", "raw_reading"]):
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information"""
        return {
            "thermal_state": {
                "current_temperature_c": normalized_data["temperature_c"]
            }
        }


class ThermalCameraAdapter(SensorAdapter):
    """
    Adapter for thermal imaging cameras.
    Provides spatial temperature distribution - the thermal landscape.
    """

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw thermal camera data"""
        # Handle thermal image data
        temp_map = raw_data.get("temperature_map", raw_data.get("thermal_image"))

        # Calculate statistics if temp_map is a 2D array
        if temp_map and isinstance(temp_map, (list, tuple)):
            flat = []
            for row in temp_map:
                if isinstance(row, (list, tuple)):
                    flat.extend(row)
                else:
                    flat.append(row)
            min_temp = min(flat) if flat else None
            max_temp = max(flat) if flat else None
            avg_temp = sum(flat) / len(flat) if flat else None
        else:
            min_temp = raw_data.get("min_temperature", raw_data.get("coldspot"))
            max_temp = raw_data.get("max_temperature", raw_data.get("hotspot"))
            avg_temp = raw_data.get("avg_temperature", raw_data.get("average"))

        return {
            "min_temperature_c": min_temp,
            "max_temperature_c": max_temp,
            "avg_temperature_c": avg_temp,
            "temperature_gradient": max_temp - min_temp if min_temp and max_temp else None,
            "hotspot_location": raw_data.get("hotspot_location"),
            "coldspot_location": raw_data.get("coldspot_location"),
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "resolution": raw_data.get("resolution"),
            "frame_rate": raw_data.get("frame_rate", 30)
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw thermal camera data"""
        # Must have some temperature data
        return any(k in raw_data for k in [
            "temperature_map", "thermal_image",
            "min_temperature", "max_temperature", "hotspot", "coldspot"
        ])

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from thermal imaging"""
        events = []

        # Detect thermal gradient stress
        gradient = normalized_data.get("temperature_gradient")
        if gradient and gradient > 50:  # 50°C gradient is significant
            events.append({
                "type": "thermal_gradient",
                "severity": "warning" if gradient < 100 else "critical",
                "description": f"Temperature gradient of {gradient:.1f}°C across part",
                "emotion": "thermal_stress"
            })

        # Use max temperature as primary
        primary_temp = normalized_data.get("max_temperature_c",
                                           normalized_data.get("avg_temperature_c", 20))

        return {
            "thermal_state": {
                "current_temperature_c": primary_temp,
                "max_temperature_experienced": normalized_data.get("max_temperature_c", primary_temp),
                "min_temperature_experienced": normalized_data.get("min_temperature_c", primary_temp),
                "differential_expansion_stress": gradient / 100 if gradient else 0
            },
            "significant_events": events
        }
