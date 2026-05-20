<script setup lang="ts">
import type { Alert } from '@/types'
import { formatDate } from '@/composables/useFormat'

defineProps<{
  alert:      Alert
  cameraName: string
}>()

defineEmits<{ (e: 'resolve', id: string): void }>()
</script>

<template>
  <div
    class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-colors"
    :class="alert.resolved ? 'border-l-4 border-l-[var(--s-ok)]' : 'border-l-4 border-l-[var(--s-err)]'"
  >
    <div class="flex items-start gap-4">
      <!-- Status Badge -->
      <div
        :class="[
          'px-2 py-1 text-[8px] font-terminal uppercase tracking-widest font-bold',
          alert.resolved
            ? 'bg-[var(--s-ok)]/10 text-[var(--s-ok)] border border-[var(--s-ok)]/20'
            : 'bg-[var(--s-err)]/10 text-[var(--s-err)] border border-[var(--s-err)]/20 animate-pulse'
        ]"
      >
        {{ alert.resolved ? 'SECURE' : 'CRITICAL_ALERT' }}
      </div>

      <div>
        <h3 class="text-sm font-bold uppercase tracking-tight font-terminal text-[var(--s-white)]">
          {{ alert.type === 'intruder' ? 'Intruder Detected' : 'Motion Triggered' }}
          // {{ cameraName || 'UNKNOWN_NODE' }}
        </h3>
        <p class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider mt-1">
          Time recorded: {{ formatDate(alert.triggered_at) }}
        </p>
      </div>
    </div>

    <div class="flex items-center gap-4">
      <span v-if="alert.resolved" class="text-[9px] font-terminal text-[var(--s-dim)] uppercase tracking-widest">
        Acknowledged &amp; Cleared
      </span>
      <button
        v-else
        @click="$emit('resolve', alert.id)"
        class="border border-[var(--s-err)] bg-red-950/10 hover:bg-[var(--s-err)] text-[var(--s-err)] hover:text-white px-3 py-2 text-[9px] font-terminal uppercase tracking-widest transition-all duration-200 cursor-pointer"
      >
        Clear Node Alert
      </button>
    </div>
  </div>
</template>
