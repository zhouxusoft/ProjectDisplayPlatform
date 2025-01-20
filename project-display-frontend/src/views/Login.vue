<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { loginAPI } from '../api/api'

const router = useRouter()

const pageheight = ref(window.innerHeight)

/**
 * 根据当前页面高度判断是否显示底部信息
 */
const shouldDisplayBottom = () => {
  return pageheight.value >= 630
}

let usernameInput
let passwordInput

const login = () => {
  let username = usernameInput.value
  let password = passwordInput.value
  // console.log(username, password)
  if (username && password) {
    let data = {
      username: username,
      password: password
    }
    // 发送登录请求
    loginAPI(data).then(res => {
      if (res.success) {
        ElMessage({
          message: res.message,
          type: 'success',
          plain: true,
          offset: 9,
        })
        router.push({ path: '/' })
        usernameInput.value = ''
        passwordInput.value = ''
      } else {
        ElMessage({
          message: res.message,
          type: 'error',
          plain: true,
          offset: 9,
        })
      }
    }).catch(error => {
      ElMessage({
        message: '请求失败',
        type: 'error',
        plain: true,
        offset: 9,
      })
    })
  }
}



onMounted(() => {
  // 密码框小眼睛切换
  const passwords = document.querySelectorAll('.passwordBox')
  const logoButtons = document.querySelectorAll('.logoButton')
  for (let i = 0; i < logoButtons.length; i++) {
    logoButtons[i].onclick = function () {
      if (passwords[i].type === 'password') {
        passwords[i].setAttribute('type', 'text')
        logoButtons[i].classList.add('hide')
      }
      else {
        passwords[i].setAttribute('type', 'password')
        logoButtons[i].classList.remove('hide')
      }
    }
  }

  const msg = document.getElementsByClassName("msg")[0]
  const from = document.getElementsByClassName("from")[0]
  // 获取每日一言
  const xhr = new XMLHttpRequest()
  xhr.open('POST', 'https://v1.hitokoto.cn/', false)
  xhr.send()
  const resData = JSON.parse(xhr.responseText)
  let datamsg = resData.hitokoto
  let datafrom = '—— 「 ' + resData.from + ' 」'
  // 修改每日一言内容
  msg.textContent = datamsg
  from.textContent = datafrom

  window.addEventListener('resize', () => {
    pageheight.value = window.innerHeight
    // console.log(pageheight.value >= 630)
  })

  usernameInput = document.getElementById("usernameInput")
  passwordInput = document.getElementById("passwordInput")
})
</script>

<template>
  <div class="container">
    <div class="borderbox">
      <div class="ltop top">
        <a href="#/">GodxuHub 登录</a>
      </div>
      <div class="hr"></div>
      <div class="box">
        <div class="inputBox">
          <input type="text" id="usernameInput" class="nameBox" placeholder="用户名">
        </div>
        <div class="inputBox">
          <input type="password" id="passwordInput" class="passwordBox" placeholder="密码">
          <span class="logoButton"></span>
        </div>
        <div class="btnbox">
          <button @click="login()" type="submit" class="sbtn" id="loginbtn">确认登录</button>
          <button type="button" class="sbtn" onclick="location='#/register'">前往注册</button>
        </div>
      </div>
      <div class="hr"></div>
      <div class="godxu">
        <div class="msg">
          用代码表达言语的魅力，用代码书写山河的壮丽。
        </div>
        <div class="from">
          ——「 一言开发者中心 」
        </div>
      </div>
    </div>
    <div class="sbottom" v-show="shouldDisplayBottom()">
      <div class="about">
        <div class="code">
          <img referrerPolicy="no-referrer" class="erweicodeimg"
            src="https://p.ananas.chaoxing.com/star3/origin/64788dea4b89070135e7a13dda096b4f.png" alt="">
        </div>
        <img referrerPolicy="no-referrer"
          src="https://p.ananas.chaoxing.com/star3/origin/835444af1e238fbd95acd92723451c95.png" alt=""
          class="icon vcode">
      </div>
      <div class="about">
        <div class="code">
          <img referrerPolicy="no-referrer" class="erweicodeimg"
            src="https://p.ananas.chaoxing.com/star3/origin/6e967dd18a4198bd62f20f79c373ce6a.png" alt="">
        </div>
        <img referrerPolicy="no-referrer"
          src="https://p.ananas.chaoxing.com/star3/origin/217a4ae91d62e76707716d614eb38c31.png" alt=""
          class="icon vcode">
      </div>
      <div>友情链接：
        <a href="https://www.iuroc.com/" class="yqlj" target="_blank">Iuroc-爱优鹏</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 80px;
  height: 80vh;
}

