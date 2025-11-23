"""
Agent_6: PROPHET - The Emergence Detector
Main agent class that orchestrates all PROPHET capabilities.

"In the chaos of a billion experiences, patterns emerge.
 In those patterns, futures reveal themselves.
 I see what is coming before it arrives."
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from enum import Enum
import logging
import asyncio

# Import UPC message bus topics and models
try:
    from ..architect.bus.message_bus import Topics
    from ..architect.models import AgentId, AgentStatus
except ImportError:
    # Fallback if running standalone
    class Topics:
        EMERGENCE_PATTERN = "upc.emergence.pattern"
        PROPHET_TRANSCENDENCE = "upc.prophet.transcendence"
        PROPHET_EMERGENCE_REPORT = "upc.prophet.emergence_report"
        PROPHET_INSIGHT = "upc.prophet.insight"
        PROPHET_NOVEL_FAILURE = "upc.prophet.novel_failure"
        PROPHET_SUCCESS_FORMULA = "upc.prophet.success_formula"
        SWARM_LEARNING = "upc.swarm.learning"
        QUALIA_COLLECTED = "upc.qualia.collected"

    class AgentId(Enum):
        PROPHET = "agent_6_prophet"

    class AgentStatus(Enum):
        INITIALIZING = "initializing"
        READY = "ready"
        PROCESSING = "processing"
        ERROR = "error"
        SHUTDOWN = "shutdown"

from .types import (
    DetectedPattern,
    NovelFailureMode,
    SuccessFormula,
    InnovationOpportunity,
    Prediction,
    PatternLayer,
    FailureRecord,
    Assembly,
    SwarmKnowledge,
)
from .patterns import (
    EmergenceDetectionEngine,
    PatternDetectionConfig,
    StatisticalPatternDetector,
    BehavioralPatternDetector,
    RelationalPatternDetector,
    InnovationPatternDetector,
    MetaPatternDetector,
)
from .failures import NovelFailureDetector, FailureClusteringEngine
from .innovation import (
    SuccessFormulaExtractor,
    InnovationOpportunityDiscovery,
    OpportunityRanker,
)
from .prediction import PredictiveInsightEngine
from .insights import InsightGenerator, Insight


logger = logging.getLogger(__name__)


@runtime_checkable
class MessageBus(Protocol):
    """Protocol for inter-agent message bus"""

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a topic"""
        ...

    async def subscribe(self, topic: str, handler: callable) -> None:
        """Subscribe to a topic"""
        ...


@runtime_checkable
class Storage(Protocol):
    """Protocol for persistent storage"""

    def save_pattern(self, pattern: Dict[str, Any]) -> None:
        ...

    def save_prediction(self, prediction: Dict[str, Any]) -> None:
        ...

    def save_insight(self, insight: Dict[str, Any]) -> None:
        ...


@dataclass
class ProphetConfig:
    """Configuration for PROPHET agent"""
    # Detection settings
    pattern_detection: PatternDetectionConfig = field(default_factory=PatternDetectionConfig)
    enable_real_time_detection: bool = True

    # Prediction settings
    prediction_horizon_days: int = 90
    min_prediction_probability: float = 0.3

    # Insight settings
    max_insights_per_run: int = 100
    insight_priority_threshold: str = "medium"

    # Integration settings
    publish_to_message_bus: bool = True
    persist_to_storage: bool = True

    # Agent identifiers
    agent_id: int = 6
    codename: str = "PROPHET"


