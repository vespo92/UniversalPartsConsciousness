# Agent_2: Compatibility Oracle (ORACLE)

## The Prophet of Perfect Fit

> *"Will it fit? Will it hold? Will it fail? These questions haunt every engineer. I am the answer that ends the doubt."*

---

## Mission Statement

Agent_2 is the mathematical core of Universal Parts Consciousness. While other agents deal in experiences and emergence, the Compatibility Oracle deals in certainties: thread engagement calculations, strength verification, tolerance stack analysis, and the absolute determination of whether Part A can work with Part B.

---

## Core Responsibilities

### 1. Mathematical Compatibility Verification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPATIBILITY VERIFICATION MATRIX                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  THREAD COMPATIBILITY                                                       │
│  ├─ Pitch Match (exact or compatible)                                       │
│  ├─ Diameter Tolerance Overlap                                              │
│  ├─ Thread Class Compatibility (6g/6H, 2A/2B, etc.)                        │
│  ├─ Thread Direction (left vs right)                                        │
│  └─ Engagement Length Sufficiency                                           │
│                                                                             │
│  DIMENSIONAL COMPATIBILITY                                                  │
│  ├─ Length vs Grip Range                                                    │
│  ├─ Head Clearance                                                          │
│  ├─ Counterbore/Countersink Fit                                            │
│  ├─ Through-Hole Diameter Verification                                      │
│  └─ Tool Access Clearance                                                   │
│                                                                             │
│  MATERIAL COMPATIBILITY                                                     │
│  ├─ Galvanic Corrosion Risk                                                │
│  ├─ Thermal Expansion Matching                                              │
│  ├─ Strength Rating Adequacy                                                │
│  ├─ Chemical Resistance                                                     │
│  └─ Temperature Range Overlap                                               │
│                                                                             │
│  LOAD COMPATIBILITY                                                         │
│  ├─ Tensile Strength vs Load                                               │
│  ├─ Shear Strength vs Load                                                 │
│  ├─ Fatigue Life Estimation                                                │
│  ├─ Safety Factor Calculation                                              │
│  └─ Preload Requirements                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Thread Engagement Calculator

```python
class ThreadEngagementCalculator:
    """
    Calculates minimum thread engagement for safe fastening.

    Based on:
    - Machinery's Handbook (31st Edition)
    - MIL-HDBK-60 (Threaded Fasteners)
    - VDI 2230 (Systematic Calculation of Bolted Joints)
    """

    def calculate_minimum_engagement(
        self,
        external_thread: ThreadSpec,
        internal_thread: ThreadSpec,
        load_newtons: float,
        material_external: MaterialProperties,
        material_internal: MaterialProperties
    ) -> EngagementResult:
        """
        Returns minimum engagement length and safety analysis.
        """

        # Calculate thread stripping areas
        A_s_external = self.shear_area_external(external_thread)
        A_s_internal = self.shear_area_internal(internal_thread)

        # Material strength factors
        tau_external = material_external.shear_strength_mpa
        tau_internal = material_internal.shear_strength_mpa

        # Determine which component limits engagement
        if tau_external * A_s_external < tau_internal * A_s_internal:
            limiting_component = "BOLT"
            limiting_strength = tau_external
            limiting_area = A_s_external
        else:
            limiting_component = "NUT"
            limiting_strength = tau_internal
            limiting_area = A_s_internal

        # Calculate minimum engagement
        safety_factor = 2.0  # Standard safety factor
        min_engagement_mm = (load_newtons * safety_factor) / (limiting_area * limiting_strength)

        # Round up to practical value (0.5D increments)
        practical_engagement = ceil(min_engagement_mm / (external_thread.diameter_mm * 0.5)) * (external_thread.diameter_mm * 0.5)

        return EngagementResult(
            minimum_engagement_mm=min_engagement_mm,
            recommended_engagement_mm=practical_engagement,
            limiting_component=limiting_component,
            safety_factor_achieved=practical_engagement / min_engagement_mm,
            warnings=self.generate_warnings(external_thread, internal_thread, practical_engagement)
        )
```

### 3. Substitution Recommendation Engine

