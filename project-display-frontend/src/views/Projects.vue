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
	function clickbtn() {
		projects.value.push({
			name: "Godxu字体库",
			main: "Flask",
			content: "这是一个字体库预览及下载项目"
		})
	}
</script>

<template>
	<div v-for="project in projects">
		<h1 class="text-primary">{{ project.name }}</h1>
		<h2>{{ project.main }}</h2>
		<h3>{{ project.content }}</h3>
	</div>
	<button class="btn btn-success" @click="clickbtn()">add</button>
	<router-view></router-view>
</template>