"""
Type definitions for Agent_6 PROPHET
Core data structures for pattern detection and emergence analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class PatternLayer(Enum):
    """Five layers of emergence detection"""
    STATISTICAL = 1      # Failure rate anomalies, correlations, distribution shifts
    BEHAVIORAL = 2       # Success formulas, failure clustering, longevity factors
    RELATIONAL = 3       # Compatibility networks, assembly archetypes
    INNOVATION = 4       # Gap detection, cross-category inspiration
    META = 5             # Pattern-of-patterns, transcendence precursors


class PatternStatus(Enum):
    """Status of detected patterns"""
    ACTIVE = "active"
    CONFIRMED = "confirmed"
    INVALIDATED = "invalidated"
    ARCHIVED = "archived"


class FailureModeStatus(Enum):
    """Status of novel failure mode documentation"""
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    DOCUMENTED = "documented"
    REJECTED = "rejected"


class UrgencyLevel(Enum):
    """Urgency levels for failures and opportunities"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class OpportunityType(Enum):
    """Types of innovation opportunities"""
    PREVENTION_INNOVATION = "prevention_innovation"
    CROSS_DOMAIN_TRANSFER = "cross_domain_transfer"
    MATERIAL_EVOLUTION = "material_evolution"
    DESIGN_EVOLUTION = "design_evolution"
    GAP_FILLING = "gap_filling"


class PredictionType(Enum):
    """Types of predictions"""
    FAILURE = "failure"
    DEMAND = "demand"
    EVOLUTION = "evolution"
    EMERGENCE = "emergence"


@dataclass
class DetectedPattern:
    """A pattern detected by the emergence detector"""
    pattern_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    layer: PatternLayer = PatternLayer.STATISTICAL
    pattern_type: str = ""
    category: str = ""
    name: str = ""
    description: str = ""
    significance_score: Decimal = Decimal("0.0")

    # Evidence
    evidence: Dict[str, Any] = field(default_factory=dict)
    sample_size: int = 0
    confidence: Decimal = Decimal("0.0")

    # Temporal
    first_detected_at: datetime = field(default_factory=datetime.now)
    last_confirmed_at: Optional[datetime] = None
    detection_count: int = 1

    # Status
    status: PatternStatus = PatternStatus.ACTIVE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "pattern_id": self.pattern_id,
            "layer": self.layer.value,
            "pattern_type": self.pattern_type,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "significance_score": float(self.significance_score),
            "evidence": self.evidence,
            "sample_size": self.sample_size,
            "confidence": float(self.confidence),
            "first_detected_at": self.first_detected_at.isoformat(),
            "last_confirmed_at": self.last_confirmed_at.isoformat() if self.last_confirmed_at else None,
            "detection_count": self.detection_count,
            "status": self.status.value,
        }


@dataclass
class FailureCluster:
    """A cluster of related failures"""
    cluster_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    failures: List[str] = field(default_factory=list)  # failure record IDs
    centroid_embedding: Optional[List[float]] = None
    common_characteristics: Dict[str, Any] = field(default_factory=dict)
    similarity_score: Decimal = Decimal("0.0")


@dataclass
class NovelFailureMode:
    """A newly discovered failure mode not in existing taxonomy"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    cluster_id: str = ""

    # Identification
    proposed_name: str = ""
    proposed_category: str = ""

    # Characteristics
    common_characteristics: Dict[str, Any] = field(default_factory=dict)
    affected_part_types: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)

    # Statistics
    failure_count: int = 0
    first_occurrence_at: Optional[datetime] = None
    affected_parts_count: int = 0

    # Documentation
    documentation_status: FailureModeStatus = FailureModeStatus.PROPOSED
    taxonomy_id: Optional[str] = None

    # Urgency and confidence
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    confidence_score: Decimal = Decimal("0.0")

    detected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "cluster_id": self.cluster_id,
            "proposed_name": self.proposed_name,
            "proposed_category": self.proposed_category,
            "common_characteristics": self.common_characteristics,
            "affected_part_types": self.affected_part_types,
            "conditions": self.conditions,
            "failure_count": self.failure_count,
            "first_occurrence_at": self.first_occurrence_at.isoformat() if self.first_occurrence_at else None,
            "affected_parts_count": self.affected_parts_count,
            "documentation_status": self.documentation_status.value,
            "taxonomy_id": self.taxonomy_id,
            "urgency": self.urgency.value,
            "confidence_score": float(self.confidence_score),
            "detected_at": self.detected_at.isoformat(),
        }


@dataclass
class SuccessFormula:
    """A pattern of success extracted from successful assemblies"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    domain: str = ""

    # Formula components
    required_parts: List[Dict[str, Any]] = field(default_factory=list)
    optional_parts: List[Dict[str, Any]] = field(default_factory=list)
    forbidden_parts: List[Dict[str, Any]] = field(default_factory=list)

    # Configuration requirements
    configuration: Dict[str, Any] = field(default_factory=dict)
    torque_specs: Optional[Dict[str, Decimal]] = None
    material_requirements: List[str] = field(default_factory=list)
    environmental_limits: Dict[str, Any] = field(default_factory=dict)

    # Success metrics
    success_rate: Decimal = Decimal("0.0")
    average_lifespan_hours: int = 0
    failure_reduction_percent: Decimal = Decimal("0.0")

    # Evidence
    sample_size: int = 0
    confidence_score: Decimal = Decimal("0.0")
    example_assemblies: List[str] = field(default_factory=list)

    # Status
    status: str = "proposed"  # proposed, validated, published, deprecated

    discovered_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "required_parts": self.required_parts,
            "optional_parts": self.optional_parts,
            "forbidden_parts": self.forbidden_parts,
            "configuration": self.configuration,
            "torque_specs": {k: float(v) for k, v in self.torque_specs.items()} if self.torque_specs else None,
            "material_requirements": self.material_requirements,
            "environmental_limits": self.environmental_limits,
            "success_rate": float(self.success_rate),
            "average_lifespan_hours": self.average_lifespan_hours,
            "failure_reduction_percent": float(self.failure_reduction_percent),
            "sample_size": self.sample_size,
            "confidence_score": float(self.confidence_score),
            "example_assemblies": self.example_assemblies,
            "status": self.status,
            "discovered_at": self.discovered_at.isoformat(),
        }


