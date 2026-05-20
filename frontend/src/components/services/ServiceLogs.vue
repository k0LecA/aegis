<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

const props = defineProps<{ logs: string[] }>()

const logContainer = ref<HTMLDivElement | null>(null)

function scrollToBottom() {
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

// Auto-scroll when new logs arrive
watch(() => props.logs.length, async () => {
  await nextTick()
  scrollToBottom()
})
</script>

<template>
  <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] flex flex-col min-h-[300px] xl:min-h-0 flex-1">
    <!-- Toolbar -->
    <div class="bg-[var(--s-bg3)] border-b border-[var(--s-line2)] px-4 py-2.5 flex items-center justify-between">
      <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">
        System Log Buffer (MediaMTX STDOUT)
      </span>
    </div>

    <!-- Log output -->
    <div
      ref="logContainer"
      class="flex-1 p-4 bg-black font-terminal text-[11px] text-[var(--s-mid)] overflow-y-auto whitespace-pre-wrap leading-relaxed select-text min-h-[250px] xl:min-h-[400px] max-h-[600px] scrollbar-thin"
    >
      <div v-for="(log, idx) in logs" :key="idx" class="border-b border-zinc-950 pb-0.5 mb-0.5">
        {{ log }}
      </div>
      <div v-if="logs.length === 0" class="text-[var(--s-dim)] uppercase tracking-widest text-center py-20">
        &gt; NO LOG RECORDS IN BUFFER
      </div>
    </div>
  </div>
</template>
