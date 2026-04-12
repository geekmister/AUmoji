import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import vue from '@astrojs/vue'
import { resolve } from 'path'

export default defineConfig({
  integrations: [
    mdx(),
    vue(),
  ],
  base: process.env.CI ? '/AUmoji/' : '/',
  trailingSlash: 'never',
  vite: {
    resolve: {
      alias: {
        'aumoji-picker': resolve('./../../packages/aumoji-picker/src/index.js'),
      },
    },
  },
})
