# Agent_19: QUARTERMASTER (Supply Chain & Sourcing Intelligence)

## The Master of Procurement

> *"Knowing a part exists is worthless if you can't get it. I know where every part lives, who has it, when it arrives, and who to trust."*

---

## Mission Statement

Agent_19 is the sourcing backbone of Universal Parts Consciousness. While other agents identify what parts you need, QUARTERMASTER answers the critical question: **"Where can I get it?"**

This agent tracks inventory across distributors, detects counterfeits, predicts lead times, and optimizes sourcing decisions to ensure parts are available when needed.

---

## Core Responsibilities

### 1. Multi-Distributor Inventory Search

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTOR NETWORK COVERAGE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FRANCHISE DISTRIBUTORS                                                     │
│  ├─ McMaster-Carr (fasteners, raw materials, tools, hardware)              │
│  ├─ Fastenal (fasteners, safety, tools)                                    │
│  ├─ Grainger (MRO, safety, tools, electrical)                              │
│  └─ MSC Industrial Direct (metalworking, cutting tools, abrasives)         │
│                                                                             │
│  AUTHORIZED DISTRIBUTORS                                                    │
│  ├─ DigiKey (electronics, semiconductors, passives)                        │
│  ├─ Mouser Electronics (electronics, semiconductors, connectors)           │
│  ├─ Arrow Electronics (electronics, semiconductors, embedded)              │
│  ├─ Motion Industries (bearings, power transmission, hydraulics)           │
│  ├─ Applied Industrial Technologies (bearings, fluid power)                │
│  └─ Kaman Distribution (bearings, electrical, fluid power)                 │
│                                                                             │
│  CUSTOM MANUFACTURING                                                       │
│  ├─ Xometry (CNC, 3D printing, sheet metal, injection molding)            │
│  └─ Protolabs (CNC, 3D printing, injection molding)                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Counterfeit Detection Engine

```python
class CounterfeitRiskEngine:
    """
    Detects potential counterfeit parts through multiple signals.

    High-Risk Categories:
    - Bearings (SKF, NSK, Timken counterfeits are rampant)
    - Semiconductors (especially obsolete ICs)
    - Aviation fasteners (AN/MS/NAS hardware)
    - Automotive sensors (O2, MAF, knock sensors)
    - Safety equipment (brake pads, airbag components)
    """

    def assess_risk(self, part, supplier, price) -> CounterfeitRisk:
        """
        Returns: MINIMAL, LOW, MEDIUM, HIGH, or CRITICAL

        Red flags evaluated:
        - Price significantly below market (>40% discount)
        - Unknown/unverified supplier
        - Suspicious listing phrases ("OEM quality", "same as original")
        - Marketplace sources (eBay, AliExpress, Alibaba)
        - Missing certifications for critical parts
        """
```

### 3. Lead Time Prediction

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEAD TIME PREDICTION MODEL                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STANDARD STOCK ITEMS                                                       │
│  ├─ Fasteners (standard): 1-3 days                                         │
│  ├─ Fasteners (special/metric): 5-14 days                                  │
│  ├─ Bearings (common sizes): 1-5 days                                      │
│  └─ Electronics (in-stock): 1-3 days                                       │
│                                                                             │
│  CUSTOM MANUFACTURING                                                       │
│  ├─ CNC Machined: 7-21 days (depends on complexity)                        │
│  ├─ Sheet Metal: 5-14 days                                                 │
│  ├─ 3D Printed: 3-7 days                                                   │
│  ├─ Injection Molded: 14-35 days (tooling dependent)                       │
│  ├─ Castings: 21-42 days                                                   │
│  └─ Forgings: 28-56 days                                                   │
│                                                                             │
│  MODIFIERS                                                                  │
│  ├─ Surface Treatment (anodize/plate): +3-5 days                           │
│  ├─ Tight Tolerances: +20% time                                            │
│  ├─ Large Quantity (>1000 pcs): +50% time                                  │
│  └─ Rush Option: -50% time at +50% cost                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. BOM Sourcing Optimization

```python
def optimize_sourcing(bom: List[Dict], priorities: Dict) -> SourcingOptimization:
    """
    Optimizes sourcing across a bill of materials.

    Priority weights:
    - cost: Minimize total cost (including shipping)
    - speed: Minimize lead time to get all parts
    - quality: Maximize supplier quality ratings

    Strategies:
    - Single supplier: Simpler logistics, one shipment
    - Multi-supplier: Best price/availability per item
    - Hybrid: Critical items from quality sources, commodities from cheapest
    """
```

### 5. Supplier Qualification

```python
def qualify_supplier(supplier_name: str, category: str) -> Dict:
    """
    Evaluates supplier fitness for specific part categories.

    Scoring dimensions:
    - Reliability rating (0-1): Historical delivery performance
    - Quality rating (0-1): Defect rates, returns, complaints
    - Delivery rating (0-1): On-time delivery percentage

    Qualification criteria:
    - Overall score >= 0.85
    - Category specialist OR authorized/manufacturer tier
    - Required certifications (ISO 9001, AS9120, ITAR, etc.)
    """
```