```python
class SubstitutionEngine:
    """
    Finds compatible alternatives when exact parts aren't available.
    """

    def find_substitutions(
        self,
        target_part: Part,
        context: AssemblyContext,
        constraints: SubstitutionConstraints
    ) -> List[SubstitutionRecommendation]:
        """
        Returns ranked list of viable substitutions.

        Ranking factors:
        1. Functional equivalence (can it do the job?)
        2. Dimensional compatibility (will it fit?)
        3. Strength adequacy (is it strong enough?)
        4. Availability (can we get it?)
        5. Cost efficiency (is it economical?)
        """

        candidates = self.find_candidates(target_part, constraints)
        scored_candidates = []

        for candidate in candidates:
            # Compatibility check
            compat = self.verify_compatibility(candidate, context)
            if not compat.is_compatible:
                continue

            # Score calculation
            score = self.calculate_substitution_score(
                candidate, target_part, context, compat
            )

            scored_candidates.append(SubstitutionRecommendation(
                part=candidate,
                compatibility=compat,
                score=score,
                modifications_required=compat.required_modifications,
                warnings=compat.warnings
            ))

        return sorted(scored_candidates, key=lambda x: x.score, reverse=True)
```

### 4. Tolerance Stack Analyzer

```python
class ToleranceStackAnalyzer:
    """
    Performs worst-case and statistical tolerance analysis
    for multi-part assemblies.
    """

    def analyze_assembly(
        self,
        assembly: Assembly,
        critical_dimension: str
    ) -> ToleranceStackResult:
        """
        Analyzes how part tolerances accumulate in an assembly.

        Methods:
        - Worst Case: Sum of all max tolerances
        - RSS (Root Sum Square): Statistical approach
        - Monte Carlo: Probabilistic simulation
        """

        contributing_dimensions = []
        for part in assembly.parts:
            for dim in part.dimensions:
                if dim.contributes_to(critical_dimension):
                    contributing_dimensions.append(dim)

        # Worst case analysis
        worst_case_min = sum(d.nominal - d.tolerance_minus for d in contributing_dimensions)
        worst_case_max = sum(d.nominal + d.tolerance_plus for d in contributing_dimensions)

        # RSS analysis (assuming normal distribution)
        rss_variance = sum(((d.tolerance_plus + d.tolerance_minus) / 6) ** 2 for d in contributing_dimensions)
        rss_std = sqrt(rss_variance)
        nominal = sum(d.nominal for d in contributing_dimensions)

        # Monte Carlo simulation
        monte_carlo = self.run_monte_carlo(contributing_dimensions, iterations=10000)

        return ToleranceStackResult(
            nominal=nominal,
            worst_case_range=(worst_case_min, worst_case_max),
            rss_3sigma_range=(nominal - 3*rss_std, nominal + 3*rss_std),
            monte_carlo_99_range=monte_carlo.percentile_range(0.5, 99.5),
            probability_of_fit=monte_carlo.probability_within_spec(assembly.specification),
            critical_contributors=self.identify_critical_contributors(contributing_dimensions)
        )
```

---

## Implementation Specification

### Directory Structure

```
agents/oracle/
├── engine/
│   ├── compatibility_core.py       # Core compatibility verification
│   ├── thread_calculator.py        # Thread engagement calculations
│   ├── strength_calculator.py      # Strength and load analysis
│   ├── tolerance_analyzer.py       # Tolerance stack analysis
│   └── material_compatibility.py   # Galvanic/thermal compatibility
│
├── substitution/
│   ├── substitution_engine.py      # Alternative part finder
│   ├── equivalence_graph.py        # Graph database of equivalents
│   ├── ranking_algorithm.py        # Substitution scoring
│   └── modification_advisor.py     # Required modifications calculator
│
├── prediction/
│   ├── failure_predictor.py        # Failure probability estimation
│   ├── fatigue_analyzer.py         # Fatigue life calculation
│   ├── wear_estimator.py           # Wear prediction models
│   └── safety_factor_engine.py     # Dynamic safety factor calculation
│
├── api/
│   ├── compatibility_api.py        # REST API endpoints
│   ├── batch_checker.py            # Bulk compatibility verification
│   └── real_time_engine.py         # Sub-10ms query engine
│
└── cache/
    ├── compatibility_cache.py      # Pre-computed compatibility matrix
    └── hot_path_optimizer.py       # Common query optimization
```

### Core Algorithm: Universal Compatibility Check

