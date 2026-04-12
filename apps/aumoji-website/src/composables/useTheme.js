import { ref } from 'vue'

// Module-level singleton — all components share the same ref
const _theme = ref(
  (typeof localStorage !== 'undefined' && localStorage.getItem('au-theme')) || 'dark'
)

// Apply immediately on module load (before first render)
if (typeof document !== 'undefined') {
  document.documentElement.setAttribute('data-theme', _theme.value)
}

export function useTheme() {
  function toggleTheme() {
    _theme.value = _theme.value === 'dark' ? 'light' : 'dark'
    document.documentElement.setAttribute('data-theme', _theme.value)
    localStorage.setItem('au-theme', _theme.value)
  }
  return { theme: _theme, toggleTheme }
}
