<script setup lang="ts">
import type { Camera } from '@/types'
import { getStreamUrl } from '@/composables/useFormat'

defineProps<{ camera: Camera }>()
const emit = defineEmits<{
  (e: 'edit', camera: Camera): void
  (e: 'delete', id: string): void
}>()
</script>

<template>
  <div class="s-card group flex flex-col h-64 overflow-hidden">
    <!-- Stream Preview -->
    <div class="flex-1 bg-black relative flex items-center justify-center border-b border-[var(--s-line)] overflow-hidden">
      <iframe
        :src="getStreamUrl(camera.name)"
        class="w-full h-full absolute inset-0 border-none pointer-events-none transition-all duration-300"
        allow="autoplay; fullscreen"
        style="filter: contrast(1.15) brightness(1.1) grayscale(0.5);"
      />

      <!-- Status Indicator -->
      <div class="absolute top-3 left-3 flex items-center gap-2 z-10">
        <div
          class="w-1.5 h-1.5"
          :class="{
            'bg-[var(--s-ok)]':   camera.status === 'online'  || !camera.status,
            'bg-[var(--s-warn)]': camera.status === 'warning',
            'bg-[var(--s-err)]':  camera.status === 'offline',
          }"
        />
        <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-widest bg-black/75 px-1.5 py-0.5 border border-zinc-900">
          {{ camera.status ?? 'online' }}
        </span>
      </div>

      <div class="absolute bottom-2 right-3 z-10">
        <span class="text-[8px] font-terminal text-[var(--s-dim)] uppercase bg-black/75 px-1.5 py-0.5 border border-zinc-900">
          REC // AUTO
        </span>
      </div>
    </div>

    <!-- Meta -->
    <div class="p-4 flex flex-col gap-1 relative">
      <div class="flex justify-between items-start">
        <h3 class="text-sm font-bold text-[var(--s-white)] font-terminal tracking-tight uppercase">
          {{ camera.name }}
        </h3>

        <!-- Context Menu -->
        <div class="relative" @click.stop>
          <button
            @click="$emit('edit', camera)"
            class="text-[var(--s-dim)] hover:text-[var(--s-white)] transition-colors p-1 text-[9px] font-terminal uppercase tracking-wider border border-[var(--s-line)] px-2"
          >
            Edit
          </button>
          <button
            @click="$emit('delete', camera.id)"
            class="ml-1 text-[var(--s-err)] hover:text-white hover:bg-red-950/30 transition-colors p-1 text-[9px] font-terminal uppercase tracking-wider border border-[var(--s-line)] px-2"
          >
            Del
          </button>
        </div>
      </div>
      <p class="text-[9px] font-terminal text-[var(--s-dim)] truncate">{{ camera.rtsp_url }}</p>
    </div>
  </div>
</template>
