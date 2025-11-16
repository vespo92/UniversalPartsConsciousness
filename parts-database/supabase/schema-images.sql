-- Image support for parts
-- Run this after the main schema

-- Part images table
CREATE TABLE IF NOT EXISTS part_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    part_id VARCHAR(100) REFERENCES parts(part_id) ON DELETE CASCADE,

    -- Image metadata
    image_url TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    thumbnail_url TEXT,

    -- Image details
    caption TEXT,
    image_type VARCHAR(50), -- 'product', 'dimension', 'installation', 'field_photo'
    is_primary BOOLEAN DEFAULT FALSE,

    -- Contributor tracking
    uploaded_by UUID REFERENCES auth.users(id),
    verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES auth.users(id),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_part_images_part ON part_images(part_id);
CREATE INDEX IF NOT EXISTS idx_part_images_type ON part_images(image_type);

-- Enable RLS
ALTER TABLE part_images ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Images are viewable by everyone" ON part_images FOR SELECT USING (true);
CREATE POLICY "Authenticated users can upload images" ON part_images FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Users can delete their own images" ON part_images FOR DELETE USING (uploaded_by = auth.uid());

-- Storage bucket setup (run in Supabase dashboard)
-- Go to Storage → Create bucket → 'part-images'
-- Enable public access for viewing
-- Set max file size to 5MB
