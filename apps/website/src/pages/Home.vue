<template>
  <div>
    <!-- ══ HERO ══ 纯居中文字，不含 picker -->
    <section class="hero-section">
      <div class="orb orb1"></div>
      <div class="orb orb2"></div>
      <div class="orb orb3"></div>

      <div class="hero-inner">
        <div class="badge" style="margin-bottom:28px">✨ &nbsp;影视级 FACS 表情系统 · Vue 3</div>

        <h1 class="hero-title">
          <span class="grad-text">AU 表情</span>选择器<br>
          <span style="font-size:0.65em; font-weight:700; color:var(--tx2)">为 AI 视频创作者打造</span>
        </h1>

        <p class="hero-sub">
          基于 FACS 面部动作编码系统，精准控制 21 种影视级表情。<br>
          轻量、可配置、开箱即用，Vue 3 零运行时依赖。
        </p>

        <div class="hero-ctas">
          <a href="#demo" class="btn btn-primary">试一试 ↓</a>
          <a href="https://github.com/Geekmister/AUmoji" target="_blank" rel="noopener" class="btn btn-outline">
            <i class="fa-brands fa-github"></i> GitHub
          </a>
          <RouterLink to="/playground" class="btn btn-outline">🎮 Playground</RouterLink>
        </div>

        <div class="hero-stats">
          <span>📦 &nbsp;零运行时依赖</span>
          <span class="stat-sep">·</span>
          <span>🎭 &nbsp;21 个表情</span>
          <span class="stat-sep">·</span>
          <span>🌍 &nbsp;中 / EN 双语</span>
          <span class="stat-sep">·</span>
          <span>🎨 &nbsp;Light / Dark</span>
        </div>

        <!-- Badges -->
        <div class="hero-badges">
          <img src="https://img.shields.io/npm/v/aumoji-picker?style=flat-square&color=8b5cf6" alt="npm version" height="20" loading="lazy">
          <img src="https://img.shields.io/npm/dm/aumoji-picker?style=flat-square&color=6366f1&label=downloads%2Fmo" alt="npm downloads" height="20" loading="lazy">
          <img src="https://img.shields.io/github/stars/Geekmister/AUmoji?style=flat-square&color=8b5cf6" alt="GitHub stars" height="20" loading="lazy">
          <img src="https://img.shields.io/github/license/Geekmister/AUmoji?style=flat-square&color=64748b" alt="license" height="20" loading="lazy">
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- ══ DEMO ══ picker 独立全宽展示区 -->
    <section id="demo" class="demo-section">
      <div class="section-hd">
        <h2>在线演示</h2>
        <p>实时切换主题与语言，选择表情查看 AU 编号与 AI 提示词</p>
      </div>

      <div class="demo-body">
        <!-- Picker -->
        <div class="demo-picker-wrap">
          <AUmojiPicker
            :theme="demoTheme"
            :lang="demoLang"
            :width="360"
            :height="460"
            @select="onDemoSelect"
          />
          <div class="demo-controls">
            <button class="demo-toggle" @click="demoTheme = demoTheme === 'dark' ? 'light' : 'dark'">
              {{ demoTheme === 'dark' ? '☀️ Light' : '🌙 Dark' }}
            </button>
            <button class="demo-toggle" @click="demoLang = demoLang === 'zh' ? 'en' : 'zh'">
              🌐 {{ demoLang === 'zh' ? 'EN' : '中文' }}
            </button>
          </div>
        </div>

        <!-- Output panel -->
        <div class="demo-output">
          <p class="demo-output-label">😊 &nbsp;{{ demoLang === 'zh' ? '选择表情查看输出' : "What's Your Mood?" }}</p>
          <template v-if="lastSelected">
            <div class="output-em">{{ lastSelected.emoji }}</div>
            <div class="output-name">{{ lastSelected.name }}</div>
            <div class="output-name-en">{{ lastSelected.nameEn }}</div>
            <code class="output-code-badge">{{ lastSelected.auCode }}</code>
            <p class="output-desc">{{ demoLang === 'zh' ? lastSelected.desc : lastSelected.descEn }}</p>
          </template>
          <p v-else class="output-hint">点击左侧表情卡片</p>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- ══ FEATURES ══ -->
    <section class="features-section">
      <div class="section-wrap-lg">
        <div class="section-hd">
          <h2>为什么选择 AUmoji</h2>
          <p>专为 AI 视频与影视制作工作流设计</p>
        </div>

        <div class="feat-grid" ref="featsRef">
          <div
            v-for="(feat, i) in features"
            :key="feat.title"
            class="feat-card will-reveal"
            :style="{ transitionDelay: i * 90 + 'ms' }"
          >
            <div class="feat-icon">{{ feat.icon }}</div>
            <h3 style="font-size:15px; margin-bottom:8px;">{{ feat.title }}</h3>
            <p style="font-size:13px; color:var(--tx2); line-height:1.6">{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- ══ QUICK START ══ -->
    <section class="qs-section">
      <div class="section-wrap-sm">
        <div class="section-hd">
          <h2>快速开始</h2>
          <p>三步集成到你的项目</p>
        </div>

        <div class="qs-steps">
          <div class="card" style="padding:24px">
            <p class="step-label">① 安装</p>
            <div class="install-tabs mt-3">
              <button
                v-for="pm in ['npm','pnpm','yarn']" :key="pm"
                :class="['install-tab', installTab === pm && 'active']"
                @click="installTab = pm"
              >{{ pm }}</button>
            </div>
            <div class="code-block install-code">{{ installCmds[installTab] }}</div>
          </div>
          <div class="card" style="padding:24px">
            <p class="step-label">② 引入组件</p>
            <div class="code-block mt-3">{{ importCode }}</div>
          </div>
          <div class="card" style="padding:24px">
            <p class="step-label">③ 使用</p>
            <div class="code-block mt-3">{{ usageCode }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ FOOTER ══ -->
    <footer class="site-footer">
      AUmoji © 2025 &nbsp;·&nbsp; 开源免费 &nbsp;·&nbsp; 基于 FACS for AI 创作者 &nbsp;·&nbsp;
      <a href="https://github.com/Geekmister/AUmoji" target="_blank" rel="noopener" class="footer-link">GitHub ↗</a>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { AUmojiPicker } from 'aumoji-picker'

const demoTheme    = ref('dark')
const demoLang     = ref('zh')
const lastSelected = ref(null)
const featsRef     = ref(null)
const installTab   = ref('npm')

const installCmds = {
  npm:  'npm install aumoji-picker',
  pnpm: 'pnpm add aumoji-picker',
  yarn: 'yarn add aumoji-picker',
}

onMounted(() => {
  if (!featsRef.value) return
  const cards = Array.from(featsRef.value.querySelectorAll('.will-reveal'))
  const reveal = (el) => el.classList.add('revealed')
  const observer = new IntersectionObserver(
    (entries) => entries.forEach(e => { if (e.isIntersecting) reveal(e.target) }),
    { threshold: 0, rootMargin: '0px 0px -20px 0px' }
  )
  cards.forEach(el => observer.observe(el))
  requestAnimationFrame(() => {
    cards.forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight - 20) reveal(el)
    })
  })
})

