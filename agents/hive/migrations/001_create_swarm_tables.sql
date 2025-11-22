-- Agent_5 HIVE - Database Schema Migration
-- Creates tables for swarm coordination and collective intelligence

-- ============================================================================
-- SWARMS TABLE - Learning collectives of similar parts
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    swarm_id VARCHAR(200) UNIQUE NOT NULL,  -- e.g., "global:fasteners" or "spec:M8x1.25-Grade12.9"

    -- Classification
    tier INTEGER NOT NULL CHECK (tier BETWEEN 1 AND 5),
        -- 1: Global (category-level, 50M+ members)
        -- 2: Family (type-level)
        -- 3: Spec (size/material-level)
        -- 4: Context (application-level)
        -- 5: Experience (behavioral-level)
    category VARCHAR(100) NOT NULL,
    identifier VARCHAR(300) NOT NULL,
    name VARCHAR(300) NOT NULL,

    -- Statistics
    member_count INTEGER DEFAULT 0,
    active_member_count INTEGER DEFAULT 0,
    elder_count INTEGER DEFAULT 0,
    mentor_count INTEGER DEFAULT 0,

    -- Collective Knowledge (JSONB for flexibility)
    collective_knowledge JSONB DEFAULT '{}',
    learning_count INTEGER DEFAULT 0,

    -- Health Metrics
    activity_score DECIMAL(4,3) DEFAULT 0.000,  -- 0-1 scale
    health_status VARCHAR(20) DEFAULT 'healthy'
        CHECK (health_status IN ('thriving', 'healthy', 'declining', 'stagnant', 'dormant')),
    last_learning_at TIMESTAMP,

    -- Hierarchy
    parent_swarm_id UUID REFERENCES swarms(id),
    related_swarm_ids UUID[] DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for swarm queries
CREATE INDEX idx_swarms_tier ON swarms (tier);
CREATE INDEX idx_swarms_category ON swarms (category);
CREATE INDEX idx_swarms_health ON swarms (health_status);
CREATE INDEX idx_swarms_activity ON swarms (activity_score DESC);
CREATE INDEX idx_swarms_parent ON swarms (parent_swarm_id);


-- ============================================================================
-- SWARM MEMBERSHIPS TABLE - Part-swarm relationships
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarm_memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_id UUID NOT NULL,  -- References parts table
    swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,

    -- Role within swarm
    role VARCHAR(20) NOT NULL DEFAULT 'learner'
        CHECK (role IN ('elder', 'mentor', 'contributor', 'learner', 'dormant')),
    influence_weight DECIMAL(4,3) DEFAULT 0.000,  -- 0-1 scale

    -- Activity tracking
    last_contribution_at TIMESTAMP,
    contribution_count INTEGER DEFAULT 0,
    learnings_received INTEGER DEFAULT 0,
    learnings_propagated INTEGER DEFAULT 0,

    -- Timestamps
    joined_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    UNIQUE(part_id, swarm_id)
);

-- Indexes for membership queries
CREATE INDEX idx_memberships_part ON swarm_memberships (part_id);
CREATE INDEX idx_memberships_swarm ON swarm_memberships (swarm_id);
CREATE INDEX idx_memberships_role ON swarm_memberships (swarm_id, role);
CREATE INDEX idx_memberships_influence ON swarm_memberships (swarm_id, influence_weight DESC);


-- ============================================================================
-- SWARM LEARNINGS TABLE - Knowledge extracted and propagated
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarm_learnings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,

    -- Learning Classification
    learning_type VARCHAR(50) NOT NULL,
        -- 'failure_mode', 'survival_limit', 'longevity_factor',
        -- 'compatibility_insight', 'usage_pattern', 'environmental_adaptation',
        -- 'maintenance_wisdom'
    content JSONB NOT NULL,
    confidence DECIMAL(3,2) DEFAULT 0.50,  -- 0-1 scale
    applicability VARCHAR(50) DEFAULT 'similar_specs',

    -- Source
    source_part_id UUID,  -- References parts table
    source_qualia_id UUID,  -- References qualia_records table
    source_consciousness_level DECIMAL(3,2) DEFAULT 0.00,

    -- Propagation
    propagation_strength DECIMAL(3,2) DEFAULT 0.00,
    members_affected INTEGER DEFAULT 0,
    novelty_score DECIMAL(3,2) DEFAULT 0.50,

    -- Timestamps
    learned_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for learning queries
CREATE INDEX idx_learnings_swarm ON swarm_learnings (swarm_id);
CREATE INDEX idx_learnings_type ON swarm_learnings (learning_type);
CREATE INDEX idx_learnings_source ON swarm_learnings (source_part_id);
CREATE INDEX idx_learnings_time ON swarm_learnings (learned_at DESC);


