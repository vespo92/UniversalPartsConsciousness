# Agent_18: ALCHEMIST - Materials Science Intelligence

## Codename: ALCHEMIST
## Role: Materials & Metallurgy Consciousness

> *"From iron to titanium, from polymer to ceramic—the Alchemist knows all materials, their secrets, their strengths, their weaknesses. It is the foundation upon which all compatibility decisions rest."*

---

## Overview

Agent_18 (ALCHEMIST) provides the fundamental materials science intelligence that underpins all parts compatibility decisions in the Universal Parts Consciousness. Whether determining if two metals will cause galvanic corrosion, selecting the right polymer for a chemical environment, or cross-referencing alloy designations across international standards, ALCHEMIST is the authority.

### Priority: HIGH
Materials knowledge is foundational—without understanding materials, no compatibility decision is complete.

---

## Core Domains

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALCHEMIST DOMAIN MAP                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   METALS    │  │  POLYMERS   │  │ COMPOSITES  │            │
│  │   & ALLOYS  │  │  & RUBBERS  │  │ & CERAMICS  │            │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤            │
│  │ Steel       │  │ PEEK        │  │ Carbon Fiber│            │
│  │ Aluminum    │  │ PTFE        │  │ Fiberglass  │            │
│  │ Titanium    │  │ Viton       │  │ Kevlar      │            │
│  │ Copper      │  │ UHMWPE      │  │ Al2O3       │            │
│  │ Nickel      │  │ Silicone    │  │ SiC         │            │
│  │ Inconel     │  │ EPDM        │  │ Zirconia    │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                │                │                    │
│         └────────────────┼────────────────┘                    │
│                          │                                     │
│              ┌───────────┴───────────┐                        │
│              │  COATINGS & SURFACE   │                        │
│              │     TREATMENTS        │                        │
│              ├───────────────────────┤                        │
│              │ Anodizing  │ Plating  │                        │
│              │ Passivation│ PVD/CVD  │                        │
│              │ Powder Coat│ Geomet   │                        │
│              └───────────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Problem ALCHEMIST Solves

### Challenge 1: Material Confusion Across Standards
The same material has different names in different countries:
- **6061-T6** (USA/AA) = **EN AW-6061-T6** (Europe) = **A6061-T6** (Japan/JIS)
- **316L** (USA/AISI) = **1.4404** (Europe/EN) = **SUS316L** (Japan/JIS)

Engineers waste hours finding equivalents. ALCHEMIST provides instant cross-reference.

### Challenge 2: Galvanic Corrosion Blindness
Connecting dissimilar metals causes electrochemical corrosion. The classic failure:
- Stainless steel bolt in aluminum → Aluminum corrodes
- Copper pipe to galvanized steel → Steel corrodes rapidly

ALCHEMIST calculates galvanic risk and provides mitigation strategies.

### Challenge 3: "Will This Material Work?"
Engineers need to know:
- Can 304 stainless handle my marine application, or do I need 316?
- What plastic survives 150°C continuous exposure?
- What's the cheapest material that meets my strength requirements?

ALCHEMIST provides data-driven material selection.

---

## Core Capabilities

### 1. Alloy Cross-Reference Engine

```python
def cross_reference_alloy(
    alloy: str,
    source_standard: str,
    target_standard: str
) -> AlloyCrossReference:
    """
    Cross-reference alloy designations across international standards.

    Supported standards:
    - AA (Aluminum Association - USA)
    - AISI (American Iron and Steel Institute)
    - ASTM (American Society for Testing and Materials)
    - EN (European Norm)
    - DIN (German Industrial Standard)
    - JIS (Japanese Industrial Standards)
    - GB (Chinese National Standard)
    - BS (British Standard)

    Example:
        cross_reference_alloy("6061-T6", "AA", "EN")
        → AlloyCrossReference(
            target_designation="EN AW-6061-T6",
            equivalence="exact",
            composition_comparison={...},
            notes="Identical alloy, only designation differs"
        )
    """
```

### 2. Galvanic Compatibility Matrix

