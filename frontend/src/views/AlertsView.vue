<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import AlertItem  from '@/components/alerts/AlertItem.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { useCameraStore } from '@/stores/cameras'
import { useAlertStore }  from '@/stores/alerts'

const cameraStore = useCameraStore()
const alertStore  = useAlertStore()

onMounted(() => Promise.all([cameraStore.load(), alertStore.load()]))

const cameraMap = computed(() =>
  Object.fromEntries(cameraStore.cameras.map(c => [c.id, c.name]))
)

const selectedCameraId = ref<string>('ALL')
const filterResolved   = ref<'ALL' | 'UNRESOLVED' | 'RESOLVED'>('UNRESOLVED')
const isSimulating     = ref(false)

const filteredAlerts = computed(() =>
  [...alertStore.alerts]
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

async function simulateAlert() {
  if (cameraStore.cameras.length === 0) return
  isSimulating.value = true
  try {
    const cam = cameraStore.cameras[Math.floor(Math.random() * cameraStore.cameras.length)]
    await alertStore.simulate(cam.id)
  } finally {
    isSimulating.value = false
  }
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto scrollbar-thin">
    <PageHeader
      title="Security Alert Dispatch"
      :subtitle="`Intrusion Registry // Unresolved Threats: ${alertStore.unresolvedCount}`"
    >
      <button
        @click="simulateAlert"
        :disabled="isSimulating || cameraStore.cameras.length === 0"
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
          <option v-for="cam in cameraStore.cameras" :key="cam.id" :value="cam.id">{{ cam.name }}</option>
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
        @resolve="alertStore.resolve"
      />
      <EmptyState v-if="filteredAlerts.length === 0" message="INTRUSION LOG IS CLEAR // SECTOR SECURE" />
    </div>
  </div>
</template>
