<template>
  <div
    class="aup"
    :data-theme="resolvedTheme"
    :style="{ width: width + 'px', height: height + 'px' }"
  >
    <!-- ─── Search ─── -->
    <div v-if="showSearch" class="aup-header">
      <label class="aup-search-box">
        <span class="aup-search-ico">🔍</span>
        <input
          v-model="query"
          class="aup-search-input"
          :placeholder="i18n.search"
          autocomplete="off"
          spellcheck="false"
        />
        <button v-if="query" class="aup-clear-btn" @click="query = ''" type="button">✕</button>
      </label>
    </div>

    <!-- ─── Category Bar ─── -->
    <nav class="aup-catbar" v-show="!query">
      <button
        v-for="cat in CATEGORIES"
        :key="cat.type"
        :class="['aup-cat', activeCategory === cat.type && 'active']"
        @click="jumpTo(cat.type)"
        type="button"
        :title="lang === 'zh' ? cat.name : cat.nameEn"
      >
        <span class="aup-cat-dot" :style="{ background: cat.color }"></span>
        <span class="aup-cat-label">{{ lang === 'zh' ? cat.name : cat.nameEn }}</span>
      </button>
    </nav>

    <!-- ─── Scrollable Body ─── -->
    <div class="aup-body" ref="bodyRef" @scroll="onScroll" :style="detailVisible ? { paddingBottom: '118px' } : {}">

      <!-- Search results -->
      <template v-if="query">
        <div class="aup-sec-hd">
          <span class="aup-sec-dot" style="background:#94a3b8"></span>
          {{ i18n.results }} · {{ searchList.length }}
        </div>
        <div v-if="searchList.length" class="aup-grid">
          <button
            v-for="item in searchList"
            :key="item.auCode"
            :class="['aup-item', selected?.auCode === item.auCode && 'sel']"
            @click="pick(item)"
            type="button"
          >
            <span class="aup-em">
              <img
                v-if="item.faceImg"
                :src="item.faceImg"
                :alt="lang === 'zh' ? item.name : item.nameEn"
                class="aup-face"
                loading="lazy"
              />
              <span v-else>{{ item.emoji }}</span>
            </span>
            <span class="aup-nm">{{ lang === 'zh' ? item.name : item.nameEn }}</span>
            <span class="aup-cd">{{ item.auCode }}</span>
          </button>
        </div>
        <div v-else class="aup-empty">😶 {{ i18n.empty }}</div>
      </template>

      <!-- Browse by category -->
      <template v-else>
        <template v-for="cat in CATEGORIES" :key="cat.type">
          <div
            class="aup-sec-hd"
            :ref="(el) => { if (el) secRefs[cat.type] = el }"
          >
            <span class="aup-sec-dot" :style="{ background: cat.color }"></span>
            {{ lang === 'zh' ? cat.name : cat.nameEn }}
          </div>
          <div class="aup-grid">
            <button
              v-for="item in AU_DATA[cat.type]"
              :key="item.auCode"
              :class="['aup-item', selected?.auCode === item.auCode && 'sel']"
              @click="pick(item)"
              type="button"
              :title="item.auCode"
            >
              <span class="aup-em">
                <img
                  v-if="item.faceImg"
                  :src="item.faceImg"
                  :alt="lang === 'zh' ? item.name : item.nameEn"
                  class="aup-face"
                  loading="lazy"
                />
                <span v-else>{{ item.emoji }}</span>
              </span>
              <span class="aup-nm">{{ lang === 'zh' ? item.name : item.nameEn }}</span>
              <span class="aup-cd">{{ item.auCode }}</span>
            </button>
          </div>
        </template>
      </template>

    </div>

    <!-- ─── Detail Panel ─── -->
    <transition name="t-detail">
      <div v-if="detailVisible" class="aup-detail">
        <div class="aup-detail-top">
          <span class="aup-detail-em">
            <img
              v-if="selected.faceImg"
              :src="selected.faceImg"
              :alt="lang === 'zh' ? selected.name : selected.nameEn"
              class="aup-detail-face"
              loading="lazy"
            />
            <span v-else>{{ selected.emoji }}</span>
          </span>
          <div class="aup-detail-meta">
            <div class="aup-detail-nm">{{ lang === 'zh' ? selected.name : selected.nameEn }}</div>
            <div class="aup-detail-nm2">{{ lang === 'zh' ? selected.nameEn : selected.name }}</div>
            <div class="aup-detail-actions">
              <span class="aup-detail-badge">{{ selected.auCode }}</span>
              <button class="aup-detail-btn" @click.stop="copyDetail(selected.auCode)" type="button">{{ i18n.copyCode }}</button>
              <button class="aup-detail-btn aup-detail-btn--p" @click.stop="copyDetail(selected.prompt)" type="button">{{ i18n.copyPrompt }}</button>
            </div>
          </div>
          <button class="aup-detail-x" @click.stop="selected = null" type="button" :title="i18n.close">✕</button>
        </div>
        <p class="aup-detail-desc">{{ lang === 'zh' ? selected.desc : selected.descEn }}</p>
      </div>
    </transition>

    <!-- ─── Toast ─── -->
    <transition name="t-toast">
      <div v-if="toast" class="aup-toast" :style="detailVisible ? { bottom: '124px' } : {}">✓ {{ toast }}</div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { AU_DATA, CATEGORIES } from './constants/auData.js'
