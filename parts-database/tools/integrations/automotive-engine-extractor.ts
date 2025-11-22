#!/usr/bin/env bun
/**
 * Automotive Engine Parts Extractor
 *
 * Extracts engine component specifications from automotive engine databases
 * Sources:
 * - OEM Service Manuals
 * - Aftermarket Parts Catalogs
 * - Community-verified specifications
 *
 * Initial Focus: AMC 4.0L I6 (1987-2006) - "The Indestructible Six"
 *
 * Usage:
 *   bun tools/integrations/automotive-engine-extractor.ts amc-4.0
 *   bun tools/integrations/automotive-engine-extractor.ts list-engines
 *   bun tools/integrations/automotive-engine-extractor.ts bom-amc-4.0
 *   bun tools/integrations/automotive-engine-extractor.ts interchangeability amc-4.0
 */

import { createClient } from '@supabase/supabase-js'
import * as fs from 'fs'
import * as path from 'path'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// Supabase is optional for local operations
const supabase = supabaseUrl && supabaseKey
  ? createClient(supabaseUrl, supabaseKey)
  : null

// Engine data directory
const ENGINE_DATA_DIR = path.join(__dirname, '../../../Automotive/Engines')

/**
 * Find master file with flexible naming (handles different naming conventions)
 */
function findMasterFile(engineDir: string, engineId: string): string | null {
  const possibleNames = [
    `${engineId.toLowerCase()}-master.json`,
    `${engineId.toLowerCase().replace(/-/g, '_')}-master.json`,
    // Handle BMW naming: BMW-N54-3.0L-I6 -> bmw-n54-master.json
    engineId.toLowerCase().split('-').slice(0, 2).join('-') + '-master.json',
    // Try finding any *-master.json file
  ]

  for (const name of possibleNames) {
    const fullPath = path.join(engineDir, name)
    if (fs.existsSync(fullPath)) {
      return fullPath
    }
  }

  // Fallback: find any -master.json file in directory
  try {
    const files = fs.readdirSync(engineDir)
    const masterFile = files.find(f => f.endsWith('-master.json'))
    if (masterFile) {
      return path.join(engineDir, masterFile)
    }
  } catch {
    // ignore
  }

  return null
}

/**
 * Load engine data from JSON files
 */
function loadEngineData(engineId: string): {
  master: any
  parts: any
  interchangeability: any
  tools: any
} | null {
  const engineDir = path.join(ENGINE_DATA_DIR, engineId)

  if (!fs.existsSync(engineDir)) {
    console.error(`Engine directory not found: ${engineDir}`)
    return null
  }

  const masterPath = findMasterFile(engineDir, engineId)
  const partsPath = path.join(engineDir, 'parts-catalog.json')
  const interchangePath = path.join(engineDir, 'interchangeability-matrix.json')
  const toolsPath = path.join(engineDir, 'tools-and-service.json')

  try {
    return {
      master: masterPath ? JSON.parse(fs.readFileSync(masterPath, 'utf-8')) : null,
      parts: fs.existsSync(partsPath) ? JSON.parse(fs.readFileSync(partsPath, 'utf-8')) : null,
      interchangeability: fs.existsSync(interchangePath) ? JSON.parse(fs.readFileSync(interchangePath, 'utf-8')) : null,
      tools: fs.existsSync(toolsPath) ? JSON.parse(fs.readFileSync(toolsPath, 'utf-8')) : null,
    }
  } catch (err) {
    console.error(`Error loading engine data:`, err)
    return null
  }
}

/**
 * List all available engines in the database
 */
