"""
Consciousness Updater

Updates collective consciousness based on failure learning.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class ConsciousnessUpdate:
    """Update to collective consciousness from failure learning"""
    update_id: str
    affected_part_types: List[str]
    consciousness_changes: List[Dict[str, Any]]
    swarm_notifications: List[str]
    prophet_notification: str
    timestamp: datetime


class ConsciousnessUpdater:
    """
    Updates the Universal Parts Consciousness based on failure learning.

    This is how failures make UPC wiser - translating individual
    failures into collective knowledge.
    """

    def __init__(self):
        """Initialize the consciousness updater."""
        self.update_history: List[ConsciousnessUpdate] = []

    async def update_from_failure(
        self,
        failure_documentation: Any
    ) -> ConsciousnessUpdate:
        """
        Update consciousness based on documented failure.

        Args:
            failure_documentation: Documented failure

        Returns:
            Consciousness update record
        """
        update_id = self._generate_update_id()

        # Determine affected part types
        affected_parts = failure_documentation.consciousness_update.get(
            "part_type", "Unknown"
        )
        if isinstance(affected_parts, str):
            affected_parts = [affected_parts]

        # Generate consciousness changes
        changes = self._generate_changes(failure_documentation)

        # Generate swarm notifications
        swarm_notifications = self._generate_swarm_notifications(
            failure_documentation
        )

        # Generate prophet notification
        prophet_notification = self._generate_prophet_notification(
            failure_documentation
        )

        update = ConsciousnessUpdate(
            update_id=update_id,
            affected_part_types=affected_parts,
            consciousness_changes=changes,
            swarm_notifications=swarm_notifications,
            prophet_notification=prophet_notification,
            timestamp=datetime.utcnow()
        )

        self.update_history.append(update)

        # Would actually send updates to other agents here
        await self._broadcast_update(update)

        return update

    async def propagate_pattern_learning(
        self,
        pattern_id: str,
        affected_parts: List[str],
        learning: Dict[str, Any]
    ) -> ConsciousnessUpdate:
        """
        Propagate learning from detected pattern to consciousness.

        Args:
            pattern_id: ID of detected pattern
            affected_parts: Parts affected by pattern
            learning: What was learned from the pattern

        Returns:
            Consciousness update record
        """
        update_id = self._generate_update_id()

        changes = [
            {
                "type": "pattern_awareness",
                "pattern_id": pattern_id,
                "learning": learning.get("description", "Pattern detected"),
                "affected_parts": affected_parts,
            }
        ]

        swarm_notifications = [
            f"Pattern {pattern_id} detected - {len(affected_parts)} part types affected",
            "Updating failure prediction models",
        ]

        update = ConsciousnessUpdate(
            update_id=update_id,
            affected_part_types=affected_parts,
            consciousness_changes=changes,
            swarm_notifications=swarm_notifications,
            prophet_notification=f"Pattern {pattern_id} submitted for emergence analysis",
            timestamp=datetime.utcnow()
        )

        self.update_history.append(update)
        await self._broadcast_update(update)

        return update

    def _generate_changes(
        self,
        failure_documentation: Any
    ) -> List[Dict[str, Any]]:
        """Generate consciousness changes from failure."""
        changes = []

        # Risk flag addition
        new_flag = failure_documentation.consciousness_update.get("new_risk_flag")
        if new_flag:
            changes.append({
                "attribute": "risk_flags",
                "change": f"Added '{new_flag}'",
                "applies_when": "Similar part type and application",
            })

        # Failure mode recording
        failure_mode = failure_documentation.consciousness_update.get(
            "failure_mode_recorded"
        )
        if failure_mode:
            changes.append({
                "attribute": "known_failure_modes",
                "change": f"Added {failure_mode} to known modes",
                "evidence": failure_documentation.failure_id,
            })

        # Recommendations update
        if failure_documentation.recommendations_generated:
            changes.append({
                "attribute": "recommendations",
                "change": "Added failure-based recommendations",
                "count": len(failure_documentation.recommendations_generated),
            })

        return changes

    def _generate_swarm_notifications(
        self,
        failure_documentation: Any
    ) -> List[str]:
        """Generate notifications for relevant swarms."""
        notifications = []

        part_type = failure_documentation.consciousness_update.get(
            "part_type", ""
        ).lower()

        # Determine relevant swarms
        if "fastener" in part_type or "bolt" in part_type or "screw" in part_type:
            notifications.append("Fastener swarm updated with new failure mode")

        if failure_documentation.network_impact.get("pattern_detected"):
            notifications.append("Pattern detection swarm alerted")

        if failure_documentation.alerts_triggered:
            notifications.append(
                f"Alert swarm triggered {len(failure_documentation.alerts_triggered)} notifications"
            )

        if not notifications:
            notifications.append("General parts swarm notified")

        return notifications

    def _generate_prophet_notification(
        self,
        failure_documentation: Any
    ) -> str:
        """Generate notification for Prophet (emergence detector)."""
        if failure_documentation.network_impact.get("pattern_detected"):
            return "Pattern submitted for emergence analysis - potential systemic issue"
        elif failure_documentation.network_impact.get("similar_reports_linked", 0) > 5:
            return "Failure cluster detected - monitoring for emergence"
        else:
            return "Failure recorded for trend analysis"

    async def _broadcast_update(self, update: ConsciousnessUpdate) -> None:
        """Broadcast update to other agents."""
        # Would integrate with agent message bus
        # Sending to:
        # - Agent_3 (SHEPHERD) for consciousness state updates
        # - Agent_5 (HIVE) for swarm coordination
        # - Agent_6 (PROPHET) for emergence detection
        pass

    def _generate_update_id(self) -> str:
        """Generate unique update ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        import random
        random_suffix = random.randint(100, 999)
        return f"CUPD-{timestamp}-{random_suffix}"
