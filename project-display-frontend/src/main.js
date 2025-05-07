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
import ProjectDetail from './views/projectDetail.vue'
import NewProject from './views/NewProject.vue'
import Chat from './views/Chat.vue'
import Circle from './views/Circle.vue'
import User from './views/User.vue'
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
            {
                path: '/circle/:id',
                component: Circle, 
                props: true
            },
            {
                path: '/user/:id',
                component: User, 
                props: true
            },
        ]
    }
)

router.beforeEach((to, from, next) => {
    if (!from.fullPath.includes('projectDetail') && !from.fullPath.includes('newProject')) {
        globalData.previousPage = from.fullPath
        globalData.previousPageParams = from.query
    }
    if (to.fullPath == globalData.previousPage) {
        globalData.previousPage = '/projects'
        globalData.previousPageParams = {}
        if (to.fullPath.includes('/user/')) {
            globalData.previousPageParams = {
                kind: 'Users'
            }
        }
    }
    
    window.scrollTo({
		top: 0,
		left: 0,
		behavior: 'smooth'
	})
    next();
})

const app = createApp(App)

app.use(ElementPlus)

app.use(router).mount('#app')