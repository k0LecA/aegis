// All shared TypeScript interfaces for AEGIS frontend

export interface Camera {
  id: string
  name: string
  rtsp_url: string
  status?: 'online' | 'offline' | 'warning'
}

export interface Alert {
  id: string
  camera_id: string
  type: string          // 'motion' | 'intruder'
  resolved: boolean
  triggered_at: string
}

export interface Recording {
  id: string
  camera_id: string
  file_path: string
  started_at: string
  ended_at: string | null
  size_bytes: number | null
  created_at: string
}

export interface MediaMTXConfig {
  record: boolean
  recordFormat: string
  recordPath: string
  recordSegmentDuration: string
}
