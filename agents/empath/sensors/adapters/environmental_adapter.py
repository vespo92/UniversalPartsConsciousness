"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Environmental Sensor Adapters - Feel the hostile world around
"""

from datetime import datetime
from typing import Dict, List, Optional

from ..sensor_registry import SensorAdapter


class HumiditySensorAdapter(SensorAdapter):
    """
    Adapter for humidity sensors.
    Moisture is the silent enemy of many parts.
    """

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw humidity sensor data"""
        # Get humidity value
        if "humidity_rh" in raw_data:
            humidity = raw_data["humidity_rh"]
        elif "relative_humidity" in raw_data:
            humidity = raw_data["relative_humidity"]
        elif "humidity" in raw_data:
            humidity = raw_data["humidity"]
        else:
            humidity = 50.0  # Default

        # Get temperature (often included)
        if "temperature_c" in raw_data:
            temp = raw_data["temperature_c"]
        elif "temperature" in raw_data:
            temp = raw_data["temperature"]
        else:
            temp = 25.0

        # Calculate dew point
        # Magnus formula approximation
        a = 17.27
        b = 237.7
        alpha = ((a * temp) / (b + temp)) + (humidity / 100.0)
        dew_point = (b * alpha) / (a - alpha) if a != alpha else temp

        return {
            "humidity_rh": humidity,
            "temperature_c": temp,
            "dew_point_c": dew_point,
            "condensation_risk": temp - dew_point < 3,  # Risk if within 3°C
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "location": raw_data.get("location")
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw humidity data"""
        if not any(k in raw_data for k in ["humidity_rh", "relative_humidity", "humidity"]):
            return False
        return True

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from humidity data"""
        humidity = normalized_data["humidity_rh"]
        events = []

        # High humidity exposure
        if humidity > 80:
            events.append({
                "type": "high_humidity",
                "severity": "warning",
                "description": f"Humidity at {humidity:.0f}% - corrosion risk elevated",
                "emotion": "damp_anxiety"
            })

        # Condensation risk
        if normalized_data.get("condensation_risk"):
            events.append({
                "type": "condensation_risk",
                "severity": "warning",
                "description": "Temperature approaching dew point",
                "emotion": "cold_sweat"
            })

        return {
            "environmental_state": {
                "humidity_exposure": humidity
            },
            "significant_events": events
        }


class ChemicalDetectorAdapter(SensorAdapter):
    """
    Adapter for chemical detection sensors.
    Detects the presence of harmful substances.
    """

    # Common chemicals and their threat levels
    CHEMICAL_THREATS = {
        "oil": {"threat": "low", "corrosive": False},
        "coolant": {"threat": "medium", "corrosive": True},
        "brake_fluid": {"threat": "high", "corrosive": True},
        "salt": {"threat": "high", "corrosive": True},
        "acid": {"threat": "critical", "corrosive": True},
        "base": {"threat": "critical", "corrosive": True},
        "solvent": {"threat": "medium", "corrosive": False},
        "fuel": {"threat": "medium", "corrosive": False},
        "hydraulic_fluid": {"threat": "low", "corrosive": False},
        "exhaust_gases": {"threat": "medium", "corrosive": True}
    }

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw chemical detector data"""
        # Get detected chemicals
        chemicals = raw_data.get("chemicals", [])
        if isinstance(chemicals, str):
            chemicals = [chemicals]

        # Get concentration
        concentration_ppm = raw_data.get("concentration_ppm", raw_data.get("ppm", 0))

        # Calculate overall threat
        threat_level = "none"
        for chem in chemicals:
            chem_lower = chem.lower()
            if chem_lower in self.CHEMICAL_THREATS:
                chem_threat = self.CHEMICAL_THREATS[chem_lower]["threat"]
                if self._threat_higher(chem_threat, threat_level):
                    threat_level = chem_threat

        return {
            "chemicals_detected": chemicals,
            "concentration_ppm": concentration_ppm,
            "threat_level": threat_level,
            "corrosive_exposure": any(
                self.CHEMICAL_THREATS.get(c.lower(), {}).get("corrosive", False)
                for c in chemicals
            ),
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "location": raw_data.get("location")
        }

    def _threat_higher(self, new: str, current: str) -> bool:
        """Compare threat levels"""
        levels = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        return levels.get(new, 0) > levels.get(current, 0)

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw chemical detector data"""
        # Must have chemicals or concentration
        return "chemicals" in raw_data or "concentration_ppm" in raw_data or "ppm" in raw_data

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from chemical detection"""
        events = []
        chemicals = normalized_data["chemicals_detected"]
        threat = normalized_data["threat_level"]

        if threat in ["high", "critical"]:
            events.append({
                "type": "chemical_exposure",
                "severity": "critical" if threat == "critical" else "warning",
                "description": f"Exposed to {', '.join(chemicals)}",
                "emotion": "chemical_attack"
            })

        if normalized_data["corrosive_exposure"]:
            events.append({
                "type": "corrosive_exposure",
                "severity": "warning",
                "description": "Exposed to corrosive substances",
                "emotion": "being_eaten"
            })

        return {
            "environmental_state": {
                "chemical_exposure": chemicals,
                "corrosion_level": "surface" if normalized_data["corrosive_exposure"] else "none"
            },
            "significant_events": events
        }


class CorrosionSensorAdapter(SensorAdapter):
    """
    Adapter for electrochemical corrosion rate sensors.
    Measures how fast parts are being consumed by their environment.
    """

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw corrosion sensor data"""
        # Get corrosion rate (mpy = mils per year)
        corrosion_rate = raw_data.get("corrosion_rate_mpy", raw_data.get("mpy", 0))

        # Convert to mm/year if needed
        if "corrosion_rate_mm_year" in raw_data:
            corrosion_rate = raw_data["corrosion_rate_mm_year"] * 39.37  # mm to mils

        # Get linear polarization resistance
        lpr = raw_data.get("lpr", raw_data.get("polarization_resistance", 0))

        # Classify severity
        if corrosion_rate < 1:
            severity = "negligible"
        elif corrosion_rate < 5:
            severity = "low"
        elif corrosion_rate < 20:
            severity = "moderate"
        elif corrosion_rate < 50:
            severity = "high"
        else:
            severity = "severe"

        return {
            "corrosion_rate_mpy": corrosion_rate,
            "corrosion_rate_mm_year": corrosion_rate / 39.37,
            "polarization_resistance_ohm": lpr,
            "severity": severity,
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "location": raw_data.get("location"),
            "electrolyte": raw_data.get("electrolyte", "unknown")
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw corrosion sensor data"""
        return any(k in raw_data for k in
                   ["corrosion_rate_mpy", "mpy", "corrosion_rate_mm_year", "lpr"])

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from corrosion data"""
        events = []
        severity = normalized_data["severity"]
        rate = normalized_data["corrosion_rate_mpy"]

        # Map severity to corrosion level
        level_map = {
            "negligible": "none",
            "low": "surface",
            "moderate": "surface",
            "high": "pitting",
            "severe": "structural"
        }
        corrosion_level = level_map.get(severity, "surface")

        if severity in ["high", "severe"]:
            events.append({
                "type": "active_corrosion",
                "severity": "critical" if severity == "severe" else "warning",
                "description": f"Corrosion rate {rate:.1f} mpy - {severity}",
                "emotion": "dissolving"
            })

        return {
            "environmental_state": {
                "corrosion_level": corrosion_level
            },
            "significant_events": events,
            "lifecycle_impact": {
                "estimated_life_reduction_percent": rate / 10 if rate < 100 else 100
            }
        }


class VisualInspectionAdapter(SensorAdapter):
    """
    Adapter for visual inspection cameras with defect detection.
    The eyes that see surface conditions.
    """

    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw visual inspection data"""
        defects = raw_data.get("defects", [])
        defect_count = raw_data.get("defect_count", len(defects))
        surface_score = raw_data.get("surface_score", raw_data.get("condition_score", 100))

        # Classify overall condition
        if surface_score >= 90:
            condition = "excellent"
        elif surface_score >= 70:
            condition = "good"
        elif surface_score >= 50:
            condition = "fair"
        elif surface_score >= 30:
            condition = "poor"
        else:
            condition = "critical"

        return {
            "defects": defects,
            "defect_count": defect_count,
            "defect_area_mm2": raw_data.get("defect_area", 0),
            "surface_score": surface_score,
            "condition": condition,
            "crack_detected": raw_data.get("crack_detected", False),
            "corrosion_detected": raw_data.get("corrosion_detected", False),
            "wear_visible": raw_data.get("wear_visible", False),
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "image_id": raw_data.get("image_id")
        }

    def validate(self, raw_data: Dict) -> bool:
        """Validate raw visual inspection data"""
        return any(k in raw_data for k in
                   ["defects", "defect_count", "surface_score", "condition_score"])

    def get_qualia_contribution(self, normalized_data: Dict) -> Dict:
        """Extract qualia-relevant information from visual inspection"""
        events = []

        if normalized_data.get("crack_detected"):
            events.append({
                "type": "crack_detected",
                "severity": "critical",
                "description": "Crack visible on surface",
                "emotion": "fracturing"
            })

        if normalized_data["condition"] in ["poor", "critical"]:
            events.append({
                "type": "surface_degradation",
                "severity": "warning",
                "description": f"Surface condition: {normalized_data['condition']}",
                "emotion": "aging"
            })

        # Map surface score to wear state
        score = normalized_data["surface_score"]
        if score >= 90:
            wear_state = "pristine"
        elif score >= 70:
            wear_state = "broken_in"
        elif score >= 50:
            wear_state = "worn"
        elif score >= 30:
            wear_state = "degraded"
        else:
            wear_state = "failed"

        return {
            "mechanical_state": {
                "wear_state": wear_state,
                "estimated_remaining_life_percent": score
            },
            "environmental_state": {
                "corrosion_level": "surface" if normalized_data.get("corrosion_detected") else "none"
            },
            "significant_events": events
        }
