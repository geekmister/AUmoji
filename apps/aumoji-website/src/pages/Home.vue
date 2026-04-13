<template>
  <div>
    <!-- ══ HERO ══ 纯居中文字，不含 picker -->
    <section class="hero-section">
      <div class="orb orb1"></div>
      <div class="orb orb2"></div>
      <div class="orb orb3"></div>

      <div class="hero-inner">
        <div class="badge" style="margin-bottom:28px">
          ✨ &nbsp;{{ lang === 'zh' ? '影视级 FACS 表情系统 · Vue 3' : 'Cinematic FACS Expression System · Vue 3' }}
        </div>

        <h1 class="hero-title">
          <span class="grad-text">{{ lang === 'zh' ? 'AU 表情' : 'AU Emoji' }}</span>{{ lang === 'zh' ? '选择器' : ' Picker' }}<br>
          <span style="font-size:0.65em; font-weight:700; color:var(--tx2)">
            {{ lang === 'zh' ? '为 AI 视频创作者打造' : 'Built for AI Video Creators' }}
          </span>
        </h1>

        <p class="hero-sub">
          <template v-if="lang === 'zh'">
            基于 FACS 面部动作编码系统，精准控制 21 种影视级表情。<br>
            轻量、可配置、开箱即用，Vue 3 零运行时依赖。
          </template>
          <template v-else>
            Based on FACS Action Coding System — precise control over 21 cinematic expressions.<br>
            Lightweight, configurable, zero runtime dependencies.
          </template>
        </p>

        <div class="hero-ctas">
          <a href="#demo" class="btn btn-primary">{{ lang === 'zh' ? '试一试 ↓' : 'Try it ↓' }}</a>
          <a href="https://github.com/Geekmister/AUmoji" target="_blank" rel="noopener" class="btn btn-outline">
            <i class="fa-brands fa-github"></i> GitHub
          </a>
          <RouterLink to="/playground" class="btn btn-outline">🎮 Playground</RouterLink>
        </div>

        <div class="hero-stats">
          <span>📦 &nbsp;{{ lang === 'zh' ? '零运行时依赖' : 'Zero Dependencies' }}</span>
          <span class="stat-sep">·</span>
          <span>🎭 &nbsp;21 {{ lang === 'zh' ? '个表情' : ' Expressions' }}</span>
          <span class="stat-sep">·</span>
          <span>🌍 &nbsp;{{ lang === 'zh' ? '中 / EN 双语' : 'zh / EN Bilingual' }}</span>
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
        <h2>{{ lang === 'zh' ? '在线演示' : 'Live Demo' }}</h2>
        <p>{{ lang === 'zh' ? '实时切换主题与语言，选择表情查看 AU 编号与 AI 提示词' : 'Toggle theme & language in real-time, select an expression to see AU code & AI prompt' }}</p>
      </div>

      <div class="demo-body">
        <!-- Picker -->
        <div class="demo-picker-wrap">
          <AUmojiPicker
            :theme="demoTheme"
            :lang="demoLang"
            :width="demoPickerSize.width"
            :height="demoPickerSize.height"
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
        <div class="demo-output" :style="demoPanelStyle">
          <div class="demo-output-glow"></div>
          <div class="demo-output-head">
            <p class="demo-output-label">
              <span class="demo-output-dot"></span>
              {{ lang === 'zh' ? '完整预览' : 'Full Preview' }}
            </p>
            <p class="demo-output-sub">{{ lang === 'zh' ? '左侧选择后，这里显示该表情的所有信息，可以快速查看描述、中/英文提示词。' : 'After selecting from the left, this panel shows all key details of the expression, including description and CN/EN prompts.' }}</p>
          </div>

          <template v-if="lastSelected">
            <div class="demo-preview-hero">
              <div v-if="lastSelected.faceImg" class="demo-preview-media">
                <img
                  :src="lastSelected.faceImg"
                  :alt="displayName"
                  class="demo-preview-face"
                  loading="lazy"
                  @click="openImageViewer(lastSelected.faceImg, displayName)"
                />
                <button
                  class="demo-preview-view-btn"
                  type="button"
                  @click="openImageViewer(lastSelected.faceImg, displayName)"
                >
                  {{ lang === 'zh' ? '查看原图' : 'View Original' }}
                </button>
              </div>
              <div v-else class="demo-preview-emoji">{{ lastSelected.emoji || '🙂' }}</div>
              <div class="demo-preview-main">
                <div class="output-name">{{ displayName }}</div>
                <code class="output-code-badge">{{ lastSelected.auCode }}</code>
                <div class="demo-preview-tag">{{ lastSelected.category || 'AU' }}</div>
              </div>
            </div>

            <div class="demo-info-layout">
              <div class="demo-copy-assist demo-info-panel">
                <div class="demo-copy-title">{{ lang === 'zh' ? '描述与提示词' : 'Description & Prompts' }}</div>
                <p class="demo-copy-desc">{{ displayDesc }}</p>
                <div class="demo-prompt-grid">
                  <div class="demo-prompt-card">
                    <div class="demo-prompt-head">
                      <div class="demo-prompt-label">{{ lang === 'zh' ? '中文提示词' : 'Prompt (ZH)' }}</div>
                      <button
                        class="demo-prompt-copy"
                        type="button"
                        @click="copyPrompt('zh', promptCnText)"
                      >
                        {{ copiedPrompt === 'zh' ? (lang === 'zh' ? '已复制' : 'Copied') : (lang === 'zh' ? '复制' : 'Copy') }}
                      </button>
                    </div>
                    <p class="demo-prompt-text">{{ promptCnText }}</p>
                  </div>
                  <div class="demo-prompt-card">
                    <div class="demo-prompt-head">
                      <div class="demo-prompt-label">{{ lang === 'zh' ? '英文提示词' : 'Prompt (EN)' }}</div>
                      <button
                        class="demo-prompt-copy"
                        type="button"
                        @click="copyPrompt('en', promptEnText)"
                      >
                        {{ copiedPrompt === 'en' ? (lang === 'zh' ? '已复制' : 'Copied') : (lang === 'zh' ? '复制' : 'Copy') }}
                      </button>
                    </div>
                    <p class="demo-prompt-text">{{ promptEnText }}</p>
                  </div>
                </div>
              </div>

              <div class="demo-info-panel demo-core-panel">
                <div class="demo-copy-title">{{ lang === 'zh' ? '核心参数' : 'Core Specs' }}</div>
                <div class="demo-core-grid">
                  <div class="demo-core-item">
                    <div class="demo-core-label">{{ lang === 'zh' ? 'AU 全称' : 'AU Full' }}</div>
                    <div class="demo-core-value">{{ displayAuFull }}</div>
                  </div>
                  <div class="demo-core-item">
                    <div class="demo-core-label">{{ lang === 'zh' ? '强度' : 'Strength' }}</div>
                    <div class="demo-core-value">{{ displayStrength }}</div>
                  </div>
                  <div class="demo-core-item">
                    <div class="demo-core-label">{{ lang === 'zh' ? '肌肉动作' : 'Muscle' }}</div>
                    <div class="demo-core-value">{{ displayMuscle }}</div>
                  </div>
                  <div class="demo-core-item">
                    <div class="demo-core-label">{{ lang === 'zh' ? '适用场景' : 'Scene' }}</div>
                    <div class="demo-core-value">{{ displayScene }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="demo-preview-fields">
              <div
                v-for="entry in previewEntries"
                :key="entry.key"
                class="demo-field"
              >
                <div class="demo-field-key">{{ entry.label }}</div>
                <div class="demo-field-val">{{ entry.value }}</div>
              </div>
            </div>
          </template>

          <template v-else>
            <div class="demo-preview-empty">
              <img
                src="/img/preview-empty-illustration.svg"
                alt="preview placeholder"
                class="demo-preview-placeholder"
                loading="lazy"
              />
              <div class="demo-preview-empty-copy">
                <div class="output-name">{{ lang === 'zh' ? '等待左侧选择' : 'Waiting for Selection' }}</div>
                <p class="output-hint">{{ lang === 'zh' ? '点击左侧任意表情后，这里会展示该表情的关键信息，并可快速查看描述与中/英文提示词。' : 'Pick any expression on the left to view key details, plus description and CN/EN prompts.' }}</p>
              </div>
            </div>
          </template>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- ══ FEATURES ══ -->
    <section class="features-section">
      <div class="section-wrap-lg">
        <div class="section-hd">
          <h2>{{ lang === 'zh' ? '为什么选择 AUmoji' : 'Why AUmoji' }}</h2>
          <p>{{ lang === 'zh' ? '专为 AI 视频与影视制作工作流设计' : 'Designed for AI video & cinematic production workflows' }}</p>
        </div>

        <div class="feat-grid" ref="featsRef">
          <div
            v-for="(feat, i) in features"
            :key="feat.title"
            class="feat-card will-reveal"
            :style="{ transitionDelay: i * 90 + 'ms' }"
          >
            <div class="feat-icon">{{ feat.icon }}</div>
            <h3 style="font-size:15px; margin-bottom:8px;">{{ lang === 'zh' ? feat.title : feat.titleEn }}</h3>
            <p style="font-size:13px; color:var(--tx2); line-height:1.6">{{ lang === 'zh' ? feat.desc : feat.descEn }}</p>
          </div>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <transition name="img-viewer">
      <div v-if="imageViewerOpen" class="img-viewer" @click="closeImageViewer">
        <div class="img-viewer-inner" @click.stop>
          <button class="img-viewer-close" type="button" @click="closeImageViewer">✕</button>
          <img :src="viewerImageSrc" :alt="viewerImageAlt" class="img-viewer-img" loading="lazy" />
        </div>
      </div>
    </transition>

    <!-- ══ QUICK START ══ -->
    <section class="qs-section">
      <div class="section-wrap-sm">
        <div class="section-hd">
          <h2>{{ lang === 'zh' ? '快速开始' : 'Quick Start' }}</h2>
          <p>{{ lang === 'zh' ? '三步集成到你的项目' : 'Integrate in 3 steps' }}</p>
        </div>

        <div class="qs-steps">
          <div class="card" style="padding:24px">
            <p class="step-label">{{ lang === 'zh' ? '① 安装' : '① Install' }}</p>
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
            <p class="step-label">{{ lang === 'zh' ? '② 引入组件' : '② Import' }}</p>
            <div class="code-block mt-3">{{ importCode }}</div>
          </div>
          <div class="card" style="padding:24px">
            <p class="step-label">{{ lang === 'zh' ? '③ 使用' : '③ Use' }}</p>
            <div class="code-block mt-3">{{ usageCode }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ FOOTER ══ -->
    <footer class="site-footer">
      AUmoji © 2025 &nbsp;·&nbsp; {{ lang === 'zh' ? '开源免费' : 'Open Source' }} &nbsp;·&nbsp; {{ lang === 'zh' ? '基于 FACS for AI 创作者' : 'FACS-based · For AI Creators' }} &nbsp;·&nbsp;
      <a href="https://github.com/Geekmister/AUmoji" target="_blank" rel="noopener" class="footer-link">GitHub ↗</a>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { AUmojiPicker } from 'aumoji-picker'
import { useTheme } from '../composables/useTheme.js'
import { useLang }  from '../composables/useLang.js'

const { theme } = useTheme()
const { lang }  = useLang()

// Demo picker mirrors global theme/lang but can also be overridden locally
const demoTheme    = ref(theme.value)
const demoLang     = ref('zh')
const demoPickerSize = ref({ width: 520, height: 720 })
const lastSelected = ref(null)
const copiedPrompt = ref('')
const imageViewerOpen = ref(false)
const viewerImageSrc = ref('')
const viewerImageAlt = ref('preview image')
const featsRef     = ref(null)
const installTab   = ref('npm')

// Keep demo in sync with global toggles
watch(theme, v => { demoTheme.value = v })

const demoPanelStyle = computed(() => ({
  width: demoPickerSize.value.width + 'px',
  height: demoPickerSize.value.height + 'px',
}))

const FIELD_LABELS_ZH = {
  id: 'ID',
  name: '名称',
  nameCn: '中文名',
  nameEn: '英文名',
  category: '分类',
  subCategory: '子分类',
  auCode: 'AU 编号',
  auFull: 'AU 全称',
  strength: '强度',
  muscle: '肌肉动作',
  conflict: '冲突项',
  desc: '描述',
  descCn: '中文描述',
  descEn: '英文描述',
  prompt: '提示词',
  promptCn: '中文提示词',
  promptEn: '英文提示词',
  scene: '适用场景',
  isMicro: '微表情',
  icon: '图标',
  faceImg: '示意图',
  emoji: '表情符号',
  pinyin: '拼音',
  pronunciation: '发音说明',
}

const FIELD_LABELS_EN = {
  id: 'ID',
  name: 'Name',
  nameCn: 'Chinese Name',
  nameEn: 'English Name',
  category: 'Category',
  subCategory: 'Subcategory',
  auCode: 'AU Code',
  auFull: 'AU Full',
  strength: 'Strength',
  muscle: 'Muscle',
  conflict: 'Conflict',
  desc: 'Description',
  descCn: 'Chinese Description',
  descEn: 'English Description',
  prompt: 'Prompt',
  promptCn: 'Chinese Prompt',
  promptEn: 'English Prompt',
  scene: 'Scene',
  isMicro: 'Micro Expression',
  icon: 'Icon',
  faceImg: 'Face Image',
  emoji: 'Emoji',
  pinyin: 'Pinyin',
  pronunciation: 'Pronunciation',
}

const HIDDEN_FIELD_KEYS = new Set([
  'id',
  'subCategory',
  'isMicro',
  'icon',
  'faceImg',
  'emoji',
  'prompt',
  'promptCn',
  'promptEn',
  'scene',
])

const displayName = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return lang.value === 'zh'
    ? (item.nameCn || item.name || item.nameEn || '—')
    : (item.nameEn || item.name || item.nameCn || '—')
})

