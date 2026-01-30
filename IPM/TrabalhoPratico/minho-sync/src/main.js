import { createApp } from 'vue'
import './style.css'
import App from './views/App.vue'
import router from './routes'

createApp(App).use(router).mount('#app')
