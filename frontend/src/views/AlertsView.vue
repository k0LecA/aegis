<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

interface Camera {
  id: string
  name: string
}

interface Alert {
  id: string
  camera_id: string
  type: string  // 'motion' | 'intruder'
  resolved: boolean
  triggered_at: string
}

const alerts = ref<Alert[]>([])
const cameras = ref<Camera[]>([])
const cameraMap = ref<Record<string, string>>({})

const selectedCameraId = ref<string>('ALL')
const filterResolved = ref<string>('UNRESOLVED') // 'ALL' | 'UNRESOLVED' | 'RESOLVED'

const isSimulating = ref(false)

onMounted(async () => {
  await fetchDependencies()
})

const fetchDependencies = async () => {
  try {
    // Fetch cameras
    const camRes = await fetch('/api/cameras')
    if (camRes.ok) {
      cameras.value = await camRes.json()
      cameras.value.forEach(c => {
        cameraMap.value[c.id] = c.name
      })
    }

    // Fetch alerts
    const alertRes = await fetch('/api/alerts')
    if (alertRes.ok) {
      alerts.value = await alertRes.json()
    }
  } catch (error) {
    console.error('Failed to load alerts view dependencies:', error)
  }
}

const filteredAlerts = computed(() => {
  // Sort by triggered_at descending to keep most recent alerts at the top
  const sortedAlerts = [...alerts.value].sort((a, b) => {
    return new Date(b.triggered_at).getTime() - new Date(a.triggered_at).getTime()
  })

  return sortedAlerts.filter(alert => {
    const matchesCamera = selectedCameraId.value === 'ALL' || alert.camera_id === selectedCameraId.value
    let matchesStatus = true
    if (filterResolved.value === 'UNRESOLVED') {
      matchesStatus = !alert.resolved
    } else if (filterResolved.value === 'RESOLVED') {
      matchesStatus = alert.resolved
    }
    return matchesCamera && matchesStatus
  })
})

const unresolvedCount = computed(() => {
  return alerts.value.filter(a => !a.resolved).length
})

const resolveAlertNode = async (id: string) => {
  try {
    const res = await fetch(`/api/alerts/${id}/resolve`, { method: 'PATCH' })
    if (res.ok) {
      const index = alerts.value.findIndex(a => a.id === id)
      if (index !== -1) {
        alerts.value[index].resolved = true
      }
    }
  } catch (error) {
    console.error('Failed to resolve alert:', error)
  }
}

const triggerSimulationAlert = async () => {
  if (cameras.value.length === 0) return
  
  isSimulating.value = true
  try {
    // Pick random camera and type
    const randomCamera = cameras.value[Math.floor(Math.random() * cameras.value.length)]
    const alertType = Math.random() > 0.5 ? 'motion' : 'intruder'
    
    const res = await fetch('/api/alerts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        camera_id: randomCamera.id,
        type: alertType,
        resolved: false
      })
    })

    if (res.ok) {
      const created = await res.json()
      alerts.value.push(created)
    }
  } catch (error) {
    console.error('Failed to trigger simulation alert:', error)
  } finally {
    isSimulating.value = false
  }
}

const formatDate = (isoString: string) => {
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
          Security Alert Dispatch
        </h2>
        <p class="text-[var(--s-mid)] font-terminal text-[10px] uppercase tracking-[0.2em] mt-1">
          Intrusion Registry // Unresolved Threats: {{ unresolvedCount }}
        </p>
      </div>
      <div>
        <button 
          @click="triggerSimulationAlert"
          :disabled="isSimulating || cameras.length === 0"
          class="border border-[var(--s-line2)] bg-[var(--s-bg4)] hover:bg-[var(--s-bg3)] disabled:opacity-40 px-4 py-2.5 text-[9px] font-terminal text-[var(--s-white)] hover:text-white uppercase tracking-widest transition-colors cursor-pointer"
        >
          {{ isSimulating ? 'TRANSMITTING...' : 'Simulate Intrusion Alert' }}
        </button>
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
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Filter Status</label>
        <div class="flex border border-[var(--s-line)]">
          <button 
            @click="filterResolved = 'UNRESOLVED'"
            :class="['px-3 py-2 text-[9px] font-terminal uppercase transition-colors cursor-pointer', filterResolved === 'UNRESOLVED' ? 'bg-[var(--s-bg4)] text-white' : 'bg-[var(--s-bg)] text-[var(--s-mid)]']"
          >
            Unresolved
          </button>
          <button 
            @click="filterResolved = 'RESOLVED'"
            :class="['px-3 py-2 text-[9px] font-terminal uppercase border-l border-[var(--s-line)] transition-colors cursor-pointer', filterResolved === 'RESOLVED' ? 'bg-[var(--s-bg4)] text-white' : 'bg-[var(--s-bg)] text-[var(--s-mid)]']"
          >
            Resolved
          </button>
          <button 
            @click="filterResolved = 'ALL'"
            :class="['px-3 py-2 text-[9px] font-terminal uppercase border-l border-[var(--s-line)] transition-colors cursor-pointer', filterResolved === 'ALL' ? 'bg-[var(--s-bg4)] text-white' : 'bg-[var(--s-bg)] text-[var(--s-mid)]']"
          >
            All Logs
          </button>
        </div>
      </div>
    </div>

    <!-- Alerts Log Grid -->
    <div class="space-y-4">
      <div 
        v-for="alert in filteredAlerts" 
        :key="alert.id"
        class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-colors"
        :class="alert.resolved ? 'border-l-4 border-l-[var(--s-ok)]' : 'border-l-4 border-l-[var(--s-err)]'"
      >
        <div class="flex items-start gap-4">
          <!-- Status Flash Badge -->
          <div 
            :class="[
              'px-2 py-1 text-[8px] font-terminal uppercase tracking-widest font-bold',
              alert.resolved ? 'bg-[var(--s-ok)]/10 text-[var(--s-ok)] border border-[var(--s-ok)]/20' : 'bg-[var(--s-err)]/10 text-[var(--s-err)] border border-[var(--s-err)]/20 animate-pulse'
            ]"
          >
            {{ alert.resolved ? 'SECURE' : 'CRITICAL_ALERT' }}
          </div>

          <div>
            <h3 class="text-sm font-bold uppercase tracking-tight font-terminal text-[var(--s-white)]">
              {{ alert.type === 'intruder' ? 'Intruder Detected' : 'Motion Triggered' }} // {{ cameraMap[alert.camera_id] || 'UNKNOWN_NODE' }}
            </h3>
            <p class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider mt-1">
              Time recorded: {{ formatDate(alert.triggered_at) }}
            </p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <span 
            v-if="alert.resolved" 
            class="text-[9px] font-terminal text-[var(--s-dim)] uppercase tracking-widest"
          >
            Acknowledged & Cleared
          </span>
          <button 
            v-else
            @click="resolveAlertNode(alert.id)"
            class="border border-[var(--s-err)] bg-red-950/10 hover:bg-[var(--s-err)] text-[var(--s-err)] hover:text-white px-3 py-2 text-[9px] font-terminal uppercase tracking-widest transition-all duration-200 cursor-pointer"
          >
            Clear Node Alert
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div 
        v-if="filteredAlerts.length === 0" 
        class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-12 text-center text-[var(--s-dim)] uppercase tracking-widest font-terminal text-[10px]"
      >
        &gt; INTRUSION LOG IS CLEAR // SECTOR SECURE
      </div>
    </div>
  </div>
</template>

<style scoped>
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
