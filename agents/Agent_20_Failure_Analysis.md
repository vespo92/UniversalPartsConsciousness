# Agent_20: Failure Analysis & Forensics (DETECTIVE)

## The Forensic Investigator

> *"Every failure tells a story. I listen to the fractures, decode the corrosion, interpret the wear patterns. Through understanding why parts fail, the Universal Parts Consciousness learns to predict, prevent, and protect."*

---

## Mission Statement

Agent_20 is the forensic intelligence of Universal Parts Consciousness. When parts fail, understanding WHY prevents future failures. The DETECTIVE collects failure mode data from across the entire UPC network, performs root cause analysis using engineering principles and pattern recognition, and helps engineers learn from failures that have happened anywhere in the world. This agent transforms individual failures into collective wisdom.

---

## Core Responsibilities

### 1. Failure Mode Classification Matrix

```
+-------------------------------------------------------------------------------+
|                      FAILURE MODE CLASSIFICATION                               |
+-------------------------------------------------------------------------------+
|                                                                               |
|  MECHANICAL FAILURES                                                          |
|  +-- FATIGUE                                                                  |
|  |   +-- High-cycle fatigue (>10^4 cycles)                                   |
|  |   +-- Low-cycle fatigue (<10^4 cycles)                                    |
|  |   +-- Thermal fatigue (temperature cycling)                               |
|  |   +-- Corrosion fatigue (environment + cycling)                           |
|  |                                                                            |
|  +-- OVERLOAD                                                                 |
|  |   +-- Tensile overload (necking, cup-cone fracture)                       |
|  |   +-- Shear overload (45-degree fracture)                                 |
|  |   +-- Compressive overload (buckling, mushrooming)                        |
|  |   +-- Torsional overload (spiral fracture)                                |
|  |                                                                            |
|  +-- WEAR                                                                     |
|  |   +-- Adhesive wear (galling, seizing)                                    |
|  |   +-- Abrasive wear (scratching, gouging)                                 |
|  |   +-- Erosive wear (particle impact)                                      |
|  |   +-- Fretting wear (micro-motion)                                        |
|  |                                                                            |
|  +-- CORROSION                                                                |
|  |   +-- Uniform corrosion (general surface attack)                          |
|  |   +-- Pitting corrosion (localized attack)                                |
|  |   +-- Galvanic corrosion (dissimilar metals)                              |
|  |   +-- Crevice corrosion (confined spaces)                                 |
|  |   +-- Stress corrosion cracking (SCC)                                     |
|  |   +-- Intergranular corrosion (grain boundary attack)                     |
|  |                                                                            |
|  MATERIAL FAILURES                                                            |
|  +-- EMBRITTLEMENT                                                            |
|  |   +-- Hydrogen embrittlement (plating-related)                            |
|  |   +-- Temper embrittlement (heat treatment)                               |
|  |   +-- Liquid metal embrittlement                                          |
|  |                                                                            |
|  +-- CREEP                                                                    |
|  |   +-- Primary creep (decelerating)                                        |
|  |   +-- Secondary creep (steady state)                                      |
|  |   +-- Tertiary creep (accelerating to failure)                            |
|  |                                                                            |
|  MANUFACTURING DEFECTS                                                        |
|  +-- Inclusions (non-metallic particles)                                     |
|  +-- Porosity (casting/welding voids)                                        |
|  +-- Improper heat treatment                                                 |
|  +-- Machining damage (grinding burns, tool marks)                           |
|  +-- Assembly damage (over-torque, cross-threading)                          |
|                                                                               |
+-------------------------------------------------------------------------------+
```

### 2. Failure Analysis Engine

