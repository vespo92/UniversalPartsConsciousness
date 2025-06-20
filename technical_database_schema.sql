-- Universal Parts Consciousness - Technical Database Schema
-- Complete dimensional and compatibility tracking for ALL mechanical parts

-- Core thread specifications table
CREATE TABLE thread_specifications (
    thread_id VARCHAR(50) PRIMARY KEY,  -- e.g., "M3x0.5-6H"
    
    -- Basic identifiers
    thread_standard VARCHAR(20) NOT NULL,  -- ISO, UNC, UNF, etc.
    nominal_diameter DECIMAL(10,4) NOT NULL,
    pitch DECIMAL(10,4) NOT NULL,
    
    -- Detailed dimensions (all in mm)
    major_diameter_min DECIMAL(10,4) NOT NULL,
    major_diameter_max DECIMAL(10,4) NOT NULL,
    pitch_diameter_min DECIMAL(10,4) NOT NULL,
    pitch_diameter_max DECIMAL(10,4) NOT NULL,
    minor_diameter_min DECIMAL(10,4) NOT NULL,
    minor_diameter_max DECIMAL(10,4) NOT NULL,
    
    -- Thread characteristics
    thread_angle DECIMAL(5,2) DEFAULT 60,  -- degrees
    thread_class VARCHAR(10),  -- 6H, 6g, 2A, 2B, etc.
    tolerance_position VARCHAR(1),  -- H, g, etc.
    tolerance_grade INTEGER,
    thread_direction VARCHAR(5) DEFAULT 'right',
    
    -- Engagement specifications
    min_engagement_ratio DECIMAL(4,2) DEFAULT 1.5,  -- x diameter
    max_engagement_ratio DECIMAL(4,2) DEFAULT 3.0,
    thread_runout DECIMAL(10,4),
    
    -- Indexing
    INDEX idx_diameter (nominal_diameter),
    INDEX idx_pitch (pitch),
    INDEX idx_standard (thread_standard)
);

-- Complete part specifications
CREATE TABLE parts (
    part_id VARCHAR(100) PRIMARY KEY,
    universal_id UUID UNIQUE DEFAULT gen_random_uuid(),
    
    -- Identification
    manufacturer VARCHAR(100),
    part_number VARCHAR(100),
    standard_designation VARCHAR(100),  -- DIN 912, ISO 4762, etc.
    
    -- Type classification  
    category VARCHAR(50) NOT NULL,  -- fastener, bearing, seal, etc.
    subcategory VARCHAR(50),  -- cap_screw, hex_bolt, etc.
    
    -- Thread specifications (if applicable)
    thread_id VARCHAR(50) REFERENCES thread_specifications(thread_id),
    thread_length DECIMAL(10,2),  -- mm
    
    -- Overall dimensions
    length DECIMAL(10,2),
    length_tolerance_plus DECIMAL(10,3),
    length_tolerance_minus DECIMAL(10,3),
    
    -- Material specifications
    material_grade VARCHAR(50),
    material_spec JSONB,  -- Detailed composition, treatments, etc.
    
    -- Mechanical properties
    tensile_strength DECIMAL(10,2),  -- MPa
    yield_strength DECIMAL(10,2),    -- MPa  
    proof_load DECIMAL(10,2),        -- kN
    hardness VARCHAR(20),            -- HRC, HB, etc.
    
    -- Source tracking
    data_source VARCHAR(50),  -- catalog, measured, reverse_engineered
    verification_status VARCHAR(20) DEFAULT 'unverified',
    last_verified TIMESTAMP,
    
    -- Full specifications as JSONB for flexibility
    full_specs JSONB NOT NULL,
    
    INDEX idx_category (category, subcategory),
    INDEX idx_manufacturer (manufacturer, part_number),
    INDEX idx_thread (thread_id)
);

