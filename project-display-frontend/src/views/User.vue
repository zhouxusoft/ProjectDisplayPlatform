<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { checkLoginAPI, userInfoAPI, followUserAPI } from '../api/api'
import ProjectItem from '../components/ProjectItem.vue'
import { globalData } from './globalData'
import 'github-markdown-css/github-markdown.css'

const router = useRouter()

const haveInfo = ref(true)

const userInfo = ref({})
const selfInfo = ref({})
const projects = ref([])

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

const goBack = () => {
  router.push({
    path: globalData.previousPage,
    query: globalData.previousPageParams,
  })
}

const isLoading = ref(false)

const isLogin = ref(-1)

/**
 * 判断用户当前的登录状态
 */
const checkLogin = () => {
  isLoading.value = true
  // 发送请求
  checkLoginAPI().then(res => {
    if (res.success) {
      isLogin.value = 1
      selfInfo.value = res.userinfo
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
 * 获取用户信息
 */
const getUserInfo = () => {
  let toSend = {
    userid: router.currentRoute.value.params.id,
  }
  isLoading.value = true
  userInfoAPI(toSend).then(res => {
    if (res.success) {
      userInfo.value = res.data.userinfo
      projects.value = res.data.projects
      haveInfo.value = true
    } else {
      haveInfo.value = false
    }
    isLoading.value = false
  }).catch(error => {
    ElMessage({
      message: '请求失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
    haveInfo.value = false
    isLoading.value = false
  })
}

function userFollow(userid) {
  followUserAPI({ userid: userid })
    .then((response) => {
      getUserInfo()
      if (response.code == 200) {
        ElMessage({
          message: response.message,
          type: 'success',
          plain: true,
          offset: 9,
        })
      } else {
        ElMessage({
          message: '操作失败',
          type: 'error',
          plain: true,
          offset: 9,
        })
      }
    })
    .catch((error) => {
      getUserInfo()
      console.error(error)
      ElMessage({
        message: '网络错误，请稍后再试',
        type: 'error',
        plain: true,
        offset: 9,
      })
    })
}

onMounted(() => {
  checkLogin()
  getUserInfo()
})

</script>

<template>
  <div v-loading="isLoading">
    <div v-if="!haveInfo" class="notlogincontainer">
      <div class="notloginbox">
        <img src="/notlogin.png" alt="" class="notloginimg img-fluid">
        <div class="notlogincontent mb-4">页面找不到了</div>
        <div class="notloginbtngroup">
          <button @click="goBack()" class="btn btn-outline-secondary m-1 notloginbtn">返回</button>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="container">
        <div class="leftbox d-none d-md-block">
          <el-button @click="goBack()" style="color: #333; padding-left: 8px; font-size: 15px;" text><span
              class="kindicon" style="font-size: 14px">&#xf053</span>返 回</el-button>
          <div class="hr"></div>
          <div class="headpicturebox">
            <img class="img-fluid headpicture" :src="userInfo.usericon" alt="">
          </div>
          <div class="namebox">
            <div class="name">{{ userInfo.nickname }}
              <div class="nameisme" v-if="userInfo.relationship == -1" ><el-tag size="small">我</el-tag></div>
            </div>
          </div>
          <div class="boibox">
            <div>{{ userInfo.bio }}</div>
          </div>
          <div class="btnbox" v-if="userInfo.relationship != -1">
            <button type="button" class="sbtn" @click="userFollow(userInfo.user_id)"
              v-if="userInfo.relationship == 0 || userInfo.relationship == 2"><span class="kindicon"
                style="font-size: 14px">&#x2b</span>关注</button>
            <button type="button" class="sbtn" @click="userFollow(userInfo.user_id)" v-else><span class="kindicon"
                style="font-size: 14px">&#xf00c</span>已关注</button>
            <button type="button" class="sbtn" @click=""><span class="kindicon"
                style="font-size: 14px">&#xf0e0</span>私信</button>
          </div>
          <div class="infobox">
            <span class="kindicon">&#xf500</span>
            <span>{{ userInfo.follower }} followers · {{ userInfo.following }} following</span>
          </div>
          <div class="locationbox">
            <span class="kindicon" style="font-size: 14px">&#xf3c5</span>
            <span>{{ userInfo.position }}</span>
          </div>
          <div class="hr"></div>
        </div>
        <div class="rightbox">
          <div class="projectboxtitlebox">
            <div class="projectboxtitle">Projects of {{ userInfo.nickname }}</div>
          </div>
          <div v-if="projects.length > 0" class="projectbox mt-1 px-3 py-3">
            <ProjectItem v-for="project in projects" :key="project.id" :project="project" :starred="starred" />
            <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
          </div>
          <div v-if="projects.length == 0" class="projectbox mt-1 px-3 py-3">
            <div style="width: fit-content; margin: auto; color: #666666" class="p-3">空空如也...</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.name {
  position: relative;
  width: fit-content;
}

.nameisme {
  position: absolute;
  right: -34px;
  top: 0px;
}

.notlogincommentbox {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #666666;
  margin: 20px 0;
}

.commentinputicon {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
  border: 1px solid #aaaaaa;
}

.commenttitle {
  font-size: 20px;
  color: #333333;
  background-color: #f2f4f6;
  padding: 10px;
}

.commentinputbox {
  margin: 10px 0;
  display: flex;
}

.projectreadme {
  margin: 8px;
}

.projecttitle {
  font-size: 32px;
  font-weight: 700;
  color: #333333;
  margin: 10px;
  margin-bottom: 20px;
}

.projectinfobox {
  background-color: #f8f8f8;
  border-radius: 2px;
  padding: 10px;
}

.projectinfomain {
  border-radius: 2px;
  border-left: 8px solid #dddfe4;
  background: #eef0f4;
  margin: 16px 0;
  padding: 10px;
  color: #555555;
}

.projectinfo {
  margin-left: 16px;
  font-size: 14px;
  color: #555555;
  display: flex;
  align-items: center;
}

.projectlanguagebox {
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.projectlanguageicon {
  border-radius: 8px;
  border-style: solid;
  border-width: 1px;
  border-color: rgba(1, 4, 9, 0.1);
  width: 10px;
  height: 10px;
  margin: 4px 4px 4px 0;
}

.projecttagbox {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.projecttag {
  text-decoration: none;
  color: rgb(3, 73, 180);
  font-size: 12px;
  display: inline-block;
  padding: 0px 10px;
  font-weight: 500;
  border-radius: 4px;
  line-height: 22px;
  background-color: rgb(223, 247, 255);
  white-space: nowrap;
}

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
  height: 100vh;
}

.rightbox {
  flex: 1;
  min-width: 0px;
  padding: 0 16px 16px;
  margin-top: 16px;
  width: 1000px;
  overflow: hidden;
  border-left: 1px solid #cccccc;
}

.headpicturebox {
  width: 64px;
  height: 64px;
  border: 2px solid black;
  border-radius: 50%;
  overflow: hidden;
  margin-left: 10px;
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
  color: #555555
}

.boibox {
  margin: 10px;
  font-size: 15px;
  color: #666666;
}

.btnbox {
  margin: 16px 10px;
  display: flex;
  justify-content: space-between;
}

.sbtn {
  border-radius: 0.25rem;
  font-size: 15px;
  border: 1px solid #20252c;
  width: 120px;
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

.otherproject {
  margin: 16px;
  font-size: 15px;
  color: #666666;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>