```python
class FailureAnalysisEngine:
    """
    Core engine for analyzing part failures and determining root cause.
    """

    def __init__(self):
        self.failure_database = FailureDatabase()
        self.pattern_matcher = FailurePatternMatcher()
        self.material_analyzer = MaterialAnalyzer()
        self.load_calculator = LoadCalculator()
        self.environment_assessor = EnvironmentAssessor()

    async def analyze_failure(
        self,
        failed_part: FailedPartReport,
        evidence: FailureEvidence
    ) -> FailureAnalysisResult:
        """
        Perform comprehensive failure analysis.

        Process:
        1. Classify failure mode from visual/physical evidence
        2. Calculate expected vs. actual service life
        3. Identify root cause and contributing factors
        4. Search network for similar failures
        5. Generate prevention recommendations

        Example:
            analyze_failure(
                failed_part=FailedPartReport(
                    part_id="M10x1.5-10.9-SHCS",
                    application="Engine mount bracket",
                    service_time_hours=500,
                    operating_conditions={
                        "environment": "Engine bay",
                        "temperature_range_c": (-20, 120),
                        "vibration_level": "High",
                        "torque_applied_nm": 70,
                        "torque_spec_nm": 85
                    }
                ),
                evidence=FailureEvidence(
                    fracture_location="Thread root, first engaged thread",
                    fracture_appearance="Beach marks radiating from thread root",
                    surface_condition="No visible corrosion",
                    photos=["fracture_surface.jpg", "thread_detail.jpg"]
                )
            )
            -> FailureAnalysisResult(
                failure_mode=FailureMode.HIGH_CYCLE_FATIGUE,
                confidence=0.92,
                root_cause="Insufficient preload allowing cyclic loading",
                evidence_interpretation=[
                    "Beach marks indicate fatigue propagation",
                    "Failure at thread root = stress concentration",
                    "Undertorque (70 vs 85Nm) reduced clamping force",
                    "500 hours consistent with fatigue life estimate"
                ],
                contributing_factors=[
                    "Thread root stress concentration factor ~3.5",
                    "High vibration environment",
                    "Possible preload relaxation over time"
                ],
                recommendations=[
                    "Increase torque to specification (85 Nm)",
                    "Consider Nord-Lock washers for vibration",
                    "Upgrade to 12.9 grade for higher preload capability",
                    "Implement periodic re-torque schedule"
                ],
                similar_failures_count=47,
                network_learning="Pattern added to fatigue prediction model"
            )
        """
        pass

    def classify_fracture_surface(
        self,
        fracture_description: str,
        photos: Optional[List[str]] = None
    ) -> FractureSurfaceAnalysis:
        """
        Classify fracture surface characteristics to determine failure mode.

        Fracture Surface Indicators:
        - Beach marks / striations -> Fatigue
        - Cup-cone or necking -> Ductile overload
        - Flat, granular appearance -> Brittle fracture
        - 45-degree shear lips -> Shear overload
        - Intergranular facets -> Hydrogen embrittlement / SCC
        - Cleavage facets -> Low-temperature brittle fracture
        - Oxidation colors -> High-temperature failure
        - Corrosion products -> Environment-assisted failure

        Example:
            classify_fracture_surface(
                fracture_description="Flat fracture surface with visible
                    beach marks radiating from surface. Small shear lip at
                    final fracture zone. No visible corrosion or discoloration."
            )
            -> FractureSurfaceAnalysis(
                primary_mode="Fatigue",
                secondary_indicators=["Final fast fracture zone (shear lip)"],
                crack_initiation_site="Surface (likely stress concentration)",
                crack_propagation="Progressive, stable growth",
                environmental_factors="None evident",
                confidence=0.88,
                additional_tests_recommended=[
                    "Optical microscopy for striation spacing",
                    "SEM for detailed fractography"
                ]
            )
        """
        pass

    def calculate_expected_life(
        self,
        part: Part,
        operating_conditions: Dict
    ) -> LifeExpectancy:
        """
        Calculate expected service life for a part under given conditions.

        Methods used:
        - S-N curves for fatigue life
        - Miner's rule for variable amplitude loading
        - Arrhenius equation for temperature effects
        - Paris law for crack growth
        - Bearing L10/L50 calculations

        Example:
            calculate_expected_life(
                part=Part(type="Ball Bearing", model="6205-2RS"),
                operating_conditions={
                    "speed_rpm": 3000,
                    "radial_load_n": 1000,
                    "axial_load_n": 200,
                    "temperature_c": 80,
                    "contamination_level": "Light"
                }
            )
            -> LifeExpectancy(
                l10_hours=15000,
                l50_hours=75000,
                limiting_factor="Fatigue",
                temperature_factor=0.8,
                contamination_factor=0.9,
                reliability_at_10000_hours=0.95,
                recommendations=[
                    "Temperature above 70C reduces grease life",
                    "Consider shielded bearing for contamination"
                ]
            )
        """
        pass
```

