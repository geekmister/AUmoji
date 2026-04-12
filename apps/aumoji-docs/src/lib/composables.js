import { ref, watch } from 'vue'

const _theme = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('au-theme') || 'dark' : 'dark')
const _lang = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('au-lang') || 'zh' : 'zh')

// 立即应用主题到 HTML
if (typeof document !== 'undefined') {
  document.documentElement.setAttribute('data-theme', _theme.value)
}

export function useTheme() {
  function toggleTheme() {
    _theme.value = _theme.value === 'dark' ? 'light' : 'dark'
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('au-theme', _theme.value)
    }
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', _theme.value)
    }
  }
  return { theme: _theme, toggleTheme }
}

export function useLang() {
  function toggleLang() {
    _lang.value = _lang.value === 'zh' ? 'en' : 'zh'
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('au-lang', _lang.value)
    }
  }
  return { lang: _lang, toggleLang }
}