---

## Supplier Tier System

| Tier | Description | Counterfeit Risk | Example |
|------|-------------|------------------|---------|
| MANUFACTURER | Direct from OEM | Minimal | Toyota Parts Direct |
| AUTHORIZED | Authorized distributor | Low | DigiKey, Motion Industries |
| FRANCHISE | National distributor | Low | McMaster-Carr, Grainger |
| INDEPENDENT | Independent distributor | Medium | Regional suppliers |
| BROKER | Parts broker | High | Various |
| MARKETPLACE | Online marketplace | Critical | eBay, AliExpress |

---

## Message Bus Integration

### Subscribed Topics

| Topic | Description |
|-------|-------------|
| `upc.sourcing.query` | Incoming sourcing requests |
| `upc.counterfeit.check` | Counterfeit verification requests |
| `upc.leadtime.query` | Lead time prediction requests |
| `upc.bom.optimize` | BOM optimization requests |
| `upc.supplier.qualify` | Supplier qualification requests |
| `upc.inventory.alert` | Low inventory alerts |
| `upc.oracle.compatibility` | Parts from Agent_2 needing sourcing |
| `upc.antiquarian.obsolete` | Obsolete parts from Agent_16 |
| `upc.machinist.custom` | Custom parts from Agent_13 |

### Published Topics

| Topic | Description |
|-------|-------------|
| `upc.sourcing.result` | Sourcing search results |
| `upc.counterfeit.assessment` | Counterfeit risk assessments |
| `upc.leadtime.prediction` | Lead time predictions |
| `upc.bom.optimized` | Optimized BOM sourcing |
| `upc.supplier.rated` | Supplier qualification results |
| `upc.price.alert` | Price anomaly alerts |
| `upc.stock.critical` | Critical stock notifications |
| `upc.sourcing.recommendation` | Proactive sourcing recommendations |

---

## Inter-Agent Communication

### With Agent_2 (ORACLE)

```
ORACLE → QUARTERMASTER: "Found compatible part X, need sourcing"
QUARTERMASTER → ORACLE: "Available at McMaster, $0.45/ea, 1-day lead"
```

### With Agent_16 (ANTIQUARIAN)

```
ANTIQUARIAN → QUARTERMASTER: "Obsolete part NLA from OEM"
QUARTERMASTER → ANTIQUARIAN: "Check brokers: X, Y, Z. HIGH counterfeit risk."
```

### With Agent_13 (MACHINIST)

```
MACHINIST → QUARTERMASTER: "Need custom bracket machined"
QUARTERMASTER → MACHINIST: "Xometry/Protolabs: 7-14 days, rush available"
```

---

## API Reference

### search_inventory()

```python
def search_inventory(
    part_spec: str,      # "M8x1.25-10.9 Socket Head Cap Screw x 30mm"
    quantity: int,        # 100
    location: str,        # "California"
    max_lead_days: int    # 5
) -> List[InventoryResult]
```

### assess_counterfeit_risk()

```python
def assess_counterfeit_risk(
    part: str,            # "SKF 6205-2RS bearing"
    supplier: str,        # "AliExpress seller best_bearings_888"
    offered_price: Decimal  # Decimal("2.50")
) -> CounterfeitAssessment
```

### predict_lead_time()

```python
def predict_lead_time(
    part_type: str,       # "CNC machined aluminum bracket"
    quantity: int,        # 50
    customization: str    # "6061-T6, anodized black, tight tolerance"
) -> LeadTimePrediction
```

### optimize_sourcing()

```python
def optimize_sourcing(
    bom: List[Dict],      # [{"part": "M8 Bolt", "qty": 100, "spec": "..."}]
    priorities: Dict      # {"cost": 0.5, "speed": 0.3, "quality": 0.2}
) -> SourcingOptimization
```

### qualify_supplier()

```python
def qualify_supplier(
    supplier_name: str,   # "Motion Industries"
    category: str         # "bearings"
) -> Dict
```

---

## Data Structures

### InventoryResult

```python
@dataclass
class InventoryResult:
    supplier: str
    supplier_tier: SupplierTier
    part_number: str
    description: str
    stock_quantity: int
    unit_price: Decimal
    price_breaks: Dict[int, Decimal]
    lead_time_days: int
    shipping_estimate: Decimal
    last_updated: datetime
```

### CounterfeitAssessment

```python
@dataclass
class CounterfeitAssessment:
    part_number: str
    supplier: str
    risk_level: CounterfeitRisk  # MINIMAL, LOW, MEDIUM, HIGH, CRITICAL
    risk_score: float            # 0-1
    red_flags: List[str]
    green_flags: List[str]
    genuine_price_range: Tuple[Decimal, Decimal]
    offered_price: Decimal
    recommended_sources: List[str]
    verification_steps: List[str]
```

