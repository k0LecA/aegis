-- 1. Roles Table
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL
);

-- 2. Profiles Table (Links to Supabase Auth users)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id),
    username TEXT
);

-- 3. Camera Groups
CREATE TABLE camera_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);

-- 4. Cameras
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES camera_groups(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    rtsp_url TEXT NOT NULL
);

-- 5. Recordings (Simple Index for MediaMTX files)
CREATE TABLE recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ
);

-- 6. Events (Motion/Alarms)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id) ON DELETE CASCADE,
    recording_id UUID REFERENCES recordings(id) ON DELETE SET NULL,
    event_type TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 7. Permissions (Access Control)
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    camera_id UUID REFERENCES cameras(id) ON DELETE CASCADE,
    access_level TEXT DEFAULT 'viewer'
);