-- Head/Feature specifications for fasteners
CREATE TABLE fastener_heads (
    part_id VARCHAR(100) REFERENCES parts(part_id),
    
    -- Head dimensions
    head_type VARCHAR(50),  -- hex, socket, pan, flat, etc.
    head_diameter DECIMAL(10,3),
    head_diameter_tolerance DECIMAL(10,3),
    head_height DECIMAL(10,3),
    head_height_tolerance DECIMAL(10,3),
    
    -- Drive specifications
    drive_type VARCHAR(50),  -- hex_socket, phillips, torx, etc.
    drive_size VARCHAR(20),  -- 2.5mm, T25, #2, etc.
    drive_depth DECIMAL(10,3),
    
    -- Special features
    bearing_surface_diameter DECIMAL(10,3),
    washer_integrated BOOLEAN DEFAULT FALSE,
    
    PRIMARY KEY (part_id)
);

-- Material compatibility matrix
CREATE TABLE material_compatibility (
    id SERIAL PRIMARY KEY,
    material_1 VARCHAR(50) NOT NULL,
    material_2 VARCHAR(50) NOT NULL,
    
    -- Mechanical compatibility
    galvanic_corrosion_risk VARCHAR(20),  -- none, low, medium, high
    differential_expansion DECIMAL(10,6),  -- ppm/°C difference
    
    -- Installation parameters
    thread_lock_required BOOLEAN,
    anti_seize_required BOOLEAN,
    insert_recommended BOOLEAN,
    
    -- Torque adjustments
    torque_reduction_factor DECIMAL(4,3) DEFAULT 1.0,
    
    UNIQUE(material_1, material_2)
);

-- Thread compatibility matrix
CREATE TABLE thread_compatibility (
    internal_thread VARCHAR(50) REFERENCES thread_specifications(thread_id),
    external_thread VARCHAR(50) REFERENCES thread_specifications(thread_id),
    
    -- Compatibility assessment
    compatibility_class VARCHAR(20),  -- perfect, acceptable, marginal, incompatible
    tolerance_stack DECIMAL(10,4),
    
    -- Engagement characteristics
    min_engagement_turns DECIMAL(5,2),
    thread_lock_recommended BOOLEAN,
    
    PRIMARY KEY (internal_thread, external_thread)
);

-- Length compatibility for specific applications
CREATE TABLE length_compatibility (
    part_id VARCHAR(100) REFERENCES parts(part_id),
    application_thickness DECIMAL(10,2),
    
    -- Results
    total_engagement DECIMAL(10,2),
    protrusion DECIMAL(10,2),
    engagement_ratio DECIMAL(4,2),
    sufficient_engagement BOOLEAN,
    
    -- Recommendations
    optimal BOOLEAN,
    usable_with_spacer DECIMAL(10,2),  -- spacer thickness needed
    usable_with_countersink DECIMAL(10,2),  -- countersink depth needed
    
    INDEX idx_part_thickness (part_id, application_thickness)
);

-- Installation requirements
CREATE TABLE installation_requirements (
    part_id VARCHAR(100) REFERENCES parts(part_id),
    
    -- Torque specifications
    recommended_torque DECIMAL(10,2),  -- Nm
    min_torque DECIMAL(10,2),
    max_torque DECIMAL(10,2),
    torque_tolerance_percent DECIMAL(5,2),
    
    -- Tool requirements
    required_tool VARCHAR(100),
    tool_size VARCHAR(50),
    min_tool_clearance DECIMAL(10,2),  -- mm
    min_swing_arc DECIMAL(5,2),  -- degrees for ratcheting
    
    -- Installation conditions
    thread_prep VARCHAR(100),  -- clean_dry, oiled, thread_lock, etc.
    
    PRIMARY KEY (part_id)
);

-- Clearance hole specifications
CREATE TABLE clearance_holes (
    part_id VARCHAR(100) REFERENCES parts(part_id),
    fit_class VARCHAR(20),  -- close, normal, loose
    
    hole_diameter DECIMAL(10,3),
    hole_tolerance DECIMAL(10,3),
    countersink_diameter DECIMAL(10,3),
    countersink_angle DECIMAL(5,2),
    
    PRIMARY KEY (part_id, fit_class)
);

