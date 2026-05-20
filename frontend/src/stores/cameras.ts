// Camera store — loads once, mutations update in-place.
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchCameras, createCamera, updateCamera, deleteCamera } from '@/api'
import type { Camera } from '@/types'

export const useCameraStore = defineStore('cameras', () => {
  const cameras     = ref<Camera[]>([])
  const initialized = ref(false)
  const loading     = ref(false)

  async function load(force = false) {
    if (initialized.value && !force) return
    loading.value = true
    try {
      cameras.value     = await fetchCameras()
      initialized.value = true
    } finally {
      loading.value = false
    }
  }

  async function add(data: Pick<Camera, 'name' | 'rtsp_url'>) {
    const created = await createCamera(data)
    cameras.value.push(created)
    return created
  }

  async function update(id: string, data: Partial<Pick<Camera, 'name' | 'rtsp_url'>>) {
    const updated = await updateCamera(id, data)
    const idx = cameras.value.findIndex(c => c.id === id)
    if (idx !== -1) cameras.value[idx] = { ...cameras.value[idx], ...updated }
  }

  async function remove(id: string) {
    await deleteCamera(id)
    cameras.value = cameras.value.filter(c => c.id !== id)
  }

  return { cameras, loading, initialized, load, add, update, remove }
})
