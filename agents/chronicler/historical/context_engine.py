"""
Historical Context Engine - Provides rich historical context for engines.

Generates comprehensive historical reports that explain why an engine
mattered in its era, including industry context, technological limitations,
and cultural significance.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class EraContext:
    """Context for a specific automotive era."""
    name: str
    years: tuple  # (start_year, end_year)
    key_events: List[str]
    technology_level: str
    regulatory_environment: str
    fuel_prices_usd_per_gallon: float
    racing_series_active: List[str]
    cultural_characteristics: str


# Automotive era definitions
AUTOMOTIVE_ERAS = {
    "pre_war": EraContext(
        name="Pre-War Era",
        years=(1900, 1945),
        key_events=["Mass production begins", "First World War", "Great Depression"],
        technology_level="Carburetors, flathead engines, mechanical everything",
        regulatory_environment="Minimal regulation",
        fuel_prices_usd_per_gallon=0.20,
        racing_series_active=["Indianapolis 500", "European Grand Prix"],
        cultural_characteristics="Automobiles as luxury items, early enthusiast culture"
    ),
    "post_war_boom": EraContext(
        name="Post-War Boom",
        years=(1945, 1965),
        key_events=["Baby Boom", "Interstate Highway System", "Muscle car genesis"],
        technology_level="OHV V8s, automatic transmissions, power accessories",
        regulatory_environment="Still minimal, no emissions or safety requirements",
        fuel_prices_usd_per_gallon=0.30,
        racing_series_active=["NASCAR", "Formula 1", "Le Mans 24"],
        cultural_characteristics="Cars as status symbols, hot rod culture, drag racing"
    ),
    "muscle_era": EraContext(
        name="Classic Muscle Era",
        years=(1964, 1973),
        key_events=["Mustang launch", "Pony car wars", "Factory supercars"],
        technology_level="High-compression V8s, Hemi, big blocks",
        regulatory_environment="Emissions looming, safety regulations beginning",
        fuel_prices_usd_per_gallon=0.35,
        racing_series_active=["Trans-Am", "NASCAR", "NHRA"],
        cultural_characteristics="Power wars, factory racing programs, youth culture"
    ),
    "malaise_era": EraContext(
        name="Malaise Era",
        years=(1973, 1983),
        key_events=["Oil Crisis 1973", "Emissions regulations", "Import invasion"],
        technology_level="Smog equipment, detuned engines, early EFI experiments",
        regulatory_environment="Strict emissions, CAFE standards introduced",
        fuel_prices_usd_per_gallon=1.20,
        racing_series_active=["IMSA", "Formula 1", "WRC"],
        cultural_characteristics="Performance decline, economy focus, Japanese imports rise"
    ),
    "turbo_group_b": EraContext(
        name="Turbo Era / Group B",
        years=(1983, 1992),
        key_events=["Turbo revolution", "Group B rallying", "Japanese sports car golden age"],
        technology_level="Turbocharging mainstream, 4-valve heads, AWD development",
        regulatory_environment="Emissions stabilizing, safety improving",
        fuel_prices_usd_per_gallon=1.00,
        racing_series_active=["Group B Rally", "Group A", "IMSA GTP", "F1 Turbo Era"],
        cultural_characteristics="Technology showcase, Japanese manufacturers rise, turbo everything"
    ),
    "jdm_golden_age": EraContext(
        name="JDM Golden Age",
        years=(1989, 2002),
        key_events=["NSX launch", "GT-R R32", "280HP gentleman's agreement", "Bubble economy"],
        technology_level="VTEC, twin-turbo, AWD, advanced electronics",
        regulatory_environment="Stable, focused on refinement",
        fuel_prices_usd_per_gallon=1.20,
        racing_series_active=["JGTC", "Le Mans", "WRC", "D1 Grand Prix"],
        cultural_characteristics="Japanese engineering peak, import tuning culture, drift scene birth"
    ),
    "modern_performance": EraContext(
        name="Modern Performance Era",
        years=(2002, 2012),
        key_events=["Direct injection mainstream", "DSG/DCT transmissions", "Turbo 4s return"],
        technology_level="Direct injection, dual-clutch, variable everything",
        regulatory_environment="Stricter emissions, global harmonization",
        fuel_prices_usd_per_gallon=3.00,
        racing_series_active=["F1", "DTM", "WTCC", "GT3"],
        cultural_characteristics="Technology democratization, tuning maturation, online communities"
    ),
    "turbo_renaissance": EraContext(
        name="Turbo Renaissance",
        years=(2012, 2020),
        key_events=["Turbo 4 performance cars", "1000HP club mainstream", "Electric competition"],
        technology_level="Sophisticated turbo systems, hybrid assistance, 8+ speed transmissions",
        regulatory_environment="Aggressive emissions targets, electrification push",
        fuel_prices_usd_per_gallon=2.50,
        racing_series_active=["Formula E debut", "F1 Hybrid", "GT3", "Time Attack"],
        cultural_characteristics="Turbo acceptance, hybrid embrace, build culture explosion"
    ),
    "electrification": EraContext(
        name="Electrification Era",
        years=(2020, 2035),
        key_events=["ICE sunset announcements", "EV performance cars", "Hypercar electrification"],
        technology_level="Hybrid everything, EV platforms, 800V systems",
        regulatory_environment="ICE phase-out timelines, EV mandates",
        fuel_prices_usd_per_gallon=3.50,
        racing_series_active=["Formula E", "Extreme E", "Hybrid Le Mans"],
        cultural_characteristics="Preservation movement, last ICE celebration, EV acceptance"
    )
}


# Engine significance narratives
ENGINE_SIGNIFICANCE = {
    "B16A": """
