<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import PageHeader    from '@/components/ui/PageHeader.vue'
import ServiceStatus from '@/components/services/ServiceStatus.vue'
import ServiceLogs   from '@/components/services/ServiceLogs.vue'
import ServiceConfig from '@/components/services/ServiceConfig.vue'
import {
  fetchServiceStatus,
  toggleService,
  restartService,
  fetchServiceConfig,
  saveServiceConfig,
  fetchServiceLogs,
} from '@/api'
import type { MediaMTXConfig } from '@/types'

const isRunning  = ref(false)
const logs       = ref<string[]>([])
const isSaving   = ref(false)
const saveSuccess = ref(false)

const config = ref<MediaMTXConfig>({
  record: false,
  recordFormat: 'fmp4',
  recordPath: './recordings/%path/%v_%Y-%m-%d_%H-%M-%S_%f',
  recordSegmentDuration: '1h',
})

let pollInterval: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  await Promise.all([refreshStatus(), loadConfig(), refreshLogs()])
  pollInterval = setInterval(async () => {
    await refreshStatus()
    await refreshLogs()
  }, 2000)
})

onUnmounted(() => { if (pollInterval) clearInterval(pollInterval) })

async function refreshStatus() {
  try {
    const data = await fetchServiceStatus()
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

async function handleToggle() {
  try {
    const data = await toggleService()
    isRunning.value = data.running
    await refreshLogs()
  } catch (err) { console.error('Toggle error:', err) }
}

async function handleRestart() {
  try {
    const data = await restartService()
    isRunning.value = data.running
    await refreshLogs()
  } catch (err) { console.error('Restart error:', err) }
}

async function handleSaveConfig(newConfig: MediaMTXConfig) {
  isSaving.value   = true
  saveSuccess.value = false
  try {
    await saveServiceConfig(newConfig)
    config.value    = newConfig
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
    await refreshLogs()
  } catch (err) { console.error('Save config error:', err) }
  finally { isSaving.value = false }
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto scrollbar-thin flex flex-col min-h-screen">
    <PageHeader title="Core Services Control" subtitle="Surveillance Node Operations // Process Controller">
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Process.Manager</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">ONLINE</span>
      </div>
    </PageHeader>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-8 flex-1 items-stretch">
      <!-- Left: Status + Logs -->
      <div class="flex flex-col gap-6 h-full">
        <ServiceStatus
          :is-running="isRunning"
          @toggle="handleToggle"
          @restart="handleRestart"
        />
        <ServiceLogs :logs="logs" />
      </div>

      <!-- Right: Config Form -->
      <ServiceConfig
        :config="config"
        :is-saving="isSaving"
        :save-success="saveSuccess"
        @save="handleSaveConfig"
      />
    </div>
  </div>
</template>
