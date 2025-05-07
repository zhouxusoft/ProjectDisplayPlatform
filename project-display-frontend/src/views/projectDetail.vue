<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { checkLoginAPI, projectDetailAPI, projectCommentsAPI, userCommentAPI } from '../api/api'
import { globalData } from './globalData'
import 'github-markdown-css/github-markdown.css'
import CommentSection from '../components/CommentSection.vue'

const router = useRouter()

const haveInfo = ref(true)

const projectInfo = ref({})
const userInfo = ref({})
const languageInfo = ref({})
const tagInfo = ref([])
const readme = ref('')
const selfInfo = ref({})

const comments = ref([])

const commentsCount = ref(0)

const userComment = ref('')

const goBack = () => {
  router.push({
    path: globalData.previousPage,
    query: globalData.previousPageParams,
  })
}

const putComment = async () => {
  if (userComment.value.length == 0) {
    return
  }
  let position = await getPosition()
  const toSend = {
    projectid: projectInfo.value.id,
    content: userComment.value,
    position: position,
  }
  userCommentAPI(toSend).then(res => {
    if (res.success) {
      ElMessage({
        message: res.message,
        type: 'success',
        plain: true,
        offset: 9,
      })
      userComment.value = ''
      getProjectComments(projectInfo.value.id)
    } else {
      ElMessage({
        message: res.message,
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
  }).catch(_ => {})
}

const getProjectComments = (projectid) => {
  const toSend = {
    projectid: projectid,
  }
  projectCommentsAPI(toSend).then(res => {
    if (res.success) {
      comments.value = res.data.reverse()
      commentsCount.value = res.data.length
    } else {
      ElMessage({
        message: res.message,
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
  }).catch(_ => { })
}

const getPosition = async () => {
  try {
    // 第一阶段请求：获取IP地址
    const ipResponse = await fetch('https://shop.godxu.top/get_ip', { method: 'GET' })
    if (!ipResponse.ok) throw new Error('IP请求失败')
    const ipData = await ipResponse.json()
    
    // 判断是否获取到有效IP
    if (!ipData?.ip) return '未知'

    // 第二阶段请求：获取地理位置
    const geoResponse = await fetch(`http://ip-api.com/json/${ipData.ip}?lang=zh-CN`)
    if (!geoResponse.ok) throw new Error('地理请求失败')
    const geoData = await geoResponse.json()

    // 返回最终结果
    return geoData.status === 'success' ? geoData.regionName.replace('省', '') : '未知'

  } catch (error) {
    return '未知'
  }
}

const getProjectDetail = () => {
  const toSend = {
    pagename: router.currentRoute.value.params.id,
  }
  projectDetailAPI(toSend).then(res => {
    if (res.success) {
      haveInfo.value = true
      projectInfo.value = res.data.project
      languageInfo.value = res.data.project.language
      tagInfo.value = res.data.project.tags
      userInfo.value = res.data.userinfo
      readme.value = res.data.readme
      getProjectComments(res.data.project.id)
    } else {
      haveInfo.value = false
      ElMessage({
        message: res.message,
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
  }).catch(_ => {
    haveInfo.value = false
    // ElMessage({
    //   message: '请求数据失败',
    //   type: 'error',
    //   plain: true,
    //   offset: 9,
    // })
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

onMounted(() => {
  checkLogin()
  getProjectDetail()
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
          <div class="headpicturebox" @click="router.push('/user/' + userInfo.user_id)">
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
            <button type="button" class="sbtn" @click=""
              v-if="userInfo.relationship == 0 || userInfo.relationship == 2"><span class="kindicon"
                style="font-size: 14px">&#x2b</span>关注</button>
            <button type="button" class="sbtn" @click="" v-else><span class="kindicon"
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
          <!-- <div style="font-size: 15px; color: #666666; margin-left: 10px;">其他作品</div>
          <div class="otherproject">暂无其它作品</div> -->
        </div>
        <div class="rightbox">
          <div class="projecttitle">{{ projectInfo.name }}</div>
          <div class="projectinfobox">
            <div class="projectinfo">
              {{ userInfo.nickname }} 编写于 {{ projectInfo.updatetime }}
              <span class="kindicon" style="font-size: 14px; margin-left: 32px; font-weight: 500;">&#xf06e</span>阅读量 {{
                projectInfo.browsenum }}
              <span class="kindicon" style="font-size: 14px; margin-left: 32px; font-weight: 500;">&#xf005</span>点赞 {{
                projectInfo.starnum }}
            </div>
            <div class="projectinfo" style="margin-top: 6px;">
              <div class="projectlanguagebox" v-if="languageInfo.name != 'None'">
                语言分类：
                <div class="projectlanguageicon" :style="{ backgroundColor: '#' + languageInfo.color }"></div>
                <div class="projectlanguage">{{ languageInfo.name }}</div>
              </div>
              <div style="display: flex; align-items: center; margin-left: 32px;">
                文章标签：
                <div class="projecttagbox">
                  <a v-for="tag in tagInfo" class="projecttag">{{ tag }}</a>
                </div>
              </div>
            </div>
          </div>
          <div class="projectinfomain">{{ projectInfo.main }}</div>
          <div>
            <div class="projectreadme markdown-body" v-html="readme"></div>
          </div>
          <div class="hr"></div>
          <div class="commenttitle">评论<span style="font-size: 14px; color: #999999; margin-left: 16px;">{{ commentsCount
              }}</span></div>
          <div class="commentinputbox" v-if="isLogin == 1">
            <div class="commentinputicon"><img style="width: 50px;" :src="selfInfo.usericon" alt="" referrerpolicy="no-referrer"></div>
            <el-input v-model="userComment" maxlength="100" style="width: 100%; font-size: 16px;" placeholder="说点什么吧"
              show-word-limit type="textarea" :autosize="{ minRows: 3, maxRows: 10 }" />
            <el-button style="margin-left: 10px; margin-top: auto;" @click="putComment()" plain>提交</el-button>
          </div>
          <div class="notlogincommentbox" v-else>
            评论需要先<el-button @click="router.push('/login')" text type="primary"
              style="padding: 5px; font-size: 16px;">登录</el-button>
          </div>
          <CommentSection v-for="comment in comments" :comment="comment"></CommentSection>
          <div
            style="height: 80px; display: flex; align-items: center; justify-content: center; color: #999999; font-size: 14px;">
            到底了...</div>
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
  cursor: pointer;
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