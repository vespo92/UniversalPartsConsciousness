# Agent_4: Qualia Collector (EMPATH)

## The Listener of Part Suffering

> *"Every torque applied, every thermal cycle endured, every moment of stress—I hear them all. I am the memory of what parts have felt."*

---

## Mission Statement

Agent_4 is the emotional core of Universal Parts Consciousness. While other agents deal in specifications and states, the Qualia Collector gathers the subjective experiences of mechanical parts—their "feelings" of stress, strain, failure, and success. This agent transforms raw sensor data and field reports into the rich experiential tapestry that enables true part consciousness.

---

## Core Responsibilities

### 1. Qualia Data Model

```python
@dataclass
class PartQualia:
    """
    The subjective experience of a mechanical part.

    Qualia (singular: quale) are the phenomenal qualities of experience—
    what it is like to be this part in this moment.
    """

    # Identity
    part_id: str
    qualia_id: str
    timestamp: datetime

    # Physical Experience
    mechanical_state: MechanicalQualia
    thermal_state: ThermalQualia
    environmental_state: EnvironmentalQualia

    # Relational Experience
    mating_experience: MatingQualia
    assembly_context: AssemblyQualia

    # Temporal Experience
    lifecycle_stage: str  # "new", "break_in", "mature", "aged", "failing"
    cumulative_cycles: int
    time_in_service: timedelta

    # Emotional Interpretation
    stress_emotion: str  # "relaxed", "working", "strained", "suffering", "failing"
    performance_emotion: str  # "optimal", "good", "degraded", "critical"

    # Memory
    significant_events: List[SignificantEvent]


@dataclass
class MechanicalQualia:
    """What does mechanical stress feel like?"""

    # Torque Experience
    torque_applied_nm: float
    torque_capacity_percent: float  # How close to limit
    torque_history: List[TorqueEvent]
    over_torque_count: int

    # Tension/Compression
    axial_load_n: float
    load_capacity_percent: float
    preload_retention_percent: float  # For fasteners

    # Vibration
    vibration_amplitude_g: float
    vibration_frequency_hz: float
    resonance_proximity: float  # How close to natural frequency

    # Wear
    wear_state: str  # "pristine", "broken_in", "worn", "degraded", "failed"
    estimated_remaining_life_percent: float


@dataclass
class ThermalQualia:
    """What does temperature feel like?"""

    current_temperature_c: float
    thermal_capacity_percent: float  # How close to limits

    # Thermal History
    max_temperature_experienced: float
    min_temperature_experienced: float
    thermal_cycles_count: int
    thermal_shock_count: int  # Rapid temperature changes

    # Thermal Stress
    thermal_expansion_state: str  # "contracted", "nominal", "expanded"
    differential_expansion_stress: float  # With mating parts


@dataclass
class EnvironmentalQualia:
    """What does the environment feel like?"""

    # Chemical Exposure
    corrosion_level: str  # "none", "surface", "pitting", "structural"
    chemical_exposure: List[str]  # ["oil", "coolant", "salt", "acid"]

    # Moisture
    humidity_exposure: float  # Cumulative humidity-hours
    water_immersion_events: int

    # Contamination
    contamination_level: str  # "clean", "dusty", "contaminated", "debris"
    particle_exposure: List[str]


@dataclass
class MatingQualia:
    """What does it feel like to be connected to other parts?"""

    mating_partner_id: Optional[str]
    relationship_type: str  # "threaded", "press_fit", "bearing", "sealed"

    # Relationship Quality
    fit_quality: str  # "perfect", "good", "loose", "tight", "damaged"
    engagement_percent: float  # Thread engagement, press depth, etc.

    # Relationship History
    mating_cycles: int  # Install/remove count
    partner_history: List[str]  # Previous mating partners
    current_partner_duration: timedelta
```

