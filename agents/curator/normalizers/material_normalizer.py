"""
Agent_1 (ARCHIVIST) - Material Property Normalizer
===================================================
"Every alloy has a story. The Archivist knows them all."

Material specification normalization across global standards:
- ASTM (American Society for Testing and Materials)
- SAE (Society of Automotive Engineers)
- EN/ISO (European/International Standards)
- JIS (Japanese Industrial Standards)
- GB (Chinese National Standards)

The normalizer harmonizes material names, grades, and properties
into a consistent format for accurate comparison and consciousness.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class MaterialCategory(Enum):
    """Primary material categories."""
    STAINLESS_STEEL = "stainless_steel"
    ALLOY_STEEL = "alloy_steel"
    CARBON_STEEL = "carbon_steel"
    ALUMINUM = "aluminum"
    BRASS = "brass"
    BRONZE = "bronze"
    COPPER = "copper"
    TITANIUM = "titanium"
    NICKEL_ALLOY = "nickel_alloy"
    PLASTIC = "plastic"
    UNKNOWN = "unknown"


class FinishType(Enum):
    """Surface finish types."""
    PLAIN = "plain"
    ZINC_PLATED = "zinc_plated"
    BLACK_OXIDE = "black_oxide"
    CHROME_PLATED = "chrome_plated"
    NICKEL_PLATED = "nickel_plated"
    CADMIUM_PLATED = "cadmium_plated"
    HOT_DIP_GALVANIZED = "hot_dip_galvanized"
    PHOSPHATE = "phosphate"
    PASSIVATED = "passivated"
    ANODIZED = "anodized"
    UNKNOWN = "unknown"


@dataclass
class MaterialProperties:
    """Mechanical properties of a material."""
    tensile_strength_mpa: Optional[float] = None  # Ultimate tensile strength
    yield_strength_mpa: Optional[float] = None    # 0.2% proof stress
    hardness_hrc: Optional[float] = None          # Rockwell C hardness
    hardness_hb: Optional[float] = None           # Brinell hardness
    elongation_pct: Optional[float] = None        # Elongation at break
    shear_strength_mpa: Optional[float] = None    # Shear strength
    density_g_cm3: Optional[float] = None         # Density

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in {
            "tensile_strength_mpa": self.tensile_strength_mpa,
            "yield_strength_mpa": self.yield_strength_mpa,
            "hardness_hrc": self.hardness_hrc,
            "hardness_hb": self.hardness_hb,
            "elongation_pct": self.elongation_pct,
            "shear_strength_mpa": self.shear_strength_mpa,
            "density_g_cm3": self.density_g_cm3,
        }.items() if v is not None}


@dataclass
class NormalizedMaterial:
    """Result of material normalization."""
    original_name: str
    normalized_name: str
    category: MaterialCategory

    # Specifications
    grade: Optional[str] = None           # e.g., "A2-70", "8.8", "Grade 8"
    alloy_type: Optional[str] = None      # e.g., "304", "316", "18-8"
    finish: FinishType = FinishType.PLAIN

    # Standards references
    astm_spec: Optional[str] = None       # e.g., "ASTM F593"
    sae_spec: Optional[str] = None        # e.g., "SAE J429"
    iso_spec: Optional[str] = None        # e.g., "ISO 3506-1"
    din_spec: Optional[str] = None        # e.g., "DIN 912"

    # Mechanical properties
    properties: MaterialProperties = field(default_factory=MaterialProperties)

    # Composition (key elements, percentages)
    composition: Dict[str, float] = field(default_factory=dict)

    # Normalization metadata
    confidence: float = 1.0
    equivalent_names: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original_name,
            "normalized": self.normalized_name,
            "category": self.category.value,
            "grade": self.grade,
            "alloy_type": self.alloy_type,
            "finish": self.finish.value,
            "astm_spec": self.astm_spec,
            "sae_spec": self.sae_spec,
            "iso_spec": self.iso_spec,
            "properties": self.properties.to_dict(),
            "confidence": self.confidence,
            "equivalent_names": self.equivalent_names,
        }


class MaterialNormalizer:
    """
    Material property normalizer for Universal Parts Consciousness.

    Converts material specifications from various naming conventions
    to a consistent internal representation with known properties.
    """

    # Stainless steel type mappings
    STAINLESS_TYPES = {
        # 18-8 family (austenitic)
        "18-8": {"normalized": "18-8 Stainless Steel", "alloy": "304", "grade": "A2"},
        "18/8": {"normalized": "18-8 Stainless Steel", "alloy": "304", "grade": "A2"},
        "304": {"normalized": "304 Stainless Steel", "alloy": "304", "grade": "A2"},
        "304L": {"normalized": "304L Stainless Steel", "alloy": "304L", "grade": "A2"},
        "A2": {"normalized": "18-8 Stainless Steel", "alloy": "304", "grade": "A2"},
        "A2-70": {"normalized": "18-8 Stainless Steel", "alloy": "304", "grade": "A2-70"},
        "A2-80": {"normalized": "18-8 Stainless Steel", "alloy": "304", "grade": "A2-80"},

        # 316 family (marine grade)
        "316": {"normalized": "316 Stainless Steel", "alloy": "316", "grade": "A4"},
        "316L": {"normalized": "316L Stainless Steel", "alloy": "316L", "grade": "A4"},
        "A4": {"normalized": "316 Stainless Steel", "alloy": "316", "grade": "A4"},
        "A4-70": {"normalized": "316 Stainless Steel", "alloy": "316", "grade": "A4-70"},
        "A4-80": {"normalized": "316 Stainless Steel", "alloy": "316", "grade": "A4-80"},

        # Other stainless types
        "410": {"normalized": "410 Stainless Steel", "alloy": "410", "grade": None},
        "17-4 PH": {"normalized": "17-4 PH Stainless Steel", "alloy": "17-4", "grade": None},
        "17-4PH": {"normalized": "17-4 PH Stainless Steel", "alloy": "17-4", "grade": None},
    }

    # Alloy steel grade mappings
    ALLOY_STEEL_GRADES = {
        # SAE grades
        "GRADE 8": {"normalized": "Alloy Steel Grade 8", "grade": "8", "metric_equiv": "10.9"},
        "GRADE 5": {"normalized": "Alloy Steel Grade 5", "grade": "5", "metric_equiv": "8.8"},
        "GRADE 2": {"normalized": "Steel Grade 2", "grade": "2", "metric_equiv": "4.6"},

        # Metric property classes
        "12.9": {"normalized": "Alloy Steel Class 12.9", "grade": "12.9", "sae_equiv": "None"},
        "10.9": {"normalized": "Alloy Steel Class 10.9", "grade": "10.9", "sae_equiv": "8"},
        "8.8": {"normalized": "Alloy Steel Class 8.8", "grade": "8.8", "sae_equiv": "5"},
        "4.6": {"normalized": "Steel Class 4.6", "grade": "4.6", "sae_equiv": "2"},
        "4.8": {"normalized": "Steel Class 4.8", "grade": "4.8", "sae_equiv": "2"},
    }

    # Material properties database
    MATERIAL_PROPERTIES = {
        "18-8 Stainless Steel": MaterialProperties(
            tensile_strength_mpa=515,
            yield_strength_mpa=205,
            hardness_hb=217,
            elongation_pct=40,
            density_g_cm3=7.9,
        ),
        "316 Stainless Steel": MaterialProperties(
            tensile_strength_mpa=515,
            yield_strength_mpa=205,
            hardness_hb=217,
            elongation_pct=40,
            density_g_cm3=8.0,
        ),
        "Alloy Steel Grade 8": MaterialProperties(
            tensile_strength_mpa=1034,
            yield_strength_mpa=930,
            hardness_hrc=33,
            density_g_cm3=7.85,
        ),
        "Alloy Steel Grade 5": MaterialProperties(
            tensile_strength_mpa=827,
            yield_strength_mpa=635,
            hardness_hrc=25,
            density_g_cm3=7.85,
        ),
        "Alloy Steel Class 12.9": MaterialProperties(
            tensile_strength_mpa=1220,
            yield_strength_mpa=1100,
            hardness_hrc=39,
            density_g_cm3=7.85,
        ),
        "Alloy Steel Class 10.9": MaterialProperties(
            tensile_strength_mpa=1040,
            yield_strength_mpa=940,
            hardness_hrc=33,
            density_g_cm3=7.85,
        ),
        "Alloy Steel Class 8.8": MaterialProperties(
            tensile_strength_mpa=800,
            yield_strength_mpa=640,
            hardness_hrc=23,
            density_g_cm3=7.85,
        ),
        "Brass": MaterialProperties(
            tensile_strength_mpa=345,
            yield_strength_mpa=95,
            elongation_pct=65,
            density_g_cm3=8.5,
        ),
        "Aluminum 6061-T6": MaterialProperties(
            tensile_strength_mpa=310,
            yield_strength_mpa=276,
            elongation_pct=12,
            density_g_cm3=2.7,
        ),
        "Titanium Grade 5": MaterialProperties(
            tensile_strength_mpa=1100,
            yield_strength_mpa=1000,
            elongation_pct=10,
            density_g_cm3=4.43,
        ),
    }

    # Finish patterns
    FINISH_PATTERNS = {
        FinishType.ZINC_PLATED: [
            re.compile(r'zinc[- ]?plated', re.I),
            re.compile(r'zinc[- ]?coated', re.I),
            re.compile(r'electroplated zinc', re.I),
        ],
        FinishType.BLACK_OXIDE: [
            re.compile(r'black[- ]?oxide', re.I),
            re.compile(r'black finish', re.I),
        ],
        FinishType.CHROME_PLATED: [
            re.compile(r'chrome[- ]?plated', re.I),
            re.compile(r'chromium', re.I),
        ],
        FinishType.HOT_DIP_GALVANIZED: [
            re.compile(r'hot[- ]?dip[- ]?galvanized', re.I),
            re.compile(r'HDG', re.I),
            re.compile(r'galvanized', re.I),
        ],
        FinishType.PHOSPHATE: [
            re.compile(r'phosphate', re.I),
            re.compile(r'parkerized', re.I),
        ],
        FinishType.PASSIVATED: [
            re.compile(r'passivated', re.I),
        ],
        FinishType.ANODIZED: [
            re.compile(r'anodized', re.I),
            re.compile(r'anodised', re.I),
        ],
    }

    def __init__(self):
        """Initialize the material normalizer."""
        pass

    def normalize(self, material: str) -> NormalizedMaterial:
        """
        Normalize a material specification.

        Args:
            material: Raw material name/specification

        Returns:
            NormalizedMaterial with normalized data and properties
        """
        mat = material.strip()
        mat_upper = mat.upper()

        # Extract finish first
        finish, cleaned_material = self._extract_finish(mat)

        # Try stainless steel
        result = self._try_stainless(cleaned_material)
        if result:
            result.finish = finish
            return result

        # Try alloy steel
        result = self._try_alloy_steel(cleaned_material)
        if result:
            result.finish = finish
            return result

        # Try other materials
        result = self._try_other_materials(cleaned_material)
        if result:
            result.finish = finish
            return result

        # Unable to categorize - return basic result
        return NormalizedMaterial(
            original_name=material,
            normalized_name=self._clean_material_name(mat),
            category=MaterialCategory.UNKNOWN,
            finish=finish,
            confidence=0.3,
            notes=["Material type could not be determined"],
        )

    def _extract_finish(self, material: str) -> Tuple[FinishType, str]:
        """Extract finish type from material string."""
        for finish_type, patterns in self.FINISH_PATTERNS.items():
            for pattern in patterns:
                if pattern.search(material):
                    # Remove finish text from material
                    cleaned = pattern.sub('', material).strip()
                    cleaned = re.sub(r'\s+', ' ', cleaned)
                    return finish_type, cleaned

        return FinishType.PLAIN, material

    def _try_stainless(self, material: str) -> Optional[NormalizedMaterial]:
        """Try to parse as stainless steel."""
        mat_upper = material.upper()

        # Check for stainless indicators
        is_stainless = (
            "STAINLESS" in mat_upper or
            "SS" in mat_upper or
            any(key.upper() in mat_upper for key in self.STAINLESS_TYPES)
        )

        if not is_stainless:
            return None

        # Find specific type
        for key, info in self.STAINLESS_TYPES.items():
            if key.upper() in mat_upper:
                normalized_name = info["normalized"]
                props = self.MATERIAL_PROPERTIES.get(
                    normalized_name,
                    self.MATERIAL_PROPERTIES.get("18-8 Stainless Steel")
                )

                return NormalizedMaterial(
                    original_name=material,
                    normalized_name=normalized_name,
                    category=MaterialCategory.STAINLESS_STEEL,
                    grade=info.get("grade"),
                    alloy_type=info.get("alloy"),
                    properties=props,
                    confidence=0.95,
                    equivalent_names=self._get_stainless_equivalents(info.get("alloy")),
                )

        # Generic stainless steel
        return NormalizedMaterial(
            original_name=material,
            normalized_name="Stainless Steel",
            category=MaterialCategory.STAINLESS_STEEL,
            confidence=0.7,
            notes=["Specific stainless type not identified"],
        )

    def _get_stainless_equivalents(self, alloy: Optional[str]) -> List[str]:
        """Get equivalent names for a stainless alloy."""
        equivalents = []
        if alloy == "304":
            equivalents = ["18-8 Stainless", "A2", "304 SS", "1.4301"]
        elif alloy == "316":
            equivalents = ["A4", "316 SS", "Marine Grade", "1.4401"]
        return equivalents

    def _try_alloy_steel(self, material: str) -> Optional[NormalizedMaterial]:
        """Try to parse as alloy/carbon steel."""
        mat_upper = material.upper()

        # Check for steel indicators
        is_steel = (
            "STEEL" in mat_upper or
            "ALLOY" in mat_upper or
            "GRADE" in mat_upper or
            re.search(r'\b\d+\.\d+\b', mat_upper)  # Property class like "8.8"
        )

        if not is_steel:
            return None

        # Check for specific grades
        for key, info in self.ALLOY_STEEL_GRADES.items():
            if key in mat_upper:
                normalized_name = info["normalized"]
                props = self.MATERIAL_PROPERTIES.get(normalized_name)

                equivalents = []
                if "metric_equiv" in info and info["metric_equiv"]:
                    equivalents.append(f"Class {info['metric_equiv']}")
                if "sae_equiv" in info and info["sae_equiv"]:
                    equivalents.append(f"Grade {info['sae_equiv']}")

                return NormalizedMaterial(
                    original_name=material,
                    normalized_name=normalized_name,
                    category=MaterialCategory.ALLOY_STEEL,
                    grade=info.get("grade"),
                    properties=props or MaterialProperties(),
                    confidence=0.95,
                    equivalent_names=equivalents,
                )

        # Generic steel
        category = MaterialCategory.CARBON_STEEL if "CARBON" in mat_upper else MaterialCategory.ALLOY_STEEL
        return NormalizedMaterial(
            original_name=material,
            normalized_name="Steel",
            category=category,
            confidence=0.6,
            notes=["Specific steel grade not identified"],
        )

    def _try_other_materials(self, material: str) -> Optional[NormalizedMaterial]:
        """Try to parse as other materials (brass, bronze, aluminum, etc.)."""
        mat_upper = material.upper()

        # Brass
        if "BRASS" in mat_upper:
            props = self.MATERIAL_PROPERTIES.get("Brass")
            return NormalizedMaterial(
                original_name=material,
                normalized_name="Brass",
                category=MaterialCategory.BRASS,
                properties=props or MaterialProperties(),
                confidence=0.9,
            )

        # Bronze
        if "BRONZE" in mat_upper:
            bronze_type = "Bronze"
            if "SILICON" in mat_upper:
                bronze_type = "Silicon Bronze"
            elif "PHOSPHOR" in mat_upper:
                bronze_type = "Phosphor Bronze"

            return NormalizedMaterial(
                original_name=material,
                normalized_name=bronze_type,
                category=MaterialCategory.BRONZE,
                confidence=0.9,
            )

        # Aluminum
        if "ALUMINUM" in mat_upper or "ALUMINIUM" in mat_upper:
            # Try to extract alloy number
            alloy_match = re.search(r'(\d{4})(?:-?([TH]\d+))?', material)
            if alloy_match:
                alloy = alloy_match.group(1)
                temper = alloy_match.group(2) or ""
                normalized = f"Aluminum {alloy}{'-' + temper if temper else ''}"
                props = self.MATERIAL_PROPERTIES.get(f"Aluminum {alloy}-{temper}")
            else:
                normalized = "Aluminum"
                alloy = None
                props = None

            return NormalizedMaterial(
                original_name=material,
                normalized_name=normalized,
                category=MaterialCategory.ALUMINUM,
                alloy_type=alloy,
                properties=props or MaterialProperties(),
                confidence=0.9 if alloy else 0.7,
            )

        # Titanium
        if "TITANIUM" in mat_upper or "TI-" in mat_upper:
            # Try to extract grade
            if "GRADE 5" in mat_upper or "6AL-4V" in mat_upper or "6AL4V" in mat_upper:
                normalized = "Titanium Grade 5 (Ti-6Al-4V)"
                grade = "Grade 5"
                props = self.MATERIAL_PROPERTIES.get("Titanium Grade 5")
            else:
                normalized = "Titanium"
                grade = None
                props = None

            return NormalizedMaterial(
                original_name=material,
                normalized_name=normalized,
                category=MaterialCategory.TITANIUM,
                grade=grade,
                properties=props or MaterialProperties(),
                confidence=0.9 if grade else 0.7,
            )

        # Plastics
        plastic_types = ["NYLON", "PEEK", "PTFE", "DELRIN", "ACETAL", "POLYCARBONATE"]
        for plastic in plastic_types:
            if plastic in mat_upper:
                return NormalizedMaterial(
                    original_name=material,
                    normalized_name=plastic.title(),
                    category=MaterialCategory.PLASTIC,
                    confidence=0.9,
                )

        return None

    def _clean_material_name(self, material: str) -> str:
        """Clean and standardize material name."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', material).strip()
        # Capitalize first letter of each word
        cleaned = cleaned.title()
        return cleaned

    def are_equivalent(
        self,
        mat_a: NormalizedMaterial,
        mat_b: NormalizedMaterial,
    ) -> Tuple[bool, float]:
        """
        Check if two materials are equivalent.

        Args:
            mat_a: First material
            mat_b: Second material

        Returns:
            Tuple of (is_equivalent, confidence_score)
        """
        # Same normalized name
        if mat_a.normalized_name == mat_b.normalized_name:
            return True, 1.0

        # Same category and grade
        if mat_a.category == mat_b.category:
            if mat_a.grade and mat_b.grade and mat_a.grade == mat_b.grade:
                return True, 0.95

            if mat_a.alloy_type and mat_b.alloy_type:
                if mat_a.alloy_type == mat_b.alloy_type:
                    return True, 0.9

        # Check equivalents
        if mat_a.normalized_name in mat_b.equivalent_names:
            return True, 0.85
        if mat_b.normalized_name in mat_a.equivalent_names:
            return True, 0.85

        # Same category but different specifics
        if mat_a.category == mat_b.category:
            return False, 0.5

        return False, 0.0


# Convenience functions
def normalize_material(material: str) -> NormalizedMaterial:
    """Normalize a material specification."""
    normalizer = MaterialNormalizer()
    return normalizer.normalize(material)


def materials_equivalent(mat_a: str, mat_b: str) -> Tuple[bool, float]:
    """Check if two material specifications are equivalent."""
    normalizer = MaterialNormalizer()
    norm_a = normalizer.normalize(mat_a)
    norm_b = normalizer.normalize(mat_b)
    return normalizer.are_equivalent(norm_a, norm_b)


__all__ = [
    "MaterialNormalizer",
    "NormalizedMaterial",
    "MaterialCategory",
    "MaterialProperties",
    "FinishType",
    "normalize_material",
    "materials_equivalent",
]
