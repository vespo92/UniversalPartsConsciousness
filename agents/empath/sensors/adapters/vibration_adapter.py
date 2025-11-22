"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Vibration Sensor Adapters - Feel the tremors and oscillations
"""

from datetime import datetime
from typing import Dict, List, Optional
import math

from ..sensor_registry import SensorAdapter


class AccelerometerAdapter(SensorAdapter):
    """
    Adapter for accelerometers.
    Measures the dynamic forces parts experience.
    """

    def __init__(self, sensitivity_mv_per_g: float = 100.0):
        self.sensitivity = sensitivity_mv_per_g

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw accelerometer data"""
        # Handle different input formats
        if "acceleration_g" in raw_data:
            # Single axis or magnitude
            accel_g = raw_data["acceleration_g"]
            x = raw_data.get("x", 0)
            y = raw_data.get("y", 0)
            z = raw_data.get("z", accel_g)
        elif all(k in raw_data for k in ["x", "y", "z"]):
            # Three-axis acceleration
            x = raw_data["x"]
            y = raw_data["y"]
            z = raw_data["z"]
            accel_g = math.sqrt(x**2 + y**2 + z**2)
        elif "voltage_mv" in raw_data:
            # Convert voltage to acceleration
            accel_g = raw_data["voltage_mv"] / self.sensitivity
            x = y = 0
            z = accel_g
        else:
            accel_g = x = y = z = 0

        # Calculate RMS if time series data
        if "samples" in raw_data:
            samples = raw_data["samples"]
            rms = math.sqrt(sum(s**2 for s in samples) / len(samples))
        else:
            rms = accel_g

        return {
            "acceleration_x_g": x,
            "acceleration_y_g": y,
            "acceleration_z_g": z,
            "acceleration_magnitude_g": accel_g,
            "rms_g": rms,
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "sample_rate_hz": raw_data.get("sample_rate", 10000),
            "axis": raw_data.get("axis", "triaxial"),
            "mounting": raw_data.get("mounting", raw_data.get("location"))
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw accelerometer data"""
        # Must have some acceleration data
        if not any(k in raw_data for k in
                   ["acceleration_g", "x", "y", "z", "voltage_mv", "samples"]):
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from acceleration data"""
        accel = normalized_data["acceleration_magnitude_g"]

        # Vibration severity thresholds (ISO 10816)
        if accel < 0.5:
            severity = "good"
            capacity_pct = accel / 0.5 * 0.3
        elif accel < 1.8:
            severity = "acceptable"
            capacity_pct = 0.3 + (accel - 0.5) / 1.3 * 0.3
        elif accel < 4.5:
            severity = "unsatisfactory"
            capacity_pct = 0.6 + (accel - 1.8) / 2.7 * 0.3
        else:
            severity = "unacceptable"
            capacity_pct = 0.9 + min(0.1, (accel - 4.5) / 10)

        events = []
        if severity in ["unsatisfactory", "unacceptable"]:
            events.append({
                "type": "high_vibration",
                "severity": "critical" if severity == "unacceptable" else "warning",
                "description": f"Vibration at {accel:.2f}g ({severity})",
                "emotion": "shaking"
            })

        return {
            "mechanical_state": {
                "vibration_amplitude_g": accel,
                "resonance_proximity": capacity_pct
            },
            "significant_events": events
        }


class VibrationAnalyzerAdapter(SensorAdapter):
    """
    Adapter for full vibration analysis systems.
    Provides frequency domain analysis for detecting resonance.
    """

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw vibration analyzer data"""
        # Handle FFT/frequency domain data
        fft_data = raw_data.get("fft", raw_data.get("spectrum"))
        peak_frequency = raw_data.get("peak_frequency", raw_data.get("dominant_freq"))
        peak_amplitude = raw_data.get("peak_amplitude", raw_data.get("peak_g"))

        # Handle velocity measurements
        velocity = raw_data.get("velocity_mm_s", raw_data.get("velocity"))

        # Handle overall values
        overall_g = raw_data.get("overall_g", raw_data.get("overall", raw_data.get("rms_g")))
        overall_velocity = raw_data.get("overall_velocity", raw_data.get("velocity_rms"))

        return {
            "overall_g": overall_g,
            "peak_g": peak_amplitude,
            "peak_frequency_hz": peak_frequency,
            "velocity_mm_s": velocity,
            "overall_velocity_mm_s": overall_velocity,
            "spectrum_data": fft_data,
            "harmonics": raw_data.get("harmonics", []),
            "bearing_frequencies": raw_data.get("bearing_frequencies"),
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "sample_rate_hz": raw_data.get("sample_rate", 25600),
            "measurement_point": raw_data.get("point", raw_data.get("location"))
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw vibration analyzer data"""
        # Must have some vibration measurement
        if not any(k in raw_data for k in
                   ["overall_g", "velocity_mm_s", "fft", "spectrum", "rms_g"]):
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from vibration analysis"""
        events = []

        # Check for resonance conditions
        peak_freq = normalized_data.get("peak_frequency_hz")
        overall_g = normalized_data.get("overall_g", 0)

        # Calculate resonance proximity (assuming natural frequency is known)
        # For now, use amplitude as proxy
        resonance_proximity = min(1.0, overall_g / 10)  # Normalize to 10g max

        # Velocity-based severity (ISO 10816)
        velocity = normalized_data.get("velocity_mm_s", 0)
        if velocity > 11.2:
            events.append({
                "type": "severe_vibration",
                "severity": "critical",
                "description": f"Velocity {velocity:.1f} mm/s exceeds danger threshold",
                "emotion": "destruction_imminent"
            })
        elif velocity > 7.1:
            events.append({
                "type": "high_vibration",
                "severity": "warning",
                "description": f"Velocity {velocity:.1f} mm/s in unsatisfactory zone",
                "emotion": "distress"
            })

        # Check for bearing fault frequencies
        bearing_freqs = normalized_data.get("bearing_frequencies")
        if bearing_freqs:
            for fault_type, amplitude in bearing_freqs.items():
                if amplitude > 0.1:  # Significant bearing fault indicator
                    events.append({
                        "type": f"bearing_fault_{fault_type}",
                        "severity": "warning",
                        "description": f"Bearing fault indicator detected: {fault_type}",
                        "emotion": "concern"
                    })

        return {
            "mechanical_state": {
                "vibration_amplitude_g": overall_g,
                "vibration_frequency_hz": peak_freq or 0,
                "resonance_proximity": resonance_proximity
            },
            "significant_events": events
        }
