#!/usr/bin/env bun
/**
 * CSV Import Tool for Universal Parts Database
 *
 * Usage:
 *   bun tools/import-csv.ts <csv-file>
 *
 * CSV Format:
 *   manufacturer,part_number,category,subcategory,thread_id,length,material_grade,tensile_strength,yield_strength,notes
 */

import { createClient } from '@supabase/supabase-js'
import { readFileSync } from 'fs'

// Get Supabase credentials from environment
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase credentials')
  console.error('Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

interface CSVRow {
  manufacturer: string
  part_number: string
  category: string
  subcategory?: string
  thread_id?: string
  length?: string
  material_grade?: string
  tensile_strength?: string
  yield_strength?: string
  notes?: string
}

function parseCSV(content: string): CSVRow[] {
  const lines = content.trim().split('\n')
  const headers = lines[0].split(',').map(h => h.trim())

  return lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim())
    const row: any = {}

    headers.forEach((header, i) => {
      if (values[i]) {
        row[header] = values[i]
      }
    })

    return row as CSVRow
  })
}

function rowToPart(row: CSVRow) {
  const part_id = `${row.manufacturer}-${row.part_number}`.replace(/\s/g, '-')

  return {
    part_id,
    manufacturer: row.manufacturer,
    part_number: row.part_number,
    category: row.category,
    subcategory: row.subcategory || null,
    thread_id: row.thread_id || null,
    length: row.length ? parseFloat(row.length) : null,
    material_grade: row.material_grade || null,
    tensile_strength: row.tensile_strength ? parseFloat(row.tensile_strength) : null,
    yield_strength: row.yield_strength ? parseFloat(row.yield_strength) : null,
    data_source: 'csv_import',
    verification_status: 'unverified',
    full_specs: {
      notes: row.notes || '',
      imported_at: new Date().toISOString(),
      import_source: 'csv'
    }
  }
}

async function importCSV(filename: string) {
  console.log(`📁 Reading ${filename}...`)

  const content = readFileSync(filename, 'utf-8')
  const rows = parseCSV(content)

  console.log(`📊 Found ${rows.length} parts to import`)

  const parts = rows.map(rowToPart)

  // Batch insert
  console.log('⬆️  Uploading to database...')

  const { data, error } = await supabase
    .from('parts')
    .insert(parts)
    .select()

  if (error) {
    console.error('❌ Import failed:', error.message)
    process.exit(1)
  }

  console.log(`✅ Successfully imported ${data?.length || 0} parts!`)

  // Show summary
  if (data && data.length > 0) {
    console.log('\n📦 Imported parts:')
    data.forEach(part => {
      console.log(`  - ${part.part_id} (${part.category})`)
    })
  }
}

// Main
const filename = process.argv[2]

if (!filename) {
  console.error('Usage: bun tools/import-csv.ts <csv-file>')
  console.error('Example: bun tools/import-csv.ts tools/csv-template.csv')
  process.exit(1)
}

importCSV(filename)
  .catch(err => {
    console.error('❌ Unexpected error:', err)
    process.exit(1)
  })
