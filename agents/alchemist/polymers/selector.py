"""
Polymer Selection Engine

Intelligent polymer selection based on application requirements
including temperature, chemical exposure, mechanical loads, and cost.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

from .database import PolymerDatabase, PolymerSpec, ChemicalResistance


class MechanicalLoad(Enum):
    """Mechanical load classification"""
    NONE = "none"       # No load (seals, liners)
    LIGHT = "light"     # Light loads, low stress
    MEDIUM = "medium"   # Moderate stress
    HEAVY = "heavy"     # High stress, load bearing
    IMPACT = "impact"   # Impact/shock loads


@dataclass
class PolymerRecommendation:
    """Polymer recommendation with scoring"""
    polymer: PolymerSpec
    suitability_score: float  # 0-1
    temperature_margin_c: float
    meets_requirements: Dict[str, bool]
    advantages: List[str]
    limitations: List[str]
    cost_factor: float
    application_notes: str = ""


class PolymerSelector:
    """
    Intelligent polymer selection engine.

    Analyzes application requirements and recommends optimal
    polymers based on temperature, chemical, mechanical, and cost criteria.
    """

    def __init__(self, database: Optional[PolymerDatabase] = None):
        self.db = database or PolymerDatabase()

    def select(
        self,
        requirements: Dict,
        constraints: Optional[Dict] = None
    ) -> List[PolymerRecommendation]:
        """
        Select polymers based on requirements.

        Args:
            requirements: {
                "temperature_max_c": float,
                "temperature_min_c": float (optional),
                "chemical_exposure": List[str],
                "mechanical_load": str,
                "outdoor_uv": bool,
                "food_contact": bool,
                "sterilization": str,
            }
            constraints: {
                "max_cost_factor": float,
                "prefer_low_friction": bool,
                "prefer_transparency": bool,
            }

        Returns:
            List of PolymerRecommendations sorted by suitability
        """
        constraints = constraints or {}
        recommendations = []

        for polymer in self.db.search():
            score, meets, advantages, limitations = self._evaluate(
                polymer, requirements, constraints
            )

            if score > 0.2:  # Minimum threshold
                temp_margin = polymer.temp_max_continuous_c - requirements.get("temperature_max_c", 25)

                recommendations.append(PolymerRecommendation(
                    polymer=polymer,
                    suitability_score=score,
                    temperature_margin_c=temp_margin,
                    meets_requirements=meets,
                    advantages=advantages,
                    limitations=limitations,
                    cost_factor=polymer.cost_factor,
                    application_notes=self._generate_notes(polymer, requirements)
                ))

        # Sort by suitability score
        recommendations.sort(key=lambda x: x.suitability_score, reverse=True)
        return recommendations[:10]  # Top 10

    def _evaluate(
        self,
        polymer: PolymerSpec,
        requirements: Dict,
        constraints: Dict
    ) -> tuple:
        """Evaluate a polymer against requirements"""
        score = 1.0
        meets = {}
        advantages = []
        limitations = []

        # Temperature evaluation
        max_temp = requirements.get("temperature_max_c", 25)
        min_temp = requirements.get("temperature_min_c", -20)

        if polymer.temp_max_continuous_c >= max_temp:
            meets["temperature_max"] = True
            margin = polymer.temp_max_continuous_c - max_temp
            if margin > 50:
                advantages.append(f"Excellent temperature margin (+{margin:.0f}°C)")
                score += 0.1
            elif margin > 20:
                advantages.append(f"Good temperature margin (+{margin:.0f}°C)")
        else:
            meets["temperature_max"] = False
            deficit = max_temp - polymer.temp_max_continuous_c
            limitations.append(f"Max temp {polymer.temp_max_continuous_c}°C, need {max_temp}°C")
            score *= 0.3 if deficit > 30 else 0.5

        if polymer.temp_min_c <= min_temp:
            meets["temperature_min"] = True
        else:
            meets["temperature_min"] = False
            limitations.append(f"Min temp {polymer.temp_min_c}°C, need {min_temp}°C")
            score *= 0.7

        # Chemical resistance evaluation
        chemicals = requirements.get("chemical_exposure", [])
        for chemical in chemicals:
            chem_clean = chemical.lower().replace(" ", "_")
            resistance = polymer.chemical_resistance.get(chem_clean)

            if resistance == ChemicalResistance.EXCELLENT:
                meets[f"chemical_{chemical}"] = True
                score += 0.05
            elif resistance == ChemicalResistance.GOOD:
                meets[f"chemical_{chemical}"] = True
            elif resistance == ChemicalResistance.FAIR:
                meets[f"chemical_{chemical}"] = True
                limitations.append(f"Limited resistance to {chemical}")
                score *= 0.9
            elif resistance in [ChemicalResistance.POOR, ChemicalResistance.NOT_RECOMMENDED]:
                meets[f"chemical_{chemical}"] = False
                limitations.append(f"Not resistant to {chemical}")
                score *= 0.2
            elif resistance is None:
                # No data - neutral
                pass

        # Mechanical load evaluation
        load = requirements.get("mechanical_load", "light")
        if load == "heavy":
            if polymer.tensile_strength_mpa >= 60:
                meets["mechanical"] = True
                advantages.append(f"High strength ({polymer.tensile_strength_mpa} MPa)")
            else:
                meets["mechanical"] = False
                limitations.append("Insufficient strength for heavy loads")
                score *= 0.5
        elif load == "impact":
            if polymer.elongation_percent >= 50:
                meets["mechanical"] = True
            else:
                meets["mechanical"] = False
                limitations.append("Low impact resistance")
                score *= 0.6

        # UV resistance
        if requirements.get("outdoor_uv"):
            if polymer.uv_resistant:
                meets["uv_resistant"] = True
                advantages.append("UV stable for outdoor use")
            else:
                meets["uv_resistant"] = False
                limitations.append("Not UV stable, will degrade outdoors")
                score *= 0.7

        # Food contact
        if requirements.get("food_contact"):
            if polymer.food_contact_approved:
                meets["food_contact"] = True
            else:
                meets["food_contact"] = False
                limitations.append("Not food contact approved")
                score *= 0.3

        # Sterilization
        sterilization = requirements.get("sterilization")
        if sterilization:
            if sterilization in polymer.sterilization_methods:
                meets["sterilization"] = True
                advantages.append(f"Can be {sterilization} sterilized")
            else:
                meets["sterilization"] = False
                limitations.append(f"Cannot be sterilized by {sterilization}")
                score *= 0.4

        # Cost constraint
        max_cost = constraints.get("max_cost_factor")
        if max_cost and polymer.cost_factor > max_cost:
            limitations.append(f"Cost factor {polymer.cost_factor}x exceeds budget")
            score *= 0.7

        # Low friction preference
        if constraints.get("prefer_low_friction"):
            if polymer.coefficient_friction < 0.15:
                advantages.append(f"Very low friction ({polymer.coefficient_friction})")
                score += 0.1
            elif polymer.coefficient_friction < 0.25:
                advantages.append(f"Low friction ({polymer.coefficient_friction})")
                score += 0.05

        # Add general advantages
        if polymer.water_absorption_percent < 0.1:
            advantages.append("Very low water absorption")
        if polymer.temp_max_continuous_c >= 200:
            advantages.append("High temperature capability")

        # Normalize score
        score = min(1.0, max(0.0, score))

        return score, meets, advantages, limitations

    def _generate_notes(self, polymer: PolymerSpec, requirements: Dict) -> str:
        """Generate application-specific notes"""
        notes = []

        max_temp = requirements.get("temperature_max_c", 25)
        chemicals = requirements.get("chemical_exposure", [])

        if polymer.water_absorption_percent > 1.0:
            notes.append("Absorbs moisture - dimension changes possible in humid environments")

        if "oils" in chemicals or "fuels" in chemicals:
            if polymer.family.value == "elastomer":
                if polymer.abbreviation == "EPDM":
                    notes.append("EPDM NOT suitable for oils/fuels - consider NBR or FKM")

        if polymer.abbreviation == "PTFE" and requirements.get("mechanical_load") == "heavy":
            notes.append("PTFE has low strength and creeps under load - add glass filler for structural use")

        if polymer.abbreviation == "POM" and max_temp > 80:
            notes.append("Consider PPS or PEEK for higher temperature applications")

        return " | ".join(notes) if notes else ""

    def select_for_seals(
        self,
        media: str,
        temp_c: float,
        pressure_bar: Optional[float] = None
    ) -> List[PolymerRecommendation]:
        """
        Specialized selection for seals and o-rings.

        Args:
            media: Fluid to be sealed (e.g., "hydraulic_oil", "water", "fuel")
            temp_c: Operating temperature
            pressure_bar: Operating pressure (optional)

        Returns:
            Recommended elastomers for sealing application
        """
        requirements = {
            "temperature_max_c": temp_c,
            "chemical_exposure": [media],
            "mechanical_load": "none"
        }

        # Get all recommendations
        all_recs = self.select(requirements)

        # Filter for elastomers and fluoropolymers (seal-appropriate)
        seal_families = ["elastomer", "fluoropolymer"]
        seal_recs = [r for r in all_recs if r.polymer.family.value in seal_families]

        # Add seal-specific notes
        for rec in seal_recs:
            if pressure_bar and pressure_bar > 200:
                rec.application_notes += " | High pressure: consider backup rings"

        return seal_recs

    def select_for_bearings(
        self,
        load_type: str,
        speed: str,
        lubrication: str
    ) -> List[PolymerRecommendation]:
        """
        Specialized selection for bearing and wear applications.

        Args:
            load_type: "light", "medium", "heavy"
            speed: "low", "medium", "high"
            lubrication: "dry", "oil", "grease", "water"

        Returns:
            Recommended polymers for bearing application
        """
        requirements = {
            "mechanical_load": load_type,
        }
        constraints = {
            "prefer_low_friction": True
        }

        if lubrication == "water":
            requirements["chemical_exposure"] = ["water"]
        elif lubrication in ["oil", "grease"]:
            requirements["chemical_exposure"] = ["oils"]

        all_recs = self.select(requirements, constraints)

        # Prioritize known bearing materials
        bearing_materials = ["UHMWPE", "PTFE", "Acetal", "Nylon 6/6", "PEEK"]
        bearing_recs = []

        for rec in all_recs:
            if rec.polymer.name in bearing_materials or rec.polymer.abbreviation in ["POM", "PA66"]:
                # Boost score for known bearing materials
                rec.suitability_score = min(1.0, rec.suitability_score + 0.1)
                bearing_recs.append(rec)
            else:
                bearing_recs.append(rec)

        bearing_recs.sort(key=lambda x: x.suitability_score, reverse=True)

        return bearing_recs


# Demo
if __name__ == "__main__":
    selector = PolymerSelector()

    print("=== Polymer Selection Demo ===\n")

    # High temperature oil exposure
    print("--- Selection: 200°C, oil exposure ---")
    recs = selector.select({
        "temperature_max_c": 200,
        "chemical_exposure": ["oils", "fuels"],
        "sterilization": "autoclave"
    })

    for rec in recs[:3]:
        print(f"\n{rec.polymer.name} ({rec.polymer.abbreviation}):")
        print(f"  Suitability: {rec.suitability_score:.0%}")
        print(f"  Temp margin: +{rec.temperature_margin_c:.0f}°C")
        print(f"  Cost factor: {rec.cost_factor}x")
        if rec.advantages:
            print(f"  Advantages: {', '.join(rec.advantages[:2])}")
        if rec.limitations:
            print(f"  Limitations: {', '.join(rec.limitations[:2])}")

    # Seal selection
    print("\n--- Seal Selection: hydraulic oil at 150°C ---")
    seal_recs = selector.select_for_seals("oils", 150)

    for rec in seal_recs[:3]:
        print(f"  {rec.polymer.abbreviation}: {rec.suitability_score:.0%}")
