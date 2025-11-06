
import router from './router'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/main.css'

const pinia = createPinia()
const app = createApp(App)
app.config.devtools = false 
app.use(pinia)
app.use(router)
app.mount('#app')