import { copyToClipboard } from './utils/copy.js'

/* ── Props ── */
const props = defineProps({
  /** 'light' | 'dark' | 'auto' */
  theme: { type: String, default: 'auto' },
  /** 'zh' | 'en' */
  lang: { type: String, default: 'zh' },
  /** Picker width in px */
  width: { type: Number, default: 460 },
  /** Picker height in px */
  height: { type: Number, default: 620 },
  /** Category to show on mount */
  defaultCategory: { type: String, default: 'basic' },
  /** Show search bar */
  showSearch: { type: Boolean, default: true },
  /** Show bottom detail panel after clicking an item */
  showDetailPanel: { type: Boolean, default: false },
  /** What to auto-copy on select: 'auCode' | 'prompt' | 'none' */
  copyFormat: { type: String, default: 'auCode' },
})

const emit = defineEmits(['select'])

/* ── State ── */
const query          = ref('')
const activeCategory = ref(props.defaultCategory)
const selected       = ref(null)
const toast          = ref('')
const bodyRef        = ref(null)
const secRefs        = reactive({})

/* ── i18n ── */
const STRINGS = {
  zh: { search: '搜索表情或 AU 编号…', results: '搜索结果', empty: '没有找到匹配的表情', copied: '已复制', copyCode: '复制编号', copyPrompt: '复制提示词', close: '关闭' },
  en: { search: 'Search expression or AU code…', results: 'Results', empty: 'No results found', copied: 'Copied', copyCode: 'Copy Code', copyPrompt: 'Copy Prompt', close: 'Close' },
}
const i18n = computed(() => STRINGS[props.lang] || STRINGS.zh)
const detailVisible = computed(() => props.showDetailPanel && !!selected.value)

/* ── Resolved theme ── */
const resolvedTheme = computed(() => {
  if (props.theme !== 'auto') return props.theme
  if (typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark'
  return 'light'
})

/* ── Search ── */
const searchList = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return []
  return Object.values(AU_DATA).flat().filter(item =>
    item.name.toLowerCase().includes(q) ||
    item.nameEn.toLowerCase().includes(q) ||
    item.auCode.toLowerCase().includes(q)
  )
})

/* ── Jump to category ── */
function jumpTo(type) {
  activeCategory.value = type
  const el = secRefs[type]
  const body = bodyRef.value
  if (el && body) {
    body.scrollTo({ top: el.offsetTop - 4, behavior: 'smooth' })
  }
}

/* ── Scroll → sync active category ── */
function onScroll() {
  const body = bodyRef.value
  if (!body) return
  const scrollTop = body.scrollTop
  for (const cat of [...CATEGORIES].reverse()) {
    const el = secRefs[cat.type]
    if (el && el.offsetTop <= scrollTop + 50) {
      activeCategory.value = cat.type
      break
    }
  }
}

/* ── Pick an item ── */
async function pick(item) {
  selected.value = item
  emit('select', item)
  if (props.copyFormat === 'none') return
  const text = props.copyFormat === 'prompt' ? item.prompt : item.auCode
  const ok = await copyToClipboard(text)
  if (ok) {
    const short = text.length > 26 ? text.slice(0, 26) + '…' : text
    toast.value = `${i18n.value.copied}: ${short}`
    setTimeout(() => { toast.value = '' }, 2000)
  }
}

/* ── Copy from detail panel ── */
async function copyDetail(text) {
  const ok = await copyToClipboard(text)
  if (ok) {
    const short = text.length > 22 ? text.slice(0, 22) + '…' : text
    toast.value = `${i18n.value.copied}: ${short}`
    setTimeout(() => { toast.value = '' }, 1800)
  }
}
</script>