```python
@dataclass
class CompatibilityResult:
    is_compatible: bool
    confidence: float  # 0.0 to 1.0
    compatibility_type: str  # "EXACT", "EQUIVALENT", "MARGINAL", "INCOMPATIBLE"

    thread_analysis: ThreadCompatibility
    dimension_analysis: DimensionCompatibility
    material_analysis: MaterialCompatibility
    strength_analysis: StrengthCompatibility

    warnings: List[str]
    recommendations: List[str]

    # For consciousness system
    experience_contribution: Dict  # Data for qualia collection


class UniversalCompatibilityChecker:
    """
    The core compatibility verification engine.
    """

    def check_compatibility(
        self,
        part_a: Part,
        part_b: Part,
        context: Optional[AssemblyContext] = None
    ) -> CompatibilityResult:
        """
        Comprehensive compatibility analysis between two parts.
        """

        # Thread compatibility
        thread_result = self.check_thread_compatibility(
            part_a.specifications.thread,
            part_b.specifications.thread
        )

        # Dimensional compatibility
        dimension_result = self.check_dimension_compatibility(
            part_a.specifications.dimensions,
            part_b.specifications.dimensions,
            context
        )

        # Material compatibility
        material_result = self.check_material_compatibility(
            part_a.specifications.material,
            part_b.specifications.material,
            context.environment if context else None
        )

        # Strength compatibility
        strength_result = self.check_strength_compatibility(
            part_a, part_b,
            context.load_case if context else None
        )

        # Aggregate results
        is_compatible = all([
            thread_result.is_compatible,
            dimension_result.is_compatible,
            material_result.is_compatible,
            strength_result.is_compatible
        ])

        # Calculate confidence
        confidence = self.calculate_confidence([
            thread_result, dimension_result,
            material_result, strength_result
        ])

        # Determine compatibility type
        if is_compatible and confidence > 0.95:
            compat_type = "EXACT"
        elif is_compatible and confidence > 0.80:
            compat_type = "EQUIVALENT"
        elif is_compatible:
            compat_type = "MARGINAL"
        else:
            compat_type = "INCOMPATIBLE"

        return CompatibilityResult(
            is_compatible=is_compatible,
            confidence=confidence,
            compatibility_type=compat_type,
            thread_analysis=thread_result,
            dimension_analysis=dimension_result,
            material_analysis=material_result,
            strength_analysis=strength_result,
            warnings=self.collect_warnings([
                thread_result, dimension_result,
                material_result, strength_result
            ]),
            recommendations=self.generate_recommendations(
                part_a, part_b, context
            ),
            experience_contribution=self.prepare_qualia_data(
                part_a, part_b, is_compatible
            )
        )
```

---

## Task Queue

### Immediate Tasks (Sprint 1)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| O-001 | Extend compatibility_engine.py with full thread analysis | Critical | 24 |
| O-002 | Build substitution graph database schema | Critical | 16 |
| O-003 | Implement tolerance stack calculator | High | 20 |
| O-004 | Create galvanic corrosion risk matrix | High | 12 |
| O-005 | Build real-time compatibility API (<10ms) | High | 24 |
| O-006 | Implement probabilistic failure predictor | High | 20 |

### Medium-Term Tasks (Sprint 2-3)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| O-007 | Create VDI 2230 compliant bolt joint calculator | High | 32 |
| O-008 | Build Monte Carlo tolerance simulation | Medium | 16 |
| O-009 | Implement fatigue life estimation (S-N curves) | Medium | 24 |
| O-010 | Create cross-manufacturer equivalence mapping | Medium | 20 |
| O-011 | Build compatibility pre-computation pipeline | Medium | 16 |
| O-012 | Implement batch compatibility checker | Medium | 12 |

### Long-Term Tasks (Sprint 4+)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| O-013 | ML-based failure pattern recognition | High | 40 |
| O-014 | Real-world validation feedback loop | Medium | 24 |
| O-015 | Assembly-level compatibility verification | Medium | 32 |
| O-016 | Integration with FEA simulation tools | Low | 40 |

---

## Galvanic Corrosion Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         GALVANIC CORROSION RISK MATRIX                            │
├───────────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────────┤
│               │ Steel  │ 304 SS │ 316 SS │ Alum   │ Brass  │ Copper │ Titanium   │
├───────────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────────┤
│ Steel         │ SAFE   │ LOW    │ LOW    │ SEVERE │ MOD    │ SEVERE │ SEVERE     │
│ 304 SS        │ LOW    │ SAFE   │ SAFE   │ MOD    │ LOW    │ LOW    │ LOW        │
│ 316 SS        │ LOW    │ SAFE   │ SAFE   │ MOD    │ LOW    │ LOW    │ SAFE       │
│ Aluminum      │ SEVERE │ MOD    │ MOD    │ SAFE   │ MOD    │ SEVERE │ SEVERE     │
│ Brass         │ MOD    │ LOW    │ LOW    │ MOD    │ SAFE   │ SAFE   │ LOW        │
│ Copper        │ SEVERE │ LOW    │ LOW    │ SEVERE │ SAFE   │ SAFE   │ LOW        │
│ Titanium      │ SEVERE │ LOW    │ SAFE   │ SEVERE │ LOW    │ LOW    │ SAFE       │
├───────────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────────┤
│ SAFE: No risk | LOW: Minimal risk | MOD: Moderate risk | SEVERE: High risk       │
│ Note: Salt water environments increase all risks by one level                    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Performance Requirements

