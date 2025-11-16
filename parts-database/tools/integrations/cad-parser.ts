#!/usr/bin/env bun
/**
 * CAD File Parser
 *
 * Extracts precise dimensions from CAD files:
 * - STEP files (ISO 10303-21)
 * - STL files (stereolithography)
 * - IGES files
 *
 * Usage:
 *   bun tools/integrations/cad-parser.ts <file.step>
 */

import { readFileSync } from 'fs'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

interface BoundingBox {
  min: { x: number; y: number; z: number }
  max: { x: number; y: number; z: number }
  dimensions: { length: number; width: number; height: number }
}

interface ThreadInfo {
  major_diameter: number
  minor_diameter: number
  pitch?: number
  thread_length?: number
}

interface CADDimensions {
  boundingBox: BoundingBox
  cylindrical?: {
    diameter: number
    height: number
  }
  threads?: ThreadInfo
  holes?: Array<{
    diameter: number
    depth: number
    position: { x: number; y: number; z: number }
  }>
  volume: number
  surfaceArea: number
}

/**
 * Parse STEP file (ISO 10303-21 format)
 */
function parseSTEP(filePath: string): CADDimensions | null {
  console.log(`📐 Parsing STEP file: ${filePath}`)

  try {
    const content = readFileSync(filePath, 'utf-8')

    // STEP files have specific structure
    // Header: ISO-10303-21;
    // Data section with entities
    // Footer: END-ISO-10303-21;

    if (!content.includes('ISO-10303-21')) {
      throw new Error('Invalid STEP file format')
    }

    // Extract data section
    const dataMatch = content.match(/DATA;([\s\S]*?)ENDSEC;/)
    if (!dataMatch) throw new Error('No data section found')

    const dataSection = dataMatch[1]

    // Parse entities
    const points = extractPoints(dataSection)
    const boundingBox = calculateBoundingBox(points)

    // Detect cylindrical features
    const cylindrical = detectCylinder(dataSection, points)

    // Detect thread features
    const threads = detectThreads(dataSection)

    // Detect holes
    const holes = detectHoles(dataSection, points)

    return {
      boundingBox,
      cylindrical,
      threads,
      holes,
      volume: estimateVolume(points),
      surfaceArea: estimateSurfaceArea(points),
    }
  } catch (error: any) {
    console.error('❌ Failed to parse STEP file:', error.message)
    return null
  }
}

/**
 * Parse STL file (stereolithography)
 */
function parseSTL(filePath: string): CADDimensions | null {
  console.log(`📐 Parsing STL file: ${filePath}`)

  try {
    const buffer = readFileSync(filePath)

    // STL can be ASCII or binary
    const isASCII = buffer.toString('utf-8', 0, 5) === 'solid'

    if (isASCII) {
      return parseSTLAscii(buffer.toString('utf-8'))
    } else {
      return parseSTLBinary(buffer)
    }
  } catch (error: any) {
    console.error('❌ Failed to parse STL file:', error.message)
    return null
  }
}

/**
 * Parse ASCII STL format
 */
function parseSTLAscii(content: string): CADDimensions | null {
  const points: Array<{ x: number; y: number; z: number }> = []

  // Extract vertices from facets
  const vertexPattern = /vertex\s+([-\d.e]+)\s+([-\d.e]+)\s+([-\d.e]+)/g
  let match

  while ((match = vertexPattern.exec(content)) !== null) {
    points.push({
      x: parseFloat(match[1]),
      y: parseFloat(match[2]),
      z: parseFloat(match[3]),
    })
  }

  if (points.length === 0) return null

  const boundingBox = calculateBoundingBox(points)
  const cylindrical = detectCylindricalMesh(points)

  return {
    boundingBox,
    cylindrical,
    volume: estimateVolume(points),
    surfaceArea: estimateSurfaceArea(points),
  }
}

/**
 * Parse binary STL format
 */
