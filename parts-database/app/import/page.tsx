'use client'

import { useState } from 'react'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'

interface ParsedPart {
  manufacturer: string
  part_number: string
  category: string
  subcategory?: string
  thread_id?: string
  length?: number
  material_grade?: string
  tensile_strength?: number
  yield_strength?: number
  notes?: string
  errors?: string[]
}

export default function ImportPage() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<ParsedPart[]>([])
  const [importing, setImporting] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')
  const [dragActive, setDragActive] = useState(false)

  const parseCSV = (text: string): ParsedPart[] => {
    const lines = text.trim().split('\n')
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase())

    return lines.slice(1).map((line, idx) => {
      const values = line.split(',').map(v => v.trim())
      const row: any = {}
      const errors: string[] = []

      headers.forEach((header, i) => {
        if (values[i]) {
          row[header] = values[i]
        }
      })

      // Validation
      if (!row.manufacturer) errors.push('Missing manufacturer')
      if (!row.part_number) errors.push('Missing part_number')
      if (!row.category) errors.push('Missing category')

      // Type conversions
      const part: ParsedPart = {
        manufacturer: row.manufacturer,
        part_number: row.part_number,
        category: row.category,
        subcategory: row.subcategory,
        thread_id: row.thread_id,
        length: row.length ? parseFloat(row.length) : undefined,
        material_grade: row.material_grade,
        tensile_strength: row.tensile_strength ? parseFloat(row.tensile_strength) : undefined,
        yield_strength: row.yield_strength ? parseFloat(row.yield_strength) : undefined,
        notes: row.notes,
        errors: errors.length > 0 ? errors : undefined
      }

      return part
    })
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file: File) => {
    setFile(file)
    setError('')
    setSuccess(false)

    const text = await file.text()
    try {
      const parts = parseCSV(text)
      setPreview(parts)
    } catch (err: any) {
      setError('Failed to parse CSV: ' + err.message)
    }
  }

  const handleImport = async () => {
    setImporting(true)
    setError('')
    setSuccess(false)

    try {
      const validParts = preview.filter(p => !p.errors || p.errors.length === 0)

      const partsToInsert = validParts.map(p => ({
        part_id: `${p.manufacturer}-${p.part_number}`.replace(/\s/g, '-'),
        manufacturer: p.manufacturer,
        part_number: p.part_number,
        category: p.category,
        subcategory: p.subcategory || null,
        thread_id: p.thread_id || null,
        length: p.length || null,
        material_grade: p.material_grade || null,
        tensile_strength: p.tensile_strength || null,
        yield_strength: p.yield_strength || null,
        data_source: 'csv_import',
        verification_status: 'unverified',
        full_specs: {
          notes: p.notes || '',
          imported_at: new Date().toISOString(),
          import_source: 'web_csv_upload'
        }
      }))

      const { error: insertError } = await supabase
        .from('parts')
        .insert(partsToInsert)

      if (insertError) throw insertError

      setSuccess(true)
      setPreview([])
      setFile(null)
    } catch (err: any) {
      setError(err.message || 'Import failed')
    } finally {
      setImporting(false)
    }
  }

  const validCount = preview.filter(p => !p.errors || p.errors.length === 0).length
  const errorCount = preview.filter(p => p.errors && p.errors.length > 0).length

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                Bulk Import
              </h1>
              <p className="mt-1 text-sm text-slate-600">
                Import hundreds of parts at once via CSV
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

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {success && (
          <div className="mb-6 bg-green-50 border-2 border-green-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="h-5 w-5 text-green-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-900">Success!</h3>
                <p className="mt-1 text-sm text-green-700">
                  {validCount} parts imported successfully!
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

        {/* Upload Area */}
        {!preview.length && (
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-8">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                dragActive
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-slate-300 hover:border-slate-400'
              }`}
            >
              <svg
                className="mx-auto h-12 w-12 text-slate-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="mt-4">
                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="text-blue-600 hover:text-blue-700 font-medium">
                    Upload a CSV file
                  </span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    accept=".csv"
                    className="sr-only"
                    onChange={handleFileInput}
                  />
                </label>
                <p className="text-slate-500"> or drag and drop</p>
              </div>
              <p className="mt-2 text-xs text-slate-500">
                CSV format: manufacturer, part_number, category, thread_id, length, ...
              </p>
            </div>

            {/* Template Download */}
            <div className="mt-6 flex items-center justify-center">
              <a
                href="/api/download-template"
                className="text-sm text-blue-600 hover:text-blue-700 flex items-center"
              >
                <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download CSV Template
              </a>
            </div>
          </div>
        )}

        {/* Preview */}
        {preview.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Preview Import</h2>
                <p className="text-sm text-slate-600 mt-1">
                  {validCount} valid parts, {errorCount} errors
                </p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={() => {
                    setPreview([])
                    setFile(null)
                  }}
                  className="px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleImport}
                  disabled={validCount === 0 || importing}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {importing ? 'Importing...' : `Import ${validCount} Parts`}
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200">
                <thead className="bg-slate-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Status</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Manufacturer</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Part Number</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Category</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Thread</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Length</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Material</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {preview.map((part, idx) => (
                    <tr key={idx} className={part.errors ? 'bg-red-50' : ''}>
                      <td className="px-4 py-3">
                        {part.errors ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            Error
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Valid
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-slate-900">{part.manufacturer}</td>
                      <td className="px-4 py-3 text-sm text-slate-900">{part.part_number}</td>
                      <td className="px-4 py-3 text-sm text-slate-600">{part.category}</td>
                      <td className="px-4 py-3 text-sm text-slate-600">{part.thread_id || '-'}</td>
                      <td className="px-4 py-3 text-sm text-slate-600">{part.length || '-'}</td>
                      <td className="px-4 py-3 text-sm text-slate-600">{part.material_grade || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {errorCount > 0 && (
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h3 className="text-sm font-medium text-yellow-900">Validation Errors</h3>
                <ul className="mt-2 text-sm text-yellow-700 list-disc list-inside">
                  {preview.filter(p => p.errors).map((part, idx) => (
                    <li key={idx}>
                      {part.manufacturer} {part.part_number}: {part.errors?.join(', ')}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