const displayDesc = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return lang.value === 'zh'
    ? (item.descCn || item.desc || item.descEn || '—')
    : (item.descEn || item.desc || item.descCn || '—')
})

const displayScene = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return item.scene || '—'
})

const displayAuFull = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return item.auFull || item.auCode || '—'
})

const displayStrength = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return item.strength || '—'
})

const displayMuscle = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return item.muscle || '—'
})

const promptCnText = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return item.promptCn || item.prompt || '—'
})

const promptEnText = computed(() => {
  const item = lastSelected.value
  if (!item) return '—'
  return item.promptEn || item.prompt || '—'
})

const previewEntries = computed(() => {
  if (!lastSelected.value) return []
  const labels = lang.value === 'zh' ? FIELD_LABELS_ZH : FIELD_LABELS_EN
  return Object.entries(lastSelected.value)
    .filter(([key]) => !HIDDEN_FIELD_KEYS.has(key))
    .map(([key, value]) => ({
      key,
      label: labels[key] || key,
      value: typeof value === 'boolean'
        ? (lang.value === 'zh' ? (value ? '是' : '否') : (value ? 'true' : 'false'))
        : String(value || '—'),
    }))
})

function updateDemoPickerSize() {
  if (typeof window === 'undefined') return
  const vw = window.innerWidth
  if (vw < 640) {
    demoPickerSize.value = { width: 336, height: 560 }
    return
  }
  if (vw < 1100) {
    demoPickerSize.value = { width: 420, height: 640 }
    return
  }
  demoPickerSize.value = { width: 520, height: 720 }
}

