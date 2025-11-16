import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Types for our database
export interface Part {
  part_id: string
  universal_id?: string
  manufacturer?: string
  part_number?: string
  standard_designation?: string
  category: string
  subcategory?: string
  thread_id?: string
  thread_length?: number
  length?: number
  length_tolerance_plus?: number
  length_tolerance_minus?: number
  material_grade?: string
  material_spec?: any
  tensile_strength?: number
  yield_strength?: number
  proof_load?: number
  hardness?: string
  data_source?: string
  verification_status?: string
  last_verified?: string
  full_specs: any
}

export interface ThreadSpecification {
  thread_id: string
  thread_standard: string
  nominal_diameter: number
  pitch: number
  major_diameter_min: number
  major_diameter_max: number
  pitch_diameter_min: number
  pitch_diameter_max: number
  minor_diameter_min: number
  minor_diameter_max: number
  thread_angle?: number
  thread_class?: string
  tolerance_position?: string
  tolerance_grade?: number
  thread_direction?: string
  min_engagement_ratio?: number
  max_engagement_ratio?: number
  thread_runout?: number
}

export interface FastenerHead {
  part_id: string
  head_type?: string
  head_diameter?: number
  head_diameter_tolerance?: number
  head_height?: number
  head_height_tolerance?: number
  drive_type?: string
  drive_size?: string
  drive_depth?: number
  bearing_surface_diameter?: number
  washer_integrated?: boolean
}