function onDemoSelect(item) {
  lastSelected.value = item
}

const features = [
  { icon: '🎭', title: 'FACS 标准', desc: '完整实现面部动作编码系统，涵盖基础情绪、复合表情、微表情、单 AU 四大分类' },
  { icon: '⚙️', title: '完全可配置', desc: '支持 theme / lang / width / height / copyFormat 等 Props，满足各类集成场景' },
  { icon: '🪶', title: '零依赖打包', desc: 'Vue 3 为 peerDependency，打包产物仅包含组件本身，不附带任何运行时依赖' },
  { icon: '🌍', title: '国际化', desc: '内置中英文双语，切换无需重新加载，所有界面文案均支持 lang prop 控制' },
]

const importCode = `import { AUmojiPicker } from 'aumoji-picker'`

const usageCode = `<AUmojiPicker
  theme="dark"
  lang="zh"
  :width="350"
  :height="450"
  @select="(item) => console.log(item.auCode)"
/>`
</script>

<style scoped>
/* ── Hero ── */
.hero-section {
  position: relative;
  overflow: hidden;
  background: var(--bg);
  padding: 100px 20px 80px;
}

.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); pointer-events: none;
}
.orb1 { width: 600px; height: 600px; top: -160px; left: -100px; background: rgba(139,92,246,0.14); }
.orb2 { width: 500px; height: 500px; top: 40px; right: -100px; background: rgba(56,189,248,0.08); }
.orb3 { width: 400px; height: 400px; bottom: -80px; left: 35%; background: rgba(249,115,22,0.06); }

.hero-inner {
  position: relative; z-index: 1;
  max-width: 720px; margin: 0 auto;
  display: flex; flex-direction: column;
  align-items: center; text-align: center;
  gap: 0;
}

.hero-title {
  font-size: clamp(2.8rem, 6vw, 4.4rem);
  font-weight: 800; line-height: 1.1;
  color: var(--tx);
  margin-bottom: 22px;
}

.hero-sub {
  font-size: 17px; color: var(--tx2);
  line-height: 1.75; max-width: 540px;
  margin-bottom: 36px;
}

