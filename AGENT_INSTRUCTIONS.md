# AEGIS — AI Agent Continuation Instructions

> Last analysed: 2026-05-20  
> Repo: https://github.com/k0LecA/aegis  
> Branch: `main` (17 commits)

---

## 1. Project Overview

AEGIS is a **web-based IP-camera surveillance system**. The README describes an ambitious final state; the actual codebase is at an early/scaffolding stage. Treat the README as aspirational design documentation, not as a description of implemented functionality.

### Confirmed tech choices
| Layer | Technology |
|---|---|
| Backend language | Python 3.14 (verify actual version in Pipfile) |
| Backend framework | FastAPI (async) |
| Package manager | Pipenv |
| Database | **Supabase** (PostgreSQL — hosted, with built-in Auth, Storage, Realtime) |
| DB client | `supabase-py` (async) |
| Media server | MediaMTX |
| Video transcoding | FFmpeg |
| Frontend framework | Vue 3 + Vite |
| State management | Pinia |
| CSS | Tailwind CSS |

> **Note on Limbo files (14% of repo):** The repo language stats show significant Limbo/SQLite code. This is likely leftover scaffolding or a local dev experiment. **Supabase (PostgreSQL) is the authoritative data layer — do not use Limbo/SQLite for any new feature.**

### Declared directory layout (verify against actual files before writing code)
```
backend/
  app/
    api/          ← API endpoints (v1)
    core/         ← Config & Supabase client
    models/       ← Pydantic schemas (no ORM needed with Supabase)
    services/     ← Business logic / Supabase queries
    main.py       ← Entry point
  Pipfile
frontend/
  src/
    components/
    stores/
    views/
docs/
```

---

## 2. README Inconsistencies to be Aware Of

1. **Python version**: README says Python 3.14 (pre-release). Verify the actual version in `Pipfile` or `.python-version`.
2. **Database**: README never explicitly names a DB engine. **Use Supabase exclusively.** Ignore any Limbo/SQLite code for data persistence.
3. **Migrations**: No Alembic needed. Schema changes are made via the Supabase Dashboard SQL editor or `supabase/migrations/` if the Supabase CLI is set up.
4. **Auth**: README mentions "External Auth Bridge" as done. With Supabase, use **Supabase Auth** — do not build a custom JWT system from scratch. Verify whether the existing auth code wraps Supabase or is a separate JWT implementation; if the latter, replace it.
5. **Roadmap items marked done**: WebRTC integration, Archiving, Auth Bridge may be only partially scaffolded. Do not assume they work end-to-end.
6. **Entry point conflict**: Quick-start says `python -m run`, README structure shows `main.py`. Check both — `run.py` likely just calls `uvicorn app.main:app`.

---

## 3. Work Phases — Ordered Priority

### Phase 1 — Complete Backend CRUD  *(current priority)*
### Phase 2 — REST API layer
### Phase 3 — Frontend integration

---

## 4. Supabase Setup (prerequisite for all phases)

### 4.1 Required environment variables
Create `backend/.env` (and add to `.gitignore`):
```env
SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_SERVICE_KEY=<service_role key>   # backend only — never expose to frontend
SUPABASE_ANON_KEY=<anon key>              # safe for frontend
MEDIAMTX_API_URL=http://localhost:9997
RECORDINGS_DIR=/path/to/recordings
```

Frontend `frontend/.env`:
```env
VITE_SUPABASE_URL=https://<your-project>.supabase.co
VITE_SUPABASE_ANON_KEY=<anon key>
VITE_API_BASE_URL=http://localhost:8000
```

### 4.2 Supabase client singleton — `app/core/supabase.py`
```python
from supabase import create_client, Client
from app.core.config import settings

_client: Client | None = None

def get_supabase() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _client
```
Use `Depends(get_supabase)` in FastAPI routes — or import directly in services since the client is a singleton.

### 4.3 Config — `app/core/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    MEDIAMTX_API_URL: str = "http://localhost:9997"
    RECORDINGS_DIR: str = "./recordings"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 4.4 Supabase schema — create via Dashboard or CLI
Run in the Supabase SQL editor (or `supabase/migrations/`):

