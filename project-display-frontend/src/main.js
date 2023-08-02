import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Projects from './views/Projects.vue'
import About from './views/About.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'

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

createApp(App).use(router).mount('#app')