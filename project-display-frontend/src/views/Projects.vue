<script setup>
import { ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
import LeftNavItem from '../components/LeftNavItem.vue'
import LeftLanguageItem from '../components/LeftLanguageItem.vue'
import LeftTagItem from '../components/LeftTagItem.vue'
const projects = ref([
	{
		id: 1,
		usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
		name: "RainManGO/vue3-composition-admin",
		main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
		tags: ["JavaScript", "Flask", "Vue", "BootStrap"],
		language: { color: "449633", name: "Vue" },
		starnum: 99586,
		updatetime: "2022/8/19"
	},
	{
		id: 2,
		usericon: "https://avatars.githubusercontent.com/u/96218937?s=96&v=4",
		name: "jeecgboot/jeecgboot-vue3",
		main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
		tags: ["JavaScript", "Vue", "BootStrap"],
		language: { color: "481828", name: "JavaScript" },
		starnum: 758,
		updatetime: "2022/8/19"
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
	}
])
const languages = ref([
	{
		id: 1,
		color: "449633",
		name: "Java",
		isactive: false
	},
	{
		id: 2,
		color: "995333",
		name: "HTML",
		isactive: false
	},
	{
		id: 3,
		color: "481828",
		name: "JavaScript",
		isactive: false
	},
	{
		id: 4,
		color: "465999",
		name: "Vue",
		isactive: false
	},
	{
		id: 5,
		color: "995333",
		name: "C++",
		isactive: false
	},
	{
		id: 6,
		color: "747252",
		name: "Golang",
		isactive: false
	},
	{
		id: 7,
		color: "da1d2c",
		name: "PHP",
		isactive: false
	},
	{
		id: 8,
		color: "ad4a14",
		name: "Rust",
		isactive: false
	}
])
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
const starred = ref([
	{
		id: 1,
		projectid: 1
	},
	{
		id: 2,
		projectid: 3
	},
	{
		id: 3,
		projectid: 5
	}
])
for (let i = 0; i < projects.value.length; i++) {
	if (projects.value[i].starnum >= 1000) {
		projects.value[i].starnum = Math.floor(projects.value[i].starnum / 100)
		projects.value[i].starnum = projects.value[i].starnum / 10
		projects.value[i].starnum = projects.value[i].starnum + "k"
	}
}

// 记录参数；类型、语言、标签、页码
let currentkind = 1
let currentlanguage = 0
let activetags = []
let currentpage = 1
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

const clickbtn = () => {
	projects.value.push({
		id: projects.value.length + 1,
		name: "Godxu字体库Godxu字体库Godxu字体库",
		main: "Flask",
		tags: ["JavaScript", "Flask", "BootStrap"],
		language: { color: "747252", name: "Golang" },
		starnum: "9.7k",
		updatetime: "2022/8/19"
	})
}

/** 点击选择左侧的展示类型 */
const chooseLeftNav = (kind) => {
	if (!kind.isactive) {
		for (let i = 0; i < kinds.value.length; i++) {
			kinds.value[i].isactive = false
		}
		kind.isactive = true
	}
	if (kind.name == "Users") {
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

/** 点击选择语言 */
const chooseLanguage = (language) => {
	if (!language.isactive && currentkind == 1) {
		for (let i = 0; i < languages.value.length; i++) {
			languages.value[i].isactive = false
		}
		language.isactive = true
		currentlanguage = language.id
	}
	setCurrentUrl()
}

/** 点击选择标签 */
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

/** 重置标签按钮 */
const resetTag = () => {
	for (let i = 0; i < tags.value.length; i++) {
		tags.value[i].isactive = false
	}
	activetags = []
	setCurrentUrl()
}

/** 加载更多语言 */
const addMoreLanguages = () => {
	languageaddnum = languageaddnum + 1
	setCurrentLanguageList()
}

/** 加载更多标签 */
const addMoreTags = () => {
	tagaddnum = tagaddnum + 1
	setCurrentTagList()
}

/** 设置当前的显示的语言列表 */
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

/** 设置当前的显示的标签列表 */
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

/** 获取当前的url */
const getCurrentUrl = () => {
	let currenturl = window.location.href
	let route = currenturl.split('?')[0]
	let key = currenturl.split('?')[1]
	// console.log(currenturl)
	// console.log(routerurl)
	// console.log(searchkey)
	// routerurl + '?' + searchkey == currenturl
	return { route: route, key: key }
}

/** 根据用户选择的类型、标签、语言，设置url */
const setCurrentUrl = () => {
	let kindurl = ''
	let languageurl = ''
	let tagsurl = []
	for (let i = 0; i < kinds.value.length; i++) {
		if (currentkind == kinds.value[i].id) {
			kindurl = kinds.value[i].name
			break
		}
	}
	for (let i = 0; i < languages.value.length; i++) {
		if (currentlanguage == 0) {
			break
		}
		if (currentlanguage == languages.value[i].id) {
			languageurl = languages.value[i].name
			break
		}
	}
	for (const id of activetags) {
		const matchingObject = tags.value.find(item => item.id === id)
		if (matchingObject) {
			tagsurl.push(matchingObject.name)
		}
	}
	let route = ''
	if (kindurl) {
		route = 'kind=' + kindurl
	}
	if (languageurl) {
		route += '&language=' + languageurl
	}
	// console.log(tagsurl == [])
	if (tagsurl.length > 0) {
		route += '&tags='
		for (let i = 0; i < tagsurl.length; i++) {
			route += tagsurl[i] + '&'
		}
		route = route.slice(0, -1)
	}
	// console.log(kindurl)
	// console.log(languageurl)
	// console.log(tagsurl)
	// console.log(route)
	window.location = getCurrentUrl().route + '?' + route + '&page=' + currentpage
	return getCurrentUrl().route + '?' + route
}
setCurrentUrl()

/** 向后端发送请求，获取项目列表数据 */
const getProjects = () => {
	let toSend = {
		page: currentpage,
	}
	// 发送获取数据请求
	fetch('http://127.0.0.1:5000/projects', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json', // 设置请求头
		},
		credentials: 'include', // 在跨域请求中发送 cookies 和 http 认证信息
		body: JSON.stringify(toSend), // 设置请求体
	}).then(response => response.json()).then(data => {
		// 处理获取的数据
		// console.log(data.data)
		projects.value = data.data
	}).catch(error => {
		// 处理请求错误
		console.error('Error:', error)
	})
}

/** 向后端发送请求，获取展示类型数据 */
const getKinds = () => {
	// 发送获取数据请求
	fetch('http://127.0.0.1:5000/kinds', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json', // 设置请求头
		},
		credentials: 'include', // 在跨域请求中发送 cookies 和 http 认证信息
	}).then(response => response.json()).then(data => {
		// 处理获取的数据
		// console.log(data.data)
		kinds.value = data.data
	}).catch(error => {
		// 处理请求错误
		console.error('Error:', error)
	})
}

