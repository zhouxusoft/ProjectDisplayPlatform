<script setup>
import { ref } from 'vue'
import ProjectItem from '../components/ProjectItem.vue'
const projects = ref([
	{
		id: 1,
		name: "RainManGO/vue3-composition-admin",
		main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
		tags: ["JavaScript", "Flask", "Vue", "BootStrap"],
		language: ["449633", "Vue"],
		starnum: 99586,
		updatetime: "2022/8/19"
	},
	{
		id: 2,
		name: "jeecgboot/jeecgboot-vue3",
		main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
		tags: ["JavaScript", "Vue", "BootStrap"],
		language: ["481828", "JavaScript"],
		starnum: 758,
		updatetime: "2022/8/19"
	},
	{
		id: 3,
		name: "Godxu电商平台",
		main: "Nodejs",
		tags: ["Flask", "Vue", "BootStrap", "JavaScript", "Flask", "BootStrap", "JavaScript", "Flask", "BootStrap"],
		language: ["995333", "Vue"],
		starnum: 10000,
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
		isactive: 0
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
		id: projects.value.length + 1,
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
		<div class="leftnav d-none d-md-block">
			<div class="leftnavborder">
				<div class="filter">Filter by</div>
				<div class="kindgroupbox p-2">
					<a class="kinditem" v-for="kind in kinds" :key="kind.id" :class="{ kinditemactive: kind.isactive }">
						<span class="kindicon" v-html="kind.icon"></span>
						<span class="kindname">{{ kind.name }}</span>
					</a>
				</div>
			</div>
		</div>
		<div class="straightline"></div>
		<div class="mainprojects px-4 py-3">
			<ProjectItem v-for="project in projects" :key="project.id" :project="project" />
			<button class="btn btn-success" @click="clickbtn()">add</button>
		</div>
		<div class="rightnav d-none d-lg-block p-2">
			这是 内容
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

.filter {
	font-size: 16px;
	font-weight: 500;
	padding: 16px 16px 8px;
	color: #000000;
}

.kinditem {
	position: relative;
	text-decoration: none;
	padding: 6px 8px;
	margin: 0 8px;
	display: flex;
	flex-grow: 1;
	border-radius: 6px;
	color: #0E1116;
}

.kinditemactive {
	background-color: rgb(206, 213, 220);
}

.kinditemactive::after {
	position: absolute;
	top: calc(50% - 12px);
	left: -8px;
	width: 4px;
	height: 24px;
	content: "";
	background-color: rgb(3, 73, 180);
	border-radius: 6px;
}

.kinditem:hover {
	background-color: rgb(231, 236, 240);
}

.kindicon {
	font-size: 14px;
	width: 20px;
	height: 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 8px;
	font-family: "Font Awesome 6 Free";
	font-weight: 600;
}

.kindname {
	font-size: 14px;
	height: 20px;
}
</style>