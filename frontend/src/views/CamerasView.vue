<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Camera {
  id: string
  name: string
  rtsp_url: string
  status: 'online' | 'offline' | 'warning'
}

const cameras = ref<Camera[]>([])

onMounted(async () => {
  const res = await fetch('/api/cameras')
  cameras.value = await res.json()
})

const isModalOpen = ref(false)
const activeMenuId = ref<string | null>(null)
const editingCameraId = ref<string | null>(null)

const newCamera = ref({
  name: '',
  rtsp_url: ''
})

const openModal = (camera?: Camera) => {
  if (camera) {
    editingCameraId.value = camera.id
    newCamera.value = { name: camera.name, rtsp_url: camera.rtsp_url }
  } else {
    editingCameraId.value = null
    newCamera.value = { name: '', rtsp_url: '' }
  }
  isModalOpen.value = true
  activeMenuId.value = null
}

const closeModal = () => {
  isModalOpen.value = false
  editingCameraId.value = null
}

const toggleMenu = (event: Event, id: string) => {
  event.stopPropagation()
  activeMenuId.value = activeMenuId.value === id ? null : id
}

const deleteCamera = async (id: string) => {
  await fetch(`/api/cameras/${id}`, { method: 'DELETE' })
  cameras.value = cameras.value.filter(c => c.id !== id)
  activeMenuId.value = null
}

