-- Universal Parts Database - Supabase Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core thread specifications table
CREATE TABLE IF NOT EXISTS thread_specifications (
    thread_id VARCHAR(50) PRIMARY KEY,

    -- Basic identifiers
    thread_standard VARCHAR(20) NOT NULL,
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
    thread_angle DECIMAL(5,2) DEFAULT 60,
    thread_class VARCHAR(10),
    tolerance_position VARCHAR(1),
    tolerance_grade INTEGER,
    thread_direction VARCHAR(5) DEFAULT 'right',

    -- Engagement specifications
    min_engagement_ratio DECIMAL(4,2) DEFAULT 1.5,
    max_engagement_ratio DECIMAL(4,2) DEFAULT 3.0,
    thread_runout DECIMAL(10,4),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_diameter ON thread_specifications(nominal_diameter);
CREATE INDEX IF NOT EXISTS idx_pitch ON thread_specifications(pitch);
CREATE INDEX IF NOT EXISTS idx_standard ON thread_specifications(thread_standard);

-- Complete part specifications
CREATE TABLE IF NOT EXISTS parts (
    part_id VARCHAR(100) PRIMARY KEY,
    universal_id UUID UNIQUE DEFAULT uuid_generate_v4(),

    -- Identification
    manufacturer VARCHAR(100),
    part_number VARCHAR(100),
    standard_designation VARCHAR(100),

    -- Type classification
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),

    -- Thread specifications (if applicable)
    thread_id VARCHAR(50) REFERENCES thread_specifications(thread_id),
    thread_length DECIMAL(10,2),

    -- Overall dimensions
    length DECIMAL(10,2),
    length_tolerance_plus DECIMAL(10,3),
    length_tolerance_minus DECIMAL(10,3),

    -- Material specifications
    material_grade VARCHAR(50),
    material_spec JSONB,

    -- Mechanical properties
    tensile_strength DECIMAL(10,2),
    yield_strength DECIMAL(10,2),
    proof_load DECIMAL(10,2),
    hardness VARCHAR(20),

    -- Source tracking
    data_source VARCHAR(50),
    verification_status VARCHAR(20) DEFAULT 'unverified',
    last_verified TIMESTAMPTZ,

    -- Full specifications as JSONB for flexibility
    full_specs JSONB NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

CREATE INDEX IF NOT EXISTS idx_category ON parts(category, subcategory);
CREATE INDEX IF NOT EXISTS idx_manufacturer ON parts(manufacturer, part_number);
CREATE INDEX IF NOT EXISTS idx_thread ON parts(thread_id);

-- Head/Feature specifications for fasteners
CREATE TABLE IF NOT EXISTS fastener_heads (
    part_id VARCHAR(100) REFERENCES parts(part_id) PRIMARY KEY,

    -- Head dimensions
    head_type VARCHAR(50),
    head_diameter DECIMAL(10,3),
    head_diameter_tolerance DECIMAL(10,3),
    head_height DECIMAL(10,3),
    head_height_tolerance DECIMAL(10,3),

    -- Drive specifications
    drive_type VARCHAR(50),
    drive_size VARCHAR(20),
    drive_depth DECIMAL(10,3),

    -- Special features
    bearing_surface_diameter DECIMAL(10,3),
    washer_integrated BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Material compatibility matrix
CREATE TABLE IF NOT EXISTS material_compatibility (
    id SERIAL PRIMARY KEY,
    material_1 VARCHAR(50) NOT NULL,
    material_2 VARCHAR(50) NOT NULL,

    -- Mechanical compatibility
    galvanic_corrosion_risk VARCHAR(20),
    differential_expansion DECIMAL(10,6),

    -- Installation parameters
    thread_lock_required BOOLEAN,
    anti_seize_required BOOLEAN,
    insert_recommended BOOLEAN,

    -- Torque adjustments
    torque_reduction_factor DECIMAL(4,3) DEFAULT 1.0,

    UNIQUE(material_1, material_2)
);

-- Thread compatibility matrix
CREATE TABLE IF NOT EXISTS thread_compatibility (
    internal_thread VARCHAR(50) REFERENCES thread_specifications(thread_id),
    external_thread VARCHAR(50) REFERENCES thread_specifications(thread_id),

    -- Compatibility assessment
    compatibility_class VARCHAR(20),
    tolerance_stack DECIMAL(10,4),

    -- Engagement characteristics
    min_engagement_turns DECIMAL(5,2),
    thread_lock_recommended BOOLEAN,

    PRIMARY KEY (internal_thread, external_thread)
);

-- Installation requirements
CREATE TABLE IF NOT EXISTS installation_requirements (
    part_id VARCHAR(100) REFERENCES parts(part_id) PRIMARY KEY,

    -- Torque specifications
    recommended_torque DECIMAL(10,2),
    min_torque DECIMAL(10,2),
    max_torque DECIMAL(10,2),
    torque_tolerance_percent DECIMAL(5,2),

    -- Tool requirements
    required_tool VARCHAR(100),
    tool_size VARCHAR(50),
    min_tool_clearance DECIMAL(10,2),
    min_swing_arc DECIMAL(5,2),

    -- Installation conditions
    thread_prep VARCHAR(100),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User contributions and community data
CREATE TABLE IF NOT EXISTS user_contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    part_id VARCHAR(100) REFERENCES parts(part_id),
    contributor_id UUID REFERENCES auth.users(id),

    contribution_type VARCHAR(50),
    data JSONB,
    notes TEXT,

    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by UUID REFERENCES auth.users(id),
    reviewed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bill of Materials support
CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    category VARCHAR(50),
    description TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

CREATE TABLE IF NOT EXISTS bom_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(product_id),
    part_id VARCHAR(100) REFERENCES parts(part_id),

    quantity INTEGER NOT NULL,
    position VARCHAR(100),
    notes TEXT,
    is_critical BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_contributions ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Allow public read, authenticated write
CREATE POLICY "Parts are viewable by everyone" ON parts FOR SELECT USING (true);
CREATE POLICY "Authenticated users can insert parts" ON parts FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Users can update their own parts" ON parts FOR UPDATE USING (created_by = auth.uid());

CREATE POLICY "Products are viewable by everyone" ON products FOR SELECT USING (true);
CREATE POLICY "Authenticated users can insert products" ON products FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Users can update their own products" ON products FOR UPDATE USING (created_by = auth.uid());

CREATE POLICY "Contributions are viewable by everyone" ON user_contributions FOR SELECT USING (true);
CREATE POLICY "Authenticated users can contribute" ON user_contributions FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Sample data - Common metric screws
INSERT INTO thread_specifications (thread_id, thread_standard, nominal_diameter, pitch,
    major_diameter_min, major_diameter_max, pitch_diameter_min, pitch_diameter_max,
    minor_diameter_min, minor_diameter_max, thread_class) VALUES
('M3x0.5-6H', 'ISO', 3.0, 0.5, 2.874, 2.980, 2.655, 2.720, 2.387, 2.540, '6H'),
('M4x0.7-6H', 'ISO', 4.0, 0.7, 3.838, 3.978, 3.545, 3.663, 3.141, 3.348, '6H'),
('M5x0.8-6H', 'ISO', 5.0, 0.8, 4.826, 4.976, 4.480, 4.605, 4.019, 4.284, '6H'),
('M6x1.0-6H', 'ISO', 6.0, 1.0, 5.794, 5.974, 5.350, 5.500, 4.773, 5.080, '6H'),
('M8x1.25-6H', 'ISO', 8.0, 1.25, 7.760, 7.972, 7.188, 7.376, 6.466, 6.826, '6H')
ON CONFLICT (thread_id) DO NOTHING;
