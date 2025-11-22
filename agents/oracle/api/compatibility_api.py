"""
ORACLE Compatibility API
Real-time compatibility checking with sub-10ms target latency.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import json
import asyncio


@dataclass
class APIRequest:
    """Standardized API request format."""
    request_id: str
    action: str
    payload: Dict[str, Any]
    priority: int = 5
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class APIResponse:
    """Standardized API response format."""
    request_id: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    latency_ms: float = 0.0
    cached: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


class CompatibilityAPI:
    """
    High-performance compatibility checking API.

    Target latencies:
    - Simple compatibility check: < 5ms (< 10ms max)
    - Substitution search (10 results): < 50ms (< 100ms max)
    - Tolerance stack analysis: < 100ms (< 200ms max)
    - Batch compatibility (100 pairs): < 500ms (< 1000ms max)
    """

    def __init__(self, cache=None, database=None):
        """
        Initialize API with optional cache and database.

        Args:
            cache: CompatibilityCache instance
            database: Database connection for parts lookup
        """
        self.cache = cache
        self.db = database

        # Import engines
        from ..engine.compatibility_core import UniversalCompatibilityChecker
        from ..substitution.substitution_engine import SubstitutionEngine
        from ..engine.tolerance_analyzer import ToleranceStackAnalyzer
        from ..prediction.failure_predictor import FailurePredictor

        self.compatibility_checker = UniversalCompatibilityChecker()
        self.substitution_engine = SubstitutionEngine(database)
        self.tolerance_analyzer = ToleranceStackAnalyzer()
        self.failure_predictor = FailurePredictor()

        # Request tracking
        self.request_count = 0
        self.total_latency_ms = 0.0

        # Message bus connection (if available)
        self.message_bus = None

    async def handle_request(self, request: APIRequest) -> APIResponse:
        """
        Handle an API request.

        Args:
            request: APIRequest object

        Returns:
            APIResponse with results
        """
        start_time = time.perf_counter()

        try:
            # Route to appropriate handler
            handlers = {
                "check_compatibility": self._handle_compatibility,
                "find_substitutions": self._handle_substitutions,
                "analyze_tolerance": self._handle_tolerance,
                "predict_failure": self._handle_failure,
                "get_galvanic_risk": self._handle_galvanic,
                "calculate_strength": self._handle_strength,
            }

            handler = handlers.get(request.action)
            if not handler:
                return APIResponse(
                    request_id=request.request_id,
                    success=False,
                    data={},
                    error=f"Unknown action: {request.action}"
                )

            result = await handler(request.payload)

            latency = (time.perf_counter() - start_time) * 1000

            # Track metrics
            self.request_count += 1
            self.total_latency_ms += latency

            # Publish to message bus if connected
            if self.message_bus:
                await self._publish_event(request, result, latency)

            return APIResponse(
                request_id=request.request_id,
                success=True,
                data=result["data"],
                latency_ms=latency,
                cached=result.get("cached", False)
            )

        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            return APIResponse(
                request_id=request.request_id,
                success=False,
                data={},
                error=str(e),
                latency_ms=latency
            )

    async def _handle_compatibility(self, payload: Dict) -> Dict:
        """Handle compatibility check request."""
        from ..engine.compatibility_core import Part, ThreadSpec, MaterialSpec, DimensionSpec, AssemblyContext

        # Check cache first
        cache_key = f"compat:{payload.get('part_a_id')}:{payload.get('part_b_id')}"
        if self.cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return {"data": cached, "cached": True}

        # Build Part objects from payload
        part_a = self._build_part(payload.get("part_a", {}))
        part_b = self._build_part(payload.get("part_b", {}))

        context = None
        if "context" in payload:
            context = self._build_context(payload["context"])

        # Run compatibility check
        result = self.compatibility_checker.check_compatibility(
            part_a, part_b, context
        )

        # Convert to serializable dict
        result_data = {
            "is_compatible": result.is_compatible,
            "confidence": result.confidence,
            "compatibility_type": result.compatibility_type.value,
            "warnings": result.warnings,
            "recommendations": result.recommendations,
            "check_duration_ms": result.check_duration_ms,
        }

        # Cache result
        if self.cache:
            await self.cache.set(cache_key, result_data, ttl=3600)

        return {"data": result_data}

    async def _handle_substitutions(self, payload: Dict) -> Dict:
        """Handle substitution search request."""
        from ..substitution.substitution_engine import PartSpec, AssemblyContext, SubstitutionConstraints

        target = self._build_part_spec(payload.get("target", {}))
        context = self._build_assembly_context(payload.get("context", {}))

        constraints = None
        if "constraints" in payload:
            constraints = SubstitutionConstraints(**payload["constraints"])

        max_results = payload.get("max_results", 10)

        # Find substitutions
        results = self.substitution_engine.find_substitutions(
            target, context, constraints, max_results
        )

        # Convert to serializable format
        substitutions = []
        for rec in results:
            substitutions.append({
                "part_id": rec.part.part_id,
                "part_number": rec.part.part_number,
                "manufacturer": rec.part.manufacturer,
                "substitution_type": rec.substitution_type.value,
                "compatibility_score": rec.compatibility_score,
                "overall_score": rec.overall_score,
                "thread_compatible": rec.thread_compatible,
                "strength_adequate": rec.strength_adequate,
                "modifications_required": len(rec.modifications_required),
                "warnings": rec.warnings,
                "advantages": rec.advantages,
                "disadvantages": rec.disadvantages,
            })

        return {"data": {"substitutions": substitutions, "count": len(substitutions)}}

    async def _handle_tolerance(self, payload: Dict) -> Dict:
        """Handle tolerance stack analysis request."""
        from ..engine.tolerance_analyzer import Dimension, AssemblySpec, DistributionType

        dimensions = []
        for dim_data in payload.get("dimensions", []):
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
        if "specification" in payload:
            spec_data = payload["specification"]
            spec = AssemblySpec(
                target=spec_data["target"],
                upper_limit=spec_data["upper_limit"],
                lower_limit=spec_data["lower_limit"]
            )

        result = self.tolerance_analyzer.analyze_assembly(dimensions, spec)

        return {"data": {
            "nominal": result.nominal,
            "worst_case_range": (result.worst_case_min, result.worst_case_max),
            "rss_3sigma_range": (result.rss_3sigma_min, result.rss_3sigma_max),
            "monte_carlo_99_range": (result.monte_carlo_99_min, result.monte_carlo_99_max),
            "probability_within_spec": result.probability_within_spec,
            "meets_spec": result.meets_spec,
            "critical_contributors": result.critical_contributors,
            "recommendations": result.recommendations,
        }}

    async def _handle_failure(self, payload: Dict) -> Dict:
        """Handle failure prediction request."""
        from ..prediction.failure_predictor import JointCondition

        condition = JointCondition(**payload.get("condition", {}))
        mission_hours = payload.get("mission_hours", 10000)

        result = self.failure_predictor.predict_failure(condition, mission_hours)

        return {"data": {
            "overall_probability": result.overall_probability,
            "risk_level": result.risk_level.value,
            "dominant_mode": result.dominant_mode.value,
            "expected_life_cycles": result.expected_life_cycles,
            "critical_factors": result.critical_factors,
            "mitigation_actions": result.mitigation_actions,
            "confidence": result.confidence,
        }}

    async def _handle_galvanic(self, payload: Dict) -> Dict:
        """Handle galvanic corrosion risk request."""
        from ..engine.material_compatibility import MaterialCompatibilityChecker, Environment

        checker = MaterialCompatibilityChecker()

        material_a = payload.get("material_a")
        material_b = payload.get("material_b")
        environment = payload.get("environment", "INDOOR")

        risk = checker.get_galvanic_risk(
            material_a, material_b, Environment(environment)
        )

        return {"data": {
            "risk_level": risk.value,
            "material_a": material_a,
            "material_b": material_b,
            "environment": environment,
        }}

    async def _handle_strength(self, payload: Dict) -> Dict:
        """Handle strength calculation request."""
        from ..engine.strength_calculator import StrengthCalculator

        calculator = StrengthCalculator()

        result = calculator.calculate_strength(
            diameter_mm=payload.get("diameter_mm"),
            pitch_mm=payload.get("pitch_mm"),
            grade=payload.get("grade"),
            engagement_mm=payload.get("engagement_mm"),
            base_material=payload.get("base_material"),
            safety_factor=payload.get("safety_factor", 2.5)
        )

        return {"data": {
            "allowable_load_kn": result.allowable_load_kn,
            "ultimate_load_kn": result.ultimate_load_kn,
            "safety_factor": result.safety_factor,
            "limiting_mode": result.limiting_mode.value,
            "tensile_strength_kn": result.tensile_strength_kn,
            "shear_strength_kn": result.shear_strength_kn,
            "warnings": result.warnings,
            "recommendations": result.recommendations,
        }}

    def _build_part(self, data: Dict):
        """Build Part object from dict."""
        from ..engine.compatibility_core import Part, ThreadSpec, MaterialSpec, DimensionSpec
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

        dimensions = None
        if "dimensions" in data:
            d = data["dimensions"]
            dimensions = DimensionSpec(
                length=Decimal(str(d.get("length", 0))),
                length_tolerance_plus=Decimal(str(d.get("tol_plus", 0))),
                length_tolerance_minus=Decimal(str(d.get("tol_minus", 0))),
            )

        proof_load = None
        if "proof_load_kn" in data:
            proof_load = Decimal(str(data["proof_load_kn"]))

        return Part(
            upc_id=data.get("id", "unknown"),
            part_number=data.get("part_number", ""),
            category=data.get("category", "fastener"),
            thread=thread,
            material=material,
            dimensions=dimensions,
            proof_load_kn=proof_load
        )

    def _build_context(self, data: Dict):
        """Build AssemblyContext from dict."""
        from ..engine.compatibility_core import AssemblyContext
        from decimal import Decimal

        return AssemblyContext(
            material_thickness=Decimal(str(data.get("thickness", 0))) if data.get("thickness") else None,
            through_hole_diameter=Decimal(str(data.get("hole_dia", 0))) if data.get("hole_dia") else None,
            load_case_kn=Decimal(str(data.get("load_kn", 0))) if data.get("load_kn") else None,
            environment=data.get("environment", "indoor"),
        )

    def _build_part_spec(self, data: Dict):
        """Build PartSpec for substitution engine."""
        from ..substitution.substitution_engine import PartSpec

        return PartSpec(
            part_id=data.get("id", "unknown"),
            manufacturer=data.get("manufacturer", ""),
            part_number=data.get("part_number", ""),
            category=data.get("category", "fastener"),
            thread_diameter_mm=data.get("diameter_mm"),
            thread_pitch_mm=data.get("pitch_mm"),
            length_mm=data.get("length_mm"),
            grade=data.get("grade"),
            proof_load_kn=data.get("proof_load_kn"),
            in_stock=data.get("in_stock", True),
            unit_price=data.get("unit_price"),
        )

    def _build_assembly_context(self, data: Dict):
        """Build AssemblyContext for substitution engine."""
        from ..substitution.substitution_engine import AssemblyContext

        return AssemblyContext(
            application=data.get("application", "general"),
            environment=data.get("environment", "indoor"),
            load_kn=data.get("load_kn"),
            safety_critical=data.get("safety_critical", False),
        )

    async def _publish_event(self, request: APIRequest, result: Dict, latency: float):
        """Publish API event to message bus."""
        event = {
            "sender": "AGENT_2",
            "type": "COMPATIBILITY_CHECK",
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "action": request.action,
                "latency_ms": latency,
                "success": True,
            },
            "consciousness_context": result.get("data", {}).get("experience_contribution", {})
        }
        # Would publish to message bus here

    def get_metrics(self) -> Dict:
        """Get API performance metrics."""
        avg_latency = self.total_latency_ms / self.request_count if self.request_count > 0 else 0

        return {
            "request_count": self.request_count,
            "total_latency_ms": self.total_latency_ms,
            "average_latency_ms": avg_latency,
            "cache_enabled": self.cache is not None,
        }
