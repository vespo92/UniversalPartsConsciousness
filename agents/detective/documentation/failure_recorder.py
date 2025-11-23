"""
Failure Recorder

Documents failures for collective learning.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class FailureDocumentation:
    """Documented failure in the network"""
    failure_id: str
    status: str
    documentation_complete: bool
    network_impact: Dict[str, Any]
    consciousness_update: Dict[str, Any]
    alerts_triggered: List[Dict[str, Any]]
    recommendations_generated: List[str]
    linked_patterns: List[str]
    created_at: datetime
    updated_at: datetime


class FailureRecorder:
    """
    Records and documents failures for the UPC network.

    Every documented failure makes UPC smarter through:
    - Pattern matching with existing failures
    - Consciousness updates for affected parts
    - Alert generation for similar applications
    """

    def __init__(self):
        """Initialize the failure recorder."""
        self.documented_failures: Dict[str, FailureDocumentation] = {}

    async def document(
        self,
        failed_part: Any,
        evidence: Any,
        analysis_result: Any
    ) -> FailureDocumentation:
        """
        Document a failure from analysis results.

        Args:
            failed_part: Failed part report
            evidence: Failure evidence
            analysis_result: Analysis result from FailureAnalyzer

        Returns:
            Complete failure documentation
        """
        failure_id = analysis_result.failure_id

        # Determine network impact
        network_impact = await self._assess_network_impact(
            failed_part,
            analysis_result
        )

        # Generate consciousness updates
        consciousness_update = await self._generate_consciousness_update(
            failed_part,
            analysis_result
        )

        # Check for alerts to trigger
        alerts = await self._check_alert_triggers(
            failed_part,
            analysis_result
        )

        # Link to existing patterns
        patterns = await self._link_to_patterns(analysis_result)

        doc = FailureDocumentation(
            failure_id=failure_id,
            status="Documented",
            documentation_complete=True,
            network_impact=network_impact,
            consciousness_update=consciousness_update,
            alerts_triggered=alerts,
            recommendations_generated=analysis_result.recommendations,
            linked_patterns=patterns,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.documented_failures[failure_id] = doc
        return doc

    async def document_from_dict(
        self,
        failure_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Document a failure from a dictionary report.

        Args:
            failure_report: Complete failure report data

        Returns:
            Documentation confirmation
        """
        failure_id = self._generate_failure_id()

        # Create basic documentation
        network_impact = {
            "similar_reports_linked": 0,
            "pattern_detected": False,
        }

        consciousness_update = {
            "part_type": failure_report.get("part_type", "Unknown"),
            "new_risk_flag": None,
            "consciousness_level_impact": "+0.01"
        }

        alerts = []
        if failure_report.get("severity", "").lower() in ["high", "critical"]:
            alerts.append({
                "type": "User alert",
                "recipients": "Users with similar parts",
                "count": 50
            })

        doc = FailureDocumentation(
            failure_id=failure_id,
            status="Documented",
            documentation_complete=True,
            network_impact=network_impact,
            consciousness_update=consciousness_update,
            alerts_triggered=alerts,
            recommendations_generated=failure_report.get("recommendations", []),
            linked_patterns=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.documented_failures[failure_id] = doc

        return {
            "failure_id": failure_id,
            "status": "Documented",
            "network_impact": network_impact,
            "consciousness_update": consciousness_update,
            "alerts_triggered": len(alerts)
        }

    async def get_documentation(
        self,
        failure_id: str
    ) -> Optional[FailureDocumentation]:
        """Retrieve failure documentation by ID."""
        return self.documented_failures.get(failure_id)

    async def _assess_network_impact(
        self,
        failed_part: Any,
        analysis_result: Any
    ) -> Dict[str, Any]:
        """Assess impact on the UPC network."""
        return {
            "similar_reports_linked": analysis_result.similar_failures_count,
            "pattern_detected": analysis_result.similar_failures_count > 5,
            "affected_part_types": [getattr(failed_part, 'part_type', 'Unknown')],
            "severity_assessment": "High" if analysis_result.similar_failures_count > 10 else "Normal"
        }

    async def _generate_consciousness_update(
        self,
        failed_part: Any,
        analysis_result: Any
    ) -> Dict[str, Any]:
        """Generate consciousness update based on failure."""
        failure_mode = str(analysis_result.failure_mode.value
                         if hasattr(analysis_result.failure_mode, 'value')
                         else analysis_result.failure_mode)

        # Determine risk flags to add
        risk_flags = {
            "hydrogen_embrittlement": "hydrogen_embrittlement_susceptible",
            "high_cycle_fatigue": "fatigue_sensitive",
            "galvanic_corrosion": "galvanic_compatibility_required",
            "stress_corrosion_cracking": "scc_susceptible",
        }

        new_flag = risk_flags.get(failure_mode)

        return {
            "part_type": getattr(failed_part, 'part_type', 'Unknown'),
            "new_risk_flag": new_flag,
            "failure_mode_recorded": failure_mode,
            "consciousness_level_impact": "+0.05",
            "knowledge_added": analysis_result.network_learning
        }

    async def _check_alert_triggers(
        self,
        failed_part: Any,
        analysis_result: Any
    ) -> List[Dict[str, Any]]:
        """Check if alerts should be triggered."""
        alerts = []

        # Alert if many similar failures
        if analysis_result.similar_failures_count > 10:
            alerts.append({
                "type": "Pattern alert",
                "recipients": "Users with similar parts",
                "count": analysis_result.similar_failures_count * 10
            })

        # Alert for hydrogen embrittlement
        failure_mode = str(analysis_result.failure_mode.value
                         if hasattr(analysis_result.failure_mode, 'value')
                         else analysis_result.failure_mode)

        if failure_mode == "hydrogen_embrittlement":
            alerts.append({
                "type": "Safety alert",
                "recipients": "Users with similar high-strength fasteners",
                "count": 100
            })

        return alerts

    async def _link_to_patterns(
        self,
        analysis_result: Any
    ) -> List[str]:
        """Link failure to existing patterns."""
        # Would query pattern database in production
        if analysis_result.similar_failures_count > 5:
            return [f"PATTERN-AUTO-{analysis_result.failure_mode.value[:3].upper()}"]
        return []

    def _generate_failure_id(self) -> str:
        """Generate unique failure ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        import random
        random_suffix = random.randint(1000, 9999)
        return f"FAIL-{timestamp}-{random_suffix}"
