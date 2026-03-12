-- Universal BOM System — Extended Schema
-- ========================================
-- Extends the parts database to support ALL part categories
-- across ALL industries. This is the McMaster-Carr killer schema.
--
-- Design principles:
--   1. Core table for all parts (universal fields)
--   2. Domain-specific extension tables (joined by part_id)
--   3. JSONB for flexible specs that vary by category
--   4. Full-text search with weighted relevance
--   5. Taxonomy-aware categorization

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text matching


-- ============================================================
-- TAXONOMY: Hierarchical Part Classification
-- ============================================================

CREATE TABLE IF NOT EXISTS taxonomy_categories (
    code VARCHAR(50) PRIMARY KEY,          -- e.g., "MECH.FAST.BOLT.HEX"
    parent_code VARCHAR(50) REFERENCES taxonomy_categories(code),
    name VARCHAR(200) NOT NULL,
    domain VARCHAR(10) NOT NULL,           -- Top-level: MECH, ELEC, HYDR, etc.
    depth INTEGER NOT NULL DEFAULT 0,
    required_specs TEXT[] DEFAULT '{}',     -- Fields required for quality record
    description TEXT,
    icon VARCHAR(50),                      -- For UI display
    sort_order INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_taxonomy_parent ON taxonomy_categories(parent_code);
CREATE INDEX IF NOT EXISTS idx_taxonomy_domain ON taxonomy_categories(domain);
CREATE INDEX IF NOT EXISTS idx_taxonomy_name ON taxonomy_categories USING gin(name gin_trgm_ops);


-- ============================================================
-- UNIVERSAL PARTS TABLE (extended)
-- ============================================================
-- Every part in the system, regardless of type, gets a row here.
-- Domain-specific data lives in extension tables + JSONB specs.

CREATE TABLE IF NOT EXISTS universal_parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Classification
    taxonomy_code VARCHAR(50) NOT NULL REFERENCES taxonomy_categories(code),

    -- Identification
    part_number VARCHAR(200),              -- Manufacturer part number
    manufacturer VARCHAR(200),
    brand VARCHAR(200),                    -- Brand name (may differ from manufacturer)
    standard_designation VARCHAR(200),     -- ISO/DIN/ANSI standard ref
    upc_code VARCHAR(50) UNIQUE,           -- Our Universal Parts Consciousness ID

    -- Description
    name VARCHAR(500) NOT NULL,            -- Short descriptive name
    description TEXT,                      -- Full description
    keywords TEXT[],                       -- Search keywords

    -- Core Physical Properties
    material VARCHAR(200),
    material_spec JSONB,                   -- Detailed material data
    weight_kg DECIMAL(12,6),

    -- Dimensions (stored in mm for consistency)
    -- Most parts have some notion of bounding dimensions
    dimension_x_mm DECIMAL(12,4),          -- Length / Width / X
    dimension_y_mm DECIMAL(12,4),          -- Width / Height / Y
    dimension_z_mm DECIMAL(12,4),          -- Height / Depth / Z

    -- Domain-Specific Specifications (flexible JSONB)
    -- This is where per-category data lives
    specifications JSONB NOT NULL DEFAULT '{}',

    -- Mechanical Properties (common enough for top-level)
    tensile_strength_mpa DECIMAL(10,2),
    yield_strength_mpa DECIMAL(10,2),
    hardness VARCHAR(50),

    -- Pricing (latest known)
    price_usd DECIMAL(12,4),
    price_unit VARCHAR(50),                -- "each", "per 100", "per ft", etc.
    currency VARCHAR(3) DEFAULT 'USD',

    -- Availability
    in_production BOOLEAN DEFAULT TRUE,
    lead_time_days INTEGER,
    moq INTEGER,                           -- Minimum order quantity

    -- CAD & Documentation
    cad_models JSONB DEFAULT '{}',         -- {"STEP": "url", "STL": "url", ...}
    datasheet_url TEXT,
    image_urls TEXT[],
    thumbnail_url TEXT,

    -- Source Tracking
    data_source VARCHAR(100),              -- Where this record came from
    source_url TEXT,                       -- Original listing URL
    source_part_id VARCHAR(200),           -- ID in source system

    -- Quality & Verification
    quality_score DECIMAL(3,2) DEFAULT 0,  -- 0.00 to 1.00
    completeness_score DECIMAL(3,2) DEFAULT 0,
    verification_status VARCHAR(20) DEFAULT 'unverified',
    verified_by VARCHAR(100),
    verification_count INTEGER DEFAULT 0,
    last_verified TIMESTAMPTZ,

    -- Consciousness State
    consciousness_level VARCHAR(20) DEFAULT 'DORMANT',
    interaction_count INTEGER DEFAULT 0,
    first_awakened TIMESTAMPTZ DEFAULT NOW(),
    last_interaction TIMESTAMPTZ,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(100),
    version INTEGER DEFAULT 1
);