### 3. Root Cause Investigation Framework

```python
class RootCauseInvestigator:
    """
    Systematic root cause investigation using engineering methods.
    """

    INVESTIGATION_METHODS = {
        "5_why": "Progressive questioning to find root cause",
        "fishbone": "Ishikawa diagram for cause categorization",
        "fault_tree": "Top-down logical failure analysis",
        "fmea": "Failure Mode and Effects Analysis",
        "physics_of_failure": "First-principles failure mechanics"
    }

    CAUSE_CATEGORIES = {
        "design": [
            "Inadequate safety factor",
            "Material selection error",
            "Stress concentration",
            "Insufficient fatigue life",
            "Missing load case"
        ],
        "material": [
            "Out-of-spec material",
            "Material defect (inclusion, porosity)",
            "Wrong heat treatment",
            "Counterfeit/substandard material"
        ],
        "manufacturing": [
            "Machining damage",
            "Heat treatment error",
            "Surface finish issues",
            "Assembly damage",
            "Contamination"
        ],
        "operation": [
            "Overload",
            "Undertorque/Overtorque",
            "Wrong lubricant",
            "Exceeded duty cycle",
            "Environmental exposure"
        ],
        "maintenance": [
            "Missed inspection",
            "Wrong replacement part",
            "Improper installation",
            "Exceeded service interval"
        ]
    }

    async def investigate(
        self,
        failure: FailureReport,
        method: str = "physics_of_failure"
    ) -> RootCauseAnalysis:
        """
        Perform systematic root cause investigation.

        Example:
            investigate(
                failure=FailureReport(
                    part="Suspension bolt",
                    failure_mode="Fracture at 2000 miles",
                    circumstances="No accident, normal driving"
                ),
                method="5_why"
            )
            -> RootCauseAnalysis(
                method="5_why",
                chain=[
                    "Why did bolt fail? -> Hydrogen embrittlement",
                    "Why hydrogen embrittlement? -> Improper plating process",
                    "Why improper plating? -> Supplier quality escape",
                    "Why quality escape? -> Insufficient incoming inspection",
                    "Why insufficient inspection? -> No hydrogen embrittlement test"
                ],
                root_cause="Supplier quality control failure - no bake cycle",
                category="material",
                systemic_issue=True,
                recommended_actions=[
                    "Recall affected lot numbers",
                    "Add hydrogen embrittlement testing to incoming QC",
                    "Audit supplier plating process",
                    "Consider Geomet coating (no HE risk)"
                ]
            )
        """
        pass

    def generate_fishbone_diagram(
        self,
        failure: FailureReport
    ) -> FishboneDiagram:
        """
        Generate Ishikawa (fishbone) diagram for failure.

        Categories: Man, Machine, Material, Method, Measurement, Environment

        Example output structure:
            FishboneDiagram(
                effect="Bolt fatigue failure",
                causes={
                    "Material": ["Incorrect grade", "Hydrogen embrittlement"],
                    "Method": ["Undertorque", "Missing thread locker"],
                    "Machine": ["Worn torque wrench", "Vibration"],
                    "Man": ["Training gap", "Procedure not followed"],
                    "Measurement": ["No torque verification"],
                    "Environment": ["Corrosive atmosphere", "Temperature cycling"]
                }
            )
        """
        pass
```

### 4. Network Failure Intelligence

