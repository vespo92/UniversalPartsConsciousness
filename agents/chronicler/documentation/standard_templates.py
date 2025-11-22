"""
Standard documentation templates for the Chronicler agent.

Defines the required structure and format for all engine
and parts documentation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Core Documentation Files (5 standard JSON files per engine)
REQUIRED_FILES = {
    "master": "{engine}-master.json",
    "catalog": "{engine}-parts-catalog.json",
    "interchange": "{engine}-interchangeability.json",
    "tools": "{engine}-tools-procedures.json",
    "aftermarket": "{engine}-aftermarket.json"
}

# Extended Documentation Files
OPTIONAL_FILES = {
    "history": "{engine}-history.md",
    "racing": "{engine}-racing-heritage.md",
    "culture": "{engine}-community-culture.md",
    "rebuild": "{engine}-rebuild-guide.md",
    "tuning": "{engine}-tuning-guide.md",
    "stories": "{engine}-stories.md"
}


@dataclass
class EngineVariant:
    """Specification for an engine variant."""
    code: str
    displacement_cc: int
    bore_mm: float
    stroke_mm: float
    compression_ratio: float
    power_hp: int
    power_rpm: int
    torque_nm: int
    torque_rpm: int
    redline_rpm: int
    production_years: str
    notes: str = ""


@dataclass
class EngineSpecifications:
    """Technical specifications for an engine family."""
    displacement_cc: int
    configuration: str  # "I4", "V6", "V8", "H4", "R2", etc.
    aspiration: str     # "NA", "Turbo", "Supercharged", "Twin-Turbo"
    compression_ratio: float
    power_hp_range: tuple  # (min, max)
    torque_nm_range: tuple # (min, max)
    redline_rpm: int
    bore_mm: float
    stroke_mm: float
    block_material: str   # "Cast Iron", "Aluminum"
    head_material: str    # "Aluminum", "Cast Iron"
    valvetrain: str       # "SOHC", "DOHC", "OHV"
    valves_per_cylinder: int
    fuel_system: str      # "Carbureted", "EFI", "Direct Injection"
    vvt_system: Optional[str] = None  # "VTEC", "VVT-i", "VANOS", etc.


@dataclass
class RacingAchievement:
    """Record of a racing achievement."""
    event: str
    year: int
    position: int
    category: str
    notes: str = ""


@dataclass
class EngineHistory:
    """Historical context for an engine family."""
    development_story: str
    engineering_team: List[str]
    design_philosophy: str
    notable_innovations: List[str]
    racing_achievements: List[RacingAchievement]
    cultural_impact: str
    production_start_year: int
    production_end_year: Optional[int] = None


@dataclass
class EngineLegacy:
    """Legacy and influence of an engine family."""
    influence_on: List[str]
    spiritual_successors: List[str]
    community_status: str  # "mythical", "legendary", "iconic", "respected", "recognized", "documented"


@dataclass
class EngineDocumentationTemplate:
    """
    Master template for comprehensive engine documentation.

    This template defines the complete structure for documenting
    an engine family within the Universal Parts Consciousness.
    """
    # Identification
    engine_family: str
    manufacturer: str
    engine_code: str

    # Variants
    variants: List[EngineVariant] = field(default_factory=list)

    # Timeline
    production_years: str = ""
    vehicles_used: List[str] = field(default_factory=list)

    # Technical
    specifications: Optional[EngineSpecifications] = None

    # History
    history: Optional[EngineHistory] = None

    # Legacy
    legacy: Optional[EngineLegacy] = None

    # Metadata
    documentation_version: str = "1.0"
    last_updated: str = ""
    documented_by: str = "Agent_7:CHRONICLER"

    def to_master_json(self) -> Dict[str, Any]:
        """Convert to master JSON format."""
        result = {
            "engine_family": self.engine_family,
            "manufacturer": self.manufacturer,
            "engine_code": self.engine_code,
            "production_years": self.production_years,
            "vehicles_used": self.vehicles_used,
            "documentation": {
                "version": self.documentation_version,
                "last_updated": self.last_updated,
                "documented_by": self.documented_by
            }
        }

        if self.variants:
            result["variants"] = [
                {
                    "code": v.code,
                    "displacement_cc": v.displacement_cc,
                    "bore_mm": v.bore_mm,
                    "stroke_mm": v.stroke_mm,
                    "compression_ratio": v.compression_ratio,
                    "power": {"hp": v.power_hp, "at_rpm": v.power_rpm},
                    "torque": {"nm": v.torque_nm, "at_rpm": v.torque_rpm},
                    "redline_rpm": v.redline_rpm,
                    "production_years": v.production_years,
                    "notes": v.notes
                }
                for v in self.variants
            ]

        if self.specifications:
            spec = self.specifications
            result["specifications"] = {
                "displacement_cc": spec.displacement_cc,
                "configuration": spec.configuration,
                "aspiration": spec.aspiration,
                "compression_ratio": spec.compression_ratio,
                "power_hp": {"min": spec.power_hp_range[0], "max": spec.power_hp_range[1]},
                "torque_nm": {"min": spec.torque_nm_range[0], "max": spec.torque_nm_range[1]},
                "redline_rpm": spec.redline_rpm,
                "bore_mm": spec.bore_mm,
                "stroke_mm": spec.stroke_mm,
                "block_material": spec.block_material,
                "head_material": spec.head_material,
                "valvetrain": spec.valvetrain,
                "valves_per_cylinder": spec.valves_per_cylinder,
                "fuel_system": spec.fuel_system,
                "vvt_system": spec.vvt_system
            }

        if self.history:
            hist = self.history
            result["history"] = {
                "development_story": hist.development_story,
                "engineering_team": hist.engineering_team,
                "design_philosophy": hist.design_philosophy,
                "notable_innovations": hist.notable_innovations,
                "racing_achievements": [
                    {
                        "event": a.event,
                        "year": a.year,
                        "position": a.position,
                        "category": a.category,
                        "notes": a.notes
                    }
                    for a in hist.racing_achievements
                ],
                "cultural_impact": hist.cultural_impact,
                "production_start_year": hist.production_start_year,
                "production_end_year": hist.production_end_year
            }

        if self.legacy:
            result["legacy"] = {
                "influence_on": self.legacy.influence_on,
                "spiritual_successors": self.legacy.spiritual_successors,
                "community_status": self.legacy.community_status
            }

        return result


# Pre-defined templates for common documentation patterns
MASTER_JSON_SCHEMA = {
    "type": "object",
    "required": ["engine_family", "manufacturer", "engine_code"],
    "properties": {
        "engine_family": {"type": "string"},
        "manufacturer": {"type": "string"},
        "engine_code": {"type": "string"},
        "production_years": {"type": "string"},
        "vehicles_used": {"type": "array", "items": {"type": "string"}},
        "variants": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "displacement_cc": {"type": "integer"},
                    "power": {"type": "object"},
                    "torque": {"type": "object"}
                }
            }
        },
        "specifications": {"type": "object"},
        "history": {"type": "object"},
        "legacy": {"type": "object"}
    }
}

PARTS_CATALOG_SCHEMA = {
    "type": "object",
    "required": ["engine_code", "parts"],
    "properties": {
        "engine_code": {"type": "string"},
        "parts": {
            "type": "object",
            "properties": {
                "block": {"type": "array"},
                "head": {"type": "array"},
                "valvetrain": {"type": "array"},
                "internals": {"type": "array"},
                "fuel_system": {"type": "array"},
                "cooling": {"type": "array"},
                "oiling": {"type": "array"},
                "ignition": {"type": "array"},
                "intake": {"type": "array"},
                "exhaust": {"type": "array"}
            }
        }
    }
}

INTERCHANGEABILITY_SCHEMA = {
    "type": "object",
    "required": ["engine_code", "compatibility_matrix"],
    "properties": {
        "engine_code": {"type": "string"},
        "compatibility_matrix": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "part_category": {"type": "string"},
                    "compatible_engines": {"type": "array"},
                    "notes": {"type": "string"}
                }
            }
        }
    }
}
