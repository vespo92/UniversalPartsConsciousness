"""
ORACLE Safety Factor Engine
Dynamic safety factor calculation based on application requirements.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ApplicationClass(Enum):
    """Application criticality classification."""
    NON_CRITICAL = "non_critical"          # Failure causes inconvenience
    STANDARD = "standard"                   # Normal industrial use
    IMPORTANT = "important"                 # Failure causes significant cost
    CRITICAL = "critical"                   # Failure causes danger
    LIFE_SAFETY = "life_safety"            # Failure can cause injury/death


class LoadCharacter(Enum):
    """Load characteristic."""
    STATIC = "static"
    CYCLIC_LOW = "cyclic_low"              # < 10,000 cycles
    CYCLIC_MEDIUM = "cyclic_medium"        # 10,000 - 1,000,000 cycles
    CYCLIC_HIGH = "cyclic_high"            # > 1,000,000 cycles
    IMPACT = "impact"
    VIBRATION = "vibration"


class MaterialKnowledge(Enum):
    """Confidence in material properties."""
    CERTIFIED = "certified"                 # Mill cert, tested
    STANDARD = "standard"                   # Known grade, not tested
    ESTIMATED = "estimated"                 # Assumed properties
    UNKNOWN = "unknown"                     # No data


class LoadKnowledge(Enum):
    """Confidence in load data."""
    MEASURED = "measured"                   # Instrumented, tested
    CALCULATED = "calculated"               # FEA, analytical
    ESTIMATED = "estimated"                 # Engineering judgment
    UNKNOWN = "unknown"                     # No data


@dataclass
class SafetyFactorResult:
    """Safety factor calculation result."""
    recommended_sf: float
    minimum_sf: float
    component_factors: Dict[str, float]

    is_adequate: bool
    margin_percent: float

    reasoning: List[str]
    recommendations: List[str]
    code_references: List[str]


@dataclass
class ApplicationContext:
    """Context for safety factor determination."""
    application_class: ApplicationClass
    load_character: LoadCharacter
    material_knowledge: MaterialKnowledge
    load_knowledge: LoadKnowledge

    # Environmental factors
    temperature_c: float = 25.0
    corrosive_environment: bool = False
    outdoor_exposure: bool = False

    # Design factors
    redundancy_available: bool = False
    inspection_possible: bool = True
    consequence_of_failure: str = "moderate"

    # Code requirements
    applicable_code: Optional[str] = None


class SafetyFactorEngine:
    """
    Dynamic safety factor calculation engine.

    Determines appropriate safety factors based on:
    - Application criticality
    - Load characteristics
    - Material and load knowledge
    - Environmental factors
    - Code requirements
    """

    # Base safety factors by application class
    BASE_FACTORS = {
        ApplicationClass.NON_CRITICAL: 1.5,
        ApplicationClass.STANDARD: 2.0,
        ApplicationClass.IMPORTANT: 2.5,
        ApplicationClass.CRITICAL: 3.0,
        ApplicationClass.LIFE_SAFETY: 4.0,
    }

    # Load character multipliers
    LOAD_MULTIPLIERS = {
        LoadCharacter.STATIC: 1.0,
        LoadCharacter.CYCLIC_LOW: 1.2,
        LoadCharacter.CYCLIC_MEDIUM: 1.5,
        LoadCharacter.CYCLIC_HIGH: 2.0,
        LoadCharacter.IMPACT: 2.5,
        LoadCharacter.VIBRATION: 1.8,
    }

    # Material knowledge factors
    MATERIAL_FACTORS = {
        MaterialKnowledge.CERTIFIED: 1.0,
        MaterialKnowledge.STANDARD: 1.1,
        MaterialKnowledge.ESTIMATED: 1.3,
        MaterialKnowledge.UNKNOWN: 1.5,
    }

    # Load knowledge factors
    LOAD_FACTORS = {
        LoadKnowledge.MEASURED: 1.0,
        LoadKnowledge.CALCULATED: 1.1,
        LoadKnowledge.ESTIMATED: 1.3,
        LoadKnowledge.UNKNOWN: 1.5,
    }

    # Industry code references
    CODE_REQUIREMENTS = {
        "ASME_BPVC": {"static": 3.5, "fatigue": 4.0, "reference": "ASME Boiler and Pressure Vessel Code"},
        "AISC_360": {"static": 1.67, "fatigue": 2.0, "reference": "AISC 360 Steel Construction"},
        "Eurocode_3": {"static": 1.5, "fatigue": 1.35, "reference": "EN 1993 Eurocode 3"},
        "VDI_2230": {"static": 1.2, "fatigue": 1.5, "reference": "VDI 2230 Bolted Joints"},
        "ISO_898": {"static": 2.5, "fatigue": 3.0, "reference": "ISO 898 Mechanical Properties"},
        "automotive": {"static": 2.0, "fatigue": 3.0, "reference": "Automotive industry practice"},
        "aerospace": {"static": 1.5, "fatigue": 4.0, "reference": "Aerospace standards (FAR 25)"},
    }

    def __init__(self):
        pass

    def calculate_safety_factor(
        self,
        context: ApplicationContext
    ) -> SafetyFactorResult:
        """
        Calculate recommended safety factor.

        Args:
            context: Application context

        Returns:
            SafetyFactorResult with recommendations
        """
        component_factors = {}
        reasoning = []
        recommendations = []
        code_refs = []

        # 1. Base factor from application class
        base_sf = self.BASE_FACTORS[context.application_class]
        component_factors["application_class"] = base_sf
        reasoning.append(
            f"Base factor {base_sf:.1f} for {context.application_class.value} application"
        )

        # 2. Load character multiplier
        load_mult = self.LOAD_MULTIPLIERS[context.load_character]
        component_factors["load_character"] = load_mult
        if load_mult > 1.0:
            reasoning.append(
                f"Load multiplier {load_mult:.1f} for {context.load_character.value} loading"
            )

        # 3. Material knowledge factor
        mat_factor = self.MATERIAL_FACTORS[context.material_knowledge]
        component_factors["material_knowledge"] = mat_factor
        if mat_factor > 1.0:
            reasoning.append(
                f"Material uncertainty factor {mat_factor:.1f}"
            )
            if context.material_knowledge in [MaterialKnowledge.ESTIMATED, MaterialKnowledge.UNKNOWN]:
                recommendations.append("Obtain material certification to reduce required safety factor")

        # 4. Load knowledge factor
        load_factor = self.LOAD_FACTORS[context.load_knowledge]
        component_factors["load_knowledge"] = load_factor
        if load_factor > 1.0:
            reasoning.append(
                f"Load uncertainty factor {load_factor:.1f}"
            )
            if context.load_knowledge in [LoadKnowledge.ESTIMATED, LoadKnowledge.UNKNOWN]:
                recommendations.append("Perform load measurement or FEA to reduce uncertainty")

        # 5. Environmental adjustments
        env_factor = 1.0
        if context.corrosive_environment:
            env_factor *= 1.2
            reasoning.append("Corrosive environment increases factor by 20%")
            recommendations.append("Consider corrosion-resistant materials or protective coating")

        if context.outdoor_exposure:
            env_factor *= 1.1
            reasoning.append("Outdoor exposure increases factor by 10%")

        if context.temperature_c > 200:
            temp_factor = 1.0 + (context.temperature_c - 200) / 500
            env_factor *= temp_factor
            reasoning.append(f"High temperature ({context.temperature_c}°C) increases factor")

        component_factors["environment"] = env_factor

        # 6. Redundancy credit
        redundancy_factor = 1.0
        if context.redundancy_available:
            redundancy_factor = 0.85
            reasoning.append("Redundancy allows 15% factor reduction")
        component_factors["redundancy"] = redundancy_factor

        # 7. Inspection credit
        inspection_factor = 1.0
        if not context.inspection_possible:
            inspection_factor = 1.2
            reasoning.append("No inspection possible - increase factor by 20%")
            recommendations.append("Consider design changes to allow periodic inspection")
        component_factors["inspection"] = inspection_factor

        # Calculate combined safety factor
        recommended_sf = (
            base_sf *
            load_mult *
            mat_factor *
            load_factor *
            env_factor *
            redundancy_factor *
            inspection_factor
        )

        # Check against code requirements
        minimum_sf = recommended_sf
        if context.applicable_code and context.applicable_code in self.CODE_REQUIREMENTS:
            code_req = self.CODE_REQUIREMENTS[context.applicable_code]
            code_sf = code_req["fatigue"] if context.load_character != LoadCharacter.STATIC else code_req["static"]
            code_refs.append(code_req["reference"])

            if code_sf > minimum_sf:
                minimum_sf = code_sf
                reasoning.append(f"Code {context.applicable_code} requires minimum SF of {code_sf:.1f}")

            recommended_sf = max(recommended_sf, minimum_sf)

        # Determine adequacy (assuming current SF of 2.5 for comparison)
        current_sf = 2.5  # This would be an input in real use
        is_adequate = current_sf >= minimum_sf
        margin = ((current_sf / minimum_sf) - 1) * 100

        # Generate recommendations based on consequence
        if context.consequence_of_failure == "severe":
            recommendations.append("Consider additional redundancy for severe consequence applications")
            if recommended_sf < 3.0:
                recommendations.append("Minimum SF of 3.0 recommended for severe consequences")

        return SafetyFactorResult(
            recommended_sf=round(recommended_sf, 2),
            minimum_sf=round(minimum_sf, 2),
            component_factors=component_factors,
            is_adequate=is_adequate,
            margin_percent=margin,
            reasoning=reasoning,
            recommendations=recommendations,
            code_references=code_refs
        )

    def get_code_requirement(
        self,
        code: str,
        load_type: str = "static"
    ) -> Optional[float]:
        """Get safety factor requirement for specific code."""
        if code not in self.CODE_REQUIREMENTS:
            return None

        return self.CODE_REQUIREMENTS[code].get(load_type)

    def compare_against_code(
        self,
        actual_sf: float,
        code: str,
        load_type: str = "static"
    ) -> Dict:
        """Compare actual safety factor against code requirement."""
        code_sf = self.get_code_requirement(code, load_type)

        if code_sf is None:
            return {
                "code_found": False,
                "message": f"Unknown code: {code}"
            }

        margin = ((actual_sf / code_sf) - 1) * 100
        passes = actual_sf >= code_sf

        return {
            "code_found": True,
            "code": code,
            "required_sf": code_sf,
            "actual_sf": actual_sf,
            "passes": passes,
            "margin_percent": margin,
            "reference": self.CODE_REQUIREMENTS[code]["reference"]
        }

    def suggest_for_application(
        self,
        application_description: str
    ) -> ApplicationContext:
        """
        Suggest application context from description.

        Simple keyword-based matching - would use NLP in production.
        """
        desc_lower = application_description.lower()

        # Determine application class
        if any(w in desc_lower for w in ["life", "safety", "medical", "aircraft", "human"]):
            app_class = ApplicationClass.LIFE_SAFETY
        elif any(w in desc_lower for w in ["critical", "pressure", "high-speed", "nuclear"]):
            app_class = ApplicationClass.CRITICAL
        elif any(w in desc_lower for w in ["structural", "crane", "elevator", "vehicle"]):
            app_class = ApplicationClass.IMPORTANT
        elif any(w in desc_lower for w in ["furniture", "consumer", "household"]):
            app_class = ApplicationClass.NON_CRITICAL
        else:
            app_class = ApplicationClass.STANDARD

        # Determine load character
        if any(w in desc_lower for w in ["vibration", "engine", "rotating"]):
            load_char = LoadCharacter.VIBRATION
        elif any(w in desc_lower for w in ["impact", "crash", "drop"]):
            load_char = LoadCharacter.IMPACT
        elif any(w in desc_lower for w in ["cyclic", "fatigue", "repeated"]):
            load_char = LoadCharacter.CYCLIC_MEDIUM
        else:
            load_char = LoadCharacter.STATIC

        # Determine environment
        corrosive = any(w in desc_lower for w in ["marine", "chemical", "acid", "salt"])
        outdoor = any(w in desc_lower for w in ["outdoor", "exterior", "exposed"])

        return ApplicationContext(
            application_class=app_class,
            load_character=load_char,
            material_knowledge=MaterialKnowledge.STANDARD,
            load_knowledge=LoadKnowledge.CALCULATED,
            corrosive_environment=corrosive,
            outdoor_exposure=outdoor
        )
