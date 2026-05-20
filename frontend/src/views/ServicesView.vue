<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const isRunning = ref(false)
const logs = ref<string[]>([])
const isSaving = ref(false)
const saveSuccess = ref(false)

// Individual configuration fields
const recordEnabled = ref(false)
const recordFormat = ref('fmp4')
const recordPath = ref('./recordings/%v_%Y-%m-%d_%H-%M-%S_%f')
const recordSegmentDuration = ref('1h')

const logContainer = ref<HTMLDivElement | null>(null)

let pollInterval: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  await fetchStatus()
  await fetchConfig()
  await fetchLogs()
  scrollToBottom()

  // Poll status and logs to keep terminal real-time
  pollInterval = setInterval(async () => {
    await fetchStatus()
    await fetchLogs()
  }, 2000)
})

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})

const fetchStatus = async () => {
  try {
    const res = await fetch('/api/services/mediamtx/status')
    if (res.ok) {
      const data = await res.json()
      isRunning.value = data.running
    }
  } catch (err) {
    console.error('Status fetch error:', err)
  }
}

const fetchConfig = async () => {
  try {
    const res = await fetch('/api/services/mediamtx/config')
    if (res.ok) {
      const data = await res.json()
      recordEnabled.value = data.record
      recordFormat.value = data.recordFormat
      recordPath.value = data.recordPath
      recordSegmentDuration.value = data.recordSegmentDuration
    }
  } catch (err) {
    console.error('Config fetch error:', err)
  }
}

const fetchLogs = async () => {
  try {
    const res = await fetch('/api/services/mediamtx/logs')
    if (res.ok) {
      const data = await res.json()
      const prevLength = logs.value.length
      logs.value = data.logs
      if (logs.value.length !== prevLength) {
        await nextTick()
        scrollToBottom()
      }
    }
  } catch (err) {
    console.error('Logs fetch error:', err)
  }
}

const toggleService = async () => {
  try {
    const res = await fetch('/api/services/mediamtx/toggle', { method: 'POST' })
    if (res.ok) {
      const data = await res.json()
      isRunning.value = data.running
      await fetchLogs()
    }
  } catch (err) {
    console.error('Toggle error:', err)
  }
}

const restartService = async () => {
  try {
    const res = await fetch('/api/services/mediamtx/restart', { method: 'POST' })
    if (res.ok) {
      const data = await res.json()
      isRunning.value = data.running
      await fetchLogs()
    }
  } catch (err) {
    console.error('Restart error:', err)
  }
}

const saveConfig = async () => {
  isSaving.value = true
  saveSuccess.value = false
  try {
    const res = await fetch('/api/services/mediamtx/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        record: recordEnabled.value,
        recordFormat: recordFormat.value,
        recordPath: recordPath.value,
        recordSegmentDuration: recordSegmentDuration.value
      })
    })
    if (res.ok) {
      saveSuccess.value = true
      setTimeout(() => {
        saveSuccess.value = false
      }, 3000)
      await fetchConfig()
      await fetchLogs()
    }
  } catch (err) {
    console.error('Save error:', err)
  } finally {
    isSaving.value = false
  }
}

