#!/usr/bin/env bun
/**
 * Data Normalization and Merging Tool
 *
 * Normalizes part data from multiple suppliers into consistent format:
 * - Standardizes thread designations (M3x0.5, 3-0.5, etc. -> M3x0.5)
 * - Converts units (inches -> mm)
 * - Maps material grades (18-8 SS -> A2-70)
 * - Merges duplicate entries
 * - Resolves conflicts using confidence scoring
 *
 * Usage:
 *   bun tools/integrations/data-normalizer.ts normalize
 *   bun tools/integrations/data-normalizer.ts merge-duplicates
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing Supabase credentials')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseKey)

interface NormalizationResult {
  partId: string
  changes: Array<{
    field: string
    original: any
    normalized: any
    confidence: number
  }>
}

/**
 * Normalize thread designation to ISO format
 */
function normalizeThreadDesignation(thread: string): { value: string; confidence: number } {
  if (!thread) return { value: '', confidence: 0 }

  thread = thread.trim().toUpperCase()

  // Already in ISO format (M3x0.5)
  if (/^M\d+[Xx]\d+(\.\d+)?$/.test(thread)) {
    return { value: thread.replace('X', 'x'), confidence: 100 }
  }

  // M3 format (missing pitch)
  if (/^M\d+$/.test(thread)) {
    const size = parseInt(thread.substring(1))
    const pitch = getStandardPitch(size)
    return { value: `${thread}x${pitch}`, confidence: 90 }
  }

  // Hyphen format (M3-0.5 -> M3x0.5)
  if (/^M\d+-\d+(\.\d+)?$/.test(thread)) {
    return { value: thread.replace('-', 'x'), confidence: 95 }
  }

  // Fractional inch (1/4-20)
  if (/^\d+\/\d+-\d+$/.test(thread)) {
    return { value: thread, confidence: 100 } // Keep as-is for imperial
  }

  // Number format (#10-24)
  if (/^#?\d+-\d+$/.test(thread)) {
    return { value: thread.replace('#', ''), confidence: 95 }
  }

  return { value: thread, confidence: 50 } // Unknown format
}

/**
 * Get standard pitch for metric thread
 */
function getStandardPitch(diameter: number): number {
  const standardPitches: Record<number, number> = {
    1: 0.25,
    1.2: 0.25,
    1.4: 0.3,
    1.6: 0.35,
    2: 0.4,
    2.5: 0.45,
    3: 0.5,
    3.5: 0.6,
    4: 0.7,
    5: 0.8,
    6: 1.0,
    8: 1.25,
    10: 1.5,
    12: 1.75,
    16: 2.0,
    20: 2.5,
  }

  return standardPitches[diameter] || 0.5
}

/**
 * Convert length to millimeters
 */