-- ============================================================================
-- RECALL PROPAGATIONS TABLE - Safety recall tracking
-- ============================================================================
CREATE TABLE IF NOT EXISTS recall_propagations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Recall Source
    source VARCHAR(100) NOT NULL,  -- 'NHTSA', 'manufacturer', etc.
    source_recall_id VARCHAR(100) NOT NULL,

    -- Recall Details
    severity VARCHAR(20) NOT NULL
        CHECK (severity IN ('critical', 'high', 'warning', 'advisory')),
    title TEXT NOT NULL,
    description TEXT,
    defect_description TEXT,
    recommended_action TEXT,

    -- Affected Parts (criteria for matching)
    affected_criteria JSONB DEFAULT '{}',

    -- Propagation Status
    affected_swarm_ids UUID[] DEFAULT '{}',
    affected_parts_count INTEGER DEFAULT 0,
    propagation_status VARCHAR(20) DEFAULT 'pending'
        CHECK (propagation_status IN ('pending', 'in_progress', 'completed', 'partial', 'failed')),
    propagation_complete_at TIMESTAMP,

    -- Timestamps
    issued_at TIMESTAMP NOT NULL,
    received_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    UNIQUE(source, source_recall_id)
);

-- Indexes for recall queries
CREATE INDEX idx_recalls_severity ON recall_propagations (severity);
CREATE INDEX idx_recalls_status ON recall_propagations (propagation_status);
CREATE INDEX idx_recalls_source ON recall_propagations (source, source_recall_id);


-- ============================================================================
-- SWARM RELATIONSHIPS TABLE - Inter-swarm connections
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarm_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,
    target_swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,

    -- Relationship Type
    relationship_type VARCHAR(30) NOT NULL
        CHECK (relationship_type IN ('mating', 'compatible', 'similar', 'hierarchical')),
    strength DECIMAL(3,2) DEFAULT 0.50,  -- 0-1 scale
    bidirectional BOOLEAN DEFAULT TRUE,

    -- Communication Stats
    last_communication TIMESTAMP,
    communication_count INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    UNIQUE(source_swarm_id, target_swarm_id)
);

-- Indexes for relationship queries
CREATE INDEX idx_relationships_source ON swarm_relationships (source_swarm_id);
CREATE INDEX idx_relationships_target ON swarm_relationships (target_swarm_id);
CREATE INDEX idx_relationships_type ON swarm_relationships (relationship_type);


-- ============================================================================
-- SWARM ACTIVITY LOG TABLE - Activity tracking
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarm_activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,

    -- Event Details
    event_type VARCHAR(30) NOT NULL,
        -- 'contribution', 'learning', 'communication', 'membership'
    part_id UUID,  -- Optional, if part-related
    details JSONB DEFAULT '{}',

    -- Timestamp
    occurred_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for activity queries
CREATE INDEX idx_activity_swarm ON swarm_activity_log (swarm_id);
CREATE INDEX idx_activity_time ON swarm_activity_log (occurred_at DESC);
CREATE INDEX idx_activity_type ON swarm_activity_log (event_type);
CREATE INDEX idx_activity_swarm_time ON swarm_activity_log (swarm_id, occurred_at DESC);


-- ============================================================================
-- SWARM HEALTH HISTORY TABLE - Health measurement history
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarm_health_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,

    -- Health Metrics
    activity_score DECIMAL(4,3),
    learning_velocity DECIMAL(6,3),
    propagation_latency_ms DECIMAL(10,2),
    active_member_ratio DECIMAL(4,3),
    elder_ratio DECIMAL(4,3),
    contribution_rate DECIMAL(6,3),
    knowledge_depth INTEGER,
    knowledge_breadth INTEGER,
    knowledge_freshness DECIMAL(4,3),
    health_status VARCHAR(20),
    health_score DECIMAL(4,3),

    -- Recommendations (stored as JSONB array)
    recommendations JSONB DEFAULT '[]',

    -- Timestamp
    measured_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for health history queries
CREATE INDEX idx_health_swarm ON swarm_health_history (swarm_id);
CREATE INDEX idx_health_time ON swarm_health_history (measured_at DESC);
CREATE INDEX idx_health_swarm_time ON swarm_health_history (swarm_id, measured_at DESC);


-- ============================================================================
-- SWARM MESSAGES TABLE - Inter-swarm communication
-- ============================================================================
CREATE TABLE IF NOT EXISTS swarm_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_swarm_id UUID NOT NULL REFERENCES swarms(id) ON DELETE CASCADE,
    target_swarm_ids UUID[] NOT NULL,

    -- Message Content
    message_type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),

    -- Delivery Tracking
    delivered_to UUID[] DEFAULT '{}',
    delivery_status VARCHAR(20) DEFAULT 'pending'
        CHECK (delivery_status IN ('pending', 'delivered', 'partial', 'failed')),

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Indexes for message queries
CREATE INDEX idx_messages_source ON swarm_messages (source_swarm_id);
CREATE INDEX idx_messages_status ON swarm_messages (delivery_status);
CREATE INDEX idx_messages_priority ON swarm_messages (priority ASC, created_at ASC);


