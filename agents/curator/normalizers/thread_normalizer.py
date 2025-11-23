"""
Agent_1 (ARCHIVIST) - Thread Specification Normalizer
======================================================
"One thread, many names. The Archivist knows them all."

Normalizes thread specifications across international standards:
- ISO (Metric): M8x1.25
- ANSI/ASME (Unified): 1/4-20 UNC, #10-24 UNF
- DIN (German): M8x1.25 (same as ISO)
- JIS (Japanese): M8x1.25 (same as ISO with variations)
- BSW/BSF (British Whitworth): 1/4" BSW
- GOST (Russian): M8x1.25 (Cyrillic designations)
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ThreadStandard(Enum):
    """International thread standards."""
    ISO = "ISO"           # International (Metric)
    ANSI_UNC = "ANSI_UNC" # American National Coarse
    ANSI_UNF = "ANSI_UNF" # American National Fine
    ANSI_UNEF = "ANSI_UNEF" # American National Extra Fine
    BSW = "BSW"           # British Standard Whitworth
    BSF = "BSF"           # British Standard Fine
    BA = "BA"             # British Association
    NPT = "NPT"           # National Pipe Thread
    BSPT = "BSPT"         # British Standard Pipe Thread
    DIN = "DIN"           # German (equiv to ISO)
    JIS = "JIS"           # Japanese (equiv to ISO)
    GOST = "GOST"         # Russian


@dataclass
class NormalizedThread:
    """Normalized thread specification."""
    canonical: str              # Canonical representation (e.g., "M8x1.25")
    standard: ThreadStandard    # Primary standard
    diameter_mm: float          # Major diameter in mm
    pitch_mm: Optional[float]   # Pitch in mm (None for coarse)
    is_coarse: bool            # True if coarse pitch
    tpi: Optional[float]       # Threads per inch (for unified)
    thread_class: Optional[str] # Class/tolerance (2A, 6g, etc.)
    original: str              # Original input


class ThreadNormalizer:
    """
    Thread specification normalizer.

    Converts thread specifications from any standard to a canonical format,
    and provides cross-reference mappings between standards.
    """

    # Metric coarse pitches (ISO 261)
    METRIC_COARSE_PITCHES = {
        1.0: 0.25, 1.2: 0.25, 1.4: 0.3, 1.6: 0.35, 1.8: 0.35,
        2.0: 0.4, 2.2: 0.45, 2.5: 0.45, 3.0: 0.5, 3.5: 0.6,
        4.0: 0.7, 4.5: 0.75, 5.0: 0.8, 6.0: 1.0, 7.0: 1.0,
        8.0: 1.25, 10.0: 1.5, 12.0: 1.75, 14.0: 2.0, 16.0: 2.0,
        18.0: 2.5, 20.0: 2.5, 22.0: 2.5, 24.0: 3.0, 27.0: 3.0,
        30.0: 3.5, 33.0: 3.5, 36.0: 4.0, 39.0: 4.0, 42.0: 4.5,
        45.0: 4.5, 48.0: 5.0, 52.0: 5.0, 56.0: 5.5, 60.0: 5.5,
        64.0: 6.0, 68.0: 6.0,
    }

    # Unified National coarse pitches (TPI)
    UNC_PITCHES = {
        "#0": 80, "#1": 64, "#2": 56, "#3": 48, "#4": 40, "#5": 40,
        "#6": 32, "#8": 32, "#10": 24, "#12": 24,
        "1/4": 20, "5/16": 18, "3/8": 16, "7/16": 14,
        "1/2": 13, "9/16": 12, "5/8": 11, "3/4": 10,
        "7/8": 9, "1": 8, "1-1/8": 7, "1-1/4": 7, "1-3/8": 6,
        "1-1/2": 6, "1-3/4": 5, "2": 4.5,
    }

    # Unified National fine pitches (TPI)
    UNF_PITCHES = {
        "#0": 80, "#1": 72, "#2": 64, "#3": 56, "#4": 48, "#5": 44,
        "#6": 40, "#8": 36, "#10": 32, "#12": 28,
        "1/4": 28, "5/16": 24, "3/8": 24, "7/16": 20,
        "1/2": 20, "9/16": 18, "5/8": 18, "3/4": 16,
        "7/8": 14, "1": 12, "1-1/8": 12, "1-1/4": 12, "1-3/8": 12,
        "1-1/2": 12,
    }

    # Numbered screw sizes to diameter (inches)
    NUMBERED_SIZES = {
        0: 0.060, 1: 0.073, 2: 0.086, 3: 0.099, 4: 0.112,
        5: 0.125, 6: 0.138, 8: 0.164, 10: 0.190, 12: 0.216,
    }

    # Regex patterns for thread parsing
    PATTERNS = {
        # Metric: M8, M8x1.25, M8-1.25, M8 x 1.25
        "metric": re.compile(
            r'^M(\d+(?:\.\d+)?)\s*[x×\-]?\s*(\d+(?:\.\d+)?)?\s*'
            r'(?:[-\s]?([46][ghHG]))?$',
            re.IGNORECASE
        ),
        # Unified fractional: 1/4-20, 1/4"-20, 1/4-20 UNC
        "unified_frac": re.compile(
            r'^(\d+(?:-\d+)?/\d+)["\s]*-?\s*(\d+)\s*'
            r'(UNC|UNF|UNEF|UN)?\s*(?:-?\s*([123][AB]))?$',
            re.IGNORECASE
        ),
        # Unified numbered: #10-24, #8-32, #6-40
        "unified_num": re.compile(
            r'^#(\d+)\s*-?\s*(\d+)\s*(UNC|UNF|UNEF|UN)?\s*(?:-?\s*([123][AB]))?$',
            re.IGNORECASE
        ),
        # BSW/BSF: 1/4" BSW, 3/8 BSF
        "british": re.compile(
            r'^(\d+/\d+)["\s]*(BSW|BSF|BA)$',
            re.IGNORECASE
        ),
        # Pipe threads: 1/4 NPT, 1/2" BSPT
        "pipe": re.compile(
            r'^(\d+(?:/\d+)?)["\s]*(NPT|BSPT|BSPP|NPS)$',
            re.IGNORECASE
        ),
    }

    def __init__(self, default_standard: ThreadStandard = ThreadStandard.ISO):
        """
        Initialize the thread normalizer.

        Args:
            default_standard: Default standard for ambiguous specifications
        """
        self.default_standard = default_standard

    def normalize(self, thread_spec: str) -> str:
        """
        Normalize a thread specification to canonical format.

        Args:
            thread_spec: Input thread specification

        Returns:
            Canonical thread specification string
        """
        parsed = self.parse(thread_spec)
        return parsed.canonical

    def parse(self, thread_spec: str) -> NormalizedThread:
        """
        Parse and normalize a thread specification.

        Args:
            thread_spec: Input thread specification

        Returns:
            NormalizedThread with all parsed details
        """
        original = thread_spec.strip()
        spec = original.upper()

        # Try metric pattern
        match = self.PATTERNS["metric"].match(spec)
        if match:
            return self._parse_metric(match, original)

        # Try unified fractional
        match = self.PATTERNS["unified_frac"].match(spec)
        if match:
            return self._parse_unified_frac(match, original)

        # Try unified numbered
        match = self.PATTERNS["unified_num"].match(spec)
        if match:
            return self._parse_unified_num(match, original)

        # Try British
        match = self.PATTERNS["british"].match(spec)
        if match:
            return self._parse_british(match, original)

        # Try pipe thread
        match = self.PATTERNS["pipe"].match(spec)
        if match:
            return self._parse_pipe(match, original)

        # Could not parse - return cleaned original
        return NormalizedThread(
            canonical=original,
            standard=self.default_standard,
            diameter_mm=0.0,
            pitch_mm=None,
            is_coarse=True,
            tpi=None,
            thread_class=None,
            original=original,
        )

    def _parse_metric(self, match: re.Match, original: str) -> NormalizedThread:
        """Parse metric thread specification."""
        diameter = float(match.group(1))
        pitch = float(match.group(2)) if match.group(2) else None
        thread_class = match.group(3)

        # Determine if coarse pitch
        coarse_pitch = self.METRIC_COARSE_PITCHES.get(diameter)
        is_coarse = pitch is None or (coarse_pitch and abs(pitch - coarse_pitch) < 0.01)

        # Use coarse pitch if not specified
        if pitch is None:
            pitch = coarse_pitch

        # Build canonical form
        if pitch:
            canonical = f"M{diameter:g}x{pitch:g}"
        else:
            canonical = f"M{diameter:g}"

        if thread_class:
            canonical += f"-{thread_class.lower()}"

        return NormalizedThread(
            canonical=canonical,
            standard=ThreadStandard.ISO,
            diameter_mm=diameter,
            pitch_mm=pitch,
            is_coarse=is_coarse,
            tpi=25.4 / pitch if pitch else None,
            thread_class=thread_class,
            original=original,
        )

    def _parse_unified_frac(self, match: re.Match, original: str) -> NormalizedThread:
        """Parse unified fractional thread specification."""
        size_str = match.group(1)
        tpi = int(match.group(2))
        series = match.group(3)
        thread_class = match.group(4)

        # Parse fractional diameter
        diameter_inch = self._parse_fraction(size_str)
        diameter_mm = diameter_inch * 25.4
        pitch_mm = 25.4 / tpi

        # Determine series
        if series:
            series = series.upper()
        else:
            # Infer from TPI
            unc_tpi = self.UNC_PITCHES.get(size_str)
            unf_tpi = self.UNF_PITCHES.get(size_str)

            if unc_tpi and tpi == unc_tpi:
                series = "UNC"
            elif unf_tpi and tpi == unf_tpi:
                series = "UNF"
            else:
                series = "UN"

        is_coarse = series == "UNC"

        # Build canonical
        canonical = f"{size_str}-{tpi}"
        if series:
            canonical += f" {series}"
        if thread_class:
            canonical += f"-{thread_class.upper()}"

        standard = {
            "UNC": ThreadStandard.ANSI_UNC,
            "UNF": ThreadStandard.ANSI_UNF,
            "UNEF": ThreadStandard.ANSI_UNEF,
        }.get(series, ThreadStandard.ANSI_UNC)

        return NormalizedThread(
            canonical=canonical,
            standard=standard,
            diameter_mm=diameter_mm,
            pitch_mm=pitch_mm,
            is_coarse=is_coarse,
            tpi=float(tpi),
            thread_class=thread_class,
            original=original,
        )

    def _parse_unified_num(self, match: re.Match, original: str) -> NormalizedThread:
        """Parse unified numbered thread specification."""
        num = int(match.group(1))
        tpi = int(match.group(2))
        series = match.group(3)
        thread_class = match.group(4)

        # Get diameter from numbered size
        diameter_inch = self.NUMBERED_SIZES.get(num, 0.060 + num * 0.013)
        diameter_mm = diameter_inch * 25.4
        pitch_mm = 25.4 / tpi

        # Determine series
        size_str = f"#{num}"
        if series:
            series = series.upper()
        else:
            unc_tpi = self.UNC_PITCHES.get(size_str)
            unf_tpi = self.UNF_PITCHES.get(size_str)

            if unc_tpi and tpi == unc_tpi:
                series = "UNC"
            elif unf_tpi and tpi == unf_tpi:
                series = "UNF"
            else:
                series = "UN"

        is_coarse = series == "UNC"

        # Build canonical
        canonical = f"#{num}-{tpi}"
        if series:
            canonical += f" {series}"
        if thread_class:
            canonical += f"-{thread_class.upper()}"

        standard = {
            "UNC": ThreadStandard.ANSI_UNC,
            "UNF": ThreadStandard.ANSI_UNF,
            "UNEF": ThreadStandard.ANSI_UNEF,
        }.get(series, ThreadStandard.ANSI_UNC)

        return NormalizedThread(
            canonical=canonical,
            standard=standard,
            diameter_mm=diameter_mm,
            pitch_mm=pitch_mm,
            is_coarse=is_coarse,
            tpi=float(tpi),
            thread_class=thread_class,
            original=original,
        )

    def _parse_british(self, match: re.Match, original: str) -> NormalizedThread:
        """Parse British thread specification."""
        size_str = match.group(1)
        standard_str = match.group(2).upper()

        diameter_inch = self._parse_fraction(size_str)
        diameter_mm = diameter_inch * 25.4

        # British Whitworth has 55-degree thread angle
        # TPI varies by size
        bsw_tpi = {
            "1/8": 40, "3/16": 24, "1/4": 20, "5/16": 18, "3/8": 16,
            "7/16": 14, "1/2": 12, "9/16": 12, "5/8": 11, "11/16": 11,
            "3/4": 10, "7/8": 9, "1": 8,
        }

        tpi = bsw_tpi.get(size_str, 20)
        pitch_mm = 25.4 / tpi

        standard = ThreadStandard.BSW if standard_str == "BSW" else ThreadStandard.BSF
        is_coarse = standard == ThreadStandard.BSW

        return NormalizedThread(
            canonical=f'{size_str}" {standard_str}',
            standard=standard,
            diameter_mm=diameter_mm,
            pitch_mm=pitch_mm,
            is_coarse=is_coarse,
            tpi=float(tpi),
            thread_class=None,
            original=original,
        )

    def _parse_pipe(self, match: re.Match, original: str) -> NormalizedThread:
        """Parse pipe thread specification."""
        size_str = match.group(1)
        standard_str = match.group(2).upper()

        # Pipe threads use nominal sizes, not actual diameters
        # This is a simplified mapping
        npt_tpi = {
            "1/8": 27, "1/4": 18, "3/8": 18, "1/2": 14,
            "3/4": 14, "1": 11.5, "1-1/4": 11.5, "1-1/2": 11.5,
            "2": 11.5, "2-1/2": 8, "3": 8, "4": 8,
        }

        tpi = npt_tpi.get(size_str, 14)
        pitch_mm = 25.4 / tpi

        standard = {
            "NPT": ThreadStandard.NPT,
            "BSPT": ThreadStandard.BSPT,
        }.get(standard_str, ThreadStandard.NPT)

        return NormalizedThread(
            canonical=f'{size_str}" {standard_str}',
            standard=standard,
            diameter_mm=0.0,  # Nominal, not actual
            pitch_mm=pitch_mm,
            is_coarse=True,
            tpi=float(tpi),
            thread_class=None,
            original=original,
        )

    def _parse_fraction(self, frac_str: str) -> float:
        """Parse a fractional string like '1/4' or '1-1/2' to decimal."""
        if '-' in frac_str:
            # Mixed number: 1-1/2
            parts = frac_str.split('-')
            whole = float(parts[0])
            num, denom = parts[1].split('/')
            return whole + float(num) / float(denom)
        elif '/' in frac_str:
            # Simple fraction: 1/4
            num, denom = frac_str.split('/')
            return float(num) / float(denom)
        else:
            return float(frac_str)

    def get_equivalents(self, thread_spec: str) -> Dict[str, str]:
        """
        Get equivalent thread specifications in other standards.

        Args:
            thread_spec: Thread specification to find equivalents for

        Returns:
            Dictionary of standard -> equivalent specification
        """
        parsed = self.parse(thread_spec)
        equivalents = {parsed.standard.value: parsed.canonical}

        # For metric threads, find close unified equivalents
        if parsed.standard == ThreadStandard.ISO and parsed.diameter_mm:
            # Find closest unified size
            closest_unified = self._find_closest_unified(parsed.diameter_mm)
            if closest_unified:
                equivalents["ANSI_UNC"] = closest_unified

        # For unified threads, find close metric equivalents
        elif parsed.standard in [ThreadStandard.ANSI_UNC, ThreadStandard.ANSI_UNF]:
            closest_metric = self._find_closest_metric(parsed.diameter_mm)
            if closest_metric:
                equivalents["ISO"] = closest_metric

        return equivalents

    def _find_closest_metric(self, diameter_mm: float) -> Optional[str]:
        """Find the closest metric thread size."""
        metric_sizes = list(self.METRIC_COARSE_PITCHES.keys())
        closest = min(metric_sizes, key=lambda x: abs(x - diameter_mm))

        # Only return if within 5%
        if abs(closest - diameter_mm) / diameter_mm < 0.05:
            pitch = self.METRIC_COARSE_PITCHES[closest]
            return f"M{closest:g}x{pitch:g}"

        return None

    def _find_closest_unified(self, diameter_mm: float) -> Optional[str]:
        """Find the closest unified thread size."""
        diameter_inch = diameter_mm / 25.4

        # Check fractional sizes
        for size_str, tpi in self.UNC_PITCHES.items():
            if size_str.startswith('#'):
                continue
            size_inch = self._parse_fraction(size_str)
            if abs(size_inch - diameter_inch) / diameter_inch < 0.05:
                return f"{size_str}-{tpi} UNC"

        return None


__all__ = [
    "ThreadNormalizer",
    "NormalizedThread",
    "ThreadStandard",
]
