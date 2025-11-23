-- Universal Parts Database - Showcases & Cross-References Schema
-- This schema enables the core UPC value proposition: tracking real-world
-- parts compatibility across different manufacturers and platforms.
-- Run this AFTER schema.sql

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- ENGINEERING SHOWCASES
-- Real-world projects that demonstrate parts compatibility (Tesla/Lotus, etc.)
-- =============================================================================

CREATE TABLE IF NOT EXISTS showcases (
    showcase_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Platform information (donor/recipient in a swap scenario)
    source_platform JSONB NOT NULL,  -- {manufacturer, model, years[], production_location[]}
    target_platform JSONB,           -- Optional for single-platform showcases

    -- Compatibility metrics
    overall_compatibility_score DECIMAL(3,2) CHECK (overall_compatibility_score >= 0 AND overall_compatibility_score <= 1),
    component_groups_count INTEGER DEFAULT 0,
    verified_cross_refs_count INTEGER DEFAULT 0,

    -- Metadata
    category VARCHAR(50),  -- automotive, aerospace, agricultural, electronics, etc.
    tags TEXT[],

    -- Economic analysis
    economic_analysis JSONB,  -- {avg_savings_percent, source_cost, target_cost}

    -- Lessons learned
    lessons_learned TEXT[],

    -- Status and verification
    verification_level VARCHAR(20) DEFAULT 'unverified',
    last_verified TIMESTAMPTZ,
    verified_by UUID REFERENCES auth.users(id),

    -- Source tracking
    data_source VARCHAR(255),  -- URL, forum thread, engineering document
    source_date DATE,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

CREATE INDEX IF NOT EXISTS idx_showcase_category ON showcases(category);
CREATE INDEX IF NOT EXISTS idx_showcase_tags ON showcases USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_showcase_source ON showcases USING GIN(source_platform);
CREATE INDEX IF NOT EXISTS idx_showcase_target ON showcases USING GIN(target_platform);

-- =============================================================================
-- CROSS-REFERENCES
-- The core of UPC: "What can I use instead of this part?"
-- =============================================================================

CREATE TYPE compatibility_type AS ENUM (
    'direct_replacement',      -- Drop-in, no modifications
    'functional_equivalent',   -- Same function, minor differences
    'upgrade',                 -- Better performance/quality
    'downgrade',              -- Reduced capability but fits
    'requires_adapter',        -- Needs adapter kit
    'requires_modification',   -- Custom work needed
    'emergency_substitute'     -- Get-home only, not recommended
);

CREATE TYPE verification_level AS ENUM (
    'unverified',             -- Just claimed, not tested
    'community_tested',       -- Multiple community reports
    'expert_verified',        -- Professional mechanic/engineer confirmed
    'manufacturer_confirmed', -- OEM documentation
    'standard_compliant'      -- ISO/SAE/MIL standard
);

CREATE TABLE IF NOT EXISTS cross_references (
    xref_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Source part (the part you have or want to replace)
    source_part_number VARCHAR(100) NOT NULL,
    source_manufacturer VARCHAR(100),
    source_part_id VARCHAR(100) REFERENCES parts(part_id),

    -- Target part (the compatible alternative)
    target_part_number VARCHAR(100) NOT NULL,
    target_manufacturer VARCHAR(100),
    target_part_id VARCHAR(100) REFERENCES parts(part_id),

    -- Compatibility assessment
    compatibility_score DECIMAL(3,2) NOT NULL CHECK (compatibility_score >= 0 AND compatibility_score <= 1),
    compatibility_type compatibility_type NOT NULL DEFAULT 'functional_equivalent',

    -- Verification status
    verification_level verification_level DEFAULT 'unverified',
    verified_by UUID REFERENCES auth.users(id),
    verified_at TIMESTAMPTZ,

    -- Modifications and adapters needed
    modifications_required TEXT[],
    adapter_parts TEXT[],  -- Part numbers of required adapters

    -- Warnings and notes
    warnings TEXT[],
    notes TEXT,

    -- Success/failure tracking
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_reported TIMESTAMPTZ,

    -- Price comparison (optional)
    source_price_usd DECIMAL(10,2),
    target_price_usd DECIMAL(10,2),
    price_date DATE,

    -- Relationship to showcase (if part of a documented project)
    showcase_id VARCHAR(50) REFERENCES showcases(showcase_id),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id),

    -- Ensure uniqueness of source-target pairs
    UNIQUE(source_part_number, target_part_number, source_manufacturer, target_manufacturer)
);