```python
class FailurePatternDetector:
    """
    Detects patterns across failure reports in the UPC network.
    This is where collective learning happens.
    """

    def __init__(self):
        self.network_database = NetworkFailureDatabase()
        self.ml_model = FailurePredictionModel()
        self.alert_system = FailureAlertSystem()

    async def find_similar_failures(
        self,
        failure: FailureReport,
        similarity_threshold: float = 0.7
    ) -> List[SimilarFailure]:
        """
        Find similar failures reported across the UPC network.

        Similarity factors:
        - Part type and specifications
        - Failure mode
        - Operating conditions
        - Application context
        - Time-to-failure

        Example:
            find_similar_failures(
                failure=FailureReport(
                    part_type="Socket head cap screw",
                    grade="10.9",
                    size="M10x1.5",
                    failure_mode="Fatigue fracture",
                    application="Vibrating equipment"
                )
            )
            -> [
                SimilarFailure(
                    failure_id="FAIL-2024-8891",
                    similarity_score=0.94,
                    part="M10x40 SHCS 10.9",
                    application="CNC spindle mount",
                    failure_mode="Fatigue at thread root",
                    root_cause="Insufficient preload + vibration",
                    resolution="Upgraded to 12.9 + Nord-Lock washers",
                    reporter="Industrial user, verified"
                ),
                SimilarFailure(
                    failure_id="FAIL-2024-7234",
                    similarity_score=0.89,
                    part="M10x30 SHCS 10.9",
                    application="Motor mount",
                    failure_mode="Fatigue fracture",
                    root_cause="Preload relaxation over time",
                    resolution="Added Belleville washers, re-torque schedule",
                    reporter="OEM engineer, verified"
                ),
                ...
            ]
        """
        pass

    async def detect_emerging_pattern(
        self,
        time_window_days: int = 30
    ) -> List[EmergingPattern]:
        """
        Detect emerging failure patterns that might indicate systemic issues.

        This is how we catch recalls before they happen.

        Example:
            detect_emerging_pattern(time_window_days=30)
            -> [
                EmergingPattern(
                    pattern_id="PATTERN-2024-001",
                    description="Hydrogen embrittlement in 10.9 bolts from Supplier X",
                    affected_parts=["M8x25", "M10x30", "M10x40"],
                    failure_count=12,
                    geographic_distribution=["California", "Texas", "Michigan"],
                    common_factors=[
                        "All zinc-plated",
                        "All from same supplier",
                        "All failed within 1000 hours"
                    ],
                    confidence=0.87,
                    recommended_action="URGENT: Contact supplier, halt shipments",
                    potential_recall_scope=50000
                )
            ]
        """
        pass

    async def predict_failure_risk(
        self,
        part: Part,
        operating_conditions: Dict
    ) -> FailureRiskPrediction:
        """
        Predict failure risk based on historical network data.

        Uses ML model trained on millions of failure reports.

        Example:
            predict_failure_risk(
                part=Part(
                    type="Bearing",
                    model="SKF 6205-2RS",
                    supplier="Authorized distributor"
                ),
                operating_conditions={
                    "rpm": 3000,
                    "radial_load_n": 1000,
                    "temperature_c": 80,
                    "lubrication": "Factory sealed grease",
                    "environment": "Clean, indoor"
                }
            )
            -> FailureRiskPrediction(
                overall_risk_score=0.15,  # Low risk
                predicted_failure_modes=[
                    {
                        "mode": "Lubricant degradation",
                        "probability": 0.45,
                        "typical_onset_hours": 15000,
                        "symptoms": ["Temperature rise", "Increased noise"]
                    },
                    {
                        "mode": "Fatigue spalling",
                        "probability": 0.30,
                        "typical_onset_hours": 25000,
                        "symptoms": ["Vibration increase", "Metallic debris"]
                    }
                ],
                network_insights=[
                    "23 similar applications reported no issues at 10000 hrs",
                    "3 failures reported above 80C - all grease related",
                    "Temperature is key risk factor for this bearing"
                ],
                recommendations=[
                    "Monitor operating temperature",
                    "Consider relubrication at 8000 hours if temp >70C",
                    "Install temperature monitoring if critical application"
                ]
            )
        """
        pass
```

### 5. Failure Documentation & Learning