const scrollToBottom = () => {
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto flex flex-col min-h-screen">
    <!-- Header -->
    <div class="mb-10 flex flex-col md:flex-row md:items-end justify-between border-b border-[var(--s-line)] pb-6 gap-4">
      <div>
        <h2 class="text-3xl font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-tighter">
          Core Services Control
        </h2>
        <p class="text-[var(--s-mid)] font-terminal text-[10px] uppercase tracking-[0.2em] mt-1">
          Surveillance Node Operations // Process Controller
        </p>
      </div>
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Process.Manager</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">ONLINE</span>
      </div>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-8 flex-1 items-stretch">
      <!-- Left Panel: Status & Logs -->
      <div class="flex flex-col gap-6 h-full">
        <!-- Status Card -->
        <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] p-6">
          <div class="flex items-center justify-between border-b border-[var(--s-line2)] pb-4 mb-6">
            <div>
              <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider block">Service Unit</span>
              <h3 class="text-sm font-bold text-[var(--s-white)] uppercase tracking-tight font-terminal">
                MediaMTX RTSP Server
              </h3>
            </div>
            <!-- Status Badge -->
            <div class="flex items-center gap-2">
              <span 
                :class="[
                  'w-2 h-2 rounded-full',
                  isRunning ? 'bg-[var(--s-ok)] animate-pulse' : 'bg-[var(--s-err)]'
                ]"
              ></span>
              <span 
                :class="[
                  'text-xs font-bold font-terminal uppercase tracking-wider',
                  isRunning ? 'text-[var(--s-ok)]' : 'text-[var(--s-err)]'
                ]"
              >
                {{ isRunning ? 'Active (Running)' : 'Inactive (Stopped)' }}
              </span>
            </div>
          </div>

          <!-- Controls -->
          <div class="flex flex-wrap gap-4">
            <button 
              @click="toggleService"
              :class="[
                'px-4 py-2.5 text-xs font-terminal uppercase tracking-widest border transition-all cursor-pointer',
                isRunning 
                  ? 'border-[var(--s-err)] text-[var(--s-err)] bg-red-950/10 hover:bg-[var(--s-err)] hover:text-white' 
                  : 'border-[var(--s-ok)] text-[var(--s-ok)] bg-emerald-950/10 hover:bg-[var(--s-ok)] hover:text-white'
              ]"
            >
              {{ isRunning ? 'Stop Server' : 'Start Server' }}
            </button>

            <button 
              @click="restartService"
              class="px-4 py-2.5 text-xs font-terminal uppercase tracking-widest border border-[var(--s-line2)] bg-[var(--s-bg4)] text-[var(--s-white)] hover:bg-[var(--s-bg3)] transition-colors cursor-pointer"
            >
              Restart Server
            </button>
          </div>
        </div>

        <!-- Terminal Logs -->
        <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] flex-1 flex flex-col min-h-[300px] xl:min-h-0">
          <div class="bg-[var(--s-bg3)] border-b border-[var(--s-line2)] px-4 py-2.5 flex items-center justify-between">
            <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">
              System Log Buffer (MediaMTX STDOUT)
            </span>
            <button 
              @click="fetchLogs"
              class="text-[9px] font-terminal text-[var(--s-dim)] hover:text-[var(--s-white)] uppercase tracking-wider transition-colors cursor-pointer"
            >
              Refresh
            </button>
          </div>
          <!-- Output stream window -->
          <div 
            ref="logContainer"
            class="flex-1 p-4 bg-black font-terminal text-[11px] text-[var(--s-mid)] overflow-y-auto whitespace-pre-wrap leading-relaxed select-text min-h-[250px] xl:min-h-[400px] max-h-[600px] xl:max-h-[600px]"
          >
            <div v-for="(log, idx) in logs" :key="idx" class="border-b border-zinc-950 pb-0.5 mb-0.5">
              {{ log }}
            </div>
            <div v-if="logs.length === 0" class="text-[var(--s-dim)] uppercase tracking-widest text-center py-20">
              &gt; NO LOG RECORDS IN BUFFER
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: Structured Config Form -->
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] flex flex-col h-full">
        <div class="bg-[var(--s-bg3)] border-b border-[var(--s-line2)] px-4 py-2.5 flex items-center justify-between">
          <span class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">
            Configuration Panel (mediamtx.yml)
          </span>
          <span v-if="saveSuccess" class="text-[9px] font-terminal text-[var(--s-ok)] uppercase tracking-wider">
            Config Saved & Sync Completed!
          </span>
        </div>
        
        <div class="p-6 flex-1 flex flex-col justify-between gap-6">
          <div class="space-y-6">
            <p class="text-[10px] font-terminal text-[var(--s-dim)] uppercase leading-relaxed mb-4">
              CONFIGURE CORE RECORDING AND PATH STREAM PROPERTIES. DATABASE CAMERAS ARE AUTOMATICALLY PARSED AND MERGED TO CONFIG STREAM PATHS ON SAVE.
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
                <span :class="['w-4 h-4 transition-colors', recordEnabled ? 'bg-[var(--s-ok)]' : 'bg-[var(--s-mid)]']"></span>
              </button>
            </div>

            <!-- Record Format Input -->
            <div class="flex flex-col gap-1.5">
              <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Record Format</label>
              <input 
                v-model="recordFormat"
                type="text"
                placeholder="e.g. fmp4"
                class="bg-black border border-[var(--s-line)] p-3 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)]"
              />
            </div>

            <!-- Record Path Input -->
            <div class="flex flex-col gap-1.5">
              <label class="text-[9px] font-terminal text-[var(--s-mid)] uppercase tracking-wider">Record Path Template</label>
              <input 
                v-model="recordPath"
                type="text"
                placeholder="e.g. ./recordings/%v_%Y-%m-%d_%H-%M-%S_%f"
                class="bg-black border border-[var(--s-line)] p-3 text-xs font-terminal text-[var(--s-white)] focus:outline-none focus:border-[var(--s-mid)]"
              />
            </div>

            <!-- Record Segment Duration Input -->
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
              @click="saveConfig"
              :disabled="isSaving"
              class="px-5 py-3 border border-[var(--s-line2)] bg-[var(--s-bg4)] hover:bg-[var(--s-bg3)] disabled:opacity-50 text-xs font-terminal text-[var(--s-white)] uppercase tracking-wider transition-colors cursor-pointer"
            >
              {{ isSaving ? 'Saving & Syncing...' : 'Save Config & Auto-Sync paths' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
