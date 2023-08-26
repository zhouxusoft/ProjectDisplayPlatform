<template>
    <div class="projectdata p-3">
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
				<div class="projectstar d-none d-sm-flex">
					<button class="starfontbtn"><span class="starfont">&#xf005</span>Star</button>
				</div>
			</div>
</template>

<script>
export default {
  props: {
    project: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
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
	width: 72px;
	display: flex;
	justify-content: flex-end;
}

.starfont {
	font-family: "Font Awesome 6 Free";
	font-weight: 300;
	margin-right: 4px;
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