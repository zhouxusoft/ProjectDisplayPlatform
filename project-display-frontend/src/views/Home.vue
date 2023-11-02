<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goLogin = () => {
    router.push({ path: '/login' })
}
const goRegister = () => {
    router.push({ path: '/register' })
}

/** 判断用户当前的登录状态 */
const isLogin = () => {
    
}
</script>

<template>
    <div class="notlogincontainer">
        <div class="notloginbox">
            <img src="/notlogin.png" alt="" class="notloginimg img-fluid">
            <div class="notlogincontent mb-4">你还未登录哦</div>
            <div class="notloginbtngroup">
                <button @click="goLogin()" class="btn btn-outline-success m-1 notloginbtn">去登录</button>
                <button @click="goRegister()" class="btn btn-outline-primary m-1 notloginbtn">去注册</button>
            </div>
        </div>
    </div>
</template>

<style scoped>

.notlogincontainer {
    display: flex;
    justify-content: center;
    align-items: center;
    height:80vh;
}
.notloginbox {
    width: fit-content;
    margin: auto;
}

.notloginimg {
    width: 480px;
}

.notlogincontent {
    margin: auto;
    width: fit-content;
    font-size: 1.5rem;
    color: #002d80;
}

.notloginbtngroup {
    width: fit-content;
    margin: auto;
}

.notloginbtn {
    width: 120px;
}
</style>