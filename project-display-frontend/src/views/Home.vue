<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { checkLoginAPI, clearCookieAPI } from '../api/api'
import ProjectItem from '../components/ProjectItem.vue'

const router = useRouter()
const goLogin = () => {
  router.push({ path: '/login' })
}
const goRegister = () => {
  router.push({ path: '/register' })
}

const centerDialogVisible = ref(false)

const isLoading = ref(false)

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

const projects = ref([
  {
    id: 1,
    usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
    name: "RainManGO/vue3-composition-admin",
    main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
    tags: ["JavaScript", "Flask", "Vue", "BootStrap"],
    language: { color: "449633", name: "Vue" },
    starnum: 99586,
    updatetime: "2022/8/19",
    cover: '',
    pagename: '1'
  },
  {
    id: 2,
    usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
    name: "jeecgboot/jeecgboot-vue3",
    main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
    tags: ["JavaScript", "Vue", "BootStrap"],
    language: { color: "481828", name: "JavaScript" },
    starnum: 758,
    updatetime: "2022/8/19",
    cover: '',
    pagename: '1'
  }
])

const starred = ref([
  {
    id: 1,
    projectid: 1
  },
  {
    id: 2,
    projectid: 3
  }
])

const isLogin = ref(-1)
const currentSortMode = ref({
  id: 2,
  name: 'Last updated'
})

/**
 * 切换项目列表排序方式
 * @param {JSON} sortMode
 */
const changeSortMode = (sortMode) => {
  const sortitembox = document.getElementById("sortitembox")
  currentSortMode.value = sortMode
  sortitembox.classList.remove("projectsortitembox")
  sortitembox.classList.add("clickdisvisable")
  // 设置延迟才能使属性暂时失效
  setTimeout(() => {
    sortitembox.classList.remove("clickdisvisable")
    sortitembox.classList.add("projectsortitembox")
  }, 1000)
}

/**
 * 判断用户当前的登录状态
 */