function listEngines(): void {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║           AUTOMOTIVE ENGINE DATABASE                        ║
╚════════════════════════════════════════════════════════════╝
`)

  if (!fs.existsSync(ENGINE_DATA_DIR)) {
    console.log('No engine data directory found.')
    return
  }

  const engines = fs.readdirSync(ENGINE_DATA_DIR, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name)

  if (engines.length === 0) {
    console.log('No engines found in database.')
    return
  }

  console.log(`Available Engines:\n`)
  console.log(`${'─'.repeat(60)}`)

  for (const engineDir of engines) {
    const masterPath = findMasterFile(path.join(ENGINE_DATA_DIR, engineDir), engineDir)
    if (masterPath) {
      try {
        const master = JSON.parse(fs.readFileSync(masterPath, 'utf-8'))
        const displacement = master.base_specifications?.displacement?.liters ||
                            (master.base_specifications?.displacement?.cc ? (master.base_specifications.displacement.cc / 1000).toFixed(1) : 'N/A')
        const turbo = master.base_specifications?.forced_induction
        const turboStr = turbo && turbo !== 'Naturally Aspirated' ? ' (Turbo)' : ''
        console.log(`  ${engineDir}`)
        console.log(`    ├─ Name: ${master.common_names?.[0] || master.engine_id}`)
        console.log(`    ├─ Years: ${master.production_years}`)
        console.log(`    ├─ Displacement: ${displacement}L${turboStr}`)
        console.log(`    └─ Configuration: ${master.base_specifications?.configuration}`)
        console.log()
      } catch {
        console.log(`  ${engineDir} (metadata unavailable)`)
      }
    } else {
      console.log(`  ${engineDir} (no master file)`)
    }
  }

  console.log(`${'─'.repeat(60)}`)
  console.log(`\nTotal Engines: ${engines.length}\n`)
}

/**
 * Display Bill of Materials for an engine
 */
function displayBOM(engineId: string): void {
  const data = loadEngineData(engineId)
  if (!data || !data.parts) {
    console.error(`Could not load parts data for ${engineId}`)
    return
  }

  const { parts } = data

  console.log(`
╔════════════════════════════════════════════════════════════╗
║  BILL OF MATERIALS: ${parts.engine_id?.padEnd(37) || engineId.padEnd(37)}║
╚════════════════════════════════════════════════════════════╝
`)

  if (parts.target_vehicle) {
    console.log(`Target Vehicle: ${parts.target_vehicle.year} ${parts.target_vehicle.make} ${parts.target_vehicle.model}`)
    console.log(`Engine: ${parts.target_vehicle.engine}\n`)
  }

  // Process each system
  const systems = parts.systems || {}
  let totalParts = 0
  const partsByCategory: Record<string, number> = {}

  for (const [systemName, systemData] of Object.entries(systems)) {
    const system = systemData as any
    console.log(`\n${'═'.repeat(60)}`)
    console.log(`  ${systemName.toUpperCase().replace(/_/g, ' ')}`)
    console.log(`${'═'.repeat(60)}`)
    console.log(`  ${system.description || ''}`)
    console.log(`${'─'.repeat(60)}`)

    if (system.components) {
      for (const [compName, compData] of Object.entries(system.components)) {
        const comp = compData as any
        totalParts++

        // Track by category
        const category = comp.wear_classification || 'unclassified'
        partsByCategory[category] = (partsByCategory[category] || 0) + 1

        // Get OEM part number
        let oemPart = comp.oem_part_numbers
        if (typeof oemPart === 'object' && !Array.isArray(oemPart)) {
          oemPart = Object.values(oemPart)[0]
        } else if (Array.isArray(oemPart)) {
          oemPart = oemPart[0]
        }

        const partId = (comp.part_id || '').padEnd(25)
        const oemStr = (oemPart || 'N/A').toString().padEnd(15)
        const qty = comp.quantity_per_engine || 1

        console.log(`  ${partId} | OEM: ${oemStr} | Qty: ${qty}`)
        console.log(`    └─ ${comp.description}`)

        // Show aftermarket options if available
        if (comp.aftermarket_options) {
          const options = Object.entries(comp.aftermarket_options)
            .slice(0, 2)
            .map(([brand, pn]) => `${brand}: ${pn}`)
            .join(', ')
          if (options) {
            console.log(`       Alt: ${options}`)
          }
        }
      }
    }
  }

  // Summary
  console.log(`\n${'═'.repeat(60)}`)
  console.log(`  SUMMARY`)
  console.log(`${'═'.repeat(60)}`)
  console.log(`  Total Components: ${totalParts}`)
  console.log(`\n  By Classification:`)
  for (const [category, count] of Object.entries(partsByCategory).sort()) {
    console.log(`    ${category.padEnd(20)}: ${count}`)
  }
  console.log(`${'═'.repeat(60)}\n`)
}

/**
 * Display interchangeability information
 */
function displayInterchangeability(engineId: string): void {
  const data = loadEngineData(engineId)
  if (!data || !data.interchangeability) {
    console.error(`Could not load interchangeability data for ${engineId}`)
    return
  }

  const { interchangeability } = data

  console.log(`
╔════════════════════════════════════════════════════════════╗
║  PARTS INTERCHANGEABILITY: ${(interchangeability.engine_id || engineId).padEnd(30)}║
╚════════════════════════════════════════════════════════════╝
`)

  // Vehicle platforms
  if (interchangeability.vehicle_platforms) {
    console.log(`\n${'═'.repeat(60)}`)
    console.log(`  VEHICLE PLATFORMS`)
    console.log(`${'═'.repeat(60)}`)
    for (const [code, platform] of Object.entries(interchangeability.vehicle_platforms)) {
      const p = platform as any
      console.log(`  ${code.padEnd(6)} ${p.name.padEnd(30)} ${p.years}`)
    }
  }

  // Era classifications
  if (interchangeability.era_classifications) {
    console.log(`\n${'═'.repeat(60)}`)
    console.log(`  ERA CLASSIFICATIONS (Critical for Parts Interchange)`)
    console.log(`${'═'.repeat(60)}`)
    for (const [era, config] of Object.entries(interchangeability.era_classifications)) {
      const c = config as any
      console.log(`\n  ${era.toUpperCase().replace(/_/g, ' ')}`)
      console.log(`  ${'─'.repeat(50)}`)
      console.log(`    Years: ${c.years}`)
      console.log(`    Fuel: ${c.fuel_injection}`)
      console.log(`    Ignition: ${c.ignition}`)
      console.log(`    ECU: ${c.ecu}`)
      console.log(`    OBD: ${c.obd}`)
    }
  }

  // Universal parts
  const groups = interchangeability.interchangeability_groups || {}

  if (groups.universal_1987_2006) {
    console.log(`\n${'═'.repeat(60)}`)
    console.log(`  UNIVERSAL PARTS (1987-2006) - These parts swap across ALL years!`)
    console.log(`${'═'.repeat(60)}`)
    console.log(`  ${groups.universal_1987_2006.description}\n`)

    for (const part of groups.universal_1987_2006.parts || []) {
      console.log(`  ✓ ${part.part_id}`)
      if (part.notes) {
        console.log(`    └─ ${part.notes}`)
      }
    }
  }

  // Cylinder head groups (critical info)
  if (groups.cylinder_head_groups) {
    console.log(`\n${'═'.repeat(60)}`)
    console.log(`  CYLINDER HEAD INTERCHANGE (⚠️ CRITICAL INFO)`)
    console.log(`${'═'.repeat(60)}`)

    for (const [groupName, groupData] of Object.entries(groups.cylinder_head_groups.groups || {})) {
      const g = groupData as any
      console.log(`\n  ${groupName.replace(/_/g, ' ').toUpperCase()}`)
      console.log(`  ${'─'.repeat(50)}`)
      console.log(`    Years: ${g.years}`)
      console.log(`    Castings: ${Array.isArray(g.castings) ? g.castings.join(', ') : g.castings || 'N/A'}`)

      if (g.known_issues) {
        console.log(`    ⚠️  ISSUE: ${g.known_issues}`)
      }
      if (g.recommendation) {
        console.log(`    💡 ${g.recommendation}`)
      }
      if (g.compatibility_score) {
        const score = g.compatibility_score
        const bar = '█'.repeat(Math.floor(score / 10)) + '░'.repeat(10 - Math.floor(score / 10))
        console.log(`    Score: [${bar}] ${score}%`)
      }
    }
  }

  // Common swaps
  if (interchangeability.common_swaps_and_upgrades) {
    console.log(`\n${'═'.repeat(60)}`)
    console.log(`  POPULAR UPGRADES & SWAPS`)
    console.log(`${'═'.repeat(60)}`)

    for (const [swapName, swapData] of Object.entries(interchangeability.common_swaps_and_upgrades)) {
      const s = swapData as any
      console.log(`\n  ${s.name || swapName}`)
      console.log(`  ${'─'.repeat(50)}`)
      console.log(`    ${s.description}`)
      if (s.power_gain) {
        console.log(`    Power Gain: ${s.power_gain}`)
      }
      if (s.difficulty) {
        console.log(`    Difficulty: ${s.difficulty}`)
      }
    }
  }

  console.log(`\n${'═'.repeat(60)}\n`)
}

/**
 * Display tools and service information
 */
function displayToolsAndService(engineId: string): void {
  const data = loadEngineData(engineId)
  if (!data || !data.tools) {
    console.error(`Could not load tools data for ${engineId}`)
    return
  }

  const { tools } = data

  console.log(`
╔════════════════════════════════════════════════════════════╗
║  TOOLS & SERVICE: ${(tools.engine_id || engineId).padEnd(39)}║
╚════════════════════════════════════════════════════════════╝
`)

  // Essential tools
  console.log(`\n${'═'.repeat(60)}`)
  console.log(`  ESSENTIAL TOOL INVENTORY`)
  console.log(`${'═'.repeat(60)}`)

  const inventory = tools.tool_inventory || {}

  // Hand tools summary
  if (inventory.hand_tools) {
    console.log(`\n  HAND TOOLS:`)
    const handTools = inventory.hand_tools
    if (handTools.sockets) {
      console.log(`    Sockets (metric): ${handTools.sockets.metric_shallow?.sizes_mm?.join(', ')}mm`)
      console.log(`    Sockets (SAE): ${handTools.sockets.sae_shallow?.sizes_inches?.join(', ')}`)
    }
    if (handTools.spark_plug_socket) {
      console.log(`    Spark Plug Socket: ${handTools.sockets?.spark_plug_socket?.size}`)
    }
  }

  // Specialty tools
  if (inventory.specialty_tools?.engine_specific) {
    console.log(`\n  SPECIALTY TOOLS (Engine-Specific):`)
    for (const [toolName, toolData] of Object.entries(inventory.specialty_tools.engine_specific)) {
      const t = toolData as any
      const rental = t.rental_available ? ' (rental available)' : ''
      console.log(`    • ${toolName.replace(/_/g, ' ')}: ${t.description}${rental}`)
    }
  }

  // Measuring tools
  if (inventory.specialty_tools?.measuring_tools) {
    console.log(`\n  MEASURING TOOLS (For Rebuild):`)
    for (const [toolName, toolData] of Object.entries(inventory.specialty_tools.measuring_tools)) {
      const t = toolData as any
      console.log(`    • ${toolName.replace(/_/g, ' ')}: ${t.usage}`)
    }
  }

  // Service operations
  console.log(`\n${'═'.repeat(60)}`)
  console.log(`  SERVICE OPERATIONS`)
  console.log(`${'═'.repeat(60)}`)

  const operations = tools.service_operations || {}

  // Maintenance
  if (operations.maintenance) {
    console.log(`\n  MAINTENANCE:`)
    for (const [opName, opData] of Object.entries(operations.maintenance)) {
      const op = opData as any
      console.log(`\n    ${opName.replace(/_/g, ' ').toUpperCase()}`)
      console.log(`    ${'─'.repeat(40)}`)
      console.log(`      Difficulty: ${op.difficulty || 'N/A'}`)
      console.log(`      Time: ${op.time_minutes ? `${op.time_minutes} min` : op.time_hours ? `${op.time_hours} hrs` : 'N/A'}`)
      if (op.interval) {
        console.log(`      Interval: ${op.interval.miles ? `${op.interval.miles} miles` : ''} ${op.interval.months ? `/ ${op.interval.months} months` : ''}`)
      }
      if (op.tools_required) {
        console.log(`      Tools: ${op.tools_required.slice(0, 3).map((t: any) => t.tool).join(', ')}...`)
      }
    }
  }

  // Repairs
  if (operations.repairs) {
    console.log(`\n  REPAIRS:`)
    for (const [opName, opData] of Object.entries(operations.repairs)) {
      const op = opData as any
      console.log(`\n    ${opName.replace(/_/g, ' ').toUpperCase()}`)
      console.log(`      Difficulty: ${op.difficulty || 'N/A'}`)
      console.log(`      Time: ${op.time_hours ? `${op.time_hours} hrs` : op.time_minutes ? `${op.time_minutes} min` : 'N/A'}`)
      if (op.symptoms) {
        console.log(`      Symptoms: ${op.symptoms.slice(0, 2).join(', ')}`)
      }
    }
  }

  console.log(`\n${'═'.repeat(60)}\n`)
}

/**
 * Import engine parts to Supabase database
 */
async function importEngineToDatabase(engineId: string): Promise<void> {
  if (!supabase) {
    console.log(`\n⚠️  Supabase not configured. Running in local-only mode.`)
    console.log(`   Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY to enable database import.\n`)
    displayBOM(engineId)
    return
  }

  const data = loadEngineData(engineId)
  if (!data || !data.parts) {
    console.error(`Could not load parts data for ${engineId}`)
    return
  }

  console.log(`
╔════════════════════════════════════════════════════════════╗
║  IMPORTING: ${(data.parts.engine_id || engineId).padEnd(46)}║
╚════════════════════════════════════════════════════════════╝
`)

  let successCount = 0
  let skipCount = 0
  let errorCount = 0

  const systems = data.parts.systems || {}

  for (const [systemName, systemData] of Object.entries(systems)) {
    const system = systemData as any
    console.log(`\n📦 Processing ${systemName}...`)

    if (system.components) {
      for (const [compName, compData] of Object.entries(system.components)) {
        const comp = compData as any
        const partId = comp.part_id

        if (!partId) {
          console.log(`   ⏭️  Skipping ${compName} (no part_id)`)
          skipCount++
          continue
        }

        try {
          // Check if part exists
          const { data: existing } = await supabase
            .from('parts')
            .select('part_id')
            .eq('part_id', partId)
            .single()

          if (existing) {
            console.log(`   ⏭️  ${partId} already exists`)
            skipCount++
            continue
          }

          // Prepare OEM part numbers
          let primaryOem = ''
          if (comp.oem_part_numbers) {
            if (typeof comp.oem_part_numbers === 'string') {
              primaryOem = comp.oem_part_numbers
            } else if (Array.isArray(comp.oem_part_numbers)) {
              primaryOem = comp.oem_part_numbers[0]
            } else {
              primaryOem = Object.values(comp.oem_part_numbers)[0] as string
            }
          }

          // Insert part
          const { error } = await supabase.from('parts').insert({
            part_id: partId,
            part_number: primaryOem || partId,
            manufacturer: 'AMC/Chrysler',
            category: 'engine_component',
            subcategory: systemName,
            material_grade: comp.material || comp.specifications?.material || 'Various',
            full_specs: {
              engine_id: data.parts.engine_id,
              description: comp.description,
              system: systemName,
              component: compName,
              oem_part_numbers: comp.oem_part_numbers,
              aftermarket_options: comp.aftermarket_options,
              specifications: comp.specifications,
              interchangeability: comp.interchangeability,
              wear_classification: comp.wear_classification,
              quantity_per_engine: comp.quantity_per_engine || 1,
              source: 'AMC 4.0L I6 Engine Database',
              verified: true,
            },
            verification_status: 'verified',
          })

          if (error) {
            console.error(`   ❌ ${partId}: ${error.message}`)
            errorCount++
          } else {
            console.log(`   ✅ ${partId}`)
            successCount++
          }

          // Rate limiting
          await new Promise(resolve => setTimeout(resolve, 100))
        } catch (err) {
          console.error(`   ❌ Error processing ${partId}:`, err)
          errorCount++
        }
      }
    }
  }

  console.log(`\n${'═'.repeat(60)}`)
  console.log(`\n✨ Import Complete!`)
  console.log(`   ✅ Imported: ${successCount}`)
  console.log(`   ⏭️  Skipped:  ${skipCount}`)
  console.log(`   ❌ Errors:   ${errorCount}`)
  console.log(`\n${'═'.repeat(60)}\n`)
}

/**
 * Display help
 */
function showHelp(): void {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║          AUTOMOTIVE ENGINE EXTRACTOR                        ║
║          Universal Parts Consciousness                      ║
╚════════════════════════════════════════════════════════════╝

Extract, view, and import automotive engine component specifications.

USAGE:
  bun tools/integrations/automotive-engine-extractor.ts <command> [engine-id]

COMMANDS:
  list-engines                List all available engines
  bom-<engine-id>            Display Bill of Materials
  interchange-<engine-id>    Show interchangeability data
  tools-<engine-id>          Show tools and service info
  import-<engine-id>         Import to Supabase database
  <engine-id>                Full info + import (if Supabase configured)

AVAILABLE ENGINES:
  AMC-4.0L-I6               AMC/Jeep 4.0L Inline-6 (1987-2006)
                            "The Indestructible Six"

  BMW STRAIGHT-6 ENGINES:
  BMW-N54-3.0L-I6           BMW N54 Twin-Turbo (2006-2016)
                            "The Legend" - 335i, 535i, 135i
  BMW-N55-3.0L-I6           BMW N55 Single-Turbo (2009-2019)
                            TwinPower Turbo with Valvetronic
  BMW-B58-3.0L-I6           BMW B58 Turbo (2015-present)
                            Current gen - M340i, Supra
  BMW-M54-3.0L-I6           BMW M54 NA (2000-2006)
                            330i, 530i, X5 - bulletproof
  BMW-M52-2.8L-I6           BMW M52 NA (1994-2000)
                            328i, 528i, Z3 - classic
  BMW-S54-3.2L-I6           BMW S54 M3 Engine (2000-2006)
                            E46 M3 - legendary NA I6

EXAMPLES:
  # List all engines
  bun tools/integrations/automotive-engine-extractor.ts list-engines

  # View AMC 4.0L Bill of Materials
  bun tools/integrations/automotive-engine-extractor.ts bom-AMC-4.0L-I6

  # View interchangeability info
  bun tools/integrations/automotive-engine-extractor.ts interchange-AMC-4.0L-I6

  # View tools and service procedures
  bun tools/integrations/automotive-engine-extractor.ts tools-AMC-4.0L-I6

  # Import to database
  bun tools/integrations/automotive-engine-extractor.ts import-AMC-4.0L-I6

ENVIRONMENT:
  NEXT_PUBLIC_SUPABASE_URL       Supabase project URL
  NEXT_PUBLIC_SUPABASE_ANON_KEY  Supabase anon key

  Without these, the tool runs in local-only mode (no database import).
`)
}

