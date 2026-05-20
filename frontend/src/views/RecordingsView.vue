<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageHeader       from '@/components/ui/PageHeader.vue'
import RecordingsTable  from '@/components/recordings/RecordingsTable.vue'
import { fetchCameras, fetchRecordings, deleteRecording, getDownloadUrl } from '@/api'
import type { Camera, Recording } from '@/types'

const cameras    = ref<Camera[]>([])
const recordings = ref<Recording[]>([])

onMounted(async () => {
  try {
    [cameras.value, recordings.value] = await Promise.all([
      fetchCameras(),
      fetchRecordings(),
    ])
  } catch (err) {
    console.error('Recordings load error:', err)
  }
})

async function handleDelete(id: string) {
  await deleteRecording(id)
  recordings.value = recordings.value.filter(r => r.id !== id)
}

function handleDownload(id: string) {
  window.open(getDownloadUrl(id), '_blank')
}
</script>

<template>
  <div class="flex-1 p-6 lg:p-10 bg-[var(--s-bg)] overflow-y-auto scrollbar-thin">
    <PageHeader
      title="Archived Segment Logs"
      :subtitle="`Sector Archives // Total Segments: ${recordings.length}`"
    >
      <div class="text-right hidden md:block">
        <span class="text-[9px] font-terminal text-[var(--s-dim)] block uppercase">Storage.Status</span>
        <span class="text-[var(--s-ok)] font-terminal text-xs">ONLINE // NORMAL</span>
      </div>
    </PageHeader>

    <RecordingsTable
      :recordings="recordings"
      :cameras="cameras"
      @delete="handleDelete"
      @download="handleDownload"
    />
  </div>
</template>
