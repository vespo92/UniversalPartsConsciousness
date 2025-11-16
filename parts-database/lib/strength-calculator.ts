/**
 * Strength Calculator Library
 *
 * Provides engineering calculations for fasteners:
 * - Thread shear strength
 * - Tensile load capacity
 * - Torque specifications
 * - Clamping force
 * - Fatigue life estimates
 * - Engagement length requirements
 *
 * Based on:
 * - ISO 898-1 (Mechanical properties of fasteners)
 * - VDI 2230 (Systematic calculation of highly stressed bolted joints)
 * - Machinery's Handbook
 */

// Material properties database
const MATERIAL_PROPERTIES = {
  'A2-70': {
    tensileStrength: 700, // MPa
    yieldStrength: 450, // MPa
    shearStrength: 420, // 60% of tensile
    proofLoad: 450,
  },
  'A4-70': {
    tensileStrength: 700,
    yieldStrength: 450,
    shearStrength: 420,
    proofLoad: 450,
  },
  '8.8': {
    tensileStrength: 800,
    yieldStrength: 640,
    shearStrength: 480,
    proofLoad: 580,
  },
  '10.9': {
    tensileStrength: 1040,
    yieldStrength: 940,
    shearStrength: 624,
    proofLoad: 830,
  },
  '12.9': {
    tensileStrength: 1220,
    yieldStrength: 1100,
    shearStrength: 732,
    proofLoad: 970,
  },
}

interface ThreadData {
  majorDiameter: number // mm
  minorDiameter: number // mm
  pitch: number // mm
  threadDesignation: string
}

interface MaterialData {
  grade: string
  tensileStrength?: number // MPa (optional override)
  yieldStrength?: number // MPa (optional override)
  shearStrength?: number // MPa (optional override)
}

interface StrengthResults {
  // Tensile capacity
  tensileStressArea: number // mm²
  tensileLoadCapacity: number // N
  proofLoad: number // N

  // Shear capacity
  shearArea: number // mm²
  shearLoadCapacity: number // N

  // Thread stripping
  minEngagementLength: number // mm
  strippingStrengthBolt: number // N
  strippingStrengthNut: number // N

  // Torque
  recommendedTorque: number // Nm
  maxTorque: number // Nm

  // Clamping force
  clampingForce: number // N

  // Safety factors
  safetyFactor: number

  // Warnings
  warnings: string[]
}

interface TorqueCalculationOptions {
  frictionCoefficient?: number
  nutFactor?: number
  preloadPercentage?: number // % of proof load (typically 75%)
}

interface FatigueOptions {
  meanStress: number // MPa
  stressAmplitude: number // MPa
  reliability?: number // % (typically 99%)
}

/**
 * Calculate tensile stress area (As) per ISO 898-1
 * As = π/4 * ((d2 + d3)/2)²
 * where d2 = pitch diameter, d3 = minor diameter
 */
function calculateTensileStressArea(thread: ThreadData): number {
  const d3 = thread.minorDiameter
  const d2 = thread.majorDiameter - 0.649519 * thread.pitch // Pitch diameter approximation
  return (Math.PI / 4) * Math.pow((d2 + d3) / 2, 2)
}

/**
 * Calculate shear area for threads
 */
function calculateShearArea(thread: ThreadData): number {
  // Simplified: use 75% of gross cross-section
  return 0.75 * (Math.PI / 4) * Math.pow(thread.majorDiameter, 2)
}

/**
 * Calculate minimum engagement length to prevent thread stripping
 * Per Alexander's formula
 */
function calculateMinEngagementLength(thread: ThreadData, material: MaterialData): number {
  const props = MATERIAL_PROPERTIES[material.grade as keyof typeof MATERIAL_PROPERTIES]
  if (!props) {
    // Default to 1.5x major diameter for unknown materials
    return 1.5 * thread.majorDiameter
  }

  // Minimum engagement = 2.0 * P for coarse threads (conservative)
  // More detailed: Le_min = (2 * Rm * As) / (π * d * τ_shear * n)
  // Simplified conservative approach:
  const minimumEngagement = Math.max(
    1.0 * thread.majorDiameter, // At least 1x diameter
    2.0 * thread.pitch // At least 2x pitch
  )

  return minimumEngagement
}

/**
 * Calculate thread stripping strength
 */
function calculateStrippingStrength(
  thread: ThreadData,
  engagementLength: number,
  material: MaterialData,
  isInternalThread: boolean = false
): number {
  const props = MATERIAL_PROPERTIES[material.grade as keyof typeof MATERIAL_PROPERTIES]
  if (!props) return 0

  const shearStrength = material.shearStrength || props.shearStrength

  // Stripping area = π * n * Le * (d2 - d3) / 2
  const d2 = thread.majorDiameter - 0.649519 * thread.pitch
  const d3 = thread.minorDiameter
  const n = engagementLength / thread.pitch // Number of engaged threads

  // Shear area of threads in engagement
  const shearArea = Math.PI * n * engagementLength * (d2 - d3) / 2

  // Internal threads (nut) are typically weaker if in different material
  const factor = isInternalThread ? 0.85 : 1.0

  return factor * shearArea * shearStrength
}