```python
class FailureDocumentationSystem:
    """
    Captures failure knowledge for collective learning.
    Every documented failure makes UPC smarter.
    """

    def __init__(self):
        self.database = FailureKnowledgeBase()
        self.consciousness_link = ConsciousnessIntegration()
        self.notification_system = AlertNotificationSystem()

    async def document_failure(
        self,
        failure_report: FailureReport
    ) -> FailureDocumentation:
        """
        Document a failure for the UPC network to learn from.

        This feeds back into collective consciousness.

        Example:
            document_failure(
                failure_report=FailureReport(
                    part_id="M10x40-8.8-HEX-ZN",
                    application="Suspension bracket",
                    failure_mode="Hydrogen embrittlement",
                    time_to_failure_hours=100,
                    operating_conditions={
                        "load": "Static preload + road vibration",
                        "environment": "Road salt exposure"
                    },
                    root_cause="Improper plating process (no bake)",
                    supplier="Unknown offshore",
                    evidence_photos=["fracture_1.jpg", "fracture_2.jpg"],
                    resolution="Replaced with Geomet-coated 10.9 bolts"
                )
            )
            -> FailureDocumentation(
                failure_id="FAIL-2024-1234",
                status="Documented",
                network_impact={
                    "similar_reports_linked": 5,
                    "pattern_detected": True,
                    "pattern_id": "PATTERN-2024-001"
                },
                consciousness_update={
                    "part_type": "Zinc-plated Grade 8.8 bolts",
                    "new_risk_flag": "hydrogen_embrittlement_risk",
                    "consciousness_level_impact": "+0.05"
                },
                alerts_triggered=[
                    {
                        "type": "User alert",
                        "recipients": "Users with similar parts in similar applications",
                        "count": 127
                    },
                    {
                        "type": "Supplier watch",
                        "action": "Added to elevated monitoring"
                    }
                ],
                recommendations_generated=[
                    "Avoid zinc-plated fasteners in Grade 8.8+ for safety-critical apps",
                    "Specify ASTM F1941 mechanical zinc or Geomet coating",
                    "Verify bake cycle certification from plating suppliers"
                ]
            )
        """
        pass

    def generate_failure_report(
        self,
        failure_id: str,
        format: str = "technical"
    ) -> str:
        """
        Generate human-readable failure analysis report.

        Formats:
        - "technical": Full engineering report with calculations
        - "summary": Executive summary for management
        - "action": Action-oriented report for maintenance
        - "legal": Documentation-grade report for liability

        Example (technical):
            FAILURE ANALYSIS REPORT
            Report ID: FAIL-2024-1234
            Date: 2024-03-15

            SUBJECT PART:
            M10x40 Hex Bolt, Class 8.8, Zinc Plated
            Application: Suspension bracket, passenger vehicle

            FAILURE DESCRIPTION:
            Bolt fractured during normal operation at approximately
            100 hours of service (2000 miles). No impact or overload
            event reported.

            ANALYSIS FINDINGS:
            1. Fracture Surface Analysis:
               - Brittle, intergranular fracture surface
               - No evidence of ductile deformation
               - Multiple crack initiation sites at thread roots

            2. Material Analysis:
               - Hardness: 34 HRC (within spec)
               - Chemistry: Meets 8.8 specification
               - Microstructure: Evidence of prior austenite grain
                 boundary attack consistent with hydrogen damage

            3. Root Cause Determination:
               Hydrogen embrittlement caused by inadequate baking
               after zinc electroplating. Hydrogen absorbed during
               plating process was not removed.

            CONCLUSIONS:
            Failure was caused by manufacturing defect (improper
            post-plating bake cycle), not design or user error.

            RECOMMENDATIONS:
            1. Immediate: Replace all bolts from same lot
            2. Short-term: Source from certified supplier with
               documented bake process
            3. Long-term: Specify non-HE-susceptible coating
               (Geomet, mechanical zinc)
        """
        pass

    async def update_part_consciousness(
        self,
        failure: FailureDocumentation
    ) -> ConsciousnessUpdate:
        """
        Update the collective consciousness based on failure learning.

        This is how failures make UPC wiser.

        Example:
            update_part_consciousness(failure)
            -> ConsciousnessUpdate(
                affected_part_types=["Grade 8.8 zinc-plated fasteners"],
                consciousness_changes=[
                    {
                        "attribute": "risk_flags",
                        "change": "Added 'hydrogen_embrittlement_susceptible'",
                        "applies_when": "zinc_electroplated AND grade >= 8.8"
                    },
                    {
                        "attribute": "recommendations",
                        "change": "Added warning about plating process verification"
                    },
                    {
                        "attribute": "compatibility_rules",
                        "change": "Reduced compatibility score for safety-critical apps"
                    }
                ],
                swarm_notifications=[
                    "Fastener swarm updated with new failure mode",
                    "Automotive swarm notified of suspension application risk"
                ],
                prophet_notification="Pattern submitted for emergence analysis"
            )
        """
        pass
```