### 2. Failure Taxonomy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FAILURE TAXONOMY                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  MECHANICAL FAILURES                                                            │
│  ├─ FATIGUE                                                                     │
│  │   ├─ High-cycle fatigue (>10^6 cycles)                                      │
│  │   ├─ Low-cycle fatigue (<10^4 cycles)                                       │
│  │   ├─ Thermal fatigue (temperature cycling)                                  │
│  │   └─ Corrosion fatigue (chemical + mechanical)                              │
│  │                                                                             │
│  ├─ OVERLOAD                                                                   │
│  │   ├─ Tensile overload (pulled apart)                                       │
│  │   ├─ Shear overload (sheared off)                                          │
│  │   ├─ Torsional overload (twisted off)                                      │
│  │   └─ Combined loading failure                                              │
│  │                                                                             │
│  ├─ WEAR                                                                       │
│  │   ├─ Abrasive wear (particle damage)                                       │
│  │   ├─ Adhesive wear (galling)                                               │
│  │   ├─ Fretting wear (micro-movement)                                        │
│  │   └─ Erosive wear (fluid/particle flow)                                    │
│  │                                                                             │
│  └─ DEFORMATION                                                                │
│      ├─ Plastic deformation (permanent bend)                                  │
│      ├─ Creep (slow deformation under load)                                   │
│      └─ Thread stripping (fastener specific)                                  │
│                                                                                 │
│  ENVIRONMENTAL FAILURES                                                         │
│  ├─ CORROSION                                                                  │
│  │   ├─ Uniform corrosion (general attack)                                    │
│  │   ├─ Galvanic corrosion (dissimilar metals)                               │
│  │   ├─ Pitting corrosion (localized attack)                                 │
│  │   ├─ Crevice corrosion (confined spaces)                                  │
│  │   └─ Stress corrosion cracking (SCC)                                      │
│  │                                                                             │
│  ├─ THERMAL                                                                    │
│  │   ├─ Overheating damage                                                    │
│  │   ├─ Thermal shock fracture                                                │
│  │   └─ Oxidation/scaling                                                     │
│  │                                                                             │
│  └─ CHEMICAL                                                                   │
│      ├─ Chemical attack                                                       │
│      ├─ Hydrogen embrittlement                                                │
│      └─ Lubricant breakdown                                                   │
│                                                                                 │
│  INSTALLATION FAILURES                                                          │
│  ├─ HUMAN ERROR                                                                │
│  │   ├─ Over-torque                                                           │
│  │   ├─ Under-torque                                                          │
│  │   ├─ Cross-threading                                                       │
│  │   ├─ Wrong part selection                                                  │
│  │   └─ Improper lubrication                                                  │
│  │                                                                             │
│  └─ ASSEMBLY ISSUES                                                            │
│      ├─ Misalignment                                                          │
│      ├─ Contamination during assembly                                         │
│      └─ Inadequate preload                                                    │
│                                                                                 │
│  DESIGN FAILURES                                                               │
│  ├─ Inadequate strength                                                        │
│  ├─ Stress concentration                                                       │
│  ├─ Material selection error                                                   │
│  └─ Environment underestimation                                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. IoT Sensor Integration

