<script setup>
import { onMounted, ref, onBeforeUnmount, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { checkLoginAPI, messageUserAPI, readMessageAPI, sendMessageAPI, uploadImageAPI } from '../api/api'
import { globalData } from './globalData'
import ChatItem from '../components/ChatItem.vue'
import dayjs from 'dayjs'

const router = useRouter()

const isLoading = ref(false)
const isLogin = ref(0)
const haveUser = ref(false)
const myInfo = ref({})
const chatmain = ref(null)
const boxcontent = ref(null)

let sendMessageFlag = 0

const userIconInfo = ref({
  user: '',
  my: '',
  myid: ''
})

/**
 * 判断用户当前的登录状态
 */
const checkLogin = () => {
  isLoading.value = true
  // 发送请求
  checkLoginAPI().then(res => {
    if (res.success) {
      isLogin.value = 1
      myInfo.value = res.userinfo
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

const goBack = () => {
  router.push({
    path: globalData.previousPage,
    query: globalData.previousPageParams,
  })
}

const nowChatUser = ref({})

const nowChatMessage = ref([])

const chatUserList = ref()

let allChatMessage = []

const getmessageUser = () => {
  messageUserAPI().then(res => {
    if (res.success) {
      allChatMessage = res.data
      chatUserList.value = res.chartUserList
      setUserLastMessage()
      if (haveUser.value) {
        getUserMessage()
      }
    } else {
      ElMessage({
        message: res.message,
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
  }).catch(error => {
    ElMessage({
      message: '请求失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
  })
}

const selectUser = (user) => {
  userIconInfo.value = {
    user: user.usericon,
    my: myInfo.value.usericon,
    myid: myInfo.value.userid
  }
  messageContent.value = ''
  nowChatUser.value = user
  haveUser.value = true
  readMessageAPI({ userid: user.user_id }).then(res => {
    if (res.success) {
      getmessageUser()
    }
  })
}

const getUserMessage = () => {
  nowChatMessage.value = allChatMessage.filter(item => item.receiver_id == nowChatUser.value.user_id || item.sender_id == nowChatUser.value.user_id)
  nowChatMessage.value = insertTimeMarkers(nowChatMessage.value)
  if (sendMessageFlag != 0) {
    if (sendMessageFlag == 1) {
      nextTick(() => {
        chatmain.value.scrollTo({
          top: chatmain.value.scrollHeight,
          behavior: 'smooth'
        })
      })
    } else {
      setTimeout(() => {
        chatmain.value.scrollTo({
          top: chatmain.value.scrollHeight,
          behavior: 'smooth'
        })
      }, 300)
    }
    sendMessageFlag = 0
  } else {
    nextTick(() => {
      chatmain.value.scrollTo({
        top: chatmain.value.scrollHeight,
      })
    })
  }
}

function insertTimeMarkers(messages) {
  if (!messages || messages.length === 0) return [];

  // 结果数组
  const result = [];

  // 先插入第一条固定时间标记
  result.push({
    type: 3,
    content: dayjs(messages[0].send_time).format("YYYY-MM-DD HH:mm")
  });

  for (let i = 0; i < messages.length; i++) {
    if (i === 0) {
      // 第一条消息，直接插入
      result.push(messages[i]);
    } else {
      // 计算和上一条消息的时间差（分钟）
      const prevTime = dayjs(messages[i - 1].send_time);
      const currTime = dayjs(messages[i].send_time);
      const diffMinutes = currTime.diff(prevTime, 'minute');

      // 如果时间间隔超过10分钟，插入时间标记
      if (diffMinutes > 10) {
        result.push({
          type: 3,
          content: currTime.format("YYYY-MM-DD HH:mm")
        });
      }

      // 插入当前消息
      result.push(messages[i]);
    }
  }

  return result;
}

const setUserLastMessage = () => {
  let reverseChatUserList = [...allChatMessage].reverse()
  chatUserList.value.forEach(user => {
    let lastmessage = reverseChatUserList.find(item => item.receiver_id == user.user_id || item.sender_id == user.user_id)
    let lastmessageTemp = { ...lastmessage }
    let now = dayjs()
    let dayFlag = dayjs(lastmessage.send_time).isSame(now, 'day')
    let yearFlag = dayjs(lastmessage.send_time).isSame(now, 'year')
    if (dayFlag) {
      lastmessageTemp.send_time = dayjs(lastmessageTemp.send_time).format('HH:mm')
    } else {
      if (yearFlag) {
        lastmessageTemp.send_time = dayjs(lastmessageTemp.send_time).format('MM-DD')
      } else {
        lastmessageTemp.send_time = dayjs(lastmessageTemp.send_time).format('YYYY-MM-DD')
      }
    }
    if (lastmessageTemp.type == 2) {
      lastmessageTemp.content = '[图片]'
    }
    user.lastmessage = lastmessageTemp
  })
}

const messageContent = ref('')

const sendMessage = (type = 1, content) => {
  if (content == '' || content == undefined || content == null) {
    return
  }
  let toSend = {
    userid: nowChatUser.value.user_id,
    content: content,
    type: type
  }
  sendMessageAPI(toSend).then(res => {
    if (res.success) {
      messageContent.value = ''
      sendMessageFlag = type
      getmessageUser()
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
      message: '发送失败',
      type: 'error',
      plain: true,
      offset: 9,
    })
  })
}

const coverInput = ref(null)
const coverPreview = ref(null)
const isUploadCover = ref(false)
const uploadCoverUrl = ref('')

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
        console.log(uploadCoverUrl.value);

        sendMessage(2, res.filepath)
      }
      isUploadCover.value = false
    })
    .catch(_ => {
      deleteCover()
      isUploadCover.value = false
      ElMessage.error('上传失败')
    })
}

// 监听内容高度变化，自动滚动到底部
let resizeObserver = null

function scrollToBottom() {
  if (chatmain.value) {
    chatmain.value.scrollTop = chatmain.value.scrollHeight
  }
}

onMounted(() => {
  checkLogin()
  getmessageUser()
  if (boxcontent.value) {
    resizeObserver = new ResizeObserver(async () => {
      // 内容高度变化时，等下一帧保证DOM更新完成，再滚动
      await nextTick()
      scrollToBottom()
    })
    resizeObserver.observe(boxcontent.value)
  }
})

onBeforeUnmount(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})
</script>

<template>
  <div class="borderbox">
    <div class="leftnav d-none d-md-block">
      <div class="leftnavborder" style="padding: 0 16px;">
        <el-button @click="goBack()" style="color: #333; padding-left: 8px; font-size: 15px; margin: 16px 0 0 0;"
          text><span class="kindicon" style="font-size: 14px">&#xf053</span>返 回</el-button>
        <div class="fengeline"></div>
        <div class="memberbox" v-for="user in chatUserList" :key="user.nickname"
          :class="{ active: user.user_id == nowChatUser.user_id }" @click="selectUser(user)">
          <div class="numtip" v-if="user.unreadnum > 0">{{ user.unreadnum }}</div>
          <div style="display: flex; justify-content: space-between;">
            <div class="memberavatar"><img :src="user.usericon" alt="" style="width: 42px;"
                referrerpolicy="no-referrer"></div>
            <div class="userinfo">
              <div style="font-weight: 700; font-size: 15px;">{{
                user.nickname }}
                <el-tag effect="plain" type="info" size="small" style="float: right; margin: 1px 0;"
                  v-if="user.relationship == 0">
                  陌生人
                </el-tag>
                <el-tag effect="plain" type="info" size="small" style="float: right; margin: 1px 0;"
                  v-if="user.relationship == 2">
                  我关注的
                </el-tag>
                <el-tag effect="plain" type="info" size="small" style="float: right; margin: 1px 0;"
                  v-if="user.relationship == 1">
                  关注我的
                </el-tag>
                <el-tag effect="plain" type="info" size="small" style="float: right; margin: 1px 0;"
                  v-if="user.relationship == 3">
                  互相关注
                </el-tag>
              </div>
              <div style="display: flex; align-items: center;">
                <div
                  style="color: #333333; margin-top: 4px; font-size: 12px; display: flex; align-items: center; white-space: nowrap;">
                  粉丝：{{ user.follower }}&nbsp;&nbsp;
                  关注：{{ user.following }}&nbsp;&nbsp;
                  作品：{{ user.projectnum }}
                </div>
              </div>
            </div>
          </div>
          <div style="color: #333333; margin-top: 6px; font-size: 13px; display: flex; justify-content: space-between;">
            <div class="lastmessage">{{ user.lastmessage.content }}</div>
            <div class="lastmessagetime">{{ user.lastmessage.send_time }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="straightline"></div>
    <div class="mainprojects">
      <div class="chatbox" v-if="haveUser">
        <div class="chatheader">
          {{ nowChatUser.nickname }}
        </div>
        <div class="chatmain" ref="chatmain">
          <div ref="boxcontent">
            <ChatItem v-for="message in nowChatMessage" :key="message.id" :message="message"
              :userIconInfo="userIconInfo"></ChatItem>
          </div>
        </div>
        <div class="chatfooter">
          <textarea placeholder="说点什么吧..." class="chatinput" v-model="messageContent"></textarea>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="kindicon1" style="font-size: 22px; margin-right: 2px;" @click="uploadCover">&#xf03e</span>
            <input type="file" ref="coverInput" style="display: none" accept="image/*" @change="handleUpload" />
            <div style="display: flex; align-items: center;">
              <span style="font-size: 13px; color: #999999; margin-right: 12px;">{{ messageContent.length }} /
                200</span>
              <el-button class="sendbtn" plain @click="sendMessage(1, messageContent)">发送</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sendbtn {
  width: 100px;
  float: right;
}

.chatinput {
  width: 100%;
  height: 76px;
  border: none;
  outline: none;
  resize: none;
}

.chatfooter {
  height: 132px;
  border: 1px solid #666666;
  border-radius: 2px;
  margin-bottom: 12px;
  padding: 8px;
}

.chatmain {
  flex: 1;
  border-right: 1px solid #666666;
  border-left: 1px solid #666666;
  overflow-y: auto;
}

.chatheader {
  margin-top: 12px;
  height: 42px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: 700;
  color: #666666;
  border: 1px solid #666666;
  border-radius: 2px;
}

.chatbox {
  height: calc(100vh - 58px);
  max-width: 640px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.lastmessagetime {
  color: #888888;
  text-align: right;
  margin-top: auto;
  margin-left: 10px;
  white-space: nowrap;
  /* 不换行 */
}

.lastmessage {
  color: #666666;
  white-space: nowrap;
  /* 不换行 */
  overflow: hidden;
  /* 超出部分隐藏 */
  text-overflow: ellipsis;
  /* 用省略号显示被截断的内容 */
}

.active {
  border-color: #0349b4 !important;
  background-color: #F5F7FA;
}

.numtip {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: #FC5531;
  color: #FFFFFF;
  min-width: 18px;
  height: 18px;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  padding: 4px;
}

.memberavatar {
  border-radius: 50%;
  overflow: hidden;
  height: 42px;
  min-width: 42px;
  margin-right: 8px;
  border: 1px solid #999999;
}

.memberbox {
  padding: 9px 8px 7px;
  border: 1px solid #aaaaaa;
  border-radius: 4px;
  width: 100%;
  position: relative;
  cursor: pointer;
  margin-bottom: 12px;
  transition: all .2s ease-in-out;
}

.memberbox:hover {
  box-shadow: 1px 2px 6px 0px rgba(0, 0, 0, 0.12);
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
  height: calc(100vh - 58px);
  top: 0;
  width: 300px;
  overflow-y: auto;
}

.mainprojects {
  flex: 1;
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
  margin: 16px 0px;
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

.addproject {
  width: 40px;
  height: 40px;
  position: fixed;
  bottom: 20px;
  right: 20px;
  border: 1px solid #FC5531;
  border-radius: 50%;
  background-color: #FC5531;
  color: white;
  font-size: 24px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2);
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
  height: 30px;
  min-width: 30px;
  margin-right: 8px;
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
}

.kindicon1 {
  padding-top: 10px;
  height: 22px;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 6px;
  font-family: "Font Awesome 6 Free";
  color: #666666;
  cursor: pointer;
}

.searchlogo {
  width: 30px;
  border: none;
  border-radius: 0.25rem 0 0 0.25rem;
}

.searchinput {
  border: none;
  border-radius: 0 0.25rem 0.25rem 0;
}

.searchinput:focus {
  box-shadow: none !important;
}

.focused {
  outline: 1px solid #0349b4;
}

.searchinputbox {
  border: 1px solid #727272;
  border-radius: 0.25rem;
}

.searchlogo::before {
  content: '\f002';
  font-family: 'Font Awesome 6 Free';
  font-weight: 600;
}

.searchbutton {
  border: none;
  border-radius: 0.25rem;
  background-color: white;
  width: 30px;
  height: 27px;
  margin: 2px;
}

.searchbutton:hover {
  background-color: #e7ecf0;
}

.searchbutton::before {
  content: '\f105';
  font-family: 'Font Awesome 6 Free';
  font-weight: 600;
}

.clear {
  font-family: 'Font Awesome 6 Free';
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  width: 16px;
  height: 16px;
  margin: 8px 0;
  border-radius: 0.25rem;
}

.clearbox {
  width: 14px;
  height: 14px;
}

.clear:hover {
  background-color: white;
  background-color: #e7ecf0;
}
</style>