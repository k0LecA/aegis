<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatCard   from '@/components/ui/StatCard.vue'
import { useTime }      from '@/composables/useTime'
import { getStreamUrl } from '@/composables/useFormat'
import { useCameraStore }  from '@/stores/cameras'
import { useAlertStore }   from '@/stores/alerts'
import { useRecordingStore } from '@/stores/recordings'

const { currentTime } = useTime()

const cameraStore    = useCameraStore()
const alertStore     = useAlertStore()
const recordingStore = useRecordingStore()

// Load all three in parallel — skips if already cached
onMounted(() => Promise.all([
  cameraStore.load(),
  alertStore.load(),
  recordingStore.load(),
]))

const isLoading = computed(() =>
  cameraStore.loading || alertStore.loading || recordingStore.loading
)

const selectedCameraId = ref(cameraStore.cameras[0]?.id ?? '')

// Keep default selection in sync when cameras first arrive
const unwatchCameras = cameraStore.$subscribe(() => {
  if (!selectedCameraId.value && cameraStore.cameras.length > 0) {
    selectedCameraId.value = cameraStore.cameras[0].id
    unwatchCameras()
  }
})

const selectedCamera = computed(() =>
  cameraStore.cameras.find(c => c.id === selectedCameraId.value)
)
const streamUrl = computed(() =>
  selectedCamera.value ? getStreamUrl(selectedCamera.value.name) : ''
)
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 overflow-y-auto bg-[var(--s-bg)] flex flex-col min-h-screen scrollbar-thin">
    <PageHeader title="Security Overview" subtitle="Welcome back, Agent. Status: Nominal // Node Active">
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] px-4 py-2.5 text-xs font-terminal text-[var(--s-mid)] tracking-widest uppercase">
        {{ currentTime }}
      </div>
    </PageHeader>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <StatCard label="Active Camera Nodes" :value="isLoading ? '...' : cameraStore.cameras.length" status="ok" status-text="SYNCED">
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
            <path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Unresolved Incidents"
        :value="isLoading ? '...' : alertStore.unresolvedCount"
        :status="alertStore.unresolvedCount > 0 ? 'err' : 'neutral'"
        :status-text="alertStore.unresolvedCount > 0 ? 'WARNING' : 'STABLE'"
      >
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </template>
      </StatCard>

      <StatCard label="Archived Segments" :value="isLoading ? '...' : recordingStore.recordings.length" status="neutral" status-text="ACTIVE">
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>
          </svg>
        </template>
      </StatCard>
    </div>

    <!-- Live Preview -->
    <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6 flex-1 flex flex-col min-h-[400px]">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[var(--s-line2)] pb-4 mb-6">
        <div>
          <span class="text-[9px] font-terminal text-[var(--s-dim)] uppercase tracking-wider block">Live Stream Monitor</span>
          <h3 class="text-base font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-tight mt-0.5">
            Surveillance Feeds // Primary Viewport
          </h3>
        </div>
        <div class="flex items-center gap-3">
          <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest">Select Node:</label>
          <select
            v-model="selectedCameraId"
            class="bg-[var(--s-bg)] border border-[var(--s-line)] px-3 py-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer appearance-none"
          >
            <option v-for="cam in cameraStore.cameras" :key="cam.id" :value="cam.id">{{ cam.name.toUpperCase() }}</option>
            <option v-if="cameraStore.cameras.length === 0" value="">NO CONFIGURED FEEDS</option>
          </select>
        </div>
      </div>

      <div class="flex-1 bg-black border border-[var(--s-line)] flex items-center justify-center relative overflow-hidden min-h-[300px]">
        <iframe
          v-if="cameraStore.cameras.length > 0 && selectedCameraId"
          :src="streamUrl"
          class="w-full h-full absolute inset-0 border-none transition-all duration-300"
          allow="autoplay; fullscreen"
          style="filter: contrast(1.15) brightness(1.1) grayscale(0.5);"
        />
        <div v-else class="text-center p-10 flex flex-col items-center justify-center">
          <span class="text-xs font-terminal text-[var(--s-dim)] uppercase tracking-widest animate-pulse mb-4">
            &gt; NO ACTIVE SURVEILLANCE STREAMS DEFINED
          </span>
          <router-link to="/cameras" class="px-4 py-2 border border-[var(--s-line2)] bg-[var(--s-bg4)] hover:bg-[var(--s-bg3)] text-[10px] font-terminal text-[var(--s-white)] uppercase tracking-wider transition-colors">
            Configure Stream Nodes
          </router-link>
        </div>
        <div v-if="selectedCamera" class="absolute bottom-4 left-4 right-4 bg-gradient-to-t from-black/80 to-transparent p-4 flex items-end justify-between pointer-events-none">
          <div>
            <span class="text-[10px] font-bold text-[var(--s-white)] font-terminal uppercase tracking-widest block">{{ selectedCamera.name }}</span>
            <span class="text-[8px] font-terminal text-[var(--s-ok)] uppercase tracking-wider block mt-0.5">STREAM QUALITY: 1080P // ON-LINE</span>
          </div>
          <span class="text-[8px] font-terminal text-[var(--s-dim)] uppercase">FEED_SRC_ADDR: {{ selectedCamera.rtsp_url }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