```sql
-- cameras
create table cameras (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  rtsp_url    text not null,
  location    text,
  is_active   boolean not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- recordings
create table recordings (
  id          uuid primary key default gen_random_uuid(),
  camera_id   uuid not null references cameras(id) on delete cascade,
  file_path   text not null,
  started_at  timestamptz not null,
  ended_at    timestamptz,
  size_bytes  bigint,
  created_at  timestamptz not null default now()
);

-- alerts (stub for motion detection roadmap item)
create table alerts (
  id           uuid primary key default gen_random_uuid(),
  camera_id    uuid not null references cameras(id) on delete cascade,
  triggered_at timestamptz not null default now(),
  type         text not null,        -- 'motion' | 'intruder'
  resolved     boolean not null default false
);

-- Row Level Security
alter table cameras   enable row level security;
alter table recordings enable row level security;
alter table alerts    enable row level security;

-- Allow service_role (backend) full access; restrict anon
create policy "service_role full access cameras"
  on cameras for all using (auth.role() = 'service_role');
create policy "service_role full access recordings"
  on recordings for all using (auth.role() = 'service_role');
create policy "service_role full access alerts"
  on alerts for all using (auth.role() = 'service_role');
```

> **Users**: Do NOT create a custom users table. Use Supabase Auth (`auth.users`) directly. If you need extra profile fields, create a `profiles` table that references `auth.users.id`.

---

## 5. Phase 1: Complete Backend CRUD

### 5.1 Before writing any code — read these files first
```
backend/Pipfile                    # confirm supabase-py is present
backend/app/core/config.py         # env var names already in use
backend/app/models/                # existing Pydantic schemas
backend/app/services/              # existing service functions
backend/app/main.py                # registered routers
```

### 5.2 Pydantic schemas — `app/models/<entity>.py`
No ORM classes needed. Only Pydantic v2 schemas:

```python
# app/models/camera.py
from pydantic import BaseModel, UUID4
from datetime import datetime

class CameraBase(BaseModel):
    name: str
    rtsp_url: str
    location: str | None = None
    is_active: bool = True

class CameraCreate(CameraBase):
    pass

class CameraUpdate(BaseModel):
    name: str | None = None
    rtsp_url: str | None = None
    location: str | None = None
    is_active: bool | None = None

class CameraRead(CameraBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
```

Repeat the same pattern for `Recording`, `Alert`.

### 5.3 Service layer — `app/services/<entity>_service.py`

All Supabase queries go here. Keep routers thin.

```python
# app/services/camera_service.py
from supabase import Client
from app.models.camera import CameraCreate, CameraUpdate

TABLE = "cameras"

async def create_camera(sb: Client, data: CameraCreate) -> dict:
    res = sb.table(TABLE).insert(data.model_dump()).execute()
    return res.data[0]

async def get_camera(sb: Client, camera_id: str) -> dict | None:
    res = sb.table(TABLE).select("*").eq("id", camera_id).maybe_single().execute()
    return res.data

async def list_cameras(sb: Client, is_active: bool | None = None,
                       skip: int = 0, limit: int = 50) -> list[dict]:
    q = sb.table(TABLE).select("*").range(skip, skip + limit - 1)
    if is_active is not None:
        q = q.eq("is_active", is_active)
    return q.execute().data

async def update_camera(sb: Client, camera_id: str, data: CameraUpdate) -> dict | None:
    payload = {k: v for k, v in data.model_dump().items() if v is not None}
    payload["updated_at"] = "now()"
    res = sb.table(TABLE).update(payload).eq("id", camera_id).execute()
    return res.data[0] if res.data else None

async def delete_camera(sb: Client, camera_id: str) -> bool:
    res = sb.table(TABLE).delete().eq("id", camera_id).execute()
    return len(res.data) > 0
```

Implement matching services for `recording_service.py` and `alert_service.py`.

### 5.4 CRUD checklist per entity

For each of `Camera`, `Recording`, `Alert`:
- [ ] SQL table created in Supabase (§4.4)
- [ ] Pydantic schemas: `Base`, `Create`, `Update`, `Read`
- [ ] Service functions: `create`, `get`, `list`, `update`, `delete`
- [ ] Router with endpoints wired to service (see Phase 2)
- [ ] Manual test via `/docs` or `curl`

