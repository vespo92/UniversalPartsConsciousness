"""
Fracture Surface Classifier

Classifies fracture surface characteristics to determine failure mode.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class FractureSurfaceAnalysis:
    """Result of fracture surface analysis"""
    primary_mode: str
    secondary_indicators: List[str]
    crack_initiation_site: str
    crack_propagation: str
    environmental_factors: str
    confidence: float
    interpretations: List[str]
    additional_tests_recommended: List[str]


class FractureClassifier:
    """
    Classifies fracture surfaces to determine failure mode.

    Fracture Surface Indicators:
    - Beach marks / striations -> Fatigue
    - Cup-cone or necking -> Ductile overload
    - Flat, granular appearance -> Brittle fracture
    - 45-degree shear lips -> Shear overload
    - Intergranular facets -> Hydrogen embrittlement / SCC
    - Cleavage facets -> Low-temperature brittle fracture
    - Oxidation colors -> High-temperature failure
    - Corrosion products -> Environment-assisted failure
    """

    # Fracture feature keywords and their associated modes
    FEATURE_MODE_MAPPING = {
        # Fatigue indicators
        "beach_marks": ("fatigue", 0.9),
        "beach marks": ("fatigue", 0.9),
        "striations": ("fatigue", 0.85),
        "striation": ("fatigue", 0.85),
        "clamshell": ("fatigue", 0.85),
        "ratchet_marks": ("fatigue", 0.8),
        "ratchet marks": ("fatigue", 0.8),
        "progressive": ("fatigue", 0.7),

        # Ductile overload indicators
        "cup_cone": ("ductile_overload", 0.9),
        "cup-cone": ("ductile_overload", 0.9),
        "cup and cone": ("ductile_overload", 0.9),
        "necking": ("ductile_overload", 0.85),
        "dimples": ("ductile_overload", 0.8),
        "ductile": ("ductile_overload", 0.7),
        "shear_lip": ("ductile_overload", 0.75),
        "shear lip": ("ductile_overload", 0.75),

        # Brittle fracture indicators
        "flat": ("brittle", 0.6),
        "granular": ("brittle", 0.7),
        "cleavage": ("brittle", 0.85),
        "transgranular": ("brittle", 0.75),

        # Hydrogen embrittlement / SCC
        "intergranular": ("hydrogen_embrittlement", 0.85),
        "inter-granular": ("hydrogen_embrittlement", 0.85),
        "rock_candy": ("hydrogen_embrittlement", 0.9),
        "rock candy": ("hydrogen_embrittlement", 0.9),
        "secondary_cracks": ("hydrogen_embrittlement", 0.7),
        "secondary cracks": ("hydrogen_embrittlement", 0.7),
        "delayed": ("hydrogen_embrittlement", 0.6),

        # Stress corrosion cracking
        "branching": ("stress_corrosion", 0.8),
        "branched_cracks": ("stress_corrosion", 0.85),
        "branched cracks": ("stress_corrosion", 0.85),
        "mud_cracking": ("stress_corrosion", 0.8),
        "mud cracking": ("stress_corrosion", 0.8),

        # Corrosion indicators
        "corrosion": ("corrosion", 0.7),
        "rust": ("corrosion", 0.8),
        "oxide": ("corrosion", 0.6),
        "pitting": ("pitting_corrosion", 0.85),
        "pits": ("pitting_corrosion", 0.8),

        # Wear indicators
        "scoring": ("wear", 0.8),
        "galling": ("adhesive_wear", 0.9),
        "seizure": ("adhesive_wear", 0.85),
        "material_transfer": ("adhesive_wear", 0.85),
        "material transfer": ("adhesive_wear", 0.85),
        "abrasion": ("abrasive_wear", 0.85),
        "scratches": ("abrasive_wear", 0.7),

        # Creep indicators
        "creep": ("creep", 0.85),
        "voids": ("creep", 0.6),
        "grain_boundary": ("creep", 0.7),
        "grain boundary": ("creep", 0.7),

        # High temperature
        "oxidation": ("high_temperature", 0.75),
        "heat_tint": ("high_temperature", 0.8),
        "heat tint": ("high_temperature", 0.8),
        "temper_colors": ("high_temperature", 0.8),
        "temper colors": ("high_temperature", 0.8),
    }

    # Initiation site keywords
    INITIATION_KEYWORDS = {
        "surface": "Surface (likely stress concentration or surface defect)",
        "thread": "Thread root (stress concentration)",
        "thread_root": "Thread root (stress concentration)",
        "fillet": "Fillet radius (stress concentration)",
        "corner": "Sharp corner (stress concentration)",
        "inclusion": "Material inclusion (internal defect)",
        "porosity": "Porosity (casting/welding defect)",
        "pit": "Corrosion pit (environment-initiated)",
        "keyway": "Keyway (stress concentration)",
        "hole": "Hole edge (stress concentration)",
        "weld": "Weld zone (heat-affected zone or defect)",
        "subsurface": "Subsurface (internal stress or defect)",
    }

    def __init__(self):
        """Initialize the fracture classifier."""
        pass

    async def classify(
        self,
        fracture_appearance: str,
        fracture_location: str,
        photos: Optional[List[str]] = None
    ) -> FractureSurfaceAnalysis:
        """
        Classify fracture surface characteristics.

        Args:
            fracture_appearance: Description of fracture surface appearance
            fracture_location: Location where fracture occurred
            photos: Optional list of photo paths for visual analysis

        Returns:
            Complete fracture surface analysis
        """
        # Normalize input
        appearance_lower = fracture_appearance.lower()
        location_lower = fracture_location.lower()

        # Find matching features
        mode_scores = {}
        matched_features = []

        for feature, (mode, weight) in self.FEATURE_MODE_MAPPING.items():
            if feature in appearance_lower or feature in location_lower:
                matched_features.append(feature)
                if mode not in mode_scores:
                    mode_scores[mode] = []
                mode_scores[mode].append(weight)

        # Calculate primary mode
        if mode_scores:
            # Average scores per mode
            mode_averages = {
                mode: sum(scores) / len(scores)
                for mode, scores in mode_scores.items()
            }
            primary_mode = max(mode_averages, key=mode_averages.get)
            confidence = min(mode_averages[primary_mode], 0.95)
        else:
            primary_mode = "unknown"
            confidence = 0.3

        # Determine secondary indicators
        secondary_indicators = []
        for mode, scores in mode_scores.items():
            if mode != primary_mode:
                secondary_indicators.append(f"{mode} features present")

        # Determine initiation site
        initiation_site = self._determine_initiation_site(location_lower)

        # Determine propagation characteristics
        propagation = self._determine_propagation(appearance_lower, primary_mode)

        # Check for environmental factors
        environmental = self._check_environmental_factors(appearance_lower)

        # Generate interpretations
        interpretations = self._generate_interpretations(
            primary_mode,
            matched_features,
            initiation_site,
            propagation
        )

        # Recommend additional tests
        additional_tests = self._recommend_tests(primary_mode, confidence)

        return FractureSurfaceAnalysis(
            primary_mode=primary_mode,
            secondary_indicators=secondary_indicators,
            crack_initiation_site=initiation_site,
            crack_propagation=propagation,
            environmental_factors=environmental,
            confidence=confidence,
            interpretations=interpretations,
            additional_tests_recommended=additional_tests
        )

    def _determine_initiation_site(self, location: str) -> str:
        """Determine crack initiation site from location description."""
        for keyword, description in self.INITIATION_KEYWORDS.items():
            if keyword.replace("_", " ") in location or keyword in location:
                return description

        return "Initiation site not clearly identified"

    def _determine_propagation(self, appearance: str, mode: str) -> str:
        """Determine crack propagation characteristics."""
        if mode == "fatigue":
            if "beach" in appearance or "progressive" in appearance:
                return "Progressive, stable fatigue crack growth"
            return "Cyclic loading propagation"

        if mode == "ductile_overload":
            return "Rapid, single-event overload"

        if mode == "brittle":
            return "Rapid, unstable crack propagation"

        if mode in ["hydrogen_embrittlement", "stress_corrosion"]:
            return "Time-dependent, environment-assisted cracking"

        return "Propagation mode requires further analysis"

    def _check_environmental_factors(self, appearance: str) -> str:
        """Check for environmental factors in failure."""
        factors = []

        if "corrosion" in appearance or "rust" in appearance:
            factors.append("Corrosion present")
        if "oxidation" in appearance or "heat" in appearance:
            factors.append("Elevated temperature exposure")
        if "contamination" in appearance:
            factors.append("Contamination detected")
        if "moisture" in appearance or "water" in appearance:
            factors.append("Moisture exposure")

        return "; ".join(factors) if factors else "None evident"

    def _generate_interpretations(
        self,
        primary_mode: str,
        matched_features: List[str],
        initiation_site: str,
        propagation: str
    ) -> List[str]:
        """Generate interpretations of the fracture analysis."""
        interpretations = []

        # Primary mode interpretation
        mode_descriptions = {
            "fatigue": "Fracture characteristics indicate fatigue failure",
            "ductile_overload": "Fracture shows ductile overload characteristics",
            "brittle": "Fracture surface indicates brittle failure",
            "hydrogen_embrittlement": "Evidence suggests hydrogen-induced cracking",
            "stress_corrosion": "Features consistent with stress corrosion cracking",
            "corrosion": "General corrosion damage observed",
            "pitting_corrosion": "Localized pitting corrosion evident",
            "adhesive_wear": "Surface damage indicates adhesive wear",
            "abrasive_wear": "Abrasive wear patterns observed",
            "creep": "Creep damage features present",
            "high_temperature": "High temperature exposure effects visible",
        }

        if primary_mode in mode_descriptions:
            interpretations.append(mode_descriptions[primary_mode])

        # Add feature-specific interpretations
        if "beach_marks" in matched_features or "beach marks" in " ".join(matched_features):
            interpretations.append("Beach marks indicate progressive crack growth under cyclic loading")
        if "intergranular" in matched_features:
            interpretations.append("Intergranular fracture path suggests grain boundary weakness or environmental attack")
        if "necking" in matched_features:
            interpretations.append("Necking indicates ductile material response before final fracture")

        # Add initiation interpretation
        if "stress concentration" in initiation_site:
            interpretations.append(f"Crack initiated at {initiation_site.split('(')[0].strip()}")

        return interpretations

    def _recommend_tests(self, mode: str, confidence: float) -> List[str]:
        """Recommend additional tests based on analysis."""
        tests = []

        if confidence < 0.7:
            tests.append("Optical microscopy for detailed surface examination")
            tests.append("SEM fractography for high-magnification analysis")

        mode_tests = {
            "fatigue": [
                "Striation spacing measurement (SEM)",
                "Hardness testing to verify material",
            ],
            "hydrogen_embrittlement": [
                "Hydrogen content analysis",
                "Grain boundary analysis (SEM)",
                "Material chemistry verification",
            ],
            "stress_corrosion": [
                "Environment sample analysis",
                "Residual stress measurement",
                "Material sensitization check",
            ],
            "corrosion": [
                "Corrosion product analysis (EDS)",
                "Environmental chemistry analysis",
            ],
        }

        if mode in mode_tests:
            tests.extend(mode_tests[mode])

        return tests[:5]  # Limit to top 5 recommendations