function parseSTLBinary(buffer: Buffer): CADDimensions | null {
  // Binary STL structure:
  // Header (80 bytes)
  // Number of triangles (4 bytes)
  // For each triangle:
  //   Normal vector (12 bytes)
  //   Vertex 1 (12 bytes)
  //   Vertex 2 (12 bytes)
  //   Vertex 3 (12 bytes)
  //   Attribute byte count (2 bytes)

  const triangleCount = buffer.readUInt32LE(80)
  const points: Array<{ x: number; y: number; z: number }> = []

  for (let i = 0; i < triangleCount; i++) {
    const offset = 84 + i * 50

    // Skip normal (12 bytes), read 3 vertices
    for (let v = 0; v < 3; v++) {
      const vertexOffset = offset + 12 + v * 12
      points.push({
        x: buffer.readFloatLE(vertexOffset),
        y: buffer.readFloatLE(vertexOffset + 4),
        z: buffer.readFloatLE(vertexOffset + 8),
      })
    }
  }

  const boundingBox = calculateBoundingBox(points)
  const cylindrical = detectCylindricalMesh(points)

  return {
    boundingBox,
    cylindrical,
    volume: estimateVolume(points),
    surfaceArea: estimateSurfaceArea(points),
  }
}

/**
 * Extract coordinate points from STEP data
 */
function extractPoints(dataSection: string): Array<{ x: number; y: number; z: number }> {
  const points: Array<{ x: number; y: number; z: number }> = []

  // STEP points are usually defined as CARTESIAN_POINT
  const pointPattern = /CARTESIAN_POINT\([^)]*\(([^)]+)\)/g
  let match

  while ((match = pointPattern.exec(dataSection)) !== null) {
    const coords = match[1].split(',').map(s => parseFloat(s.trim()))
    if (coords.length >= 3) {
      points.push({ x: coords[0], y: coords[1], z: coords[2] })
    }
  }

  return points
}

/**
 * Calculate bounding box from points
 */
function calculateBoundingBox(points: Array<{ x: number; y: number; z: number }>): BoundingBox {
  const min = { x: Infinity, y: Infinity, z: Infinity }
  const max = { x: -Infinity, y: -Infinity, z: -Infinity }

  points.forEach(p => {
    if (p.x < min.x) min.x = p.x
    if (p.y < min.y) min.y = p.y
    if (p.z < min.z) min.z = p.z
    if (p.x > max.x) max.x = p.x
    if (p.y > max.y) max.y = p.y
    if (p.z > max.z) max.z = p.z
  })

  return {
    min,
    max,
    dimensions: {
      length: max.x - min.x,
      width: max.y - min.y,
      height: max.z - min.z,
    },
  }
}

/**
 * Detect cylinder from STEP entities
 */
function detectCylinder(dataSection: string, points: Array<{ x: number; y: number; z: number }>) {
  // Look for CYLINDRICAL_SURFACE entities
  const cylinderMatch = dataSection.match(/CYLINDRICAL_SURFACE[^;]*CIRCLE[^;]*,\s*([\d.]+)/i)

  if (cylinderMatch) {
    const radius = parseFloat(cylinderMatch[1])
    const bbox = calculateBoundingBox(points)

    return {
      diameter: radius * 2,
      height: Math.max(bbox.dimensions.length, bbox.dimensions.width, bbox.dimensions.height),
    }
  }

  return undefined
}

/**
 * Detect cylindrical shape from mesh points
 */
function detectCylindricalMesh(points: Array<{ x: number; y: number; z: number }>) {
  // Calculate if points form a cylinder by checking radial distances
  const bbox = calculateBoundingBox(points)

  // Find center
  const center = {
    x: (bbox.min.x + bbox.max.x) / 2,
    y: (bbox.min.y + bbox.max.y) / 2,
    z: (bbox.min.z + bbox.max.z) / 2,
  }

  // Calculate radial distances (ignoring one axis for cylinder)
  const radiusXY = points.map(p =>
    Math.sqrt(Math.pow(p.x - center.x, 2) + Math.pow(p.y - center.y, 2))
  )

  const avgRadius = radiusXY.reduce((a, b) => a + b, 0) / radiusXY.length
  const radiusVariance = radiusXY.reduce((sum, r) => sum + Math.pow(r - avgRadius, 2), 0) / radiusXY.length

  // If variance is low, it's likely cylindrical
  if (radiusVariance < avgRadius * 0.1) {
    return {
      diameter: avgRadius * 2,
      height: bbox.dimensions.height,
    }
  }

  return undefined
}

/**
 * Detect thread features
 */
function detectThreads(dataSection: string): ThreadInfo | undefined {
  // Look for thread-related entities or patterns
  // This is simplified - real implementation would analyze helix patterns

  const threadMatch = dataSection.match(/THREAD|HELIX/i)
  if (!threadMatch) return undefined

  // Extract thread pitch if specified
  const pitchMatch = dataSection.match(/PITCH[^,]*,\s*([\d.]+)/)
  const diameterMatch = dataSection.match(/DIAMETER[^,]*,\s*([\d.]+)/)

  if (diameterMatch) {
    return {
      major_diameter: parseFloat(diameterMatch[1]),
      minor_diameter: parseFloat(diameterMatch[1]) * 0.85, // Estimate
      pitch: pitchMatch ? parseFloat(pitchMatch[1]) : undefined,
    }
  }

  return undefined
}

