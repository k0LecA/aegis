<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import AlertItem  from '@/components/alerts/AlertItem.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { fetchCameras, fetchAlerts, createAlert, resolveAlert } from '@/api'
import type { Camera, Alert } from '@/types'

const cameras      = ref<Camera[]>([])
const alerts       = ref<Alert[]>([])
const cameraMap    = computed(() => Object.fromEntries(cameras.value.map(c => [c.id, c.name])))
const isSimulating = ref(false)

// Filter state
const selectedCameraId = ref<string>('ALL')
const filterResolved   = ref<'ALL' | 'UNRESOLVED' | 'RESOLVED'>('UNRESOLVED')

onMounted(async () => {
  try {
    [cameras.value, alerts.value] = await Promise.all([fetchCameras(), fetchAlerts()])
  } catch (err) {
    console.error('Alerts load error:', err)
  }
})

const unresolvedCount = computed(() => alerts.value.filter(a => !a.resolved).length)

const filteredAlerts = computed(() =>
  [...alerts.value]
    .sort((a, b) => new Date(b.triggered_at).getTime() - new Date(a.triggered_at).getTime())
    .filter(alert => {
      const matchCamera = selectedCameraId.value === 'ALL' || alert.camera_id === selectedCameraId.value
      const matchStatus =
        filterResolved.value === 'ALL'        ? true :
        filterResolved.value === 'UNRESOLVED' ? !alert.resolved :
                                                 alert.resolved
      return matchCamera && matchStatus
    })
)

async function handleResolve(id: string) {
  try {
    await resolveAlert(id)
    const idx = alerts.value.findIndex(a => a.id === id)
    if (idx !== -1) alerts.value[idx].resolved = true
  } catch (err) {
    console.error('Resolve alert error:', err)
  }
}

async function simulateAlert() {
  if (cameras.value.length === 0) return
  isSimulating.value = true
  try {
    const cam  = cameras.value[Math.floor(Math.random() * cameras.value.length)]
    const type = Math.random() > 0.5 ? 'motion' : 'intruder'
    const created = await createAlert({ camera_id: cam.id, type, resolved: false })
    alerts.value.push(created)
  } catch (err) {
    console.error('Simulate alert error:', err)
  } finally {
    isSimulating.value = false
  }
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto scrollbar-thin">
    <PageHeader
      title="Security Alert Dispatch"
      :subtitle="`Intrusion Registry // Unresolved Threats: ${unresolvedCount}`"
    >
      <button
        @click="simulateAlert"
        :disabled="isSimulating || cameras.length === 0"
        class="border border-[var(--s-line2)] bg-[var(--s-bg4)] hover:bg-[var(--s-bg3)] disabled:opacity-40 px-4 py-2.5 text-[9px] font-terminal text-[var(--s-white)] uppercase tracking-widest transition-colors cursor-pointer"
      >
        {{ isSimulating ? 'TRANSMITTING...' : 'Simulate Intrusion Alert' }}
      </button>
    </PageHeader>

    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-8 p-4 bg-[var(--s-bg2)] border border-[var(--s-line)]">
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Filter Node</label>
        <select
          v-model="selectedCameraId"
          class="bg-[var(--s-bg)] border border-[var(--s-line)] p-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer"
        >
          <option value="ALL">ALL NODES</option>
          <option v-for="cam in cameras" :key="cam.id" :value="cam.id">{{ cam.name }}</option>
        </select>
      </div>

      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Filter Status</label>
        <div class="flex border border-[var(--s-line)]">
          <button
            v-for="opt in (['UNRESOLVED', 'RESOLVED', 'ALL'] as const)"
            :key="opt"
            @click="filterResolved = opt"
            :class="[
              'px-3 py-2 text-[9px] font-terminal uppercase transition-colors cursor-pointer border-l border-[var(--s-line)] first:border-l-0',
              filterResolved === opt ? 'bg-[var(--s-bg4)] text-white' : 'bg-[var(--s-bg)] text-[var(--s-mid)]'
            ]"
          >
            {{ opt === 'UNRESOLVED' ? 'Unresolved' : opt === 'RESOLVED' ? 'Resolved' : 'All Logs' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Alert List -->
    <div class="space-y-4">
      <AlertItem
        v-for="alert in filteredAlerts"
        :key="alert.id"
        :alert="alert"
        :camera-name="cameraMap[alert.camera_id]"
        @resolve="handleResolve"
      />
      <EmptyState
        v-if="filteredAlerts.length === 0"
        message="INTRUSION LOG IS CLEAR // SECTOR SECURE"
      />
    </div>
  </div>
</template>