@dataclass
class InnovationOpportunity:
    """An identified opportunity for innovation"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    opportunity_type: OpportunityType = OpportunityType.GAP_FILLING
    title: str = ""
    description: str = ""

    # Problem/Solution
    problem_statement: str = ""
    proposed_solution: str = ""

    # For cross-domain transfer
    source_domain: Optional[str] = None
    target_domain: Optional[str] = None
    success_principle: Optional[str] = None

    # Impact assessment
    affected_market_size: int = 0
    estimated_impact_score: Decimal = Decimal("0.0")
    priority_score: Decimal = Decimal("0.0")

    # Evidence
    supporting_patterns: List[str] = field(default_factory=list)
    confidence: Decimal = Decimal("0.0")

    # Status
    status: str = "identified"  # identified, validated, in_progress, realized, dismissed

    identified_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "opportunity_type": self.opportunity_type.value,
            "title": self.title,
            "description": self.description,
            "problem_statement": self.problem_statement,
            "proposed_solution": self.proposed_solution,
            "source_domain": self.source_domain,
            "target_domain": self.target_domain,
            "success_principle": self.success_principle,
            "affected_market_size": self.affected_market_size,
            "estimated_impact_score": float(self.estimated_impact_score),
            "priority_score": float(self.priority_score),
            "supporting_patterns": self.supporting_patterns,
            "confidence": float(self.confidence),
            "status": self.status,
            "identified_at": self.identified_at.isoformat(),
        }


@dataclass
class Prediction:
    """A prediction about future state"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prediction_type: PredictionType = PredictionType.FAILURE
    subject_id: str = ""
    subject_type: str = ""

    # Prediction content
    prediction: Dict[str, Any] = field(default_factory=dict)
    probability: Decimal = Decimal("0.0")
    timeline_days: int = 0

    # For failure predictions
    predicted_failure_mode: Optional[str] = None
    prevention_actions: List[str] = field(default_factory=list)

    # Validation
    confidence: Decimal = Decimal("0.0")
    validated: bool = False
    validation_result: Optional[Dict[str, Any]] = None
    validated_at: Optional[datetime] = None

    predicted_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "prediction_type": self.prediction_type.value,
            "subject_id": self.subject_id,
            "subject_type": self.subject_type,
            "prediction": self.prediction,
            "probability": float(self.probability),
            "timeline_days": self.timeline_days,
            "predicted_failure_mode": self.predicted_failure_mode,
            "prevention_actions": self.prevention_actions,
            "confidence": float(self.confidence),
            "validated": self.validated,
            "validation_result": self.validation_result,
            "validated_at": self.validated_at.isoformat() if self.validated_at else None,
            "predicted_at": self.predicted_at.isoformat(),
        }


@dataclass
class EmergenceIndicator:
    """Indicators of emergence in a swarm or pattern"""
    swarm_id: str = ""
    emergence_type: str = ""  # new_category, behavioral_shift, collective_learning
    description: str = ""
    score: Decimal = Decimal("0.0")
    estimated_timeline: str = ""
    estimated_impact: str = ""
    confidence: Decimal = Decimal("0.0")


@dataclass
class FailureRecord:
    """A record of a part failure"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    part_id: str = ""
    failure_mode: str = ""
    failure_timestamp: datetime = field(default_factory=datetime.now)

    # Context
    environment: Dict[str, Any] = field(default_factory=dict)
    load_conditions: Dict[str, Any] = field(default_factory=dict)
    age_at_failure: Optional[int] = None  # hours

    # Characteristics
    material: str = ""
    part_type: str = ""
    prior_events: List[str] = field(default_factory=list)

    # Embedding for similarity search
    embedding: Optional[List[float]] = None


@dataclass
class Assembly:
    """An assembly of parts"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parts: List[str] = field(default_factory=list)
    domain: str = ""
    application: str = ""

    # Performance
    success: bool = True
    lifespan_hours: Optional[int] = None
    failure_mode: Optional[str] = None

    # Configuration
    configuration: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmKnowledge:
    """Knowledge from a swarm of parts"""
    swarm_id: str = ""
    swarm_tier: int = 1  # 1-5: global, family, spec, context, experience
    member_count: int = 0

    # Collective knowledge
    common_failures: List[str] = field(default_factory=list)
    success_patterns: List[str] = field(default_factory=list)
    environmental_adaptations: Dict[str, Any] = field(default_factory=dict)

    # Emergence indicators
    emergence_score: Decimal = Decimal("0.0")
    collective_learning_rate: Decimal = Decimal("0.0")