const installCmds = {
  npm:  'npm install aumoji-picker',
  pnpm: 'pnpm add aumoji-picker',
  yarn: 'yarn add aumoji-picker',
}

onMounted(() => {
  updateDemoPickerSize()
  window.addEventListener('resize', updateDemoPickerSize)
  window.addEventListener('keydown', onPageKeydown)

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

onUnmounted(() => {
  window.removeEventListener('resize', updateDemoPickerSize)
  window.removeEventListener('keydown', onPageKeydown)
})

function onDemoSelect(item) {
  lastSelected.value = item
}

function openImageViewer(src, altText) {
  if (!src) return
  viewerImageSrc.value = src
  viewerImageAlt.value = altText || 'preview image'
  imageViewerOpen.value = true
}

function closeImageViewer() {
  imageViewerOpen.value = false
}

function onPageKeydown(event) {
  if (event.key === 'Escape' && imageViewerOpen.value) {
    closeImageViewer()
  }
}

async function copyPrompt(kind, text) {
  const content = String(text || '').trim()
  if (!content || content === '—') return

  try {
    if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(content)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = content
      textarea.setAttribute('readonly', '')
      textarea.style.position = 'absolute'
      textarea.style.left = '-9999px'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }

    copiedPrompt.value = kind
    setTimeout(() => {
      if (copiedPrompt.value === kind) copiedPrompt.value = ''
    }, 1200)
  } catch {
    copiedPrompt.value = ''
  }
}

const features = [
  {
    icon: '🎭',
    title: 'FACS 标准', titleEn: 'FACS Standard',
    desc: '完整实现面部动作编码系统，涵盖基础情绪、复合表情、微表情、单 AU 四大分类',
    descEn: 'Full FACS implementation — basic emotions, compound expressions, micro-expressions & single AUs'
  },
  {
    icon: '⚙️',
    title: '完全可配置', titleEn: 'Fully Configurable',
    desc: '支持 theme / lang / width / height / copyFormat 等 Props，满足各类集成场景',
    descEn: 'Flexible props: theme, lang, width, height, copyFormat — fits any integration scenario'
  },
  {
    icon: '🪶',
    title: '零依赖打包', titleEn: 'Zero Dependencies',
    desc: 'Vue 3 为 peerDependency，打包产物仅包含组件本身，不附带任何运行时依赖',
    descEn: 'Vue 3 is a peerDependency — bundle only contains the component itself, no extra runtime deps'
  },
  {
    icon: '🌍',
    title: '国际化', titleEn: 'i18n Built-in',
    desc: '内置中英文双语，切换无需重新加载，所有界面文案均支持 lang prop 控制',
    descEn: 'Built-in zh / en bilingual support — no reload needed, all labels follow the lang prop'
  },
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
  padding: var(--space-section-lg) 24px var(--space-section-md);
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
  max-width: 760px; margin: 0 auto;
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
  font-size: 18px; color: var(--tx2);
  line-height: 1.86;
  max-width: 640px;
  margin-bottom: 42px;
}

.hero-ctas {
  display: flex; flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  margin-bottom: 36px;
}

.hero-stats {
  display: flex; flex-wrap: wrap; gap: 10px 16px;
  justify-content: center; align-items: center;
  font-size: 14px;
  color: var(--tx3);
  margin-bottom: 24px;
}
.stat-sep { color: var(--divider); user-select: none; }

.hero-badges {
  display: flex; flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  min-height: 20px;
}

/* ── Demo section ── */
.demo-section {
  padding: var(--space-section-md) 24px;
  background: var(--bg2);
}

.section-hd {
  text-align: center;
  margin-bottom: 56px;
}
.section-hd h2 {
  font-size: 30px;
  margin-bottom: 12px;
}
.section-hd p {
  color: var(--tx2);
  font-size: 16px;
  max-width: 720px;
  margin: 0 auto;
  line-height: 1.75;
}

.demo-body {
  max-width: 1240px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: auto auto;
  justify-content: center;
  gap: 28px;
  align-items: start;
}

.demo-picker-wrap {
  display: flex; flex-direction: column;
  align-items: center;
  gap: 18px;
  min-width: 0;
}

.demo-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.demo-toggle {
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid var(--card-bd);
  background: rgba(255,255,255,0.04); color: var(--tx2);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--ease); font-family: inherit;
}
.demo-toggle:hover { border-color: var(--ac-bd); color: var(--tx); background: var(--ac-soft); }

