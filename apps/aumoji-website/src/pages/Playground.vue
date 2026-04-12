<template>
  <div class="pg-page">
    <div class="pg-hd">
      <h1 class="pg-title">{{ lang === 'zh' ? '交互演示场' : 'Interactive Playground' }}</h1>
      <p class="pg-sub">{{ lang === 'zh' ? '实时调整配置，查看 AUmoji Picker 的效果变化' : 'Tweak settings in real-time and see AUmoji Picker respond instantly' }}</p>
    </div>

    <div class="pg-body">

      <!-- Config Panel -->
      <div class="card pg-config">
        <div class="config-header">
          <p class="config-title">⚙️ &nbsp;{{ lang === 'zh' ? '配置' : 'Config' }}</p>
          <button class="reset-btn" @click="reset" type="button">{{ lang === 'zh' ? '重置' : 'Reset' }}</button>
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '主题' : 'Theme' }} (theme)</label>
          <div class="seg-ctrl">
            <button v-for="opt in ['light','dark','auto']" :key="opt"
              :class="['seg-btn', cfg.theme === opt && 'active']"
              @click="cfg.theme = opt">{{ opt }}</button>
          </div>
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '语言' : 'Language' }} (lang)</label>
          <div class="seg-ctrl">
            <button v-for="opt in ['zh','en']" :key="opt"
              :class="['seg-btn', cfg.lang === opt && 'active']"
              @click="cfg.lang = opt">{{ opt }}</button>
          </div>
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '默认分类' : 'Default Category' }} (defaultCategory)</label>
          <div class="seg-ctrl" style="flex-wrap:wrap">
            <button v-for="opt in ['basic','compound','micro','single']" :key="opt"
              :class="['seg-btn', cfg.defaultCategory === opt && 'active']"
              @click="cfg.defaultCategory = opt">{{ opt }}</button>
          </div>
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '复制格式' : 'Copy Format' }} (copyFormat)</label>
          <div class="seg-ctrl">
            <button v-for="opt in ['auCode','prompt','none']" :key="opt"
              :class="['seg-btn', cfg.copyFormat === opt && 'active']"
              @click="cfg.copyFormat = opt">{{ opt }}</button>
          </div>
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '显示搜索' : 'Show Search' }} (showSearch)</label>
          <div class="seg-ctrl">
            <button :class="['seg-btn', cfg.showSearch && 'active']" @click="cfg.showSearch = true">true</button>
            <button :class="['seg-btn', !cfg.showSearch && 'active']" @click="cfg.showSearch = false">false</button>
          </div>
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '宽度' : 'Width' }} (width): {{ cfg.width }}px</label>
          <input type="range" min="280" max="500" v-model.number="cfg.width" class="range-input" />
        </div>

        <div class="config-group">
          <label class="config-label">{{ lang === 'zh' ? '高度' : 'Height' }} (height): {{ cfg.height }}px</label>
          <input type="range" min="320" max="640" v-model.number="cfg.height" class="range-input" />
        </div>

        <!-- Code preview -->
        <div style="margin-top:20px">
          <div class="code-preview-hd">
            <p class="config-label">{{ lang === 'zh' ? '生成代码' : 'Generated Code' }}</p>
            <button class="copy-code-btn" @click="copyCode" :class="{ copied: codeCopied }" type="button">
              {{ codeCopied ? (lang === 'zh' ? '✓ 已复制' : '✓ Copied') : (lang === 'zh' ? '复制' : 'Copy') }}
            </button>
          </div>
          <div style="background:rgba(0,0,0,0.4); border:1px solid var(--card-bd); border-radius:8px; padding:12px; font-family:monospace; font-size:11.5px; color:#a5f3fc; line-height:1.7; white-space:pre-wrap; word-break:break-all">{{ generatedCode }}</div>
        </div>
      </div>

      <!-- Picker Preview -->
      <div class="pg-preview">
        <AUmojiPicker
          :key="pickerKey"
          :theme="cfg.theme"
          :lang="cfg.lang"
          :width="cfg.width"
          :height="cfg.height"
          :default-category="cfg.defaultCategory"
          :show-search="cfg.showSearch"
          :copy-format="cfg.copyFormat"
          @select="onSelect"
        />

        <!-- Output -->
        <div v-if="output" class="pg-output card">
          <p class="config-label" style="margin-bottom:10px">📋 &nbsp;{{ lang === 'zh' ? 'onSelect 输出' : 'onSelect output' }}</p>
          <div class="output-row">
            <span class="output-key">emoji</span>
            <span class="output-val">{{ output.emoji }}</span>
          </div>
          <div class="output-row">
            <span class="output-key">name</span>
            <span class="output-val">{{ output.name }}</span>
          </div>
          <div class="output-row">
            <span class="output-key">auCode</span>
            <code class="output-code">{{ output.auCode }}</code>
          </div>
          <div class="output-row" style="align-items:flex-start">
            <span class="output-key">prompt</span>
            <span class="output-val" style="font-size:11px; line-height:1.5">{{ output.prompt }}</span>
          </div>
          <div v-if="output.conflict" class="output-row">
            <span class="output-key" style="color:#f87171">conflict</span>
            <span class="output-val" style="color:#f87171">{{ output.conflict }}</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { AUmojiPicker } from 'aumoji-picker'
import { useLang } from '../composables/useLang.js'

const { lang } = useLang()

const DEFAULT_CFG = {
  theme: 'dark',
  lang: 'zh',
  width: 350,
  height: 450,
  defaultCategory: 'basic',
  showSearch: true,
  copyFormat: 'auCode',
}