-- Core indexes
CREATE INDEX IF NOT EXISTS idx_uparts_taxonomy ON universal_parts(taxonomy_code);
CREATE INDEX IF NOT EXISTS idx_uparts_manufacturer ON universal_parts(manufacturer, part_number);
CREATE INDEX IF NOT EXISTS idx_uparts_material ON universal_parts(material);
CREATE INDEX IF NOT EXISTS idx_uparts_source ON universal_parts(data_source, source_part_id);
CREATE INDEX IF NOT EXISTS idx_uparts_consciousness ON universal_parts(consciousness_level);
CREATE INDEX IF NOT EXISTS idx_uparts_quality ON universal_parts(quality_score DESC);
CREATE INDEX IF NOT EXISTS idx_uparts_specs ON universal_parts USING gin(specifications);
CREATE INDEX IF NOT EXISTS idx_uparts_keywords ON universal_parts USING gin(keywords);

-- Full-text search
CREATE INDEX IF NOT EXISTS idx_uparts_fts ON universal_parts USING gin(
    to_tsvector('english',
        coalesce(name, '') || ' ' ||
        coalesce(description, '') || ' ' ||
        coalesce(manufacturer, '') || ' ' ||
        coalesce(part_number, '') || ' ' ||
        coalesce(material, '') || ' ' ||
        coalesce(standard_designation, '')
    )
);

