"""
Galvanic Corrosion Calculator

Calculates corrosion risk when two metals are in contact in marine environments.
This is THE core marine specialty - more marine hardware fails from galvanic
corrosion than any other cause.

Reference: ASTM G82, MIL-STD-889
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

from .material_series import (
    GalvanicSeries,
    MarineEnvironment,
    ENVIRONMENT_FACTORS,
    SAFE_COUPLES,
    DANGEROUS_COUPLES,
)


class RiskLevel(Enum):
    """Galvanic corrosion risk classification"""
    MINIMAL = "MINIMAL"      # < 100 mV effective
    LOW = "LOW"              # 100-200 mV effective
    MODERATE = "MODERATE"    # 200-350 mV effective
    HIGH = "HIGH"            # 350-500 mV effective
    SEVERE = "SEVERE"        # > 500 mV effective


@dataclass
class GalvanicRisk:
    """Assessment of galvanic corrosion risk between two materials"""
    risk_level: RiskLevel
    voltage_difference_mv: float
    effective_voltage_mv: float  # After environment factor
    anode_material: str          # Will corrode (sacrifice)
    cathode_material: str        # Will be protected
    corrosion_rate: str          # Qualitative rate description
    time_to_damage: str          # Expected time to visible damage
    recommendations: List[str]
    zinc_specification: Optional[str]
    isolation_method: Optional[str]
    anode_area_ratio: Optional[str]


@dataclass
class GalvanicPair:
    """Two metals in contact in a marine environment"""
    anode_material: str
    cathode_material: str
    environment: MarineEnvironment
    voltage_difference_mv: float
    effective_voltage_mv: float
    risk: GalvanicRisk
    area_ratio: Optional[float] = None  # anode area / cathode area


@dataclass
class IsolationRecommendation:
    """Recommendation for isolating incompatible metals"""
    method: str
    product_examples: List[str]
    effectiveness: float  # 0-1
    installation_notes: str


class GalvanicCorrosionCalculator:
    """
    Calculator for galvanic corrosion risk assessment.

    This is the heart of marine materials compatibility analysis.
    """

    def __init__(self):
        self.galvanic_series = GalvanicSeries()
        self._isolation_methods = self._init_isolation_methods()

    def _init_isolation_methods(self) -> Dict[str, IsolationRecommendation]:
        """Initialize isolation method database"""
        return {
            "nylon_washer": IsolationRecommendation(
                method="Nylon/Delrin isolation washer",
                product_examples=[
                    "McMaster 90295A029",
                    "Tef-Cap nylon isolation kit",
                ],
                effectiveness=0.85,
                installation_notes="Use nylon washer under bolt head AND nut. Sleeve the bolt shank if through dissimilar metal."
            ),
            "dielectric_grease": IsolationRecommendation(
                method="Dielectric grease",
                product_examples=[
                    "Permatex 22058 Dielectric Grease",
                    "3M Scotchkote",
                    "LPS Cold Galvanize",
                ],
                effectiveness=0.70,
                installation_notes="Apply liberally to all contact surfaces. Re-apply annually. Does NOT replace mechanical isolation."
            ),
            "isolation_sleeve": IsolationRecommendation(
                method="Full bolt isolation kit",
                product_examples=[
                    "PTFE bolt sleeves",
                    "Garlock isolation kits",
                    "GPT Industries isolation sets",
                ],
                effectiveness=0.95,
                installation_notes="Completely isolates bolt from one or both materials. Required for HIGH/SEVERE risk pairs."
            ),
            "barrier_coating": IsolationRecommendation(
                method="Barrier coating on anode material",
                product_examples=[
                    "3M Scotchkote 323",
                    "Tectyl 506",
                    "Zinc-rich primer",
                ],
                effectiveness=0.80,
                installation_notes="Apply thick coating to anodic material. Touch-up any damage immediately."
            ),
            "sacrificial_anode": IsolationRecommendation(
                method="Sacrificial zinc/aluminum anode",
                product_examples=[
                    "MIL-A-18001K zinc anode",
                    "MIL-DTL-24779 aluminum anode",
                ],
                effectiveness=0.90,
                installation_notes="Install anode in electrical contact with protected metal. Replace when 50% consumed."
            ),
        }

    def calculate_risk(
        self,
        metal_a: str,
        metal_b: str,
        environment: MarineEnvironment,
        anode_cathode_area_ratio: Optional[float] = None
    ) -> GalvanicRisk:
        """
        Calculate galvanic corrosion risk between two metals.

        Args:
            metal_a: First metal (name or alias)
            metal_b: Second metal (name or alias)
            environment: Marine environment type
            anode_cathode_area_ratio: Ratio of anode to cathode area (larger = better)

        Returns:
            GalvanicRisk assessment with recommendations
        """
        # Get galvanic potentials
        pot_a = self.galvanic_series.get_potential(metal_a)
        pot_b = self.galvanic_series.get_potential(metal_b)

        if pot_a is None:
            raise ValueError(f"Unknown material: {metal_a}")
        if pot_b is None:
            raise ValueError(f"Unknown material: {metal_b}")

        # Calculate voltage difference
        voltage_diff_mv = abs(pot_a - pot_b) * 1000

        # Determine anode and cathode
        if pot_a < pot_b:
            anode, cathode = metal_a, metal_b
        else:
            anode, cathode = metal_b, metal_a

        # Apply environment factor
        env_factor = ENVIRONMENT_FACTORS.get(environment, 1.0)
        effective_voltage = voltage_diff_mv * env_factor

        # Adjust for area ratio (small anode + large cathode = VERY BAD)
        area_ratio_note = None
        if anode_cathode_area_ratio is not None:
            if anode_cathode_area_ratio < 0.1:
                effective_voltage *= 2.0
                area_ratio_note = "CRITICAL: Small anode + large cathode - corrosion rate doubled"
            elif anode_cathode_area_ratio < 0.5:
                effective_voltage *= 1.3
                area_ratio_note = "WARNING: Unfavorable area ratio - corrosion rate increased"
            elif anode_cathode_area_ratio > 2.0:
                effective_voltage *= 0.8
                area_ratio_note = "Favorable: Large anode area distributes corrosion"

        # Determine risk level and time to damage
        if effective_voltage < 100:
            risk_level = RiskLevel.MINIMAL
            corrosion_rate = "Negligible"
            time_to_damage = "Many years if at all"
        elif effective_voltage < 200:
            risk_level = RiskLevel.LOW
            corrosion_rate = "Slow, minimal practical impact"
            time_to_damage = "3-5+ years to notice"
        elif effective_voltage < 350:
            risk_level = RiskLevel.MODERATE
            corrosion_rate = "Noticeable over time"
            time_to_damage = "1-2 years to visible damage"
        elif effective_voltage < 500:
            risk_level = RiskLevel.HIGH
            corrosion_rate = "Significant, requires mitigation"
            time_to_damage = "Months to visible damage"
        else:
            risk_level = RiskLevel.SEVERE
            corrosion_rate = "Rapid destruction"
            time_to_damage = "Weeks to failure"

        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_level,
            effective_voltage,
            anode,
            cathode,
            environment,
        )

        # Determine zinc specification if needed
        zinc_spec = None
        isolation_method = None

        if effective_voltage > 200:
            if environment == MarineEnvironment.FRESHWATER:
                zinc_spec = "ASTM B843 Type M1C (magnesium) for freshwater"
            else:
                zinc_spec = "MIL-A-18001K (zinc anode) or MIL-DTL-24779 (aluminum anode)"

        if effective_voltage > 100:
            isolation_method = self._recommend_isolation(risk_level, environment)

        return GalvanicRisk(
            risk_level=risk_level,
            voltage_difference_mv=voltage_diff_mv,
            effective_voltage_mv=effective_voltage,
            anode_material=anode,
            cathode_material=cathode,
            corrosion_rate=corrosion_rate,
            time_to_damage=time_to_damage,
            recommendations=recommendations,
            zinc_specification=zinc_spec,
            isolation_method=isolation_method,
            anode_area_ratio=area_ratio_note,
        )

    def _generate_recommendations(
        self,
        risk_level: RiskLevel,
        effective_voltage: float,
        anode: str,
        cathode: str,
        environment: MarineEnvironment,
    ) -> List[str]:
        """Generate specific recommendations based on risk assessment"""
        recommendations = []

        if risk_level == RiskLevel.MINIMAL:
            recommendations.append("Acceptable combination for marine use")
            recommendations.append("Standard stainless fasteners are appropriate")
            return recommendations

        # Low risk
        if risk_level == RiskLevel.LOW:
            recommendations.append("Generally acceptable with basic precautions")
            recommendations.append("Apply dielectric grease to joint surfaces")
            recommendations.append("Inspect annually for early signs of corrosion")

        # Moderate risk
        if risk_level == RiskLevel.MODERATE:
            recommendations.append(f"Isolate {anode} from {cathode} with nylon/plastic washers")
            recommendations.append("Apply dielectric grease to all contact surfaces")
            recommendations.append("Consider barrier coating on anodic material")
            recommendations.append("Inspect every 6 months")

        # High risk
        if risk_level == RiskLevel.HIGH:
            recommendations.insert(0, f"WARNING: {anode} will corrode significantly near {cathode}")
            recommendations.append("Full electrical isolation required (bolt sleeves + washers)")
            recommendations.append(f"Strongly recommend replacing {anode} with compatible material")
            recommendations.append("Install sacrificial anode near junction")
            recommendations.append("Monthly inspection recommended")

        # Severe risk
        if risk_level == RiskLevel.SEVERE:
            recommendations.insert(0, f"CRITICAL: Do NOT use {anode} in contact with {cathode}")
            recommendations.insert(1, f"Rapid corrosion WILL occur - {anode} will be destroyed")
            recommendations.append("Complete redesign required - choose compatible materials")
            recommendations.append("If unavoidable, use complete isolation system + sacrificial anodes")
            recommendations.append("Weekly inspection required if used")

        # Environment-specific
        if environment == MarineEnvironment.SPLASH_ZONE:
            recommendations.append("SPLASH ZONE: Highest corrosion risk area - extra vigilance required")

        if environment == MarineEnvironment.TROPICAL:
            recommendations.append("TROPICAL: Warm water accelerates corrosion - shorter inspection intervals")

        return recommendations

    def _recommend_isolation(
        self,
        risk_level: RiskLevel,
        environment: MarineEnvironment
    ) -> str:
        """Recommend isolation method based on risk"""
        if risk_level in [RiskLevel.SEVERE, RiskLevel.HIGH]:
            return "Full isolation kit (PTFE sleeve + washers) + sacrificial anode"
        elif risk_level == RiskLevel.MODERATE:
            return "Nylon isolation washers + dielectric grease"
        else:
            return "Dielectric grease application"

    def analyze_fastener_joint(
        self,
        fastener_material: str,
        base_material: str,
        environment: MarineEnvironment,
        fastener_quantity: int = 1
    ) -> Dict:
        """
        Analyze a fastener joint for galvanic compatibility.

        Fastener joints are the #1 source of galvanic corrosion problems
        because fasteners are small (unfavorable anode/cathode ratio).

        Args:
            fastener_material: Material of bolt/screw
            base_material: Material being fastened
            environment: Marine environment
            fastener_quantity: Number of fasteners (more = better)

        Returns:
            Detailed joint analysis
        """
        # Assume unfavorable area ratio for single fastener
        area_ratio = 0.05 * fastener_quantity

        risk = self.calculate_risk(
            fastener_material,
            base_material,
            environment,
            anode_cathode_area_ratio=area_ratio,
        )

        # Determine which material will be sacrificed
        if risk.anode_material == fastener_material:
            failure_mode = "Fastener will corrode - STRUCTURAL FAILURE RISK"
            critical = True
        else:
            failure_mode = "Base material will corrode around fastener - cosmetic then structural"
            critical = False

        return {
            "risk_assessment": risk,
            "failure_mode": failure_mode,
            "critical_failure_risk": critical,
            "recommended_fastener": self._recommend_fastener_for_base(base_material, environment),
            "isolation_kit_needed": risk.risk_level in [RiskLevel.HIGH, RiskLevel.SEVERE, RiskLevel.MODERATE],
            "notes": self._get_fastener_notes(fastener_material, base_material),
        }

    def _recommend_fastener_for_base(
        self,
        base_material: str,
        environment: MarineEnvironment
    ) -> str:
        """Recommend best fastener material for a base material"""
        base_lower = base_material.lower()

        if "aluminum" in base_lower:
            return "316 stainless with isolation OR aluminum fastener (weaker)"

        if "stainless" in base_lower or "316" in base_lower:
            return "316 stainless (same material = no galvanic couple)"

        if "bronze" in base_lower or "copper" in base_lower:
            return "Silicon bronze (traditional) or Monel (premium)"

        if "wood" in base_lower or "fiberglass" in base_lower:
            return "316 stainless (most versatile) or silicon bronze (traditional)"

        if "steel" in base_lower:
            return "316 stainless with isolation OR zinc-plated steel with barrier coating"

        return "316 stainless steel (marine standard)"

    def _get_fastener_notes(self, fastener: str, base: str) -> List[str]:
        """Get specific notes for fastener/base combination"""
        notes = []
        fastener_lower = fastener.lower()
        base_lower = base.lower()

        # Common problematic combinations
        if "aluminum" in base_lower and "stainless" in fastener_lower:
            notes.append("VERY COMMON MISTAKE: Always isolate stainless from aluminum")
            notes.append("Use nylon washers under head and nut")
            notes.append("Apply Tef-Gel or Lanocote to threads")

        if "bronze" in fastener_lower and "stainless" in base_lower:
            notes.append("Bronze fasteners in stainless = bronze will corrode")
            notes.append("Use stainless fasteners in stainless base")

        if "304" in fastener_lower:
            notes.append("304 stainless: OK for freshwater, will pit in saltwater")
            notes.append("Upgrade to 316 stainless for ocean use")

        return notes

    def check_known_dangerous_couple(
        self,
        metal_a: str,
        metal_b: str
    ) -> Optional[str]:
        """Check if this is a known dangerous combination"""
        a_lower = metal_a.lower()
        b_lower = metal_b.lower()

        for mat_1, mat_2, warning in DANGEROUS_COUPLES:
            if (mat_1 in a_lower and mat_2 in b_lower) or \
               (mat_1 in b_lower and mat_2 in a_lower):
                return warning

        return None

    def check_known_safe_couple(
        self,
        metal_a: str,
        metal_b: str
    ) -> bool:
        """Check if this is a known safe combination"""
        for mat_1, mat_2 in SAFE_COUPLES:
            a_norm = metal_a.lower().replace(" ", "_").replace("-", "_")
            b_norm = metal_b.lower().replace(" ", "_").replace("-", "_")

            if (mat_1 in a_norm and mat_2 in b_norm) or \
               (mat_1 in b_norm and mat_2 in a_norm):
                return True

        return False