/**
 * Calculate recommended torque
 * T = K * d * P
 * where K = nut factor (0.15-0.20 for dry, 0.10-0.12 for lubricated)
 *       d = nominal diameter
 *       P = preload force
 */
function calculateTorque(
  thread: ThreadData,
  material: MaterialData,
  options: TorqueCalculationOptions = {}
): { recommended: number; max: number; clampingForce: number } {
  const props = MATERIAL_PROPERTIES[material.grade as keyof typeof MATERIAL_PROPERTIES]
  if (!props) {
    return { recommended: 0, max: 0, clampingForce: 0 }
  }

  const nutFactor = options.nutFactor || 0.20 // Conservative (dry)
  const preloadPercentage = options.preloadPercentage || 75 // 75% of proof load

  const As = calculateTensileStressArea(thread)
  const proofLoad = (material.tensileStrength || props.proofLoad) * As
  const preload = (preloadPercentage / 100) * proofLoad

  const recommendedTorque = nutFactor * (thread.majorDiameter / 1000) * preload // Convert diameter to meters
  const maxTorque = 0.20 * (thread.majorDiameter / 1000) * proofLoad // Conservative max

  return {
    recommended: recommendedTorque,
    max: maxTorque,
    clampingForce: preload,
  }
}

/**
 * Estimate fatigue life using simplified S-N curve approach
 * Returns estimated cycles to failure
 */
function estimateFatigueLife(
  thread: ThreadData,
  material: MaterialData,
  options: FatigueOptions
): number {
  const props = MATERIAL_PROPERTIES[material.grade as keyof typeof MATERIAL_PROPERTIES]
  if (!props) return 0

  const tensileStrength = material.tensileStrength || props.tensileStrength
  const reliability = options.reliability || 99

  // Goodman diagram approach
  const enduranceLimit = 0.5 * tensileStrength // Conservative approximation

  // Adjusted stress amplitude considering mean stress
  const adjustedAmplitude = options.stressAmplitude / (1 - options.meanStress / tensileStrength)

  // Basquin equation: σ_a = σ'_f * (2N)^b
  // Simplified: use Miner's rule
  const stressRatio = adjustedAmplitude / enduranceLimit

  if (stressRatio < 1.0) {
    return Infinity // Infinite life (below endurance limit)
  }

  // Simplified S-N curve (conservative)
  const b = -0.12 // Fatigue strength exponent
  const cycles = Math.pow(stressRatio, 1 / b)

  return cycles
}

/**
 * Main strength calculation function
 */
export function calculateFastenerStrength(
  thread: ThreadData,
  material: MaterialData,
  options: {
    engagementLength?: number
    torqueOptions?: TorqueCalculationOptions
  } = {}
): StrengthResults {
  const props = MATERIAL_PROPERTIES[material.grade as keyof typeof MATERIAL_PROPERTIES]
  const warnings: string[] = []

  if (!props) {
    warnings.push(`Unknown material grade: ${material.grade}. Using generic values.`)
  }

  // Tensile calculations
  const tensileStressArea = calculateTensileStressArea(thread)
  const tensileStrength = material.tensileStrength || props?.tensileStrength || 400
  const proofLoadStress = material.tensileStrength || props?.proofLoad || 300

  const tensileLoadCapacity = tensileStrength * tensileStressArea
  const proofLoad = proofLoadStress * tensileStressArea

  // Shear calculations
  const shearArea = calculateShearArea(thread)
  const shearStrength = material.shearStrength || props?.shearStrength || 240
  const shearLoadCapacity = shearStrength * shearArea

  // Thread stripping
  const minEngagementLength = calculateMinEngagementLength(thread, material)
  const engagementLength = options.engagementLength || minEngagementLength

  if (engagementLength < minEngagementLength) {
    warnings.push(
      `Engagement length (${engagementLength.toFixed(1)}mm) is less than minimum ` +
      `(${minEngagementLength.toFixed(1)}mm). Thread stripping likely!`
    )
  }

  const strippingStrengthBolt = calculateStrippingStrength(thread, engagementLength, material, false)
  const strippingStrengthNut = calculateStrippingStrength(thread, engagementLength, material, true)

  // Torque calculations
  const torqueResults = calculateTorque(thread, material, options.torqueOptions)

  // Safety factor (based on proof load vs actual capacity)
  const safetyFactor = proofLoad / (0.75 * proofLoad) // Conservative

  // Check for common issues
  if (tensileLoadCapacity < shearLoadCapacity * 0.8) {
    warnings.push('Tensile failure likely before shear failure')
  }

  if (strippingStrengthBolt < tensileLoadCapacity) {
    warnings.push('Thread stripping may occur before bolt fracture. Increase engagement length.')
  }

  return {
    tensileStressArea,
    tensileLoadCapacity,
    proofLoad,
    shearArea,
    shearLoadCapacity,
    minEngagementLength,
    strippingStrengthBolt,
    strippingStrengthNut,
    recommendedTorque: torqueResults.recommended,
    maxTorque: torqueResults.max,
    clampingForce: torqueResults.clampingForce,
    safetyFactor,
    warnings,
  }
}