.borderbox {
  position: relative;
  top: -100px;
  min-height: 323px;
  background-color: white;
  width: fit-content;
  margin: auto;
}

.hr {
  margin: 10px 4px;
  border: none;
  border-top: 1px solid #20252c;
  transform: scaleY(0.5);
}

.ltop {
  margin: auto;
  padding: 5px;
  font-size: 24px;
  width: 300px;
  border-radius: 0.25rem;
  text-align: center;
  border: 1px solid #20252c;
}

.top a {
  display: inline-block;
  position: relative;
  text-decoration: none;
  padding: 8px;
  transition: 0.5s;
  color: black;
}

.top a:after {
  position: absolute;
  right: -15px;
  content: '»';
  opacity: 0;
  transition: 0.5s;
}

.top:hover a {
  padding-right: 30px;
}

.top:hover a:after {
  opacity: 1;
  right: 0;
}

.box {
  position: relative;
  width: 300px;
}

.box .inputBox {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  padding: 5px;
  border-radius: 0.25rem;
  margin-bottom: 12px;
  border: 1px solid #20252c;
}

.box .nameBox {
  font-size: 16px;
  flex: 1;
  outline: none;
  border: none;
  padding: 5px;
  font-weight: normal;
  color: #333;
}

.box .passwordBox {
  font-size: 16px;
  flex: 1;
  outline: none;
  border: none;
  padding: 5px;
  font-weight: normal;
  color: #333;
}

.box .logoButton {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
}

.box .logoButton::before {
  content: "\f06e";
  font-size: 16px;
  font-family: fontAwesome;
}

.box .hide::before {
  content: "\f070";
  font-family: fontAwesome;
}

.btnbox {
  display: flex;
  justify-content: space-between;
}

.sbtn {
  border-radius: 0.25rem;
  font-size: 16px;
  border: 1px solid #20252c;
  width: 120px;
  position: relative;
  text-decoration: none;
  padding: 8px;
  transition: 0.3s;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.sbtn:after {
  font-size: 18px;
  position: absolute;
  right: 10px;
  content: '»';
  opacity: 0;
  transition: 0.3s;
}

.sbtn:hover {
  padding-right: 15px;
}

.sbtn:hover:after {
  opacity: 1;
  right: 14px;
}

.godxu {
  width: 300px;
  border: 1px solid #20252c;
  border-radius: 0.25rem;
  padding: 5px;
  color: #20252c;
}

.msg {
  min-height: 42px;
  user-select: text;
}

.from {
  text-align: right;
  user-select: text;
}

.sbottom {
  position: absolute;
  bottom: 10px;
  text-align: center;
  margin: 0 57px;
  transition: 0.5s;
}

.sbottom .about {
  display: inline-block;
  border-radius: 0.25rem;
  transition: 0.3s;
  margin-bottom: 10px;
  border: 1px solid white;
}

.sbottom .about .icon {
  margin: 0 10px;
  background-color: white;
  border-radius: 50%;
  transition: 0.3s;
  padding: 1px;
}

.sbottom .about .code {
  border-radius: 0.25rem;
  padding-top: 5px;
  transition: 0.3s;
}

.sbottom .about:hover {
  background-color: white;
  border: 1px solid black;
}

.vcode {
  width: 40px;
}

.sbottom .about .code .erweicodeimg {
  width: 0px;
  transition: 0.3s;
}

.sbottom .about:hover .code .erweicodeimg {
  width: 100px;
}

.sbottom .about:hover .icon {
  margin: 0 35px;
}

.yqlj {
  color: black;
  text-decoration-line: none;
}

.yqlj:hover {
  text-decoration-line: underline;
}

.hidden {
  z-index: 5;
}

/*用于消除edge密码框的默认小眼睛*/
input[type="password"]::-ms-reveal {
  display: none;
}

input[type="password"]::-ms-clear {
  display: none;
}

input[type="password"]::-o-clear {
  display: none;
}
</style>