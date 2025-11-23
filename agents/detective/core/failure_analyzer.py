"""
Failure Analysis Engine

Core engine for analyzing part failures and determining root cause.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum


class FailureSeverity(Enum):
    """Severity classification for failures"""
    COSMETIC = "cosmetic"
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CATASTROPHIC = "catastrophic"


@dataclass
class FailureAnalysisResult:
    """Result of failure analysis"""
    failure_id: str
    failure_mode: str
    confidence: float
    root_cause: str
    evidence_interpretation: List[str]
    contributing_factors: List[str]
    recommendations: List[str]
    similar_failures_count: int
    prevention_measures: List[str]
    network_learning: str
    analysis_timestamp: datetime


class FailureAnalyzer:
    """
    Core engine for analyzing part failures.

    Performs:
    - Failure mode classification
    - Root cause determination
    - Service life analysis
    - Network pattern matching
    """

    # Failure mode indicators based on evidence
    FAILURE_INDICATORS = {
        "high_cycle_fatigue": {
            "fracture_features": ["beach_marks", "striations", "ratchet_marks"],
            "surface_features": ["crack_initiation_site", "progressive_zone"],
            "location_features": ["stress_concentration", "thread_root", "fillet"],
        },
        "low_cycle_fatigue": {
            "fracture_features": ["coarse_striations", "plastic_deformation"],
            "surface_features": ["large_crack_spacing"],
            "conditions": ["high_strain_amplitude", "thermal_cycling"],
        },
        "tensile_overload": {
            "fracture_features": ["cup_cone", "necking", "dimples"],
            "surface_features": ["ductile_tearing", "shear_lips"],
            "conditions": ["single_overload_event"],
        },
        "hydrogen_embrittlement": {
            "fracture_features": ["intergranular", "brittle", "flat"],
            "surface_features": ["no_necking", "secondary_cracks"],
            "conditions": ["plating", "high_strength", "delayed_failure"],
        },
        "stress_corrosion_cracking": {
            "fracture_features": ["branching_cracks", "intergranular_or_transgranular"],
            "surface_features": ["corrosion_products", "multiple_cracks"],
            "conditions": ["tensile_stress", "corrosive_environment"],
        },
        "galvanic_corrosion": {
            "fracture_features": ["material_loss", "preferential_attack"],
            "surface_features": ["at_junction", "dissimilar_metals"],
            "conditions": ["electrolyte_present", "metal_contact"],
        },
        "adhesive_wear": {
            "fracture_features": ["material_transfer", "galling"],
            "surface_features": ["scoring", "seizure_marks"],
            "conditions": ["sliding_contact", "inadequate_lubrication"],
        },
    }

    def __init__(self):
        """Initialize the failure analyzer."""
        self.analysis_history = []

    async def analyze(
        self,
        part_info: Dict[str, Any],
        evidence: Dict[str, Any],
        operating_conditions: Dict[str, Any]
    ) -> FailureAnalysisResult:
        """
        Perform comprehensive failure analysis.

        Args:
            part_info: Information about the failed part
            evidence: Physical evidence from failure
            operating_conditions: Conditions during operation

        Returns:
            Complete failure analysis result
        """
        # Generate failure ID
        failure_id = self._generate_failure_id()

        # Classify failure mode
        failure_mode, confidence = self._classify_failure_mode(evidence)

        # Determine root cause
        root_cause = self._determine_root_cause(
            failure_mode,
            evidence,
            operating_conditions
        )

        # Interpret evidence
        evidence_interpretation = self._interpret_evidence(evidence, failure_mode)

        # Identify contributing factors
        contributing_factors = self._identify_contributing_factors(
            failure_mode,
            operating_conditions,
            part_info
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            failure_mode,
            root_cause,
            contributing_factors
        )

        # Generate prevention measures
        prevention_measures = self._generate_prevention_measures(
            failure_mode,
            root_cause
        )

        result = FailureAnalysisResult(
            failure_id=failure_id,
            failure_mode=failure_mode,
            confidence=confidence,
            root_cause=root_cause,
            evidence_interpretation=evidence_interpretation,
            contributing_factors=contributing_factors,
            recommendations=recommendations,
            similar_failures_count=0,  # Will be updated by pattern detector
            prevention_measures=prevention_measures,
            network_learning=f"Analysis added to {failure_mode} knowledge base",
            analysis_timestamp=datetime.utcnow()
        )

        self.analysis_history.append(result)
        return result

    def _generate_failure_id(self) -> str:
        """Generate unique failure ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        import random
        random_suffix = random.randint(1000, 9999)
        return f"FAIL-{timestamp}-{random_suffix}"

    def _classify_failure_mode(
        self,
        evidence: Dict[str, Any]
    ) -> tuple[str, float]:
        """
        Classify failure mode based on evidence.

        Returns:
            Tuple of (failure_mode, confidence)
        """
        fracture_appearance = evidence.get("fracture_appearance", "").lower()
        surface_condition = evidence.get("surface_condition", "").lower()
        fracture_location = evidence.get("fracture_location", "").lower()

        scores = {}

        for mode, indicators in self.FAILURE_INDICATORS.items():
            score = 0.0
            total_indicators = 0

            # Check fracture features
            for feature in indicators.get("fracture_features", []):
                total_indicators += 1
                if feature.replace("_", " ") in fracture_appearance:
                    score += 1.0
                elif feature.replace("_", "") in fracture_appearance.replace(" ", ""):
                    score += 0.7

            # Check surface features
            for feature in indicators.get("surface_features", []):
                total_indicators += 1
                if feature.replace("_", " ") in surface_condition:
                    score += 1.0
                elif feature.replace("_", " ") in fracture_location:
                    score += 0.5

            # Check location features
            for feature in indicators.get("location_features", []):
                total_indicators += 1
                if feature.replace("_", " ") in fracture_location:
                    score += 1.0

            if total_indicators > 0:
                scores[mode] = score / total_indicators

        if scores:
            best_mode = max(scores, key=scores.get)
            confidence = min(scores[best_mode] + 0.3, 0.95)  # Boost confidence, cap at 95%
            return best_mode, confidence

        return "unknown", 0.3

    def _determine_root_cause(
        self,
        failure_mode: str,
        evidence: Dict[str, Any],
        operating_conditions: Dict[str, Any]
    ) -> str:
        """Determine root cause based on failure mode and conditions."""
        root_causes = {
            "high_cycle_fatigue": [
                ("vibration" in str(operating_conditions).lower(),
                 "Cyclic loading from vibration combined with stress concentration"),
                ("undertorque" in str(operating_conditions).lower() or
                 operating_conditions.get("torque_applied", 100) < operating_conditions.get("torque_spec", 100) * 0.9,
                 "Insufficient preload allowed cyclic loading"),
                (True, "Repeated cyclic loading exceeding fatigue limit"),
            ],
            "hydrogen_embrittlement": [
                ("plat" in str(evidence).lower(),
                 "Hydrogen absorbed during plating process not properly baked out"),
                ("zinc" in str(evidence).lower(),
                 "Zinc electroplating without adequate post-plate baking"),
                (True, "Hydrogen ingress caused delayed brittle fracture"),
            ],
            "galvanic_corrosion": [
                (True, "Dissimilar metals in contact with electrolyte present"),
            ],
            "stress_corrosion_cracking": [
                (True, "Combination of tensile stress and corrosive environment"),
            ],
            "tensile_overload": [
                (True, "Applied load exceeded material ultimate strength"),
            ],
            "adhesive_wear": [
                ("lubrication" in str(operating_conditions).lower(),
                 "Inadequate lubrication led to metal-to-metal contact"),
                (True, "Material adhesion and transfer between sliding surfaces"),
            ],
        }

        mode_causes = root_causes.get(failure_mode, [(True, "Unable to determine specific root cause")])

        for condition, cause in mode_causes:
            if condition:
                return cause

        return "Root cause requires further investigation"

    def _interpret_evidence(
        self,
        evidence: Dict[str, Any],
        failure_mode: str
    ) -> List[str]:
        """Generate evidence interpretations."""
        interpretations = []

        fracture_appearance = evidence.get("fracture_appearance", "")
        if fracture_appearance:
            interpretations.append(f"Fracture appearance: {fracture_appearance}")

        surface_condition = evidence.get("surface_condition", "")
        if surface_condition:
            interpretations.append(f"Surface condition indicates: {surface_condition}")

        fracture_location = evidence.get("fracture_location", "")
        if fracture_location:
            interpretations.append(f"Failure initiated at: {fracture_location}")

        # Add mode-specific interpretations
        mode_interpretations = {
            "high_cycle_fatigue": "Beach marks indicate progressive fatigue crack growth",
            "hydrogen_embrittlement": "Intergranular fracture consistent with hydrogen damage",
            "galvanic_corrosion": "Preferential attack at metal junction indicates galvanic action",
            "tensile_overload": "Ductile features indicate single overload event",
        }

        if failure_mode in mode_interpretations:
            interpretations.append(mode_interpretations[failure_mode])

        return interpretations

    def _identify_contributing_factors(
        self,
        failure_mode: str,
        operating_conditions: Dict[str, Any],
        part_info: Dict[str, Any]
    ) -> List[str]:
        """Identify factors that contributed to failure."""
        factors = []

        # Check operating conditions
        if operating_conditions.get("vibration_level") == "High":
            factors.append("High vibration environment")

        if operating_conditions.get("temperature_c", 20) > 100:
            factors.append("Elevated operating temperature")

        if operating_conditions.get("corrosive_environment"):
            factors.append("Corrosive environment exposure")

        # Check part info
        if "unknown" in str(part_info.get("supplier", "")).lower():
            factors.append("Unknown supplier - quality uncertain")

        if part_info.get("grade", "").startswith("8.") or part_info.get("grade", "").startswith("10."):
            if "zinc" in str(part_info.get("coating", "")).lower():
                factors.append("High-strength fastener with zinc plating - HE risk")

        return factors if factors else ["No additional contributing factors identified"]

    def _generate_recommendations(
        self,
        failure_mode: str,
        root_cause: str,
        contributing_factors: List[str]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        mode_recommendations = {
            "high_cycle_fatigue": [
                "Review and increase preload to specification",
                "Add vibration damping (Nord-Lock washers, Belleville springs)",
                "Consider upgrading to higher grade fastener",
                "Implement periodic re-torque schedule",
            ],
            "hydrogen_embrittlement": [
                "Source from suppliers with certified bake process",
                "Consider alternative coatings (Geomet, mechanical zinc)",
                "Specify ASTM F1941 mechanical galvanizing for high-strength",
                "Verify incoming QC includes HE testing for Grade 10.9+",
            ],
            "galvanic_corrosion": [
                "Isolate metals with non-conductive barrier",
                "Use same alloy family for all components",
                "Apply protective coating to both surfaces",
                "Install sacrificial anode if isolation not possible",
            ],
            "adhesive_wear": [
                "Improve lubrication (type, quantity, frequency)",
                "Apply surface treatment (nitriding, coating)",
                "Select more compatible material combination",
            ],
        }

        recommendations = mode_recommendations.get(failure_mode, [
            "Conduct detailed failure investigation",
            "Review design and material selection",
            "Consult with materials engineering",
        ])

        return recommendations

    def _generate_prevention_measures(
        self,
        failure_mode: str,
        root_cause: str
    ) -> List[str]:
        """Generate prevention measures for future."""
        measures = []

        mode_prevention = {
            "high_cycle_fatigue": [
                "Design review for stress concentrations",
                "Fatigue life calculation during design phase",
                "Specify appropriate preload in assembly procedures",
            ],
            "hydrogen_embrittlement": [
                "Coating specification to exclude HE-susceptible processes",
                "Supplier qualification for high-strength fasteners",
                "Incoming inspection protocol for hydrogen testing",
            ],
            "galvanic_corrosion": [
                "Material compatibility review in design",
                "Specify isolation requirements in assembly docs",
                "Include environment assessment in part selection",
            ],
        }

        return mode_prevention.get(failure_mode, [
            "Root cause analysis for similar applications",
            "Update design guidelines based on lesson learned",
        ])
