"""
Agent_18: ALCHEMIST - Materials Science Intelligence

The foundation of all parts compatibility decisions. What material?
Will it corrode? Will it fail at temperature? What's the best choice?

Domains:
- Metals & alloys (steel, aluminum, titanium, copper, exotic)
- Polymers & plastics (engineering plastics, elastomers)
- Composites (carbon fiber, fiberglass, Kevlar)
- Ceramics & advanced materials
- Coatings & surface treatments
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from decimal import Decimal


class MaterialFamily(Enum):
    """Primary material classification"""
    FERROUS = "ferrous"              # Steel, iron, stainless
    ALUMINUM = "aluminum"            # All aluminum alloys
    TITANIUM = "titanium"            # Ti alloys
    COPPER = "copper"                # Copper, brass, bronze
    NICKEL = "nickel"                # Inconel, Monel, Hastelloy
    POLYMER = "polymer"              # Plastics, rubbers
    COMPOSITE = "composite"          # Carbon fiber, fiberglass
    CERAMIC = "ceramic"              # Technical ceramics
    REFRACTORY = "refractory"        # Tungsten, molybdenum


class CorrosionResistance(Enum):
    """Corrosion resistance classification"""
    POOR = "poor"           # Unprotected carbon steel
    FAIR = "fair"           # Protected carbon steel, some Al alloys
    GOOD = "good"           # 300 series stainless, most Al
    EXCELLENT = "excellent"  # 316SS, titanium, Inconel
    INERT = "inert"         # PTFE, ceramics, gold


@dataclass
class MaterialProperties:
    """Core material properties for compatibility assessment"""
    # Identity
    designation: str          # "6061-T6", "316L", "PEEK"
    family: MaterialFamily
    standard: str             # "AA", "AISI", "ASTM"

    # Mechanical properties
    tensile_strength_mpa: float
    yield_strength_mpa: float
    elongation_percent: float
    hardness: str             # "HRC 30-35" or "HRB 85"
    modulus_gpa: float        # Young's modulus

    # Thermal properties
    melting_point_c: Optional[float]
    max_service_temp_c: float
    thermal_conductivity_w_mk: float
    thermal_expansion_um_mk: float  # Coefficient of thermal expansion

    # Corrosion & Environment
    corrosion_resistance: CorrosionResistance
    galvanic_series_position: float  # -1.0 (anodic) to +1.0 (cathodic)

    # Additional properties
    density_g_cm3: float
    electrical_conductivity_percent_iacs: Optional[float] = None
    magnetic: bool = False
    weldable: bool = True
    machinability_rating: Optional[int] = None  # 0-100 scale


@dataclass
class GalvanicPair:
    """Two materials in electrical contact"""
    material_a: str
    material_b: str
    voltage_difference_mv: float
    anode: str              # Material that will corrode
    cathode: str            # Material that will be protected
    corrosion_rate_factor: float  # Relative rate multiplier

    @property
    def is_problematic(self) -> bool:
        """Voltage difference > 250mV is generally problematic"""
        return self.voltage_difference_mv > 250


@dataclass
class MaterialRecommendation:
    """A recommended material for an application"""
    material: str
    designation: str
    suitability_score: float  # 0-1
    properties: MaterialProperties
    meets_requirements: Dict[str, bool]
    advantages: List[str]
    limitations: List[str]
    cost_factor: float  # Relative cost (1.0 = baseline carbon steel)
    availability: str   # "common", "specialty", "exotic"


@dataclass
class AlloyCrossReference:
    """Cross-reference between alloy standards"""
    source_designation: str
    source_standard: str
    target_designation: str
    target_standard: str
    equivalence: str  # "exact", "approximate", "similar"
    composition_differences: Dict[str, Dict[str, str]]
    property_differences: Dict[str, Dict[str, float]]
    notes: str


@dataclass
class MaterialCompatibility:
    """Compatibility assessment between two materials"""
    material_a: str
    material_b: str
    compatible: bool
    issue: Optional[str]
    galvanic_data: Optional[GalvanicPair]
    mitigation_options: List[str]
    environment_notes: Dict[str, str]


class AlchemistAgent:
    """
    Agent_18: ALCHEMIST - Materials Science Intelligence

    Core responsibilities:
    1. Material property lookup and comparison
    2. Alloy cross-referencing across standards
    3. Galvanic compatibility assessment
    4. Material selection for applications
    5. Polymer selection for temperature/chemical exposure
    """

    def __init__(self):
        self.alloy_database = self._initialize_alloy_database()
        self.polymer_database = self._initialize_polymer_database()
        self.galvanic_series = self._initialize_galvanic_series()

    def _initialize_alloy_database(self) -> Dict[str, MaterialProperties]:
        """Initialize common alloy database"""
        # This would be loaded from database in production
        return {
            "6061-T6": MaterialProperties(
                designation="6061-T6",
                family=MaterialFamily.ALUMINUM,
                standard="AA",
                tensile_strength_mpa=310,
                yield_strength_mpa=276,
                elongation_percent=12,
                hardness="HB 95",
                modulus_gpa=68.9,
                melting_point_c=582,
                max_service_temp_c=150,
                thermal_conductivity_w_mk=167,
                thermal_expansion_um_mk=23.6,
                corrosion_resistance=CorrosionResistance.GOOD,
                galvanic_series_position=-0.75,
                density_g_cm3=2.70,
                electrical_conductivity_percent_iacs=43,
                magnetic=False,
                weldable=True,
                machinability_rating=85
            ),
            "316L": MaterialProperties(
                designation="316L",
                family=MaterialFamily.FERROUS,
                standard="AISI",
                tensile_strength_mpa=485,
                yield_strength_mpa=170,
                elongation_percent=40,
                hardness="HRB 79",
                modulus_gpa=193,
                melting_point_c=1400,
                max_service_temp_c=870,
                thermal_conductivity_w_mk=16.3,
                thermal_expansion_um_mk=16.0,
                corrosion_resistance=CorrosionResistance.EXCELLENT,
                galvanic_series_position=0.0,  # Reference point
                density_g_cm3=8.00,
                electrical_conductivity_percent_iacs=2.3,
                magnetic=False,
                weldable=True,
                machinability_rating=45
            ),
            "Ti-6Al-4V": MaterialProperties(
                designation="Ti-6Al-4V",
                family=MaterialFamily.TITANIUM,
                standard="AMS",
                tensile_strength_mpa=950,
                yield_strength_mpa=880,
                elongation_percent=14,
                hardness="HRC 36",
                modulus_gpa=113.8,
                melting_point_c=1660,
                max_service_temp_c=400,
                thermal_conductivity_w_mk=6.7,
                thermal_expansion_um_mk=8.6,
                corrosion_resistance=CorrosionResistance.EXCELLENT,
                galvanic_series_position=0.05,
                density_g_cm3=4.43,
                electrical_conductivity_percent_iacs=1.0,
                magnetic=False,
                weldable=True,
                machinability_rating=22
            ),
            "Inconel 718": MaterialProperties(
                designation="Inconel 718",
                family=MaterialFamily.NICKEL,
                standard="AMS",
                tensile_strength_mpa=1375,
                yield_strength_mpa=1100,
                elongation_percent=21,
                hardness="HRC 44",
                modulus_gpa=208,
                melting_point_c=1336,
                max_service_temp_c=700,
                thermal_conductivity_w_mk=11.4,
                thermal_expansion_um_mk=13.0,
                corrosion_resistance=CorrosionResistance.EXCELLENT,
                galvanic_series_position=0.02,
                density_g_cm3=8.19,
                electrical_conductivity_percent_iacs=1.6,
                magnetic=False,
                weldable=True,
                machinability_rating=12
            ),
        }

    def _initialize_polymer_database(self) -> Dict[str, Dict]:
        """Initialize common polymer database"""
        return {
            "PEEK": {
                "full_name": "Polyether Ether Ketone",
                "temp_range_c": (-60, 260),
                "temp_continuous_c": 250,
                "chemical_resistance": ["acids", "bases", "hydrocarbons", "solvents"],
                "chemical_weakness": ["concentrated sulfuric acid"],
                "strength_mpa": 100,
                "applications": ["aerospace", "medical", "oil_gas"],
                "cost_factor": 15.0,
                "sterilizable": ["autoclave", "gamma", "eto"]
            },
            "PTFE": {
                "full_name": "Polytetrafluoroethylene (Teflon)",
                "temp_range_c": (-200, 260),
                "temp_continuous_c": 260,
                "chemical_resistance": ["all"],
                "chemical_weakness": [],
                "strength_mpa": 25,
                "applications": ["seals", "bearings", "chemical"],
                "cost_factor": 8.0,
                "sterilizable": ["autoclave", "gamma", "eto"]
            },
            "Viton": {
                "full_name": "Fluoroelastomer (FKM)",
                "temp_range_c": (-20, 200),
                "temp_continuous_c": 200,
                "chemical_resistance": ["oils", "fuels", "hydraulic_fluid", "acids"],
                "chemical_weakness": ["ketones", "esters", "amines"],
                "strength_mpa": 15,
                "applications": ["seals", "o-rings", "gaskets"],
                "cost_factor": 5.0,
                "sterilizable": ["autoclave"]
            },
            "UHMWPE": {
                "full_name": "Ultra-High Molecular Weight Polyethylene",
                "temp_range_c": (-200, 80),
                "temp_continuous_c": 80,
                "chemical_resistance": ["acids", "bases", "alcohols"],
                "chemical_weakness": ["aromatic_hydrocarbons", "chlorinated_solvents"],
                "strength_mpa": 40,
                "applications": ["wear_parts", "bearings", "medical_implants"],
                "cost_factor": 3.0,
                "sterilizable": ["gamma", "eto"]
            },
        }

    def _initialize_galvanic_series(self) -> Dict[str, float]:
        """
        Initialize galvanic series (seawater reference)
        More negative = more anodic (will corrode)
        More positive = more cathodic (will be protected)
        """
        return {
            "magnesium": -1.60,
            "zinc": -1.10,
            "aluminum_5052": -0.85,
            "aluminum_6061": -0.75,
            "cadmium": -0.70,
            "carbon_steel": -0.60,
            "cast_iron": -0.55,
            "304_stainless_active": -0.50,
            "lead": -0.45,
            "tin": -0.40,
            "nickel_active": -0.35,
            "brass": -0.30,
            "copper": -0.20,
            "bronze": -0.18,
            "316_stainless_active": -0.05,
            "nickel_passive": 0.00,
            "316_stainless_passive": 0.05,
            "304_stainless_passive": 0.08,
            "titanium": 0.10,
            "silver": 0.15,
            "graphite": 0.25,
            "gold": 0.35,
            "platinum": 0.40,
        }

    def get_material_properties(self, designation: str) -> Optional[MaterialProperties]:
        """Look up material properties by designation"""
        return self.alloy_database.get(designation)

    def cross_reference_alloy(
        self,
        alloy: str,
        source_standard: str,
        target_standard: str
    ) -> AlloyCrossReference:
        """
        Cross-reference alloy designations across standards.

        Example: 6061-T6 (AA) -> EN AW-6061-T6 (EN)
        """
        # Cross-reference mapping (production would use database)
        cross_ref_map = {
            ("6061-T6", "AA", "EN"): ("EN AW-6061-T6", "exact"),
            ("6061-T6", "AA", "JIS"): ("A6061-T6", "exact"),
            ("316L", "AISI", "EN"): ("1.4404", "exact"),
            ("316L", "AISI", "JIS"): ("SUS316L", "exact"),
            ("Ti-6Al-4V", "AMS", "EN"): ("3.7165", "exact"),
        }

        key = (alloy, source_standard, target_standard)
        if key in cross_ref_map:
            target, equiv = cross_ref_map[key]
            return AlloyCrossReference(
                source_designation=alloy,
                source_standard=source_standard,
                target_designation=target,
                target_standard=target_standard,
                equivalence=equiv,
                composition_differences={},
                property_differences={},
                notes=f"Standard cross-reference: {alloy} = {target}"
            )

        return AlloyCrossReference(
            source_designation=alloy,
            source_standard=source_standard,
            target_designation="NOT FOUND",
            target_standard=target_standard,
            equivalence="unknown",
            composition_differences={},
            property_differences={},
            notes="No direct equivalent found in database"
        )

    def check_galvanic_compatibility(
        self,
        material_a: str,
        material_b: str,
        environment: str = "seawater"
    ) -> MaterialCompatibility:
        """
        Check galvanic compatibility between two materials.

        Args:
            material_a: First material (e.g., "316_stainless_passive")
            material_b: Second material (e.g., "aluminum_6061")
            environment: "seawater", "freshwater", "industrial", "atmosphere"

        Returns:
            MaterialCompatibility with assessment and mitigation options
        """
        pos_a = self.galvanic_series.get(material_a.lower().replace(" ", "_"), 0)
        pos_b = self.galvanic_series.get(material_b.lower().replace(" ", "_"), 0)

        voltage_diff = abs(pos_a - pos_b) * 1000  # Convert to mV

        # Determine which is anode (will corrode)
        if pos_a < pos_b:
            anode, cathode = material_a, material_b
        else:
            anode, cathode = material_b, material_a

        galvanic_data = GalvanicPair(
            material_a=material_a,
            material_b=material_b,
            voltage_difference_mv=voltage_diff,
            anode=anode,
            cathode=cathode,
            corrosion_rate_factor=1.0 + (voltage_diff / 500)
        )

        # Environment adjustment
        env_factors = {
            "seawater": 1.0,
            "brackish": 0.8,
            "freshwater": 0.3,
            "industrial": 0.5,
            "atmosphere": 0.2,
        }
        env_factor = env_factors.get(environment, 1.0)
        effective_risk = voltage_diff * env_factor

        # Determine compatibility
        if effective_risk < 100:
            compatible = True
            issue = None
        elif effective_risk < 250:
            compatible = True
            issue = f"Minor galvanic risk - {anode} may corrode slowly"
        else:
            compatible = False
            issue = f"HIGH galvanic risk - {anode} will corrode rapidly"

        mitigation = []
        if voltage_diff > 100:
            mitigation.append("Isolate with non-conductive material (nylon washer)")
            mitigation.append("Apply dielectric grease")
        if voltage_diff > 250:
            mitigation.append("Use sacrificial zinc anode")
            mitigation.append("Consider material substitution")
        if voltage_diff > 400:
            mitigation.append("STRONGLY recommend material change")
            mitigation.append(f"Replace {anode} with material closer to {cathode}")

        return MaterialCompatibility(
            material_a=material_a,
            material_b=material_b,
            compatible=compatible,
            issue=issue,
            galvanic_data=galvanic_data,
            mitigation_options=mitigation,
            environment_notes={
                "tested_environment": environment,
                "risk_factor": str(env_factor),
                "effective_voltage_mv": str(effective_risk)
            }
        )

    def recommend_material(
        self,
        application: str,
        requirements: Dict,
        constraints: Dict
    ) -> List[MaterialRecommendation]:
        """
        Recommend materials for an application based on requirements.

        Args:
            application: Description of use case
            requirements: {
                "temperature_c": max operating temp,
                "corrosion_resistance": "good"/"excellent",
                "strength_mpa": minimum tensile strength,
                ...
            }
            constraints: {
                "max_cost_factor": relative cost limit,
                "must_be_weldable": bool,
                "must_be_machinable": bool,
                ...
            }

        Returns:
            List of MaterialRecommendation sorted by suitability
        """
        recommendations = []

        for designation, props in self.alloy_database.items():
            score = 1.0
            meets = {}
            advantages = []
            limitations = []

            # Check temperature requirement
            if "temperature_c" in requirements:
                req_temp = requirements["temperature_c"]
                if props.max_service_temp_c >= req_temp:
                    meets["temperature"] = True
                    if props.max_service_temp_c > req_temp * 1.5:
                        advantages.append(f"Excellent temperature margin ({props.max_service_temp_c}°C)")
                else:
                    meets["temperature"] = False
                    score *= 0.3
                    limitations.append(f"Max temp {props.max_service_temp_c}°C below requirement")

            # Check strength requirement
            if "strength_mpa" in requirements:
                req_strength = requirements["strength_mpa"]
                if props.tensile_strength_mpa >= req_strength:
                    meets["strength"] = True
                    if props.tensile_strength_mpa > req_strength * 1.5:
                        advantages.append(f"High strength margin ({props.tensile_strength_mpa} MPa)")
                else:
                    meets["strength"] = False
                    score *= 0.4

            # Check corrosion requirement
            if "corrosion_resistance" in requirements:
                req_corr = requirements["corrosion_resistance"]
                corr_levels = {"poor": 1, "fair": 2, "good": 3, "excellent": 4, "inert": 5}
                if corr_levels.get(props.corrosion_resistance.value, 0) >= corr_levels.get(req_corr, 0):
                    meets["corrosion"] = True
                    if props.corrosion_resistance == CorrosionResistance.EXCELLENT:
                        advantages.append("Excellent corrosion resistance")
                else:
                    meets["corrosion"] = False
                    score *= 0.5

            # Cost factors (relative to carbon steel)
            cost_factors = {
                MaterialFamily.FERROUS: 1.0,
                MaterialFamily.ALUMINUM: 2.5,
                MaterialFamily.COPPER: 4.0,
                MaterialFamily.TITANIUM: 15.0,
                MaterialFamily.NICKEL: 20.0,
            }
            cost = cost_factors.get(props.family, 5.0)

            if "max_cost_factor" in constraints:
                if cost > constraints["max_cost_factor"]:
                    score *= 0.5
                    limitations.append(f"Cost factor {cost}x exceeds limit")

            # Weldability check
            if constraints.get("must_be_weldable") and not props.weldable:
                score *= 0.2
                limitations.append("Not weldable")

            if score > 0.3:  # Only include reasonable candidates
                recommendations.append(MaterialRecommendation(
                    material=props.family.value,
                    designation=designation,
                    suitability_score=score,
                    properties=props,
                    meets_requirements=meets,
                    advantages=advantages,
                    limitations=limitations,
                    cost_factor=cost,
                    availability="common" if cost < 5 else "specialty"
                ))

        # Sort by suitability score
        recommendations.sort(key=lambda x: x.suitability_score, reverse=True)
        return recommendations[:5]  # Top 5

    def select_polymer(
        self,
        requirements: Dict
    ) -> List[Dict]:
        """
        Select polymers based on requirements.

        Args:
            requirements: {
                "temperature_max_c": max operating temp,
                "chemical_exposure": ["oil", "fuel", ...],
                "outdoor_uv": bool,
                "sterilizable": "autoclave" / "gamma" / "eto"
            }
        """
        recommendations = []

        for name, props in self.polymer_database.items():
            score = 1.0
            issues = []

            # Temperature check
            if "temperature_max_c" in requirements:
                req_temp = requirements["temperature_max_c"]
                if props["temp_continuous_c"] >= req_temp:
                    score += 0.2
                else:
                    score *= 0.3
                    issues.append(f"Max temp {props['temp_continuous_c']}°C")

            # Chemical resistance
            if "chemical_exposure" in requirements:
                for chem in requirements["chemical_exposure"]:
                    if chem in props.get("chemical_weakness", []):
                        score *= 0.2
                        issues.append(f"Not resistant to {chem}")
                    elif chem in props.get("chemical_resistance", []) or "all" in props.get("chemical_resistance", []):
                        score += 0.1

            # Sterilization
            if "sterilizable" in requirements:
                method = requirements["sterilizable"]
                if method in props.get("sterilizable", []):
                    score += 0.1
                else:
                    score *= 0.5
                    issues.append(f"Cannot be sterilized by {method}")

            if score > 0.3:
                recommendations.append({
                    "material": name,
                    "full_name": props["full_name"],
                    "suitability_score": min(score, 1.0),
                    "temp_range": props["temp_range_c"],
                    "cost_factor": props["cost_factor"],
                    "issues": issues,
                    "applications": props["applications"]
                })

        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        return recommendations


# Demo usage
if __name__ == "__main__":
    agent = AlchemistAgent()

    print("=" * 60)
    print("Agent_18: ALCHEMIST - Materials Science Intelligence")
    print("=" * 60)

    # Test galvanic compatibility
    print("\n--- Galvanic Compatibility Check ---")
    result = agent.check_galvanic_compatibility(
        "316_stainless_passive",
        "aluminum_6061",
        "seawater"
    )
    print(f"Materials: {result.material_a} + {result.material_b}")
    print(f"Compatible: {result.compatible}")
    print(f"Issue: {result.issue}")
    print(f"Voltage difference: {result.galvanic_data.voltage_difference_mv:.0f} mV")
    print(f"Mitigation options:")
    for opt in result.mitigation_options:
        print(f"  - {opt}")

    # Test material recommendation
    print("\n--- Material Recommendation ---")
    recs = agent.recommend_material(
        application="Exhaust manifold studs",
        requirements={
            "temperature_c": 800,
            "corrosion_resistance": "excellent",
            "strength_mpa": 500
        },
        constraints={
            "max_cost_factor": 25
        }
    )
    for rec in recs:
        print(f"\n{rec.designation}:")
        print(f"  Suitability: {rec.suitability_score:.0%}")
        print(f"  Cost factor: {rec.cost_factor}x")
        print(f"  Advantages: {', '.join(rec.advantages) or 'None noted'}")

    # Test polymer selection
    print("\n--- Polymer Selection ---")
    polymers = agent.select_polymer({
        "temperature_max_c": 200,
        "chemical_exposure": ["oils", "fuels"],
        "sterilizable": "autoclave"
    })
    for p in polymers[:3]:
        print(f"\n{p['material']} ({p['full_name']}):")
        print(f"  Suitability: {p['suitability_score']:.0%}")
        print(f"  Temp range: {p['temp_range'][0]} to {p['temp_range'][1]}°C")
