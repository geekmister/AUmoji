# AUmoji Astro Website

现代化的表情选择器网站，使用 Astro 4.7 + Vue 3 构建，支持 MDX 文档。

## 快速开始

### 安装依赖

```bash
pnpm install
```

### 开发模式

```bash
cd apps/aumoji-web
pnpm dev
```

访问 `http://localhost:3000`

### 构建生产版本

```bash
pnpm build
```

静态网站将生成在 `dist/` 目录

### 预览构建结果

```bash
pnpm preview
```

## 项目结构

```
src/
├── layouts/
│   ├── Base.astro       # 基础 HTML 模板
│   └── Main.astro       # 带导航栏和页脚的布局
├── components/
│   ├── Header.astro     # 导航栏
│   ├── Footer.astro     # 页脚
│   ├── Docs.vue         # 表情浏览和搜索
│   └── PopupDemo.vue    # 选择器演示
├── pages/
│   ├── index.astro      # 首页
│   ├── docs.astro       # 文档主页
│   ├── docs/index.astro # 文档列表
│   ├── docs/[...slug].astro  # 文档动态路由
│   └── playground.astro # 演示页面
├── content/
│   ├── config.ts        # Content Collections 配置
│   └── docs/
│       ├── quick-start.mdx
│       ├── au-reference.mdx
│       └── facs-guide.mdx
├── lib/
│   └── composables.js   # 主题和语言 composables
├── styles/
│   └── global.css       # 全局样式
└── assets/              # 静态资源
```

## 关键特性

- ✅ **静态生成** — Astro 预渲染所有页面
- ✅ **MDX 文档** — 支持 Markdown + React/Vue 组件混合
- ✅ **主题系统** — 深色/浅色模式自动切换
- ✅ **多语言** — 中英文双语支持
- ✅ **无 JavaScript** — 关键路径完全静态
- ✅ **性能优化** — 按需加载（`client:load`）

## 集成的依赖

- `aumoji-picker` — 表情选择器组件
- `aumoji-data` — 31 个表情数据源

## 部署到 GitHub Pages

GitHub Actions 会自动在每次推送时构建并部署到 GitHub Pages。

查看 `.github/workflows/deploy.yml` 了解详情。

本项目文档使用以下工具构建：

- [Astro](https://astro.build)
- [Vue 3](https://vuejs.org)
- [Tailwind CSS](https://tailwindcss.com)
- [MDX](https://mdxjs.com)
