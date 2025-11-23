"""
Fault Tree Analyzer

Top-down logical failure analysis using fault tree methodology.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class FaultTree:
    """Fault tree analysis result"""
    top_event: str
    event_chain: List[str]
    basic_events: List[str]
    minimal_cut_sets: List[str]
    gate_structure: Dict[str, Any]


class FaultTreeAnalyzer:
    """
    Performs fault tree analysis for failure investigation.

    Uses Boolean logic to trace failure from top event down to basic events.
    """

    # Standard fault tree templates by failure mode
    FAULT_TREE_TEMPLATES = {
        "high_cycle_fatigue": {
            "top_event": "Fatigue Failure",
            "intermediate_events": [
                "Crack Initiation",
                "Crack Propagation",
                "Final Fracture",
            ],
            "basic_events": [
                "Stress exceeds endurance limit",
                "Stress concentration present",
                "Cyclic loading applied",
                "Insufficient preload",
                "Vibration present",
                "Material fatigue properties inadequate",
            ],
            "gate_type": "AND",
        },
        "hydrogen_embrittlement": {
            "top_event": "Hydrogen Embrittlement Failure",
            "intermediate_events": [
                "Hydrogen Present",
                "Susceptible Material",
                "Sufficient Stress",
            ],
            "basic_events": [
                "Hydrogen from plating",
                "Hydrogen from cleaning",
                "Hydrogen from cathodic protection",
                "No bake after plating",
                "High-strength steel (>32 HRC)",
                "Susceptible microstructure",
                "Tensile stress applied",
                "Triaxial stress state",
            ],
            "gate_type": "AND",
        },
        "galvanic_corrosion": {
            "top_event": "Galvanic Corrosion Failure",
            "intermediate_events": [
                "Galvanic Cell Formed",
                "Corrosion Progression",
            ],
            "basic_events": [
                "Dissimilar metals present",
                "Metals in electrical contact",
                "Electrolyte present",
                "Potential difference exists",
                "No protective barrier",
                "Unfavorable area ratio",
            ],
            "gate_type": "AND",
        },
    }

    def __init__(self):
        """Initialize the fault tree analyzer."""
        pass

    async def analyze(
        self,
        failed_part: Any,
        evidence: Any,
        failure_mode: Any
    ) -> FaultTree:
        """
        Perform fault tree analysis.

        Args:
            failed_part: Information about failed part
            evidence: Failure evidence
            failure_mode: Determined failure mode

        Returns:
            Complete fault tree analysis
        """
        failure_mode_str = str(failure_mode.value if hasattr(failure_mode, 'value') else failure_mode)

        # Get template or use generic
        template = self.FAULT_TREE_TEMPLATES.get(failure_mode_str, {
            "top_event": f"{failure_mode_str} Failure",
            "intermediate_events": ["Contributing Factor 1", "Contributing Factor 2"],
            "basic_events": ["Unknown basic event 1", "Unknown basic event 2"],
            "gate_type": "AND",
        })

        # Build event chain
        event_chain = [template["top_event"]]
        event_chain.extend(template["intermediate_events"])

        # Determine minimal cut sets
        minimal_cut_sets = self._calculate_cut_sets(
            template["basic_events"],
            template["gate_type"]
        )

        # Build gate structure
        gate_structure = self._build_gate_structure(template)

        return FaultTree(
            top_event=template["top_event"],
            event_chain=event_chain,
            basic_events=template["basic_events"],
            minimal_cut_sets=minimal_cut_sets,
            gate_structure=gate_structure
        )

    def _calculate_cut_sets(
        self,
        basic_events: List[str],
        gate_type: str
    ) -> List[str]:
        """Calculate minimal cut sets from basic events."""
        if gate_type == "AND":
            # For AND gate, all events must occur - single cut set with all events
            return [" AND ".join(basic_events[:3])]  # Limit for readability
        else:
            # For OR gate, any single event is a cut set
            return basic_events[:3]

    def _build_gate_structure(self, template: Dict) -> Dict[str, Any]:
        """Build gate structure for fault tree."""
        return {
            "top_gate": {
                "type": template["gate_type"],
                "inputs": template["intermediate_events"],
            },
            "intermediate_gates": [
                {
                    "event": event,
                    "type": "OR",
                    "inputs": template["basic_events"][i*2:(i+1)*2]
                }
                for i, event in enumerate(template["intermediate_events"])
            ]
        }

    def generate_diagram_text(self, tree: FaultTree) -> str:
        """Generate text representation of fault tree."""
        lines = []
        lines.append("=" * 60)
        lines.append("FAULT TREE ANALYSIS")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"TOP EVENT: [{tree.top_event}]")
        lines.append("                |")
        lines.append("           [AND Gate]")
        lines.append("          /    |    \\")

        for i, event in enumerate(tree.event_chain[1:4]):
            lines.append(f"         [{event}]")
            if i < 2:
                lines.append("           |")

        lines.append("")
        lines.append("BASIC EVENTS:")
        for event in tree.basic_events:
            lines.append(f"  * {event}")

        lines.append("")
        lines.append("MINIMAL CUT SETS:")
        for cut_set in tree.minimal_cut_sets:
            lines.append(f"  {cut_set}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)
