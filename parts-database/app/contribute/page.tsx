'use client'

import { useState } from 'react'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'

export default function Contribute() {
  const [formData, setFormData] = useState({
    part_id: '',
    manufacturer: '',
    part_number: '',
    category: 'fastener',
    subcategory: '',
    thread_id: '',
    length: '',
    material_grade: '',
    tensile_strength: '',
    yield_strength: '',
    notes: ''
  })
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    setSuccess(false)

    try {
      // Build the part object
      const part = {
        part_id: formData.part_id || `${formData.manufacturer}-${formData.part_number}-${Date.now()}`,
        manufacturer: formData.manufacturer,
        part_number: formData.part_number,
        category: formData.category,
        subcategory: formData.subcategory || null,
        thread_id: formData.thread_id || null,
        length: formData.length ? parseFloat(formData.length) : null,
        material_grade: formData.material_grade || null,
        tensile_strength: formData.tensile_strength ? parseFloat(formData.tensile_strength) : null,
        yield_strength: formData.yield_strength ? parseFloat(formData.yield_strength) : null,
        data_source: 'user_contribution',
        verification_status: 'unverified',
        full_specs: {
          notes: formData.notes,
          contributed_at: new Date().toISOString()
        }
      }

      const { error: insertError } = await supabase
        .from('parts')
        .insert([part])

      if (insertError) throw insertError

      setSuccess(true)
      // Reset form
      setFormData({
        part_id: '',
        manufacturer: '',
        part_number: '',
        category: 'fastener',
        subcategory: '',
        thread_id: '',
        length: '',
        material_grade: '',
        tensile_strength: '',
        yield_strength: '',
        notes: ''
      })

    } catch (err: any) {
      console.error('Error submitting part:', err)
      setError(err.message || 'Failed to submit part. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const updateField = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                Add a Part
              </h1>
              <p className="mt-1 text-sm text-slate-600">
                Help build the world's most comprehensive parts database
              </p>
            </div>
            <Link
              href="/"
              className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors font-medium"
            >
              Back
            </Link>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          {success && (
            <div className="mb-6 bg-green-50 border-2 border-green-200 rounded-lg p-4">
              <div className="flex items-start">
                <svg className="h-5 w-5 text-green-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-green-900">Success!</h3>
                  <p className="mt-1 text-sm text-green-700">
                    Your part has been added to the database. Thank you for contributing!
                  </p>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="mb-6 bg-red-50 border-2 border-red-200 rounded-lg p-4">
              <div className="flex items-start">
                <svg className="h-5 w-5 text-red-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-900">Error</h3>
                  <p className="mt-1 text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Basic Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Manufacturer *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.manufacturer}
                    onChange={(e) => updateField('manufacturer', e.target.value)}
                    placeholder="e.g., DIN, ISO, McMaster-Carr"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Part Number *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.part_number}
                    onChange={(e) => updateField('part_number', e.target.value)}
                    placeholder="e.g., 912-M3x12"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Category *
                  </label>
                  <select
                    required
                    value={formData.category}
                    onChange={(e) => updateField('category', e.target.value)}
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="fastener">Fastener</option>
                    <option value="bearing">Bearing</option>
                    <option value="seal">Seal</option>
                    <option value="hardware">Hardware</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Subcategory
                  </label>
                  <input
                    type="text"
                    value={formData.subcategory}
                    onChange={(e) => updateField('subcategory', e.target.value)}
                    placeholder="e.g., socket_head_cap_screw"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            {/* Dimensions */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Dimensions</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Thread Size
                  </label>
                  <input
                    type="text"
                    value={formData.thread_id}
                    onChange={(e) => updateField('thread_id', e.target.value)}
                    placeholder="e.g., M3x0.5, M5x0.8"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <p className="mt-1 text-xs text-slate-500">For threaded parts only</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Length (mm)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.length}
                    onChange={(e) => updateField('length', e.target.value)}
                    placeholder="e.g., 12.0"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            {/* Material Properties */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Material Properties</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Material Grade
                  </label>
                  <input
                    type="text"
                    value={formData.material_grade}
                    onChange={(e) => updateField('material_grade', e.target.value)}
                    placeholder="e.g., A2-70, 8.8"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Tensile Strength (MPa)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.tensile_strength}
                    onChange={(e) => updateField('tensile_strength', e.target.value)}
                    placeholder="e.g., 700"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Yield Strength (MPa)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.yield_strength}
                    onChange={(e) => updateField('yield_strength', e.target.value)}
                    placeholder="e.g., 450"
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Additional Notes
              </label>
              <textarea
                value={formData.notes}
                onChange={(e) => updateField('notes', e.target.value)}
                rows={4}
                placeholder="Any additional information about this part, where it's used, compatibility notes, etc."
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Submit */}
            <div className="flex justify-end space-x-4">
              <Link
                href="/"
                className="px-6 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors font-medium"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={submitting}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {submitting ? 'Submitting...' : 'Add Part'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}