function normalizeLength(length: number | string, unit?: string): { value: number; confidence: number } {
  if (typeof length === 'string') {
    const match = length.match(/([\d.]+)\s*(mm|in|inch|")?/)
    if (!match) return { value: 0, confidence: 0 }

    length = parseFloat(match[1])
    unit = match[2] || unit
  }

  // Already in mm or no unit specified (assume mm)
  if (!unit || unit === 'mm') {
    return { value: length, confidence: unit ? 100 : 80 }
  }

  // Convert inches to mm
  if (unit === 'in' || unit === 'inch' || unit === '"') {
    return { value: length * 25.4, confidence: 100 }
  }

  return { value: length, confidence: 50 }
}

/**
 * Map material grades to standard designations
 */
function normalizeMaterial(material: string): { value: string; confidence: number } {
  if (!material) return { value: '', confidence: 0 }

  material = material.trim().toUpperCase()

  const materialMap: Record<string, string> = {
    // Stainless steel
    '18-8': 'A2-70',
    '18-8 SS': 'A2-70',
    '18-8 STAINLESS': 'A2-70',
    '304': 'A2-70',
    '304 SS': 'A2-70',
    '316': 'A4-70',
    '316L': 'A4-70',
    '316 SS': 'A4-70',

    // Steel grades
    'GRADE 5': '8.8',
    'GR 5': '8.8',
    'SAE J429 GRADE 5': '8.8',
    'GRADE 8': '10.9',
    'GR 8': '10.9',
    'SAE J429 GRADE 8': '10.9',

    // ISO grades (already standard)
    'A2-70': 'A2-70',
    'A4-70': 'A4-70',
    '8.8': '8.8',
    '10.9': '10.9',
    '12.9': '12.9',
  }

  // Direct match
  if (materialMap[material]) {
    return { value: materialMap[material], confidence: 100 }
  }

  // Partial match
  for (const [key, value] of Object.entries(materialMap)) {
    if (material.includes(key)) {
      return { value, confidence: 85 }
    }
  }

  return { value: material, confidence: 50 }
}

/**
 * Normalize a single part
 */
async function normalizePart(part: any): Promise<NormalizationResult> {
  const changes: NormalizationResult['changes'] = []

  // Normalize thread_id
  if (part.thread_id) {
    const normalized = normalizeThreadDesignation(part.thread_id)
    if (normalized.value !== part.thread_id) {
      changes.push({
        field: 'thread_id',
        original: part.thread_id,
        normalized: normalized.value,
        confidence: normalized.confidence,
      })
    }
  }

  // Normalize length
  if (part.length) {
    const normalized = normalizeLength(part.length)
    if (Math.abs(normalized.value - part.length) > 0.01) {
      changes.push({
        field: 'length',
        original: part.length,
        normalized: normalized.value,
        confidence: normalized.confidence,
      })
    }
  }

  // Normalize material
  if (part.material_grade) {
    const normalized = normalizeMaterial(part.material_grade)
    if (normalized.value !== part.material_grade) {
      changes.push({
        field: 'material_grade',
        original: part.material_grade,
        normalized: normalized.value,
        confidence: normalized.confidence,
      })
    }
  }

  return {
    partId: part.part_id,
    changes,
  }
}

/**
 * Apply normalization to database
 */
async function applyNormalization(result: NormalizationResult): Promise<void> {
  if (result.changes.length === 0) return

  const updates: any = {}

  result.changes.forEach(change => {
    updates[change.field] = change.normalized

    // Log the normalization
    supabase.from('data_normalization_log').insert({
      part_id: result.partId,
      action_type: `${change.field}_normalized`,
      original_value: String(change.original),
      normalized_value: String(change.normalized),
      confidence: change.confidence,
      data_source: 'auto',
      processed_by: 'data-normalizer',
    })
  })

  await supabase
    .from('parts')
    .update(updates)
    .eq('part_id', result.partId)
}

/**
 * Find and merge duplicate parts
 */
async function findDuplicates(): Promise<Array<{ primary: any; duplicates: any[] }>> {
  console.log('🔍 Finding duplicates...')

  const { data: allParts } = await supabase
    .from('parts')
    .select('*')
    .order('created_at', { ascending: true })

  if (!allParts) return []

  const groups = new Map<string, any[]>()

  // Group by normalized key (manufacturer + part_number + thread + length)
  allParts.forEach(part => {
    const key = [
      part.manufacturer?.toLowerCase(),
      part.part_number?.toLowerCase(),
      normalizeThreadDesignation(part.thread_id || '').value,
      Math.round((part.length || 0) * 10) / 10, // Round to 0.1mm
    ].join('|')

    const existing = groups.get(key) || []
    existing.push(part)
    groups.set(key, existing)
  })

  // Find groups with more than one part
  const duplicateGroups: Array<{ primary: any; duplicates: any[] }> = []

  groups.forEach(parts => {
    if (parts.length > 1) {
      duplicateGroups.push({
        primary: parts[0], // Keep oldest
        duplicates: parts.slice(1),
      })
    }
  })

  return duplicateGroups
}

/**
 * Merge duplicate parts
 */
async function mergeDuplicates(group: { primary: any; duplicates: any[] }): Promise<void> {
  console.log(`  Merging ${group.duplicates.length} duplicates into ${group.primary.part_id}`)

  // Merge full_specs from duplicates
  const mergedSpecs = { ...group.primary.full_specs }

  group.duplicates.forEach(dup => {
    Object.assign(mergedSpecs, dup.full_specs)
  })

  // Update primary with merged data
  await supabase
    .from('parts')
    .update({ full_specs: mergedSpecs })
    .eq('part_id', group.primary.part_id)

  // Create cross-references to duplicates before deleting
  for (const dup of group.duplicates) {
    await supabase
      .from('part_cross_references')
      .upsert({
        primary_part_id: group.primary.part_id,
        equivalent_part_id: dup.part_id,
        match_quality: 100,
        match_type: 'exact',
        notes: 'Merged duplicate entry',
      })
  }

  // Delete duplicates
  const duplicateIds = group.duplicates.map(d => d.part_id)
  await supabase
    .from('parts')
    .delete()
    .in('part_id', duplicateIds)
}

/**
 * Main normalization command
 */
async function normalizeCommand(): Promise<void> {
  console.log('🔧 Data Normalization Tool')
  console.log('─'.repeat(60))

  const { data: parts } = await supabase
    .from('parts')
    .select('*')
    .limit(1000)

  if (!parts || parts.length === 0) {
    console.log('No parts to normalize')
    return
  }

  console.log(`\nNormalizing ${parts.length} parts...`)

  let normalizedCount = 0

  for (const part of parts) {
    const result = await normalizePart(part)

    if (result.changes.length > 0) {
      console.log(`\n${part.part_id}:`)
      result.changes.forEach(change => {
        console.log(`  ${change.field}: ${change.original} -> ${change.normalized} (${change.confidence}% confidence)`)
      })

      await applyNormalization(result)
      normalizedCount++
    }
  }

  console.log(`\n✅ Normalized ${normalizedCount} parts`)
}

/**
 * Main merge duplicates command
 */
async function mergeDuplicatesCommand(): Promise<void> {
  console.log('🔧 Duplicate Merger Tool')
  console.log('─'.repeat(60))

  const duplicateGroups = await findDuplicates()

  if (duplicateGroups.length === 0) {
    console.log('No duplicates found')
    return
  }

  console.log(`\nFound ${duplicateGroups.length} duplicate groups`)

  for (const group of duplicateGroups) {
    await mergeDuplicates(group)
  }

  console.log(`\n✅ Merged ${duplicateGroups.length} duplicate groups`)
}

// Main
const command = process.argv[2]

if (!command) {
  console.error('Usage:')
  console.error('  bun tools/integrations/data-normalizer.ts normalize')
  console.error('  bun tools/integrations/data-normalizer.ts merge-duplicates')
  process.exit(1)
}

console.log('🔧 Data Normalization and Merging Tool')

if (command === 'normalize') {
  normalizeCommand()
    .catch(err => {
      console.error('❌ Unexpected error:', err)
      process.exit(1)
    })
} else if (command === 'merge-duplicates') {
  mergeDuplicatesCommand()
    .catch(err => {
      console.error('❌ Unexpected error:', err)
      process.exit(1)
    })
} else {
  console.error(`❌ Unknown command: ${command}`)
  process.exit(1)
}