.hero-ctas {
  display: flex; flex-wrap: wrap;
  gap: 10px; justify-content: center;
  margin-bottom: 32px;
}

.hero-stats {
  display: flex; flex-wrap: wrap; gap: 8px 14px;
  justify-content: center; align-items: center;
  font-size: 13px; color: var(--tx3);
  margin-bottom: 20px;
}
.stat-sep { color: var(--divider); user-select: none; }

.hero-badges {
  display: flex; flex-wrap: wrap;
  gap: 6px; justify-content: center;
  min-height: 20px;
}

/* ── Demo section ── */
.demo-section {
  padding: 80px 20px;
  background: var(--bg2);
}

.section-hd {
  text-align: center; margin-bottom: 48px;
}
.section-hd h2 { font-size: 28px; margin-bottom: 8px; }
.section-hd p { color: var(--tx2); font-size: 15px; }

.demo-body {
  max-width: 860px; margin: 0 auto;
  display: flex; flex-wrap: wrap;
  gap: 40px; align-items: flex-start;
  justify-content: center;
}

.demo-picker-wrap {
  display: flex; flex-direction: column;
  align-items: center; gap: 14px;
}

.demo-controls {
  display: flex; gap: 8px;
}

.demo-toggle {
  padding: 6px 16px; border-radius: 20px;
  border: 1px solid var(--card-bd);
  background: rgba(255,255,255,0.04); color: var(--tx2);
  font-size: 12.5px; font-weight: 500; cursor: pointer;
  transition: all var(--ease); font-family: inherit;
}
.demo-toggle:hover { border-color: var(--ac-bd); color: var(--tx); background: var(--ac-soft); }

.demo-output {
  width: 240px; min-width: 200px;
  display: flex; flex-direction: column;
  align-items: center; text-align: center;
  gap: 10px; padding: 28px 20px;
  background: var(--card); border: 1px solid var(--card-bd);
  border-radius: 16px;
}

.demo-output-label {
  font-size: 12px; font-weight: 600; color: var(--tx3);
  letter-spacing: 0.05em; text-transform: uppercase;
}

.output-em   { font-size: 52px; line-height: 1; user-select: none; }
.output-name { font-size: 15px; font-weight: 700; color: var(--tx); }
.output-name-en { font-size: 12px; color: var(--tx3); margin-top: -6px; }

.output-code-badge {
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 12px; font-weight: 700;
  color: #a78bfa; background: rgba(167,139,250,0.12);
  border: 1px solid rgba(167,139,250,0.24);
  border-radius: 6px; padding: 3px 10px;
}

.output-desc {
  font-size: 12px; color: var(--tx2); line-height: 1.55;
  max-width: 200px;
}

.output-hint {
  font-size: 13px; color: var(--tx3);
  margin-top: 20px;
}

/* ── Section layout helpers ── */
.features-section { padding: 80px 0; }
.qs-section { padding: 80px 0; }

.section-wrap-lg {
  max-width: 1152px;
  margin: 0 auto;
  padding: 0 20px;
}
.section-wrap-sm {
  max-width: 768px;
  margin: 0 auto;
  padding: 0 20px;
}

.feat-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 16px;
}
@media (min-width: 768px) {
  .feat-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .feat-grid { grid-template-columns: repeat(4, 1fr); }
}

.qs-steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── Footer ── */
.site-footer {
  text-align: center;
  padding: 40px 20px;
  border-top: 1px solid var(--divider);
  color: var(--tx3);
  font-size: 13px;
}
.footer-link { color: var(--tx2); text-decoration: none; }
.footer-link:hover { color: var(--tx); }

/* ── Step label ── */
.step-label { font-size: 12px; font-weight: 600; color: var(--ac); letter-spacing: 0.04em; }

/* ── Scroll reveal ── */
.will-reveal {
  opacity: 0; transform: translateY(22px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.will-reveal.revealed { opacity: 1; transform: translateY(0); }

/* ── Install tabs ── */
.install-tabs {
  display: flex;
  border: 1px solid var(--card-bd);
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
}
.install-tab {
  flex: 1; padding: 7px 0;
  font-size: 12px; font-weight: 600;
  font-family: ui-monospace, monospace;
  background: rgba(255,255,255,0.03);
  border: none; border-right: 1px solid var(--card-bd);
  color: var(--tx3); cursor: pointer;
  transition: background 0.14s, color 0.14s;
}
.install-tab:last-child { border-right: none; }
.install-tab:hover  { background: var(--ac-soft); color: var(--tx); }
.install-tab.active { background: var(--ac-soft); color: var(--ac); }

.install-code {
  border-radius: 0 0 8px 8px !important;
  margin-top: 0 !important;
  border-top: none !important;
}
</style>
