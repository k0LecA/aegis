<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Camera {
  id: string
  name: string
  rtsp_url: string
}

interface Alert {
  id: string
  camera_id: string
  type: string
  resolved: boolean
}

interface Recording {
  id: string
  camera_id: string
  file_path: string
}

const cameras = ref<Camera[]>([])
const alerts = ref<Alert[]>([])
const recordings = ref<Recording[]>([])

const selectedCameraId = ref('')
const isLoading = ref(true)

// Dynamic Timestamp
const currentTime = ref('')
let timeInterval: ReturnType<typeof setInterval> | null = null

const updateTime = () => {
  const now = new Date()
  const yyyy = now.getFullYear()
  const mm = String(now.getMonth() + 1).padStart(2, '0')
  const dd = String(now.getDate()).padStart(2, '0')
  const hh = String(now.getHours()).padStart(2, '0')
  const min = String(now.getMinutes()).padStart(2, '0')
  const ss = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${yyyy}.${mm}.${dd} // ${hh}:${min}:${ss}`
}

onMounted(async () => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)

  try {
    const camRes = await fetch('/api/cameras')
    if (camRes.ok) {
      cameras.value = await camRes.json()
      if (cameras.value.length > 0) {
        selectedCameraId.value = cameras.value[0].id
      }
    }

    const alertRes = await fetch('/api/alerts')
    if (alertRes.ok) {
      alerts.value = await alertRes.json()
    }

    const recRes = await fetch('/api/recordings')
    if (recRes.ok) {
      recordings.value = await recRes.json()
    }
  } catch (err) {
    console.error('Failed to load dashboard metrics:', err)
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})

const activeAlertsCount = computed(() => {
  return alerts.value.filter(a => !a.resolved).length
})

const selectedCamera = computed(() => {
  return cameras.value.find(c => c.id === selectedCameraId.value)
})

