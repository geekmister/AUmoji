import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import App from './App.vue'
import Home from './pages/Home.vue'
import Playground from './pages/Playground.vue'
import Docs from './pages/Docs.vue'

const router = createRouter({
  // Respect Vite base path (e.g. /AUmoji/ on GitHub Pages) for correct initial routing.
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',            component: Home        },
    { path: '/playground',  component: Playground  },
    { path: '/docs',        component: Docs        },
  ],
  scrollBehavior(to, from, saved) {
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return saved || { top: 0 }
  },
})

createApp(App).use(router).mount('#app')