-- Strength calculations
CREATE TABLE strength_data (
    part_id VARCHAR(100) REFERENCES parts(part_id),
    material_base VARCHAR(50),
    
    -- Thread strength
    thread_shear_area DECIMAL(10,4),  -- mm²
    internal_thread_shear_strength DECIMAL(10,2),  -- N
    external_thread_shear_strength DECIMAL(10,2),  -- N
    
    -- Joint strength
    proof_load_joint DECIMAL(10,2),  -- kN
    ultimate_load_joint DECIMAL(10,2),  -- kN
    
    -- Environmental derating
    temperature_derating JSONB,  -- temp -> strength factor
    
    PRIMARY KEY (part_id, material_base)
);

-- Real-world variations and substitutions
CREATE TABLE field_variations (
    id SERIAL PRIMARY KEY,
    original_part VARCHAR(100) REFERENCES parts(part_id),
    context VARCHAR(200),  -- "2005 Honda Civic door handle"
    
    -- Actual measurements
    measured_dimensions JSONB,
    variance_from_spec JSONB,
    
    -- Field modifications
    modification_type VARCHAR(100),  -- cut_to_length, drilled_out, etc.
    modification_details TEXT,
    
    -- Verification
    verified_by VARCHAR(100),
    verification_date DATE,
    success_count INTEGER DEFAULT 1,
    failure_count INTEGER DEFAULT 0
);

-- Substitution matrix
CREATE TABLE substitutions (
    original_part VARCHAR(100) REFERENCES parts(part_id),
    substitute_part VARCHAR(100) REFERENCES parts(part_id),
    
    -- Compatibility scoring
    dimensional_match DECIMAL(5,2),  -- percentage
    strength_match DECIMAL(5,2),
    overall_compatibility DECIMAL(5,2),
    
    -- Required modifications
    requires_modification BOOLEAN DEFAULT FALSE,
    modification_details JSONB,
    
    -- Usage tracking
    successful_uses INTEGER DEFAULT 0,
    failed_uses INTEGER DEFAULT 0,
    
    PRIMARY KEY (original_part, substitute_part)
);

-- Search optimization views
CREATE MATERIALIZED VIEW part_search AS
SELECT 
    p.part_id,
    p.universal_id,
    p.manufacturer,
    p.part_number,
    p.category,
    p.subcategory,
    t.nominal_diameter,
    t.pitch,
    p.length,
    p.material_grade,
    p.tensile_strength,
    fh.head_type,
    fh.drive_type,
    fh.drive_size,
    p.full_specs
FROM parts p
LEFT JOIN thread_specifications t ON p.thread_id = t.thread_id
LEFT JOIN fastener_heads fh ON p.part_id = fh.part_id;

CREATE INDEX idx_search_thread ON part_search(nominal_diameter, pitch);
CREATE INDEX idx_search_length ON part_search(length);
CREATE INDEX idx_search_drive ON part_search(drive_type, drive_size);

-- Example: Complete compatibility check function
CREATE OR REPLACE FUNCTION check_complete_compatibility(
    screw_id VARCHAR(100),
    hole_thread VARCHAR(50),
    material VARCHAR(50),
    thickness DECIMAL(10,2)
) RETURNS TABLE (
    compatible BOOLEAN,
    engagement_length DECIMAL(10,2),
    protrusion DECIMAL(10,2),
    strength_ok BOOLEAN,
    torque_spec DECIMAL(10,2),
    warnings TEXT[]
) AS $$
DECLARE
    screw_thread VARCHAR(50);
    screw_length DECIMAL(10,2);
    thread_compat RECORD;
    material_compat RECORD;
    strength RECORD;
BEGIN
    -- Get screw specifications
    SELECT thread_id, length INTO screw_thread, screw_length
    FROM parts WHERE part_id = screw_id;
    
    -- Check thread compatibility
    SELECT * INTO thread_compat
    FROM thread_compatibility
    WHERE external_thread = screw_thread 
    AND internal_thread = hole_thread;
    
    -- More checks would follow...
    
    RETURN QUERY
    SELECT 
        thread_compat.compatibility_class IN ('perfect', 'acceptable'),
        LEAST(screw_length, thickness),
        GREATEST(screw_length - thickness, 0),
        TRUE,  -- Simplified
        12.5,  -- Simplified
        ARRAY['Check thread engagement ratio']::TEXT[];
END;
$$ LANGUAGE plpgsql;