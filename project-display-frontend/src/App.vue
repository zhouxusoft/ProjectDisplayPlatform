<script setup>
import { onMounted, defineProps, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps()
//当前所处的路由
const currentroute = ref('/')

onMounted(() => {
	const router = useRouter()
	const homelink = document.getElementById("homelink")
	const projectslink = document.getElementById("projectslink")
	const aboutlink = document.getElementById("aboutlink")
	/** 刷新路由时，激活对应的导航显示状态 */
	router.afterEach((to, from) => {
		currentroute.value = to.path
		console.log(currentroute.value)
		if (to.path === '/') {
			homelink.classList.add('activelink')
			projectslink.classList.remove('activelink')
			aboutlink.classList.remove('activelink')
		} else if (to.path === '/projects') {
			homelink.classList.remove('activelink')
			projectslink.classList.add('activelink')
			aboutlink.classList.remove('activelink')
		} else if (to.path === '/about') {
			homelink.classList.remove('activelink')
			projectslink.classList.remove('activelink')
			aboutlink.classList.add('activelink')
		}
	})
})
</script>

<template>
	<nav class="navbar navbar-expand-lg bg-body-tertiary navborder mb-2">
		<div class="container-fluid">
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
				aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<a class="navbar-brand py-2" href="https://godxu.top" target="_blank"><img src="../public/hublogo.jfif" alt=""
					class="logoimg"></a>
			<div class="collapse navbar-collapse" id="navbarTogglerDemo03">
				<ul class="navbar-nav me-auto mb-2 mb-lg-0"
					v-show="currentroute != '/login' && currentroute != '/register'">
					<li class="nav-item px-2 pt-3" id="homelink">
						<a class="nav-link" aria-current="page" href="#">Home</a>
					</li>
					<li class="nav-item px-2 pt-3" id="projectslink">
						<a class="nav-link" href="#/projects">Projects</a>
					</li>
					<li class="nav-item px-2 pt-3" id="aboutlink">
						<a class="nav-link" href="#/about">About</a>
					</li>
				</ul>
				<form class="d-flex p-2" role="search">
					<input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
						v-show="currentroute != '/login' && currentroute != '/register'">
					<button class="btn btn-outline-success" type="submit"
						v-show="currentroute != '/login' && currentroute != '/register'">Search</button>
				</form>
			</div>
		</div>
	</nav>
	<router-view></router-view>
</template>

<style scoped>
.logoimg {
	width: 300px;
}

.navborder {
	padding: 0;
	background-color: #fff !important;
	box-shadow: inset 0 -1px #888888;
}

.nav-item {
	width: 100px;
}

.nav-link {
	margin: auto;
	width: fit-content;
}

.activelink {
	border-bottom: 2px solid orangered;
	font-weight: bold;
}

.btn:focus {
	box-shadow: none !important;
}

.navbar-toggler:focus {
	box-shadow: none !important;
}</style>
