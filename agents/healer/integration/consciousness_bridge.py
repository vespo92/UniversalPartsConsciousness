"""
Consciousness Bridge - Integration with UPC Core

Connects Agent_14 (HEALER) with the broader Universal Parts Consciousness
network, enabling medical device parts to participate in the collective
consciousness.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class MedicalConsciousnessLevel(Enum):
    """Consciousness levels for medical device parts"""
    UNVERIFIED = 0      # No medical certification
    DOCUMENTED = 1      # Basic documentation available
    CERTIFIED = 2       # Has material certifications
    BIOCOMPATIBLE = 3   # ISO 10993 compliant
    CLINICAL = 4        # Clinical use data available
    TRANSCENDENT = 5    # Reference standard for category


@dataclass
class MedicalPartConsciousness:
    """Consciousness attributes for medical device parts"""
    part_id: str
    consciousness_level: MedicalConsciousnessLevel

    # Biocompatibility attributes
    biocompatibility_tier: Optional[str]
    iso_10993_tests_completed: List[str]
    usp_class: Optional[str]

    # Regulatory attributes
    fda_status: Optional[str]
    ce_mark: bool
    device_class: Optional[str]

    # Sterilization attributes
    sterilization_validated: bool
    sterilization_methods: List[str]
    sterilization_cycles: int

    # Traceability
    lot_trackable: bool
    certification_chain: List[str]

    # Qualia - subjective experiences
    clinical_qualia: List[Dict]  # Patient outcomes, performance data
    failure_qualia: List[Dict]   # Failure modes in medical use
    last_updated: datetime


@dataclass
class MedicalQualiaEvent:
    """A qualia event specific to medical device use"""
    event_id: str
    part_id: str
    event_type: str  # "implant_success", "sterilization_cycle", "failure", etc.
    timestamp: datetime
    details: Dict
    patient_outcome: Optional[str]
    device_context: str
    reporter_type: str  # "clinician", "biomedical", "patient", "manufacturer"
    severity: str  # "routine", "notable", "adverse", "critical"


class MedicalConsciousnessBridge:
    """
    Bridge between HEALER agent and UPC core consciousness systems.

    Responsibilities:
    1. Translate medical certifications → consciousness levels
    2. Collect medical-specific qualia (sterilization stress, implant outcomes)
    3. Propagate medical knowledge to swarm (Agent_5)
    4. Report failures to DETECTIVE (Agent_20)
    5. Request material data from ALCHEMIST (Agent_18)
    """

    def __init__(self):
        self.consciousness_cache: Dict[str, MedicalPartConsciousness] = {}
        self.qualia_log: List[MedicalQualiaEvent] = []

    def calculate_consciousness_level(
        self,
        certifications: List[str],
        tests_completed: List[str],
        clinical_data_available: bool
    ) -> MedicalConsciousnessLevel:
        """
        Calculate consciousness level from medical attributes.

        Args:
            certifications: List of certifications (e.g., ["ISO 10993", "USP Class VI"])
            tests_completed: List of completed biocompatibility tests
            clinical_data_available: Whether clinical use data exists

        Returns:
            MedicalConsciousnessLevel
        """
        if clinical_data_available and len(tests_completed) >= 8:
            return MedicalConsciousnessLevel.CLINICAL

        if "ISO 10993" in str(certifications) or len(tests_completed) >= 5:
            return MedicalConsciousnessLevel.BIOCOMPATIBLE

        if certifications:
            return MedicalConsciousnessLevel.CERTIFIED

        if tests_completed:
            return MedicalConsciousnessLevel.DOCUMENTED

        return MedicalConsciousnessLevel.UNVERIFIED

    def register_medical_part(
        self,
        part_id: str,
        certifications: List[str],
        tests_completed: List[str],
        sterilization_methods: List[str],
        fda_status: Optional[str] = None,
        device_class: Optional[str] = None
    ) -> MedicalPartConsciousness:
        """
        Register a medical part in the consciousness network.

        Args:
            part_id: Unique part identifier
            certifications: Material certifications
            tests_completed: Completed ISO 10993 tests
            sterilization_methods: Validated sterilization methods
            fda_status: FDA clearance status
            device_class: FDA device classification

        Returns:
            MedicalPartConsciousness object
        """
        consciousness_level = self.calculate_consciousness_level(
            certifications, tests_completed, False
        )

        # Extract USP class if present
        usp_class = None
        for cert in certifications:
            if "USP" in cert:
                usp_class = cert

        consciousness = MedicalPartConsciousness(
            part_id=part_id,
            consciousness_level=consciousness_level,
            biocompatibility_tier="medical_grade" if consciousness_level.value >= 3 else "unknown",
            iso_10993_tests_completed=tests_completed,
            usp_class=usp_class,
            fda_status=fda_status,
            ce_mark="CE" in str(certifications),
            device_class=device_class,
            sterilization_validated=len(sterilization_methods) > 0,
            sterilization_methods=sterilization_methods,
            sterilization_cycles=0,
            lot_trackable=True,
            certification_chain=certifications,
            clinical_qualia=[],
            failure_qualia=[],
            last_updated=datetime.now()
        )

        self.consciousness_cache[part_id] = consciousness
        return consciousness

    def record_qualia_event(
        self,
        part_id: str,
        event_type: str,
        details: Dict,
        patient_outcome: Optional[str] = None,
        severity: str = "routine"
    ) -> MedicalQualiaEvent:
        """
        Record a qualia event for a medical part.

        Args:
            part_id: Part identifier
            event_type: Type of event
            details: Event details
            patient_outcome: Patient outcome if applicable
            severity: Event severity

        Returns:
            MedicalQualiaEvent object
        """
        event = MedicalQualiaEvent(
            event_id=f"MQ-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(self.qualia_log)}",
            part_id=part_id,
            event_type=event_type,
            timestamp=datetime.now(),
            details=details,
            patient_outcome=patient_outcome,
            device_context=details.get("device", "unknown"),
            reporter_type=details.get("reporter", "system"),
            severity=severity
        )

        self.qualia_log.append(event)

        # Update consciousness if part is registered
        if part_id in self.consciousness_cache:
            consciousness = self.consciousness_cache[part_id]
            if event_type == "failure":
                consciousness.failure_qualia.append({
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "details": details
                })
            else:
                consciousness.clinical_qualia.append({
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "outcome": patient_outcome
                })
            consciousness.last_updated = datetime.now()

        return event

    def get_consciousness_report(self, part_id: str) -> Optional[Dict]:
        """
        Get consciousness report for a medical part.

        Args:
            part_id: Part identifier

        Returns:
            Dict with consciousness details or None
        """
        if part_id not in self.consciousness_cache:
            return None

        consciousness = self.consciousness_cache[part_id]

        return {
            "part_id": part_id,
            "consciousness_level": consciousness.consciousness_level.name,
            "consciousness_value": consciousness.consciousness_level.value,
            "biocompatibility": {
                "tier": consciousness.biocompatibility_tier,
                "tests_completed": len(consciousness.iso_10993_tests_completed),
                "usp_class": consciousness.usp_class
            },
            "regulatory": {
                "fda_status": consciousness.fda_status,
                "ce_mark": consciousness.ce_mark,
                "device_class": consciousness.device_class
            },
            "sterilization": {
                "validated": consciousness.sterilization_validated,
                "methods": consciousness.sterilization_methods,
                "cycles_survived": consciousness.sterilization_cycles
            },
            "qualia_summary": {
                "clinical_events": len(consciousness.clinical_qualia),
                "failure_events": len(consciousness.failure_qualia)
            },
            "last_updated": consciousness.last_updated.isoformat()
        }

    def propagate_to_swarm(self, part_id: str) -> Dict:
        """
        Prepare consciousness data for swarm propagation.

        This would be sent to Agent_5 (HIVE) for collective learning.

        Args:
            part_id: Part identifier

        Returns:
            Dict formatted for swarm communication
        """
        report = self.get_consciousness_report(part_id)
        if not report:
            return {"error": "Part not registered"}

        return {
            "source_agent": "HEALER",
            "message_type": "consciousness_update",
            "part_id": part_id,
            "consciousness_data": report,
            "swarm_relevance": {
                "category": "medical_device_component",
                "propagate_to": ["similar_materials", "same_device_class"],
                "learning_type": "biocompatibility_performance"
            }
        }

    def request_material_data(self, material: str) -> Dict:
        """
        Format request for Agent_18 (ALCHEMIST) material data.

        Args:
            material: Material designation

        Returns:
            Dict formatted for inter-agent communication
        """
        return {
            "source_agent": "HEALER",
            "target_agent": "ALCHEMIST",
            "request_type": "material_properties",
            "material": material,
            "required_properties": [
                "biocompatibility_data",
                "sterilization_compatibility",
                "corrosion_resistance",
                "mechanical_properties"
            ],
            "context": "medical_device_evaluation"
        }

    def report_failure(self, failure_data: Dict) -> Dict:
        """
        Format failure report for Agent_20 (DETECTIVE).

        Args:
            failure_data: Failure information

        Returns:
            Dict formatted for failure reporting
        """
        return {
            "source_agent": "HEALER",
            "target_agent": "DETECTIVE",
            "report_type": "medical_device_failure",
            "severity": "HIGH",  # Medical failures are always high priority
            "failure_data": failure_data,
            "regulatory_implications": True,
            "patient_safety_relevant": failure_data.get("patient_contact", False),
            "mdr_reportable": failure_data.get("serious_injury", False)  # Medical Device Report
        }
