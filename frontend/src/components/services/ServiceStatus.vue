<script setup lang="ts">
defineProps<{ isRunning: boolean }>()
defineEmits<{
  (e: 'toggle'):  void
  (e: 'restart'): void
}>()
</script>

<template>
  <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6">
    <div class="flex items-center justify-between border-b border-[var(--s-line2)] pb-4 mb-6">
      <div>
        <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider block">Service Unit</span>
        <h3 class="text-sm font-bold text-[var(--s-white)] uppercase tracking-tight font-terminal">
          MediaMTX RTSP Server
        </h3>
      </div>
      <!-- Status Badge -->
      <div class="flex items-center gap-2">
        <span
          class="w-2 h-2 rounded-full"
          :class="isRunning ? 'bg-[var(--s-ok)] animate-pulse' : 'bg-[var(--s-err)]'"
        />
        <span
          class="text-xs font-bold font-terminal uppercase tracking-wider"
          :class="isRunning ? 'text-[var(--s-ok)]' : 'text-[var(--s-err)]'"
        >
          {{ isRunning ? 'Active (Running)' : 'Inactive (Stopped)' }}
        </span>
      </div>
    </div>

    <!-- Controls -->
    <div class="flex flex-wrap gap-4">
      <button
        @click="$emit('toggle')"
        :class="[
          'px-4 py-2.5 text-xs font-terminal uppercase tracking-widest border transition-all cursor-pointer',
          isRunning
            ? 'border-[var(--s-err)] text-[var(--s-err)] bg-red-950/10 hover:bg-[var(--s-err)] hover:text-white'
            : 'border-[var(--s-ok)] text-[var(--s-ok)] bg-emerald-950/10 hover:bg-[var(--s-ok)] hover:text-white'
        ]"
      >
        {{ isRunning ? 'Stop Server' : 'Start Server' }}
      </button>

      <button
        @click="$emit('restart')"
        class="px-4 py-2.5 text-xs font-terminal uppercase tracking-widest border border-[var(--s-line2)] bg-[var(--s-bg4)] text-[var(--s-white)] hover:bg-[var(--s-bg3)] transition-colors cursor-pointer"
      >
        Restart Server
      </button>
    </div>
  </div>
</template>
