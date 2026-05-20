<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import PageHeader    from '@/components/ui/PageHeader.vue'
import ServiceStatus from '@/components/services/ServiceStatus.vue'
import ServiceLogs   from '@/components/services/ServiceLogs.vue'
import ServiceConfig from '@/components/services/ServiceConfig.vue'
import { useServiceStore } from '@/stores/services'
import type { MediaMTXConfig } from '@/types'

const store = useServiceStore()

let pollInterval: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  // init() is idempotent — only fetches on first visit
  await store.init()
  // Keep polling while this tab is active
  pollInterval = setInterval(async () => {
    await store.refreshStatus()
    await store.refreshLogs()
  }, 2000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
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
      <div class="flex flex-col gap-6 h-full">
        <ServiceStatus
          :is-running="store.isRunning"
          @toggle="store.toggle"
          @restart="store.restart"
        />
        <ServiceLogs :logs="store.logs" />
      </div>

      <ServiceConfig
        :config="store.config"
        :is-saving="store.isSaving"
        :save-success="store.saveSuccess"
        @save="(cfg: MediaMTXConfig) => store.saveConfig(cfg)"
      />
    </div>
  </div>
</template>