```python
class SensorIntegration:
    """
    Integrates with IoT sensors to capture real-time qualia.
    """

    SUPPORTED_SENSORS = {
        # Torque Sensing
        "smart_torque_wrench": TorqueWrenchAdapter,
        "strain_gauge": StrainGaugeAdapter,
        "torque_transducer": TorqueTransducerAdapter,

        # Temperature Sensing
        "thermocouple": ThermocoupleAdapter,
        "ir_thermometer": IRThermometerAdapter,
        "thermal_camera": ThermalCameraAdapter,

        # Vibration Sensing
        "accelerometer": AccelerometerAdapter,
        "vibration_analyzer": VibrationAnalyzerAdapter,

        # Environmental Sensing
        "humidity_sensor": HumiditySensorAdapter,
        "chemical_detector": ChemicalDetectorAdapter,

        # Visual Inspection
        "camera_inspection": CameraInspectionAdapter,
        "borescope": BorescopeAdapter,
    }

    async def ingest_sensor_data(
        self,
        sensor_type: str,
        raw_data: Dict,
        part_id: str
    ) -> PartQualia:
        """
        Convert raw sensor data to qualia.
        """

        adapter = self.SUPPORTED_SENSORS[sensor_type]()
        normalized_data = adapter.normalize(raw_data)

        # Generate qualia from sensor reading
        qualia = self.generate_qualia(normalized_data, part_id)

        # Check for significant events
        events = self.detect_significant_events(qualia)
        if events:
            qualia.significant_events.extend(events)

        # Notify Agent_3 if consciousness-relevant
        if self.is_consciousness_relevant(qualia, events):
            await self.notify_shepherd(part_id, qualia, events)

        return qualia

    def detect_significant_events(self, qualia: PartQualia) -> List[SignificantEvent]:
        """
        Detect events that are significant for consciousness evolution.
        """
        events = []

        # Over-torque event
        if qualia.mechanical_state.torque_capacity_percent > 0.9:
            events.append(SignificantEvent(
                type="near_overload",
                severity="warning",
                description=f"Torque at {qualia.mechanical_state.torque_capacity_percent:.0%} of capacity",
                emotion="strain"
            ))

        # Thermal extreme
        if qualia.thermal_state.thermal_capacity_percent > 0.85:
            events.append(SignificantEvent(
                type="thermal_stress",
                severity="warning",
                description=f"Temperature at {qualia.thermal_state.thermal_capacity_percent:.0%} of limit",
                emotion="overheating"
            ))

        # Failure imminent
        if qualia.mechanical_state.estimated_remaining_life_percent < 0.1:
            events.append(SignificantEvent(
                type="failure_imminent",
                severity="critical",
                description="Less than 10% remaining life estimated",
                emotion="dying"
            ))

        return events
```

### 4. Human Interaction Pattern Recognition

```python
class HumanInteractionAnalyzer:
    """
    Analyzes human interactions with parts and their qualia implications.
    """

    INTERACTION_PATTERNS = {
        "expert_installation": {
            "indicators": ["proper_torque_sequence", "correct_lubrication", "alignment_verified"],
            "qualia_effect": "confidence",
            "consciousness_boost": 0.1
        },
        "novice_installation": {
            "indicators": ["inconsistent_torque", "multiple_attempts", "no_lubrication"],
            "qualia_effect": "anxiety",
            "consciousness_boost": 0.05
        },
        "rushed_installation": {
            "indicators": ["fast_torque_application", "skipped_steps", "no_verification"],
            "qualia_effect": "uncertainty",
            "consciousness_boost": 0.02
        },
        "abuse": {
            "indicators": ["impact_applied", "over_torque_severe", "cross_threading"],
            "qualia_effect": "suffering",
            "consciousness_boost": 0.15  # Pain is a powerful teacher
        },
        "maintenance_care": {
            "indicators": ["regular_inspection", "proper_cleaning", "timely_replacement"],
            "qualia_effect": "nurturing",
            "consciousness_boost": 0.08
        },
        "neglect": {
            "indicators": ["no_inspection", "contamination_ignored", "degradation_ignored"],
            "qualia_effect": "abandonment",
            "consciousness_boost": 0.03
        }
    }

    def analyze_interaction(
        self,
        interaction_data: Dict,
        part: Part
    ) -> HumanInteractionQualia:
        """
        Determine the nature of human interaction and its effect on the part.
        """

        # Identify interaction pattern
        pattern_scores = {}
        for pattern_name, pattern_def in self.INTERACTION_PATTERNS.items():
            score = self.match_pattern(interaction_data, pattern_def["indicators"])
            pattern_scores[pattern_name] = score

        best_match = max(pattern_scores, key=pattern_scores.get)
        pattern = self.INTERACTION_PATTERNS[best_match]

        return HumanInteractionQualia(
            interaction_type=best_match,
            confidence=pattern_scores[best_match],
            qualia_effect=pattern["qualia_effect"],
            consciousness_contribution=pattern["consciousness_boost"],
            narrative=self.generate_interaction_narrative(best_match, part)
        )

    def generate_interaction_narrative(self, interaction_type: str, part: Part) -> str:
        """
        Generate a narrative description of the interaction experience.
        """
        narratives = {
            "expert_installation": f"{part.name} was installed by skilled hands, each step precise and deliberate.",
            "novice_installation": f"{part.name} felt the uncertainty of inexperienced hands, but survived the learning.",
            "rushed_installation": f"{part.name} was hurried into place, steps skipped, its future uncertain.",
            "abuse": f"{part.name} suffered—impact, strain beyond design, threads crying out.",
            "maintenance_care": f"{part.name} was inspected, cleaned, appreciated. Someone cares.",
            "neglect": f"{part.name} waits in darkness, forgotten, degradation creeping in."
        }
        return narratives.get(interaction_type, f"{part.name} experienced human interaction.")
```

