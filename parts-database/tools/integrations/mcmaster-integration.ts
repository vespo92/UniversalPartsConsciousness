#!/usr/bin/env bun
/**
 * McMaster-Carr Integration
 *
 * Scrapes product data from McMaster-Carr including:
 * - Product specifications
 * - CAD model URLs
 * - Pricing information
 * - Technical drawings
 *
 * Usage:
 *   bun tools/integrations/mcmaster-integration.ts <part-number>
 *   bun tools/integrations/mcmaster-integration.ts 91292A115
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase credentials')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

interface McMasterPart {
  part_number: string
  description: string
  product_name: string
  specifications: Record<string, string>
  cad_formats: {
    step?: string
    stl?: string
    dwg?: string
    pdf?: string
  }
  dimensions: {
    length?: number
    diameter?: number
    thread_size?: string
    drive_size?: string
    head_diameter?: number
    head_height?: number
  }
  material: string
  price?: number
  availability: string
}

/**
 * Fetch McMaster-Carr product page
 */
async function fetchMcMasterProduct(partNumber: string): Promise<McMasterPart | null> {
  const url = `https://www.mcmaster.com/${partNumber}`

  console.log(`🌐 Fetching McMaster-Carr product ${partNumber}...`)

  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; UniversalPartsDatabase/1.0)',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const html = await response.text()

    // Parse McMaster-Carr's page structure
    // Note: This is a template - actual implementation needs HTML parsing
    const part: McMasterPart = {
      part_number: partNumber,
      description: extractDescription(html),
      product_name: extractProductName(html),
      specifications: extractSpecifications(html),
      cad_formats: extractCADLinks(html),
      dimensions: extractDimensions(html),
      material: extractMaterial(html),
      availability: 'In Stock', // Would need to parse actual availability
    }

    return part
  } catch (error: any) {
    console.error('❌ Failed to fetch:', error.message)
    return null
  }
}

/**
 * Extract product description from HTML
 */
function extractDescription(html: string): string {
  // McMaster uses specific meta tags for descriptions
  const match = html.match(/<meta name="description" content="([^"]+)"/)
  return match ? match[1] : ''
}

/**
 * Extract product name/title
 */
function extractProductName(html: string): string {
  const match = html.match(/<h1[^>]*>([^<]+)<\/h1>/)
  return match ? match[1].trim() : ''
}

/**
 * Extract specifications table from McMaster page
 */
function extractSpecifications(html: string): Record<string, string> {
  const specs: Record<string, string> = {}

  // McMaster has specification tables
  // This would need proper HTML parsing with cheerio or similar
  const tableMatch = html.match(/<table[^>]*class="[^"]*SpecTbl[^"]*"[^>]*>([\s\S]*?)<\/table>/)

  if (tableMatch) {
    const rows = tableMatch[1].match(/<tr[^>]*>([\s\S]*?)<\/tr>/g) || []

    rows.forEach(row => {
      const cells = row.match(/<td[^>]*>([\s\S]*?)<\/td>/g) || []
      if (cells.length >= 2) {
        const key = cells[0].replace(/<[^>]+>/g, '').trim()
        const value = cells[1].replace(/<[^>]+>/g, '').trim()
        specs[key] = value
      }
    })
  }

  return specs
}

/**
 * Extract CAD model download links
 */
function extractCADLinks(html: string): McMasterPart['cad_formats'] {
  const formats: McMasterPart['cad_formats'] = {}

  // McMaster provides multiple CAD formats
  const stepMatch = html.match(/href="([^"]+\.step)"/)
  const stlMatch = html.match(/href="([^"]+\.stl)"/)
  const dwgMatch = html.match(/href="([^"]+\.dwg)"/)
  const pdfMatch = html.match(/href="([^"]+\.pdf)"/)

  if (stepMatch) formats.step = `https://www.mcmaster.com${stepMatch[1]}`
  if (stlMatch) formats.stl = `https://www.mcmaster.com${stlMatch[1]}`
  if (dwgMatch) formats.dwg = `https://www.mcmaster.com${dwgMatch[1]}`
  if (pdfMatch) formats.pdf = `https://www.mcmaster.com${pdfMatch[1]}`

  return formats
}

/**
 * Extract dimensions from specifications
 */
function extractDimensions(html: string): McMasterPart['dimensions'] {
  const specs = extractSpecifications(html)
  const dimensions: McMasterPart['dimensions'] = {}

  // Common dimension fields in McMaster specs
  const lengthKeys = ['Length', 'Overall Length', 'Lg.', 'L']
  const diameterKeys = ['Diameter', 'Thread Diameter', 'Dia.', 'D']
  const threadKeys = ['Thread Size', 'Thread', 'Thd. Size']
  const driveKeys = ['Drive Size', 'Socket Size', 'Hex Size']

  // Extract length
  for (const key of lengthKeys) {
    if (specs[key]) {
      const match = specs[key].match(/(\d+\.?\d*)\s*(?:mm|in)/)
      if (match) dimensions.length = parseFloat(match[1])
      break
    }
  }

  // Extract diameter
  for (const key of diameterKeys) {
    if (specs[key]) {
      const match = specs[key].match(/(\d+\.?\d*)\s*(?:mm|in)/)
      if (match) dimensions.diameter = parseFloat(match[1])
      break
    }
  }

  // Extract thread size
  for (const key of threadKeys) {
    if (specs[key]) {
      dimensions.thread_size = specs[key]
      break
    }
  }

  // Extract drive size
  for (const key of driveKeys) {
    if (specs[key]) {
      dimensions.drive_size = specs[key]
      break
    }
  }

  return dimensions
}

