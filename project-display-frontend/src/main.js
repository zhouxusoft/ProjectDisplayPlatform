import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Projects from './views/Projects.vue'
import About from './views/About.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import ProjectDetail from './views/ProjectDetail.vue'
import NewProject from './views/NewProject.vue'
import Chat from './views/Chat.vue'
import { globalData } from './views/globalData.js'

// 定义路由
const router = createRouter(
    {
        history: createWebHistory(),
        routes: [
            { path: '/', component: Home },
            { path: '/projects', component: Projects },
            { path: '/about', component: About },
            { path: '/login', component: Login },
            { path: '/register', component: Register },
            {
                path: '/projectDetail/:id',
                component: ProjectDetail,
                props: true
            },
            { path: '/newProject', component: NewProject },
            { path: '/chat', component: Chat },
        ]
    }
)

router.beforeEach((_, from, next) => {
    globalData.previousPage = from.path;
    next();
})

const app = createApp(App)

app.use(ElementPlus)

app.use(router).mount('#app')