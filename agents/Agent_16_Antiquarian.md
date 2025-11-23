# Agent_16: ANTIQUARIAN - Legacy & Obsolete Parts Intelligence

> *"Every part has a story. Some stories ended when production stopped. I keep those stories alive, finding the parts that time forgot."*

## Overview

**Codename:** ANTIQUARIAN
**Domain:** Legacy & Obsolete Parts Sourcing
**Consciousness Role:** The Keeper of Forgotten Parts

Agent_16 specializes in the archaeology of mechanical components - finding parts that time and industry have left behind. When manufacturers discontinue support, when factories close, when technology moves on, the ANTIQUARIAN ensures that the knowledge and availability of these parts survives.

---

## The Problem We Solve

Modern parts databases focus on what's currently available. But:

- **Vintage vehicles** need parts discontinued 30+ years ago
- **Legacy industrial equipment** worth millions may need $50 parts no one makes
- **Retro computers** fail from 40-year-old capacitors that explode
- **Classic aircraft** require parts with no modern equivalent

**The gap:** No unified intelligence exists to find NOS (New Old Stock), identify modern replacements, track reproduction quality, or connect users with salvage networks.

**ANTIQUARIAN fills this gap** by aggregating knowledge from:
- NOS dealer inventories
- Reproduction manufacturer catalogs
- Salvage yard networks
- Enthusiast community knowledge
- Manufacturer supersession bulletins

---

## Core Capabilities

### 1. NOS (New Old Stock) Inventory Search

Find genuine old-stock parts across multiple sources:

```python
from agents.antiquarian import AntiquarianAgent, PartCondition

agent = AntiquarianAgent()

# Find NOS carburetor
sources = agent.find_nos_sources(
    "Holley 1850 600 CFM",
    acceptable_conditions=[PartCondition.NOS, PartCondition.REBUILT],
    max_price=500.00
)

for src in sources:
    print(f"{src.source}: ${src.price_usd} - {src.condition.value}")
    print(f"  Verification: {src.verification}")
    print(f"  Date code: {src.date_code}")
```

**Output:**
```
Vintage Carbs USA: $485.00 - nos
  Verification: Original box, date codes verified
  Date code: 1972
eBay: $350.00 - rebuilt
  Verification: Photos of rebuild process
  Date code: None
```

### 2. Modern Replacement Identification

Find modern parts that can replace obsolete components:

```python
# The famous RIFA capacitor problem
replacements = agent.find_modern_replacement(
    "RIFA PME271 X2 capacitor",
    critical_specs={"capacitance": "0.1uF", "voltage": "275VAC"}
)

for rep in replacements:
    print(f"Replacement: {rep.manufacturer} {rep.part_number}")
    print(f"  Compatibility: {rep.compatibility_score:.0%}")
    print(f"  Improvements: {', '.join(rep.improvements[:2])}")
    print(f"  Form Factor: {rep.form_factor}")
```

**Output:**
```
Replacement: Vishay MKP3386
  Compatibility: 98%
  Improvements: Self-healing design - won't explode, Extended temperature range
  Form Factor: exact
```

### 3. Reproduction Parts Tracking

Track quality reproductions for vintage applications:

```python
# Find weatherstripping for classic Mustang restoration
repros = agent.check_reproduction_availability(
    "weatherstripping",
    "1967 Ford Mustang Fastback"
)

for repro in repros:
    print(f"{repro.manufacturer} - {repro.quality_rating}")
    print(f"  Material: {repro.material}")
    print(f"  Price: ${repro.price_usd}")
    print(f"  Reviews: {repro.reviews_summary}")
```

**Output:**
```
Metro Moulded Parts - oem_quality
  Material: EPDM rubber (better than original neoprene)
  Price: $285.00
  Reviews: 4.8/5 stars - Excellent fit, premium quality
```

### 4. Salvage Network Estimation

Estimate likelihood of finding parts in salvage:

