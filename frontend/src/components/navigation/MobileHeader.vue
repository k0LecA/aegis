<script setup lang="ts">
defineProps<{ isSidebarOpen: boolean }>()
defineEmits<{ (e: 'toggle'): void }>()
</script>

<template>
  <header class="lg:hidden flex items-center justify-between p-4 bg-[var(--s-bg2)] border-b border-[var(--s-line2)] z-30">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 border border-[var(--s-line2)] bg-[var(--s-bg4)] flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-white">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
      </div>
      <span class="font-bold text-white tracking-tight font-[var(--font-sans)]">AEGIS</span>
    </div>

    <button
      @click="$emit('toggle')"
      class="p-2 border border-[var(--s-line)] bg-[var(--s-bg3)] text-[var(--s-mid)] hover:text-[var(--s-white)] hover:bg-[var(--s-bg4)] transition-colors"
    >
      <!-- Hamburger -->
      <svg v-if="!isSidebarOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
      <!-- Close -->
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
  </header>
</template>
