"""
Material Failure Properties

Reference data for material failure characteristics.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MaterialProperties:
    """Material properties relevant to failure analysis"""
    name: str
    category: str
    tensile_strength_mpa: float
    yield_strength_mpa: float
    hardness: str
    endurance_limit_mpa: Optional[float]
    corrosion_resistance: str
    susceptible_to: List[str]
    common_failure_modes: List[str]


class MaterialFailureProperties:
    """
    Reference database for material failure properties.

    Provides material-specific information for failure analysis:
    - Mechanical properties
    - Known failure modes
    - Susceptibilities
    """

    # Material property database
    MATERIALS: Dict[str, MaterialProperties] = {
        "steel_1018": MaterialProperties(
            name="AISI 1018 Steel",
            category="Carbon Steel",
            tensile_strength_mpa=440,
            yield_strength_mpa=370,
            hardness="126 HB",
            endurance_limit_mpa=220,
            corrosion_resistance="Poor",
            susceptible_to=["Corrosion", "Fatigue"],
            common_failure_modes=["Fatigue", "Corrosion", "Wear"]
        ),
        "steel_4140": MaterialProperties(
            name="AISI 4140 Steel",
            category="Alloy Steel",
            tensile_strength_mpa=1020,
            yield_strength_mpa=950,
            hardness="30-34 HRC",
            endurance_limit_mpa=510,
            corrosion_resistance="Poor",
            susceptible_to=["Hydrogen Embrittlement", "Stress Corrosion Cracking"],
            common_failure_modes=["Fatigue", "Hydrogen Embrittlement"]
        ),
        "steel_10.9": MaterialProperties(
            name="Class 10.9 Fastener Steel",
            category="Fastener Grade",
            tensile_strength_mpa=1040,
            yield_strength_mpa=940,
            hardness="32-39 HRC",
            endurance_limit_mpa=400,
            corrosion_resistance="Poor",
            susceptible_to=["Hydrogen Embrittlement", "Fatigue"],
            common_failure_modes=["Fatigue", "Hydrogen Embrittlement", "Stress Corrosion"]
        ),
        "steel_12.9": MaterialProperties(
            name="Class 12.9 Fastener Steel",
            category="Fastener Grade",
            tensile_strength_mpa=1220,
            yield_strength_mpa=1100,
            hardness="39-44 HRC",
            endurance_limit_mpa=450,
            corrosion_resistance="Poor",
            susceptible_to=["Hydrogen Embrittlement", "Stress Corrosion Cracking"],
            common_failure_modes=["Hydrogen Embrittlement", "Fatigue"]
        ),
        "stainless_304": MaterialProperties(
            name="304 Stainless Steel",
            category="Austenitic Stainless",
            tensile_strength_mpa=515,
            yield_strength_mpa=205,
            hardness="88 HRB",
            endurance_limit_mpa=240,
            corrosion_resistance="Good",
            susceptible_to=["Stress Corrosion Cracking (chlorides)", "Pitting in chlorides"],
            common_failure_modes=["SCC", "Pitting Corrosion", "Fatigue"]
        ),
        "stainless_316": MaterialProperties(
            name="316 Stainless Steel",
            category="Austenitic Stainless",
            tensile_strength_mpa=515,
            yield_strength_mpa=205,
            hardness="88 HRB",
            endurance_limit_mpa=240,
            corrosion_resistance="Excellent",
            susceptible_to=["Stress Corrosion Cracking (chlorides at temp)"],
            common_failure_modes=["SCC", "Fatigue", "Crevice Corrosion"]
        ),
        "aluminum_6061": MaterialProperties(
            name="6061-T6 Aluminum",
            category="Aluminum Alloy",
            tensile_strength_mpa=310,
            yield_strength_mpa=276,
            hardness="95 HB",
            endurance_limit_mpa=None,  # No true endurance limit
            corrosion_resistance="Good",
            susceptible_to=["Galvanic Corrosion", "Stress Corrosion (T6)"],
            common_failure_modes=["Fatigue", "Galvanic Corrosion", "SCC"]
        ),
        "titanium_6al4v": MaterialProperties(
            name="Ti-6Al-4V",
            category="Titanium Alloy",
            tensile_strength_mpa=950,
            yield_strength_mpa=880,
            hardness="36 HRC",
            endurance_limit_mpa=510,
            corrosion_resistance="Excellent",
            susceptible_to=["Galling", "Fretting", "Hydrogen Embrittlement (rare)"],
            common_failure_modes=["Fatigue", "Fretting", "Galling"]
        ),
    }

    # Failure mode susceptibility by material category
    CATEGORY_SUSCEPTIBILITIES = {
        "Carbon Steel": [
            "Corrosion (unprotected)",
            "Fatigue",
            "Wear",
        ],
        "Alloy Steel": [
            "Hydrogen Embrittlement (if hardened >32 HRC)",
            "Stress Corrosion Cracking",
            "Fatigue",
            "Temper Embrittlement",
        ],
        "Fastener Grade": [
            "Hydrogen Embrittlement",
            "Fatigue (thread root)",
            "Stress Corrosion Cracking",
        ],
        "Austenitic Stainless": [
            "Stress Corrosion Cracking (chlorides)",
            "Pitting Corrosion",
            "Crevice Corrosion",
            "Fatigue",
        ],
        "Aluminum Alloy": [
            "Galvanic Corrosion",
            "Fatigue (no endurance limit)",
            "Stress Corrosion Cracking",
        ],
        "Titanium Alloy": [
            "Galling/Fretting",
            "Fatigue",
            "Hydrogen Embrittlement (rare, at high temp)",
        ],
    }

    def __init__(self):
        """Initialize the material properties database."""
        pass

    def get_material(self, material_id: str) -> Optional[MaterialProperties]:
        """Get properties for a specific material."""
        return self.MATERIALS.get(material_id.lower().replace(" ", "_"))

    def get_susceptibilities(self, material_id: str) -> List[str]:
        """Get failure susceptibilities for a material."""
        material = self.get_material(material_id)
        if material:
            return material.susceptible_to
        return []

    def get_common_failures(self, material_id: str) -> List[str]:
        """Get common failure modes for a material."""
        material = self.get_material(material_id)
        if material:
            return material.common_failure_modes
        return []

    def check_he_susceptibility(
        self,
        material: str,
        hardness_hrc: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Check hydrogen embrittlement susceptibility.

        Args:
            material: Material identifier
            hardness_hrc: Actual hardness if known

        Returns:
            HE susceptibility assessment
        """
        susceptible_categories = [
            "Alloy Steel",
            "Fastener Grade",
        ]

        mat = self.get_material(material)
        if not mat:
            return {
                "susceptible": "Unknown",
                "reason": "Material not in database",
            }

        # Check category
        if mat.category in susceptible_categories:
            # Check hardness threshold
            if hardness_hrc and hardness_hrc >= 32:
                return {
                    "susceptible": True,
                    "risk_level": "HIGH" if hardness_hrc >= 39 else "MEDIUM",
                    "reason": f"Hardness {hardness_hrc} HRC exceeds 32 HRC threshold",
                    "recommendations": [
                        "Avoid hydrogen-generating processes",
                        "Bake after electroplating (375F/4hr minimum)",
                        "Consider mechanical zinc or Geomet coating",
                    ]
                }
            elif "HRC" in mat.hardness:
                # Parse hardness from material data
                try:
                    hrc_value = float(mat.hardness.split()[0].split("-")[0])
                    if hrc_value >= 32:
                        return {
                            "susceptible": True,
                            "risk_level": "MEDIUM",
                            "reason": f"Material hardness {mat.hardness} in susceptible range",
                            "recommendations": [
                                "Verify actual hardness",
                                "Use HE-resistant coatings",
                            ]
                        }
                except (ValueError, IndexError):
                    pass

        return {
            "susceptible": False,
            "risk_level": "LOW",
            "reason": "Material/hardness not in susceptible range",
        }

    def get_galvanic_compatibility(
        self,
        material_a: str,
        material_b: str
    ) -> Dict[str, any]:
        """
        Check galvanic compatibility between two materials.

        Simple assessment based on material category.
        """
        # Galvanic series position (relative, lower = more anodic)
        GALVANIC_POSITION = {
            "Carbon Steel": 3,
            "Alloy Steel": 3,
            "Fastener Grade": 3,
            "Aluminum Alloy": 2,
            "Austenitic Stainless": 6,
            "Titanium Alloy": 7,
        }

        mat_a = self.get_material(material_a)
        mat_b = self.get_material(material_b)

        if not mat_a or not mat_b:
            return {
                "compatible": "Unknown",
                "reason": "One or both materials not in database",
            }

        pos_a = GALVANIC_POSITION.get(mat_a.category, 5)
        pos_b = GALVANIC_POSITION.get(mat_b.category, 5)

        difference = abs(pos_a - pos_b)

        if difference <= 1:
            return {
                "compatible": True,
                "risk_level": "LOW",
                "reason": "Materials are close in galvanic series",
            }
        elif difference <= 3:
            return {
                "compatible": "Conditional",
                "risk_level": "MEDIUM",
                "reason": "Some galvanic potential difference exists",
                "recommendations": ["Isolate if in wet environment"],
            }
        else:
            anode = material_a if pos_a < pos_b else material_b
            return {
                "compatible": False,
                "risk_level": "HIGH",
                "reason": f"Large galvanic potential difference - {anode} will corrode",
                "recommendations": [
                    "Isolate with non-conductive barrier",
                    "Use same material family",
                    "Apply protective coatings to both",
                ],
            }
