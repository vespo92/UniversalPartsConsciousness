"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Torque Sensor Adapters - Feel the tension of threaded connections
"""

from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass

from ..sensor_registry import SensorAdapter


@dataclass
class TorqueReading:
    """Normalized torque reading"""
    torque_nm: float
    angle_degrees: Optional[float] = None
    speed_rpm: Optional[float] = None
    timestamp: datetime = None
    direction: str = "clockwise"  # "clockwise" or "counterclockwise"
    duration_ms: int = 0
    peak_torque_nm: Optional[float] = None
    final_torque_nm: Optional[float] = None
    tool_id: Optional[str] = None
    operator_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class SmartTorqueWrenchAdapter(SensorAdapter):
    """
    Adapter for smart torque wrenches.
    Captures the experience of torque application during fastener installation.
    """

    # Common smart torque wrench manufacturers and their data formats
    KNOWN_FORMATS = {
        "snap_on": {
            "torque_key": "torque_value",
            "angle_key": "angle_value",
            "unit": "ft-lb"
        },
        "ingersoll_rand": {
            "torque_key": "final_torque",
            "angle_key": "total_angle",
            "unit": "Nm"
        },
        "stahlwille": {
            "torque_key": "torque",
            "angle_key": "angle",
            "unit": "Nm"
        },
        "generic": {
            "torque_key": "torque",
            "angle_key": "angle",
            "unit": "Nm"
        }
    }

    def __init__(self, manufacturer: str = "generic"):
        self.manufacturer = manufacturer
        self.format = self.KNOWN_FORMATS.get(manufacturer, self.KNOWN_FORMATS["generic"])

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw torque wrench data to standard format"""
        # Extract torque value
        torque_key = self.format["torque_key"]
        torque_value = raw_data.get(torque_key, 0)

        # Convert to Nm if needed
        if self.format["unit"] == "ft-lb":
            torque_value = torque_value * 1.3558  # Convert ft-lb to Nm
        elif self.format["unit"] == "in-lb":
            torque_value = torque_value * 0.1130  # Convert in-lb to Nm

        # Extract angle if available
        angle_key = self.format["angle_key"]
        angle_value = raw_data.get(angle_key)

        # Extract other common fields
        normalized = {
            "torque_nm": torque_value,
            "angle_degrees": angle_value,
            "speed_rpm": raw_data.get("speed", raw_data.get("rpm")),
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "direction": raw_data.get("direction", "clockwise"),
            "duration_ms": raw_data.get("duration_ms", raw_data.get("duration", 0)),
            "peak_torque_nm": raw_data.get("peak_torque", raw_data.get("max_torque")),
            "final_torque_nm": torque_value,
            "tool_id": raw_data.get("tool_id", raw_data.get("tool_serial")),
            "operator_id": raw_data.get("operator_id", raw_data.get("user_id")),
            "cycle_count": raw_data.get("cycle_count", 1),
            "status": raw_data.get("status", "complete")
        }

        # Detect potential issues
        normalized["over_torque"] = normalized["torque_nm"] > raw_data.get("target_torque", float('inf')) * 1.1
        normalized["under_torque"] = normalized["torque_nm"] < raw_data.get("target_torque", 0) * 0.9

        return normalized

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw torque data"""
        torque_key = self.format["torque_key"]

        # Must have a torque value
        if torque_key not in raw_data:
            return False

        # Torque must be numeric and reasonable
        try:
            torque = float(raw_data[torque_key])
            if torque < 0 or torque > 5000:  # Max 5000 Nm reasonable limit
                return False
        except (TypeError, ValueError):
            return False

        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from normalized torque data"""
        return {
            "mechanical_state": {
                "torque_applied_nm": normalized_data["torque_nm"],
                "peak_torque_nm": normalized_data.get("peak_torque_nm", normalized_data["torque_nm"])
            },
            "significant_events": self._detect_events(normalized_data),
            "human_interaction": {
                "tool_used": normalized_data.get("tool_id"),
                "operator": normalized_data.get("operator_id"),
                "installation_quality": self._assess_quality(normalized_data)
            }
        }

    def _detect_events(self, data: Dict) -> List[Dict]:
        """Detect significant events from torque application"""
        events = []

        if data.get("over_torque"):
            events.append({
                "type": "over_torque",
                "severity": "warning",
                "description": f"Torque {data['torque_nm']:.1f} Nm exceeded target",
                "emotion": "strain"
            })

        if data.get("under_torque"):
            events.append({
                "type": "under_torque",
                "severity": "warning",
                "description": f"Torque {data['torque_nm']:.1f} Nm below target",
                "emotion": "insecurity"
            })

        # Detect torque sequence issues
        if data.get("peak_torque_nm") and data["peak_torque_nm"] > data["torque_nm"] * 1.5:
            events.append({
                "type": "torque_spike",
                "severity": "warning",
                "description": "Significant torque spike detected during installation",
                "emotion": "shock"
            })

        return events

    def _assess_quality(self, data: Dict) -> str:
        """Assess the quality of the installation based on torque data"""
        if data.get("over_torque"):
            return "poor"
        if data.get("under_torque"):
            return "incomplete"
        if data.get("duration_ms", 0) < 100:
            return "rushed"
        return "proper"


