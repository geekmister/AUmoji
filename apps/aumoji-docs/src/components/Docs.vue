<template>
  <div class="docs-wrapper">
    <div class="search-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        :placeholder="lang === 'zh' ? '搜索表情...' : 'Search expressions...'"
        class="search-input"
      />
    </div>

    <div class="category-tabs">
      <button
        v-for="(cat, idx) in categories"
        :key="idx"
        :class="['tab', { active: activeCategory === idx }]"
        @click="activeCategory = idx"
      >
        {{ cat.emoji }} {{ lang === 'zh' ? cat.name : cat.nameEn }}
      </button>
    </div>

    <div class="au-grid">
      <div
        v-for="au in filteredData"
        :key="au.id"
        class="au-card"
        @click="selectedAU = au"
      >
        <div class="au-emoji">{{ au.emoji }}</div>
        <div class="au-name">{{ lang === 'zh' ? au.nameCn : au.nameEn }}</div>
        <button class="copy-btn" @click.stop="copyCode(au)">📋</button>
      </div>
    </div>

    <div v-if="selectedAU" class="detail-panel">
      <button class="close-btn" @click="selectedAU = null">✕</button>
      <div class="detail-content">
        <div class="detail-header">
          <span class="detail-emoji">{{ selectedAU.emoji }}</span>
          <div>
            <h2>{{ lang === 'zh' ? selectedAU.nameCn : selectedAU.nameEn }}</h2>
            <p class="detail-code">{{ selectedAU.auCode }}</p>
          </div>
        </div>

        <div class="detail-desc">
          <p>{{ lang === 'zh' ? selectedAU.descCn : selectedAU.descEn }}</p>
        </div>

        <div class="detail-grid">
          <div class="detail-item">
            <span class="label">{{ lang === 'zh' ? '强度' : 'Intensity' }}</span>
            <span class="value">{{ selectedAU.strength }}</span>
          </div>
          <div class="detail-item">
            <span class="label">{{ lang === 'zh' ? '肌肉' : 'Muscle' }}</span>
            <span class="value">{{ selectedAU.muscle }}</span>
          </div>
          <div class="detail-item">
            <span class="label">{{ lang === 'zh' ? '场景' : 'Scene' }}</span>
            <span class="value">{{ selectedAU.scene }}</span>
          </div>
        </div>

        <button class="copy-prompt" @click="copyPrompt(selectedAU)">
          {{ lang === 'zh' ? '📋 复制提示词' : '📋 Copy Prompt' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { AU_DATA, CATEGORIES } from '../data/auData.js'

// 收集所有表情数据
const allExpressions = Object.values(AU_DATA).flat()

// 构建分类数据
const categories = [
  { emoji: '📌', name_cn: '全部', name_en: 'All' },
  ...CATEGORIES,
]

const searchQuery = ref('')
const activeCategory = ref(0)
const selectedAU = ref(null)
const lang = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('au-lang') || 'zh' : 'zh')

const filteredData = computed(() => {
  let filtered = allExpressions
  
  // 按分类过滤
  if (activeCategory.value !== 0) {
    const category = categories[activeCategory.value].type
    filtered = filtered.filter(au => au.category === category)
  }

  // 按搜索词过滤
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    filtered = filtered.filter(au => 
      (au.nameCn || '').toLowerCase().includes(q) ||
      (au.nameEn || '').toLowerCase().includes(q) ||
      (au.auCode || '').toLowerCase().includes(q)
    )
  }

  return filtered
})

function copyCode(au) {
  const code = au.auCode || au.id
  navigator.clipboard.writeText(code)
  alert(lang.value === 'zh' ? '已复制!' : 'Copied!')
}

function copyPrompt(au) {
  const text = lang.value === 'zh' ? au.promptCn : au.promptEn
  navigator.clipboard.writeText(text)
  alert(lang.value === 'zh' ? '已复制!' : 'Copied!')
}

// 监听语言变更事件
if (typeof window !== 'undefined') {
  window.addEventListener('lang-change', (e) => {
    lang.value = e.detail.lang
  })
  window.addEventListener('storage', () => {
    lang.value = localStorage.getItem('au-lang') || 'zh'
  })
}
</script>

<style scoped>
.docs-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.search-input {
  width: 100%;
  max-width: 400px;
  padding: 12px 16px;
  font-size: 14px;
  background: var(--card);
  border: 1px solid var(--card-bd);
  border-radius: 8px;
  color: var(--tx);
  transition: all 0.14s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--ac-bd);
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.category-tabs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 24px;
}

.tab {
  padding: 8px 16px;
  font-size: 14px;
  background: var(--card);
  border: 1px solid var(--card-bd);
  border-radius: 6px;
  color: var(--tx2);
  cursor: pointer;
  transition: all 0.14s ease;
}

.tab.active {
  background: var(--ac);
  border-color: var(--ac);
  color: white;
}

.tab:hover {
  border-color: var(--ac-bd);
}

.au-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.au-card {
  background: var(--card);
  border: 1px solid var(--card-bd);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.14s ease;
  position: relative;
}

.au-card:hover {
  border-color: var(--ac-bd);
  background: rgba(124, 58, 237, 0.08);
  transform: translateY(-2px);
}

.au-emoji {
  font-size: 32px;
  margin-bottom: 8px;
}

.au-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--tx);
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.copy-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.14s ease;
}

.au-card:hover .copy-btn {
  opacity: 1;
}

.detail-panel {
  background: var(--card);
  border: 1px solid var(--card-bd);
  border-radius: 8px;
  padding: 24px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  color: var(--tx2);
  font-size: 18px;
  cursor: pointer;
  transition: color 0.14s ease;
}

.close-btn:hover {
  color: var(--tx);
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-header {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.detail-emoji {
  font-size: 48px;
}

.detail-header h2 {
  margin: 0;
  font-size: 24px;
}

.detail-code {
  font-size: 12px;
  color: var(--tx2);
  margin: 4px 0 0 0;
  font-family: monospace;
}

.detail-desc {
  line-height: 1.6;
  color: var(--tx2);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.detail-item {
  background: rgba(124, 58, 237, 0.1);
  border-radius: 6px;
  padding: 12px;
  display: flex;
  flex-direction: column;
}

.detail-item .label {
  font-size: 12px;
  color: var(--tx2);
  margin-bottom: 4px;
}

.detail-item .value {
  font-size: 14px;
  font-weight: 600;
  color: var(--ac);
}

.copy-prompt {
  background: var(--ac);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.14s ease;
}

.copy-prompt:hover {
  background: var(--ac2);
  transform: translateY(-2px);
}
</style>
