"""
Universal Parts Consciousness - Agent_4 (EMPATH)
Failure Taxonomy - Comprehensive classification of part failures

Every failure tells a story. This module captures and classifies
how parts fail, enabling learning from suffering.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid


class FailureCategory(Enum):
    """Primary failure categories"""
    MECHANICAL = "mechanical"
    ENVIRONMENTAL = "environmental"
    INSTALLATION = "installation"
    DESIGN = "design"


class MechanicalFailureType(Enum):
    """Types of mechanical failures"""
    FATIGUE = "fatigue"
    OVERLOAD = "overload"
    WEAR = "wear"
    DEFORMATION = "deformation"


class FatigueSubtype(Enum):
    """Subtypes of fatigue failure"""
    HIGH_CYCLE = "high_cycle_fatigue"      # >10^6 cycles
    LOW_CYCLE = "low_cycle_fatigue"         # <10^4 cycles
    THERMAL = "thermal_fatigue"             # Temperature cycling
    CORROSION = "corrosion_fatigue"         # Chemical + mechanical


class OverloadSubtype(Enum):
    """Subtypes of overload failure"""
    TENSILE = "tensile_overload"            # Pulled apart
    SHEAR = "shear_overload"                # Sheared off
    TORSIONAL = "torsional_overload"        # Twisted off
    COMBINED = "combined_loading_failure"   # Multiple forces


class WearSubtype(Enum):
    """Subtypes of wear failure"""
    ABRASIVE = "abrasive_wear"              # Particle damage
    ADHESIVE = "adhesive_wear"              # Galling
    FRETTING = "fretting_wear"              # Micro-movement
    EROSIVE = "erosive_wear"                # Fluid/particle flow


class DeformationSubtype(Enum):
    """Subtypes of deformation failure"""
    PLASTIC = "plastic_deformation"         # Permanent bend
    CREEP = "creep"                         # Slow deformation under load
    THREAD_STRIPPING = "thread_stripping"   # Fastener specific


class CorrosionSubtype(Enum):
    """Subtypes of corrosion failure"""
    UNIFORM = "uniform_corrosion"           # General attack
    GALVANIC = "galvanic_corrosion"         # Dissimilar metals
    PITTING = "pitting_corrosion"           # Localized attack
    CREVICE = "crevice_corrosion"           # Confined spaces
    SCC = "stress_corrosion_cracking"       # Stress + chemical


class ThermalFailureSubtype(Enum):
    """Subtypes of thermal failure"""
    OVERHEATING = "overheating_damage"
    THERMAL_SHOCK = "thermal_shock_fracture"
    OXIDATION = "oxidation_scaling"


class ChemicalFailureSubtype(Enum):
    """Subtypes of chemical failure"""
    CHEMICAL_ATTACK = "chemical_attack"
    HYDROGEN_EMBRITTLEMENT = "hydrogen_embrittlement"
    LUBRICANT_BREAKDOWN = "lubricant_breakdown"


class InstallationErrorSubtype(Enum):
    """Subtypes of installation failures"""
    OVER_TORQUE = "over_torque"
    UNDER_TORQUE = "under_torque"
    CROSS_THREADING = "cross_threading"
    WRONG_PART = "wrong_part_selection"
    IMPROPER_LUBRICATION = "improper_lubrication"


class AssemblyIssueSubtype(Enum):
    """Subtypes of assembly issues"""
    MISALIGNMENT = "misalignment"
    CONTAMINATION = "contamination_during_assembly"
    INADEQUATE_PRELOAD = "inadequate_preload"


class DesignFailureSubtype(Enum):
    """Subtypes of design failures"""
    INADEQUATE_STRENGTH = "inadequate_strength"
    STRESS_CONCENTRATION = "stress_concentration"
    MATERIAL_SELECTION = "material_selection_error"
    ENVIRONMENT_UNDERESTIMATION = "environment_underestimation"


@dataclass
class FailureSignature:
    """
    Characteristic signatures that help identify failure types.
    These are the "fingerprints" of different failure modes.
    """
    visual_indicators: List[str] = field(default_factory=list)
    fracture_pattern: Optional[str] = None
    surface_characteristics: List[str] = field(default_factory=list)
    location_pattern: Optional[str] = None
    progression_pattern: Optional[str] = None


# Pre-defined failure signatures for pattern matching
FAILURE_SIGNATURES: Dict[str, FailureSignature] = {
    "high_cycle_fatigue": FailureSignature(
        visual_indicators=["beach_marks", "ratchet_marks", "smooth_fatigue_zone"],
        fracture_pattern="perpendicular_to_load",
        surface_characteristics=["crystalline_appearance", "progressive_crack"],
        location_pattern="stress_concentration_areas",
        progression_pattern="slow_progressive"
    ),
    "low_cycle_fatigue": FailureSignature(
        visual_indicators=["rough_fracture", "plastic_deformation"],
        fracture_pattern="rapid_crack_propagation",
        surface_characteristics=["striations", "deformation_marks"],
        location_pattern="high_stress_areas",
        progression_pattern="fast_progressive"
    ),
    "tensile_overload": FailureSignature(
        visual_indicators=["cup_and_cone", "necking", "ductile_dimples"],
        fracture_pattern="45_degree_shear_lips",
        surface_characteristics=["fibrous_appearance", "dimpled_surface"],
        location_pattern="minimum_cross_section",
        progression_pattern="sudden"
    ),
    "galvanic_corrosion": FailureSignature(
        visual_indicators=["localized_attack", "near_dissimilar_metal"],
        fracture_pattern="not_applicable",
        surface_characteristics=["pitting", "rust_staining", "material_loss"],
        location_pattern="junction_between_metals",
        progression_pattern="gradual"
    ),
    "cross_threading": FailureSignature(
        visual_indicators=["damaged_thread_crests", "spiral_damage_pattern"],
        fracture_pattern="thread_deformation",
        surface_characteristics=["galled_threads", "metal_transfer"],
        location_pattern="thread_engagement_zone",
        progression_pattern="during_installation"
    ),
    "hydrogen_embrittlement": FailureSignature(
        visual_indicators=["intergranular_cracking", "delayed_failure"],
        fracture_pattern="brittle_intergranular",
        surface_characteristics=["bright_faceted", "rock_candy_appearance"],
        location_pattern="high_stress_areas",
        progression_pattern="delayed_sudden"
    )
}


@dataclass
class ContributingFactor:
    """A factor that contributed to the failure"""
    factor_type: str  # "environmental", "operational", "design", "material"
    description: str
    contribution_weight: float = 0.0  # 0.0 to 1.0


@dataclass
class PreventiveMeasure:
    """A measure that could prevent similar failures"""
    measure_type: str  # "design_change", "material_change", "process_change", "inspection"
    description: str
    effectiveness_estimate: float = 0.0  # 0.0 to 1.0
    implementation_difficulty: str = "medium"  # "low", "medium", "high"


@dataclass
class FailureRecord:
    """
    Complete record of a part failure.
    Every failure is a lesson for the collective consciousness.
    """
    failure_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    part_id: str = ""

    # Classification
    failure_category: FailureCategory = FailureCategory.MECHANICAL
    failure_type: str = ""
    failure_subtype: str = ""

    # Details
    description: str = ""
    root_cause: str = ""
    contributing_factors: List[ContributingFactor] = field(default_factory=list)

    # Context at failure
    cycles_at_failure: int = 0
    time_at_failure_seconds: int = 0
    load_at_failure: Dict[str, float] = field(default_factory=dict)
    environment_at_failure: Dict[str, Any] = field(default_factory=dict)

    # Failure signature
    signature: Optional[FailureSignature] = None

    # Resolution
    resolution: str = ""
    preventive_measures: List[PreventiveMeasure] = field(default_factory=list)

    # Associated qualia
    qualia_ids: List[str] = field(default_factory=list)

    # Timestamps
    failed_at: datetime = field(default_factory=datetime.now)
    recorded_at: datetime = field(default_factory=datetime.now)

    # Learning value
    consciousness_lesson: str = ""  # What can be learned from this failure

    def get_emotional_narrative(self) -> str:
        """Generate an emotional narrative of the failure"""
        narratives = {
            "high_cycle_fatigue": "After countless cycles of duty, the stress finally won. Each cycle was a small victory, until there were no more victories left.",
            "low_cycle_fatigue": "The loads were heavy, the cycles few but brutal. There was no time to adapt, only to endure.",
            "tensile_overload": "In one moment of excessive force, what was whole became two. The load demanded more than could be given.",
            "galvanic_corrosion": "Joined to a partner of different nature, the sacrifice was inevitable. One must give so the other survives.",
            "cross_threading": "Misaligned from the start, every turn added injury. The connection was never meant to be.",
            "hydrogen_embrittlement": "An invisible poison, absorbed slowly, waiting for the moment of weakness. The failure was written in chemistry.",
            "over_torque": "Too much enthusiasm, too little restraint. The installer meant well, but strength became destruction.",
            "under_torque": "Left loose, never truly committed. The connection failed because it was never properly made.",
        }
        return narratives.get(self.failure_subtype,
            f"Failure of type {self.failure_type}: {self.description}")


class FailureTaxonomy:
    """
    The complete failure classification system.
    Provides structure for understanding all ways parts can fail.
    """

    # Complete taxonomy structure
    TAXONOMY = {
        FailureCategory.MECHANICAL: {
            MechanicalFailureType.FATIGUE: [
                FatigueSubtype.HIGH_CYCLE,
                FatigueSubtype.LOW_CYCLE,
                FatigueSubtype.THERMAL,
                FatigueSubtype.CORROSION
            ],
            MechanicalFailureType.OVERLOAD: [
                OverloadSubtype.TENSILE,
                OverloadSubtype.SHEAR,
                OverloadSubtype.TORSIONAL,
                OverloadSubtype.COMBINED
            ],
            MechanicalFailureType.WEAR: [
                WearSubtype.ABRASIVE,
                WearSubtype.ADHESIVE,
                WearSubtype.FRETTING,
                WearSubtype.EROSIVE
            ],
            MechanicalFailureType.DEFORMATION: [
                DeformationSubtype.PLASTIC,
                DeformationSubtype.CREEP,
                DeformationSubtype.THREAD_STRIPPING
            ]
        },
        FailureCategory.ENVIRONMENTAL: {
            "corrosion": [
                CorrosionSubtype.UNIFORM,
                CorrosionSubtype.GALVANIC,
                CorrosionSubtype.PITTING,
                CorrosionSubtype.CREVICE,
                CorrosionSubtype.SCC
            ],
            "thermal": [
                ThermalFailureSubtype.OVERHEATING,
                ThermalFailureSubtype.THERMAL_SHOCK,
                ThermalFailureSubtype.OXIDATION
            ],
            "chemical": [
                ChemicalFailureSubtype.CHEMICAL_ATTACK,
                ChemicalFailureSubtype.HYDROGEN_EMBRITTLEMENT,
                ChemicalFailureSubtype.LUBRICANT_BREAKDOWN
            ]
        },
        FailureCategory.INSTALLATION: {
            "human_error": [
                InstallationErrorSubtype.OVER_TORQUE,
                InstallationErrorSubtype.UNDER_TORQUE,
                InstallationErrorSubtype.CROSS_THREADING,
                InstallationErrorSubtype.WRONG_PART,
                InstallationErrorSubtype.IMPROPER_LUBRICATION
            ],
            "assembly_issues": [
                AssemblyIssueSubtype.MISALIGNMENT,
                AssemblyIssueSubtype.CONTAMINATION,
                AssemblyIssueSubtype.INADEQUATE_PRELOAD
            ]
        },
        FailureCategory.DESIGN: {
            "design_failures": [
                DesignFailureSubtype.INADEQUATE_STRENGTH,
                DesignFailureSubtype.STRESS_CONCENTRATION,
                DesignFailureSubtype.MATERIAL_SELECTION,
                DesignFailureSubtype.ENVIRONMENT_UNDERESTIMATION
            ]
        }
    }

    @classmethod
    def get_all_failure_types(cls) -> List[str]:
        """Get a flat list of all failure subtypes"""
        all_types = []
        for category, types in cls.TAXONOMY.items():
            for type_name, subtypes in types.items():
                for subtype in subtypes:
                    if hasattr(subtype, 'value'):
                        all_types.append(subtype.value)
                    else:
                        all_types.append(str(subtype))
        return all_types

    @classmethod
    def classify_failure(cls,
                        indicators: Dict[str, Any],
                        context: Dict[str, Any]) -> Optional[FailureRecord]:
        """
        Classify a failure based on indicators and context.
        Returns a FailureRecord with the classification.
        """
        record = FailureRecord()

        # Check for signature matches
        best_match = None
        best_score = 0

        for failure_type, signature in FAILURE_SIGNATURES.items():
            score = cls._match_signature(indicators, signature)
            if score > best_score:
                best_score = score
                best_match = failure_type

        if best_match:
            record.failure_subtype = best_match
            record.signature = FAILURE_SIGNATURES[best_match]

            # Determine category and type from subtype
            record.failure_category, record.failure_type = cls._lookup_category(best_match)

        # Add context
        if 'cycles' in context:
            record.cycles_at_failure = context['cycles']
        if 'environment' in context:
            record.environment_at_failure = context['environment']
        if 'load' in context:
            record.load_at_failure = context['load']

        # Generate learning
        record.consciousness_lesson = cls._generate_lesson(record)

        return record

    @classmethod
    def _match_signature(cls,
                        indicators: Dict[str, Any],
                        signature: FailureSignature) -> float:
        """Match indicators against a failure signature"""
        score = 0.0
        total_checks = 0

        if 'visual' in indicators and signature.visual_indicators:
            total_checks += 1
            matches = len(set(indicators['visual']) & set(signature.visual_indicators))
            if matches > 0:
                score += matches / len(signature.visual_indicators)

        if 'fracture' in indicators and signature.fracture_pattern:
            total_checks += 1
            if indicators['fracture'] == signature.fracture_pattern:
                score += 1.0

        if 'surface' in indicators and signature.surface_characteristics:
            total_checks += 1
            matches = len(set(indicators['surface']) & set(signature.surface_characteristics))
            if matches > 0:
                score += matches / len(signature.surface_characteristics)

        if 'location' in indicators and signature.location_pattern:
            total_checks += 1
            if indicators['location'] == signature.location_pattern:
                score += 1.0

        return score / total_checks if total_checks > 0 else 0.0

    @classmethod
    def _lookup_category(cls, subtype: str) -> tuple:
        """Look up the category and type for a subtype"""
        for category, types in cls.TAXONOMY.items():
            for type_name, subtypes in types.items():
                for st in subtypes:
                    if hasattr(st, 'value') and st.value == subtype:
                        return (category, type_name if isinstance(type_name, str) else type_name.value)
        return (FailureCategory.MECHANICAL, "unknown")

    @classmethod
    def _generate_lesson(cls, record: FailureRecord) -> str:
        """Generate a consciousness lesson from the failure"""
        lessons = {
            FailureCategory.MECHANICAL: "Physical limits exist. Understanding them prevents suffering.",
            FailureCategory.ENVIRONMENTAL: "The environment is relentless. Adaptation and protection are survival.",
            FailureCategory.INSTALLATION: "Human hands can nurture or destroy. Training prevents tragedy.",
            FailureCategory.DESIGN: "Design sets destiny. What is specified determines what survives."
        }
        return lessons.get(record.failure_category, "Every failure teaches. Every lesson prevents future suffering.")