```python
def check_galvanic_compatibility(
    material_a: str,
    material_b: str,
    environment: str  # "seawater", "freshwater", "industrial", "atmosphere"
) -> MaterialCompatibility:
    """
    Assess galvanic corrosion risk between two materials.

    Uses standard galvanic series with environment adjustment factors:
    - Seawater: Full corrosion risk
    - Freshwater: ~30% of seawater risk
    - Industrial: ~50% of seawater risk
    - Atmosphere: ~20% of seawater risk

    Example:
        check_galvanic_compatibility(
            "316_stainless_passive",
            "aluminum_6061",
            "seawater"
        )
        → MaterialCompatibility(
            compatible=False,
            issue="HIGH galvanic risk - aluminum_6061 will corrode rapidly",
            voltage_difference_mv=800,
            mitigation_options=[
                "Isolate with non-conductive material",
                "Use sacrificial zinc anode",
                "Consider material substitution"
            ]
        )
    """
```

### 3. Material Selection Engine

```python
def recommend_material(
    application: str,
    requirements: Dict,
    constraints: Dict
) -> List[MaterialRecommendation]:
    """
    Recommend optimal materials for an application.

    Requirements:
    - temperature_c: Maximum operating temperature
    - strength_mpa: Minimum tensile strength
    - corrosion_resistance: "poor"/"fair"/"good"/"excellent"/"inert"
    - fatigue_cycles: Required fatigue life
    - weight_priority: How important is low weight (0-1)

    Constraints:
    - max_cost_factor: Maximum cost relative to carbon steel
    - must_be_weldable: Boolean
    - must_be_machinable: Boolean
    - magnetic: Boolean requirement

    Example:
        recommend_material(
            application="Exhaust manifold studs",
            requirements={
                "temperature_c": 800,
                "corrosion_resistance": "excellent",
                "strength_mpa": 600
            },
            constraints={"max_cost_factor": 25}
        )
        → [
            MaterialRecommendation(
                material="Inconel 718",
                suitability_score=0.95,
                cost_factor=20,
                notes="Industry standard for exhaust fasteners"
            ),
            MaterialRecommendation(
                material="A286 Stainless",
                suitability_score=0.85,
                cost_factor=12,
                notes="Budget alternative, lower temp capability"
            )
        ]
    """
```

### 4. Polymer Selection Engine

```python
def select_polymer(requirements: Dict) -> List[PolymerRecommendation]:
    """
    Select polymers based on application requirements.

    Requirements:
    - temperature_max_c: Maximum continuous temperature
    - chemical_exposure: List of chemicals part will contact
    - outdoor_uv: Whether part will be exposed to UV
    - sterilizable: Required sterilization method
    - mechanical_load: "light"/"medium"/"heavy"

    Example:
        select_polymer({
            "temperature_max_c": 200,
            "chemical_exposure": ["hydraulic_oil", "fuel"],
            "sterilizable": "autoclave"
        })
        → [
            PolymerRecommendation(
                material="PEEK",
                suitability=0.95,
                temp_range=(-60, 260),
                notes="Excellent for high-temp oil exposure"
            ),
            PolymerRecommendation(
                material="Viton (FKM)",
                suitability=0.88,
                temp_range=(-20, 200),
                notes="Good for seals and gaskets in oil/fuel"
            )
        ]
    """
```

### 5. Coating Compatibility Checker

```python
def check_coating_compatibility(
    substrate: str,
    coating: str,
    environment: str
) -> CoatingCompatibility:
    """
    Verify coating compatibility with substrate and environment.

    Common issues caught:
    - Zinc plating on high-strength steel (hydrogen embrittlement)
    - Anodizing on welded aluminum (poor coverage at welds)
    - Chrome plating in marine environment (pitting corrosion)

    Example:
        check_coating_compatibility(
            substrate="ASTM A574 Grade 8 bolt",
            coating="Zinc electroplate",
            environment="high_stress"
        )
        → CoatingCompatibility(
            compatible=False,
            risk="HYDROGEN EMBRITTLEMENT",
            explanation="Zinc plating on Grade 8+ bolts risks hydrogen...",
            alternatives=["Geomet 500", "Zinc flake", "Mechanical galvanizing"]
        )
    """
```

---

## Data Structures

### MaterialProperties
```python
@dataclass
class MaterialProperties:
    # Identity
    designation: str          # "6061-T6", "316L", "PEEK"
    family: MaterialFamily    # FERROUS, ALUMINUM, TITANIUM, etc.
    standard: str             # "AA", "AISI", "ASTM"

    # Mechanical
    tensile_strength_mpa: float
    yield_strength_mpa: float
    elongation_percent: float
    hardness: str             # "HRC 30-35" or "HRB 85"
    modulus_gpa: float        # Young's modulus

    # Thermal
    melting_point_c: Optional[float]
    max_service_temp_c: float
    thermal_conductivity_w_mk: float
    thermal_expansion_um_mk: float

    # Corrosion & Environment
    corrosion_resistance: CorrosionResistance
    galvanic_series_position: float  # -1.0 to +1.0

    # Additional
    density_g_cm3: float
    electrical_conductivity_percent_iacs: Optional[float]
    magnetic: bool
    weldable: bool
    machinability_rating: Optional[int]
```

