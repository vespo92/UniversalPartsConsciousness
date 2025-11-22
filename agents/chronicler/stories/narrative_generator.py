"""
Narrative Generator - Creates compelling stories about engines.

Generates narrative content for engine histories, racing heritage,
community culture, and legendary build stories.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class NarrativeTemplate:
    """Template for narrative generation."""
    template_type: str
    sections: List[str]
    tone: str
    target_length_words: int


# Narrative templates
NARRATIVE_TEMPLATES = {
    "engine_history": NarrativeTemplate(
        template_type="Engine History",
        sections=["Origins", "Development", "Evolution", "Legacy"],
        tone="informative_reverent",
        target_length_words=1500
    ),
    "racing_heritage": NarrativeTemplate(
        template_type="Racing Heritage",
        sections=["Competition Birth", "Glory Days", "Iconic Moments", "Legacy"],
        tone="dramatic_triumphant",
        target_length_words=1200
    ),
    "community_culture": NarrativeTemplate(
        template_type="Community Culture",
        sections=["The Scene", "The People", "The Builds", "The Future"],
        tone="passionate_inclusive",
        target_length_words=1000
    ),
    "legendary_build": NarrativeTemplate(
        template_type="Legendary Build",
        sections=["The Vision", "The Build", "The Results", "The Impact"],
        tone="enthusiastic_detailed",
        target_length_words=800
    )
}


# Pre-written narratives for legendary engines
ENGINE_NARRATIVES = {
    "2JZ-GTE": {
        "title": "The Inline-Six That Conquered the World",
        "narrative": """
## The 2JZ-GTE: The Inline-Six That Conquered the World

### Origins: Born for Grand Touring

When Toyota's engineers set out to create the powerplant for the fourth-generation
Supra (A80), they weren't just designing an engine—they were engineering a statement.
The 2JZ-GTE would need to match the best from BMW and Mercedes while embodying
Toyota's uncompromising reliability standards.

The result was a 3.0L twin-turbocharged inline-six that would become the most
celebrated engine in tuning history. But its legend would be built not by Toyota's
intentions, but by what enthusiasts discovered hidden within.

### The Discovery: Accidental Overengineering

Toyota, conservative by nature, built the 2JZ with massive safety margins. The iron
block, forged crankshaft, and robust bottom end were designed to handle years of
abuse in grand touring duty. What the engineers didn't anticipate was a global
community of tuners who would push these safety margins to their absolute limits.

The discovery was almost accidental. Early Supra tuners, upgrading to single-turbo
setups, found they could double the stock horsepower without touching the internals.
Then triple it. The stock bottom end, rated for 320 HP, could reliably handle over
700 HP. With basic modifications, 1,000 HP became achievable.

### The Phenomenon: Democratizing Big Power

Before the 2JZ, building 1,000 HP required a NASCAR-level budget. Purpose-built
race engines cost $50,000 or more and required constant rebuilds. The 2JZ changed
everything.

Suddenly, enthusiasts could achieve supercar-slaying power for a fraction of the
cost. The engine started every time, didn't leak, and could be daily driven.
Forums exploded with build threads documenting 800, 1,000, even 1,500 HP builds
on stock internals.

The Fast & Furious franchise cemented its pop culture status. "The supra is
not just a car, it's a lifestyle" became a reality for hundreds of thousands
of enthusiasts worldwide.

### Legacy: The Standard Against Which All Are Measured

Today, the 2JZ-GTE is the benchmark for engine potential. When manufacturers
release new performance engines, the first question asked is inevitably:
"How does it compare to a 2JZ?"

The world record 2JZ builds exceed 2,500 HP. Drag cars run 6-second quarter
miles. Time attack vehicles shatter lap records. All powered by an engine
designed for comfortable highway cruising.

The 2JZ proved that with the right foundation, limits are meant to be broken.
It democratized high-horsepower builds and created a global community united
by their reverence for a twin-turbo inline-six from Japan.

*"Is that a Supra?!"* - The question that launched a thousand builds.
"""
    },
    "13B-REW": {
        "title": "The Rotary Anomaly: Mazda's Defiant Masterpiece",
        "narrative": """
## The 13B-REW: The Rotary Anomaly

### The Hiroshima Spirit

When other manufacturers abandoned the rotary engine—citing emissions problems,
poor fuel economy, and apex seal failures—Mazda refused. In Hiroshima, a team
of 47 engineers, known internally as "The 47 Ronin," dedicated themselves to
making the impossible work.

The 13B-REW was their masterpiece.

### Against All Odds

The rotary engine should not exist in the modern era. Its combustion chamber
shape makes emissions control difficult. Its sealing requirements demand
precision beyond what most manufacturers consider economical. Its fuel
consumption embarrasses even V8s.

Yet here stood the 13B-REW: a 1.3L twin-turbocharged engine producing 255 HP—
nearly 200 HP per liter. In naturally aspirated form, it achieved 215 HP/L,
a figure that piston engines struggle to match even today.

### The Physics of Defiance

The rotary's advantages are as unique as its challenges. No reciprocating
mass means an engine that revs with supernatural eagerness. No valves mean
no valve float. The compact size allows mid-engine placement where piston
engines cannot fit.

