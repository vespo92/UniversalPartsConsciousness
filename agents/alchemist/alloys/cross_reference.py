"""
Alloy Standards Cross-Reference Engine

Cross-references alloy designations across international standards:
AA (Aluminum Association), AISI, ASTM, EN, DIN, JIS, GB, BS
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class Standard(Enum):
    """International material standards"""
    AA = "AA"           # Aluminum Association (USA)
    AISI = "AISI"       # American Iron & Steel Institute
    ASTM = "ASTM"       # American Society for Testing & Materials
    SAE = "SAE"         # Society of Automotive Engineers
    UNS = "UNS"         # Unified Numbering System
    EN = "EN"           # European Norm
    DIN = "DIN"         # Deutsches Institut fur Normung (Germany)
    JIS = "JIS"         # Japanese Industrial Standards
    GB = "GB"           # Chinese National Standard
    BS = "BS"           # British Standard
    GOST = "GOST"       # Russian Standard
    AMS = "AMS"         # Aerospace Material Specification


class Equivalence(Enum):
    """Level of equivalence between standards"""
    EXACT = "exact"           # Identical composition and properties
    APPROXIMATE = "approximate"  # Minor composition differences
    SIMILAR = "similar"        # Similar but not interchangeable
    FUNCTIONAL = "functional"   # Different but functionally equivalent


@dataclass
class StandardsMapping:
    """Mapping between two standard designations"""
    source_designation: str
    source_standard: Standard
    target_designation: str
    target_standard: Standard
    equivalence: Equivalence
    composition_notes: str = ""
    property_notes: str = ""
    caution: Optional[str] = None


class CrossReferenceEngine:
    """
    Cross-reference engine for alloy standards.

    Provides mappings between international standards for
    common alloys used in engineering applications.
    """

    def __init__(self):
        self._mappings: Dict[Tuple[str, str, str], StandardsMapping] = {}
        self._load_aluminum_mappings()
        self._load_stainless_mappings()
        self._load_carbon_steel_mappings()
        self._load_titanium_mappings()
        self._load_nickel_mappings()

    def _add_mapping(self, mapping: StandardsMapping):
        """Add a mapping to the database"""
        key = (
            mapping.source_designation,
            mapping.source_standard.value,
            mapping.target_standard.value
        )
        self._mappings[key] = mapping

        # Add reverse mapping
        reverse_key = (
            mapping.target_designation,
            mapping.target_standard.value,
            mapping.source_standard.value
        )
        reverse_mapping = StandardsMapping(
            source_designation=mapping.target_designation,
            source_standard=mapping.target_standard,
            target_designation=mapping.source_designation,
            target_standard=mapping.source_standard,
            equivalence=mapping.equivalence,
            composition_notes=mapping.composition_notes,
            property_notes=mapping.property_notes,
            caution=mapping.caution
        )
        self._mappings[reverse_key] = reverse_mapping

    def _load_aluminum_mappings(self):
        """Load aluminum alloy cross-references"""
        # 6061-T6 mappings
        for target_std, target_des in [
            (Standard.EN, "EN AW-6061-T6"),
            (Standard.JIS, "A6061-T6"),
            (Standard.GB, "6061-T6"),
            (Standard.DIN, "AlMg1SiCu"),
        ]:
            self._add_mapping(StandardsMapping(
                source_designation="6061-T6",
                source_standard=Standard.AA,
                target_designation=target_des,
                target_standard=target_std,
                equivalence=Equivalence.EXACT,
                composition_notes="Identical composition across all standards"
            ))

        # 7075-T6 mappings
        for target_std, target_des in [
            (Standard.EN, "EN AW-7075-T6"),
            (Standard.JIS, "A7075-T6"),
            (Standard.DIN, "AlZnMgCu1.5"),
        ]:
            self._add_mapping(StandardsMapping(
                source_designation="7075-T6",
                source_standard=Standard.AA,
                target_designation=target_des,
                target_standard=target_std,
                equivalence=Equivalence.EXACT
            ))

        # 2024-T3 mappings
        for target_std, target_des in [
            (Standard.EN, "EN AW-2024-T3"),
            (Standard.JIS, "A2024-T3"),
        ]:
            self._add_mapping(StandardsMapping(
                source_designation="2024-T3",
                source_standard=Standard.AA,
                target_designation=target_des,
                target_standard=target_std,
                equivalence=Equivalence.EXACT
            ))

        # 5052-H32 mappings
        for target_std, target_des in [
            (Standard.EN, "EN AW-5052-H32"),
            (Standard.JIS, "A5052-H32"),
        ]:
            self._add_mapping(StandardsMapping(
                source_designation="5052-H32",
                source_standard=Standard.AA,
                target_designation=target_des,
                target_standard=target_std,
                equivalence=Equivalence.EXACT
            ))

    def _load_stainless_mappings(self):
        """Load stainless steel cross-references"""
        # 304 mappings
        self._add_mapping(StandardsMapping(
            source_designation="304",
            source_standard=Standard.AISI,
            target_designation="1.4301",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="X5CrNi18-10"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="304",
            source_standard=Standard.AISI,
            target_designation="SUS304",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))
        self._add_mapping(StandardsMapping(
            source_designation="304",
            source_standard=Standard.AISI,
            target_designation="0Cr18Ni9",
            target_standard=Standard.GB,
            equivalence=Equivalence.EXACT
        ))

        # 316L mappings
        self._add_mapping(StandardsMapping(
            source_designation="316L",
            source_standard=Standard.AISI,
            target_designation="1.4404",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="X2CrNiMo17-12-2"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="316L",
            source_standard=Standard.AISI,
            target_designation="SUS316L",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))
        self._add_mapping(StandardsMapping(
            source_designation="316L",
            source_standard=Standard.AISI,
            target_designation="022Cr17Ni12Mo2",
            target_standard=Standard.GB,
            equivalence=Equivalence.EXACT
        ))

        # 17-4PH mappings
        self._add_mapping(StandardsMapping(
            source_designation="17-4PH",
            source_standard=Standard.AISI,
            target_designation="1.4542",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="X5CrNiCuNb16-4"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="17-4PH",
            source_standard=Standard.AISI,
            target_designation="SUS630",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))

        # 303 (free machining) mappings
        self._add_mapping(StandardsMapping(
            source_designation="303",
            source_standard=Standard.AISI,
            target_designation="1.4305",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT
        ))

        # 430 (ferritic) mappings
        self._add_mapping(StandardsMapping(
            source_designation="430",
            source_standard=Standard.AISI,
            target_designation="1.4016",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT
        ))

    def _load_carbon_steel_mappings(self):
        """Load carbon and alloy steel cross-references"""
        # 1018 mappings
        self._add_mapping(StandardsMapping(
            source_designation="1018",
            source_standard=Standard.AISI,
            target_designation="1.0453",
            target_standard=Standard.EN,
            equivalence=Equivalence.APPROXIMATE,
            composition_notes="C15E4 is closest EN equivalent"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="1018",
            source_standard=Standard.AISI,
            target_designation="S15C",
            target_standard=Standard.JIS,
            equivalence=Equivalence.APPROXIMATE
        ))

        # 4140 mappings
        self._add_mapping(StandardsMapping(
            source_designation="4140",
            source_standard=Standard.AISI,
            target_designation="1.7225",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="42CrMo4"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="4140",
            source_standard=Standard.AISI,
            target_designation="SCM440",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))

        # 4340 mappings
        self._add_mapping(StandardsMapping(
            source_designation="4340",
            source_standard=Standard.AISI,
            target_designation="1.6582",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="34CrNiMo6"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="4340",
            source_standard=Standard.AISI,
            target_designation="SNCM439",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))

        # 8620 mappings
        self._add_mapping(StandardsMapping(
            source_designation="8620",
            source_standard=Standard.AISI,
            target_designation="1.6523",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="21NiCrMo2"
        ))

    def _load_titanium_mappings(self):
        """Load titanium alloy cross-references"""
        # Ti-6Al-4V mappings
        self._add_mapping(StandardsMapping(
            source_designation="Ti-6Al-4V",
            source_standard=Standard.AMS,
            target_designation="3.7165",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="TiAl6V4"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="Ti-6Al-4V",
            source_standard=Standard.AMS,
            target_designation="TAB6V4",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))
        self._add_mapping(StandardsMapping(
            source_designation="Ti-6Al-4V",
            source_standard=Standard.AMS,
            target_designation="Grade 5",
            target_standard=Standard.ASTM,
            equivalence=Equivalence.EXACT
        ))

        # Grade 2 Ti mappings
        self._add_mapping(StandardsMapping(
            source_designation="Grade 2 Ti",
            source_standard=Standard.ASTM,
            target_designation="3.7035",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT
        ))

    def _load_nickel_mappings(self):
        """Load nickel alloy cross-references"""
        # Inconel 718 mappings
        self._add_mapping(StandardsMapping(
            source_designation="Inconel 718",
            source_standard=Standard.AMS,
            target_designation="2.4668",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="NiCr19NbMo"
        ))
        self._add_mapping(StandardsMapping(
            source_designation="Inconel 718",
            source_standard=Standard.AMS,
            target_designation="NCF718",
            target_standard=Standard.JIS,
            equivalence=Equivalence.EXACT
        ))

        # Inconel 625 mappings
        self._add_mapping(StandardsMapping(
            source_designation="Inconel 625",
            source_standard=Standard.AMS,
            target_designation="2.4856",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="NiCr22Mo9Nb"
        ))

        # Hastelloy C-276 mappings
        self._add_mapping(StandardsMapping(
            source_designation="Hastelloy C-276",
            source_standard=Standard.ASTM,
            target_designation="2.4819",
            target_standard=Standard.EN,
            equivalence=Equivalence.EXACT,
            composition_notes="NiMo16Cr15W"
        ))

    def cross_reference(
        self,
        designation: str,
        source_standard: str,
        target_standard: str
    ) -> Optional[StandardsMapping]:
        """
        Find equivalent designation in target standard.

        Args:
            designation: Source alloy designation (e.g., "6061-T6")
            source_standard: Source standard code (e.g., "AA")
            target_standard: Target standard code (e.g., "EN")

        Returns:
            StandardsMapping if found, None otherwise
        """
        key = (designation, source_standard, target_standard)
        return self._mappings.get(key)

    def find_all_equivalents(self, designation: str) -> List[StandardsMapping]:
        """
        Find all equivalent designations for an alloy.

        Args:
            designation: Alloy designation to search

        Returns:
            List of all StandardsMappings for this alloy
        """
        results = []
        for key, mapping in self._mappings.items():
            if key[0] == designation:
                results.append(mapping)
        return results

    def search_by_designation(self, partial: str) -> List[str]:
        """
        Search for designations matching a partial string.

        Args:
            partial: Partial designation to search

        Returns:
            List of matching designations
        """
        matches = set()
        for key in self._mappings.keys():
            if partial.lower() in key[0].lower():
                matches.add(key[0])
        return sorted(matches)


# Demo
if __name__ == "__main__":
    engine = CrossReferenceEngine()

    print("=== Cross-Reference Demo ===\n")

    # Test 6061-T6
    result = engine.cross_reference("6061-T6", "AA", "EN")
    if result:
        print(f"6061-T6 (AA) -> {result.target_designation} ({result.target_standard.value})")
        print(f"Equivalence: {result.equivalence.value}")

    # Test 316L
    result = engine.cross_reference("316L", "AISI", "JIS")
    if result:
        print(f"\n316L (AISI) -> {result.target_designation} ({result.target_standard.value})")

    # Find all equivalents
    print("\n=== All equivalents for Ti-6Al-4V ===")
    for mapping in engine.find_all_equivalents("Ti-6Al-4V"):
        print(f"  {mapping.target_standard.value}: {mapping.target_designation}")
