-- Integration schema for multi-supplier and CAD data
-- Run this after the main schema

-- CAD file storage
CREATE TABLE IF NOT EXISTS part_cad_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    part_id VARCHAR(100) REFERENCES parts(part_id) ON DELETE CASCADE,

    -- File URLs
    step_url TEXT,
    stl_url TEXT,
    iges_url TEXT,
    dwg_url TEXT,
    pdf_url TEXT,

    -- Extracted dimensions from CAD
    cad_dimensions JSONB, -- BoundingBox, cylindrical, threads, etc.

    -- Metadata
    file_size_bytes BIGINT,
    last_downloaded TIMESTAMPTZ,
    parse_status VARCHAR(20) DEFAULT 'pending', -- pending, parsed, failed

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(part_id)
);

CREATE INDEX IF NOT EXISTS idx_cad_part ON part_cad_files(part_id);
CREATE INDEX IF NOT EXISTS idx_cad_status ON part_cad_files(parse_status);

-- Cross-references between equivalent parts from different suppliers
CREATE TABLE IF NOT EXISTS part_cross_references (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    primary_part_id VARCHAR(100) REFERENCES parts(part_id),
    equivalent_part_id VARCHAR(100) REFERENCES parts(part_id),

    -- Match quality
    match_quality INTEGER CHECK (match_quality >= 0 AND match_quality <= 100),
    match_type VARCHAR(50), -- 'exact', 'functional', 'dimensional', 'material'

    -- Differences (if any)
    dimension_differences JSONB, -- {"length": 0.5, "diameter": 0}
    material_difference TEXT,
    price_difference DECIMAL(10,2),

    -- Verification
    verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES auth.users(id),
    verified_at TIMESTAMPTZ,

    -- Notes
    notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(primary_part_id, equivalent_part_id)
);

CREATE INDEX IF NOT EXISTS idx_crossref_primary ON part_cross_references(primary_part_id);
CREATE INDEX IF NOT EXISTS idx_crossref_equiv ON part_cross_references(equivalent_part_id);
CREATE INDEX IF NOT EXISTS idx_crossref_quality ON part_cross_references(match_quality);

-- Supplier catalog tracking
CREATE TABLE IF NOT EXISTS supplier_catalogs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    supplier_name VARCHAR(100) NOT NULL,
    catalog_url TEXT,
    catalog_type VARCHAR(50), -- 'fasteners', 'bearings', 'hardware', etc.

    -- Import stats
    total_parts INTEGER DEFAULT 0,
    last_import_date TIMESTAMPTZ,
    last_import_status VARCHAR(20), -- 'success', 'partial', 'failed'
    parts_imported_count INTEGER DEFAULT 0,
    parts_failed_count INTEGER DEFAULT 0,

    -- Configuration
    scraper_config JSONB, -- Specific settings for this supplier

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_supplier_name ON supplier_catalogs(supplier_name);

-- Data quality and normalization log
CREATE TABLE IF NOT EXISTS data_normalization_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    part_id VARCHAR(100) REFERENCES parts(part_id),

    -- Normalization actions
    action_type VARCHAR(50), -- 'thread_standardized', 'dimension_converted', 'material_mapped'
    original_value TEXT,
    normalized_value TEXT,
    confidence DECIMAL(5,2), -- 0-100

    -- Source
    data_source VARCHAR(100),
    processed_by VARCHAR(100), -- 'auto', 'manual', 'verified'

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_norm_part ON data_normalization_log(part_id);
CREATE INDEX IF NOT EXISTS idx_norm_action ON data_normalization_log(action_type);

-- Material compatibility data from multiple sources
CREATE TABLE IF NOT EXISTS material_standards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    material_designation VARCHAR(100) NOT NULL,

    -- Standard references
    iso_standard VARCHAR(50),
    din_standard VARCHAR(50),
    ansi_standard VARCHAR(50),
    astm_standard VARCHAR(50),

    -- Properties
    tensile_strength_min DECIMAL(10,2),
    tensile_strength_max DECIMAL(10,2),
    yield_strength_min DECIMAL(10,2),
    yield_strength_max DECIMAL(10,2),
    hardness_min VARCHAR(20),
    hardness_max VARCHAR(20),

    -- Composition
    composition JSONB, -- {"C": 0.15, "Cr": 18, "Ni": 8}

    -- Equivalents
    equivalent_materials TEXT[], -- Array of equivalent material grades

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(material_designation)
);

CREATE INDEX IF NOT EXISTS idx_material_desg ON material_standards(material_designation);

