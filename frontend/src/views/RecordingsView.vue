<script setup lang="ts">
import { onMounted } from 'vue'
import PageHeader      from '@/components/ui/PageHeader.vue'
import RecordingsTable from '@/components/recordings/RecordingsTable.vue'
import { useCameraStore }    from '@/stores/cameras'
import { useRecordingStore } from '@/stores/recordings'

const cameraStore    = useCameraStore()
const recordingStore = useRecordingStore()

// Both load-once — recordings fetch also triggers FS sync on backend
onMounted(() => Promise.all([cameraStore.load(), recordingStore.load()]))
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto scrollbar-thin">
    <PageHeader
      title="Archived Segment Logs"
      :subtitle="`Sector Archives // Total Segments: ${recordingStore.recordings.length}`"
    >
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Storage.Status</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">ONLINE // NORMAL</span>
      </div>
    </PageHeader>

    <RecordingsTable
      :recordings="recordingStore.recordings"
      :cameras="cameraStore.cameras"
      @delete="recordingStore.remove"
      @download="recordingStore.download"
    />
  </div>
</template>
