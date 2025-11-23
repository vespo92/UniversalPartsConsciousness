"""
Failure Database

Knowledge base of documented failures.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class FailureRecord:
    """Record of a documented failure"""
    failure_id: str
    part_type: str
    part_specification: str
    failure_mode: str
    root_cause: str
    application: str
    operating_conditions: Dict[str, Any]
    service_time: Optional[float]
    resolution: str
    documentation_date: datetime
    reporter_type: str
    verified: bool


class FailureDatabase:
    """
    Knowledge base of documented failures in the UPC network.

    Provides:
    - Failure record storage and retrieval
    - Search and query capabilities
    - Statistics and analytics
    """

    def __init__(self):
        """Initialize the failure database."""
        self.failures: Dict[str, FailureRecord] = {}
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Initialize with sample failure data for demonstration."""
        sample_failures = [
            FailureRecord(
                failure_id="FAIL-2024-0001",
                part_type="Socket head cap screw",
                part_specification="M10x40 SHCS 10.9",
                failure_mode="high_cycle_fatigue",
                root_cause="Insufficient preload + vibration",
                application="CNC spindle mount",
                operating_conditions={"vibration": "high", "temperature_c": 45},
                service_time=8500,
                resolution="Upgraded to 12.9 + Nord-Lock washers",
                documentation_date=datetime(2024, 1, 15),
                reporter_type="verified_engineer",
                verified=True
            ),
            FailureRecord(
                failure_id="FAIL-2024-0002",
                part_type="Hex bolt",
                part_specification="M8x25 8.8 Zinc",
                failure_mode="hydrogen_embrittlement",
                root_cause="No bake after zinc plating",
                application="Suspension bracket",
                operating_conditions={"environment": "road_salt", "load": "cyclic"},
                service_time=100,
                resolution="Switched to Geomet coating",
                documentation_date=datetime(2024, 2, 20),
                reporter_type="professional",
                verified=True
            ),
            FailureRecord(
                failure_id="FAIL-2024-0003",
                part_type="Ball bearing",
                part_specification="6205-2RS",
                failure_mode="lubricant_degradation",
                root_cause="Operating temperature exceeded grease limit",
                application="Motor shaft",
                operating_conditions={"rpm": 3000, "temperature_c": 95},
                service_time=12000,
                resolution="Upgraded to high-temp grease bearing",
                documentation_date=datetime(2024, 3, 10),
                reporter_type="oem_engineer",
                verified=True
            ),
        ]

        for failure in sample_failures:
            self.failures[failure.failure_id] = failure

    async def add_failure(self, record: FailureRecord) -> str:
        """Add a failure record to the database."""
        self.failures[record.failure_id] = record
        return record.failure_id

    async def get_failure(self, failure_id: str) -> Optional[FailureRecord]:
        """Retrieve a failure record by ID."""
        return self.failures.get(failure_id)

    async def search_failures(
        self,
        part_type: Optional[str] = None,
        failure_mode: Optional[str] = None,
        application: Optional[str] = None,
        limit: int = 100
    ) -> List[FailureRecord]:
        """
        Search failures by criteria.

        Args:
            part_type: Filter by part type (partial match)
            failure_mode: Filter by failure mode
            application: Filter by application (partial match)
            limit: Maximum results to return

        Returns:
            List of matching failure records
        """
        results = []

        for failure in self.failures.values():
            match = True

            if part_type and part_type.lower() not in failure.part_type.lower():
                match = False

            if failure_mode and failure_mode != failure.failure_mode:
                match = False

            if application and application.lower() not in failure.application.lower():
                match = False

            if match:
                results.append(failure)

            if len(results) >= limit:
                break

        return results

    async def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        if not self.failures:
            return {
                "total_failures": 0,
                "failure_modes": {},
                "part_types": {},
            }

        # Count by failure mode
        mode_counts = {}
        for failure in self.failures.values():
            mode = failure.failure_mode
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        # Count by part type
        type_counts = {}
        for failure in self.failures.values():
            ptype = failure.part_type
            type_counts[ptype] = type_counts.get(ptype, 0) + 1

        return {
            "total_failures": len(self.failures),
            "failure_modes": mode_counts,
            "part_types": type_counts,
            "verified_count": sum(1 for f in self.failures.values() if f.verified),
        }

    async def get_failure_modes_for_part(
        self,
        part_type: str
    ) -> List[Dict[str, Any]]:
        """Get all known failure modes for a part type."""
        modes = {}

        for failure in self.failures.values():
            if part_type.lower() in failure.part_type.lower():
                mode = failure.failure_mode
                if mode not in modes:
                    modes[mode] = {
                        "mode": mode,
                        "count": 0,
                        "avg_service_time": [],
                        "root_causes": set(),
                    }
                modes[mode]["count"] += 1
                if failure.service_time:
                    modes[mode]["avg_service_time"].append(failure.service_time)
                modes[mode]["root_causes"].add(failure.root_cause)

        # Calculate averages and convert sets
        results = []
        for mode, data in modes.items():
            avg_time = (sum(data["avg_service_time"]) / len(data["avg_service_time"])
                       if data["avg_service_time"] else None)
            results.append({
                "mode": mode,
                "count": data["count"],
                "avg_service_time": avg_time,
                "root_causes": list(data["root_causes"]),
            })

        return sorted(results, key=lambda x: x["count"], reverse=True)
