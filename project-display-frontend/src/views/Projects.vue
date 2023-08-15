<script setup>
import { ref } from 'vue'
const projects = ref([
	{
		name: "Godxu聊天室",
		main: "Nodejs",
		content: "这是一个简易的线上聊天室项目"
	},
	{
		name: "Godxu云盘",
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
		name: "Godxu字体库",
		main: "Flask",
		content: "这是一个字体库预览及下载项目"
	})
}
</script>

<template>
	<div class="">
		<div class="borderbox">
			<div class="leftnav d-none d-md-block p-2">
				zsss
			</div>
			<div class="mainprojects p-2">
				<div v-for="project in projects" class="projectdata m-2 p-2">
					<h1 class="text-primary">{{ project.name }}</h1>
					<h2>{{ project.main }}</h2>
					<h3>{{ project.content }}</h3>
				</div>
				<button class="btn btn-success" @click="clickbtn()">add</button>
			</div>
			<div class="rightnav d-none d-lg-block p-2">
				zsss
			</div>
		</div>
	</div>
</template>

<style scoped>
.borderbox {
	display: flex;
	justify-content: space-between;
}

.leftnav {
	position: sticky;
	max-height: 100vh;
	top: 0;
	width: 270px;
	box-shadow: inset -1px 0 #666666;
}

.mainprojects {
	flex: 1;
}

.rightnav {
	width: 270px;
}

.projectdata {
	border: 1px solid #666666;
	border-radius: 6px;
}
</style>