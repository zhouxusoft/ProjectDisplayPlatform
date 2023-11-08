<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const goLogin = () => {
    router.push({ path: '/login' })
}
const goRegister = () => {
    router.push({ path: '/register' })
}

const isLogin = ref(false)
const isSortListShow = ref(false)

/** 
 * 点击显示排序下拉菜单
 */
const showSortList = () => {
    isSortListShow.value = !isSortListShow.value
}

/**
 * 判断用户当前的登录状态
 */
const checkLogin = () => {
    // 发送请求
    fetch('http://127.0.0.1:5000/checkLogin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // 设置请求头
        },
        credentials: 'include', // 在跨域请求中发送 cookies 和 http 认证信息
    }).then(response => response.json()).then(data => {
        // 处理获取的数据
        // console.log(data)
        isLogin.value = data.success
        // console.log(isLogin.value)
    }).catch(error => {
        // 处理请求错误
        console.error('Error:', error)
    })
}
checkLogin()

/**
 * 退出登录
 */
const logout = () => {
    // 发送请求, 清除 cookie
    fetch('http://127.0.0.1:5000/clearCookie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // 设置请求头
        },
        credentials: 'include', // 在跨域请求中发送 cookies 和 http 认证信息
    }).then(response => response.json()).then(data => {
        console.log(data)
        // 设置登录状态
        isLogin.value = false
    }).catch(error => {
        // 处理请求错误
        console.error('Error:', error)
    })
}

</script>

<template>
    <div v-if="!isLogin" class="notlogincontainer">
        <div class="notloginbox">
            <img src="/notlogin.png" alt="" class="notloginimg img-fluid">
            <div class="notlogincontent mb-4">你还未登录哦</div>
            <div class="notloginbtngroup">
                <button @click="goLogin()" class="btn btn-outline-success m-1 notloginbtn">去登录</button>
                <button @click="goRegister()" class="btn btn-outline-primary m-1 notloginbtn">去注册</button>
            </div>
        </div>
    </div>
    <div v-else>
        <div class="container">
            <div class="leftbox d-none d-md-block">
                <div class="headpicturebox">
                    <img class="img-fluid headpicture" src="https://avatars.githubusercontent.com/u/96218937?v=4" alt="">
                </div>
            </div>
            <div class="rightbox">
                <div class="projectboxborder">
                    <div class="projectboxtitlebox">
                        <div class="projectboxtitle">Projects of Mine</div>
                        <div class="projectsortbox">Sort by:
                            <button class="projectsortitembox" @click="showSortList()">
                                Most stars <span class="dropdownicon">&#xf0d7</span>
                            </button>
                            <div v-show="isSortListShow" class="dropdownbox">
                            </div>
                        </div>
                    </div>
                    <div class="projectbox">

                    </div>
                </div>

            </div>
        </div>
        您已登录
        <button class="btn btn-outline-success" @click="logout">退出登录</button>
    </div>
</template>

<style scoped>
.notlogincontainer {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
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

.container {
    display: flex;
}

.leftbox {
    width: 300px;
    padding: 16px;
    padding-top: 32px;
    height: 100vh;
    /* border-left: 1px solid black; */
    /* border-right: 1px solid black; */
}

.rightbox {
    flex: 1;
    min-width: 0px;
    padding: 16px;
    padding-top: 32px;
    /* border-right: 1px solid black; */
    height: 100vh;
}

.headpicturebox {
    width: 264px;
    height: 264px;
    border: 2px solid black;
    border-radius: 50%;
    overflow: hidden;
}

.headpicture {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.projectboxtitlebox {
    display: flex;
    justify-content: space-between;
    height: 36px;
}

.projectboxtitle {
    display: flex;
    align-items: center;
}

.projectbox {
    width: 100%;
    height: 400px;
    border: 1px solid black;
    border-radius: 4px;
}

.projectsortbox {
    position: relative;
    font-size: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.projectsortitembox {
    font-size: 13px;
    background-color: rgb(231, 236, 240);
    border: 1px solid #666666;
    border-radius: 4px;
    margin-left: 4px;
    padding: 2px 6px;
}

.projectsortitembox:hover {
    background-color: rgb(206, 213, 220);
}

.dropdownicon {
    font-family: "Font Awesome 6 Free";
	font-weight: 600;
    margin: 0 2px 0 4px;
}

.dropdownbox {
    position: absolute;
    left: 32px;
    top: 32px;
    width: 120px;
    height: 100px;
    border: 1px solid black;
}
</style>