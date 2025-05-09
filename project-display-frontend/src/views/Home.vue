<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { checkLoginAPI, clearCookieAPI, myInfoAPI, uploadImageAPI, updateProfileAPI, unreadMessageNumAPI, systemMessageAPI, readSystemMessageAPI } from '../api/api'
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

const userInfo = ref({})

const isLogin = ref(-1)
const currentSortMode = ref({
  id: 2,
  name: 'Last updated'
})

const messageList = ref([
  {
    id: 1,
    content: '<div>你的文章 <span style="color: #0349B4; text-decoration: underline">RainManGO/vue3-composition-admin</span> 被3个人点赞</div>',
  },
  {
    id: 2,
    content: '<div>你的文章 <span style="color: #0349B4; text-decoration: underline">RainManGO/vue3-composition-admin</span> 被2个人评论</div>',
  },
  {
    id: 3,
    content: '<div><span style="color: #0349B4; text-decoration: underline">OuYangPeng</span> 关注了你</div>',
  },
])

const messageBoxHeight = ref([0])

const setMessageBoxHeight = () => {
  if (systemMessageNum.value == 0) {
    messageBoxHeight.value = 66
  } else if (systemMessageNum.value > 5) {
    messageBoxHeight.value = 5 * 66
  } else {
    messageBoxHeight.value = systemMessageNum.value * 66
  }
}

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
 * 获取用户信息
 */
