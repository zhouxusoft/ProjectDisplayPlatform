<script setup>
import { ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import LeftNavItem from '../components/LeftNavItem.vue'
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

/**
 * 加载页面时获取数据
 */
const getAllInfo = () => {
}
getAllInfo()

</script>

<template>
  <div class="borderbox">
    <div class="leftnav d-none d-md-block">
      <div class="leftnavborder" style="padding: 16px;">
        <div class="searchinputbox d-flex me-1" :class="{ focused: isinputfocus }">
          <div class="form-control form-control-sm searchlogo"></div>
          <input class="form-control form-control-sm searchinput p-0" placeholder="Search" v-model="searchKey"
            aria-label="Search" @focus="inputFocus()" @blur="inputBlur()" @input="inputInput()">
          <span class="clearbox">
            <span v-show="showClear" class="clear" @click="clearInput()">&#xf00d</span>
          </span>
          <button class="searchbutton" type="button"></button>
        </div>
        <div class="fengeline"></div>
        <div class="userbox" style="background-color: #CED5DC;">
          <div class="useravatar"><img src="../assets/images/touxaing.webp" alt="" style="width: 30px;"></div>
          <div class="userinfo">
            <div style="font-weight: 700;">ZhouFuKang</div>
            <div style="color: #555555; margin-top: 4px; font-size: 14px;">感谢关注up主，✌以后多多...</div>
          </div>
        </div>
        <div class="userbox" style="margin-top: 8px;">
          <div class="useravatar"><img src="../assets/images/20231026-213431.jpg" alt="" style="width: 30px;"></div>
          <div class="userinfo">
            <div style="font-weight: 700;">OuYangPeng</div>
            <div style="color: #555555; margin-top: 4px; font-size: 14px;">昨天的那个文章我有一点疑...</div>
          </div>
        </div>
      </div>
    </div>
    <div class="straightline"></div>
    <div class="mainprojects px-4 py-3">
      <img src="../assets/images/image.png" alt="" style="width: 800px; border: 1px solid #666666">
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
  width: 300px;
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
  color: #555555;
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