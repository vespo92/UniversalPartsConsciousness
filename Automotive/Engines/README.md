# Automotive Engine Parts Database

## Universal Parts Consciousness - Automotive Domain

This directory contains comprehensive engine parts catalogs with full specifications, interchangeability data, aftermarket ecosystem information, and service procedures.

## Directory Structure - Organized by Manufacturer

```
Automotive/Engines/
├── README.md                           # This file
└── Manufacturers/
    ├── AMC/
    │   └── AMC-4.0L-I6/               # Jeep 4.0L Inline-6
    ├── BMW/
    │   ├── BMW-B58-3.0L-I6/           # B58 TwinPower Turbo
    │   ├── BMW-M52-2.8L-I6/           # M52 VANOS
    │   ├── BMW-M54-3.0L-I6/           # M54 VANOS
    │   ├── BMW-N54-3.0L-I6/           # N54 Twin-Turbo
    │   ├── BMW-N55-3.0L-I6/           # N55 Single Twin-Scroll
    │   └── BMW-S54-3.2L-I6/           # S54 Motorsport
    └── VAG/                            # Volkswagen Auto Group
        ├── Audi/
        │   ├── AUDI-EA211-1.4L-TFSI-I4/   # EA211 1.4T
        │   └── AUDI-EA888-2.0L-TFSI-I4/   # EA888 2.0T (Gen1-4)
        ├── Volkswagen/                  # (Future)
        ├── Porsche/                     # (Future)
        └── Shared-Components/           # VAG-wide shared parts
            ├── VAG-engine-families.json
            ├── turbo-is20.json
            └── turbo-is38.json
```

## Available Engines

### VAG (Volkswagen Auto Group)

#### Audi EA211 1.4L TFSI I4 (2012-present)
- **Directory:** `Manufacturers/VAG/Audi/AUDI-EA211-1.4L-TFSI-I4/`
- **Displacement:** 1.4L (1395cc)
- **Configuration:** Inline 4-cylinder, DOHC, turbocharged
- **Power:** 125-150 HP
- **Turbo:** IHI IS12
- **Applications:** Audi A1, A3, Q2, Q3 | VW Golf, Tiguan | SEAT Leon | Skoda Octavia

#### Audi EA888 2.0L TFSI I4 (2008-present)
- **Directory:** `Manufacturers/VAG/Audi/AUDI-EA888-2.0L-TFSI-I4/`
- **Displacement:** 2.0L (1984cc)
- **Configuration:** Inline 4-cylinder, DOHC, turbocharged
- **Power:** 170-333 HP (variant dependent)
- **Generations:** Gen1, Gen2, Gen3, Gen3B, Gen4
- **Turbo:** IS20 (GTI) / IS38 (Golf R, S3)
- **Applications:**
  - VW Golf GTI/R, Jetta GLI, Tiguan, Passat, Arteon
  - Audi A3, S3, A4, TT, TTS, Q3, Q5
  - SEAT Leon Cupra, Ateca
  - Skoda Octavia RS, Superb
  - Porsche Macan (base)

### BMW

#### BMW B58 3.0L I6 (2015-present)
- **Directory:** `Manufacturers/BMW/BMW-B58-3.0L-I6/`
- **Displacement:** 3.0L (2998cc)
- **Configuration:** Inline 6-cylinder, DOHC, single twin-scroll turbo
- **Power:** 335-382 HP
- **Applications:** 340i, M340i, 540i, X3 M40i, Supra

#### BMW N54 3.0L I6 (2006-2016)
- **Directory:** `Manufacturers/BMW/BMW-N54-3.0L-I6/`
- **Displacement:** 3.0L (2979cc)
- **Configuration:** Inline 6-cylinder, DOHC, twin turbo
- **Power:** 300-335 HP
- **Applications:** 135i, 335i, 535i, Z4 35i

#### BMW N55 3.0L I6 (2009-2018)
- **Directory:** `Manufacturers/BMW/BMW-N55-3.0L-I6/`
- **Displacement:** 3.0L (2979cc)
- **Configuration:** Inline 6-cylinder, DOHC, single twin-scroll turbo
- **Power:** 302-326 HP
- **Applications:** 335i, 435i, 535i, X5 35i, M235i

#### BMW M54 3.0L I6 (2000-2006)
- **Directory:** `Manufacturers/BMW/BMW-M54-3.0L-I6/`
- **Displacement:** 3.0L (2979cc)
- **Configuration:** Inline 6-cylinder, DOHC, naturally aspirated
- **Power:** 231 HP
- **Applications:** 330i, 530i, X3 3.0i, X5 3.0i, Z4 3.0i

#### BMW M52 2.8L I6 (1994-2000)
- **Directory:** `Manufacturers/BMW/BMW-M52-2.8L-I6/`
- **Displacement:** 2.8L (2793cc)
- **Configuration:** Inline 6-cylinder, DOHC, naturally aspirated
- **Power:** 193 HP
- **Applications:** 328i, 528i, Z3 2.8

#### BMW S54 3.2L I6 (2000-2006)
- **Directory:** `Manufacturers/BMW/BMW-S54-3.2L-I6/`
- **Displacement:** 3.2L (3246cc)
- **Configuration:** Inline 6-cylinder, DOHC, naturally aspirated, motorsport
- **Power:** 333-360 HP
- **Applications:** M3 E46, Z3M, Z4M

### AMC

