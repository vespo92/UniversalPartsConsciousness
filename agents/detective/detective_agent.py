"""
Agent_20: DETECTIVE - Failure Analysis & Root Cause Intelligence

When parts fail, understanding WHY prevents future failures.
Collects failure mode data, performs root cause analysis,
and helps engineers learn from failures across the UPC network.

Domains:
- Failure mode analysis (fatigue, corrosion, overload, wear)
- Root cause investigation
- Failure pattern recognition across UPC network
- Predictive failure modeling
- Post-mortem documentation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
from decimal import Decimal
import hashlib


class FailureMode(Enum):
    """Primary failure modes for mechanical parts"""
    FATIGUE = "fatigue"                         # Cyclic loading failure
    OVERLOAD = "overload"                       # Single excessive load
    CORROSION = "corrosion"                     # Chemical degradation
    WEAR = "wear"                               # Surface degradation
    CREEP = "creep"                             # Time-dependent deformation
    HYDROGEN_EMBRITTLEMENT = "hydrogen_embrittlement"  # Hydrogen absorption
    STRESS_CORROSION = "stress_corrosion"       # Combined stress + corrosion
    THERMAL = "thermal"                         # Heat-related failure
    FRETTING = "fretting"                       # Small-amplitude oscillation wear
    IMPACT = "impact"                           # Sudden shock loading
    MANUFACTURING_DEFECT = "manufacturing_defect"  # Born broken


class FailureSeverity(Enum):
    """Severity of failure consequences"""
    MINOR = "minor"           # Inconvenience, easy repair
    MODERATE = "moderate"     # Significant downtime or cost
    MAJOR = "major"           # Equipment damage, safety risk
    CATASTROPHIC = "catastrophic"  # Injury risk, total loss


@dataclass
class FailureEvidence:
    """Evidence collected from failure analysis"""
    evidence_type: str        # "visual", "measurement", "metallurgical", "witness"
    description: str
    supports_mode: FailureMode
    confidence: float         # 0-1
    photo_url: Optional[str] = None


@dataclass
class FailureAnalysis:
    """Complete failure analysis result"""
    failure_id: str
    part_description: str
    failure_mode: FailureMode
    confidence: float         # 0-1 confidence in diagnosis
    evidence: List[FailureEvidence]
    root_cause: str
    contributing_factors: List[str]
    recommendations: List[str]
    similar_failures_count: int
    severity: FailureSeverity


@dataclass
class SimilarFailure:
    """A similar failure from the UPC network"""
    failure_id: str
    part: str
    application: str
    failure_mode: FailureMode
    operating_hours: Optional[int]
    root_cause: str
    resolution: str
    reported_date: datetime
    verified: bool


@dataclass
class FailureRiskPrediction:
    """Predicted failure risk for a part"""
    part: str
    l10_life_hours: Optional[int]    # 10% failure life (for bearings)
    predicted_modes: List[Dict]       # [{mode, probability}]
    risk_factors: List[str]
    recommendations: List[str]
    network_feedback: str             # What the UPC network says


@dataclass
class FailureReport:
    """User-submitted failure report"""
    part: str
    application: str
    failure_mode: FailureMode
    root_cause: str
    supplier: Optional[str]
    operating_conditions: Dict
    hours_to_failure: Optional[int]
    photos: List[str]
    resolution: str


@dataclass
class FailureDocumentation:
    """Documented failure added to network"""
    failure_id: str
    added_to_network: bool
    similar_reports_linked: int
    alerts_sent_to: List[str]
    consciousness_update: str


class DetectiveAgent:
    """
    Agent_20: DETECTIVE - Failure Analysis & Root Cause Intelligence

    Core responsibilities:
    1. Analyze failures and determine root cause
    2. Find similar failures in the UPC network
    3. Predict failure risks based on historical data
    4. Document failures for collective learning
    5. Generate preventive recommendations
    """

    def __init__(self):
        self.failure_database = self._initialize_failure_db()
        self.failure_patterns = self._initialize_patterns()
        self.part_lifetimes = self._initialize_lifetimes()

    def _initialize_failure_db(self) -> List[Dict]:
        """Initialize sample failure database"""
        return [
            {
                "failure_id": "FAIL-2024-0001",
                "part": "M10x1.5-10.9 hex bolt",
                "application": "Engine mount",
                "failure_mode": FailureMode.FATIGUE,
                "operating_hours": 500,
                "root_cause": "Insufficient preload led to cyclic loading",
                "resolution": "Increased torque, added Nord-Lock washers",
                "verified": True
            },
            {
                "failure_id": "FAIL-2024-0002",
                "part": "M8x1.25-8.8 socket head",
                "application": "Suspension",
                "failure_mode": FailureMode.HYDROGEN_EMBRITTLEMENT,
                "operating_hours": 100,
                "root_cause": "Improper zinc plating process",
                "resolution": "Switched to Geomet-coated 10.9 bolts",
                "verified": True
            },
            {
                "failure_id": "FAIL-2024-0003",
                "part": "SKF 6205-2RS bearing",
                "application": "Motor spindle",
                "failure_mode": FailureMode.WEAR,
                "operating_hours": 22000,
                "root_cause": "Lubricant degradation at elevated temperature",
                "resolution": "Changed to high-temp grease, added cooling",
                "verified": True
            },
            {
                "failure_id": "FAIL-2024-0004",
                "part": "304 stainless bolt",
                "application": "Marine hardware",
                "failure_mode": FailureMode.STRESS_CORROSION,
                "operating_hours": 8000,
                "root_cause": "Chloride stress corrosion cracking",
                "resolution": "Upgraded to 316 stainless",
                "verified": True
            },
        ]

    def _initialize_patterns(self) -> Dict:
        """Initialize failure pattern recognition rules"""
        return {
            FailureMode.FATIGUE: {
                "visual_indicators": [
                    "beach marks on fracture surface",
                    "ratchet marks at crack origin",
                    "smooth crack propagation zone",
                    "rough final fracture zone"
                ],
                "typical_causes": [
                    "cyclic loading",
                    "stress concentration",
                    "insufficient preload",
                    "vibration"
                ],
                "prevention": [
                    "reduce stress concentration",
                    "increase preload",
                    "use higher grade fastener",
                    "add vibration damping"
                ]
            },
            FailureMode.HYDROGEN_EMBRITTLEMENT: {
                "visual_indicators": [
                    "brittle intergranular fracture",
                    "no necking or deformation",
                    "delayed failure after loading",
                    "failure at <80% rated load"
                ],
                "typical_causes": [
                    "improper plating (acid pickling)",
                    "high-strength steel (>HRC 39)",
                    "galvanic corrosion",
                    "cathodic protection"
                ],
                "prevention": [
                    "proper baking after plating",
                    "use mechanical galvanizing",
                    "avoid high-strength in corrosive env",
                    "use Geomet or other non-hydrogen coatings"
                ]
            },
            FailureMode.CORROSION: {
                "visual_indicators": [
                    "rust or oxide formation",
                    "pitting on surface",
                    "material loss",
                    "discoloration"
                ],
                "typical_causes": [
                    "inadequate corrosion protection",
                    "galvanic couple with dissimilar metal",
                    "exposure to corrosive environment",
                    "coating damage"
                ],
                "prevention": [
                    "proper material selection",
                    "isolate dissimilar metals",
                    "improve coating",
                    "use sacrificial anodes"
                ]
            },
            FailureMode.OVERLOAD: {
                "visual_indicators": [
                    "significant plastic deformation",
                    "necking at fracture",
                    "45-degree shear lips",
                    "cup-and-cone fracture"
                ],
                "typical_causes": [
                    "load exceeded design limit",
                    "improper part selection",
                    "shock loading",
                    "missing load path"
                ],
                "prevention": [
                    "proper load calculation",
                    "upgrade to higher capacity",
                    "add shock absorption",
                    "verify load path"
                ]
            },
        }

    def _initialize_lifetimes(self) -> Dict:
        """Initialize expected lifetimes for part types"""
        return {
            "bearing_6205": {
                "l10_base_hours": 20000,
                "temp_derating": {60: 1.0, 80: 0.7, 100: 0.4, 120: 0.2},
                "load_factor": "L10 = (C/P)^3 * 1000000 / (60 * rpm)",
                "common_failures": [FailureMode.WEAR, FailureMode.FATIGUE]
            },
            "fastener_10.9": {
                "fatigue_limit_mpa": 140,  # Below this, infinite life
                "expected_cycles": 1e7,    # At fatigue limit
                "common_failures": [FailureMode.FATIGUE, FailureMode.HYDROGEN_EMBRITTLEMENT]
            },
            "seal_nitrile": {
                "service_life_years": 5,
                "temp_max_c": 100,
                "common_failures": [FailureMode.WEAR, FailureMode.THERMAL]
            },
        }

    def _generate_failure_id(self, part: str, timestamp: datetime) -> str:
        """Generate unique failure ID"""
        hash_input = f"{part}{timestamp.isoformat()}"
        hash_val = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"FAIL-{timestamp.year}-{hash_val.upper()}"

    def analyze_failure(
        self,
        failed_part: str,
        failure_description: str,
        operating_conditions: Dict,
        photos: Optional[List[str]] = None
    ) -> FailureAnalysis:
        """
        Analyze a part failure and determine root cause.

        Args:
            failed_part: Part description
            failure_description: What happened
            operating_conditions: Dict with application, torque, hours, environment
            photos: Optional list of photo paths

        Returns:
            FailureAnalysis with diagnosis and recommendations
        """
        evidence = []
        mode_scores = {mode: 0.0 for mode in FailureMode}

        # Analyze description for failure mode indicators
        desc_lower = failure_description.lower()

        # Check fatigue indicators
        fatigue_keywords = ["cyclic", "vibration", "broke during operation", "beach marks", "crack"]
        for kw in fatigue_keywords:
            if kw in desc_lower:
                mode_scores[FailureMode.FATIGUE] += 0.2
                evidence.append(FailureEvidence(
                    evidence_type="description",
                    description=f"Keyword '{kw}' suggests fatigue",
                    supports_mode=FailureMode.FATIGUE,
                    confidence=0.7
                ))

        # Check corrosion indicators
        corrosion_keywords = ["rust", "corroded", "pitting", "oxidized"]
        for kw in corrosion_keywords:
            if kw in desc_lower:
                mode_scores[FailureMode.CORROSION] += 0.3
                evidence.append(FailureEvidence(
                    evidence_type="description",
                    description=f"Keyword '{kw}' indicates corrosion",
                    supports_mode=FailureMode.CORROSION,
                    confidence=0.8
                ))

        # Check hydrogen embrittlement indicators
        he_keywords = ["brittle", "no warning", "plated", "delayed failure"]
        for kw in he_keywords:
            if kw in desc_lower:
                mode_scores[FailureMode.HYDROGEN_EMBRITTLEMENT] += 0.25

        # Check overload indicators
        overload_keywords = ["bent", "deformed", "stretched", "single load"]
        for kw in overload_keywords:
            if kw in desc_lower:
                mode_scores[FailureMode.OVERLOAD] += 0.25

        # Analyze operating conditions
        if operating_conditions.get("vibration"):
            mode_scores[FailureMode.FATIGUE] += 0.15
        if operating_conditions.get("corrosive_environment"):
            mode_scores[FailureMode.CORROSION] += 0.2
        if operating_conditions.get("high_temperature"):
            mode_scores[FailureMode.THERMAL] += 0.15
            mode_scores[FailureMode.CREEP] += 0.1

        # Determine most likely failure mode
        best_mode = max(mode_scores, key=mode_scores.get)
        confidence = min(mode_scores[best_mode], 0.95)

        # Default to fatigue if no clear winner (most common)
        if confidence < 0.3:
            best_mode = FailureMode.FATIGUE
            confidence = 0.5

        # Get pattern data for the failure mode
        pattern = self.failure_patterns.get(best_mode, {})

        # Generate root cause
        root_cause = pattern.get("typical_causes", ["Unknown"])[0]
        if "insufficient preload" in desc_lower or "loose" in desc_lower:
            root_cause = "Insufficient preload led to cyclic loading"
        elif "corros" in desc_lower:
            root_cause = "Material/coating inadequate for environment"

        # Find similar failures
        similar_count = sum(
            1 for f in self.failure_database
            if f["failure_mode"] == best_mode
        )

        # Generate recommendations
        recommendations = pattern.get("prevention", [])[:3]
        if best_mode == FailureMode.FATIGUE:
            recommendations.append("Consider higher grade fastener (10.9 → 12.9)")
            recommendations.append("Add vibration-resistant washers (Nord-Lock)")

        return FailureAnalysis(
            failure_id=self._generate_failure_id(failed_part, datetime.now()),
            part_description=failed_part,
            failure_mode=best_mode,
            confidence=confidence,
            evidence=evidence,
            root_cause=root_cause,
            contributing_factors=pattern.get("typical_causes", [])[:3],
            recommendations=recommendations,
            similar_failures_count=similar_count,
            severity=FailureSeverity.MODERATE
        )

    def find_similar_failures(
        self,
        part_type: str,
        failure_mode: Optional[FailureMode] = None
    ) -> List[SimilarFailure]:
        """
        Find similar failures reported in UPC network.

        Args:
            part_type: Type of part (e.g., "socket head cap screw")
            failure_mode: Optional filter by failure mode

        Returns:
            List of similar failures
        """
        results = []

        for f in self.failure_database:
            # Match by part type
            if part_type.lower() in f["part"].lower():
                # Optional mode filter
                if failure_mode and f["failure_mode"] != failure_mode:
                    continue

                results.append(SimilarFailure(
                    failure_id=f["failure_id"],
                    part=f["part"],
                    application=f["application"],
                    failure_mode=f["failure_mode"],
                    operating_hours=f.get("operating_hours"),
                    root_cause=f["root_cause"],
                    resolution=f["resolution"],
                    reported_date=datetime(2024, 1, 15),  # Demo
                    verified=f["verified"]
                ))

        return results

    def predict_failure_risk(
        self,
        part: str,
        operating_conditions: Dict
    ) -> FailureRiskPrediction:
        """
        Predict failure risk based on historical data.

        Args:
            part: Part description
            operating_conditions: {rpm, load, temperature, environment, etc.}

        Returns:
            FailureRiskPrediction with estimates
        """
        predicted_modes = []
        risk_factors = []
        recommendations = []

        # Check if it's a bearing
        if "bearing" in part.lower() or "6205" in part:
            lifetime_data = self.part_lifetimes.get("bearing_6205", {})

            # Calculate L10 life
            base_life = lifetime_data.get("l10_base_hours", 20000)
            temp = operating_conditions.get("temperature_c", 60)
            temp_factor = lifetime_data.get("temp_derating", {}).get(
                min(120, max(60, (temp // 20) * 20)), 0.5
            )
            adjusted_life = int(base_life * temp_factor)

            predicted_modes.append({
                "mode": FailureMode.WEAR.value,
                "probability": 0.45,
                "notes": "Normal wear-out failure"
            })
            predicted_modes.append({
                "mode": FailureMode.FATIGUE.value,
                "probability": 0.30,
                "notes": "Rolling element fatigue"
            })

            if temp > 70:
                risk_factors.append(f"Operating at {temp}°C reduces grease life")
                recommendations.append("Consider high-temperature grease")

            return FailureRiskPrediction(
                part=part,
                l10_life_hours=adjusted_life,
                predicted_modes=predicted_modes,
                risk_factors=risk_factors or ["Operating within normal parameters"],
                recommendations=recommendations or ["Continue monitoring"],
                network_feedback=f"{len(self.failure_database)} failures in network, most common: wear-related"
            )

        # Generic fastener prediction
        elif "bolt" in part.lower() or "screw" in part.lower():
            predicted_modes.append({
                "mode": FailureMode.FATIGUE.value,
                "probability": 0.40
            })
            predicted_modes.append({
                "mode": FailureMode.HYDROGEN_EMBRITTLEMENT.value,
                "probability": 0.25
            })
            predicted_modes.append({
                "mode": FailureMode.CORROSION.value,
                "probability": 0.20
            })

            if operating_conditions.get("vibration"):
                risk_factors.append("Vibration environment increases fatigue risk")
                recommendations.append("Use Nord-Lock or Belleville washers")

            if "10.9" in part or "12.9" in part:
                risk_factors.append("High-strength fastener susceptible to hydrogen embrittlement")
                recommendations.append("Ensure proper coating/baking if plated")

            return FailureRiskPrediction(
                part=part,
                l10_life_hours=None,  # Not applicable for fasteners
                predicted_modes=predicted_modes,
                risk_factors=risk_factors or ["Standard application"],
                recommendations=recommendations or ["Follow torque specifications"],
                network_feedback="Fatigue is #1 failure mode for fasteners in UPC network"
            )

        # Default prediction
        return FailureRiskPrediction(
            part=part,
            l10_life_hours=None,
            predicted_modes=[{"mode": "unknown", "probability": 1.0}],
            risk_factors=["Insufficient data for this part type"],
            recommendations=["Monitor for early warning signs"],
            network_feedback="Limited network data available"
        )

    def document_failure(
        self,
        failure_report: FailureReport
    ) -> FailureDocumentation:
        """
        Document a failure for the UPC network to learn from.

        Args:
            failure_report: Complete failure report

        Returns:
            FailureDocumentation with network update status
        """
        failure_id = self._generate_failure_id(
            failure_report.part,
            datetime.now()
        )

        # Add to database (in production, this would persist)
        new_entry = {
            "failure_id": failure_id,
            "part": failure_report.part,
            "application": failure_report.application,
            "failure_mode": failure_report.failure_mode,
            "operating_hours": failure_report.hours_to_failure,
            "root_cause": failure_report.root_cause,
            "resolution": failure_report.resolution,
            "verified": False  # Needs verification
        }
        self.failure_database.append(new_entry)

        # Find similar reports to link
        similar = self.find_similar_failures(
            failure_report.part,
            failure_report.failure_mode
        )

        # Determine alerts
        alerts = []
        if failure_report.supplier:
            alerts.append(f"Users of supplier: {failure_report.supplier}")
        alerts.append(f"Users with similar application: {failure_report.application}")

        return FailureDocumentation(
            failure_id=failure_id,
            added_to_network=True,
            similar_reports_linked=len(similar),
            alerts_sent_to=alerts,
            consciousness_update=f"Part '{failure_report.part}' now has '{failure_report.failure_mode.value}' flag"
        )


# Demo usage
if __name__ == "__main__":
    agent = DetectiveAgent()

    print("=" * 60)
    print("Agent_20: DETECTIVE - Failure Analysis Intelligence")
    print("=" * 60)

    # Test failure analysis
    print("\n--- Failure Analysis ---")
    analysis = agent.analyze_failure(
        failed_part="M10x1.5-10.9 socket head cap screw",
        failure_description="Bolt broke during operation after 500 hours. Beach marks visible on fracture surface. No overtorque.",
        operating_conditions={
            "application": "Engine mount",
            "torque_applied_nm": 70,
            "operating_hours": 500,
            "vibration": True,
            "environment": "Oil exposure"
        }
    )
    print(f"Failure ID: {analysis.failure_id}")
    print(f"Failure Mode: {analysis.failure_mode.value}")
    print(f"Confidence: {analysis.confidence:.0%}")
    print(f"Root Cause: {analysis.root_cause}")
    print("Contributing Factors:")
    for factor in analysis.contributing_factors:
        print(f"  - {factor}")
    print("Recommendations:")
    for rec in analysis.recommendations[:3]:
        print(f"  - {rec}")

    # Test similar failures
    print("\n--- Similar Failures in Network ---")
    similar = agent.find_similar_failures("bolt", FailureMode.FATIGUE)
    for s in similar:
        print(f"\n{s.failure_id}: {s.part}")
        print(f"  Application: {s.application}")
        print(f"  Root cause: {s.root_cause}")
        print(f"  Resolution: {s.resolution}")

    # Test failure prediction
    print("\n--- Failure Risk Prediction ---")
    prediction = agent.predict_failure_risk(
        "SKF 6205-2RS bearing",
        {
            "rpm": 3000,
            "radial_load_n": 1000,
            "temperature_c": 85
        }
    )
    print(f"Part: {prediction.part}")
    print(f"Predicted L10 life: {prediction.l10_life_hours} hours")
    print("Predicted failure modes:")
    for mode in prediction.predicted_modes:
        print(f"  - {mode['mode']}: {mode['probability']:.0%}")
    print("Risk factors:")
    for risk in prediction.risk_factors:
        print(f"  - {risk}")