-- Critical indexes for fast cross-reference lookups
CREATE INDEX IF NOT EXISTS idx_xref_source_pn ON cross_references(source_part_number);
CREATE INDEX IF NOT EXISTS idx_xref_source_mfr ON cross_references(source_manufacturer);
CREATE INDEX IF NOT EXISTS idx_xref_target_pn ON cross_references(target_part_number);
CREATE INDEX IF NOT EXISTS idx_xref_target_mfr ON cross_references(target_manufacturer);
CREATE INDEX IF NOT EXISTS idx_xref_score ON cross_references(compatibility_score DESC);
CREATE INDEX IF NOT EXISTS idx_xref_type ON cross_references(compatibility_type);
CREATE INDEX IF NOT EXISTS idx_xref_showcase ON cross_references(showcase_id);

-- Full-text search on part numbers
CREATE INDEX IF NOT EXISTS idx_xref_source_fts ON cross_references
    USING GIN(to_tsvector('english', source_part_number || ' ' || COALESCE(source_manufacturer, '')));
CREATE INDEX IF NOT EXISTS idx_xref_target_fts ON cross_references
    USING GIN(to_tsvector('english', target_part_number || ' ' || COALESCE(target_manufacturer, '')));

-- =============================================================================
-- QUALIA (EXPERIENTIAL KNOWLEDGE)
-- Community-sourced experiences with cross-references
-- =============================================================================

