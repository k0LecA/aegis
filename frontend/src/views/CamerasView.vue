<template>
  <div class="flex-1 p-10 flex flex-col items-center justify-center text-center bg-[var(--s-bg)]">
    <div class="w-20 h-20 border border-[var(--s-line)] bg-[var(--s-bg2)] flex items-center justify-center mb-6">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
        <path d="M23 7l-7 5 7 5V7z"/>
        <rect width="15" height="14" x="1" y="5" rx="0" ry="0"/>
      </svg>
    </div>
    <h2 class="text-2xl font-bold text-[var(--s-white)] mb-2 uppercase font-[var(--font-sans)] tracking-tight">Camera Network</h2>
    <p class="text-[var(--s-mid)] max-w-sm font-terminal text-xs uppercase tracking-wider mb-8">The camera configuration module is currently under encryption review. Monitoring offline.</p>
    
    <!-- Status Demonstration -->
    <div class="grid grid-cols-3 gap-8 border-t border-[var(--s-line)] pt-8">
      <div class="flex flex-col items-center gap-2">
        <div class="w-3 h-3 bg-[var(--s-ok)]"></div>
        <span class="text-[9px] font-terminal text-[var(--s-dim)] uppercase">Stream.01</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <div class="w-3 h-3 bg-[var(--s-warn)]"></div>
        <span class="text-[9px] font-terminal text-[var(--s-dim)] uppercase">Stream.02</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <div class="w-3 h-3 bg-[var(--s-err)]"></div>
        <span class="text-[9px] font-terminal text-[var(--s-dim)] uppercase">Stream.03</span>
      </div>
    </div>
  </div>
</template>