const saveCamera = async () => {
  if (!newCamera.value.name || !newCamera.value.rtsp_url) return

  if (editingCameraId.value) {
    await fetch(`/api/cameras/${editingCameraId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newCamera.value.name.toUpperCase(),
        rtsp_url: newCamera.value.rtsp_url
      })
    })
  } else {
    const res = await fetch('/api/cameras', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newCamera.value.name.toUpperCase(),
        rtsp_url: newCamera.value.rtsp_url
      })
    })
    const created = await res.json()
    cameras.value.push(created)
    closeModal()
    return
  }

  const index = cameras.value.findIndex(c => c.id === editingCameraId.value)
  if (index !== -1) {
    cameras.value[index] = { ...cameras.value[index], name: newCamera.value.name.toUpperCase(), rtsp_url: newCamera.value.rtsp_url }
  }
  closeModal()
}

// Close menus on click outside
const handleClickOutside = () => {
  activeMenuId.value = null
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto">
    <!-- Header Section -->
    <div class="mb-10 flex flex-col md:flex-row md:items-end justify-between border-b border-[var(--s-line)] pb-6 gap-4">
      <div>
        <h2 class="text-3xl font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-tighter">
          Visual Surveillance
        </h2>
        <p class="text-[var(--s-mid)] font-terminal text-[10px] uppercase tracking-[0.2em] mt-1">
          Active Node Count: {{ cameras.length }} / System.Status: Nominal
        </p>
      </div>
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Network.Latency</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">12ms</span>
      </div>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6">
      <!-- Camera Tiles -->
      <div 
        v-for="camera in cameras" 
        :key="camera.id"
        class="s-card group flex flex-col h-64 overflow-hidden"
      >
        <!-- Feed Placeholder -->
        <div class="flex-1 bg-black relative flex items-center justify-center border-b border-[var(--s-line)]">
          <div class="absolute inset-0 opacity-10 pointer-events-none overflow-hidden">
            <div class="w-full h-full bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(255,255,255,0.05)_3px)]"></div>
          </div>
          
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-dim)] group-hover:text-[var(--s-mid)] transition-colors">
            <path d="M23 7l-7 5 7 5V7z"/>
            <rect width="15" height="14" x="1" y="5" rx="0" ry="0"/>
          </svg>

          <!-- Status Indicator -->
          <div class="absolute top-3 left-3 flex items-center gap-2">
            <div 
              class="w-1.5 h-1.5" 
              :class="{
                'bg-[var(--s-ok)]': camera.status === 'online',
                'bg-[var(--s-warn)]': camera.status === 'warning',
                'bg-[var(--s-err)]': camera.status === 'offline'
              }"
            ></div>
            <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest bg-black/50 px-1">
              {{ camera.status }}
            </span>
          </div>
          
          <div class="absolute bottom-2 right-3">
             <span class="text-[8px] font-terminal text-[var(--s-dim)] uppercase">REC // AUTO</span>
          </div>
        </div>

        <!-- Meta Info -->
        <div class="p-4 flex flex-col gap-1 relative">
          <div class="flex justify-between items-start">
            <h3 class="text-sm font-bold text-[var(--s-white)] font-terminal tracking-tight uppercase">{{ camera.name }}</h3>
            <div class="relative">
              <button 
                @click="(e) => toggleMenu(e, camera.id)"
                class="text-[var(--s-dim)] hover:text-[var(--s-white)] transition-colors p-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
              </button>
              
              <!-- Dropdown Menu -->
              <Transition
                enter-active-class="transition duration-100 ease-out"
                enter-from-class="opacity-0 scale-95"
                enter-to-class="opacity-100 scale-100"
                leave-active-class="transition duration-75 ease-in"
                leave-from-class="opacity-100 scale-100"
                leave-to-class="opacity-0 scale-95"
              >
                <div 
                  v-if="activeMenuId === camera.id" 
                  class="absolute right-0 bottom-full mb-2 w-32 bg-[var(--s-bg3)] border border-[var(--s-line2)] shadow-xl z-20"
                >
                  <button 
                    @click="openModal(camera)"
                    class="w-full text-left px-3 py-2 text-[9px] font-terminal text-[var(--s-mid)] hover:text-[var(--s-white)] hover:bg-[var(--s-bg4)] uppercase tracking-wider"
                  >
                    Edit Node
                  </button>
                  <button 
                    @click="deleteCamera(camera.id)"
                    class="w-full text-left px-3 py-2 text-[9px] font-terminal text-[var(--s-err)] hover:bg-red-950/30 uppercase tracking-wider border-t border-[var(--s-line)]"
                  >
                    Delete Node
                  </button>
                </div>
              </Transition>
            </div>
          </div>
          <p class="text-[9px] font-terminal text-[var(--s-dim)] truncate">{{ camera.rtsp_url }}</p>
        </div>
      </div>

      <!-- Add Tile -->
      <button 
        @click="() => openModal()"
        class="border border-dashed border-[var(--s-line2)] bg-transparent hover:bg-[var(--s-bg2)] hover:border-[var(--s-mid)] transition-all duration-300 flex flex-col items-center justify-center h-64 group gap-4"
      >
        <div class="w-12 h-12 border border-[var(--s-line2)] flex items-center justify-center group-hover:scale-110 transition-transform">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-mid)] group-hover:text-[var(--s-white)]">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
        </div>
        <span class="text-[10px] font-terminal text-[var(--s-mid)] uppercase tracking-[0.2em] group-hover:text-[var(--s-white)]">Initialize New Node</span>
      </button>
    </div>

    <!-- Modal -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="closeModal"></div>
        
        <div class="relative w-full max-w-md bg-[var(--s-bg2)] border border-[var(--s-line2)] p-8 shadow-2xl">
          <!-- Modal Header -->
          <div class="flex items-center justify-between mb-8 border-b border-[var(--s-line)] pb-4">
            <h3 class="text-xl font-bold text-[var(--s-white)] uppercase tracking-tighter font-[var(--font-sans)]">
              {{ editingCameraId ? 'Update Security Node' : 'Add Security Node' }}
            </h3>
            <button @click="closeModal" class="text-[var(--s-dim)] hover:text-[var(--s-white)]">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- Form -->
          <div class="space-y-6">
            <div class="space-y-2">
              <label class="block text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest">Node Name (Identifier)</label>
              <input 
                v-model="newCamera.name"
                type="text" 
                placeholder="E.G. HALLWAY_01"
                class="w-full bg-[var(--s-bg)] border border-[var(--s-line)] p-3 text-[var(--s-white)] font-terminal text-sm focus:outline-none focus:border-[var(--s-mid)] placeholder:text-[var(--s-dim)]"
              />
            </div>
            <div class="space-y-2">
              <label class="block text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest">RTSP Stream Address</label>
              <input 
                v-model="newCamera.rtsp_url"
                type="text" 
                placeholder="rtsp://admin:pass@192.168.1.XX:554/live"
                class="w-full bg-[var(--s-bg)] border border-[var(--s-line)] p-3 text-[var(--s-white)] font-terminal text-sm focus:outline-none focus:border-[var(--s-mid)] placeholder:text-[var(--s-dim)]"
              />
            </div>
          </div>

          <!-- Actions -->
          <div class="mt-10 flex gap-4">
            <button 
              @click="closeModal"
              class="flex-1 border border-[var(--s-line)] p-3 text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest hover:bg-[var(--s-bg3)] hover:text-[var(--s-white)] transition-colors"
            >
              Terminate
            </button>
            <button 
              @click="saveCamera"
              class="flex-1 bg-[var(--s-white)] text-[var(--s-bg)] p-3 text-[9px] font-terminal font-bold uppercase tracking-widest hover:bg-white transition-colors"
            >
              {{ editingCameraId ? 'Commit Changes' : 'Initialize Node' }}
            </button>
          </div>
          
          <div class="mt-6 pt-4 border-t border-[var(--s-line)]">
             <p class="text-[8px] font-terminal text-[var(--s-dim)] uppercase text-center">Security clearance required for remote access.</p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
/* Scrollbar styling */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}
.overflow-y-auto::-webkit-scrollbar-track {
  background: var(--s-bg);
}
.overflow-y-auto::-webkit-scrollbar-thumb {
  background: var(--s-line2);
}
.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: var(--s-mid);
}
</style>
