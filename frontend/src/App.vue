<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/navigation/Sidebar.vue'

const isSidebarOpen = ref(false)
const route = useRoute()

// Check if we are on the login page
// You can also use route.meta.hideNavigation if you set that up in your router config
const isAuthPage = computed(() => route.path === '/login' || route.name === 'Login')

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

watch(() => route.path, () => {
  isSidebarOpen.value = false
})
</script>

<template>
  <div v-if="!isAuthPage" class="flex h-screen w-full bg-[#0f172a] overflow-hidden relative">
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="isSidebarOpen" 
        @click="isSidebarOpen = false"
        class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
      ></div>
    </Transition>

    <Sidebar :is-open="isSidebarOpen" @toggle="toggleSidebar" />

    <main class="flex-1 flex flex-col relative overflow-hidden">
      <header class="lg:hidden flex items-center justify-between p-4 glass border-b border-white/5 z-30">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-white">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <span class="font-bold text-white tracking-tight">AEGIS</span>
        </div>
        <button 
          @click="toggleSidebar"
          class="p-2 rounded-xl glass text-white/60 hover:text-white"
        >
          <svg v-if="!isSidebarOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </header>

      <div class="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-primary/20 blur-[120px] pointer-events-none"></div>
      
      <router-view v-slot="{ Component }">
        <Transition 
          mode="out-in"
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>
  </div>

  <div v-else class="h-screen w-full bg-[#f0f0f0]">
    <router-view />
  </div>
</template>