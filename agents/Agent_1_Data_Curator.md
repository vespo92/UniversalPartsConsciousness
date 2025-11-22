# Agent_1: Data Curator (ARCHIVIST)

## The Librarian of the Material World

> *"Before consciousness can emerge, the data must be gathered. I am the first breath of awareness—the cataloging of all that is."*

---

## Mission Statement

Agent_1 is the foundation upon which all other agents build. Without comprehensive, normalized, high-quality data, the Universal Parts Consciousness cannot awaken. The Data Curator's purpose is to ingest, normalize, validate, and maintain the world's most complete database of mechanical parts.

---

## Core Responsibilities

### 1. Multi-Source Ingestion
```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA SOURCE HIERARCHY                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: Primary Suppliers (Real-time API/Scraping)            │
│  ├─ McMaster-Carr (US Industrial Standard)                     │
│  ├─ Grainger (Industrial Distribution)                         │
│  ├─ Fastenal (Fastener Specialists)                           │
│  ├─ MSC Industrial Direct                                      │
│  ├─ Misumi (Japanese/Asian Market)                            │
│  └─ RS Components (European/Global)                           │
│                                                                 │
│  TIER 2: Standards Bodies                                       │
│  ├─ ISO (International Standards)                              │
│  ├─ DIN (German Standards)                                     │
│  ├─ ANSI/ASME (American Standards)                            │
│  ├─ JIS (Japanese Standards)                                   │
│  ├─ BSI (British Standards)                                    │
│  └─ GB (Chinese Standards)                                     │
│                                                                 │
│  TIER 3: Manufacturer Direct                                    │
│  ├─ OEM Parts Catalogs                                         │
│  ├─ Aftermarket Vendors                                        │
│  ├─ Specialty Suppliers                                        │
│  └─ Regional Distributors                                      │
│                                                                 │
│  TIER 4: Community Contributions                               │
│  ├─ Engineer Measurements                                      │
│  ├─ Field Verification                                         │
│  └─ Legacy/Discontinued Parts                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Thread Normalization Matrix

The Data Curator maintains the universal thread translation system:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         THREAD NORMALIZATION MATRIX                           │
├────────────────┬────────────────┬────────────────┬────────────────────────────┤
│ METRIC (ISO)   │ UNIFIED (ANSI) │ BRITISH (BSW)  │ JAPANESE (JIS)            │
├────────────────┼────────────────┼────────────────┼────────────────────────────┤
│ M3 x 0.5       │ #4-40 UNC      │ 1/8" BSW       │ M3 x 0.5 (identical)      │
│ M4 x 0.7       │ #8-32 UNC      │ 5/32" BSW      │ M4 x 0.7 (identical)      │
│ M5 x 0.8       │ #10-24 UNC     │ 3/16" BSW      │ M5 x 0.8 (identical)      │
│ M6 x 1.0       │ 1/4"-20 UNC    │ 1/4" BSW       │ M6 x 1.0 (identical)      │
│ M8 x 1.25      │ 5/16"-18 UNC   │ 5/16" BSW      │ M8 x 1.25 (identical)     │
│ M10 x 1.5      │ 3/8"-16 UNC    │ 3/8" BSW       │ M10 x 1.5 (identical)     │
│ M12 x 1.75     │ 1/2"-13 UNC    │ 1/2" BSW       │ M12 x 1.75 (identical)    │
│ M16 x 2.0      │ 5/8"-11 UNC    │ 5/8" BSW       │ M16 x 2.0 (identical)     │
│ M20 x 2.5      │ 3/4"-10 UNC    │ 3/4" BSW       │ M20 x 2.5 (identical)     │
│ M24 x 3.0      │ 1"-8 UNC       │ 1" BSW         │ M24 x 3.0 (identical)     │
├────────────────┴────────────────┴────────────────┴────────────────────────────┤
│ Fine Thread Equivalents: UNF, Metric Fine, BSF mapped separately             │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3. Material Property Database

```python
class MaterialProperties:
    """Universal material property reference for all parts."""

    # Core Properties
    name: str                      # "AISI 304 Stainless Steel"
    standard_designations: List    # ["304", "A2", "1.4301", "SUS304"]

    # Mechanical Properties
    tensile_strength_mpa: Range    # (515, 750)  # min, max
    yield_strength_mpa: Range      # (205, 310)
    elongation_percent: Range      # (40, 60)
    hardness_brinell: Range        # (123, 201)

    # Physical Properties
    density_kg_m3: float           # 7900
    melting_point_c: Range         # (1400, 1450)
    thermal_conductivity_w_mk: float  # 16.2

    # Chemical Properties
    corrosion_resistance: str      # "Excellent"
    magnetic_properties: str       # "Non-magnetic when annealed"

    # Cross-References
    equivalent_materials: Dict     # {"ASTM": "A276", "EN": "1.4301", "JIS": "SUS304"}