const cfg        = ref({ ...DEFAULT_CFG })
const output     = ref(null)
const pickerKey  = ref(0)
const codeCopied = ref(false)

// Re-mount picker when defaultCategory changes (to reset scroll)
watch(() => cfg.value.defaultCategory, () => { pickerKey.value++ })

function reset() {
  cfg.value = { ...DEFAULT_CFG }
  output.value = null
}

async function copyCode() {
  try {
    await navigator.clipboard.writeText(generatedCode.value)
    codeCopied.value = true
    setTimeout(() => { codeCopied.value = false }, 1800)
  } catch {}
}

function onSelect(item) {
  output.value = item
}

const generatedCode = computed(() => {
  const c = cfg.value
  const lines = ['<AUmojiPicker']
  if (c.theme !== 'auto')          lines.push(`  theme="${c.theme}"`)
  if (c.lang !== 'zh')             lines.push(`  lang="${c.lang}"`)
  if (c.width !== 350)             lines.push(`  :width="${c.width}"`)
  if (c.height !== 450)            lines.push(`  :height="${c.height}"`)
  if (c.defaultCategory !== 'basic') lines.push(`  default-category="${c.defaultCategory}"`)
  if (!c.showSearch)               lines.push(`  :show-search="false"`)
  if (c.copyFormat !== 'auCode')   lines.push(`  copy-format="${c.copyFormat}"`)
  lines.push('  @select="handleSelect"')
  lines.push('/>')
  return lines.join('\n')
})
</script>

<style scoped>
/* ── Page layout ── */
.pg-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 56px 24px 80px;
}
.pg-hd {
  margin-bottom: 40px;
}
.pg-title {
  font-size: 26px;
  font-weight: 800;
  color: var(--tx);
  margin-bottom: 6px;
}
.pg-sub { font-size: 15px; color: var(--tx2); }

.pg-body {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

/* Config panel */
.pg-config {
  width: 300px;
  flex-shrink: 0;
  padding: 24px;
  position: sticky;
  top: 72px;
}

/* Picker preview column */
.pg-preview {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* Output card */
.pg-output {
  width: 100%;
  max-width: 460px;
  padding: 18px;
}

@media (max-width: 860px) {
  .pg-body { flex-direction: column; align-items: stretch; }
  .pg-config { width: 100%; position: static; }
  .pg-preview { align-items: stretch; }
}

.config-title { font-size:13px; font-weight:700; color:var(--tx); margin-bottom:0; }
.config-group { margin-bottom:18px; }
.config-label { display:block; font-size:11.5px; font-weight:600; color:var(--tx2); margin-bottom:7px; letter-spacing:0.02em; }

/* Segmented control */
.seg-ctrl { display:flex; gap:3px; }
.seg-btn {
  flex:1; padding:5px 8px; border-radius:7px; border:1px solid var(--card-bd);
  background:transparent; color:var(--tx2); font-size:11.5px; font-weight:500;
  cursor:pointer; transition:all var(--ease); font-family:inherit;
}
.seg-btn:hover  { color:var(--tx); border-color:rgba(255,255,255,0.15); }
.seg-btn.active { background:var(--ac-soft); border-color:var(--ac-bd); color:var(--ac); }

/* Range */
.range-input { width:100%; accent-color:var(--ac); cursor:pointer; }

/* Output */
.output-row  { display:flex; gap:10px; align-items:center; padding:5px 0; border-bottom:1px solid var(--divider); font-size:12.5px; }
.output-row:last-child { border-bottom:none; }
.output-key  { flex-shrink:0; width:60px; font-size:11px; font-weight:600; color:var(--tx3); font-family:monospace; }
.output-val  { color:var(--tx2); }
.output-code { font-family:ui-monospace,monospace; color:#a78bfa; font-size:12px; font-weight:600; }

/* Config header row */
.config-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
.config-header .config-title { margin-bottom:0; }
.reset-btn {
  font-size:11px; font-weight:600; color:var(--tx3);
  background:transparent; border:1px solid var(--card-bd);
  border-radius:6px; padding:3px 10px; cursor:pointer;
  font-family:inherit; transition:all var(--ease);
}
.reset-btn:hover { color:var(--tx); border-color:rgba(255,255,255,0.2); }

/* Code preview header */
.code-preview-hd { display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }
.code-preview-hd .config-label { margin-bottom:0 !important; }
.copy-code-btn {
  font-size:11px; font-weight:600; color:var(--ac);
  background:var(--ac-soft); border:1px solid var(--ac-bd);
  border-radius:6px; padding:3px 10px; cursor:pointer;
  font-family:inherit; transition:all var(--ease);
}
.copy-code-btn:hover { opacity:0.8; }
.copy-code-btn.copied { color:#4ade80; background:rgba(74,222,128,0.1); border-color:rgba(74,222,128,0.3); }

/* ── Page layout ── */
.pg-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 56px 24px 80px;
}
.pg-hd { margin-bottom: 40px; }
.pg-title { font-size: 26px; font-weight: 800; color: var(--tx); margin-bottom: 6px; }
.pg-sub { font-size: 15px; color: var(--tx2); }

.pg-body {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

/* Config panel */
.pg-config {
  width: 300px;
  flex-shrink: 0;
  padding: 24px;
  position: sticky;
  top: 72px;
}

/* Picker preview column */
.pg-preview {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* Output card */
.pg-output {
  width: 100%;
  max-width: 460px;
  padding: 18px;
}

@media (max-width: 860px) {
  .pg-body { flex-direction: column; }
  .pg-config { width: 100%; position: static; }
  .pg-preview { align-items: stretch; }
}
</style>