<style scoped>
/* ════════════════════════════════════════
   DESIGN TOKENS
════════════════════════════════════════ */
.aup {
  /* Light */
  --bg:       #ffffff;
  --surface:  #f7f8fa;
  --bd:       #e4e7eb;
  --tx:       #111827;
  --tx2:      #6b7280;
  --tx3:      #9ca3af;
  --hov:      #f3f4f6;
  --sel-bg:   rgba(124, 58, 237, 0.08);
  --sel-bd:   rgba(124, 58, 237, 0.22);
  --sel-c:    #7c3aed;
  --r:        12px;
  --ease:     0.14s ease;
}

.aup[data-theme="dark"] {
  --bg:       #15171e;
  --surface:  #1d2030;
  --bd:       #2a2d3e;
  --tx:       #f1f5f9;
  --tx2:      #94a3b8;
  --tx3:      #64748b;
  --hov:      #1d2030;
  --sel-bg:   rgba(167, 139, 250, 0.12);
  --sel-bd:   rgba(167, 139, 250, 0.28);
  --sel-c:    #a78bfa;
}

/* ════════════════════════════════════════
   CONTAINER
════════════════════════════════════════ */
.aup {
  display: flex;
  flex-direction: column;
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: var(--r);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-size: 13px;
  color: var(--tx);
  position: relative;
  -webkit-font-smoothing: antialiased;
}

/* ════════════════════════════════════════
   SEARCH HEADER
════════════════════════════════════════ */
.aup-header {
  padding: 14px 14px 12px;
  border-bottom: 1px solid var(--bd);
  flex-shrink: 0;
}

.aup-search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--surface);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 0 14px;
  height: 42px;
  cursor: text;
  transition: border-color var(--ease), box-shadow var(--ease);
}
.aup-search-box:focus-within {
  border-color: var(--sel-c);
  box-shadow: 0 0 0 3px var(--sel-bg);
}

.aup-search-ico   { font-size: 14px; color: var(--tx3); flex-shrink: 0; user-select: none; }
.aup-search-input { flex: 1; border: none; outline: none; background: transparent; font-size: 13.5px; color: var(--tx); }
.aup-search-input::placeholder { color: var(--tx3); }

.aup-clear-btn {
  border: none; outline: none; background: transparent;
  color: var(--tx3); cursor: pointer; padding: 2px 4px;
  font-size: 13px; line-height: 1;
  transition: color var(--ease);
}
.aup-clear-btn:hover { color: var(--tx); }

/* ════════════════════════════════════════
   CATEGORY BAR
════════════════════════════════════════ */
.aup-catbar {
  display: flex;
  padding: 10px 12px;
  gap: 8px;
  border-bottom: 1px solid var(--bd);
  flex-shrink: 0;
  overflow-x: auto;
  scrollbar-width: none;
}
.aup-catbar::-webkit-scrollbar { display: none; }

.aup-cat {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--tx2);
  cursor: pointer;
  font-size: 12.5px;
  font-weight: 500;
  white-space: nowrap;
  transition: all var(--ease);
}
.aup-cat:hover  { background: var(--hov); color: var(--tx); }
.aup-cat.active { background: var(--hov); border-color: var(--bd); color: var(--tx); }

.aup-cat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

@media (max-width: 640px) {
  .aup-header {
    padding: 12px 12px 10px;
  }

  .aup-search-box {
    height: 40px;
    padding: 0 12px;
  }

  .aup-catbar {
    padding: 8px 10px;
    gap: 6px;
  }

  .aup-cat {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* ════════════════════════════════════════
   SCROLL BODY
════════════════════════════════════════ */
.aup-body {
  flex: 1;
  overflow-y: auto;
  padding: 10px 12px 18px;
  scrollbar-width: thin;
  scrollbar-color: var(--bd) transparent;
}
.aup-body::-webkit-scrollbar       { width: 4px; }
.aup-body::-webkit-scrollbar-thumb { background: var(--bd); border-radius: 2px; }

/* ════════════════════════════════════════
   SECTION HEADER
════════════════════════════════════════ */
.aup-sec-hd {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 18px 6px 10px;
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--tx3);
}

.aup-sec-hd:first-child {
  padding-top: 8px;
}

.aup-sec-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ════════════════════════════════════════
   GRID
════════════════════════════════════════ */
.aup-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 6px;
}

@media (max-width: 640px) {
  .aup-body {
    padding: 8px 10px 14px;
  }

  .aup-sec-hd {
    padding: 16px 4px 9px;
    font-size: 11px;
  }
}

/* ════════════════════════════════════════
   GRID ITEM
════════════════════════════════════════ */
.aup-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 14px 12px 12px;
  border-radius: 12px;
  border: 1.5px solid transparent;
  background: transparent;
  cursor: pointer;
  outline: none;
  min-height: 178px;
  transition: background var(--ease), border-color var(--ease), transform 0.1s ease;
}
.aup-item:hover  { background: var(--hov); transform: scale(1.05); }
.aup-item:active { transform: scale(0.95); transition-duration: 0.05s; }
.aup-item.sel    { background: var(--sel-bg); border-color: var(--sel-bd); }

