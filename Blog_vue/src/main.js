import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

import './assets/main.css'

const app = createApp(App)

axios.defaults.baseURL = import.meta.env.VITE_API_URL
axios.interceptors.request.use(config => {
  if (config.method === 'get') {
    const cacheBuster = new Date().getTime()
    config.url += (config.url.includes('?') ? '&' : '?') + `_=${cacheBuster}`
  }
  return config
})
app.use(createPinia())
app.use(router, axios)

app.mount('#app')
