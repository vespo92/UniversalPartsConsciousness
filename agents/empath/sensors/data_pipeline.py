"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Data Pipeline - Ingestion and processing of sensor data into qualia
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import logging

from .sensor_registry import SensorRegistry, SensorAdapter, sensor_registry
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
from ..schema import (
    PartQualia,
    MechanicalQualia,
    ThermalQualia,
    EnvironmentalQualia,
    SignificantEvent,
    EventSeverity,
    WearState,
    CorrosionLevel,
    ContaminationLevel,
    ThermalExpansionState
)

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuration for the data pipeline"""
    batch_size: int = 100
    flush_interval_seconds: float = 1.0
    enable_aggregation: bool = True
    significant_event_threshold: float = 0.7
    notify_shepherd_threshold: float = 0.8


@dataclass
class QualiaUpdate:
    """An update to part qualia from sensor data"""
    part_id: str
    sensor_type: str
    normalized_data: Dict
    qualia_contribution: Dict
    timestamp: datetime = field(default_factory=datetime.now)
    events: List[SignificantEvent] = field(default_factory=list)


class SensorDataPipeline:
    """
    Pipeline for processing sensor data into qualia.
    Transforms raw sensor readings into the subjective experience of parts.
    """

    # Map sensor types to their adapter classes
    ADAPTER_MAP = {
        "smart_torque_wrench": SmartTorqueWrenchAdapter,
        "strain_gauge": StrainGaugeAdapter,
        "torque_transducer": TorqueTransducerAdapter,
        "thermocouple": ThermocoupleAdapter,
        "ir_thermometer": IRThermometerAdapter,
        "thermal_camera": ThermalCameraAdapter,
        "accelerometer": AccelerometerAdapter,
        "vibration_analyzer": VibrationAnalyzerAdapter,
        "humidity_sensor": HumiditySensorAdapter,
        "chemical_detector": ChemicalDetectorAdapter,
        "corrosion_sensor": CorrosionSensorAdapter,
        "camera_inspection": VisualInspectionAdapter
    }

    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self.adapters: Dict[str, SensorAdapter] = {}
        self.pending_updates: List[QualiaUpdate] = []
        self.event_handlers: List[Callable] = []
        self.shepherd_notifier: Optional[Callable] = None
        self._init_adapters()

    def _init_adapters(self):
        """Initialize all sensor adapters"""
        for sensor_type, adapter_class in self.ADAPTER_MAP.items():
            self.adapters[sensor_type] = adapter_class()

    def register_event_handler(self, handler: Callable):
        """Register a handler for significant events"""
        self.event_handlers.append(handler)

    def register_shepherd_notifier(self, notifier: Callable):
        """Register the Agent_3 (Shepherd) notification callback"""
        self.shepherd_notifier = notifier

    async def ingest_sensor_data(self,
                                  sensor_type: str,
                                  raw_data: Dict,
                                  part_id: str) -> Optional[PartQualia]:
        """
        Ingest raw sensor data and convert to qualia.
        This is the main entry point for sensor data.
        """
        # Get appropriate adapter
        adapter = self.adapters.get(sensor_type)
        if not adapter:
            logger.warning(f"No adapter for sensor type: {sensor_type}")
            return None

        # Validate data
        if not adapter.validate(raw_data):
            logger.warning(f"Invalid data for {sensor_type}: {raw_data}")
            return None

        # Normalize data
        normalized = adapter.normalize(raw_data)

        # Get qualia contribution
        contribution = adapter.get_qualia_contribution(normalized)

        # Build qualia update
        update = QualiaUpdate(
            part_id=part_id,
            sensor_type=sensor_type,
            normalized_data=normalized,
            qualia_contribution=contribution
        )

        # Detect significant events
        events = self._extract_events(contribution)
        update.events = events

        # Generate qualia
        qualia = self._build_qualia(part_id, contribution, sensor_type)
        qualia.significant_events = events

        # Check for consciousness-relevant events
        if self._is_consciousness_relevant(qualia, events):
            await self._notify_shepherd(part_id, qualia, events)

        # Notify event handlers
        for event in events:
            await self._notify_event_handlers(event, qualia)

        return qualia

    def _build_qualia(self,
                     part_id: str,
                     contribution: Dict,
                     source_type: str) -> PartQualia:
        """Build a PartQualia object from sensor contribution"""
        qualia = PartQualia(part_id=part_id, source_type=source_type)

        # Apply mechanical state contributions
        if "mechanical_state" in contribution:
            mech = contribution["mechanical_state"]
            qualia.mechanical_state.torque_applied_nm = mech.get(
                "torque_applied_nm", qualia.mechanical_state.torque_applied_nm)
            qualia.mechanical_state.torque_capacity_percent = mech.get(
                "torque_capacity_percent", qualia.mechanical_state.torque_capacity_percent)
            qualia.mechanical_state.axial_load_n = mech.get(
                "axial_load_n", qualia.mechanical_state.axial_load_n)
            qualia.mechanical_state.load_capacity_percent = mech.get(
                "load_capacity_percent", qualia.mechanical_state.load_capacity_percent)
            qualia.mechanical_state.vibration_amplitude_g = mech.get(
                "vibration_amplitude_g", qualia.mechanical_state.vibration_amplitude_g)
            qualia.mechanical_state.vibration_frequency_hz = mech.get(
                "vibration_frequency_hz", qualia.mechanical_state.vibration_frequency_hz)
            qualia.mechanical_state.resonance_proximity = mech.get(
                "resonance_proximity", qualia.mechanical_state.resonance_proximity)

            if "wear_state" in mech:
                wear_val = mech["wear_state"]
                if isinstance(wear_val, str):
                    qualia.mechanical_state.wear_state = WearState(wear_val)
                else:
                    qualia.mechanical_state.wear_state = wear_val

            if "estimated_remaining_life_percent" in mech:
                qualia.mechanical_state.estimated_remaining_life_percent = mech[
                    "estimated_remaining_life_percent"]

        # Apply thermal state contributions
        if "thermal_state" in contribution:
            therm = contribution["thermal_state"]
            qualia.thermal_state.current_temperature_c = therm.get(
                "current_temperature_c", qualia.thermal_state.current_temperature_c)
            qualia.thermal_state.thermal_capacity_percent = therm.get(
                "thermal_capacity_percent", qualia.thermal_state.thermal_capacity_percent)
            qualia.thermal_state.max_temperature_experienced = therm.get(
                "max_temperature_experienced", qualia.thermal_state.max_temperature_experienced)
            qualia.thermal_state.min_temperature_experienced = therm.get(
                "min_temperature_experienced", qualia.thermal_state.min_temperature_experienced)

        # Apply environmental state contributions
        if "environmental_state" in contribution:
            env = contribution["environmental_state"]
            if "corrosion_level" in env:
                level = env["corrosion_level"]
                if isinstance(level, str):
                    qualia.environmental_state.corrosion_level = CorrosionLevel(level)
                else:
                    qualia.environmental_state.corrosion_level = level

            if "chemical_exposure" in env:
                qualia.environmental_state.chemical_exposure = env["chemical_exposure"]

            if "contamination_level" in env:
                level = env["contamination_level"]
                if isinstance(level, str):
                    qualia.environmental_state.contamination_level = ContaminationLevel(level)

            if "humidity_exposure" in env:
                qualia.environmental_state.humidity_exposure = env["humidity_exposure"]

        # Apply cumulative cycles if provided
        if "cumulative_cycles" in contribution:
            qualia.cumulative_cycles = contribution["cumulative_cycles"]

        # Update emotions based on new state
        qualia.update_emotions()

        return qualia

    def _extract_events(self, contribution: Dict) -> List[SignificantEvent]:
        """Extract significant events from qualia contribution"""
        events = []

        if "significant_events" in contribution:
            for event_data in contribution["significant_events"]:
                event = SignificantEvent(
                    event_type=event_data.get("type", "unknown"),
                    severity=EventSeverity(event_data.get("severity", "info")),
                    description=event_data.get("description", ""),
                    emotion=event_data.get("emotion", ""),
                    emotional_intensity=event_data.get("intensity", 0.5)
                )
                events.append(event)

        return events

    def _is_consciousness_relevant(self,
                                   qualia: PartQualia,
                                   events: List[SignificantEvent]) -> bool:
        """
        Determine if these qualia/events should trigger consciousness evolution.
        Returns True if Agent_3 (Shepherd) should be notified.
        """
        # Any critical event is consciousness-relevant
        for event in events:
            if event.severity == EventSeverity.CRITICAL:
                return True

        # High stress/strain is consciousness-relevant
        if qualia.mechanical_state.torque_capacity_percent > self.config.notify_shepherd_threshold:
            return True

        if qualia.mechanical_state.load_capacity_percent > self.config.notify_shepherd_threshold:
            return True

        # Low remaining life is consciousness-relevant
        if qualia.mechanical_state.estimated_remaining_life_percent < 20:
            return True

        # Hostile environment is consciousness-relevant
        if qualia.environmental_state.is_hostile_environment():
            return True

        return False

    async def _notify_shepherd(self,
                              part_id: str,
                              qualia: PartQualia,
                              events: List[SignificantEvent]):
        """Notify Agent_3 (Consciousness Shepherd) of significant experiences"""
        if self.shepherd_notifier:
            try:
                await self.shepherd_notifier(part_id, qualia, events)
            except Exception as e:
                logger.error(f"Failed to notify Shepherd: {e}")

    async def _notify_event_handlers(self,
                                    event: SignificantEvent,
                                    qualia: PartQualia):
        """Notify registered event handlers"""
        for handler in self.event_handlers:
            try:
                await handler(event, qualia)
            except Exception as e:
                logger.error(f"Event handler error: {e}")

    async def process_batch(self,
                           sensor_readings: List[Dict]) -> List[PartQualia]:
        """
        Process a batch of sensor readings.
        Each reading should have: sensor_type, part_id, data
        """
        results = []

        for reading in sensor_readings:
            sensor_type = reading.get("sensor_type")
            part_id = reading.get("part_id")
            data = reading.get("data", {})

            if not sensor_type or not part_id:
                logger.warning(f"Invalid reading: {reading}")
                continue

            qualia = await self.ingest_sensor_data(sensor_type, data, part_id)
            if qualia:
                results.append(qualia)

        return results

    def get_supported_sensors(self) -> List[str]:
        """Get list of supported sensor types"""
        return list(self.adapters.keys())


# Global pipeline instance
data_pipeline = SensorDataPipeline()
