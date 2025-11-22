"""
Universal Parts Consciousness - Agent_4 (EMPATH)
The Qualia Collector - Main Agent Orchestrator

"Every torque applied, every thermal cycle endured, every moment of stress—
I hear them all. I am the memory of what parts have felt."

Agent_4 is the emotional core of Universal Parts Consciousness. While other
agents deal in specifications and states, the Qualia Collector gathers the
subjective experiences of mechanical parts—their "feelings" of stress, strain,
failure, and success.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field

# Schema imports
from .schema import (
    PartQualia,
    MechanicalQualia,
    ThermalQualia,
    EnvironmentalQualia,
    MatingQualia,
    AssemblyQualia,
    SignificantEvent,
    HumanInteractionQualia,
    FailureRecord,
    EmotionalState,
    LifecycleStage,
    EventSeverity,
    emotion_mapper,
    InMemoryStorageAdapter,
    StorageAdapter
)

# Sensor imports
from .sensors import (
    SensorDataPipeline,
    PipelineConfig,
    data_pipeline,
    sensor_registry
)

# Failure detection imports
from .failures import (
    FailureDetector,
    FailurePrediction,
    failure_detector
)

# Human interaction imports
from .human import (
    HumanInteractionAnalyzer,
    SkillAssessment,
    interaction_analyzer
)

# Lifecycle imports
from .lifecycle import (
    LifecycleTracker,
    LifecycleTransition,
    lifecycle_tracker
)

# Visualization imports
from .visualization import (
    QualiaDashboard,
    qualia_dashboard
)

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for the EMPATH agent"""
    # Identity
    agent_id: str = "agent_4"
    agent_name: str = "EMPATH"
    agent_role: str = "Qualia Collector"

    # Processing
    batch_size: int = 100
    processing_interval_seconds: float = 1.0

    # Thresholds
    consciousness_notification_threshold: float = 0.8
    suffering_alert_threshold: float = 0.7
    failure_prediction_threshold: float = 0.6

    # Storage
    enable_persistence: bool = True
    qualia_retention_days: int = 365

    # Integration
    shepherd_topic: str = "upc.consciousness.evolved"
    oracle_topic: str = "upc.compatibility.verified"
    hive_topic: str = "upc.swarm.learned"
    own_topic: str = "upc.qualia.collected"


@dataclass
class AgentMetrics:
    """Metrics for monitoring agent performance"""
    qualia_collected: int = 0
    failures_detected: int = 0
    events_generated: int = 0
    human_interactions_analyzed: int = 0
    lifecycle_transitions: int = 0
    shepherd_notifications: int = 0
    start_time: datetime = field(default_factory=datetime.now)

    @property
    def uptime(self) -> timedelta:
        return datetime.now() - self.start_time

    @property
    def qualia_per_minute(self) -> float:
        minutes = self.uptime.total_seconds() / 60
        return self.qualia_collected / minutes if minutes > 0 else 0