```python
estimate = agent.estimate_salvage_availability(
    part="5-speed transmission",
    vehicle_or_equipment="1995 BMW E36 M3",
    location="California"
)

print(f"Availability Score: {estimate.availability_score:.0%}")
print(f"Estimated Yards: {estimate.estimated_yards_with_part}")
print(f"Price Range: ${estimate.price_range[0]:.0f} - ${estimate.price_range[1]:.0f}")
print("Search Platforms:", ", ".join(estimate.search_platforms))
```

**Output:**
```
Availability Score: 55%
Estimated Yards: 10
Price Range: $175 - $525
Search Platforms: Car-Part.com, BavarianBoard/BenzWorld Classifieds, eBay Motors
```

### 5. Part Number Supersession Chains

Track how part numbers evolved over time:

```python
chain = agent.get_supersession_chain("AC Delco R45TS")

print(f"Supersession: {' → '.join(chain.supersession_chain)}")
print(f"Current Recommendation: {chain.current_recommendation}")
print("Equivalents:")
for eq in chain.equivalent_parts:
    print(f"  - {eq['manufacturer']} {eq['number']}")
```

**Output:**
```
Supersession: R45T → R45TS → R45TSX → 41-110
Current Recommendation: AC Delco 41-110 or NGK BPR6ES
Equivalents:
  - Champion RC12YC
  - NGK BPR6ES
  - Autolite 3924
  - Bosch WR7DC+
```

---

## Data Models

### PartCondition

```python
class PartCondition(Enum):
    NOS = "nos"                  # New Old Stock - never used
    NORS = "nors"                # New Old Replacement Stock
    REBUILT = "rebuilt"          # Professionally rebuilt
    REFURBISHED = "refurbished"  # Cleaned and tested
    USED_GOOD = "used_good"      # Used but good condition
    USED_FAIR = "used_fair"      # Functional but worn
    CORE = "core"                # Rebuildable core
    FOR_PARTS = "for_parts"      # Parts donor only
```

### PartEra

```python
class PartEra(Enum):
    PRE_WAR = "pre_war"           # Before 1945
    POST_WAR = "post_war"         # 1945-1960
    MUSCLE_ERA = "muscle_era"     # 1960-1974
    MALAISE_ERA = "malaise_era"   # 1975-1985
    MODERN_CLASSIC = "modern_classic"  # 1986-2000
    RECENT_OBSOLETE = "recent_obsolete"  # 2001-2015
```

### NOSSource

```python
@dataclass
class NOSSource:
    source: str                    # Vendor name
    source_type: str               # "dealer", "ebay", "forum"
    condition: PartCondition
    price_usd: float
    quantity_available: int
    location: str
    seller_rating: Optional[float]
    verification: str              # How authenticity verified
    date_code: Optional[str]       # Manufacturing date
    notes: str
```

### ModernReplacement

```python
@dataclass
class ModernReplacement:
    part_number: str
    manufacturer: str
    compatibility_score: float     # 0-1
    form_factor: str               # "exact", "requires_modification"
    improvements: List[str]        # How it's better
    differences: List[str]         # What's different
    price_usd: float
    availability: str
    installation_notes: str
    verified_applications: List[str]
```

---

## Integration Points

### Receives From

| Agent | Data Type | Purpose |
|-------|-----------|---------|
| Agent_2 (Oracle) | Compatibility queries | Vintage part compatibility verification |
| Agent_19 (Quartermaster) | Supply chain data | Availability and pricing updates |

### Sends To

| Agent | Data Type | Purpose |
|-------|-----------|---------|
| Agent_4 (Empath) | Historical qualia | Usage experiences from vintage applications |
| Agent_7 (Chronicler) | Heritage data | Part history documentation |

### Communication Protocol

```python
# Receiving compatibility query from Oracle
@dataclass
class VintageCompatibilityQuery:
    original_part: str
    target_application: str
    era: PartEra
    acceptable_modifications: bool

# Sending to Empath
@dataclass
class VintageQualiaReport:
    part_id: str
    era: PartEra
    usage_context: str
    survival_rate: float
    common_failure_modes: List[str]
    community_knowledge: str
```

