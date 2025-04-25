// src/main.js
import {createApp} from 'vue'
import App from './App.vue'
import router from './router' // 如果你使用了 vue-router
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
