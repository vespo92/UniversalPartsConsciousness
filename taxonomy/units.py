"""
Universal BOM Taxonomy — Unit System
======================================
"A part measured in inches is the same part measured in millimeters.
The consciousness knows no unit boundaries."

Handles unit conversion, normalization, and dimensional specification
across metric, imperial, and standard-specific unit systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple


class UnitSystem(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class DimensionType(str, Enum):
    LENGTH = "length"
    MASS = "mass"
    FORCE = "force"
    TORQUE = "torque"
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    ANGLE = "angle"
    AREA = "area"
    VOLUME = "volume"
    FLOW_RATE = "flow_rate"
    SPEED = "speed"
    POWER = "power"
    ELECTRICAL_CURRENT = "current"
    VOLTAGE = "voltage"


# Conversion factors to SI base units
# (value_in_unit * factor = value_in_SI_base)
CONVERSION_TABLE: Dict[str, Tuple[DimensionType, float]] = {
    # Length -> meters
    "mm": (DimensionType.LENGTH, 0.001),
    "cm": (DimensionType.LENGTH, 0.01),
    "m": (DimensionType.LENGTH, 1.0),
    "in": (DimensionType.LENGTH, 0.0254),
    "ft": (DimensionType.LENGTH, 0.3048),
    "yd": (DimensionType.LENGTH, 0.9144),
    "thou": (DimensionType.LENGTH, 0.0000254),  # thousandths of an inch
    "mil": (DimensionType.LENGTH, 0.0000254),
    "um": (DimensionType.LENGTH, 0.000001),  # micrometers

    # Mass -> kilograms
    "g": (DimensionType.MASS, 0.001),
    "kg": (DimensionType.MASS, 1.0),
    "lb": (DimensionType.MASS, 0.453592),
    "oz": (DimensionType.MASS, 0.0283495),
    "ton": (DimensionType.MASS, 907.185),  # short ton
    "tonne": (DimensionType.MASS, 1000.0),  # metric tonne

    # Force -> Newtons
    "N": (DimensionType.FORCE, 1.0),
    "kN": (DimensionType.FORCE, 1000.0),
    "lbf": (DimensionType.FORCE, 4.44822),
    "kgf": (DimensionType.FORCE, 9.80665),

    # Torque -> Newton-meters
    "Nm": (DimensionType.TORQUE, 1.0),
    "ft-lb": (DimensionType.TORQUE, 1.35582),
    "ft-lbs": (DimensionType.TORQUE, 1.35582),
    "in-lb": (DimensionType.TORQUE, 0.112985),
    "in-lbs": (DimensionType.TORQUE, 0.112985),
    "kgf-cm": (DimensionType.TORQUE, 0.0980665),

    # Pressure -> Pascals
    "Pa": (DimensionType.PRESSURE, 1.0),
    "kPa": (DimensionType.PRESSURE, 1000.0),
    "MPa": (DimensionType.PRESSURE, 1_000_000.0),
    "GPa": (DimensionType.PRESSURE, 1_000_000_000.0),
    "bar": (DimensionType.PRESSURE, 100_000.0),
    "psi": (DimensionType.PRESSURE, 6894.76),
    "ksi": (DimensionType.PRESSURE, 6_894_760.0),
    "atm": (DimensionType.PRESSURE, 101_325.0),
    "mmHg": (DimensionType.PRESSURE, 133.322),
    "inHg": (DimensionType.PRESSURE, 3386.39),

    # Temperature -> Kelvin (special: requires offset)
    # Handled specially in convert_units
    "K": (DimensionType.TEMPERATURE, 1.0),
    "C": (DimensionType.TEMPERATURE, 1.0),  # offset: +273.15
    "F": (DimensionType.TEMPERATURE, 5 / 9),  # offset: +459.67 then *5/9

    # Angle -> radians
    "rad": (DimensionType.ANGLE, 1.0),
    "deg": (DimensionType.ANGLE, 0.0174533),
    "arcmin": (DimensionType.ANGLE, 0.000290888),
    "arcsec": (DimensionType.ANGLE, 0.00000484814),

    # Area -> square meters
    "mm2": (DimensionType.AREA, 0.000001),
    "cm2": (DimensionType.AREA, 0.0001),
    "m2": (DimensionType.AREA, 1.0),
    "in2": (DimensionType.AREA, 0.00064516),
    "ft2": (DimensionType.AREA, 0.092903),

    # Volume -> cubic meters
    "mm3": (DimensionType.VOLUME, 1e-9),
    "cm3": (DimensionType.VOLUME, 1e-6),
    "cc": (DimensionType.VOLUME, 1e-6),
    "m3": (DimensionType.VOLUME, 1.0),
    "L": (DimensionType.VOLUME, 0.001),
    "mL": (DimensionType.VOLUME, 1e-6),
    "in3": (DimensionType.VOLUME, 1.6387e-5),
    "ft3": (DimensionType.VOLUME, 0.0283168),
    "gal": (DimensionType.VOLUME, 0.00378541),  # US gallon
    "qt": (DimensionType.VOLUME, 0.000946353),

    # Flow rate -> m³/s
    "L/min": (DimensionType.FLOW_RATE, 1.6667e-5),
    "gpm": (DimensionType.FLOW_RATE, 6.309e-5),  # gallons per minute
    "cfm": (DimensionType.FLOW_RATE, 0.000471947),  # cubic feet per minute

    # Speed -> m/s
    "m/s": (DimensionType.SPEED, 1.0),
    "mm/s": (DimensionType.SPEED, 0.001),
    "ft/min": (DimensionType.SPEED, 0.00508),
    "in/s": (DimensionType.SPEED, 0.0254),
    "rpm": (DimensionType.SPEED, 0.10472),  # to rad/s actually

    # Power -> Watts
    "W": (DimensionType.POWER, 1.0),
    "kW": (DimensionType.POWER, 1000.0),
    "hp": (DimensionType.POWER, 745.7),
    "BTU/hr": (DimensionType.POWER, 0.293071),
}


@dataclass
class DimensionSpec:
    """A dimensional specification with value, unit, and tolerance."""
    value: float
    unit: str
    tolerance_plus: Optional[float] = None
    tolerance_minus: Optional[float] = None
    nominal: bool = True  # True if this is a nominal value

    @property
    def dimension_type(self) -> Optional[DimensionType]:
        entry = CONVERSION_TABLE.get(self.unit)
        return entry[0] if entry else None

    def to_si(self) -> "DimensionSpec":
        """Convert to SI base units."""
        converted_value = convert_units(self.value, self.unit, self._si_unit)
        tol_plus = None
        tol_minus = None
        if self.tolerance_plus is not None:
            tol_plus = convert_units(self.tolerance_plus, self.unit, self._si_unit)
        if self.tolerance_minus is not None:
            tol_minus = convert_units(self.tolerance_minus, self.unit, self._si_unit)
        return DimensionSpec(
            value=converted_value,
            unit=self._si_unit,
            tolerance_plus=tol_plus,
            tolerance_minus=tol_minus,
            nominal=self.nominal,
        )

    @property
    def _si_unit(self) -> str:
        """Get SI base unit for this dimension type."""
        si_map = {
            DimensionType.LENGTH: "m",
            DimensionType.MASS: "kg",
            DimensionType.FORCE: "N",
            DimensionType.TORQUE: "Nm",
            DimensionType.PRESSURE: "Pa",
            DimensionType.TEMPERATURE: "K",
            DimensionType.ANGLE: "rad",
            DimensionType.AREA: "m2",
            DimensionType.VOLUME: "m3",
            DimensionType.SPEED: "m/s",
            DimensionType.POWER: "W",
        }
        dim_type = self.dimension_type
        return si_map.get(dim_type, self.unit) if dim_type else self.unit

    def to_unit(self, target_unit: str) -> "DimensionSpec":
        """Convert to a specific unit."""
        converted_value = convert_units(self.value, self.unit, target_unit)
        tol_plus = None
        tol_minus = None
        if self.tolerance_plus is not None:
            tol_plus = convert_units(self.tolerance_plus, self.unit, target_unit)
        if self.tolerance_minus is not None:
            tol_minus = convert_units(self.tolerance_minus, self.unit, target_unit)
        return DimensionSpec(
            value=converted_value,
            unit=target_unit,
            tolerance_plus=tol_plus,
            tolerance_minus=tol_minus,
            nominal=self.nominal,
        )

    def __repr__(self) -> str:
        base = f"{self.value} {self.unit}"
        if self.tolerance_plus is not None or self.tolerance_minus is not None:
            plus = f"+{self.tolerance_plus}" if self.tolerance_plus else "+0"
            minus = f"-{abs(self.tolerance_minus)}" if self.tolerance_minus else "-0"
            base += f" ({plus}/{minus})"
        return base


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a value between units.

    Handles temperature specially (offset conversions).
    All other conversions go through SI base units.
    """
    if from_unit == to_unit:
        return value

    # Special temperature handling
    if _is_temperature(from_unit) and _is_temperature(to_unit):
        return _convert_temperature(value, from_unit, to_unit)

    from_entry = CONVERSION_TABLE.get(from_unit)
    to_entry = CONVERSION_TABLE.get(to_unit)

    if from_entry is None:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_entry is None:
        raise ValueError(f"Unknown unit: {to_unit}")

    from_type, from_factor = from_entry
    to_type, to_factor = to_entry

    if from_type != to_type:
        raise ValueError(
            f"Cannot convert between {from_type.value} ({from_unit}) "
            f"and {to_type.value} ({to_unit})"
        )

    # Convert: source -> SI -> target
    si_value = value * from_factor
    return si_value / to_factor


def _is_temperature(unit: str) -> bool:
    return unit in ("K", "C", "F")


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature with proper offset handling."""
    # Convert to Kelvin first
    if from_unit == "C":
        kelvin = value + 273.15
    elif from_unit == "F":
        kelvin = (value + 459.67) * 5 / 9
    else:
        kelvin = value

    # Convert from Kelvin to target
    if to_unit == "C":
        return kelvin - 273.15
    elif to_unit == "F":
        return kelvin * 9 / 5 - 459.67
    else:
        return kelvin