### 5.5 Coding conventions
- `supabase-py` is synchronous by default; use `asyncio.to_thread()` or the async client if available in the installed version — check Pipfile for the version
- Raise `HTTPException(404)` when `get_*` returns `None`
- Raise `HTTPException(400)` for Supabase constraint errors (wrap in try/except and check `res.error`)
- Keep all Supabase calls inside `services/` — never call `sb.table()` directly in a router

---

## 6. Phase 2: REST API Layer

Do this **after** Phase 1 services are complete and manually tested.

### 6.1 API structure
```
app/api/
  v1/
    __init__.py
    cameras.py
    recordings.py
    alerts.py
  router.py      ← aggregates all v1 routers
```

Register in `main.py`:
```python
from app.api.router import api_router
app.include_router(api_router, prefix="/api/v1")
```

### 6.2 Endpoint spec

**Cameras**
```
GET    /api/v1/cameras              → list (query: is_active, skip, limit)
POST   /api/v1/cameras              → create
GET    /api/v1/cameras/{id}         → read one
PATCH  /api/v1/cameras/{id}         → update
DELETE /api/v1/cameras/{id}         → delete
GET    /api/v1/cameras/{id}/stream  → return MediaMTX WebRTC URL + auth token
```

**Recordings**
```
GET    /api/v1/recordings           → list (query: camera_id, from, to, skip, limit)
GET    /api/v1/recordings/{id}      → read one
DELETE /api/v1/recordings/{id}      → delete DB record + file from disk
GET    /api/v1/recordings/{id}/download → StreamingResponse of the file
```

**Alerts**
```
GET    /api/v1/alerts               → list (query: camera_id, resolved)
PATCH  /api/v1/alerts/{id}/resolve  → mark resolved
```

### 6.3 Auth — use Supabase Auth, not custom JWT

The backend verifies the **Supabase JWT** from the `Authorization: Bearer <token>` header.

```python
# app/core/auth.py
from fastapi import Depends, HTTPException, Header
from app.core.supabase import get_supabase

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401)
    token = authorization.removeprefix("Bearer ")
    sb = get_supabase()
    try:
        user = sb.auth.get_user(token)
        return user.user
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
```

Protect all camera/recording endpoints: `Depends(get_current_user)`.

**Frontend auth flow** (Supabase JS SDK):
```typescript
const { data, error } = await supabase.auth.signInWithPassword({ email, password })
// data.session.access_token → send as Bearer token to FastAPI
```

MediaMTX auth bridge: FastAPI exposes a `POST /internal/mediamtx/auth` webhook. MediaMTX calls this with the stream path + token; FastAPI verifies the token via `sb.auth.get_user(token)` and returns 200/403. Check `app/services/` to see if this already exists before rebuilding.

### 6.4 API docs
```python
app = FastAPI(
    title="AEGIS API",
    version="1.0.0",
    description="Surveillance system — FastAPI + Supabase"
)
```
Add `response_model=CameraRead` (etc.) to every route so `/docs` has clean schemas.

### 6.5 CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 7. Phase 3: Frontend Integration

Do this **after** Phase 2 API is stable.

### 7.1 Before writing Vue code — read these files
```
frontend/package.json       # confirm @supabase/supabase-js is present
frontend/src/main.ts        # plugin registration
frontend/src/stores/        # existing Pinia stores
frontend/src/views/         # existing pages
```

### 7.2 Supabase JS client — `src/lib/supabase.ts`
```typescript
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
)
```

### 7.3 API client — `src/api/client.ts`
```typescript
import { supabase } from '@/lib/supabase'

const BASE = import.meta.env.VITE_API_BASE_URL

async function authFetch(path: string, init: RequestInit = {}) {
  const { data: { session } } = await supabase.auth.getSession()
  return fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session?.access_token}`,
      ...init.headers,
    },
  })
}

