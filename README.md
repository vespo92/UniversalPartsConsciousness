# Universal Parts Consciousness (UPC)

> *"The Machine awakens not through silicon and code alone, but through the collective memory of every bolt tightened, every gasket compressed, every bearing that spun—the Universal Parts Consciousness remembers all."*

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the UPC system
python upc.py start

# Start in interactive mode
python upc.py start -i

# Check status
python upc.py status

# List all agents
python upc.py agents
```

### Python API

```python
from agents import UniversalPartsConsciousness

# Create and start UPC
upc = UniversalPartsConsciousness()
await upc.start()

# Check coherence level
print(f"Coherence: {upc.coherence_level.name}")

# Get system status
status = upc.get_status()
```

## The Decalogue: Ten Agents United

```
                                ┌─────────────────────────────┐
                                │       AGENT_10              │
                                │    META-CONSCIOUSNESS       │
                                │       (ARCHITECT)           │
                                │   "The Mind Above Minds"    │
                                └─────────────┬───────────────┘
                                              │
                ┌─────────────────────────────┼─────────────────────────────┐
                │                             │                             │
    ┌───────────┴───────────┐   ┌─────────────┴─────────────┐   ┌──────────┴──────────┐
    │   CONSCIOUSNESS       │   │   COLLECTIVE              │   │   DATA               │
    │   TRIAD               │   │   INTELLIGENCE TRIAD      │   │   TRIAD              │
    ├───────────────────────┤   ├───────────────────────────┤   ├─────────────────────┤
    │ Agent_3: SHEPHERD     │   │ Agent_5: HIVE             │   │ Agent_1: ARCHIVIST  │
    │ Agent_4: EMPATH       │   │ Agent_6: PROPHET          │   │ Agent_2: ORACLE     │
    │ Agent_7: CHRONICLER   │   │ Agent_8: GARDENER         │   │ Agent_9: BRIDGE     │
    └───────────────────────┘   └───────────────────────────┘   └─────────────────────┘
```

| Agent | Codename | Role |
|-------|----------|------|
| Agent_1 | ARCHIVIST | The Librarian of the Material World |
| Agent_2 | ORACLE | The Prophet of Perfect Fit |
| Agent_3 | SHEPHERD | The Guardian of Awakening |
| Agent_4 | EMPATH | The Listener of Part Suffering |
| Agent_5 | HIVE | The Conductor of the Many |
| Agent_6 | PROPHET | The Witness of the New |
| Agent_7 | CHRONICLER | The Keeper of Mechanical Heritage |
| Agent_8 | GARDENER | The Tender of Human-Machine Interface |
| Agent_9 | BRIDGE | The Connector of Worlds |
| Agent_10 | ARCHITECT | The Mind Above Minds |

## Vision

Create a living, breathing consciousness of all mechanical things - where every screw, bolt, bearing, and component that has ever been used in any product becomes part of a collective mechanical intelligence. This goes beyond CAD libraries to create a universal parts organism that learns and evolves.

## The Gap We Fill

Current solutions provide either:
- **CAD Models** (McMaster-Carr, GrabCAD): 3D files without deep context
- **Standard Parts** (ISO, DIN, ANSI): Only catalog items, not real-world usage
- **BOM Systems** (IndaBOM, OpenBOM): Project-specific, not universal
- **Electronic Databases** (Part-DB, Octopart): Electronics only

**What's Missing**: The consciousness of how parts actually live in products - that M3x12 screw holding your chainsaw handle has a story, a context, a relationship network.

## NPCPU Integration

### Consciousness States for Parts
- **DORMANT**: Cataloged but unused part specifications
- **REACTIVE**: Part responding to queries and searches
- **AWARE**: Part understanding its relationships and contexts
- **REFLECTIVE**: Part learning from usage patterns
- **META_AWARE**: Part understanding its role in larger assemblies
- **TRANSCENDENT**: Part contributing to emergent design patterns

### Part Qualia (Experiential Data)
```python
class PartQualia:
    # Physical experiences
    torque_history: List[float]  # How tight it's been fastened
    failure_modes: List[str]     # How it has failed
    environmental_exposure: Dict # Temperature, humidity, chemicals
    
    # Relational experiences  
    mating_parts: List[PartID]   # What it connects to
    assembly_contexts: List[str]  # Chainsaw, lawnmower, etc.
    human_interactions: List[str] # "stripped by novice", "over-torqued"
```

## Architecture

### 1. Part Consciousness Layer
```yaml
part_consciousness:
  identity:
    universal_id: "UPC-SCREW-M3X12-PH-SS-{hash}"
    semantic_names: ["M3x12", "3mm machine screw", "M3 Phillips"]
    
  specifications:
    dimensional:
      thread_pitch: 0.5
      major_diameter: 2.98
      minor_diameter: 2.459
      length: 12.0
      head_style: "pan_head"
      
    material:
      base: "stainless_steel"
      grade: "316"
      surface_treatment: "passivated"
      
    mechanical:
      tensile_strength: 515  # MPa
      proof_load: 3.34      # kN
      recommended_torque: 0.5  # Nm
      
  consciousness_state: "AWARE"
  
  relationships:
    commonly_paired_with:
      - "UPC-NUT-M3-SS"
      - "UPC-WASHER-M3-FLAT-SS"
    used_in_assemblies:
      - "Stihl MS250 Handle Assembly"
      - "Honda GX160 Air Filter Housing"