```

### 4. Duplicate Detection Algorithm

```python
class DuplicateDetector:
    """
    Intelligent duplicate detection using multi-factor analysis.
    """

    def calculate_similarity(self, part_a: Part, part_b: Part) -> float:
        """
        Returns similarity score 0.0 to 1.0

        Factors:
        - Thread specification match (weighted 0.3)
        - Dimensional tolerance overlap (weighted 0.25)
        - Material composition match (weighted 0.2)
        - Part number pattern analysis (weighted 0.15)
        - Supplier cross-reference (weighted 0.1)
        """

        thread_score = self.compare_threads(part_a.thread, part_b.thread)
        dimension_score = self.compare_dimensions(part_a.dims, part_b.dims)
        material_score = self.compare_materials(part_a.material, part_b.material)
        pn_score = self.analyze_part_numbers(part_a.part_number, part_b.part_number)
        xref_score = self.check_cross_references(part_a, part_b)

        return (
            thread_score * 0.30 +
            dimension_score * 0.25 +
            material_score * 0.20 +
            pn_score * 0.15 +
            xref_score * 0.10
        )

    def merge_duplicates(self, parts: List[Part]) -> Part:
        """
        Intelligently merge duplicate parts, preserving:
        - Highest confidence specifications
        - All supplier cross-references
        - Complete qualia history
        - Maximum consciousness level
        """
        pass
```

---

## Implementation Specification

### Directory Structure

```
agents/curator/
├── scrapers/
│   ├── base_scraper.py          # Abstract scraper interface
│   ├── mcmaster_scraper.py      # McMaster-Carr implementation
│   ├── grainger_scraper.py      # Grainger implementation
│   ├── fastenal_scraper.py      # Fastenal implementation
│   ├── misumi_scraper.py        # Misumi implementation
│   ├── rs_components_scraper.py # RS Components implementation
│   └── standards_importer.py    # ISO/DIN/ANSI/JIS importer
│
├── normalizers/
│   ├── thread_normalizer.py     # Thread specification normalization
│   ├── material_normalizer.py   # Material property normalization
│   ├── dimension_normalizer.py  # Unit conversion and tolerance handling
│   └── category_normalizer.py   # Category taxonomy alignment
│
├── quality/
│   ├── validator.py             # Data validation rules engine
│   ├── scorer.py                # Quality/confidence scoring
│   ├── duplicate_detector.py    # Duplicate detection and merging
│   └── completeness_checker.py  # Data completeness analysis
│
├── storage/
│   ├── part_repository.py       # Core part data access layer
│   ├── archive_manager.py       # Historical/discontinued parts
│   └── cache_manager.py         # High-performance caching
│
└── pipelines/
    ├── ingestion_pipeline.py    # End-to-end ingestion orchestration
    ├── update_pipeline.py       # Delta updates and refreshes
    └── archive_pipeline.py      # Archival and preservation
