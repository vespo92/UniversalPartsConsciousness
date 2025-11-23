"""
Agent_1 (ARCHIVIST) - Dimension Normalizer
===========================================
"All measurements speak the same language."

Normalizes dimensional specifications:
- Length units: mm, cm, m, in, ft
- Angular units: degrees, radians, gradians
- Tolerance parsing: +/- 0.01, 10.00 +0.02/-0.01
- Fractional to decimal conversion: 1/4" -> 6.35mm
"""

import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union


class LengthUnit(Enum):
    """Length measurement units."""
    MILLIMETER = "mm"
    CENTIMETER = "cm"
    METER = "m"
    INCH = "in"
    FOOT = "ft"
    THOU = "thou"  # 1/1000 inch


class AngularUnit(Enum):
    """Angular measurement units."""
    DEGREE = "deg"
    RADIAN = "rad"
    GRADIAN = "grad"
    ARCMINUTE = "arcmin"
    ARCSECOND = "arcsec"


@dataclass
class Tolerance:
    """Dimensional tolerance specification."""
    plus: float
    minus: float

    @property
    def symmetric(self) -> bool:
        """Check if tolerance is symmetric."""
        return abs(self.plus - abs(self.minus)) < 0.0001

    @property
    def total_range(self) -> float:
        """Get total tolerance range."""
        return self.plus + abs(self.minus)

    def __str__(self) -> str:
        if self.symmetric:
            return f"±{self.plus}"
        return f"+{self.plus}/-{abs(self.minus)}"


@dataclass
class NormalizedDimension:
    """Normalized dimensional value."""
    value: float               # Nominal value
    unit: LengthUnit          # Target unit
    tolerance: Optional[Tolerance] = None
    original_value: Optional[float] = None
    original_unit: Optional[str] = None
    precision: int = 3         # Decimal places


# Conversion factors to millimeters
LENGTH_TO_MM: Dict[LengthUnit, float] = {
    LengthUnit.MILLIMETER: 1.0,
    LengthUnit.CENTIMETER: 10.0,
    LengthUnit.METER: 1000.0,
    LengthUnit.INCH: 25.4,
    LengthUnit.FOOT: 304.8,
    LengthUnit.THOU: 0.0254,
}

# Conversion factors for angular units (to degrees)
ANGULAR_TO_DEG: Dict[AngularUnit, float] = {
    AngularUnit.DEGREE: 1.0,
    AngularUnit.RADIAN: 57.29577951308232,  # 180/pi
    AngularUnit.GRADIAN: 0.9,
    AngularUnit.ARCMINUTE: 1/60,
    AngularUnit.ARCSECOND: 1/3600,
}

# Common fractional inches to decimal
FRACTIONAL_INCHES: Dict[str, float] = {
    "1/64": 0.015625, "1/32": 0.03125, "3/64": 0.046875, "1/16": 0.0625,
    "5/64": 0.078125, "3/32": 0.09375, "7/64": 0.109375, "1/8": 0.125,
    "9/64": 0.140625, "5/32": 0.15625, "11/64": 0.171875, "3/16": 0.1875,
    "13/64": 0.203125, "7/32": 0.21875, "15/64": 0.234375, "1/4": 0.25,
    "17/64": 0.265625, "9/32": 0.28125, "19/64": 0.296875, "5/16": 0.3125,
    "21/64": 0.328125, "11/32": 0.34375, "23/64": 0.359375, "3/8": 0.375,
    "25/64": 0.390625, "13/32": 0.40625, "27/64": 0.421875, "7/16": 0.4375,
    "29/64": 0.453125, "15/32": 0.46875, "31/64": 0.484375, "1/2": 0.5,
    "33/64": 0.515625, "17/32": 0.53125, "35/64": 0.546875, "9/16": 0.5625,
    "37/64": 0.578125, "19/32": 0.59375, "39/64": 0.609375, "5/8": 0.625,
    "41/64": 0.640625, "21/32": 0.65625, "43/64": 0.671875, "11/16": 0.6875,
    "45/64": 0.703125, "23/32": 0.71875, "47/64": 0.734375, "3/4": 0.75,
    "49/64": 0.765625, "25/32": 0.78125, "51/64": 0.796875, "13/16": 0.8125,
    "53/64": 0.828125, "27/32": 0.84375, "55/64": 0.859375, "7/8": 0.875,
    "57/64": 0.890625, "29/32": 0.90625, "59/64": 0.921875, "15/16": 0.9375,
    "61/64": 0.953125, "31/32": 0.96875, "63/64": 0.984375, "1": 1.0,
}