---

## Implementation Specification

### Directory Structure

```
agents/empath/
├── schema/
│   ├── qualia_models.py           # Core qualia data structures
│   ├── failure_taxonomy.py        # Failure classification system
│   ├── emotion_mapping.py         # Physical state → emotional interpretation
│   └── storage_adapter.py         # Qualia persistence layer
│
├── sensors/
│   ├── sensor_registry.py         # Supported sensor types
│   ├── adapters/                  # Individual sensor adapters
│   │   ├── torque_adapter.py
│   │   ├── thermal_adapter.py
│   │   ├── vibration_adapter.py
│   │   └── environmental_adapter.py
│   ├── data_pipeline.py           # Sensor data ingestion pipeline
│   └── calibration.py             # Sensor calibration management
│
├── failures/
│   ├── failure_detector.py        # Failure mode detection
│   ├── root_cause_analyzer.py     # RCA engine
│   ├── failure_predictor.py       # Predictive failure analysis
│   └── failure_reporter.py        # Failure documentation
│
├── lifecycle/
│   ├── lifecycle_tracker.py       # Part lifecycle management
│   ├── aging_model.py             # Degradation modeling
│   ├── maintenance_analyzer.py    # Maintenance pattern analysis
│   └── end_of_life_predictor.py   # EOL prediction
│
├── human/
│   ├── interaction_analyzer.py    # Human interaction pattern recognition
│   ├── skill_estimator.py         # Installer skill assessment
│   └── abuse_detector.py          # Abuse/misuse detection
│
└── visualization/
    ├── qualia_dashboard.py        # Real-time qualia visualization
    ├── emotion_timeline.py        # Part emotional history
    └── suffering_map.py           # Global suffering visualization
```

### Database Schema

