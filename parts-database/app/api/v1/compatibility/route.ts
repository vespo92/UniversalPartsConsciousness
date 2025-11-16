import { NextRequest, NextResponse } from 'next/server'

// POST /api/v1/compatibility - Check compatibility between screw and hole
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const { screw_thread, screw_length, hole_thread, material_thickness } = body

    if (!screw_thread || !screw_length || !hole_thread || !material_thickness) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields' },
        { status: 400 }
      )
    }

    const length = parseFloat(screw_length)
    const thickness = parseFloat(material_thickness)

    const warnings: string[] = []
    const recommendations: string[] = []
    let compatible = true

    // Thread match check
    if (screw_thread !== hole_thread) {
      compatible = false
      warnings.push('Thread sizes do not match')
    }

    // Engagement calculation
    const engagement = Math.min(length, thickness)
    const protrusion = Math.max(length - thickness, 0)

    // Parse diameter
    const threadMatch = screw_thread.match(/M?(\d+\.?\d*)/)
    const diameter = threadMatch ? parseFloat(threadMatch[1]) : 0

    // Engagement ratio check
    if (diameter > 0) {
      const engagementRatio = engagement / diameter

      if (engagementRatio < 1.5) {
        warnings.push(`Insufficient thread engagement (${engagementRatio.toFixed(1)}x diameter, need 1.5x minimum)`)
        recommendations.push('Use a longer screw or reduce material thickness')
        compatible = false
      } else if (engagementRatio > 3.0) {
        warnings.push(`Excessive engagement (${engagementRatio.toFixed(1)}x diameter, max recommended 3x)`)
        recommendations.push('Consider a shorter screw')
      } else {
        recommendations.push(`Good engagement ratio: ${engagementRatio.toFixed(1)}x diameter`)
      }
    }

    // Protrusion check
    if (protrusion > diameter * 2) {
      warnings.push(`Excessive protrusion: ${protrusion.toFixed(1)}mm`)
      recommendations.push('Use a shorter screw or add a spacer')
    }

    return NextResponse.json({
      success: true,
      data: {
        compatible,
        engagement_length: engagement,
        protrusion,
        engagement_ratio: diameter > 0 ? engagement / diameter : null,
        warnings,
        recommendations,
      },
    })
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    )
  }
}
