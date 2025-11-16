# Quick Start: Building The Collective

## 🚀 Bun-Powered Development

**All dependencies are Bun compatible!**

```bash
# Install with Bun (faster)
bun install

# Run dev server with Bun
bun dev:bun

# Build with Bun
bun build:bun
```

Traditional npm/yarn also work fine.

## 📊 What APIs Are We Using?

**Answer: ONLY YOUR OWN DATABASE**

- ✅ Supabase (PostgreSQL) - your own instance
- ❌ No external API calls
- ❌ No third-party data dependencies
- ❌ No tracking or analytics

**This means:**
- Full data privacy
- No rate limits from external services
- Complete control over your data
- Works offline (after initial load)
- No vendor lock-in

## 🤝 Contributing Data (The Collective)

### Method 1: Web Interface (Easy)
1. Visit your deployed site
2. Click "Add Part"
3. Fill in the form
4. Submit!

### Method 2: CSV Bulk Import (Fast)
```bash
# 1. Create a CSV file (see tools/csv-template.csv)
# Format: manufacturer,part_number,category,thread_id,length,...

# 2. Import it
bun tools/import-csv.ts your-parts.csv

# 3. Done! Check your database
```

**Example CSV:**
```csv
manufacturer,part_number,category,thread_id,length,material_grade
DIN,912-M3x12,fastener,M3x0.5,12,A2-70
McMaster,91292A115,fastener,M3x0.5,10,18-8_SS
```

### Method 3: API (Programmatic)
```typescript
// Coming soon: REST API for batch imports
POST /api/v1/parts/batch
{
  "parts": [
    {
      "manufacturer": "DIN",
      "part_number": "912-M3x12",
      // ... more fields
    }
  ]
}
```

## 🎯 Data Collection Strategy

### What to Add

1. **Standard Parts** (High Priority)
   - ISO screws and bolts
   - DIN fasteners
   - ANSI hardware
   - Common metric threads

2. **Real-World Parts** (High Value)
   - Parts from your projects
   - Discontinued parts you've measured
   - Oddball hardware that's hard to find
   - Field modifications that actually work

3. **Specialized Parts** (Nice to Have)
   - Industry-specific hardware
   - Proprietary fasteners
   - Custom modified parts
   - Regional variations

### Where to Get Data

**Free Sources:**
1. McMaster-Carr catalog (public data)
2. Wikipedia engineering tables
3. Your personal parts bin
4. Manufacturer spec sheets (PDFs)
5. Old machinery you're taking apart
6. Hardware store visits with calipers

**Community Sources:**
1. Reddit r/MechanicalEngineering
2. Engineering forums
3. Makerspace inventories
4. University lab equipment lists

## 🔧 Tools Included

### CSV Import Script
```bash
bun tools/import-csv.ts tools/csv-template.csv
```
Bulk import parts from spreadsheets.

### Template CSV
```
tools/csv-template.csv
```
Example format with 5 sample parts.

### Coming Soon
- Web scraper for manufacturer catalogs
- Image upload for parts
- CAD file parser (STEP/STL dimensions)
- Barcode scanner integration

## 🎮 Gamification Ideas

### Contributor Levels
- **Bronze**: 10 parts added
- **Silver**: 50 parts added
- **Gold**: 200 parts added
- **Platinum**: 1000 parts added

### Badges
- 🔩 Metric Master (100 metric parts)
- 🇺🇸 Imperial Expert (100 imperial parts)
- ✅ Verifier (verified 50 parts)
- 📏 Precision (measured parts with calipers)
- 🏭 Standards Guru (added official specs)

### Reputation System
- +10 points: Add a new part
- +5 points: Verify someone's part
- +20 points: Add manufacturer spec sheet
- +50 points: Add complete product BOM

## 📈 Growth Strategy

### Phase 1: Seed Data (Now)
**Goal: 1,000 common parts**
- Top 100 metric screws/bolts
- Top 100 imperial screws/bolts
- Common bearings, seals, washers
- Standard hardware store items

### Phase 2: Community Growth (1-3 months)
**Goal: 10,000 parts, 100 active contributors**
- Launch public site
- Post on Reddit, HackerNews
- Partner with makerspaces
- Create import tools for manufacturers

### Phase 3: Critical Mass (3-6 months)
**Goal: 100,000 parts, 1,000 active contributors**
- API for CAD integrations
- Mobile app
- Manufacturer partnerships
- Academic partnerships

### Phase 4: The Standard (6-12 months)
**Goal: 1M+ parts, industry recognition**
- Default parts database for CAD software
- Referenced in repair manuals
- Used by hardware stores
- Industry standard

## 🚀 Quick Wins

**Can be built in < 4 hours:**
1. CSV import with drag-drop UI
2. Image upload for parts
3. Export database to JSON/CSV
4. Public API endpoints
5. Search by image (ML part identification)

**Want me to build any of these?**

## 🤝 How to Contribute

1. **Add Your Parts**
   - Use the web form or CSV import
   - Include as much detail as possible
   - Add notes about real-world usage

2. **Verify Others' Parts**
   - Check against your physical parts
   - Confirm dimensions with calipers
   - Report errors

3. **Code Contributions**
   - Build import scrapers
   - Improve search
   - Add features
   - Fix bugs

4. **Spread the Word**
   - Share on social media
   - Tell your engineering friends
   - Post in maker communities
   - Write blog posts

## 🎯 Next Steps

**Tell me what to build next:**

A. CSV drag-drop import UI
B. Public API for programmatic access
C. Web scraper for McMaster-Carr
D. Image upload and recognition
E. Mobile app for field measurements

Or suggest your own ideas!

---

**The goal:** Make finding compatible parts as easy as Googling a question.

**The method:** Community-driven, open database, zero external dependencies.

**The result:** Never lose a screw again.
