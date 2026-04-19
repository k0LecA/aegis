<template>
  <div class="flex-1 p-10 flex flex-col items-center justify-center text-center bg-[var(--s-bg)]">
    <div class="w-20 h-20 border border-[var(--s-line)] bg-[var(--s-bg2)] flex items-center justify-center mb-6">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--s-white)]">
        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
        <circle cx="12" cy="12" r="3"/>
      </svg>
    </div>
    <h2 class="text-2xl font-bold text-[var(--s-white)] mb-2 uppercase font-[var(--font-sans)] tracking-tight">System Settings</h2>
    <p class="text-[var(--s-mid)] max-w-sm font-terminal text-xs uppercase tracking-wider mb-8">Node configuration is strictly restricted to Level 4 clearance. Access denied.</p>
    
    <div class="w-full max-w-md border border-[var(--s-line)] bg-[var(--s-bg2)] p-4 font-terminal text-[10px] text-left">
      <div class="flex justify-between border-b border-[var(--s-line)] pb-2 mb-2">
        <span class="text-[var(--s-dim)]">BUILD_ID</span>
        <span class="text-[var(--s-mid)]">AEGIS_PROD_0419</span>
      </div>
      <div class="flex justify-between border-b border-[var(--s-line)] pb-2 mb-2">
        <span class="text-[var(--s-dim)]">KERNEL</span>
        <span class="text-[var(--s-mid)]">0.9.4-SECURE</span>
      </div>
      <div class="flex justify-between">
        <span class="text-[var(--s-dim)]">ENCRYPTION</span>
        <span class="text-[var(--s-ok)]">AES-256-GCM_ACTIVE</span>
      </div>
    </div>
  </div>
</template>
