<script setup>
import { ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import LeftNavItem from '../components/LeftNavItem.vue'
import LeftLanguageItem from '../components/LeftLanguageItem.vue'
import LeftTagItem from '../components/LeftTagItem.vue'
import CircleItem from '../components/CircleItem.vue'
import UserItem from '../components/UserItem.vue'
import { ElMessage } from 'element-plus'
import { projectsAPI, kindsAPI, languagesAPI, tagsAPI, circleListAPI, userListAPI } from '../api/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const isLoading = ref(false)

const projects = ref([
	// {
	// 	id: 1,
	// 	usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
	// 	name: "RainManGO/vue3-composition-admin",
	// 	main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
	// 	tags: ["JavaScript", "Flask", "Vue", "BootStrap"],
	// 	language: { color: "449633", name: "Vue" },
	// 	starnum: 99586,
	// 	updatetime: "2022/8/19",
	// 	cover: '123',
	// },
	// {
	// 	id: 2,
	// 	usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
	// 	name: "jeecgboot/jeecgboot-vue3",
	// 	main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
	// 	tags: ["JavaScript", "Vue", "BootStrap"],
	// 	language: { color: "481828", name: "JavaScript" },
	// 	starnum: 758,
	// 	updatetime: "2022/8/19",
	// 	cover: '123',
	// }
])
const kinds = ref([])
const languages = ref([])
const tags = ref([])
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

const toCircleDetail = (circleid) => {
	router.push({ path: `/circle/${circleid}` })
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

// 记录参数；类型、语言、标签、页码
let currentkind = 0
let currentlanguage = 0
let activetags = []
// 记录所有语言、标签
let alllanguages = []
let alltags = []
// 语言、标签基础加载数量
let baselanguageaddnum = 10
let basetagaddnum = 16
// 记录语言的加载次数
let languageaddnum = 1
// 记录标签的加载次数
let tagaddnum = 1
// 显示不同的加载样式
const lastlanguageaddtip = ref([true, 'More languages...'])
const lasttagaddtip = ref([true, 'More tags...'])

const currentpage = ref(1)

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
	if (kind.name != "Projects") {
		for (let i = 0; i < languages.value.length; i++) {
			languages.value[i].isactive = false
		}
		for (let i = 0; i < tags.value.length; i++) {
			tags.value[i].isactive = false
		}
		activetags = []
		currentlanguage = 0
	}
	currentkind = kind.id
	setCurrentUrl()
}

/**
 * 点击选择语言
 * @param {JSON} language 
 */
const chooseLanguage = (language) => {
	if (!language.isactive && currentkind == 1) {
		for (let i = 0; i < languages.value.length; i++) {
			languages.value[i].isactive = false
		}
		language.isactive = true
		currentlanguage = language.id
	} else if (language.isactive && currentkind == 1) {
		language.isactive = false
		currentlanguage = 0
	}
	setCurrentUrl()
}

/**
 * 点击选择标签
 * @param {JSON} tag 
 */
const chooseTag = (tag) => {
	activetags = []
	if (currentkind == 1) {
		tag.isactive = !tag.isactive
		for (let i = 0; i < tags.value.length; i++) {
			if (tags.value[i].isactive) {
				activetags.push(tags.value[i].id)
			}
		}
	}
	setCurrentUrl()
	// console.log(activetags)
}

/** 
 * 重置标签按钮 
 */
const resetTag = () => {
	for (let i = 0; i < tags.value.length; i++) {
		tags.value[i].isactive = false
	}
	activetags = []
	setCurrentUrl()
}

/**
 * 加载更多语言 
 */
const addMoreLanguages = () => {
	languageaddnum = languageaddnum + 1
	setCurrentLanguageList()
}

/**
 * 加载更多标签 
 */
const addMoreTags = () => {
	tagaddnum = tagaddnum + 1
	setCurrentTagList()
}

/**
 * 设置当前的显示的语言列表
 */
const setCurrentLanguageList = () => {
	let endnum = baselanguageaddnum * languageaddnum
	if (alllanguages.length > endnum) {
		languages.value = alllanguages.slice(0, endnum)
	} else if (alllanguages.length <= endnum - baselanguageaddnum) {
		languageaddnum = 1
		languages.value = alllanguages.slice(0, baselanguageaddnum)
		lastlanguageaddtip.value = [true, 'More languages...']
	} else {
		languages.value = alllanguages
		lastlanguageaddtip.value = [false, 'No more languages']
	}
}

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

/**
 * 根据用户选择的类型、标签、语言，设置url
 */
const setCurrentUrl = () => {
	const queryParams = new URLSearchParams()

	// 处理 kind 参数
	const activeKind = kinds.value.find(k => k.id === currentkind)
	if (activeKind) queryParams.set('kind', activeKind.name)

	// 处理 language 参数
	if (currentlanguage !== 0) {
		const activeLang = languages.value.find(l => l.id === currentlanguage)
		if (activeLang) queryParams.set('language', activeLang.name)
	}

	// 处理 tags 参数
	const activeTags = tags.value
		.filter(t => activetags.includes(t.id))
		.map(t => t.name);
	if (activeTags.length > 0) {
		queryParams.set('tags', activeTags.join(','))
	}

	// 添加页码
	queryParams.set('page', currentpage.value)

	// 执行路由跳转
	router.push({
		query: Object.fromEntries(queryParams)
	})
}

const circleList = ref([])

const getCircleList = () => {
	circleListAPI().then(res => {
		circleList.value = res.data
	}).catch(error => {
		isLoading.value = false
		console.error('Error:', error)
	})
}

const userList = ref([])

const getUserList = () => {
	// 发送获取数据请求
	isLoading.value = true
	userListAPI().then(res => {
		isLoading.value = false
		userList.value = res.data
	}).catch(error => {
		isLoading.value = false
		console.error('Error:', error)
	})
}

/**
 * 向后端发送请求，获取项目列表数据
 */
const getProjects = () => {
	let toSend = {
		page: currentpage.value,
	}
	// 发送获取数据请求
	isLoading.value = true
	projectsAPI(toSend).then(res => {
		isLoading.value = false
		projects.value = res.data
		total.value = res.total
		starnumFormat()
	}).catch(error => {
		isLoading.value = false
		console.error('Error:', error)
	})
}

/**
 * 向后端发送请求，获取展示类型数据
 */
const getKinds = () => {
	// 发送获取数据请求
	isLoading.value = true
	kindsAPI().then(res => {
		isLoading.value = false
		kinds.value = res.data
		let parmas = router.currentRoute.value.query
		if (parmas?.kind) {
			let ckind = kinds.value.find((item) => item.name == parmas.kind)
			if (ckind) {
				currentkind = ckind.id
				chooseLeftNav(ckind)
			} else {
				currentkind = kinds.value[0].id
				kinds.value[0].isactive = true
				setCurrentUrl()
			}
		} else {
			currentkind = kinds.value[0].id
			kinds.value[0].isactive = true
			setCurrentUrl()
		}
	}).catch(error => {
		isLoading.value = false
		console.error('Error:', error)
	})
}

/**
 * 向后端发送请求，获取语言类型数据
 */
const getLanguages = () => {
	// 发送获取数据请求
	isLoading.value = true
	languagesAPI().then(res => {
		isLoading.value = false
		alllanguages = res.data
		languages.value = alllanguages.slice(0, baselanguageaddnum)
	}).catch(error => {
		isLoading.value = false
		console.error('Error:', error)
	})
}

/**
 * 向后端发送请求，获取标签类型数据
 */
const getTags = () => {
	// 发送获取数据请求
	isLoading.value = true
	tagsAPI().then(res => {
		isLoading.value = false
		alltags = res.data
		setCurrentTagList()
	}).catch(error => {
		isLoading.value = false
		console.error('Error:', error)
	})
}

const changPage = () => {
	window.scrollTo({
		top: 0,
		left: 0,
		behavior: 'smooth'
	})
	getProjects()
}

const total = ref(0)

const updateUser = () => {
	getUserList()
}

const handleImageError = (event) => {
	// 检查当前src是否已经是默认图片，避免无限循环
	if (!event.target.src.endsWith('/error_img.png')) {
		event.target.src = '/error_img.png'
	}
}

/**
 * 加载页面时获取数据
 */
const getAllInfo = () => {
	getKinds()
	getLanguages()
	getTags()
	getProjects()
	getCircleList()
	getUserList()
}
getAllInfo()
</script>

<template>
	<div class="borderbox">
		<div class="leftnav d-none d-md-block">
			<div class="leftnavborder">
				<div class="filter">Filter by</div>
				<div class="kindgroupbox p-2">
					<LeftNavItem v-for="kind in kinds" :key="kind.id" :kind="kind" @click="chooseLeftNav(kind)" />
				</div>
				<div class="fengeline"></div>
				<div v-if="currentkind == 1">
					<div class="languagetitle">Lagnuages</div>
					<div class="languagegroupbox p-2">
						<LeftLanguageItem v-for="language in languages" :key="language.id" :language="language"
							@click="chooseLanguage(language)" />
						<div class="addmorelanguage" @click="addMoreLanguages"><span class="addmoreicon"
								v-if="lastlanguageaddtip[0]">&#x2b</span><span class="addlessicon" v-else>&#xf068</span>{{
									lastlanguageaddtip[1] }}</div>
					</div>
					<div class="fengeline"></div>
					<div class="resettagbox">
						<div class="languagetitle">Tags</div>
						<div class="resettags" @click="resetTag()">Reset</div>
					</div>
					<div class="taggroupbox">
						<LeftTagItem v-for="tag in tags" :key="tag.id" :tag="tag" @click="chooseTag(tag)" />
						<div class="addmoretag" @click="addMoreTags"><span class="addmoreicon"
								v-if="lasttagaddtip[0]">&#x2b</span><span class="addlessicon" v-else>&#xf068</span>{{
									lasttagaddtip[1] }}</div>
					</div>
				</div>
				<div class="languagegroupbox px-2"></div>
			</div>
		</div>
		<div class="straightline"></div>
		<div class="mainprojects px-4 py-3" v-loading="isLoading">
			<ProjectItem v-for="project in projects" :key="project.id" :project="project" :starred="starred"
				v-if="currentkind == 1" />
			<div v-if="currentkind == 2">
				<UserItem v-for="user in userList" :key="user.id" :user="user" @updateUser="updateUser" />
				<div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
			</div>
			<div v-if="currentkind == 3">
				<CircleItem v-for="circle in circleList" :key="circle.id" :circle="circle" />
				<div style="width: fit-content; margin: 10px auto; color: #666666">没有更多了...</div>
			</div>
			<el-pagination plain layout="prev, pager, next" :total="total" :page-size="15" v-if="currentkind == 1"
				v-model:current-page="currentpage" hide-on-single-page @current-change="changPage()" style="margin: 0 auto;" />
		</div>
		<div class="rightnav d-none d-xl-block">
			<div class="circlebox" v-if="currentkind == 1 && circleList.length > 0">
				<div style="display: flex; height: 30px; font-size: 18px; font-weight: 700; color: #303133;">推 荐 圈 子</div>
				<div class="fengeline2"></div>
				<div style="display: flex; justify-content: space-between; cursor: pointer"
					@click="toCircleDetail(circleList[0].id)">
					<div class="circleavatar" style="border-radius: 0.25em;"><img :src="circleList[0].cover" alt=""
							style="width: 70px;" referrerpolicy="no-referrer" @error="handleImageError"></div>
					<div class="userinfo">
						<div style="font-weight: 700; font-size: 18px;">{{ circleList[0].name }}</div>
						<div style="color: #333333; margin-top: 4px;">{{ circleList[0].description }}</div>
					</div>
				</div>
				<div style="display: flex; justify-content: center; align-items: center; margin-top: 8px;">
					<div
						style="color: #333333; margin-top: 4px; font-size: 13px; display: flex; align-items: center; white-space: nowrap;">
						<span class="kindicon" style="font-size: 13px;">&#xf0c0</span>成员：{{ circleList[0].member_count
						}}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 13px">&#xf06e</span>粉丝：{{
							circleList[0].follower_count }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon"
							style="font-size: 13px">&#xf1ea</span>作品：{{ circleList[0].project_count }}
					</div>
				</div>
			</div>
			<div class="rightinfobox">
				Vue.js（通常简称为Vue）是一款流行的JavaScript框架，用于构建交互式的用户界面（UI）。Vue的设计目标是简化Web应用程序的开发，并提供一种灵活且高效的方式来构建单页面应用程序（SPA）和其他前端项目。
			</div>
			<div class="rightinfobox">
				🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持
				RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城等功能。你的 ⭐️ Star ⭐️，是作者生发的动力！
			</div>
			<div class="rightinfobox">
				广告位招租
			</div>
		</div>
	</div>
	<div class="addproject" @click="this.$router.push('/newProject')">+</div>
</template>

<style scoped>
.userbox {
	border: 1px solid black;
	border-radius: 4px;
	padding: 16px;
	display: flex;
	justify-content: space-between;
	margin-bottom: 16px;
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
	padding: 16px;
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
	margin: 8px 16px;
}

.fengeline2 {
	height: 1px;
	background-color: rgb(136, 146, 157);
	margin: 6px 0 12px;
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
	color: #555555;
}
</style>