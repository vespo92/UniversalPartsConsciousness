"""
Agent_1 (ARCHIVIST) - Material Normalizer
==========================================
"One material, a thousand names. The Archivist harmonizes all."

Normalizes material designations across international standards:
- AISI (American): 304, 316, 4340
- DIN/EN (European): 1.4301, 1.4401, 42CrMo4
- JIS (Japanese): SUS304, SUS316, SCM440
- BS (British): 304S15, 316S16
- GOST (Russian): 08Х18Н10, 10Х17Н13М2Т
- UNS (Unified Numbering): S30400, S31600

Also maps material grades and property classes:
- ISO property classes: 8.8, 10.9, 12.9
- SAE grades: Grade 2, Grade 5, Grade 8
- Stainless grades: A2-70, A4-80
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any


class MaterialFamily(Enum):
    """Material family classifications."""
    STAINLESS_AUSTENITIC = "stainless_austenitic"
    STAINLESS_FERRITIC = "stainless_ferritic"
    STAINLESS_MARTENSITIC = "stainless_martensitic"
    STAINLESS_DUPLEX = "stainless_duplex"
    CARBON_STEEL = "carbon_steel"
    ALLOY_STEEL = "alloy_steel"
    TOOL_STEEL = "tool_steel"
    ALUMINUM = "aluminum"
    BRASS = "brass"
    BRONZE = "bronze"
    COPPER = "copper"
    TITANIUM = "titanium"
    NICKEL_ALLOY = "nickel_alloy"
    PLASTIC = "plastic"
    UNKNOWN = "unknown"


@dataclass
class MaterialEquivalent:
    """Material equivalence across standards."""
    aisi: Optional[str] = None
    din_en: Optional[str] = None
    jis: Optional[str] = None
    bs: Optional[str] = None
    gost: Optional[str] = None
    uns: Optional[str] = None
    common_name: Optional[str] = None


@dataclass
class NormalizedMaterial:
    """Normalized material specification."""
    canonical_name: str          # Canonical name (e.g., "304 Stainless Steel")
    family: MaterialFamily       # Material family
    grade: Optional[str] = None  # Property class/grade (e.g., "A2-70", "8.8")
    finish: Optional[str] = None # Surface finish (e.g., "zinc-plated")
    equivalents: Dict[str, str] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    original: str = ""           # Original input


# Material equivalence database
MATERIAL_EQUIVALENTS: Dict[str, MaterialEquivalent] = {
    # Austenitic stainless steels
    "304": MaterialEquivalent(
        aisi="304",
        din_en="1.4301",
        jis="SUS304",
        bs="304S15",
        gost="08Х18Н10",
        uns="S30400",
        common_name="18-8 Stainless Steel",
    ),
    "304L": MaterialEquivalent(
        aisi="304L",
        din_en="1.4307",
        jis="SUS304L",
        bs="304S11",
        gost="03Х18Н11",
        uns="S30403",
        common_name="304L Stainless Steel",
    ),
    "316": MaterialEquivalent(
        aisi="316",
        din_en="1.4401",
        jis="SUS316",
        bs="316S16",
        gost="10Х17Н13М2Т",
        uns="S31600",
        common_name="316 Stainless Steel",
    ),
    "316L": MaterialEquivalent(
        aisi="316L",
        din_en="1.4404",
        jis="SUS316L",
        bs="316S11",
        gost="03Х17Н14М3",
        uns="S31603",
        common_name="316L Stainless Steel",
    ),
    "303": MaterialEquivalent(
        aisi="303",
        din_en="1.4305",
        jis="SUS303",
        bs="303S21",
        gost="12Х18Н10Е",
        uns="S30300",
        common_name="303 Stainless Steel",
    ),

    # Alloy steels
    "4140": MaterialEquivalent(
        aisi="4140",
        din_en="1.7225 (42CrMo4)",
        jis="SCM440",
        bs="708M40",
        gost="40ХМ",
        uns="G41400",
        common_name="4140 Alloy Steel",
    ),
    "4340": MaterialEquivalent(
        aisi="4340",
        din_en="1.6565 (40NiCrMo6)",
        jis="SNCM439",
        bs="817M40",
        gost="40ХНМА",
        uns="G43400",
        common_name="4340 Alloy Steel",
    ),
    "8620": MaterialEquivalent(
        aisi="8620",
        din_en="1.6523 (20NiCrMo2)",
        jis="SNCM220",
        bs="805M20",
        gost="20ХГНМ",
        uns="G86200",
        common_name="8620 Alloy Steel",
    ),

    # Carbon steels
    "1018": MaterialEquivalent(
        aisi="1018",
        din_en="1.0453 (C18)",
        jis="S18C",
        bs="080M15",
        gost="Ст18",
        uns="G10180",
        common_name="1018 Carbon Steel",
    ),
    "1045": MaterialEquivalent(
        aisi="1045",
        din_en="1.0503 (C45)",
        jis="S45C",
        bs="080M46",
        gost="Ст45",
        uns="G10450",
        common_name="1045 Carbon Steel",
    ),

    # Aluminum alloys
    "6061": MaterialEquivalent(
        aisi=None,
        din_en="3.3211 (AlMg1SiCu)",
        jis="A6061",
        bs="HE20",
        gost="АД33",
        uns="A96061",
        common_name="6061 Aluminum",
    ),
    "7075": MaterialEquivalent(
        aisi=None,
        din_en="3.4365 (AlZnMgCu1.5)",
        jis="A7075",
        bs="DTD5024",
        gost="В95",
        uns="A97075",
        common_name="7075 Aluminum",
    ),

    # Titanium
    "Ti-6Al-4V": MaterialEquivalent(
        aisi=None,
        din_en="3.7165",
        jis="TAB6400",
        bs="TA10",
        gost="ВТ6",
        uns="R56400",
        common_name="Ti-6Al-4V (Grade 5 Titanium)",
    ),
}

# Property class/grade equivalents
GRADE_EQUIVALENTS: Dict[str, Dict[str, Any]] = {
    # Metric property classes (ISO 898-1)
    "4.6": {
        "tensile_mpa": 400,
        "yield_mpa": 240,
        "sae_equiv": "Grade 1",
        "astm_equiv": "A307 Grade A",
    },
    "4.8": {
        "tensile_mpa": 420,
        "yield_mpa": 340,
        "sae_equiv": "Grade 2",
        "astm_equiv": "A307 Grade B",
    },
    "5.8": {
        "tensile_mpa": 520,
        "yield_mpa": 420,
        "sae_equiv": None,
        "astm_equiv": None,
    },
    "8.8": {
        "tensile_mpa": 800,
        "yield_mpa": 640,
        "sae_equiv": "Grade 5",
        "astm_equiv": "A449",
    },
    "9.8": {
        "tensile_mpa": 900,
        "yield_mpa": 720,
        "sae_equiv": None,
        "astm_equiv": None,
    },
    "10.9": {
        "tensile_mpa": 1040,
        "yield_mpa": 940,
        "sae_equiv": "Grade 8",
        "astm_equiv": "A490",
    },
    "12.9": {
        "tensile_mpa": 1220,
        "yield_mpa": 1100,
        "sae_equiv": None,
        "astm_equiv": "A574",
    },

    # SAE grades
    "Grade 2": {
        "tensile_mpa": 510,
        "yield_mpa": 394,
        "metric_equiv": "4.6/5.8",
    },
    "Grade 5": {
        "tensile_mpa": 827,
        "yield_mpa": 634,
        "metric_equiv": "8.8",
    },
    "Grade 8": {
        "tensile_mpa": 1034,
        "yield_mpa": 896,
        "metric_equiv": "10.9",
    },

    # Stainless steel grades (ISO 3506)
    "A2-50": {
        "tensile_mpa": 500,
        "yield_mpa": 210,
        "material": "304/A2",
    },
    "A2-70": {
        "tensile_mpa": 700,
        "yield_mpa": 450,
        "material": "304/A2",
    },
    "A2-80": {
        "tensile_mpa": 800,
        "yield_mpa": 600,
        "material": "304/A2",
    },
    "A4-50": {
        "tensile_mpa": 500,
        "yield_mpa": 210,
        "material": "316/A4",
    },
    "A4-70": {
        "tensile_mpa": 700,
        "yield_mpa": 450,
        "material": "316/A4",
    },
    "A4-80": {
        "tensile_mpa": 800,
        "yield_mpa": 600,
        "material": "316/A4",
    },
}


class MaterialNormalizer:
    """
    Material designation normalizer.

    Converts material specifications from any standard to a canonical format,
    and provides cross-reference mappings between standards.
    """

    # Patterns for material identification
    PATTERNS = {
        # AISI stainless: 304, 316, 303, 430, etc.
        "aisi_stainless": re.compile(r'^(3\d{2}|4\d{2})([LS])?$', re.IGNORECASE),
        # AISI carbon/alloy: 1018, 4140, 4340, 8620
        "aisi_steel": re.compile(r'^([1-9]\d{3})([HL])?$', re.IGNORECASE),
        # DIN/EN: 1.4301, 1.7225
        "din": re.compile(r'^1\.\d{4}$'),
        # JIS stainless: SUS304, SUS316
        "jis_stainless": re.compile(r'^SUS(3\d{2}|4\d{2})([LS])?$', re.IGNORECASE),
        # JIS steel: SCM440, SNCM439
        "jis_steel": re.compile(r'^(SCM|SNCM|S)\d{2,3}[A-Z]?$', re.IGNORECASE),
        # Aluminum: 6061, 7075, 2024
        "aluminum": re.compile(r'^([2567]\d{3})(-[TO]\d+)?$', re.IGNORECASE),
        # Property class: 8.8, 10.9, 12.9
        "property_class": re.compile(r'^(\d{1,2})\.(\d)$'),
        # SAE grade: Grade 5, Grade 8
        "sae_grade": re.compile(r'^Grade\s*(\d)$', re.IGNORECASE),
        # Stainless grade: A2-70, A4-80
        "stainless_grade": re.compile(r'^([AB]\d)-(\d{2})$', re.IGNORECASE),
        # 18-8 stainless
        "18_8": re.compile(r'^18[-/]8$', re.IGNORECASE),
    }

    # Material name aliases
    ALIASES: Dict[str, str] = {
        # Stainless
        "18-8": "304",
        "18/8": "304",
        "a2": "304",
        "a4": "316",
        "marine grade": "316",
        "surgical steel": "316L",

        # Common names
        "mild steel": "1018",
        "chrome moly": "4140",
        "chromoly": "4140",

        # Aluminum
        "aircraft aluminum": "7075",

        # Finishes (mapped to base material)
        "zinc plated steel": "1018",
        "galvanized steel": "1018",
        "black oxide steel": "1018",
    }

    # Surface finishes
    FINISHES = {
        "zinc": ["zinc", "galvanized", "zinc-plated", "galv"],
        "black_oxide": ["black oxide", "black-oxide", "blackened"],
        "chromate": ["chromate", "yellow zinc", "yellow chromate"],
        "nickel": ["nickel", "nickel-plated"],
        "cadmium": ["cadmium", "cad", "cadmium-plated"],
        "phosphate": ["phosphate", "parkerized"],
        "passivated": ["passivated", "passivation"],
    }

    def __init__(self):
        """Initialize the material normalizer."""
        # Build reverse lookup indices
        self._build_indices()

    def _build_indices(self) -> None:
        """Build reverse lookup indices for fast matching."""
        self._din_to_aisi: Dict[str, str] = {}
        self._jis_to_aisi: Dict[str, str] = {}
        self._uns_to_aisi: Dict[str, str] = {}

        for aisi, equiv in MATERIAL_EQUIVALENTS.items():
            if equiv.din_en:
                # Extract just the numeric code
                din_match = re.search(r'(\d\.\d{4})', equiv.din_en)
                if din_match:
                    self._din_to_aisi[din_match.group(1)] = aisi
            if equiv.jis:
                self._jis_to_aisi[equiv.jis.upper()] = aisi
            if equiv.uns:
                self._uns_to_aisi[equiv.uns.upper()] = aisi

    def normalize(self, material_spec: str) -> Dict[str, Any]:
        """
        Normalize a material specification.

        Args:
            material_spec: Input material specification

        Returns:
            Dictionary with normalized material information
        """
        parsed = self.parse(material_spec)
        return {
            "canonical_name": parsed.canonical_name,
            "family": parsed.family.value,
            "grade": parsed.grade,
            "finish": parsed.finish,
            "equivalents": parsed.equivalents,
            "properties": parsed.properties,
        }

    def parse(self, material_spec: str) -> NormalizedMaterial:
        """
        Parse and normalize a material specification.

        Args:
            material_spec: Input material specification

        Returns:
            NormalizedMaterial with all parsed details
        """
        original = material_spec.strip()
        spec = original.upper()
        spec_lower = original.lower()

        # Extract and remove finish information
        finish = self._extract_finish(spec_lower)
        if finish:
            for pattern in self.FINISHES.get(finish, []):
                spec_lower = spec_lower.replace(pattern, "").strip()
            spec = spec_lower.upper()

        # Extract and remove grade information
        grade = self._extract_grade(spec)
        if grade:
            # Remove grade from spec for material identification
            spec = re.sub(r'\b(A[24]-\d{2}|\d{1,2}\.\d|Grade\s*\d)\b', '', spec, flags=re.IGNORECASE).strip()

        # Check aliases first
        alias_match = self._check_aliases(spec_lower)
        if alias_match:
            spec = alias_match.upper()

        # Try to identify material
        material = self._identify_material(spec)

        if material:
            result = NormalizedMaterial(
                canonical_name=material.canonical_name,
                family=material.family,
                grade=grade,
                finish=finish,
                equivalents=material.equivalents,
                properties=material.properties,
                original=original,
            )
        else:
            # Unknown material - return cleaned original
            result = NormalizedMaterial(
                canonical_name=self._clean_material_name(original),
                family=self._guess_family(spec),
                grade=grade,
                finish=finish,
                equivalents={},
                properties={},
                original=original,
            )

        # Add grade properties if available
        if grade and grade in GRADE_EQUIVALENTS:
            result.properties.update(GRADE_EQUIVALENTS[grade])

        return result

    def _extract_finish(self, spec: str) -> Optional[str]:
        """Extract surface finish from specification."""
        for finish_name, patterns in self.FINISHES.items():
            for pattern in patterns:
                if pattern in spec:
                    return finish_name
        return None

    def _extract_grade(self, spec: str) -> Optional[str]:
        """Extract grade/property class from specification."""
        # Check property class (8.8, 10.9, 12.9)
        match = self.PATTERNS["property_class"].search(spec)
        if match:
            return f"{match.group(1)}.{match.group(2)}"

        # Check SAE grade
        match = self.PATTERNS["sae_grade"].search(spec)
        if match:
            return f"Grade {match.group(1)}"

        # Check stainless grade (A2-70, A4-80)
        match = self.PATTERNS["stainless_grade"].search(spec)
        if match:
            return f"{match.group(1).upper()}-{match.group(2)}"

        return None

    def _check_aliases(self, spec: str) -> Optional[str]:
        """Check for material aliases."""
        spec = spec.lower().strip()
        for alias, canonical in self.ALIASES.items():
            if alias in spec:
                return canonical
        return None

    def _identify_material(self, spec: str) -> Optional[NormalizedMaterial]:
        """Identify material from specification."""
        # Direct lookup in equivalents
        for key in [spec, spec.replace(" ", ""), spec.replace("-", "")]:
            if key in MATERIAL_EQUIVALENTS:
                equiv = MATERIAL_EQUIVALENTS[key]
                return NormalizedMaterial(
                    canonical_name=equiv.common_name or f"{key} Steel",
                    family=self._get_family(key),
                    equivalents=self._build_equivalents_dict(equiv),
                    properties=self._get_material_properties(key),
                    original=spec,
                )

        # Try pattern matching
        # AISI stainless
        match = self.PATTERNS["aisi_stainless"].match(spec)
        if match:
            base = match.group(1)
            suffix = match.group(2) or ""
            key = f"{base}{suffix}"
            if key in MATERIAL_EQUIVALENTS:
                equiv = MATERIAL_EQUIVALENTS[key]
                return NormalizedMaterial(
                    canonical_name=equiv.common_name or f"{key} Stainless Steel",
                    family=MaterialFamily.STAINLESS_AUSTENITIC,
                    equivalents=self._build_equivalents_dict(equiv),
                    properties=self._get_material_properties(key),
                    original=spec,
                )

        # DIN number
        if self.PATTERNS["din"].match(spec):
            aisi = self._din_to_aisi.get(spec)
            if aisi and aisi in MATERIAL_EQUIVALENTS:
                equiv = MATERIAL_EQUIVALENTS[aisi]
                return NormalizedMaterial(
                    canonical_name=equiv.common_name or f"{aisi} Steel",
                    family=self._get_family(aisi),
                    equivalents=self._build_equivalents_dict(equiv),
                    properties=self._get_material_properties(aisi),
                    original=spec,
                )

        # JIS stainless
        match = self.PATTERNS["jis_stainless"].match(spec)
        if match:
            jis_key = spec.upper()
            aisi = self._jis_to_aisi.get(jis_key)
            if aisi and aisi in MATERIAL_EQUIVALENTS:
                equiv = MATERIAL_EQUIVALENTS[aisi]
                return NormalizedMaterial(
                    canonical_name=equiv.common_name or f"{aisi} Stainless Steel",
                    family=MaterialFamily.STAINLESS_AUSTENITIC,
                    equivalents=self._build_equivalents_dict(equiv),
                    properties=self._get_material_properties(aisi),
                    original=spec,
                )

        # Aluminum
        match = self.PATTERNS["aluminum"].match(spec)
        if match:
            alloy = match.group(1)
            if alloy in MATERIAL_EQUIVALENTS:
                equiv = MATERIAL_EQUIVALENTS[alloy]
                return NormalizedMaterial(
                    canonical_name=equiv.common_name or f"{alloy} Aluminum",
                    family=MaterialFamily.ALUMINUM,
                    equivalents=self._build_equivalents_dict(equiv),
                    properties=self._get_material_properties(alloy),
                    original=spec,
                )

        return None

    def _get_family(self, key: str) -> MaterialFamily:
        """Determine material family from key."""
        key = key.upper()

        if key.startswith("3") and len(key) == 3:
            return MaterialFamily.STAINLESS_AUSTENITIC
        elif key.startswith("4") and len(key) == 3:
            return MaterialFamily.STAINLESS_FERRITIC
        elif key.startswith(("1", "10", "11", "12")):
            return MaterialFamily.CARBON_STEEL
        elif key.startswith(("4", "8", "5")):
            return MaterialFamily.ALLOY_STEEL
        elif key[0].isdigit() and len(key) == 4:
            series = int(key[0])
            if series in [2, 5, 6, 7]:
                return MaterialFamily.ALUMINUM

        return MaterialFamily.UNKNOWN

    def _guess_family(self, spec: str) -> MaterialFamily:
        """Guess material family from specification text."""
        spec_lower = spec.lower()

        if "stainless" in spec_lower or "inox" in spec_lower:
            return MaterialFamily.STAINLESS_AUSTENITIC
        elif "aluminum" in spec_lower or "aluminium" in spec_lower:
            return MaterialFamily.ALUMINUM
        elif "brass" in spec_lower:
            return MaterialFamily.BRASS
        elif "bronze" in spec_lower:
            return MaterialFamily.BRONZE
        elif "titanium" in spec_lower:
            return MaterialFamily.TITANIUM
        elif "alloy" in spec_lower:
            return MaterialFamily.ALLOY_STEEL
        elif "steel" in spec_lower or "carbon" in spec_lower:
            return MaterialFamily.CARBON_STEEL
        elif "nylon" in spec_lower or "plastic" in spec_lower:
            return MaterialFamily.PLASTIC

        return MaterialFamily.UNKNOWN

    def _build_equivalents_dict(self, equiv: MaterialEquivalent) -> Dict[str, str]:
        """Build equivalents dictionary from MaterialEquivalent."""
        result = {}
        if equiv.aisi:
            result["AISI"] = equiv.aisi
        if equiv.din_en:
            result["DIN/EN"] = equiv.din_en
        if equiv.jis:
            result["JIS"] = equiv.jis
        if equiv.bs:
            result["BS"] = equiv.bs
        if equiv.gost:
            result["GOST"] = equiv.gost
        if equiv.uns:
            result["UNS"] = equiv.uns
        return result

    def _get_material_properties(self, key: str) -> Dict[str, Any]:
        """Get material properties for common materials."""
        # Basic properties for common materials
        properties = {
            "304": {"density_g_cm3": 8.0, "melting_point_c": 1400, "magnetic": False},
            "316": {"density_g_cm3": 8.0, "melting_point_c": 1370, "magnetic": False},
            "4140": {"density_g_cm3": 7.85, "melting_point_c": 1415, "magnetic": True},
            "4340": {"density_g_cm3": 7.85, "melting_point_c": 1425, "magnetic": True},
            "6061": {"density_g_cm3": 2.7, "melting_point_c": 582, "magnetic": False},
            "7075": {"density_g_cm3": 2.81, "melting_point_c": 477, "magnetic": False},
        }
        return properties.get(key, {})

    def _clean_material_name(self, name: str) -> str:
        """Clean up a material name for canonical form."""
        # Remove multiple spaces
        name = re.sub(r'\s+', ' ', name)
        # Title case
        return name.strip().title()

    def get_equivalents(self, material_spec: str) -> Dict[str, str]:
        """
        Get equivalent material designations in other standards.

        Args:
            material_spec: Material specification

        Returns:
            Dictionary of standard -> equivalent designation
        """
        parsed = self.parse(material_spec)
        return parsed.equivalents


__all__ = [
    "MaterialNormalizer",
    "NormalizedMaterial",
    "MaterialFamily",
    "MaterialEquivalent",
    "MATERIAL_EQUIVALENTS",
    "GRADE_EQUIVALENTS",
]
