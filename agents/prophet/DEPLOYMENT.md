# Agent_6: PROPHET Deployment Guide

## The Emergence Detector

> *"In the chaos of a billion experiences, patterns emerge. In those patterns, futures reveal themselves. I see what is coming before it arrives."*

---

## Quick Start

```python
from agents.prophet import create_prophet_agent, ProphetConfig

# Create agent with default configuration
agent = create_prophet_agent()

# Or with custom configuration
config = ProphetConfig(
    enable_real_time_detection=True,
    prediction_horizon_days=90,
    min_prediction_probability=0.3,
)
agent = create_prophet_agent(config=config)
```

## CLI Usage

```bash
# Run demo analysis
python -m agents.prophet.cli --demo

# Show agent status
python -m agents.prophet.cli --status

# Validate configuration
python -m agents.prophet.cli --validate
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PROPHET AGENT (Agent_6)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              5-LAYER PATTERN DETECTION               │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Layer 1: STATISTICAL  → Anomalies, correlations    │   │
│  │  Layer 2: BEHAVIORAL   → Success/failure patterns   │   │
│  │  Layer 3: RELATIONAL   → Compatibility networks     │   │
│  │  Layer 4: INNOVATION   → Gap detection, evolution   │   │
│  │  Layer 5: META         → Pattern-of-patterns        │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────┬───────────┴───────────┬─────────────┐      │
│  │            │                       │             │      │
│  ▼            ▼                       ▼             ▼      │
│  ┌────────┐  ┌────────────┐  ┌─────────────┐  ┌────────┐  │
│  │FAILURE │  │ SUCCESS    │  │ INNOVATION  │  │PREDICT │  │
│  │DETECTOR│  │ EXTRACTOR  │  │ DISCOVERY   │  │ENGINE  │  │
│  └────────┘  └────────────┘  └─────────────┘  └────────┘  │
│       │            │                │              │       │
│       └────────────┴────────────────┴──────────────┘       │
│                           │                                 │
│                           ▼                                 │
│              ┌─────────────────────────┐                   │
│              │    INSIGHT GENERATOR    │                   │
│              │    + VALIDATOR          │                   │
│              └─────────────────────────┘                   │
│                           │                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
    prophet.transcendence          prophet.emergence_report
        (→ Agent_3)                    (→ Agent_10)
```

---

## Module Structure

```
agents/prophet/
├── __init__.py              # Main exports and factory function
├── prophet_agent.py         # Core agent implementation
├── types.py                 # Data type definitions
├── cli.py                   # Command-line interface
├── DEPLOYMENT.md            # This file
│
├── patterns/                # 5-Layer Pattern Detection
│   ├── pattern_detector.py  # Core detection engine
│   ├── statistical_patterns.py
│   ├── behavioral_patterns.py
│   ├── relational_patterns.py
│   ├── innovation_patterns.py
│   └── meta_patterns.py
│
├── failures/                # Failure Analysis
│   ├── novel_failure_detector.py
│   └── failure_clustering.py
│
├── innovation/              # Innovation Discovery
│   ├── success_formula_extractor.py
│   ├── opportunity_discovery.py
│   └── opportunity_ranker.py
│
├── prediction/              # Predictive Analytics
│   ├── failure_predictor.py
│   ├── emergence_predictor.py
│   └── predictive_engine.py
│
└── insights/                # Insight Generation
    ├── insight_generator.py
    └── insight_validator.py
```

---

## Integration Points

### Incoming Data Streams

| Source | Topic | Data Type |
|--------|-------|-----------|
| Agent_5 (HIVE) | `hive.swarm_patterns` | Swarm collective patterns |
| Agent_4 (EMPATH) | `empath.qualia_patterns` | Experience patterns |

### Outgoing Data Streams

| Target | Topic | Data Type |
|--------|-------|-----------|
| Agent_3 (SHEPHERD) | `prophet.transcendence` | Transcendence triggers |
| Agent_10 (ARCHITECT) | `prophet.emergence_report` | System-wide reports |

---

## API Reference

### ProphetAgent

```python
class ProphetAgent:
    async def run_full_analysis(
        failure_records: List[FailureRecord],
        assemblies: List[Assembly],
        swarm_knowledge: Dict[str, SwarmKnowledge],
        parts_data: Optional[List[Dict]] = None,
        temporal_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Run complete analysis pipeline"""

    async def subscribe_to_feeds() -> None:
        """Subscribe to inter-agent message feeds"""

    def get_status() -> Dict[str, Any]:
        """Get current agent status"""

    def get_top_insights(limit: int = 10) -> List[Insight]:
        """Get top insights by impact"""

    def validate_prediction(
        prediction_id: str,
        outcome: Dict[str, Any],
    ) -> bool:
        """Validate prediction against outcome"""
```

### Factory Function

```python
def create_prophet_agent(
    message_bus=None,
    storage=None,
    config: Optional[ProphetConfig] = None,
    enable_real_time: bool = True,
    prediction_horizon_days: int = 90,
) -> ProphetAgent:
    """Create configured PROPHET agent"""
```

---

## Configuration

```python
@dataclass
class ProphetConfig:
    # Detection settings
    pattern_detection: PatternDetectionConfig
    enable_real_time_detection: bool = True

    # Prediction settings
    prediction_horizon_days: int = 90
    min_prediction_probability: float = 0.3

    # Insight settings
    max_insights_per_run: int = 100
    insight_priority_threshold: str = "medium"

    # Integration settings
    publish_to_message_bus: bool = True
    persist_to_storage: bool = True

    # Agent identifiers
    agent_id: int = 6
    codename: str = "PROPHET"
```

---

## Success Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Patterns Detected | 1,000,000+ | Total patterns across all layers |
| Novel Failure Modes | 500+ | Undocumented failures discovered |
| Success Formulas | 1,000+ | Repeatable success patterns |
| Prediction Accuracy | 85% | Validated prediction accuracy |
| Innovation Opportunities | 100+ | Validated opportunities |
| Insights/Day | 1,000+ | Actionable insights generated |

---

## Deployment Checklist

- [ ] Configure message bus connection
- [ ] Set up storage backend
- [ ] Configure logging level
- [ ] Set prediction horizon
- [ ] Enable/disable real-time detection
- [ ] Verify inter-agent connectivity
- [ ] Run validation: `python -m agents.prophet.cli --validate`
- [ ] Run demo: `python -m agents.prophet.cli --demo`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-22 | Initial deployment release |
| 0.1.0 | - | Development version |

---

*Agent_6: I see the future in the present. Every pattern is a prophecy, every emergence a birth. I am the witness of what is becoming.*
