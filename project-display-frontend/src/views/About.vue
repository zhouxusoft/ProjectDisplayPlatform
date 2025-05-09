<script setup>
import { onMounted, ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import LeftNavItem from '../components/LeftNavItem.vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { checkLoginAPI, userStarredAPI, userListAPI, circleListAPI, starredListAPI, uploadImageAPI, createCircleAPI } from '../api/api'
import CircleItem from '../components/CircleItem.vue'
import UserItem from '../components/UserItem.vue'
import dayjs from 'dayjs'

const router = useRouter()

const isLoading = ref(false)

const projects = ref([])

const projects2 = ref([
  {
    id: 3,
    usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
    name: "RainManGO/vue3-composition-admin",
    main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
    tags: ["JavaScript", "Flask", "Vue", "BootStrap"],
    language: { color: "449633", name: "Vue" },
    starnum: 2,
    updatetime: "2022/8/19",
    cover: 'https://p.cldisk.com/star3/origin/d1f2cf3372c1fc55585292c694de46a9.png',
  },
  {
    id: 4,
    usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
    name: "jeecgboot/jeecgboot-vue3",
    main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
    tags: ["JavaScript", "Vue", "BootStrap"],
    language: { color: "481828", name: "JavaScript" },
    starnum: 1,
    updatetime: "2022/8/19",
    cover: '123',
  }
])
const kinds = ref([
  {
    id: 1,
    name: "Projects",
    icon: "&#xf828",
    isactive: true
  },
  {
    id: 2,
    name: "Users",
    icon: "&#xf500",
    isactive: false
  },
  {
    icon: "&#xf015",
    id: 3,
    isactive: false,
    name: "Circle"
  },
  // {
  //   icon: "&#xf1da",
  //   id: 4,
  //   isactive: false,
  //   name: "History"
  // }
])

const userActiveName = ref('first')
const circleActiveName = ref('first')
const historyActiveName = ref('first')

const currentkind = ref(1)

const starred = ref([])

const isLogin = ref(0)

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
      router.push('/login')
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
    router.push('/login')
  })
}

/**
 * 格式化收藏数量
 */
const starnumFormat = () => {
  for (let i = 0; i < projects.value.length; i++) {
    if (projects.value[i].starnum >= 1000) {
      projects.value[i].starnum = Math.floor(projects.value[i].starnum / 100)
      projects.value[i].starnum = projects.value[i].starnum / 10
      projects.value[i].starnum = projects.value[i].starnum + "k"
    }
  }
}

/**
 * 点击选择左侧的展示类型
 * @param {JSON} kind 
 */
const chooseLeftNav = (kind) => {
  if (!kind.isactive) {
    for (let i = 0; i < kinds.value.length; i++) {
      kinds.value[i].isactive = false
    }
    kind.isactive = true
  }
  currentkind.value = kind.id
}

const circleList = ref([])
const circleCreateList = ref([])
const circleJoinList = ref([])
const circleStarList = ref([])

const getCircleList = () => {
  isLoading.value = true
  circleListAPI().then(res => {
    isLoading.value = false
    circleList.value = res.data
    circleCreateList.value = res.data.filter((item) => item.flag == 1)
    circleJoinList.value = res.data.filter((item) => item.flag == 2)
    circleStarList.value = res.data.filter((item) => item.flag == 3)
  }).catch(error => {
    console.error('Error:', error)
  })
}

const updateUser = (info) => {
  let userid = info.userid
  let flag = info.flag
  for (let i = 0; i < userList.value.length; i++) {
    if (userList.value[i].user_id == userid) {
      if (flag == 1) {
        userList.value[i].follower_num += 1
      } else if (flag == 0) {
        userList.value[i].follower_num -= 1
      }
      if (userList.value[i].flag == 1) {
        userList.value[i].flag = 3
      } else if (userList.value[i].flag == 2) {
        userList.value[i].flag = 0
      } else if (userList.value[i].flag == 3) {
        userList.value[i].flag = 1
      } else if (userList.value[i].flag == 0) {
        userList.value[i].flag = 2
      }
      break
    }
  }
  // getUserList()
}

const userList = ref([])
const userFollowList = ref([])
const userFanList = ref([])
const userLinkList = ref([])

const getUserList = () => {
  // 发送获取数据请求
  isLoading.value = true
  userListAPI().then(res => {
    isLoading.value = false
    userList.value = res.data
    userFollowList.value = res.data.filter((item) => item.flag == 2 || item.flag == 3)
    userFanList.value = res.data.filter((item) => item.flag == 1 || item.flag == 3)
    userLinkList.value = res.data.filter((item) => item.flag == 3)
  }).catch(error => {
    console.error('Error:', error)
  })
}

