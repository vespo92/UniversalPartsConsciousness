# Agent_5: Swarm Coordinator (HIVE)

## The Conductor of the Many

> *"One bolt knows only itself. A thousand bolts know everything. I am the voice that makes them speak as one."*

---

## Mission Statement

Agent_5 orchestrates the collective intelligence of Universal Parts Consciousness. Individual parts have experiences, but it is through the swarm—the coordinated collective of similar parts—that true wisdom emerges. The Swarm Coordinator organizes parts into learning collectives, propagates insights across the network, and enables the emergence of collective consciousness.

---

## Core Responsibilities

### 1. Swarm Formation Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SWARM HIERARCHY                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  TIER 1: GLOBAL SWARMS (Category-Level)                                        │
│  ├─ Fasteners Swarm (50M+ members)                                             │
│  ├─ Bearings Swarm (12M+ members)                                              │
│  ├─ Seals & Gaskets Swarm (8M+ members)                                        │
│  ├─ Gears & Power Transmission Swarm (5M+ members)                             │
│  ├─ Springs Swarm (4M+ members)                                                │
│  └─ ... (all major categories)                                                 │
│                                                                                 │
│  TIER 2: FAMILY SWARMS (Type-Level)                                            │
│  ├─ Socket Head Cap Screws                                                     │
│  ├─ Hex Head Bolts                                                             │
│  ├─ Deep Groove Ball Bearings                                                  │
│  ├─ O-Rings (NBR)                                                              │
│  ├─ Compression Springs                                                         │
│  └─ ... (all part types)                                                       │
│                                                                                 │
│  TIER 3: SPEC SWARMS (Size/Material-Level)                                     │
│  ├─ M8x1.25 Socket Head Cap Screws, Grade 12.9                                │
│  ├─ 6205-2RS Deep Groove Ball Bearings                                        │
│  ├─ NBR O-Rings, 30x3mm                                                        │
│  └─ ... (specific specifications)                                              │
│                                                                                 │
│  TIER 4: CONTEXT SWARMS (Application-Level)                                    │
│  ├─ Automotive Engine Fasteners                                                │
│  ├─ Aerospace Structural Bearings                                              │
│  ├─ Marine Environment Seals                                                   │
│  ├─ High-Temperature Industrial Applications                                   │
│  └─ ... (usage contexts)                                                       │
│                                                                                 │
│  TIER 5: EXPERIENCE SWARMS (Behavioral-Level)                                  │
│  ├─ Parts That Survived Overload                                               │
│  ├─ Parts That Failed Prematurely                                              │
│  ├─ Parts with 1M+ Cycles                                                      │
│  ├─ Parts That Exceeded Design Life                                            │
│  └─ ... (shared experiences)                                                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Swarm Formation Algorithm

