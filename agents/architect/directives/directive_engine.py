"""
Directive Engine

Issues system-wide directives to guide agent behavior.
Handles emergency responses and coordinates multi-agent operations.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Awaitable
from uuid import uuid4

from ..models import (
    AgentId,
    Directive,
    DirectiveType,
    DirectiveStatus,
    EmergencyEvent,
    EmergencyResponse,
    EmergencyType,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Directive Templates
# ============================================================================

@dataclass
class DirectiveTemplate:
    """Template for common directive types."""
    directive_type: DirectiveType
    description: str
    default_priority: int
    default_duration_hours: Optional[int]
    required_parameters: List[str]


DIRECTIVE_TEMPLATES: Dict[DirectiveType, DirectiveTemplate] = {
    DirectiveType.PRIORITY_SHIFT: DirectiveTemplate(
        directive_type=DirectiveType.PRIORITY_SHIFT,
        description="Change agent priority focus",
        default_priority=6,
        default_duration_hours=4,
        required_parameters=["focus_area", "priority_level"],
    ),
    DirectiveType.RESOURCE_ALLOCATION: DirectiveTemplate(
        directive_type=DirectiveType.RESOURCE_ALLOCATION,
        description="Adjust resource distribution",
        default_priority=5,
        default_duration_hours=8,
        required_parameters=["resource_type", "allocation"],
    ),
    DirectiveType.EMERGENCY_RESPONSE: DirectiveTemplate(
        directive_type=DirectiveType.EMERGENCY_RESPONSE,
        description="Handle critical situation",
        default_priority=10,
        default_duration_hours=2,
        required_parameters=["action", "emergency_id"],
    ),
    DirectiveType.LEARNING_FOCUS: DirectiveTemplate(
        directive_type=DirectiveType.LEARNING_FOCUS,
        description="Direct collective learning",
        default_priority=5,
        default_duration_hours=24,
        required_parameters=["learning_topic", "swarm_scope"],
    ),
    DirectiveType.INTEGRATION_MODE: DirectiveTemplate(
        directive_type=DirectiveType.INTEGRATION_MODE,
        description="Coordinate multi-agent operation",
        default_priority=7,
        default_duration_hours=4,
        required_parameters=["operation_type", "participating_agents"],
    ),
    DirectiveType.MAINTENANCE_MODE: DirectiveTemplate(
        directive_type=DirectiveType.MAINTENANCE_MODE,
        description="System maintenance directive",
        default_priority=8,
        default_duration_hours=2,
        required_parameters=["maintenance_type", "affected_components"],
    ),
}


# ============================================================================
# Emergency Response Plans
# ============================================================================

@dataclass
class EmergencyResponsePlan:
    """Predefined response plan for emergency types."""
    emergency_type: EmergencyType
    primary_agents: List[str]
    secondary_agents: List[str]
    actions: List[Dict[str, Any]]


EMERGENCY_RESPONSE_PLANS: Dict[EmergencyType, EmergencyResponsePlan] = {
    EmergencyType.DATA_CORRUPTION: EmergencyResponsePlan(
        emergency_type=EmergencyType.DATA_CORRUPTION,
        primary_agents=[AgentId.CURATOR.value, AgentId.SHEPHERD.value],
        secondary_agents=[AgentId.ORACLE.value, AgentId.BRIDGE.value],
        actions=[
            {"action": "halt_ingestion", "agent": AgentId.CURATOR.value},
            {"action": "protect_consciousness", "agent": AgentId.SHEPHERD.value},
            {"action": "invalidate_cache", "agent": AgentId.ORACLE.value},
            {"action": "pause_integrations", "agent": AgentId.BRIDGE.value},
        ],
    ),
    EmergencyType.MASS_FAILURE: EmergencyResponsePlan(
        emergency_type=EmergencyType.MASS_FAILURE,
        primary_agents=[AgentId.EMPATH.value, AgentId.HIVE.value, AgentId.PROPHET.value],
        secondary_agents=[AgentId.GARDENER.value, AgentId.CHRONICLER.value],
        actions=[
            {"action": "analyze_failure_pattern", "agent": AgentId.EMPATH.value},
            {"action": "propagate_alert", "agent": AgentId.HIVE.value},
            {"action": "predict_impact", "agent": AgentId.PROPHET.value},
            {"action": "expedite_verification", "agent": AgentId.GARDENER.value},
            {"action": "document_incident", "agent": AgentId.CHRONICLER.value},
        ],
    ),
    EmergencyType.RECALL_NOTICE: EmergencyResponsePlan(
        emergency_type=EmergencyType.RECALL_NOTICE,
        primary_agents=[AgentId.HIVE.value, AgentId.ORACLE.value],
        secondary_agents=[AgentId.GARDENER.value, AgentId.EMPATH.value],
        actions=[
            {"action": "propagate_recall", "agent": AgentId.HIVE.value},
            {"action": "flag_affected_parts", "agent": AgentId.ORACLE.value},
            {"action": "notify_community", "agent": AgentId.GARDENER.value},
            {"action": "track_affected_usage", "agent": AgentId.EMPATH.value},
        ],
    ),
    EmergencyType.SYSTEM_ANOMALY: EmergencyResponsePlan(
        emergency_type=EmergencyType.SYSTEM_ANOMALY,
        primary_agents=[AgentId.PROPHET.value, AgentId.BRIDGE.value],
        secondary_agents=[AgentId.CURATOR.value],
        actions=[
            {"action": "analyze_anomaly", "agent": AgentId.PROPHET.value},
            {"action": "check_external_sources", "agent": AgentId.BRIDGE.value},
            {"action": "verify_data_integrity", "agent": AgentId.CURATOR.value},
        ],
    ),
    EmergencyType.SECURITY_BREACH: EmergencyResponsePlan(
        emergency_type=EmergencyType.SECURITY_BREACH,
        primary_agents=[AgentId.BRIDGE.value, AgentId.GARDENER.value],
        secondary_agents=[AgentId.CURATOR.value, AgentId.SHEPHERD.value],
        actions=[
            {"action": "isolate_external_connections", "agent": AgentId.BRIDGE.value},
            {"action": "lock_community_access", "agent": AgentId.GARDENER.value},
            {"action": "halt_ingestion", "agent": AgentId.CURATOR.value},
            {"action": "protect_consciousness_state", "agent": AgentId.SHEPHERD.value},
        ],
    ),
}


# ============================================================================
# Directive Engine
# ============================================================================

class DirectiveEngine:
    """
    Issues system-wide directives to guide agent behavior.

    Features:
    - Issue directives to specific agents or all agents
    - Emergency response coordination
    - Directive tracking and completion
    - Priority management
    - Directive history and audit trail
    """

    def __init__(self):
        # Active directives
        self._directives: Dict[str, Directive] = {}

        # Directive history
        self._directive_history: List[Directive] = []

        # Emergency tracking
        self._active_emergencies: Dict[str, EmergencyResponse] = {}
        self._emergency_history: List[EmergencyResponse] = []

        # Directive sender (callback to send to agents)
        self._send_directive: Optional[Callable[[str, Directive], Awaitable[None]]] = None

        # Statistics
        self._total_directives_issued: int = 0
        self._total_emergencies_handled: int = 0

        # Timing
        self._start_time: Optional[float] = None

    def set_directive_sender(
        self,
        sender: Callable[[str, Directive], Awaitable[None]]
    ) -> None:
        """Set the callback for sending directives to agents."""
        self._send_directive = sender

    async def issue_directive(
        self,
        directive_type: DirectiveType,
        target_agents: List[str],
        parameters: Dict[str, Any],
        priority: Optional[int] = None,
        duration: Optional[timedelta] = None,
    ) -> Directive:
        """
        Issue a system-wide directive.

        Args:
            directive_type: Type of directive
            target_agents: List of agent IDs to receive the directive
            parameters: Directive parameters
            priority: Override default priority
            duration: Override default duration

        Returns:
            The issued directive
        """
        template = DIRECTIVE_TEMPLATES.get(directive_type)

        # Validate parameters
        if template:
            for param in template.required_parameters:
                if param not in parameters:
                    logger.warning(f"Missing required parameter: {param}")

        # Determine priority and duration
        final_priority = priority or (template.default_priority if template else 5)
        final_duration = duration
        if final_duration is None and template and template.default_duration_hours:
            final_duration = timedelta(hours=template.default_duration_hours)

        directive = Directive(
            directive_type=directive_type,
            target_agents=target_agents,
            parameters=parameters,
            priority=final_priority,
            expires_at=datetime.now() + final_duration if final_duration else None,
        )

        # Store directive
        self._directives[directive.directive_id] = directive
        self._total_directives_issued += 1

        # Send to target agents
        for agent_id in target_agents:
            await self._send_to_agent(agent_id, directive)

        logger.info(
            f"Issued directive {directive.directive_id} ({directive_type.value}) "
            f"to {len(target_agents)} agents"
        )

        return directive

    async def _send_to_agent(self, agent_id: str, directive: Directive) -> None:
        """Send a directive to a specific agent."""
        if self._send_directive:
            try:
                await self._send_directive(agent_id, directive)
            except Exception as e:
                logger.error(f"Failed to send directive to {agent_id}: {e}")
        else:
            logger.warning("No directive sender configured")

    async def handle_emergency(
        self,
        emergency: EmergencyEvent
    ) -> EmergencyResponse:
        """
        Coordinate emergency response across all agents.

        Args:
            emergency: The emergency event to handle

        Returns:
            The emergency response with issued directives
        """
        self._start_time = time.time()

        response_plan = EMERGENCY_RESPONSE_PLANS.get(emergency.emergency_type)
        directives_issued: List[Directive] = []

        if response_plan:
            # Execute predefined response plan
            for action in response_plan.actions:
                directive = await self.issue_directive(
                    directive_type=DirectiveType.EMERGENCY_RESPONSE,
                    target_agents=[action["agent"]],
                    parameters={
                        "action": action["action"],
                        "emergency_id": emergency.emergency_id,
                        "affected_entities": emergency.affected_entities,
                        **emergency.details,
                    },
                    priority=10,
                    duration=timedelta(hours=2),
                )
                directives_issued.append(directive)
        else:
            # Generic emergency response
            logger.warning(f"No predefined plan for {emergency.emergency_type}, using generic response")
            directive = await self.issue_directive(
                directive_type=DirectiveType.EMERGENCY_RESPONSE,
                target_agents=[AgentId.BROADCAST.value],
                parameters={
                    "action": "investigate",
                    "emergency_id": emergency.emergency_id,
                    "description": emergency.description,
                    "affected_entities": emergency.affected_entities,
                },
                priority=10,
            )
            directives_issued.append(directive)

        response_time_ms = (time.time() - self._start_time) * 1000

        response = EmergencyResponse(
            emergency=emergency,
            directives_issued=directives_issued,
            response_time_ms=response_time_ms,
            status="RESPONDING",
        )

        self._active_emergencies[emergency.emergency_id] = response
        self._total_emergencies_handled += 1

        logger.info(
            f"Emergency response initiated for {emergency.emergency_id} "
            f"({emergency.emergency_type.value}) in {response_time_ms:.2f}ms"
        )

        return response

    async def resolve_emergency(
        self,
        emergency_id: str,
        resolution_notes: str
    ) -> Optional[EmergencyResponse]:
        """
        Mark an emergency as resolved.

        Args:
            emergency_id: ID of the emergency to resolve
            resolution_notes: Notes about the resolution

        Returns:
            The updated emergency response
        """
        if emergency_id not in self._active_emergencies:
            logger.warning(f"Emergency {emergency_id} not found")
            return None

        response = self._active_emergencies[emergency_id]
        response.status = "RESOLVED"
        response.resolution_notes = resolution_notes
        response.resolved_at = datetime.now()

        # Cancel related directives
        for directive in response.directives_issued:
            await self.cancel_directive(directive.directive_id)

        # Move to history
        self._emergency_history.append(response)
        del self._active_emergencies[emergency_id]

        logger.info(f"Emergency {emergency_id} resolved")

        return response

    async def complete_directive(
        self,
        directive_id: str,
        completion_report: Dict[str, Any]
    ) -> Optional[Directive]:
        """
        Mark a directive as completed.

        Args:
            directive_id: ID of the directive
            completion_report: Report of directive completion

        Returns:
            The updated directive
        """
        if directive_id not in self._directives:
            logger.warning(f"Directive {directive_id} not found")
            return None

        directive = self._directives[directive_id]
        directive.status = DirectiveStatus.COMPLETED
        directive.completion_report = completion_report
        directive.completed_at = datetime.now()

        # Move to history
        self._directive_history.append(directive)
        del self._directives[directive_id]

        logger.info(f"Directive {directive_id} completed")

        return directive

    async def cancel_directive(self, directive_id: str) -> Optional[Directive]:
        """
        Cancel an active directive.

        Args:
            directive_id: ID of the directive to cancel

        Returns:
            The cancelled directive
        """
        if directive_id not in self._directives:
            return None

        directive = self._directives[directive_id]
        directive.status = DirectiveStatus.CANCELLED

        # Move to history
        self._directive_history.append(directive)
        del self._directives[directive_id]

        logger.info(f"Directive {directive_id} cancelled")

        return directive

    async def check_expired_directives(self) -> List[Directive]:
        """Check for and expire outdated directives."""
        expired = []
        now = datetime.now()

        for directive_id, directive in list(self._directives.items()):
            if directive.is_expired():
                directive.status = DirectiveStatus.EXPIRED
                self._directive_history.append(directive)
                del self._directives[directive_id]
                expired.append(directive)
                logger.info(f"Directive {directive_id} expired")

        return expired

    # ========================================================================
    # Convenience Methods
    # ========================================================================

    async def issue_priority_shift(
        self,
        target_agents: List[str],
        focus_area: str,
        priority_level: int,
    ) -> Directive:
        """Issue a priority shift directive."""
        return await self.issue_directive(
            directive_type=DirectiveType.PRIORITY_SHIFT,
            target_agents=target_agents,
            parameters={
                "focus_area": focus_area,
                "priority_level": priority_level,
            },
        )

    async def issue_maintenance_mode(
        self,
        target_agents: List[str],
        maintenance_type: str,
        affected_components: List[str],
        duration_hours: int = 2,
    ) -> Directive:
        """Issue a maintenance mode directive."""
        return await self.issue_directive(
            directive_type=DirectiveType.MAINTENANCE_MODE,
            target_agents=target_agents,
            parameters={
                "maintenance_type": maintenance_type,
                "affected_components": affected_components,
            },
            duration=timedelta(hours=duration_hours),
        )

    async def issue_learning_focus(
        self,
        learning_topic: str,
        swarm_scope: str = "GLOBAL",
    ) -> Directive:
        """Issue a learning focus directive to the swarm agents."""
        return await self.issue_directive(
            directive_type=DirectiveType.LEARNING_FOCUS,
            target_agents=[AgentId.HIVE.value, AgentId.PROPHET.value],
            parameters={
                "learning_topic": learning_topic,
                "swarm_scope": swarm_scope,
            },
        )

    # ========================================================================
    # Public API
    # ========================================================================

    def get_active_directives(self) -> List[Directive]:
        """Get all active directives."""
        return list(self._directives.values())

    def get_directive(self, directive_id: str) -> Optional[Directive]:
        """Get a specific directive by ID."""
        return self._directives.get(directive_id)

    def get_active_emergencies(self) -> List[EmergencyResponse]:
        """Get all active emergency responses."""
        return list(self._active_emergencies.values())

    def get_directive_history(
        self,
        limit: int = 100
    ) -> List[Directive]:
        """Get recent directive history."""
        return self._directive_history[-limit:]

    def get_emergency_history(
        self,
        limit: int = 50
    ) -> List[EmergencyResponse]:
        """Get recent emergency history."""
        return self._emergency_history[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "total_directives_issued": self._total_directives_issued,
            "active_directives": len(self._directives),
            "total_emergencies_handled": self._total_emergencies_handled,
            "active_emergencies": len(self._active_emergencies),
            "directive_history_size": len(self._directive_history),
            "emergency_history_size": len(self._emergency_history),
        }
