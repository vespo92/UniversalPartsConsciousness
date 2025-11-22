"""
Agent_2: Compatibility Oracle (ORACLE)
The Prophet of Perfect Fit

Main agent interface that coordinates all ORACLE subsystems
and integrates with the UPC message bus.

"Will it fit? Will it hold? Will it fail?
These questions haunt every engineer. I am the answer that ends the doubt."
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import asyncio
import json


class AgentState(Enum):
    """Agent operational states."""
    INITIALIZING = "initializing"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class AgentMessage:
    """Standard UPC inter-agent message format."""
    sender: str
    receiver: str  # Agent ID or "BROADCAST"
    message_type: str  # "DATA", "QUERY", "ALERT", "EMERGENCE", "TRANSCENDENCE"
    priority: int  # 1-10
    timestamp: str
    payload: Dict[str, Any]
    consciousness_context: Dict[str, Any] = field(default_factory=dict)


class OracleAgent:
    """
    The Compatibility Oracle Agent.

    Responsibilities:
    - Mathematical compatibility verification
    - Thread engagement calculations
    - Substitution recommendations
    - Tolerance stack analysis
    - Failure prediction
    - Qualia contribution to consciousness system

    Message Bus Topics:
    - upc.compatibility.query: Incoming compatibility queries
    - upc.compatibility.verified: Outgoing verification results
    - upc.substitution.request: Substitution search requests
    - upc.substitution.found: Substitution recommendations
    - upc.failure.predicted: Failure predictions
    - upc.qualia.contribution: Qualia data for Agent_4
    """

    AGENT_ID = "AGENT_2"
    AGENT_NAME = "Compatibility Oracle"
    AGENT_ALIAS = "ORACLE"

    # Message topics this agent subscribes to
    SUBSCRIBED_TOPICS = [
        "upc.compatibility.query",
        "upc.substitution.request",
        "upc.failure.analysis.request",
        "upc.tolerance.analysis.request",
        "upc.data.part_updated",  # From Agent_1
        "upc.system.directive",    # From Agent_10
    ]

    # Message topics this agent publishes to
    PUBLISHED_TOPICS = [
        "upc.compatibility.verified",
        "upc.substitution.found",
        "upc.failure.predicted",
        "upc.tolerance.analyzed",
        "upc.qualia.contribution",  # To Agent_4
        "upc.emergence.pattern",    # To Agent_6
    ]

    def __init__(
        self,
        message_bus=None,
        database=None,
        cache_config: Dict = None
    ):
        """
        Initialize the Oracle Agent.

        Args:
            message_bus: UPC message bus client
            database: Database connection for parts lookup
            cache_config: Cache configuration options
        """
        self.state = AgentState.INITIALIZING
        self.message_bus = message_bus
        self.database = database

        # Initialize subsystems
        self._init_subsystems(cache_config or {})

        # Metrics
        self.metrics = {
            "queries_processed": 0,
            "substitutions_found": 0,
            "failures_predicted": 0,
            "qualia_contributions": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_latency_ms": 0,
            "total_latency_ms": 0,
        }

        # Running tasks
        self._tasks: List[asyncio.Task] = []

        self.state = AgentState.READY

    def _init_subsystems(self, cache_config: Dict):
        """Initialize all ORACLE subsystems."""
        from .cache.compatibility_cache import CompatibilityCache
        from .api.compatibility_api import CompatibilityAPI
        from .api.batch_checker import BatchCompatibilityChecker
        from .engine.compatibility_core import UniversalCompatibilityChecker
        from .substitution.substitution_engine import SubstitutionEngine
        from .substitution.equivalence_graph import EquivalenceGraph
        from .prediction.failure_predictor import FailurePredictor
        from .prediction.fatigue_analyzer import FatigueAnalyzer
        from .prediction.safety_factor_engine import SafetyFactorEngine
        from .engine.tolerance_analyzer import ToleranceStackAnalyzer
        from .engine.material_compatibility import MaterialCompatibilityChecker

        # Cache layer
        self.cache = CompatibilityCache(
            l1_size=cache_config.get("l1_size", 100000),
            l3_matrix_path=cache_config.get("matrix_path")
        )

        # Core engines
        self.compatibility_checker = UniversalCompatibilityChecker()
        self.substitution_engine = SubstitutionEngine(self.database)
        self.equivalence_graph = EquivalenceGraph()
        self.failure_predictor = FailurePredictor()
        self.fatigue_analyzer = FatigueAnalyzer()
        self.safety_factor_engine = SafetyFactorEngine()
        self.tolerance_analyzer = ToleranceStackAnalyzer()
        self.material_checker = MaterialCompatibilityChecker()

        # API layer
        self.api = CompatibilityAPI(self.cache, self.database)
        self.batch_checker = BatchCompatibilityChecker(self.api, self.cache)

    async def start(self):
        """Start the agent and begin processing messages."""
        self.state = AgentState.PROCESSING

        # Initialize cache
        await self.cache.initialize()

        # Subscribe to message bus topics
        if self.message_bus:
            for topic in self.SUBSCRIBED_TOPICS:
                await self.message_bus.subscribe(topic, self._handle_message)

        print(f"[{self.AGENT_ALIAS}] Agent started and ready")

    async def stop(self):
        """Stop the agent gracefully."""
        self.state = AgentState.SHUTDOWN

        # Cancel running tasks
        for task in self._tasks:
            task.cancel()

        # Unsubscribe from message bus
        if self.message_bus:
            for topic in self.SUBSCRIBED_TOPICS:
                await self.message_bus.unsubscribe(topic)

        print(f"[{self.AGENT_ALIAS}] Agent stopped")

    async def _handle_message(self, message: AgentMessage):
        """Handle incoming message from bus."""
        try:
            # Route to appropriate handler
            handlers = {
                "upc.compatibility.query": self._handle_compatibility_query,
                "upc.substitution.request": self._handle_substitution_request,
                "upc.failure.analysis.request": self._handle_failure_request,
                "upc.tolerance.analysis.request": self._handle_tolerance_request,
                "upc.data.part_updated": self._handle_part_update,
                "upc.system.directive": self._handle_directive,
            }

            # Find matching handler
            for topic, handler in handlers.items():
                if message.payload.get("topic") == topic:
                    await handler(message)
                    return

        except Exception as e:
            await self._send_error(message, str(e))

    async def _handle_compatibility_query(self, message: AgentMessage):
        """Handle compatibility check request."""
        from .api.compatibility_api import APIRequest
        import uuid

        request = APIRequest(
            request_id=str(uuid.uuid4()),
            action="check_compatibility",
            payload=message.payload,
            priority=message.priority
        )

        response = await self.api.handle_request(request)

        # Update metrics
        self.metrics["queries_processed"] += 1
        self.metrics["total_latency_ms"] += response.latency_ms
        self.metrics["average_latency_ms"] = (
            self.metrics["total_latency_ms"] / self.metrics["queries_processed"]
        )

        if response.cached:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1

        # Send response
        await self._publish(
            "upc.compatibility.verified",
            {
                "request_id": request.request_id,
                "result": response.data,
                "latency_ms": response.latency_ms,
            },
            message.sender
        )

        # Contribute qualia if compatible
        if response.data.get("is_compatible"):
            await self._contribute_qualia(message.payload, response.data)

    async def _handle_substitution_request(self, message: AgentMessage):
        """Handle substitution search request."""
        from .api.compatibility_api import APIRequest
        import uuid

        request = APIRequest(
            request_id=str(uuid.uuid4()),
            action="find_substitutions",
            payload=message.payload,
            priority=message.priority
        )

        response = await self.api.handle_request(request)

        self.metrics["substitutions_found"] += len(response.data.get("substitutions", []))

        await self._publish(
            "upc.substitution.found",
            {
                "request_id": request.request_id,
                "substitutions": response.data.get("substitutions", []),
                "count": response.data.get("count", 0),
            },
            message.sender
        )

    async def _handle_failure_request(self, message: AgentMessage):
        """Handle failure prediction request."""
        from .prediction.failure_predictor import JointCondition

        condition_data = message.payload.get("condition", {})
        condition = JointCondition(**condition_data)

        mission_hours = message.payload.get("mission_hours", 10000)

        result = self.failure_predictor.predict_failure(condition, mission_hours)

        self.metrics["failures_predicted"] += 1

        await self._publish(
            "upc.failure.predicted",
            {
                "overall_probability": result.overall_probability,
                "risk_level": result.risk_level.value,
                "dominant_mode": result.dominant_mode.value,
                "expected_life_cycles": result.expected_life_cycles,
                "critical_factors": result.critical_factors,
                "mitigation_actions": result.mitigation_actions,
            },
            message.sender
        )

    async def _handle_tolerance_request(self, message: AgentMessage):
        """Handle tolerance stack analysis request."""
        from .engine.tolerance_analyzer import Dimension, AssemblySpec, DistributionType

        dimensions = []
        for dim_data in message.payload.get("dimensions", []):
            dim = Dimension(
                name=dim_data["name"],
                nominal=dim_data["nominal"],
                tolerance_plus=dim_data.get("tolerance_plus", 0),
                tolerance_minus=dim_data.get("tolerance_minus", 0),
                distribution=DistributionType(dim_data.get("distribution", "NORMAL")),
                contributes_positive=dim_data.get("contributes_positive", True)
            )
            dimensions.append(dim)

        spec = None
        if "specification" in message.payload:
            spec_data = message.payload["specification"]
            spec = AssemblySpec(
                target=spec_data["target"],
                upper_limit=spec_data["upper_limit"],
                lower_limit=spec_data["lower_limit"]
            )

        result = self.tolerance_analyzer.analyze_assembly(dimensions, spec)

        await self._publish(
            "upc.tolerance.analyzed",
            {
                "nominal": result.nominal,
                "worst_case_range": (result.worst_case_min, result.worst_case_max),
                "rss_3sigma_range": (result.rss_3sigma_min, result.rss_3sigma_max),
                "probability_within_spec": result.probability_within_spec,
                "meets_spec": result.meets_spec,
                "critical_contributors": result.critical_contributors,
            },
            message.sender
        )

    async def _handle_part_update(self, message: AgentMessage):
        """Handle part data update from Agent_1."""
        part_id = message.payload.get("part_id")

        if part_id:
            # Invalidate cache for this part
            await self.cache.invalidate_part(part_id)

    async def _handle_directive(self, message: AgentMessage):
        """Handle system directive from Agent_10."""
        directive = message.payload.get("directive")

        if directive == "report_status":
            await self._report_status()
        elif directive == "clear_cache":
            await self.cache.l1_cache.clear()
        elif directive == "warmup_cache":
            pairs = message.payload.get("pairs", [])
            await self.cache.warmup(pairs)

    async def _contribute_qualia(self, request: Dict, result: Dict):
        """Send qualia data to Agent_4 (Qualia Collector)."""
        qualia_data = {
            "event_type": "compatibility_verification",
            "timestamp": datetime.now().isoformat(),
            "parts": [
                request.get("part_a", {}).get("id"),
                request.get("part_b", {}).get("id")
            ],
            "result": result.get("is_compatible", False),
            "confidence": result.get("confidence", 0.0),
            "compatibility_type": result.get("compatibility_type"),
            "experience_type": "relationship" if result.get("is_compatible") else "rejection",
        }

        await self._publish(
            "upc.qualia.contribution",
            qualia_data,
            "AGENT_4"
        )

        self.metrics["qualia_contributions"] += 1

    async def _report_status(self):
        """Report agent status to Agent_10."""
        status = {
            "agent_id": self.AGENT_ID,
            "agent_name": self.AGENT_NAME,
            "state": self.state.value,
            "metrics": self.metrics,
            "cache_stats": self.cache.stats(),
            "api_metrics": self.api.get_metrics(),
            "timestamp": datetime.now().isoformat(),
        }

        await self._publish(
            "upc.agent.status",
            status,
            "AGENT_10"
        )

    async def _publish(
        self,
        topic: str,
        payload: Dict,
        receiver: str = "BROADCAST"
    ):
        """Publish message to bus."""
        if not self.message_bus:
            return

        message = AgentMessage(
            sender=self.AGENT_ID,
            receiver=receiver,
            message_type="DATA",
            priority=5,
            timestamp=datetime.now().isoformat(),
            payload={"topic": topic, **payload},
            consciousness_context={}
        )

        await self.message_bus.publish(topic, message)

    async def _send_error(self, original: AgentMessage, error: str):
        """Send error response."""
        await self._publish(
            "upc.error",
            {
                "original_topic": original.payload.get("topic"),
                "error": error,
            },
            original.sender
        )

    # Public API methods for direct use

    def check_compatibility(self, part_a: Dict, part_b: Dict, context: Dict = None) -> Dict:
        """
        Check compatibility between two parts.

        Args:
            part_a: First part specification
            part_b: Second part specification
            context: Optional assembly context

        Returns:
            Compatibility result
        """
        from .engine.compatibility_core import Part, AssemblyContext

        # Build parts
        part_a_obj = self._dict_to_part(part_a)
        part_b_obj = self._dict_to_part(part_b)

        context_obj = None
        if context:
            context_obj = self._dict_to_context(context)

        result = self.compatibility_checker.check_compatibility(
            part_a_obj, part_b_obj, context_obj
        )

        return {
            "is_compatible": result.is_compatible,
            "confidence": result.confidence,
            "compatibility_type": result.compatibility_type.value,
            "warnings": result.warnings,
            "recommendations": result.recommendations,
        }

    def find_substitutions(
        self,
        target: Dict,
        context: Dict = None,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Find substitution recommendations for a part.

        Args:
            target: Target part specification
            context: Assembly context
            max_results: Maximum results to return

        Returns:
            List of substitution recommendations
        """
        from .substitution.substitution_engine import PartSpec, AssemblyContext

        target_spec = PartSpec(**target)
        context_obj = AssemblyContext(**(context or {}))

        results = self.substitution_engine.find_substitutions(
            target_spec, context_obj, max_results=max_results
        )

        return [
            {
                "part_id": r.part.part_id,
                "score": r.overall_score,
                "type": r.substitution_type.value,
                "warnings": r.warnings,
            }
            for r in results
        ]

    def predict_failure(self, condition: Dict, mission_hours: float = 10000) -> Dict:
        """
        Predict failure probability for a joint.

        Args:
            condition: Joint condition specification
            mission_hours: Mission duration in hours

        Returns:
            Failure prediction result
        """
        from .prediction.failure_predictor import JointCondition

        cond = JointCondition(**condition)
        result = self.failure_predictor.predict_failure(cond, mission_hours)

        return {
            "probability": result.overall_probability,
            "risk_level": result.risk_level.value,
            "dominant_mode": result.dominant_mode.value,
            "expected_life": result.expected_life_cycles,
            "critical_factors": result.critical_factors,
            "mitigation": result.mitigation_actions,
        }

    def get_galvanic_risk(
        self,
        material_a: str,
        material_b: str,
        environment: str = "indoor"
    ) -> str:
        """Get galvanic corrosion risk between materials."""
        from .engine.material_compatibility import Environment

        risk = self.material_checker.get_galvanic_risk(
            material_a, material_b, Environment(environment.upper())
        )
        return risk.value

    def _dict_to_part(self, data: Dict):
        """Convert dict to Part object."""
        from .engine.compatibility_core import Part, ThreadSpec, MaterialSpec, DimensionSpec
        from decimal import Decimal

        thread = None
        if "thread" in data:
            t = data["thread"]
            thread = ThreadSpec(
                nominal_diameter=Decimal(str(t.get("diameter", 0))),
                pitch=Decimal(str(t.get("pitch", 0))),
                thread_class=t.get("class", "6g"),
                major_dia_min=Decimal(str(t.get("major_dia_min", 0))),
                major_dia_max=Decimal(str(t.get("major_dia_max", 0))),
                pitch_dia_min=Decimal(str(t.get("pitch_dia_min", 0))),
                pitch_dia_max=Decimal(str(t.get("pitch_dia_max", 0))),
                minor_dia_min=Decimal(str(t.get("minor_dia_min", 0))),
                minor_dia_max=Decimal(str(t.get("minor_dia_max", 0))),
            )

        material = None
        if "material" in data:
            m = data["material"]
            material = MaterialSpec(
                material_type=m.get("type", "steel"),
                grade=m.get("grade", "8.8"),
                tensile_strength_mpa=Decimal(str(m.get("tensile_mpa", 800))),
                yield_strength_mpa=Decimal(str(m.get("yield_mpa", 640))),
                shear_strength_mpa=Decimal(str(m.get("shear_mpa", 460))),
            )

        return Part(
            upc_id=data.get("id", "unknown"),
            part_number=data.get("part_number", ""),
            category=data.get("category", "fastener"),
            thread=thread,
            material=material,
        )

    def _dict_to_context(self, data: Dict):
        """Convert dict to AssemblyContext."""
        from .engine.compatibility_core import AssemblyContext
        from decimal import Decimal

        return AssemblyContext(
            material_thickness=Decimal(str(data.get("thickness"))) if data.get("thickness") else None,
            load_case_kn=Decimal(str(data.get("load_kn"))) if data.get("load_kn") else None,
            environment=data.get("environment", "indoor"),
        )


# Convenience function to create agent
def create_oracle_agent(
    message_bus=None,
    database=None,
    cache_config: Dict = None
) -> OracleAgent:
    """Create and configure an Oracle Agent instance."""
    return OracleAgent(
        message_bus=message_bus,
        database=database,
        cache_config=cache_config or {}
    )
