// Recordings store — load once, sync FS on first visit, mutations update in-place.
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchRecordings, deleteRecording, getDownloadUrl } from '@/api'
import type { Recording } from '@/types'

export const useRecordingStore = defineStore('recordings', () => {
  const recordings  = ref<Recording[]>([])
  const initialized = ref(false)
  const loading     = ref(false)

  async function load(force = false) {
    if (initialized.value && !force) return
    loading.value = true
    try {
      recordings.value  = await fetchRecordings()
      initialized.value = true
    } finally {
      loading.value = false
    }
  }

  async function remove(id: string) {
    await deleteRecording(id)
    recordings.value = recordings.value.filter(r => r.id !== id)
  }

  function download(id: string) {
    window.open(getDownloadUrl(id), '_blank')
  }

  return { recordings, loading, initialized, load, remove, download }
})