CREATE TABLE IF NOT EXISTS cross_reference_qualia (
    qualia_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    xref_id UUID NOT NULL REFERENCES cross_references(xref_id) ON DELETE CASCADE,

    -- Source of the experience
    source VARCHAR(255) NOT NULL,  -- Forum URL, shop name, etc.
    source_date DATE,
    source_user VARCHAR(100),

    -- The experience itself
    content TEXT NOT NULL,
    sentiment VARCHAR(20) CHECK (sentiment IN ('positive', 'neutral', 'negative', 'warning')),

    -- Application context
    application_context VARCHAR(255),  -- "2008 Mazda Miata LS swap"
    vehicle_or_equipment VARCHAR(255),
    mileage_or_hours INTEGER,

    -- Community validation
    verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES auth.users(id),
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

CREATE INDEX IF NOT EXISTS idx_qualia_xref ON cross_reference_qualia(xref_id);
CREATE INDEX IF NOT EXISTS idx_qualia_sentiment ON cross_reference_qualia(sentiment);
CREATE INDEX IF NOT EXISTS idx_qualia_verified ON cross_reference_qualia(verified);

-- =============================================================================
-- FASTENER REQUIREMENTS
-- Detailed fastener specifications for swap/compatibility projects
-- =============================================================================

CREATE TABLE IF NOT EXISTS showcase_fasteners (
    fastener_req_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    showcase_id VARCHAR(50) REFERENCES showcases(showcase_id) ON DELETE CASCADE,

    -- Component context
    component_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,

    -- Fastener specification
    fastener_spec VARCHAR(100) NOT NULL,  -- "M8x1.25-10.9"
    fastener_standard VARCHAR(20),         -- ISO, DIN, AN, MS
    length_mm DECIMAL(10,2),
    quantity INTEGER NOT NULL DEFAULT 1,

    -- Installation specs
    torque_nm DECIMAL(10,2),
    torque_ftlb DECIMAL(10,2),
    torque_inlb DECIMAL(10,2),
    torque_sequence TEXT,
    thread_locker VARCHAR(50),  -- "Loctite 243", "none", "anti-seize"

    -- Warnings and notes
    warnings TEXT[],
    notes TEXT,

    -- Link to parts table if we have detailed specs
    part_id VARCHAR(100) REFERENCES parts(part_id),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sfastener_showcase ON showcase_fasteners(showcase_id);
CREATE INDEX IF NOT EXISTS idx_sfastener_spec ON showcase_fasteners(fastener_spec);
CREATE INDEX IF NOT EXISTS idx_sfastener_component ON showcase_fasteners(component_name);

-- =============================================================================
-- SWAP GUIDES
-- Complete swap documentation generated from showcases and cross-references
-- =============================================================================

CREATE TABLE IF NOT EXISTS swap_guides (
    guide_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- What's being swapped
    source_platform VARCHAR(255) NOT NULL,
    target_platform VARCHAR(255) NOT NULL,
    swap_type VARCHAR(100),  -- "engine swap", "suspension upgrade", "parts interchange"

    -- Guide content
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    difficulty VARCHAR(20) CHECK (difficulty IN ('beginner', 'intermediate', 'advanced', 'expert')),
    estimated_hours INTEGER,
    estimated_cost_usd DECIMAL(10,2),

    -- Guide document (markdown)
    content_md TEXT,

    -- Related data
    showcase_id VARCHAR(50) REFERENCES showcases(showcase_id),

    -- Community stats
    success_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) CHECK (rating >= 0 AND rating <= 5),
    rating_count INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

CREATE INDEX IF NOT EXISTS idx_guide_source ON swap_guides(source_platform);
CREATE INDEX IF NOT EXISTS idx_guide_target ON swap_guides(target_platform);
CREATE INDEX IF NOT EXISTS idx_guide_type ON swap_guides(swap_type);
CREATE INDEX IF NOT EXISTS idx_guide_status ON swap_guides(status);

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

-- View: Find all cross-references with high compatibility
CREATE OR REPLACE VIEW v_high_compatibility_xrefs AS
SELECT
    xr.xref_id,
    xr.source_part_number,
    xr.source_manufacturer,
    xr.target_part_number,
    xr.target_manufacturer,
    xr.compatibility_score,
    xr.compatibility_type,
    xr.verification_level,
    xr.success_count,
    xr.failure_count,
    CASE WHEN (xr.success_count + xr.failure_count) > 0
         THEN xr.success_count::DECIMAL / (xr.success_count + xr.failure_count)
         ELSE 0 END AS success_rate,
    s.title AS showcase_title
FROM cross_references xr
LEFT JOIN showcases s ON xr.showcase_id = s.showcase_id
WHERE xr.compatibility_score >= 0.8
ORDER BY xr.compatibility_score DESC, xr.success_count DESC;

-- View: Cross-reference summary with qualia counts
CREATE OR REPLACE VIEW v_xref_with_qualia AS
SELECT
    xr.*,
    COUNT(q.qualia_id) AS qualia_count,
    COUNT(CASE WHEN q.sentiment = 'positive' THEN 1 END) AS positive_count,
    COUNT(CASE WHEN q.sentiment = 'negative' THEN 1 END) AS negative_count,
    COUNT(CASE WHEN q.sentiment = 'warning' THEN 1 END) AS warning_count
FROM cross_references xr
LEFT JOIN cross_reference_qualia q ON xr.xref_id = q.xref_id
GROUP BY xr.xref_id;

-- View: Showcase summary
CREATE OR REPLACE VIEW v_showcase_summary AS
SELECT
    s.showcase_id,
    s.title,
    s.category,
    s.overall_compatibility_score,
    s.source_platform->>'manufacturer' AS source_mfr,
    s.source_platform->>'model' AS source_model,
    s.target_platform->>'manufacturer' AS target_mfr,
    s.target_platform->>'model' AS target_model,
    COUNT(DISTINCT xr.xref_id) AS cross_reference_count,
    COUNT(DISTINCT sf.fastener_req_id) AS fastener_spec_count,
    s.verification_level,
    s.created_at
FROM showcases s
LEFT JOIN cross_references xr ON s.showcase_id = xr.showcase_id
LEFT JOIN showcase_fasteners sf ON s.showcase_id = sf.showcase_id
GROUP BY s.showcase_id;

-- =============================================================================
-- FUNCTIONS FOR CROSS-REFERENCE QUERIES
-- =============================================================================

-- Function: Find all compatible parts for a given part number
CREATE OR REPLACE FUNCTION find_compatible_parts(
    p_part_number VARCHAR,
    p_manufacturer VARCHAR DEFAULT NULL,
    p_min_score DECIMAL DEFAULT 0.5
)
RETURNS TABLE (
    part_number VARCHAR,
    manufacturer VARCHAR,
    compatibility_score DECIMAL,
    compatibility_type compatibility_type,
    verification_level verification_level,
    modifications_required TEXT[],
    success_rate DECIMAL,
    qualia_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        xr.target_part_number,
        xr.target_manufacturer,
        xr.compatibility_score,
        xr.compatibility_type,
        xr.verification_level,
        xr.modifications_required,
        CASE WHEN (xr.success_count + xr.failure_count) > 0
             THEN xr.success_count::DECIMAL / (xr.success_count + xr.failure_count)
             ELSE NULL END,
        (SELECT COUNT(*) FROM cross_reference_qualia q WHERE q.xref_id = xr.xref_id)
    FROM cross_references xr
    WHERE UPPER(xr.source_part_number) LIKE UPPER('%' || p_part_number || '%')
      AND (p_manufacturer IS NULL OR UPPER(xr.source_manufacturer) LIKE UPPER('%' || p_manufacturer || '%'))
      AND xr.compatibility_score >= p_min_score

    UNION

    -- Also search target parts (bidirectional compatibility)
    SELECT
        xr.source_part_number,
        xr.source_manufacturer,
        xr.compatibility_score,
        xr.compatibility_type,
        xr.verification_level,
        xr.modifications_required,
        CASE WHEN (xr.success_count + xr.failure_count) > 0
             THEN xr.success_count::DECIMAL / (xr.success_count + xr.failure_count)
             ELSE NULL END,
        (SELECT COUNT(*) FROM cross_reference_qualia q WHERE q.xref_id = xr.xref_id)
    FROM cross_references xr
    WHERE UPPER(xr.target_part_number) LIKE UPPER('%' || p_part_number || '%')
      AND (p_manufacturer IS NULL OR UPPER(xr.target_manufacturer) LIKE UPPER('%' || p_manufacturer || '%'))
      AND xr.compatibility_score >= p_min_score

    ORDER BY compatibility_score DESC;
END;
$$ LANGUAGE plpgsql;

-- Function: Record a cross-reference usage (success or failure)
CREATE OR REPLACE FUNCTION record_xref_usage(
    p_xref_id UUID,
    p_success BOOLEAN,
    p_context VARCHAR DEFAULT NULL,
    p_notes TEXT DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    -- Update success/failure counts
    IF p_success THEN
        UPDATE cross_references
        SET success_count = success_count + 1,
            last_reported = NOW()
        WHERE xref_id = p_xref_id;
    ELSE
        UPDATE cross_references
        SET failure_count = failure_count + 1,
            last_reported = NOW()
        WHERE xref_id = p_xref_id;
    END IF;

    -- Optionally add qualia entry
    IF p_notes IS NOT NULL THEN
        INSERT INTO cross_reference_qualia (xref_id, source, content, sentiment, application_context)
        VALUES (
            p_xref_id,
            'user_report',
            p_notes,
            CASE WHEN p_success THEN 'positive' ELSE 'negative' END,
            p_context
        );
    END IF;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- TRIGGERS FOR AUTO-UPDATE
-- =============================================================================

-- Trigger to update showcase cross_ref count when cross_references change
CREATE OR REPLACE FUNCTION update_showcase_xref_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE showcases
        SET verified_cross_refs_count = verified_cross_refs_count + 1
        WHERE showcase_id = NEW.showcase_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE showcases
        SET verified_cross_refs_count = verified_cross_refs_count - 1
        WHERE showcase_id = OLD.showcase_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_update_showcase_xref_count
AFTER INSERT OR DELETE ON cross_references
FOR EACH ROW
WHEN (NEW.showcase_id IS NOT NULL OR OLD.showcase_id IS NOT NULL)
EXECUTE FUNCTION update_showcase_xref_count();

-- Trigger to update timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_showcases_timestamp
BEFORE UPDATE ON showcases
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER tr_cross_references_timestamp
BEFORE UPDATE ON cross_references
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER tr_showcase_fasteners_timestamp
BEFORE UPDATE ON showcase_fasteners
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER tr_swap_guides_timestamp
BEFORE UPDATE ON swap_guides
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- =============================================================================
-- SAMPLE DATA - Tesla/Lotus Showcase
-- =============================================================================

-- Insert the Tesla/Lotus showcase
INSERT INTO showcases (
    showcase_id,
    title,
    description,
    source_platform,
    target_platform,
    overall_compatibility_score,
    category,
    tags,
    lessons_learned,
    verification_level,
    data_source
) VALUES (
    'SHOWCASE-001',
    'Tesla Roadster / Lotus Elise Parts Compatibility',
    'Cross-platform parts sharing between Tesla''s first EV and its donor Lotus platform. A landmark example of startup-to-OEM parts adaptation.',
    '{"manufacturer": "Lotus", "model": "Elise", "years": [2005, 2006, 2007], "generation": "Series 2", "production_location": ["UK", "Malaysia"]}',
    '{"manufacturer": "Tesla", "model": "Roadster", "years": [2008, 2009, 2010, 2011, 2012], "generation": "1.0, 1.5, 2.0, 2.5", "production_location": ["UK"]}',
    0.68,
    'automotive',
    ARRAY['electric vehicle', 'sports car', 'platform sharing', 'startup engineering'],
    ARRAY[
        'Cross-platform parts sharing is common but poorly documented',
        'Manufacturing tolerance variations exist within same part numbers',
        'Supplier information is valuable but often hidden',
        'Community knowledge fills gaps manufacturers won''t share',
        'Price arbitrage opportunities exist between OEM sources'
    ],
    'expert_verified',
    'teslamotorsclub.com, lotustalk.com, engineering documentation'
) ON CONFLICT (showcase_id) DO NOTHING;

-- Insert some cross-references from the showcase
INSERT INTO cross_references (
    source_part_number, source_manufacturer,
    target_part_number, target_manufacturer,
    compatibility_score, compatibility_type, verification_level,
    showcase_id, notes
) VALUES
(
    'A117C0035F', 'Lotus',
    'TR-SUS-001', 'Tesla',
    0.96, 'direct_replacement', 'expert_verified',
    'SHOWCASE-001', 'Front Upper A-Arm - Direct fit, no modifications needed'
),
(
    'A117C0034F', 'Lotus',
    'TR-SUS-002', 'Tesla',
    0.96, 'direct_replacement', 'expert_verified',
    'SHOWCASE-001', 'Front Lower A-Arm - Direct fit'
),
(
    'A117D0049F', 'Lotus',
    'TR-SUS-020', 'Tesla',
    0.95, 'direct_replacement', 'expert_verified',
    'SHOWCASE-001', 'Front Shock (Bilstein B6) - Same damper unit, direct swap'
),
(
    'A117W0023F', 'Lotus',
    'TR-INT-003', 'Tesla',
    1.0, 'direct_replacement', 'expert_verified',
    'SHOWCASE-001', 'Door Latch Mechanism - Identical part'
)
ON CONFLICT DO NOTHING;

-- Insert fastener requirements
INSERT INTO showcase_fasteners (showcase_id, component_name, location, fastener_spec, fastener_standard, length_mm, quantity, torque_nm, notes)
VALUES
('SHOWCASE-001', 'Front Upper A-Arm', 'Inner pivot', 'M10x1.5-10.9', 'ISO', 45, 2, 75, 'Torque to 75 Nm'),
('SHOWCASE-001', 'Front Upper A-Arm', 'Outer ball joint', 'M12x1.75-10.9', 'ISO', 35, 1, 90, 'Torque to 90 Nm'),
('SHOWCASE-001', 'Front Subframe', 'Main chassis mount', 'M12x1.75-10.9', 'ISO', 80, 8, 115, 'Critical structural fastener'),
('SHOWCASE-001', 'Rear Subframe (Tesla)', 'Main chassis mount', 'M14x2.0-12.9', 'ISO', 85, 8, 180, 'Upgraded from Lotus spec due to motor torque and battery loads')
ON CONFLICT DO NOTHING;

COMMENT ON TABLE showcases IS 'Real-world engineering projects demonstrating parts compatibility across platforms';
COMMENT ON TABLE cross_references IS 'The core UPC value: parts that can substitute for each other with confidence scores';
COMMENT ON TABLE cross_reference_qualia IS 'Community-sourced experiential knowledge about cross-references';
COMMENT ON TABLE showcase_fasteners IS 'Detailed fastener specifications for compatibility projects';
COMMENT ON TABLE swap_guides IS 'Complete swap documentation generated from showcases and cross-references';
COMMENT ON FUNCTION find_compatible_parts IS 'Core UPC query: Find all parts compatible with a given part number';
