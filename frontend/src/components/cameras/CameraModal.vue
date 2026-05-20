<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Camera } from '@/types'

const props = defineProps<{
  modelValue: boolean           // v-model for open/close
  camera?: Camera | null        // null/undefined = create mode
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'save', data: { name: string; rtsp_url: string }): void
}>()

const name    = ref('')
const rtspUrl = ref('')

// Populate fields when editing an existing camera
watch(
  () => props.camera,
  (cam) => {
    name.value    = cam?.name     ?? ''
    rtspUrl.value = cam?.rtsp_url ?? ''
  },
  { immediate: true }
)

function close()  { emit('update:modelValue', false) }
function submit() {
  if (!name.value.trim() || !rtspUrl.value.trim()) return
  emit('save', { name: name.value.toUpperCase(), rtsp_url: rtspUrl.value })
  close()
}
</script>

<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="close" />

      <!-- Panel -->
      <div class="relative w-full max-w-md bg-[var(--s-bg2)] border border-[var(--s-line2)] p-8 shadow-2xl">
        <!-- Header -->
        <div class="flex items-center justify-between mb-8 border-b border-[var(--s-line)] pb-4">
          <h3 class="text-xl font-bold text-[var(--s-white)] uppercase tracking-tighter font-[var(--font-sans)]">
            {{ camera ? 'Update Security Node' : 'Add Security Node' }}
          </h3>
          <button @click="close" class="text-[var(--s-dim)] hover:text-[var(--s-white)]">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Fields -->
        <div class="space-y-6">
          <div class="space-y-2">
            <label class="block text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest">
              Node Name (Identifier)
            </label>
            <input
              v-model="name"
              type="text"
              placeholder="E.G. HALLWAY_01"
              class="w-full bg-[var(--s-bg)] border border-[var(--s-line)] p-3 text-[var(--s-white)] font-terminal text-sm focus:outline-none focus:border-[var(--s-mid)] placeholder:text-[var(--s-dim)]"
            />
          </div>
          <div class="space-y-2">
            <label class="block text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest">
              RTSP Stream Address
            </label>
            <input
              v-model="rtspUrl"
              type="text"
              placeholder="rtsp://admin:pass@192.168.1.XX:554/live"
              class="w-full bg-[var(--s-bg)] border border-[var(--s-line)] p-3 text-[var(--s-white)] font-terminal text-sm focus:outline-none focus:border-[var(--s-mid)] placeholder:text-[var(--s-dim)]"
            />
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-10 flex gap-4">
          <button
            @click="close"
            class="flex-1 border border-[var(--s-line)] p-3 text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest hover:bg-[var(--s-bg3)] hover:text-[var(--s-white)] transition-colors"
          >
            Cancel
          </button>
          <button
            @click="submit"
            class="flex-1 bg-[var(--s-white)] text-[var(--s-bg)] p-3 text-[9px] font-terminal font-bold uppercase tracking-widest hover:bg-white transition-colors"
          >
            {{ camera ? 'Commit Changes' : 'Initialize Node' }}
          </button>
        </div>

        <p class="mt-6 pt-4 border-t border-[var(--s-line)] text-[8px] font-terminal text-[var(--s-dim)] uppercase text-center">
          Security clearance required for remote access.
        </p>
      </div>
    </div>
  </Transition>
</template>
