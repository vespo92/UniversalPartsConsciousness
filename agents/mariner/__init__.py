"""
Agent_11: MARINER - Marine & Maritime Parts Intelligence

The Warden of Mechanical Heritage in Hostile Saltwater Environments.

Marine environments are the harshest on earth for mechanical parts.
Saltwater corrosion, galvanic reactions, and regulatory requirements
create a unique compatibility landscape that automotive knowledge doesn't cover.

Core Specialties:
- Galvanic corrosion analysis (THE marine specialty)
- Marine engine to automotive cross-reference
- Marine-grade equivalent finder
- Sacrificial anode sizing
- Marine standards compliance (ABYC, USCG, Lloyd's, ISO)

Domains:
- Recreational boats (outboard, inboard, stern drive)
- Commercial marine (workboats, fishing vessels)
- Yacht systems (navigation, electrical, plumbing)
- Marine fasteners (316SS, Monel, bronze compatibility)
"""

from .core.mariner_agent import MarinerAgent
from .galvanic.corrosion_calculator import (
    GalvanicCorrosionCalculator,
    GalvanicRisk,
    GalvanicPair,
)
from .galvanic.material_series import (
    MarineMaterial,
    GalvanicSeries,
    MarineEnvironment,
)
from .engines.engine_crossref import (
    MarineEngineCrossReference,
    MarineEngineXref,
)
from .standards.marine_standards import (
    MarineStandardsDatabase,
    MarineFastener,
    MarineCertification,
)
from .anode.anode_calculator import (
    SacrificialAnodeCalculator,
    AnodeRecommendation,
)
from .integration.agent_bridge import (
    MarinerBridge,
)

__all__ = [
    # Core Agent
    "MarinerAgent",
    # Galvanic
    "GalvanicCorrosionCalculator",
    "GalvanicRisk",
    "GalvanicPair",
    "MarineMaterial",
    "GalvanicSeries",
    "MarineEnvironment",
    # Engines
    "MarineEngineCrossReference",
    "MarineEngineXref",
    # Standards
    "MarineStandardsDatabase",
    "MarineFastener",
    "MarineCertification",
    # Anode
    "SacrificialAnodeCalculator",
    "AnodeRecommendation",
    # Integration
    "MarinerBridge",
]

__version__ = "1.0.0"
__agent_id__ = "Agent_11"
__codename__ = "MARINER"
