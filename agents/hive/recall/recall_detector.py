"""
Recall Detector - Detects and ingests industry recalls.

Monitors various sources for recall notices and converts them
to structured RecallNotice objects for propagation.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Protocol
from uuid import UUID

from ..models import RecallNotice, RecallSeverity


@dataclass
class RawRecall:
    """Raw recall data from an external source."""
    source: str
    source_id: str
    title: str
    description: str
    severity: str
    affected_parts: list[dict[str, Any]]
    issued_date: datetime
    raw_data: dict[str, Any]


class RecallSource(Protocol):
    """Protocol for recall data sources."""

    async def fetch_recent_recalls(
        self,
        since: Optional[datetime] = None,
    ) -> list[RawRecall]:
        """Fetch recent recalls from the source."""
        ...


class PartMatchingService(Protocol):
    """Protocol for matching recalls to parts."""

    async def find_matching_parts(
        self,
        criteria: dict[str, Any],
    ) -> list[UUID]:
        """Find parts matching the criteria."""
        ...

    async def find_matching_swarms(
        self,
        criteria: dict[str, Any],
    ) -> list[UUID]:
        """Find swarms containing matching parts."""
        ...


class RecallDetector:
    """
    Detects and ingests recalls from various sources.
    """

    # Severity mapping from external sources
    SEVERITY_MAPPING = {
        "critical": RecallSeverity.CRITICAL,
        "high": RecallSeverity.HIGH,
        "medium": RecallSeverity.WARNING,
        "warning": RecallSeverity.WARNING,
        "low": RecallSeverity.ADVISORY,
        "advisory": RecallSeverity.ADVISORY,
        "info": RecallSeverity.ADVISORY,
    }

    def __init__(
        self,
        sources: list[RecallSource],
        part_matcher: PartMatchingService,
    ):
        self.sources = sources
        self.part_matcher = part_matcher
        self.processed_recalls: set[str] = set()

    async def detect_new_recalls(
        self,
        since: Optional[datetime] = None,
    ) -> list[RecallNotice]:
        """
        Detect new recalls from all sources.

        Args:
            since: Only fetch recalls issued after this time

        Returns:
            List of new RecallNotice objects
        """
        all_recalls = []

        for source in self.sources:
            try:
                raw_recalls = await source.fetch_recent_recalls(since)
                for raw in raw_recalls:
                    # Skip already processed
                    recall_key = f"{raw.source}:{raw.source_id}"
                    if recall_key in self.processed_recalls:
                        continue

                    # Convert to RecallNotice
                    notice = await self._convert_to_notice(raw)
                    if notice:
                        all_recalls.append(notice)
                        self.processed_recalls.add(recall_key)

            except Exception as e:
                # Log error but continue with other sources
                print(f"Error fetching from {source}: {e}")
                continue

        return all_recalls

    async def _convert_to_notice(
        self,
        raw: RawRecall,
    ) -> Optional[RecallNotice]:
        """Convert raw recall data to a RecallNotice."""
        # Parse severity
        severity = self.SEVERITY_MAPPING.get(
            raw.severity.lower(),
            RecallSeverity.WARNING,
        )

        # Build affected criteria from raw data
        affected_criteria = self._build_affected_criteria(raw.affected_parts)

        # Find matching swarms
        matching_swarms = await self.part_matcher.find_matching_swarms(affected_criteria)

        if not matching_swarms:
            # No matching parts in our system
            return None

        # Count affected parts
        matching_parts = await self.part_matcher.find_matching_parts(affected_criteria)

        # Extract defect description
        defect_description = self._extract_defect_description(raw.description)

        # Extract recommended action
        recommended_action = self._extract_recommended_action(raw.description)

        return RecallNotice(
            source=raw.source,
            source_recall_id=raw.source_id,
            severity=severity,
            title=raw.title,
            description=raw.description,
            defect_description=defect_description,
            recommended_action=recommended_action,
            affected_criteria=affected_criteria,
            affected_swarm_ids=matching_swarms,
            affected_parts_count=len(matching_parts),
            issued_at=raw.issued_date,
            received_at=datetime.utcnow(),
        )

    def _build_affected_criteria(
        self,
        affected_parts: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Build matching criteria from affected parts list."""
        criteria = {
            "manufacturers": [],
            "part_numbers": [],
            "date_ranges": [],
            "categories": [],
        }

        for part in affected_parts:
            if "manufacturer" in part:
                criteria["manufacturers"].append(part["manufacturer"])
            if "part_number" in part:
                criteria["part_numbers"].append(part["part_number"])
            if "category" in part:
                criteria["categories"].append(part["category"])
            if "date_from" in part and "date_to" in part:
                criteria["date_ranges"].append({
                    "from": part["date_from"],
                    "to": part["date_to"],
                })

        # Remove empty lists
        criteria = {k: v for k, v in criteria.items() if v}

        return criteria

    def _extract_defect_description(self, description: str) -> str:
        """Extract the defect description from full text."""
        # Look for common patterns
        patterns = [
            r"defect[:\s]+(.+?)(?:\.|$)",
            r"issue[:\s]+(.+?)(?:\.|$)",
            r"problem[:\s]+(.+?)(?:\.|$)",
            r"the (.+?) (?:may|could|might) (?:fail|break|malfunction)",
        ]

        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Fall back to first sentence
        first_sentence = description.split(".")[0]
        return first_sentence[:200]

    def _extract_recommended_action(self, description: str) -> str:
        """Extract recommended action from full text."""
        # Look for action patterns
        patterns = [
            r"recommend(?:ed|s)?[:\s]+(.+?)(?:\.|$)",
            r"should[:\s]+(.+?)(?:\.|$)",
            r"action[:\s]+(.+?)(?:\.|$)",
            r"(?:replace|remove|inspect|stop using)[^.]+",
        ]

        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.lastindex else match.group(0).strip()

        return "Contact manufacturer for guidance"


class NHTSARecallSource:
    """
    NHTSA (National Highway Traffic Safety Administration) recall source.
    """

    async def fetch_recent_recalls(
        self,
        since: Optional[datetime] = None,
    ) -> list[RawRecall]:
        """Fetch recalls from NHTSA."""
        # This would integrate with NHTSA's API
        # For now, return empty list as placeholder
        return []


class ManufacturerRecallSource:
    """
    Direct manufacturer recall source.
    """

    def __init__(self, manufacturer: str, api_endpoint: str):
        self.manufacturer = manufacturer
        self.api_endpoint = api_endpoint

    async def fetch_recent_recalls(
        self,
        since: Optional[datetime] = None,
    ) -> list[RawRecall]:
        """Fetch recalls from manufacturer."""
        # This would integrate with manufacturer's API
        return []


class IndustryFeedRecallSource:
    """
    Industry-wide recall feed source.
    """

    async def fetch_recent_recalls(
        self,
        since: Optional[datetime] = None,
    ) -> list[RawRecall]:
        """Fetch recalls from industry feed."""
        return []