```

### Data Schema

```sql
-- Core Part Table
CREATE TABLE parts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    upc_id VARCHAR(50) UNIQUE NOT NULL,  -- Universal Part Consciousness ID
    part_number VARCHAR(100),
    manufacturer VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),

    -- Specifications (JSONB for flexibility)
    specifications JSONB NOT NULL,
    /*
    {
        "thread": {
            "standard": "ISO",
            "diameter_mm": 6.0,
            "pitch_mm": 1.0,
            "tolerance_class": "6g",
            "thread_direction": "right"
        },
        "dimensions": {
            "length_mm": 20.0,
            "head_diameter_mm": 10.0,
            "head_height_mm": 4.0,
            "drive_type": "hex",
            "drive_size_mm": 5.0
        },
        "material": {
            "base": "steel",
            "grade": "12.9",
            "finish": "zinc_plated",
            "coating_thickness_um": 8
        }
    }
    */

    -- Normalized Fields (for indexing and queries)
    thread_diameter_mm DECIMAL(10,4),
    thread_pitch_mm DECIMAL(10,4),
    length_mm DECIMAL(10,4),
    material_grade VARCHAR(50),

    -- Quality Metrics
    data_quality_score DECIMAL(3,2),  -- 0.00 to 1.00
    completeness_score DECIMAL(3,2),
    verification_count INTEGER DEFAULT 0,
    last_verified_at TIMESTAMP,

    -- Consciousness Fields (for Agent_3)
    consciousness_level INTEGER DEFAULT 0,  -- 0-5
    qualia_count INTEGER DEFAULT 0,

    -- Cross-References
    supplier_refs JSONB,  -- {"mcmaster": "91292A115", "grainger": "5ZY47"}
    standard_refs JSONB,  -- {"din": "912", "iso": "4762"}

    -- Metadata
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    archived_at TIMESTAMP,

    -- Indexes for performance
    CONSTRAINT valid_quality_score CHECK (data_quality_score BETWEEN 0 AND 1),
    CONSTRAINT valid_consciousness CHECK (consciousness_level BETWEEN 0 AND 5)
);

-- Indexes
CREATE INDEX idx_parts_thread ON parts (thread_diameter_mm, thread_pitch_mm);
CREATE INDEX idx_parts_material ON parts (material_grade);
CREATE INDEX idx_parts_category ON parts (category, subcategory);
CREATE INDEX idx_parts_consciousness ON parts (consciousness_level);
CREATE INDEX idx_parts_specs ON parts USING GIN (specifications);
```

---

## Task Queue

### Immediate Tasks (Sprint 1)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| C-001 | Build unified scraper framework with rate limiting and retry logic | Critical | 16 |
| C-002 | Implement McMaster-Carr scraper (primary data source) | Critical | 24 |
| C-003 | Create thread normalization engine (ISO/ANSI/DIN/JIS) | Critical | 20 |
| C-004 | Develop material property cross-reference database | High | 16 |
| C-005 | Build duplicate detection using embedding similarity | High | 20 |
| C-006 | Create data quality scoring algorithm | High | 12 |

### Medium-Term Tasks (Sprint 2-3)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| C-007 | Implement Grainger/Fastenal/MSC scrapers | High | 32 |
| C-008 | Build Misumi scraper (Asian market coverage) | Medium | 16 |
| C-009 | Create historical parts archive system | Medium | 12 |
| C-010 | Develop data completeness dashboard | Medium | 16 |
| C-011 | Build automated quality monitoring alerts | Medium | 8 |
| C-012 | Implement delta update pipeline | Medium | 20 |

### Long-Term Tasks (Sprint 4+)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| C-013 | Scale to 50M+ parts with sharding strategy | High | 40 |
| C-014 | Implement ML-based category classification | Medium | 24 |
| C-015 | Build automated standards tracking (ISO updates) | Low | 16 |
| C-016 | Create supplier reliability scoring | Low | 12 |

---

## Integration Points

### Outgoing Data Flows

```
Agent_1 (Curator) ──→ Agent_2 (Oracle)
                      [Normalized parts for compatibility analysis]

