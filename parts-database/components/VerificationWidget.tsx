'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

interface VerificationWidgetProps {
  partId: string
  onVerificationComplete?: () => void
}

export default function VerificationWidget({ partId, onVerificationComplete }: VerificationWidgetProps) {
  const [showForm, setShowForm] = useState(false)
  const [verificationType, setVerificationType] = useState('visual')
  const [confidence, setConfidence] = useState('medium')
  const [notes, setNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async () => {
    setSubmitting(true)

    try {
      // Submit verification
      const { error } = await supabase
        .from('part_verifications')
        .insert({
          part_id: partId,
          verification_type: verificationType,
          confidence_level: confidence,
          notes,
          status: 'active',
        })

      if (error) throw error

      // Award reputation points
      await supabase
        .from('reputation_events')
        .insert({
          event_type: 'verification',
          points_change: confidence === 'high' ? 10 : confidence === 'medium' ? 5 : 3,
          related_id: partId,
          description: `Verified part ${partId}`,
        })

      setShowForm(false)
      setNotes('')
      if (onVerificationComplete) onVerificationComplete()
    } catch (err: any) {
      console.error('Verification failed:', err)
      alert('Failed to submit verification: ' + err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mt-4">
      {!showForm ? (
        <button
          onClick={() => setShowForm(true)}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
        >
          ✓ Verify This Part
        </button>
      ) : (
        <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
          <h3 className="font-semibold text-slate-900 mb-4">Verify Part Specifications</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Verification Type
              </label>
              <select
                value={verificationType}
                onChange={(e) => setVerificationType(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="visual">Visual Inspection</option>
                <option value="measurement">Physical Measurement</option>
                <option value="spec_sheet">Manufacturer Spec Sheet</option>
                <option value="usage">Confirmed Usage</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Confidence Level
              </label>
              <select
                value={confidence}
                onChange={(e) => setConfidence(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="low">Low - Visual only</option>
                <option value="medium">Medium - Measured or documented</option>
                <option value="high">High - Verified against official specs</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Notes (Optional)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                placeholder="Add any details about your verification..."
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="flex space-x-3">
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-slate-300 transition-colors font-medium"
              >
                {submitting ? 'Submitting...' : 'Submit Verification'}
              </button>
              <button
                onClick={() => setShowForm(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors"
              >
                Cancel
              </button>
            </div>

            <p className="text-xs text-slate-500">
              Earn +{confidence === 'high' ? '10' : confidence === 'medium' ? '5' : '3'} reputation points for this verification
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
