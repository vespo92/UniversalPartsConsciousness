"""
MACHINIST Agent Data Schemas

Data structures for industrial equipment intelligence.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class EquipmentStatus(Enum):
    """Equipment lifecycle status"""
    ACTIVE = "active"
    SUPPORTED = "supported"
    LIMITED_SUPPORT = "limited_support"
    END_OF_LIFE = "end_of_life"
    OBSOLETE = "obsolete"


class MaintenanceUrgency(Enum):
    """Maintenance urgency levels"""
    ROUTINE = "routine"
    SCHEDULED = "scheduled"
    ATTENTION = "attention"
    URGENT = "urgent"
    CRITICAL = "critical"


@dataclass
class IndustrialEquipment:
    """Base class for industrial equipment"""
    equipment_id: str
    manufacturer: str
    model: str
    serial_number: Optional[str]
    year_manufactured: Optional[int]
    installation_date: Optional[datetime]
    status: EquipmentStatus
    location: str
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CNCMachine(IndustrialEquipment):
    """CNC machine specification"""
    machine_type: str              # "Mill", "Lathe", "Router", "EDM"
    control_manufacturer: str
    control_model: str
    control_generation: str
    axes: int
    spindle_max_rpm: int
    table_size_mm: tuple           # (X, Y) or (swing, length)
    tool_changer_capacity: int
    coolant_type: str


@dataclass
class PLCSystem(IndustrialEquipment):
    """PLC system specification"""
    cpu_model: str
    firmware_version: str
    io_modules: List[Dict[str, Any]]
    total_io_points: int
    communication_modules: List[str]
    program_size_kb: int
    scan_time_ms: float


@dataclass
class ServoSystem(IndustrialEquipment):
    """Servo system specification"""
    drive_model: str
    motor_model: str
    power_kw: float
    encoder_type: str
    encoder_resolution: int
    interface_type: str
    axis_assignment: str


@dataclass
class MaintenanceRecord:
    """Equipment maintenance record"""
    record_id: str
    equipment_id: str
    date: datetime
    maintenance_type: str          # "Preventive", "Corrective", "Retrofit"
    description: str
    parts_replaced: List[Dict[str, str]]
    labor_hours: float
    cost_usd: float
    technician: str
    notes: str


@dataclass
class RetrofitProject:
    """Retrofit project tracking"""
    project_id: str
    equipment_id: str
    project_name: str
    scope: str
    status: str                    # "Planning", "In Progress", "Complete"
    start_date: Optional[datetime]
    completion_date: Optional[datetime]
    budget_usd: float
    actual_cost_usd: Optional[float]
    downtime_hours: float
    components_replaced: List[Dict[str, Any]]
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    lessons_learned: str


@dataclass
class PartQuery:
    """Query for industrial parts"""
    query_id: str
    timestamp: datetime
    equipment_context: Optional[IndustrialEquipment]
    query_type: str                # "Retrofit", "Replacement", "Cross-reference"
    original_part: str
    requirements: Dict[str, Any]
    constraints: Dict[str, Any]


@dataclass
class PartRecommendation:
    """Part recommendation result"""
    recommendation_id: str
    query_id: str
    recommended_part: str
    manufacturer: str
    part_number: str
    compatibility_score: float
    price_estimate_usd: Optional[float]
    lead_time_days: Optional[int]
    installation_notes: str
    warnings: List[str]
    alternatives: List[Dict[str, Any]]


# Message schemas for UPC message bus
@dataclass
class MachinistQuery:
    """Query message for MACHINIST agent"""
    query_id: str
    sender: str
    timestamp: str
    query_type: str               # "cnc_retrofit", "plc_migration", "servo_xref", "fastener"
    parameters: Dict[str, Any]
    priority: int = 5


@dataclass
class MachinistResponse:
    """Response message from MACHINIST agent"""
    response_id: str
    query_id: str
    timestamp: str
    success: bool
    results: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None


__all__ = [
    "EquipmentStatus",
    "MaintenanceUrgency",
    "IndustrialEquipment",
    "CNCMachine",
    "PLCSystem",
    "ServoSystem",
    "MaintenanceRecord",
    "RetrofitProject",
    "PartQuery",
    "PartRecommendation",
    "MachinistQuery",
    "MachinistResponse",
]