The Honda B16A (1989) was revolutionary because it achieved what many thought
impossible: 100+ horsepower per liter from a naturally aspirated production
engine, without turbocharging or exotic materials.

VTEC (Variable Valve Timing and Lift Electronic Control) changed everything.
By using two different cam profiles and switching between them at high RPM,
Honda created an engine that was docile in traffic but screamed to 8,000+ RPM
when pushed.

The B16A proved that engineering innovation could overcome displacement
disadvantage. It influenced every performance 4-cylinder that followed and
created a tuning culture that persists 30+ years later.
""",
    "2JZ-GTE": """
The Toyota 2JZ-GTE (1991) was over-engineered from the factory. Toyota's
engineers, expecting turbo lag complaints from the twin-turbo setup, built
a bottom end strong enough for racing applications.

What they didn't anticipate was the tuning community's discovery of this
strength. The iron block, forged internals, and robust design allowed
1,000+ HP on stock internals - a feat that became the engine's legend.

The 2JZ democratized high-horsepower builds. Where 1,000 HP once required
a $50,000 NASCAR engine, the 2JZ offered it for $15,000 with better
reliability. It changed what was possible for amateur builders.
""",
    "13B-REW": """
The Mazda 13B-REW (1992) represents perhaps the most stubborn act of
engineering defiance in automotive history. When other manufacturers
abandoned rotary technology due to emissions and reliability issues,
Mazda's '47 Ronin' - a dedicated engineering team - refused to give up.

The result: a twin-turbo rotary producing 255 HP from 1.3L, achieving
power density that piston engines couldn't match. At 215 HP/liter
naturally aspirated, the 13B-REW was a technical marvel.

But the 13B-REW transcends specifications. It represents the romantic
notion that passion can overcome practicality, that some things are worth
preserving regardless of efficiency metrics.
""",
    "LS1": """
The General Motors LS1 (1997) initiated what would become the 'LS Swap'
revolution. Its aluminum block reduced weight by 100 lbs over iron small
blocks while maintaining legendary pushrod V8 reliability.

The engine's compact dimensions - shorter, narrower, and lighter than
predecessors - made it fit where V8s shouldn't. This physical advantage,
combined with massive aftermarket support, made 'LS Swap It' the universal
answer to any underpowered vehicle.

The LS1 democratized V8 performance. Its cathedral-port heads, modern
fuel injection, and accessible tuning meant ordinary enthusiasts could
build 500+ HP engines that started every time and lasted 200,000 miles.
""",
    "RB26DETT": """
The Nissan RB26DETT (1989) was born for Group A racing. Its straight-six
layout, individual throttle bodies, and twin-turbo system were designed
with competition in mind, not cost accountants.

The 'gentleman's agreement' rating of 280 HP was immediately recognized
as fictional. Tuners found that stock internals could handle 500+ HP,
and the engine's racing DNA showed in every component.

The RB26 defined the GT-R legend. Each R32, R33, and R34 that dominated
track days and time attack events reinforced the engine's reputation as
the ultimate expression of Japanese engineering philosophy.
""",
    "K20A": """
The Honda K20A (2001) evolved the VTEC philosophy for a new era. Where
the B-series proved high-revving NA 4-cylinders were viable, the K-series
proved they could be refined.

With i-VTEC combining variable timing and lift, a 2.0L engine that revved
to 8,400 RPM, and Honda's legendary build quality, the K20A became the
benchmark for naturally aspirated 4-cylinder performance.

