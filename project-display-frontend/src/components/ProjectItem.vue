<template>
	<div class="projectdata p-3">
		<div class="project_img_box_border d-none d-lg-block" v-if="project.cover">
			<div class="project_img_box">
				<img :src="imgUrl" alt="图片加载失败" class="project_img" style="width: 160px;" @error="handleImageError" referrerpolicy="no-referrer">
			</div>
		</div>
		<div class="projectinfo">
			<div class="projecttop">
				<div class="projectusericonbox">
					<img :src="project.usericon" alt="User Icon" class="projectusericon">
				</div>
				<div class="projectnamebox" @click="toProjectDetail(project.pagename)">
					<span class="projectname">{{ project.name }}</span>
				</div>
			</div>
			<div class="projectoverview">
				<span>{{ project.main }}</span>
			</div>
			<div class="projecttagbox my-2">
				<a v-for="tag in project.tags" class="projecttag">{{ tag }}</a>
			</div>
			<div class="projectbottom">
				<div class="projectlanguagebox">
					<div class="projectlanguageicon" :style="{ backgroundColor: '#' + project.language.color }"></div>
					<div class="projectlanguage">{{ project.language.name }}</div>
				</div>
				<span class="mx-2">·</span>
				<div><span class="starfont">&#xf005</span>{{ project.starnum }}</div>
				<span class="mx-2">·</span>
				<div class="projectupdatetime">Updated on {{ project.updatetime }}</div>
			</div>
		</div>
		<div class="projectstar d-none d-sm-flex">
			<button class="starfontbtn" v-if="!isStared(project.id)" @click="projectStar(1, project.id)">
				<span class="starfont">&#xf005</span>
				Star
			</button>
			<button class="starfontbtn" v-else @click="projectStar(0, project.id)">
				<span class="starredfont">&#xf005</span>
				Starred
			</button>
		</div>
	</div>
</template>

<script>
import { ElMessage } from 'element-plus'
export default {
	props: {
		project: {
			type: Object,
			required: true
		},
		starred: {
			type: Object,
			required: true
		},
	},
	data() {
		return {
			imgUrl: this.project.cover
		}
	},
	methods: {
		debounce(fn, delay, immediate = false) {
			let timer = null
			return function (...args) {
				const callNow = immediate && !timer
				if (timer) {
					// 在等待期间再次触发，弹出提示
					ElMessage({
						message: '手速太快了，休息一下吧',
						type: 'error',
						plain: true,
						offset: 9,
					})
				}
				clearTimeout(timer)
				timer = setTimeout(() => {
					timer = null
					if (!immediate) fn.apply(this, args)
				}, delay)
				if (callNow) fn.apply(this, args)
			}
		},
		isStared(projectid) {
			return this.starred.some((item) => item.projectid === projectid)
		},
		projectStar(type ,projectid) {
			if (type == 1) {
				this.starred.push({ id: this.starred.length + 1, projectid: projectid })
			} else {
				for (let i = 0; i < this.starred.length; i++) {
				if (this.starred[i].projectid == projectid) {
					this.starred.splice(i, 1)
					break
				}
			}
			}
		},
		handleImageError(event) {
			// 检查当前src是否已经是默认图片，避免无限循环
			if (!event.target.src.endsWith('/error_img.png')) {
				this.imgUrl = '/error_img.png'
			}
		},
		toProjectDetail(projectid) {
			this.$router.push({ path: `/projectDetail/${projectid}` })
		}
	},

	created() {
		this.projectStar = this.debounce(this.projectStar, 500, true)
	}
}
</script>

<style lang="scss" scoped>
.projectdata {
	border: 1px solid #666666;
	border-radius: 6px;
	display: flex;

	&:hover {
		box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12);
		background-color: #FDFDFD;
	}
}

.project_img_box_border {
	display: flex;
}

.project_img_box {
	width: 160px;
	height: 100px;
	margin-right: 16px;
	background-color: #F5F6F7;
	display: flex;
	align-items: center;
	overflow: hidden;
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
	width: 72px;
	display: flex;
	justify-content: flex-end;
}

.starfont {
	font-family: "Font Awesome 6 Free";
	font-weight: 300;
	margin-right: 4px;
}

.starredfont {
	font-family: "Font Awesome 6 Free";
	font-weight: 600;
	margin-right: 4px;
	color: #d5a824;
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
	overflow: hidden;
	max-width: 100%;
	font-size: 16px;
	font-weight: 600;
	color: rgb(3, 73, 180);
}

.projectoverview {
	margin-top: 4px;
	font-size: 14px;
	word-wrap: break-word;
	display: -webkit-box;
	/* 必须指定为块级元素 */
	-webkit-box-orient: vertical;
	/* 设置为垂直布局 */
	-webkit-line-clamp: 2;
	line-clamp: 2;
	/* 显示的行数 */
	overflow: hidden;
	/* 隐藏溢出的文本 */
}

.starfontbtn {
	border: 1px solid #666666;
	border-radius: 6px;
	font-size: 12px;
	height: 28px;
	padding: 0 8px;
	background-color: rgb(231, 236, 240);
	white-space: nowrap;
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
	white-space: nowrap;
}

.projectlanguageicon {
	border-radius: 8px;
	border-style: solid;
	border-width: 1px;
	border-color: rgba(1, 4, 9, 0.1);
	width: 10px;
	height: 10px;
	margin: 4px 4px 4px 0;
}
</style>