-- Trigram index for fuzzy matching
CREATE INDEX IF NOT EXISTS idx_uparts_name_trgm ON universal_parts USING gin(name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_uparts_partnum_trgm ON universal_parts USING gin(part_number gin_trgm_ops);


-- ============================================================
-- DOMAIN EXTENSION TABLES
-- ============================================================
-- These tables hold domain-specific data that benefits from
-- being queryable in SQL (vs buried in JSONB).

-- Fastener-specific data
CREATE TABLE IF NOT EXISTS ext_fasteners (
    part_id UUID PRIMARY KEY REFERENCES universal_parts(id) ON DELETE CASCADE,

    thread_standard VARCHAR(20),           -- ISO, UNC, UNF, BSP, NPT
    thread_spec VARCHAR(50),               -- "M8x1.25", "1/4-20"
    thread_pitch_mm DECIMAL(10,4),
    thread_major_diameter_mm DECIMAL(10,4),
    thread_class VARCHAR(20),              -- 6g, 6H, 2A, 2B
    thread_direction VARCHAR(10) DEFAULT 'right',

    head_type VARCHAR(50),
    head_diameter_mm DECIMAL(10,3),
    head_height_mm DECIMAL(10,3),
    drive_type VARCHAR(50),
    drive_size VARCHAR(20),

    shank_length_mm DECIMAL(10,2),
    thread_length_mm DECIMAL(10,2),
    overall_length_mm DECIMAL(10,2),

    grade VARCHAR(20),                     -- "8.8", "10.9", "A2-70"
    proof_load_kn DECIMAL(10,2),

    finish VARCHAR(100),                   -- "Zinc Plated", "Black Oxide"
    coating VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_ext_fast_thread ON ext_fasteners(thread_spec);
CREATE INDEX IF NOT EXISTS idx_ext_fast_grade ON ext_fasteners(grade);

-- Bearing-specific data
CREATE TABLE IF NOT EXISTS ext_bearings (
    part_id UUID PRIMARY KEY REFERENCES universal_parts(id) ON DELETE CASCADE,

    bearing_type VARCHAR(50),              -- deep_groove, angular_contact, tapered
    bore_diameter_mm DECIMAL(10,3),
    outer_diameter_mm DECIMAL(10,3),
    width_mm DECIMAL(10,3),

    dynamic_load_rating_kn DECIMAL(10,2),
    static_load_rating_kn DECIMAL(10,2),
    max_rpm INTEGER,

    seal_type VARCHAR(50),                 -- open, shielded, sealed
    cage_material VARCHAR(50),
    precision_class VARCHAR(20),           -- ABEC-1, ABEC-3, ABEC-7

    designation VARCHAR(100)               -- "6205-2RS", "32008X"
);

CREATE INDEX IF NOT EXISTS idx_ext_bear_bore ON ext_bearings(bore_diameter_mm);
CREATE INDEX IF NOT EXISTS idx_ext_bear_type ON ext_bearings(bearing_type);

-- Seal/O-Ring-specific data
CREATE TABLE IF NOT EXISTS ext_seals (
    part_id UUID PRIMARY KEY REFERENCES universal_parts(id) ON DELETE CASCADE,

    seal_type VARCHAR(50),                 -- o-ring, lip_seal, gasket
    inner_diameter_mm DECIMAL(10,3),
    outer_diameter_mm DECIMAL(10,3),
    cross_section_mm DECIMAL(10,3),

    durometer VARCHAR(20),                 -- "70A", "90A"
    compound VARCHAR(50),                  -- NBR, FKM, EPDM, Silicone

    max_pressure_bar DECIMAL(10,2),
    min_temp_c DECIMAL(6,1),
    max_temp_c DECIMAL(6,1),

    standard_size VARCHAR(50),             -- AS568-210, metric 10x2
    application VARCHAR(20)                -- static, dynamic, rotary
);

CREATE INDEX IF NOT EXISTS idx_ext_seal_size ON ext_seals(inner_diameter_mm, cross_section_mm);

-- Electrical connector-specific data
CREATE TABLE IF NOT EXISTS ext_connectors (
    part_id UUID PRIMARY KEY REFERENCES universal_parts(id) ON DELETE CASCADE,

    connector_type VARCHAR(50),            -- circular, rectangular, terminal
    connector_series VARCHAR(100),         -- "Deutsch DT", "Molex Micro-Fit"
    pin_count INTEGER,
    gender VARCHAR(20),                    -- male, female, hermaphroditic

    voltage_rating_v DECIMAL(8,2),
    current_rating_a DECIMAL(8,2),
    contact_resistance_mohm DECIMAL(8,2),

    wire_gauge_range VARCHAR(50),          -- "18-22 AWG"
    mounting_type VARCHAR(50),             -- panel, PCB, cable, DIN rail
    ip_rating VARCHAR(10),                 -- IP67, IP68

    mating_connector VARCHAR(200)          -- Compatible mating part number
);

-- Motor-specific data
CREATE TABLE IF NOT EXISTS ext_motors (
    part_id UUID PRIMARY KEY REFERENCES universal_parts(id) ON DELETE CASCADE,

    motor_type VARCHAR(50),                -- DC, AC, stepper, servo, BLDC
    voltage_v DECIMAL(8,2),
    power_watts DECIMAL(10,2),
    rated_rpm INTEGER,
    rated_torque_nm DECIMAL(10,4),
    stall_torque_nm DECIMAL(10,4),

    frame_size VARCHAR(30),                -- NEMA 17, NEMA 23, IEC 71
    shaft_diameter_mm DECIMAL(8,3),
    mounting_pattern VARCHAR(50),

    efficiency_percent DECIMAL(5,2),
    insulation_class VARCHAR(5),           -- B, F, H
    ip_rating VARCHAR(10),
    phases INTEGER,                        -- 1, 3
    poles INTEGER
);

-- Raw material / stock-specific data
CREATE TABLE IF NOT EXISTS ext_raw_materials (
    part_id UUID PRIMARY KEY REFERENCES universal_parts(id) ON DELETE CASCADE,

    alloy_designation VARCHAR(100),        -- "6061-T6", "304", "1018"
    form VARCHAR(50),                      -- sheet, plate, bar, rod, tube, wire

    -- Dimensions depend on form
    thickness_mm DECIMAL(10,3),
    width_mm DECIMAL(10,3),
    length_mm DECIMAL(10,3),
    outer_diameter_mm DECIMAL(10,3),
    inner_diameter_mm DECIMAL(10,3),
    wall_thickness_mm DECIMAL(10,3),

    temper VARCHAR(50),                    -- T6, annealed, cold-rolled, hot-rolled
    surface_finish VARCHAR(100),           -- mill, polished, brushed, anodized

    density_g_cm3 DECIMAL(6,3),
    thermal_conductivity_w_mk DECIMAL(8,2),
    thermal_expansion_ppm_k DECIMAL(6,2),
    elastic_modulus_gpa DECIMAL(8,2),
    melting_point_c DECIMAL(8,1)
);


-- ============================================================
-- PART RELATIONSHIPS
-- ============================================================

CREATE TABLE IF NOT EXISTS part_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    part_a_id UUID NOT NULL REFERENCES universal_parts(id) ON DELETE CASCADE,
    part_b_id UUID NOT NULL REFERENCES universal_parts(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,
    -- Types: 'replaces', 'mates_with', 'requires', 'alternative_to',
    --        'assembly_parent', 'assembly_child', 'compatible_with',
    --        'supercedes', 'variant_of'

    confidence DECIMAL(3,2) DEFAULT 1.0,   -- 0-1 confidence in relationship
    bidirectional BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',

    source VARCHAR(100),                   -- How we know about this relationship
    verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(part_a_id, part_b_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_partrel_a ON part_relationships(part_a_id);
CREATE INDEX IF NOT EXISTS idx_partrel_b ON part_relationships(part_b_id);
CREATE INDEX IF NOT EXISTS idx_partrel_type ON part_relationships(relationship_type);


-- ============================================================
-- BILL OF MATERIALS (BOM)
-- ============================================================

CREATE TABLE IF NOT EXISTS bom_assemblies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name VARCHAR(500) NOT NULL,
    description TEXT,
    version VARCHAR(50) DEFAULT '1.0',

    -- What is this a BOM for?
    assembly_type VARCHAR(50),             -- product, sub_assembly, kit
    industry VARCHAR(100),                 -- automotive, aerospace, marine, etc.

    -- Source
    source VARCHAR(200),                   -- Who created this BOM
    source_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS bom_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    bom_id UUID NOT NULL REFERENCES bom_assemblies(id) ON DELETE CASCADE,
    part_id UUID REFERENCES universal_parts(id),

    -- Position in BOM hierarchy
    parent_item_id UUID REFERENCES bom_items(id),
    level INTEGER DEFAULT 0,               -- Depth in BOM tree
    item_number VARCHAR(50),               -- BOM line item number (e.g., "1.2.3")

    -- Quantity
    quantity DECIMAL(12,4) NOT NULL DEFAULT 1,
    unit VARCHAR(20) DEFAULT 'each',       -- each, ft, m, kg, L

    -- Reference
    reference_designator VARCHAR(100),     -- "R1", "C5", "BOLT-A3"
    notes TEXT,

    -- If part_id is NULL, this is a description-only line
    description VARCHAR(500),

    -- Alternates
    alternate_parts UUID[],                -- Array of acceptable substitute part IDs

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bom_items_bom ON bom_items(bom_id);
CREATE INDEX IF NOT EXISTS idx_bom_items_part ON bom_items(part_id);
CREATE INDEX IF NOT EXISTS idx_bom_items_parent ON bom_items(parent_item_id);


-- ============================================================
-- DATA SOURCE TRACKING
-- ============================================================

CREATE TABLE IF NOT EXISTS data_sources (
    id VARCHAR(100) PRIMARY KEY,           -- "mcmaster", "grainger", "iso_standards"
    name VARCHAR(200) NOT NULL,
    source_type VARCHAR(50) NOT NULL,      -- supplier, standard, community, cad_library
    tier INTEGER NOT NULL DEFAULT 1,       -- 1=primary, 2=standards, 3=manufacturer, 4=community

    base_url TEXT,
    api_endpoint TEXT,

    -- Ingestion stats
    total_parts_ingested INTEGER DEFAULT 0,
    last_ingestion TIMESTAMPTZ,
    ingestion_frequency VARCHAR(50),       -- "daily", "weekly", "monthly", "on_demand"

    -- Status
    active BOOLEAN DEFAULT TRUE,
    health_status VARCHAR(20) DEFAULT 'unknown',
    last_health_check TIMESTAMPTZ,

    config JSONB DEFAULT '{}',             -- Source-specific configuration

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- INGESTION LOG
-- ============================================================

CREATE TABLE IF NOT EXISTS ingestion_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_id VARCHAR(100) REFERENCES data_sources(id),
    run_id VARCHAR(100) NOT NULL,

    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'running',

    parts_fetched INTEGER DEFAULT 0,
    parts_accepted INTEGER DEFAULT 0,
    parts_rejected INTEGER DEFAULT 0,
    parts_updated INTEGER DEFAULT 0,
    duplicates_found INTEGER DEFAULT 0,

    average_quality_score DECIMAL(3,2),

    error_message TEXT,
    details JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_ingest_source ON ingestion_log(source_id);
CREATE INDEX IF NOT EXISTS idx_ingest_status ON ingestion_log(status);


-- ============================================================
-- SEARCH FUNCTIONS
-- ============================================================

-- Full-text search with relevance ranking
CREATE OR REPLACE FUNCTION search_parts(
    query TEXT,
    category_filter VARCHAR(50) DEFAULT NULL,
    material_filter VARCHAR(200) DEFAULT NULL,
    limit_count INTEGER DEFAULT 50,
    offset_count INTEGER DEFAULT 0
) RETURNS TABLE (
    part_id UUID,
    name VARCHAR(500),
    taxonomy_code VARCHAR(50),
    manufacturer VARCHAR(200),
    part_number VARCHAR(200),
    material VARCHAR(200),
    price_usd DECIMAL(12,4),
    quality_score DECIMAL(3,2),
    relevance REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.taxonomy_code,
        p.manufacturer,
        p.part_number,
        p.material,
        p.price_usd,
        p.quality_score,
        ts_rank_cd(
            to_tsvector('english',
                coalesce(p.name, '') || ' ' ||
                coalesce(p.description, '') || ' ' ||
                coalesce(p.manufacturer, '') || ' ' ||
                coalesce(p.part_number, '') || ' ' ||
                coalesce(p.material, '')
            ),
            plainto_tsquery('english', query)
        ) AS relevance
    FROM universal_parts p
    WHERE
        to_tsvector('english',
            coalesce(p.name, '') || ' ' ||
            coalesce(p.description, '') || ' ' ||
            coalesce(p.manufacturer, '') || ' ' ||
            coalesce(p.part_number, '') || ' ' ||
            coalesce(p.material, '')
        ) @@ plainto_tsquery('english', query)
        AND (category_filter IS NULL OR p.taxonomy_code LIKE category_filter || '%')
        AND (material_filter IS NULL OR p.material ILIKE '%' || material_filter || '%')
    ORDER BY relevance DESC, p.quality_score DESC
    LIMIT limit_count
    OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;


-- Find compatible/substitute parts
CREATE OR REPLACE FUNCTION find_substitutes(
    target_part_id UUID,
    min_confidence DECIMAL DEFAULT 0.7
) RETURNS TABLE (
    substitute_id UUID,
    substitute_name VARCHAR(500),
    relationship_type VARCHAR(50),
    confidence DECIMAL(3,2),
    manufacturer VARCHAR(200),
    part_number VARCHAR(200),
    price_usd DECIMAL(12,4)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        r.relationship_type,
        r.confidence,
        p.manufacturer,
        p.part_number,
        p.price_usd
    FROM part_relationships r
    JOIN universal_parts p ON (
        CASE WHEN r.part_a_id = target_part_id THEN r.part_b_id
             ELSE r.part_a_id END
    ) = p.id
    WHERE
        (r.part_a_id = target_part_id OR (r.part_b_id = target_part_id AND r.bidirectional))
        AND r.relationship_type IN ('replaces', 'alternative_to', 'compatible_with')
        AND r.confidence >= min_confidence
    ORDER BY r.confidence DESC, p.quality_score DESC;
END;
$$ LANGUAGE plpgsql;


-- Get full BOM tree
CREATE OR REPLACE FUNCTION get_bom_tree(
    target_bom_id UUID
) RETURNS TABLE (
    item_id UUID,
    item_number VARCHAR(50),
    level INTEGER,
    part_id UUID,
    part_name VARCHAR(500),
    quantity DECIMAL(12,4),
    unit VARCHAR(20),
    taxonomy_code VARCHAR(50),
    manufacturer VARCHAR(200),
    part_number VARCHAR(200)
) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE bom_tree AS (
        -- Root items
        SELECT
            bi.id,
            bi.item_number,
            bi.level,
            bi.part_id,
            bi.quantity,
            bi.unit,
            bi.parent_item_id,
            bi.description
        FROM bom_items bi
        WHERE bi.bom_id = target_bom_id AND bi.parent_item_id IS NULL

        UNION ALL

        -- Child items
        SELECT
            bi.id,
            bi.item_number,
            bi.level,
            bi.part_id,
            bi.quantity,
            bi.unit,
            bi.parent_item_id,
            bi.description
        FROM bom_items bi
        JOIN bom_tree bt ON bi.parent_item_id = bt.id
    )
    SELECT
        bt.id,
        bt.item_number,
        bt.level,
        bt.part_id AS part_id,
        COALESCE(p.name, bt.description) AS part_name,
        bt.quantity,
        bt.unit,
        p.taxonomy_code,
        p.manufacturer,
        p.part_number
    FROM bom_tree bt
    LEFT JOIN universal_parts p ON bt.part_id = p.id
    ORDER BY bt.item_number;
END;
$$ LANGUAGE plpgsql;


-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_universal_parts_modtime
    BEFORE UPDATE ON universal_parts
    FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_taxonomy_modtime
    BEFORE UPDATE ON taxonomy_categories
    FOR EACH ROW EXECUTE FUNCTION update_modified_column();
