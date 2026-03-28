<script setup lang="ts">
  const streamUrl = "http://127.0.0.1:8000/video_feed";
</script>

<template>
  <section id="center">
    <img :src="streamUrl" alt="AEGIS Live Feed" class="camera-stream" />
  </section>
</template>

<style scoped>
  .camera-stream {
    border: 2px solid #555;
    border-radius: 4px;
    width: 100%;
    max-width: 800px;
  }
</style>