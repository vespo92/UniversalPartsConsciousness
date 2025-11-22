"""
Agent_1 (ARCHIVIST) - Data Quality Scoring System
==================================================
"Truth is measured. Quality is quantified. Trust is earned."

The quality scoring system evaluates every piece of data entering
the Universal Parts Consciousness, ensuring only verified truth
contributes to part awakening.
"""

import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from ..scrapers.base_scraper import ScrapedPart


class QualityDimension(Enum):
    """Dimensions of data quality assessment."""
    COMPLETENESS = "completeness"     # All required fields present
    ACCURACY = "accuracy"             # Values within expected ranges
    CONSISTENCY = "consistency"       # No contradictory data
    PRECISION = "precision"           # Appropriate level of detail
    TIMELINESS = "timeliness"         # Data freshness
    VALIDITY = "validity"             # Conformance to standards
    UNIQUENESS = "uniqueness"         # No duplicates


@dataclass
class QualityRule:
    """A single quality rule for validation."""
    dimension: QualityDimension
    name: str
    description: str
    weight: float = 1.0
    required: bool = False

    def __hash__(self):
        return hash((self.dimension, self.name))


@dataclass
class QualityViolation:
    """A quality rule violation."""
    rule: QualityRule
    message: str
    severity: str = "warning"  # info, warning, error
    field: Optional[str] = None
    value: Optional[Any] = None


@dataclass
class QualityScore:
    """Comprehensive quality score for a part."""
    overall_score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    violations: List[QualityViolation] = field(default_factory=list)

    # Component scores
    completeness_score: float = 0.0
    accuracy_score: float = 0.0
    consistency_score: float = 0.0
    precision_score: float = 0.0
    timeliness_score: float = 0.0
    validity_score: float = 0.0

    # Metadata
    rules_evaluated: int = 0
    rules_passed: int = 0
    scored_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def pass_rate(self) -> float:
        """Percentage of rules passed."""
        return self.rules_passed / self.rules_evaluated if self.rules_evaluated > 0 else 0.0

    @property
    def has_critical_violations(self) -> bool:
        """Check if any critical violations exist."""
        return any(v.severity == "error" for v in self.violations)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "overall_score": round(self.overall_score, 4),
            "dimension_scores": {k: round(v, 4) for k, v in self.dimension_scores.items()},
            "completeness": round(self.completeness_score, 4),
            "accuracy": round(self.accuracy_score, 4),
            "consistency": round(self.consistency_score, 4),
            "precision": round(self.precision_score, 4),
            "timeliness": round(self.timeliness_score, 4),
            "validity": round(self.validity_score, 4),
            "rules_evaluated": self.rules_evaluated,
            "rules_passed": self.rules_passed,
            "pass_rate": round(self.pass_rate, 4),
            "violations": [
                {
                    "rule": v.rule.name,
                    "dimension": v.rule.dimension.value,
                    "message": v.message,
                    "severity": v.severity,
                    "field": v.field,
                }
                for v in self.violations
            ],
            "scored_at": self.scored_at.isoformat(),
        }