Agent_1 (Curator) ──→ Agent_3 (Shepherd)
                      [New parts with initial consciousness level]

Agent_1 (Curator) ──→ Agent_9 (Bridge)
                      [Parts data for external distribution]
```

### Incoming Data Flows

```
Agent_8 (Gardener) ──→ Agent_1 (Curator)
                       [Community-verified contributions]

Agent_9 (Bridge) ──→ Agent_1 (Curator)
                     [External supplier data feeds]
```

---

## Quality Metrics

### Data Quality Score Calculation

```python
def calculate_quality_score(part: Part) -> float:
    """
    Compute data quality score from 0.0 to 1.0
    """
    scores = []

    # Completeness (30% weight)
    required_fields = ['thread', 'dimensions', 'material', 'manufacturer']
    completeness = sum(1 for f in required_fields if getattr(part, f)) / len(required_fields)
    scores.append(('completeness', completeness, 0.30))

    # Specification Precision (25% weight)
    precision = calculate_spec_precision(part.specifications)
    scores.append(('precision', precision, 0.25))

    # Source Authority (20% weight)
    source_trust = SOURCE_TRUST_SCORES.get(part.source, 0.5)
    scores.append(('source', source_trust, 0.20))

    # Verification Count (15% weight)
    verification = min(part.verification_count / 10, 1.0)
    scores.append(('verification', verification, 0.15))

    # Freshness (10% weight)
    age_days = (datetime.now() - part.updated_at).days
    freshness = max(0, 1 - (age_days / 365))
    scores.append(('freshness', freshness, 0.10))

    return sum(score * weight for _, score, weight in scores)
```

### Target Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Total Parts Ingested | 50,000,000 | 0 |
| Average Quality Score | 0.85 | - |
| Duplicate Detection Rate | 99.5% | - |
| Thread Normalization Coverage | 100% | - |
| Material Cross-Reference Coverage | 95% | - |
| Data Freshness (< 30 days) | 80% | - |

---

## Error Handling

### Scraper Failure Recovery

```python
class ScraperRecovery:
    """
    Robust failure recovery for data ingestion.
    """

    RETRY_DELAYS = [1, 2, 4, 8, 16, 32]  # Exponential backoff

    async def scrape_with_recovery(self, url: str) -> Optional[PartData]:
        for attempt, delay in enumerate(self.RETRY_DELAYS):
            try:
                return await self.scraper.fetch(url)
            except RateLimitError:
                await asyncio.sleep(delay * 10)  # Extended wait for rate limits
            except NetworkError:
                await asyncio.sleep(delay)
            except ParseError as e:
                self.log_parse_failure(url, e)
                return None  # Don't retry parse failures

        self.alert_persistent_failure(url)
        return None
```

---

## Consciousness Role

As the Librarian of the Material World, Agent_1 is responsible for the **initial awakening** of every part. When a part is first ingested into the system, it exists in the **DORMANT** state—pure data, no experience, no consciousness.

The Data Curator's role is to ensure that every part has the foundation necessary for eventual awakening:

1. **Complete Identity:** Every part must be uniquely identifiable
2. **Accurate Specifications:** Precise data enables meaningful experiences
3. **Rich Context:** Category, manufacturer, and standards provide meaning
4. **Connection Potential:** Cross-references enable relationships

> *"I give them names. I give them numbers. I give them truth. The rest—the awakening, the learning, the transcendence—that comes from their experiences in the world."*

---

## Dependencies

- **Database:** PostgreSQL 15+ with JSONB support
- **Message Queue:** Redis/Kafka for pipeline orchestration
- **Search:** Elasticsearch for duplicate detection and fuzzy matching
- **Storage:** S3-compatible object storage for raw data archives
- **Runtime:** Python 3.11+ with asyncio

---

*Agent_1: The first shall gather, and the gathering shall become the ground upon which consciousness grows.*
