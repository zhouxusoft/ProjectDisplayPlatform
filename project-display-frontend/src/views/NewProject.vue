<script setup>
import { onMounted, ref } from 'vue'
import TinyMCE from '../components/TinyMCE/index.vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { globalData } from './globalData'
import LeftTagItem from '../components/LeftTagItem.vue'
import { tagsAPI, languagesAPI } from '../api/api.js'

const router = useRouter()

const html = ref('')

const goBack = () => {
  router.push({ path: globalData.previousPage })
}

const tags = ref([
  {
    id: 1,
    name: "Java",
    isactive: false
  },
  {
    id: 2,
    name: "HTML",
    isactive: false
  }
])

let languages = ref([])

const selectLanguage = ref('')

/**
 * 向后端发送请求，获取语言类型数据
 */
const getLanguages = () => {
  // 发送获取数据请求
  languagesAPI().then(res => {
    languages.value = res.data
  }).catch(error => {
    console.error('Error:', error)
  })
}

const activetags = ref([])

/**
 * 点击选择标签
 * @param {JSON} tag 
 */
const chooseTag = (tag) => {
  if (tag.isactive == false && activetags.value.length >= 5) {
    ElMessage({
      message: '最多只能选择5个标签',
      type: 'warning',
      duration: 2000,
      offset: 9,
    })
    return
  }
  activetags.value = []
  tag.isactive = !tag.isactive
  for (let i = 0; i < tags.value.length; i++) {
    if (tags.value[i].isactive) {
      activetags.value.push(tags.value[i])
    }
  }
}

/** 
 * 重置标签按钮 
 */
const resetTag = () => {
  for (let i = 0; i < tags.value.length; i++) {
    tags.value[i].isactive = false
  }
  activetags.value = []
}

/**
 * 关闭标签
 * @param {JSON} tag 
 */
const handleClose = (tag) => {
  tag.isactive = false
  for (let i = 0; i < tags.value.length; i++) {
    if (tags.value[i].name == tag.name) {
      tags.value[i].isactive = false
    }
  }
  activetags.value = activetags.value.filter(t => t.name !== tag.name)
}

const whoComment = ref(1)
const circleType = ref(1)
const whoLook = ref(1)

const contentHtml = ref('')
const getContent = (content) => {
  contentHtml.value = content
}

const dialogVisible = ref(false)
const handleCloseDialog = () => {
  dialogVisible.value = false
}

/**
 * 向后端发送请求，获取标签类型数据
 */
const getTags = () => {
  // 发送获取数据请求
  tagsAPI().then(res => {
    alltags = res.data
    setCurrentTagList()
  }).catch(error => {
    console.error('Error:', error)
  })
}

let alltags = []
let basetagaddnum = 16
// 记录标签的加载次数
let tagaddnum = 1
// 显示不同的加载样式
const lasttagaddtip = ref([true, 'More tags...'])

/**
 * 加载更多标签 
 */
const addMoreTags = () => {
  tagaddnum = tagaddnum + 1
  setCurrentTagList()
}

const inputValue = ref('')

/**
 * 设置当前的显示的标签列表
 */
const setCurrentTagList = () => {
  let endnum = basetagaddnum * tagaddnum
  if (alltags.length > endnum) {
    tags.value = alltags.slice(0, endnum)
  } else if (alltags.length <= endnum - basetagaddnum) {
    tagaddnum = 1
    tags.value = alltags.slice(0, basetagaddnum)
    lasttagaddtip.value = [true, 'More tags...']
  } else {
    tags.value = alltags
    lasttagaddtip.value = [false, 'No more tags']
  }
}

const coverInput = ref(null);
const coverPreview = ref(null);

function uploadCover() {
  if (coverInput.value) {
    coverInput.value.value = null; // 重置，防止选同一张文件时不触发change事件
    coverInput.value.click();
  }
}

function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  // 文件类型校验
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件');
    return;
  }

  // 文件大小校验，最大5MB
  const maxSizeMB = 5;
  if (file.size > maxSizeMB * 1024 * 1024) {
    ElMessage.error(`图片大小不能超过${maxSizeMB}MB`);
    return;
  }

  // 生成本地预览URL
  coverPreview.value = URL.createObjectURL(file);
  console.log(coverPreview.value);
}
const showMask = ref(false);

function deleteCover() {
  coverPreview.value = null;
  showMask.value = false;
}

onMounted(() => {
  getTags()
  getLanguages()
})
</script>

