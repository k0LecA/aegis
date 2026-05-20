// Shared formatting utilities used across multiple views.

export function formatDate(isoString: string | null): string {
  if (!isoString) return 'ACTIVE_STREAM'
  return new Date(isoString).toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).replace(',', '')
}

export function formatBytes(bytes: number | null): string {
  if (bytes === null || bytes === undefined) return 'N/A'
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

export function getStreamUrl(cameraName: string): string {
  const cleanedName = cameraName.toLowerCase().replace(/[^a-z0-9 _-]/g, '').replace(/\s+/g, '_')
  const token = localStorage.getItem('user-token') ?? ''
  return `http://127.0.0.1:8889/${cleanedName}?user=${token}`
}
