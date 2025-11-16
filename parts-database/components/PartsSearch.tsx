'use client'

import { useState, useEffect } from 'react'
import { supabase, type Part } from '@/lib/supabase'
import ModelViewer from '@/components/ModelViewer'

export default function PartsSearch() {
  const [searchQuery, setSearchQuery] = useState('')
  const [category, setCategory] = useState('')
  const [results, setResults] = useState<Part[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedPart, setSelectedPart] = useState<Part | null>(null)
  const [cadData, setCadData] = useState<any>(null)

  const fetchCadData = async (partId: string) => {
    try {
      const { data, error } = await supabase
        .from('part_cad_files')
        .select('*')
        .eq('part_id', partId)
        .single()

      if (!error && data) {
        setCadData(data)
      } else {
        setCadData(null)
      }
    } catch (error) {
      console.error('Error fetching CAD data:', error)
      setCadData(null)
    }
  }

  const searchParts = async () => {
    setLoading(true)
    try {
      let query = supabase.from('parts').select('*')

      if (searchQuery) {
        query = query.or(`part_number.ilike.%${searchQuery}%,manufacturer.ilike.%${searchQuery}%,standard_designation.ilike.%${searchQuery}%`)
      }

      if (category) {
        query = query.eq('category', category)
      }

      const { data, error } = await query.limit(50)

      if (error) throw error
      setResults(data || [])
    } catch (error) {
      console.error('Error searching parts:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      searchParts()
    }, 300)

    return () => clearTimeout(timer)
  }, [searchQuery, category])

  return (
    <div className="space-y-6">
      {/* Search Form */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Search Parts
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Enter part number, manufacturer, or thread size (e.g., M3, M5x0.8)"
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Categories</option>
              <option value="fastener">Fasteners</option>
              <option value="bearing">Bearings</option>
              <option value="seal">Seals</option>
              <option value="hardware">Hardware</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-slate-600">Searching...</p>
        </div>
      ) : results.length > 0 ? (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-slate-900">
            {results.length} {results.length === 1 ? 'Result' : 'Results'}
          </h3>
          <div className="grid gap-3">
            {results.map((part) => (
              <div
                key={part.part_id}
                onClick={() => {
                  const newPart = selectedPart?.part_id === part.part_id ? null : part
                  setSelectedPart(newPart)
                  if (newPart) {
                    fetchCadData(newPart.part_id)
                  } else {
                    setCadData(null)
                  }
                }}
                className="border border-slate-200 rounded-lg p-4 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer bg-white"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-semibold text-slate-900">
                      {part.part_number || part.part_id}
                    </h4>
                    {part.manufacturer && (
                      <p className="text-sm text-slate-600">{part.manufacturer}</p>
                    )}
                    <div className="mt-2 flex flex-wrap gap-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {part.category}
                      </span>
                      {part.thread_id && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {part.thread_id}
                        </span>
                      )}
                      {part.length && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          {part.length}mm
                        </span>
                      )}
                      {part.material_grade && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                          {part.material_grade}
                        </span>
                      )}
                    </div>
                  </div>
                  <button className="text-blue-600 hover:text-blue-700">
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>

                {selectedPart?.part_id === part.part_id && (
                  <div className="mt-4 pt-4 border-t border-slate-200 space-y-4">
                    {/* 3D Model Viewer */}
                    {cadData && (cadData.stl_url || cadData.step_url) && (
                      <div>
                        <h5 className="font-medium text-slate-900 mb-3">3D Model</h5>
                        <ModelViewer
                          modelUrl={cadData.stl_url || cadData.step_url}
                          modelType={cadData.stl_url ? 'stl' : 'step'}
                          partName={part.part_number || part.part_id}
                        />
                      </div>
                    )}

                    <h5 className="font-medium text-slate-900">Specifications</h5>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      {part.tensile_strength && (
                        <div>
                          <span className="text-slate-600">Tensile Strength:</span>
                          <span className="ml-2 font-medium">{part.tensile_strength} MPa</span>
                        </div>
                      )}
                      {part.yield_strength && (
                        <div>
                          <span className="text-slate-600">Yield Strength:</span>
                          <span className="ml-2 font-medium">{part.yield_strength} MPa</span>
                        </div>
                      )}
                      {part.proof_load && (
                        <div>
                          <span className="text-slate-600">Proof Load:</span>
                          <span className="ml-2 font-medium">{part.proof_load} kN</span>
                        </div>
                      )}
                      <div>
                        <span className="text-slate-600">Status:</span>
                        <span className="ml-2 font-medium capitalize">{part.verification_status}</span>
                      </div>
                    </div>
                    {part.full_specs && (
                      <details className="mt-3">
                        <summary className="cursor-pointer text-sm font-medium text-blue-600 hover:text-blue-700">
                          View Full Specifications
                        </summary>
                        <pre className="mt-2 p-3 bg-slate-50 rounded text-xs overflow-x-auto">
                          {JSON.stringify(part.full_specs, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : searchQuery || category ? (
        <div className="text-center py-8 text-slate-600">
          No parts found. Try adjusting your search criteria.
        </div>
      ) : (
        <div className="text-center py-8 text-slate-600">
          Enter search criteria to find parts
        </div>
      )}
    </div>
  )
}
