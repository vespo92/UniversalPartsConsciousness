"""
Agent_1 (ARCHIVIST) - Thread Specification Normalizer
======================================================
"One thread, many names. The Archivist unifies all."

Thread specification normalization across global standards:
- ISO (Metric): M6x1.0, M8x1.25, M10x1.5
- ANSI/ASME (Unified): 1/4-20 UNC, #10-24 UNF
- DIN (German Standard): Equivalent to ISO
- JIS (Japanese Industrial): Metric with specific tolerances
- BSW/BSF (British): Whitworth and Fine threads

The normalizer ensures all thread specifications are converted to a
consistent internal format for accurate comparison and consciousness.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ThreadStandard(Enum):
    """Thread specification standards."""
    ISO_METRIC = "ISO"
    ANSI_UNIFIED = "ANSI"
    DIN = "DIN"
    JIS = "JIS"
    BSW = "BSW"  # British Standard Whitworth
    BSF = "BSF"  # British Standard Fine
    UNKNOWN = "UNKNOWN"


class ThreadType(Enum):
    """Thread pitch type."""
    COARSE = "coarse"
    FINE = "fine"
    EXTRA_FINE = "extra_fine"
    UNKNOWN = "unknown"


@dataclass
class NormalizedThread:
    """Result of thread normalization."""
    original_spec: str
    normalized_spec: str
    standard: ThreadStandard
    thread_type: ThreadType

    # Metric specifications
    major_diameter_mm: Optional[float] = None
    pitch_mm: Optional[float] = None

    # Unified specifications
    tpi: Optional[int] = None  # Threads per inch

    # Additional info
    class_fit: Optional[str] = None  # e.g., "6H", "2A"
    hand: str = "right"  # "right" or "left"

    # Parsing confidence
    confidence: float = 1.0
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original_spec,
            "normalized": self.normalized_spec,
            "standard": self.standard.value,
            "thread_type": self.thread_type.value,
            "major_diameter_mm": self.major_diameter_mm,
            "pitch_mm": self.pitch_mm,
            "tpi": self.tpi,
            "class_fit": self.class_fit,
            "hand": self.hand,
            "confidence": self.confidence,
        }


class ThreadNormalizer:
    """
    Thread specification normalizer for Universal Parts Consciousness.

    Converts thread specifications from various formats and standards
    to a consistent internal representation.
    """

    # Metric coarse pitch lookup (ISO 262)
    METRIC_COARSE_PITCH = {
        1.0: 0.25, 1.2: 0.25, 1.4: 0.30, 1.6: 0.35, 1.8: 0.35,
        2.0: 0.40, 2.2: 0.45, 2.5: 0.45, 3.0: 0.50, 3.5: 0.60,
        4.0: 0.70, 4.5: 0.75, 5.0: 0.80, 6.0: 1.00, 7.0: 1.00,
        8.0: 1.25, 10.0: 1.50, 12.0: 1.75, 14.0: 2.00, 16.0: 2.00,
        18.0: 2.50, 20.0: 2.50, 22.0: 2.50, 24.0: 3.00, 27.0: 3.00,
        30.0: 3.50, 33.0: 3.50, 36.0: 4.00, 39.0: 4.00, 42.0: 4.50,
        45.0: 4.50, 48.0: 5.00, 52.0: 5.00, 56.0: 5.50, 60.0: 5.50,
        64.0: 6.00,
    }

    # Metric fine pitch lookup (common values)
    METRIC_FINE_PITCH = {
        (8.0, 1.0): True, (10.0, 1.0): True, (10.0, 1.25): True,
        (12.0, 1.0): True, (12.0, 1.25): True, (12.0, 1.5): True,
        (14.0, 1.5): True, (16.0, 1.5): True, (18.0, 1.5): True,
        (18.0, 2.0): True, (20.0, 1.5): True, (20.0, 2.0): True,
        (22.0, 1.5): True, (22.0, 2.0): True, (24.0, 1.5): True,
        (24.0, 2.0): True, (27.0, 1.5): True, (27.0, 2.0): True,
        (30.0, 1.5): True, (30.0, 2.0): True, (36.0, 2.0): True,
        (36.0, 3.0): True,
    }

    # Unified number screw sizes to decimal inch
    UNIFIED_NUMBER_SIZES = {
        0: 0.0600, 1: 0.0730, 2: 0.0860, 3: 0.0990, 4: 0.1120,
        5: 0.1250, 6: 0.1380, 8: 0.1640, 10: 0.1900, 12: 0.2160,
    }

    # Common UNC (Unified Coarse) threads per inch
    UNC_TPI = {
        "1/4": 20, "5/16": 18, "3/8": 16, "7/16": 14, "1/2": 13,
        "9/16": 12, "5/8": 11, "3/4": 10, "7/8": 9, "1": 8,
        "1-1/8": 7, "1-1/4": 7, "1-3/8": 6, "1-1/2": 6,
        "#0": 80, "#1": 64, "#2": 56, "#3": 48, "#4": 40,
        "#5": 40, "#6": 32, "#8": 32, "#10": 24, "#12": 24,
    }

    # Common UNF (Unified Fine) threads per inch
    UNF_TPI = {
        "1/4": 28, "5/16": 24, "3/8": 24, "7/16": 20, "1/2": 20,
        "9/16": 18, "5/8": 18, "3/4": 16, "7/8": 14, "1": 12,
        "1-1/8": 12, "1-1/4": 12, "1-3/8": 12, "1-1/2": 12,
        "#0": 80, "#1": 72, "#2": 64, "#3": 56, "#4": 48,
        "#5": 44, "#6": 40, "#8": 36, "#10": 32, "#12": 28,
    }

    # Regex patterns
    PATTERNS = {
        # Metric: M8x1.25, M8-1.25, M8 x 1.25, M 8 x 1.25
        "metric_full": re.compile(
            r'^M\s*(\d+(?:\.\d+)?)\s*[x×-]\s*(\d+(?:\.\d+)?)\s*(?:\s*LH)?$',
            re.IGNORECASE
        ),
        # Metric coarse: M8, M 8
        "metric_coarse": re.compile(
            r'^M\s*(\d+(?:\.\d+)?)\s*(?:\s*LH)?$',
            re.IGNORECASE
        ),
        # Unified fractional: 1/4-20 UNC, 1/4"-20, 1/4-20
        "unified_fractional": re.compile(
            r'^(\d+(?:-\d+)?/\d+)\s*["\']?\s*-?\s*(\d+)\s*(UNC|UNF|UNEF)?(?:\s*-?\s*(\d[AB]))?(?:\s*LH)?$',
            re.IGNORECASE
        ),
        # Unified numbered: #10-24, #10-24 UNC, No. 10-24
        "unified_numbered": re.compile(
            r'^(?:#|No\.?\s*)(\d+)\s*-\s*(\d+)\s*(UNC|UNF|UNEF)?(?:\s*-?\s*(\d[AB]))?(?:\s*LH)?$',
            re.IGNORECASE
        ),
        # British Whitworth: 1/4 BSW, 1/4" BSW
        "british_whitworth": re.compile(
            r'^(\d+/\d+)\s*["\']?\s*(BSW|BSF|BA)$',
            re.IGNORECASE
        ),
    }

    def __init__(self, prefer_metric: bool = True):
        """
        Initialize the thread normalizer.

        Args:
            prefer_metric: If true, output metric specs when possible
        """
        self.prefer_metric = prefer_metric

    def normalize(self, thread_spec: str) -> NormalizedThread:
        """
        Normalize a thread specification.

        Args:
            thread_spec: Raw thread specification string

        Returns:
            NormalizedThread with normalized data
        """
        spec = thread_spec.strip()
        is_left_hand = "LH" in spec.upper() or "LEFT" in spec.upper()

        # Try each pattern
        result = self._try_metric_full(spec)
        if result:
            result.hand = "left" if is_left_hand else "right"
            return result

        result = self._try_metric_coarse(spec)
        if result:
            result.hand = "left" if is_left_hand else "right"
            return result

        result = self._try_unified_fractional(spec)
        if result:
            result.hand = "left" if is_left_hand else "right"
            return result

        result = self._try_unified_numbered(spec)
        if result:
            result.hand = "left" if is_left_hand else "right"
            return result

        result = self._try_british(spec)
        if result:
            result.hand = "left" if is_left_hand else "right"
            return result

        # Unable to parse - return cleaned original
        return NormalizedThread(
            original_spec=thread_spec,
            normalized_spec=self._clean_spec(spec),
            standard=ThreadStandard.UNKNOWN,
            thread_type=ThreadType.UNKNOWN,
            confidence=0.3,
            notes=["Unable to parse thread specification"],
        )

    def _try_metric_full(self, spec: str) -> Optional[NormalizedThread]:
        """Try to parse as full metric thread (M8x1.25)."""
        match = self.PATTERNS["metric_full"].match(spec)
        if not match:
            return None

        diameter = float(match.group(1))
        pitch = float(match.group(2))

        # Determine thread type
        coarse_pitch = self.METRIC_COARSE_PITCH.get(diameter)
        if coarse_pitch and abs(pitch - coarse_pitch) < 0.01:
            thread_type = ThreadType.COARSE
        elif (diameter, pitch) in self.METRIC_FINE_PITCH:
            thread_type = ThreadType.FINE
        else:
            thread_type = ThreadType.FINE  # Assume fine for non-standard

        normalized = f"M{diameter:g}x{pitch:g}"

        return NormalizedThread(
            original_spec=spec,
            normalized_spec=normalized,
            standard=ThreadStandard.ISO_METRIC,
            thread_type=thread_type,
            major_diameter_mm=diameter,
            pitch_mm=pitch,
            confidence=1.0,
        )

    def _try_metric_coarse(self, spec: str) -> Optional[NormalizedThread]:
        """Try to parse as coarse metric thread (M8)."""
        match = self.PATTERNS["metric_coarse"].match(spec)
        if not match:
            return None

        diameter = float(match.group(1))
        pitch = self.METRIC_COARSE_PITCH.get(diameter)

        if pitch:
            normalized = f"M{diameter:g}x{pitch:g}"
            confidence = 1.0
        else:
            # Unknown diameter, assume coarse exists
            normalized = f"M{diameter:g}"
            pitch = None
            confidence = 0.7

        return NormalizedThread(
            original_spec=spec,
            normalized_spec=normalized,
            standard=ThreadStandard.ISO_METRIC,
            thread_type=ThreadType.COARSE,
            major_diameter_mm=diameter,
            pitch_mm=pitch,
            confidence=confidence,
            notes=[] if pitch else ["Coarse pitch assumed but not verified"],
        )

    def _try_unified_fractional(self, spec: str) -> Optional[NormalizedThread]:
        """Try to parse as unified fractional thread (1/4-20)."""
        match = self.PATTERNS["unified_fractional"].match(spec)
        if not match:
            return None

        size = match.group(1)
        tpi = int(match.group(2))
        series = match.group(3).upper() if match.group(3) else None
        class_fit = match.group(4)

        # Clean up size (handle mixed fractions like 1-1/2)
        if '-' in size and '/' in size.split('-')[1]:
            parts = size.split('-')
            whole = int(parts[0])
            frac = parts[1]
            num, denom = map(int, frac.split('/'))
            diameter_inch = whole + num / denom
        else:
            num, denom = map(int, size.split('/'))
            diameter_inch = num / denom

        diameter_mm = diameter_inch * 25.4
        pitch_mm = 25.4 / tpi

        # Determine thread type from series or TPI
        if series:
            if series == "UNC":
                thread_type = ThreadType.COARSE
            elif series == "UNF":
                thread_type = ThreadType.FINE
            else:
                thread_type = ThreadType.EXTRA_FINE
        else:
            # Infer from TPI
            size_key = f"{size}"
            if size_key in self.UNC_TPI and self.UNC_TPI[size_key] == tpi:
                thread_type = ThreadType.COARSE
                series = "UNC"
            elif size_key in self.UNF_TPI and self.UNF_TPI[size_key] == tpi:
                thread_type = ThreadType.FINE
                series = "UNF"
            else:
                thread_type = ThreadType.UNKNOWN

        normalized = f"{size}-{tpi}"
        if series:
            normalized += f" {series}"

        return NormalizedThread(
            original_spec=spec,
            normalized_spec=normalized,
            standard=ThreadStandard.ANSI_UNIFIED,
            thread_type=thread_type,
            major_diameter_mm=round(diameter_mm, 3),
            pitch_mm=round(pitch_mm, 4),
            tpi=tpi,
            class_fit=class_fit,
            confidence=1.0 if series else 0.9,
        )

    def _try_unified_numbered(self, spec: str) -> Optional[NormalizedThread]:
        """Try to parse as unified numbered thread (#10-24)."""
        match = self.PATTERNS["unified_numbered"].match(spec)
        if not match:
            return None

        number = int(match.group(1))
        tpi = int(match.group(2))
        series = match.group(3).upper() if match.group(3) else None
        class_fit = match.group(4)

        # Get diameter from lookup
        diameter_inch = self.UNIFIED_NUMBER_SIZES.get(number)
        if diameter_inch:
            diameter_mm = diameter_inch * 25.4
        else:
            diameter_mm = None

        pitch_mm = 25.4 / tpi if tpi > 0 else None

        # Determine thread type
        size_key = f"#{number}"
        if series:
            if series == "UNC":
                thread_type = ThreadType.COARSE
            elif series == "UNF":
                thread_type = ThreadType.FINE
            else:
                thread_type = ThreadType.EXTRA_FINE
        else:
            if size_key in self.UNC_TPI and self.UNC_TPI[size_key] == tpi:
                thread_type = ThreadType.COARSE
                series = "UNC"
            elif size_key in self.UNF_TPI and self.UNF_TPI[size_key] == tpi:
                thread_type = ThreadType.FINE
                series = "UNF"
            else:
                thread_type = ThreadType.UNKNOWN

        normalized = f"#{number}-{tpi}"
        if series:
            normalized += f" {series}"

        return NormalizedThread(
            original_spec=spec,
            normalized_spec=normalized,
            standard=ThreadStandard.ANSI_UNIFIED,
            thread_type=thread_type,
            major_diameter_mm=round(diameter_mm, 3) if diameter_mm else None,
            pitch_mm=round(pitch_mm, 4) if pitch_mm else None,
            tpi=tpi,
            class_fit=class_fit,
            confidence=0.95 if diameter_mm else 0.8,
        )

    def _try_british(self, spec: str) -> Optional[NormalizedThread]:
        """Try to parse as British standard thread."""
        match = self.PATTERNS["british_whitworth"].match(spec)
        if not match:
            return None

        size = match.group(1)
        standard_code = match.group(2).upper()

        num, denom = map(int, size.split('/'))
        diameter_inch = num / denom
        diameter_mm = diameter_inch * 25.4

        if standard_code == "BSW":
            standard = ThreadStandard.BSW
            thread_type = ThreadType.COARSE
        elif standard_code == "BSF":
            standard = ThreadStandard.BSF
            thread_type = ThreadType.FINE
        else:
            standard = ThreadStandard.UNKNOWN
            thread_type = ThreadType.UNKNOWN

        normalized = f"{size} {standard_code}"

        return NormalizedThread(
            original_spec=spec,
            normalized_spec=normalized,
            standard=standard,
            thread_type=thread_type,
            major_diameter_mm=round(diameter_mm, 3),
            confidence=0.9,
            notes=["British thread standards require specific TPI lookup"],
        )

    def _clean_spec(self, spec: str) -> str:
        """Clean and normalize a spec string."""
        # Uppercase
        spec = spec.upper()
        # Remove extra spaces
        spec = re.sub(r'\s+', ' ', spec).strip()
        # Normalize separators
        spec = spec.replace('×', 'x').replace('X', 'x')
        return spec

    def to_metric(self, thread: NormalizedThread) -> Optional[str]:
        """
        Convert any thread to metric equivalent.

        Args:
            thread: Normalized thread specification

        Returns:
            Metric thread string (e.g., "M6.35x1.27") or None if not convertible
        """
        if thread.standard == ThreadStandard.ISO_METRIC:
            return thread.normalized_spec

        if thread.major_diameter_mm and thread.pitch_mm:
            diameter = round(thread.major_diameter_mm, 2)
            pitch = round(thread.pitch_mm, 3)
            return f"M{diameter}x{pitch}"

        return None

    def are_compatible(
        self,
        thread_a: NormalizedThread,
        thread_b: NormalizedThread,
        tolerance_pct: float = 0.02,
    ) -> bool:
        """
        Check if two threads are mechanically compatible.

        Args:
            thread_a: First thread specification
            thread_b: Second thread specification
            tolerance_pct: Dimensional tolerance percentage

        Returns:
            True if threads are compatible
        """
        if not (thread_a.major_diameter_mm and thread_b.major_diameter_mm):
            return False
        if not (thread_a.pitch_mm and thread_b.pitch_mm):
            return False

        # Check diameter within tolerance
        avg_dia = (thread_a.major_diameter_mm + thread_b.major_diameter_mm) / 2
        dia_diff = abs(thread_a.major_diameter_mm - thread_b.major_diameter_mm)
        if dia_diff / avg_dia > tolerance_pct:
            return False

        # Check pitch within tolerance
        avg_pitch = (thread_a.pitch_mm + thread_b.pitch_mm) / 2
        pitch_diff = abs(thread_a.pitch_mm - thread_b.pitch_mm)
        if pitch_diff / avg_pitch > tolerance_pct:
            return False

        # Check handedness
        if thread_a.hand != thread_b.hand:
            return False

        return True


# Convenience functions
def normalize_thread(spec: str) -> NormalizedThread:
    """Normalize a thread specification."""
    normalizer = ThreadNormalizer()
    return normalizer.normalize(spec)


def threads_compatible(spec_a: str, spec_b: str) -> bool:
    """Check if two thread specifications are compatible."""
    normalizer = ThreadNormalizer()
    thread_a = normalizer.normalize(spec_a)
    thread_b = normalizer.normalize(spec_b)
    return normalizer.are_compatible(thread_a, thread_b)


__all__ = [
    "ThreadNormalizer",
    "NormalizedThread",
    "ThreadStandard",
    "ThreadType",
    "normalize_thread",
    "threads_compatible",
]
