import { defineConfig } from 'astro/config'
import vue from '@astrojs/vue'
import { resolve } from 'path'

export default defineConfig({
  integrations: [
    vue(),
  ],
  base: process.env.CI ? '/AUmoji/' : '/',
  trailingSlash: 'never',
  vite: {
    resolve: {
      alias: {
        'aumoji-picker': resolve('./../../packages/aumoji-picker/src/index.js'),
        'aumoji-data': resolve('./../../packages/aumoji-data/index.js'),
      },
    },
  },
})
