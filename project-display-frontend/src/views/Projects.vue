<script setup>
import { ref } from 'vue'
const projects = ref([
	{
		name: "RainManGO/vue3-composition-admin",
		main: "🎉 基于vue3 的管理端模板(Vue3 TS Vuex4 element-plus vue-i18n-next composition-api) vue3-admin vue3-ts-admin",
		content: "这是一个简易的线上聊天室项目"
	},
	{
		name: "jeecgboot/jeecgboot-vue3",
		main: "🔥 JeecgBoot—Vue3版前端源码，采用 Vue3.0+TypeScript+Vite+Ant-Design-Vue等新技术方案，包括二次封装组件、utils、hooks、动态菜单、权限校验、按钮级别权限控制等功能。 是JeecgBoot低代码平台的vue3技术栈的全…",
		content: "这是一个基于超星云盘的云盘"
	},
	{
		name: "Godxu电商平台",
		main: "Nodejs",
		content: "这是一个简易的电商平台项目"
	}
])
const clickbtn = () => {
	projects.value.push({
		name: "Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库Godxu字体库",
		main: "Flask",
		content: "这是一个字体库预览及下载项目"
	})
}
</script>

<template>
	<div class="">
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
						<h5>{{ project.content }}</h5>
					</div>
					<div class="projectstar">
						star
					</div>
				</div>
				<button class="btn btn-success" @click="clickbtn()">add</button>
			</div>
			<div class="rightnav d-none d-lg-block p-2">
				这是内容
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
	max-height: 100vh;
	top: 0;
	width: 270px;
}

.mainprojects {
	flex: 1;
	display: grid;
	gap: 16px;
	min-width: 0px;
	grid-template-columns: 1fr;
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
	border: 1px solid #666666;
	border-radius: 6px;
	height: 80px;
	padding: 8px;
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
</style>