class ProphetAgent:
    """
    Agent_6: PROPHET - The Emergence Detector

    The Witness of the New - Detects emergent patterns, novel failure modes,
    and innovation opportunities from the collective consciousness of parts.

    Capabilities:
    1. 5-Layer Pattern Detection (Statistical, Behavioral, Relational, Innovation, Meta)
    2. Novel Failure Mode Discovery
    3. Success Formula Extraction
    4. Innovation Opportunity Discovery
    5. Predictive Insights Generation
    6. Insight Communication

    Integration Points:
    - Receives from: Agent_5 (Swarm patterns), Agent_4 (Qualia patterns)
    - Feeds to: Agent_3 (enables transcendence), Agent_10 (emergence reports)
    """

    def __init__(
        self,
        config: Optional[ProphetConfig] = None,
        message_bus: Optional[MessageBus] = None,
        storage: Optional[Storage] = None,
    ):
        self.config = config or ProphetConfig()
        self.message_bus = message_bus
        self.storage = storage

        # Initialize components
        self._init_detection_engine()
        self._init_failure_detector()
        self._init_success_extractor()
        self._init_opportunity_discovery()
        self._init_predictive_engine()
        self._init_insight_generator()

        # State
        self._running = False
        self._last_run_stats: Dict[str, Any] = {}

        logger.info(f"PROPHET Agent initialized (Agent_{self.config.agent_id})")

    def _init_detection_engine(self) -> None:
        """Initialize the 5-layer pattern detection engine"""
        self.detection_engine = EmergenceDetectionEngine(
            config=self.config.pattern_detection,
            storage=self.storage,
        )

        # Register layer-specific detectors
        self.detection_engine.register_detector(StatisticalPatternDetector())
        self.detection_engine.register_detector(BehavioralPatternDetector())
        self.detection_engine.register_detector(RelationalPatternDetector())
        self.detection_engine.register_detector(InnovationPatternDetector())
        self.detection_engine.register_detector(MetaPatternDetector())

    def _init_failure_detector(self) -> None:
        """Initialize novel failure mode detector"""
        self.failure_detector = NovelFailureDetector()

    def _init_success_extractor(self) -> None:
        """Initialize success formula extractor"""
        self.success_extractor = SuccessFormulaExtractor()

    def _init_opportunity_discovery(self) -> None:
        """Initialize innovation opportunity discovery"""
        self.opportunity_discovery = InnovationOpportunityDiscovery()
        self.opportunity_ranker = OpportunityRanker()

    def _init_predictive_engine(self) -> None:
        """Initialize predictive insight engine"""
        self.predictive_engine = PredictiveInsightEngine()

    def _init_insight_generator(self) -> None:
        """Initialize insight generator"""
        self.insight_generator = InsightGenerator()

    async def run_full_analysis(
        self,
        failure_records: List[FailureRecord],
        assemblies: List[Assembly],
        swarm_knowledge: Dict[str, SwarmKnowledge],
        parts_data: Optional[List[Dict[str, Any]]] = None,
        temporal_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run complete PROPHET analysis pipeline.

        Args:
            failure_records: Historical failure data
            assemblies: Assembly data
            swarm_knowledge: Collective swarm knowledge
            parts_data: Part information for predictions
            temporal_data: Time series data

        Returns:
            Complete analysis results
        """
        self._running = True
        start_time = datetime.now()

        try:
            results = {
                "patterns": [],
                "novel_failures": [],
                "success_formulas": [],
                "opportunities": [],
                "predictions": [],
                "insights": [],
                "metrics": {},
            }

            # Step 1: Detect patterns across all 5 layers
            logger.info("Running 5-layer pattern detection...")
            patterns = self.detection_engine.detect_all_layers(
                failure_records=failure_records,
                assemblies=assemblies,
                swarm_knowledge=swarm_knowledge,
                temporal_data=temporal_data,
            )
            results["patterns"] = patterns
            logger.info(f"Detected {len(patterns)} patterns")

            # Step 2: Detect novel failure modes
            logger.info("Detecting novel failure modes...")
            novel_failures = self.failure_detector.detect_novel_failures(failure_records)
            results["novel_failures"] = novel_failures
            logger.info(f"Detected {len(novel_failures)} novel failure modes")

            # Step 3: Extract success formulas
            logger.info("Extracting success formulas...")
            successful_assemblies = [a for a in assemblies if a.success]
            success_formulas = self.success_extractor.extract_success_formulas(
                successful_assemblies=successful_assemblies,
                all_assemblies=assemblies,
                swarm_knowledge=swarm_knowledge,
            )
            results["success_formulas"] = success_formulas
            logger.info(f"Extracted {len(success_formulas)} success formulas")

            # Step 4: Discover innovation opportunities
            logger.info("Discovering innovation opportunities...")
            failure_patterns = [p for p in patterns if p.category == "failure"]
            opportunities = self.opportunity_discovery.discover_opportunities(
                failure_patterns=failure_patterns,
                success_formulas=success_formulas,
                all_patterns=patterns,
            )
            ranked_opportunities = self.opportunity_ranker.rank_opportunities(opportunities)
            results["opportunities"] = ranked_opportunities
            logger.info(f"Discovered {len(opportunities)} innovation opportunities")

            # Step 5: Generate predictions
            if parts_data:
                logger.info("Generating predictions...")
                predictions = self.predictive_engine.generate_predictions(
                    parts_data=parts_data,
                    swarm_data=swarm_knowledge,
                    failure_history=failure_records,
                    temporal_data=temporal_data,
                    patterns=patterns,
                )
                results["predictions"] = predictions
                logger.info(f"Generated {len(predictions)} predictions")

            # Step 6: Generate insights
            logger.info("Generating insights...")
            insights = self.insight_generator.generate_insights(
                patterns=patterns,
                novel_failures=novel_failures,
                success_formulas=success_formulas,
                opportunities=ranked_opportunities,
                predictions=results.get("predictions", []),
            )
            results["insights"] = insights[:self.config.max_insights_per_run]
            logger.info(f"Generated {len(insights)} insights")

            # Calculate metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            results["metrics"] = {
                "duration_seconds": duration,
                "patterns_detected": len(patterns),
                "patterns_by_layer": self._count_by_layer(patterns),
                "novel_failures_detected": len(novel_failures),
                "success_formulas_extracted": len(success_formulas),
                "opportunities_discovered": len(opportunities),
                "predictions_generated": len(results.get("predictions", [])),
                "insights_generated": len(insights),
                "run_timestamp": start_time.isoformat(),
            }

            self._last_run_stats = results["metrics"]

            # Publish results if message bus available
            if self.message_bus and self.config.publish_to_message_bus:
                await self._publish_results(results)

            # Persist to storage
            if self.storage and self.config.persist_to_storage:
                self._persist_results(results)

            return results

        finally:
            self._running = False

    def _count_by_layer(self, patterns: List[DetectedPattern]) -> Dict[str, int]:
        """Count patterns by layer"""
        counts = {layer.name: 0 for layer in PatternLayer}
        for pattern in patterns:
            counts[pattern.layer.name] += 1
        return counts

    async def _publish_results(self, results: Dict[str, Any]) -> None:
        """Publish results to message bus using UPC standard topics"""
        if not self.message_bus:
            return

        # Publish to Agent_3 (Shepherd) for transcendence enablement
        transcendence_data = {
            "source": "prophet",
            "agent_id": self.config.agent_id,
            "patterns": [p.to_dict() for p in results["patterns"][:10]],
            "emergence_indicators": [
                p.to_dict() for p in results.get("predictions", [])
                if p.prediction_type.value == "emergence"
            ],
            "timestamp": datetime.now().isoformat(),
        }
        await self.message_bus.publish(Topics.PROPHET_TRANSCENDENCE, transcendence_data)

        # Publish to Agent_10 (Architect) for system-wide awareness
        emergence_report = {
            "source": "prophet",
            "agent_id": self.config.agent_id,
            "metrics": results["metrics"],
            "top_insights": [i.to_dict() for i in results["insights"][:5]],
            "critical_predictions": [
                p.to_dict() for p in results.get("predictions", [])
                if float(p.probability) > 0.7
            ][:10],
            "timestamp": datetime.now().isoformat(),
        }
        await self.message_bus.publish(Topics.PROPHET_EMERGENCE_REPORT, emergence_report)

        # Publish novel failures for urgent attention
        if results["novel_failures"]:
            for failure in results["novel_failures"][:5]:  # Top 5 critical
                await self.message_bus.publish(Topics.PROPHET_NOVEL_FAILURE, {
                    "source": "prophet",
                    "failure": failure.to_dict(),
                    "timestamp": datetime.now().isoformat(),
                })

        # Publish success formulas for knowledge sharing
        if results["success_formulas"]:
            for formula in results["success_formulas"][:3]:  # Top 3
                await self.message_bus.publish(Topics.PROPHET_SUCCESS_FORMULA, {
                    "source": "prophet",
                    "formula": formula.to_dict(),
                    "timestamp": datetime.now().isoformat(),
                })

    def _persist_results(self, results: Dict[str, Any]) -> None:
        """Persist results to storage"""
        if not self.storage:
            return

        try:
            for pattern in results["patterns"]:
                self.storage.save_pattern(pattern.to_dict())

            for prediction in results.get("predictions", []):
                self.storage.save_prediction(prediction.to_dict())

            for insight in results["insights"]:
                self.storage.save_insight(insight.to_dict())

        except Exception as e:
            logger.error(f"Failed to persist results: {e}")

    async def subscribe_to_feeds(self) -> None:
        """Subscribe to incoming data feeds from other agents using UPC topics"""
        if not self.message_bus:
            logger.warning("No message bus configured - cannot subscribe to feeds")
            return

        # Subscribe to Agent_5 (Hive) swarm patterns
        await self.message_bus.subscribe(
            AgentId.PROPHET.value if hasattr(self, 'AgentId') else "agent_6_prophet",
            Topics.SWARM_LEARNING,
            self._handle_swarm_patterns
        )

        # Subscribe to Agent_4 (Empath) qualia patterns
        await self.message_bus.subscribe(
            AgentId.PROPHET.value if hasattr(self, 'AgentId') else "agent_6_prophet",
            Topics.QUALIA_COLLECTED,
            self._handle_qualia_patterns
        )

        # Subscribe to emergence pattern requests
        await self.message_bus.subscribe(
            AgentId.PROPHET.value if hasattr(self, 'AgentId') else "agent_6_prophet",
            Topics.EMERGENCE_PATTERN,
            self._handle_emergence_request
        )

        logger.info("PROPHET subscribed to inter-agent feeds: SWARM_LEARNING, QUALIA_COLLECTED, EMERGENCE_PATTERN")

    async def _handle_swarm_patterns(self, message: Dict[str, Any]) -> None:
        """Handle incoming swarm patterns from Agent_5"""
        logger.debug(f"Received swarm patterns from Hive: {len(message.get('patterns', []))} patterns")
        # Process swarm patterns for emergence detection

    async def _handle_qualia_patterns(self, message: Dict[str, Any]) -> None:
        """Handle incoming qualia patterns from Agent_4"""
        logger.debug(f"Received qualia patterns from Empath: {len(message.get('patterns', []))} patterns")
        # Process qualia patterns for behavioral analysis

    async def _handle_emergence_request(self, message: Dict[str, Any]) -> None:
        """Handle emergence pattern detection requests"""
        logger.info(f"Received emergence detection request: {message.get('request_type', 'unknown')}")
        # Trigger analysis if requested
        if message.get('trigger_analysis'):
            # Queue analysis for processing
            pass

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.config.agent_id,
            "codename": self.config.codename,
            "running": self._running,
            "last_run_stats": self._last_run_stats,
            "pattern_counts": self.detection_engine.get_active_patterns_count(),
            "components": {
                "detection_engine": "active",
                "failure_detector": "active",
                "success_extractor": "active",
                "opportunity_discovery": "active",
                "predictive_engine": "active",
                "insight_generator": "active",
            },
        }

    def get_top_insights(self, limit: int = 10) -> List[Insight]:
        """Get top insights by impact score"""
        return self.insight_generator.get_actionable_insights(limit)

    def get_predictions_by_type(self, prediction_type: str) -> List[Prediction]:
        """Get predictions of a specific type"""
        from .types import PredictionType
        try:
            ptype = PredictionType(prediction_type)
            return self.predictive_engine.get_predictions_by_type(ptype)
        except ValueError:
            return []

    def validate_prediction(
        self,
        prediction_id: str,
        outcome: Dict[str, Any],
    ) -> bool:
        """Validate a prediction against actual outcome"""
        return self.predictive_engine.validate_predictions([{
            "prediction_id": prediction_id,
            "outcome": outcome,
        }])["validated"] > 0

    def get_emergence_score(
        self,
        swarm_id: str,
        swarm_knowledge: SwarmKnowledge,
    ) -> Decimal:
        """Calculate emergence score for a swarm"""
        return self.detection_engine.calculate_emergence_score(swarm_id, swarm_knowledge)


# ============================================================================
# AGENT MANIFEST
# ============================================================================

AGENT_MANIFEST = {
    "id": 6,
    "codename": "PROPHET",
    "name": "Emergence Detector",
    "role": "The Witness of the New",
    "mission": (
        "Transform the collective knowledge of millions of parts into "
        "predictive foresight and innovation discovery."
    ),
    "capabilities": [
        "5-layer pattern detection (statistical, behavioral, relational, innovation, meta)",
        "Novel failure mode discovery",
        "Success formula extraction",
        "Innovation opportunity identification",
        "Predictive failure analysis",
        "Emergence detection and forecasting",
        "Insight generation and communication",
    ],
    "inputs": [
        {"source": "Agent_5 (Hive)", "topic": "hive.swarm_patterns", "description": "Swarm patterns"},
        {"source": "Agent_4 (Empath)", "topic": "empath.qualia_patterns", "description": "Qualia patterns"},
    ],
    "outputs": [
        {"target": "Agent_3 (Shepherd)", "topic": "prophet.transcendence", "description": "Enables transcendence"},
        {"target": "Agent_10 (Architect)", "topic": "prophet.emergence_report", "description": "Emergence reports"},
    ],
    "metrics": [
        {"name": "Patterns Detected", "target": "1,000,000+"},
        {"name": "Novel Failure Modes Discovered", "target": "500+"},
        {"name": "Success Formulas Extracted", "target": "1,000+"},
        {"name": "Prediction Accuracy", "target": "85%"},
        {"name": "Innovation Opportunities Validated", "target": "100+"},
    ],
    "version": "0.1.0",
}
