"""
Agent_11 MARINER - Marine Standards Module

Marine equipment must meet specific standards for safety and certification.

Standards Bodies Covered:
- ABYC (American Boat and Yacht Council)
- USCG (US Coast Guard) 33 CFR 183
- ISO (International Organization for Standardization)
- Lloyd's Register
- NMMA (National Marine Manufacturers Association)
- CE Mark (European Conformity)

Key Standards:
- SAE J1171 (Ignition Protection)
- ISO 8846 (Electrical Ignition Protection)
- ABYC H-27 (Fuel Systems)
- ABYC E-11 (AC and DC Electrical Systems)
"""

from .marine_standards import (
    MarineStandardsDatabase,
    MarineFastener,
    MarineCertification,
    MarineStandard,
)

__all__ = [
    "MarineStandardsDatabase",
    "MarineFastener",
    "MarineCertification",
    "MarineStandard",
]
