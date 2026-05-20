<script setup lang="ts">
import { ref, watch } from 'vue'
import type { MediaMTXConfig } from '@/types'

const props = defineProps<{
  config:      MediaMTXConfig
  isSaving:    boolean
  saveSuccess: boolean
}>()

const emit = defineEmits<{ (e: 'save', config: MediaMTXConfig): void }>()

// Local copies so the form is editable without mutating props
const recordEnabled         = ref(props.config.record)
const recordFormat          = ref(props.config.recordFormat)
const recordPath            = ref(props.config.recordPath)
const recordSegmentDuration = ref(props.config.recordSegmentDuration)

// Sync if parent updates the config (e.g. after a fetch)
watch(() => props.config, (cfg) => {
  recordEnabled.value         = cfg.record
  recordFormat.value          = cfg.recordFormat
  recordPath.value            = cfg.recordPath
  recordSegmentDuration.value = cfg.recordSegmentDuration
})

function submit() {
  emit('save', {
    record:                recordEnabled.value,
    recordFormat:          recordFormat.value,
    recordPath:            recordPath.value,
    recordSegmentDuration: recordSegmentDuration.value,
  })
}
</script>

<template>
  <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] flex flex-col h-full">
    <!-- Header -->
    <div class="bg-[var(--s-bg3)] border-b border-[var(--s-line2)] px-4 py-2.5 flex items-center justify-between">
      <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">
        Configuration Panel (mediamtx.yml)
      </span>
      <span v-if="saveSuccess" class="text-[9px] font-terminal text-[var(--s-ok)] uppercase tracking-wider">
        Config Saved &amp; Sync Completed!
      </span>
    </div>

    <div class="p-6 flex-1 flex flex-col justify-between gap-6">
      <div class="space-y-6">
        <p class="text-[10px] font-terminal text-[var(--s-dim)] uppercase leading-relaxed mb-4">
          Configure core recording and path stream properties. Database cameras are automatically parsed and merged to config stream paths on save.
        </p>

        <!-- Enable Recording Toggle -->
        <div class="flex items-center justify-between border border-[var(--s-line)] bg-black p-4">
          <div class="flex flex-col">
            <span class="text-xs font-bold font-terminal text-[var(--s-white)] uppercase">Enable Video Recording</span>
            <span class="text-[8px] font-terminal text-[var(--s-dim)] uppercase mt-0.5">Key: record (yes/no)</span>
          </div>
          <button
            @click="recordEnabled = !recordEnabled"
            :class="[
              'w-12 h-6 border transition-colors flex items-center px-1 cursor-pointer',
              recordEnabled ? 'bg-[var(--s-ok)]/20 border-[var(--s-ok)] justify-end' : 'bg-zinc-950 border-[var(--s-line)] justify-start'
            ]"
          >
            <span :class="['w-4 h-4 transition-colors', recordEnabled ? 'bg-[var(--s-ok)]' : 'bg-[var(--s-mid)]']" />
          </button>
        </div>

        <!-- Record Format -->
        <div class="flex flex-col gap-1.5">
          <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Record Format</label>
          <input
            v-model="recordFormat"
            type="text"
            placeholder="e.g. fmp4"
            class="bg-black border border-[var(--s-line)] p-3 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)]"
          />
        </div>

        <!-- Record Path -->
        <div class="flex flex-col gap-1.5">
          <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Record Path Template</label>
          <input
            v-model="recordPath"
            type="text"
            placeholder="e.g. ./recordings/%path/%v_%Y-%m-%d_%H-%M-%S_%f"
            class="bg-black border border-[var(--s-line)] p-3 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)]"
          />
        </div>

        <!-- Segment Duration -->
        <div class="flex flex-col gap-1.5">
          <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Record Segment Duration</label>
          <input
            v-model="recordSegmentDuration"
            type="text"
            placeholder="e.g. 1h"
            class="bg-black border border-[var(--s-line)] p-3 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)]"
          />
        </div>
      </div>

      <div class="flex items-center justify-between gap-4 mt-6 border-t border-[var(--s-line)] pt-4">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] uppercase">
          STATUS: {{ isSaving ? 'SYNCHRONIZING...' : 'READY' }}
        </span>
        <button
          @click="submit"
          :disabled="isSaving"
          class="px-5 py-3 border border-[var(--s-line2)] bg-[var(--s-bg4)] hover:bg-[var(--s-bg3)] disabled:opacity-50 text-xs font-terminal text-[var(--s-white)] uppercase tracking-wider transition-colors cursor-pointer"
        >
          {{ isSaving ? 'Saving & Syncing...' : 'Save Config & Auto-Sync Paths' }}
        </button>
      </div>
    </div>
  </div>
</template>
