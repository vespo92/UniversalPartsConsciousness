# Agent_11: MARINER - Marine & Maritime Parts Intelligence

## The Warden of Mechanical Heritage in Hostile Saltwater Environments

---

## Overview

**Agent ID:** Agent_11
**Codename:** MARINER
**Role:** Marine & Maritime Parts Intelligence
**Version:** 1.0.0

Marine environments are the harshest on earth for mechanical parts. Saltwater corrosion, galvanic reactions, and regulatory requirements (USCG, ABYC, Lloyd's, ISO) create a unique compatibility landscape that automotive knowledge simply doesn't cover.

MARINER is the definitive source for marine parts compatibility, galvanic corrosion analysis, and marine-to-automotive cross-reference within the Universal Parts Consciousness.

---

## Core Capabilities

### 1. Galvanic Corrosion Analysis (THE Marine Specialty)

Galvanic corrosion destroys more marine hardware than any other failure mode. MARINER provides:

- **Galvanic series database** (ASTM G82 compliant, 40+ materials)
- **Risk assessment calculator** with environment factors
- **Fastener joint analysis** (unfavorable area ratio detection)
- **Isolation recommendations** (washers, sleeves, coatings)
- **Sacrificial anode specifications**

```python
from agents.mariner import MarinerAgent, MarineEnvironment

agent = MarinerAgent()
risk = agent.check_galvanic_compatibility(
    "316_stainless_passive",
    "aluminum_6061_t6",
    MarineEnvironment.SALTWATER
)

print(f"Risk Level: {risk.risk_level}")  # HIGH
print(f"Anode (will corrode): {risk.anode_material}")  # aluminum
print(f"Time to damage: {risk.time_to_damage}")  # Months to visible damage
```

### 2. Marine Engine Cross-Reference

Marine engines are often marinized automotive engines. MARINER reveals:

- **Which parts are SHARED** (save money on rebuilds)
- **Which parts are MARINE-SPECIFIC** (don't interchange)
- **NEVER INTERCHANGE parts** (FIRE/EXPLOSION hazards)

```python
xref = agent.cross_reference_marine_engine("Mercruiser", "5.7 MPI")

print(f"Automotive Base: {xref.automotive_base}")
# GM Vortec 5700 (1996-2002 truck)

print("Shared parts (save money):")
for part in xref.shared_parts:
    print(f"  - {part}")
# Pistons, connecting rods, crankshaft, cylinder heads...

print("NEVER INTERCHANGE:")
for part, danger in xref.never_interchange.items():
    print(f"  - {part}: {danger}")
# Starter: Marine is IGNITION PROTECTED - automotive can spark and EXPLODE
```

### 3. Marine-Grade Equivalent Finder

Find proper marine-rated alternatives for automotive parts:

```python
equivalents = agent.find_marine_equivalent("GM alternator 10SI")

for eq in equivalents:
    print(f"Marine: {eq.marine_equivalent}")
    print(f"Why needed: {eq.why_marine_needed}")
    print(f"Certifications: {eq.certifications}")
```

### 4. Sacrificial Anode Calculator

Proper anode sizing prevents galvanic destruction of underwater hardware:

```python
assessment = agent.calculate_anode_system(
    wetted_area_sq_ft=150,
    hull_material="fiberglass",
    propeller_material="bronze",
    shaft_material="stainless",
    shaft_diameter_in=1.25,
    drive_type="inboard",
    environment="saltwater",
    num_thru_hulls=4
)

print(f"Required zinc area: {assessment.total_required_area_sq_in} sq.in")
for anode in assessment.recommended_anodes:
    print(f"  - {anode.quantity}x {anode.size}")
```

### 5. Marine Standards Compliance

Verify compliance with marine safety standards:

```python
# Check if ignition protection is required
result = agent.check_ignition_protection_required(
    component="starter",
    location="engine compartment"
)

print(f"Required: {result['requires_ignition_protection']}")  # True
print(f"Standard: {result['applicable_standard']}")
# SAE J1171 / ISO 8846 / USCG 33 CFR 183.410
```

---

## Module Structure

```
agents/mariner/
├── __init__.py                 # Package exports
├── core/
│   ├── __init__.py
│   └── mariner_agent.py        # Main orchestration agent
├── galvanic/
│   ├── __init__.py
│   ├── material_series.py      # ASTM G82 galvanic series
│   └── corrosion_calculator.py # Risk assessment engine
├── engines/
│   ├── __init__.py
│   └── engine_crossref.py      # Marine-to-automotive database
├── standards/
│   ├── __init__.py
│   └── marine_standards.py     # ABYC, USCG, ISO standards
├── anode/
│   ├── __init__.py
│   └── anode_calculator.py     # Sacrificial anode sizing
├── integration/
│   ├── __init__.py
│   └── agent_bridge.py         # UPC network integration
└── mariner_agent.py            # Legacy single-file (deprecated)
```

---

## Domains Covered

- **Recreational boats** (outboard, inboard, stern drive)
- **Commercial marine** (workboats, fishing vessels)
- **Yacht systems** (navigation, electrical, plumbing)
- **Marine fasteners** (316SS, Monel, silicon bronze)
- **Marine engines** (Mercruiser, Volvo Penta, Crusader, Indmar)
- **Marine standards** (ABYC, USCG, ISO, Lloyd's)

---

## Key Data Structures

### GalvanicRisk

Assessment of galvanic corrosion risk between two materials:

```python
@dataclass
class GalvanicRisk:
    risk_level: RiskLevel        # MINIMAL, LOW, MODERATE, HIGH, SEVERE
    voltage_difference_mv: float
    effective_voltage_mv: float  # After environment factor
    anode_material: str          # Will corrode
    cathode_material: str        # Will be protected
    corrosion_rate: str          # Qualitative rate
    time_to_damage: str          # Expected time to visible damage
    recommendations: List[str]
    zinc_specification: Optional[str]
    isolation_method: Optional[str]
```

### MarineEngineXref

Cross-reference between marine and automotive engines:

```python
@dataclass
class MarineEngineXref:
    marine_engine: str
    marine_manufacturer: str
    automotive_base: str
    automotive_years: str
    displacement_liters: float
    shared_parts: Dict[str, str]         # Safe to interchange
    marine_specific_parts: Dict[str, str] # Do not interchange
    never_interchange: Dict[str, str]     # SAFETY CRITICAL
    notes: List[str]
    common_failures: List[str]
    rebuild_tips: List[str]
```

### AnodeSystemAssessment

Complete anode system recommendation:

```python
@dataclass
class AnodeSystemAssessment:
    hull_material: str
    wetted_area_sq_ft: float
    environment: str
    total_required_area_sq_in: float
    recommended_anodes: List[AnodeRecommendation]
    anode_type: AnodeType        # ZINC, ALUMINUM, MAGNESIUM
    inspection_interval: str
    replacement_threshold: str
    warnings: List[str]
    cost_estimate_annual: float
```

---

## Integration Points

MARINER integrates with the broader UPC agent network:

### Agent_2 (ORACLE) - Compatibility Enhancement

```
MARINER enhances ORACLE compatibility queries with galvanic risk data.

ORACLE: "Is this part compatible?"
MARINER: "Mechanically yes, but galvanic corrosion risk is HIGH"
```

### Agent_4 (EMPATH) - Qualia Collection

```
MARINER collects experiential data from marine environments.

"How did this part perform after 5 years in saltwater?"
```

### Agent_18 (ALCHEMIST) - Material Science

```
MARINER collaborates with ALCHEMIST for material recommendations.

"What material should I use for this marine application?"
```

### Agent_20 (DETECTIVE) - Failure Analysis

```
MARINER reports marine failures for pattern analysis.

"Galvanic corrosion failure: 316SS fastener in aluminum hull"
```

---

## Safety Critical Information

### NEVER Use Automotive Parts For:

| Component | Why Not | Consequence |
|-----------|---------|-------------|
| **Starter** | Not ignition protected | Sparks can ignite fuel vapors = EXPLOSION |
| **Alternator** | Not sealed/protected | Corrosion + fire hazard |
| **Distributor** | Cap not ignition protected | Arcing ignites vapors |
| **Fuel Pump** | Not sealed | Vapor leaks = fire hazard |
| **Carburetor** | No flame arrestor | FIRE HAZARD (USCG required) |
| **Exhaust Manifolds** | Not water-cooled | Will OVERHEAT and burn through |

### Galvanic Risk Summary

| Combination | Risk | Action |
|-------------|------|--------|
| 316SS + 316SS | MINIMAL | Safe |
| 316SS + Aluminum | HIGH | Isolate with nylon/plastic |
| Aluminum + Copper | SEVERE | NEVER use together |
| Bronze + Stainless | MODERATE | Isolate or use anodes |
| Graphite + Aluminum | SEVERE | Rapid destruction |

---

## Standards Covered

| Standard | Body | Scope |
|----------|------|-------|
| **SAE J1171** | SAE | Ignition protection |
| **ISO 8846** | ISO | Ignition protection (EU) |
| **ABYC E-11** | ABYC | Electrical systems |
| **ABYC H-27** | ABYC | Fuel systems |
| **USCG 33 CFR 183** | USCG | Federal safety requirements |

---

## Showcase Use Cases

### 1. "What fastener can I use on my aluminum hull?"

```python
# Analyze galvanic risk of stainless fastener on aluminum
risk = agent.check_galvanic_compatibility(
    "316_stainless_passive",
    "aluminum_5086",
    MarineEnvironment.SALTWATER
)

# Answer: HIGH risk - isolate with nylon washers + dielectric grease
# Or use aluminum fasteners (weaker but compatible)
```

### 2. "Can I use truck parts in my Mercruiser rebuild?"

```python
xref = agent.cross_reference_marine_engine("Mercruiser", "5.7 MPI")

# Shared (YES, save money): Pistons, rods, crank, heads, oil pump
# Marine-specific (NO): Intake, exhaust, water pump
# NEVER (DANGER): Starter, alternator, distributor
```

### 3. "How much zinc do I need for my boat?"

```python
assessment = agent.calculate_anode_system(
    wetted_area_sq_ft=200,
    hull_material="fiberglass",
    propeller_material="nibral",
    shaft_material="stainless",
    shaft_diameter_in=1.5,
    drive_type="inboard",
    environment="saltwater"
)

# Returns: Specific anode recommendations with part numbers
```

---

## Implementation Notes

- MARINER is part of the **Second Decalogue** (Agents 11-20)
- Priority: **MEDIUM** (clear niche, galvanic expertise is unique)
- Dependencies: None (standalone capable)
- Integration: Full UPC network connectivity via BRIDGE

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial full deployment with multi-module architecture |
| 0.1.0 | 2024 | Single-file prototype (mariner_agent.py) |

---

*Agent_11: MARINER - Because the sea respects no one who ignores galvanic corrosion.*
