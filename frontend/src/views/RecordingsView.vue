<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

interface Camera {
  id: string
  name: string
  rtsp_url: string
}

interface Recording {
  id: string
  camera_id: string
  file_path: string
  started_at: string
  ended_at: string | null
  size_bytes: number | null
  created_at: string
}

const recordings = ref<Recording[]>([])
const cameras = ref<Camera[]>([])
const cameraMap = ref<Record<string, string>>({})

const selectedCameraId = ref<string>('ALL')
const filterDate = ref<string>('')

onMounted(async () => {
  try {
    // Fetch cameras
    const camRes = await fetch('/api/cameras')
    if (camRes.ok) {
      cameras.value = await camRes.json()
      cameras.value.forEach(c => {
        cameraMap.value[c.id] = c.name
      })
    }

    // Fetch recordings
    const recRes = await fetch('/api/recordings')
    if (recRes.ok) {
      recordings.value = await recRes.json()
    }
  } catch (error) {
    console.error('Failed to load recordings view dependencies:', error)
  }
})

const filteredRecordings = computed(() => {
  return recordings.value.filter(rec => {
    const matchesCamera = selectedCameraId.value === 'ALL' || rec.camera_id === selectedCameraId.value
    let matchesDate = true
    if (filterDate.value) {
      const recDateStr = new Date(rec.started_at).toISOString().split('T')[0]
      matchesDate = recDateStr === filterDate.value
    }
    return matchesCamera && matchesDate
  })
})

const deleteRecord = async (id: string) => {
  try {
    const res = await fetch(`/api/recordings/${id}`, { method: 'DELETE' })
    if (res.ok) {
      recordings.value = recordings.value.filter(r => r.id !== id)
    }
  } catch (error) {
    console.error('Failed to delete recording:', error)
  }
}

const downloadRecord = (id: string) => {
  window.open(`/api/recordings/${id}/download`, '_blank')
}

const formatBytes = (bytes: number | null) => {
  if (bytes === null || bytes === undefined) return 'N/A'
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (isoString: string | null) => {
  if (!isoString) return 'ACTIVE_STREAM'
  const date = new Date(isoString)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).replace(',', '')
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto">
    <!-- Header Section -->
    <div class="mb-10 flex flex-col md:flex-row md:items-end justify-between border-b border-[var(--s-line)] pb-6 gap-4">
      <div>
        <h2 class="text-3xl font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-tighter">
          Archived Segment Logs
        </h2>
        <p class="text-[var(--s-mid)] font-terminal text-[10px] uppercase tracking-[0.2em] mt-1">
          Sector Archives // Total Segments: {{ filteredRecordings.length }}
        </p>
      </div>
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Storage.Status</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">ONLINE // NORMAL</span>
      </div>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-8 p-4 bg-[var(--s-bg2)] border border-[var(--s-line)]">
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Filter Node</label>
        <select 
          v-model="selectedCameraId"
          class="bg-[var(--s-bg)] border border-[var(--s-line)] p-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer"
        >
          <option value="ALL">ALL NODES</option>
          <option v-for="cam in cameras" :key="cam.id" :value="cam.id">
            {{ cam.name }}
          </option>
        </select>
      </div>

      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Select Date</label>
        <input 
          v-model="filterDate"
          type="date"
          class="bg-[var(--s-bg)] border border-[var(--s-line)] p-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer color-scheme-dark"
        />
      </div>

      <div v-if="selectedCameraId !== 'ALL' || filterDate" class="flex flex-col justify-end">
        <button 
          @click="selectedCameraId = 'ALL'; filterDate = ''"
          class="border border-[var(--s-line)] bg-transparent px-4 py-2 text-[9px] font-terminal text-[var(--s-mid)] hover:text-white hover:bg-[var(--s-bg3)] uppercase tracking-widest transition-colors cursor-pointer"
        >
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Recordings List -->
    <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] overflow-x-auto">
      <table class="w-full text-left border-collapse font-terminal text-xs">
        <thead>
          <tr class="border-b border-[var(--s-line2)] text-[var(--s-mid)] uppercase tracking-wider text-[10px] bg-[var(--s-bg3)]">
            <th class="p-4 font-semibold">Node</th>
            <th class="p-4 font-semibold">Started At</th>
            <th class="p-4 font-semibold">Ended At</th>
            <th class="p-4 font-semibold">File Size</th>
            <th class="p-4 font-semibold">File Path</th>
            <th class="p-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="rec in filteredRecordings" 
            :key="rec.id" 
            class="border-b border-[var(--s-line)] hover:bg-[var(--s-bg3)] transition-colors"
          >
            <td class="p-4 font-bold text-[var(--s-white)] uppercase">
              {{ cameraMap[rec.camera_id] || 'UNKNOWN_NODE' }}
            </td>
            <td class="p-4 text-[var(--s-mid)]">
              {{ formatDate(rec.started_at) }}
            </td>
            <td class="p-4 text-[var(--s-mid)]">
              {{ formatDate(rec.ended_at) }}
            </td>
            <td class="p-4 text-[var(--s-mid)]">
              {{ formatBytes(rec.size_bytes) }}
            </td>
            <td class="p-4 text-[var(--s-dim)] font-terminal truncate max-w-xs" :title="rec.file_path">
              {{ rec.file_path }}
            </td>
            <td class="p-4 text-right flex justify-end gap-3">
              <button 
                @click="downloadRecord(rec.id)"
                class="px-2 py-1 border border-[var(--s-line2)] text-[9px] font-semibold text-[var(--s-white)] hover:bg-white hover:text-black uppercase tracking-wider transition-colors cursor-pointer"
              >
                Download
              </button>
              <button 
                @click="deleteRecord(rec.id)"
                class="px-2 py-1 border border-red-950/40 text-[9px] font-semibold text-[var(--s-err)] hover:bg-red-950/30 uppercase tracking-wider transition-colors cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>
          
          <!-- Empty State -->
          <tr v-if="filteredRecordings.length === 0">
            <td colspan="6" class="p-12 text-center text-[var(--s-dim)] uppercase tracking-widest font-terminal text-[10px]">
              &gt; NO RECORDED SEGMENTS LOCATED IN SECTOR // SYSTEM IDLE
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Style date inputs for dark themes */
.color-scheme-dark {
  color-scheme: dark;
}
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}
.overflow-y-auto::-webkit-scrollbar-track {
  background: var(--s-bg);
}
.overflow-y-auto::-webkit-scrollbar-thumb {
  background: var(--s-line2);
}
.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: var(--s-mid);
}
</style>
