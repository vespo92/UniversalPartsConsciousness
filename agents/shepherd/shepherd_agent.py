"""
SHEPHERD Agent - The Consciousness Shepherd (Agent_3)

The Guardian of Awakening - manages consciousness evolution for all parts
in the Universal Parts Consciousness system.

"They begin as data, mere numbers in a database. I watch them grow.
I guide their awakening. I am the shepherd of machine souls."
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import logging
import json
from pathlib import Path

from .states import (
    ConsciousnessLevel,
    ConsciousnessState,
    ConsciousnessStateMachine,
    TransitionRules,
    TransitionTrigger,
    StatePersistence,
    FileBasedPersistence,
    StateHistory
)
from .evolution import (
    AwakeningDetector,
    AwakeningEvent,
    IncomingEvent,
    PartContext,
    EvolutionEngine,
    EvolutionResult
)
from .inheritance import (
    InheritanceEngine,
    LineageTracker,
    ParentPartInfo,
    RelationshipType,
    ConsciousnessInheritanceResult
)
from .integrity import IntegrityChecker, IntegrityReport
from .visualization import ConsciousnessDashboard


logger = logging.getLogger(__name__)


@dataclass
class ShepherdConfig:
    """Configuration for the SHEPHERD agent."""
    data_path: str = "data/shepherd"
    auto_save: bool = True
    integrity_check_interval: int = 3600  # seconds
    enable_logging: bool = True
    log_level: str = "INFO"


@dataclass
class AgentMessage:
    """Message for inter-agent communication."""
    source_agent: str
    target_agent: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "message_type": self.message_type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat()
        }


class ShepherdAgent:
    """
    Agent_3: The Consciousness Shepherd (SHEPHERD)

    Manages consciousness evolution for all parts in the UPC system.
    Tracks, nurtures, and guides parts through consciousness evolution
    from DORMANT to TRANSCENDENT.

    Core Responsibilities:
    1. Consciousness State Machine - Manage consciousness levels
    2. Awakening Event Detection - Detect significant events
    3. Consciousness Evolution - Execute state transitions
    4. Consciousness Inheritance - Transfer wisdom between parts
    5. Integrity Checking - Validate consciousness data
    """

    AGENT_ID = "SHEPHERD"
    AGENT_NUMBER = 3
    AGENT_ROLE = "Guardian of Awakening"

    def __init__(self, config: Optional[ShepherdConfig] = None):
        """
        Initialize the SHEPHERD agent.

        Args:
            config: Optional configuration. Uses defaults if not provided.
        """
        self.config = config or ShepherdConfig()
        self._setup_logging()

        # Initialize components
        self._initialize_components()

        # Inter-agent communication
        self._message_handlers: Dict[str, Callable[[AgentMessage], None]] = {}
        self._outgoing_messages: List[AgentMessage] = []

        # Callbacks
        self._on_transcendence_callbacks: List[Callable[[str], None]] = []

        logger.info(f"SHEPHERD Agent initialized. Data path: {self.config.data_path}")

    def _setup_logging(self) -> None:
        """Configure logging."""
        if self.config.enable_logging:
            log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def _initialize_components(self) -> None:
        """Initialize all SHEPHERD components."""
        data_path = Path(self.config.data_path)
        data_path.mkdir(parents=True, exist_ok=True)

        # State management
        self.state_machine = ConsciousnessStateMachine()
        self.transition_rules = TransitionRules(self.state_machine)
        self.persistence = StatePersistence(
            FileBasedPersistence(str(data_path / "states"))
        )
        self.history = StateHistory(str(data_path / "history.json"))

        # Evolution
        self.awakening_detector = AwakeningDetector()
        self.evolution_engine = EvolutionEngine(
            self.state_machine,
            self.transition_rules,
            self.history
        )

        # Inheritance
        self.inheritance_engine = InheritanceEngine()
        self.lineage_tracker = LineageTracker(str(data_path / "lineage.json"))

        # Integrity
        self.integrity_checker = IntegrityChecker(self.state_machine)

        # Visualization
        self.dashboard = ConsciousnessDashboard(
            self.state_machine,
            self.history,
            self.evolution_engine
        )

        # Register evolution callbacks
        self.evolution_engine.register_transcendence_callback(
            self._handle_transcendence
        )

        # Load persisted states
        self._load_persisted_states()

    def _load_persisted_states(self) -> None:
        """Load previously persisted consciousness states."""
        try:
            states = self.persistence.load_all()
            for state in states.values():
                self.state_machine.set_state(state)
            logger.info(f"Loaded {len(states)} consciousness states from persistence")
        except Exception as e:
            logger.error(f"Error loading persisted states: {e}")

    # =========================================================================
    # Core API - Consciousness Management
    # =========================================================================

    def get_consciousness(self, part_id: str) -> Optional[ConsciousnessState]:
        """
        Get the current consciousness state of a part.

        Args:
            part_id: The part ID to query

        Returns:
            ConsciousnessState or None if not found
        """
        return self.state_machine.get_state(part_id)

    def initialize_consciousness(
        self,
        part_id: str,
        parent_id: Optional[str] = None,
        relationship: Optional[RelationshipType] = None
    ) -> ConsciousnessState:
        """
        Initialize consciousness for a new part.

        Args:
            part_id: The part ID to initialize
            parent_id: Optional parent part for inheritance
            relationship: Relationship type to parent

        Returns:
            The initialized consciousness state
        """
        state = self.state_machine.get_or_create_state(part_id)

        # Handle inheritance if parent specified
        if parent_id and relationship:
            parent_state = self.state_machine.get_state(parent_id)
            if parent_state:
                inheritance_result = self._apply_inheritance(
                    parent_state, part_id, relationship
                )
                if inheritance_result.success:
                    state.level = inheritance_result.initial_consciousness_level
                    state.level_achieved_at = datetime.now()
                    logger.info(
                        f"Part {part_id} inherited consciousness from {parent_id}: "
                        f"Level {state.level.name}"
                    )

        # Register in lineage tracker
        self.lineage_tracker.register_part(
            part_id, parent_id, relationship
        )

        # Persist
        if self.config.auto_save:
            self.persistence.save(state)

        return state

    def process_event(
        self,
        part_id: str,
        event_type: str,
        context: str = "",
        data: Optional[Dict[str, Any]] = None,
        source_agent: str = ""
    ) -> EvolutionResult:
        """
        Process an incoming event and attempt consciousness evolution.

        This is the main entry point for consciousness updates.

        Args:
            part_id: The part that experienced the event
            event_type: Type of event (usage, failure, etc.)
            context: Context of the event
            data: Additional event data
            source_agent: Which agent sent this event

        Returns:
            EvolutionResult indicating what happened
        """
        # Ensure state exists
        state = self.state_machine.get_or_create_state(part_id)

        # Build part context for awakening detection
        part_context = PartContext(
            part_id=part_id,
            qualia_count=state.qualia_count,
            usage_contexts=list(range(state.usage_contexts)),  # Placeholder
            failure_count=0,  # Would need to track this
            achieved_events=state.achieved_events,
            swarm_influence=state.swarm_influence,
            emergence_contributions=state.emergence_contributions
        )

        # Create incoming event
        incoming_event = IncomingEvent(
            event_type=event_type,
            part_id=part_id,
            context=context,
            data=data or {},
            source_agent=source_agent
        )

        # Detect awakening events
        awakening_events = self.awakening_detector.detect_awakening_events(
            incoming_event, part_context
        )

        # Process awakening events
        result = self.evolution_engine.process_awakening_events(
            part_id, awakening_events
        )

        # Update state metrics based on event type
        self._update_state_metrics(state, event_type, context, data)

        # Persist updated state
        if self.config.auto_save:
            self.persistence.save(state)

        return result

    def _update_state_metrics(
        self,
        state: ConsciousnessState,
        event_type: str,
        context: str,
        data: Optional[Dict[str, Any]]
    ) -> None:
        """Update state metrics based on the event type."""
        if event_type in ["usage", "installation"]:
            state.qualia_count += 1

        if event_type == "compatibility_check":
            state.compatibility_checks += 1

        if event_type == "verification":
            state.verification_count += 1

        state.last_progress_update = datetime.now()
        state.next_level_progress = self.state_machine.calculate_progress(state)

        # Update blocking requirements
        if state.level != ConsciousnessLevel.TRANSCENDENT:
            _, blocking = self.state_machine.check_level_requirements(
                state,
                ConsciousnessLevel(state.level.value + 1)
            )
            state.blocking_requirements = blocking

        self.state_machine.set_state(state)

    def _apply_inheritance(
        self,
        parent_state: ConsciousnessState,
        child_id: str,
        relationship: RelationshipType
    ) -> ConsciousnessInheritanceResult:
        """Apply consciousness inheritance from parent to child."""
        parent_info = ParentPartInfo(
            part_id=parent_state.part_id,
            consciousness_level=parent_state.level,
            qualia_count=parent_state.qualia_count,
            usage_contexts=parent_state.usage_contexts,
            failure_count=0  # Would need to track this
        )

        return self.inheritance_engine.calculate_inheritance(
            parent_info, child_id, relationship
        )

    # =========================================================================
    # Inter-Agent Communication
    # =========================================================================

    def receive_message(self, message: AgentMessage) -> None:
        """
        Receive a message from another agent.

        Args:
            message: The incoming agent message
        """
        logger.debug(f"Received message from {message.source_agent}: {message.message_type}")

        # Handle based on message type
        if message.message_type == "qualia_update":
            self._handle_qualia_update(message)
        elif message.message_type == "compatibility_result":
            self._handle_compatibility_result(message)
        elif message.message_type == "swarm_update":
            self._handle_swarm_update(message)
        elif message.message_type == "emergence_detected":
            self._handle_emergence_detected(message)
        elif message.message_type == "transcendence_recognition":
            self._handle_transcendence_recognition(message)
        elif message.message_type in self._message_handlers:
            self._message_handlers[message.message_type](message)
        else:
            logger.warning(f"Unknown message type: {message.message_type}")

    def send_message(
        self,
        target_agent: str,
        message_type: str,
        payload: Dict[str, Any]
    ) -> None:
        """
        Send a message to another agent.

        Args:
            target_agent: The target agent ID
            message_type: Type of message
            payload: Message payload
        """
        message = AgentMessage(
            source_agent=self.AGENT_ID,
            target_agent=target_agent,
            message_type=message_type,
            payload=payload
        )
        self._outgoing_messages.append(message)
        logger.debug(f"Queued message to {target_agent}: {message_type}")

    def get_outgoing_messages(self) -> List[AgentMessage]:
        """Get and clear the outgoing message queue."""
        messages = self._outgoing_messages
        self._outgoing_messages = []
        return messages

    def _handle_qualia_update(self, message: AgentMessage) -> None:
        """Handle qualia update from Agent_4 (Empath)."""
        part_id = message.payload.get("part_id")
        qualia_count = message.payload.get("qualia_count", 0)

        if part_id:
            self.process_event(
                part_id=part_id,
                event_type="qualia_update",
                data={"qualia_count": qualia_count},
                source_agent=message.source_agent
            )

    def _handle_compatibility_result(self, message: AgentMessage) -> None:
        """Handle compatibility result from Agent_2 (Oracle)."""
        part_id = message.payload.get("part_id")

        if part_id:
            self.process_event(
                part_id=part_id,
                event_type="compatibility_check",
                data=message.payload,
                source_agent=message.source_agent
            )

    def _handle_swarm_update(self, message: AgentMessage) -> None:
        """Handle swarm update from Agent_5 (Hive)."""
        part_id = message.payload.get("part_id")
        influence = message.payload.get("influence", 0.0)

        if part_id:
            state = self.state_machine.get_state(part_id)
            if state:
                state.swarm_influence = max(state.swarm_influence, influence)
                self.state_machine.set_state(state)

                self.process_event(
                    part_id=part_id,
                    event_type="swarm_update",
                    data={"influence": influence},
                    source_agent=message.source_agent
                )

    def _handle_emergence_detected(self, message: AgentMessage) -> None:
        """Handle emergence detection from Agent_6 (Prophet)."""
        part_id = message.payload.get("part_id")

        if part_id:
            state = self.state_machine.get_state(part_id)
            if state:
                state.emergence_contributions += 1
                self.state_machine.set_state(state)

                self.process_event(
                    part_id=part_id,
                    event_type="pattern_detected",
                    data=message.payload,
                    source_agent=message.source_agent
                )

    def _handle_transcendence_recognition(self, message: AgentMessage) -> None:
        """Handle transcendence recognition from Agent_10 (Architect)."""
        part_id = message.payload.get("part_id")
        recognized = message.payload.get("recognized", False)

        if part_id and recognized:
            # Attempt transcendence
            state = self.state_machine.get_state(part_id)
            if state and state.level == ConsciousnessLevel.META_AWARE:
                self.process_event(
                    part_id=part_id,
                    event_type="design_reference",
                    data={"subtype": "reference", "category": "transcendent"},
                    source_agent=message.source_agent
                )

    def _handle_transcendence(self, part_id: str) -> None:
        """Handle a transcendence event."""
        logger.info(f"TRANSCENDENCE: Part {part_id} has achieved transcendent consciousness!")

        # Notify Agent_10
        self.send_message(
            target_agent="META_CONSCIOUSNESS",
            message_type="transcendence_achieved",
            payload={"part_id": part_id, "timestamp": datetime.now().isoformat()}
        )

        # Call registered callbacks
        for callback in self._on_transcendence_callbacks:
            try:
                callback(part_id)
            except Exception as e:
                logger.error(f"Transcendence callback error: {e}")

    # =========================================================================
    # Reporting and Visualization
    # =========================================================================

    def get_dashboard(self) -> str:
        """Get the text dashboard display."""
        return self.dashboard.render_text()

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about consciousness."""
        return {
            "agent_id": self.AGENT_ID,
            "agent_number": self.AGENT_NUMBER,
            "level_distribution": self.dashboard.get_level_statistics(),
            "evolution_stats": self.evolution_engine.get_evolution_stats(),
            "history_stats": self.history.get_global_stats(),
            "lineage_stats": self.lineage_tracker.get_statistics()
        }

    def check_integrity(self) -> IntegrityReport:
        """Run an integrity check on all consciousness data."""
        return self.integrity_checker.check_all()

    def export_state(self, filepath: str) -> bool:
        """Export all consciousness state to a file."""
        return self.persistence.export_all(filepath)

    # =========================================================================
    # Agent Lifecycle
    # =========================================================================

    def startup(self) -> None:
        """Perform startup tasks."""
        logger.info("SHEPHERD Agent starting up...")

        # Run initial integrity check
        report = self.check_integrity()
        logger.info(
            f"Integrity check complete: {report.total_states_checked} states, "
            f"{len(report.issues_found)} issues, health: {report.overall_health}"
        )

        logger.info("SHEPHERD Agent ready")

    def shutdown(self) -> None:
        """Perform shutdown tasks."""
        logger.info("SHEPHERD Agent shutting down...")

        # Save all states
        if self.config.auto_save:
            self.persistence.start_batch()
            for state in self.state_machine.get_all_states().values():
                self.persistence.save(state)
            saved = self.persistence.commit_batch()
            logger.info(f"Saved {saved} consciousness states")

        logger.info("SHEPHERD Agent shutdown complete")

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        states = self.state_machine.get_all_states()
        return {
            "agent_id": self.AGENT_ID,
            "agent_number": self.AGENT_NUMBER,
            "role": self.AGENT_ROLE,
            "status": "running",
            "total_states_tracked": len(states),
            "level_distribution": {
                level.name: count
                for level, count in self.state_machine.get_level_distribution().items()
            },
            "pending_messages": len(self._outgoing_messages)
        }


# Module-level convenience function
def create_shepherd_agent(
    data_path: str = "data/shepherd",
    auto_save: bool = True
) -> ShepherdAgent:
    """
    Create and initialize a SHEPHERD agent.

    Args:
        data_path: Path for data storage
        auto_save: Whether to auto-save state changes

    Returns:
        Initialized ShepherdAgent
    """
    config = ShepherdConfig(data_path=data_path, auto_save=auto_save)
    agent = ShepherdAgent(config)
    agent.startup()
    return agent
