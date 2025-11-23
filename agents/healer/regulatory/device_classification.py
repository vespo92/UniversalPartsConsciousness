"""
Medical Device Classification Module

Provides FDA device classification guidance and 510(k) decision support.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class DeviceClassification(Enum):
    """FDA Device Classification"""
    CLASS_I = "I"        # Low risk - general controls
    CLASS_II = "II"      # Moderate risk - 510(k) required
    CLASS_III = "III"    # High risk - PMA required


class RegulatoryPathway(Enum):
    """FDA Regulatory Pathways"""
    EXEMPT = "exempt"                    # Class I exempt
    GENERAL_CONTROLS = "general"         # Class I non-exempt
    PREMARKET_510K = "510k"              # Class II
    DE_NOVO = "de_novo"                  # Novel Class II
    PMA = "pma"                          # Class III
    HDE = "hde"                          # Humanitarian Device


@dataclass
class DeviceClassificationResult:
    """Result of device classification analysis"""
    device_type: str
    classification: DeviceClassification
    regulation_number: Optional[str]
    product_code: Optional[str]
    regulatory_pathway: RegulatoryPathway
    predicate_devices: List[str]
    special_controls: List[str]
    guidance_documents: List[str]


# Common medical device classifications
DEVICE_CLASSIFICATIONS: Dict[str, Dict] = {
    "infusion_pump": {
        "classification": DeviceClassification.CLASS_II,
        "regulation": "21 CFR 880.5725",
        "product_code": "FRN",
        "pathway": RegulatoryPathway.PREMARKET_510K,
        "special_controls": [
            "Software validation",
            "Electrical safety (IEC 60601-1)",
            "Accuracy and reliability testing",
            "Alarm system verification"
        ]
    },
    "surgical_instrument": {
        "classification": DeviceClassification.CLASS_I,
        "regulation": "21 CFR 878.4800",
        "product_code": "GEI",
        "pathway": RegulatoryPathway.EXEMPT,
        "special_controls": []
    },
    "orthopedic_implant": {
        "classification": DeviceClassification.CLASS_II,
        "regulation": "21 CFR 888.3030",
        "product_code": "HRS",
        "pathway": RegulatoryPathway.PREMARKET_510K,
        "special_controls": [
            "Biocompatibility (ISO 10993)",
            "Mechanical testing",
            "Corrosion resistance",
            "Sterility assurance"
        ]
    },
    "pacemaker": {
        "classification": DeviceClassification.CLASS_III,
        "regulation": "21 CFR 870.3610",
        "product_code": "DXY",
        "pathway": RegulatoryPathway.PMA,
        "special_controls": [
            "Clinical trials",
            "Comprehensive biocompatibility",
            "EMC testing",
            "Reliability testing"
        ]
    },
    "hip_implant": {
        "classification": DeviceClassification.CLASS_III,
        "regulation": "21 CFR 888.3300",
        "product_code": "NRJ",
        "pathway": RegulatoryPathway.PMA,
        "special_controls": [
            "Clinical trials",
            "Wear testing",
            "Biocompatibility",
            "Long-term performance"
        ]
    },
    "patient_monitor": {
        "classification": DeviceClassification.CLASS_II,
        "regulation": "21 CFR 870.1025",
        "product_code": "DRT",
        "pathway": RegulatoryPathway.PREMARKET_510K,
        "special_controls": [
            "Electrical safety",
            "Accuracy validation",
            "Alarm testing"
        ]
    },
    "bandage": {
        "classification": DeviceClassification.CLASS_I,
        "regulation": "21 CFR 880.5240",
        "product_code": "FRO",
        "pathway": RegulatoryPathway.EXEMPT,
        "special_controls": []
    },
    "ct_scanner": {
        "classification": DeviceClassification.CLASS_II,
        "regulation": "21 CFR 892.1750",
        "product_code": "JAK",
        "pathway": RegulatoryPathway.PREMARKET_510K,
        "special_controls": [
            "Radiation safety",
            "Image quality",
            "Electrical safety"
        ]
    },
}


def classify_device(device_description: str) -> DeviceClassificationResult:
    """
    Classify a medical device based on description.

    Args:
        device_description: Description of the medical device

    Returns:
        DeviceClassificationResult with classification details
    """
    desc_lower = device_description.lower()

    # Match against known device types
    for device_type, info in DEVICE_CLASSIFICATIONS.items():
        if device_type.replace("_", " ") in desc_lower or device_type in desc_lower:
            return DeviceClassificationResult(
                device_type=device_type,
                classification=info["classification"],
                regulation_number=info["regulation"],
                product_code=info["product_code"],
                regulatory_pathway=info["pathway"],
                predicate_devices=[],  # Would be populated from database
                special_controls=info["special_controls"],
                guidance_documents=[]
            )

    # Default classification (conservative)
    return DeviceClassificationResult(
        device_type="unknown",
        classification=DeviceClassification.CLASS_II,
        regulation_number=None,
        product_code=None,
        regulatory_pathway=RegulatoryPathway.PREMARKET_510K,
        predicate_devices=[],
        special_controls=["Classification review required"],
        guidance_documents=["Consult FDA Classification Database"]
    )


def assess_510k_requirement(
    original_device: str,
    proposed_change: str,
    change_type: str
) -> Dict:
    """
    Assess whether a device change requires a new 510(k).

    Based on FDA guidance "Deciding When to Submit a 510(k)
    for a Change to an Existing Device"

    Args:
        original_device: Description of original device
        proposed_change: Description of the change
        change_type: Type of change (material, design, software, etc.)

    Returns:
        Dict with 510(k) requirement assessment
    """
    change_lower = change_type.lower()

    # High-risk changes that likely require 510(k)
    high_risk_changes = [
        "technology", "energy source", "operating principle",
        "indication", "patient population", "anatomical site"
    ]

    # Medium-risk changes that may require 510(k)
    medium_risk_changes = [
        "material", "component", "software", "sterilization",
        "manufacturing process", "packaging"
    ]

    # Low-risk changes typically Letter to File
    low_risk_changes = [
        "supplier", "labeling", "cosmetic", "minor specification"
    ]

    if any(change in change_lower for change in high_risk_changes):
        return {
            "requires_510k": True,
            "confidence": "HIGH",
            "reason": f"Change type '{change_type}' typically requires new 510(k)",
            "recommendation": "Prepare new 510(k) submission",
            "documentation": [
                "Substantial equivalence determination",
                "Device description and specifications",
                "Performance testing",
                "Biocompatibility (if applicable)"
            ]
        }
    elif any(change in change_lower for change in medium_risk_changes):
        return {
            "requires_510k": None,  # Uncertain
            "confidence": "MEDIUM",
            "reason": f"Change type '{change_type}' may or may not require 510(k)",
            "recommendation": "Perform detailed assessment per FDA guidance flowcharts",
            "documentation": [
                "Change assessment documentation",
                "Risk analysis impact",
                "Verification/validation testing",
                "Letter to File or 510(k) based on assessment"
            ]
        }
    else:
        return {
            "requires_510k": False,
            "confidence": "HIGH",
            "reason": f"Change type '{change_type}' typically does not require 510(k)",
            "recommendation": "Document in Letter to File per QMS procedures",
            "documentation": [
                "Change description",
                "Risk analysis review",
                "Justification for Letter to File"
            ]
        }