.demo-output {
  width: 100%;
  min-width: 0;
  display: flex; flex-direction: column;
  align-items: stretch;
  text-align: left;
  gap: 16px;
  padding: 28px 24px 24px;
  background:
    radial-gradient(120% 120% at 100% 0%, rgba(14,165,233,0.16), transparent 42%),
    radial-gradient(120% 120% at 0% 100%, rgba(244,114,182,0.14), transparent 38%),
    var(--card);
  border: 1px solid color-mix(in srgb, var(--card-bd) 70%, rgba(148,163,184,0.45));
  border-radius: 20px;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.08),
    0 16px 40px rgba(2,6,23,0.26);
  overflow-x: hidden;
  overflow-y: auto;
  position: relative;
}

@media (max-width: 1100px) {
  .demo-body {
    max-width: 860px;
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 22px;
  }

  .demo-output {
    max-width: none;
      align-items: center;
      text-align: center;
  }
}

.demo-output-head {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-bottom: 10px;
  border-bottom: 1px dashed color-mix(in srgb, var(--card-bd) 82%, rgba(148,163,184,0.22));
}

.demo-output-glow {
  position: absolute;
  top: -26px;
  right: -26px;
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(56,189,248,0.32), rgba(56,189,248,0));
  pointer-events: none;
}

