// Services store — polled every 2s while the view is mounted, cached between visits.
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  fetchServiceStatus,
  toggleService,
  restartService,
  fetchServiceConfig,
  saveServiceConfig,
  fetchServiceLogs,
} from '@/api'
import type { MediaMTXConfig } from '@/types'

const DEFAULT_CONFIG: MediaMTXConfig = {
  record: false,
  recordFormat: 'fmp4',
  recordPath: './recordings/%path/%v_%Y-%m-%d_%H-%M-%S_%f',
  recordSegmentDuration: '1h',
}

export const useServiceStore = defineStore('services', () => {
  const isRunning   = ref(false)
  const logs        = ref<string[]>([])
  const config      = ref<MediaMTXConfig>({ ...DEFAULT_CONFIG })
  const isSaving    = ref(false)
  const saveSuccess = ref(false)
  const initialized = ref(false)

  async function init() {
    if (initialized.value) return
    await Promise.all([refreshStatus(), loadConfig(), refreshLogs()])
    initialized.value = true
  }

  async function refreshStatus() {
    try {
      const data   = await fetchServiceStatus()
      isRunning.value = data.running
    } catch (err) { console.error('Status error:', err) }
  }

  async function loadConfig() {
    try {
      config.value = await fetchServiceConfig()
    } catch (err) { console.error('Config load error:', err) }
  }

  async function refreshLogs() {
    try {
      const data = await fetchServiceLogs()
      logs.value = data.logs
    } catch (err) { console.error('Logs error:', err) }
  }

  async function toggle() {
    const data = await toggleService()
    isRunning.value = data.running
    await refreshLogs()
  }

  async function restart() {
    const data = await restartService()
    isRunning.value = data.running
    await refreshLogs()
  }

  async function saveConfig(newConfig: MediaMTXConfig) {
    isSaving.value    = true
    saveSuccess.value = false
    try {
      await saveServiceConfig(newConfig)
      config.value      = { ...newConfig }
      saveSuccess.value = true
      setTimeout(() => { saveSuccess.value = false }, 3000)
      await refreshLogs()
    } finally {
      isSaving.value = false
    }
  }

  return {
    isRunning, logs, config, isSaving, saveSuccess, initialized,
    init, refreshStatus, refreshLogs, toggle, restart, saveConfig,
  }
})
