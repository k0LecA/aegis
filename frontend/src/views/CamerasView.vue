<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageHeader  from '@/components/ui/PageHeader.vue'
import CameraCard  from '@/components/cameras/CameraCard.vue'
import CameraModal from '@/components/cameras/CameraModal.vue'
import { useCameraStore } from '@/stores/cameras'
import type { Camera } from '@/types'

const store         = useCameraStore()
const isModalOpen   = ref(false)
const editingCamera = ref<Camera | null>(null)

// Load once — instant if already cached from Dashboard visit
onMounted(() => store.load())

function openAdd()             { editingCamera.value = null; isModalOpen.value = true }
function openEdit(cam: Camera) { editingCamera.value = cam;  isModalOpen.value = true }

async function handleSave(data: { name: string; rtsp_url: string }) {
  if (editingCamera.value) {
    await store.update(editingCamera.value.id, data)
  } else {
    await store.add(data)
  }
}

async function handleDelete(id: string) {
  await store.remove(id)
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto scrollbar-thin">
    <PageHeader title="Visual Surveillance" :subtitle="`Active Node Count: ${store.cameras.length} / System.Status: Nominal`">
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Network.Latency</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">12ms</span>
      </div>
    </PageHeader>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6">
      <CameraCard
        v-for="cam in store.cameras"
        :key="cam.id"
        :camera="cam"
        @edit="openEdit"
        @delete="handleDelete"
      />

      <button
        @click="openAdd"
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

    <CameraModal v-model="isModalOpen" :camera="editingCamera" @save="handleSave" />
  </div>
</template>