.demo-output-label {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--tx3);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.demo-output-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: linear-gradient(120deg, #38bdf8, #818cf8);
  box-shadow: 0 0 10px rgba(56,189,248,0.8);
}

.demo-output-sub {
  font-size: 13px;
  color: var(--tx2);
  line-height: 1.7;
}

.demo-preview-hero {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
  padding: 14px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 86%, rgba(148,163,184,0.2));
  border-radius: 16px;
  background: color-mix(in srgb, var(--card) 82%, rgba(15,23,42,0.26));
}

.demo-preview-media {
  position: relative;
  width: 100%;
  min-width: 0;
  height: 240px;
  border-radius: 12px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 76%, rgba(148,163,184,0.24));
  background: color-mix(in srgb, var(--bg2) 72%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.demo-preview-face,
.demo-preview-placeholder {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
  display: block;
}

.demo-preview-face {
  cursor: zoom-in;
}

.demo-preview-view-btn {
  position: absolute;
  right: 10px;
  bottom: 10px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 74%, rgba(148,163,184,0.22));
  background: rgba(15, 23, 42, 0.68);
  color: #f8fafc;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 11px;
  line-height: 1.4;
  cursor: pointer;
  transition: opacity var(--ease), transform var(--ease);
}

.demo-preview-view-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.demo-preview-emoji {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-width: 0;
  height: 240px;
  border-radius: 12px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 76%, rgba(148,163,184,0.24));
  background: color-mix(in srgb, var(--bg2) 72%, transparent);
  font-size: 88px;
}

