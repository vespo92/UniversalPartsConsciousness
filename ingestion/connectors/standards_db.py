"""
Standards Database Connector
==============================
"Standards are the language of engineering. We speak them all."

Connectors for engineering standards databases:
  - ISO (International Organization for Standardization)
  - DIN (Deutsches Institut für Normung)
  - ANSI (American National Standards Institute)
  - JIS (Japanese Industrial Standards)
  - Thread specification databases

These connectors import standard part definitions — the canonical
specifications that all manufactured parts are built against.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import (
    ConnectorRegistry,
    DataSourceConnector,
    FetchedPart,
    FetchResult,
    SourceConfig,
    SourceTier,
    SourceType,
)

logger = logging.getLogger("UPC.Connector.Standards")


# ============================================================
# ISO STANDARDS (from bundled data)
# ============================================================

ISO_CONFIG = SourceConfig(
    source_id="iso_standards",
    name="ISO Standards Database",
    source_type=SourceType.STANDARDS_DB,
    tier=SourceTier.TIER_2_STANDARDS,
    requests_per_second=100.0,  # Local data, no rate limit needed
    max_concurrent=1,
)


# Bundled ISO metric thread data (ISO 261 / ISO 965)
# This is the canonical reference for metric threads worldwide
ISO_METRIC_THREADS = {
    # Coarse threads (ISO 261)
    # size: (pitch, major_d_nom, pitch_d_nom, minor_d_nom)
    "M1": (0.25, 1.000, 0.838, 0.693),
    "M1.2": (0.25, 1.200, 1.038, 0.893),
    "M1.4": (0.3, 1.400, 1.205, 1.032),
    "M1.6": (0.35, 1.600, 1.373, 1.171),
    "M2": (0.4, 2.000, 1.740, 1.509),
    "M2.5": (0.45, 2.500, 2.208, 1.948),
    "M3": (0.5, 3.000, 2.675, 2.387),
    "M3.5": (0.6, 3.500, 3.110, 2.764),
    "M4": (0.7, 4.000, 3.545, 3.141),
    "M5": (0.8, 5.000, 4.480, 4.019),
    "M6": (1.0, 6.000, 5.350, 4.773),
    "M7": (1.0, 7.000, 6.350, 5.773),
    "M8": (1.25, 8.000, 7.188, 6.466),
    "M10": (1.5, 10.000, 9.026, 8.160),
    "M12": (1.75, 12.000, 10.863, 9.853),
    "M14": (2.0, 14.000, 12.701, 11.546),
    "M16": (2.0, 16.000, 14.701, 13.546),
    "M18": (2.5, 18.000, 16.376, 14.933),
    "M20": (2.5, 20.000, 18.376, 16.933),
    "M22": (2.5, 22.000, 20.376, 18.933),
    "M24": (3.0, 24.000, 22.051, 20.319),
    "M27": (3.0, 27.000, 25.051, 23.319),
    "M30": (3.5, 30.000, 27.727, 25.706),
    "M33": (3.5, 33.000, 30.727, 28.706),
    "M36": (4.0, 36.000, 33.402, 31.093),
    "M39": (4.0, 39.000, 36.402, 34.093),
    "M42": (4.5, 42.000, 39.077, 36.479),
    "M45": (4.5, 45.000, 42.077, 39.479),
    "M48": (5.0, 48.000, 44.752, 41.866),
    "M52": (5.0, 52.000, 48.752, 45.866),
    "M56": (5.5, 56.000, 52.428, 49.252),
    "M60": (5.5, 60.000, 56.428, 53.252),
    "M64": (6.0, 64.000, 60.103, 56.639),
}

# ISO metric fine threads (common sizes)
ISO_METRIC_FINE_THREADS = {
    "M8x1": (1.0, 8.000, 7.350, 6.773),
    "M10x1": (1.0, 10.000, 9.350, 8.773),
    "M10x1.25": (1.25, 10.000, 9.188, 8.466),
    "M12x1.25": (1.25, 12.000, 11.188, 10.466),
    "M12x1.5": (1.5, 12.000, 11.026, 10.160),
    "M14x1.5": (1.5, 14.000, 13.026, 12.160),
    "M16x1.5": (1.5, 16.000, 15.026, 14.160),
    "M18x1.5": (1.5, 18.000, 17.026, 16.160),
    "M18x2": (2.0, 18.000, 16.701, 15.546),
    "M20x1.5": (1.5, 20.000, 19.026, 18.160),
    "M20x2": (2.0, 20.000, 18.701, 17.546),
    "M22x1.5": (1.5, 22.000, 21.026, 20.160),
    "M24x2": (2.0, 24.000, 22.701, 21.546),
    "M27x2": (2.0, 27.000, 25.701, 24.546),
    "M30x2": (2.0, 30.000, 28.701, 27.546),
    "M36x3": (3.0, 36.000, 34.051, 32.319),
}

# Standard fastener grades (ISO 898-1 for steel)
ISO_FASTENER_GRADES = {
    "4.6": {
        "proof_stress_mpa": 225, "tensile_strength_min_mpa": 400,
        "yield_stress_min_mpa": 240, "hardness_hrc_min": None, "hardness_hrc_max": None,
        "material": "Low/Medium Carbon Steel",
    },
    "4.8": {
        "proof_stress_mpa": 310, "tensile_strength_min_mpa": 420,
        "yield_stress_min_mpa": 340, "material": "Low/Medium Carbon Steel",
    },
    "5.6": {
        "proof_stress_mpa": 380, "tensile_strength_min_mpa": 500,
        "yield_stress_min_mpa": 420, "material": "Low/Medium Carbon Steel",
    },
    "5.8": {
        "proof_stress_mpa": 380, "tensile_strength_min_mpa": 520,
        "yield_stress_min_mpa": 420, "material": "Low/Medium Carbon Steel",
    },
    "8.8": {
        "proof_stress_mpa": 580, "tensile_strength_min_mpa": 800,
        "yield_stress_min_mpa": 640, "hardness_hrc_min": 22, "hardness_hrc_max": 32,
        "material": "Medium Carbon Steel, Quenched & Tempered",
    },
    "9.8": {
        "proof_stress_mpa": 650, "tensile_strength_min_mpa": 900,
        "yield_stress_min_mpa": 720, "material": "Medium Carbon Steel, Quenched & Tempered",
    },
    "10.9": {
        "proof_stress_mpa": 830, "tensile_strength_min_mpa": 1040,
        "yield_stress_min_mpa": 940, "hardness_hrc_min": 32, "hardness_hrc_max": 39,
        "material": "Alloy Steel, Quenched & Tempered",
    },
    "12.9": {
        "proof_stress_mpa": 970, "tensile_strength_min_mpa": 1220,
        "yield_stress_min_mpa": 1100, "hardness_hrc_min": 39, "hardness_hrc_max": 44,
        "material": "Alloy Steel, Quenched & Tempered",
    },
    # Stainless grades (ISO 3506-1)
    "A2-50": {
        "proof_stress_mpa": 210, "tensile_strength_min_mpa": 500,
        "yield_stress_min_mpa": 210, "material": "Austenitic Stainless Steel (304)",
    },
    "A2-70": {
        "proof_stress_mpa": 450, "tensile_strength_min_mpa": 700,
        "yield_stress_min_mpa": 450, "material": "Austenitic Stainless Steel (304), Cold Worked",
    },
    "A2-80": {
        "proof_stress_mpa": 600, "tensile_strength_min_mpa": 800,
        "yield_stress_min_mpa": 600, "material": "Austenitic Stainless Steel (304), High Strength",
    },
    "A4-70": {
        "proof_stress_mpa": 450, "tensile_strength_min_mpa": 700,
        "yield_stress_min_mpa": 450, "material": "Austenitic Stainless Steel (316), Cold Worked",
    },
    "A4-80": {
        "proof_stress_mpa": 600, "tensile_strength_min_mpa": 800,
        "yield_stress_min_mpa": 600, "material": "Austenitic Stainless Steel (316), High Strength",
    },
}

# Common DIN/ISO fastener standards mapping
FASTENER_STANDARDS = {
    "DIN 912": {"iso": "ISO 4762", "type": "Socket Head Cap Screw", "taxonomy": "MECH.FAST.SCRW.SHCS"},
    "DIN 7991": {"iso": "ISO 10642", "type": "Flat Head Socket Cap Screw", "taxonomy": "MECH.FAST.SCRW.FHCS"},
    "DIN 7380": {"iso": "ISO 7380", "type": "Button Head Socket Cap Screw", "taxonomy": "MECH.FAST.SCRW.BHCS"},
    "DIN 931": {"iso": "ISO 4014", "type": "Hex Head Bolt (partial thread)", "taxonomy": "MECH.FAST.BOLT.HEX"},
    "DIN 933": {"iso": "ISO 4017", "type": "Hex Head Bolt (full thread)", "taxonomy": "MECH.FAST.BOLT.HEX"},
    "DIN 934": {"iso": "ISO 4032", "type": "Hex Nut", "taxonomy": "MECH.FAST.NUT.HEX"},
    "DIN 985": {"iso": "ISO 10511", "type": "Nyloc Lock Nut", "taxonomy": "MECH.FAST.NUT.LOCK"},
    "DIN 125": {"iso": "ISO 7089", "type": "Flat Washer", "taxonomy": "MECH.FAST.WASH.FLAT"},
    "DIN 127": {"iso": "ISO 7090", "type": "Spring Lock Washer", "taxonomy": "MECH.FAST.WASH.LOCK"},
    "DIN 7984": {"iso": "ISO 14580", "type": "Low Head Socket Cap Screw", "taxonomy": "MECH.FAST.SCRW.SHCS"},
    "DIN 916": {"iso": "ISO 4029", "type": "Cup Point Set Screw", "taxonomy": "MECH.FAST.SCRW.SSET"},
    "DIN 914": {"iso": "ISO 4027", "type": "Cone Point Set Screw", "taxonomy": "MECH.FAST.SCRW.SSET"},
    "DIN 913": {"iso": "ISO 4026", "type": "Flat Point Set Screw", "taxonomy": "MECH.FAST.SCRW.SSET"},
    "DIN 915": {"iso": "ISO 4028", "type": "Dog Point Set Screw", "taxonomy": "MECH.FAST.SCRW.SSET"},
    "DIN 6912": {"iso": None, "type": "Low Head Socket Cap Screw w/ Key Guide", "taxonomy": "MECH.FAST.SCRW.SHCS"},
    "DIN 6921": {"iso": None, "type": "Hex Flange Bolt", "taxonomy": "MECH.FAST.BOLT.FLNG"},
    "DIN 603": {"iso": "ISO 8677", "type": "Carriage Bolt", "taxonomy": "MECH.FAST.BOLT.CARR"},
}

# Standard O-Ring sizes (AS568 / ISO 3601)
STANDARD_ORING_SIZES = {
    # AS568 dash number: (ID_mm, CS_mm)
    "AS568-001": (0.74, 1.02),
    "AS568-002": (1.07, 1.27),
    "AS568-003": (1.42, 1.52),
    "AS568-004": (1.78, 1.78),
    "AS568-005": (2.57, 1.78),
    "AS568-006": (2.90, 1.78),
    "AS568-007": (3.68, 1.78),
    "AS568-010": (6.07, 1.78),
    "AS568-011": (7.65, 1.78),
    "AS568-012": (9.25, 1.78),
    "AS568-013": (10.82, 1.78),
    "AS568-014": (12.42, 1.78),
    "AS568-015": (14.00, 1.78),
    "AS568-016": (15.60, 1.78),
    "AS568-017": (17.17, 1.78),
    "AS568-018": (18.77, 1.78),
    "AS568-110": (9.19, 2.62),
    "AS568-111": (10.77, 2.62),
    "AS568-112": (12.37, 2.62),
    "AS568-113": (13.95, 2.62),
    "AS568-114": (15.54, 2.62),
    "AS568-115": (17.12, 2.62),
    "AS568-116": (18.72, 2.62),
    "AS568-210": (18.64, 3.53),
    "AS568-211": (20.22, 3.53),
    "AS568-212": (21.82, 3.53),
    "AS568-213": (23.39, 3.53),
    "AS568-214": (24.99, 3.53),
    "AS568-215": (26.57, 3.53),
    "AS568-216": (28.17, 3.53),
    "AS568-217": (29.74, 3.53),
    "AS568-218": (31.34, 3.53),
    "AS568-220": (34.52, 3.53),
    "AS568-225": (47.22, 3.53),
    "AS568-230": (63.09, 3.53),
    "AS568-240": (101.19, 3.53),
    "AS568-250": (139.29, 3.53),
    "AS568-325": (37.69, 5.33),
    "AS568-350": (101.32, 5.33),
    "AS568-425": (107.32, 6.99),
    "AS568-450": (228.19, 6.99),
}


@ConnectorRegistry.register("iso_standards")
class ISOStandardsConnector(DataSourceConnector):
    """
    ISO Standards connector — serves canonical thread, fastener,
    and O-ring specifications from bundled reference data.

    This is local data, no external API needed.
    """

    def __init__(self, config: Optional[SourceConfig] = None):
        super().__init__(config or ISO_CONFIG)

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> FetchResult:
        """Search across all bundled standards data."""
        query_lower = query.lower().strip()
        parts: List[FetchedPart] = []

        # Search threads
        parts.extend(self._search_threads(query_lower))

        # Search fastener grades
        parts.extend(self._search_grades(query_lower))

        # Search DIN/ISO standards
        parts.extend(self._search_standards(query_lower))

        # Search O-rings
        parts.extend(self._search_orings(query_lower))

        # Paginate
        start = (page - 1) * page_size
        end = start + page_size
        page_parts = parts[start:end]

        return FetchResult(
            success=True,
            source_id=self.source_id,
            parts=page_parts,
            total_available=len(parts),
            page=page,
            has_more=end < len(parts),
        )

    async def fetch_part(self, part_id: str) -> FetchResult:
        """Fetch a specific standard specification."""
        result = await self.search(part_id, page_size=1)
        return result

    async def fetch_category(
        self, category: str, page: int = 1, page_size: int = 50,
    ) -> FetchResult:
        """Fetch all items in a category."""
        category_lower = category.lower()

        parts: List[FetchedPart] = []

        if "thread" in category_lower or "metric" in category_lower:
            for size, data in {**ISO_METRIC_THREADS, **ISO_METRIC_FINE_THREADS}.items():
                parts.append(self._thread_to_part(size, data))
        elif "grade" in category_lower:
            for grade, data in ISO_FASTENER_GRADES.items():
                parts.append(self._grade_to_part(grade, data))
        elif "oring" in category_lower or "o-ring" in category_lower or "seal" in category_lower:
            for dash, data in STANDARD_ORING_SIZES.items():
                parts.append(self._oring_to_part(dash, data))
        elif "standard" in category_lower or "din" in category_lower or "iso" in category_lower:
            for din, data in FASTENER_STANDARDS.items():
                parts.append(self._standard_to_part(din, data))
        else:
            return await self.search(category, page=page, page_size=page_size)

        start = (page - 1) * page_size
        page_parts = parts[start:start + page_size]

        return FetchResult(
            success=True,
            source_id=self.source_id,
            parts=page_parts,
            total_available=len(parts),
            page=page,
            has_more=(start + page_size) < len(parts),
        )

    def _search_threads(self, query: str) -> List[FetchedPart]:
        """Search ISO metric thread database."""
        parts = []
        all_threads = {**ISO_METRIC_THREADS, **ISO_METRIC_FINE_THREADS}

        for size, data in all_threads.items():
            if query in size.lower() or query in f"m{data[1]}":
                parts.append(self._thread_to_part(size, data))

        return parts

    def _search_grades(self, query: str) -> List[FetchedPart]:
        parts = []
        for grade, data in ISO_FASTENER_GRADES.items():
            if query in grade.lower() or query in data.get("material", "").lower():
                parts.append(self._grade_to_part(grade, data))
        return parts

    def _search_standards(self, query: str) -> List[FetchedPart]:
        parts = []
        for din, data in FASTENER_STANDARDS.items():
            iso = data.get("iso", "")
            if (query in din.lower() or
                (iso and query in iso.lower()) or
                query in data["type"].lower()):
                parts.append(self._standard_to_part(din, data))
        return parts

    def _search_orings(self, query: str) -> List[FetchedPart]:
        parts = []
        for dash, data in STANDARD_ORING_SIZES.items():
            if query in dash.lower() or "oring" in query or "o-ring" in query:
                parts.append(self._oring_to_part(dash, data))
        return parts

    def _thread_to_part(self, size: str, data: tuple) -> FetchedPart:
        pitch, major_d, pitch_d, minor_d = data
        is_fine = "x" in size

        return FetchedPart(
            source_id=f"ISO-THREAD-{size}",
            source_name="ISO Standards",
            raw_data={
                "size": size,
                "pitch": pitch,
                "major_diameter": major_d,
                "pitch_diameter": pitch_d,
                "minor_diameter": minor_d,
                "series": "fine" if is_fine else "coarse",
            },
            name=f"{size} {'Fine' if is_fine else 'Coarse'} Metric Thread (ISO 261)",
            part_number=size,
            description=(
                f"ISO metric {'fine' if is_fine else 'coarse'} thread {size}, "
                f"pitch {pitch}mm, major diameter {major_d}mm"
            ),
            category="thread_specification",
            specifications={
                "thread_spec": f"{size}x{pitch}" if not is_fine else size,
                "pitch_mm": pitch,
                "major_diameter_mm": major_d,
                "pitch_diameter_mm": pitch_d,
                "minor_diameter_mm": minor_d,
                "standard": "ISO 261 / ISO 965",
                "series": "fine" if is_fine else "coarse",
            },
        )

    def _grade_to_part(self, grade: str, data: Dict) -> FetchedPart:
        return FetchedPart(
            source_id=f"ISO-GRADE-{grade}",
            source_name="ISO Standards",
            raw_data=data,
            name=f"Grade {grade} Fastener Specification",
            part_number=grade,
            description=(
                f"ISO {grade} fastener grade — "
                f"tensile {data.get('tensile_strength_min_mpa')} MPa, "
                f"yield {data.get('yield_stress_min_mpa')} MPa"
            ),
            category="fastener_grade",
            material=data.get("material", ""),
            specifications={
                "grade": grade,
                "proof_stress_mpa": data.get("proof_stress_mpa"),
                "tensile_strength_min_mpa": data.get("tensile_strength_min_mpa"),
                "yield_stress_min_mpa": data.get("yield_stress_min_mpa"),
                "hardness_hrc_min": data.get("hardness_hrc_min"),
                "hardness_hrc_max": data.get("hardness_hrc_max"),
                "standard": "ISO 898-1" if not grade.startswith("A") else "ISO 3506-1",
            },
        )

    def _standard_to_part(self, din: str, data: Dict) -> FetchedPart:
        iso = data.get("iso", "")
        return FetchedPart(
            source_id=f"STANDARD-{din.replace(' ', '')}",
            source_name="ISO Standards",
            raw_data=data,
            name=f"{din} / {iso} — {data['type']}" if iso else f"{din} — {data['type']}",
            part_number=din,
            description=f"{data['type']} per {din}" + (f" (equivalent to {iso})" if iso else ""),
            category=data.get("taxonomy", "MECH.FAST"),
            specifications={
                "din_standard": din,
                "iso_standard": iso,
                "fastener_type": data["type"],
                "taxonomy_code": data.get("taxonomy"),
            },
        )

    def _oring_to_part(self, dash: str, data: tuple) -> FetchedPart:
        inner_d, cross_section = data
        return FetchedPart(
            source_id=f"ORING-{dash}",
            source_name="ISO Standards",
            raw_data={"dash_number": dash, "id_mm": inner_d, "cs_mm": cross_section},
            name=f"O-Ring {dash} ({inner_d:.2f} x {cross_section:.2f} mm)",
            part_number=dash,
            description=(
                f"Standard O-ring size {dash}, "
                f"ID {inner_d:.2f}mm, cross-section {cross_section:.2f}mm"
            ),
            category="MECH.SEAL.ORNG",
            specifications={
                "dash_number": dash,
                "inner_diameter_mm": inner_d,
                "cross_section_mm": cross_section,
                "outer_diameter_mm": round(inner_d + 2 * cross_section, 2),
                "standard": "AS568 / ISO 3601",
            },
        )
