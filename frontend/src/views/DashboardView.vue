<script setup lang="ts">
const stats = [
  { name: 'Active Cameras', value: '12', trend: '+2', iconPath: 'M23 7l-7 5 7 5V7z M1 5h15v14H1z' },
  { name: 'Storage Used', value: '64%', trend: 'Stable', iconPath: 'M21 12V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h7 M16 5V3 M8 5V3' },
  { name: 'Alerts (24h)', value: '4', trend: '-15%', iconPath: 'M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z M12 9v4 M12 17h.01' },
]

const token = localStorage.getItem('user-token');

const streamUrl = `http://localhost:8889/mystream?user=${token}&password=unused`;
</script>

<template>
  <div class="flex-1 p-10 overflow-auto bg-slate-900/50">
    <header class="mb-10 flex justify-between items-end">
      <div>
        <h2 class="text-4xl font-extrabold text-white tracking-tight">Security Overview</h2>
        <p class="text-white/40 mt-1">Welcome back, Agent. Everything looks secure.</p>
      </div>
      <div class="glass px-4 py-2 rounded-lg text-sm font-medium text-white/60">
        Mon, April 13, 2026
      </div>
    </header>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <div v-for="stat in stats" :key="stat.name" class="glass rounded-3xl p-6 transition-transform hover:scale-[1.02] cursor-default border border-white/5">
        <div class="flex justify-between items-start mb-4">
          <div class="p-3 bg-white/5 rounded-2xl">
             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary">
               <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
             </svg>
          </div>
          <span :class="['text-xs font-bold px-2 py-1 rounded-full', stat.trend.startsWith('+') ? 'bg-accent/10 text-accent' : 'bg-white/5 text-white/40']">
            {{ stat.trend }}
          </span>
        </div>
        <p class="text-sm font-medium text-white/40 mb-1">{{ stat.name }}</p>
        <p class="text-3xl font-bold text-white">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Live Preview Placeholder -->
    <div class="glass rounded-[2rem] p-8 border border-white/10 min-h-[400px] flex flex-col">
      <div class="flex items-center justify-between mb-8">
        <h3 class="text-xl font-bold text-white">Live Feed (Priority)</h3>
        <button class="text-xs font-bold text-primary uppercase tracking-widest hover:text-white transition-colors">View All Streams</button>
      </div>
      <div class="flex-1 rounded-2xl bg-black/40 border border-white/5 flex items-center justify-center relative overflow-hidden group">
        <iframe 
            src=streamUrl
            width="640" 
            height="480" 
            allow="autoplay; fullscreen" 
            style="border: none;">
        </iframe>
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
           <p class="text-white text-sm font-medium">Main Entrance - Cam 01</p>
        </div>
        
      </div>
    </div>
  </div>
</template>