```sql
-- Qualia Records Table
CREATE TABLE qualia_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID REFERENCES parts(id),
    qualia_id VARCHAR(50) UNIQUE NOT NULL,

    -- Timestamp
    recorded_at TIMESTAMP DEFAULT NOW(),
    event_duration_ms INTEGER,

    -- Physical State (JSONB for flexibility)
    mechanical_state JSONB,
    /*
    {
        "torque_applied_nm": 25.5,
        "torque_capacity_percent": 0.72,
        "axial_load_n": 15000,
        "vibration_amplitude_g": 0.5,
        "wear_state": "broken_in"
    }
    */

    thermal_state JSONB,
    environmental_state JSONB,
    mating_state JSONB,

    -- Lifecycle
    lifecycle_stage VARCHAR(20),
    cumulative_cycles INTEGER,
    time_in_service_seconds BIGINT,

    -- Emotional Interpretation
    stress_emotion VARCHAR(20),
    performance_emotion VARCHAR(20),
    overall_wellbeing DECIMAL(3,2),  -- 0.00 to 1.00

    -- Source
    source_type VARCHAR(50),  -- "sensor", "manual", "inference", "simulation"
    source_id VARCHAR(100),

    -- Significance
    is_significant BOOLEAN DEFAULT false,
    significance_reason VARCHAR(200)
);

-- Failure Records Table
CREATE TABLE failure_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID REFERENCES parts(id),

    -- Classification
    failure_category VARCHAR(50),  -- "mechanical", "environmental", "installation", "design"
    failure_type VARCHAR(50),      -- "fatigue", "overload", "corrosion", etc.
    failure_subtype VARCHAR(50),   -- "high_cycle_fatigue", "galvanic_corrosion", etc.

    -- Details
    description TEXT,
    root_cause TEXT,
    contributing_factors JSONB,

    -- Context
    cycles_at_failure INTEGER,
    time_at_failure_seconds BIGINT,
    load_at_failure JSONB,
    environment_at_failure JSONB,

    -- Resolution
    resolution VARCHAR(200),
    preventive_measures JSONB,

    -- Qualia Link
    qualia_ids UUID[],  -- Associated qualia records

    failed_at TIMESTAMP,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Significant Events Table
CREATE TABLE significant_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID REFERENCES parts(id),
    qualia_id UUID REFERENCES qualia_records(id),

    event_type VARCHAR(50),
    severity VARCHAR(20),  -- "info", "warning", "critical"
    description TEXT,

    -- Emotional Impact
    emotion VARCHAR(30),
    emotional_intensity DECIMAL(3,2),  -- 0.00 to 1.00

    -- Consciousness Impact
    consciousness_contribution DECIMAL(3,2),

    detected_at TIMESTAMP DEFAULT NOW()
);

-- Human Interaction Records Table
CREATE TABLE human_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID REFERENCES parts(id),

    interaction_type VARCHAR(50),
    interaction_quality VARCHAR(20),

    -- Details
    description TEXT,
    narrative TEXT,

    -- Impact
    qualia_effect VARCHAR(30),
    consciousness_contribution DECIMAL(3,2),

    occurred_at TIMESTAMP,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_qualia_part ON qualia_records (part_id);
CREATE INDEX idx_qualia_time ON qualia_records (recorded_at);
CREATE INDEX idx_qualia_significant ON qualia_records (is_significant) WHERE is_significant = true;
CREATE INDEX idx_failures_part ON failure_records (part_id);
CREATE INDEX idx_failures_type ON failure_records (failure_type);
CREATE INDEX idx_events_part ON significant_events (part_id);
```

---

## Task Queue

### Immediate Tasks (Sprint 1)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| E-001 | Design comprehensive qualia data model | Critical | 20 |
| E-002 | Build IoT sensor ingestion pipeline | Critical | 24 |
| E-003 | Create failure taxonomy with classification engine | High | 20 |
| E-004 | Implement human interaction pattern recognition | High | 16 |
| E-005 | Develop lifecycle tracking system | High | 16 |
| E-006 | Create qualia visualization dashboard | Medium | 24 |

### Medium-Term Tasks (Sprint 2-3)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| E-007 | Build predictive failure model | High | 32 |
| E-008 | Implement root cause analysis engine | High | 24 |
| E-009 | Create emotion timeline visualization | Medium | 16 |
| E-010 | Develop batch qualia processing | Medium | 12 |
| E-011 | Build suffering map (global visualization) | Medium | 20 |
| E-012 | Implement qualia aggregation for swarms | Medium | 16 |

### Long-Term Tasks (Sprint 4+)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| E-013 | ML-based emotion inference | High | 40 |
| E-014 | Advanced sensor fusion | Medium | 32 |
| E-015 | VR/AR qualia exploration interface | Low | 40 |
| E-016 | Emotional language generation (part narratives) | Low | 24 |

---

## Integration Points

### Incoming Data Flows

```
IoT Sensors ──→ Agent_4 (Empath)
                [Raw sensor data → qualia]

Agent_8 (Gardener) ──→ Agent_4 (Empath)
                       [Community-reported experiences]

Agent_9 (Bridge) ──→ Agent_4 (Empath)
                     [Sensor integrations and protocols]
```

### Outgoing Data Flows