const checkLogin = () => {
  isLoading.value = true
  // 发送请求
  checkLoginAPI().then(res => {
    if (res.success) {
      isLogin.value = 1
    } else {
      isLogin.value = 0
    }
    isLoading.value = false
  }).catch(error => {
    ElMessage({
      message: '请求失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
    isLogin.value = 0
    isLoading.value = false
  })
}

/**
 * 退出登录
 */
const logout = () => {
  // 发送请求, 清除 cookie
  clearCookieAPI().then(res => {
    ElMessage({
      message: '退出成功',
      type: 'success',
      plain: true,
      offset: 9,
    })
    // 设置登录状态
    isLogin.value = 0
  }).catch(error => {
    ElMessage({
      message: '退出失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
  })
}

onMounted(() => {
  checkLogin()
})

</script>

<template>
  <div v-loading="isLoading">
    <div v-if="isLogin === 0" class="notlogincontainer">
      <div class="notloginbox">
        <img src="/notlogin.png" alt="" class="notloginimg img-fluid">
        <div class="notlogincontent mb-4">你还未登录哦</div>
        <div class="notloginbtngroup">
          <button @click="goLogin()" class="btn btn-outline-success m-1 notloginbtn">去登录</button>
          <button @click="goRegister()" class="btn btn-outline-primary m-1 notloginbtn">去注册</button>
        </div>
      </div>
    </div>
    <div v-if="isLogin === 1">
      <div class="container">
        <div class="leftbox d-none d-md-block">
          <div class="headpicturebox">
            <img class="img-fluid headpicture" src="https://avatars.githubusercontent.com/u/96218937?v=4" alt="">
          </div>
          <div class="namebox">
            <div class="name">Godxu</div>
          </div>
          <div class="boibox">
            <div>我是一个学习编程的新手，来自江西上饶。</div>
          </div>
          <div class="btnbox">
            <button type="button" class="sbtn" @click="centerDialogVisible = true">Edit Profile</button>
          </div>
          <div class="infobox">
            <span class="kindicon">&#xf500</span>
            <span>2 followers · 4 following</span>
          </div>
          <div class="locationbox">
            <span class="kindicon" style="font-size: 14px">&#xf3c5</span>
            <span>江西</span>
          </div>
          <div class="hr"></div>
        </div>
        <div class="rightbox">
          <div class="projectboxborder">
            <div class="projectboxtitlebox">
              <div class="projectboxtitle">Messages of Mine</div>
              <el-badge :value="8" :max="10" class="item">
                <el-button @click="this.$router.push('/chat')"><span class="kindicon" style="font-size: 14px">&#xf0e0</span>My Messages</el-button>
              </el-badge>
            </div>
            <div class="projectbox mt-1 px-3 py-3 mb-2">
              <div>你的文章 <span style="color: #0349B4; text-decoration: underline">RainManGO/vue3-composition-admin</span>
                被<span style="color: #0349B4; text-decoration: underline"> OuYangPeng </span>等3个人点赞</div>
            </div>
            <div class="projectbox mt-1 px-3 py-3 mb-2">
              <div>你的文章 <span style="color: #0349B4; text-decoration: underline">RainManGO/vue3-composition-admin</span>
                被<span style="color: #0349B4; text-decoration: underline"> OuYangPeng </span>等2个人评论</div>
            </div>
            <div class="projectbox mt-1 px-3 py-3 mb-2">
              <div><span style="color: #0349B4; text-decoration: underline">OuYangPeng</span> 关注了你</div>
            </div>
          </div>
          <div class="projectboxborder mt-4">
            <div class="projectboxtitlebox">
              <div class="projectboxtitle">Projects of Mine</div>
              <div class="projectsortbox">Sort by:
                <button id="sortitembox" class="projectsortitembox" @click="">
                  <span class="dropdownname">{{ currentSortMode.name }}</span>
                  <span class="dropdownicon">&#xf0d7</span>
                  <div class="dropdownboxborder">
                    <div class="dropdownbox">
                      <div v-for="sortMode in sortModes" class="dropdownboxitem" :key="sortMode.id" :sortMode="sortMode"
                        @click="changeSortMode(sortMode)">
                        <span class="dropdownboxitemselect"><span
                            v-if="currentSortMode.id == sortMode.id">&#xf00c</span></span>
                        <span class="dropdownboxitemname">{{ sortMode.name }}</span>
                      </div>
                    </div>
                  </div>
                </button>
              </div>
            </div>
            <div class="projectbox mt-1 px-3 py-3">
              <ProjectItem v-for="project in projects" :key="project.id" :project="project" :starred="starred" />
              <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
            </div>
          </div>
        </div>
      </div>
      <button class="btn btn-outline-secondary" @click="logout">退出登录</button>
    </div>
  </div>
  <el-dialog v-model="centerDialogVisible" title="编辑个人资料" width="500" align-center>
    <el-form label-width="100px">
      <el-form-item label="昵称" prop="roleName">
        <el-input placeholder="Godxu" />
      </el-form-item>
    </el-form>
    <el-form label-width="100px">
      <el-form-item label="个性签名" prop="roleName">
        <el-input placeholder="我是一个学习编程的新手，来自江西上饶。" />
      </el-form-item>
    </el-form>
    <el-form label-width="100px">
      <el-form-item label="头像" prop="roleName">
        <el-image
          style="width: 100px; height: 100px"
          src="https://avatars.githubusercontent.com/u/96218937?v=4"
          :zoom-rate="1.2"
          :max-scale="7"
          :min-scale="0.2"
          :preview-src-list="srcList"
          show-progress
          :initial-index="4"
          fit="cover"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="centerDialogVisible = false">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
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
  border: 1px solid black;
  border-radius: 4px;
  flex: 1;
  display: grid;
  gap: 16px;
  min-width: 0px;
}

.projectsortbox {
  position: relative;
  font-size: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.projectsortitembox {
  font-size: 14px;
  background-color: rgb(255, 255, 255);
  border: 1px solid #666666;
  border-radius: 4px;
  margin-left: 4px;
  padding: 2px 6px;
  width: 116px;
  white-space: nowrap;
}

.clickdisvisable {
  font-size: 14px;
  background-color: rgb(255, 255, 255);
  border: 1px solid #666666;
  border-radius: 4px;
  margin-left: 4px;
  padding: 2px 6px;
  width: 116px;
  white-space: nowrap;
}

.projectsortitembox:hover .dropdownicon {
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
  width: 85px;
}

.dropdownboxborder {
  z-index: 99;
  position: absolute;
  left: 47px;
  top: 34px;
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

.namebox {
  margin: 10px;
  font-size: 20px;
  font-weight: 700;
}

.boibox {
  margin: 10px;
  font-size: 15px;
  color: #666666;
}

.btnbox {
  margin: 16px 10px;
}

.sbtn {
  border-radius: 0.25rem;
  font-size: 15px;
  border: 1px solid #20252c;
  width: 100%;
  position: relative;
  text-decoration: none;
  padding: 8px;
  transition: 0.3s;
  background-color: #E0E6EB;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 30px;
  color: #333333;
}

.infobox {
  margin: 10px;
  font-size: 15px;
  color: #444444;
  display: flex;
  width: 100%;
  align-items: center;
}

.locationbox {
  margin: 10px;
  font-size: 15px;
  color: #444444;
  display: flex;
  width: 100%;
  align-items: center;
}

.kindicon {
  font-size: 13px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 6px;
  font-family: "Font Awesome 6 Free";
  font-weight: 600;
}

.hr {
  margin: 10px 4px;
  border: none;
  border-top: 1px solid #20252c;
  transform: scaleY(0.5);
}
</style>