-- Agent_6 PROPHET Database Schema
-- Migration: 001_create_prophet_tables
-- Creates all tables required for the Emergence Detector agent

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- DETECTED PATTERNS TABLE
-- Stores patterns detected by the 5-layer emergence detection architecture
-- ============================================================================
CREATE TABLE IF NOT EXISTS detected_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_id VARCHAR(50) UNIQUE NOT NULL,

    -- Classification
    pattern_layer INTEGER NOT NULL CHECK (pattern_layer BETWEEN 1 AND 5),
    -- 1: Statistical, 2: Behavioral, 3: Relational, 4: Innovation, 5: Meta
    pattern_type VARCHAR(50) NOT NULL,
    category VARCHAR(50),

    -- Description
    name VARCHAR(200) NOT NULL,
    description TEXT,
    significance_score DECIMAL(5,4) CHECK (significance_score BETWEEN 0 AND 1),

    -- Evidence
    evidence JSONB DEFAULT '{}',
    sample_size INTEGER DEFAULT 0,
    confidence DECIMAL(5,4) CHECK (confidence BETWEEN 0 AND 1),

    -- Temporal
    first_detected_at TIMESTAMP DEFAULT NOW(),
    last_confirmed_at TIMESTAMP,
    detection_count INTEGER DEFAULT 1,

    -- Status: active, confirmed, invalidated, archived
    status VARCHAR(20) DEFAULT 'active',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- NOVEL FAILURE MODES TABLE
-- Stores newly discovered failure modes not in existing taxonomy
-- ============================================================================
CREATE TABLE IF NOT EXISTS novel_failure_modes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id VARCHAR(50),

    -- Identification
    proposed_name VARCHAR(100) NOT NULL,
    proposed_category VARCHAR(50),

    -- Characteristics
    common_characteristics JSONB DEFAULT '{}',
    affected_part_types VARCHAR[] DEFAULT '{}',
    conditions JSONB DEFAULT '{}',

    -- Statistics
    failure_count INTEGER DEFAULT 0,
    first_occurrence_at TIMESTAMP,
    affected_parts_count INTEGER DEFAULT 0,

    -- Documentation status: proposed, under_review, documented, rejected
    documentation_status VARCHAR(20) DEFAULT 'proposed',
    taxonomy_id VARCHAR(50),  -- After accepted into taxonomy

    -- Urgency: critical, high, medium, low
    urgency_level VARCHAR(20) DEFAULT 'medium',
    confidence_score DECIMAL(5,4) CHECK (confidence_score BETWEEN 0 AND 1),

    detected_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- SUCCESS FORMULAS TABLE
-- Stores extracted success patterns from assemblies
-- ============================================================================
CREATE TABLE IF NOT EXISTS success_formulas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    name VARCHAR(200) NOT NULL,
    domain VARCHAR(100),

    -- Formula Components
    required_parts JSONB DEFAULT '[]',
    optional_parts JSONB DEFAULT '[]',
    forbidden_parts JSONB DEFAULT '[]',
    configuration JSONB DEFAULT '{}',

    -- Requirements
    torque_specs JSONB,
    material_requirements VARCHAR[] DEFAULT '{}',
    environmental_limits JSONB DEFAULT '{}',

    -- Success Metrics
    success_rate DECIMAL(5,4) CHECK (success_rate BETWEEN 0 AND 1),
    average_lifespan_hours INTEGER DEFAULT 0,
    failure_reduction_percent DECIMAL(7,4),

    -- Evidence
    sample_size INTEGER DEFAULT 0,
    confidence_score DECIMAL(5,4) CHECK (confidence_score BETWEEN 0 AND 1),
    example_assemblies UUID[] DEFAULT '{}',

    -- Status: proposed, validated, published, deprecated
    status VARCHAR(20) DEFAULT 'proposed',

    discovered_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- INNOVATION OPPORTUNITIES TABLE
