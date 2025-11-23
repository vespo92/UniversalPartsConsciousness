"""
ISO 10993 Biocompatibility Testing Requirements

ISO 10993 is the international standard for evaluating the biological
compatibility of medical devices. This module provides the test matrix
and evaluation guidance.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ContactCategory(Enum):
    """ISO 10993-1 Contact Categories"""
    # Surface Devices
    SKIN = "skin"
    MUCOSAL_MEMBRANE = "mucosal_membrane"
    BREACHED_SURFACE = "breached_surface"

    # External Communicating
    BLOOD_PATH_INDIRECT = "blood_path_indirect"
    TISSUE_BONE_DENTIN = "tissue_bone_dentin"
    CIRCULATING_BLOOD = "circulating_blood"

    # Implant Devices
    TISSUE_BONE = "tissue_bone"
    BLOOD = "blood"


class TestType(Enum):
    """ISO 10993 Test Types"""
    CYTOTOXICITY = "cytotoxicity"                    # ISO 10993-5
    SENSITIZATION = "sensitization"                  # ISO 10993-10
    IRRITATION = "irritation"                        # ISO 10993-23
    ACUTE_SYSTEMIC_TOXICITY = "acute_systemic"       # ISO 10993-11
    SUBCHRONIC_TOXICITY = "subchronic"               # ISO 10993-11
    CHRONIC_TOXICITY = "chronic"                     # ISO 10993-11
    GENOTOXICITY = "genotoxicity"                    # ISO 10993-3
    IMPLANTATION = "implantation"                    # ISO 10993-6
    HEMOCOMPATIBILITY = "hemocompatibility"          # ISO 10993-4
    CARCINOGENICITY = "carcinogenicity"              # ISO 10993-3
    REPRODUCTIVE_TOXICITY = "reproductive_toxicity"  # ISO 10993-3
    BIODEGRADATION = "biodegradation"                # ISO 10993-9/13/14/15


@dataclass
class BiocompatibilityTest:
    """Definition of a biocompatibility test"""
    test_type: TestType
    iso_standard: str
    description: str
    typical_duration_weeks: int
    typical_cost_usd: int
    required_samples: str
    acceptance_criteria: str


# ISO 10993 Test Definitions
TEST_DEFINITIONS: Dict[TestType, BiocompatibilityTest] = {
    TestType.CYTOTOXICITY: BiocompatibilityTest(
        test_type=TestType.CYTOTOXICITY,
        iso_standard="ISO 10993-5",
        description="In vitro test for cell death/damage when exposed to material extracts",
        typical_duration_weeks=2,
        typical_cost_usd=3000,
        required_samples="3 samples, 10cm² each or equivalent",
        acceptance_criteria="Cell viability >70% of negative control"
    ),
    TestType.SENSITIZATION: BiocompatibilityTest(
        test_type=TestType.SENSITIZATION,
        iso_standard="ISO 10993-10",
        description="Allergic response potential assessment (GPMT or LLNA)",
        typical_duration_weeks=6,
        typical_cost_usd=8000,
        required_samples="Material extract, control vehicles",
        acceptance_criteria="No sensitization response in test animals"
    ),
    TestType.IRRITATION: BiocompatibilityTest(
        test_type=TestType.IRRITATION,
        iso_standard="ISO 10993-23",
        description="Tissue irritation potential from device contact",
        typical_duration_weeks=4,
        typical_cost_usd=6000,
        required_samples="Material samples for extraction",
        acceptance_criteria="Primary irritation index <1.0"
    ),
    TestType.ACUTE_SYSTEMIC_TOXICITY: BiocompatibilityTest(
        test_type=TestType.ACUTE_SYSTEMIC_TOXICITY,
        iso_standard="ISO 10993-11",
        description="Short-term systemic effects from material exposure",
        typical_duration_weeks=4,
        typical_cost_usd=10000,
        required_samples="Material extract for injection",
        acceptance_criteria="No adverse systemic effects vs control"
    ),
    TestType.SUBCHRONIC_TOXICITY: BiocompatibilityTest(
        test_type=TestType.SUBCHRONIC_TOXICITY,
        iso_standard="ISO 10993-11",
        description="Medium-term systemic effects (typically 90 days)",
        typical_duration_weeks=16,
        typical_cost_usd=35000,
        required_samples="Material extract or implant",
        acceptance_criteria="No adverse effects in organs/tissues"
    ),
    TestType.CHRONIC_TOXICITY: BiocompatibilityTest(
        test_type=TestType.CHRONIC_TOXICITY,
        iso_standard="ISO 10993-11",
        description="Long-term systemic effects (6-12 months)",
        typical_duration_weeks=52,
        typical_cost_usd=100000,
        required_samples="Material extract or implant",
        acceptance_criteria="NOAEL established, no adverse effects"
    ),
    TestType.GENOTOXICITY: BiocompatibilityTest(
        test_type=TestType.GENOTOXICITY,
        iso_standard="ISO 10993-3",
        description="DNA damage potential (Ames, chromosomal aberration, micronucleus)",
        typical_duration_weeks=8,
        typical_cost_usd=15000,
        required_samples="Material extract",
        acceptance_criteria="Negative in all three assays"
    ),
    TestType.IMPLANTATION: BiocompatibilityTest(
        test_type=TestType.IMPLANTATION,
        iso_standard="ISO 10993-6",
        description="Local tissue response to implanted material",
        typical_duration_weeks=26,
        typical_cost_usd=40000,
        required_samples="Implant samples (sterile)",
        acceptance_criteria="Response comparable to or less than control"
    ),
    TestType.HEMOCOMPATIBILITY: BiocompatibilityTest(
        test_type=TestType.HEMOCOMPATIBILITY,
        iso_standard="ISO 10993-4",
        description="Blood compatibility (hemolysis, thrombogenicity, coagulation)",
        typical_duration_weeks=6,
        typical_cost_usd=20000,
        required_samples="Material samples for blood contact",
        acceptance_criteria="Hemolysis <5%, acceptable thrombus formation"
    ),
    TestType.CARCINOGENICITY: BiocompatibilityTest(
        test_type=TestType.CARCINOGENICITY,
        iso_standard="ISO 10993-3",
        description="Tumor formation potential (rarely required)",
        typical_duration_weeks=104,
        typical_cost_usd=500000,
        required_samples="Implant samples",
        acceptance_criteria="No significant tumor incidence vs control"
    ),
}


def get_required_tests(
    contact_category: ContactCategory,
    duration: str,  # "limited" (<24h), "prolonged" (24h-30d), "permanent" (>30d)
    blood_contact: bool = False
) -> List[BiocompatibilityTest]:
    """
    Get required ISO 10993 tests based on device contact and duration.

    Args:
        contact_category: Type of body contact
        duration: Contact duration category
        blood_contact: Whether device contacts blood

    Returns:
        List of required BiocompatibilityTest objects
    """
    required = []

    # Cytotoxicity is always required
    required.append(TEST_DEFINITIONS[TestType.CYTOTOXICITY])

    # Sensitization for prolonged/permanent
    if duration in ["prolonged", "permanent"]:
        required.append(TEST_DEFINITIONS[TestType.SENSITIZATION])

    # Irritation for most contact types
    if contact_category in [ContactCategory.SKIN, ContactCategory.MUCOSAL_MEMBRANE,
                           ContactCategory.BREACHED_SURFACE]:
        required.append(TEST_DEFINITIONS[TestType.IRRITATION])

    # Systemic toxicity for communicating/implant devices
    if contact_category in [ContactCategory.BLOOD_PATH_INDIRECT,
                           ContactCategory.TISSUE_BONE_DENTIN,
                           ContactCategory.CIRCULATING_BLOOD,
                           ContactCategory.TISSUE_BONE,
                           ContactCategory.BLOOD]:
        required.append(TEST_DEFINITIONS[TestType.ACUTE_SYSTEMIC_TOXICITY])

        if duration == "prolonged":
            required.append(TEST_DEFINITIONS[TestType.SUBCHRONIC_TOXICITY])
        elif duration == "permanent":
            required.append(TEST_DEFINITIONS[TestType.SUBCHRONIC_TOXICITY])
            required.append(TEST_DEFINITIONS[TestType.CHRONIC_TOXICITY])

    # Genotoxicity for prolonged/permanent contact
    if duration in ["prolonged", "permanent"] and contact_category not in [
        ContactCategory.SKIN
    ]:
        required.append(TEST_DEFINITIONS[TestType.GENOTOXICITY])

    # Implantation for implant devices
    if contact_category in [ContactCategory.TISSUE_BONE, ContactCategory.BLOOD]:
        if duration in ["prolonged", "permanent"]:
            required.append(TEST_DEFINITIONS[TestType.IMPLANTATION])

    # Hemocompatibility for blood-contacting devices
    if blood_contact or contact_category in [
        ContactCategory.BLOOD_PATH_INDIRECT,
        ContactCategory.CIRCULATING_BLOOD,
        ContactCategory.BLOOD
    ]:
        required.append(TEST_DEFINITIONS[TestType.HEMOCOMPATIBILITY])

    return required


def estimate_testing_cost(tests: List[BiocompatibilityTest]) -> Dict:
    """
    Estimate total cost and duration for a set of tests.

    Args:
        tests: List of required tests

    Returns:
        Dict with cost and timeline estimates
    """
    total_cost = sum(t.typical_cost_usd for t in tests)
    max_duration = max(t.typical_duration_weeks for t in tests) if tests else 0

    return {
        "total_cost_usd": total_cost,
        "total_duration_weeks": max_duration,  # Tests can run in parallel
        "test_count": len(tests),
        "breakdown": [
            {
                "test": t.test_type.value,
                "standard": t.iso_standard,
                "cost_usd": t.typical_cost_usd,
                "duration_weeks": t.typical_duration_weeks
            }
            for t in tests
        ]
    }
