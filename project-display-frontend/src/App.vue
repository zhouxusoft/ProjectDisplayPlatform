<script setup>
import { onMounted, ref} from 'vue'
import { useRouter } from 'vue-router'

//当前所处的路由
const currentroute = ref('/')
const isinputfocus = ref(false)
const searchKey = ref()
const showClear = ref(false)

// 当搜索框获得焦点时
const inputFocus = () => {
  isinputfocus.value = true
}
// 当搜索框失去焦点时
const inputBlur = () => {
  isinputfocus.value = false
}

const inputInput = () => {
	if (searchKey.value == '') {
		showClear.value = false
	} else {
		showClear.value = true
	}
	console.log(showClear.value)
}

const clearInput = () => {
	searchKey.value = ''
	showClear.value = false
	console.log(searchKey.value)
}

onMounted(() => {
	const router = useRouter()
	const homelink = document.getElementById("homelink")
	const projectslink = document.getElementById("projectslink")
	const aboutlink = document.getElementById("aboutlink")
	/** 刷新路由时，激活对应的导航显示状态 */
	router.afterEach((to, from) => {
		currentroute.value = to.path
		// console.log(currentroute.value)
		if (to.path === '/') {
			homelink.classList.add('activelink')
			projectslink.classList.remove('activelink')
			aboutlink.classList.remove('activelink')
		} else if (to.path === '/projects' || to.path.includes('projectDetail') || to.path.includes('circle') || to.path.includes('user')) {
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
	<nav class="navbar navbar-expand-lg bg-body-tertiary navborder">
		<div class="container-fluid">
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
				aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<a class="navbar-brand py-2" href="/" target="_blank"><img src="/hublogo.jfif" alt=""
					class="logoimg"></a>
			<div class="autobox d-none d-lg-block"></div>
			<div class="collapse navbar-collapse" id="navbarTogglerDemo03">
				<ul class="navbar-nav me-auto mb-2 mb-lg-0"
					v-show="currentroute != '/login' && currentroute != '/register' && currentroute != '/newProject' && currentroute != '/chat'">
					<li class="nav-item px-2 pt-3" id="homelink">
						<a class="nav-link" aria-current="page" href="/">Hello</a>
					</li>
					<li class="nav-item px-2 pt-3" id="projectslink">
						<a class="nav-link" href="/projects">World</a>
					</li>
					<li class="nav-item px-2 pt-3" id="aboutlink">
						<a class="nav-link" href="/about">Stars</a>
					</li>
				</ul>
				<div class="p-2" v-show="currentroute == '/projectsxxx'">
					<div class="searchinputbox d-flex me-1" :class="{ focused: isinputfocus }">
						<div class="form-control form-control-sm searchlogo"></div>
						<input class="form-control form-control-sm searchinput p-0" placeholder="Search"
							v-model="searchKey"
							aria-label="Search"
							@focus="inputFocus()"
      				@blur="inputBlur()"
							@input="inputInput()">
						<span class="clearbox">
							<span v-show="showClear" class="clear" @click="clearInput()">&#xf00d</span>
						</span>
						<button class="searchbutton" type="button"></button>
					</div>
				</div>
			</div>
		</div>
	</nav>
	<router-view></router-view>
</template>

<style scoped>
.logoimg {
	width: 194px;
}

.autobox {
	width: 8%;
}

.navborder {
	padding: 0;
	background-color: #fff !important;
	box-shadow: inset 0 -1px #666666;
	z-index: 999;
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
}

.searchlogo {
	width: 30px;
	border: none;
	border-radius: 0.25rem 0 0 0.25rem;
}

.searchinput {
	border: none;
	border-radius: 0 0.25rem 0.25rem 0;
}

.searchinput:focus {
	box-shadow: none !important;
}

.focused {
	outline: 1px solid #0349b4;	
}

.searchinputbox {
	border: 1px solid #727272;
	border-radius: 0.25rem;
}

.searchlogo::before {
	content: '\f002';
	font-family: 'Font Awesome 6 Free';
	font-weight: 600;
}

.searchbutton {
	border: none;
	border-radius: 0.25rem;
	background-color: white;
	width: 30px;
	height: 27px;
	margin: 2px;
}

.searchbutton:hover {
	background-color: #e7ecf0;
}

.searchbutton::before {
	content: '\f105';
	font-family: 'Font Awesome 6 Free';
	font-weight: 600;
}

.clear {
	font-family: 'Font Awesome 6 Free';
	font-weight: 600;
  	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 13px;
	width: 16px;
	height: 16px;
	margin: 8px 0;
	border-radius: 0.25rem;
}

.clearbox {
	width: 14px;
	height: 14px;
}

.clear:hover {
	background-color: white;
	background-color: #e7ecf0;
}
</style>
