<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Camera, Recording } from '@/types'
import { formatDate, formatBytes } from '@/composables/useFormat'

const props = defineProps<{
  recordings: Recording[]
  cameras:    Camera[]
}>()

const emit = defineEmits<{
  (e: 'delete',   id: string): void
  (e: 'download', id: string): void
}>()

// Build a quick id→name lookup
const cameraMap = computed(() =>
  Object.fromEntries(props.cameras.map(c => [c.id, c.name]))
)

const selectedCameraId = ref<string>('ALL')
const filterDate       = ref<string>('')

const filtered = computed(() =>
  props.recordings.filter(rec => {
    const matchCamera = selectedCameraId.value === 'ALL' || rec.camera_id === selectedCameraId.value
    const matchDate   = !filterDate.value || new Date(rec.started_at).toISOString().split('T')[0] === filterDate.value
    return matchCamera && matchDate
  })
)

function clearFilters() {
  selectedCameraId.value = 'ALL'
  filterDate.value = ''
}
</script>

<template>
  <div>
    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-8 p-4 bg-[var(--s-bg2)] border border-[var(--s-line)]">
      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Filter Node</label>
        <select
          v-model="selectedCameraId"
          class="bg-[var(--s-bg)] border border-[var(--s-line)] p-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer"
        >
          <option value="ALL">ALL NODES</option>
          <option v-for="cam in cameras" :key="cam.id" :value="cam.id">{{ cam.name }}</option>
        </select>
      </div>

      <div class="flex flex-col gap-1.5">
        <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Select Date</label>
        <input
          v-model="filterDate"
          type="date"
          class="bg-[var(--s-bg)] border border-[var(--s-line)] p-2 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)] cursor-pointer"
          style="color-scheme: dark;"
        />
      </div>

      <div v-if="selectedCameraId !== 'ALL' || filterDate" class="flex flex-col justify-end">
        <button
          @click="clearFilters"
          class="border border-[var(--s-line)] bg-transparent px-4 py-2 text-[9px] font-terminal text-[var(--s-mid)] hover:text-white hover:bg-[var(--s-bg3)] uppercase tracking-widest transition-colors cursor-pointer"
        >
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] overflow-x-auto">
      <table class="w-full text-left border-collapse font-terminal text-xs">
        <thead>
          <tr class="border-b border-[var(--s-line2)] text-[var(--s-mid)] uppercase tracking-wider text-[10px] bg-[var(--s-bg3)]">
            <th class="p-4 font-semibold">Node</th>
            <th class="p-4 font-semibold">Started At</th>
            <th class="p-4 font-semibold">Ended At</th>
            <th class="p-4 font-semibold">Size</th>
            <th class="p-4 font-semibold">File Path</th>
            <th class="p-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="rec in filtered"
            :key="rec.id"
            class="border-b border-[var(--s-line)] hover:bg-[var(--s-bg3)] transition-colors"
          >
            <td class="p-4 font-bold text-[var(--s-white)] uppercase">
              {{ cameraMap[rec.camera_id] ?? 'UNKNOWN_NODE' }}
            </td>
            <td class="p-4 text-[var(--s-mid)]">{{ formatDate(rec.started_at) }}</td>
            <td class="p-4 text-[var(--s-mid)]">{{ formatDate(rec.ended_at) }}</td>
            <td class="p-4 text-[var(--s-mid)]">{{ formatBytes(rec.size_bytes) }}</td>
            <td class="p-4 text-[var(--s-dim)] truncate max-w-xs" :title="rec.file_path">
              {{ rec.file_path }}
            </td>
            <td class="p-4 text-right flex justify-end gap-3">
              <button
                @click="$emit('download', rec.id)"
                class="px-2 py-1 border border-[var(--s-line2)] text-[9px] font-semibold text-[var(--s-white)] hover:bg-white hover:text-black uppercase tracking-wider transition-colors cursor-pointer"
              >
                Download
              </button>
              <button
                @click="$emit('delete', rec.id)"
                class="px-2 py-1 border border-red-950/40 text-[9px] font-semibold text-[var(--s-err)] hover:bg-red-950/30 uppercase tracking-wider transition-colors cursor-pointer"
              >
                Delete
              </button>
            </td>
          </tr>

          <tr v-if="filtered.length === 0">
            <td colspan="6" class="p-12 text-center text-[var(--s-dim)] uppercase tracking-widest font-terminal text-[10px]">
              &gt; NO RECORDED SEGMENTS LOCATED IN SECTOR // SYSTEM IDLE
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