The K20A's influence extends to this day. Its swap compatibility, endless
aftermarket support, and proven reliability make it the spiritual successor
to the B-series - and for many, an improvement.
"""
}


class HistoricalContextEngine:
    """
    Generates rich historical context for engines and parts.

    Provides era-appropriate context including technology limitations,
    competitive landscape, regulatory environment, and cultural factors
    that influenced engineering decisions.
    """

    def __init__(self):
        """Initialize the context engine."""
        self._context_cache: Dict[str, Dict[str, Any]] = {}

    def generate_context(
        self,
        engine_code: str,
        year: int,
        manufacturer: str
    ) -> Dict[str, Any]:
        """
        Generate comprehensive historical context for an engine.

        Args:
            engine_code: Engine code
            year: Production year
            manufacturer: Manufacturer name

        Returns:
            Historical context report
        """
        era = self.determine_era(year)
        era_context = AUTOMOTIVE_ERAS.get(era, AUTOMOTIVE_ERAS["modern_performance"])

        return {
            "engine_code": engine_code,
            "production_year": year,
            "manufacturer": manufacturer,
            "era": {
                "name": era_context.name,
                "period": f"{era_context.years[0]}-{era_context.years[1]}",
                "key_events": era_context.key_events
            },
            "industry_context": {
                "technology_level": era_context.technology_level,
                "regulatory_environment": era_context.regulatory_environment,
                "fuel_prices": f"${era_context.fuel_prices_usd_per_gallon:.2f}/gallon",
                "racing_series": era_context.racing_series_active
            },
            "engineering_context": self._get_engineering_context(year),
            "cultural_context": {
                "automotive_culture": era_context.cultural_characteristics,
                "market_conditions": self._get_market_conditions(year, manufacturer)
            },
            "significance": {
                "narrative": self.explain_significance(engine_code),
                "era_position": self._assess_era_position(engine_code, year)
            }
        }

    def determine_era(self, year: int) -> str:
        """Determine the automotive era for a given year."""
        for era_key, era_context in AUTOMOTIVE_ERAS.items():
            if era_context.years[0] <= year <= era_context.years[1]:
                return era_key
        return "electrification" if year > 2020 else "pre_war"

    def _get_engineering_context(self, year: int) -> Dict[str, str]:
        """Get engineering context for a year."""
        if year < 1970:
            return {
                "materials": "Cast iron blocks, steel cranks, limited aluminum",
                "manufacturing": "Manual assembly, basic machining",
                "simulation": "Slide rules, analog calculations",
                "cad_status": "Non-existent"
            }
        elif year < 1985:
            return {
                "materials": "Aluminum heads becoming common, steel internals",
                "manufacturing": "CNC emerging, tighter tolerances",
                "simulation": "Basic computer modeling",
                "cad_status": "Primitive 2D drafting"
            }
        elif year < 2000:
            return {
                "materials": "Aluminum blocks common, composite intake manifolds",
                "manufacturing": "CNC standard, robotic welding",
                "simulation": "CFD and FEA emerging",
                "cad_status": "3D CAD mainstream"
            }
        else:
            return {
                "materials": "Advanced alloys, carbon fiber applications",
                "manufacturing": "High-precision CNC, additive manufacturing",
                "simulation": "Full digital twins, advanced CFD/FEA",
                "cad_status": "Parametric 3D standard"
            }

    def _get_market_conditions(self, year: int, manufacturer: str) -> str:
        """Get market conditions for a year and manufacturer."""
        if year < 1970:
            return "Growth market, domestic dominance, minimal imports"
        elif year < 1985:
            return "Oil crisis aftermath, Japanese import surge, downsizing"
        elif year < 2000:
            return "Globalization, platform sharing, performance resurgence"
        elif year < 2015:
            return "Global financial crisis recovery, turbo renaissance"
        else:
            return "Electrification transition, SUV dominance, performance preservation"

    def _assess_era_position(self, engine_code: str, year: int) -> str:
        """Assess where the engine stood in its era."""
        if engine_code in ENGINE_SIGNIFICANCE:
            return "Pioneer - defined its era and influenced successors"
        return "Contemporary - reflected the technology and culture of its time"

    def explain_significance(self, engine_code: str) -> str:
        """
        Generate a narrative explanation of why an engine mattered.

        This is the soul of the Chronicler - the human story behind
        mechanical engineering.
        """
        if engine_code in ENGINE_SIGNIFICANCE:
            return ENGINE_SIGNIFICANCE[engine_code].strip()

        # Generic significance for unknown engines
        return (
            f"The {engine_code} represents its manufacturer's engineering "
            f"philosophy and technological capabilities of its era. While "
            f"specific historical significance data is not yet documented, "
            f"the engine contributed to the evolution of automotive technology."
        )

    def get_era_competitors(self, engine_code: str, year: int) -> List[str]:
        """Get competing engines from the same era."""
        era = self.determine_era(year)

        competitors = {
            "muscle_era": ["426 Hemi", "LS6 454", "Boss 429", "440 Six Pack"],
            "jdm_golden_age": ["2JZ-GTE", "RB26DETT", "13B-REW", "4G63T", "SR20DET"],
            "modern_performance": ["LS3", "S65", "2UR-GSE", "VQ37VHR"],
            "turbo_renaissance": ["S55", "M178", "VR30DDTT", "B58"]
        }

        return competitors.get(era, [])

    def get_era_overview(self, era_key: str) -> Optional[Dict[str, Any]]:
        """Get complete overview of an automotive era."""
        if era_key not in AUTOMOTIVE_ERAS:
            return None

        era = AUTOMOTIVE_ERAS[era_key]
        return {
            "name": era.name,
            "years": f"{era.years[0]}-{era.years[1]}",
            "key_events": era.key_events,
            "technology": era.technology_level,
            "regulations": era.regulatory_environment,
            "fuel_price": f"${era.fuel_prices_usd_per_gallon:.2f}/gallon",
            "racing": era.racing_series_active,
            "culture": era.cultural_characteristics
        }

    def list_eras(self) -> List[str]:
        """List all defined automotive eras."""
        return list(AUTOMOTIVE_ERAS.keys())
