<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>

<template>
  <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-12 text-center text-[var(--s-dim)] uppercase tracking-widest font-terminal text-[10px]">
    &gt; {{ message ?? 'NO DATA FOUND // SECTOR CLEAR' }}
  </div>
</template>
