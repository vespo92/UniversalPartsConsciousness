"""
ICARUS Fluids Module
====================

Aviation fluid compatibility intelligence.

CRITICAL: Aviation hydraulic fluids are NOT interchangeable.
Mixing incompatible fluids causes seal destruction and system failure.

Fluid Families:
- MIL-PRF-5606 (Red mineral oil) - GA piston aircraft
- MIL-PRF-83282 (Synthetic hydrocarbon) - Military aircraft
- Skydrol (Purple phosphate ester) - Commercial jets

NEVER MIX THESE. The consequences are catastrophic.
"""

from agents.icarus.fluids.hydraulic_matrix import (
    HydraulicFluidMatrix,
    FluidCompatibility,
    FluidFamily,
    CompatibilityCheckResult,
)

__all__ = [
    "HydraulicFluidMatrix",
    "FluidCompatibility",
    "FluidFamily",
    "CompatibilityCheckResult",
]