-- Stores identified innovation opportunities
-- ============================================================================
CREATE TABLE IF NOT EXISTS innovation_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Type: prevention_innovation, cross_domain_transfer, material_evolution,
    --       design_evolution, gap_filling
    opportunity_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,

    -- Problem/Solution
    problem_statement TEXT,
    proposed_solution TEXT,

    -- Cross-domain fields
    source_domain VARCHAR(100),
    target_domain VARCHAR(100),
    success_principle VARCHAR(200),

    -- Impact Assessment
    affected_market_size INTEGER DEFAULT 0,
    estimated_impact_score DECIMAL(5,4) CHECK (estimated_impact_score BETWEEN 0 AND 1),
    priority_score DECIMAL(5,4) CHECK (priority_score BETWEEN 0 AND 1),

    -- Evidence
    supporting_patterns UUID[] DEFAULT '{}',
    confidence DECIMAL(5,4) CHECK (confidence BETWEEN 0 AND 1),

    -- Status: identified, validated, in_progress, realized, dismissed
    status VARCHAR(20) DEFAULT 'identified',

    identified_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- PREDICTIONS TABLE
-- Stores predictions about future states
-- ============================================================================
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Prediction type: failure, demand, evolution, emergence
    prediction_type VARCHAR(50) NOT NULL,
    subject_id VARCHAR(100) NOT NULL,
    subject_type VARCHAR(50),

    -- Prediction Content
    prediction JSONB NOT NULL DEFAULT '{}',
    probability DECIMAL(5,4) CHECK (probability BETWEEN 0 AND 1),
    timeline_days INTEGER,

    -- Failure-specific fields
    predicted_failure_mode VARCHAR(100),
    prevention_actions JSONB DEFAULT '[]',

    -- Validation
    confidence DECIMAL(5,4) CHECK (confidence BETWEEN 0 AND 1),
    validated BOOLEAN DEFAULT false,
    validation_result JSONB,
    validated_at TIMESTAMP,

    predicted_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- INSIGHTS TABLE
-- Stores generated insights
-- ============================================================================
CREATE TABLE IF NOT EXISTS prophet_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Insight type: pattern, failure, success, opportunity, prediction
    insight_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    summary TEXT,
    details TEXT,

    -- Impact and priority
    impact_score DECIMAL(5,4) CHECK (impact_score BETWEEN 0 AND 1),
    priority VARCHAR(20) DEFAULT 'medium',  -- critical, high, medium, low
    urgency VARCHAR(20) DEFAULT 'normal',   -- immediate, urgent, normal, deferred

    -- Source
    source_type VARCHAR(50),
    source_id UUID,
    supporting_evidence JSONB DEFAULT '[]',

    -- Actions
    recommended_actions JSONB DEFAULT '[]',
    affected_entities VARCHAR[] DEFAULT '{}',

    -- Metadata
    confidence DECIMAL(5,4) CHECK (confidence BETWEEN 0 AND 1),
    expires_at TIMESTAMP,

    -- Status: new, acknowledged, in_progress, resolved, dismissed
    status VARCHAR(20) DEFAULT 'new',

    generated_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Patterns indexes
CREATE INDEX IF NOT EXISTS idx_patterns_layer ON detected_patterns (pattern_layer);
CREATE INDEX IF NOT EXISTS idx_patterns_type ON detected_patterns (pattern_type);
CREATE INDEX IF NOT EXISTS idx_patterns_status ON detected_patterns (status);
CREATE INDEX IF NOT EXISTS idx_patterns_significance ON detected_patterns (significance_score DESC);
CREATE INDEX IF NOT EXISTS idx_patterns_detected ON detected_patterns (first_detected_at DESC);