const streamUrl = computed(() => {
  if (!selectedCamera.value) return ''
  const name = selectedCamera.value.name
  const cleanedName = name.toLowerCase().replace(/[^a-z0-9 _-]/g, '').replace(/\s+/g, '_')
  const token = localStorage.getItem('user-token') || ''
  return `http://127.0.0.1:8889/${cleanedName}?user=${token}`
})
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 overflow-y-auto bg-[var(--s-bg)] flex flex-col min-h-screen">
    <!-- Header -->
    <header class="mb-10 flex flex-col sm:flex-row sm:items-end justify-between border-b border-[var(--s-line)] pb-6 gap-4">
      <div>
        <h2 class="text-3xl font-bold text-[var(--s-white)] tracking-tighter uppercase font-[var(--font-sans)]">
          Security Overview
        </h2>
        <p class="text-[var(--s-mid)] mt-1 font-terminal text-[10px] uppercase tracking-[0.2em]">
          Welcome back, Agent. Status: Nominal // Node Active
        </p>
      </div>
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] px-4 py-2.5 text-xs font-terminal text-[var(--s-mid)] tracking-widest uppercase">
        {{ currentTime }}
      </div>
    </header>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <!-- Active Cameras Card -->
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start mb-6">
          <div class="p-3 border border-[var(--s-line2)] bg-[var(--s-bg3)]">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
              <path d="M23 7l-7 5 7 5V7z" />
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
            </svg>
          </div>
          <span class="text-[9px] font-terminal text-[var(--s-ok)] uppercase tracking-widest bg-emerald-950/20 px-2 py-0.5 border border-emerald-900/30">
            SYNCED
          </span>
        </div>
        <div>
          <p class="text-[10px] font-terminal text-[var(--s-dim)] uppercase tracking-wider mb-1">
            Active Camera Nodes
          </p>
          <p class="text-3xl font-bold text-[var(--s-white)] font-[var(--font-sans)] tracking-tight">
            {{ isLoading ? '...' : cameras.length }}
          </p>
        </div>
      </div>

      <!-- Active Threats Card -->
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start mb-6">
          <div class="p-3 border border-[var(--s-line2)] bg-[var(--s-bg3)]">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          </div>
          <span 
            :class="[
              'text-[9px] font-terminal uppercase tracking-widest px-2 py-0.5 border',
              activeAlertsCount > 0 
                ? 'text-[var(--s-err)] bg-red-950/20 border-red-900/30 animate-pulse' 
                : 'text-[var(--s-mid)] bg-zinc-950 border-zinc-900'
            ]"
          >
            {{ activeAlertsCount > 0 ? 'WARNING' : 'STABLE' }}
          </span>
        </div>
        <div>
          <p class="text-[10px] font-terminal text-[var(--s-dim)] uppercase tracking-wider mb-1">
            Unresolved Incidents
          </p>
          <p class="text-3xl font-bold text-[var(--s-white)] font-[var(--font-sans)] tracking-tight">
            {{ isLoading ? '...' : activeAlertsCount }}
          </p>
        </div>
      </div>

      <!-- Storage segments Card -->
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start mb-6">
          <div class="p-3 border border-[var(--s-line2)] bg-[var(--s-bg3)]">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
              <line x1="12" y1="22.08" x2="12" y2="12" />
            </svg>
          </div>
          <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest bg-zinc-950 px-2 py-0.5 border border-zinc-900">
            ACTIVE
          </span>
        </div>
        <div>
          <p class="text-[10px] font-terminal text-[var(--s-dim)] uppercase tracking-wider mb-1">
            Archived Segments
          </p>
          <p class="text-3xl font-bold text-[var(--s-white)] font-[var(--font-sans)] tracking-tight">
            {{ isLoading ? '...' : recordings.length }}
          </p>
        </div>
      </div>
    </div>

    <!-- Live Preview Display -->
    <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6 flex-1 flex flex-col min-h-[400px]">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[var(--s-line2)] pb-4 mb-6">
        <div>
          <span class="text-[9px] font-terminal text-[var(--s-dim)] uppercase tracking-wider block">Live Stream Monitor</span>
          <h3 class="text-base font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-tight mt-0.5">
            Surveillance Feeds // Primary Viewport
          </h3>
        </div>

        <!-- Camera Switch Dropdown -->
        <div class="flex items-center gap-3">
          <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest">Select Node:</label>
          <select 
            v-model="selectedCameraId"
            class="bg-[var(--s-bg)] border border-[var(--s-line)] px-3 py-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer"
          >
            <option v-for="cam in cameras" :key="cam.id" :value="cam.id">
              {{ cam.name.toUpperCase() }}
            </option>
            <option v-if="cameras.length === 0" value="">
              NO CONFIGURED FEEDS
            </option>
          </select>
        </div>
      </div>

      <!-- Stream Frame viewport -->
      <div class="flex-1 bg-black border border-[var(--s-line)] flex items-center justify-center relative overflow-hidden group min-h-[300px]">
        <iframe 
          v-if="cameras.length > 0 && selectedCameraId"
          :src="streamUrl"
          class="w-full h-full absolute inset-0 border-none transition-all duration-300"
          allow="autoplay; fullscreen" 
          style="filter: contrast(1.15) brightness(1.1) grayscale(0.5);"
        ></iframe>

        <!-- Empty state when no cameras exist -->
        <div v-else class="text-center p-10 flex flex-col items-center justify-center">
          <span class="text-xs font-terminal text-[var(--s-dim)] uppercase tracking-widest animate-pulse mb-4">
            &gt; NO ACTIVE SURVEILLANCE STREAMS DEFINED
          </span>
          <router-link 
            to="/cameras"
            class="px-4 py-2 border border-[var(--s-line2)] bg-[var(--s-bg4)] hover:bg-[var(--s-bg3)] text-[10px] font-terminal text-[var(--s-white)] uppercase tracking-wider transition-colors cursor-pointer"
          >
            Configure Stream Nodes
          </router-link>
        </div>

        <!-- Camera Identifier Overlay -->
        <div v-if="selectedCamera" class="absolute bottom-4 left-4 right-4 bg-gradient-to-t from-black/80 to-transparent p-4 flex items-end justify-between pointer-events-none">
          <div>
            <span class="text-[10px] font-bold text-[var(--s-white)] font-terminal uppercase tracking-widest block">
              {{ selectedCamera.name }}
            </span>
            <span class="text-[8px] font-terminal text-[var(--s-ok)] uppercase tracking-wider block mt-0.5">
              STREAM QUALITY: 1080P // ON-LINE
            </span>
          </div>
          <span class="text-[8px] font-terminal text-[var(--s-dim)] uppercase">
            FEED_SRC_ADDR: {{ selectedCamera.rtsp_url }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 32px;
}
</style>