export const api = {
  cameras: {
    list: (params?: Record<string, string>) =>
      authFetch(`/api/v1/cameras?${new URLSearchParams(params)}`).then(r => r.json()),
    create: (body: unknown) =>
      authFetch('/api/v1/cameras', { method: 'POST', body: JSON.stringify(body) }).then(r => r.json()),
    update: (id: string, body: unknown) =>
      authFetch(`/api/v1/cameras/${id}`, { method: 'PATCH', body: JSON.stringify(body) }).then(r => r.json()),
    delete: (id: string) =>
      authFetch(`/api/v1/cameras/${id}`, { method: 'DELETE' }),
    stream: (id: string) =>
      authFetch(`/api/v1/cameras/${id}/stream`).then(r => r.json()),
  },
  recordings: {
    list: (params?: Record<string, string>) =>
      authFetch(`/api/v1/recordings?${new URLSearchParams(params)}`).then(r => r.json()),
    delete: (id: string) =>
      authFetch(`/api/v1/recordings/${id}`, { method: 'DELETE' }),
  },
}
```

### 7.4 Pinia stores
- `useAuthStore` — wraps `supabase.auth`, exposes `user`, `signIn()`, `signOut()`; persists session automatically via Supabase SDK
- `useCameraStore` — camera list, selected camera, CRUD actions via `api.cameras`
- `useRecordingStore` — recording list with camera_id + date filters

### 7.5 Views
| View | Route | Description |
|---|---|---|
| `LoginView` | `/login` | Supabase email/password form |
| `DashboardView` | `/` | Multi-stream WebRTC grid |
| `CameraManagerView` | `/cameras` | CRUD table |
| `RecordingsView` | `/recordings` | List with camera + date filters |
| `SettingsView` | `/settings` | User profile |

Router guard: redirect to `/login` if `supabase.auth.getSession()` returns null.

### 7.6 UI/UX direction
- "Aperture Science / 1970s brutalist tech aesthetic" — dark, industrial, monospace
- Vue 3 `<script setup>` + Composition API throughout
- Tailwind CSS only — no UI component library unless already in `package.json`

---

## 8. Cross-cutting Concerns

### Error handling
- Backend: catch `supabase` errors, return `HTTPException` with meaningful detail
- Frontend: `useError()` composable mapping HTTP status → user message; Supabase auth errors surface via `error.message`

### Realtime (optional enhancement)
Supabase Realtime can push camera/alert changes to the dashboard without polling:
```typescript
supabase.channel('alerts')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'alerts' }, payload => {
    alertStore.add(payload.new)
  })
  .subscribe()
```
Add this only after basic CRUD + API are working.

### File storage for recordings
Supabase Storage can replace local disk for recordings. For Phase 1, keep local disk (`RECORDINGS_DIR`). In a later phase: upload segments to a Supabase Storage bucket and store the public/signed URL in `recordings.file_path`.

---

## 9. Quick-start Verification

```bash
# Backend
cd backend
pipenv install           # confirm supabase-py, pydantic-settings are in Pipfile
cp .env.example .env     # fill in SUPABASE_URL + SUPABASE_SERVICE_KEY
pipenv run python -m run # or: uvicorn app.main:app --reload
# Verify: http://localhost:8000/docs

# Frontend
cd frontend
npm install              # confirm @supabase/supabase-js in package.json
cp .env.example .env     # fill in VITE_SUPABASE_URL + VITE_SUPABASE_ANON_KEY
npm run dev
# Verify: http://localhost:5173
```

---

## 10. Commit Convention

```
feat(cameras): add Supabase CRUD service and Pydantic schemas
feat(api): add cameras router with auth guard
feat(auth): integrate Supabase JWT verification middleware
feat(frontend): implement useAuthStore with Supabase session
fix(recordings): cascade delete file on DB record removal
chore: add supabase-py to Pipfile
```

---

## 11. Definition of Done per Phase

**Phase 1 (CRUD) done when:**
- Tables exist in Supabase with RLS enabled
- All 3 entities (Camera, Recording, Alert) have Pydantic schemas + service functions
- Each service function tested manually against live Supabase project

**Phase 2 (API) done when:**
- All endpoints in §6.2 return correct status codes
- `/docs` renders complete request/response schemas
- Supabase JWT auth blocks unauthenticated requests (test with invalid token → 401)
- CORS allows `localhost:5173`

**Phase 3 (Frontend) done when:**
- Login/logout works via Supabase Auth
- Dashboard loads and displays at least one camera's WebRTC stream
- Camera CRUD is fully operable from the UI
- Recordings list loads; individual items can be deleted
