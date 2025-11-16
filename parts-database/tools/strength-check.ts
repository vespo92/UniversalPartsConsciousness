#!/usr/bin/env bun
/**
 * Strength Calculator CLI Tool
 *
 * Quick command-line tool to check if a fastener will hold
 *
 * Usage:
 *   bun tools/strength-check.ts M3x0.5 A2-70 100
 *   bun tools/strength-check.ts M5x0.8 8.8 500 --engagement 10
 *   bun tools/strength-check.ts "1/4-20" 10.9 1000
 */

import { willItHold, calculateFastenerStrength, parseThreadDesignation, formatStrengthResults } from '../lib/strength-calculator'

// Parse command line arguments
const args = process.argv.slice(2)

if (args.length < 3 || args.includes('--help') || args.includes('-h')) {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║          FASTENER STRENGTH CALCULATOR                      ║
╚════════════════════════════════════════════════════════════╝

USAGE:
  bun tools/strength-check.ts <thread> <grade> <load> [options]

ARGUMENTS:
  thread    Thread designation (e.g., M3x0.5, M5x0.8, 1/4-20)
  grade     Material grade (A2-70, A4-70, 8.8, 10.9, 12.9)
  load      Required load in Newtons (N)

OPTIONS:
  --engagement <mm>    Thread engagement length (optional)
  --detailed           Show detailed calculations
  --help, -h           Show this help message

EXAMPLES:
  # Will M3x0.5 stainless hold 100N?
  bun tools/strength-check.ts M3x0.5 A2-70 100

  # Will M5x0.8 Grade 8.8 hold 500N with 10mm engagement?
  bun tools/strength-check.ts M5x0.8 8.8 500 --engagement 10

  # Imperial thread check
  bun tools/strength-check.ts "1/4-20" 10.9 1000 --detailed

MATERIAL GRADES:
  A2-70    304 Stainless Steel (700 MPa tensile)
  A4-70    316 Stainless Steel (700 MPa tensile)
  8.8      Medium Carbon Steel (800 MPa tensile)
  10.9     Alloy Steel (1040 MPa tensile)
  12.9     High Strength Steel (1220 MPa tensile)

CONVERSION:
  1 kg ≈ 10 N
  1 lb ≈ 4.4 N
`)
  process.exit(0)
}

const threadId = args[0]
const materialGrade = args[1]
const requiredLoad = parseFloat(args[2])

// Parse optional arguments
let engagementLength: number | undefined
let showDetailed = false

for (let i = 3; i < args.length; i++) {
  if (args[i] === '--engagement' && args[i + 1]) {
    engagementLength = parseFloat(args[i + 1])
    i++
  } else if (args[i] === '--detailed') {
    showDetailed = true
  }
}

// Validate inputs
if (!threadId || !materialGrade || isNaN(requiredLoad)) {
  console.error('❌ Invalid arguments. Use --help for usage information.')
  process.exit(1)
}

console.log('\n╔════════════════════════════════════════════════════════════╗')
console.log('║          FASTENER STRENGTH ANALYSIS                       ║')
console.log('╚════════════════════════════════════════════════════════════╝\n')

console.log(`Thread:          ${threadId}`)
console.log(`Material:        ${materialGrade}`)
console.log(`Required Load:   ${requiredLoad} N (${(requiredLoad / 9.81).toFixed(1)} kg)`)
if (engagementLength) {
  console.log(`Engagement:      ${engagementLength} mm`)
}
console.log('')

// Perform quick check
const result = willItHold(threadId, materialGrade, requiredLoad, engagementLength)

// Display results
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

if (result.safe) {
  console.log('✅ \x1b[32mSAFE TO USE\x1b[0m\n')
} else {
  console.log('❌ \x1b[31mUNSAFE - DO NOT USE\x1b[0m\n')
}

console.log(`Safety Margin:     ${result.margin > 0 ? '+' : ''}${result.margin.toFixed(1)}%`)
console.log(`Limiting Factor:   ${result.limitingFactor}`)
console.log(`\nRecommendation:    ${result.recommendation}`)

// Show detailed calculations if requested
if (showDetailed) {
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.log('DETAILED CALCULATIONS')
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

  const thread = parseThreadDesignation(threadId)
  if (thread) {
    const detailed = calculateFastenerStrength(
      thread,
      { grade: materialGrade },
      { engagementLength }
    )
    console.log(formatStrengthResults(detailed))
  }
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

// Exit with appropriate code
process.exit(result.safe ? 0 : 1)
