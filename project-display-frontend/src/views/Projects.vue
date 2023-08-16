<script setup>
import { ref } from 'vue'
const projects = ref([
	{
		name: "RainManGO/vue3-composition-admin",
		main: "Nodejs",
		content: "这是一个简易的线上聊天室项目"
	},
	{
		name: "jeecgboot/jeecgboot-vue3",
		main: "Flask",
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
					<div class="projecttop">
						<div class="projectinfo">
							<div class="projectusericonbox">
								<img src="https://avatars.githubusercontent.com/u/96218937?s=96&v=4" alt="User Icon"
									class="projectusericon">
							</div>
							<div class="projectnamebox">
								<span class="projectname">{{ project.name }}</span>
							</div>
						</div>
						<h2>{{ project.main }}</h2>
						<h3>{{ project.content }}</h3>
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
}

.projectinfo {
	display: flex;
	flex: 1;
}

.projectstar {
	width: 80px;
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
</style>