.demo-preview-main {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-info-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  align-items: start;
}

.demo-info-panel {
  padding: 12px 14px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 78%, rgba(148,163,184,0.24));
  border-radius: 14px;
  background: color-mix(in srgb, var(--card) 88%, rgba(15,23,42,0.2));
}

.demo-copy-assist {
  min-width: 0;
}

.demo-core-panel {
  min-width: 0;
}

.demo-copy-title {
  font-size: 12px;
  font-weight: 700;
  color: color-mix(in srgb, var(--tx3) 82%, #38bdf8 18%);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.demo-copy-desc {
  margin-top: 6px;
  font-size: 13px;
  line-height: 1.72;
  color: var(--tx2);
}

.demo-core-grid {
  margin-top: 10px;
  display: grid;
  gap: 8px;
}

.demo-core-item {
  padding: 9px 10px;
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 80%, rgba(148,163,184,0.24));
  background: color-mix(in srgb, var(--bg2) 72%, transparent);
}

.demo-core-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--tx3);
  letter-spacing: 0.03em;
}

.demo-core-value {
  margin-top: 4px;
  font-size: 12.5px;
  line-height: 1.66;
  color: var(--tx2);
  word-break: break-word;
}

.demo-prompt-grid {
  margin-top: 10px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.demo-prompt-card {
  padding: 10px 11px;
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 80%, rgba(148,163,184,0.24));
  background: color-mix(in srgb, var(--bg2) 72%, transparent);
}

.demo-prompt-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.demo-prompt-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--tx3);
  letter-spacing: 0.03em;
}

.demo-prompt-copy {
  border: 1px solid color-mix(in srgb, var(--card-bd) 80%, rgba(148,163,184,0.28));
  background: color-mix(in srgb, var(--card) 86%, rgba(15,23,42,0.18));
  color: var(--tx2);
  border-radius: 999px;
  padding: 3px 10px;
  font-size: 11px;
  line-height: 1.4;
  cursor: pointer;
  white-space: nowrap;
  transition: border-color var(--ease), color var(--ease), background var(--ease);
}

.demo-prompt-copy:hover {
  border-color: var(--ac-bd);
  color: var(--tx);
  background: var(--ac-soft);
}

.demo-prompt-text {
  margin-top: 5px;
  font-size: 12.5px;
  line-height: 1.66;
  color: var(--tx2);
  word-break: break-word;
}

.demo-preview-tag {
  align-self: flex-start;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #f8fafc;
  background: linear-gradient(120deg, #0ea5e9, #6366f1);
  border-radius: 999px;
  padding: 4px 10px;
}

.demo-preview-fields {
  display: flex;
  flex-direction: column;
  gap: 11px;
  min-height: 0;
  overflow: auto;
  padding-right: 4px;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in srgb, var(--card-bd) 80%, rgba(148,163,184,0.55)) transparent;
}

.demo-preview-fields::-webkit-scrollbar {
  width: 6px;
}

