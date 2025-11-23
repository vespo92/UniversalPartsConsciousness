"""
Coating Selection Engine

Intelligent coating selection based on substrate, environment,
and performance requirements including corrosion, wear, and friction.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

from .database import CoatingDatabase, CoatingSpec, CoatingType


class EnvironmentSeverity(Enum):
    """Environmental severity for coating selection"""
    INDOOR_DRY = "indoor_dry"
    INDOOR_HUMID = "indoor_humid"
    OUTDOOR_MILD = "outdoor_mild"
    OUTDOOR_INDUSTRIAL = "outdoor_industrial"
    MARINE = "marine"
    CHEMICAL = "chemical"
    HIGH_TEMP = "high_temp"


@dataclass
class CoatingRecommendation:
    """Coating recommendation with scoring"""
    coating: CoatingSpec
    suitability_score: float  # 0-1
    meets_requirements: Dict[str, bool]
    advantages: List[str]
    warnings: List[str]
    application_notes: str = ""


@dataclass
class HydrogenEmbrittlementAssessment:
    """Assessment of hydrogen embrittlement risk"""
    risk_present: bool
    substrate_hardness_hrc: float
    coating_he_risk: bool
    threshold_hrc: Optional[int]
    mitigation_required: bool
    bake_required: bool
    bake_spec: str = ""
    alternative_coatings: List[str] = None


class CoatingSelector:
    """
    Intelligent coating selection engine.

    Selects coatings based on substrate material, hardness,
    environment, and performance requirements.
    """

    # Salt spray requirements by environment (hours to red rust)
    ENVIRONMENT_SALT_SPRAY = {
        EnvironmentSeverity.INDOOR_DRY: 24,
        EnvironmentSeverity.INDOOR_HUMID: 96,
        EnvironmentSeverity.OUTDOOR_MILD: 200,
        EnvironmentSeverity.OUTDOOR_INDUSTRIAL: 500,
        EnvironmentSeverity.MARINE: 720,
        EnvironmentSeverity.CHEMICAL: 500,
        EnvironmentSeverity.HIGH_TEMP: 200,
    }

    def __init__(self, database: Optional[CoatingDatabase] = None):
        self.db = database or CoatingDatabase()

    def select(
        self,
        substrate: str,
        environment: EnvironmentSeverity,
        requirements: Optional[Dict] = None
    ) -> List[CoatingRecommendation]:
        """
        Select coatings for a substrate and environment.

        Args:
            substrate: Substrate material (e.g., "carbon_steel", "aluminum")
            environment: Operating environment severity
            requirements: {
                "hardness_hrc": float,  # Substrate hardness
                "min_salt_spray_hours": int,
                "max_friction_coefficient": float,
                "temperature_max_c": float,
                "low_friction": bool,
                "wear_resistant": bool,
                "no_hex_chrome": bool,
                "rohs_required": bool,
            }

        Returns:
            List of CoatingRecommendations sorted by suitability
        """
        requirements = requirements or {}
        recommendations = []

        # Get minimum salt spray requirement
        min_salt_spray = requirements.get(
            "min_salt_spray_hours",
            self.ENVIRONMENT_SALT_SPRAY.get(environment, 96)
        )

        substrate_normalized = substrate.lower().replace(" ", "_").replace("-", "_")

        for coating in self.db.search():
            score, meets, advantages, warnings = self._evaluate(
                coating, substrate_normalized, environment, requirements, min_salt_spray
            )

            if score > 0.2:
                recommendations.append(CoatingRecommendation(
                    coating=coating,
                    suitability_score=score,
                    meets_requirements=meets,
                    advantages=advantages,
                    warnings=warnings,
                    application_notes=self._generate_notes(coating, substrate_normalized, requirements)
                ))

        recommendations.sort(key=lambda x: x.suitability_score, reverse=True)
        return recommendations[:8]

    def _evaluate(
        self,
        coating: CoatingSpec,
        substrate: str,
        environment: EnvironmentSeverity,
        requirements: Dict,
        min_salt_spray: int
    ) -> tuple:
        """Evaluate a coating against requirements"""
        score = 1.0
        meets = {}
        advantages = []
        warnings = []

        # Substrate compatibility
        substrate_compatible = self._check_substrate_compatibility(coating, substrate)
        if not substrate_compatible:
            return 0.0, {}, [], ["Not compatible with substrate"]
        meets["substrate"] = True

        # Salt spray performance
        if coating.salt_spray_hours >= min_salt_spray:
            meets["corrosion"] = True
            if coating.salt_spray_hours >= min_salt_spray * 2:
                advantages.append(f"Excellent corrosion protection ({coating.salt_spray_hours}hr)")
                score += 0.1
        else:
            meets["corrosion"] = False
            deficit = min_salt_spray - coating.salt_spray_hours
            if deficit > 200:
                score *= 0.3
            else:
                score *= 0.6
            warnings.append(f"Salt spray {coating.salt_spray_hours}hr may be insufficient")

        # Temperature requirement
        temp_max = requirements.get("temperature_max_c", 100)
        if coating.temperature_max_c >= temp_max:
            meets["temperature"] = True
            if coating.temperature_max_c >= temp_max + 100:
                advantages.append(f"High temperature capable ({coating.temperature_max_c}°C)")
        else:
            meets["temperature"] = False
            score *= 0.4
            warnings.append(f"Max temp {coating.temperature_max_c}°C below requirement")

        # Friction requirement
        if requirements.get("low_friction"):
            if coating.friction_coefficient and coating.friction_coefficient < 0.15:
                meets["friction"] = True
                advantages.append(f"Low friction ({coating.friction_coefficient})")
                score += 0.1
            elif coating.friction_coefficient and coating.friction_coefficient < 0.25:
                meets["friction"] = True
            else:
                meets["friction"] = False
                score *= 0.7

        # Wear resistance
        if requirements.get("wear_resistant"):
            wear_coatings = ["hard_chrome", "electroless_nickel", "hard_anodize"]
            if any(w in coating.name.lower().replace(" ", "_") for w in wear_coatings):
                meets["wear"] = True
                advantages.append("Excellent wear resistance")
                score += 0.1
            elif coating.hardness and "hv" in coating.hardness.lower():
                # Extract hardness value
                try:
                    hv = int(coating.hardness.lower().split("hv")[1].split()[0].strip("-"))
                    if hv >= 400:
                        meets["wear"] = True
                except (ValueError, IndexError):
                    pass

        # Hydrogen embrittlement
        hardness_hrc = requirements.get("hardness_hrc", 30)
        if coating.hydrogen_embrittlement_risk:
            if hardness_hrc >= (coating.he_risk_threshold_hrc or 39):
                warnings.append(
                    f"HE RISK: Substrate HRC {hardness_hrc} >= threshold. "
                    f"Baking required per ASTM B850."
                )
                score *= 0.8
        else:
            if hardness_hrc >= 39:
                advantages.append("No hydrogen embrittlement risk")
                score += 0.15

        # Environmental compliance
        if requirements.get("no_hex_chrome") and coating.contains_hex_chrome:
            score *= 0.1
            warnings.append("Contains hexavalent chromium")
            meets["hex_chrome_free"] = False
        elif requirements.get("no_hex_chrome"):
            meets["hex_chrome_free"] = True

        if requirements.get("rohs_required") and not coating.rohs_compliant:
            score *= 0.2
            warnings.append("Not RoHS compliant")
            meets["rohs"] = False
        elif requirements.get("rohs_required"):
            meets["rohs"] = True

        # Cost consideration
        if coating.relative_cost > 4:
            warnings.append(f"Higher cost ({coating.relative_cost}x baseline)")
        elif coating.relative_cost < 1.5:
            advantages.append("Cost effective")

        score = min(1.0, max(0.0, score))
        return score, meets, advantages, warnings

    def _check_substrate_compatibility(self, coating: CoatingSpec, substrate: str) -> bool:
        """Check if coating is compatible with substrate"""
        # Check compatible substrates
        for compat in coating.compatible_substrates:
            compat_norm = compat.lower().replace(" ", "_").replace("-", "_")
            if compat_norm in substrate or substrate in compat_norm:
                return True
            # Generic checks
            if "steel" in substrate and "steel" in compat_norm:
                return True
            if "aluminum" in substrate and "aluminum" in compat_norm:
                return True

        # Check not recommended
        for not_rec in coating.not_recommended_for:
            not_rec_norm = not_rec.lower().replace(" ", "_").replace("-", "_")
            if not_rec_norm in substrate:
                return False

        return False

    def _generate_notes(
        self,
        coating: CoatingSpec,
        substrate: str,
        requirements: Dict
    ) -> str:
        """Generate application-specific notes"""
        notes = []

        hardness_hrc = requirements.get("hardness_hrc", 30)

        if coating.hydrogen_embrittlement_risk and hardness_hrc >= 39:
            notes.append(
                f"Bake within 4 hours of plating per ASTM B850. "
                f"Typical: 375°F (190°C) for 4-24 hours."
            )

        if "anodize" in coating.name.lower() and "7" in substrate:
            notes.append(
                "7xxx series aluminum requires special anodizing procedures. "
                "May have lower coating quality than 6xxx series."
            )

        if coating.coating_type == CoatingType.MECHANICAL:
            notes.append("No hydrogen embrittlement risk - suitable for high-strength fasteners.")

        return " | ".join(notes) if notes else ""

    def assess_he_risk(
        self,
        substrate: str,
        hardness_hrc: float,
        proposed_coating: str
    ) -> HydrogenEmbrittlementAssessment:
        """
        Assess hydrogen embrittlement risk for a coating application.

        Args:
            substrate: Substrate material
            hardness_hrc: Substrate hardness in HRC
            proposed_coating: Proposed coating name

        Returns:
            HydrogenEmbrittlementAssessment with risk analysis
        """
        coating = self.db.get(proposed_coating)
        if coating is None:
            raise ValueError(f"Unknown coating: {proposed_coating}")

        threshold = coating.he_risk_threshold_hrc or 39
        risk_present = coating.hydrogen_embrittlement_risk and hardness_hrc >= threshold
        mitigation_required = risk_present
        bake_required = risk_present

        bake_spec = ""
        if bake_required:
            if hardness_hrc >= 50:
                bake_spec = "375°F (190°C) for 23+ hours per ASTM B850 Table 1"
            elif hardness_hrc >= 40:
                bake_spec = "375°F (190°C) for 8-14 hours per ASTM B850"
            else:
                bake_spec = "375°F (190°C) for 4-8 hours per ASTM B850"

        # Find alternative coatings without HE risk
        alternatives = []
        if risk_present:
            for alt_coating in self.db.search(no_he_risk=True):
                if self._check_substrate_compatibility(alt_coating, substrate.lower()):
                    alternatives.append(alt_coating.name)

        return HydrogenEmbrittlementAssessment(
            risk_present=risk_present,
            substrate_hardness_hrc=hardness_hrc,
            coating_he_risk=coating.hydrogen_embrittlement_risk,
            threshold_hrc=threshold,
            mitigation_required=mitigation_required,
            bake_required=bake_required,
            bake_spec=bake_spec,
            alternative_coatings=alternatives[:5] if alternatives else None
        )

    def select_for_fasteners(
        self,
        grade: str,
        environment: EnvironmentSeverity,
        controlled_friction: bool = False
    ) -> List[CoatingRecommendation]:
        """
        Specialized selection for fasteners.

        Args:
            grade: Fastener grade (e.g., "Grade 8", "Class 10.9", "A2-70")
            environment: Operating environment
            controlled_friction: Whether torque-tension control is needed

        Returns:
            Recommended coatings for fastener application
        """
        # Determine hardness from grade
        hardness_hrc = self._grade_to_hardness(grade)
        high_strength = hardness_hrc >= 39

        requirements = {
            "hardness_hrc": hardness_hrc,
            "low_friction": controlled_friction,
        }

        if high_strength:
            # Prefer non-HE coatings for high-strength
            requirements["no_he_risk_preferred"] = True

        # Get recommendations
        recs = self.select("carbon_steel", environment, requirements)

        # Boost mechanical coatings for high-strength fasteners
        if high_strength:
            for rec in recs:
                if rec.coating.coating_type == CoatingType.MECHANICAL:
                    rec.suitability_score = min(1.0, rec.suitability_score + 0.2)
                    rec.advantages.append("Ideal for high-strength fasteners")

        # Re-sort after adjustment
        recs.sort(key=lambda x: x.suitability_score, reverse=True)

        return recs

    def _grade_to_hardness(self, grade: str) -> float:
        """Convert fastener grade to approximate HRC hardness"""
        grade_hardness = {
            # SAE grades
            "grade_2": 25,
            "grade_5": 28,
            "grade_8": 39,
            # Metric classes
            "class_4.8": 22,
            "class_8.8": 28,
            "class_10.9": 36,
            "class_12.9": 42,
            # Stainless
            "a2-70": 25,
            "a4-70": 25,
            "a2-80": 30,
            "a4-80": 30,
        }

        grade_normalized = grade.lower().replace(" ", "_")
        return grade_hardness.get(grade_normalized, 30)


# Demo
if __name__ == "__main__":
    selector = CoatingSelector()

    print("=== Coating Selection Demo ===\n")

    # Select for carbon steel in marine environment
    print("--- Marine environment coating for carbon steel ---")
    recs = selector.select(
        "carbon_steel",
        EnvironmentSeverity.MARINE,
        {"temperature_max_c": 150}
    )

    for rec in recs[:3]:
        print(f"\n{rec.coating.name}:")
        print(f"  Suitability: {rec.suitability_score:.0%}")
        print(f"  Salt spray: {rec.coating.salt_spray_hours} hours")
        if rec.advantages:
            print(f"  Advantages: {', '.join(rec.advantages[:2])}")
        if rec.warnings:
            print(f"  Warnings: {', '.join(rec.warnings[:2])}")

    # High-strength fastener HE assessment
    print("\n--- HE Risk Assessment for Grade 8 Fastener ---")
    he_assessment = selector.assess_he_risk(
        "alloy_steel",
        hardness_hrc=42,
        proposed_coating="Zinc Electroplate"
    )
    print(f"Risk present: {he_assessment.risk_present}")
    print(f"Bake required: {he_assessment.bake_required}")
    if he_assessment.bake_spec:
        print(f"Bake spec: {he_assessment.bake_spec}")
    if he_assessment.alternative_coatings:
        print(f"Alternatives: {', '.join(he_assessment.alternative_coatings[:3])}")
