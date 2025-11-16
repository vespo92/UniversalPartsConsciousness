# Multi-Supplier Integration Guide

Complete guide to integrating McMaster-Carr, Grainger, Fastenal, and other suppliers with CAD model support.

## Overview

The integration system provides:

1. **Multi-Supplier Scraping** - Pull data from major distributors
2. **CAD File Parsing** - Extract dimensions from STEP/STL files
3. **Cross-Reference System** - Link equivalent parts across suppliers
4. **Data Normalization** - Standardize inconsistent data
5. **Duplicate Merging** - Combine redundant entries

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                             │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ McMaster-Carr│   Grainger   │  Fastenal    │  MSC/Others   │
│  + CAD Files │              │              │               │
└──────┬───────┴──────┬───────┴──────┬───────┴───────┬───────┘
       │              │              │               │
       ▼              ▼              ▼               ▼
┌────────────────────────────────────────────────────────────┐
│            Integration Layer                                │
│  • HTML Scraping                                           │
│  • CAD Parsing (STEP/STL)                                  │
│  • Specification Extraction                                │
└───────────────────────────┬────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│            Normalization Layer                              │
│  • Thread standardization (M3x0.5)                        │
│  • Unit conversion (inches -> mm)                         │
│  • Material mapping (18-8 SS -> A2-70)                    │
└───────────────────────────┬────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│            Cross-Reference System                           │
│  • Specification matching                                  │
│  • Dimensional comparison                                  │
│  • Supplier equivalence                                    │
└───────────────────────────┬────────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────────┐
│            Universal Parts Database                         │
│  • Deduplicated parts                                      │
│  • Cross-references                                        │
│  • CAD dimensions                                          │
└────────────────────────────────────────────────────────────┘
```

---

## Setup

### 1. Install Additional Dependencies

```bash
cd parts-database
npm install three @types/three step-parser
```

### 2. Run Integration Schema

```sql
-- In Supabase SQL Editor
-- Run: supabase/schema-integrations.sql
```

This creates:
- `part_cad_files` - CAD file storage
- `part_cross_references` - Supplier equivalents
- `supplier_catalogs` - Import tracking
- `material_standards` - Material equivalents
- `thread_standards_extended` - Thread compatibility

### 3. Make Tools Executable

```bash
chmod +x tools/integrations/*.ts
```

---

## Usage Guide

### A. McMaster-Carr Integration

McMaster-Carr provides detailed specs and CAD files for every part.

**Single Part Import:**
```bash
bun tools/integrations/mcmaster-integration.ts 91292A115
```

**Catalog Import:**
```bash
bun tools/integrations/mcmaster-integration.ts https://www.mcmaster.com/screws/socket-head-cap-screws/
```

**What It Does:**
- Scrapes product page HTML
- Extracts specifications table
- Downloads CAD file URLs (STEP, STL, DWG, PDF)
- Stores in database
- Creates cross-references

**Example Output:**
```
🔧 McMaster-Carr Integration Tool
🌐 Fetching McMaster-Carr product 91292A115...
📦 Importing 91292A115 to database...
✅ Successfully imported 91292A115!
```

---

### B. CAD File Parsing

Extract precise dimensions from STEP or STL files.

**Parse Local File:**
```bash
bun tools/integrations/cad-parser.ts screw.step
```

**What It Extracts:**
- Bounding box dimensions
- Cylindrical features (diameter, height)
- Thread features (major/minor diameter, pitch)
- Holes (diameter, position)
- Volume and surface area

**Example Output:**
```
📐 Parsing STEP file: screw.step

📊 Extracted Dimensions:
──────────────────────────────────────────────────
🔲 Bounding Box:
  Length: 12.00 mm
  Width:  3.00 mm
  Height: 3.00 mm

🔵 Cylindrical Features:
  Diameter: 3.00 mm
  Height:   12.00 mm

🔩 Thread Features:
  Major Diameter: 3.00 mm
  Minor Diameter: 2.46 mm
  Pitch:          0.50 mm

📦 Volume:       84.82 mm³
📏 Surface Area: 141.37 mm²
```

---

### C. Multi-Supplier Search

Search across all suppliers and find cross-references.

**Search All Suppliers:**
```bash
bun tools/integrations/multi-supplier.ts search "M3x12 socket head cap screw stainless"
```

**Find Cross-References:**
```bash
bun tools/integrations/multi-supplier.ts crossref McMaster-91292A115
```

**What It Does:**
- Searches Grainger, Fastenal, MSC simultaneously
- Extracts part numbers and specs
- Finds equivalent parts across suppliers
- Stores cross-references with match quality score

**Example Output:**
```
🌐 Searching across all suppliers...
Query: "M3x12 socket head cap screw stainless"
────────────────────────────────────────────────────────────

Grainger (5 results):
  12345678
    URL: https://www.grainger.com/product/12345678
  ...

Fastenal (3 results):
  987654321
    URL: https://www.fastenal.com/products/details/987654321
  ...

🔗 Found 2 potential cross-references
💾 Storing cross-references...
✅ Cross-references stored
```

---

### D. Data Normalization

Standardize inconsistent data from different suppliers.

**Normalize All Parts:**
```bash
bun tools/integrations/data-normalizer.ts normalize
```

**Merge Duplicates:**
```bash
bun tools/integrations/data-normalizer.ts merge-duplicates
```

**What It Normalizes:**

1. **Thread Designations:**
   - `M3-0.5` → `M3x0.5`
   - `M3` → `M3x0.5` (adds standard pitch)
   - `3-0.5` → `M3x0.5`

2. **Length Units:**
   - `0.5 inches` → `12.7 mm`
   - `1/2"` → `12.7 mm`

3. **Material Grades:**
   - `18-8 SS` → `A2-70`
   - `Grade 5` → `8.8`
   - `316L` → `A4-70`

**Example Output:**
```
🔧 Data Normalization Tool
────────────────────────────────────────────────────────────
Normalizing 150 parts...

McMaster-91292A115:
  thread_id: M3-0.5 -> M3x0.5 (95% confidence)
  material_grade: 18-8 SS -> A2-70 (100% confidence)

Grainger-12345678:
  length: 0.5 in -> 12.7 mm (100% confidence)

✅ Normalized 47 parts
```

---

## Workflow Examples

### Complete McMaster Import Workflow

```bash
# 1. Import parts from McMaster catalog
bun tools/integrations/mcmaster-integration.ts https://www.mcmaster.com/screws/socket-head-cap-screws/

# 2. Download and parse CAD files for precise dimensions
for file in downloads/*.step; do
  bun tools/integrations/cad-parser.ts "$file"
done

# 3. Normalize the imported data
bun tools/integrations/data-normalizer.ts normalize

# 4. Merge any duplicates
bun tools/integrations/data-normalizer.ts merge-duplicates
```

### Cross-Supplier Comparison Workflow

```bash
# 1. Search for a part across all suppliers
bun tools/integrations/multi-supplier.ts search "M5x20 hex socket cap screw 10.9"

# 2. Find cross-references for specific part
bun tools/integrations/multi-supplier.ts crossref McMaster-91292A207

# 3. Query database for equivalents
psql -c "SELECT * FROM find_equivalent_parts('McMaster-91292A207')"
```

---

## Database Schema

### Cross-Reference System

```sql
-- Find all equivalent parts for McMaster part
SELECT * FROM find_equivalent_parts('McMaster-91292A115');

-- Returns:
-- equivalent_id | supplier  | part_number | match_quality | notes
-- Grainger-123  | Grainger  | 12345678    | 95           | Match based on: M3X0.5_L12_A2-70_SOCKET
-- Fastenal-456  | Fastenal  | 987654321   | 92           | Match based on: M3X0.5_L12_A2-70_SOCKET
```

### CAD Dimensions

```sql
-- Get CAD file info for part
SELECT * FROM part_cad_files WHERE part_id = 'McMaster-91292A115';

-- Returns CAD download URLs and extracted dimensions
```

### Material Standards

```sql
-- Find equivalent materials
SELECT equivalent_materials FROM material_standards WHERE material_designation = 'A2-70';

-- Returns: ['304', '18-8 SS', 'X5CrNi18-10']
```

---

## API Integration

### REST API Cross-Reference Endpoint

```typescript
// GET /api/v1/cross-references/:partId
const response = await fetch('/api/v1/cross-references/McMaster-91292A115')
const { equivalents } = await response.json()

// Returns:
// {
//   "primary": "McMaster-91292A115",
//   "equivalents": [
//     {
//       "supplier": "Grainger",
//       "part_number": "12345678",
//       "match_quality": 95,
//       "price_difference": 0.15
//     }
//   ]
// }
```

---

## Best Practices

### 1. Respectful Scraping

```typescript
// Always use delays between requests
await new Promise(resolve => setTimeout(resolve, 2000)) // 2 second delay

// Check robots.txt
// Use appropriate User-Agent
// Consider contacting suppliers for official API access
```

### 2. Data Quality

```typescript
// Always log normalization changes
await supabase.from('data_normalization_log').insert({
  part_id: partId,
  action_type: 'thread_standardized',
  original_value: 'M3-0.5',
  normalized_value: 'M3x0.5',
  confidence: 95,
})

// Verify before auto-merging
// Keep audit trail
```

### 3. CAD File Management

```typescript
// Store CAD files in Supabase Storage
const { data } = await supabase.storage
  .from('cad-files')
  .upload(`${partId}/model.step`, stepFile)

// Parse asynchronously for large files
// Cache parsed dimensions
```

---

## Troubleshooting

### Issue: Scraping Fails

```bash
# Check if site structure changed
curl -I https://www.mcmaster.com/91292A115

# Check robots.txt
curl https://www.mcmaster.com/robots.txt

# Use manual import instead
bun tools/import-csv.ts manual-data.csv
```

### Issue: CAD Parsing Errors

```bash
# Verify file format
file screw.step

# Try different parser
# STEP files should start with "ISO-10303-21"
head screw.step

# Check file size
ls -lh screw.step
```

### Issue: Duplicates Not Merging

```sql
-- Check normalization log
SELECT * FROM data_normalization_log
WHERE part_id LIKE 'McMaster%'
ORDER BY created_at DESC;

-- Manually check potential duplicates
SELECT manufacturer, part_number, thread_id, length, COUNT(*)
FROM parts
GROUP BY manufacturer, part_number, thread_id, length
HAVING COUNT(*) > 1;
```

---

## Files Created

```
parts-database/
└── tools/
    └── integrations/
        ├── mcmaster-integration.ts      - McMaster scraper + CAD links
        ├── cad-parser.ts                - STEP/STL dimension extraction
        ├── multi-supplier.ts            - Multi-supplier search
        └── data-normalizer.ts           - Normalization + merging

supabase/
└── schema-integrations.sql              - Database schema
```

---

## Next Steps

**Immediate:**
1. Set up Supabase schema: `schema-integrations.sql`
2. Test McMaster import with one part
3. Parse sample CAD file
4. Run normalizer on test data

**Short-term:**
1. Build web UI for cross-reference browsing
2. Add API endpoint for CAD dimensions
3. Create automated import scheduler
4. Add more suppliers (Amazon, eBay, AliExpress)

**Long-term:**
1. Machine learning for better cross-matching
2. Image recognition for part identification
3. Price tracking and alerts
4. Integration with CAD software (FreeCAD, Fusion 360)

---

## Support

For issues:
1. Check `data_normalization_log` table for clues
2. Review supplier website structure (may have changed)
3. Test with sample files in `tools/test-data/`
4. Open GitHub issue with error logs

**This integration system makes UPC the most comprehensive parts database by leveraging CAD models and multi-supplier data!**
