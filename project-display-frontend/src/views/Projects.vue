<script setup>
import { ref } from 'vue'
const projects = ref([
	{
		name: "RainManGO/vue3-composition-admin",
		main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
		tags: ["JavaScript", "Flask", "Vue", "BootStrap"],
		language: ["449633", "Vue"],
		starnum: 99586,
		updatetime: "2022/8/19"
	},
	{
		name: "jeecgboot/jeecgboot-vue3",
		main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
		tags: ["JavaScript", "Vue", "BootStrap"],
		language: ["481828", "Vue"],
		starnum: 758,
		updatetime: "2022/8/19"
	},
	{
		name: "Godxu电商平台",
		main: "Nodejs",
		tags: ["Flask", "Vue", "BootStrap"],
		language: ["995333", "Vue"],
		starnum: 10000,
		updatetime: "2022/8/19"
	}
])
for (let i = 0; i < projects.value.length; i++) {
	if (projects.value[i].starnum >= 1000) {
		projects.value[i].starnum = Math.floor(projects.value[i].starnum / 100)
		projects.value[i].starnum = projects.value[i].starnum / 10
		projects.value[i].starnum = projects.value[i].starnum + "k"
	}
}
const clickbtn = () => {
	projects.value.push({
		name: "Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库",
		main: "Flask",
		tags: ["JavaScript", "Flask", "BootStrap"],
		language: ["449633", "Vue"],
		starnum: "9.7k",
		updatetime: "2022/8/19"
	})
}
</script>

<template>
	<div class="borderbox">
		<div class="leftnav d-none d-md-block p-2">
			这是内容
		</div>
		<div class="straightline"></div>
		<div class="mainprojects px-4 py-3">
			<div v-for="project in projects" class="projectdata p-3">
				<div class="projectinfo">
					<div class="projecttop">
						<div class="projectusericonbox">
							<img src="https://avatars.githubusercontent.com/u/96218937?s=96&v=4" alt="User Icon"
								class="projectusericon">
						</div>
						<div class="projectnamebox">
							<span class="projectname">{{ project.name }}</span>
						</div>
					</div>
					<div class="projectoverview">
						<span>{{ project.main }}</span>
					</div>
					<div class="projecttagbox my-2">
						<a v-for="tag in project.tags" class="projecttag" href="/">{{ tag }}</a>
					</div>
					<div class="projectbottom">
						<div class="projectlanguagebox">
							<div class="projectlanguageicon" :style="{ backgroundColor: '#' + project.language[0] }"></div>
							<div class="projectlanguage">{{ project.language[1] }}</div>
						</div>
						<span class="mx-2">·</span>
						<div><span class="starfont">&#xf005</span>{{ project.starnum }}</div>
						<span class="mx-2">·</span>
						<div class="projectupdatetime">Updated on {{ project.updatetime }}</div>
					</div>
				</div>
				<div class="projectstar">
					<button class="starfontbtn"><span class="starfont">&#xf005</span>Star</button>
				</div>
			</div>
			<button class="btn btn-success" @click="clickbtn()">add</button>
		</div>
		<div class="rightnav d-none d-lg-block p-2">
			这是内容
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
	width: 270px;
}

.projectdata {
	border: 1px solid #666666;
	border-radius: 6px;
	display: flex;
}

.projectinfo {
	flex: 1;
}

.projecttop {
	display: flex;
	flex: 1;
}

.projectstar {
	margin-left: 8px;
	width: 80px;
	display: flex;
	justify-content: flex-end;
}

.starfont {
	font-family: "Font Awesome 6 Free";
	font-weight: 300;
	margin-right: 6px;
}

.projectusericonbox {
	width: 20px;
	height: 20px;
	border-radius: 50%;
	box-shadow: rgba(1, 4, 9, 0.8) 0px 0px 0px 1px;
	overflow: hidden;
	display: flex;
	margin-right: 10px;
}

.projectusericon {
	width: 20px;
}

.projectnamebox {
	flex: 1;
	width: 0;
	overflow: hidden;
	display: flex;
	align-items: end;
	cursor: pointer;
}

.projectname:hover {
	text-decoration: underline;
}

.projectname {
	text-overflow: ellipsis;
	white-space: nowrap;
	font-size: 16px;
	font-weight: 600;
	color: rgb(3, 73, 180);
}

.projectoverview {
	margin-top: 4px;
	font-size: 14px;
	word-wrap: break-word;
}

.starfontbtn {
	border: 1px solid #666666;
	border-radius: 6px;
	font-size: 12px;
	height: 28px;
	padding: 0 8px;
	background-color: rgb(231, 236, 240);
}

.starfontbtn:hover {
	background-color: rgb(206, 213, 220);
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
	border-radius: 2em;
	line-height: 22px;
	background-color: rgb(223, 247, 255);
	white-space: nowrap;
}

.projecttag:hover {
	background-color: rgb(3, 73, 180);
	color: rgb(255, 255, 255);
}

.projectbottom {
	font-size: 12px;
	display: flex;
}

.projectlanguagebox {
	display: flex;
	align-items: center;
}

.projectlanguageicon {
	border-radius: 8px;
    border-style: solid;
    border-width: 1px;
    border-color: rgba(1, 4, 9, 0.1);
    width: 10px;
    height: 10px;
	margin-right: 8px;
}
</style>