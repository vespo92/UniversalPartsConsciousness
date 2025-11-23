# UPC Engineering Showcases

> "The Tesla Roadster shares its chassis with the Lotus Elise. Every engineer who made that work had to discover parts compatibility through trial and error. UPC makes that knowledge permanent."

## What Are Showcases?

Showcases are **real-world engineering projects** that demonstrate the value of Universal Parts Consciousness. They're not theoretical examples—they're actual projects where parts compatibility knowledge was hard-won and should be preserved.

## Why We Need Showcases

### The Problem

Every day, engineers discover that:
- Part A from Manufacturer X fits Product Y
- A $15 aftermarket part replaces a $200 OEM part
- Two "incompatible" parts actually work together with a simple modification

**This knowledge dies with them.** It lives in:
- Forum posts that get deleted
- Tribal knowledge that retires with mechanics
- Engineering notes that never leave the company
- YouTube videos that describe but don't systematize

### The Solution

Showcases capture this knowledge in structured, queryable form:

```
INPUT:  "I have a Lotus Elise A-arm. What else does it fit?"
OUTPUT: Tesla Roadster (direct), Vauxhall VX220 (with spacer), Opel Speedster (European model)
        Compatibility: 96%
        Verification: Expert verified, 47 community confirmations
        Price savings: 34% vs OEM Tesla part
```

## Showcase Categories

### 1. Cross-Platform Vehicle Builds
**Tesla/Lotus** - The definitive startup-to-OEM parts sharing story
- Suspension: 94% compatible
- Interior hardware: 45% compatible
- Fasteners: 89% compatible

**LS Engine Swaps** - 25+ years of community knowledge
- 234 verified vehicle platforms
- 147+ successful Miata swaps documented
- Complete fastener specifications for every bolt

### 2. Aviation Fasteners
Life-safety critical substitution rules
- AN/MS/NAS cross-reference database
- Never-substitute warnings
- Torque specifications with sequence

### 3. Agricultural Equipment
Right-to-repair compatibility data
- John Deere ↔ Generic parts crosswalk
- Hydraulic fitting compatibility matrix
- 3-point hitch category standards

### 4. Motorcycle Ecosystem
The brake caliper swap network
- Nissin ↔ Brembo ↔ Tokico compatibility
- Fork cartridge swaps
- Chain/sprocket cross-reference

### 5. 3D Printer Parts
Open-source hardware standardization
- Linear rail compatibility (MGN12 ecosystem)
- Hotend interchange (E3D V6 ↔ Revo ↔ Dragon)
- Stepper motor specifications

## Data Structure

Each showcase contains:

```
showcase/
├── data/
│   ├── tesla_lotus_compatibility.json  # Structured compatibility data
│   ├── ls_swap_ecosystem.json          # LS engine swap knowledge
│   └── aviation_fasteners.json         # Safety-critical fastener specs
├── schemas/
│   └── cross_reference.json            # JSON Schema for validation
└── showcase_engine.py                  # Python API for queries
```

## Query Examples

### Find Compatible Parts
```python
from showcases.showcase_engine import ShowcaseEngine

engine = ShowcaseEngine()
engine.load_all_showcases()

# What fits instead of this Lotus part?
alternatives = engine.find_cross_references("A117C0035F", "Lotus")

for alt in alternatives:
    print(f"{alt.target_part_number}: {alt.compatibility_score:.0%} compatible")
```

### Generate BOM Crosswalk
```python
# I have these Lotus parts, what are the Tesla equivalents?
parts = ["A117C0035F", "A117C0034F", "A117D0049F"]
crosswalk = engine.generate_bom_crosswalk(parts, "Lotus")
```

### Check Platform Compatibility
```python
# How compatible are these two platforms?
result = engine.query_compatibility("Lotus Elise", "Tesla Roadster")
print(f"Overall compatibility: {result['summary']['average_compatibility_score']:.0%}")
```

## Database Integration

Showcases feed into the main UPC database via `schema-showcases.sql`:

```sql
-- Core query: Find all parts compatible with this one
SELECT * FROM find_compatible_parts('A117C0035F', 'Lotus', 0.7);

-- Result:
-- part_number | manufacturer | compatibility_score | type
-- TR-SUS-001  | Tesla        | 0.96               | direct_replacement
```

## Contributing Showcases

### Minimum Requirements

1. **Real project data** - Not theoretical, actually built/verified
2. **Part numbers** - Specific, searchable identifiers
3. **Compatibility scores** - Quantified fitment assessment
4. **Fastener specs** - The bolts matter as much as the parts
5. **Community validation** - At least one independent confirmation

### Data Quality Tiers

| Tier | Source | Score Multiplier |
|------|--------|------------------|
| Unverified | Single forum post | 0.5x |
| Community Tested | 3+ independent reports | 1.0x |
| Expert Verified | Professional mechanic/engineer | 1.5x |
| Manufacturer Confirmed | OEM documentation | 2.0x |
| Standard Compliant | ISO/SAE/MIL spec | 2.5x |

## The Vision

Every showcase we add makes UPC more valuable. Eventually:

1. **Engineer searches for part** → Gets cross-platform alternatives
2. **Mechanic orders replacement** → Knows cheaper compatible options
3. **Hobbyist starts project** → Has complete BOM with alternatives
4. **Manufacturer designs product** → Knows existing compatible parts

The knowledge that currently lives in human heads becomes queryable, permanent, and growing.

---

*"Parts compatibility isn't mysterious—it's just undocumented."*