/** 向后端发送请求，获取语言类型数据 */
const getLanguages = () => {
	// 发送获取数据请求
	fetch('http://127.0.0.1:5000/languages', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json', // 设置请求头
		},
		credentials: 'include', // 在跨域请求中发送 cookies 和 http 认证信息
	}).then(response => response.json()).then(data => {
		// 处理获取的数据
		// console.log(data.data)
		alllanguages = data.data
		languages.value = alllanguages.slice(0, baselanguageaddnum)
	}).catch(error => {
		// 处理请求错误
		console.error('Error:', error)
	})
}

/** 向后端发送请求，获取标签类型数据 */
const getTags = () => {
	// 发送获取数据请求
	fetch('http://127.0.0.1:5000/tags', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json', // 设置请求头
		},
		credentials: 'include', // 在跨域请求中发送 cookies 和 http 认证信息
	}).then(response => response.json()).then(data => {
		// 处理获取的数据
		// console.log(data.data)
		alltags = data.data
		setCurrentTagList()
	}).catch(error => {
		// 处理请求错误
		console.error('Error:', error)
	})
}

/** 加载页面时获取数据 */
const getAllInfo = () => {
	getKinds()
	getLanguages()
	getTags()
	getProjects()
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
				<div class="languagegroupbox px-2">
					
				</div>
			</div>
		</div>
		<div class="straightline"></div>
		<div class="mainprojects px-4 py-3">
			<ProjectItem v-for="project  in  projects" :key="project.id" :project="project" :starred="starred" />
			<button class="btn btn-success" @click="clickbtn()">add</button>
		</div>
		<div class="rightnav d-none d-lg-block">
			<div class="rightinfobox">
				Vue.js（通常简称为Vue）是一款流行的JavaScript框架，用于构建交互式的用户界面（UI）。Vue的设计目标是简化Web应用程序的开发，并提供一种灵活且高效的方式来构建单页面应用程序（SPA）和其他前端项目。
			</div>
			<div class="rightinfobox">
				🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持
				RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城等功能。你的 ⭐️ Star ⭐️，是作者生发的动力！
			</div>
			<div class="rightinfobox">
				Hello World!
			</div>
			<div class="rightinfobox">
				广告位招租
			</div>
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
</style>