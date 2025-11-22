# Automotive Engine Parts Database

## Universal Parts Consciousness - Automotive Domain

This directory contains comprehensive engine parts catalogs with full specifications, interchangeability data, and service information.

## Available Engines

### AMC 4.0L I6 (1987-2006) - "The Indestructible Six"
- **Directory:** `AMC-4.0L-I6/`
- **Displacement:** 4.0L (242 cu in)
- **Configuration:** Inline 6-cylinder, OHV pushrod
- **Applications:** Jeep Cherokee XJ, Wrangler TJ, Grand Cherokee ZJ/WJ, Comanche MJ

## Directory Structure

```
Automotive/Engines/
├── README.md                          # This file
├── AMC-4.0L-I6/
│   ├── amc-4.0l-i6-master.json       # Engine specifications
│   ├── parts-catalog.json            # Complete parts database
│   ├── interchangeability-matrix.json # Parts interchange data
│   └── tools-and-service.json        # Tools & service procedures
└── [future-engine]/
    └── ...
```

## File Descriptions

### Master Specification File (`*-master.json`)
Contains core engine specifications:
- Displacement, bore, stroke
- Power output by year
- Vehicle applications
- Fluid capacities
- Critical dimensions
- Known issues and strengths

### Parts Catalog (`parts-catalog.json`)
Complete component database organized by system:
- **Short Block:** Block, crankshaft, connecting rods, pistons, bearings
- **Cylinder Head:** Head, valves, springs, rockers, lifters
- **Timing System:** Camshaft, timing chain, gears
- **Lubrication:** Oil pump, pickup, pan, filter
- **Cooling:** Water pump, thermostat
- **Intake/Exhaust:** Manifolds, injectors, throttle body
- **Ignition:** Distributor/coils, spark plugs, sensors
- **Gaskets & Seals:** Complete gasket sets

Each component includes:
- OEM part numbers (by year range)
- Aftermarket alternatives
- Specifications and dimensions
- Wear classification
- Quantity per engine

### Interchangeability Matrix (`interchangeability-matrix.json`)
Critical information for parts sourcing:
- **Universal Parts:** Components that swap across ALL years
- **Era Classifications:** Renix (87-90), HO (91-99), COP (00-06)
- **Cylinder Head Castings:** Good (0630, 0700) vs problematic (0331)
- **Sensor/ECU Compatibility:** What works with what
- **Popular Upgrades:** Header options, stroker kits, fuel system swaps
- **Donor Vehicle Recommendations:** Best sources for parts

### Tools & Service (`tools-and-service.json`)
Everything needed to work on the engine:
- **Tool Inventory:** Hand tools, specialty tools, measuring equipment
- **Service Operations:** Step-by-step procedures with:
  - Difficulty level
  - Time estimates
  - Required tools
  - Parts needed
  - Torque specifications
  - Procedure notes
- **Diagnostic Procedures:** Compression test, leak-down, oil pressure

## Using the Extractor Tool

```bash
# List all available engines
bun tools/integrations/automotive-engine-extractor.ts list-engines

# View Bill of Materials
bun tools/integrations/automotive-engine-extractor.ts bom-AMC-4.0L-I6

# View interchangeability data
bun tools/integrations/automotive-engine-extractor.ts interchange-AMC-4.0L-I6

# View tools and service info
bun tools/integrations/automotive-engine-extractor.ts tools-AMC-4.0L-I6

# Import to Supabase database
bun tools/integrations/automotive-engine-extractor.ts import-AMC-4.0L-I6
```

## Contributing New Engines

To add a new engine to the database:

1. Create a directory under `Automotive/Engines/` with the engine ID
2. Create the four JSON files following the existing format:
   - `{engine-id}-master.json`
   - `parts-catalog.json`
   - `interchangeability-matrix.json`
   - `tools-and-service.json`
3. Add engine data to the extractor tool
4. Run the import command

### Recommended Data Sources
- OEM Service Manuals (most authoritative)
- Aftermarket Parts Catalogs (cross-references)
- Technical Service Bulletins (known issues)
- Community Forums (real-world experience)

## Database Schema

The automotive schema extends the base parts database:

```sql
-- Core tables
engines                      -- Engine specifications
engine_components           -- Parts linked to engines
engine_vehicle_applications -- Vehicle fitment
engine_eras                 -- Production era configurations

-- Interchangeability
engine_parts_interchangeability
cylinder_head_castings

-- Service information
engine_torque_specs
engine_service_tools
engine_service_operations
engine_diagnostics
engine_fluid_specs
```

See `supabase/schema-automotive.sql` for the complete schema.

## AMC 4.0L Quick Reference

### Key Specifications
| Spec | Value |
|------|-------|
| Displacement | 4.0L (242 cu in) |
| Bore x Stroke | 3.875" x 3.414" |
| Compression | 8.8:1 |
| HP | 177-190 (varies by year) |
| Torque | 224-235 lb-ft |
| Oil Capacity | 6 quarts (with filter) |
| Coolant | 12 quarts |

### Critical Torque Specs (lb-ft)
| Fastener | Torque |
|----------|--------|
| Head Bolts | 110 (3 passes) |
| Main Caps | 80 |
| Rod Bolts | 33 |
| Flywheel | 105 |
| Spark Plugs | 27 |
| Exhaust Manifold | 23 |

### Era Quick Guide
| Era | Years | Key Feature |
|-----|-------|-------------|
| Renix | 1987-1990 | Coil pack ignition |
| HO Pre-OBD2 | 1991-1995 | Distributor, 1 O2 sensor |
| HO OBD-II | 1996-1999 | 2 O2 sensors |
| HO COP | 2000-2006 | Coil-on-plug |

### ⚠️ Important Warnings
1. **AVOID 0331 cylinder head casting** (1999-2001) - Prone to cracking
2. **Exhaust manifolds crack** - Plan for replacement or header upgrade
3. **Water pump typically fails around 100k miles** - Replace proactively
4. **Pre-oil engine before first start** after rebuild

## License

This data is provided for educational and reference purposes. Always verify specifications against official service manuals before performing work.
