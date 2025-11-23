"""
Agent_20: DETECTIVE - Main Agent Orchestration

The DetectiveAgent coordinates all failure analysis, root cause investigation,
pattern detection, and predictive maintenance capabilities.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any
import asyncio


class FailureMode(Enum):
    """Enumeration of all recognized failure modes"""
    # Fatigue failures
    HIGH_CYCLE_FATIGUE = "high_cycle_fatigue"
    LOW_CYCLE_FATIGUE = "low_cycle_fatigue"
    THERMAL_FATIGUE = "thermal_fatigue"
    CORROSION_FATIGUE = "corrosion_fatigue"

    # Overload failures
    TENSILE_OVERLOAD = "tensile_overload"
    SHEAR_OVERLOAD = "shear_overload"
    COMPRESSIVE_OVERLOAD = "compressive_overload"
    TORSIONAL_OVERLOAD = "torsional_overload"

    # Wear failures
    ADHESIVE_WEAR = "adhesive_wear"
    ABRASIVE_WEAR = "abrasive_wear"
    EROSIVE_WEAR = "erosive_wear"
    FRETTING_WEAR = "fretting_wear"

    # Corrosion failures
    UNIFORM_CORROSION = "uniform_corrosion"
    PITTING_CORROSION = "pitting_corrosion"
    GALVANIC_CORROSION = "galvanic_corrosion"
    CREVICE_CORROSION = "crevice_corrosion"
    STRESS_CORROSION_CRACKING = "stress_corrosion_cracking"
    INTERGRANULAR_CORROSION = "intergranular_corrosion"

    # Material failures
    HYDROGEN_EMBRITTLEMENT = "hydrogen_embrittlement"
    TEMPER_EMBRITTLEMENT = "temper_embrittlement"
    LIQUID_METAL_EMBRITTLEMENT = "liquid_metal_embrittlement"
    CREEP = "creep"

    # Manufacturing defects
    MATERIAL_DEFECT = "material_defect"
    MANUFACTURING_DEFECT = "manufacturing_defect"
    ASSEMBLY_DAMAGE = "assembly_damage"

    # Unknown/Other
    UNKNOWN = "unknown"


@dataclass
class FailedPartReport:
    """Report of a failed part submitted for analysis"""
    part_id: str
    part_type: str
    part_specification: str
    manufacturer: Optional[str]
    supplier: Optional[str]
    application: str
    service_time_hours: Optional[float]
    service_time_cycles: Optional[int]
    operating_conditions: Dict[str, Any]
    failure_date: datetime
    failure_description: str
    reporter_id: str
    reporter_type: str  # "oem", "professional", "consumer", "verified_engineer"


@dataclass
class FailureEvidence:
    """Physical evidence collected from a failure"""
    fracture_location: str
    fracture_appearance: str
    surface_condition: str
    dimensional_changes: Optional[Dict[str, float]]
    photos: List[str]
    material_test_results: Optional[Dict[str, Any]]
    environmental_samples: Optional[Dict[str, Any]]
    additional_notes: Optional[str]


@dataclass
class FailureAnalysisResult:
    """Complete result of failure analysis"""
    failure_id: str
    failure_mode: FailureMode
    confidence: float
    root_cause: str
    evidence_interpretation: List[str]
    contributing_factors: List[str]
    recommendations: List[str]
    similar_failures_count: int
    prevention_measures: List[str]
    network_learning: str
    analysis_timestamp: datetime


class DetectiveAgent:
    """
    Agent_20: The Forensic Investigator

    Main orchestration class for all failure analysis capabilities.
    Coordinates between analysis, investigation, patterns, prediction,
    and documentation subsystems.
    """

    AGENT_ID = "AGENT_20"
    CODENAME = "DETECTIVE"

    def __init__(self):
        """Initialize the DETECTIVE agent with all subsystems."""
        self.failure_analyzer = None  # FailureAnalyzer()
        self.fracture_classifier = None  # FractureClassifier()
        self.life_calculator = None  # LifeCalculator()
        self.root_cause_investigator = None  # RootCauseInvestigator()
        self.pattern_detector = None  # FailurePatternDetector()
        self.failure_predictor = None  # FailurePredictor()
        self.failure_recorder = None  # FailureRecorder()
        self.failure_database = None  # FailureDatabase()

        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize all subsystems and connections."""
        # Import and initialize subsystems
        from .failure_analyzer import FailureAnalyzer
        from .fracture_classifier import FractureClassifier
        from .life_calculator import LifeCalculator
        from ..investigation.root_cause import RootCauseInvestigator
        from ..patterns.pattern_detector import FailurePatternDetector
        from ..prediction.failure_predictor import FailurePredictor
        from ..documentation.failure_recorder import FailureRecorder
        from ..knowledge.failure_database import FailureDatabase

        self.failure_analyzer = FailureAnalyzer()
        self.fracture_classifier = FractureClassifier()
        self.life_calculator = LifeCalculator()
        self.root_cause_investigator = RootCauseInvestigator()
        self.pattern_detector = FailurePatternDetector()
        self.failure_predictor = FailurePredictor()
        self.failure_recorder = FailureRecorder()
        self.failure_database = FailureDatabase()

        self._initialized = True
        return True

    async def analyze_failure(
        self,
        failed_part: FailedPartReport,
        evidence: FailureEvidence
    ) -> FailureAnalysisResult:
        """
        Perform comprehensive failure analysis.

        This is the main entry point for failure analysis. It:
        1. Classifies the failure mode from evidence
        2. Determines root cause using investigation methods
        3. Searches network for similar failures
        4. Generates prevention recommendations
        5. Documents the failure for collective learning

        Args:
            failed_part: Report describing the failed part and conditions
            evidence: Physical evidence from the failure

        Returns:
            Complete failure analysis result
        """
        failure_id = self._generate_failure_id()

        # Step 1: Classify fracture surface
        fracture_analysis = await self.fracture_classifier.classify(
            evidence.fracture_appearance,
            evidence.fracture_location,
            evidence.photos
        )

        # Step 2: Determine failure mode
        failure_mode = self._determine_failure_mode(
            fracture_analysis,
            failed_part.operating_conditions,
            evidence
        )

        # Step 3: Investigate root cause
        root_cause_result = await self.root_cause_investigator.investigate(
            failed_part,
            evidence,
            failure_mode
        )

        # Step 4: Find similar failures in network
        similar_failures = await self.pattern_detector.find_similar_failures(
            failed_part.part_type,
            failure_mode,
            failed_part.application
        )

        # Step 5: Generate recommendations
        recommendations = self._generate_recommendations(
            failure_mode,
            root_cause_result,
            similar_failures,
            failed_part.operating_conditions
        )

        # Step 6: Create analysis result
        result = FailureAnalysisResult(
            failure_id=failure_id,
            failure_mode=failure_mode,
            confidence=fracture_analysis.confidence,
            root_cause=root_cause_result.root_cause,
            evidence_interpretation=fracture_analysis.interpretations,
            contributing_factors=root_cause_result.contributing_factors,
            recommendations=recommendations,
            similar_failures_count=len(similar_failures),
            prevention_measures=root_cause_result.prevention_measures,
            network_learning=f"Pattern added to {failure_mode.value} prediction model",
            analysis_timestamp=datetime.utcnow()
        )

        # Step 7: Document for collective learning
        await self.failure_recorder.document(
            failed_part,
            evidence,
            result
        )

        return result

    async def predict_failure_risk(
        self,
        part_id: str,
        part_type: str,
        operating_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict failure risk for a part under given conditions.

        Uses ML models trained on network failure data.

        Args:
            part_id: Identifier for the part
            part_type: Type/category of part
            operating_conditions: Current or expected operating conditions

        Returns:
            Failure risk prediction with probabilities and recommendations
        """
        return await self.failure_predictor.predict(
            part_id,
            part_type,
            operating_conditions
        )

    async def find_similar_failures(
        self,
        part_type: str,
        failure_mode: str,
        application: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find similar failures reported in the UPC network.

        Args:
            part_type: Type of part that failed
            failure_mode: Mode of failure to match
            application: Optional application context for better matching

        Returns:
            List of similar failures with details and resolutions
        """
        return await self.pattern_detector.find_similar_failures(
            part_type,
            FailureMode(failure_mode) if isinstance(failure_mode, str) else failure_mode,
            application
        )

    async def detect_emerging_patterns(
        self,
        time_window_days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Detect emerging failure patterns that might indicate systemic issues.

        This is how we catch recalls before they happen.

        Args:
            time_window_days: Time window to analyze for patterns

        Returns:
            List of emerging patterns with severity and recommended actions
        """
        return await self.pattern_detector.detect_emerging_patterns(time_window_days)

    async def document_failure(
        self,
        failure_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Document a failure for the UPC network to learn from.

        This feeds back into collective consciousness.

        Args:
            failure_report: Complete failure report data

        Returns:
            Documentation confirmation with network impact
        """
        return await self.failure_recorder.document_from_dict(failure_report)

    async def generate_report(
        self,
        failure_id: str,
        format: str = "technical"
    ) -> str:
        """
        Generate human-readable failure analysis report.

        Args:
            failure_id: ID of the documented failure
            format: Report format (technical, summary, action, legal)

        Returns:
            Formatted report string
        """
        from ..documentation.report_generator import ReportGenerator
        generator = ReportGenerator()
        return await generator.generate(failure_id, format)

    def _generate_failure_id(self) -> str:
        """Generate unique failure ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        import random
        random_suffix = random.randint(1000, 9999)
        return f"FAIL-{timestamp}-{random_suffix}"

    def _determine_failure_mode(
        self,
        fracture_analysis,
        operating_conditions: Dict,
        evidence: FailureEvidence
    ) -> FailureMode:
        """Determine failure mode from analysis and evidence."""
        # Use fracture analysis primary mode
        mode_mapping = {
            "fatigue": FailureMode.HIGH_CYCLE_FATIGUE,
            "high_cycle_fatigue": FailureMode.HIGH_CYCLE_FATIGUE,
            "low_cycle_fatigue": FailureMode.LOW_CYCLE_FATIGUE,
            "thermal_fatigue": FailureMode.THERMAL_FATIGUE,
            "overload": FailureMode.TENSILE_OVERLOAD,
            "tensile_overload": FailureMode.TENSILE_OVERLOAD,
            "shear_overload": FailureMode.SHEAR_OVERLOAD,
            "brittle_fracture": FailureMode.HYDROGEN_EMBRITTLEMENT,
            "corrosion": FailureMode.UNIFORM_CORROSION,
            "pitting": FailureMode.PITTING_CORROSION,
            "galvanic": FailureMode.GALVANIC_CORROSION,
            "stress_corrosion": FailureMode.STRESS_CORROSION_CRACKING,
            "wear": FailureMode.ADHESIVE_WEAR,
            "hydrogen_embrittlement": FailureMode.HYDROGEN_EMBRITTLEMENT,
            "creep": FailureMode.CREEP,
        }

        primary_mode = getattr(fracture_analysis, 'primary_mode', 'unknown').lower()
        return mode_mapping.get(primary_mode, FailureMode.UNKNOWN)

    def _generate_recommendations(
        self,
        failure_mode: FailureMode,
        root_cause_result,
        similar_failures: List,
        operating_conditions: Dict
    ) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []

        # Add recommendations from root cause analysis
        if hasattr(root_cause_result, 'recommended_actions'):
            recommendations.extend(root_cause_result.recommended_actions)

        # Add mode-specific recommendations
        mode_recommendations = {
            FailureMode.HIGH_CYCLE_FATIGUE: [
                "Review preload specifications",
                "Consider vibration damping measures",
                "Evaluate stress concentration factors"
            ],
            FailureMode.HYDROGEN_EMBRITTLEMENT: [
                "Verify plating process includes bake cycle",
                "Consider alternative coatings (Geomet, mechanical zinc)",
                "Source from certified suppliers with HE testing"
            ],
            FailureMode.GALVANIC_CORROSION: [
                "Isolate dissimilar metals",
                "Use appropriate barrier materials",
                "Consider sacrificial anodes"
            ],
            FailureMode.ADHESIVE_WEAR: [
                "Review lubrication adequacy",
                "Consider surface treatments",
                "Evaluate material compatibility"
            ],
        }

        if failure_mode in mode_recommendations:
            for rec in mode_recommendations[failure_mode]:
                if rec not in recommendations:
                    recommendations.append(rec)

        # Add recommendations from similar failures
        for similar in similar_failures[:3]:  # Top 3 similar
            if 'resolution' in similar and similar['resolution']:
                resolution_rec = f"From similar case: {similar['resolution']}"
                if resolution_rec not in recommendations:
                    recommendations.append(resolution_rec)

        return recommendations[:10]  # Limit to top 10 recommendations