/**
 * Extract material information
 */
function extractMaterial(html: string): string {
  const specs = extractSpecifications(html)
  return specs['Material'] || specs['Matl.'] || 'Unknown'
}

/**
 * Download and parse CAD file for precise dimensions
 */
async function downloadAndParseCAD(part: McMasterPart): Promise<void> {
  if (!part.cad_formats.step) {
    console.log('⚠️  No STEP file available')
    return
  }

  console.log(`📥 Downloading CAD file: ${part.cad_formats.step}`)

  try {
    const response = await fetch(part.cad_formats.step)
    const stepData = await response.text()

    // Parse STEP file for dimensions
    // This would use a proper STEP parser
    console.log('📏 Parsing CAD file for precise dimensions...')

    // Extract bounding box, thread pitch, etc. from CAD
    // See cad-parser.ts for implementation

  } catch (error: any) {
    console.error('❌ CAD download failed:', error.message)
  }
}

/**
 * Import part into database
 */
async function importPart(part: McMasterPart): Promise<void> {
  console.log(`📦 Importing ${part.part_number} to database...`)

  const dbPart = {
    part_id: `McMaster-${part.part_number}`,
    manufacturer: 'McMaster-Carr',
    part_number: part.part_number,
    category: categorizePart(part),
    thread_id: part.dimensions.thread_size || null,
    length: part.dimensions.length || null,
    material_grade: part.material,
    data_source: 'mcmaster_scraper',
    verification_status: 'unverified',
    full_specs: {
      description: part.description,
      product_name: part.product_name,
      specifications: part.specifications,
      cad_formats: part.cad_formats,
      dimensions: part.dimensions,
      scraped_at: new Date().toISOString(),
    },
  }

  const { data, error } = await supabase
    .from('parts')
    .upsert([dbPart], { onConflict: 'part_id' })
    .select()

  if (error) {
    console.error('❌ Import failed:', error.message)
    return
  }

  console.log(`✅ Successfully imported ${part.part_number}!`)

  // Also store CAD links separately if needed
  if (Object.keys(part.cad_formats).length > 0) {
    await supabase
      .from('part_cad_files')
      .upsert([{
        part_id: dbPart.part_id,
        step_url: part.cad_formats.step,
        stl_url: part.cad_formats.stl,
        dwg_url: part.cad_formats.dwg,
        pdf_url: part.cad_formats.pdf,
      }], { onConflict: 'part_id' })
  }
}

/**
 * Categorize part based on description
 */
function categorizePart(part: McMasterPart): string {
  const desc = part.description.toLowerCase()
  const name = part.product_name.toLowerCase()
  const combined = `${desc} ${name}`

  if (combined.includes('screw') || combined.includes('bolt')) return 'fastener'
  if (combined.includes('nut')) return 'fastener'
  if (combined.includes('washer')) return 'fastener'
  if (combined.includes('bearing')) return 'bearing'
  if (combined.includes('seal') || combined.includes('o-ring')) return 'seal'
  if (combined.includes('spring')) return 'spring'

  return 'hardware'
}

/**
 * Batch import from McMaster catalog page
 */
async function importCatalogPage(catalogUrl: string): Promise<void> {
  console.log(`📚 Importing catalog page: ${catalogUrl}`)

  const response = await fetch(catalogUrl)
  const html = await response.text()

  // Extract all part numbers from catalog page
  const partNumbers = html.match(/\d{4,5}[A-Z]\d{1,4}/g) || []
  const uniquePartNumbers = [...new Set(partNumbers)]

  console.log(`Found ${uniquePartNumbers.length} unique part numbers`)

  // Process in batches with delays to be respectful
  for (let i = 0; i < uniquePartNumbers.length; i++) {
    const partNumber = uniquePartNumbers[i]
    console.log(`\nProcessing ${i + 1}/${uniquePartNumbers.length}: ${partNumber}`)

    const part = await fetchMcMasterProduct(partNumber)
    if (part) {
      await importPart(part)
    }

    // Respectful delay (2 seconds between requests)
    if (i < uniquePartNumbers.length - 1) {
      console.log('⏳ Waiting 2 seconds...')
      await new Promise(resolve => setTimeout(resolve, 2000))
    }
  }

  console.log(`\n✅ Catalog import complete!`)
}

// Main
const input = process.argv[2]

if (!input) {
  console.error('Usage: bun tools/integrations/mcmaster-integration.ts <part-number-or-catalog-url>')
  console.error('Examples:')
  console.error('  Single part:  bun tools/integrations/mcmaster-integration.ts 91292A115')
  console.error('  Catalog page: bun tools/integrations/mcmaster-integration.ts https://www.mcmaster.com/screws/')
  console.error('')
  console.error('⚠️  IMPORTANT:')
  console.error('  - Respect robots.txt')
  console.error('  - Use rate limiting (2s delay between requests)')
  console.error('  - Consider contacting McMaster for official data access')
  process.exit(1)
}

console.log('🔧 McMaster-Carr Integration Tool')
console.log('⚠️  Note: Scraping should respect terms of service')
console.log('')

if (input.startsWith('http')) {
  // Catalog page import
  importCatalogPage(input)
    .catch(err => {
      console.error('❌ Unexpected error:', err)
      process.exit(1)
    })
} else {
  // Single part import
  fetchMcMasterProduct(input)
    .then(part => {
      if (part) {
        return importPart(part)
      }
    })
    .catch(err => {
      console.error('❌ Unexpected error:', err)
      process.exit(1)
    })
}
