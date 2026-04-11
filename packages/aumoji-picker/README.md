# aumoji-picker

> Cinematic FACS Action Unit expression picker for Vue 3

[![npm version](https://img.shields.io/npm/v/aumoji-picker?style=flat-square&color=8b5cf6)](https://www.npmjs.com/package/aumoji-picker)
[![npm downloads](https://img.shields.io/npm/dm/aumoji-picker?style=flat-square&color=6366f1)](https://www.npmjs.com/package/aumoji-picker)
[![license](https://img.shields.io/github/license/Geekmister/AUmoji?style=flat-square&color=64748b)](./LICENSE)

**AUmoji Picker** is a self-contained, zero-dependency Vue 3 component for selecting [FACS](https://en.wikipedia.org/wiki/Facial_Action_Coding_System) (Facial Action Coding System) expressions — built for AI video creators, digital human pipelines, and motion-capture workflows.

👉 [Live Demo & Docs](https://geekmister.github.io/AUmoji/)

---

## Installation

```bash
npm install aumoji-picker
# or
pnpm add aumoji-picker
# or
yarn add aumoji-picker
```

---

## Usage

```vue
<script setup>
import { AUmojiPicker } from 'aumoji-picker'
</script>

<template>
  <AUmojiPicker
    theme="dark"
    lang="zh"
    :width="350"
    :height="450"
    @select="(item) => console.log(item.auCode)"
  />
</template>
```

---

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `theme` | `'light' \| 'dark' \| 'auto'` | `'auto'` | Color theme. `'auto'` follows system preference |
| `lang` | `'zh' \| 'en'` | `'zh'` | UI language |
| `width` | `Number` | `350` | Picker width in px |
| `height` | `Number` | `450` | Picker height in px |
| `defaultCategory` | `'basic' \| 'compound' \| 'micro' \| 'single'` | `'basic'` | Category shown on mount |
| `showSearch` | `Boolean` | `true` | Show the search bar |
| `copyFormat` | `'auCode' \| 'prompt' \| 'none'` | `'auCode'` | What to auto-copy on item click |

---

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `select` | `AUItem` | Fired on every item click with the full item object |

### `AUItem` shape

```ts
{
  name: string        // Chinese name, e.g. "真笑(自然)"
  nameEn: string      // English name, e.g. "Genuine Smile"
  emoji: string       // Emoji character, e.g. "😄"
  auCode: string      // AU code string, e.g. "AU6+AU12"
  desc: string        // Chinese description
  descEn: string      // English description
  prompt: string      // AI prompt text for use in video generation
  conflict?: string   // Optional conflict warning
}
```

---

## Exported utilities

```js
import { AUmojiPicker, AU_DATA, CATEGORIES } from 'aumoji-picker'

// AU_DATA — grouped by category type
// { basic: [...], compound: [...], micro: [...], single: [...] }

// CATEGORIES — category metadata array
// [{ type, name, nameEn, emoji, color }, ...]
```

---

## Data overview

| Category | Count | Description |
|----------|-------|-------------|
| `basic` | 8 | Basic emotions (joy, anger, surprise…) |
| `compound` | 4 | Compound expressions (contempt, nervous…) |
| `micro` | 3 | Micro-expressions (micro-smile, micro-fear…) |
| `single` | 6 | Single AUs (AU1, AU2, AU4, AU7…) |

---

## License

MIT © [Geekmister](https://github.com/Geekmister)
