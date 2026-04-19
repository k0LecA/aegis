<script setup lang="ts">
const stats = [
  { name: 'Active Cameras', value: '12', trend: '+2', iconPath: 'M23 7l-7 5 7 5V7z M1 5h15v14H1z' },
  { name: 'Storage Used', value: '64%', trend: 'Stable', iconPath: 'M21 12V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h7 M16 5V3 M8 5V3' },
  { name: 'Alerts (24h)', value: '4', trend: '-15%', iconPath: 'M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z M12 9v4 M12 17h.01' },
]

const token = localStorage.getItem('user-token');

const streamUrl = `http://localhost:8889/mystream?user=${token}`;
</script>

<template>
  <div class="flex-1 p-10 overflow-auto bg-[var(--s-bg)]">
    <header class="mb-10 flex justify-between items-end">
      <div>
        <h2 class="text-4xl font-bold text-[var(--s-white)] tracking-tight uppercase font-[var(--font-sans)]">Security Overview</h2>
        <p class="text-[var(--s-dim)] mt-1 font-terminal text-sm uppercase tracking-wider">Welcome back, Agent. Status: Nominal.</p>
      </div>
      <div class="border border-[var(--s-line)] bg-[var(--s-bg2)] px-4 py-2 text-xs font-medium text-[var(--s-mid)] font-terminal uppercase">
        2026.04.13 // 22:48:16
      </div>
    </header>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <div v-for="stat in stats" :key="stat.name" class="s-card p-6 cursor-default">
        <div class="flex justify-between items-start mb-4">
          <div class="p-3 border border-[var(--s-line)] bg-[var(--s-bg3)]">
             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
               <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
             </svg>
          </div>
          <span :class="['text-[10px] font-bold px-2 py-1 font-terminal', stat.trend.startsWith('+') ? 'text-[var(--s-ok)]' : 'text-[var(--s-dim)]']">
            {{ stat.trend }}
          </span>
        </div>
        <p class="text-[10px] font-medium text-[var(--s-dim)] mb-1 font-terminal uppercase tracking-wider">{{ stat.name }}</p>
        <p class="text-3xl font-bold text-[var(--s-white)] font-[var(--font-sans)] uppercase tracking-tight">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Live Preview Placeholder -->
    <div class="s-card p-8 min-h-[400px] flex flex-col">
      <div class="flex items-center justify-between mb-8">
        <h3 class="text-lg font-bold text-[var(--s-white)] uppercase font-[var(--font-sans)] tracking-wider">Live Feed // Secondary Cluster</h3>
        <button class="text-[10px] font-bold text-[var(--s-mid)] uppercase tracking-widest hover:text-[var(--s-white)] transition-colors font-terminal">Expand _All_Streams</button>
      </div>
      <div class="flex-1 bg-[var(--s-bg)] border border-[var(--s-line)] flex items-center justify-center relative overflow-hidden group">
        <iframe 
            :src="streamUrl"
            width="640" 
            height="480" 
            allow="autoplay; fullscreen" 
            style="border: none; filter: contrast(1.1) brightness(1.1) grayscale(1);">
        </iframe>
        <div class="absolute inset-0 bg-gradient-to-t from-[var(--s-bg)] via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
           <p class="text-[var(--s-white)] text-xs font-medium font-terminal uppercase tracking-widest">Main Entrance - Cam 01</p>
        </div>
      </div>
    </div>
  </div>
</template>
