# Building The Collective: Community Data Strategy

## Vision

Create the world's most comprehensive parts database through crowdsourced data from:
- Manufacturers and distributors
- Engineers and mechanics
- DIY enthusiasts
- Open source CAD libraries
- Field measurements and real-world usage

## Current State

### APIs in Use
✅ **Only Supabase** - our own PostgreSQL database (no external dependencies)
- No third-party API calls
- All data stored and queried locally
- Full control over data structure
- Privacy-focused (no data leaks to external services)

### Bun Compatibility
✅ **Fully Bun Compatible**
- All dependencies work with Bun runtime
- Faster dev server and builds
- Use `bun dev:bun` or `bun build:bun`
- No Node.js-specific dependencies

## Data Collection Strategy

### Phase 1: Manual Contributions (Current)
- ✅ Web form for adding parts
- ✅ Basic validation
- ✅ User contribution tracking

### Phase 2: Bulk Import Tools (Next)

#### CSV Import Tool
Create a bulk import interface:
```typescript
// tools/import-csv.ts
import { parse } from 'csv-parse'
import { supabase } from '@/lib/supabase'

// Import format:
// manufacturer, part_number, thread_id, length, material_grade, category, ...
// Validates and batch inserts into database
```

**Supported Sources:**
- McMaster-Carr catalog exports
- Grainger product lists
- Manufacturer spec sheets
- Your personal inventory spreadsheets

#### Web Scraping Tools
```typescript
// tools/scrape-manufacturer.ts
// Scrape public manufacturer catalogs
// Examples:
// - DIN/ISO standards tables
// - Hardware store websites
// - Open source CAD libraries
```

**Targets:**
- Standards organizations (ISO, DIN, ANSI)
- Major distributors
- 3D model repositories (GrabCAD, Thingiverse)

#### API Integrations
Connect to open data sources:
- **OpenParts API** (if exists)
- **Manufacturing standards databases**
- **CAD file metadata** (STEP, STL files often contain dimensions)

### Phase 3: Community Verification

#### Trust Levels
1. **Unverified**: Community submission (show warning)
2. **Community Verified**: 3+ users confirm measurements
3. **Measured**: Physical measurement with calipers/micrometers
4. **Manufacturer Verified**: Direct from spec sheet
5. **Standards Verified**: Matches ISO/DIN/ANSI official standards

#### Gamification
```typescript
// Track contributor reputation
interface Contributor {
  parts_added: number
  verifications_made: number
  accuracy_score: number  // Based on verification outcomes
  badges: string[]
  reputation_points: number
}
```

**Badges:**
- First Contribution
- Metric Master (50+ metric parts)
- Imperial Expert (50+ imperial parts)
- Verifier (100+ verifications)
- Standards Guru (added official standards)

### Phase 4: Data Quality

#### Automatic Validation
```typescript
// Validate thread engagement calculations
// Check material compatibility makes sense
// Flag outliers (M3 screw with 800mm length = suspicious)
// Cross-reference against known standards
```

#### Conflict Resolution
When multiple users submit different specs for same part:
1. Show all variants
2. Users vote on correct version
3. Higher reputation users have weighted votes
4. Eventually mark one as "canonical"

## Implementation Plan

### Immediate (Next Sprint)

1. **CSV Import Tool**
```typescript
// app/admin/import/page.tsx
// Upload CSV, preview data, validate, bulk insert
```

2. **Batch Operations API**
```typescript
// app/api/bulk-import/route.ts
// POST endpoint for programmatic imports
// Authentication required
// Rate limited
```

3. **Data Export**
```typescript
// app/api/export/route.ts
// Export entire database or filtered subset
// JSON, CSV, SQL formats
// Enable community backups and forks
```

### Short-term (1-2 months)

1. **User Accounts & Reputation**
- Supabase Auth integration
- Track contributions per user
- Reputation scoring system

2. **Verification Workflow**
- "Verify this part" button
- Measurement upload (photo of calipers)
- Community voting

3. **Manufacturer Import Scripts**
```bash
# scripts/import-mcmaster.ts
# scripts/import-din-standards.ts
# scripts/import-iso-standards.ts
```

### Medium-term (3-6 months)

1. **Public API**
```typescript
// app/api/v1/parts/[id]/route.ts
// RESTful API for programmatic access
// GraphQL endpoint for complex queries
// API keys for rate limiting
```

2. **CAD Integration**
- FreeCAD plugin
- Fusion 360 addon
- OpenSCAD library
- Query database from within CAD software

3. **Mobile App**
- Scan barcodes/part numbers
- Take photos for verification
- Field measurements on the go

## Data Sources to Target

### Free/Open
1. **ISO/DIN Standards** (public portions)
2. **Wikipedia machinery tables**
3. **Open source CAD libraries**
4. **McMaster-Carr** (public catalog)
5. **Grainger** (public catalog)
6. **Fastenal** (public catalog)
7. **Community spreadsheets** (Reddit, forums)

### Community Generated
1. **Field measurements** from repairs
2. **Reverse engineering** of discontinued parts
3. **3D scanned parts**
4. **Manufacturer spec sheet uploads**

### Partnerships (Future)
1. Hardware stores (data licensing)
2. Makerspaces (collaborative measurement events)
3. Universities (engineering student projects)
4. Standards organizations (official data feeds)

## Technical Architecture

### Data Pipeline
```
1. Source → Scraper/Importer
2. Scraper → Validator
3. Validator → Staging Table
4. Staging → Review Queue (if conflicts)
5. Review → Production Database
6. Production → Search Index
```

### Storage Strategy
- **PostgreSQL (Supabase)**: Primary relational data
- **S3/Supabase Storage**: Images, PDFs, CAD files
- **Algolia/MeiliSearch**: Fast full-text search (future)
- **Redis**: Caching for popular queries (future)

### Scalability
Current setup handles:
- ✅ Thousands of parts
- ✅ Hundreds of concurrent users
- ✅ Real-time search

Future needs:
- Millions of parts
- Thousands of concurrent users
- ML-powered compatibility suggestions
- Image recognition for part identification

## How You Can Help

### As a User
1. Add parts you use regularly
2. Verify others' submissions
3. Upload manufacturer spec sheets
4. Report errors/conflicts

### As a Developer
1. Build import scripts for specific manufacturers
2. Create CAD integrations
3. Improve search algorithms
4. Add ML part identification

### As an Organization
1. Share your parts inventory
2. Contribute official specifications
3. Fund development
4. Host community measurement events

## Next Steps

**Ready to implement:**
1. CSV import tool (2 hours)
2. Bulk API endpoint (1 hour)
3. Export functionality (1 hour)

**Want to build:**
1. Web scraper for McMaster-Carr
2. Image upload for parts
3. Measurement verification workflow

Tell me which direction to go and I'll build it out!
