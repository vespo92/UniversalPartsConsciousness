"""
MACHINIST Agent API Module

API interfaces for industrial equipment intelligence.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class APIRequest:
    """Standard API request format"""
    request_id: str
    action: str
    payload: Dict[str, Any]
    priority: int = 5


@dataclass
class APIResponse:
    """Standard API response format"""
    request_id: str
    success: bool
    data: Dict[str, Any]
    latency_ms: float
    cached: bool = False
    error: Optional[str] = None


class MachinistAPI:
    """
    API interface for MACHINIST agent

    Provides:
    - CNC retrofit queries
    - PLC migration analysis
    - Servo drive cross-reference
    - Industrial fastener recommendations
    """

    def __init__(self, agent):
        """
        Initialize API with MACHINIST agent instance.

        Args:
            agent: MachinistAgent instance
        """
        self.agent = agent
        self.request_count = 0
        self.cache = {}

    async def handle_request(self, request: APIRequest) -> APIResponse:
        """
        Handle incoming API request.

        Args:
            request: APIRequest object

        Returns:
            APIResponse with results
        """
        start_time = datetime.now()

        try:
            # Route to appropriate handler
            handlers = {
                "cnc_retrofit": self._handle_cnc_retrofit,
                "plc_migration": self._handle_plc_migration,
                "servo_crossref": self._handle_servo_crossref,
                "fastener_recommend": self._handle_fastener,
                "controller_info": self._handle_controller_info,
            }

            handler = handlers.get(request.action)
            if not handler:
                return APIResponse(
                    request_id=request.request_id,
                    success=False,
                    data={},
                    latency_ms=0,
                    error=f"Unknown action: {request.action}"
                )

            result = await handler(request.payload)

            latency = (datetime.now() - start_time).total_seconds() * 1000
            self.request_count += 1

            return APIResponse(
                request_id=request.request_id,
                success=True,
                data=result,
                latency_ms=latency
            )

        except Exception as e:
            latency = (datetime.now() - start_time).total_seconds() * 1000
            return APIResponse(
                request_id=request.request_id,
                success=False,
                data={},
                latency_ms=latency,
                error=str(e)
            )

    async def _handle_cnc_retrofit(self, payload: Dict) -> Dict:
        """Handle CNC retrofit query"""
        brand = payload.get("brand", "")
        model = payload.get("model", "")
        component = payload.get("component", "")

        retrofits = self.agent.find_cnc_retrofit(brand, model, component)

        return {
            "count": len(retrofits),
            "retrofits": [
                {
                    "solution": r.solution_name,
                    "vendor": r.vendor,
                    "part_number": r.part_number,
                    "type": r.retrofit_type.value,
                    "price_usd": r.price_usd,
                    "install_hours": r.installation_hours,
                    "compatibility": r.compatibility_score,
                    "notes": r.notes,
                }
                for r in retrofits
            ]
        }

    async def _handle_plc_migration(self, payload: Dict) -> Dict:
        """Handle PLC migration query"""
        source_plc = payload.get("source_plc", "")
        io_count = payload.get("io_count")

        plan = self.agent.find_plc_migration_path(source_plc, io_count)

        if not plan:
            return {"error": "No migration path found", "source": source_plc}

        return {
            "source": plan.source_plc,
            "target": plan.recommended_target,
            "compatibility": plan.io_compatibility_score,
            "conversion_tool": plan.code_conversion_tool,
            "downtime_hours": plan.estimated_downtime_hours,
            "cost_usd": plan.estimated_cost_usd,
            "alternatives": plan.alternatives,
            "risks": plan.risks,
        }

    async def _handle_servo_crossref(self, payload: Dict) -> Dict:
        """Handle servo drive cross-reference"""
        original = payload.get("original_drive", "")
        motor_specs = payload.get("motor_specs")

        matches = self.agent.cross_reference_servo_drives(original, motor_specs)

        return {
            "original": original,
            "count": len(matches),
            "matches": [
                {
                    "replacement": m.replacement_drive,
                    "manufacturer": m.manufacturer,
                    "compatibility": m.compatibility_score,
                    "encoder_match": m.encoder_compatibility,
                    "price_ratio": m.price_vs_original,
                    "wiring_changes": m.wiring_changes,
                }
                for m in matches
            ]
        }

    async def _handle_fastener(self, payload: Dict) -> Dict:
        """Handle industrial fastener recommendation"""
        from .industrial_fasteners import FastenerApplication

        application_str = payload.get("application", "general")
        try:
            application = FastenerApplication(application_str)
        except ValueError:
            application = FastenerApplication.GENERAL

        environment = payload.get("environment", "")
        load = payload.get("load_requirements", {})

        recommendation = self.agent.find_industrial_fastener(
            application_str, environment, load
        )

        return recommendation

    async def _handle_controller_info(self, payload: Dict) -> Dict:
        """Handle controller information query"""
        manufacturer = payload.get("manufacturer", "")
        model = payload.get("model", "")

        info = self.agent.get_controller_info(manufacturer, model)

        if not info:
            return {"error": "Controller not found"}

        return {
            "manufacturer": info.manufacturer,
            "model": info.model,
            "generation": info.generation,
            "year_introduced": info.year_introduced,
            "year_discontinued": info.year_discontinued,
            "axes": info.axes_supported,
            "display": info.display_type,
            "compatible_drives": info.compatible_drives,
            "retrofit_options": info.retrofit_options,
        }

    def get_metrics(self) -> Dict:
        """Get API metrics"""
        return {
            "total_requests": self.request_count,
            "cache_size": len(self.cache),
        }


__all__ = ["APIRequest", "APIResponse", "MachinistAPI"]