// Main execution
const command = process.argv[2]

if (!command || command === '--help' || command === '-h') {
  showHelp()
  process.exit(0)
}

;(async () => {
  try {
    if (command === 'list-engines') {
      listEngines()
    } else if (command.startsWith('bom-')) {
      const engineId = command.replace('bom-', '')
      displayBOM(engineId)
    } else if (command.startsWith('interchange-')) {
      const engineId = command.replace('interchange-', '')
      displayInterchangeability(engineId)
    } else if (command.startsWith('tools-')) {
      const engineId = command.replace('tools-', '')
      displayToolsAndService(engineId)
    } else if (command.startsWith('import-')) {
      const engineId = command.replace('import-', '')
      await importEngineToDatabase(engineId)
    } else {
      // Assume it's an engine ID - show all info
      const engineId = command
      const data = loadEngineData(engineId)

      if (!data) {
        console.error(`Unknown command or engine: ${command}`)
        console.error(`Use 'list-engines' to see available engines or --help for usage.`)
        process.exit(1)
      }

      displayBOM(engineId)
      displayInterchangeability(engineId)
      displayToolsAndService(engineId)
      await importEngineToDatabase(engineId)
    }
  } catch (err) {
    console.error('Fatal error:', err)
    process.exit(1)
  }
})()
