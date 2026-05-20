<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar      from '@/components/navigation/Sidebar.vue'
import MobileHeader from '@/components/navigation/MobileHeader.vue'

const route         = useRoute()
const isSidebarOpen = ref(false)

const isAuthPage = computed(() => route.path === '/login' || route.name === 'Login')

function toggleSidebar() { isSidebarOpen.value = !isSidebarOpen.value }

// Close sidebar on navigation
watch(() => route.path, () => { isSidebarOpen.value = false })
</script>

<template>
  <!-- Authenticated shell -->
  <div v-if="!isAuthPage" class="flex h-screen w-full bg-[var(--s-bg)] overflow-hidden relative">
    <!-- Mobile overlay backdrop -->
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
        class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
        @click="isSidebarOpen = false"
      />
    </Transition>

    <Sidebar :is-open="isSidebarOpen" @toggle="toggleSidebar" />

    <main class="flex-1 flex flex-col relative overflow-hidden">
      <MobileHeader :is-sidebar-open="isSidebarOpen" @toggle="toggleSidebar" />

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

  <!-- Auth page (no shell) -->
  <div v-else class="h-screen w-full bg-[var(--s-bg)]">
    <router-view />
  </div>
</template>