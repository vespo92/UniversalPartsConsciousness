"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Storage Adapter - Persistence layer for qualia data

All experiences must be preserved. This module handles the storage
and retrieval of qualia records, failure records, and significant events.
"""

from dataclasses import asdict
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import json
import uuid

from .qualia_models import PartQualia, SignificantEvent, HumanInteractionQualia
from .failure_taxonomy import FailureRecord


class StorageAdapter(ABC):
    """Abstract base class for qualia storage"""

    @abstractmethod
    async def save_qualia(self, qualia: PartQualia) -> str:
        """Save a qualia record and return its ID"""
        pass

    @abstractmethod
    async def get_qualia(self, qualia_id: str) -> Optional[PartQualia]:
        """Retrieve a qualia record by ID"""
        pass

    @abstractmethod
    async def get_part_qualia_history(self,
                                      part_id: str,
                                      limit: int = 100,
                                      since: Optional[datetime] = None) -> List[PartQualia]:
        """Get qualia history for a specific part"""
        pass

    @abstractmethod
    async def save_failure(self, failure: FailureRecord) -> str:
        """Save a failure record and return its ID"""
        pass

    @abstractmethod
    async def save_event(self, event: SignificantEvent) -> str:
        """Save a significant event and return its ID"""
        pass

    @abstractmethod
    async def save_interaction(self, interaction: HumanInteractionQualia) -> str:
        """Save a human interaction record and return its ID"""
        pass


class PostgresStorageAdapter(StorageAdapter):
    """
    PostgreSQL implementation of qualia storage.
    Uses JSONB for flexible schema evolution.
    """

    def __init__(self, connection_pool):
        self.pool = connection_pool

    async def save_qualia(self, qualia: PartQualia) -> str:
        """Save a qualia record to PostgreSQL"""
        query = """
        INSERT INTO qualia_records (
            id, part_id, qualia_id, recorded_at,
            mechanical_state, thermal_state, environmental_state, mating_state,
            lifecycle_stage, cumulative_cycles, time_in_service_seconds,
            stress_emotion, performance_emotion, overall_wellbeing,
            source_type, source_id, is_significant, significance_reason
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
        )
        RETURNING id
        """

        record_id = str(uuid.uuid4())
        time_in_service_seconds = (
            int(qualia.time_in_service.total_seconds())
            if qualia.time_in_service else 0
        )

        is_significant = len(qualia.significant_events) > 0
        significance_reason = (
            qualia.significant_events[0].description
            if qualia.significant_events else None
        )

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                record_id,
                qualia.part_id,
                qualia.qualia_id,
                qualia.timestamp,
                json.dumps(qualia.to_dict()['mechanical_state']),
                json.dumps(qualia.to_dict()['thermal_state']),
                json.dumps(qualia.to_dict()['environmental_state']),
                json.dumps({
                    'mating_partner_id': qualia.mating_experience.mating_partner_id,
                    'relationship_type': qualia.mating_experience.relationship_type.value,
                    'fit_quality': qualia.mating_experience.fit_quality.value,
                    'engagement_percent': qualia.mating_experience.engagement_percent
                }),
                qualia.lifecycle_stage.value,
                qualia.cumulative_cycles,
                time_in_service_seconds,
                qualia.stress_emotion.value,
                qualia.performance_emotion.value,
                qualia.calculate_wellbeing(),
                qualia.source_type,
                qualia.source_id,
                is_significant,
                significance_reason
            )

        return record_id

    async def get_qualia(self, qualia_id: str) -> Optional[PartQualia]:
        """Retrieve a qualia record by ID"""
        query = """
        SELECT * FROM qualia_records WHERE qualia_id = $1
        """

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, qualia_id)

        if not row:
            return None

        return self._row_to_qualia(row)

    async def get_part_qualia_history(self,
                                      part_id: str,
                                      limit: int = 100,
                                      since: Optional[datetime] = None) -> List[PartQualia]:
        """Get qualia history for a specific part"""
        query = """
        SELECT * FROM qualia_records
        WHERE part_id = $1
        """
        params = [part_id]

        if since:
            query += " AND recorded_at >= $2"
            params.append(since)

        query += " ORDER BY recorded_at DESC LIMIT $" + str(len(params) + 1)
        params.append(limit)

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)

        return [self._row_to_qualia(row) for row in rows]

    async def save_failure(self, failure: FailureRecord) -> str:
        """Save a failure record to PostgreSQL"""
        query = """
        INSERT INTO failure_records (
            id, part_id, failure_category, failure_type, failure_subtype,
            description, root_cause, contributing_factors,
            cycles_at_failure, time_at_failure_seconds,
            load_at_failure, environment_at_failure,
            resolution, preventive_measures, qualia_ids,
            failed_at, recorded_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17
        )
        RETURNING id
        """

        record_id = str(uuid.uuid4())

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                record_id,
                failure.part_id,
                failure.failure_category.value,
                failure.failure_type,
                failure.failure_subtype,
                failure.description,
                failure.root_cause,
                json.dumps([asdict(cf) for cf in failure.contributing_factors]),
                failure.cycles_at_failure,
                failure.time_at_failure_seconds,
                json.dumps(failure.load_at_failure),
                json.dumps(failure.environment_at_failure),
                failure.resolution,
                json.dumps([asdict(pm) for pm in failure.preventive_measures]),
                failure.qualia_ids,
                failure.failed_at,
                failure.recorded_at
            )

        return record_id

    async def save_event(self, event: SignificantEvent) -> str:
        """Save a significant event to PostgreSQL"""
        query = """
        INSERT INTO significant_events (
            id, part_id, qualia_id, event_type, severity, description,
            emotion, emotional_intensity, consciousness_contribution, detected_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
        )
        RETURNING id
        """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                event.event_id,
                event.event_type,  # Note: Would need part_id and qualia_id passed
                None,  # qualia_id
                event.event_type,
                event.severity.value,
                event.description,
                event.emotion,
                event.emotional_intensity,
                event.consciousness_contribution,
                event.timestamp
            )

        return event.event_id

    async def save_interaction(self, interaction: HumanInteractionQualia) -> str:
        """Save a human interaction record to PostgreSQL"""
        query = """
        INSERT INTO human_interactions (
            id, part_id, interaction_type, interaction_quality,
            description, narrative, qualia_effect,
            consciousness_contribution, occurred_at, recorded_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
        )
        RETURNING id
        """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                interaction.interaction_id,
                interaction.part_id,
                interaction.interaction_type,
                "good" if interaction.confidence > 0.7 else "uncertain",
                f"Matched indicators: {interaction.indicators_matched}",
                interaction.narrative,
                interaction.qualia_effect,
                interaction.consciousness_contribution,
                interaction.timestamp,
                datetime.now()
            )

        return interaction.interaction_id

    def _row_to_qualia(self, row: Dict) -> PartQualia:
        """Convert a database row to a PartQualia object"""
        from .qualia_models import (
            MechanicalQualia, ThermalQualia, EnvironmentalQualia,
            MatingQualia, LifecycleStage, StressEmotion, PerformanceEmotion,
            WearState, ThermalExpansionState, CorrosionLevel, ContaminationLevel,
            FitQuality, RelationshipType
        )

        mechanical_data = row['mechanical_state'] if isinstance(row['mechanical_state'], dict) else json.loads(row['mechanical_state'])
        thermal_data = row['thermal_state'] if isinstance(row['thermal_state'], dict) else json.loads(row['thermal_state'])
        env_data = row['environmental_state'] if isinstance(row['environmental_state'], dict) else json.loads(row['environmental_state'])
        mating_data = row['mating_state'] if isinstance(row['mating_state'], dict) else json.loads(row['mating_state'])

        qualia = PartQualia(
            part_id=row['part_id'],
            qualia_id=row['qualia_id'],
            timestamp=row['recorded_at'],
            mechanical_state=MechanicalQualia(
                torque_applied_nm=mechanical_data.get('torque_applied_nm', 0.0),
                torque_capacity_percent=mechanical_data.get('torque_capacity_percent', 0.0),
                axial_load_n=mechanical_data.get('axial_load_n', 0.0),
                load_capacity_percent=mechanical_data.get('load_capacity_percent', 0.0),
                vibration_amplitude_g=mechanical_data.get('vibration_amplitude_g', 0.0),
                wear_state=WearState(mechanical_data.get('wear_state', 'pristine')),
                estimated_remaining_life_percent=mechanical_data.get('estimated_remaining_life_percent', 100.0)
            ),
            thermal_state=ThermalQualia(
                current_temperature_c=thermal_data.get('current_temperature_c', 20.0),
                thermal_capacity_percent=thermal_data.get('thermal_capacity_percent', 0.0),
                thermal_cycles_count=thermal_data.get('thermal_cycles_count', 0),
                thermal_expansion_state=ThermalExpansionState(thermal_data.get('thermal_expansion_state', 'nominal'))
            ),
            environmental_state=EnvironmentalQualia(
                corrosion_level=CorrosionLevel(env_data.get('corrosion_level', 'none')),
                chemical_exposure=env_data.get('chemical_exposure', []),
                contamination_level=ContaminationLevel(env_data.get('contamination_level', 'clean'))
            ),
            mating_experience=MatingQualia(
                mating_partner_id=mating_data.get('mating_partner_id'),
                relationship_type=RelationshipType(mating_data.get('relationship_type', 'threaded')),
                fit_quality=FitQuality(mating_data.get('fit_quality', 'good')),
                engagement_percent=mating_data.get('engagement_percent', 100.0)
            ),
            lifecycle_stage=LifecycleStage(row['lifecycle_stage']),
            cumulative_cycles=row['cumulative_cycles'],
            time_in_service=timedelta(seconds=row['time_in_service_seconds']) if row['time_in_service_seconds'] else None,
            stress_emotion=StressEmotion(row['stress_emotion']),
            performance_emotion=PerformanceEmotion(row['performance_emotion']),
            source_type=row['source_type'],
            source_id=row['source_id']
        )

        return qualia


class InMemoryStorageAdapter(StorageAdapter):
    """
    In-memory implementation for testing and development.
    All data is lost when the process ends.
    """

    def __init__(self):
        self.qualia_records: Dict[str, PartQualia] = {}
        self.failure_records: Dict[str, FailureRecord] = {}
        self.events: Dict[str, SignificantEvent] = {}
        self.interactions: Dict[str, HumanInteractionQualia] = {}

    async def save_qualia(self, qualia: PartQualia) -> str:
        """Save a qualia record in memory"""
        self.qualia_records[qualia.qualia_id] = qualia
        return qualia.qualia_id

    async def get_qualia(self, qualia_id: str) -> Optional[PartQualia]:
        """Retrieve a qualia record by ID"""
        return self.qualia_records.get(qualia_id)

    async def get_part_qualia_history(self,
                                      part_id: str,
                                      limit: int = 100,
                                      since: Optional[datetime] = None) -> List[PartQualia]:
        """Get qualia history for a specific part"""
        history = [
            q for q in self.qualia_records.values()
            if q.part_id == part_id
        ]

        if since:
            history = [q for q in history if q.timestamp >= since]

        # Sort by timestamp descending
        history.sort(key=lambda q: q.timestamp, reverse=True)

        return history[:limit]

    async def save_failure(self, failure: FailureRecord) -> str:
        """Save a failure record in memory"""
        self.failure_records[failure.failure_id] = failure
        return failure.failure_id

    async def save_event(self, event: SignificantEvent) -> str:
        """Save a significant event in memory"""
        self.events[event.event_id] = event
        return event.event_id

    async def save_interaction(self, interaction: HumanInteractionQualia) -> str:
        """Save a human interaction record in memory"""
        self.interactions[interaction.interaction_id] = interaction
        return interaction.interaction_id

    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics"""
        return {
            'qualia_count': len(self.qualia_records),
            'failure_count': len(self.failure_records),
            'event_count': len(self.events),
            'interaction_count': len(self.interactions),
            'unique_parts': len(set(q.part_id for q in self.qualia_records.values()))
        }