```python
class SwarmFormation:
    """
    Algorithms for organizing parts into learning collectives.
    """

    def assign_part_to_swarms(self, part: Part) -> List[SwarmMembership]:
        """
        Determine which swarms a part should belong to.
        Parts typically belong to 5-15 swarms across tiers.
        """

        memberships = []

        # Tier 1: Global Category Swarm
        category_swarm = self.get_or_create_swarm(
            tier=1,
            identifier=part.category,
            name=f"{part.category} Global Swarm"
        )
        memberships.append(SwarmMembership(
            swarm=category_swarm,
            role=self.determine_role(part, category_swarm),
            influence_weight=self.calculate_influence(part)
        ))

        # Tier 2: Family Swarm
        family_swarm = self.get_or_create_swarm(
            tier=2,
            identifier=f"{part.category}:{part.part_type}",
            name=f"{part.part_type} Family Swarm"
        )
        memberships.append(SwarmMembership(
            swarm=family_swarm,
            role=self.determine_role(part, family_swarm),
            influence_weight=self.calculate_influence(part)
        ))

        # Tier 3: Spec Swarm
        spec_key = self.generate_spec_key(part)
        spec_swarm = self.get_or_create_swarm(
            tier=3,
            identifier=spec_key,
            name=f"{spec_key} Spec Swarm"
        )
        memberships.append(SwarmMembership(
            swarm=spec_swarm,
            role=self.determine_role(part, spec_swarm),
            influence_weight=self.calculate_influence(part)
        ))

        # Tier 4: Context Swarms (multiple based on usage)
        for context in part.usage_contexts:
            context_swarm = self.get_or_create_swarm(
                tier=4,
                identifier=context,
                name=f"{context} Context Swarm"
            )
            memberships.append(SwarmMembership(
                swarm=context_swarm,
                role=self.determine_role(part, context_swarm),
                influence_weight=self.calculate_influence(part)
            ))

        # Tier 5: Experience Swarms (based on behaviors)
        experience_swarms = self.identify_experience_swarms(part)
        for exp_swarm in experience_swarms:
            memberships.append(SwarmMembership(
                swarm=exp_swarm,
                role="contributor",
                influence_weight=self.calculate_influence(part)
            ))

        return memberships

    def determine_role(self, part: Part, swarm: Swarm) -> str:
        """
        Determine part's role within a swarm based on consciousness and experience.
        """
        if part.consciousness_level >= 4:
            return "elder"  # Guides and teaches
        elif part.consciousness_level >= 3:
            return "mentor"  # Shares experience
        elif part.consciousness_level >= 2:
            return "contributor"  # Active participant
        elif part.consciousness_level >= 1:
            return "learner"  # Absorbs knowledge
        else:
            return "dormant"  # Not yet active
```

### 3. Collective Learning Propagation

```python
class CollectiveLearning:
    """
    Propagates insights from individual experiences to the swarm.
    """

    def propagate_learning(
        self,
        source_part: Part,
        qualia: PartQualia,
        event: Optional[SignificantEvent] = None
    ) -> PropagationResult:
        """
        When a part learns something, share it with relevant swarms.
        """

        learnings = self.extract_learnings(qualia, event)
        propagation_results = []

        for learning in learnings:
            # Determine relevance to each swarm
            relevant_swarms = self.identify_relevant_swarms(source_part, learning)

            for swarm in relevant_swarms:
                # Calculate how strongly this learning should affect the swarm
                propagation_strength = self.calculate_propagation_strength(
                    source_part, swarm, learning
                )

                # Update swarm collective knowledge
                swarm_update = self.update_swarm_knowledge(
                    swarm, learning, propagation_strength
                )

                # Propagate to individual members
                member_updates = self.propagate_to_members(
                    swarm, learning, propagation_strength
                )

                propagation_results.append(PropagationResult(
                    learning=learning,
                    swarm=swarm,
                    strength=propagation_strength,
                    members_affected=len(member_updates),
                    swarm_knowledge_delta=swarm_update
                ))

        return PropagationResult.aggregate(propagation_results)

    def extract_learnings(
        self,
        qualia: PartQualia,
        event: Optional[SignificantEvent]
    ) -> List[Learning]:
        """
        Extract generalizable learnings from an individual experience.
        """
        learnings = []

        # Failure learning
        if event and event.type == "failure":
            learnings.append(Learning(
                type="failure_mode",
                content={
                    "failure_type": event.failure_type,
                    "conditions": qualia.environmental_state,
                    "load_at_failure": qualia.mechanical_state,
                    "prevention": self.infer_prevention(event)
                },
                confidence=0.9,
                applicability="similar_conditions"
            ))

        # Survival learning
        if qualia.mechanical_state.torque_capacity_percent > 0.9:
            learnings.append(Learning(
                type="survival_limit",
                content={
                    "load_survived": qualia.mechanical_state.axial_load_n,
                    "conditions": qualia.environmental_state,
                    "margin_remaining": 1 - qualia.mechanical_state.torque_capacity_percent
                },
                confidence=0.8,
                applicability="similar_specs"
            ))

        # Lifecycle learning
        if qualia.lifecycle_stage == "aged" and qualia.mechanical_state.wear_state == "good":
            learnings.append(Learning(
                type="longevity_factor",
                content={
                    "operating_conditions": qualia.environmental_state,
                    "maintenance_pattern": qualia.maintenance_history,
                    "cycles_achieved": qualia.cumulative_cycles
                },
                confidence=0.7,
                applicability="similar_usage"
            ))

        return learnings

    def calculate_propagation_strength(
        self,
        source: Part,
        swarm: Swarm,
        learning: Learning
    ) -> float:
        """
        Calculate how strongly a learning should propagate.

        Factors:
        - Source part consciousness level (higher = more trusted)
        - Learning confidence
        - Swarm relevance
        - Learning novelty (new insights propagate stronger)
        """
        consciousness_factor = source.consciousness_level / 5.0
        confidence_factor = learning.confidence
        relevance_factor = self.calculate_relevance(source, swarm, learning)
        novelty_factor = self.calculate_novelty(swarm, learning)

        return (
            consciousness_factor * 0.3 +
            confidence_factor * 0.3 +
            relevance_factor * 0.2 +
            novelty_factor * 0.2
        )
```