const getStarredList = () => {
  userStarredAPI().then(res => {
    if (res.success) {
      projects.value = res.data

      const today = dayjs()
      const yesterday = today.subtract(1, 'day')

      let todayList = []
      let yesterdayList = []
      let earlierList = []

      starred.value.forEach(item => {
        const dt = dayjs(item.starredtime, 'YYYY-MM-DD HH:mm:ss')

        if (dt.isSame(today, 'day')) {
          todayList.push(item)
        } else if (dt.isSame(yesterday, 'day')) {
          yesterdayList.push(item)
        } else if (dt.isBefore(yesterday, 'day')) {
          earlierList.push(item)
        }
        console.log(todayList, yesterdayList, earlierList)
      })

      todayStarList.value = projects.value.filter((item) => todayList.some((star) => star.projectid == item.id))
      yesterdayStarList.value = projects.value.filter((item) => yesterdayList.some((star) => star.projectid == item.id))
      earlierStarList.value = projects.value.filter((item) => earlierList.some((star) => star.projectid == item.id))
    }
  }).catch(error => {
    console.error('Error:', error)
  })
}

let firstin = true

const starProject = (id) => {
  getStarList()
}

const getStarList = () => {
  starredListAPI().then(res => {
    if (firstin) {
      getStarredList()
      firstin = false
    }
    starred.value = res.data
  })
}

const todayStarList = ref([])
const yesterdayStarList = ref([])
const earlierStarList = ref([])

const handleClick = () => {
  getCircleList()
  getUserList()
}

const circleDialogVisible = ref(false)

/**
 * 判断字符串是否包含空白符
 * @param {*} str 
 */
 function hasWhiteSpace(str) {
  return /\s/g.test(str)
}

/**
 * 判断用户名是否合法
 * @param {string} data 
 */
function checkUserName(data) {
  const length = new RegExp('(^.{1,12}$)')
  return length.test(data) && !hasWhiteSpace(data)
}

function checkBio(titleStr, options = {}) {
  const {
    forbiddenPattern = /[\x00-\x1F\x7F]/g // 控制字符
  } = options

  if (forbiddenPattern.test(titleStr)) {
    return { valid: false, message: '个性签名包含非法字符' }
  }
  if (/\s{2,}/.test(titleStr)) {
    return { valid: false, message: '个性签名不能包含连续空格' };
  }
  return { valid: true, message: '' }
}

const nicknameNew = ref('')
const bioNew = ref('')

const coverInput = ref(null)
const isUploadCover = ref(false)
const uploadCoverUrl = ref('')
const circleVisibleType = ref('2')

function uploadCover() {
  if (coverInput.value) {
    coverInput.value.value = null; // 重置，防止选同一张文件时不触发change事件
    coverInput.value.click();
  }
}

function handleUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // 文件类型校验
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件')
    return
  }

  // 文件大小校验，最大5MB
  const maxSizeMB = 5;
  if (file.size > maxSizeMB * 1024 * 1024) {
    ElMessage.error(`图片大小不能超过${maxSizeMB}MB`)
    return
  }
  
  uploadCoverAction(file)
}

const uploadCoverAction = (file) => {
  const formData = new FormData()
  formData.append('image', file)

  isUploadCover.value = true
  uploadImageAPI(formData)
    .then(res => {
      if (res.success) {
        uploadCoverUrl.value = res.filepath
      }
      isUploadCover.value = false
    })
    .catch(_ => {
      deleteCover()
      isUploadCover.value = false
      ElMessage.error('上传失败')
    })
}

