import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'

// GET /api/v1/parts - List parts with filtering
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams

  // Query parameters
  const category = searchParams.get('category')
  const manufacturer = searchParams.get('manufacturer')
  const thread = searchParams.get('thread')
  const search = searchParams.get('search')
  const limit = parseInt(searchParams.get('limit') || '50')
  const offset = parseInt(searchParams.get('offset') || '0')

  try {
    let query = supabase.from('parts').select('*', { count: 'exact' })

    // Apply filters
    if (category) query = query.eq('category', category)
    if (manufacturer) query = query.ilike('manufacturer', `%${manufacturer}%`)
    if (thread) query = query.eq('thread_id', thread)
    if (search) {
      query = query.or(`part_number.ilike.%${search}%,manufacturer.ilike.%${search}%,standard_designation.ilike.%${search}%`)
    }

    // Pagination
    query = query.range(offset, offset + limit - 1)

    const { data, error, count } = await query

    if (error) throw error

    return NextResponse.json({
      success: true,
      data,
      pagination: {
        total: count,
        limit,
        offset,
        hasMore: count ? offset + limit < count : false,
      },
    })
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    )
  }
}

// POST /api/v1/parts - Create new part
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validate required fields
    if (!body.manufacturer || !body.part_number || !body.category) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields: manufacturer, part_number, category' },
        { status: 400 }
      )
    }

    // Generate part_id if not provided
    const part_id = body.part_id || `${body.manufacturer}-${body.part_number}`.replace(/\s/g, '-')

    const part = {
      part_id,
      manufacturer: body.manufacturer,
      part_number: body.part_number,
      category: body.category,
      subcategory: body.subcategory || null,
      thread_id: body.thread_id || null,
      length: body.length || null,
      material_grade: body.material_grade || null,
      tensile_strength: body.tensile_strength || null,
      yield_strength: body.yield_strength || null,
      data_source: body.data_source || 'api',
      verification_status: 'unverified',
      full_specs: body.full_specs || {},
    }

    const { data, error } = await supabase
      .from('parts')
      .insert([part])
      .select()

    if (error) throw error

    return NextResponse.json({
      success: true,
      data: data[0],
    }, { status: 201 })
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    )
  }
}
