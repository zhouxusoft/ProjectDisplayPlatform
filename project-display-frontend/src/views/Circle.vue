<script setup>
import { onMounted, ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import { ElMessage } from 'element-plus'
import { circleDetailAPI } from '../api/api'
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
      starnumFormat()
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
                  <div style="font-weight: 700; font-size: 15px;">{{ user.nickname }}
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
          <div class="filter" style="padding-top: 0;">成员 <span style="font-size: 14px; color: #666666;">{{ circleInfo.member_count }}</span></div>
          <div class="taggroupbox" v-if="circleUsers.length > 0">
            <div class="memberbox" v-for="user in circleUsers" :key="user.nickname">
              <div style="display: flex; justify-content: space-between;">
                <div class="memberavatar"><img :src="user.usericon" alt="" style="width: 40px;"
                    referrerpolicy="no-referrer"></div>
                <div class="userinfo">
                  <div style="font-weight: 700; font-size: 15px;">{{ user.nickname }}
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
      <ProjectItem v-for="project in circleProjects" :key="project.id" :project="project" :starred="starred" />
      <div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
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
            <span class="kindicon" style="font-size: 13px;">&#xf0c0</span>成员：{{ circleInfo.member_count
            }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 13px">&#xf06e</span>粉丝：{{
              circleInfo.follower_count }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon"
              style="font-size: 13px">&#xf1ea</span>作品：{{ circleInfo.project_count }}
          </div>
        </div>
        <div class="btnbox">
          <el-button size="small" plain v-if="circleInfo.flag == 4">申请加入</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 2"><span class="kindicon"
              style="font-size: 14px">&#xf00c</span>已加入</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 4">订阅圈子</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 3"><span class="kindicon"
              style="font-size: 14px">&#xf0e0</span>已订阅</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 1"><span class="kindicon"
              style="font-size: 14px">&#xf0c9</span>管理圈子</el-button>
          <el-button size="small" plain v-if="circleInfo.flag == 1"><span class="kindicon"
              style="font-size: 14px">&#xf00d</span>解散圈子</el-button>
        </div>
      </div>

      <div class="rightnotitlebox">
        暂无公告
      </div>
      <div class="rightnotitlebox">
        广告位招租
      </div>
      <div class="rightinfobox">
        🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持
        RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城等功能。你的 ⭐️ Star ⭐️，是作者生发的动力！
      </div>
    </div>
  </div>
</template>

<style scoped>
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
  display: flex;
  justify-content: center;
  align-items: center;
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