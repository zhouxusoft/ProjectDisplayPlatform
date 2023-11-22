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

const sortModes = [
    {
        id: 1,
        name: 'Most stars'
    },
    {
        id: 2,
        name: 'Last updated'
    },
    {
        id: 3,
        name: 'Create time'
    }
]

const isLogin = ref(false)
const currentSortMode = ref({
    id: 2,
    name: 'Last updated'
})

/**
 * 切换项目列表排序方式
 * @param {JSON} sortMode
 */
const changeSortMode = (sortMode) => {
    currentSortMode.value = sortMode
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
                            <button class="projectsortitembox" @click="">
                                <span class="dropdownname">{{ currentSortMode.name }}</span>
                                <span class="dropdownicon">&#xf0d7</span>
                                <div class="dropdownboxborder">
                                    <div class="dropdownbox">
                                        <div v-for="sortMode in sortModes" class="dropdownboxitem" :key="sortMode.id" :sortMode="sortMode" @click="changeSortMode(sortMode)">
                                            <span class="dropdownboxitemselect"><span v-if="currentSortMode.id == sortMode.id">&#xf00c</span></span>
                                            <span class="dropdownboxitemname">{{ sortMode.name }}</span>
                                        </div>
                                    </div>
                                </div>
                            </button>
                        </div>
                    </div>
                    <div class="projectbox">

                    </div>
                </div>
            </div>
        </div>
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
}

.rightbox {
    flex: 1;
    min-width: 0px;
    padding: 16px;
    padding-top: 32px;
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
    height: 40px;
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
    background-color: rgb(255, 255, 255);
    border: 1px solid #666666;
    border-radius: 4px;
    margin-left: 4px;
    padding: 2px 6px;
    width: 111px;
}

.projectsortitembox:hover .dropdownicon{
    transform: rotate(360deg);
    transition: transform 0.3s ease-out;
}

.projectsortitembox:hover .dropdownboxborder {
    height: 82px;
    padding: 0 5px;
}

.dropdownicon {
    display: inline-block;
    font-family: "Font Awesome 6 Free";
	font-weight: 600;
    margin: 0 2px 0 6px;
}

.dropdownname {
    display: inline-block;
    width: 81px;
}

.dropdownboxborder {
    z-index: 99;
    position: absolute;
    left: 42px;
    top: 33px;
    width: 130px;
    height: 0;
    transition: 0.2s;
    display: flex;
    justify-content: center;
}

.dropdownbox {
    height: 100%;
    padding: 0 5px;
    overflow: hidden;
    width: 120px;
    visibility: hidden;
}

.projectsortitembox:hover .dropdownbox {
    visibility: visible;
    padding: 5px;
    border-radius: 4px;
    background-color: rgb(255, 255, 255);
    box-shadow: rgba(1, 4, 9, 0.12) 0px 1px 3px, rgba(52, 59, 67, 0.12) 0px 8px 24px;
}

.dropdownboxitem {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    padding: 4px 0;
    height: 24px;
    align-items: center;
    border-radius: 4px;
}

.dropdownboxitem:hover {
    background-color: rgb(231, 236, 240);
}

.dropdownboxitemselect {
    font-family: "Font Awesome 6 Free";
	font-weight: 600;
    width: 20px;
    display: flex;
    justify-content: center;

}

.dropdownboxitemname {
    flex: 1;
    text-align: left;
    margin-left: 2px;
}
</style>