-- ============================================================================
-- AUTOMOTIVE ENGINE SCHEMA EXTENSION
-- Universal Parts Consciousness - Automotive Domain
-- ============================================================================
-- This schema extends the base parts database to support automotive engine
-- components with full interchangeability tracking, service specifications,
-- and tool requirements.
-- ============================================================================

-- ============================================================================
-- ENGINES TABLE
-- Master table for engine specifications
-- ============================================================================
CREATE TABLE IF NOT EXISTS engines (
  engine_id VARCHAR(100) PRIMARY KEY,
  manufacturer VARCHAR(100) NOT NULL,
  engine_family VARCHAR(100),
  common_names TEXT[], -- Array of common names (e.g., "AMC 4.0", "Jeep 4.0")
  production_start_year INTEGER,
  production_end_year INTEGER,

  -- Basic specifications
  configuration VARCHAR(50), -- "Inline 6", "V8", "Flat 4", etc.
  displacement_cc INTEGER,
  displacement_liters DECIMAL(4,2),
  displacement_cubic_inches DECIMAL(6,2),
  bore_mm DECIMAL(6,3),
  stroke_mm DECIMAL(6,3),
  compression_ratio DECIMAL(4,2),

  -- Performance (base/stock)
  horsepower_peak INTEGER,
  horsepower_rpm INTEGER,
  torque_lb_ft_peak INTEGER,
  torque_rpm INTEGER,

  -- Construction
  block_material VARCHAR(50), -- cast_iron, aluminum, etc.
  head_material VARCHAR(50),
  valvetrain_type VARCHAR(50), -- OHV, SOHC, DOHC
  valve_count INTEGER,
  firing_order VARCHAR(50),

  -- Extended specifications (JSONB for flexibility)
  full_specs JSONB DEFAULT '{}'::JSONB,

  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  data_source VARCHAR(200),
  verification_status VARCHAR(50) DEFAULT 'unverified'
);