-- Thread standards from multiple specifications
CREATE TABLE IF NOT EXISTS thread_standards_extended (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    thread_designation VARCHAR(100) NOT NULL,

    -- Multiple standard systems
    iso_designation VARCHAR(50),
    din_designation VARCHAR(50),
    ansi_designation VARCHAR(50),
    jis_designation VARCHAR(50),

    -- Dimensions from official standards
    major_diameter DECIMAL(10,4),
    minor_diameter DECIMAL(10,4),
    pitch_diameter DECIMAL(10,4),
    pitch DECIMAL(10,4),

    -- Tolerance classes
    internal_tolerance_classes TEXT[], -- ['6H', '7H']
    external_tolerance_classes TEXT[], -- ['6g', '6h']

    -- Compatibility
    compatible_threads TEXT[], -- Other thread standards that mate

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_thread_desg ON thread_standards_extended(thread_designation);

-- Enable RLS
ALTER TABLE part_cad_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE part_cross_references ENABLE ROW LEVEL SECURITY;
ALTER TABLE supplier_catalogs ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "CAD files viewable by everyone" ON part_cad_files FOR SELECT USING (true);
CREATE POLICY "Cross-refs viewable by everyone" ON part_cross_references FOR SELECT USING (true);
CREATE POLICY "Authenticated users can add cross-refs" ON part_cross_references FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Function to find equivalent parts
CREATE OR REPLACE FUNCTION find_equivalent_parts(p_part_id VARCHAR)
RETURNS TABLE (
    equivalent_id VARCHAR,
    supplier VARCHAR,
    part_number VARCHAR,
    match_quality INTEGER,
    notes TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        CASE
            WHEN pcr.primary_part_id = p_part_id THEN pcr.equivalent_part_id
            ELSE pcr.primary_part_id
        END as equivalent_id,
        p.manufacturer as supplier,
        p.part_number,
        pcr.match_quality,
        pcr.notes
    FROM part_cross_references pcr
    JOIN parts p ON (
        (pcr.primary_part_id = p_part_id AND pcr.equivalent_part_id = p.part_id) OR
        (pcr.equivalent_part_id = p_part_id AND pcr.primary_part_id = p.part_id)
    )
    WHERE pcr.primary_part_id = p_part_id OR pcr.equivalent_part_id = p_part_id
    ORDER BY pcr.match_quality DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to normalize thread designation across standards
CREATE OR REPLACE FUNCTION normalize_thread_designation(thread_input VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    normalized VARCHAR;
BEGIN
    -- Convert various formats to standard ISO format
    -- M3x0.5, 3-0.5, M3, etc. -> M3x0.5

    thread_input := TRIM(UPPER(thread_input));

    -- Already in ISO format
    IF thread_input ~ '^M\d+[Xx]\d+(\.\d+)?$' THEN
        RETURN thread_input;
    END IF;

    -- M3 format (add standard pitch)
    IF thread_input ~ '^M\d+$' THEN
        -- Would look up standard pitch from table
        RETURN thread_input || 'x0.5'; -- Simplified
    END IF;

    -- Other formats would be handled here

    RETURN thread_input;
END;
$$ LANGUAGE plpgsql;

-- Insert common material standards
INSERT INTO material_standards (material_designation, iso_standard, din_standard, ansi_standard, tensile_strength_min, tensile_strength_max, equivalent_materials) VALUES
('A2-70', 'ISO 3506', 'DIN 267-13', 'ASTM F593', 700, 900, ARRAY['304', '18-8 SS', 'X5CrNi18-10']),
('A4-70', 'ISO 3506', 'DIN 267-13', 'ASTM F593', 700, 900, ARRAY['316', '316L', 'X5CrNiMo17-12-2']),
('8.8', 'ISO 898-1', 'DIN 267-4', 'SAE J429 Grade 5', 800, 1040, ARRAY['Grade 5', 'Medium Carbon Steel']),
('10.9', 'ISO 898-1', 'DIN 267-4', 'SAE J429 Grade 8', 1040, 1220, ARRAY['Grade 8', 'Alloy Steel']),
('12.9', 'ISO 898-1', 'DIN 267-4', 'SAE J429 Grade 8', 1220, 1420, ARRAY['Grade 8.2', 'High Strength Alloy'])
ON CONFLICT (material_designation) DO NOTHING;

-- Insert common thread equivalents
INSERT INTO thread_standards_extended (thread_designation, iso_designation, ansi_designation, major_diameter, pitch, compatible_threads) VALUES
('M3x0.5', 'M3x0.5', NULL, 3.0, 0.5, ARRAY['M3x0.5-6H', 'M3x0.5-6g']),
('M4x0.7', 'M4x0.7', NULL, 4.0, 0.7, ARRAY['M4x0.7-6H', 'M4x0.7-6g']),
('M5x0.8', 'M5x0.8', NULL, 5.0, 0.8, ARRAY['M5x0.8-6H', 'M5x0.8-6g']),
('M6x1.0', 'M6x1.0', NULL, 6.0, 1.0, ARRAY['M6x1.0-6H', 'M6x1.0-6g']),
('M8x1.25', 'M8x1.25', NULL, 8.0, 1.25, ARRAY['M8x1.25-6H', 'M8x1.25-6g']),
('1/4-20', NULL, '1/4-20 UNC', 6.35, 1.27, ARRAY['#12-24', '10-32']),
('5/16-18', NULL, '5/16-18 UNC', 7.94, 1.41, ARRAY['5/16-24', 'M8x1.25']),
('3/8-16', NULL, '3/8-16 UNC', 9.53, 1.59, ARRAY['3/8-24', 'M10x1.5'])
ON CONFLICT DO NOTHING;
