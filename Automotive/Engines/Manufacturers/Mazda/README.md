# Mazda Motor Corporation - Engine Database

## Overview

Mazda Motor Corporation, headquartered in Hiroshima, Japan, is a unique automaker known for its commitment to the rotary (Wankel) engine and its philosophy of "Jinba Ittai" (horse and rider as one). This database documents Mazda's complete engine history from the 1950s to present day.

## Company History

- **1920**: Founded as Toyo Cork Kogyo Co., Ltd.
- **1931**: First motorized vehicle - Mazda-Go three-wheeled truck
- **1967**: Cosmo Sport 110S - World's first twin-rotor production car
- **1991**: 787B wins Le Mans 24 Hours - Only rotary victory in history
- **2012**: Skyactiv technology debuts with revolutionary high-compression engines
- **2019**: Skyactiv-X SPCCI - World's first production compression-ignition gasoline engine

## Engine Families

### Rotary (Wankel) Engines
Mazda is the only manufacturer to successfully mass-produce rotary engines.

| Engine | Displacement | Years | Notable Applications |
|--------|-------------|-------|---------------------|
| 10A | 982cc | 1967-1973 | Cosmo Sport, R100 |
| **12A** | 1,146cc | 1970-1985 | RX-3, RX-7 FB |
| **13B** | 1,308cc | 1973-2012 | RX-7 FC/FD, RX-8 |
| 13B-REW | 1,308cc | 1992-2002 | RX-7 FD (Twin Turbo) |
| Renesis | 1,308cc | 2003-2012 | RX-8 |
| 20B | 1,962cc | 1990-1995 | Eunos Cosmo |
| 8C | 830cc | 2021-present | MX-30 R-EV |

### B-Series (Miata/MX-5)
The heart of the world's best-selling roadster.

| Engine | Displacement | Years | Notable Applications |
|--------|-------------|-------|---------------------|
| **B6-ZE** | 1.6L | 1989-1993 | Miata NA (1st gen) |
| **BP-ZE/4W** | 1.8L | 1994-2005 | Miata NA/NB |

### MZR Series
Co-developed with Ford, powering Mazda's 2000s lineup.

| Engine | Displacement | Years | Notable Applications |
|--------|-------------|-------|---------------------|
| LF-DE/VE | 2.0L | 2001-2018 | Mazda3, MX-5 NC |
| **L3-VDT** | 2.3L Turbo | 2005-2013 | Mazdaspeed 3/6 |

### Skyactiv-G (Gasoline)
Revolutionary ultra-high compression naturally aspirated engines.

| Engine | Displacement | Compression | Years | Notable Applications |
|--------|-------------|-------------|-------|---------------------|
| PE-VPS | 2.0L | 13.0:1 | 2011-present | Mazda3, MX-5 ND |
| PY-VPS | 2.5L | 13.0:1 | 2012-present | Mazda6, CX-5 |
| **PY-VPTS** | 2.5L Turbo | 10.5:1 | 2016-present | CX-9, Mazda3 Turbo |

### Skyactiv-X (SPCCI)
World's first production spark-controlled compression ignition engine.

| Engine | Displacement | Compression | Years |
|--------|-------------|-------------|-------|
| HF-VPH | 2.0L | 16.3:1 | 2019-present |

### Skyactiv-D (Diesel)
Ultra-low compression diesels - no DEF required.

| Engine | Displacement | Compression | Years |
|--------|-------------|-------------|-------|
| SH-VPTS | 2.2L | 14.0:1 | 2012-present |

## Directory Structure

```
Mazda/
├── MAZDA-Rotary-12A/           # 1970-1985 RX-3/RX-7 FB
├── MAZDA-Rotary-13B-NA/        # 1973-2002 NA 13B
├── MAZDA-Rotary-13B-REW-Turbo/ # 1992-2002 FD RX-7 Twin Turbo
├── MAZDA-Rotary-Renesis-13B-MSP/ # 2003-2012 RX-8
├── MAZDA-B6-1.6L-I4/           # 1989-1993 Miata 1.6
├── MAZDA-BP-1.8L-I4/           # 1994-2005 Miata 1.8
├── MAZDA-FE-2.0L-I4/           # 1983-2002 626/MX-6
├── MAZDA-MZR-2.0L-I4/          # 2001-2018 Mazda3/MX-5 NC
├── MAZDA-MZR-2.3L-I4-Turbo/    # 2005-2013 Mazdaspeed 3/6
├── MAZDA-Skyactiv-G-2.0L-I4/   # 2011-present
├── MAZDA-Skyactiv-G-2.5L-I4/   # 2012-present
├── MAZDA-Skyactiv-G-2.5L-I4-Turbo/ # 2016-present
├── MAZDA-Skyactiv-X-2.0L-I4/   # 2019-present SPCCI
├── MAZDA-Skyactiv-D-2.2L-Diesel/ # 2012-present
├── mazda-history-timeline.json  # Complete company history
└── mazda-engine-families.json   # Engine code reference
```

## Key Documentation Files

Each engine directory contains:
- `*-master.json` - Complete engine specifications and history
- `parts-catalog.json` - OEM and aftermarket parts database
- `aftermarket-ecosystem.json` - Tuning parts, vendors, build packages
- `interchangeability-matrix.json` - Cross-compatibility information
- `tools-and-service.json` - Service procedures and special tools

## Iconic Engines

### 13B-REW Twin-Turbo (1992-2002)
The pinnacle of Mazda's rotary development. Sequential twin-turbocharged 1.3L producing 280HP (JDM). Powers the legendary FD3S RX-7.

### BP 1.8L (1994-2005)
The heart of the Mazda Miata. Iron block, aluminum DOHC head, rev-happy character. Beloved by enthusiasts worldwide.

### L3-VDT DISI Turbo (2005-2013)
Mazda's return to turbocharged power with direct injection. 263HP from 2.3L. Powers Mazdaspeed 3 and Mazdaspeed 6.

### Skyactiv-X SPCCI (2019-present)
Revolutionary compression-ignition gasoline engine. 16.3:1 compression ratio - highest for any production gasoline engine.

## Mazda's Engineering Philosophy

### Rotary Commitment
Mazda is the only manufacturer to successfully mass-produce rotary engines for passenger vehicles. The technology continues in the MX-30 R-EV as a range extender.

### Skyactiv Technology
Mazda's holistic approach to efficiency includes:
- Ultra-high compression gasoline engines (13:1)
- Ultra-low compression diesels (14:1)
- Lightweight chassis and body construction
- Efficient transmissions

### Jinba Ittai
"Horse and rider as one" - Mazda's philosophy of driver engagement influences every aspect of vehicle development.

## Motorsport Heritage

- **1991 Le Mans 24 Hours**: 787B overall victory with R26B 4-rotor engine
- **IMSA GTO**: Multiple championships with RX-7
- **Global MX-5 Cup**: Largest single-make racing series in the world

## Resources

- [Mazda USA](https://www.mazdausa.com)
- [Racing Beat](https://www.racingbeat.com) - Rotary specialists since 1971
- [Flyin' Miata](https://www.flyinmiata.com) - Premier Miata performance
- [CorkSport](https://www.corksport.com) - Mazda performance parts
- [Atkins Rotary](https://www.atkinsrotary.com) - Rotary engine specialists

---
*This database is part of the Universal Parts Consciousness project.*