const getMyInfo = () => {
  isLoading.value = true
  // 发送请求
  myInfoAPI().then(res => {
    if (res.success) {
      // 设置用户信息
      projects.value = res.data.projects
      userInfo.value = res.data.userinfo
      coverPreview.value = res.data.userinfo.usericon
    } else {
      ElMessage({
        message: '获取用户信息失败',
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
    isLoading.value = false
  }).catch(error => {
    ElMessage({
      message: '请求失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
    isLoading.value = false
  })
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
      getMyInfo()
      getUnreadMessageNum()
      getSystemMessage()
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
  ElMessageBox.confirm(
    '确认退出?',
    '提示',
    {
      confirmButtonText: '退出',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
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
    })
    .catch(() => { })
}

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
const coverPreview = ref(null)
const isUploadCover = ref(false)
const uploadCoverUrl = ref('')

const updateUserinfo = () => {
  if (!nicknameNew.value && !bioNew.value && uploadCoverUrl.value == userInfo.value.usericon) {
    centerDialogVisible.value = false
    return
  }
  let toSend = {}
  if (nicknameNew.value) {
    if (checkUserName(nicknameNew.value)) {
      toSend.nickname = nicknameNew.value
    } else {
      ElMessage({
        message: '昵称不合法',
        type: 'error',
        plain: true,
        offset: 9,
      })
      return
    }
  } else {
    toSend.nickname = userInfo.value.nickname
  }
  if (bioNew.value) {
    if (checkBio(bioNew.value).valid) {
      toSend.bio = bioNew.value
    } else {
      let msg = checkBio(bioNew.value).message
      ElMessage({
        message: msg,
        type: 'error',
        plain: true,
        offset: 9,
      })
      return
    }
  } else {
    toSend.bio = userInfo.value.bio
  }
  if (uploadCoverUrl.value) {
    toSend.usericon = uploadCoverUrl.value
  } else {
    toSend.usericon = userInfo.value.usericon
  }
  updateProfileAPI(toSend).then(res => {
    if (res.success) {
      ElMessage({
        message: '更新成功',
        type: 'success',
        plain: true,
        offset: 9,
      })
      centerDialogVisible.value = false
      getMyInfo()
    } else {
      ElMessage({
        message: '更新失败',
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
    nicknameNew.value = ''
    bioNew.value = ''
  }).catch(_ => {
    ElMessage({
      message: '更新失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
    nicknameNew.value = ''
    bioNew.value = ''
  })
}

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

  // 生成本地预览URL
  coverPreview.value = URL.createObjectURL(file)
  
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

const unreadMessageNum = ref(0)

const getUnreadMessageNum = () => {
  unreadMessageNum.value = 0
  unreadMessageNumAPI().then(res => {
    if (res.success) {
      unreadMessageNum.value = res.data
    } else {
      unreadMessageNum.value = 0
    }
  }).catch(_ => {
    unreadMessageNum.value = 0
  })
}

const systemMessageNum = ref(0)
const starMessageList = ref([])
const commentMessageList = ref([])
const followMessageList = ref('')
const inviteMessageList = ref([])
const removeMessageList = ref([])

const getSystemMessage = () => {
  systemMessageAPI().then(res => {
    if (res.success) {
      starMessageList.value = res.data.star
      commentMessageList.value = res.data.comment
      followMessageList.value = res.data.follow
      inviteMessageList.value = res.data.invite
      removeMessageList.value = res.data.remove
      systemMessageNum.value += starMessageList.value.length
      systemMessageNum.value += commentMessageList.value.length
      systemMessageNum.value += inviteMessageList.value.length
      systemMessageNum.value += removeMessageList.value.length
      if (followMessageList.value != '') {
        systemMessageNum.value += 1
      }
      setMessageBoxHeight()
      console.log(systemMessageNum.value)
    }
  })
}

const readMessage = (message, type) => {
  let toSend = {}
  if (type == 1) {
    toSend = {
      type: 1,
      content: message.id,
    }
  } else if (type == 2) {
    toSend = {
      type: 2,
      content: message.id,
    }
  } else if (type == 3) {
    toSend = {
      type: 3,
    }
  } else if (type == 4) {
    toSend = {
      type: 4,
      content: message.id,
    }
  } else if (type == 5) {
    toSend = {
      type: 5,
      content: message.id,
    }
  }
  readSystemMessageAPI(toSend).then(res => {
    if (res.success) {
      getSystemMessage()
    }
  })
}

onMounted(() => {
  checkLogin()
  setMessageBoxHeight()
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
            <img class="img-fluid headpicture" :src="userInfo.usericon" alt="" referrerpolicy="no-referrer">
          </div>
          <div class="namebox">
            <div class="name">{{ userInfo.nickname }}</div>
          </div>
          <div class="boibox">
            <div>{{ userInfo.bio || '这个人很神秘，什么都没有写' }}</div>
          </div>
          <div class="btnbox">
            <button type="button" class="sbtn" @click="centerDialogVisible = true">Edit Profile</button>
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
          <el-button @click="logout()" class="logoutbtn" text style="padding: 4px 8px;"><span class="kindicon"
              style="font-size: 13px; margin-right: 2px;">&#xf011</span>退出登录</el-button>
        </div>
        <div class="rightbox">
          <div class="projectboxborder">
            <div class="projectboxtitlebox">
              <div class="projectboxtitle">Messages of Mine</div>
              <el-badge :value="unreadMessageNum" :max="99" class="item" v-if="unreadMessageNum > 0">
                <el-button @click="this.$router.push('/chat')"><span class="kindicon"
                    style="font-size: 14px">&#xf0e0</span>My Messages</el-button>
              </el-badge>
              <el-button @click="this.$router.push('/chat')" v-else><span class="kindicon"
                style="font-size: 14px">&#xf0e0</span>My Messages</el-button>
            </div>
            <div class="messagebox" :style="{ height: messageBoxHeight + 'px' }">
              <div class="messageitem" v-for="message in starMessageList">
                <div>你的文章 <span style="color: #0349B4; text-decoration: underline">{{ message.project_name }}</span> 被 {{ message.num }} 个人点赞</div>
                <button type="button" class="dbtn" @click="readMessage(message, 1)"><span class="kindicon"
                  style="font-size: 12px; margin-right: 2px;">&#xf00c</span>已阅</button>
              </div>
              <div class="messageitem" v-for="message in commentMessageList">
                <div>你的文章 <span style="color: #0349B4; text-decoration: underline">{{ message.project_name }}</span> 被 {{ message.num }} 个人评论</div>
                <button type="button" class="dbtn" @click="readMessage(message, 2)"><span class="kindicon"
                  style="font-size: 12px; margin-right: 2px;">&#xf00c</span>已阅</button>
              </div>
              <div class="messageitem" v-for="message in followMessageList">
                <div>{{ message }} 个人关注了你</div>
                <button type="button" class="dbtn" @click="readMessage(message, 3)"><span class="kindicon"
                  style="font-size: 12px; margin-right: 2px;">&#xf00c</span>已阅</button>
              </div>
              <div class="messageitem" v-for="message in inviteMessageList">
                <div><span style="color: #0349B4; text-decoration: underline">{{ message.nickname }}</span> 邀请你加入圈子 <span style="color: #0349B4; text-decoration: underline">{{ message.circle_name }}</span></div>
                <div style="display: flex;">
                  <button type="button" class="dbtn" @click="readMessage(message, 4)" style="margin-right: 8px;"><span class="kindicon"
                  style="font-size: 12px; margin-right: 2px;">&#xf00c</span>同意</button>
                  <button type="button" class="dbtn" @click="readMessage(message, 5)"><span class="kindicon"
                    style="font-size: 12px; margin-right: 2px;">&#xf00d</span>拒绝</button>
                </div>
              </div>
              <div class="messageitem" v-for="message in removeMessageList">
                <div>你被移出圈子 <span style="color: #0349B4; text-decoration: underline">{{ message.circle_name }}</span></div>
                <button type="button" class="dbtn" @click="readMessage(message, 6)"><span class="kindicon"
                  style="font-size: 12px; margin-right: 2px;">&#xf00c</span>已阅</button>
              </div>
              <!-- <div class="messageitem" v-for="message in messageList">
                <div v-html="message.content"></div>
                <button type="button" class="dbtn" @click="readMessage(message.id)"><span class="kindicon"
                  style="font-size: 12px; margin-right: 2px;">&#xf00c</span>已阅</button>
              </div> -->
              <div v-if="messageList.length == 0" class="messageitem" style="display: flex; justify-content: center;">暂无通知</div>
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
            <div v-if="projects.length > 0" class="projectbox mt-1 px-3 py-3">
              <ProjectItem v-for="project in projects" :key="project.id" :project="project" :starred="starred" />
              <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
            </div>
            <div v-if="projects.length == 0" class="projectbox mt-1 px-3 py-3">
              <div style="width: fit-content; margin: auto; color: #666666">空空如也...</div>
            </div>
            <div style="height: 40px;"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <el-dialog v-model="centerDialogVisible" title="编辑个人资料" width="500" align-center>
    <el-form label-width="100px">
      <el-form-item label="昵称" prop="roleName">
        <el-input :placeholder="userInfo.nickname" v-model="nicknameNew" />
      </el-form-item>
    </el-form>
    <el-form label-width="100px">
      <el-form-item label="个性签名" prop="roleName">
        <el-input :placeholder="userInfo.bio" v-model="bioNew" />
      </el-form-item>
    </el-form>
    <el-form label-width="100px" v-loading="isUploadCover">
      <el-form-item label="头像" prop="roleName">
        <el-image style="width: 100px; height: 100px" :src="coverPreview" :zoom-rate="1.2" :max-scale="7"
          :min-scale="0.2" :preview-src-list="srcList" show-progress :initial-index="4" fit="cover"
          referrerpolicy="no-referrer" />
        <el-button style="position: absolute; bottom: 0px; left: 110px;" @click="uploadCover">上传头像</el-button>
        <input type="file" ref="coverInput" style="display: none" accept="image/*" @change="handleUpload" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateUserinfo">保存</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.messagebox {
  padding-top: 2px;
  padding-right: 4px;
  transition: all 0.4s ease;
  overflow-y: auto;
}

.messageitem {
  width: 100%;
  border: 1px solid black;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
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
  min-height: 360px;
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
  font-size: 24px;
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

.dbtn {
  border-radius: 0.25rem;
  font-size: 13px;
  border: 1px solid #20252c;
  width: 60px;
  position: relative;
  text-decoration: none;
  padding: 4px;
  transition: 0.3s;
  background-color: #E7ECF0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 24px;
  color: #333333;
}

.dbtn:hover {
  background-color: rgb(206, 213, 220);
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

.sbtn:hover {
  background-color: rgb(206, 213, 220);
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