/**
 * Parse thread designation and return thread data
 */
export function parseThreadDesignation(threadId: string): ThreadData | null {
  // Match M3x0.5 format
  const metricMatch = threadId.match(/M(\d+(?:\.\d+)?)(?:x|\-)(\d+(?:\.\d+)?)/)
  if (metricMatch) {
    const majorDiameter = parseFloat(metricMatch[1])
    const pitch = parseFloat(metricMatch[2])

    // Calculate minor diameter using ISO formula
    // d3 = d - 1.226869 * P
    const minorDiameter = majorDiameter - 1.226869 * pitch

    return {
      majorDiameter,
      minorDiameter,
      pitch,
      threadDesignation: threadId,
    }
  }

  // Match imperial threads like 1/4-20
  const imperialMatch = threadId.match(/(\d+)\/(\d+)\-(\d+)/)
  if (imperialMatch) {
    const numerator = parseFloat(imperialMatch[1])
    const denominator = parseFloat(imperialMatch[2])
    const tpi = parseFloat(imperialMatch[3]) // Threads per inch

    const majorDiameter = (numerator / denominator) * 25.4 // Convert to mm
    const pitch = 25.4 / tpi // Convert to mm
    const minorDiameter = majorDiameter - 1.226869 * pitch

    return {
      majorDiameter,
      minorDiameter,
      pitch,
      threadDesignation: threadId,
    }
  }

  return null
}

/**
 * Quick check: Will this fastener hold?
 */
export function willItHold(
  threadId: string,
  materialGrade: string,
  requiredLoad: number, // N
  engagementLength?: number
): {
  safe: boolean
  margin: number // %
  limitingFactor: string
  recommendation: string
} {
  const thread = parseThreadDesignation(threadId)
  if (!thread) {
    return {
      safe: false,
      margin: 0,
      limitingFactor: 'unknown',
      recommendation: 'Invalid thread designation',
    }
  }

  const results = calculateFastenerStrength(thread, { grade: materialGrade }, { engagementLength })

  // Find the limiting strength
  const limits = {
    'tensile failure': results.tensileLoadCapacity,
    'shear failure': results.shearLoadCapacity,
    'thread stripping (bolt)': results.strippingStrengthBolt,
    'thread stripping (nut)': results.strippingStrengthNut,
  }

  let minLimit = Infinity
  let limitingFactor = ''

  for (const [factor, limit] of Object.entries(limits)) {
    if (limit < minLimit) {
      minLimit = limit
      limitingFactor = factor
    }
  }

  const margin = ((minLimit - requiredLoad) / requiredLoad) * 100
  const safe = margin > 0

  let recommendation = ''
  if (!safe) {
    if (limitingFactor.includes('thread stripping')) {
      recommendation = `Increase engagement length to at least ${results.minEngagementLength.toFixed(1)}mm`
    } else if (limitingFactor === 'tensile failure') {
      recommendation = `Use higher grade material (e.g., 10.9 or 12.9) or larger diameter`
    } else {
      recommendation = `Use larger diameter fastener`
    }
  } else {
    recommendation = `Safe with ${margin.toFixed(0)}% margin. Apply torque: ${results.recommendedTorque.toFixed(1)} Nm`
  }

  return {
    safe,
    margin,
    limitingFactor,
    recommendation,
  }
}

/**
 * Format results for display
 */
export function formatStrengthResults(results: StrengthResults): string {
  return `
STRENGTH ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TENSILE CAPACITY
  Stress Area:           ${results.tensileStressArea.toFixed(2)} mm²
  Load Capacity:         ${(results.tensileLoadCapacity / 1000).toFixed(2)} kN
  Proof Load:            ${(results.proofLoad / 1000).toFixed(2)} kN

SHEAR CAPACITY
  Shear Area:            ${results.shearArea.toFixed(2)} mm²
  Load Capacity:         ${(results.shearLoadCapacity / 1000).toFixed(2)} kN

THREAD ENGAGEMENT
  Minimum Length:        ${results.minEngagementLength.toFixed(1)} mm
  Stripping (Bolt):      ${(results.strippingStrengthBolt / 1000).toFixed(2)} kN
  Stripping (Nut):       ${(results.strippingStrengthNut / 1000).toFixed(2)} kN

TORQUE SPECIFICATIONS
  Recommended Torque:    ${results.recommendedTorque.toFixed(1)} Nm
  Maximum Torque:        ${results.maxTorque.toFixed(1)} Nm
  Clamping Force:        ${(results.clampingForce / 1000).toFixed(2)} kN

${results.warnings.length > 0 ? `WARNINGS:\n${results.warnings.map(w => `  ⚠️  ${w}`).join('\n')}` : '✅ No warnings'}
`
}