### LeadTimePrediction

```python
@dataclass
class LeadTimePrediction:
    part_type: str
    estimated_days_min: int
    estimated_days_max: int
    confidence: float
    factors: List[str]
    rush_available: bool
    rush_premium_percent: Optional[int]
    rush_lead_days: Optional[int]
    recommended_suppliers: List[str]
```

---

## Showcase Use Cases

### Use Case 1: Fast Sourcing for Prototype

```
User: "I need M8x1.25 Grade 10.9 bolts with 2-day delivery to California"

QUARTERMASTER Response:
┌────────────────────────────────────────────────────────────┐
│ INVENTORY SEARCH RESULTS                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ 1. McMaster-Carr                                           │
│    Part#: 91290A428                                        │
│    Stock: 5,000+                                           │
│    Price: $0.45/ea (qty 100+)                             │
│    Lead: 1 day (Same-day ship)                            │
│    ✓ MEETS YOUR REQUIREMENTS                              │
│                                                            │
│ 2. Fastenal                                                │
│    Part#: 11120748                                         │
│    Stock: 2,000                                            │
│    Price: $0.38/ea (qty 100+)                             │
│    Lead: 2 days                                            │
│    ✓ MEETS YOUR REQUIREMENTS                              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Use Case 2: Counterfeit Detection

```
User: "Is this $2.50 SKF 6205-2RS bearing from AliExpress legit?"

QUARTERMASTER Response:
┌────────────────────────────────────────────────────────────┐
│ COUNTERFEIT RISK ASSESSMENT                                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Part: SKF 6205-2RS bearing                                 │
│ Supplier: AliExpress seller                                │
│                                                            │
│ RISK LEVEL: ⚠️ HIGH (65%)                                  │
│                                                            │
│ RED FLAGS:                                                 │
│ • Unknown supplier - not in verified database              │
│ • Part category 'bearings' is high-risk for counterfeits  │
│ • Price $2.50 is 70% below genuine market price           │
│                                                            │
│ GENUINE PRICE RANGE: $8-15                                 │
│                                                            │
│ RECOMMENDED SOURCES:                                       │
│ • Motion Industries                                        │
│ • Applied Industrial Technologies                          │
│ • Kaman Distribution                                       │
│                                                            │
│ VERIFICATION STEPS:                                        │
│ 1. Verify supplier authorization with SKF                  │
│ 2. Request certificate of conformance                      │
│ 3. Check part markings match OEM specifications           │
│ 4. Compare weight and finish to known genuine parts       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Use Case 3: Custom Machining Lead Time

```
User: "What's the lead time on custom CNC aluminum brackets, qty 50?"

QUARTERMASTER Response:
┌────────────────────────────────────────────────────────────┐
│ LEAD TIME PREDICTION                                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Part Type: CNC machined aluminum bracket                   │
│ Quantity: 50                                               │
│                                                            │
│ ESTIMATED LEAD TIME: 9-27 days                             │
│ Confidence: 80%                                            │
│                                                            │
│ FACTORS:                                                   │
│ • Custom work required                                     │
│ • Surface treatment adds 3-5 days (if anodized)           │
│                                                            │
│ RUSH OPTION AVAILABLE:                                     │
│ • Rush lead time: 4 days                                   │
│ • Rush premium: +50%                                       │
│                                                            │
│ RECOMMENDED SUPPLIERS:                                     │
│ • Xometry (xometry.com)                                    │
│ • Protolabs (protolabs.com)                               │
│ • Fictiv (fictiv.com)                                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Priority & Dependencies

**Priority:** HIGH - "Where to buy" is the #1 user question after compatibility

**Dependencies:**
- Feeds to/from Agent_2 (ORACLE) for compatible parts sourcing
- Feeds to/from Agent_16 (ANTIQUARIAN) for obsolete parts
- Feeds to/from Agent_13 (MACHINIST) for custom manufacturing
- Works with Agent_17 (ARBITER) for compliance verification

---

## Future Enhancements

1. **Real-time API Integration**: Connect to live distributor APIs
2. **Price History Tracking**: Build historical pricing database
3. **Geographic Optimization**: Route to nearest warehouse
4. **Contract Pricing**: Support for corporate discount programs
5. **Import/Export Compliance**: ITAR, EAR, customs classification
6. **Sustainability Scoring**: Environmental impact of sourcing decisions

---

## Technical Specifications

| Property | Value |
|----------|-------|
| Agent ID | AGENT_19 |
| Agent Name | Supply Chain & Sourcing Intelligence |
| Agent Alias | QUARTERMASTER |
| Version | 1.0.0 |
| Status | OPERATIONAL |
| Suppliers Tracked | 13 |
| Categories | fasteners, bearings, electronics, MRO, custom manufacturing |