-- ============================================================================
-- ENGINE COMPONENTS TABLE
-- Links parts to specific engines with location and quantity
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_components (
  component_id VARCHAR(150) PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,
  part_id VARCHAR(100), -- References parts table if exists

  -- Component identification
  component_type VARCHAR(100) NOT NULL, -- piston, crankshaft, camshaft, etc.
  component_name VARCHAR(200),
  system_category VARCHAR(100), -- short_block, cylinder_head, timing, etc.

  -- Location in engine
  location_description VARCHAR(200),
  cylinder_number INTEGER, -- For cylinder-specific parts
  bank VARCHAR(10), -- For V/flat engines: 'left', 'right'

  -- Quantity and specs
  quantity_per_engine INTEGER DEFAULT 1,
  oem_part_numbers JSONB, -- Can be multiple by year
  aftermarket_options JSONB,

  -- Service information
  wear_classification VARCHAR(50), -- consumable, rebuild_item, long_life
  replacement_interval_miles INTEGER,
  replacement_interval_hours INTEGER,

  -- Specifications
  specifications JSONB DEFAULT '{}'::JSONB,

  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- ENGINE VEHICLE APPLICATIONS
-- Which vehicles used which engines
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_vehicle_applications (
  application_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  -- Vehicle information
  make VARCHAR(100) NOT NULL,
  model VARCHAR(100) NOT NULL,
  platform_code VARCHAR(20), -- XJ, TJ, ZJ, etc.
  start_year INTEGER NOT NULL,
  end_year INTEGER NOT NULL,

  -- Variant information
  transmission_options TEXT[],
  drive_type VARCHAR(50), -- 4WD, RWD, FWD, AWD

  -- Notes
  notes TEXT,

  UNIQUE(engine_id, make, model, start_year)
);

-- ============================================================================
-- ENGINE ERA CLASSIFICATIONS
-- Different configurations by production era
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_eras (
  era_id VARCHAR(100) PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  era_name VARCHAR(100) NOT NULL,
  start_year INTEGER NOT NULL,
  end_year INTEGER NOT NULL,

  -- System configurations
  fuel_injection_type VARCHAR(100),
  ignition_type VARCHAR(100),
  ecu_type VARCHAR(100),
  obd_standard VARCHAR(50), -- Pre-OBD, OBD-I, OBD-II

  -- Era-specific specs
  horsepower INTEGER,
  torque_lb_ft INTEGER,
  compression_ratio DECIMAL(4,2),

  -- Extended specs
  era_specs JSONB DEFAULT '{}'::JSONB,

  -- Interchangeability notes
  interchangeability_notes TEXT
);

-- ============================================================================
-- PARTS INTERCHANGEABILITY
-- Cross-reference for parts that work across years/vehicles
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_parts_interchangeability (
  interchange_id SERIAL PRIMARY KEY,
  part_id VARCHAR(100), -- Source part
  component_type VARCHAR(100) NOT NULL,

  -- Compatible range
  compatible_engines VARCHAR(100)[], -- Array of engine_ids
  compatible_years_start INTEGER,
  compatible_years_end INTEGER,

  -- Compatibility details
  compatibility_score INTEGER CHECK (compatibility_score BETWEEN 0 AND 100),
  compatibility_notes TEXT,
  modifications_required TEXT,
  warnings TEXT,

  -- Verification
  verified BOOLEAN DEFAULT FALSE,
  verified_by VARCHAR(100),
  verified_date TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- CYLINDER HEAD CASTINGS
-- Track specific castings and their characteristics
-- ============================================================================
CREATE TABLE IF NOT EXISTS cylinder_head_castings (
  casting_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  casting_number VARCHAR(50) NOT NULL,
  production_years VARCHAR(50),

  -- Specifications
  combustion_chamber_cc DECIMAL(6,2),
  intake_port_volume_cc DECIMAL(6,2),
  exhaust_port_volume_cc DECIMAL(6,2),
  intake_valve_diameter_inches DECIMAL(5,4),
  exhaust_valve_diameter_inches DECIMAL(5,4),

  -- Quality rating
  quality_rating VARCHAR(50), -- excellent, good, problematic, avoid
  known_issues TEXT,
  recommendations TEXT,

  -- Interchangeability
  interchanges_with TEXT[], -- Other casting numbers

  UNIQUE(engine_id, casting_number)
);

-- ============================================================================
-- TORQUE SPECIFICATIONS
-- Detailed torque specs for all fasteners
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_torque_specs (
  torque_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  -- Fastener identification
  fastener_location VARCHAR(200) NOT NULL,
  fastener_description VARCHAR(200),
  fastener_size VARCHAR(50), -- M10x1.5, 7/16-14, etc.

  -- Torque specifications
  torque_lb_ft DECIMAL(6,1),
  torque_nm DECIMAL(6,1),
  torque_lb_in DECIMAL(6,1),

  -- Procedure
  torque_sequence TEXT, -- Description or JSON array of sequence
  torque_method VARCHAR(50), -- standard, torque_angle, torque_to_yield
  angle_degrees INTEGER, -- For torque-angle method
  passes INTEGER DEFAULT 1, -- Number of passes

  -- Thread preparation
  thread_prep VARCHAR(100), -- dry, oiled, thread_lock, anti_seize

  -- Notes
  notes TEXT,

  UNIQUE(engine_id, fastener_location)
);

-- ============================================================================
-- SERVICE TOOLS
-- Required tools for engine service operations
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_service_tools (
  tool_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  -- Tool identification
  tool_name VARCHAR(200) NOT NULL,
  tool_category VARCHAR(100), -- hand_tool, specialty, measuring, etc.
  tool_description TEXT,

  -- Specifications
  sizes_required TEXT[], -- Array of sizes needed
  part_numbers JSONB, -- Brand -> part number mapping

  -- Usage
  operations_used_for TEXT[],
  priority VARCHAR(50), -- essential, recommended, optional

  -- Availability
  rental_available BOOLEAN DEFAULT FALSE,
  diy_alternative TEXT,
  estimated_cost_usd DECIMAL(8,2),

  UNIQUE(engine_id, tool_name)
);

-- ============================================================================
-- SERVICE OPERATIONS
-- Detailed service procedures
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_service_operations (
  operation_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  -- Operation identification
  operation_name VARCHAR(200) NOT NULL,
  operation_category VARCHAR(100), -- maintenance, repair, rebuild
  operation_description TEXT,

  -- Timing
  difficulty_level VARCHAR(50), -- beginner, intermediate, advanced, expert
  estimated_time_hours DECIMAL(4,1),
  estimated_time_minutes INTEGER,

  -- Intervals (for maintenance)
  interval_miles INTEGER,
  interval_months INTEGER,
  interval_hours INTEGER, -- Engine hours for stationary/marine

  -- Requirements
  tools_required JSONB, -- Array of tool references
  parts_required JSONB, -- Array of part references
  consumables_required JSONB, -- Fluids, gaskets, etc.

  -- Procedure
  procedure_steps JSONB, -- Ordered array of steps
  torque_specs JSONB, -- Relevant torque specs
  warnings TEXT[],
  tips TEXT[],

  -- Symptoms (for repairs)
  symptoms TEXT[],

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(engine_id, operation_name)
);

-- ============================================================================
-- DIAGNOSTIC PROCEDURES
-- Troubleshooting and testing procedures
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_diagnostics (
  diagnostic_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  -- Test identification
  test_name VARCHAR(200) NOT NULL,
  test_category VARCHAR(100), -- compression, leak_down, oil_pressure, etc.
  test_description TEXT,

  -- Requirements
  tools_required JSONB,
  preconditions TEXT[],

  -- Procedure
  procedure_steps JSONB,

  -- Specifications
  specifications JSONB, -- Expected values with min/max
  diagnosis_guide JSONB, -- Symptom -> likely cause mapping

  UNIQUE(engine_id, test_name)
);

-- ============================================================================
-- ENGINE FLUIDS
-- Fluid specifications and capacities
-- ============================================================================
CREATE TABLE IF NOT EXISTS engine_fluid_specs (
  fluid_id SERIAL PRIMARY KEY,
  engine_id VARCHAR(100) REFERENCES engines(engine_id) ON DELETE CASCADE,

  -- Fluid identification
  fluid_type VARCHAR(100) NOT NULL, -- engine_oil, coolant, trans_fluid, etc.
  fluid_location VARCHAR(100),

  -- Capacity
  capacity_quarts DECIMAL(5,2),
  capacity_liters DECIMAL(5,2),
  includes_filter BOOLEAN DEFAULT FALSE,

  -- Specifications
  fluid_specifications TEXT[], -- 5W-30, ATF+4, etc.
  api_rating VARCHAR(50),
  oem_part_number VARCHAR(100),

  -- Notes
  notes TEXT,

  UNIQUE(engine_id, fluid_type, fluid_location)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_engines_manufacturer ON engines(manufacturer);
CREATE INDEX IF NOT EXISTS idx_engines_displacement ON engines(displacement_liters);
CREATE INDEX IF NOT EXISTS idx_engines_years ON engines(production_start_year, production_end_year);

CREATE INDEX IF NOT EXISTS idx_engine_components_engine ON engine_components(engine_id);
CREATE INDEX IF NOT EXISTS idx_engine_components_type ON engine_components(component_type);
CREATE INDEX IF NOT EXISTS idx_engine_components_system ON engine_components(system_category);

CREATE INDEX IF NOT EXISTS idx_vehicle_apps_engine ON engine_vehicle_applications(engine_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_apps_make_model ON engine_vehicle_applications(make, model);
CREATE INDEX IF NOT EXISTS idx_vehicle_apps_years ON engine_vehicle_applications(start_year, end_year);

CREATE INDEX IF NOT EXISTS idx_interchange_part ON engine_parts_interchangeability(part_id);
CREATE INDEX IF NOT EXISTS idx_interchange_type ON engine_parts_interchangeability(component_type);

CREATE INDEX IF NOT EXISTS idx_torque_engine ON engine_torque_specs(engine_id);
CREATE INDEX IF NOT EXISTS idx_operations_engine ON engine_service_operations(engine_id);
CREATE INDEX IF NOT EXISTS idx_operations_category ON engine_service_operations(operation_category);

-- ============================================================================
-- HELPER VIEWS
-- ============================================================================

-- View: Complete engine info with vehicle applications
CREATE OR REPLACE VIEW v_engine_applications AS
SELECT
  e.engine_id,
  e.manufacturer,
  e.common_names[1] AS primary_name,
  e.displacement_liters,
  e.configuration,
  e.horsepower_peak,
  e.production_start_year,
  e.production_end_year,
  a.make,
  a.model,
  a.platform_code,
  a.start_year AS app_start_year,
  a.end_year AS app_end_year
FROM engines e
LEFT JOIN engine_vehicle_applications a ON e.engine_id = a.engine_id;

-- View: Parts with interchangeability summary
CREATE OR REPLACE VIEW v_parts_interchange AS
SELECT
  c.component_id,
  c.engine_id,
  c.component_type,
  c.component_name,
  c.quantity_per_engine,
  c.wear_classification,
  i.compatible_years_start,
  i.compatible_years_end,
  i.compatibility_score,
  i.compatibility_notes
FROM engine_components c
LEFT JOIN engine_parts_interchangeability i
  ON c.component_type = i.component_type
  AND c.engine_id = ANY(i.compatible_engines);

-- ============================================================================
-- SAMPLE DATA: AMC 4.0L I6
-- ============================================================================

-- Insert the AMC 4.0L engine
INSERT INTO engines (
  engine_id,
  manufacturer,
  engine_family,
  common_names,
  production_start_year,
  production_end_year,
  configuration,
  displacement_cc,
  displacement_liters,
  displacement_cubic_inches,
  bore_mm,
  stroke_mm,
  compression_ratio,
  horsepower_peak,
  horsepower_rpm,
  torque_lb_ft_peak,
  torque_rpm,
  block_material,
  head_material,
  valvetrain_type,
  valve_count,
  firing_order,
  verification_status,
  data_source
) VALUES (
  'AMC-4.0L-I6-POWERTECH',
  'American Motors Corporation / Chrysler',
  'AMC Straight-6',
  ARRAY['AMC 4.0', 'Jeep 4.0', 'Power Tech I6', '242 Inline Six', 'The Indestructible Six'],
  1987,
  2006,
  'Inline 6-cylinder',
  3958,
  4.0,
  242,
  98.43,
  86.72,
  8.8,
  190,
  4750,
  235,
  3200,
  'cast_iron',
  'cast_iron',
  'OHV pushrod',
  12,
  '1-5-3-6-2-4',
  'verified',
  'OEM Service Manual, Community Verification'
) ON CONFLICT (engine_id) DO NOTHING;

-- Insert vehicle applications
INSERT INTO engine_vehicle_applications (engine_id, make, model, platform_code, start_year, end_year, transmission_options, drive_type, notes) VALUES
('AMC-4.0L-I6-POWERTECH', 'Jeep', 'Cherokee', 'XJ', 1987, 2001, ARRAY['AX5', 'AX15', 'AW4', '42RE'], '4WD', 'Most common application'),
('AMC-4.0L-I6-POWERTECH', 'Jeep', 'Comanche', 'MJ', 1987, 1992, ARRAY['AX5', 'AX15', 'AW4'], '4WD', 'Pickup truck variant'),
('AMC-4.0L-I6-POWERTECH', 'Jeep', 'Grand Cherokee', 'ZJ', 1993, 1998, ARRAY['AX15', 'AW4', '42RE'], '4WD', 'First gen Grand Cherokee'),
('AMC-4.0L-I6-POWERTECH', 'Jeep', 'Wrangler', 'TJ', 1997, 2006, ARRAY['AX5', 'AX15', 'NV3550', '42RLE'], '4WD', 'Most popular Wrangler engine'),
('AMC-4.0L-I6-POWERTECH', 'Jeep', 'Grand Cherokee', 'WJ', 1999, 2004, ARRAY['42RE', '45RFE'], '4WD', 'Second gen Grand Cherokee')
ON CONFLICT DO NOTHING;

-- Insert era classifications
INSERT INTO engine_eras (era_id, engine_id, era_name, start_year, end_year, fuel_injection_type, ignition_type, ecu_type, obd_standard, horsepower, torque_lb_ft, interchangeability_notes) VALUES
('AMC-40-RENIX', 'AMC-4.0L-I6-POWERTECH', 'Renix Era', 1987, 1990, 'Renix Multi-Point Fuel Injection', 'Distributorless coil pack', 'Renix ECU', 'Pre-OBD', 177, 224, 'Renix components not compatible with later years without significant modification'),
('AMC-40-HO-PRE-OBD2', 'AMC-4.0L-I6-POWERTECH', 'HO Pre-OBD-II', 1991, 1995, 'Chrysler SMPI', 'Distributor with single coil', 'Chrysler SBEC', 'OBD-I', 190, 225, 'Cross-compatible with 1996-1999 with minor harness changes'),
('AMC-40-HO-OBD2', 'AMC-4.0L-I6-POWERTECH', 'HO OBD-II', 1996, 1999, 'Chrysler SMPI', 'Distributor with single coil', 'Chrysler PCM', 'OBD-II', 190, 225, 'Requires upstream and downstream O2 sensors'),
('AMC-40-HO-COP', 'AMC-4.0L-I6-POWERTECH', 'HO Coil-on-Plug', 2000, 2006, 'Chrysler SMPI', 'Coil-on-Plug (distributorless)', 'Chrysler NGC PCM', 'OBD-II', 190, 235, 'Requires 60-tooth reluctor wheel on crankshaft')
ON CONFLICT DO NOTHING;

-- Insert cylinder head castings
INSERT INTO cylinder_head_castings (engine_id, casting_number, production_years, combustion_chamber_cc, intake_valve_diameter_inches, exhaust_valve_diameter_inches, quality_rating, known_issues, recommendations, interchanges_with) VALUES
('AMC-4.0L-I6-POWERTECH', '7120', '1987-1990', 58.86, 1.895, 1.505, 'good', 'Smaller intake ports than later heads', 'Adequate for stock applications', ARRAY['7120']),
('AMC-4.0L-I6-POWERTECH', '0630', '1991-1998', 59.02, 1.895, 1.505, 'excellent', 'None known', 'Best head casting - highly recommended', ARRAY['0630', '0700']),
('AMC-4.0L-I6-POWERTECH', '0700', '1991-1998', 59.02, 1.895, 1.505, 'excellent', 'None known', 'Excellent choice - equivalent to 0630', ARRAY['0630', '0700']),
('AMC-4.0L-I6-POWERTECH', '0331', '1999-2001', 59.02, 1.895, 1.505, 'problematic', 'Prone to cracking between cylinders #3 and #4. 15-20% failure rate.', 'AVOID - Replace with 0630 or 0700 casting if possible', ARRAY['0331'])
ON CONFLICT DO NOTHING;

-- Insert key torque specifications
INSERT INTO engine_torque_specs (engine_id, fastener_location, fastener_description, fastener_size, torque_lb_ft, torque_method, passes, thread_prep, notes) VALUES
('AMC-4.0L-I6-POWERTECH', 'Cylinder head bolts', 'Head to block', '7/16-14 x 4.0"', 110, 'standard', 3, 'oiled', 'Torque in 3 passes: 40, 80, 110 lb-ft. Center-out pattern.'),
('AMC-4.0L-I6-POWERTECH', 'Main bearing cap bolts', 'Main caps to block', '1/2-13', 80, 'standard', 1, 'oiled', 'Torque evenly, center caps first'),
('AMC-4.0L-I6-POWERTECH', 'Connecting rod bolts', 'Rod cap to rod', '3/8-24', 33, 'standard', 1, 'oiled', 'Check rod side clearance after torque'),
('AMC-4.0L-I6-POWERTECH', 'Flywheel/flexplate bolts', 'Flywheel to crank', '7/16-20', 105, 'standard', 1, 'thread_lock', 'Use blue thread locker'),
('AMC-4.0L-I6-POWERTECH', 'Harmonic balancer bolt', 'Balancer to crank', '5/8-18', 80, 'standard', 1, 'oiled', 'Hold crank with flywheel lock'),
('AMC-4.0L-I6-POWERTECH', 'Intake manifold bolts', 'Intake to head', '5/16-18', 23, 'standard', 2, 'dry', 'Torque in 2 passes, center-out'),
('AMC-4.0L-I6-POWERTECH', 'Exhaust manifold nuts', 'Exhaust to head', '3/8-16', 23, 'standard', 1, 'anti_seize', 'Apply copper anti-seize for future removal'),
('AMC-4.0L-I6-POWERTECH', 'Valve cover bolts', 'Valve cover to head', '1/4-20', 7, 'standard', 1, 'dry', '85 lb-in, do not overtighten'),
('AMC-4.0L-I6-POWERTECH', 'Oil pan bolts', 'Pan to block', '1/4-20', 11, 'standard', 1, 'dry', 'Torque in crisscross pattern'),
('AMC-4.0L-I6-POWERTECH', 'Water pump bolts', 'Pump to cover', '5/16-18', 22, 'standard', 1, 'thread_sealant', 'Use thread sealant on bolts entering water jacket'),
('AMC-4.0L-I6-POWERTECH', 'Thermostat housing bolts', 'Housing to head', '5/16-18', 17, 'standard', 1, 'dry', NULL),
('AMC-4.0L-I6-POWERTECH', 'Spark plugs', 'Plugs to head', '14mm x 1.25', 27, 'standard', 1, 'anti_seize', 'Apply thin coat of anti-seize to threads'),
('AMC-4.0L-I6-POWERTECH', 'Oil drain plug', 'Plug to pan', '18mm x 1.5', 25, 'standard', 1, 'dry', 'Replace crush washer if damaged'),
('AMC-4.0L-I6-POWERTECH', 'Rocker arm bolts', 'Rocker to head', '5/16-18', 21, 'standard', 1, 'oiled', 'Torque with lifter on base circle')
ON CONFLICT DO NOTHING;

-- Insert fluid specifications
INSERT INTO engine_fluid_specs (engine_id, fluid_type, fluid_location, capacity_quarts, capacity_liters, includes_filter, fluid_specifications, api_rating, notes) VALUES
('AMC-4.0L-I6-POWERTECH', 'engine_oil', 'crankcase', 6.0, 5.7, true, ARRAY['5W-30', '10W-30'], 'SJ or higher', 'Capacity includes filter. Use 5W-30 for cold climates.'),
('AMC-4.0L-I6-POWERTECH', 'coolant', 'cooling_system', 12.0, 11.4, false, ARRAY['HOAT', 'MS-9769'], NULL, 'Use HOAT (Hybrid Organic Acid Technology) coolant only. 50/50 mix.'),
('AMC-4.0L-I6-POWERTECH', 'transmission_fluid', 'AX15_manual', 3.25, 3.1, false, ARRAY['75W-90 GL-3'], NULL, 'Do not use GL-5 - will damage synchros'),
('AMC-4.0L-I6-POWERTECH', 'transmission_fluid', '42RE_auto', 8.0, 7.6, true, ARRAY['ATF+4', 'MS-9602'], NULL, 'Use ATF+4 only. Do not mix with other ATF types.'),
('AMC-4.0L-I6-POWERTECH', 'transfer_case', 'NP231', 1.2, 1.1, false, ARRAY['ATF+4', 'Dexron III'], NULL, 'ATF+4 preferred'),
('AMC-4.0L-I6-POWERTECH', 'power_steering', 'reservoir', 1.5, 1.4, false, ARRAY['ATF+4', 'Power Steering Fluid'], NULL, 'ATF+4 works well as PS fluid')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================
COMMENT ON TABLE engines IS 'Master table for automotive engine specifications';
COMMENT ON TABLE engine_components IS 'Individual components/parts that make up an engine';
COMMENT ON TABLE engine_vehicle_applications IS 'Which vehicles used which engines';
COMMENT ON TABLE engine_eras IS 'Production era classifications with configuration differences';
COMMENT ON TABLE engine_parts_interchangeability IS 'Parts compatibility across years and models';
COMMENT ON TABLE cylinder_head_castings IS 'Cylinder head casting numbers with quality ratings';
COMMENT ON TABLE engine_torque_specs IS 'Torque specifications for all engine fasteners';
COMMENT ON TABLE engine_service_tools IS 'Required tools for engine service operations';
COMMENT ON TABLE engine_service_operations IS 'Detailed service and repair procedures';
COMMENT ON TABLE engine_diagnostics IS 'Diagnostic and testing procedures';
COMMENT ON TABLE engine_fluid_specs IS 'Fluid types, specifications, and capacities';
