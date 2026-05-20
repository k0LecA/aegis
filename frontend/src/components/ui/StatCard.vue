<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  status?: 'ok' | 'warn' | 'err' | 'neutral'
  statusText?: string
}>()

const STATUS_CLASSES = {
  ok:      'text-[var(--s-ok)] bg-emerald-950/20 border-emerald-900/30',
  warn:    'text-[var(--s-warn)] bg-yellow-950/20 border-yellow-900/30',
  err:     'text-[var(--s-err)] bg-red-950/20 border-red-900/30 animate-pulse',
  neutral: 'text-[var(--s-mid)] bg-zinc-950 border-zinc-900',
}
</script>

<template>
  <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6 flex flex-col justify-between">
    <div class="flex justify-between items-start mb-6">
      <div class="p-3 border border-[var(--s-line2)] bg-[var(--s-bg3)]">
        <slot name="icon" />
      </div>
      <span
        v-if="statusText"
        :class="['text-[9px] font-terminal uppercase tracking-widest px-2 py-0.5 border', STATUS_CLASSES[status ?? 'neutral']]"
      >
        {{ statusText }}
      </span>
    </div>
    <div>
      <p class="text-[10px] font-terminal text-[var(--s-dim)] uppercase tracking-wider mb-1">
        {{ label }}
      </p>
      <p class="text-3xl font-bold text-[var(--s-white)] font-[var(--font-sans)] tracking-tight">
        {{ value }}
      </p>
    </div>
  </div>
</template>
