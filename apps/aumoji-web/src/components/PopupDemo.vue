<template>
  <div class="demo">
    <button class="open-btn" @click="showPicker = true">
      🎭 {{ lang === 'zh' ? '打开选择器' : 'Open Picker' }}
    </button>

    <div v-if="showPicker" class="modal-backdrop" @click.self="showPicker = false">
      <div class="modal">
        <!-- TODO: 这里插入 AUmoji 选择器组件 -->
        <p style="text-align: center; color: var(--tx2);">
          {{ lang === 'zh' ? 'AUmoji 选择器将在此显示' : 'AUmoji Picker will be displayed here' }}
        </p>
        <button class="close-btn" @click="showPicker = false">关闭 / Close</button>
      </div>
    </div>

    <div v-if="selectedAU" class="result-box">
      <h3>{{ lang === 'zh' ? '选中表情' : 'Selected Expression' }}</h3>
      <pre>{{ JSON.stringify(selectedAU, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showPicker = ref(false)
const selectedAU = ref(null)
const lang = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('au-lang') || 'zh' : 'zh')

if (typeof window !== 'undefined') {
  window.addEventListener('lang-change', (e) => {
    lang.value = e.detail.lang
  })
}
</script>

<style scoped>
.demo {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
}

.open-btn {
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  background: var(--ac);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.14s ease;
}

.open-btn:hover {
  background: var(--ac2);
  transform: translateY(-2px);
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg);
  border: 1px solid var(--card-bd);
  border-radius: 12px;
  padding: 40px;
  max-width: 600px;
  width: 90%;
}

.close-btn {
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background: var(--card);
  color: var(--tx);
  border: 1px solid var(--card-bd);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.14s ease;
}

.close-btn:hover {
  background: var(--hover-bg);
}

.result-box {
  background: var(--card);
  border: 1px solid var(--card-bd);
  border-radius: 8px;
  padding: 20px;
  width: 100%;
  max-width: 600px;
}

.result-box h3 {
  margin-bottom: 16px;
}

.result-box pre {
  margin: 0;
  overflow-x: auto;
}
</style>
