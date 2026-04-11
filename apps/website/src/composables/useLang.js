import { ref } from 'vue'

// Module-level singleton — all components share the same ref
const _lang = ref(
  (typeof localStorage !== 'undefined' && localStorage.getItem('au-lang')) || 'zh'
)

export function useLang() {
  function toggleLang() {
    _lang.value = _lang.value === 'zh' ? 'en' : 'zh'
    localStorage.setItem('au-lang', _lang.value)
  }
  return { lang: _lang, toggleLang }
}