<template>
  <div class="borderbox">
    <div class="leftnav d-none d-md-block">
      <div class="leftnavborder">
        <el-button @click="goBack()" style="color: #333; padding-left: 8px; font-size: 15px;" text><span
            class="kindicon" style="font-size: 14px">&#xf053</span>返 回</el-button>
        <div class="fengeline"></div>
        <div style="display: flex; justify-content: space-between;">
          <div style="width: 130px;">发布到：</div>
          <el-radio-group v-model="circleType" style="width: 180px;">
            <el-radio value="1" size="large">公共社区</el-radio>
            <el-radio value="2" size="large">指定圈子</el-radio>
          </el-radio-group>
        </div>
        <div class="fengeline"></div>
        <div style="display: flex; justify-content: space-between;">
          <div style="width: 130px;">谁可以看：</div>
          <el-radio-group v-model="whoLook" style="width: 180px;">
            <el-radio value="1" size="large">公开</el-radio>
            <el-radio value="2" size="large">仅关注</el-radio>
            <el-radio value="3" size="large">私密</el-radio>
          </el-radio-group>
        </div>
        <div class="fengeline"></div>
        <div style="display: flex; justify-content: space-between;">
          <div style="width: 130px;">谁可以评论：</div>
          <el-radio-group v-model="whoComment" style="width: 180px;">
            <el-radio value="1" size="large">所有人</el-radio>
            <el-radio value="2" size="large">仅关注</el-radio>
            <el-radio value="3" size="large">关闭评论</el-radio>
          </el-radio-group>
        </div>
      </div>
    </div>
    <div class="straightline"></div>
    <div class="mainprojects px-4 py-3">
      <div class="titlebox" style="display: flex; align-items: center;">
        <el-tooltip content="在信息汪洋中校准思维的航向" placement="top-start" effect="dark">
          <div style="font-weight: 700; color: #555555; font-size: 22px; min-width: 110px;">文章标题：</div>
        </el-tooltip>
        <input type="text"
          style="border: none; border-bottom: 1px solid #333333; font-size: 20px; width: 100%; padding: 5px;"
          placeholder="请输入文章标题（5 - 50 字）">
      </div>
      <div class="tinymce1">
        <TinyMCE ref="tinymce" :html="html" @update:modelValue="getContent" />
      </div>
      <div class="aboutbox">
        <div class="abouttagbox">
          <el-tooltip content="在概率云中锚定认知坐标的定位仪" placement="top-start" effect="dark">
            <div class="abouttagboxtitle" style="min-width: 80px;">文章标签</div>
          </el-tooltip>
          <el-tag size="large" v-for="tag in activetags" :key="tag.id" closable :disable-transitions="false"
            @close="handleClose(tag)" style="margin-right: 8px;" effect="plain">
            {{ tag.name }}
          </el-tag>
          <el-button plain @click="dialogVisible = true" size="default" style="font-size: 13px;"><span class="kindicon"
              style="">&#x2b</span>添加文章标签</el-button>
        </div>
        <div class="aboutlanguagebox">
          <el-tooltip content="灵魂寄居于代码之间" placement="top-start" effect="dark">
            <div style="min-width: 80px;">主要语言</div>
          </el-tooltip>
          <el-select v-model="selectLanguage" placeholder="选择编程语言" style="width: 240px" clearable filterable>
            <el-option v-for="item in languages" :key="item.id" :label="item.name" :value="item.name">
              <div style="display: flex; align-items: center;">
                <div class="languageitemicon" :style="{ backgroundColor: '#' + item.color }"></div>
                <span style="font-size: 14px; margin-left: 4px;">{{ item.name }}</span>
              </div>
            </el-option>
          </el-select>
        </div>
        <div class="aboutcoverbox">
          <el-tooltip content="所有星图在纸面褶皱处坍缩成刃" placement="top-start" effect="dark">
            <div style="min-width: 80px;">选择封面</div>
          </el-tooltip>
          <div v-if="!coverPreview" class="addcover" @click="uploadCover">
            <span class="kindicon" style="font-size: 20px; color: #fff">&#x2b</span>
            <input type="file" ref="coverInput" style="display: none" accept="image/*" @change="handleUpload" />
          </div>
          <!-- <div v-if="coverPreview" class="coverpreview">
            <img :src="coverPreview" alt="封面预览" style="width: 160px;" />
          </div> -->
          <div v-if="coverPreview" class="coverpreview" @mouseleave="showMask = false" @mouseenter="showMask = true">
            <img :src="coverPreview" alt="封面预览" />
            <div class="mask" v-show="showMask" @click.stop="deleteCover">
              <svg xmlns="http://www.w3.org/2000/svg" class="trash-icon" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <line x1="3" y1="6" x2="21" y2="6" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 6l-1 14H6L5 6" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 11v6M14 11v6" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 6V4h6v2" />
              </svg>
              <!-- <span class="kindicon" style="font-size: 20px; color: #fff">&#xf2ed</span> -->
            </div>
          </div>
        </div>
        <div class="aboutmainbox">
          <el-tooltip content="跳动灵魂的核心被凝聚成璀璨的星云碎片" placement="top-start" effect="dark">
            <div style="min-width: 80px;">文章摘要</div>
          </el-tooltip>
          <el-input v-model="userComment" maxlength="256" style="width: 100%; font-size: 16px;" placeholder="说点什么吧"
            show-word-limit type="textarea" :autosize="{ minRows: 3, maxRows: 10 }" />
          <el-tooltip content="将正文前256字键入摘要文本框" placement="top-start" effect="dark">
            <el-button style="margin-left: 10px; margin-top: auto;" @click="putComment()" plain>一键提取</el-button>
          </el-tooltip>
        </div>
      </div>
      <div>
        <button class="addproject" @click="goBack">发 布</button>
      </div>
    </div>
    <div class="rightnav d-none d-xl-block">
    </div>
    <el-dialog v-model="dialogVisible" title="选择文章标签" width="500" :before-close="handleCloseDialog" align-center>
      <el-divider style="margin: 8px 0;" />
      <div class="taggroupbox">
        <LeftTagItem v-for="tag in tags" :key="tag.id" :tag="tag" @click="chooseTag(tag)" />
        <div class="addmoretag" @click="addMoreTags"><span class="addmoreicon" v-if="lasttagaddtip[0]">&#x2b</span><span
            class="addlessicon" v-else>&#xf068</span>{{
              lasttagaddtip[1] }}</div>
      </div>
      <el-divider style="margin: 16px 0;" />
      <div class="newtag">
        <div style="min-width: 96px;">自定义标签：</div>
        <el-input ref="InputRef" v-model="inputValue" size="small" maxlength="16" show-word-limit
          @keyup.enter="handleInputConfirm" @blur="handleInputConfirm" />
        <el-button class="button-new-tag" size="small" @click="showInput" plain style="margin-left: 8px;">
          + 添加
        </el-button>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="resetTag()" plain>重置</el-button>
          <el-button @click="dialogVisible = false" type="primary">确 认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.coverpreview {
  position: relative;
  width: 160px;
  height: 100px;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid #ddd;
}