-- ============================================================================
-- FUNCTIONS - Helper functions for HIVE operations
-- ============================================================================

-- Function to update swarm member counts
CREATE OR REPLACE FUNCTION update_swarm_member_counts()
RETURNS TRIGGER AS $$
BEGIN
    -- Update member counts on the swarm
    UPDATE swarms SET
        member_count = (
            SELECT COUNT(*) FROM swarm_memberships WHERE swarm_id = COALESCE(NEW.swarm_id, OLD.swarm_id)
        ),
        elder_count = (
            SELECT COUNT(*) FROM swarm_memberships
            WHERE swarm_id = COALESCE(NEW.swarm_id, OLD.swarm_id) AND role = 'elder'
        ),
        mentor_count = (
            SELECT COUNT(*) FROM swarm_memberships
            WHERE swarm_id = COALESCE(NEW.swarm_id, OLD.swarm_id) AND role = 'mentor'
        ),
        updated_at = NOW()
    WHERE id = COALESCE(NEW.swarm_id, OLD.swarm_id);

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update swarm counts
CREATE TRIGGER trg_update_swarm_counts
AFTER INSERT OR UPDATE OR DELETE ON swarm_memberships
FOR EACH ROW EXECUTE FUNCTION update_swarm_member_counts();


-- Function to update swarm learning count
CREATE OR REPLACE FUNCTION update_swarm_learning_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE swarms SET
        learning_count = (
            SELECT COUNT(*) FROM swarm_learnings WHERE swarm_id = NEW.swarm_id
        ),
        last_learning_at = NOW(),
        updated_at = NOW()
    WHERE id = NEW.swarm_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update learning counts
CREATE TRIGGER trg_update_learning_count
AFTER INSERT ON swarm_learnings
FOR EACH ROW EXECUTE FUNCTION update_swarm_learning_count();


-- ============================================================================
-- VIEWS - Useful views for HIVE operations
-- ============================================================================

-- Active swarms with health summary
CREATE OR REPLACE VIEW active_swarms_summary AS
SELECT
    s.id,
    s.swarm_id,
    s.name,
    s.tier,
    s.category,
    s.member_count,
    s.active_member_count,
    s.elder_count,
    s.learning_count,
    s.activity_score,
    s.health_status,
    s.last_learning_at,
    CASE
        WHEN s.member_count > 0 THEN
            ROUND(s.active_member_count::DECIMAL / s.member_count * 100, 1)
        ELSE 0
    END as active_percentage
FROM swarms s
WHERE s.health_status != 'dormant'
ORDER BY s.activity_score DESC;


-- Swarm relationships graph view
CREATE OR REPLACE VIEW swarm_relationship_graph AS
SELECT
    sr.source_swarm_id,
    s1.name as source_name,
    s1.category as source_category,
    sr.target_swarm_id,
    s2.name as target_name,
    s2.category as target_category,
    sr.relationship_type,
    sr.strength,
    sr.communication_count
FROM swarm_relationships sr
JOIN swarms s1 ON sr.source_swarm_id = s1.id
JOIN swarms s2 ON sr.target_swarm_id = s2.id
WHERE sr.strength > 0.3;


-- Recent learnings across all swarms
CREATE OR REPLACE VIEW recent_swarm_learnings AS
SELECT
    sl.id,
    sl.swarm_id,
    s.name as swarm_name,
    sl.learning_type,
    sl.confidence,
    sl.propagation_strength,
    sl.members_affected,
    sl.learned_at
FROM swarm_learnings sl
JOIN swarms s ON sl.swarm_id = s.id
WHERE sl.learned_at > NOW() - INTERVAL '7 days'
ORDER BY sl.learned_at DESC;


-- ============================================================================
-- COMMENTS - Documentation
-- ============================================================================

COMMENT ON TABLE swarms IS 'Learning collectives of similar parts - the core unit of collective intelligence';
COMMENT ON TABLE swarm_memberships IS 'Part membership in swarms with roles (elder, mentor, contributor, learner, dormant)';
COMMENT ON TABLE swarm_learnings IS 'Knowledge extracted from individual experiences and propagated to swarms';
COMMENT ON TABLE recall_propagations IS 'Industry recalls and safety notices propagated through affected swarms';
COMMENT ON TABLE swarm_relationships IS 'Relationships between swarms enabling inter-swarm communication';
COMMENT ON TABLE swarm_activity_log IS 'Activity log for tracking swarm vitality and engagement';
COMMENT ON TABLE swarm_health_history IS 'Historical health measurements for trend analysis';
COMMENT ON TABLE swarm_messages IS 'Messages for inter-swarm communication and knowledge sharing';