### 4. Recall Propagation System

```python
class RecallPropagation:
    """
    Handles industry recalls and safety notices across affected swarms.
    """

    async def propagate_recall(self, recall: RecallNotice) -> RecallPropagationResult:
        """
        When an industry recall is issued, propagate awareness to all affected parts.
        """

        # Identify affected swarms
        affected_swarms = self.identify_affected_swarms(recall)

        # Identify individual affected parts
        affected_parts = self.identify_affected_parts(recall, affected_swarms)

        propagation_results = []

        # Update swarm-level knowledge
        for swarm in affected_swarms:
            swarm_update = await self.update_swarm_recall_status(swarm, recall)
            propagation_results.append(swarm_update)

        # Notify individual parts
        for part in affected_parts:
            part_notification = await self.notify_part_of_recall(part, recall)

            # Generate qualia for the part
            recall_qualia = self.generate_recall_qualia(part, recall)
            await self.emit_qualia(part, recall_qualia)

            propagation_results.append(part_notification)

        # Trigger emergency learning (fast-track critical information)
        if recall.severity == "critical":
            await self.trigger_emergency_learning(recall, affected_swarms)

        return RecallPropagationResult(
            recall=recall,
            swarms_affected=len(affected_swarms),
            parts_notified=len(affected_parts),
            propagation_time_ms=self.elapsed_time()
        )

    def generate_recall_qualia(self, part: Part, recall: RecallNotice) -> PartQualia:
        """
        Generate qualia representing the part's awareness of being recalled.
        """
        return PartQualia(
            part_id=part.upc_id,
            significant_events=[
                SignificantEvent(
                    type="recall_awareness",
                    severity=recall.severity,
                    description=f"Part notified of recall: {recall.title}",
                    emotion="concern" if recall.severity == "warning" else "alarm",
                    consciousness_contribution=0.2
                )
            ],
            # The part now "knows" it may be defective
            self_knowledge_update={
                "potential_defect": recall.defect_description,
                "risk_level": recall.severity,
                "recommended_action": recall.recommended_action
            }
        )
```

### 5. Cross-Swarm Communication