class PartQualityScorer:
    """
    Comprehensive quality scorer for part data.

    Evaluates data across multiple dimensions:
    - Completeness: Are all required fields present?
    - Accuracy: Are values within expected ranges?
    - Consistency: Do related fields agree?
    - Precision: Are specifications appropriately detailed?
    - Timeliness: Is the data fresh?
    - Validity: Does data conform to standards?
    """

    # Field importance weights for completeness scoring
    FIELD_WEIGHTS = {
        # Critical fields (must have for consciousness)
        "thread_spec": 0.15,
        "length": 0.10,
        "material": 0.12,
        "head_type": 0.08,
        "drive_type": 0.08,

        # Important fields (enhance consciousness)
        "diameter": 0.06,
        "material_grade": 0.06,
        "drive_size": 0.04,
        "tensile_strength": 0.05,
        "yield_strength": 0.03,
        "hardness": 0.03,

        # Supporting fields
        "category": 0.04,
        "subcategory": 0.02,
        "description": 0.04,
        "manufacturer": 0.03,
        "price": 0.02,
        "availability": 0.02,

        # Documentation
        "cad_urls": 0.02,
        "datasheet_url": 0.01,
    }

    # Valid thread patterns
    THREAD_PATTERNS = {
        "metric": re.compile(r'^M(\d+(?:\.\d+)?)(x(\d+(?:\.\d+)?))?$'),
        "unified_fractional": re.compile(r'^(\d+/\d+)-(\d+)(?:\s*(UNC|UNF|UNEF))?$'),
        "unified_numbered": re.compile(r'^#(\d+)-(\d+)(?:\s*(UNC|UNF|UNEF))?$'),
    }

    # Valid materials
    VALID_MATERIALS = {
        "18-8 Stainless Steel", "304 Stainless Steel", "316 Stainless Steel",
        "316L Stainless Steel", "17-4 PH Stainless Steel",
        "Alloy Steel", "Alloy Steel Grade 8", "Steel Grade 5", "Steel Grade 2",
        "Carbon Steel", "Medium Carbon Steel", "Low Carbon Steel",
        "Brass", "Bronze", "Phosphor Bronze", "Silicon Bronze",
        "Aluminum", "Aluminum 2024", "Aluminum 6061", "Aluminum 7075",
        "Titanium", "Titanium Grade 5",
        "Nylon", "PEEK", "PTFE",
        "Zinc-Plated Steel", "Black-Oxide Steel",
    }

    # Expected ranges for validation
    EXPECTED_RANGES = {
        "length_mm": (0.5, 1000.0),
        "diameter_mm": (0.5, 100.0),
        "tensile_strength_mpa": (100.0, 2000.0),
        "yield_strength_mpa": (50.0, 1800.0),
        "price": (0.001, 10000.0),
    }

    # Material grade patterns
    MATERIAL_GRADE_PATTERNS = {
        "metric": re.compile(r'^[A-Z]\d+-\d+$'),  # A2-70, A4-80
        "sae": re.compile(r'^Grade\s*\d+$', re.IGNORECASE),  # Grade 5, Grade 8
        "property_class": re.compile(r'^\d+\.\d+$'),  # 8.8, 10.9, 12.9
    }

    def __init__(
        self,
        max_data_age_days: int = 90,
        required_fields: Optional[Set[str]] = None,
        custom_rules: Optional[List[QualityRule]] = None,
    ):
        """
        Initialize the quality scorer.

        Args:
            max_data_age_days: Maximum age of data before timeliness penalty
            required_fields: Override default required fields
            custom_rules: Additional custom validation rules
        """
        self.max_data_age_days = max_data_age_days
        self.required_fields = required_fields or {
            "thread_spec", "length", "material", "head_type", "drive_type"
        }
        self.custom_rules = custom_rules or []

    def score(self, part: ScrapedPart) -> QualityScore:
        """
        Calculate comprehensive quality score for a part.

        Args:
            part: ScrapedPart to evaluate

        Returns:
            QualityScore with detailed breakdown
        """
        score = QualityScore()
        violations = []

        # Evaluate each dimension
        score.completeness_score, comp_violations = self._score_completeness(part)
        violations.extend(comp_violations)

        score.accuracy_score, acc_violations = self._score_accuracy(part)
        violations.extend(acc_violations)

        score.consistency_score, cons_violations = self._score_consistency(part)
        violations.extend(cons_violations)

        score.precision_score, prec_violations = self._score_precision(part)
        violations.extend(prec_violations)

        score.timeliness_score, time_violations = self._score_timeliness(part)
        violations.extend(time_violations)

        score.validity_score, val_violations = self._score_validity(part)
        violations.extend(val_violations)

        # Store all violations
        score.violations = violations

        # Calculate dimension scores
        score.dimension_scores = {
            QualityDimension.COMPLETENESS.value: score.completeness_score,
            QualityDimension.ACCURACY.value: score.accuracy_score,
            QualityDimension.CONSISTENCY.value: score.consistency_score,
            QualityDimension.PRECISION.value: score.precision_score,
            QualityDimension.TIMELINESS.value: score.timeliness_score,
            QualityDimension.VALIDITY.value: score.validity_score,
        }

        # Calculate overall score (weighted average)
        dimension_weights = {
            "completeness": 0.25,
            "accuracy": 0.20,
            "consistency": 0.15,
            "precision": 0.15,
            "timeliness": 0.10,
            "validity": 0.15,
        }

        score.overall_score = (
            score.completeness_score * dimension_weights["completeness"] +
            score.accuracy_score * dimension_weights["accuracy"] +
            score.consistency_score * dimension_weights["consistency"] +
            score.precision_score * dimension_weights["precision"] +
            score.timeliness_score * dimension_weights["timeliness"] +
            score.validity_score * dimension_weights["validity"]
        )

        # Count rules
        score.rules_evaluated = len(violations) + sum(1 for d in score.dimension_scores.values() if d > 0)
        score.rules_passed = sum(1 for d in score.dimension_scores.values() if d >= 0.8)

        return score

    def _score_completeness(self, part: ScrapedPart) -> Tuple[float, List[QualityViolation]]:
        """Evaluate data completeness."""
        violations = []
        total_weight = 0.0
        achieved_weight = 0.0

        field_values = {
            "thread_spec": part.thread_spec,
            "length": part.length,
            "diameter": part.diameter,
            "material": part.material,
            "material_grade": part.material_grade,
            "head_type": part.head_type,
            "drive_type": part.drive_type,
            "drive_size": part.drive_size,
            "tensile_strength": part.tensile_strength,
            "yield_strength": part.yield_strength,
            "hardness": part.hardness,
            "category": part.category,
            "subcategory": part.subcategory,
            "description": part.description,
            "manufacturer": part.manufacturer,
            "price": part.price,
            "availability": part.availability,
            "cad_urls": bool(part.cad_urls),
            "datasheet_url": part.datasheet_url,
        }

        for field_name, weight in self.FIELD_WEIGHTS.items():
            total_weight += weight
            value = field_values.get(field_name)

            if value:
                achieved_weight += weight
            else:
                severity = "error" if field_name in self.required_fields else "warning"
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.COMPLETENESS,
                        name=f"field_{field_name}",
                        description=f"Field '{field_name}' should be present",
                        weight=weight,
                        required=field_name in self.required_fields,
                    ),
                    message=f"Missing field: {field_name}",
                    severity=severity,
                    field=field_name,
                ))

        score = achieved_weight / total_weight if total_weight > 0 else 0.0
        return score, violations

    def _score_accuracy(self, part: ScrapedPart) -> Tuple[float, List[QualityViolation]]:
        """Evaluate data accuracy (values within expected ranges)."""
        violations = []
        checks_passed = 0
        checks_total = 0

        # Check length range
        if part.length is not None:
            checks_total += 1
            min_val, max_val = self.EXPECTED_RANGES["length_mm"]
            if min_val <= part.length <= max_val:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.ACCURACY,
                        name="length_range",
                        description="Length should be within expected range",
                    ),
                    message=f"Length {part.length}mm outside expected range ({min_val}-{max_val}mm)",
                    severity="error",
                    field="length",
                    value=part.length,
                ))

        # Check diameter range
        if part.diameter is not None:
            checks_total += 1
            min_val, max_val = self.EXPECTED_RANGES["diameter_mm"]
            if min_val <= part.diameter <= max_val:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.ACCURACY,
                        name="diameter_range",
                        description="Diameter should be within expected range",
                    ),
                    message=f"Diameter {part.diameter}mm outside expected range ({min_val}-{max_val}mm)",
                    severity="warning",
                    field="diameter",
                    value=part.diameter,
                ))

        # Check tensile strength range
        if part.tensile_strength is not None:
            checks_total += 1
            min_val, max_val = self.EXPECTED_RANGES["tensile_strength_mpa"]
            if min_val <= part.tensile_strength <= max_val:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.ACCURACY,
                        name="tensile_strength_range",
                        description="Tensile strength should be within expected range",
                    ),
                    message=f"Tensile strength {part.tensile_strength}MPa outside expected range",
                    severity="warning",
                    field="tensile_strength",
                    value=part.tensile_strength,
                ))

        # Check price range
        if part.price is not None:
            checks_total += 1
            min_val, max_val = self.EXPECTED_RANGES["price"]
            if min_val <= part.price <= max_val:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.ACCURACY,
                        name="price_range",
                        description="Price should be within expected range",
                    ),
                    message=f"Price ${part.price} outside expected range",
                    severity="warning",
                    field="price",
                    value=part.price,
                ))

        # Check material is known
        if part.material:
            checks_total += 1
            if part.material in self.VALID_MATERIALS:
                checks_passed += 1
            else:
                # Partial match check
                material_match = any(
                    vm.lower() in part.material.lower() or part.material.lower() in vm.lower()
                    for vm in self.VALID_MATERIALS
                )
                if material_match:
                    checks_passed += 0.5
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.ACCURACY,
                            name="material_known",
                            description="Material should be a known type",
                        ),
                        message=f"Material '{part.material}' is not exactly matching known materials",
                        severity="info",
                        field="material",
                        value=part.material,
                    ))
                else:
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.ACCURACY,
                            name="material_known",
                            description="Material should be a known type",
                        ),
                        message=f"Unknown material: '{part.material}'",
                        severity="warning",
                        field="material",
                        value=part.material,
                    ))

        score = checks_passed / checks_total if checks_total > 0 else 1.0
        return score, violations

    def _score_consistency(self, part: ScrapedPart) -> Tuple[float, List[QualityViolation]]:
        """Evaluate internal consistency of data."""
        violations = []
        checks_passed = 0
        checks_total = 0

        # Check thread spec matches diameter (for metric)
        if part.thread_spec and part.diameter:
            checks_total += 1
            metric_match = self.THREAD_PATTERNS["metric"].match(part.thread_spec)
            if metric_match:
                thread_diameter = float(metric_match.group(1))
                # Allow 10% tolerance for thread vs major diameter
                if abs(thread_diameter - part.diameter) / thread_diameter <= 0.10:
                    checks_passed += 1
                else:
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.CONSISTENCY,
                            name="thread_diameter_match",
                            description="Thread specification should match diameter",
                        ),
                        message=f"Thread M{thread_diameter} inconsistent with diameter {part.diameter}mm",
                        severity="warning",
                        field="thread_spec",
                    ))
            else:
                checks_passed += 1  # Non-metric threads, skip check

        # Check yield strength < tensile strength
        if part.yield_strength and part.tensile_strength:
            checks_total += 1
            if part.yield_strength < part.tensile_strength:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.CONSISTENCY,
                        name="strength_relationship",
                        description="Yield strength should be less than tensile strength",
                    ),
                    message=f"Yield ({part.yield_strength}MPa) >= Tensile ({part.tensile_strength}MPa)",
                    severity="error",
                    field="yield_strength",
                ))

        # Check material matches expected strength ranges
        if part.material and part.tensile_strength:
            checks_total += 1
            # Basic material-strength consistency
            if "stainless" in part.material.lower():
                if 400 <= part.tensile_strength <= 900:
                    checks_passed += 1
                else:
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.CONSISTENCY,
                            name="material_strength_match",
                            description="Strength should match material type",
                        ),
                        message=f"Stainless steel strength {part.tensile_strength}MPa unusual",
                        severity="info",
                        field="tensile_strength",
                    ))
                    checks_passed += 0.5
            elif "grade 8" in part.material.lower() or "10.9" in str(part.material_grade):
                if 800 <= part.tensile_strength <= 1200:
                    checks_passed += 1
                else:
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.CONSISTENCY,
                            name="material_strength_match",
                            description="Strength should match material type",
                        ),
                        message=f"Grade 8/10.9 strength {part.tensile_strength}MPa unusual",
                        severity="info",
                        field="tensile_strength",
                    ))
                    checks_passed += 0.5
            else:
                checks_passed += 1  # Unknown material, assume OK

        score = checks_passed / checks_total if checks_total > 0 else 1.0
        return score, violations

    def _score_precision(self, part: ScrapedPart) -> Tuple[float, List[QualityViolation]]:
        """Evaluate precision/detail level of specifications."""
        violations = []
        precision_scores = []

        # Thread spec precision
        if part.thread_spec:
            metric_match = self.THREAD_PATTERNS["metric"].match(part.thread_spec)
            if metric_match:
                # Check if pitch is specified
                if metric_match.group(3):  # Has pitch
                    precision_scores.append(1.0)
                else:
                    precision_scores.append(0.7)
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.PRECISION,
                            name="thread_pitch",
                            description="Thread specification should include pitch",
                        ),
                        message="Thread spec missing pitch (using coarse assumed)",
                        severity="info",
                        field="thread_spec",
                    ))
            else:
                precision_scores.append(1.0)  # Non-metric, assume OK

        # Length precision (decimal places)
        if part.length is not None:
            length_str = str(part.length)
            if '.' in length_str:
                decimals = len(length_str.split('.')[1])
                if decimals >= 2:
                    precision_scores.append(1.0)
                elif decimals == 1:
                    precision_scores.append(0.8)
                else:
                    precision_scores.append(0.6)
            else:
                precision_scores.append(0.5)
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.PRECISION,
                        name="length_precision",
                        description="Length should have decimal precision",
                    ),
                    message="Length lacks decimal precision",
                    severity="info",
                    field="length",
                ))

        # Material grade precision
        if part.material and part.material_grade:
            precision_scores.append(1.0)
        elif part.material:
            precision_scores.append(0.7)
            violations.append(QualityViolation(
                rule=QualityRule(
                    dimension=QualityDimension.PRECISION,
                    name="material_grade",
                    description="Material should include grade specification",
                ),
                message="Material missing grade specification",
                severity="info",
                field="material_grade",
            ))

        # Drive size precision
        if part.drive_type and part.drive_size:
            precision_scores.append(1.0)
        elif part.drive_type:
            precision_scores.append(0.7)

        score = sum(precision_scores) / len(precision_scores) if precision_scores else 1.0
        return score, violations

    def _score_timeliness(self, part: ScrapedPart) -> Tuple[float, List[QualityViolation]]:
        """Evaluate data freshness."""
        violations = []

        if part.scraped_at:
            age = datetime.utcnow() - part.scraped_at
            age_days = age.days

            if age_days <= 7:
                score = 1.0
            elif age_days <= 30:
                score = 0.9
            elif age_days <= 60:
                score = 0.7
            elif age_days <= self.max_data_age_days:
                score = 0.5
            else:
                score = 0.3
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.TIMELINESS,
                        name="data_freshness",
                        description=f"Data should be less than {self.max_data_age_days} days old",
                    ),
                    message=f"Data is {age_days} days old (max: {self.max_data_age_days})",
                    severity="warning",
                    field="scraped_at",
                ))
        else:
            score = 0.5  # Unknown age

        return score, violations

    def _score_validity(self, part: ScrapedPart) -> Tuple[float, List[QualityViolation]]:
        """Evaluate conformance to standards and formats."""
        violations = []
        checks_passed = 0
        checks_total = 0

        # Validate thread spec format
        if part.thread_spec:
            checks_total += 1
            is_valid = any(
                pattern.match(part.thread_spec)
                for pattern in self.THREAD_PATTERNS.values()
            )
            if is_valid:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.VALIDITY,
                        name="thread_format",
                        description="Thread specification should match standard format",
                    ),
                    message=f"Invalid thread format: '{part.thread_spec}'",
                    severity="warning",
                    field="thread_spec",
                    value=part.thread_spec,
                ))

        # Validate material grade format
        if part.material_grade:
            checks_total += 1
            is_valid = any(
                pattern.match(part.material_grade)
                for pattern in self.MATERIAL_GRADE_PATTERNS.values()
            )
            if is_valid:
                checks_passed += 1
            else:
                # Check for common variations
                if re.match(r'^\d+\.\d+$', part.material_grade):  # e.g., "8.8"
                    checks_passed += 1
                else:
                    violations.append(QualityViolation(
                        rule=QualityRule(
                            dimension=QualityDimension.VALIDITY,
                            name="grade_format",
                            description="Material grade should match standard format",
                        ),
                        message=f"Non-standard grade format: '{part.material_grade}'",
                        severity="info",
                        field="material_grade",
                        value=part.material_grade,
                    ))
                    checks_passed += 0.5

        # Validate UPC ID format
        if part.upc_id:
            checks_total += 1
            if re.match(r'^UPC-[A-F0-9]{12}$', part.upc_id):
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.VALIDITY,
                        name="upc_format",
                        description="UPC ID should match expected format",
                    ),
                    message=f"Invalid UPC ID format: '{part.upc_id}'",
                    severity="error",
                    field="upc_id",
                    value=part.upc_id,
                ))

        # Validate currency code
        if part.price:
            checks_total += 1
            valid_currencies = {"USD", "EUR", "GBP", "JPY", "CNY", "CAD"}
            if part.currency in valid_currencies:
                checks_passed += 1
            else:
                violations.append(QualityViolation(
                    rule=QualityRule(
                        dimension=QualityDimension.VALIDITY,
                        name="currency_code",
                        description="Currency should be a valid ISO code",
                    ),
                    message=f"Unknown currency: '{part.currency}'",
                    severity="info",
                    field="currency",
                    value=part.currency,
                ))
                checks_passed += 0.5

        score = checks_passed / checks_total if checks_total > 0 else 1.0
        return score, violations


