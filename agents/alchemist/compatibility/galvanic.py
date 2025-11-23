"""
Galvanic Compatibility Analysis

Calculates galvanic corrosion risk between dissimilar metals
based on the galvanic series and environmental factors.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class CorrosionRisk(Enum):
    """Galvanic corrosion risk level"""
    NEGLIGIBLE = "negligible"    # < 50mV difference
    LOW = "low"                  # 50-150mV difference
    MODERATE = "moderate"        # 150-250mV difference
    HIGH = "high"                # 250-400mV difference
    SEVERE = "severe"            # > 400mV difference


class Environment(Enum):
    """Operating environment classification"""
    SEAWATER = "seawater"              # Full corrosion potential
    BRACKISH = "brackish"              # Partial salinity
    FRESHWATER = "freshwater"          # Low conductivity
    INDUSTRIAL = "industrial"          # Humid, polluted
    URBAN = "urban"                    # Moderate pollution
    RURAL = "rural"                    # Clean atmosphere
    CONTROLLED = "controlled"          # Indoor, dry
    IMMERSED = "immersed"              # Fully submerged (non-marine)


@dataclass
class GalvanicPair:
    """Two metals in electrical contact"""
    material_a: str
    material_b: str
    potential_a_mv: float
    potential_b_mv: float
    voltage_difference_mv: float
    anode: str          # Material that will corrode
    cathode: str        # Material that will be protected
    risk: CorrosionRisk
    environment: Environment
    effective_risk_mv: float  # After environment adjustment


@dataclass
class MitigationStrategy:
    """Strategy to prevent galvanic corrosion"""
    method: str
    effectiveness: float  # 0-1
    cost_factor: float
    implementation_notes: str


@dataclass
class GalvanicAssessment:
    """Complete galvanic compatibility assessment"""
    pair: GalvanicPair
    compatible: bool
    risk_description: str
    mitigation_strategies: List[MitigationStrategy]
    material_substitutions: List[str]
    inspection_interval_months: Optional[int]


class GalvanicSeries:
    """
    Galvanic series of metals and alloys.

    Potential values are referenced to Saturated Calomel Electrode (SCE)
    in flowing seawater at 25°C.
    """

    def __init__(self):
        # Galvanic series: more negative = more anodic (will corrode first)
        self._series: Dict[str, float] = {
            # Active (anodic) end
            "magnesium": -1.60,
            "magnesium_alloy": -1.55,
            "zinc": -1.10,
            "galvanized_steel": -1.05,
            "aluminum_1100": -0.90,
            "aluminum_5052": -0.85,
            "aluminum_6061": -0.75,
            "aluminum_7075": -0.73,
            "cadmium": -0.70,
            "mild_steel": -0.60,
            "carbon_steel": -0.60,
            "cast_iron": -0.55,
            "low_alloy_steel": -0.55,
            "4140_steel": -0.52,

            # Stainless steels (active state)
            "304_stainless_active": -0.50,
            "316_stainless_active": -0.45,
            "410_stainless_active": -0.52,

            # Intermediate
            "lead": -0.45,
            "tin": -0.40,
            "nickel_active": -0.35,
            "brasses": -0.30,
            "yellow_brass": -0.30,
            "naval_brass": -0.28,
            "copper": -0.20,
            "bronze": -0.18,
            "silicon_bronze": -0.18,
            "phosphor_bronze": -0.17,
            "copper_nickel_70_30": -0.15,
            "copper_nickel_90_10": -0.18,

            # Stainless steels (passive state)
            "316_stainless_passive": 0.05,
            "304_stainless_passive": 0.08,
            "17_4ph_stainless": 0.05,
            "duplex_stainless": 0.10,

            # Noble (cathodic) end
            "nickel_passive": 0.00,
            "monel_400": 0.00,
            "monel_k500": 0.02,
            "inconel_600": 0.05,
            "inconel_625": 0.05,
            "inconel_718": 0.05,
            "hastelloy_c276": 0.08,
            "titanium": 0.10,
            "ti_6al_4v": 0.10,
            "silver": 0.15,
            "graphite": 0.25,
            "gold": 0.35,
            "platinum": 0.40,
        }

        # Common name aliases
        self._aliases = {
            "stainless_steel": "304_stainless_passive",
            "stainless": "304_stainless_passive",
            "ss304": "304_stainless_passive",
            "ss316": "316_stainless_passive",
            "316l": "316_stainless_passive",
            "304l": "304_stainless_passive",
            "6061": "aluminum_6061",
            "7075": "aluminum_7075",
            "5052": "aluminum_5052",
            "aluminum": "aluminum_6061",
            "steel": "carbon_steel",
            "iron": "cast_iron",
            "brass": "yellow_brass",
            "bronze_silicon": "silicon_bronze",
            "cupronickel": "copper_nickel_70_30",
            "monel": "monel_400",
            "inconel": "inconel_625",
            "hastelloy": "hastelloy_c276",
        }

    def get_potential(self, material: str) -> Optional[float]:
        """Get galvanic potential for a material"""
        # Normalize material name
        normalized = material.lower().replace(" ", "_").replace("-", "_")

        # Check aliases first
        if normalized in self._aliases:
            normalized = self._aliases[normalized]

        return self._series.get(normalized)

    def list_materials(self) -> List[str]:
        """List all materials in galvanic series"""
        return list(self._series.keys())


class GalvanicCalculator:
    """
    Calculator for galvanic corrosion risk.

    Analyzes material pairs and provides risk assessment
    with mitigation strategies.
    """

    # Environment adjustment factors
    ENVIRONMENT_FACTORS = {
        Environment.SEAWATER: 1.0,
        Environment.BRACKISH: 0.8,
        Environment.IMMERSED: 0.6,
        Environment.FRESHWATER: 0.3,
        Environment.INDUSTRIAL: 0.5,
        Environment.URBAN: 0.3,
        Environment.RURAL: 0.15,
        Environment.CONTROLLED: 0.05,
    }

    def __init__(self):
        self.series = GalvanicSeries()

    def calculate_risk(
        self,
        material_a: str,
        material_b: str,
        environment: Environment = Environment.INDUSTRIAL
    ) -> GalvanicAssessment:
        """
        Calculate galvanic corrosion risk between two materials.

        Args:
            material_a: First material
            material_b: Second material
            environment: Operating environment

        Returns:
            GalvanicAssessment with risk analysis and mitigation strategies
        """
        pot_a = self.series.get_potential(material_a)
        pot_b = self.series.get_potential(material_b)

        if pot_a is None:
            raise ValueError(f"Unknown material: {material_a}")
        if pot_b is None:
            raise ValueError(f"Unknown material: {material_b}")

        # Calculate voltage difference (in mV)
        voltage_diff = abs(pot_a - pot_b) * 1000

        # Determine anode (corrodes) and cathode (protected)
        if pot_a < pot_b:
            anode, cathode = material_a, material_b
        else:
            anode, cathode = material_b, material_a

        # Apply environment factor
        env_factor = self.ENVIRONMENT_FACTORS.get(environment, 0.5)
        effective_risk = voltage_diff * env_factor

        # Determine risk level
        risk = self._classify_risk(effective_risk)

        # Create galvanic pair
        pair = GalvanicPair(
            material_a=material_a,
            material_b=material_b,
            potential_a_mv=pot_a * 1000,
            potential_b_mv=pot_b * 1000,
            voltage_difference_mv=voltage_diff,
            anode=anode,
            cathode=cathode,
            risk=risk,
            environment=environment,
            effective_risk_mv=effective_risk
        )

        # Determine compatibility
        compatible = risk in [CorrosionRisk.NEGLIGIBLE, CorrosionRisk.LOW]

        # Generate risk description
        risk_desc = self._describe_risk(pair)

        # Generate mitigation strategies
        mitigations = self._get_mitigations(pair)

        # Suggest material substitutions
        substitutions = self._suggest_substitutions(anode, cathode)

        # Suggest inspection interval
        inspection = self._get_inspection_interval(risk, environment)

        return GalvanicAssessment(
            pair=pair,
            compatible=compatible,
            risk_description=risk_desc,
            mitigation_strategies=mitigations,
            material_substitutions=substitutions,
            inspection_interval_months=inspection
        )

    def _classify_risk(self, effective_mv: float) -> CorrosionRisk:
        """Classify risk based on effective voltage difference"""
        if effective_mv < 50:
            return CorrosionRisk.NEGLIGIBLE
        elif effective_mv < 150:
            return CorrosionRisk.LOW
        elif effective_mv < 250:
            return CorrosionRisk.MODERATE
        elif effective_mv < 400:
            return CorrosionRisk.HIGH
        else:
            return CorrosionRisk.SEVERE

    def _describe_risk(self, pair: GalvanicPair) -> str:
        """Generate human-readable risk description"""
        descriptions = {
            CorrosionRisk.NEGLIGIBLE: (
                f"Negligible risk. {pair.material_a} and {pair.material_b} are "
                f"galvanically compatible ({pair.effective_risk_mv:.0f}mV effective)."
            ),
            CorrosionRisk.LOW: (
                f"Low risk. Minor galvanic corrosion possible over time. "
                f"{pair.anode} may show surface discoloration after extended exposure."
            ),
            CorrosionRisk.MODERATE: (
                f"Moderate risk. {pair.anode} will corrode in contact with "
                f"{pair.cathode}. Isolation or protection recommended."
            ),
            CorrosionRisk.HIGH: (
                f"HIGH RISK. {pair.anode} will corrode rapidly when in contact "
                f"with {pair.cathode} ({pair.voltage_difference_mv:.0f}mV difference). "
                f"Isolation required."
            ),
            CorrosionRisk.SEVERE: (
                f"SEVERE RISK. {pair.anode} will experience accelerated corrosion "
                f"and potential failure. This material combination is not recommended. "
                f"Change materials or implement multiple isolation methods."
            ),
        }
        return descriptions.get(pair.risk, "Unknown risk level")

    def _get_mitigations(self, pair: GalvanicPair) -> List[MitigationStrategy]:
        """Generate mitigation strategies based on risk"""
        mitigations = []

        if pair.risk == CorrosionRisk.NEGLIGIBLE:
            return mitigations

        # Basic isolation
        if pair.risk.value in ["low", "moderate", "high", "severe"]:
            mitigations.append(MitigationStrategy(
                method="Dielectric isolation (nylon washer, sleeve)",
                effectiveness=0.9,
                cost_factor=1.0,
                implementation_notes="Insert non-conductive material between metals"
            ))

        if pair.risk.value in ["moderate", "high", "severe"]:
            mitigations.append(MitigationStrategy(
                method="Dielectric grease/compound",
                effectiveness=0.7,
                cost_factor=1.0,
                implementation_notes="Apply to joint surfaces to prevent electrolyte contact"
            ))

        if pair.risk.value in ["high", "severe"]:
            mitigations.append(MitigationStrategy(
                method="Sacrificial anode (zinc)",
                effectiveness=0.95,
                cost_factor=1.5,
                implementation_notes="Add zinc anode in electrical contact with both metals"
            ))
            mitigations.append(MitigationStrategy(
                method="Barrier coating (paint, powder coat)",
                effectiveness=0.85,
                cost_factor=2.0,
                implementation_notes="Coat the cathodic material to reduce area ratio"
            ))

        if pair.risk == CorrosionRisk.SEVERE:
            mitigations.append(MitigationStrategy(
                method="Material substitution",
                effectiveness=1.0,
                cost_factor=3.0,
                implementation_notes="Replace one material with galvanically compatible alternative"
            ))
            mitigations.append(MitigationStrategy(
                method="Cathodic protection system",
                effectiveness=0.98,
                cost_factor=5.0,
                implementation_notes="Impressed current or extensive sacrificial anode system"
            ))

        return mitigations

    def _suggest_substitutions(self, anode: str, cathode: str) -> List[str]:
        """Suggest material substitutions to improve compatibility"""
        suggestions = []

        # Aluminum + stainless steel is common problem
        if "aluminum" in anode.lower() and "stainless" in cathode.lower():
            suggestions.append(
                f"Replace {cathode} with 6000-series aluminum for best compatibility"
            )
            suggestions.append(
                f"Use 5000-series aluminum (marine grade) if aluminum must contact stainless"
            )

        # Carbon steel + copper alloys
        if "steel" in anode.lower() and "copper" in cathode.lower():
            suggestions.append(
                f"Replace {anode} with stainless steel or apply zinc coating"
            )
            suggestions.append(
                "Consider brass or bronze fittings with dielectric unions"
            )

        # General suggestions based on anode
        if "aluminum" in anode.lower():
            suggestions.append(
                "For aluminum protection: anodize or use chromate conversion coating"
            )
        if "steel" in anode.lower():
            suggestions.append(
                "For steel protection: galvanize, paint, or use zinc-rich primer"
            )

        return suggestions

    def _get_inspection_interval(
        self,
        risk: CorrosionRisk,
        environment: Environment
    ) -> Optional[int]:
        """Recommend inspection interval in months"""
        base_intervals = {
            CorrosionRisk.NEGLIGIBLE: None,  # No special inspection needed
            CorrosionRisk.LOW: 24,
            CorrosionRisk.MODERATE: 12,
            CorrosionRisk.HIGH: 6,
            CorrosionRisk.SEVERE: 3,
        }

        base = base_intervals.get(risk)
        if base is None:
            return None

        # Adjust for environment
        if environment in [Environment.SEAWATER, Environment.BRACKISH]:
            base = base // 2
        elif environment == Environment.CONTROLLED:
            base = base * 2

        return max(1, base)


# Demo
if __name__ == "__main__":
    calc = GalvanicCalculator()

    print("=== Galvanic Compatibility Demo ===\n")

    # Test: Aluminum + Stainless Steel (common problem)
    result = calc.calculate_risk(
        "aluminum_6061",
        "316_stainless_passive",
        Environment.SEAWATER
    )

    print(f"Materials: {result.pair.material_a} + {result.pair.material_b}")
    print(f"Voltage difference: {result.pair.voltage_difference_mv:.0f} mV")
    print(f"Risk: {result.pair.risk.value.upper()}")
    print(f"Compatible: {result.compatible}")
    print(f"\n{result.risk_description}")

    if result.mitigation_strategies:
        print("\nMitigation strategies:")
        for m in result.mitigation_strategies[:3]:
            print(f"  - {m.method} ({m.effectiveness:.0%} effective)")

    if result.inspection_interval_months:
        print(f"\nRecommended inspection: Every {result.inspection_interval_months} months")