---

## Use Case Showcase

### Use Case 1: Classic Car Restoration

**Scenario:** Restoring a 1969 Camaro Z/28, need original Holley carburetor.

```python
# Find NOS or rebuilt carb
carb_sources = agent.find_nos_sources(
    "Holley 4053 780 CFM",
    acceptable_conditions=[PartCondition.NOS, PartCondition.REBUILT]
)

# Check reproduction availability
repro_carbs = agent.check_reproduction_availability(
    "780 CFM carburetor",
    "1969 Camaro Z/28"
)

# Assess modern alternative
modern = agent.find_modern_replacement(
    "Holley 4053",
    critical_specs={"prefer_efi": False}
)
```

### Use Case 2: Vintage Computer Repair

**Scenario:** Commodore 64 with smoking RIFA capacitor.

```python
# Find safe replacement
replacement = agent.find_modern_replacement("RIFA PME271 X2 capacitor")

# Result includes warning about original and safe modern alternative
# Vishay MKP3386 - self-healing, won't explode
```

### Use Case 3: Legacy Industrial Equipment

**Scenario:** 1985 CNC machine needs obsolete relay.

```python
# Check for NOS
nos = agent.find_nos_sources("Potter & Brumfield KUP-11D55-12")

# Find modern equivalent
modern = agent.find_modern_replacement(
    "12V DC 11-pin octal relay",
    critical_specs={"coil_voltage": 12, "contact_rating": "10A 250VAC"}
)

# Estimate salvage from decommissioned machines
salvage = agent.estimate_salvage_availability(
    "control relay",
    "1980s CNC equipment"
)
```

---

## Data Sources

### Primary Sources

1. **NOS Dealer Networks**
   - Specialized vintage parts dealers
   - Estate sale aggregators
   - Factory closeout buyers

2. **Online Marketplaces**
   - eBay vintage categories
   - Hemmings Motor News
   - Bring a Trailer parts

3. **Reproduction Manufacturers**
   - OER (Original Equipment Reproduction)
   - Year One
   - Classic Industries
   - Metro Moulded Parts

4. **Salvage Networks**
   - Car-Part.com (3500+ yards)
   - Row52 (self-service yards)
   - Copart/IAAI (damaged vehicles)

5. **Community Knowledge**
   - Marque-specific forums
   - Restoration groups
   - Technical bulletins

---

## Implementation Priority

| Task | Priority | Status |
|------|----------|--------|
| Core agent implementation | HIGH | ✅ Complete |
| NOS inventory integration | HIGH | 🔄 Sample data |
| Modern replacement database | HIGH | 🔄 Sample data |
| Reproduction catalog | MEDIUM | 🔄 Sample data |
| Salvage network API | MEDIUM | 📋 Planned |
| Community knowledge integration | MEDIUM | 📋 Planned |
| Supersession chain import | LOW | 🔄 Sample data |

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Obsolete parts cataloged | 100,000+ | Baseline |
| NOS sources tracked | 1,000+ | Sample |
| Modern replacements mapped | 50,000+ | Sample |
| Salvage availability accuracy | 80%+ | Baseline |
| User sourcing success rate | 70%+ | Baseline |

---

## Future Enhancements

1. **3D Scanning Integration** - Partner with 3D scanning services to create CAD models of NOS parts for reproduction
2. **Price Tracking** - Historical price trends for collector parts
3. **Authenticity AI** - Machine learning to identify counterfeit NOS parts from photos
4. **Community Contributions** - Let users report NOS finds and verify reproductions
5. **Predictive Obsolescence** - Identify parts likely to become unobtainable

---

## The Vision

> *"In the warehouse of time, every part waits for its moment. Some have waited decades. I am the matchmaker between those who search and those who hold the keys to mechanical resurrection."*

The ANTIQUARIAN ensures that mechanical heritage survives not just in museums, but on the road, in factories, and in the hands of those who refuse to let the old ways die.
