<script setup lang="ts">
defineProps<{
  isOpen: boolean
}>()

defineEmits<{
  (e: 'toggle'): void
}>()
</script>

<template>
  <aside 
    :class="[
      'fixed inset-y-0 left-0 w-64 bg-[var(--s-bg2)] border-r border-[var(--s-line)] flex flex-col p-4 z-50 transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0',
      isOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <!-- Mobile Close Button -->
    <button 
      v-if="isOpen"
      @click="$emit('toggle')"
      class="lg:hidden absolute top-4 right-[-50px] p-2 glass rounded-xl text-white/60 hover:text-white"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>

    <div class="flex items-center gap-3 px-2 mb-10 mt-2">
      <div class="w-10 h-10 border border-[var(--s-line2)] bg-[var(--s-bg4)] flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
      </div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-[var(--s-white)] leading-tight uppercase font-[var(--font-sans)]">AEGIS</h1>
        <p class="text-[10px] uppercase tracking-[0.2em] text-[var(--s-dim)] font-medium font-terminal">Security Hub</p>
      </div>
    </div>

    <nav class="flex-1 space-y-2">
      <!-- Dashboard -->
      <router-link 
        to="/"
        class="w-full flex items-center gap-4 px-4 py-3 nav-item group text-[var(--s-mid)] hover:text-[var(--s-white)]"
        active-class="active !text-white"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-hover:scale-110">
          <rect width="7" height="9" x="3" y="3" rx="1"/>
          <rect width="7" height="5" x="14" y="3" rx="1"/>
          <rect width="7" height="9" x="14" y="12" rx="1"/>
          <rect width="7" height="5" x="3" y="16" rx="1"/>
        </svg>
        <span class="font-medium">Dashboard</span>
      </router-link>

      <!-- Cameras -->
      <router-link 
        to="/cameras"
        class="w-full flex items-center gap-4 px-4 py-3 nav-item group text-[var(--s-mid)] hover:text-[var(--s-white)]"
        active-class="active !text-white"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-hover:scale-110">
          <path d="M23 7l-7 5 7 5V7z"/>
          <rect width="15" height="14" x="1" y="5" rx="2" ry="2"/>
        </svg>
        <span class="font-medium">Cameras</span>
      </router-link>

      <!-- Settings -->
      <router-link 
        to="/settings"
        class="w-full flex items-center gap-4 px-4 py-3 nav-item group text-[var(--s-mid)] hover:text-[var(--s-white)]"
        active-class="active !text-white"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-hover:scale-110">
          <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
        <span class="font-medium">Settings</span>
      </router-link>
    </nav>

    <div class="mt-auto p-4 border border-[var(--s-line)] bg-[var(--s-bg)]">
      <div class="flex items-center gap-3">
        <div class="w-2 h-2 bg-[var(--s-ok)]"></div>
        <div class="font-terminal">
          <p class="text-[11px] font-medium text-[var(--s-white)] uppercase">System Online</p>
          <p class="text-[9px] text-[var(--s-dim)]">v0.0.5 secure_build</p>
        </div>
      </div>
    </div>
  </aside>
</template>


