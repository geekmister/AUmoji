<template>
  <div class="docs-outer">

    <!-- Sidebar navigation -->
    <aside class="docs-sidebar">
      <p class="sidebar-title">分类导航</p>
      <a
        v-for="cat in CATEGORIES"
        :key="'nav-' + cat.type"
        :href="'#cat-' + cat.type"
        class="sidebar-link"
      >
        <span class="sidebar-dot" :style="{ background: cat.color }"></span>
        {{ cat.name }}
        <span class="sidebar-count">{{ (AU_DATA[cat.type] || []).length }}</span>
      </a>
    </aside>

    <!-- Main Content -->
    <div class="docs-main">
    <div class="mb-10">
      <h1 class="text-3xl mb-2">AU 指令对照表</h1>
      <p style="color:var(--tx2)">FACS Action Units 完整参考文档 · 共 {{ totalCount }} 条</p>
    </div>

    <!-- Search -->
    <div class="docs-search-wrap mb-8">
      <span style="font-size:14px; color:var(--tx3)">🔍</span>
      <input
        v-model="q"
        class="docs-search"
        placeholder="搜索 AU 编号、表情名称…"
        autocomplete="off"
      />
    </div>

    <!-- Categories -->
    <div v-for="cat in CATEGORIES" :key="cat.type" :id="'cat-' + cat.type" class="mb-12" style="scroll-margin-top: 90px">
      <h2 class="cat-headline" :style="{ '--cat-c': cat.color }">
        <span class="cat-dot" :style="{ background: cat.color }"></span>
        {{ cat.name }}
        <span class="cat-badge">{{ filteredByCat(cat.type).length }}</span>
      </h2>

      <div v-if="filteredByCat(cat.type).length" class="docs-grid">
        <div
          v-for="item in filteredByCat(cat.type)"
          :key="item.auCode"
          class="docs-card"
          :style="{ '--cat-c': cat.color }"
        >
          <div class="docs-card-top">
            <span class="docs-emoji">{{ item.emoji }}</span>
            <div style="flex:1; min-width:0">
              <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap">
                <p class="docs-name">{{ item.name }}</p>
                <span v-if="item.isMicro" class="docs-micro-badge">微</span>
              </div>
              <p class="docs-name-en">{{ item.nameEn }}</p>
            </div>
            <code class="docs-code">{{ item.auCode }}</code>
          </div>

          <p class="docs-desc">{{ item.desc }}</p>
          <p class="docs-desc-en">{{ item.descEn }}</p>

          <!-- Meta tags -->
          <div class="docs-meta">
            <span v-if="item.strength" class="docs-tag">💪 {{ item.strength }}</span>
            <span v-if="item.muscle" class="docs-tag">🔬 {{ item.muscle }}</span>
            <span v-if="item.scene" class="docs-tag docs-tag-scene">🎬 {{ item.scene }}</span>
          </div>

          <details class="docs-prompt-details">
            <summary>AI 提示词</summary>
            <p class="docs-prompt"><span class="prompt-lang">中</span>{{ item.promptCn || item.prompt }}</p>
            <p class="docs-prompt" style="margin-top:6px"><span class="prompt-lang">EN</span>{{ item.promptEn }}</p>
          </details>

          <div v-if="item.conflict" class="docs-conflict">
            ⚠ {{ item.conflict }}
          </div>
          <div class="docs-card-footer">
            <button class="docs-copy-btn" @click="copyAuCode(item.auCode)" type="button">
              {{ copiedCode === item.auCode ? '✓ 已复制' : '复制 AU 代码' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else class="docs-empty">暂无匹配结果</div>
    </div>
    </div><!-- /docs-main -->
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { AU_DATA, CATEGORIES } from 'aumoji-picker'

const q          = ref('')
const copiedCode = ref(null)

const totalCount = computed(() => Object.values(AU_DATA).flat().length)

async function copyAuCode(code) {
  try {
    await navigator.clipboard.writeText(code)
    copiedCode.value = code
    setTimeout(() => { copiedCode.value = null }, 1800)
  } catch {}
}

function filteredByCat(type) {
  const list = AU_DATA[type] || []
  if (!q.value.trim()) return list
  const sq = q.value.toLowerCase()
  return list.filter(item =>
    item.name.toLowerCase().includes(sq) ||
    item.nameEn.toLowerCase().includes(sq) ||
    item.auCode.toLowerCase().includes(sq) ||
    item.desc.toLowerCase().includes(sq)
  )
}
</script>

<style scoped>
/* Search */
.docs-search-wrap {
  display: flex; align-items: center; gap: 10px;
  background: var(--card); border: 1px solid var(--card-bd);
  border-radius: 10px; padding: 0 14px; height: 42px;
  transition: border-color var(--ease);
}
.docs-search-wrap:focus-within { border-color: var(--ac-bd); }
.docs-search {
  flex:1; border:none; outline:none; background:transparent;
  font-size:14px; color:var(--tx); font-family:inherit;
}
.docs-search::placeholder { color:var(--tx3); }

/* Category heading */
.cat-headline {
  display: flex; align-items: center; gap: 10px;
  font-size:18px; font-weight:700; color:var(--tx);
  margin-bottom:16px; padding-bottom:10px;
  border-bottom: 1px solid var(--divider);
}
.cat-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
.cat-badge {
  margin-left:auto; font-size:11px; font-weight:600;
  padding:2px 10px; border-radius:20px;
  background:rgba(255,255,255,0.06); color:var(--tx3);
}

/* Grid */
.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.docs-card {
  background: var(--card); border: 1px solid var(--card-bd);
  border-radius: 12px; padding: 16px;
  transition: border-color var(--ease);
}
.docs-card:hover { border-color: var(--cat-c, var(--ac-bd)); }

.docs-card-top {
  display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}
.docs-emoji { font-size: 28px; flex-shrink:0; }
.docs-name    { font-size:14px; font-weight:600; color:var(--tx); }
.docs-name-en { font-size:11.5px; color:var(--tx3); }
.docs-code {
  margin-left:auto; font-family:ui-monospace,monospace;
  font-size:11px; font-weight:700; padding:3px 8px;
  border-radius:6px; background:rgba(167,139,250,0.12);
  color:#a78bfa; border:1px solid rgba(167,139,250,0.22);
  white-space:nowrap; flex-shrink:0;
}

.docs-desc    { font-size:12.5px; color:var(--tx2); margin-bottom:3px; }
.docs-desc-en { font-size:11.5px; color:var(--tx3); margin-bottom:10px; }

.docs-prompt-details summary {
  font-size:11.5px; color:var(--tx3); cursor:pointer;
  user-select:none; font-weight:500;
}
.docs-prompt {
  font-size:11.5px; color:#a5f3fc; font-family:ui-monospace,monospace;
  margin-top:6px; line-height:1.6;
  background:rgba(0,0,0,0.3); border:1px solid var(--card-bd);
  border-radius:6px; padding:8px 10px;
}

.docs-conflict {
  margin-top:8px; font-size:11.5px; color:#f87171;
  background:rgba(248,113,113,0.08); border:1px solid rgba(248,113,113,0.2);
  border-radius:6px; padding:5px 10px;
}

/* ── 微表情 badge ── */
.docs-micro-badge {
  font-size: 9.5px; font-weight: 700;
  color: #06b6d4; background: rgba(6,182,212,0.12);
  border: 1px solid rgba(6,182,212,0.28);
  border-radius: 4px; padding: 1px 5px;
  letter-spacing: 0.04em;
}

/* ── Meta tags ── */
.docs-meta {
  display: flex; flex-wrap: wrap; gap: 5px;
  margin: 8px 0 4px;
}
.docs-tag {
  font-size: 10.5px; color: var(--tx3);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--card-bd);
  border-radius: 5px; padding: 2px 7px;
  white-space: nowrap; max-width: 100%; overflow: hidden;
  text-overflow: ellipsis;
}
.docs-tag-scene { color: var(--ac); border-color: var(--ac-bd); background: var(--ac-soft); }

/* ── Prompt lang label ── */
.prompt-lang {
  display: inline-block; font-size: 9px; font-weight: 700;
  color: var(--tx3); background: rgba(255,255,255,0.07);
  border-radius: 3px; padding: 0 4px; margin-right: 5px;
  vertical-align: middle; letter-spacing: 0.04em;
}

.docs-empty { color:var(--tx3); font-size:13px; padding:16px 0; }

/* ── 2-column layout ── */
.docs-outer {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 56px 20px 80px;
  gap: 32px;
  align-items: flex-start;
}
.docs-main { flex: 1; min-width: 0; }

/* Sidebar */
.docs-sidebar {
  width: 154px;
  flex-shrink: 0;
  position: sticky;
  top: 76px;
  padding-top: 4px;
}
.sidebar-title {
  font-size: 10.5px; font-weight: 700; color: var(--tx3);
  letter-spacing: 0.08em; text-transform: uppercase;
  padding: 0 8px; margin-bottom: 8px;
}
.sidebar-link {
  display: flex; align-items: center; gap: 7px;
  padding: 6px 8px; border-radius: 7px;
  font-size: 12.5px; color: var(--tx2);
  text-decoration: none; font-weight: 500;
  transition: all var(--ease); margin-bottom: 1px;
}
.sidebar-link:hover { background: var(--card); color: var(--tx); }
.sidebar-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.sidebar-count { margin-left: auto; font-size: 10.5px; color: var(--tx3); }

/* Card footer */
.docs-card-footer {
  margin-top: 10px; padding-top: 10px;
  border-top: 1px solid var(--divider);
  display: flex; justify-content: flex-end;
}
.docs-copy-btn {
  font-size: 11px; font-weight: 600; color: var(--tx3);
  background: transparent; border: 1px solid var(--card-bd);
  border-radius: 6px; padding: 3px 10px; cursor: pointer;
  font-family: inherit; transition: all var(--ease); white-space: nowrap;
}
.docs-copy-btn:hover { color: var(--ac); border-color: var(--ac-bd); background: var(--ac-soft); }

@media (max-width: 768px) {
  .docs-sidebar { display: none; }
  .docs-outer { padding: 40px 16px 60px; }
}
</style>
