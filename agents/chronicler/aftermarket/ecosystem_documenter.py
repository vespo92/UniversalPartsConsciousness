"""
Aftermarket Ecosystem Documenter - Maps the aftermarket landscape.

Documents vendor ecosystems, build levels, popular modifications,
and community resources for each engine.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Vendor:
    """Aftermarket vendor information."""
    name: str
    category: str  # "performance", "oem", "budget", "specialty", "machine_shop"
    website: str = ""
    specialties: List[str] = field(default_factory=list)
    reputation_score: float = 0.0  # 0-10
    notes: str = ""


@dataclass
class BuildLevel:
    """Build level specification."""
    name: str  # "stage_1", "stage_2", "stage_3", "race"
    description: str
    typical_power_gain_percent: tuple  # (min, max)
    typical_cost_usd: tuple  # (min, max)
    recommended_parts: List[str]
    requirements: List[str]
    notes: str = ""


@dataclass
class PowerPotential:
    """Power potential for an engine."""
    stock_hp: int
    stock_internals_max_hp: int
    built_motor_max_hp: int
    world_record_hp: int
    notes: str = ""


# Known aftermarket ecosystems for legendary engines
AFTERMARKET_ECOSYSTEMS = {
    "2JZ-GTE": {
        "power_potential": PowerPotential(
            stock_hp=320,
            stock_internals_max_hp=700,
            built_motor_max_hp=2000,
            world_record_hp=2500,
            notes="Stock bottom end is legendary for strength"
        ),
        "vendors": {
            "performance": ["Precision Turbo", "Garrett", "Brian Crower", "CP Pistons", "Titan Motorsports"],
            "specialty": ["Supra Store", "TunerMart", "Boost Logic", "Real Street Performance"],
            "tuning": ["Haltech", "AEM", "Link ECU", "Motec"]
        },
        "build_levels": {
            "stage_1": BuildLevel(
                name="Stage 1",
                description="Bolt-ons and tune",
                typical_power_gain_percent=(20, 40),
                typical_cost_usd=(2000, 5000),
                recommended_parts=["Intake", "Exhaust", "Boost controller", "ECU tune"],
                requirements=["Stock internals sufficient"]
            ),
            "stage_2": BuildLevel(
                name="Stage 2",
                description="Single turbo conversion",
                typical_power_gain_percent=(80, 120),
                typical_cost_usd=(8000, 15000),
                recommended_parts=["Single turbo kit", "Larger injectors", "Fuel pump", "Intercooler"],
                requirements=["Upgraded fuel system", "ECU management"]
            ),
            "stage_3": BuildLevel(
                name="Stage 3",
                description="Built internals, big power",
                typical_power_gain_percent=(150, 300),
                typical_cost_usd=(20000, 40000),
                recommended_parts=["Forged internals", "Head studs", "Large turbo", "Built transmission"],
                requirements=["Complete engine build", "Strengthened drivetrain"]
            )
        },
        "community_resources": {
            "forums": ["Supraforums.com", "SupraMkIV.com"],
            "youtube": ["Papadakis Racing", "Cleetus McFarland", "That Racing Channel"],
            "notable_builders": ["Titan Motorsports", "Boost Logic", "Real Street"]
        }
    },
    "LS1": {
        "power_potential": PowerPotential(
            stock_hp=350,
            stock_internals_max_hp=550,
            built_motor_max_hp=2500,
            world_record_hp=3000,
            notes="Endless aftermarket support, swap king"
        ),
        "vendors": {
            "performance": ["Texas Speed", "Holley", "COMP Cams", "BTR"],
            "specialty": ["Tick Performance", "Brian Tooley Racing", "Late Model Engines"],
            "tuning": ["HP Tuners", "EFI Live", "Holley Terminator"]
        },
        "build_levels": {
            "stage_1": BuildLevel(
                name="Stage 1",
                description="Cam and bolt-ons",
                typical_power_gain_percent=(15, 30),
                typical_cost_usd=(1500, 3500),
                recommended_parts=["Camshaft", "Intake", "Headers", "Tune"],
                requirements=["Stock internals fine"]
            ),
            "stage_2": BuildLevel(
                name="Stage 2",
                description="Heads and forced induction",
                typical_power_gain_percent=(50, 100),
                typical_cost_usd=(6000, 12000),
                recommended_parts=["Ported heads", "Supercharger or turbo kit", "Supporting mods"],
                requirements=["Upgraded fuel system"]
            ),
            "stage_3": BuildLevel(
                name="Stage 3",
                description="Built bottom end, big boost",
                typical_power_gain_percent=(150, 300),
                typical_cost_usd=(15000, 35000),
                recommended_parts=["Forged rotating assembly", "Billet oil pump", "Large turbo"],
                requirements=["Full engine build"]
            )
        },
        "community_resources": {
            "forums": ["LS1Tech.com", "LS1.com", "ModernCamaro.com"],
            "youtube": ["Holley", "Cleetus McFarland", "Fasterproms"],
            "notable_builders": ["Tick Performance", "Texas Speed", "Late Model Engines"]
        }
    },
    "K20A": {
        "power_potential": PowerPotential(
            stock_hp=220,
            stock_internals_max_hp=350,
            built_motor_max_hp=1000,
            world_record_hp=1200,
            notes="NA legend, turbo capable"
        ),
        "vendors": {
            "performance": ["Skunk2", "Toda Racing", "Spoon Sports", "Inline Pro"],
            "specialty": ["4Piston Racing", "Golden Eagle", "Ktuned"],
            "tuning": ["KPro", "Hondata", "AEM"]
        },
        "build_levels": {
            "stage_1": BuildLevel(
                name="Stage 1",
                description="NA bolt-ons",
                typical_power_gain_percent=(10, 20),
                typical_cost_usd=(2000, 4000),
                recommended_parts=["Intake", "Header", "Exhaust", "Tune"],
                requirements=["Stock internals OK"]
            ),
            "stage_2": BuildLevel(
                name="Stage 2",
                description="Cams, valvetrain, ITBs",
                typical_power_gain_percent=(30, 50),
                typical_cost_usd=(6000, 12000),
                recommended_parts=["Cams", "Valve springs", "ITBs or ported intake"],
                requirements=["Valve spring upgrade recommended"]
            ),
            "stage_3": BuildLevel(
                name="Stage 3",
                description="Turbo K-series",
                typical_power_gain_percent=(100, 200),
                typical_cost_usd=(12000, 25000),
                recommended_parts=["Turbo kit", "Forged internals", "Built transmission"],
                requirements=["Full engine build for high boost"]
            )
        },
        "community_resources": {
            "forums": ["K20a.org", "Honda-Tech.com"],
            "youtube": ["Honda Pro Jason", "Speed Academy"],
            "notable_builders": ["4Piston Racing", "Inline Pro", "Drag Cartel"]
        }
    }
}


class AftermarketEcosystemDocumenter:
    """
    Documents the aftermarket ecosystem for engines.

    Maps vendors, build levels, power potential, and community
    resources for each engine family.
    """

    def __init__(self):
        """Initialize the ecosystem documenter."""
        self._ecosystem_cache: Dict[str, Dict[str, Any]] = {}

    def document_ecosystem(
        self,
        engine_code: str,
        ecosystem_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Document the complete aftermarket ecosystem for an engine.

        Args:
            engine_code: Engine code to document
            ecosystem_data: Optional ecosystem data

        Returns:
            Complete ecosystem documentation
        """
        # Check for known ecosystem
        if engine_code in AFTERMARKET_ECOSYSTEMS:
            known = AFTERMARKET_ECOSYSTEMS[engine_code]
            return self._build_ecosystem_doc(engine_code, known)

        # Use provided data or return minimal doc
        if ecosystem_data:
            return self._build_ecosystem_doc(engine_code, ecosystem_data)

        return {
            "engine_code": engine_code,
            "status": "ecosystem_data_needed",
            "message": f"No aftermarket ecosystem data for {engine_code}. "
                       f"Contribute knowledge to map this ecosystem.",
            "template": self._get_ecosystem_template()
        }

    def _build_ecosystem_doc(
        self,
        engine_code: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build complete ecosystem documentation."""
        power = data.get("power_potential")
        if isinstance(power, PowerPotential):
            power_doc = {
                "stock_hp": power.stock_hp,
                "stock_internals_max_hp": power.stock_internals_max_hp,
                "built_motor_max_hp": power.built_motor_max_hp,
                "world_record_hp": power.world_record_hp,
                "notes": power.notes
            }
        else:
            power_doc = power or {}

        vendors = data.get("vendors", {})
        builds = data.get("build_levels", {})
        community = data.get("community_resources", {})

        # Convert build levels if they're BuildLevel objects
        build_doc = {}
        for level_name, level_data in builds.items():
            if isinstance(level_data, BuildLevel):
                build_doc[level_name] = {
                    "name": level_data.name,
                    "description": level_data.description,
                    "power_gain_percent": {
                        "min": level_data.typical_power_gain_percent[0],
                        "max": level_data.typical_power_gain_percent[1]
                    },
                    "cost_usd": {
                        "min": level_data.typical_cost_usd[0],
                        "max": level_data.typical_cost_usd[1]
                    },
                    "recommended_parts": level_data.recommended_parts,
                    "requirements": level_data.requirements
                }
            else:
                build_doc[level_name] = level_data

        return {
            "engine_code": engine_code,
            "ecosystem_maturity": self._assess_maturity(vendors, builds),
            "power_potential": power_doc,
            "vendors": vendors,
            "build_levels": build_doc,
            "community_resources": community,
            "ecosystem_summary": self._generate_summary(engine_code, power_doc)
        }

    def _assess_maturity(
        self,
        vendors: Dict[str, Any],
        builds: Dict[str, Any]
    ) -> str:
        """Assess the maturity of the aftermarket ecosystem."""
        vendor_count = sum(len(v) if isinstance(v, list) else 0 for v in vendors.values())
        build_count = len(builds)

        if vendor_count >= 10 and build_count >= 3:
            return "mature"
        elif vendor_count >= 5 and build_count >= 2:
            return "established"
        elif vendor_count >= 2:
            return "developing"
        else:
            return "emerging"

    def _generate_summary(
        self,
        engine_code: str,
        power_potential: Dict[str, Any]
    ) -> str:
        """Generate ecosystem summary narrative."""
        if not power_potential:
            return f"Aftermarket ecosystem for {engine_code} is not yet fully documented."

        stock = power_potential.get("stock_hp", 0)
        max_power = power_potential.get("built_motor_max_hp", 0)

        if max_power > stock * 5:
            return (
                f"The {engine_code} has extraordinary aftermarket potential, with "
                f"built motors achieving {max_power}HP - over {max_power/stock:.0f}x "
                f"stock power. A mature ecosystem with extensive vendor support."
            )
        elif max_power > stock * 2:
            return (
                f"The {engine_code} enjoys strong aftermarket support with "
                f"built motors reaching {max_power}HP. Well-developed ecosystem "
                f"with proven build paths."
            )
        else:
            return (
                f"The {engine_code} has growing aftermarket support with "
                f"reasonable modification potential. Developing ecosystem."
            )

    def _get_ecosystem_template(self) -> Dict[str, Any]:
        """Get template for ecosystem documentation."""
        return {
            "power_potential": {
                "stock_hp": 0,
                "stock_internals_max_hp": 0,
                "built_motor_max_hp": 0,
                "world_record_hp": 0,
                "notes": ""
            },
            "vendors": {
                "performance": [],
                "oem_replacement": [],
                "specialty": [],
                "tuning": []
            },
            "build_levels": {
                "stage_1": {
                    "description": "",
                    "typical_power_gain_percent": [0, 0],
                    "typical_cost_usd": [0, 0],
                    "recommended_parts": [],
                    "requirements": []
                }
            },
            "community_resources": {
                "forums": [],
                "youtube": [],
                "notable_builders": []
            }
        }

    def get_build_recommendation(
        self,
        engine_code: str,
        target_hp: int,
        budget_usd: int
    ) -> Dict[str, Any]:
        """
        Get build recommendation based on target and budget.

        Args:
            engine_code: Engine code
            target_hp: Target horsepower
            budget_usd: Available budget in USD

        Returns:
            Build recommendation
        """
        if engine_code not in AFTERMARKET_ECOSYSTEMS:
            return {
                "engine_code": engine_code,
                "status": "no_data",
                "message": "Build data not available for this engine."
            }

        ecosystem = AFTERMARKET_ECOSYSTEMS[engine_code]
        power = ecosystem.get("power_potential")
        builds = ecosystem.get("build_levels", {})

        if isinstance(power, PowerPotential):
            stock_hp = power.stock_hp
        else:
            stock_hp = power.get("stock_hp", 0) if power else 0

        # Determine required build level
        power_increase_needed = target_hp - stock_hp
        power_increase_percent = (power_increase_needed / stock_hp * 100) if stock_hp > 0 else 0

        recommended_level = None
        for level_name, level_data in builds.items():
            if isinstance(level_data, BuildLevel):
                min_gain = level_data.typical_power_gain_percent[0]
                max_gain = level_data.typical_power_gain_percent[1]
                min_cost = level_data.typical_cost_usd[0]
                max_cost = level_data.typical_cost_usd[1]
            else:
                continue

            if min_gain <= power_increase_percent <= max_gain * 1.2:
                if min_cost <= budget_usd:
                    recommended_level = level_name
                    break

        if recommended_level and recommended_level in builds:
            level = builds[recommended_level]
            if isinstance(level, BuildLevel):
                return {
                    "engine_code": engine_code,
                    "target_hp": target_hp,
                    "budget_usd": budget_usd,
                    "recommended_level": recommended_level,
                    "description": level.description,
                    "estimated_cost": {
                        "min": level.typical_cost_usd[0],
                        "max": level.typical_cost_usd[1]
                    },
                    "recommended_parts": level.recommended_parts,
                    "requirements": level.requirements,
                    "feasibility": "achievable"
                }

        return {
            "engine_code": engine_code,
            "target_hp": target_hp,
            "budget_usd": budget_usd,
            "recommended_level": None,
            "message": "Target may require custom build approach",
            "feasibility": "requires_consultation"
        }

    def list_documented_ecosystems(self) -> List[str]:
        """List all engines with documented ecosystems."""
        return list(AFTERMARKET_ECOSYSTEMS.keys())