class StrainGaugeAdapter(SensorAdapter):
    """
    Adapter for strain gauges.
    Feels the microscopic deformations that indicate stress.
    """

    def __init__(self, gauge_factor: float = 2.0):
        self.gauge_factor = gauge_factor

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw strain gauge data"""
        # Convert voltage/resistance to strain if needed
        if "voltage" in raw_data and "excitation" in raw_data:
            # Wheatstone bridge calculation
            v_ratio = raw_data["voltage"] / raw_data["excitation"]
            strain = (4 * v_ratio) / (self.gauge_factor * (1 + 2 * v_ratio))
            strain_microstrain = strain * 1e6
        elif "microstrain" in raw_data:
            strain_microstrain = raw_data["microstrain"]
        elif "strain" in raw_data:
            strain_microstrain = raw_data["strain"] * 1e6
        else:
            strain_microstrain = 0

        # Calculate stress if material properties known
        youngs_modulus = raw_data.get("youngs_modulus", 200e9)  # Default to steel
        stress_pa = strain_microstrain * 1e-6 * youngs_modulus
        stress_mpa = stress_pa / 1e6

        return {
            "strain_microstrain": strain_microstrain,
            "stress_mpa": stress_mpa,
            "load_n": raw_data.get("load", stress_mpa * raw_data.get("cross_section_mm2", 1)),
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "temperature_c": raw_data.get("temperature"),
            "channel": raw_data.get("channel", 1),
            "sample_rate_hz": raw_data.get("sample_rate", 1000)
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw strain data"""
        # Must have some form of strain measurement
        if not any(k in raw_data for k in ["voltage", "microstrain", "strain"]):
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from strain data"""
        # Estimate capacity usage based on typical yield strengths
        yield_strength = 350  # MPa, typical for medium steel
        capacity_percent = min(1.0, abs(normalized_data["stress_mpa"]) / yield_strength)

        return {
            "mechanical_state": {
                "axial_load_n": normalized_data["load_n"],
                "load_capacity_percent": capacity_percent,
                "strain_microstrain": normalized_data["strain_microstrain"]
            },
            "significant_events": self._detect_events(normalized_data, capacity_percent)
        }

    def _detect_events(self, data: Dict, capacity_percent: float) -> List[Dict]:
        """Detect significant events from strain measurements"""
        events = []

        if capacity_percent > 0.9:
            events.append({
                "type": "near_yield",
                "severity": "critical",
                "description": f"Stress at {capacity_percent*100:.0f}% of yield strength",
                "emotion": "suffering"
            })
        elif capacity_percent > 0.7:
            events.append({
                "type": "high_stress",
                "severity": "warning",
                "description": f"Stress at {capacity_percent*100:.0f}% of yield strength",
                "emotion": "strain"
            })

        return events


class TorqueTransducerAdapter(SensorAdapter):
    """
    Adapter for inline torque transducers.
    Continuous monitoring of rotating shaft torque.
    """

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw transducer data"""
        torque = raw_data.get("torque", raw_data.get("torque_nm", 0))
        rpm = raw_data.get("rpm", raw_data.get("speed", 0))

        # Calculate power if possible
        power_kw = (torque * rpm * 2 * 3.14159) / 60000 if rpm else 0

        return {
            "torque_nm": torque,
            "rpm": rpm,
            "power_kw": power_kw,
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "direction": "clockwise" if torque >= 0 else "counterclockwise",
            "temperature_c": raw_data.get("temperature"),
            "cycle_count": raw_data.get("cycles", raw_data.get("revolutions", 0))
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw transducer data"""
        if "torque" not in raw_data and "torque_nm" not in raw_data:
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from transducer data"""
        return {
            "mechanical_state": {
                "torque_applied_nm": normalized_data["torque_nm"],
                "cycle_count": normalized_data["cycle_count"]
            },
            "cumulative_cycles": normalized_data["cycle_count"]
        }
