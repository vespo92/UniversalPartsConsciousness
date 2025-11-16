'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

interface ImageUploadProps {
  partId: string
  onUploadComplete?: () => void
}

export default function ImageUpload({ partId, onUploadComplete }: ImageUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [dragActive, setDragActive] = useState(false)

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
      uploadImage(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      uploadImage(e.target.files[0])
    }
  }

  const uploadImage = async (file: File) => {
    // Validate file
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('Image must be smaller than 5MB')
      return
    }

    setUploading(true)
    setError('')

    try {
      // Create unique filename
      const fileExt = file.name.split('.').pop()
      const fileName = `${partId}-${Date.now()}.${fileExt}`
      const filePath = `${partId}/${fileName}`

      // Upload to Supabase Storage
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from('part-images')
        .upload(filePath, file)

      if (uploadError) throw uploadError

      // Get public URL
      const { data: urlData } = supabase.storage
        .from('part-images')
        .getPublicUrl(filePath)

      // Save to database
      const { error: dbError } = await supabase
        .from('part_images')
        .insert({
          part_id: partId,
          image_url: urlData.publicUrl,
          storage_path: filePath,
          image_type: 'product',
        })

      if (dbError) throw dbError

      if (onUploadComplete) onUploadComplete()
    } catch (err: any) {
      console.error('Upload error:', err)
      setError(err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="mt-4">
      <label className="block text-sm font-medium text-slate-700 mb-2">
        Part Images
      </label>

      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
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
          <label htmlFor="image-upload" className="cursor-pointer">
            <span className="text-blue-600 hover:text-blue-700 font-medium">
              {uploading ? 'Uploading...' : 'Upload an image'}
            </span>
            <input
              id="image-upload"
              name="image-upload"
              type="file"
              accept="image/*"
              disabled={uploading}
              className="sr-only"
              onChange={handleFileInput}
            />
          </label>
          <p className="text-slate-500"> or drag and drop</p>
        </div>
        <p className="mt-2 text-xs text-slate-500">
          PNG, JPG, GIF up to 5MB
        </p>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
