<script setup>
import { onMounted, ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { circleDetailAPI, uploadImageAPI, updateCircleAPI, inviteUserListAPI, orderCircleAPI } from '../api/api'
import { useRouter } from 'vue-router'
import { globalData } from './globalData'

const router = useRouter()

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

/**
 * 格式化收藏数量
 */
const starnumFormat = () => {
  for (let i = 0; i < circleProjects.value.length; i++) {
    if (circleProjects.value[i].starnum >= 1000) {
      circleProjects.value[i].starnum = Math.floor(circleProjects.value[i].starnum / 100)
      circleProjects.value[i].starnum = circleProjects.value[i].starnum / 10
      circleProjects.value[i].starnum = circleProjects.value[i].starnum + "k"
    }
  }
}

const circleProjects = ref([])

const circleInfo = ref({})

const circleUsers = ref([])

const circleCreater = ref([])


const getCircleDetail = () => {
  let toSend = {
    circleid: router.currentRoute.value.params.id,
  }
  circleDetailAPI(toSend).then(res => {
    if (res.code == 200) {
      circleInfo.value = res.data.circle
      circleProjects.value = res.data.projects
      circleCreater.value = [res.data.users[0]]
      circleUsers.value = res.data.users.slice(1)
      uploadCoverUrl.value = circleInfo.value.cover
      noticeNew.value = circleInfo.value.notice
      circleInfotype.value = circleInfo.value.type + ''
      starnumFormat()
      checkVisible()
    }
  }).catch(error => {
    console.error('Error:', error)
  })
}

const goBack = () => {
  router.push({
    path: globalData.previousPage,
    query: globalData.previousPageParams,
  })
}

const toUserDetail = (userid) => {
  router.push({ path: `/user/${userid}` })
}

const disbandCircle = () => {
  ElMessageBox.confirm(
    '确认解散圈子?',
    '警告',
    {
      confirmButtonText: '确认',
      confirmButtonClass: 'error',
      cancelButtonText: '取消',
      type: 'error',
    }
  )
    .then(() => {

    })
    .catch(() => { })
}

const coverInput = ref(null)
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

const outerVisible = ref(false)
const inviteVisible = ref(false)
const removeVisible = ref(false)
const noticeNew = ref('')
const descriptionNew = ref('')
const circleInfotype = ref('')

const updateCircle = () => {
  let descriptionNewTemp = descriptionNew.value
  if (!descriptionNew.value) {
    descriptionNewTemp = circleInfo.value.description
  }
  let uploadCoverUrlTemp = uploadCoverUrl.value
  if (!uploadCoverUrl.value) {
    uploadCoverUrlTemp = circleInfo.value.cover
  }
  let toSend = {
    circleid: circleInfo.value.id,
    notice: noticeNew.value,
    description: descriptionNewTemp,
    cover: uploadCoverUrlTemp
  }
  updateCircleAPI(toSend).then(res => {
    if (res.code == 200) {
      ElMessage.success(res.message)
      outerVisible.value = false
      descriptionNew.value = ''
      getCircleDetail()
    } else {
      ElMessage.error(res.message)
    }
  }).catch(error => {
    console.error('Error:', error)
    ElMessage.error('出错了')
  })
}

const projectVisible = ref(0)

const checkVisible = () => {
  if (circleInfo.value.flag == 1 || circleInfo.value.flag == 2) {
    projectVisible.value = 1
  } else if (circleInfo.value.flag == 3) {
      if (circleInfo.value.type == 0) {
        projectVisible.value = 3
      } else if (circleInfo.value.type == 1) {
        projectVisible.value = 3
      } else if (circleInfo.value.type == 2) {
        projectVisible.value = 1
      }
  } else if (circleInfo.value.flag == 4) {
    if (circleInfo.value.type == 0) {
      projectVisible.value = 3
    } else if (circleInfo.value.type == 1) {
      projectVisible.value = 2
    } else if (circleInfo.value.type == 2) {
      projectVisible.value = 1
    }
  }
}

const inviteUserClick = () => {
  inviteVisible.value = true
  getInviteUserList()
}

const inviteUserList = ref([])
const selectInviteUserList = ref([])
const selectRemoveUserList = ref([])

const getInviteUserList = () => {
  let toSend = {
    circleid: circleInfo.value.id
  }
  inviteUserListAPI(toSend).then(res => {
    if (res.success) {
      inviteUserList.value = res.data
    }
  })
}

const clickInviteUser = (user) => {
  const index = selectInviteUserList.value.indexOf(user.user_id);
  if (index !== -1) {
    selectInviteUserList.value.splice(index, 1)
  } else {
    selectInviteUserList.value.push(user.user_id)
  }
  console.log(selectInviteUserList.value)
}

const clickRemoveUser = (user) => {
  const index = selectRemoveUserList.value.indexOf(user.user_id);
  if (index !== -1) {
    selectRemoveUserList.value.splice(index, 1)
  } else {
    selectRemoveUserList.value.push(user.user_id)
  }
  console.log(selectRemoveUserList.value)
}

const yesInviteUser = () => {
  if (selectInviteUserList.value.length == 0) {
    ElMessage.warning('请选择要邀请的用户')
  } else {
    ElMessage.success('邀请已发送')
    inviteVisible.value = false
    selectInviteUserList.value = []
  }
}

const yesRemoveUser = () => {
  if (selectRemoveUserList.value.length == 0) {
    ElMessage.warning('请选择要移除的用户')
  } else {
    ElMessageBox.confirm(
    '确认移除这些用户?',
    '提示',
    {
      confirmButtonText: '移除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      ElMessage({
        type: 'success',
        message: '移除成功',
      })
    })
    .catch(() => {})
  }
}