class DimensionNormalizer:
    """
    Dimension normalizer for converting between units.

    Handles:
    - Metric/Imperial conversions
    - Fractional inch to decimal
    - Tolerance parsing
    - Precision management
    """

    # Regex patterns
    PATTERNS = {
        # Decimal with unit: 25.4mm, 1.5 in, 10cm
        "decimal": re.compile(
            r'^(-?\d+(?:\.\d+)?)\s*(mm|cm|m|in|inch|inches|ft|foot|feet|thou)?$',
            re.IGNORECASE
        ),
        # Fractional inch: 1/4", 1/4 in, 3/8"
        "fractional": re.compile(
            r'^(\d+/\d+)\s*["\']?\s*(in|inch|inches)?$',
            re.IGNORECASE
        ),
        # Mixed fraction: 1-1/2", 2 3/4 in
        "mixed": re.compile(
            r'^(\d+)\s*[-\s]\s*(\d+/\d+)\s*["\']?\s*(in|inch|inches)?$',
            re.IGNORECASE
        ),
        # With tolerance: 10.00 +/- 0.01, 25.4 +0.02/-0.01
        "with_tolerance": re.compile(
            r'^(-?\d+(?:\.\d+)?)\s*(mm|cm|m|in)?\s*'
            r'(?:±|\+/-|\+-)\s*(\d+(?:\.\d+)?)\s*(mm|cm|m|in)?$',
            re.IGNORECASE
        ),
        # Asymmetric tolerance: 10.00 +0.02/-0.01
        "asym_tolerance": re.compile(
            r'^(-?\d+(?:\.\d+)?)\s*(mm|cm|m|in)?\s*'
            r'\+(\d+(?:\.\d+)?)\s*/\s*-(\d+(?:\.\d+)?)\s*(mm|cm|m|in)?$',
            re.IGNORECASE
        ),
    }

    # Unit string mappings
    UNIT_MAP: Dict[str, LengthUnit] = {
        "mm": LengthUnit.MILLIMETER,
        "millimeter": LengthUnit.MILLIMETER,
        "millimeters": LengthUnit.MILLIMETER,
        "cm": LengthUnit.CENTIMETER,
        "centimeter": LengthUnit.CENTIMETER,
        "centimeters": LengthUnit.CENTIMETER,
        "m": LengthUnit.METER,
        "meter": LengthUnit.METER,
        "meters": LengthUnit.METER,
        "in": LengthUnit.INCH,
        "inch": LengthUnit.INCH,
        "inches": LengthUnit.INCH,
        '"': LengthUnit.INCH,
        "ft": LengthUnit.FOOT,
        "foot": LengthUnit.FOOT,
        "feet": LengthUnit.FOOT,
        "'": LengthUnit.FOOT,
        "thou": LengthUnit.THOU,
        "mil": LengthUnit.THOU,
    }

    def __init__(
        self,
        default_unit: str = "mm",
        precision: int = 3,
    ):
        """
        Initialize the dimension normalizer.

        Args:
            default_unit: Default output unit
            precision: Decimal precision for output
        """
        self.default_unit = self.UNIT_MAP.get(default_unit.lower(), LengthUnit.MILLIMETER)
        self.precision = precision

    def to_millimeters(
        self,
        value: Union[str, float, int],
        source_unit: str = "mm",
    ) -> float:
        """
        Convert a dimension to millimeters.

        Args:
            value: Dimension value (number or string with unit)
            source_unit: Source unit if value is numeric

        Returns:
            Value in millimeters
        """
        if isinstance(value, str):
            parsed = self.parse(value)
            return parsed.value
        else:
            # Numeric value with specified unit
            unit = self.UNIT_MAP.get(source_unit.lower(), LengthUnit.MILLIMETER)
            mm_value = float(value) * LENGTH_TO_MM[unit]
            return round(mm_value, self.precision)

    def convert(
        self,
        value: Union[str, float],
        from_unit: str,
        to_unit: str,
    ) -> float:
        """
        Convert between units.

        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit

        Returns:
            Converted value
        """
        # Convert to mm first
        mm_value = self.to_millimeters(value, from_unit)

        # Convert from mm to target
        target_unit = self.UNIT_MAP.get(to_unit.lower(), LengthUnit.MILLIMETER)
        result = mm_value / LENGTH_TO_MM[target_unit]

        return round(result, self.precision)

    def parse(self, dimension_str: str) -> NormalizedDimension:
        """
        Parse a dimension string.

        Args:
            dimension_str: Input dimension string

        Returns:
            NormalizedDimension with parsed values
        """
        original = dimension_str.strip()
        s = original

        # Try asymmetric tolerance first
        match = self.PATTERNS["asym_tolerance"].match(s)
        if match:
            return self._parse_asym_tolerance(match, original)

        # Try symmetric tolerance
        match = self.PATTERNS["with_tolerance"].match(s)
        if match:
            return self._parse_symmetric_tolerance(match, original)

        # Try mixed fraction
        match = self.PATTERNS["mixed"].match(s)
        if match:
            return self._parse_mixed_fraction(match, original)

        # Try simple fraction
        match = self.PATTERNS["fractional"].match(s)
        if match:
            return self._parse_fraction(match, original)

        # Try decimal
        match = self.PATTERNS["decimal"].match(s)
        if match:
            return self._parse_decimal(match, original)

        # Could not parse - try to extract number
        num_match = re.search(r'(-?\d+(?:\.\d+)?)', s)
        if num_match:
            value = float(num_match.group(1))
            return NormalizedDimension(
                value=value,
                unit=self.default_unit,
                original_value=value,
                original_unit="unknown",
                precision=self.precision,
            )

        # Return zero if nothing parseable
        return NormalizedDimension(
            value=0.0,
            unit=self.default_unit,
            precision=self.precision,
        )

    def _parse_decimal(self, match: re.Match, original: str) -> NormalizedDimension:
        """Parse decimal value with optional unit."""
        value = float(match.group(1))
        unit_str = match.group(2)

        if unit_str:
            unit = self.UNIT_MAP.get(unit_str.lower(), LengthUnit.MILLIMETER)
        else:
            unit = self.default_unit

        # Convert to target unit (mm by default)
        mm_value = value * LENGTH_TO_MM[unit]
        target_value = mm_value / LENGTH_TO_MM[self.default_unit]

        return NormalizedDimension(
            value=round(target_value, self.precision),
            unit=self.default_unit,
            original_value=value,
            original_unit=unit_str or unit.value,
            precision=self.precision,
        )

    def _parse_fraction(self, match: re.Match, original: str) -> NormalizedDimension:
        """Parse fractional inch."""
        frac_str = match.group(1)

        # Look up or calculate
        if frac_str in FRACTIONAL_INCHES:
            value_inch = FRACTIONAL_INCHES[frac_str]
        else:
            num, denom = frac_str.split('/')
            value_inch = float(num) / float(denom)

        # Convert to mm
        mm_value = value_inch * 25.4
        target_value = mm_value / LENGTH_TO_MM[self.default_unit]

        return NormalizedDimension(
            value=round(target_value, self.precision),
            unit=self.default_unit,
            original_value=value_inch,
            original_unit="in",
            precision=self.precision,
        )

    def _parse_mixed_fraction(self, match: re.Match, original: str) -> NormalizedDimension:
        """Parse mixed fractional inch (e.g., 1-1/2")."""
        whole = int(match.group(1))
        frac_str = match.group(2)

        # Calculate fractional part
        if frac_str in FRACTIONAL_INCHES:
            frac_value = FRACTIONAL_INCHES[frac_str]
        else:
            num, denom = frac_str.split('/')
            frac_value = float(num) / float(denom)

        value_inch = whole + frac_value

        # Convert to mm
        mm_value = value_inch * 25.4
        target_value = mm_value / LENGTH_TO_MM[self.default_unit]

        return NormalizedDimension(
            value=round(target_value, self.precision),
            unit=self.default_unit,
            original_value=value_inch,
            original_unit="in",
            precision=self.precision,
        )

    def _parse_symmetric_tolerance(self, match: re.Match, original: str) -> NormalizedDimension:
        """Parse value with symmetric tolerance."""
        value = float(match.group(1))
        value_unit_str = match.group(2)
        tol_value = float(match.group(3))
        tol_unit_str = match.group(4)

        value_unit = self.UNIT_MAP.get((value_unit_str or "mm").lower(), LengthUnit.MILLIMETER)
        tol_unit = self.UNIT_MAP.get((tol_unit_str or value_unit_str or "mm").lower(), value_unit)

        # Convert to target unit
        mm_value = value * LENGTH_TO_MM[value_unit]
        target_value = mm_value / LENGTH_TO_MM[self.default_unit]

        mm_tol = tol_value * LENGTH_TO_MM[tol_unit]
        target_tol = mm_tol / LENGTH_TO_MM[self.default_unit]

        return NormalizedDimension(
            value=round(target_value, self.precision),
            unit=self.default_unit,
            tolerance=Tolerance(plus=target_tol, minus=-target_tol),
            original_value=value,
            original_unit=value_unit_str or value_unit.value,
            precision=self.precision,
        )

    def _parse_asym_tolerance(self, match: re.Match, original: str) -> NormalizedDimension:
        """Parse value with asymmetric tolerance."""
        value = float(match.group(1))
        value_unit_str = match.group(2)
        plus_tol = float(match.group(3))
        minus_tol = float(match.group(4))
        tol_unit_str = match.group(5)

        value_unit = self.UNIT_MAP.get((value_unit_str or "mm").lower(), LengthUnit.MILLIMETER)
        tol_unit = self.UNIT_MAP.get((tol_unit_str or value_unit_str or "mm").lower(), value_unit)

        # Convert to target unit
        mm_value = value * LENGTH_TO_MM[value_unit]
        target_value = mm_value / LENGTH_TO_MM[self.default_unit]

        mm_plus = plus_tol * LENGTH_TO_MM[tol_unit]
        mm_minus = minus_tol * LENGTH_TO_MM[tol_unit]
        target_plus = mm_plus / LENGTH_TO_MM[self.default_unit]
        target_minus = mm_minus / LENGTH_TO_MM[self.default_unit]

        return NormalizedDimension(
            value=round(target_value, self.precision),
            unit=self.default_unit,
            tolerance=Tolerance(plus=target_plus, minus=-target_minus),
            original_value=value,
            original_unit=value_unit_str or value_unit.value,
            precision=self.precision,
        )

    def format_dimension(
        self,
        value: float,
        unit: str = "mm",
        tolerance: Optional[Tolerance] = None,
    ) -> str:
        """
        Format a dimension for display.

        Args:
            value: Dimension value
            unit: Unit for display
            tolerance: Optional tolerance

        Returns:
            Formatted dimension string
        """
        formatted = f"{value:.{self.precision}f} {unit}"
        if tolerance:
            formatted += f" {tolerance}"
        return formatted

    def fractional_to_decimal(self, fraction: str) -> float:
        """
        Convert a fractional string to decimal.

        Args:
            fraction: Fractional string (e.g., "1/4", "1-1/2")

        Returns:
            Decimal value
        """
        if '-' in fraction:
            # Mixed fraction
            parts = fraction.split('-')
            whole = float(parts[0])
            num, denom = parts[1].split('/')
            return whole + float(num) / float(denom)
        elif '/' in fraction:
            num, denom = fraction.split('/')
            return float(num) / float(denom)
        else:
            return float(fraction)

    def decimal_to_fractional(
        self,
        value: float,
        denominator: int = 64,
    ) -> str:
        """
        Convert decimal to nearest fractional representation.

        Args:
            value: Decimal value
            denominator: Maximum denominator (default 64ths)

        Returns:
            Fractional string
        """
        # Find nearest fraction
        whole = int(value)
        frac = value - whole

        # Find closest fraction
        best_num = 0
        best_denom = 1
        best_diff = abs(frac)

        for denom in [2, 4, 8, 16, 32, 64]:
            if denom > denominator:
                break
            num = round(frac * denom)
            diff = abs(frac - num / denom)
            if diff < best_diff:
                best_diff = diff
                best_num = num
                best_denom = denom

        # Simplify fraction
        from math import gcd
        if best_num > 0:
            g = gcd(best_num, best_denom)
            best_num //= g
            best_denom //= g

        # Format result
        if whole > 0 and best_num > 0:
            return f"{whole}-{best_num}/{best_denom}"
        elif whole > 0:
            return str(whole)
        elif best_num > 0:
            return f"{best_num}/{best_denom}"
        else:
            return "0"


__all__ = [
    "DimensionNormalizer",
    "NormalizedDimension",
    "Tolerance",
    "LengthUnit",
    "AngularUnit",
]
