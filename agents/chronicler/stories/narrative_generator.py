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
    },
    "RB26DETT": {
        "title": "The Godzilla Heart: Nissan's Racing Weapon",
        "narrative": """
## The RB26DETT: The Godzilla Heart

### Born for Battle

The RB26DETT was never meant for commuting. When Nissan's engineers designed
the heart of the R32 GT-R, they had one purpose: dominate Group A racing.
Every design decision was made with competition in mind.

Six individual throttle bodies. Twin ceramic turbochargers. A forged crankshaft.
An iron block that could handle abuse no road car would ever experience.
This was a racing engine that happened to be street legal.

### The Gentleman's Lie

Japan's "gentleman's agreement" rated the RB26DETT at 280 HP - the same as
every other Japanese sports car of the era. This was pure fiction. Dyno tests
routinely showed 330+ HP from stock engines. The agreement was a wink, not
a truth.

What the engineers knew - and what tuners quickly discovered - was that the
stock internals could handle far more. 500 HP on stock bottom end was routine.
The RB26 was overbuilt in ways that wouldn't be fully appreciated for years.

### Godzilla Awakens

When the R32 GT-R arrived at the Australian Touring Car Championship, the
competition didn't know what hit them. The car was so dominant - winning
every race it entered - that it earned the nickname "Godzilla." The monster
had awakened.

Back home in Japan, the GT-R swept Group A. At Bathurst, it conquered.
The RB26DETT proved that Japanese engineering could match and exceed
anything from Europe or America.

### The Tuner's Canvas

The RB26 became the ultimate tuner's canvas. Unlike the single-turbo 2JZ,
the RB26's twin-turbo setup offered choices: keep the twins, go single,
or even triple-turbo. The inline-six's perfect balance allowed for
astronomical boost levels without tearing itself apart.

Tomei, HKS, Trust, Nismo - Japan's finest tuners built their reputations
on the RB26. The engine rewarded expertise. It demanded respect. And it
delivered power that seemed impossible from 2.6 liters.

### Legacy: The Original Supercar Killer

Before the GT-R became mainstream with the R35, the RB26-powered Skylines
were underground heroes. Imported illegally to countries with strict
regulations, they were whispered about in car meets and celebrated
in video games.

The RB26DETT proved that a straight-six could compete with V8s and V12s.
It proved that Japanese engineering had reached world-class status.
And it created a legacy that the modern VR38DETT still lives in the
shadow of.

*"It's a Skyline"* - Said with the same reverence as prayer.
"""
    },
    "B16A": {
        "title": "VTEC Just Kicked In, Yo: Honda's Revolution",
        "narrative": """
## The B16A: When VTEC Changed Everything

### The Impossible Dream

In the late 1980s, the accepted wisdom was simple: you couldn't have both
low-end tractability AND high-RPM screaming power from the same engine.
You picked one. You compromised. That was physics.

Honda's engineers disagreed.

### The Breakthrough: VTEC

Variable Valve Timing and Lift Electronic Control. VTEC. The system that
would become a meme started as an engineering marvel. By using two
different cam profiles and switching between them at high RPM, Honda
created an engine with two personalities.

Below 5,500 RPM, the B16A was docile. Smooth. Economical. The mild cam
profile prioritized fuel efficiency and low-end torque. Perfect for
traffic. Boring for enthusiasts.

Then you hit the crossover point.

### The Switch

Anyone who has driven a VTEC engine remembers their first time. The engine
note changes. The power delivery transforms. What was a sensible commuter
engine suddenly becomes a screaming high-RPM monster demanding you chase
the redline.

160 HP from 1.6 liters, naturally aspirated. 100 HP per liter in 1989.
Numbers that forced the automotive world to reconsider what was possible
from a four-cylinder engine.

### The Culture

The B16A didn't just create an engine—it created a culture. Honda-Tech forums.
Integra vs. Civic debates. The endless quest for more power without boost.
"All motor" became a badge of honor.

The distinctive intake sound. The metallic exhaust note at high RPM.
The moment of transition. These became defining characteristics of a
generation of enthusiasts who learned to love engines that rewarded
RPM over displacement.

### Legacy: The Template

Every turbocharged 2.0-liter that revs to 7,000 RPM today owes a debt to
the B16A. It proved that small displacement didn't mean small power.
It proved that technology could overcome physics. It proved that Honda's
engineering philosophy - high revs, high efficiency, high excitement -
was viable.

The B16A spawned the B18C, the K20, and eventually influenced every
performance four-cylinder that followed. When manufacturers design
their latest hot hatch engine, they're building on foundations the
B16A laid.

*"VTEC just kicked in, yo!"* - More than a meme. A moment of transformation.
"""
    },
    "426 Hemi": {
        "title": "The Elephant Motor: Mopar's Nuclear Option",
        "narrative": """
## The 426 Hemi: The Elephant Motor

### The NASCAR Necessity

In 1964, Chrysler had a problem. Their wedge-head engines were being
outpaced on NASCAR ovals. They needed something radical. Something
that would dominate so completely that competitors would cry foul.

They needed the Hemi.

### The Hemispherical Advantage

The hemispherical combustion chamber wasn't new—aircraft engines had
used the design for decades. But applying it to a production V8
meant solving problems no one had tackled before. Chrysler's engineers
rose to the challenge.

The hemispherical chamber allowed for larger valves at optimal angles.
Better breathing. More efficient combustion. More power per cubic inch.
The geometry was complex, the manufacturing expensive, but the results
were undeniable.

### Daytona Domination

When the 426 Hemi arrived at the 1964 Daytona 500, it was massacre.
Richard Petty led a 1-2-3 Chrysler sweep. The competition was so
demoralized that NASCAR banned the engine for 1965, demanding Chrysler
produce a street version.

Chrysler complied. The Street Hemi arrived in 1966, detuned to "only"
425 HP. It came with a four-speed manual and a warranty that basically
said "good luck." The message was clear: this was a race engine with
license plates.

### The Muscle Car King

The 426 Hemi became the ultimate status symbol of the muscle car era.
Available in the Charger, 'Cuda, Challenger, and GTX, it was the
apex predator of Woodward Avenue. The "Elephant Motor" nickname came
from its size and weight, but it might as well have described its
impact on the competition.

For 1970, you could order a Hemi 'Cuda with a shaker hood, pistol-grip
four-speed, and Dana 60 rear. It was the most dangerous thing on four
wheels that didn't require a pilot's license.

### Legacy: The Ultimate Mopar

The 426 Hemi lived for only seven years (1964-1971), but its legend
is immortal. It defined what a muscle car engine could be. It proved
that American manufacturers could build world-class performance
equipment. It created a collector market where Hemi 'Cudas sell for
millions.

When Dodge revived the Hemi name in 2003, they were trading on
heritage. When they released the Hellcat and Demon, they were chasing
the 426's ghost. The original Elephant Motor remains the standard
against which all American muscle is measured.

*"Yeah, it's got a Hemi"* - The answer that ends all arguments.
"""
    },
    "LS1": {
        "title": "The Swap King: GM's Aluminum Revolution",
        "narrative": """
## The LS1: The Engine That Goes In Everything

### The Impossible Task

By the mid-1990s, the small block Chevy was ancient. The basic design
dated to 1955. While it had evolved, it was fundamentally a 1950s engine
in a modern world. GM's engineers faced an impossible task: replace an
icon.

The LS1 was their answer.

### Aluminum Revolution

The LS1 did everything differently. Aluminum block instead of iron—100
pounds lighter. Modern fuel injection with individual coils per cylinder.
Plastic intake manifold. Computer-controlled everything.

But it kept the pushrods.

This was the genius compromise. While the world moved to DOHC, GM's
engineers realized that pushrods weren't the problem. With modern
airflow analysis and careful engineering, a pushrod engine could
breathe with the best. And pushrod engines were compact, lightweight,
and simple.

### The C5 Corvette Launches a Legend

When the LS1 debuted in the 1997 C5 Corvette, skeptics were silenced.
345 HP. 0-60 in 4.7 seconds. Competitive with Porsches and Ferraris
at a fraction of the cost. The little engine from Kentucky proved
that American engineering had arrived.

But it was what came next that created the legend.

### The Swap Era Begins

Someone dropped an LS1 into a Miata. Then a 240SX. Then an RX-7. Then
a Porsche 944. Then a Volvo. Then a BMW. Then everything else with
wheels.

"LS Swap It" became the universal answer to any automotive problem.
Underpowered? LS swap. Engine blown? LS swap. Wrong number of cylinders?
LS swap. The LS1's compact dimensions, massive aftermarket support, and
accessibility created a swap culture that shows no signs of slowing.

### Legacy: The Democratizer

The LS1 did something revolutionary: it made V8 power accessible. Where
traditional American V8s were heavy, thirsty, and complicated, the LS
was lightweight, efficient (for a V8), and simple to work on.

It proved that pushrod engines weren't obsolete. It created an
aftermarket industry worth billions. And it gave enthusiasts around
the world a reliable, powerful option for any chassis they could
dream of swapping one into.

The LS1 isn't just an engine. It's a universal parts bin. A solution
to every horsepower problem. The great equalizer.

*"Just LS swap it"* - The answer to every automotive question.
"""
    },
    "4G63T": {
        "title": "The Rally Warrior: Mitsubishi's Turbocharged Legend",
        "narrative": """
## The 4G63T: Born in the Forests

### Rally Roots

While other engines were designed for street cars and adapted for racing,
the 4G63T's destiny was written in dirt. The turbocharged 2.0-liter
four-cylinder was Mitsubishi's weapon for the World Rally Championship,
and every design decision reflected this purpose.

Iron block for strength. Forged internals from the factory. A turbocharger
system that could handle boost levels that would destroy lesser engines.
This was war machinery.

### The Lancer Evolution

When Mitsubishi needed to homologate their rally cars, they created
the Lancer Evolution. Initially Japan-only, word spread quickly:
this was something special. By the time the Evo VIII arrived in
American showrooms, the legend was already established.

276 HP (the gentleman's agreement number, of course). All-wheel drive.
Active differentials. A turbocharged engine that tuners had already
proven could handle 600+ HP without breaking a sweat. The Evo was
the street-legal rally car everyone had been waiting for.

### The Subaru War

The rivalry with the Subaru WRX STI defined a generation. Two
turbocharged AWD sedans. Two passionate fan bases. Endless forum
arguments. Track day battles. Time attack championships.

The 4G63T held one crucial advantage: its iron block. While the
EJ257's open deck design limited power potential, the 4G63T's
closed-deck iron construction could handle over 1,000 HP. In
the escalating horsepower war, this mattered.

### Tuner's Delight

The 4G63T rewarded those who understood it. The 7-bolt vs. 6-bolt
debates. The balance shaft delete discussions. The optimal turbo
sizing for various power goals. AMS, Buschur, English Racing—
specialty shops built empires serving the Evo community.

When someone finally breaks the Pikes Peak record, there's a good
chance a 4G63T will be involved. The engine's combination of
strength, response, and tunability made it the ultimate weapon
for serious competitors.

### Legacy: The Rally Spirit

The 4G63T represented something pure: an engine designed for
competition, offered to the public. It never compromised for
fuel economy or emissions beyond what was legally required.
It existed to go fast, and it did that job brilliantly.

When Mitsubishi ended Evo production in 2016, they closed a
chapter. But the 4G63T's influence lives on in every turbocharged
AWD sedan that followed. The rally spirit, preserved in iron
and aluminum.

*"It's an Evo thing"* - You either understand, or you don't.
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
