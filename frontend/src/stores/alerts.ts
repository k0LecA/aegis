// Alerts store — load once, optimistic resolve and create mutations.
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchAlerts, createAlert, resolveAlert } from '@/api'
import type { Alert } from '@/types'

export const useAlertStore = defineStore('alerts', () => {
  const alerts      = ref<Alert[]>([])
  const initialized = ref(false)
  const loading     = ref(false)

  const unresolvedCount = computed(() => alerts.value.filter(a => !a.resolved).length)

  async function load(force = false) {
    if (initialized.value && !force) return
    loading.value = true
    try {
      alerts.value      = await fetchAlerts()
      initialized.value = true
    } finally {
      loading.value = false
    }
  }

  async function resolve(id: string) {
    await resolveAlert(id)
    // Optimistic update — no full refetch
    const idx = alerts.value.findIndex(a => a.id === id)
    if (idx !== -1) alerts.value[idx].resolved = true
  }

  async function simulate(cameraId: string) {
    const type    = Math.random() > 0.5 ? 'motion' : 'intruder'
    const created = await createAlert({ camera_id: cameraId, type, resolved: false })
    alerts.value.push(created)
    return created
  }

  return { alerts, loading, initialized, unresolvedCount, load, resolve, simulate }
})