#### AMC 4.0L I6 (1987-2006) - "The Indestructible Six"
- **Directory:** `Manufacturers/AMC/AMC-4.0L-I6/`
- **Displacement:** 4.0L (242 cu in)
- **Configuration:** Inline 6-cylinder, OHV pushrod
- **Power:** 177-190 HP
- **Applications:** Jeep Cherokee XJ, Wrangler TJ/YJ, Grand Cherokee ZJ/WJ, Comanche MJ

## File Structure Per Engine

Each engine directory contains 5 standardized JSON files:

```
{ENGINE-ID}/
├── {engine}-master.json           # Engine specifications
├── parts-catalog.json             # Complete parts database
├── interchangeability-matrix.json # Parts interchange data
├── tools-and-service.json         # Tools & service procedures
└── aftermarket-ecosystem.json     # Vendors, parts, tuning (performance engines)
```

### Master Specification File (`*-master.json`)
Contains core engine specifications:
- Displacement, bore, stroke, compression
- Power output by variant/year
- Vehicle applications
- Fluid capacities
- Design features
- Known issues and strengths
- Tuning potential

### Parts Catalog (`parts-catalog.json`)
Complete component database organized by system:
- **Short Block:** Block, crankshaft, connecting rods, pistons, bearings
- **Cylinder Head:** Head, valves, springs, camshafts, timing
- **Turbo System:** Turbocharger, intercooler, wastegate (where applicable)
- **Fuel System:** Pumps, injectors, rails
- **Intake/Exhaust:** Manifolds, filters, downpipes
- **Cooling:** Water pump, thermostat, radiator
- **Ignition:** Coils, spark plugs, sensors
- **Lubrication:** Oil pump, filter, pan
- **Gaskets & Seals:** Complete sets

### Interchangeability Matrix (`interchangeability-matrix.json`)
Critical information for parts sourcing:
- Cross-brand compatibility (VAG engines especially)
- Era/generation classifications
- Turbo interchange guides
- Popular upgrade paths
- ECU tuning compatibility
- Transmission compatibility

### Tools & Service (`tools-and-service.json`)
Everything needed to work on the engine:
- Tool inventory (hand tools, specialty tools)
- Service procedures with step-by-step instructions
- Diagnostic procedures
- Torque specifications
- Fluid specifications

### Aftermarket Ecosystem (`aftermarket-ecosystem.json`)
Performance and maintenance parts market:
- Vendors and retailers
- Tuning companies and software
- Performance parts catalog
- Build packages with pricing
- Community resources

## VAG Shared Components

VAG (Volkswagen Auto Group) engines share many components across brands. The `Shared-Components` directory contains:

- **VAG-engine-families.json:** Overview of all VAG engine families
- **turbo-is20.json:** IS20 turbo specifications and applications
- **turbo-is38.json:** IS38 turbo specifications and applications

### Cross-Brand Compatibility
VAG engines are extensively shared:
- EA211 1.4T: Audi A3, VW Golf, SEAT Leon, Skoda Octavia
- EA888 2.0T: VW GTI/R, Audi S3, SEAT Cupra, Porsche Macan

Parts like turbos, injectors, and sensors are fully interchangeable across brands.

## Using the Extractor Tool

```bash
# List all available engines
bun tools/integrations/automotive-engine-extractor.ts list-engines

# View Bill of Materials
bun tools/integrations/automotive-engine-extractor.ts bom-AMC-4.0L-I6

# View interchangeability data
bun tools/integrations/automotive-engine-extractor.ts interchange-VAG-EA888-2.0L-TFSI-I4

# View tools and service info
bun tools/integrations/automotive-engine-extractor.ts tools-BMW-B58-3.0L-I6

# View aftermarket ecosystem
bun tools/integrations/automotive-engine-extractor.ts aftermarket-VAG-EA888-2.0L-TFSI-I4

# Import to Supabase database
bun tools/integrations/automotive-engine-extractor.ts import-VAG-EA888-2.0L-TFSI-I4
```

## Contributing New Engines

To add a new engine to the database:

1. Create a directory under the appropriate manufacturer folder
2. Create the five JSON files following the existing format
3. Update this README with the new engine
4. Add engine data to the extractor tool
5. Run the import command

### Organization Guidelines
- Group by manufacturer first
- For conglomerates (VAG, Stellantis), use shared component directories
- Include cross-references between related engines
- Document interchangeability with other brands/engines

## Quick Reference - Popular Engines

### VAG EA888 2.0T Tuning Quick Reference
| Stage | Power (IS20) | Power (IS38) | Required Mods |
|-------|--------------|--------------|---------------|
| Stock | 220-245 HP | 310 HP | - |
| Stage 1 | 280-300 HP | 370-400 HP | ECU tune |
| Stage 2 | 320-340 HP | 420-450 HP | Tune + downpipe + intake |
| IS38 Swap | 370-420 HP | - | IS38 turbo + tune |
| Hybrid | - | 475-550 HP | TTE475/525 + tune |

### BMW B58 Tuning Quick Reference
| Stage | Power | Required Mods |
|-------|-------|---------------|
| Stock | 335-382 HP | - |
| Stage 1 | 420-450 HP | ECU tune |
| Stage 2 | 500-550 HP | Tune + downpipe + intake |
| Pure 800 | 700-800 HP | Big turbo + built engine |

## License

This data is provided for educational and reference purposes. Always verify specifications against official service manuals before performing work.