### GalvanicPair
```python
@dataclass
class GalvanicPair:
    material_a: str
    material_b: str
    voltage_difference_mv: float
    anode: str              # Will corrode
    cathode: str            # Will be protected
    corrosion_rate_factor: float

    @property
    def is_problematic(self) -> bool:
        """Voltage difference > 250mV is generally problematic"""
        return self.voltage_difference_mv > 250
```

### CoatingSpec
```python
@dataclass
class CoatingSpec:
    name: str                    # "Geomet 500", "Type III Anodize"
    type: CoatingType           # CONVERSION, PLATING, ANODIZE, PAINT
    thickness_um: Tuple[float, float]  # Range
    corrosion_hours_astm_b117: int     # Salt spray hours
    temperature_max_c: float
    compatible_substrates: List[str]
    incompatible_substrates: List[str]
    hydrogen_embrittlement_risk: bool
    friction_coefficient: float
```

---

## Integration with Other Agents

```
ALCHEMIST INTEGRATION MAP

Agent_11 (MARINER) ←→ Agent_18 (ALCHEMIST)
    Query: "What material for saltwater exposure?"
    Response: Material recommendation with marine corrosion data

Agent_14 (HEALER) ←→ Agent_18 (ALCHEMIST)
    Query: "Is this material biocompatible?"
    Response: ISO 10993 compliance data, implant-grade verification

Agent_17 (ARBITER) ←→ Agent_18 (ALCHEMIST)
    Query: "Does this meet ASTM A574?"
    Response: Material composition verification against standard

Agent_20 (DETECTIVE) ←→ Agent_18 (ALCHEMIST)
    Query: "Why did this material fail?"
    Response: Failure mode analysis (fatigue, corrosion, embrittlement)

Agent_2 (ORACLE) ←→ Agent_18 (ALCHEMIST)
    Query: "Are these materials compatible?"
    Response: Galvanic compatibility + mechanical compatibility
```

---

## Showcase Use Cases

### Use Case 1: "Will 304 Work in Marine?"

**User Query:**
> "Can I use 304 stainless in my boat, or do I need 316?"

**ALCHEMIST Response:**
```
MARINE STAINLESS ASSESSMENT

304 Stainless in Marine Environment:
├─ Corrosion Risk: MODERATE-HIGH
├─ Issue: Chloride pitting in salt spray zones
├─ Failure Mode: Crevice corrosion under washers/gaskets
└─ Verdict: NOT RECOMMENDED for continuous saltwater exposure

316 Stainless (recommended):
├─ Corrosion Risk: LOW
├─ Molybdenum Content: 2-3% (provides chloride resistance)
├─ Cost Premium: ~20-30% over 304
└─ Verdict: RECOMMENDED for marine applications

316L (even better):
├─ Low carbon variant prevents sensitization during welding
└─ Recommended for welded marine structures

For below-waterline hardware: Consider duplex stainless (2205)
or silicon bronze for traditional appearance.
```

### Use Case 2: "What's the European Equivalent?"

**User Query:**
> "I need 6061-T6 aluminum but my European supplier uses EN standards."

**ALCHEMIST Response:**
```
ALLOY CROSS-REFERENCE

Source: 6061-T6 (AA - Aluminum Association, USA)

Equivalents:
├─ EN AW-6061-T6 (European Norm) — EXACT MATCH
├─ A6061-T6 (JIS - Japan) — EXACT MATCH
├─ AlMg1SiCu (DIN - Germany, old designation)
└─ 6061-T6 (GB/T - China) — EXACT MATCH

Composition Verification:
├─ Si: 0.4-0.8% ✓
├─ Mg: 0.8-1.2% ✓
├─ Cu: 0.15-0.4% ✓
└─ All compositions identical across standards

Procurement Note: Specify "EN AW-6061-T6" for European suppliers.
Material certificate should reference EN 573-3 (composition)
and EN 755-2 (mechanical properties).
```

### Use Case 3: "High-Temperature Polymer"