.demo-preview-fields::-webkit-scrollbar-thumb {
  border-radius: 6px;
  background: color-mix(in srgb, var(--card-bd) 80%, rgba(148,163,184,0.55));
}

.demo-field {
  padding: 12px 14px 13px;
  border: 1px solid color-mix(in srgb, var(--card-bd) 76%, rgba(148,163,184,0.28));
  border-radius: 14px;
  background:
    linear-gradient(120deg, rgba(255,255,255,0.015), rgba(255,255,255,0.04)),
    rgba(255,255,255,0.01);
}

.demo-field-key {
  font-size: 11.5px;
  font-weight: 700;
  color: color-mix(in srgb, var(--tx3) 84%, #60a5fa 16%);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.demo-field-val {
  font-size: 13px;
  color: var(--tx2);
  line-height: 1.72;
  word-break: break-word;
}

.demo-preview-empty {
  display: flex;
  flex-direction: column;
  gap: 18px;
  align-items: center;
  justify-content: center;
  flex: 1;
  min-height: 0;
  padding: 14px;
  border: 1px dashed color-mix(in srgb, var(--card-bd) 70%, rgba(148,163,184,0.35));
  border-radius: 16px;
}

.demo-preview-empty-copy {
  max-width: 320px;
  text-align: center;
}

.output-em   { font-size: 52px; line-height: 1; user-select: none; }
.output-name { font-size: 16px; font-weight: 700; color: var(--tx); }

.output-code-badge {
  font-family: ui-monospace, 'Fira Code', monospace;
  font-size: 12px; font-weight: 700;
  color: #a78bfa; background: rgba(167,139,250,0.12);
  border: 1px solid rgba(167,139,250,0.24);
  border-radius: 6px; padding: 3px 10px;
}

.output-desc {
  font-size: 13px;
  color: var(--tx2);
  line-height: 1.75;
  max-width: 240px;
}

.output-hint {
  font-size: 14px;
  color: var(--tx3);
  margin-top: 16px;
  line-height: 1.75;
}

/* ── Section layout helpers ── */
.features-section { padding: var(--space-section-md) 0; }
.qs-section { padding: var(--space-section-sm) 0 var(--space-section-md); }

.section-wrap-lg {
  max-width: 1152px;
  margin: 0 auto;
  padding: 0 24px;
}
.section-wrap-sm {
  max-width: 820px;
  margin: 0 auto;
  padding: 0 24px;
}

.feat-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 22px;
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
  gap: 28px;
}

/* ── Footer ── */
.site-footer {
  text-align: center;
  padding: 52px 24px;
  border-top: 1px solid var(--divider);
  color: var(--tx3);
  font-size: 14px;
}

.img-viewer {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.8);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 120;
  padding: 24px;
}

.img-viewer-inner {
  position: relative;
  width: min(92vw, 1120px);
  max-height: 92vh;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(15, 23, 42, 0.92);
  box-shadow: 0 18px 44px rgba(2, 6, 23, 0.48);
}

.img-viewer-img {
  width: 100%;
  max-height: 92vh;
  object-fit: contain;
  display: block;
}

.img-viewer-close {
  position: absolute;
  top: 10px;
  right: 10px;
  border: 1px solid rgba(148, 163, 184, 0.4);
  background: rgba(15, 23, 42, 0.72);
  color: #f8fafc;
  border-radius: 8px;
  width: 32px;
  height: 32px;
  font-size: 15px;
  cursor: pointer;
}

.img-viewer-enter-active,
.img-viewer-leave-active {
  transition: opacity 0.18s ease;
}

.img-viewer-enter-from,
.img-viewer-leave-to {
  opacity: 0;
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
  flex: 1;
  padding: 9px 0;
  font-size: 12.5px;
  font-weight: 600;
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

@media (max-width: 768px) {
  .hero-section {
    padding: 84px 20px 68px;
  }

  .hero-sub {
    font-size: 16px;
    margin-bottom: 34px;
  }

  .demo-section {
    padding: 68px 20px;
  }

  .section-hd {
    margin-bottom: 42px;
  }

  .section-hd h2 {
    font-size: 27px;
  }

  .section-hd p {
    font-size: 15px;
  }

  .demo-preview-hero {
    flex-direction: column;
    align-items: stretch;
  }

  .demo-preview-media,
  .demo-preview-emoji {
    width: 100%;
    min-width: 0;
    height: 200px;
  }
}
</style>
