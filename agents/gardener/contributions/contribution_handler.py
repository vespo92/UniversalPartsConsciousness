"""
Contribution Handler - Submission and processing of community contributions

Handles the lifecycle of contributions from submission through initial validation.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from ..models import (
    Contribution,
    ContributionType,
    CommunityUser,
    VerificationStatus,
    GardenerMessage,
    GardenerTopics,
)


@dataclass
class SubmissionResult:
    """Result of a contribution submission"""
    success: bool
    contribution_id: str
    contribution: Optional[Contribution] = None
    errors: List[str] = None
    warnings: List[str] = None
    next_steps: List[str] = None

    def __post_init__(self):
        self.errors = self.errors or []
        self.warnings = self.warnings or []
        self.next_steps = self.next_steps or []


class ContributionHandler:
    """
    Handles contribution submissions from the community.

    Responsibilities:
    - Accept and validate contribution submissions
    - Assign contribution IDs
    - Queue contributions for verification
    - Track contribution lifecycle
    """

    # Valid contribution fields by type
    REQUIRED_FIELDS = {
        ContributionType.PART_DATA: [
            "part_number", "manufacturer", "description"
        ],
        ContributionType.MEASUREMENT: [
            "part_id", "measurement_type", "value", "unit"
        ],
        ContributionType.FAILURE_REPORT: [
            "part_id", "failure_mode", "conditions", "description"
        ],
        ContributionType.CORRECTION: [
            "target_contribution_id", "field", "original_value", "corrected_value", "reason"
        ],
        ContributionType.PHOTO: [
            "part_id", "photo_type", "file_reference"
        ],
        ContributionType.CAD_MODEL: [
            "part_id", "model_format", "file_reference"
        ],
        ContributionType.APPLICATION_NOTE: [
            "part_id", "application", "notes"
        ],
        ContributionType.CROSS_REFERENCE: [
            "source_part_id", "target_part_id", "relationship_type"
        ],
        ContributionType.TRIBAL_KNOWLEDGE: [
            "category", "topic", "knowledge", "source_experience"
        ],
    }

    def __init__(self, db_connection=None, message_bus=None):
        self.db = db_connection
        self.message_bus = message_bus

    def submit_contribution(
        self,
        user: CommunityUser,
        contribution_type: ContributionType,
        content: Dict[str, Any],
        target_part_id: Optional[UUID] = None,
    ) -> SubmissionResult:
        """
        Submit a new contribution from a community member.

        Args:
            user: The submitting user
            contribution_type: Type of contribution
            content: Contribution content/data
            target_part_id: Optional target part UUID

        Returns:
            SubmissionResult with status and contribution details
        """
        errors = []
        warnings = []

        # Check user permissions
        if "submit" not in user.permissions:
            return SubmissionResult(
                success=False,
                contribution_id="",
                errors=["User does not have permission to submit contributions"]
            )

        # Check user status
        if user.status != "active":
            return SubmissionResult(
                success=False,
                contribution_id="",
                errors=[f"User account is {user.status}. Cannot submit contributions."]
            )

        # Validate required fields
        field_validation = self._validate_required_fields(contribution_type, content)
        if not field_validation["valid"]:
            errors.extend(field_validation["errors"])
            return SubmissionResult(
                success=False,
                contribution_id="",
                errors=errors
            )
        warnings.extend(field_validation.get("warnings", []))

        # Format validation
        format_validation = self._validate_content_format(contribution_type, content)
        if not format_validation["valid"]:
            errors.extend(format_validation["errors"])
            return SubmissionResult(
                success=False,
                contribution_id="",
                errors=errors
            )
        warnings.extend(format_validation.get("warnings", []))

        # Create contribution
        contribution = Contribution(
            user_id=user.id,
            contribution_type=contribution_type,
            target_part_id=target_part_id,
            content=content,
            verification_status=VerificationStatus.PENDING,
        )
        contribution.generate_contribution_id()

        # Store contribution
        stored = self._store_contribution(contribution)
        if not stored:
            return SubmissionResult(
                success=False,
                contribution_id="",
                errors=["Failed to store contribution. Please try again."]
            )

        # Update user statistics
        self._update_user_stats(user, contribution)

        # Determine next steps
        next_steps = self._determine_next_steps(contribution, user)

        return SubmissionResult(
            success=True,
            contribution_id=contribution.contribution_id,
            contribution=contribution,
            warnings=warnings if warnings else None,
            next_steps=next_steps
        )

    def _validate_required_fields(
        self,
        contribution_type: ContributionType,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate that all required fields are present"""
        required = self.REQUIRED_FIELDS.get(contribution_type, [])
        missing = [field for field in required if field not in content or not content[field]]

        if missing:
            return {
                "valid": False,
                "errors": [f"Missing required fields: {', '.join(missing)}"]
            }

        return {"valid": True, "errors": [], "warnings": []}

    def _validate_content_format(
        self,
        contribution_type: ContributionType,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate content format and data types"""
        errors = []
        warnings = []

        # Type-specific validation
        if contribution_type == ContributionType.MEASUREMENT:
            # Validate measurement value is numeric
            value = content.get("value")
            if not isinstance(value, (int, float)):
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors.append("Measurement value must be numeric")

            # Validate unit is provided
            unit = content.get("unit", "")
            if not unit:
                errors.append("Measurement unit is required")

        elif contribution_type == ContributionType.PART_DATA:
            # Validate part number format
            part_number = content.get("part_number", "")
            if len(part_number) < 3:
                errors.append("Part number must be at least 3 characters")
            if not any(c.isalnum() for c in part_number):
                errors.append("Part number must contain alphanumeric characters")

        elif contribution_type == ContributionType.FAILURE_REPORT:
            # Validate failure mode description length
            failure_mode = content.get("failure_mode", "")
            if len(failure_mode) < 10:
                warnings.append("Consider providing more detail in failure mode description")

        elif contribution_type == ContributionType.PHOTO:
            # Validate file reference
            file_ref = content.get("file_reference", "")
            valid_extensions = [".jpg", ".jpeg", ".png", ".webp", ".heic"]
            if not any(file_ref.lower().endswith(ext) for ext in valid_extensions):
                errors.append(f"Photo must be one of: {', '.join(valid_extensions)}")

        elif contribution_type == ContributionType.CAD_MODEL:
            # Validate CAD format
            model_format = content.get("model_format", "").upper()
            valid_formats = ["STEP", "IGES", "STL", "OBJ", "DXF", "DWG"]
            if model_format not in valid_formats:
                errors.append(f"CAD format must be one of: {', '.join(valid_formats)}")

        if errors:
            return {"valid": False, "errors": errors, "warnings": warnings}

        return {"valid": True, "errors": [], "warnings": warnings}

    def _store_contribution(self, contribution: Contribution) -> bool:
        """Store contribution in database"""
        if self.db is None:
            # In-memory storage for testing
            return True

        try:
            # Store in database
            # self.db.contributions.insert(contribution)
            return True
        except Exception:
            return False

    def _update_user_stats(self, user: CommunityUser, contribution: Contribution):
        """Update user statistics after submission"""
        user.contribution_count += 1
        user.last_contribution = datetime.now()

        # Update streak
        if user.last_contribution:
            days_since = (datetime.now() - user.last_contribution).days
            if days_since <= 1:
                user.streak_days += 1
            elif days_since > 1:
                user.streak_days = 1
        else:
            user.streak_days = 1

    def _determine_next_steps(
        self,
        contribution: Contribution,
        user: CommunityUser
    ) -> List[str]:
        """Determine and explain next steps for the contribution"""
        steps = []

        steps.append(f"Contribution {contribution.contribution_id} submitted successfully")
        steps.append("Automated verification will begin shortly")

        # Based on contribution type and user reputation
        if user.lifetime_points < 100:
            steps.append("As a new contributor, your submission will undergo peer review")
        elif contribution.contribution_type in [
            ContributionType.CAD_MODEL,
            ContributionType.FAILURE_REPORT
        ]:
            steps.append("This contribution type requires additional verification")

        steps.append("You will be notified when verification is complete")

        return steps

    def get_contribution(self, contribution_id: str) -> Optional[Contribution]:
        """Retrieve a contribution by ID"""
        if self.db is None:
            return None

        # Query database
        # return self.db.contributions.find_one({"contribution_id": contribution_id})
        return None

    def get_user_contributions(
        self,
        user_id: UUID,
        status: Optional[VerificationStatus] = None,
        limit: int = 50
    ) -> List[Contribution]:
        """Get contributions by a user"""
        if self.db is None:
            return []

        # Query database
        # query = {"user_id": user_id}
        # if status:
        #     query["verification_status"] = status
        # return self.db.contributions.find(query).limit(limit)
        return []

    def update_contribution_status(
        self,
        contribution_id: str,
        new_status: VerificationStatus,
        notes: str = ""
    ) -> bool:
        """Update contribution verification status"""
        if self.db is None:
            return True

        try:
            # self.db.contributions.update(
            #     {"contribution_id": contribution_id},
            #     {"$set": {
            #         "verification_status": new_status,
            #         "resolution_notes": notes
            #     }}
            # )
            return True
        except Exception:
            return False
