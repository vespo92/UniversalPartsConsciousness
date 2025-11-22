"""
Automated Verifier - Tier 1 automated verification of contributions

Performs automated checks including format validation, duplicate detection,
physical plausibility, and cross-reference validation.
"""

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional

from ..models import (
    Contribution,
    ContributionType,
    VerificationCheck,
    AutoVerificationResult,
)


@dataclass
class PlausibilityRule:
    """Rule for physical plausibility checking"""
    field: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: str = ""
    description: str = ""


class AutoVerifier:
    """
    Tier 1 automated verification system.

    Performs automated checks on contributions:
    - Format validation
    - Duplicate detection
    - Physical plausibility
    - Cross-reference validation
    - Source validation
    """

    # Physical plausibility rules for common measurements
    PLAUSIBILITY_RULES = {
        "thread_diameter": [
            PlausibilityRule("value", min_value=0.5, max_value=300, unit="mm",
                           description="Thread diameter must be 0.5-300mm"),
        ],
        "thread_pitch": [
            PlausibilityRule("value", min_value=0.2, max_value=8, unit="mm",
                           description="Thread pitch must be 0.2-8mm"),
        ],
        "length": [
            PlausibilityRule("value", min_value=1, max_value=2000, unit="mm",
                           description="Part length must be 1-2000mm"),
        ],
        "weight": [
            PlausibilityRule("value", min_value=0.001, max_value=10000, unit="kg",
                           description="Part weight must be 0.001-10000kg"),
        ],
        "tensile_strength": [
            PlausibilityRule("value", min_value=100, max_value=3000, unit="MPa",
                           description="Tensile strength must be 100-3000 MPa"),
        ],
        "hardness_hrc": [
            PlausibilityRule("value", min_value=20, max_value=70, unit="HRC",
                           description="Hardness must be 20-70 HRC"),
        ],
        "temperature_rating": [
            PlausibilityRule("value", min_value=-273, max_value=3500, unit="C",
                           description="Temperature rating must be -273 to 3500C"),
        ],
    }

    # Known part number patterns by manufacturer
    PART_NUMBER_PATTERNS = {
        "generic": r"^[A-Z0-9][A-Z0-9\-_.]{2,50}$",
        "din": r"^DIN\s*\d{1,5}",
        "iso": r"^ISO\s*\d{1,5}",
        "ansi": r"^ANSI\s*[A-Z]?\d+",
    }

    def __init__(self, db_connection=None):
        self.db = db_connection
        self._known_parts_cache: Dict[str, Any] = {}

    async def verify(self, contribution: Contribution) -> AutoVerificationResult:
        """
        Run all automated verification checks on a contribution.

        Args:
            contribution: The contribution to verify

        Returns:
            AutoVerificationResult with status and details
        """
        checks: List[VerificationCheck] = []

        # Run all checks
        checks.append(self._check_format(contribution))
        checks.append(await self._check_duplicates(contribution))
        checks.append(self._check_plausibility(contribution))
        checks.append(await self._check_cross_references(contribution))
        checks.append(self._check_source(contribution))

        # Add type-specific checks
        type_checks = self._get_type_specific_checks(contribution)
        checks.extend(type_checks)

        # Aggregate results
        return self._aggregate_results(checks)

    def _check_format(self, contribution: Contribution) -> VerificationCheck:
        """Validate format and completeness of contribution"""
        content = contribution.content

        # Check for empty content
        if not content:
            return VerificationCheck(
                name="format_validation",
                passed=False,
                critical=True,
                reason="Contribution content is empty"
            )

        # Check for minimum content length
        content_str = str(content)
        if len(content_str) < 10:
            return VerificationCheck(
                name="format_validation",
                passed=False,
                critical=True,
                reason="Contribution content is too short"
            )

        # Check for suspicious patterns (spam indicators)
        spam_patterns = [
            r"https?://[^\s]+",  # URLs (except in application notes)
            r"\b(buy|sell|price|discount|offer)\b",  # Commercial terms
            r"(.)\1{5,}",  # Repeated characters
        ]

        if contribution.contribution_type != ContributionType.APPLICATION_NOTE:
            for pattern in spam_patterns:
                if re.search(pattern, content_str, re.IGNORECASE):
                    return VerificationCheck(
                        name="format_validation",
                        passed=False,
                        critical=True,
                        reason="Contribution contains suspicious content"
                    )

        # Part number format validation
        if contribution.contribution_type == ContributionType.PART_DATA:
            part_number = content.get("part_number", "")
            if not self._validate_part_number_format(part_number):
                return VerificationCheck(
                    name="format_validation",
                    passed=False,
                    warning=True,
                    reason=f"Part number format '{part_number}' may be invalid"
                )

        return VerificationCheck(
            name="format_validation",
            passed=True,
            details={"checks_passed": ["content_not_empty", "content_length", "no_spam"]}
        )

    async def _check_duplicates(self, contribution: Contribution) -> VerificationCheck:
        """Check for duplicate contributions"""
        content = contribution.content

        # Generate content fingerprint
        fingerprint = self._generate_fingerprint(contribution)

        # Check against recent contributions
        duplicate = await self._find_duplicate(fingerprint)

        if duplicate:
            return VerificationCheck(
                name="duplicate_detection",
                passed=False,
                critical=False,  # Not critical - could be update
                warning=True,
                reason=f"Similar contribution already exists: {duplicate['contribution_id']}",
                details={"duplicate_id": duplicate["contribution_id"]}
            )

        # Check for very similar content
        similar = await self._find_similar(contribution)
        if similar:
            return VerificationCheck(
                name="duplicate_detection",
                passed=True,
                warning=True,
                reason=f"Similar content found in {len(similar)} existing contributions",
                details={"similar_ids": [s["contribution_id"] for s in similar]}
            )

        return VerificationCheck(
            name="duplicate_detection",
            passed=True,
            details={"status": "no_duplicates_found"}
        )

    def _check_plausibility(self, contribution: Contribution) -> VerificationCheck:
        """Check physical plausibility of values"""
        content = contribution.content
        violations = []
        warnings = []

        # Check measurements against plausibility rules
        if contribution.contribution_type == ContributionType.MEASUREMENT:
            measurement_type = content.get("measurement_type", "").lower()
            value = content.get("value")
            unit = content.get("unit", "")

            rules = self.PLAUSIBILITY_RULES.get(measurement_type, [])
            for rule in rules:
                try:
                    numeric_value = float(value)
                    if rule.min_value is not None and numeric_value < rule.min_value:
                        violations.append(
                            f"{measurement_type}: {value} is below minimum {rule.min_value} {rule.unit}"
                        )
                    if rule.max_value is not None and numeric_value > rule.max_value:
                        violations.append(
                            f"{measurement_type}: {value} exceeds maximum {rule.max_value} {rule.unit}"
                        )
                except (ValueError, TypeError):
                    violations.append(f"Cannot parse {measurement_type} value: {value}")

        # Check part data plausibility
        if contribution.contribution_type == ContributionType.PART_DATA:
            # Validate dimensional relationships
            plausibility_result = self._check_dimensional_plausibility(content)
            if not plausibility_result["valid"]:
                violations.extend(plausibility_result["violations"])
            warnings.extend(plausibility_result.get("warnings", []))

        if violations:
            return VerificationCheck(
                name="plausibility_check",
                passed=False,
                critical=True,
                reason="; ".join(violations),
                details={"violations": violations}
            )

        if warnings:
            return VerificationCheck(
                name="plausibility_check",
                passed=True,
                warning=True,
                reason="; ".join(warnings),
                details={"warnings": warnings}
            )

        return VerificationCheck(
            name="plausibility_check",
            passed=True,
            details={"status": "all_values_plausible"}
        )

    async def _check_cross_references(
        self,
        contribution: Contribution
    ) -> VerificationCheck:
        """Validate cross-references to existing data"""
        content = contribution.content
        issues = []

        # Check target part exists
        if contribution.target_part_id:
            part_exists = await self._verify_part_exists(contribution.target_part_id)
            if not part_exists:
                issues.append(f"Target part {contribution.target_part_id} not found")

        # Check cross-reference contribution
        if contribution.contribution_type == ContributionType.CROSS_REFERENCE:
            source_id = content.get("source_part_id")
            target_id = content.get("target_part_id")

            if source_id:
                if not await self._verify_part_exists(source_id):
                    issues.append(f"Source part {source_id} not found")

            if target_id:
                if not await self._verify_part_exists(target_id):
                    issues.append(f"Target part {target_id} not found")

            if source_id == target_id:
                issues.append("Source and target part cannot be the same")

        # Check correction target
        if contribution.contribution_type == ContributionType.CORRECTION:
            target_contribution_id = content.get("target_contribution_id")
            if target_contribution_id:
                target_exists = await self._verify_contribution_exists(target_contribution_id)
                if not target_exists:
                    issues.append(f"Target contribution {target_contribution_id} not found")

        if issues:
            return VerificationCheck(
                name="cross_reference_validation",
                passed=False,
                critical=True,
                reason="; ".join(issues),
                details={"issues": issues}
            )

        return VerificationCheck(
            name="cross_reference_validation",
            passed=True,
            details={"status": "all_references_valid"}
        )

    def _check_source(self, contribution: Contribution) -> VerificationCheck:
        """Validate source information if provided"""
        content = contribution.content
        source = content.get("source")
        source_url = content.get("source_url")

        # If no source provided, that's okay but note it
        if not source and not source_url:
            return VerificationCheck(
                name="source_validation",
                passed=True,
                warning=True,
                reason="No source information provided",
                details={"has_source": False}
            )

        # Validate URL format if provided
        if source_url:
            if not self._is_valid_url(source_url):
                return VerificationCheck(
                    name="source_validation",
                    passed=False,
                    critical=False,
                    reason=f"Invalid source URL format: {source_url}"
                )

            # Check for blocked domains
            blocked_domains = ["spam.com", "fake.com", "test.com"]
            if any(domain in source_url for domain in blocked_domains):
                return VerificationCheck(
                    name="source_validation",
                    passed=False,
                    critical=True,
                    reason="Source URL is from a blocked domain"
                )

        return VerificationCheck(
            name="source_validation",
            passed=True,
            details={"source": source, "source_url": source_url}
        )

    def _get_type_specific_checks(
        self,
        contribution: Contribution
    ) -> List[VerificationCheck]:
        """Get additional checks specific to contribution type"""
        checks = []

        if contribution.contribution_type == ContributionType.CAD_MODEL:
            checks.append(self._check_cad_model_validity(contribution))

        elif contribution.contribution_type == ContributionType.FAILURE_REPORT:
            checks.append(self._check_failure_report_completeness(contribution))

        elif contribution.contribution_type == ContributionType.TRIBAL_KNOWLEDGE:
            checks.append(self._check_tribal_knowledge_quality(contribution))

        return checks

    def _check_cad_model_validity(self, contribution: Contribution) -> VerificationCheck:
        """Validate CAD model contribution"""
        content = contribution.content
        model_format = content.get("model_format", "").upper()
        file_ref = content.get("file_reference", "")

        valid_formats = ["STEP", "IGES", "STL", "OBJ", "DXF", "DWG"]
        if model_format not in valid_formats:
            return VerificationCheck(
                name="cad_model_validation",
                passed=False,
                critical=True,
                reason=f"Invalid CAD format: {model_format}"
            )

        # Check file extension matches format
        expected_extensions = {
            "STEP": [".step", ".stp"],
            "IGES": [".iges", ".igs"],
            "STL": [".stl"],
            "OBJ": [".obj"],
            "DXF": [".dxf"],
            "DWG": [".dwg"],
        }

        expected = expected_extensions.get(model_format, [])
        if not any(file_ref.lower().endswith(ext) for ext in expected):
            return VerificationCheck(
                name="cad_model_validation",
                passed=False,
                warning=True,
                reason=f"File extension doesn't match format {model_format}"
            )

        return VerificationCheck(
            name="cad_model_validation",
            passed=True,
            details={"format": model_format, "file": file_ref}
        )

    def _check_failure_report_completeness(
        self,
        contribution: Contribution
    ) -> VerificationCheck:
        """Check failure report has sufficient detail"""
        content = contribution.content
        warnings = []

        # Check description length
        description = content.get("description", "")
        if len(description) < 50:
            warnings.append("Failure description is very short - consider adding more detail")

        # Check conditions are specified
        conditions = content.get("conditions", {})
        if not conditions:
            warnings.append("Operating conditions not specified")

        # Check for severity
        if not content.get("severity"):
            warnings.append("Failure severity not specified")

        if warnings:
            return VerificationCheck(
                name="failure_report_completeness",
                passed=True,
                warning=True,
                reason="; ".join(warnings),
                details={"warnings": warnings}
            )

        return VerificationCheck(
            name="failure_report_completeness",
            passed=True,
            details={"status": "complete"}
        )

    def _check_tribal_knowledge_quality(
        self,
        contribution: Contribution
    ) -> VerificationCheck:
        """Check tribal knowledge contribution quality"""
        content = contribution.content
        knowledge = content.get("knowledge", "")

        # Check length - tribal knowledge should be substantive
        if len(knowledge) < 100:
            return VerificationCheck(
                name="tribal_knowledge_quality",
                passed=False,
                warning=True,
                reason="Tribal knowledge entry is too short - please provide more detail"
            )

        # Check for experience context
        if not content.get("source_experience"):
            return VerificationCheck(
                name="tribal_knowledge_quality",
                passed=True,
                warning=True,
                reason="No source experience provided - helps validate knowledge authenticity"
            )

        return VerificationCheck(
            name="tribal_knowledge_quality",
            passed=True,
            details={"length": len(knowledge)}
        )

    def _aggregate_results(
        self,
        checks: List[VerificationCheck]
    ) -> AutoVerificationResult:
        """Aggregate individual check results into final result"""
        failed_critical = [c for c in checks if not c.passed and c.critical]
        failed_non_critical = [c for c in checks if not c.passed and not c.critical]
        warnings = [c for c in checks if c.warning]

        # Critical failure = immediate rejection
        if failed_critical:
            return AutoVerificationResult(
                status="REJECTED",
                confidence=Decimal("0"),
                reason=failed_critical[0].reason,
                checks=checks,
                concerns=failed_critical,
                suggestions=self._generate_suggestions(failed_critical)
            )

        # Non-critical failures = needs review
        if failed_non_critical:
            return AutoVerificationResult(
                status="NEEDS_REVIEW",
                confidence=Decimal("0.6"),
                checks=checks,
                concerns=failed_non_critical,
                warnings=warnings
            )

        # Warnings only = needs review with higher confidence
        if warnings:
            return AutoVerificationResult(
                status="NEEDS_REVIEW",
                confidence=Decimal("0.8"),
                checks=checks,
                warnings=warnings,
                notes="All checks passed with warnings"
            )

        # All clear = approved
        return AutoVerificationResult(
            status="APPROVED",
            confidence=Decimal("0.95"),
            checks=checks,
            notes="All automated checks passed"
        )

    def _generate_suggestions(
        self,
        failed_checks: List[VerificationCheck]
    ) -> List[str]:
        """Generate suggestions based on failed checks"""
        suggestions = []

        for check in failed_checks:
            if check.name == "format_validation":
                suggestions.append("Review your submission for formatting issues")
            elif check.name == "duplicate_detection":
                suggestions.append("Check if this data already exists before resubmitting")
            elif check.name == "plausibility_check":
                suggestions.append("Verify your measurements are correct and in the right units")
            elif check.name == "cross_reference_validation":
                suggestions.append("Ensure all referenced parts exist in the database")

        return suggestions

    def _validate_part_number_format(self, part_number: str) -> bool:
        """Validate part number against known patterns"""
        if not part_number:
            return False

        for pattern_name, pattern in self.PART_NUMBER_PATTERNS.items():
            if re.match(pattern, part_number, re.IGNORECASE):
                return True

        return False

    def _generate_fingerprint(self, contribution: Contribution) -> str:
        """Generate content fingerprint for duplicate detection"""
        content = contribution.content
        key_fields = []

        if contribution.contribution_type == ContributionType.PART_DATA:
            key_fields = ["part_number", "manufacturer"]
        elif contribution.contribution_type == ContributionType.MEASUREMENT:
            key_fields = ["part_id", "measurement_type", "value"]
        else:
            key_fields = list(content.keys())[:3]

        fingerprint_parts = [str(content.get(f, "")) for f in key_fields]
        return "|".join(fingerprint_parts).lower()

    def _check_dimensional_plausibility(self, content: Dict) -> Dict[str, Any]:
        """Check dimensional relationships in part data"""
        violations = []
        warnings = []

        # Thread dimensions check
        thread_diameter = content.get("thread_diameter")
        thread_pitch = content.get("thread_pitch")

        if thread_diameter and thread_pitch:
            try:
                d = float(thread_diameter)
                p = float(thread_pitch)

                # Pitch should be reasonable fraction of diameter
                if p > d / 2:
                    violations.append(f"Thread pitch {p}mm too large for diameter {d}mm")
                if p < d / 20:
                    warnings.append(f"Thread pitch {p}mm seems very fine for diameter {d}mm")
            except (ValueError, TypeError):
                pass

        return {"valid": len(violations) == 0, "violations": violations, "warnings": warnings}

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return bool(url_pattern.match(url))

    # Database operation stubs
    async def _find_duplicate(self, fingerprint: str) -> Optional[Dict]:
        return None

    async def _find_similar(self, contribution: Contribution) -> List[Dict]:
        return []

    async def _verify_part_exists(self, part_id) -> bool:
        return True

    async def _verify_contribution_exists(self, contribution_id: str) -> bool:
        return True
