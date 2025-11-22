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

-- Material reference library - thermal and mechanical properties
CREATE TABLE materials_reference (
    material_id VARCHAR(50) PRIMARY KEY,  -- e.g., "A356.0-T6", "Gray_Iron_Class_30"

    -- Classification
    material_category VARCHAR(50) NOT NULL,  -- aluminum_alloy, cast_iron, steel, superalloy
    common_names TEXT[],  -- Array of common names
    description TEXT,

    -- Thermal properties (CRITICAL for material consciousness)
    thermal_expansion_ppm_k DECIMAL(6,2),  -- Coefficient of thermal expansion
    thermal_conductivity_w_mk DECIMAL(8,2),  -- W/(m·K)
    melting_point_c DECIMAL(8,2),
    specific_heat_j_kg_k DECIMAL(8,2),
    max_service_temp_c DECIMAL(8,2),

    -- Mechanical properties
    tensile_strength_mpa DECIMAL(10,2),
    yield_strength_mpa DECIMAL(10,2),
    elongation_percent DECIMAL(5,2),
    hardness VARCHAR(30),  -- "80 HB", "35 HRC", etc.
    elastic_modulus_gpa DECIMAL(8,2),
    fatigue_strength_mpa DECIMAL(10,2),

    -- Composition (stored as JSONB for flexibility)
    composition JSONB,  -- {"aluminum": "balance", "silicon": "6.5-7.5", ...}

    -- Processing information
    typical_processing TEXT[],  -- ["sand_casting", "die_casting", ...]
    heat_treatment VARCHAR(100),  -- "T6", "Normalized", etc.

    -- Usage context
    typical_applications TEXT[],
    oem_usage_examples TEXT[],

    -- Metadata
    data_source VARCHAR(100),
    last_updated TIMESTAMP DEFAULT NOW(),

    INDEX idx_material_category (material_category),
    INDEX idx_thermal_expansion (thermal_expansion_ppm_k)
);

-- Material interface definitions - WHERE MATERIALS MEET
CREATE TABLE material_interfaces (
    interface_id VARCHAR(100) PRIMARY KEY,  -- e.g., "aluminum_block_iron_liner"

    -- Materials involved
    material_1_id VARCHAR(50) REFERENCES materials_reference(material_id),
    material_2_id VARCHAR(50) REFERENCES materials_reference(material_id),
    interface_description TEXT NOT NULL,

    -- Thermal differential (THE KEY TO MATERIAL CONSCIOUSNESS)
    expansion_differential_ppm_k DECIMAL(6,2),  -- Calculated: |mat1_expansion - mat2_expansion|
    at_100c_rise_notes TEXT,  -- Human-readable impact at typical temperature rise

    -- Engineering considerations
    critical_considerations TEXT[],
    failure_modes TEXT[],
    design_solutions TEXT[],

    -- Service implications
    service_notes JSONB,  -- Detailed service guidance

    -- Examples
    engines_using_this_interface TEXT[],

    INDEX idx_materials (material_1_id, material_2_id)
);

-- Material compatibility matrix (enhanced)
CREATE TABLE material_compatibility (
    id SERIAL PRIMARY KEY,
    material_1 VARCHAR(50) NOT NULL REFERENCES materials_reference(material_id),
    material_2 VARCHAR(50) NOT NULL REFERENCES materials_reference(material_id),

    -- Mechanical compatibility
    galvanic_corrosion_risk VARCHAR(20),  -- none, low, medium, high, very_high
    galvanic_voltage_mv INTEGER,  -- Galvanic potential difference
    differential_expansion DECIMAL(10,6),  -- ppm/°C difference (calculated)

    -- Installation parameters
    thread_lock_required BOOLEAN,
    anti_seize_required BOOLEAN,
    insert_recommended BOOLEAN,
    isolation_required BOOLEAN,  -- For high galvanic risk

    -- Torque adjustments
    torque_reduction_factor DECIMAL(4,3) DEFAULT 1.0,

    -- Thread engagement requirements
    min_engagement_multiplier DECIMAL(3,2) DEFAULT 1.0,  -- 1.5 for aluminum threads

    -- Prevention methods
    corrosion_prevention TEXT[],  -- ["coating", "anti-seize", "isolation"]

    UNIQUE(material_1, material_2)
);