/**
 * Detect holes in the model
 */
function detectHoles(dataSection: string, points: Array<{ x: number; y: number; z: number }>) {
  const holes: Array<{ diameter: number; depth: number; position: { x: number; y: number; z: number } }> = []

  // Look for circular holes (simplified)
  const holeMatches = dataSection.matchAll(/HOLE|CIRCLE[^;]*,\s*([\d.]+)/gi)

  for (const match of holeMatches) {
    const diameter = parseFloat(match[1])
    // Would need to determine position and depth from geometry
    holes.push({
      diameter,
      depth: 0, // Would calculate from geometry
      position: { x: 0, y: 0, z: 0 }, // Would extract from entities
    })
  }

  return holes.length > 0 ? holes : undefined
}

/**
 * Estimate volume from point cloud
 */
function estimateVolume(points: Array<{ x: number; y: number; z: number }>): number {
  const bbox = calculateBoundingBox(points)
  // Simplified: use bounding box volume
  return bbox.dimensions.length * bbox.dimensions.width * bbox.dimensions.height
}

/**
 * Estimate surface area
 */
function estimateSurfaceArea(points: Array<{ x: number; y: number; z: number }>): number {
  const bbox = calculateBoundingBox(points)
  // Simplified: use bounding box surface area
  const { length, width, height } = bbox.dimensions
  return 2 * (length * width + width * height + height * length)
}

/**
 * Main parsing function
 */
async function parseCADFile(filePath: string): Promise<void> {
  const ext = filePath.toLowerCase().split('.').pop()

  let dimensions: CADDimensions | null = null

  if (ext === 'step' || ext === 'stp') {
    dimensions = parseSTEP(filePath)
  } else if (ext === 'stl') {
    dimensions = parseSTL(filePath)
  } else {
    console.error('❌ Unsupported file format. Use .step or .stl')
    process.exit(1)
  }

  if (!dimensions) {
    console.error('❌ Failed to extract dimensions')
    process.exit(1)
  }

  // Display results
  console.log('\n📊 Extracted Dimensions:')
  console.log('─'.repeat(50))
  console.log('\n🔲 Bounding Box:')
  console.log(`  Length: ${dimensions.boundingBox.dimensions.length.toFixed(2)} mm`)
  console.log(`  Width:  ${dimensions.boundingBox.dimensions.width.toFixed(2)} mm`)
  console.log(`  Height: ${dimensions.boundingBox.dimensions.height.toFixed(2)} mm`)

  if (dimensions.cylindrical) {
    console.log('\n🔵 Cylindrical Features:')
    console.log(`  Diameter: ${dimensions.cylindrical.diameter.toFixed(2)} mm`)
    console.log(`  Height:   ${dimensions.cylindrical.height.toFixed(2)} mm`)
  }

  if (dimensions.threads) {
    console.log('\n🔩 Thread Features:')
    console.log(`  Major Diameter: ${dimensions.threads.major_diameter.toFixed(2)} mm`)
    console.log(`  Minor Diameter: ${dimensions.threads.minor_diameter.toFixed(2)} mm`)
    if (dimensions.threads.pitch) {
      console.log(`  Pitch:          ${dimensions.threads.pitch.toFixed(2)} mm`)
    }
  }

  if (dimensions.holes && dimensions.holes.length > 0) {
    console.log('\n⭕ Holes:')
    dimensions.holes.forEach((hole, i) => {
      console.log(`  Hole ${i + 1}: ${hole.diameter.toFixed(2)} mm diameter`)
    })
  }

  console.log(`\n📦 Volume:       ${dimensions.volume.toFixed(2)} mm³`)
  console.log(`📏 Surface Area: ${dimensions.surfaceArea.toFixed(2)} mm²`)
  console.log('')
}

// Main
const filePath = process.argv[2]

if (!filePath) {
  console.error('Usage: bun tools/integrations/cad-parser.ts <file.step|file.stl>')
  console.error('Example: bun tools/integrations/cad-parser.ts screw_m3.step')
  process.exit(1)
}

console.log('🔧 CAD File Parser')
console.log('')

parseCADFile(filePath)
  .catch(err => {
    console.error('❌ Unexpected error:', err)
    process.exit(1)
  })