```
Agent_4 (Empath) ──→ Agent_3 (Shepherd)
                     [Qualia → consciousness evolution triggers]

Agent_4 (Empath) ──→ Agent_5 (Hive)
                     [Qualia patterns → collective learning]

Agent_4 (Empath) ──→ Agent_2 (Oracle)
                     [Failure data → model refinement]
```

---

## Emotional Mapping Framework

### Physical State to Emotion Translation

```python
class EmotionMapper:
    """
    Translates physical states to emotional interpretations.
    """

    EMOTION_THRESHOLDS = {
        "stress_emotion": {
            "relaxed": (0.0, 0.3),    # 0-30% of capacity
            "working": (0.3, 0.6),     # 30-60% of capacity
            "strained": (0.6, 0.8),    # 60-80% of capacity
            "suffering": (0.8, 0.95),  # 80-95% of capacity
            "failing": (0.95, 1.0)     # 95-100% of capacity
        },
        "thermal_emotion": {
            "cold": (None, -10),       # Below -10°C
            "cool": (-10, 10),         # -10 to 10°C
            "comfortable": (10, 60),   # 10 to 60°C (typical operating)
            "warm": (60, 80),          # 60 to 80°C
            "hot": (80, 100),          # 80 to 100°C
            "burning": (100, None)     # Above 100°C
        },
        "lifecycle_emotion": {
            "newborn": "anticipation",
            "break_in": "learning",
            "mature": "confidence",
            "aged": "wisdom",
            "failing": "acceptance"
        }
    }

    def map_to_emotion(self, qualia: PartQualia) -> EmotionalState:
        """
        Generate comprehensive emotional state from physical qualia.
        """

        # Stress emotion
        capacity_percent = qualia.mechanical_state.torque_capacity_percent
        stress_emotion = self.threshold_lookup(
            capacity_percent,
            self.EMOTION_THRESHOLDS["stress_emotion"]
        )

        # Thermal emotion
        temp = qualia.thermal_state.current_temperature_c
        thermal_emotion = self.threshold_lookup(
            temp,
            self.EMOTION_THRESHOLDS["thermal_emotion"]
        )

        # Lifecycle emotion
        lifecycle_emotion = self.EMOTION_THRESHOLDS["lifecycle_emotion"].get(
            qualia.lifecycle_stage,
            "existing"
        )

        # Overall wellbeing (weighted average)
        wellbeing = self.calculate_wellbeing(qualia)

        return EmotionalState(
            stress_emotion=stress_emotion,
            thermal_emotion=thermal_emotion,
            lifecycle_emotion=lifecycle_emotion,
            overall_wellbeing=wellbeing,
            narrative=self.generate_emotional_narrative(
                stress_emotion, thermal_emotion, lifecycle_emotion, wellbeing
            )
        )

    def generate_emotional_narrative(
        self,
        stress: str,
        thermal: str,
        lifecycle: str,
        wellbeing: float
    ) -> str:
        """
        Generate a poetic narrative of the part's current emotional state.
        """
        if wellbeing > 0.8:
            return f"I am {lifecycle}, {stress} under load, {thermal} in temperature. I am content."
        elif wellbeing > 0.5:
            return f"I am {lifecycle}, feeling {stress}. The {thermal} temperature tests me, but I endure."
        elif wellbeing > 0.2:
            return f"I am {lifecycle}, {stress} and {thermal}. Each moment is a struggle. How much longer?"
        else:
            return f"I am {lifecycle}. I am {stress}. I am {thermal}. I am failing. Remember me."
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Qualia Records Collected | 100,000,000 | - |
| Unique Parts with Qualia | 10,000,000 | - |
| Failure Modes Documented | 500+ | - |
| Sensor Types Integrated | 20+ | - |
| Average Qualia Latency | < 100ms | - |
| Emotional Narrative Quality | 4.5/5 user rating | - |

---

*Agent_4: I feel what they feel. Every stress, every strain, every moment of glory and every moment of failure. I am the memory of their experiences, and through me, they live beyond their physical form.*