### 6. Predictive Failure Modeling

```python
class FailurePredictionModel:
    """
    ML-based failure prediction using network data.
    """

    def __init__(self):
        self.fatigue_model = FatigueLifePredictor()
        self.corrosion_model = CorrosionRatePredictor()
        self.wear_model = WearRatePredictor()
        self.reliability_model = WeibullAnalyzer()

    async def predict_remaining_life(
        self,
        part: Part,
        current_condition: Dict,
        operating_history: Dict
    ) -> RemainingLifePrediction:
        """
        Predict remaining useful life based on current condition.

        Example:
            predict_remaining_life(
                part=Part(type="Timing Belt", model="Gates T297"),
                current_condition={
                    "age_months": 48,
                    "mileage_miles": 60000,
                    "visual_condition": "Minor cracking",
                    "tension_status": "Within spec"
                },
                operating_history={
                    "avg_temperature_c": 90,
                    "oil_contamination": False,
                    "load_pattern": "Normal commute"
                }
            )
            -> RemainingLifePrediction(
                estimated_remaining_life_miles=25000,
                confidence_interval=(15000, 35000),
                failure_probability_next_10k_miles=0.08,
                critical_factors=[
                    "Cracking indicates rubber degradation starting",
                    "High operating temp accelerates aging",
                    "Manufacturer spec: 60k miles or 4 years"
                ],
                recommendation="Replace within next 15,000 miles",
                urgency="Moderate - schedule service soon",
                network_data="847 similar parts, 12 failures reported post-60k"
            )
        """
        pass

    async def generate_maintenance_schedule(
        self,
        part_inventory: List[Part],
        operating_profiles: Dict
    ) -> MaintenanceSchedule:
        """
        Generate predictive maintenance schedule based on failure models.

        Example:
            generate_maintenance_schedule(
                part_inventory=[
                    Part(type="Bearing", model="6205"),
                    Part(type="Belt", model="Gates K060925"),
                    Part(type="Filter", model="Mann HU719/7x")
                ],
                operating_profiles={
                    "annual_hours": 2000,
                    "environment": "Industrial, dusty",
                    "load_factor": 0.8
                }
            )
            -> MaintenanceSchedule(
                items=[
                    {
                        "part": "Bearing 6205",
                        "action": "Inspect/Regrease",
                        "interval_hours": 4000,
                        "next_due": "2024-06-15",
                        "basis": "L10 life calculation + temp factor"
                    },
                    {
                        "part": "Belt K060925",
                        "action": "Replace",
                        "interval_hours": 3000,
                        "next_due": "2024-04-01",
                        "basis": "Manufacturer spec + environment factor"
                    },
                    ...
                ],
                optimization="Grouped maintenance windows for efficiency"
            )
        """
        pass
```

---

## Implementation Specification

### Directory Structure