const createCircle = () => {
  if (!nicknameNew.value) {
    ElMessage({
      message: '请输入圈子名称',
      type: 'error',
      plain: true,
      offset: 9,
    })
    return
  }
  if (!bioNew.value) {
    ElMessage({
      message: '请输入圈子简介',
      type: 'error',
      plain: true,
      offset: 9,
    })
    return
  }
  if (!uploadCoverUrl.value) {
    ElMessage({
      message: '请上传圈子头像',
      type: 'error',
      plain: true,
    })
    return
  }
  let toSend = {
    name: nicknameNew.value,
    description: bioNew.value,
    cover: uploadCoverUrl.value,
    type: circleVisibleType.value
  }
  createCircleAPI(toSend).then(res => {
    if (res.success) {
      ElMessage({
        message: '创建成功',
        type: 'success',
        plain: true,
        offset: 9,
      })
      nicknameNew.value = ''
      bioNew.value = ''
      uploadCoverUrl.value = ''
      circleDialogVisible.value = false
      getCircleList()
    } else {
      ElMessage({
        message: res.message,
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
  }).catch(_ => {
    ElMessage({
      message: '创建失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
  })
}

onMounted(() => {
  checkLogin()
  getStarList()
  getCircleList()
  getUserList()
})

</script>

<template>
  <div class="borderbox">
    <div class="leftnav d-none d-md-block">
      <div class="leftnavborder">
        <div class="filter">Filter by</div>
        <div class="kindgroupbox p-2">
          <LeftNavItem v-for="kind in kinds" :key="kind.id" :kind="kind" @click="chooseLeftNav(kind)" />
        </div>
      </div>
    </div>
    <div class="straightline"></div>
    <div class="mainprojects px-4 py-3" v-loading="isLoading">
      <div class="mainprojects" v-if="currentkind == 1">
        <div style="font-weight: 700; color: #333333; width: fit-content; margin: 0 auto; font-size: 18px;">我的 Starred
        </div>
        <div style="font-size: 15px; color: #333333; font-weight: 700;" v-if="todayStarList.length > 0">· 今天</div>
        <ProjectItem v-for="project in todayStarList" :key="project.id" :project="project" :starred="starred"
          @starProject="starProject" />
        <div style="font-size: 15px; color: #333333; font-weight: 700;" v-if="yesterdayStarList.length > 0">· 昨天</div>
        <ProjectItem v-for="project in yesterdayStarList" :key="project.id" :project="project" :starred="starred"
          @starProject="starProject" />
        <div style="font-size: 15px; color: #333333; font-weight: 700;" v-if="earlierStarList.length > 0">· 更早</div>
        <ProjectItem v-for="project in earlierStarList" :key="project.id" :project="project" :starred="starred"
          @starProject="starProject" />
      </div>
      <div class="mainprojects" v-if="currentkind == 2">
        <el-tabs v-model="userActiveName" class="demo-tabs" @tab-click="handleClick">
          <el-tab-pane label="我关注的" name="first"></el-tab-pane>
          <el-tab-pane label="关注我的" name="second"></el-tab-pane>
          <el-tab-pane label="互相关注" name="third"></el-tab-pane>
        </el-tabs>
        <div v-if="userActiveName == 'first'">
          <UserItem v-for="user in userFollowList" :key="user.id" :user="user" @updateUser="updateUser" />
          <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
        </div>
        <div v-if="userActiveName == 'second'">
          <UserItem v-for="user in userFanList" :key="user.id" :user="user" @updateUser="updateUser" />
          <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
        </div>
        <div v-if="userActiveName == 'third'">
          <UserItem v-for="user in userLinkList" :key="user.id" :user="user" @updateUser="updateUser" />
          <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
        </div>
      </div>
      <div class="mainprojects" v-if="currentkind == 3">
        <div class="addproject" @click="circleDialogVisible = true">创建圈子</div>
        <el-tabs v-model="circleActiveName" class="demo-tabs" @tab-click="handleClick">
          <el-tab-pane label="我管理的" name="first"></el-tab-pane>
          <el-tab-pane label="我加入的" name="second"></el-tab-pane>
          <el-tab-pane label="我关注的" name="third"></el-tab-pane>
        </el-tabs>
        <div v-if="circleActiveName == 'first'">
          <CircleItem v-for="circle in circleCreateList" :key="circle.id" :circle="circle" />
          <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
        </div>
        <div v-if="circleActiveName == 'second'">
          <CircleItem v-for="circle in circleJoinList" :key="circle.id" :circle="circle" />
          <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
        </div>
        <div v-if="circleActiveName == 'third'">
          <CircleItem v-for="circle in circleStarList" :key="circle.id" :circle="circle" />
          <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
        </div>
      </div>
      <div class="mainprojects" v-if="currentkind == 4">
        <el-tabs v-model="historyActiveName" class="demo-tabs" @tab-click="handleClick">
          <el-tab-pane label="看过的文章" name="first"></el-tab-pane>
          <el-tab-pane label="看过的创作者" name="second"></el-tab-pane>
          <el-tab-pane label="看过的圈子" name="third"></el-tab-pane>
        </el-tabs>
        <div style="font-size: 15px; color: #333333; font-weight: 700;">· 今天</div>
        <ProjectItem v-for="project in projects" :key="project.id" :project="project" :starred="starred" />
        <div style="font-size: 15px; color: #333333; font-weight: 700;">· 2024-12-11</div>
        <ProjectItem v-for="project in projects" :key="project.id" :project="project" :starred="starred" />
      </div>
    </div>
    <div class="rightnav d-none d-xl-block"></div>
    <el-dialog v-model="circleDialogVisible" title="创建圈子" width="500" align-center>
      <el-form label-width="100px">
        <el-form-item label="圈子名称" prop="roleName">
          <el-input placeholder="圈子名称" v-model="nicknameNew" maxlength="20" show-word-limit  />
        </el-form-item>
      </el-form>
      <el-form label-width="100px">
        <el-form-item label="圈子简介" prop="roleName">
          <el-input placeholder="圈子简介" v-model="bioNew" type="textarea" maxlength="42" show-word-limit />
        </el-form-item>
      </el-form>
      <el-form label-width="100px">
        <el-form-item label="可见范围" prop="roleName">
          <el-radio-group v-model="circleVisibleType" size="default">
            <el-radio-button label="所有人" value="2" />
            <el-radio-button label="仅成员" value="0" />
            <el-radio-button label="需订阅" value="1" />
          </el-radio-group>
          <div style="display: flex; align-items: end;">
            <span style="font-size: 12px; color: #F56C6C; margin-left: 12px; height: 18px;">可见范围后续无法修改</span>
          </div>
        </el-form-item>
      </el-form>
      <el-form label-width="100px" v-loading="isUploadCover">
        <el-form-item label="圈子头像" prop="roleName">
          <div style="width: 100px; height: 100px; background-color: #E7ECF0;" v-if="!uploadCoverUrl"></div>
          <el-image v-else style="width: 100px; height: 100px" :src="uploadCoverUrl" :zoom-rate="1.2" :max-scale="7"
            :min-scale="0.2" :preview-src-list="srcList" show-progress :initial-index="4" fit="cover"
            referrerpolicy="no-referrer" />
          <el-button style="position: absolute; bottom: 0px; left: 110px;" @click="uploadCover">上传头像</el-button>
          <input type="file" ref="coverInput" style="display: none" accept="image/*" @change="handleUpload" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="circleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createCircle">
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.addproject {
  width: 100px;
  height: 36px;
  position: fixed;
  bottom: 20px;
  right: 20px;
  border: 1px solid #FC5531;
  border-radius: 18px;
  background-color: #FC5531;
  color: white;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.borderbox {
  display: flex;
  justify-content: space-between;
}

.straightline {
  width: 1px;
  background-color: #666666;
}

.leftnav {
  position: sticky;
  height: 100vh;
  top: 0;
  width: 270px;
  overflow-y: auto;
}

.mainprojects {
  flex: 1;
  display: grid;
  gap: 16px;
  min-width: 0px;
  grid-template-columns: 1fr;
  height: fit-content;
}

.rightnav {
  width: 330px;
  padding: 16px 24px 0 0;
}

.filter {
  font-size: 16px;
  font-weight: 500;
  padding: 16px 16px 8px;
  color: #000000;
}

.fengeline {
  height: 1px;
  background-color: rgb(136, 146, 157);
  margin: 8px 16px;
}

.languagetitle {
  color: #0E1116;
  padding: 8px 20px;
  font-size: 14px;
}

.taggroupbox {
  padding: 8px;
  padding-left: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.resettagbox {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resettags {
  margin-right: 24px;
  font-size: 12px;
  background-color: rgb(231, 236, 240);
  padding: 2px 8px;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
  color: #0E1116;
  ;
}

.resettags:hover {
  background-color: #0349B4;
  color: rgb(255, 255, 255);
}

.rightinfobox {
  border: 1px solid #666666;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
}

.leftnavborder {
  padding-bottom: 60px;
}

.addmorelanguage {
  display: flex;
  white-space: nowrap;
  align-items: center;
  padding: 6px 8px;
  margin: 0 8px;
  border-radius: 6px;
  color: #0E1116;
  cursor: pointer;
  user-select: none;
  font-size: 14px;
}

.addmorelanguage:hover {
  background-color: rgb(231, 236, 240);
}

.addmoretag {
  display: flex;
  white-space: nowrap;
  align-items: center;
  padding: 3px 8px;
  border-radius: 6px;
  color: #0E1116;
  cursor: pointer;
  user-select: none;
  font-size: 13px;
  padding-right: 12px;
}

.addmoretag:hover {
  background-color: rgb(223, 247, 255);
}

.addmoreicon {
  font-family: "Font Awesome 6 Free";
  font-weight: 300;
  margin: 0 8px 0 4px;
}

.addlessicon {
  font-family: "Font Awesome 6 Free";
  font-weight: 600;
  margin: 0 8px 0 4px;
  padding-top: 1px;
  color: red;
}

.userbox {
  border: 1px solid black;
  border-radius: 4px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
}

.useravatar {
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid black;
  height: 80px;
  min-width: 80px;
  margin-right: 16px;
}

.userinfo {
  width: 100%;
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
  color: #555555;
}
</style>