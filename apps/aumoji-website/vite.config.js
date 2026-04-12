import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [tailwindcss(), vue()],
  base: process.env.CI ? '/AUmoji/' : '/',
  resolve: {
    alias: {
      // In dev: resolve aumoji-picker directly from source (no build needed)
      'aumoji-picker': resolve(__dirname, '../../packages/aumoji-picker/src/index.js'),
      'aumoji-data':   resolve(__dirname, '../../packages/aumoji-data/index.js'),
    },
  },
  server: {
    port: 3000,
    open: true,
  },
})