const joinCircle = () => {
  ElMessage.success('申请已发送')
}

const orderCircle = () => {
  let toSend = {
    circleid: circleInfo.value.id
  }
  orderCircleAPI(toSend).then(res => {
    if (res.success) {
      ElMessage.success(res.message)
      getCircleDetail()
    } else {
      ElMessage.error(res.message)
    }
  }).catch(error => {
    console.error('Error:', error)
    ElMessage.error('出错了')
  })
}

onMounted(() => {
  getCircleDetail()
})
</script>

<template>
  <div class="borderbox">
    <div class="leftnav d-none d-md-block">
      <div class="leftnavborder">
        <el-button @click="goBack()" style="color: #333; padding-left: 8px; font-size: 15px; margin: 16px;" text><span
            class="kindicon" style="font-size: 14px">&#xf053</span>返 回</el-button>
        <div class="fengeline"></div>
        <div class="memberborder">
          <div class="filter">创建者</div>
          <div class="taggroupbox">
            <div class="memberbox" v-for="user in circleCreater" :key="user.user_id">
              <div style="display: flex; justify-content: space-between;">
                <div class="memberavatar"><img :src="user.usericon" alt="" style="width: 40px;"
                    referrerpolicy="no-referrer"></div>
                <div class="userinfo">
                  <div style="font-weight: 700; font-size: 15px; cursor: pointer;" @click="toUserDetail(user.user_id)">
                    {{ user.nickname }}
                    <el-tag effect="plain" type="info" size="small" style="float: right;" v-if="user.flag == 4">
                      我
                    </el-tag>
                  </div>
                  <div style="display: flex; align-items: center;">
                    <div
                      style="color: #333333; margin-top: 2px; font-size: 12px; display: flex; align-items: center; white-space: nowrap;">
                      粉丝：{{ user.follower_num }}&nbsp;&nbsp;
                      关注：{{ user.following_num }}&nbsp;&nbsp;
                      作品：{{ user.projects_num }}
                    </div>
                  </div>
                </div>
              </div>
              <div style="color: #333333; margin-top: 4px; font-size: 13px;">{{ user.bio || '这个人很神秘，什么都没有写' }}</div>
            </div>
          </div>
          <div class="filter" style="padding-top: 0;">成员 <span style="font-size: 14px; color: #666666;">{{
            circleInfo.member_count }}</span></div>
          <div class="taggroupbox" v-if="circleUsers.length > 0">
            <div class="memberbox" v-for="user in circleUsers" :key="user.nickname">
              <div style="display: flex; justify-content: space-between;">
                <div class="memberavatar"><img :src="user.usericon" alt="" style="width: 40px;"
                    referrerpolicy="no-referrer"></div>
                <div class="userinfo">
                  <div style="font-weight: 700; font-size: 15px; cursor: pointer;" @click="toUserDetail(user.user_id)">
                    {{ user.nickname }}
                    <el-tag effect="plain" type="info" size="small" style="float: right;" v-if="user.flag == 4">
                      我
                    </el-tag>
                  </div>
                  <div style="display: flex; align-items: center;">
                    <div
                      style="color: #333333; margin-top: 2px; font-size: 12px; display: flex; align-items: center; white-space: nowrap;">
                      粉丝：{{ user.follower_num }}&nbsp;&nbsp;
                      关注：{{ user.following_num }}&nbsp;&nbsp;
                      作品：{{ user.projects_num }}
                    </div>
                  </div>
                </div>
              </div>
              <div style="color: #333333; margin-top: 4px; font-size: 13px;">{{ user.bio || '这个人很神秘，什么都没有写' }}</div>
            </div>
          </div>
          <div class="taggroupbox" v-else>
            <div class="memberbox" style="text-align: center; font-size: 14px; color: #666666; border: none;">暂无成员</div>
          </div>
        </div>
      </div>
    </div>
    <div class="straightline"></div>
    <div class="mainprojects px-4 py-3">
      <div v-if="projectVisible == 1">
        <ProjectItem v-for="project in circleProjects" :key="project.id" :project="project" :starred="starred" />
        <div style="width: fit-content; margin: 10px auto; color: #666666" v-if="circleProjects.length > 0">没有更多了...</div>
        <div style="width: fit-content; margin: 10px auto; color: #666666; margin-top: 40vh" v-else>空空如也</div>
      </div>
      <div v-if="projectVisible == 2">
        <div style="width: fit-content; margin: 10px auto; color: #666666; margin-top: 40vh">圈子内容仅成员可见</div>
      </div>
      <div v-if="projectVisible == 3">
        <div style="width: fit-content; margin: 10px auto; color: #666666; margin-top: 40vh">圈子内容订阅后可见</div>
      </div>
    </div>
    <div class="rightnav d-none d-xl-block">
      <div class="circlebox">
        <div style="display: flex; justify-content: space-between;">
          <div class="circleavatar" style="border-radius: 0.25em;"><img :src="circleInfo.cover" alt=""
              style="width: 70px;" referrerpolicy="no-referrer"></div>
          <div class="userinfo">
            <div style="font-weight: 700; font-size: 18px;">{{ circleInfo.name }}</div>
            <div style="color: #333333; margin-top: 4px;">{{ circleInfo.description }}</div>
          </div>
        </div>
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 8px;">
          <div
            style="color: #333333; margin-top: 4px; font-size: 13px; display: flex; align-items: center; white-space: nowrap;">
            <span class="kindicon" style="font-size: 13px;">&#xf0c0</span>成员：{{ circleInfo.member_count + 1
            }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 13px">&#xf06e</span>粉丝：{{
              circleInfo.follower_count }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon"
              style="font-size: 13px">&#xf1ea</span>作品：{{ circleInfo.project_count }}
          </div>
        </div>
        <div class="btnbox">
          <el-button size="small" plain v-if="circleInfo.flag == 4" @click="joinCircle">申请加入</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 2"><span class="kindicon"
              style="font-size: 14px">&#xf00c</span>已加入</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 4" @click="orderCircle">订阅圈子</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 3" @click="orderCircle"><span class="kindicon"
              style="font-size: 14px">&#xf0e0</span>已订阅</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 1" @click="outerVisible = true"><span class="kindicon"
              style="font-size: 14px">&#xf0c9</span>管理圈子</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 1" @click="disbandCircle"><span class="kindicon"
              style="font-size: 14px">&#xf00d</span>解散圈子</el-button>
        </div>
      </div>

      <div class="rightnotitlebox" v-if="circleInfo.flag == 1 || circleInfo.flag == 2">
        <div style="display: flex; align-items: center; justify-content: center; height: 86px;"
          v-if="!circleInfo.notice">
          暂无公告
        </div>
        <div v-else>
          {{ circleInfo.notice }}
        </div>
      </div>
      <div class="rightnotitlebox">
        广告位招租
      </div>
      <div class="rightinfobox">
        🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持
        RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城等功能。你的 ⭐️ Star ⭐️，是作者生发的动力！
      </div>
    </div>
    <el-dialog v-model="outerVisible" title="管理圈子" width="500" align-center>
      <el-form label-width="80px">
        <el-form-item label="圈子公告" prop="roleName">
          <el-input :placeholder="circleInfo.notice ? circleInfo.notice : '暂无公告'" v-model="noticeNew" type="textarea"
            maxlength="100" show-word-limit :rows="3" />
        </el-form-item>
      </el-form>
      <el-form label-width="80px">
        <el-form-item label="圈子简介" prop="roleName">
          <el-input :placeholder="circleInfo.description" v-model="descriptionNew" type="textarea" maxlength="42"
            show-word-limit />
        </el-form-item>
      </el-form>
      <el-form label-width="80px">
        <el-form-item label="可见范围" prop="roleName">
          <!-- <el-tag size="large" effect="dark" v-if="circleInfo.type == 2" >所有人</el-tag>
          <el-tag size="default" effect="dark" v-if="circleInfo.type == 0" style="font-size: 14px;">仅成员</el-tag>
          <el-tag size="large" effect="dark" v-if="circleInfo.type == 1">需订阅</el-tag> -->
          <el-radio-group v-model="circleInfotype" size="default">
            <el-radio-button label="所有人" value="2" :disabled="circleInfo.type != 2" />
            <el-radio-button label="仅成员" value="0" :disabled="circleInfo.type != 0" />
            <el-radio-button label="需订阅" value="1" :disabled="circleInfo.type != 1" />
          </el-radio-group>
        </el-form-item>
      </el-form>
      <el-form label-width="80px" v-loading="isUploadCover">
        <el-form-item label="圈子头像" prop="roleName">
          <div style="width: 100px; height: 100px; background-color: #E7ECF0;" v-if="!uploadCoverUrl"></div>
          <el-image v-else style="width: 100px; height: 100px" :src="uploadCoverUrl" :zoom-rate="1.2" :max-scale="7"
            :min-scale="0.2" show-progress :initial-index="4" fit="cover"
            referrerpolicy="no-referrer" />
          <el-button style="position: absolute; bottom: 0px; left: 110px;" @click="uploadCover">上传头像</el-button>
          <input type="file" ref="coverInput" style="display: none" accept="image/*" @change="handleUpload" />
        </el-form-item>
      </el-form>
      <el-dialog v-model="inviteVisible" width="500" title="邀请成员" append-to-body align-center style="min-height: 450px;">
        <span>仅可邀请我关注的用户</span>
        <div class="invitetaggroupbox" v-if="inviteUserList.length > 0">
          <div class="invitememberbox" v-for="user in inviteUserList" :key="user.nickname" @click="clickInviteUser(user)" :class="{ selectactive: selectInviteUserList.includes(user.user_id) }">
            <div style="display: flex; justify-content: space-between;">
              <div class="memberavatar"><img :src="user.usericon" alt="" style="width: 40px;"
                  referrerpolicy="no-referrer"></div>
              <div class="userinfo">
                <div style="font-weight: 700; font-size: 15px; cursor: pointer;">
                  {{ user.nickname }}
                </div>
                <div style="display: flex; align-items: center;">
                  <div
                    style="color: #333333; margin-top: 2px; font-size: 12px; display: flex; align-items: center; white-space: nowrap;">
                    粉丝：{{ user.follower }}&nbsp;&nbsp;
                    关注：{{ user.following }}&nbsp;&nbsp;
                    作品：{{ user.projectnum }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="invitetaggroupbox" v-else>
          <div style="width: 100%; text-align: center; color: #999999; padding-top: 110px;">暂无可邀请用户</div>
        </div>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="inviteVisible = false">取 消</el-button>
            <el-button type="primary" @click="yesInviteUser">邀 请</el-button>
          </div>
        </template>
      </el-dialog>
      <el-dialog v-model="removeVisible" width="500" title="移除成员" append-to-body align-center style="min-height: 450px;">
        <div class="invitetaggroupbox" v-if="circleUsers.length > 0">
          <div class="removememberbox" v-for="user in circleUsers" :key="user.nickname" @click="clickRemoveUser(user)" :class="{ selectactive: selectRemoveUserList.includes(user.user_id) }">
            <div style="display: flex; justify-content: space-between;">
              <div class="memberavatar"><img :src="user.usericon" alt="" style="width: 40px;"
                  referrerpolicy="no-referrer"></div>
              <div class="userinfo">
                <div style="font-weight: 700; font-size: 15px; cursor: pointer;">
                  {{ user.nickname }}
                </div>
                <div style="display: flex; align-items: center;">
                  <div
                    style="color: #333333; margin-top: 2px; font-size: 12px; display: flex; align-items: center; white-space: nowrap;">
                    粉丝：{{ user.follower_num }}&nbsp;&nbsp;
                    关注：{{ user.following_num }}&nbsp;&nbsp;
                    作品：{{ user.projects_num }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="invitetaggroupbox" v-else>
          <div style="width: 100%; text-align: center; color: #999999; padding-top: 110px;">暂无可移除用户</div>
        </div>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="removeVisible = false">取 消</el-button>
            <el-button type="primary" @click="yesRemoveUser">移 除</el-button>
          </div>
        </template>
      </el-dialog>
      <template #footer>
        <div class="dialog-footer">
          <div style="display: flex; justify-content: space-between">
            <div style="margin-top: auto;">
              <el-button type="success" @click="inviteUserClick" size="default">邀请成员</el-button>
              <el-button type="warning" @click="removeVisible = true" size="default">移除成员</el-button>
            </div>
            <div>
              <el-button @click="outerVisible = false">取 消</el-button>
              <el-button type="primary" @click="updateCircle">
                保 存
              </el-button>
            </div>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.selectactive {
  background-color: #E0E6EB !important;
  border-color: #0349B4 !important;
}

.removememberbox {
  padding: 8px;
  border: 1px solid #aaaaaa;
  border-radius: 4px;
  width: 100%;
  cursor: pointer;
  height: fit-content;
}

.removememberbox:hover {
  background-color: #F8F8F8;
}

.invitetaggroupbox {
  padding: 16px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  height: 329px;
  overflow-y: scroll;
}

.invitememberbox {
  padding: 8px;
  border: 1px solid #aaaaaa;
  border-radius: 4px;
  width: 100%;
  cursor: pointer;
  height: fit-content;
}

.invitememberbox:hover {
  background-color: #F5F5F5;
}


.memberavatar {
  border-radius: 50%;
  overflow: hidden;
  height: 40px;
  min-width: 40px;
  margin-right: 8px;
  border: 1px solid #999999;
}

.memberbox {
  padding: 8px;
  border: 1px solid #666666;
  border-radius: 4px;
  width: 100%;
}

.userbox {
  border: 1px solid black;
  border-radius: 4px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.btnbox {
  display: flex;
  align-items: center;
  width: fit-content;
  margin: 12px 0 0 auto;
}

.useravatar {
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid black;
  height: 80px;
  min-width: 80px;
  margin-right: 16px;
}

.circlebox {
  border: 1px solid #F2F3F5;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 16px;
  background-color: #F2F3F5;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2);
}

.circleavatar {
  border-radius: 50%;
  overflow: hidden;
  height: 70px;
  min-width: 70px;
  margin: 4px 10px 0 0;
}

.userinfo {
  width: 100%;
  color: #333333;
}

.circleName {
  font-size: 18px;
  color: #333333;
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
  margin: 0px 16px;
}

.languagetitle {
  color: #0E1116;
  padding: 8px 20px;
  font-size: 14px;
}

.taggroupbox {
  padding: 16px;
  padding-top: 4px;
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

.rightnotitlebox {
  border: 1px solid #666666;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
  min-height: 120px;

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

.kindicon {
  font-size: 13px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 4px;
  font-family: "Font Awesome 6 Free";
  font-weight: 600;
}
</style>