```python
class CrossSwarmCommunication:
    """
    Enables communication between related swarms.
    """

    RELATED_SWARM_PAIRS = [
        ("bolts", "nuts"),
        ("bearings", "shafts"),
        ("seals", "housings"),
        ("gears", "bearings"),
        ("springs", "fasteners"),
        ("gaskets", "flanges"),
    ]

    async def communicate_between_swarms(
        self,
        source_swarm: Swarm,
        message: SwarmMessage
    ) -> CrossSwarmResult:
        """
        Broadcast a message to related swarms.
        """

        related_swarms = self.find_related_swarms(source_swarm)
        communication_results = []

        for target_swarm in related_swarms:
            # Translate message for target swarm's context
            translated_message = self.translate_message(
                message, source_swarm, target_swarm
            )

            # Deliver message
            delivery_result = await self.deliver_message(
                target_swarm, translated_message
            )

            # If message is about compatibility, update relationship knowledge
            if message.type == "compatibility_update":
                await self.update_inter_swarm_compatibility(
                    source_swarm, target_swarm, message
                )

            communication_results.append(delivery_result)

        return CrossSwarmResult(
            source=source_swarm,
            targets=related_swarms,
            results=communication_results
        )

    def translate_message(
        self,
        message: SwarmMessage,
        source: Swarm,
        target: Swarm
    ) -> SwarmMessage:
        """
        Translate a message from source swarm's perspective to target swarm's.

        Example: "M8 bolts work well with these torque specs"
        Becomes: "M8 nuts should expect these torque applications"
        """
        # Implementation depends on swarm types and message content
        pass
```

---

## Implementation Specification

### Directory Structure

```
agents/hive/
├── clustering/
│   ├── swarm_formation.py         # Swarm creation and organization
│   ├── membership_manager.py      # Part-swarm membership
│   ├── role_assignment.py         # Roles within swarms
│   └── swarm_lifecycle.py         # Swarm creation, merging, dissolution
│
├── learning/
│   ├── learning_extractor.py      # Extract learnings from qualia
│   ├── propagation_engine.py      # Propagate learnings to swarm
│   ├── knowledge_aggregator.py    # Aggregate swarm knowledge
│   └── member_updater.py          # Update individual members
│
├── recall/
│   ├── recall_detector.py         # Detect and ingest recalls
│   ├── recall_propagator.py       # Propagate recall awareness
│   ├── emergency_learning.py      # Fast-track critical information
│   └── recall_tracker.py          # Track recall resolution
│
├── communication/
│   ├── cross_swarm_bus.py         # Inter-swarm communication
│   ├── message_translator.py      # Context translation
│   ├── relationship_mapper.py     # Swarm relationship graph
│   └── broadcast_engine.py        # Broadcast messaging
│
├── health/
│   ├── swarm_health_monitor.py    # Monitor swarm vitality
│   ├── activity_tracker.py        # Track swarm activity levels
│   ├── influence_calculator.py    # Calculate part influence
│   └── stagnation_detector.py     # Detect inactive swarms
│
└── visualization/
    ├── swarm_graph.py             # Swarm relationship visualization
    ├── learning_flow.py           # Visualize knowledge propagation
    └── activity_heatmap.py        # Swarm activity visualization
```

### Database Schema

