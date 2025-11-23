"""
ICARUS Avionics Module
======================

Avionics cross-reference and compatibility intelligence.

Navigates 50+ years of avionics equipment:
- Legacy units (King, Narco, Collins)
- Modern systems (Garmin, Avidyne, Aspen)
- Installation requirements (STCs, wiring)
- Interface protocols (ARINC 429, RS-232)
"""

from agents.icarus.avionics.crossref_database import (
    AvionicsCrossReference,
    AvionicsUnit,
    InstallationRequirement,
    InterfaceProtocol,
)

__all__ = [
    "AvionicsCrossReference",
    "AvionicsUnit",
    "InstallationRequirement",
    "InterfaceProtocol",
]
