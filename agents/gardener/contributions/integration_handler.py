"""
Integration Handler - Merges verified contributions into main database

Handles the final integration of approved contributions into the main
parts database and triggers downstream updates.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..models import (
    Contribution,
    ContributionType,
    GardenerMessage,
    GardenerTopics,
)


@dataclass
class IntegrationResult:
    """Result of contribution integration"""
    success: bool
    merged_records: int = 0
    updated_records: int = 0
    errors: List[str] = None
    warnings: List[str] = None
    affected_parts: List[UUID] = None

    def __post_init__(self):
        self.errors = self.errors or []
        self.warnings = self.warnings or []
        self.affected_parts = self.affected_parts or []


class IntegrationHandler:
    """
    Integrates verified contributions into the main parts database.

    Responsibilities:
    - Transform contribution data to database format
    - Merge new data with existing records
    - Handle conflicts and duplicates
    - Trigger consciousness updates
    - Maintain audit trail
    """

    def __init__(self, db_connection=None, message_bus=None):
        self.db = db_connection
        self.message_bus = message_bus

    async def integrate(self, contribution: Contribution) -> IntegrationResult:
        """
        Integrate an approved contribution into the main database.

        Args:
            contribution: The approved contribution to integrate

        Returns:
            IntegrationResult with details of the integration
        """
        try:
            # Route to type-specific handler
            handler = self._get_handler(contribution.contribution_type)
            result = await handler(contribution)

            if result.success:
                # Update contribution status
                contribution.resolution = "merged"
                contribution.resolved_at = datetime.now()

                # Trigger consciousness update for affected parts
                await self._trigger_consciousness_update(result.affected_parts)

                # Record integration in audit log
                await self._record_audit(contribution, result)

            return result

        except Exception as e:
            return IntegrationResult(
                success=False,
                errors=[f"Integration failed: {str(e)}"]
            )

    def _get_handler(self, contribution_type: ContributionType):
        """Get the appropriate handler for contribution type"""
        handlers = {
            ContributionType.PART_DATA: self._integrate_part_data,
            ContributionType.MEASUREMENT: self._integrate_measurement,
            ContributionType.FAILURE_REPORT: self._integrate_failure_report,
            ContributionType.CORRECTION: self._integrate_correction,
            ContributionType.PHOTO: self._integrate_photo,
            ContributionType.CAD_MODEL: self._integrate_cad_model,
            ContributionType.APPLICATION_NOTE: self._integrate_application_note,
            ContributionType.CROSS_REFERENCE: self._integrate_cross_reference,
            ContributionType.TRIBAL_KNOWLEDGE: self._integrate_tribal_knowledge,
        }
        return handlers.get(contribution_type, self._integrate_generic)

    async def _integrate_part_data(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate new part data"""
        content = contribution.content
        affected_parts = []
        merged = 0
        updated = 0

        # Check if part already exists
        existing_part = await self._find_existing_part(
            content.get("part_number"),
            content.get("manufacturer")
        )

        if existing_part:
            # Update existing part with new data
            update_fields = self._extract_update_fields(content, existing_part)
            if update_fields:
                await self._update_part(existing_part["id"], update_fields, contribution)
                updated = 1
                affected_parts.append(existing_part["id"])
        else:
            # Create new part record
            new_part_id = await self._create_part(content, contribution)
            if new_part_id:
                merged = 1
                affected_parts.append(new_part_id)

        return IntegrationResult(
            success=True,
            merged_records=merged,
            updated_records=updated,
            affected_parts=affected_parts
        )

    async def _integrate_measurement(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate measurement data"""
        content = contribution.content
        part_id = contribution.target_part_id

        if not part_id:
            return IntegrationResult(
                success=False,
                errors=["No target part specified for measurement"]
            )

        # Add measurement to part's measurement history
        measurement_record = {
            "type": content.get("measurement_type"),
            "value": content.get("value"),
            "unit": content.get("unit"),
            "method": content.get("measurement_method"),
            "conditions": content.get("conditions", {}),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "measured_at": datetime.now().isoformat(),
            "confidence": float(contribution.confidence_score or 0.8)
        }

        await self._add_measurement(part_id, measurement_record)

        return IntegrationResult(
            success=True,
            merged_records=1,
            affected_parts=[part_id]
        )

    async def _integrate_failure_report(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate failure report"""
        content = contribution.content
        part_id = contribution.target_part_id

        failure_record = {
            "failure_mode": content.get("failure_mode"),
            "description": content.get("description"),
            "conditions": content.get("conditions"),
            "root_cause": content.get("root_cause"),
            "prevention": content.get("prevention"),
            "severity": content.get("severity", "unknown"),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "reported_at": datetime.now().isoformat(),
            "verified": True
        }

        await self._add_failure_mode(part_id, failure_record)

        return IntegrationResult(
            success=True,
            merged_records=1,
            affected_parts=[part_id] if part_id else []
        )

    async def _integrate_correction(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate correction to existing data"""
        content = contribution.content
        target_id = content.get("target_contribution_id")
        field = content.get("field")
        corrected_value = content.get("corrected_value")

        # Apply correction to target contribution's data
        correction_record = {
            "field": field,
            "original_value": content.get("original_value"),
            "corrected_value": corrected_value,
            "reason": content.get("reason"),
            "corrector_id": str(contribution.user_id),
            "correction_id": contribution.contribution_id,
            "applied_at": datetime.now().isoformat()
        }

        await self._apply_correction(target_id, correction_record)

        return IntegrationResult(
            success=True,
            updated_records=1
        )

    async def _integrate_photo(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate photo contribution"""
        content = contribution.content
        part_id = contribution.target_part_id

        photo_record = {
            "photo_type": content.get("photo_type"),
            "file_reference": content.get("file_reference"),
            "description": content.get("description", ""),
            "angle": content.get("angle"),
            "scale_reference": content.get("scale_reference"),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "uploaded_at": datetime.now().isoformat()
        }

        await self._add_photo(part_id, photo_record)

        return IntegrationResult(
            success=True,
            merged_records=1,
            affected_parts=[part_id] if part_id else []
        )

    async def _integrate_cad_model(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate CAD model contribution"""
        content = contribution.content
        part_id = contribution.target_part_id

        model_record = {
            "model_format": content.get("model_format"),
            "file_reference": content.get("file_reference"),
            "version": content.get("version", "1.0"),
            "units": content.get("units", "mm"),
            "notes": content.get("notes", ""),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "uploaded_at": datetime.now().isoformat()
        }

        await self._add_cad_model(part_id, model_record)

        return IntegrationResult(
            success=True,
            merged_records=1,
            affected_parts=[part_id] if part_id else []
        )

    async def _integrate_application_note(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate application note"""
        content = contribution.content
        part_id = contribution.target_part_id

        note_record = {
            "application": content.get("application"),
            "notes": content.get("notes"),
            "warnings": content.get("warnings", []),
            "recommendations": content.get("recommendations", []),
            "related_parts": content.get("related_parts", []),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "created_at": datetime.now().isoformat()
        }

        await self._add_application_note(part_id, note_record)

        return IntegrationResult(
            success=True,
            merged_records=1,
            affected_parts=[part_id] if part_id else []
        )

    async def _integrate_cross_reference(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate cross-reference between parts"""
        content = contribution.content
        source_id = content.get("source_part_id")
        target_id = content.get("target_part_id")

        xref_record = {
            "source_part_id": source_id,
            "target_part_id": target_id,
            "relationship_type": content.get("relationship_type"),
            "confidence": float(contribution.confidence_score or 0.8),
            "notes": content.get("notes", ""),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "created_at": datetime.now().isoformat()
        }

        await self._add_cross_reference(xref_record)

        affected = []
        if source_id:
            affected.append(UUID(source_id) if isinstance(source_id, str) else source_id)
        if target_id:
            affected.append(UUID(target_id) if isinstance(target_id, str) else target_id)

        return IntegrationResult(
            success=True,
            merged_records=1,
            affected_parts=affected
        )

    async def _integrate_tribal_knowledge(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Integrate tribal knowledge"""
        content = contribution.content

        knowledge_record = {
            "category": content.get("category"),
            "topic": content.get("topic"),
            "knowledge": content.get("knowledge"),
            "source_experience": content.get("source_experience"),
            "related_parts": content.get("related_parts", []),
            "tags": content.get("tags", []),
            "contributor_id": str(contribution.user_id),
            "contribution_id": contribution.contribution_id,
            "created_at": datetime.now().isoformat(),
            "verified": True
        }

        await self._add_tribal_knowledge(knowledge_record)

        return IntegrationResult(
            success=True,
            merged_records=1
        )

    async def _integrate_generic(
        self,
        contribution: Contribution
    ) -> IntegrationResult:
        """Generic integration for unknown types"""
        return IntegrationResult(
            success=False,
            errors=[f"No handler for contribution type: {contribution.contribution_type}"]
        )

    async def _trigger_consciousness_update(self, part_ids: List[UUID]):
        """Trigger consciousness update for affected parts via Agent_3"""
        if not self.message_bus or not part_ids:
            return

        for part_id in part_ids:
            await self.message_bus.publish(GardenerMessage(
                target_agent="Agent_3_Shepherd",
                topic="upc.consciousness.update.triggered",
                message_type="data_updated",
                payload={
                    "part_id": str(part_id),
                    "source": "community_contribution",
                    "timestamp": datetime.now().isoformat()
                }
            ))

    async def _record_audit(
        self,
        contribution: Contribution,
        result: IntegrationResult
    ):
        """Record integration in audit log"""
        audit_record = {
            "contribution_id": contribution.contribution_id,
            "user_id": str(contribution.user_id),
            "type": contribution.contribution_type.value,
            "merged_records": result.merged_records,
            "updated_records": result.updated_records,
            "affected_parts": [str(p) for p in result.affected_parts],
            "integrated_at": datetime.now().isoformat()
        }

        # Store audit record
        # await self.db.audit_log.insert(audit_record)

    # Database operation stubs (implement with actual DB)
    async def _find_existing_part(self, part_number: str, manufacturer: str) -> Optional[Dict]:
        return None

    def _extract_update_fields(self, content: Dict, existing: Dict) -> Dict:
        return {}

    async def _update_part(self, part_id: UUID, fields: Dict, contribution: Contribution):
        pass

    async def _create_part(self, content: Dict, contribution: Contribution) -> Optional[UUID]:
        return None

    async def _add_measurement(self, part_id: UUID, record: Dict):
        pass

    async def _add_failure_mode(self, part_id: UUID, record: Dict):
        pass

    async def _apply_correction(self, target_id: str, record: Dict):
        pass

    async def _add_photo(self, part_id: UUID, record: Dict):
        pass

    async def _add_cad_model(self, part_id: UUID, record: Dict):
        pass

    async def _add_application_note(self, part_id: UUID, record: Dict):
        pass

    async def _add_cross_reference(self, record: Dict):
        pass

    async def _add_tribal_knowledge(self, record: Dict):
        pass