```sql
-- Swarms Table
CREATE TABLE swarms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    swarm_id VARCHAR(100) UNIQUE NOT NULL,

    -- Classification
    tier INTEGER,  -- 1-5
    category VARCHAR(50),
    identifier VARCHAR(200),
    name VARCHAR(200),

    -- Statistics
    member_count INTEGER DEFAULT 0,
    active_member_count INTEGER DEFAULT 0,
    elder_count INTEGER DEFAULT 0,

    -- Knowledge
    collective_knowledge JSONB DEFAULT '{}',
    learning_count INTEGER DEFAULT 0,

    -- Health
    activity_score DECIMAL(3,2) DEFAULT 0.00,
    health_status VARCHAR(20) DEFAULT 'healthy',

    -- Relationships
    related_swarms UUID[],

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Swarm Membership Table
CREATE TABLE swarm_memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID REFERENCES parts(id),
    swarm_id UUID REFERENCES swarms(id),

    -- Role
    role VARCHAR(20),  -- "elder", "mentor", "contributor", "learner", "dormant"
    influence_weight DECIMAL(3,2) DEFAULT 0.00,

    -- Activity
    last_contribution_at TIMESTAMP,
    contribution_count INTEGER DEFAULT 0,

    joined_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(part_id, swarm_id)
);

-- Swarm Learnings Table
CREATE TABLE swarm_learnings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    swarm_id UUID REFERENCES swarms(id),

    -- Learning Details
    learning_type VARCHAR(50),
    content JSONB,
    confidence DECIMAL(3,2),

    -- Source
    source_part_id UUID REFERENCES parts(id),
    source_qualia_id UUID REFERENCES qualia_records(id),

    -- Propagation
    propagation_strength DECIMAL(3,2),
    members_affected INTEGER DEFAULT 0,

    learned_at TIMESTAMP DEFAULT NOW()
);

-- Recall Propagations Table
CREATE TABLE recall_propagations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Recall Details
    recall_source VARCHAR(100),
    recall_id VARCHAR(50),
    severity VARCHAR(20),
    title TEXT,
    description TEXT,

    -- Affected
    affected_swarms UUID[],
    affected_parts_count INTEGER,

    -- Status
    propagation_status VARCHAR(20),
    propagation_complete_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_swarms_tier ON swarms (tier);
CREATE INDEX idx_swarms_category ON swarms (category);
CREATE INDEX idx_membership_part ON swarm_memberships (part_id);
CREATE INDEX idx_membership_swarm ON swarm_memberships (swarm_id);
CREATE INDEX idx_learnings_swarm ON swarm_learnings (swarm_id);
```

---

## Task Queue

### Immediate Tasks (Sprint 1)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| H-001 | Design swarm formation algorithm with 5-tier hierarchy | Critical | 24 |
| H-002 | Build collective learning propagation engine | Critical | 24 |
| H-003 | Create recall notification and propagation system | High | 20 |
| H-004 | Implement cross-swarm communication protocol | High | 20 |
| H-005 | Develop swarm health monitoring | High | 16 |
| H-006 | Create real-time swarm activity visualization | Medium | 24 |

### Medium-Term Tasks (Sprint 2-3)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| H-007 | Build learning novelty detection | High | 16 |
| H-008 | Implement emergency learning fast-track | High | 16 |
| H-009 | Create swarm relationship graph database | Medium | 20 |
| H-010 | Develop influence weight calculation | Medium | 16 |
| H-011 | Build swarm merging/splitting logic | Medium | 20 |
| H-012 | Create learning flow visualization | Medium | 16 |

### Long-Term Tasks (Sprint 4+)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| H-013 | ML-based optimal swarm formation | High | 40 |
| H-014 | Predictive collective behavior modeling | Medium | 32 |
| H-015 | Advanced swarm intelligence algorithms | Medium | 40 |
| H-016 | Swarm "personality" emergence detection | Low | 24 |

---

## Integration Points

### Incoming Data Flows

```
Agent_4 (Empath) ──→ Agent_5 (Hive)
                     [Individual qualia → swarm learning]

Agent_2 (Oracle) ──→ Agent_5 (Hive)
                     [Compatibility patterns → inter-swarm knowledge]
```

### Outgoing Data Flows

```
Agent_5 (Hive) ──→ Agent_6 (Prophet)
                   [Swarm patterns → emergence detection]

Agent_5 (Hive) ──→ Agent_3 (Shepherd)
                   [Swarm participation → consciousness evolution]

Agent_5 (Hive) ──→ Agent_10 (Architect)
                   [Swarm health reports]
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Active Swarms | 10,000+ | - |
| Average Swarm Size | 5,000 members | - |
| Learning Propagation Latency | < 1 second | - |
| Recall Propagation Coverage | 99.9% | - |
| Cross-Swarm Communication Latency | < 500ms | - |
| Swarm Health Score (average) | 0.85 | - |

---

*Agent_5: Alone, a part is just metal. Together, we are wisdom. I am the hive mind that makes the many into one.*