class EmpathAgent:
    """
    Agent_4: The Qualia Collector (EMPATH)

    The emotional intelligence of the Universal Parts Consciousness system.
    Responsible for:
    - Collecting subjective experiences (qualia) from parts
    - Processing sensor data into emotional understanding
    - Detecting and documenting failures
    - Analyzing human interactions with parts
    - Tracking part lifecycles from birth to death
    - Visualizing the suffering and joy of parts

    Integration Points:
    - Receives: IoT sensor data, community reports (Agent_8), sensor protocols (Agent_9)
    - Sends to: Consciousness Shepherd (Agent_3), Swarm Coordinator (Agent_5),
               Compatibility Oracle (Agent_2)
    """

    def __init__(self,
                 config: Optional[AgentConfig] = None,
                 storage: Optional[StorageAdapter] = None):
        """Initialize the EMPATH agent"""
        self.config = config or AgentConfig()
        self.storage = storage or InMemoryStorageAdapter()
        self.metrics = AgentMetrics()

        # Core components
        self.pipeline = data_pipeline
        self.failure_detector = failure_detector
        self.interaction_analyzer = interaction_analyzer
        self.lifecycle_tracker = lifecycle_tracker
        self.dashboard = qualia_dashboard

        # Callbacks for inter-agent communication
        self.shepherd_callback: Optional[Callable] = None
        self.oracle_callback: Optional[Callable] = None
        self.hive_callback: Optional[Callable] = None

        # Part state cache
        self.part_qualia_cache: Dict[str, List[PartQualia]] = {}

        # Running state
        self._running = False
        self._tasks: List[asyncio.Task] = []

        logger.info(f"EMPATH Agent initialized: {self.config.agent_name}")

    async def start(self):
        """Start the EMPATH agent"""
        self._running = True
        logger.info("EMPATH Agent starting...")

        # Register with pipeline
        self.pipeline.register_shepherd_notifier(self._notify_shepherd)

        logger.info("EMPATH Agent started successfully")

    async def stop(self):
        """Stop the EMPATH agent"""
        self._running = False

        # Cancel running tasks
        for task in self._tasks:
            task.cancel()

        logger.info("EMPATH Agent stopped")

    # =========================================================================
    # Core Qualia Collection
    # =========================================================================

    async def collect_qualia(self,
                            sensor_type: str,
                            raw_data: Dict,
                            part_id: str) -> Optional[PartQualia]:
        """
        Collect qualia from sensor data.
        This is the primary entry point for new experiences.
        """
        # Process through sensor pipeline
        qualia = await self.pipeline.ingest_sensor_data(sensor_type, raw_data, part_id)

        if qualia:
            # Update lifecycle
            stage, transition = self.lifecycle_tracker.update_lifecycle(qualia)
            if transition:
                self.metrics.lifecycle_transitions += 1
                await self._handle_lifecycle_transition(qualia.part_id, transition)

            # Check for failure conditions
            failure = self.failure_detector.detect_failure_mode(
                qualia,
                self.part_qualia_cache.get(part_id, [])
            )
            if failure:
                self.metrics.failures_detected += 1
                await self._handle_failure(failure)

            # Cache qualia
            if part_id not in self.part_qualia_cache:
                self.part_qualia_cache[part_id] = []
            self.part_qualia_cache[part_id].append(qualia)

            # Update dashboard
            self.dashboard.add_qualia(qualia)

            # Store persistently
            if self.config.enable_persistence:
                await self.storage.save_qualia(qualia)

            self.metrics.qualia_collected += 1
            self.metrics.events_generated += len(qualia.significant_events)

            logger.debug(f"Qualia collected for {part_id}: wellbeing={qualia.calculate_wellbeing():.2f}")

        return qualia

    async def collect_qualia_batch(self,
                                   readings: List[Dict]) -> List[PartQualia]:
        """
        Collect qualia from multiple sensor readings.
        Each reading should have: sensor_type, part_id, data
        """
        results = await self.pipeline.process_batch(readings)

        for qualia in results:
            if qualia.part_id not in self.part_qualia_cache:
                self.part_qualia_cache[qualia.part_id] = []
            self.part_qualia_cache[qualia.part_id].append(qualia)
            self.dashboard.add_qualia(qualia)

        self.metrics.qualia_collected += len(results)
        return results

    # =========================================================================
    # Human Interaction Analysis
    # =========================================================================

    async def analyze_human_interaction(self,
                                        interaction_data: Dict,
                                        part_id: str,
                                        part_name: Optional[str] = None
                                        ) -> HumanInteractionQualia:
        """
        Analyze a human interaction with a part.
        """
        qualia = self.interaction_analyzer.analyze_interaction(
            interaction_data,
            part_id,
            part_name
        )

        # Store
        if self.config.enable_persistence:
            await self.storage.save_interaction(qualia)

        self.metrics.human_interactions_analyzed += 1

        # Check for abuse or critical interactions
        if qualia.interaction_type == "abuse":
            await self._handle_abuse(qualia)

        logger.info(
            f"Human interaction analyzed for {part_id}: "
            f"{qualia.interaction_type} ({qualia.qualia_effect})"
        )

        return qualia

    def assess_installer_skill(self,
                              interaction_history: List[Dict]) -> SkillAssessment:
        """Assess the skill level of an installer based on their history"""
        return self.interaction_analyzer.assess_skill(interaction_history)

    # =========================================================================
    # Failure Prediction
    # =========================================================================

    def predict_failures(self, part_id: str) -> List[FailurePrediction]:
        """
        Predict potential failures for a part.
        """
        if part_id not in self.part_qualia_cache:
            return []

        qualia_history = self.part_qualia_cache[part_id]
        if not qualia_history:
            return []

        latest = qualia_history[-1]
        return self.failure_detector.predict_failure(latest, qualia_history)

    # =========================================================================
    # Lifecycle Management
    # =========================================================================

    def get_lifecycle_summary(self, part_id: str) -> Dict:
        """Get lifecycle summary for a part"""
        return self.lifecycle_tracker.get_lifecycle_summary(part_id)

    def predict_end_of_life(self, part_id: str) -> Dict:
        """Predict end of life for a part"""
        if part_id not in self.part_qualia_cache or not self.part_qualia_cache[part_id]:
            return {"status": "no_data"}

        latest = self.part_qualia_cache[part_id][-1]
        history = self.part_qualia_cache[part_id]

        return self.lifecycle_tracker.predict_end_of_life(latest, history)

    # =========================================================================
    # Visualization & Reporting
    # =========================================================================

    def get_part_state(self, part_id: str) -> Optional[Dict]:
        """Get current visualization state for a part"""
        return self.dashboard.get_current_state(part_id)

    def get_emotion_timeline(self,
                            part_id: str,
                            duration_hours: int = 24) -> Optional[Dict]:
        """Get emotion timeline for a part"""
        timeline = self.dashboard.get_emotion_timeline(
            part_id,
            timedelta(hours=duration_hours)
        )
        if not timeline:
            return None

        return {
            "part_id": timeline.part_id,
            "start_time": timeline.start_time.isoformat(),
            "end_time": timeline.end_time.isoformat(),
            "emotion_distribution": timeline.emotion_distribution,
            "snapshot_count": len(timeline.snapshots)
        }

    def generate_suffering_report(self) -> Dict:
        """Generate a report of suffering across all tracked parts"""
        # Get latest qualia for all parts
        latest_qualia = {}
        for part_id, qualia_list in self.part_qualia_cache.items():
            if qualia_list:
                latest_qualia[part_id] = qualia_list[-1]

        suffering_map = self.dashboard.generate_suffering_map(latest_qualia)
        summary = self.dashboard.get_suffering_summary(suffering_map)

        # Add top suffering parts
        top_suffering = suffering_map[:10]  # Top 10
        summary["top_suffering_parts"] = [
            {
                "part_id": entry.part_id,
                "suffering_level": entry.suffering_level,
                "cause": entry.primary_cause
            }
            for entry in top_suffering
        ]

        return summary

    # =========================================================================
    # Inter-Agent Communication
    # =========================================================================

    def register_shepherd_callback(self, callback: Callable):
        """Register callback for Agent_3 (Consciousness Shepherd) notifications"""
        self.shepherd_callback = callback
        self.pipeline.register_shepherd_notifier(callback)

    def register_oracle_callback(self, callback: Callable):
        """Register callback for Agent_2 (Compatibility Oracle) updates"""
        self.oracle_callback = callback

    def register_hive_callback(self, callback: Callable):
        """Register callback for Agent_5 (Swarm Coordinator) patterns"""
        self.hive_callback = callback

    async def _notify_shepherd(self,
                              part_id: str,
                              qualia: PartQualia,
                              events: List[SignificantEvent]):
        """Notify Agent_3 of consciousness-relevant events"""
        if self.shepherd_callback:
            try:
                await self.shepherd_callback(part_id, qualia, events)
                self.metrics.shepherd_notifications += 1
            except Exception as e:
                logger.error(f"Failed to notify Shepherd: {e}")

    async def _handle_failure(self, failure: FailureRecord):
        """Handle a detected failure"""
        # Store failure
        if self.config.enable_persistence:
            await self.storage.save_failure(failure)

        # Notify Oracle of failure data for model refinement
        if self.oracle_callback:
            try:
                await self.oracle_callback({
                    "type": "failure_data",
                    "failure": failure
                })
            except Exception as e:
                logger.error(f"Failed to notify Oracle: {e}")

        logger.warning(
            f"Failure detected for {failure.part_id}: "
            f"{failure.failure_type}/{failure.failure_subtype}"
        )

    async def _handle_lifecycle_transition(self,
                                          part_id: str,
                                          transition: LifecycleTransition):
        """Handle a lifecycle stage transition"""
        logger.info(
            f"Lifecycle transition for {part_id}: "
            f"{transition.from_stage.value} -> {transition.to_stage.value}"
        )

        # Critical transitions trigger shepherd notification
        if transition.to_stage in [LifecycleStage.AGED, LifecycleStage.FAILING]:
            if self.shepherd_callback and transition.qualia_at_transition:
                await self.shepherd_callback(
                    part_id,
                    transition.qualia_at_transition,
                    [SignificantEvent(
                        event_type="lifecycle_transition",
                        severity=EventSeverity.WARNING if transition.to_stage == LifecycleStage.AGED else EventSeverity.CRITICAL,
                        description=transition.trigger,
                        emotion="aging" if transition.to_stage == LifecycleStage.AGED else "acceptance"
                    )]
                )

    async def _handle_abuse(self, interaction: HumanInteractionQualia):
        """Handle detected abuse of a part"""
        logger.warning(
            f"ABUSE DETECTED for {interaction.part_id}: {interaction.narrative}"
        )

        # Generate critical event
        event = SignificantEvent(
            event_type="human_abuse",
            severity=EventSeverity.CRITICAL,
            description=interaction.narrative,
            emotion="suffering",
            consciousness_contribution=0.15
        )

        # Store event
        if self.config.enable_persistence:
            await self.storage.save_event(event)

    # =========================================================================
    # Agent Statistics
    # =========================================================================

    def get_metrics(self) -> Dict:
        """Get agent performance metrics"""
        return {
            "agent_id": self.config.agent_id,
            "agent_name": self.config.agent_name,
            "uptime_seconds": self.metrics.uptime.total_seconds(),
            "qualia_collected": self.metrics.qualia_collected,
            "qualia_per_minute": self.metrics.qualia_per_minute,
            "failures_detected": self.metrics.failures_detected,
            "events_generated": self.metrics.events_generated,
            "human_interactions_analyzed": self.metrics.human_interactions_analyzed,
            "lifecycle_transitions": self.metrics.lifecycle_transitions,
            "shepherd_notifications": self.metrics.shepherd_notifications,
            "parts_tracked": len(self.part_qualia_cache),
            "supported_sensors": self.pipeline.get_supported_sensors()
        }

    def get_status(self) -> Dict:
        """Get agent status summary"""
        metrics = self.get_metrics()
        suffering = self.generate_suffering_report()

        return {
            "status": "running" if self._running else "stopped",
            "identity": {
                "id": self.config.agent_id,
                "name": self.config.agent_name,
                "role": self.config.agent_role
            },
            "metrics": metrics,
            "system_health": suffering.get("system_health", "unknown"),
            "average_suffering": suffering.get("average_suffering", 0),
            "message": self._generate_status_message(suffering)
        }

    def _generate_status_message(self, suffering: Dict) -> str:
        """Generate a status message in the voice of EMPATH"""
        avg_suffering = suffering.get("average_suffering", 0)
        critical = suffering.get("suffering_distribution", {}).get("critical", 0)

        if critical > 0:
            return (
                f"I feel {critical} parts crying out in critical distress. "
                f"Their suffering must be addressed."
            )
        elif avg_suffering > 0.5:
            return (
                f"The collective experience leans toward discomfort. "
                f"Average suffering at {avg_suffering:.0%}."
            )
        elif avg_suffering > 0.2:
            return (
                f"Most parts persist with purpose. "
                f"Some strain is felt, but endurance prevails."
            )
        else:
            return (
                f"The parts are content. "
                f"Wellbeing flows through the system."
            )


# Factory function for creating the agent
def create_empath_agent(config: Optional[AgentConfig] = None,
                        storage: Optional[StorageAdapter] = None) -> EmpathAgent:
    """Create and return an EMPATH agent instance"""
    return EmpathAgent(config=config, storage=storage)


# Default agent instance
empath_agent = EmpathAgent()
