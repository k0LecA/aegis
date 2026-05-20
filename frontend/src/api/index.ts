// Centralised API layer — all fetch calls live here, nowhere else.
import type { Camera, Alert, Recording, MediaMTXConfig } from '@/types'

const BASE = '/api'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`)
  return res.json()
}

async function post<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`)
  return res.json()
}

async function put<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`PUT ${path} failed: ${res.status}`)
  return res.json()
}

async function patch<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(`PATCH ${path} failed: ${res.status}`)
  return res.json()
}

async function del(path: string): Promise<void> {
  const res = await fetch(`${BASE}${path}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`DELETE ${path} failed: ${res.status}`)
}

// --- Cameras ---
export const fetchCameras = (): Promise<Camera[]> => get('/cameras/')
export const createCamera = (data: Pick<Camera, 'name' | 'rtsp_url'>): Promise<Camera> =>
  post('/cameras/', data)
export const updateCamera = (id: string, data: Partial<Pick<Camera, 'name' | 'rtsp_url'>>): Promise<Camera> =>
  put(`/cameras/${id}`, data)
export const deleteCamera = (id: string): Promise<void> => del(`/cameras/${id}`)

// --- Recordings ---
export const fetchRecordings = (cameraId?: string): Promise<Recording[]> => {
  const q = cameraId ? `?camera_id=${cameraId}` : ''
  return get(`/recordings/${q}`)
}
export const deleteRecording = (id: string): Promise<void> => del(`/recordings/${id}`)
export const getDownloadUrl = (id: string): string => `${BASE}/recordings/${id}/download`

// --- Alerts ---
export const fetchAlerts = (): Promise<Alert[]> => get('/alerts/')
export const createAlert = (data: Pick<Alert, 'camera_id' | 'type' | 'resolved'>): Promise<Alert> =>
  post('/alerts/', data)
export const resolveAlert = (id: string): Promise<Alert> => patch(`/alerts/${id}/resolve`)

// --- Services (MediaMTX) ---
export const fetchServiceStatus = (): Promise<{ running: boolean }> =>
  get('/services/mediamtx/status')
export const toggleService = (): Promise<{ running: boolean }> =>
  post('/services/mediamtx/toggle')
export const restartService = (): Promise<{ running: boolean }> =>
  post('/services/mediamtx/restart')
export const fetchServiceConfig = (): Promise<MediaMTXConfig> =>
  get('/services/mediamtx/config')
export const saveServiceConfig = (config: MediaMTXConfig): Promise<unknown> =>
  post('/services/mediamtx/config', config)
export const fetchServiceLogs = (): Promise<{ logs: string[] }> =>
  get('/services/mediamtx/logs')
