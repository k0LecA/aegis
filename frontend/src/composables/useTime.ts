// Provides a reactive clock string that ticks every second.
import { ref, onMounted, onUnmounted } from 'vue'

export function useTime() {
  const currentTime = ref('')

  function tick() {
    const now = new Date()
    const pad = (n: number) => String(n).padStart(2, '0')
    currentTime.value = [
      `${now.getFullYear()}.${pad(now.getMonth() + 1)}.${pad(now.getDate())}`,
      '//',
      `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`,
    ].join(' ')
  }

  let interval: ReturnType<typeof setInterval> | null = null

  onMounted(() => {
    tick()
    interval = setInterval(tick, 1000)
  })

  onUnmounted(() => {
    if (interval) clearInterval(interval)
  })

  return { currentTime }
}
