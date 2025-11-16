'use client'

import { useState } from 'react'
import { willItHold, calculateFastenerStrength, parseThreadDesignation, formatStrengthResults } from '@/lib/strength-calculator'

/**
 * Strength Calculator Component
 *
 * Interactive tool to answer: "Will this fastener hold?"
 * Provides engineering calculations for safety-critical applications
 */
export default function StrengthCalculator() {
  const [threadId, setThreadId] = useState('M3x0.5')
  const [materialGrade, setMaterialGrade] = useState('A2-70')
  const [requiredLoad, setRequiredLoad] = useState(100)
  const [engagementLength, setEngagementLength] = useState<number>(0)
  const [results, setResults] = useState<any>(null)
  const [detailedResults, setDetailedResults] = useState<string>('')
  const [showDetailed, setShowDetailed] = useState(false)

  const handleCalculate = () => {
    // Quick check
    const quickResult = willItHold(
      threadId,
      materialGrade,
      requiredLoad,
      engagementLength > 0 ? engagementLength : undefined
    )
    setResults(quickResult)

    // Detailed calculations
    const thread = parseThreadDesignation(threadId)
    if (thread) {
      const detailed = calculateFastenerStrength(
        thread,
        { grade: materialGrade },
        { engagementLength: engagementLength > 0 ? engagementLength : undefined }
      )
      setDetailedResults(formatStrengthResults(detailed))
    }
  }

  const getSafetyColor = (margin: number) => {
    if (margin < 0) return 'text-red-600 bg-red-50 border-red-200'
    if (margin < 50) return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    return 'text-green-600 bg-green-50 border-green-200'
  }

  const getSafetyIcon = (safe: boolean) => {
    if (safe) {
      return (
        <svg className="h-12 w-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    } else {
      return (
        <svg className="h-12 w-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
        <h2 className="text-2xl font-bold mb-2">Strength Calculator</h2>
        <p className="text-blue-100">Engineering calculations for fastener strength and safety</p>
      </div>

      {/* Input Form */}
      <div className="bg-white rounded-lg border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Fastener Specifications</h3>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Thread Designation
            </label>
            <input
              type="text"
              value={threadId}
              onChange={(e) => setThreadId(e.target.value)}
              placeholder="e.g., M3x0.5, M5x0.8, 1/4-20"
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="mt-1 text-xs text-slate-500">
              Metric (M3x0.5) or Imperial (1/4-20)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Material Grade
            </label>
            <select
              value={materialGrade}
              onChange={(e) => setMaterialGrade(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="A2-70">A2-70 (304 SS)</option>
              <option value="A4-70">A4-70 (316 SS)</option>
              <option value="8.8">8.8 (Grade 5)</option>
              <option value="10.9">10.9 (Grade 8)</option>
              <option value="12.9">12.9 (High Strength)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Required Load (N)
            </label>
            <input
              type="number"
              value={requiredLoad}
              onChange={(e) => setRequiredLoad(parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="mt-1 text-xs text-slate-500">
              1 kg ≈ 10 N, 1 lb ≈ 4.4 N
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Engagement Length (mm) - Optional
            </label>
            <input
              type="number"
              value={engagementLength}
              onChange={(e) => setEngagementLength(parseFloat(e.target.value))}
              placeholder="Auto-calculate"
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="mt-1 text-xs text-slate-500">
              Leave 0 for minimum safe engagement
            </p>
          </div>
        </div>

        <button
          onClick={handleCalculate}
          className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          Calculate Strength
        </button>
      </div>

      {/* Results */}
      {results && (
        <div className={`rounded-lg border-2 p-6 ${getSafetyColor(results.margin)}`}>
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              {getSafetyIcon(results.safe)}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold mb-2">
                {results.safe ? 'SAFE TO USE' : 'UNSAFE - DO NOT USE'}
              </h3>
              <div className="space-y-2 text-sm">
                <p>
                  <strong>Safety Margin:</strong>{' '}
                  <span className="font-mono">
                    {results.margin > 0 ? '+' : ''}{results.margin.toFixed(1)}%
                  </span>
                </p>
                <p>
                  <strong>Limiting Factor:</strong> {results.limitingFactor}
                </p>
                <p>
                  <strong>Recommendation:</strong> {results.recommendation}
                </p>
              </div>

              <button
                onClick={() => setShowDetailed(!showDetailed)}
                className="mt-4 text-sm font-medium underline hover:no-underline"
              >
                {showDetailed ? 'Hide' : 'Show'} Detailed Analysis
              </button>

              {showDetailed && (
                <pre className="mt-4 p-4 bg-white rounded border text-xs overflow-x-auto">
                  {detailedResults}
                </pre>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Educational Info */}
      <div className="bg-blue-50 rounded-lg border border-blue-200 p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">How It Works</h3>
        <div className="space-y-2 text-sm text-blue-800">
          <p>
            <strong>Tensile Strength:</strong> Maximum pulling force before the bolt breaks
          </p>
          <p>
            <strong>Shear Strength:</strong> Maximum sideways force before failure
          </p>
          <p>
            <strong>Thread Stripping:</strong> Force required to strip the threads (often the weakest link)
          </p>
          <p>
            <strong>Engagement Length:</strong> How far the bolt threads into the nut/hole
          </p>
          <p className="pt-2 border-t border-blue-300">
            <strong>Safety Factor:</strong> We recommend at least 2x safety margin (100% margin) for critical applications
          </p>
        </div>
      </div>

      {/* Examples */}
      <div className="bg-slate-50 rounded-lg border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-3">Common Examples</h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div className="bg-white p-3 rounded border border-slate-200">
            <p className="font-medium text-slate-900">Hanging a 10kg shelf</p>
            <p className="text-xs text-slate-600 mt-1">
              Load: ~100N, Use: M4x0.7 Grade 8.8 minimum
            </p>
          </div>
          <div className="bg-white p-3 rounded border border-slate-200">
            <p className="font-medium text-slate-900">Structural beam connection</p>
            <p className="text-xs text-slate-600 mt-1">
              Load: 5000N+, Use: M12x1.75 Grade 10.9 minimum
            </p>
          </div>
          <div className="bg-white p-3 rounded border border-slate-200">
            <p className="font-medium text-slate-900">Engine mount bolt</p>
            <p className="text-xs text-slate-600 mt-1">
              High vibration, Use: Grade 12.9 with thread locker
            </p>
          </div>
          <div className="bg-white p-3 rounded border border-slate-200">
            <p className="font-medium text-slate-900">3D printer frame</p>
            <p className="text-xs text-slate-600 mt-1">
              Low load: M3x0.5 A2-70 adequate
            </p>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 rounded-lg border border-yellow-200 p-4">
        <p className="text-xs text-yellow-800">
          <strong>Disclaimer:</strong> These calculations are for educational and reference purposes only.
          For safety-critical applications, consult a qualified engineer and follow applicable codes and standards.
          Always use appropriate safety factors and consider environmental conditions, fatigue, corrosion, and other factors.
        </p>
      </div>
    </div>
  )
}
