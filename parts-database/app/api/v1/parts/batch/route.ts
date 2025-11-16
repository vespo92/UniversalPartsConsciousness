import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'

// POST /api/v1/parts/batch - Batch import parts
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    if (!Array.isArray(body.parts)) {
      return NextResponse.json(
        { success: false, error: 'Body must contain "parts" array' },
        { status: 400 }
      )
    }

    if (body.parts.length === 0) {
      return NextResponse.json(
        { success: false, error: 'Parts array is empty' },
        { status: 400 }
      )
    }

    if (body.parts.length > 1000) {
      return NextResponse.json(
        { success: false, error: 'Maximum 1000 parts per batch' },
        { status: 400 }
      )
    }

    // Transform and validate parts
    const parts = body.parts.map((p: any) => {
      if (!p.manufacturer || !p.part_number || !p.category) {
        throw new Error('Missing required fields in part')
      }

      return {
        part_id: p.part_id || `${p.manufacturer}-${p.part_number}`.replace(/\s/g, '-'),
        manufacturer: p.manufacturer,
        part_number: p.part_number,
        category: p.category,
        subcategory: p.subcategory || null,
        thread_id: p.thread_id || null,
        length: p.length || null,
        material_grade: p.material_grade || null,
        tensile_strength: p.tensile_strength || null,
        yield_strength: p.yield_strength || null,
        data_source: p.data_source || 'api_batch',
        verification_status: 'unverified',
        full_specs: p.full_specs || {},
      }
    })

    const { data, error } = await supabase
      .from('parts')
      .insert(parts)
      .select()

    if (error) throw error

    return NextResponse.json({
      success: true,
      data: {
        imported: data?.length || 0,
        parts: data,
      },
    }, { status: 201 })
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    )
  }
}
