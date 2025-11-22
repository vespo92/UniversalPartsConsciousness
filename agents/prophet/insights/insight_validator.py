"""
Insight Validator
Validates and scores insights for accuracy and relevance.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
import logging

from .insight_generator import Insight


logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of insight validation"""
    insight_id: str = ""
    is_valid: bool = True
    validation_score: Decimal = Decimal("0.0")
    validation_type: str = ""  # automated, peer_review, outcome_based

    # Details
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    # Metadata
    validated_by: str = "automated"
    validated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "insight_id": self.insight_id,
            "is_valid": self.is_valid,
            "validation_score": float(self.validation_score),
            "validation_type": self.validation_type,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at.isoformat(),
        }


class InsightValidator:
    """
    Validates insights for quality, accuracy, and actionability.

    Validation layers:
    1. Structural validation (required fields, data types)
    2. Logical validation (consistency, plausibility)
    3. Evidence validation (supporting data quality)
    4. Actionability validation (actionable recommendations)
    """

    def __init__(
        self,
        min_confidence: float = 0.3,
        min_evidence_count: int = 1,
        require_actions: bool = True,
    ):
        self.min_confidence = min_confidence
        self.min_evidence_count = min_evidence_count
        self.require_actions = require_actions
        self._validation_history: List[ValidationResult] = []

    def validate(self, insight: Insight) -> ValidationResult:
        """
        Validate a single insight.

        Args:
            insight: The insight to validate

        Returns:
            ValidationResult with validation details
        """
        result = ValidationResult(
            insight_id=insight.id,
            validation_type="automated",
        )

        errors = []
        warnings = []
        suggestions = []
        score = Decimal("1.0")

        # Structural validation
        struct_errors, struct_warnings = self._validate_structure(insight)
        errors.extend(struct_errors)
        warnings.extend(struct_warnings)

        # Logical validation
        logic_errors, logic_warnings = self._validate_logic(insight)
        errors.extend(logic_errors)
        warnings.extend(logic_warnings)

        # Evidence validation
        evidence_errors, evidence_warnings, evidence_suggestions = self._validate_evidence(insight)
        errors.extend(evidence_errors)
        warnings.extend(evidence_warnings)
        suggestions.extend(evidence_suggestions)

        # Actionability validation
        action_errors, action_warnings, action_suggestions = self._validate_actionability(insight)
        errors.extend(action_errors)
        warnings.extend(action_warnings)
        suggestions.extend(action_suggestions)

        # Calculate score
        score -= Decimal("0.3") * len(errors)
        score -= Decimal("0.1") * len(warnings)
        score = max(Decimal("0.0"), min(Decimal("1.0"), score))

        result.is_valid = len(errors) == 0
        result.validation_score = score
        result.errors = errors
        result.warnings = warnings
        result.suggestions = suggestions

        self._validation_history.append(result)

        logger.info(
            f"Validated insight {insight.id}: valid={result.is_valid}, "
            f"score={float(result.validation_score):.2f}"
        )

        return result

    def validate_batch(self, insights: List[Insight]) -> List[ValidationResult]:
        """Validate multiple insights"""
        return [self.validate(insight) for insight in insights]

    def _validate_structure(self, insight: Insight) -> tuple:
        """Validate structural requirements"""
        errors = []
        warnings = []

        # Required fields
        if not insight.title:
            errors.append("Missing title")
        if not insight.summary:
            errors.append("Missing summary")
        if not insight.insight_type:
            warnings.append("Missing insight type")

        # Field lengths
        if insight.title and len(insight.title) > 200:
            warnings.append("Title exceeds recommended length (200 chars)")
        if insight.summary and len(insight.summary) > 500:
            warnings.append("Summary exceeds recommended length (500 chars)")

        return errors, warnings

    def _validate_logic(self, insight: Insight) -> tuple:
        """Validate logical consistency"""
        errors = []
        warnings = []

        # Confidence check
        if float(insight.confidence) < self.min_confidence:
            warnings.append(f"Low confidence ({float(insight.confidence):.2f})")

        # Impact score check
        if float(insight.impact_score) <= 0:
            warnings.append("Zero or negative impact score")

        # Priority consistency
        priority_thresholds = {
            "critical": 0.8,
            "high": 0.6,
            "medium": 0.4,
            "low": 0.0,
        }

        expected_priority = "low"
        for priority, threshold in sorted(priority_thresholds.items(), key=lambda x: -x[1]):
            if float(insight.impact_score) >= threshold:
                expected_priority = priority
                break

        if insight.priority != expected_priority:
            warnings.append(
                f"Priority '{insight.priority}' may not match impact score "
                f"(expected '{expected_priority}')"
            )

        return errors, warnings

    def _validate_evidence(self, insight: Insight) -> tuple:
        """Validate supporting evidence"""
        errors = []
        warnings = []
        suggestions = []

        evidence_count = len(insight.supporting_evidence)

        if evidence_count < self.min_evidence_count:
            if self.min_evidence_count == 1:
                errors.append("No supporting evidence provided")
            else:
                warnings.append(
                    f"Insufficient evidence ({evidence_count}/{self.min_evidence_count})"
                )

        # Check evidence quality
        for i, evidence in enumerate(insight.supporting_evidence):
            if not evidence:
                warnings.append(f"Empty evidence item at index {i}")
            elif isinstance(evidence, dict) and not evidence.keys():
                warnings.append(f"Evidence item {i} has no data")

        if evidence_count < 3:
            suggestions.append("Consider adding more supporting evidence")

        return errors, warnings, suggestions

    def _validate_actionability(self, insight: Insight) -> tuple:
        """Validate actionability of the insight"""
        errors = []
        warnings = []
        suggestions = []

        if self.require_actions and not insight.recommended_actions:
            errors.append("No recommended actions provided")

        if insight.recommended_actions:
            if len(insight.recommended_actions) > 5:
                warnings.append("Too many recommended actions (max 5)")

            for action in insight.recommended_actions:
                if len(action) < 10:
                    warnings.append(f"Action too brief: '{action}'")
                if not any(verb in action.lower() for verb in [
                    "investigate", "review", "update", "implement", "monitor",
                    "document", "evaluate", "develop", "create", "apply",
                    "conduct", "share", "validate", "prepare", "check",
                ]):
                    suggestions.append(f"Action may lack actionable verb: '{action}'")

        return errors, warnings, suggestions

    def get_validation_stats(self) -> Dict[str, Any]:
        """Get statistics on validation history"""
        if not self._validation_history:
            return {
                "total_validated": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "average_score": 0.0,
            }

        valid_count = sum(1 for r in self._validation_history if r.is_valid)
        scores = [float(r.validation_score) for r in self._validation_history]

        return {
            "total_validated": len(self._validation_history),
            "valid_count": valid_count,
            "invalid_count": len(self._validation_history) - valid_count,
            "valid_rate": valid_count / len(self._validation_history),
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
        }

    def get_invalid_insights(self) -> List[ValidationResult]:
        """Get all invalid validation results"""
        return [r for r in self._validation_history if not r.is_valid]
