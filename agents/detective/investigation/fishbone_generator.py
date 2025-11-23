"""
Fishbone (Ishikawa) Diagram Generator

Generates cause-and-effect diagrams for failure analysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class FishboneDiagram:
    """Fishbone diagram representation"""
    effect: str
    causes: Dict[str, List[str]]
    primary_cause: str
    diagram_text: str


class FishboneGenerator:
    """
    Generates Ishikawa (fishbone) diagrams for failure analysis.

    Standard categories (6M):
    - Man (People)
    - Machine (Equipment)
    - Material
    - Method (Process)
    - Measurement
    - Environment (Mother Nature)
    """

    STANDARD_CAUSES = {
        "Man": [
            "Training deficiency",
            "Procedure not followed",
            "Human error",
            "Fatigue",
            "Communication failure",
        ],
        "Machine": [
            "Equipment malfunction",
            "Worn tooling",
            "Calibration error",
            "Improper setup",
            "Inadequate maintenance",
        ],
        "Material": [
            "Out-of-spec material",
            "Material defect",
            "Wrong material used",
            "Contamination",
            "Material degradation",
        ],
        "Method": [
            "Inadequate procedure",
            "Wrong specification",
            "Process variation",
            "Design error",
            "Assembly error",
        ],
        "Measurement": [
            "Calibration error",
            "Wrong measurement method",
            "Inadequate inspection",
            "Measurement uncertainty",
            "Missing measurement",
        ],
        "Environment": [
            "Temperature extreme",
            "Humidity/Moisture",
            "Contamination",
            "Vibration",
            "Corrosive atmosphere",
        ],
    }

    # Failure-mode specific cause mapping
    FAILURE_MODE_CAUSES = {
        "high_cycle_fatigue": {
            "Method": ["Undertorque", "Missing thread locker", "Wrong torque sequence"],
            "Machine": ["Vibration", "Resonance condition", "Worn bearings"],
            "Material": ["Low fatigue strength", "Surface defects", "Inclusions"],
            "Man": ["Incorrect assembly", "Missed torque check"],
            "Measurement": ["No torque verification", "Wrong torque spec"],
            "Environment": ["Thermal cycling", "Corrosive environment"],
        },
        "hydrogen_embrittlement": {
            "Material": ["High-strength steel (>32 HRC)", "Susceptible microstructure"],
            "Method": ["No bake after plating", "Acid pickling", "Improper cleaning"],
            "Machine": ["Plating bath contamination", "Incorrect plating time"],
            "Man": ["Process deviation", "Training gap"],
            "Measurement": ["No hydrogen testing", "No bake verification"],
            "Environment": ["Hydrogen source", "Cathodic protection"],
        },
        "galvanic_corrosion": {
            "Material": ["Dissimilar metals", "Large potential difference"],
            "Method": ["No isolation specified", "Wrong fastener material"],
            "Machine": ["N/A"],
            "Man": ["Wrong part installed", "Barrier omitted"],
            "Measurement": ["No compatibility check", "No inspection"],
            "Environment": ["Electrolyte present", "High humidity", "Salt exposure"],
        },
    }

    def __init__(self):
        """Initialize the fishbone generator."""
        pass

    async def generate(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any
    ) -> FishboneDiagram:
        """
        Generate fishbone diagram for failure.

        Args:
            failed_part: Information about failed part
            evidence: Failure evidence
            failure_mode: Determined failure mode

        Returns:
            FishboneDiagram with causes and visualization
        """
        failure_mode_str = str(failure_mode.value if hasattr(failure_mode, 'value') else failure_mode)

        # Get failure-mode specific causes or use defaults
        causes = self.FAILURE_MODE_CAUSES.get(failure_mode_str, self.STANDARD_CAUSES)

        # Customize based on evidence if available
        causes = self._customize_causes(causes, failed_part, evidence)

        # Determine primary cause
        primary_cause = self._determine_primary_cause(causes, failure_mode_str)

        # Generate text diagram
        effect = f"{failure_mode_str} failure"
        diagram_text = self._generate_diagram_text(effect, causes)

        return FishboneDiagram(
            effect=effect,
            causes=causes,
            primary_cause=primary_cause,
            diagram_text=diagram_text
        )

    def _customize_causes(
        self,
        base_causes: Dict[str, List[str]],
        failed_part: Any,
        evidence: Any
    ) -> Dict[str, List[str]]:
        """Customize causes based on specific failure context."""
        causes = {k: list(v) for k, v in base_causes.items()}

        # Add part-specific causes if we have part info
        if hasattr(failed_part, 'operating_conditions'):
            conditions = failed_part.operating_conditions
            if conditions.get('vibration_level') == 'High':
                if 'Vibration' not in causes.get('Machine', []):
                    causes.setdefault('Machine', []).append('Vibration exposure')
            if conditions.get('temperature_c', 20) > 100:
                causes.setdefault('Environment', []).append('Elevated temperature')

        # Add evidence-based causes
        if hasattr(evidence, 'fracture_location'):
            location = evidence.fracture_location.lower()
            if 'thread' in location:
                causes.setdefault('Method', []).append('Thread root stress concentration')

        return causes

    def _determine_primary_cause(
        self,
        causes: Dict[str, List[str]],
        failure_mode: str
    ) -> str:
        """Determine the most likely primary cause."""
        # Mode-specific primary causes
        primary_map = {
            "high_cycle_fatigue": "Cyclic loading with inadequate preload",
            "hydrogen_embrittlement": "Hydrogen from plating not baked out",
            "galvanic_corrosion": "Dissimilar metals without isolation",
            "stress_corrosion_cracking": "Tensile stress in corrosive environment",
            "adhesive_wear": "Inadequate lubrication",
        }

        return primary_map.get(failure_mode, "Multiple contributing factors")

    def _generate_diagram_text(
        self,
        effect: str,
        causes: Dict[str, List[str]]
    ) -> str:
        """Generate ASCII text representation of fishbone diagram."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"FISHBONE DIAGRAM: {effect.upper()}")
        lines.append("=" * 70)
        lines.append("")

        # Top causes (Man, Machine, Material)
        top_categories = ["Man", "Machine", "Material"]
        bottom_categories = ["Method", "Measurement", "Environment"]

        # Draw top branches
        for category in top_categories:
            category_causes = causes.get(category, [])
            if category_causes:
                lines.append(f"  {category}")
                for cause in category_causes[:3]:  # Limit to 3 per category
                    lines.append(f"    |-- {cause}")
                lines.append(f"    \\")

        # Main spine
        lines.append("      \\                                          /")
        lines.append("       \\                                        /")
        lines.append(f"        \\======================================/---->[{effect}]")
        lines.append("       /                                        \\")
        lines.append("      /                                          \\")

        # Draw bottom branches
        for category in bottom_categories:
            category_causes = causes.get(category, [])
            if category_causes:
                lines.append(f"    /")
                for cause in category_causes[:3]:
                    lines.append(f"    |-- {cause}")
                lines.append(f"  {category}")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)