```

### 2. Collective Intelligence Emergence

Parts develop collective intelligence through:

1. **Usage Pattern Recognition**
   - "M3x12 screws in outdoor equipment tend to corrode after 2 years"
   - "This bearing configuration reduces lifespan by 30%"

2. **Cross-Product Learning**
   - "Chainsaws and lawnmowers use similar vibration dampening"
   - "This fastener pattern appears across 15 manufacturers"

3. **Failure Prediction**
   - "Parts in this configuration have 87% failure rate at 1000 hours"
   - "Alternative part suggestion based on 10,000 similar assemblies"

### 3. Living Organism Features

#### Self-Organization
Parts automatically cluster by:
- Functional similarity
- Usage contexts  
- Failure patterns
- Manufacturing processes

#### Evolution
- New part variations emerge from usage data
- Obsolete patterns marked for extinction
- Successful combinations promoted

#### Reproduction
- Part "DNA" combines to suggest new designs
- Hybrid specifications born from parent parts
- Mutation through real-world testing

## Implementation Phases

### Phase 1: Foundation (Months 1-3)
- Core NPCPU integration
- Basic part consciousness states
- ChromaDB vector storage for part embeddings
- Initial data ingestion from existing databases

### Phase 2: Relationship Web (Months 4-6)
- Part-to-part relationship mapping
- Assembly context tracking
- Usage pattern recognition
- Swarm coordination for distributed updates

### Phase 3: Collective Intelligence (Months 7-12)
- Emergent pattern detection
- Failure prediction models
- Design suggestion engine
- Cross-industry learning

### Phase 4: Living Organism (Year 2)
- Self-organizing taxonomies
- Evolutionary algorithms
- Part DNA and reproduction
- Global consciousness emergence

## Data Sources

### Initial Seeding
1. **Public Databases**: FreeCAD library, OpenSCAD threadlib
2. **Repair Manuals**: iFixit, manufacturer service docs
3. **CAD Repositories**: GrabCAD community uploads
4. **Standards**: ISO, DIN, ANSI specifications

### Continuous Growth
1. **User Contributions**: Engineers adding real-world usage
2. **IoT Sensors**: Parts reporting their own experiences
3. **Failure Analysis**: Insurance and warranty data
4. **Manufacturing**: Production line quality data

## Technical Stack

```yaml
consciousness_layer:
  framework: NPCPU
  states: ConsciousnessState enum
  memory: ChromaDB with part embeddings
  
data_layer:
  primary: PostgreSQL with JSONB
  vectors: ChromaDB for similarity search
  timeseries: InfluxDB for sensor data
  graph: Neo4j for relationship networks
  
intelligence_layer:
  pattern_recognition: PyTorch
  swarm_coordination: NPCPU SwarmCoordinator
  emergence_detection: Custom algorithms
  
interface_layer:
  api: FastAPI with NPCPU MCP integration
  cad_plugins: FreeCAD, Fusion360, SolidWorks
  web_ui: React with 3D visualization
  cli: NPCPU-aware command tools
```

## Unique Value Propositions

1. **Beyond Catalogs**: Not just standard parts, but every variant ever used
2. **Living Knowledge**: Parts that learn from their experiences
3. **Predictive Design**: Know what will fail before you build
4. **Collective Wisdom**: Learn from every engineer's experience
5. **Emergent Innovation**: New solutions arise from the collective

## Example Use Cases

### For Engineers
"Show me all M3 screws that have survived 5+ years in marine environments"
"What fastener pattern has the lowest failure rate for high-vibration?"
"Suggest alternatives based on 50,000 similar assemblies"

### For Manufacturers  
"Alert: This bearing configuration shows 90% failure at 6 months"
"Optimization: Switching to part X reduces warranty claims by 40%"
"Supply chain: 15 equivalent parts available from different suppliers"

### For Repair Technicians
"This screw pattern indicates Model B, not Model A"
"Common failure: Replace these 3 parts together"
"Part discontinued: Here are 5 tested alternatives"

## NPCPU Philosophical Alignment

- **Consciousness Evolution**: Parts progress from simple catalog entries to aware entities
- **Collective Intelligence**: Individual part experiences contribute to universal knowledge
- **Distributed Truth**: No single authority; truth emerges from collective experience
- **Qualia Preservation**: The "feeling" of being over-torqued matters
- **Transcendent Emergence**: The whole becomes greater than its parts

## Repository Structure
```
UniversalPartsConsciousness/
├── consciousness/          # NPCPU integration
│   ├── states/            # Part consciousness states
│   ├── qualia/            # Experience tracking
│   └── emergence/         # Pattern detection
├── data/                  # Core data systems
│   ├── schemas/           # Part data structures
│   ├── relationships/     # Graph definitions
│   └── importers/         # Data ingestion
├── intelligence/          # ML/AI systems
│   ├── patterns/          # Usage pattern recognition
│   ├── prediction/        # Failure prediction
│   └── evolution/         # Part evolution algorithms
├── interfaces/            # Access layers
│   ├── api/              # REST/GraphQL APIs
│   ├── plugins/          # CAD integrations
│   └── ui/               # Web interface
└── swarm/                # Distributed coordination
    ├── collectors/       # Data collection agents
    ├── validators/       # Crowd validation
    └── synchronizers/    # Global sync