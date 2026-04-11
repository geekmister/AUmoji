<template>
  <div>
    <!-- Sticky Nav -->
    <nav class="site-nav">
      <div class="nav-inner">
        <RouterLink to="/" class="flex items-center gap-2 no-underline">
          <span style="font-size:22px">🎭</span>
          <span class="font-bold text-base" style="color:var(--tx)">AUmoji</span>
        </RouterLink>

        <div class="flex items-center gap-1">
          <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</RouterLink>
          <RouterLink to="/playground" class="nav-link" :class="{ active: $route.path === '/playground' }">Playground</RouterLink>
          <RouterLink to="/docs" class="nav-link" :class="{ active: $route.path === '/docs' }">AU 文档</RouterLink>
          <a href="https://github.com/Geekmister/AUmoji" target="_blank" rel="noopener" class="nav-link" style="gap:4px">
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
</script>

<style scoped>
.nav-link {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 5px 12px; border-radius: 8px; font-size: 13.5px;
  font-weight: 500; color: var(--tx2); text-decoration: none;
  transition: color var(--ease), background var(--ease);
}
.nav-link:hover, .nav-link.active { color: var(--tx); background: rgba(255,255,255,0.06); }

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
