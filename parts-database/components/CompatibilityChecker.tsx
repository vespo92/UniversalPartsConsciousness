'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

interface CompatibilityResult {
  compatible: boolean
  engagement_length?: number
  protrusion?: number
  warnings: string[]
  recommendations: string[]
}

export default function CompatibilityChecker() {
  const [screwThread, setScrewThread] = useState('')
  const [screwLength, setScrewLength] = useState('')
  const [holeThread, setHoleThread] = useState('')
  const [materialThickness, setMaterialThickness] = useState('')
  const [result, setResult] = useState<CompatibilityResult | null>(null)
  const [loading, setLoading] = useState(false)

  const checkCompatibility = async () => {
    setLoading(true)
    try {
      // Basic compatibility check logic
      const length = parseFloat(screwLength)
      const thickness = parseFloat(materialThickness)

      const warnings: string[] = []
      const recommendations: string[] = []
      let compatible = true

      // Check thread match
      if (screwThread !== holeThread) {
        compatible = false
        warnings.push('Thread sizes do not match')
      }

      // Calculate engagement
      const engagement = Math.min(length, thickness)
      const protrusion = Math.max(length - thickness, 0)

      // Parse thread diameter (e.g., "M3x0.5" -> 3)
      const threadMatch = screwThread.match(/M?(\d+\.?\d*)/)
      const diameter = threadMatch ? parseFloat(threadMatch[1]) : 0

      // Check engagement ratio (should be 1.5x to 3x diameter)
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

      // Check protrusion
      if (protrusion > diameter * 2) {
        warnings.push(`Excessive protrusion: ${protrusion.toFixed(1)}mm`)
        recommendations.push('Use a shorter screw or add a spacer')
      } else if (protrusion > 0) {
        recommendations.push(`Protrusion: ${protrusion.toFixed(1)}mm`)
      }

      setResult({
        compatible,
        engagement_length: engagement,
        protrusion,
        warnings,
        recommendations
      })

    } catch (error) {
      console.error('Error checking compatibility:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Input Form */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Screw Thread Size
          </label>
          <input
            type="text"
            value={screwThread}
            onChange={(e) => setScrewThread(e.target.value)}
            placeholder="e.g., M3x0.5, M5x0.8"
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Screw Length (mm)
          </label>
          <input
            type="number"
            value={screwLength}
            onChange={(e) => setScrewLength(e.target.value)}
            placeholder="e.g., 12"
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Hole Thread Size
          </label>
          <input
            type="text"
            value={holeThread}
            onChange={(e) => setHoleThread(e.target.value)}
            placeholder="e.g., M3x0.5, M5x0.8"
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Material Thickness (mm)
          </label>
          <input
            type="number"
            value={materialThickness}
            onChange={(e) => setMaterialThickness(e.target.value)}
            placeholder="e.g., 10"
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      <button
        onClick={checkCompatibility}
        disabled={!screwThread || !screwLength || !holeThread || !materialThickness || loading}
        className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors font-medium"
      >
        {loading ? 'Checking...' : 'Check Compatibility'}
      </button>

      {/* Results */}
      {result && (
        <div className={`rounded-lg p-6 ${
          result.compatible
            ? 'bg-green-50 border-2 border-green-200'
            : 'bg-red-50 border-2 border-red-200'
        }`}>
          <div className="flex items-start">
            <div className="flex-shrink-0">
              {result.compatible ? (
                <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              ) : (
                <svg className="h-8 w-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
            </div>
            <div className="ml-4 flex-1">
              <h3 className={`text-lg font-semibold ${
                result.compatible ? 'text-green-900' : 'text-red-900'
              }`}>
                {result.compatible ? 'Compatible' : 'Incompatible'}
              </h3>

              {result.engagement_length !== undefined && (
                <div className="mt-3 space-y-2 text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-slate-700 font-medium">Thread Engagement:</span>
                      <span className="ml-2">{result.engagement_length.toFixed(1)}mm</span>
                    </div>
                    {result.protrusion !== undefined && result.protrusion > 0 && (
                      <div>
                        <span className="text-slate-700 font-medium">Protrusion:</span>
                        <span className="ml-2">{result.protrusion.toFixed(1)}mm</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {result.warnings.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium text-red-900 mb-2">Warnings:</h4>
                  <ul className="space-y-1">
                    {result.warnings.map((warning, i) => (
                      <li key={i} className="text-sm text-red-800 flex items-start">
                        <span className="mr-2">•</span>
                        <span>{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {result.recommendations.length > 0 && (
                <div className="mt-4">
                  <h4 className={`font-medium mb-2 ${
                    result.compatible ? 'text-green-900' : 'text-slate-900'
                  }`}>
                    {result.compatible ? 'Notes:' : 'Recommendations:'}
                  </h4>
                  <ul className="space-y-1">
                    {result.recommendations.map((rec, i) => (
                      <li key={i} className={`text-sm flex items-start ${
                        result.compatible ? 'text-green-800' : 'text-slate-700'
                      }`}>
                        <span className="mr-2">•</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Quick Reference */}
      <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
        <h4 className="font-medium text-blue-900 mb-2">Quick Reference</h4>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• Thread engagement should be 1.5x to 3x the thread diameter</li>
          <li>• Thread sizes must match exactly (e.g., M3x0.5 only fits M3x0.5)</li>
          <li>• Consider material compatibility (steel in aluminum requires thread inserts)</li>
          <li>• Use thread lock for critical applications</li>
        </ul>
      </div>
    </div>
  )
}
