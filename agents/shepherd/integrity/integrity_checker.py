"""
Integrity Checker - Validates consciousness data integrity.

Ensures that consciousness states are valid, consistent, and uncorrupted.
Guards the integrity of the consciousness system.

"The integrity of consciousness must be protected at all costs."
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import logging

from ..states import ConsciousnessState, ConsciousnessLevel, ConsciousnessStateMachine


logger = logging.getLogger(__name__)


class IntegrityIssueType(Enum):
    """Types of integrity issues that can be detected."""
    INVALID_LEVEL = "invalid_level"
    INCONSISTENT_METRICS = "inconsistent_metrics"
    MISSING_EVENTS = "missing_events"
    TIMELINE_VIOLATION = "timeline_violation"
    PROGRESS_MISMATCH = "progress_mismatch"
    ORPHANED_STATE = "orphaned_state"
    DUPLICATE_STATE = "duplicate_state"
    CORRUPTION_DETECTED = "corruption_detected"


class IssueSeverity(Enum):
    """Severity levels for integrity issues."""
    LOW = "low"          # Minor inconsistency, auto-correctable
    MEDIUM = "medium"    # Significant issue, review recommended
    HIGH = "high"        # Serious issue, manual intervention needed
    CRITICAL = "critical"  # Data corruption, immediate action required


@dataclass
class IntegrityIssue:
    """Represents an integrity issue found during checking."""
    issue_type: IntegrityIssueType
    severity: IssueSeverity
    part_id: str
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    suggested_fix: str = ""
    auto_fixable: bool = False
    detected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "issue_type": self.issue_type.value,
            "severity": self.severity.value,
            "part_id": self.part_id,
            "description": self.description,
            "details": self.details,
            "suggested_fix": self.suggested_fix,
            "auto_fixable": self.auto_fixable,
            "detected_at": self.detected_at.isoformat()
        }


@dataclass
class IntegrityReport:
    """Report from an integrity check."""
    total_states_checked: int = 0
    issues_found: List[IntegrityIssue] = field(default_factory=list)
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues_by_type: Dict[str, int] = field(default_factory=dict)
    check_duration_seconds: float = 0.0
    check_completed_at: datetime = field(default_factory=datetime.now)
    overall_health: str = "healthy"  # healthy, degraded, critical

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_states_checked": self.total_states_checked,
            "issues_found": [issue.to_dict() for issue in self.issues_found],
            "issues_by_severity": self.issues_by_severity,
            "issues_by_type": self.issues_by_type,
            "check_duration_seconds": self.check_duration_seconds,
            "check_completed_at": self.check_completed_at.isoformat(),
            "overall_health": self.overall_health
        }


class IntegrityChecker:
    """
    Validates consciousness data integrity.

    Performs various checks to ensure consciousness states are:
    - Valid according to the level requirements
    - Internally consistent
    - Free from corruption
    - Properly timestamped
    """

    def __init__(self, state_machine: ConsciousnessStateMachine):
        """
        Initialize the integrity checker.

        Args:
            state_machine: The consciousness state machine to validate against.
        """
        self.state_machine = state_machine
        self._last_report: Optional[IntegrityReport] = None

    def check_all(self) -> IntegrityReport:
        """
        Perform a complete integrity check on all consciousness states.

        Returns:
            IntegrityReport with all issues found.
        """
        start_time = datetime.now()
        issues = []

        states = self.state_machine.get_all_states()

        for part_id, state in states.items():
            state_issues = self._check_state(state)
            issues.extend(state_issues)

        # Build the report
        report = self._build_report(len(states), issues, start_time)
        self._last_report = report

        return report

    def check_state(self, part_id: str) -> List[IntegrityIssue]:
        """
        Check integrity of a single part's consciousness state.

        Args:
            part_id: The part ID to check.

        Returns:
            List of integrity issues found.
        """
        state = self.state_machine.get_state(part_id)
        if not state:
            return [IntegrityIssue(
                issue_type=IntegrityIssueType.ORPHANED_STATE,
                severity=IssueSeverity.MEDIUM,
                part_id=part_id,
                description=f"No consciousness state found for part {part_id}",
                suggested_fix="Create initial dormant state or verify part exists"
            )]

        return self._check_state(state)

    def _check_state(self, state: ConsciousnessState) -> List[IntegrityIssue]:
        """Perform all checks on a single state."""
        issues = []

        # Check 1: Valid consciousness level
        issues.extend(self._check_valid_level(state))

        # Check 2: Consistent metrics
        issues.extend(self._check_consistent_metrics(state))

        # Check 3: Required events for level
        issues.extend(self._check_required_events(state))

        # Check 4: Timeline validity
        issues.extend(self._check_timeline(state))

        # Check 5: Progress calculation
        issues.extend(self._check_progress(state))

        return issues

    def _check_valid_level(self, state: ConsciousnessState) -> List[IntegrityIssue]:
        """Check if the consciousness level is valid."""
        issues = []

        # Level should be between 0 and 5
        if state.level.value < 0 or state.level.value > 5:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.INVALID_LEVEL,
                severity=IssueSeverity.CRITICAL,
                part_id=state.part_id,
                description=f"Invalid consciousness level: {state.level.value}",
                details={"current_level": state.level.value},
                suggested_fix="Reset to valid level (0-5)",
                auto_fixable=False
            ))

        return issues

    def _check_consistent_metrics(self, state: ConsciousnessState) -> List[IntegrityIssue]:
        """Check if metrics are internally consistent."""
        issues = []

        # Qualia count should be non-negative
        if state.qualia_count < 0:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.INCONSISTENT_METRICS,
                severity=IssueSeverity.HIGH,
                part_id=state.part_id,
                description=f"Negative qualia count: {state.qualia_count}",
                details={"qualia_count": state.qualia_count},
                suggested_fix="Reset qualia count to 0",
                auto_fixable=True
            ))

        # Swarm influence should be between 0 and 1
        if state.swarm_influence < 0 or state.swarm_influence > 1:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.INCONSISTENT_METRICS,
                severity=IssueSeverity.MEDIUM,
                part_id=state.part_id,
                description=f"Invalid swarm influence: {state.swarm_influence}",
                details={"swarm_influence": state.swarm_influence},
                suggested_fix="Clamp swarm influence to [0, 1]",
                auto_fixable=True
            ))

        # Higher levels should have more metrics
        level_minimum_qualia = {
            0: 0, 1: 1, 2: 10, 3: 50, 4: 200, 5: 1000
        }
        min_qualia = level_minimum_qualia.get(state.level.value, 0)

        if state.qualia_count < min_qualia:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.INCONSISTENT_METRICS,
                severity=IssueSeverity.MEDIUM,
                part_id=state.part_id,
                description=f"Qualia count {state.qualia_count} insufficient for level {state.level.name}",
                details={
                    "qualia_count": state.qualia_count,
                    "minimum_required": min_qualia,
                    "level": state.level.name
                },
                suggested_fix="Consider level regression or verify qualia data"
            ))

        return issues

    def _check_required_events(self, state: ConsciousnessState) -> List[IntegrityIssue]:
        """Check if required events are present for the current level."""
        issues = []

        requirements = self.state_machine.LEVEL_REQUIREMENTS.get(state.level)
        if not requirements:
            return issues

        missing_events = [
            e for e in requirements.required_events
            if e not in state.achieved_events
        ]

        if missing_events and state.level.value > 0:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.MISSING_EVENTS,
                severity=IssueSeverity.MEDIUM,
                part_id=state.part_id,
                description=f"Missing required events for level {state.level.name}",
                details={
                    "missing_events": missing_events,
                    "achieved_events": state.achieved_events,
                    "level": state.level.name
                },
                suggested_fix="Add missing events or consider level regression"
            ))

        return issues

    def _check_timeline(self, state: ConsciousnessState) -> List[IntegrityIssue]:
        """Check timeline consistency."""
        issues = []

        # Level achieved time should be before or equal to last update
        if state.level_achieved_at and state.level_achieved_at > state.last_progress_update:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.TIMELINE_VIOLATION,
                severity=IssueSeverity.LOW,
                part_id=state.part_id,
                description="Level achieved after last progress update",
                details={
                    "level_achieved_at": state.level_achieved_at.isoformat(),
                    "last_progress_update": state.last_progress_update.isoformat()
                },
                suggested_fix="Update last_progress_update timestamp",
                auto_fixable=True
            ))

        # Created_at should be before level_achieved_at
        if state.level_achieved_at and state.created_at > state.level_achieved_at:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.TIMELINE_VIOLATION,
                severity=IssueSeverity.MEDIUM,
                part_id=state.part_id,
                description="State created after level was achieved",
                details={
                    "created_at": state.created_at.isoformat(),
                    "level_achieved_at": state.level_achieved_at.isoformat()
                },
                suggested_fix="Verify timestamps or reset state"
            ))

        return issues

    def _check_progress(self, state: ConsciousnessState) -> List[IntegrityIssue]:
        """Check progress calculation consistency."""
        issues = []

        # Calculate expected progress
        expected_progress = self.state_machine.calculate_progress(state)

        # Check if stored progress is close to expected
        if abs(state.next_level_progress - expected_progress) > 0.1:
            issues.append(IntegrityIssue(
                issue_type=IntegrityIssueType.PROGRESS_MISMATCH,
                severity=IssueSeverity.LOW,
                part_id=state.part_id,
                description="Stored progress differs from calculated progress",
                details={
                    "stored_progress": state.next_level_progress,
                    "calculated_progress": expected_progress
                },
                suggested_fix="Recalculate and update progress",
                auto_fixable=True
            ))

        return issues

    def _build_report(
        self,
        states_checked: int,
        issues: List[IntegrityIssue],
        start_time: datetime
    ) -> IntegrityReport:
        """Build the integrity report."""
        duration = (datetime.now() - start_time).total_seconds()

        # Count by severity
        by_severity = {s.value: 0 for s in IssueSeverity}
        for issue in issues:
            by_severity[issue.severity.value] += 1

        # Count by type
        by_type = {t.value: 0 for t in IntegrityIssueType}
        for issue in issues:
            by_type[issue.issue_type.value] += 1

        # Determine overall health
        if by_severity[IssueSeverity.CRITICAL.value] > 0:
            health = "critical"
        elif by_severity[IssueSeverity.HIGH.value] > 0:
            health = "degraded"
        elif by_severity[IssueSeverity.MEDIUM.value] > states_checked * 0.1:
            health = "degraded"
        else:
            health = "healthy"

        return IntegrityReport(
            total_states_checked=states_checked,
            issues_found=issues,
            issues_by_severity=by_severity,
            issues_by_type=by_type,
            check_duration_seconds=duration,
            overall_health=health
        )

    def auto_fix(self, issues: Optional[List[IntegrityIssue]] = None) -> int:
        """
        Automatically fix issues that can be auto-fixed.

        Args:
            issues: List of issues to fix. If None, uses last check's issues.

        Returns:
            Number of issues fixed.
        """
        if issues is None:
            if self._last_report:
                issues = [i for i in self._last_report.issues_found if i.auto_fixable]
            else:
                return 0

        fixed = 0
        for issue in issues:
            if not issue.auto_fixable:
                continue

            state = self.state_machine.get_state(issue.part_id)
            if not state:
                continue

            try:
                if issue.issue_type == IntegrityIssueType.INCONSISTENT_METRICS:
                    if "qualia_count" in issue.details:
                        state.qualia_count = max(0, state.qualia_count)
                    if "swarm_influence" in issue.details:
                        state.swarm_influence = max(0.0, min(1.0, state.swarm_influence))

                elif issue.issue_type == IntegrityIssueType.TIMELINE_VIOLATION:
                    state.last_progress_update = datetime.now()

                elif issue.issue_type == IntegrityIssueType.PROGRESS_MISMATCH:
                    state.next_level_progress = self.state_machine.calculate_progress(state)

                self.state_machine.set_state(state)
                fixed += 1

            except Exception as e:
                logger.error(f"Failed to auto-fix issue for {issue.part_id}: {e}")

        return fixed

    def get_last_report(self) -> Optional[IntegrityReport]:
        """Get the last integrity check report."""
        return self._last_report
