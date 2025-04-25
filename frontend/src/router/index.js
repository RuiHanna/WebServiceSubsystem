// src/router/index.js
import {createRouter, createWebHistory} from 'vue-router'
import KgGraph from '@/components/KgGraph.vue' // 示例：主页
import TestPage1 from '@/components/TestPage1.vue'     // 示例页面
import TestPage2 from '@/components/TestPage2.vue'
import TestPage3 from '@/components/TestPage3.vue'

const routes = [
    {path: '/', component: KgGraph},
    {path: '/page1', component: TestPage1},
    {path: '/page2', component: TestPage2},
    {path: '/page3', component: TestPage3},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