.aup-em {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 96px;
  border-radius: 8px;
  overflow: visible;
  font-size: 22px;
  line-height: 1.1;
}

.aup-face {
  width: auto;
  height: auto;
  max-width: none;
  max-height: none;
  object-fit: unset;
  display: block;
  border-radius: 0;
}

.aup-nm {
  font-size: 12px;
  color: var(--tx2);
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 3px;
}
.aup-item.sel .aup-nm { color: var(--sel-c); }

.aup-cd {
  font-family: ui-monospace, 'Cascadia Code', 'Fira Code', monospace;
  font-size: 10.5px;
  color: var(--tx3);
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 3px;
}
.aup-item.sel .aup-cd { color: var(--sel-c); opacity: 0.75; }

/* ════════════════════════════════════════
   EMPTY STATE
════════════════════════════════════════ */
.aup-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 120px;
  font-size: 13px;
  color: var(--tx3);
  gap: 8px;
}

/* ════════════════════════════════════════
   TOAST
════════════════════════════════════════ */
.aup-toast {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--tx);
  color: var(--bg);
  font-size: 11.5px;
  font-weight: 500;
  padding: 5px 14px;
  border-radius: 20px;
  white-space: nowrap;
  pointer-events: none;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.t-toast-enter-active,
.t-toast-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.t-toast-enter-from,
.t-toast-leave-to    { opacity: 0; transform: translateX(-50%) translateY(8px); }

/* ════════════════════════════════════════
   DETAIL PANEL
════════════════════════════════════════ */
.aup-detail {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg);
  border-top: 1px solid var(--bd);
  box-shadow: 0 -6px 24px rgba(0, 0, 0, 0.09);
  padding: 10px 12px 12px;
  z-index: 5;
}

.aup-detail-top {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.aup-detail-em {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 96px;
  max-width: none;
  min-height: 76px;
  border-radius: 8px;
  overflow: visible;
  font-size: 30px;
  line-height: 1;
  flex-shrink: 0;
  user-select: none;
}

.aup-detail-face {
  width: auto;
  height: auto;
  max-width: none;
  max-height: none;
  object-fit: unset;
  display: block;
  border-radius: 0;
}

.aup-detail-meta {
  flex: 1;
  min-width: 0;
}

.aup-detail-nm {
  font-size: 13px;
  font-weight: 600;
  color: var(--tx);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.aup-detail-nm2 {
  font-size: 10.5px;
  color: var(--tx3);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.aup-detail-actions {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.aup-detail-badge {
  font-family: ui-monospace, 'Cascadia Code', 'Fira Code', monospace;
  font-size: 10px;
  font-weight: 600;
  color: var(--sel-c);
  background: var(--sel-bg);
  border: 1px solid var(--sel-bd);
  border-radius: 4px;
  padding: 1px 6px;
  line-height: 1.6;
}

.aup-detail-btn {
  font-size: 10px;
  font-weight: 500;
  color: var(--tx2);
  background: var(--surface);
  border: 1px solid var(--bd);
  border-radius: 4px;
  padding: 1.5px 7px;
  cursor: pointer;
  line-height: 1.6;
  transition: color var(--ease), border-color var(--ease), background var(--ease);
  white-space: nowrap;
}
.aup-detail-btn:hover         { color: var(--tx); border-color: var(--sel-c); }
.aup-detail-btn--p            { color: var(--sel-c); background: var(--sel-bg); border-color: var(--sel-bd); }
.aup-detail-btn--p:hover      { opacity: 0.75; }

.aup-detail-x {
  flex-shrink: 0;
  border: none;
  background: transparent;
  color: var(--tx3);
  cursor: pointer;
  font-size: 11px;
  line-height: 1;
  padding: 3px 5px;
  border-radius: 5px;
  margin-top: 1px;
  transition: color var(--ease), background var(--ease);
}
.aup-detail-x:hover { color: var(--tx); background: var(--hov); }

.aup-detail-desc {
  margin: 8px 0 0;
  font-size: 11px;
  color: var(--tx2);
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Detail slide-up transition ── */
.t-detail-enter-active { transition: transform 0.2s cubic-bezier(0.34, 1.2, 0.64, 1), opacity 0.18s ease; }
.t-detail-leave-active { transition: transform 0.15s ease, opacity 0.14s ease; }
.t-detail-enter-from,
.t-detail-leave-to    { transform: translateY(100%); opacity: 0; }
</style>
