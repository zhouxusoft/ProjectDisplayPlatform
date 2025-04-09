<script setup>
import { ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import LeftNavItem from '../components/LeftNavItem.vue'
import TinyMCE from '../components/TinyMCE/index.vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

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
    cover: '123',
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
  {
    icon: "&#xf1da",
    id: 4,
    isactive: false,
    name: "History"
  }
])

const activeName = ref('first')

const currentkind = ref(1)

const starred = ref([
  {
    id: 1,
    projectid: 1
  },
  {
    id: 2,
    projectid: 2
  }
])

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
 * 加载页面时获取数据
 */
const getAllInfo = () => {
}
getAllInfo()

const radio1 = ref(1)
const content = ref('')
const getContent = (content) => {  
    content.value = content
    console.log(666);
    
}

</script>

<template>
  <div class="borderbox">
    <div class="leftnav d-none d-md-block">
      <div class="leftnavborder">
        <div style="display: flex; justify-content: space-between;">
          <div style="width: 130px;">发布到：</div>
          <el-radio-group v-model="radio1" style="width: 180px;">
            <el-radio value="1" size="large">公共社区</el-radio>
            <el-radio value="2" size="large">指定圈子</el-radio>
          </el-radio-group>
        </div>
        <div class="fengeline"></div>
        <div style="display: flex; justify-content: space-between;">
          <div style="width: 130px;">谁可以看：</div>
          <el-radio-group v-model="radio1" style="width: 180px;">
            <el-radio value="1" size="large">公开</el-radio>
            <el-radio value="2" size="large">仅关注</el-radio>
            <el-radio value="3" size="large">私密</el-radio>
          </el-radio-group>
        </div>
        <div class="fengeline"></div>
        <div style="display: flex; justify-content: space-between;">
          <div style="width: 130px;">谁可以评论：</div>
          <el-radio-group v-model="radio1" style="width: 180px;">
            <el-radio value="1" size="large">所有人</el-radio>
            <el-radio value="2" size="large">仅关注</el-radio>
            <el-radio value="3" size="large">关闭评论</el-radio>
          </el-radio-group>
        </div>
      </div>
    </div>
    <div class="straightline"></div>
    <div class="mainprojects px-4 py-3">
      <div class="titlebox" style="display: flex;">
        <div style="font-weight: 700; color: #555555; font-size: 22px;">文章标题：</div>
        <input type="text" style="border: none; border-bottom: 1px solid #333333; font-size: 20px; width: 500px;" placeholder="请输入文章标题（5 - 50 字）">
      </div>
      <div class="tinymce1">
        <TinyMCE ref="tinymce" :html="html" @input="getContent" />
      </div>
    </div>
    <div class="rightnav d-none d-xl-block">

    </div>
  </div>
</template>

<style scoped>
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
  padding: 16px 16px 60px;
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

.fengeline {
  height: 1px;
  background-color: rgb(136, 146, 157);
  margin: 8px 0px;
}
</style>