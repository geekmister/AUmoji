<template>
  <div>
    <!-- Sticky Nav -->
    <nav class="site-nav">
      <div class="nav-inner">
        <RouterLink to="/" class="nav-logo" style="text-decoration:none">
          <span style="font-size:22px">🎭</span>
          <span style="font-weight:700; font-size:15px; color:var(--tx)">AUmoji</span>
        </RouterLink>

        <div class="nav-right">
          <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">
            {{ lang === 'zh' ? '首页' : 'Home' }}
          </RouterLink>
          <RouterLink to="/playground" class="nav-link" :class="{ active: $route.path === '/playground' }">Playground</RouterLink>
          <RouterLink to="/docs" class="nav-link" :class="{ active: $route.path === '/docs' }">
            {{ lang === 'zh' ? 'AU 文档' : 'AU Docs' }}
          </RouterLink>

          <div class="nav-sep"></div>

          <button
            class="nav-icon-btn"
            @click="toggleTheme"
            :title="theme === 'dark' ? (lang === 'zh' ? '切换浅色' : 'Switch to Light') : (lang === 'zh' ? '切换深色' : 'Switch to Dark')"
          >{{ theme === 'dark' ? '☀️' : '🌙' }}</button>

          <button
            class="nav-icon-btn nav-lang-btn"
            @click="toggleLang"
            :title="lang === 'zh' ? 'Switch to English' : '切换中文'"
          >{{ lang === 'zh' ? 'EN' : '中' }}</button>

          <a href="https://github.com/Geekmister/AUmoji" target="_blank" rel="noopener" class="nav-link nav-github">
            <i class="fa-brands fa-github"></i> GitHub
          </a>
        </div>
      </div>
    </nav>

    <!-- Page content -->
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useTheme } from './composables/useTheme.js'
import { useLang }  from './composables/useLang.js'

const { theme, toggleTheme } = useTheme()
const { lang, toggleLang }   = useLang()
</script>

<style scoped>
.nav-logo {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 2px;
}

.nav-link {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 5px 12px; border-radius: 8px; font-size: 13.5px;
  font-weight: 500; color: var(--tx2); text-decoration: none;
  transition: color var(--ease), background var(--ease);
}
.nav-link:hover, .nav-link.active {
  color: var(--tx);
  background: var(--hover-bg);
}

.nav-sep {
  width: 1px;
  height: 16px;
  background: var(--divider);
  margin: 0 6px;
  flex-shrink: 0;
}

.nav-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px; height: 34px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--tx2);
  font-size: 15px;
  cursor: pointer;
  transition: background var(--ease), color var(--ease);
  font-family: inherit;
}
.nav-icon-btn:hover { background: var(--hover-bg); color: var(--tx); }

.nav-lang-btn {
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.nav-inner {
  max-width: 1152px;
  margin: 0 auto;
  padding: 0 20px;
  height: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