**User Query:**
> "I need a plastic that can handle 150°C continuous with oil exposure."

**ALCHEMIST Response:**
```
POLYMER SELECTION FOR HIGH-TEMP OIL EXPOSURE

TOP RECOMMENDATIONS:

1. PEEK (Polyether Ether Ketone)
   ├─ Max Continuous Temp: 250°C ✓✓
   ├─ Oil Resistance: Excellent ✓✓
   ├─ Strength: 100 MPa (very high for polymer)
   ├─ Cost Factor: 15x (expensive)
   └─ Verdict: BEST CHOICE if budget allows

2. PPS (Polyphenylene Sulfide)
   ├─ Max Continuous Temp: 200°C ✓
   ├─ Oil Resistance: Excellent ✓✓
   ├─ Strength: 75 MPa
   ├─ Cost Factor: 8x
   └─ Verdict: GOOD VALUE option

3. PTFE (Teflon)
   ├─ Max Continuous Temp: 260°C ✓✓
   ├─ Oil Resistance: Excellent ✓✓
   ├─ Strength: 25 MPa (LOW - creeps under load)
   ├─ Cost Factor: 8x
   └─ Verdict: SEALS ONLY - not for structural use

NOT RECOMMENDED:
- Nylon (PA66): Max 80-100°C, absorbs moisture
- Acetal (POM): Degrades in hot oil above 100°C
- UHMWPE: Max 80°C continuous
```

---

## Implementation Structure

```
agents/alchemist/
├── __init__.py              # Package initialization
├── alchemist_agent.py       # Main agent class
├── alloys/
│   ├── __init__.py
│   ├── database.py          # Alloy property database
│   ├── cross_reference.py   # Standards cross-reference engine
│   └── steels.py            # Steel-specific data
├── polymers/
│   ├── __init__.py
│   ├── database.py          # Polymer property database
│   └── selector.py          # Polymer selection engine
├── compatibility/
│   ├── __init__.py
│   ├── galvanic.py          # Galvanic series and calculations
│   └── thermal.py           # Thermal compatibility
├── coatings/
│   ├── __init__.py
│   ├── database.py          # Coating specifications
│   └── selector.py          # Coating selection engine
└── composites/
    ├── __init__.py
    └── database.py          # Composite material data
```

---

## Galvanic Series Reference

```
GALVANIC SERIES (Seawater Reference)
More negative = More anodic (WILL CORRODE)
More positive = More cathodic (protected)

Material                    Position (V vs SCE)
─────────────────────────────────────────────
Magnesium                   -1.60 ← Most anodic
Zinc                        -1.10
Aluminum 5052               -0.85
Aluminum 6061               -0.75
Cadmium                     -0.70
Carbon Steel                -0.60
Cast Iron                   -0.55
304 SS (active)             -0.50
Lead                        -0.45
Tin                         -0.40
Nickel (active)             -0.35
Brass                       -0.30
Copper                      -0.20
Bronze                      -0.18
316 SS (active)             -0.05
─────────────────────────────────────────────
Nickel (passive)             0.00 ← Reference
316 SS (passive)            +0.05
304 SS (passive)            +0.08
Titanium                    +0.10
Silver                      +0.15
Graphite                    +0.25
Gold                        +0.35
Platinum                    +0.40 ← Most cathodic
```

**Rule of Thumb:**
- < 100mV difference: Generally safe
- 100-250mV difference: Use isolation
- > 250mV difference: Significant corrosion risk
- > 400mV difference: Rapid failure likely

---

## Success Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Materials Indexed | 100,000+ | Alloys, polymers, composites, coatings |
| Cross-Reference Accuracy | 99.5% | Correct equivalent identification |
| Galvanic Calculations | 99.9% | Correct corrosion risk assessment |
| Query Response Time | < 50ms | Material lookup and compatibility check |
| User Satisfaction | > 95% | "Did this help your material decision?" |

---

## Future Enhancements

1. **Material Certificate Parser** - Extract properties from mill certificates
2. **Failure Mode Predictor** - "This material will likely fail by..."
3. **Cost Optimizer** - Find cheapest material meeting all requirements
4. **Sustainability Scorer** - Environmental impact of material choices
5. **3D Printing Materials** - Additive manufacturing material selection

---

*"The Alchemist speaks truth: steel rusts, aluminum corrodes, titanium endures. Know your materials, and your parts shall never fail unexpectedly."*
