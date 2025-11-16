#!/usr/bin/env bun
/**
 * McMaster-Carr Web Scraper
 *
 * Scrapes parts data from McMaster-Carr public pages
 *
 * Usage:
 *   bun tools/scrape-mcmaster.ts <category-url>
 *   bun tools/scrape-mcmaster.ts https://www.mcmaster.com/screws/
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase credentials')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

interface ScrapedPart {
  part_number: string
  description: string
  thread_size?: string
  length?: number
  material?: string
  specs: Record<string, any>
}

async function scrapeMcMaster(url: string): Promise<ScrapedPart[]> {
  console.log(`🌐 Fetching ${url}...`)

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

    // Parse HTML for parts data
    // NOTE: This is a simplified example. Real scraping would need:
    // 1. HTML parser (cheerio or similar)
    // 2. Proper CSS selectors for McMaster's structure
    // 3. Handling of pagination
    // 4. Rate limiting and politeness delays
    // 5. Respect for robots.txt

    const parts: ScrapedPart[] = []

    // Example pattern matching (would need actual parsing)
    const partPattern = /Part Number: (\d+)/g
    let match

    while ((match = partPattern.exec(html)) !== null) {
      parts.push({
        part_number: match[1],
        description: 'Scraped from McMaster-Carr',
        specs: {
          source_url: url,
          scraped_at: new Date().toISOString(),
        },
      })
    }

    return parts
  } catch (error: any) {
    console.error('❌ Scraping failed:', error.message)
    return []
  }
}

async function importScrapedParts(parts: ScrapedPart[]) {
  console.log(`📦 Importing ${parts.length} parts...`)

  const partsToInsert = parts.map(p => ({
    part_id: `McMaster-${p.part_number}`,
    manufacturer: 'McMaster-Carr',
    part_number: p.part_number,
    category: 'fastener', // Would need to be determined from context
    thread_id: p.thread_size || null,
    length: p.length || null,
    material_grade: p.material || null,
    data_source: 'web_scraper',
    verification_status: 'unverified',
    full_specs: {
      description: p.description,
      ...p.specs,
    },
  }))

  const { data, error } = await supabase
    .from('parts')
    .insert(partsToInsert)
    .select()

  if (error) {
    console.error('❌ Import failed:', error.message)
    return
  }

  console.log(`✅ Successfully imported ${data?.length || 0} parts!`)
}

// Main
const url = process.argv[2]

if (!url) {
  console.error('Usage: bun tools/scrape-mcmaster.ts <category-url>')
  console.error('Example: bun tools/scrape-mcmaster.ts https://www.mcmaster.com/screws/')
  console.error('')
  console.error('⚠️  IMPORTANT: Respect robots.txt and rate limits!')
  console.error('⚠️  Consider contacting McMaster for official data access.')
  process.exit(1)
}

console.log('🕷️  McMaster-Carr Web Scraper')
console.log('⚠️  Note: This is a demonstration. Production use requires:')
console.log('   - Respecting robots.txt')
console.log('   - Rate limiting (delays between requests)')
console.log('   - Proper error handling')
console.log('   - Legal compliance with terms of service')
console.log('')

scrapeMcMaster(url)
  .then(importScrapedParts)
  .catch(err => {
    console.error('❌ Unexpected error:', err)
    process.exit(1)
  })
