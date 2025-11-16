import StrengthCalculator from '@/components/StrengthCalculator'
import Link from 'next/link'

export const metadata = {
  title: 'Strength Calculator - Universal Parts Consciousness',
  description: 'Engineering calculations for fastener strength, torque, and safety',
}

export default function CalculatorPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-5xl mx-auto p-6">
        {/* Navigation */}
        <div className="mb-6">
          <Link
            href="/"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
          >
            <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Parts Database
          </Link>
        </div>

        {/* Main Content */}
        <StrengthCalculator />

        {/* API Info */}
        <div className="mt-8 bg-white rounded-lg border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-3">Developer API</h3>
          <p className="text-sm text-slate-600 mb-4">
            Use the strength calculator in your applications via our API or command-line tool.
          </p>

          <div className="space-y-3">
            <div>
              <p className="text-xs font-medium text-slate-700 mb-1">Command Line:</p>
              <pre className="bg-slate-900 text-slate-100 p-3 rounded text-xs overflow-x-auto">
                bun tools/strength-check.ts M3x0.5 A2-70 100 --detailed
              </pre>
            </div>

            <div>
              <p className="text-xs font-medium text-slate-700 mb-1">TypeScript/JavaScript:</p>
              <pre className="bg-slate-900 text-slate-100 p-3 rounded text-xs overflow-x-auto">
{`import { willItHold } from '@/lib/strength-calculator'

const result = willItHold('M3x0.5', 'A2-70', 100)
console.log(result.safe)        // true/false
console.log(result.margin)      // safety margin %
console.log(result.recommendation)`}
              </pre>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-slate-500">
          <p>
            Based on ISO 898-1, VDI 2230, and Machinery's Handbook standards.
            <br />
            Always consult a qualified engineer for safety-critical applications.
          </p>
        </div>
      </div>
    </div>
  )
}