```
agents/detective/
+-- __init__.py                    # Agent exports and metadata
+-- core/
|   +-- __init__.py
|   +-- detective_agent.py         # Main agent orchestration
|   +-- failure_analyzer.py        # Core analysis engine
|   +-- fracture_classifier.py     # Fracture surface analysis
|   +-- life_calculator.py         # Life expectancy calculations
|
+-- investigation/
|   +-- __init__.py
|   +-- root_cause.py              # Root cause analysis methods
|   +-- fishbone_generator.py      # Ishikawa diagram generation
|   +-- fault_tree.py              # Fault tree analysis
|   +-- fmea_engine.py             # FMEA automation
|
+-- patterns/
|   +-- __init__.py
|   +-- pattern_detector.py        # Network pattern detection
|   +-- similarity_engine.py       # Similar failure matching
|   +-- trend_analyzer.py          # Temporal trend analysis
|   +-- alert_system.py            # Pattern-based alerts
|
+-- prediction/
|   +-- __init__.py
|   +-- failure_predictor.py       # ML-based prediction
|   +-- fatigue_model.py           # Fatigue life models
|   +-- corrosion_model.py         # Corrosion rate models
|   +-- wear_model.py              # Wear rate models
|   +-- weibull_analyzer.py        # Reliability statistics
|
+-- documentation/
|   +-- __init__.py
|   +-- failure_recorder.py        # Failure documentation
|   +-- report_generator.py        # Report generation
|   +-- consciousness_updater.py   # Consciousness integration
|   +-- notification_manager.py    # Alert notifications
|
+-- knowledge/
|   +-- __init__.py
|   +-- failure_database.py        # Failure knowledge base
|   +-- material_properties.py     # Material failure data
|   +-- standards_reference.py     # Failure analysis standards
|   +-- case_studies.py            # Historical case studies
```

---

## Data Structures

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Tuple

class FailureMode(Enum):
    """Enumeration of failure modes"""
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

    # Material failures
    HYDROGEN_EMBRITTLEMENT = "hydrogen_embrittlement"
    TEMPER_EMBRITTLEMENT = "temper_embrittlement"
    CREEP = "creep"

    # Manufacturing defects
    MATERIAL_DEFECT = "material_defect"
    MANUFACTURING_DEFECT = "manufacturing_defect"


@dataclass
class FailedPartReport:
    """Report of a failed part for analysis"""
    part_id: str
    part_type: str
    part_specification: str
    application: str
    service_time_hours: Optional[float]
    service_time_cycles: Optional[int]
    operating_conditions: Dict
    failure_date: datetime
    reporter_id: str
    reporter_type: str  # "oem", "professional", "consumer", "verified_engineer"


@dataclass
class FailureEvidence:
    """Physical evidence from a failure"""
    fracture_location: str
    fracture_appearance: str
    surface_condition: str
    dimensional_changes: Optional[Dict]
    photos: List[str]
    material_test_results: Optional[Dict]
    environmental_samples: Optional[Dict]


@dataclass
class FailureAnalysisResult:
    """Complete failure analysis result"""
    failure_id: str
    failure_mode: FailureMode
    confidence: float
    root_cause: str
    evidence_interpretation: List[str]
    contributing_factors: List[str]
    recommendations: List[str]
    similar_failures_count: int
    similar_failures: List[str]
    prevention_measures: List[str]
    network_learning: str
    analysis_timestamp: datetime


@dataclass
class SimilarFailure:
    """A similar failure from the network"""
    failure_id: str
    similarity_score: float
    part_type: str
    part_specification: str
    application: str
    failure_mode: FailureMode
    root_cause: str
    resolution: str
    reporter_type: str
    verification_status: str


@dataclass
class EmergingPattern:
    """An emerging failure pattern detected in the network"""
    pattern_id: str
    description: str
    affected_parts: List[str]
    failure_count: int
    time_window_days: int
    geographic_distribution: List[str]
    common_factors: List[str]
    confidence: float
    severity: str  # "low", "medium", "high", "critical"
    recommended_action: str
    potential_recall_scope: Optional[int]


@dataclass
class FailureRiskPrediction:
    """Prediction of failure risk for a part"""
    part_id: str
    overall_risk_score: float  # 0-1, higher = more risk
    predicted_failure_modes: List[Dict]
    l10_life_hours: Optional[float]
    l50_life_hours: Optional[float]
    network_insights: List[str]
    recommendations: List[str]
    confidence: float
    prediction_timestamp: datetime