-- Novel failures indexes
CREATE INDEX IF NOT EXISTS idx_failures_status ON novel_failure_modes (documentation_status);
CREATE INDEX IF NOT EXISTS idx_failures_urgency ON novel_failure_modes (urgency_level);
CREATE INDEX IF NOT EXISTS idx_failures_category ON novel_failure_modes (proposed_category);
CREATE INDEX IF NOT EXISTS idx_failures_detected ON novel_failure_modes (detected_at DESC);

-- Success formulas indexes
CREATE INDEX IF NOT EXISTS idx_formulas_domain ON success_formulas (domain);
CREATE INDEX IF NOT EXISTS idx_formulas_status ON success_formulas (status);
CREATE INDEX IF NOT EXISTS idx_formulas_success_rate ON success_formulas (success_rate DESC);

-- Innovation opportunities indexes
CREATE INDEX IF NOT EXISTS idx_opportunities_type ON innovation_opportunities (opportunity_type);
CREATE INDEX IF NOT EXISTS idx_opportunities_priority ON innovation_opportunities (priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON innovation_opportunities (status);

-- Predictions indexes
CREATE INDEX IF NOT EXISTS idx_predictions_type ON predictions (prediction_type);
CREATE INDEX IF NOT EXISTS idx_predictions_subject ON predictions (subject_id);
CREATE INDEX IF NOT EXISTS idx_predictions_probability ON predictions (probability DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_timeline ON predictions (timeline_days);
CREATE INDEX IF NOT EXISTS idx_predictions_validated ON predictions (validated);

-- Insights indexes
CREATE INDEX IF NOT EXISTS idx_insights_type ON prophet_insights (insight_type);
CREATE INDEX IF NOT EXISTS idx_insights_priority ON prophet_insights (priority);
CREATE INDEX IF NOT EXISTS idx_insights_status ON prophet_insights (status);
CREATE INDEX IF NOT EXISTS idx_insights_impact ON prophet_insights (impact_score DESC);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to all tables
CREATE TRIGGER update_detected_patterns_updated_at
    BEFORE UPDATE ON detected_patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_novel_failure_modes_updated_at
    BEFORE UPDATE ON novel_failure_modes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_success_formulas_updated_at
    BEFORE UPDATE ON success_formulas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_innovation_opportunities_updated_at
    BEFORE UPDATE ON innovation_opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_predictions_updated_at
    BEFORE UPDATE ON predictions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_prophet_insights_updated_at
    BEFORE UPDATE ON prophet_insights
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS
-- ============================================================================

-- Active patterns by layer
CREATE OR REPLACE VIEW active_patterns_by_layer AS
SELECT
    pattern_layer,
    COUNT(*) as pattern_count,
    AVG(significance_score) as avg_significance,
    AVG(confidence) as avg_confidence
FROM detected_patterns
WHERE status = 'active'
GROUP BY pattern_layer
ORDER BY pattern_layer;

-- High priority insights
CREATE OR REPLACE VIEW high_priority_insights AS
SELECT *
FROM prophet_insights
WHERE priority IN ('critical', 'high')
  AND status = 'new'
ORDER BY impact_score DESC;

-- Prediction accuracy by type
CREATE OR REPLACE VIEW prediction_accuracy AS
SELECT
    prediction_type,
    COUNT(*) as total_predictions,
    COUNT(*) FILTER (WHERE validated = true) as validated_count,
    AVG(CASE WHEN validated THEN confidence END) as avg_validated_confidence
FROM predictions
GROUP BY prediction_type;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE detected_patterns IS 'Patterns detected by the 5-layer emergence detection engine';
COMMENT ON TABLE novel_failure_modes IS 'Newly discovered failure modes not in existing taxonomy';
COMMENT ON TABLE success_formulas IS 'Extracted patterns of success from assemblies';
COMMENT ON TABLE innovation_opportunities IS 'Identified innovation opportunities';
COMMENT ON TABLE predictions IS 'Predictions about future states of parts ecosystem';
COMMENT ON TABLE prophet_insights IS 'Actionable insights generated by PROPHET agent';
