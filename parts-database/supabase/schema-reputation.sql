-- Reputation and verification system
-- Run this after the main schema

-- User profiles and reputation
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Display info
    display_name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,

    -- Reputation stats
    reputation_points INTEGER DEFAULT 0,
    parts_added INTEGER DEFAULT 0,
    parts_verified INTEGER DEFAULT 0,
    accuracy_score DECIMAL(5,2) DEFAULT 100.0, -- 0-100

    -- Badges
    badges JSONB DEFAULT '[]'::jsonb,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Part verifications
CREATE TABLE IF NOT EXISTS part_verifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    part_id VARCHAR(100) REFERENCES parts(part_id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id),

    -- Verification details
    verification_type VARCHAR(50), -- 'measurement', 'spec_sheet', 'usage', 'visual'
    verified_fields JSONB, -- Which fields were verified
    measurements JSONB, -- Actual measurements if available

    -- Verification metadata
    confidence_level VARCHAR(20), -- 'low', 'medium', 'high'
    notes TEXT,
    images TEXT[], -- URLs to verification images

    -- Status
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'disputed', 'superseded'

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_verifications_part ON part_verifications(part_id);
CREATE INDEX IF NOT EXISTS idx_verifications_user ON part_verifications(user_id);

-- Verification votes (community voting)
CREATE TABLE IF NOT EXISTS verification_votes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    verification_id UUID REFERENCES part_verifications(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id),

    vote INTEGER CHECK (vote IN (-1, 1)), -- -1 = disagree, 1 = agree
    notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(verification_id, user_id)
);

-- Reputation events log
CREATE TABLE IF NOT EXISTS reputation_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),

    event_type VARCHAR(50), -- 'part_added', 'verification', 'vote', 'badge_earned'
    points_change INTEGER,
    related_id UUID, -- part_id, verification_id, etc.
    description TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reputation_user ON reputation_events(user_id);

-- Badges definitions
CREATE TABLE IF NOT EXISTS badges (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url TEXT,
    requirements JSONB, -- Criteria for earning
    points_value INTEGER DEFAULT 0
);

-- Insert default badges
INSERT INTO badges (id, name, description, requirements, points_value) VALUES
('first_contribution', 'First Contribution', 'Added your first part to the database', '{"parts_added": 1}'::jsonb, 10),
('metric_master', 'Metric Master', 'Added 50+ metric parts', '{"parts_added": 50, "thread_type": "metric"}'::jsonb, 100),
('imperial_expert', 'Imperial Expert', 'Added 50+ imperial parts', '{"parts_added": 50, "thread_type": "imperial"}'::jsonb, 100),
('verifier', 'Verifier', 'Verified 100 parts', '{"parts_verified": 100}'::jsonb, 200),
('trusted_source', 'Trusted Source', '95%+ accuracy score with 20+ verifications', '{"accuracy_score": 95, "parts_verified": 20}'::jsonb, 300),
('community_leader', 'Community Leader', '1000+ reputation points', '{"reputation_points": 1000}'::jsonb, 500)
ON CONFLICT (id) DO NOTHING;

-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE part_verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_votes ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Profiles are viewable by everyone" ON user_profiles FOR SELECT USING (true);
CREATE POLICY "Users can update own profile" ON user_profiles FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Verifications are viewable by everyone" ON part_verifications FOR SELECT USING (true);
CREATE POLICY "Authenticated users can verify" ON part_verifications FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Votes are viewable by everyone" ON verification_votes FOR SELECT USING (true);
CREATE POLICY "Authenticated users can vote" ON verification_votes FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Function to update reputation
CREATE OR REPLACE FUNCTION update_user_reputation()
RETURNS TRIGGER AS $$
BEGIN
    -- Update user profile stats based on the event
    IF NEW.event_type = 'part_added' THEN
        UPDATE user_profiles
        SET
            parts_added = parts_added + 1,
            reputation_points = reputation_points + NEW.points_change
        WHERE user_id = NEW.user_id;
    ELSIF NEW.event_type = 'verification' THEN
        UPDATE user_profiles
        SET
            parts_verified = parts_verified + 1,
            reputation_points = reputation_points + NEW.points_change
        WHERE user_id = NEW.user_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update reputation
CREATE TRIGGER reputation_update_trigger
    AFTER INSERT ON reputation_events
    FOR EACH ROW
    EXECUTE FUNCTION update_user_reputation();

-- Function to calculate part verification level
CREATE OR REPLACE FUNCTION get_part_verification_level(p_part_id VARCHAR)
RETURNS TEXT AS $$
DECLARE
    verification_count INTEGER;
    avg_confidence NUMERIC;
BEGIN
    SELECT
        COUNT(*),
        AVG(CASE confidence_level
            WHEN 'high' THEN 3
            WHEN 'medium' THEN 2
            WHEN 'low' THEN 1
            ELSE 0
        END)
    INTO verification_count, avg_confidence
    FROM part_verifications
    WHERE part_id = p_part_id AND status = 'active';

    IF verification_count >= 5 AND avg_confidence >= 2.5 THEN
        RETURN 'verified';
    ELSIF verification_count >= 2 THEN
        RETURN 'community_verified';
    ELSE
        RETURN 'unverified';
    END IF;
END;
$$ LANGUAGE plpgsql;