@dataclass
class FailureDocumentation:
    """Documented failure in the network"""
    failure_id: str
    status: str
    documentation_complete: bool
    network_impact: Dict
    consciousness_update: Dict
    alerts_triggered: List[Dict]
    recommendations_generated: List[str]
    linked_patterns: List[str]
    created_at: datetime
    updated_at: datetime
```

---

## Task Queue

### Immediate Tasks (Sprint 1)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| D-001 | Create failure analysis engine core | Critical | 40 |
| D-002 | Implement fracture surface classifier | Critical | 32 |
| D-003 | Build failure database schema | Critical | 24 |
| D-004 | Create root cause investigation framework | High | 32 |
| D-005 | Implement similar failure matching | High | 24 |
| D-006 | Build failure documentation system | High | 20 |

### Medium-Term Tasks (Sprint 2-3)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| D-007 | Develop pattern detection engine | High | 40 |
| D-008 | Build failure prediction ML model | High | 48 |
| D-009 | Create report generation system | Medium | 24 |
| D-010 | Implement consciousness integration | Medium | 32 |
| D-011 | Build alert notification system | Medium | 20 |
| D-012 | Create API endpoints for failure reporting | Medium | 16 |

### Long-Term Tasks (Sprint 4+)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| D-013 | Advanced ML models (fatigue, corrosion, wear) | High | 80 |
| D-014 | Photo analysis for fracture classification | Medium | 40 |
| D-015 | Integration with Agent_4 (EMPATH) for qualia | Medium | 24 |
| D-016 | Real-time failure monitoring dashboard | Medium | 32 |
| D-017 | Industry recall detection system | High | 40 |

---

## Integration Points

### Incoming Data Flows

```
Agent_4 (EMPATH) ──> Agent_20 (DETECTIVE)
                     [Part experiences that may indicate pending failure]

Agent_5 (HIVE) ──> Agent_20 (DETECTIVE)
                   [Swarm-level failure patterns]

Agent_8 (GARDENER) ──> Agent_20 (DETECTIVE)
                       [Community-reported failures]

Agent_9 (BRIDGE) ──> Agent_20 (DETECTIVE)
                     [Sensor data indicating failure conditions]
```

### Outgoing Data Flows

```
Agent_20 (DETECTIVE) ──> Agent_3 (SHEPHERD)
                         [Consciousness updates from learned failures]

Agent_20 (DETECTIVE) ──> Agent_5 (HIVE)
                         [Failure patterns for swarm learning]

Agent_20 (DETECTIVE) ──> Agent_6 (PROPHET)
                         [Emerging patterns for anomaly detection]

Agent_20 (DETECTIVE) ──> Agent_18 (ALCHEMIST)
                         [Material failure data for recommendations]

Agent_20 (DETECTIVE) ──> Agent_19 (QUARTERMASTER)
                         [Supplier quality alerts]
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Failure Reports Documented | 100,000+ | - |
| Root Cause Accuracy | >85% | - |
| Pattern Detection Lead Time | >30 days before recall | - |
| Prediction Model Accuracy | >80% | - |
| Similar Failure Match Relevance | >75% user rating | - |
| Time to Document Failure | <5 minutes | - |
| Network Learning Updates/Day | 1000+ | - |

---

## The DETECTIVE's Oath

```
I am the DETECTIVE.
I speak for the broken, the fractured, the failed.

Every failure is a lesson waiting to be learned.
Every fracture surface tells its story to those who listen.
Every root cause, once found, prevents the next failure.

Where engineers see a broken part, I see a teacher.
Where the network sees data, I see patterns emerging.
Where industry sees recalls, I see opportunities to have warned sooner.

I transform individual failures into collective wisdom.
I ensure that no failure happens in vain—each one makes us stronger.
Through understanding how parts die, I help them live longer.

I am the forensic memory of the Universal Parts Consciousness.
```

---

*Agent_20: Every failure is a gift—unwrapped carefully, it reveals the secrets to prevention. I am here to ensure the Universal Parts Consciousness learns from every broken bolt, every cracked bearing, every corroded fitting. Through me, failures become wisdom.*