In the RX-7 FD, the 13B-REW sat behind the front axle, creating a weight
distribution that made the car dance. Professional drivers spoke of the
engine's character—how it encouraged you to explore its upper reaches,
how it rewarded commitment.

### The Community: Keepers of the Flame

Today, the rotary community is perhaps the most dedicated in automotive
culture. They understand their engines are orphans—no manufacturer will
build another. Every rebuild is performed with reverence, every apex seal
installed with ritual precision.

YouTube tutorials document rebuild procedures in exhaustive detail.
Facebook groups share hard-won wisdom about premixing oil, about the
sounds that precede failure, about the modifications that work and
those that don't.

Rob Dahm's 4-rotor builds push the boundaries of what's possible.
Mad Mike's RADBUL shows the world what a rotary can do in competition.
Each new achievement is celebrated as a victory for the tribe.

### Legacy: The Rebel's Choice

The 13B-REW represents something beyond specifications. It represents
the romantic notion that some things are worth preserving regardless
of efficiency metrics. That passion can overcome practicality. That
engineers can be artists.

When someone chooses a rotary in 2024, they're not choosing the
sensible option. They're choosing to join a community that refuses
to let go of something beautiful.

*"It goes brap brap brap"* - And that's all the explanation needed.
"""
    }
}


class NarrativeGenerator:
    """
    Generates narrative content for engines and parts.

    Creates compelling stories that transform specifications
    into meaningful cultural documentation.
    """

    def __init__(self):
        """Initialize the narrative generator."""
        self._generated_count = 0

    def generate_narrative(
        self,
        engine_code: str,
        narrative_type: str = "engine_history",
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a narrative for an engine.

        Args:
            engine_code: Engine code
            narrative_type: Type of narrative to generate
            context_data: Optional context data

        Returns:
            Narrative content and metadata
        """
        # Check for pre-written narratives
        if engine_code in ENGINE_NARRATIVES:
            narrative = ENGINE_NARRATIVES[engine_code]
            return {
                "engine_code": engine_code,
                "type": narrative_type,
                "title": narrative["title"],
                "content": narrative["narrative"].strip(),
                "word_count": len(narrative["narrative"].split()),
                "source": "chronicler_archive",
                "status": "complete"
            }

        # Generate from template
        template = NARRATIVE_TEMPLATES.get(
            narrative_type,
            NARRATIVE_TEMPLATES["engine_history"]
        )

        # Create skeleton narrative
        content = self._generate_skeleton(engine_code, template, context_data)

        return {
            "engine_code": engine_code,
            "type": narrative_type,
            "title": f"The {engine_code} Story",
            "content": content,
            "word_count": len(content.split()),
            "source": "generated_skeleton",
            "status": "needs_enrichment",
            "template_used": template.template_type
        }

    def _generate_skeleton(
        self,
        engine_code: str,
        template: NarrativeTemplate,
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a skeleton narrative from template."""
        sections = []

        for section in template.sections:
            section_content = f"## {section}\n\n"
            section_content += f"[{section} content for {engine_code} to be documented]\n\n"
            sections.append(section_content)

        header = f"# The {engine_code}: A Story to be Told\n\n"
        header += f"*This narrative requires community contributions to complete.*\n\n"

        return header + "\n".join(sections)

    def generate_racing_heritage(
        self,
        engine_code: str,
        racing_data: Dict[str, Any]
    ) -> str:
        """Generate racing heritage narrative."""
        wins = racing_data.get("wins", [])
        series = racing_data.get("series", [])
        drivers = racing_data.get("notable_drivers", [])

        content = f"# Racing Heritage: {engine_code}\n\n"

        if series:
            content += "## Competition History\n\n"
            content += f"The {engine_code} competed in: {', '.join(series)}\n\n"

        if wins:
            content += "## Notable Victories\n\n"
            for win in wins[:5]:
                content += f"- {win}\n"
            content += "\n"

        if drivers:
            content += "## Legendary Drivers\n\n"
            content += f"Driven by: {', '.join(drivers)}\n"

        return content

    def generate_community_profile(
        self,
        engine_code: str,
        community_data: Dict[str, Any]
    ) -> str:
        """Generate community culture profile."""
        forums = community_data.get("forums", [])
        builders = community_data.get("notable_builders", [])
        culture = community_data.get("culture_notes", "")

        content = f"# Community Profile: {engine_code}\n\n"

        if culture:
            content += f"## The Scene\n\n{culture}\n\n"

        if forums:
            content += "## Community Hubs\n\n"
            for forum in forums:
                content += f"- {forum}\n"
            content += "\n"

        if builders:
            content += "## Notable Builders\n\n"
            for builder in builders:
                content += f"- {builder}\n"

        return content

    def get_available_narratives(self) -> List[str]:
        """Get list of engines with pre-written narratives."""
        return list(ENGINE_NARRATIVES.keys())

    def get_narrative_types(self) -> List[str]:
        """Get available narrative types."""
        return list(NARRATIVE_TEMPLATES.keys())