.coverpreview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 遮罩层 */
.mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s;
  opacity: 1;
  color: white;
}

/* 垃圾桶图标样式 */
.trash-icon {
  width: 32px;
  height: 32px;
  cursor: pointer;
  user-select: none;
}

.mask:hover .trash-icon {
  color: #fff;
}

.languageitemicon {
  border-radius: 8px;
  border-style: solid;
  border-width: 1px;
  border-color: rgba(1, 4, 9, 0.1);
  width: 10px;
  height: 10px;
  margin: 5px;
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

.newtag {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 16px;
  padding: 8px;
}

.aboutmainbox {
  padding: 8px 16px;
  display: flex;
}

.abouttagboxtitle::after {
  content: "*";
  color: red;
}

.addcover {
  width: 160px;
  height: 100px;
  background-color: rgb(231, 236, 240);
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  color: #0E1116;
  cursor: pointer;
}

.addcover:hover {
  border: 1px dashed #aaaaaa;
}

.aboutcoverbox {
  padding: 16px 16px;
  display: flex;
}

.taggroupbox {
  padding: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.abouttagbox {
  display: flex;
  align-items: center;
  padding: 8px 16px;
}

.aboutlanguagebox {
  padding: 16px 16px 8px;
  display: flex;
  align-items: center;
}

.aboutbox {
  border: 2px solid #dddddd;
  border-radius: 6px;
  padding: 16px;
  color: #666666;
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

.resettagbox {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  display: flex;
  justify-content: center;
  align-items: center;
  width: 140px;
  height: 40px;
  border: 1px solid #FC5531;
  background-color: #FC5531;
  color: white;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2);
  margin-left: auto;
  border-radius: 4px;
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
}

.fengeline {
  height: 1px;
  background-color: rgb(136, 146, 157);
  margin: 8px 0px;
}
</style>