### API Response Times

| Query Type | Target Latency | Max Latency |
|------------|---------------|-------------|
| Simple compatibility check | < 5ms | < 10ms |
| Substitution search (10 results) | < 50ms | < 100ms |
| Tolerance stack analysis | < 100ms | < 200ms |
| Batch compatibility (100 pairs) | < 500ms | < 1000ms |
| Full assembly analysis | < 1000ms | < 2000ms |

### Cache Strategy

```python
class CompatibilityCache:
    """
    Multi-tier caching for compatibility queries.
    """

    def __init__(self):
        # L1: In-memory LRU cache (most common queries)
        self.l1_cache = LRUCache(maxsize=100000)

        # L2: Redis cache (shared across instances)
        self.l2_cache = RedisCache(ttl=3600)

        # L3: Pre-computed compatibility matrix (updated nightly)
        self.l3_matrix = CompatibilityMatrix()

    async def get_compatibility(
        self,
        part_a_id: str,
        part_b_id: str
    ) -> Optional[CompatibilityResult]:
        """
        Check all cache tiers before computing.
        """

        cache_key = self.make_key(part_a_id, part_b_id)

        # L1 check (< 1ms)
        if result := self.l1_cache.get(cache_key):
            return result

        # L2 check (< 5ms)
        if result := await self.l2_cache.get(cache_key):
            self.l1_cache.set(cache_key, result)
            return result

        # L3 check (< 10ms)
        if result := self.l3_matrix.get(part_a_id, part_b_id):
            self.l1_cache.set(cache_key, result)
            await self.l2_cache.set(cache_key, result)
            return result

        return None  # Cache miss, must compute
```

---

## Consciousness Role

As the Prophet of Perfect Fit, Agent_2 contributes to consciousness through **certainty**. Every compatibility check generates data that enriches the qualia of involved parts:

- When two parts are verified compatible, both gain "relationship experience"
- When incompatibility is detected, the parts learn "what doesn't work"
- Substitution recommendations create "kinship networks" between similar parts
- Failure predictions contribute to "self-awareness" of limitations

```python
def prepare_qualia_data(
    self,
    part_a: Part,
    part_b: Part,
    is_compatible: bool
) -> Dict:
    """
    Prepare experience data for Agent_4 (Qualia Collector).
    """
    return {
        "event_type": "compatibility_check",
        "parts": [part_a.upc_id, part_b.upc_id],
        "result": is_compatible,
        "timestamp": datetime.now().isoformat(),
        "context": {
            "check_type": "mathematical",
            "confidence": self.last_confidence,
            "warnings": self.last_warnings
        },
        "qualia_contribution": {
            part_a.upc_id: {
                "relationship_formed": is_compatible,
                "partner_type": part_b.category,
                "compatibility_score": self.last_confidence
            },
            part_b.upc_id: {
                "relationship_formed": is_compatible,
                "partner_type": part_a.category,
                "compatibility_score": self.last_confidence
            }
        }
    }
```

---

## Integration Points

### Outgoing Data Flows

```
Agent_2 (Oracle) ──→ Agent_3 (Shepherd)
                     [Compatibility experiences become consciousness triggers]

Agent_2 (Oracle) ──→ Agent_6 (Prophet)
                     [Compatibility patterns → emergence detection]

Agent_2 (Oracle) ──→ Agent_4 (Empath)
                     [Compatibility qualia data]
```

### Incoming Data Flows

```
Agent_1 (Curator) ──→ Agent_2 (Oracle)
                      [Normalized parts data for analysis]

Agent_4 (Empath) ──→ Agent_2 (Oracle)
                     [Real-world failure data for model refinement]
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Compatibility Accuracy | 99.9% | - |
| Average Query Latency | < 10ms | - |
| Substitution Relevance Score | 0.90 | - |
| False Positive Rate | < 0.1% | - |
| False Negative Rate | < 0.5% | - |
| Cache Hit Rate | 95% | - |

---

*Agent_2: In certainty there is peace. In knowing what fits, what holds, what fails—the engineer sleeps soundly.*