def score_part(part: ScrapedPart) -> QualityScore:
    """Convenience function to score a single part."""
    scorer = PartQualityScorer()
    return scorer.score(part)


def score_batch(parts: List[ScrapedPart]) -> List[QualityScore]:
    """Score a batch of parts."""
    scorer = PartQualityScorer()
    return [scorer.score(part) for part in parts]


def calculate_batch_statistics(scores: List[QualityScore]) -> Dict[str, Any]:
    """Calculate aggregate statistics for a batch of quality scores."""
    if not scores:
        return {}

    overall_scores = [s.overall_score for s in scores]
    completeness_scores = [s.completeness_score for s in scores]
    accuracy_scores = [s.accuracy_score for s in scores]

    all_violations = []
    for s in scores:
        all_violations.extend(s.violations)

    violation_counts = {}
    for v in all_violations:
        key = v.rule.name
        violation_counts[key] = violation_counts.get(key, 0) + 1

    return {
        "total_parts": len(scores),
        "average_overall_score": sum(overall_scores) / len(overall_scores),
        "min_overall_score": min(overall_scores),
        "max_overall_score": max(overall_scores),
        "average_completeness": sum(completeness_scores) / len(completeness_scores),
        "average_accuracy": sum(accuracy_scores) / len(accuracy_scores),
        "parts_with_critical_violations": sum(1 for s in scores if s.has_critical_violations),
        "total_violations": len(all_violations),
        "top_violations": sorted(
            violation_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10],
    }


__all__ = [
    "PartQualityScorer",
    "QualityScore",
    "QualityViolation",
    "QualityRule",
    "QualityDimension",
    "score_part",
    "score_batch",
    "calculate_batch_statistics",
]
