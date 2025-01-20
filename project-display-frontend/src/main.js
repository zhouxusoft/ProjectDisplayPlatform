import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Projects from './views/Projects.vue'
import About from './views/About.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'

// 定义路由
const router = createRouter(
    {
        history: createWebHashHistory(),
        routes: [
            { path: '/', component: Home },
            { path: '/projects', component: Projects },
            { path: '/about', component: About },
            { path: '/login', component: Login },
            { path: '/register', component: Register },
        ]
    }
)

const app = createApp(App)

app.use(ElementPlus)

app.use(router).mount('#app')