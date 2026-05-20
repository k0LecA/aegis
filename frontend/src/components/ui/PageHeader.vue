<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <div class="mb-10 flex flex-col md:flex-row md:items-end justify-between border-b border-[var(--s-line)] pb-6 gap-4">
    <div>
      <h2 class="text-3xl font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-tighter">
        {{ title }}
      </h2>
      <p v-if="subtitle" class="text-[var(--s-mid)] font-terminal text-[10px] uppercase tracking-[0.2em] mt-1">
        {{ subtitle }}
      </p>
    </div>
    <!-- Optional right-side content (e.g. clock, button, badge) -->
    <slot />
  </div>
</template>