-- Engine material configurations - links engines to their material interfaces
CREATE TABLE engine_material_configuration (
    engine_id VARCHAR(100) PRIMARY KEY,

    -- Block configuration
    block_material_id VARCHAR(50) REFERENCES materials_reference(material_id),
    block_casting_method VARCHAR(50),

    -- Liner/bore configuration
    bore_type VARCHAR(50),  -- "iron_liner", "nikasil", "alusil", "ptwa", "parent_bore"
    liner_material_id VARCHAR(50) REFERENCES materials_reference(material_id),
    liner_interference_fit_mm VARCHAR(20),  -- "0.05-0.08"

    -- Head configuration
    head_material_id VARCHAR(50) REFERENCES materials_reference(material_id),
    head_casting_method VARCHAR(50),

    -- Interface types
    block_liner_interface VARCHAR(100) REFERENCES material_interfaces(interface_id),
    head_block_interface VARCHAR(100) REFERENCES material_interfaces(interface_id),

    -- Head gasket requirements
    head_gasket_type VARCHAR(50),  -- "MLS", "composite", "copper"
    deck_surface_finish_ra_microns DECIMAL(4,2),

    -- Material consciousness notes
    thermal_management_notes TEXT,
    service_considerations TEXT[],

    INDEX idx_block_material (block_material_id),
    INDEX idx_bore_type (bore_type)
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

-- Material consciousness helper functions

-- Calculate thermal expansion difference between two materials
CREATE OR REPLACE FUNCTION calculate_expansion_differential(
    material_1_id VARCHAR(50),
    material_2_id VARCHAR(50)
) RETURNS TABLE (
    expansion_difference_ppm_k DECIMAL(6,2),
    at_100c_growth_per_100mm_difference_mm DECIMAL(6,4),
    ratio DECIMAL(4,2),
    consciousness_note TEXT
) AS $$
DECLARE
    mat1_expansion DECIMAL(6,2);
    mat2_expansion DECIMAL(6,2);
    diff DECIMAL(6,2);
    growth_diff DECIMAL(6,4);
BEGIN
    -- Get expansion coefficients
    SELECT thermal_expansion_ppm_k INTO mat1_expansion
    FROM materials_reference WHERE material_id = material_1_id;

    SELECT thermal_expansion_ppm_k INTO mat2_expansion
    FROM materials_reference WHERE material_id = material_2_id;

    -- Calculate difference
    diff := ABS(mat1_expansion - mat2_expansion);
    -- Growth difference per 100mm at 100°C rise: (diff ppm/K) * 100K * 100mm / 1,000,000
    growth_diff := diff * 100 * 100 / 1000000;

    RETURN QUERY
    SELECT
        diff,
        growth_diff,
        CASE WHEN mat2_expansion > 0 THEN mat1_expansion / mat2_expansion ELSE NULL END,
        CASE
            WHEN diff < 3 THEN 'Matched expansion - simple sealing'
            WHEN diff < 8 THEN 'Moderate differential - standard gaskets OK'
            WHEN diff < 12 THEN 'Significant differential - MLS gasket recommended, consider interference fits'
            ELSE 'High differential - critical engineering required for interface'
        END;
END;
$$ LANGUAGE plpgsql;

-- Get material consciousness summary for an engine
CREATE OR REPLACE FUNCTION get_engine_material_consciousness(
    engine VARCHAR(100)
) RETURNS TABLE (
    interface_type VARCHAR(100),
    materials TEXT,
    expansion_differential DECIMAL(6,2),
    critical_notes TEXT[],
    failure_modes TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        mi.interface_id,
        mr1.material_id || ' <-> ' || mr2.material_id,
        mi.expansion_differential_ppm_k,
        mi.critical_considerations,
        mi.failure_modes
    FROM engine_material_configuration emc
    LEFT JOIN material_interfaces mi ON
        emc.block_liner_interface = mi.interface_id OR
        emc.head_block_interface = mi.interface_id
    LEFT JOIN materials_reference mr1 ON mi.material_1_id = mr1.material_id
    LEFT JOIN materials_reference mr2 ON mi.material_2_id = mr2.material_id
    WHERE emc.engine_id = engine;
END;
$$ LANGUAGE plpgsql;

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