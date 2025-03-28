<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { registerAPI } from '../api/api'

const router = useRouter()

let userLengthCase
let lengthCase
let recheckCase
let rbtn
let pwd
let rpwd
let userNameOK = ref(0)
let checkPasswordOK = ref(0)
let recheckPasswordOK = ref(0)

let usernameInput
let passwordInput
let rpasswordInput

/**
 * 检查所有用户输入是否合法
 */
function inputOK() {
  if (userNameOK.value === 1 && checkPasswordOK.value === 1 && recheckPasswordOK.value === 1) {
    rbtn.disabled = false
    rbtn.classList.remove('default')
    rbtn.classList.add('sbtn')
  } else {
    rbtn.disabled = true
    rbtn.classList.remove('sbtn')
    rbtn.classList.add('default')
  }
}

/**
 * 判断字符串是否包含空白符
 * @param {*} str 
 */
function hasWhiteSpace(str) {
  return /\s/g.test(str)
}

/**
 * 判断用户名是否合法
 * @param {string} data 
 */
function checkUserName(data) {
  const length = new RegExp('(^.{1,12}$)')

  if (length.test(data) && !hasWhiteSpace(data)) {
    userLengthCase.classList.add('valid')
    userNameOK.value = 1
  } else {
    userLengthCase.classList.remove('valid')
    userNameOK.value = 0
  }

  inputOK()
}

/**
 * 判断密码是否合法
 * @param {string} data 
 */
function checkPassword(data) {
  pwd = data

  const length = new RegExp('(?=.{6,})')

  if (length.test(data) && !hasWhiteSpace(data)) {
    lengthCase.classList.add('valid')
    checkPasswordOK.value = 1
  } else {
    lengthCase.classList.remove('valid')
    checkPasswordOK.value = 0
  }

  recheckPassword(rpwd)

  inputOK()
}

/**
 * 判断两次密码是否一致
 * @param {string} data 
 */
function recheckPassword(data) {
  rpwd = data

  if (data === '') {
    recheckCase.classList.remove('valid')
  } else if (data === pwd) {
    recheckCase.classList.add('valid')
    recheckPasswordOK.value = 1
  } else {
    recheckCase.classList.remove('valid')
    recheckPasswordOK.value = 0
  }

  inputOK()
}

/**
 * 向后端发送注册请求
 */
const register = () => {
  let username = usernameInput.value
  let password = passwordInput.value
  let repassword = rpasswordInput.value

  let toSend = {
    username: username,
    password: password,
    repassword: repassword
  }
  // 发送注册请求
  registerAPI(toSend).then(res => {
    if (res.success) {
      // 注册成功
      ElMessage({
        message: res.message,
        type: 'success',
        plain: true,
        offset: 9,
      })
      router.push({ path: '/login' })
    } else {
      // 注册失败, 将输入判断还原
      pwd = ''
      rpwd = ''
      usernameInput.value = ''
      passwordInput.value = ''
      rpasswordInput.value = ''
      userNameOK.value = 0
      checkPasswordOK.value = 0
      recheckPasswordOK.value = 0
      userLengthCase.classList.remove('valid')
      lengthCase.classList.remove('valid')
      recheckCase.classList.remove('valid')
      inputOK()
      ElMessage({
        message: res.message,
        type: 'error',
        plain: true,
        offset: 9,
      })
    }
  }).catch(error => {
    ElMessage({
      message: '请求失败，请稍后再试',
      type: 'error',
      plain: true,
      offset: 9,
    })
  })
}

onMounted(() => {
  userLengthCase = document.getElementById('nameLength')
  lengthCase = document.getElementById('length')
  recheckCase = document.getElementById('recheck')
  rbtn = document.getElementById('registerbtn')

  usernameInput = document.getElementById("usernameInput")
  passwordInput = document.getElementById("passwordInput")
  rpasswordInput = document.getElementById("rpasswordInput")

  const passwords = document.querySelectorAll('.passwordBox')
  const logoButtons = document.querySelectorAll('.logoButton')

  for (let i = 0; i < logoButtons.length; i++) {
    logoButtons[i].onclick = function () {
      if (passwords[i].type === 'password') {
        passwords[i].setAttribute('type', 'text')
        logoButtons[i].classList.add('hide')
      } else {
        passwords[i].setAttribute('type', 'password')
        logoButtons[i].classList.remove('hide')
      }
    }
  }
})
</script>
<template>
  <div class="container">
    <div class="borderbox">
      <div class="rtop top">
        <a href="/">GodxuHub 注册</a>
      </div>
      <div class="hr"></div>
      <div class="box">
        <div class="inputBox">
          <input type="text" class="nameBox" id="usernameInput" placeholder="用户名" autocomplete="off"
            @keyup="checkUserName($event.target.value)">
        </div>
        <div class="inputBox">
          <input type="password" class="passwordBox" id="passwordInput" placeholder="密码"
            @keyup="checkPassword($event.target.value)">
          <span class="logoButton"></span>
        </div>
        <div class="checkBox">
          <input type="password" class="passwordBox" id="rpasswordInput" placeholder="确认密码"
            @keyup="recheckPassword($event.target.value)">
          <span class="logoButton"></span>
        </div>
        <div class="validation">
          <ul>
            <li id="nameLength">用户名不能过短或过长</li>
            <li id="length">密码长度至少为6</li>
            <li id="recheck">两次输入密码一致</li>
          </ul>
        </div>
        <div class="btnbox">
          <button @click="register()" type="submit" class="default" id="registerbtn">
            确认注册
          </button>
          <button type="button" class="sbtn" onclick="location='/login'">
            返回登录
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

.borderbox {
  position: relative;
  top: -20px;
  min-height: 323px;
  background-color: white;
  width: fit-content;
  margin: auto;
}

.hr {
  margin: 10px 2px;
  border: none;
  border-top: 1px solid #20252c;
  transform: scaleY(0.5);
}

.rtop {
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
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  text-decoration: none;
  padding: 8px;
  transition: 0.3s;
  background-color: white;
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

.validation {
  padding: 20px;
  border-radius: 0.25rem;
  margin-bottom: 10px;
  border: 1px solid #20252c;
}

.validation ul {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0;
  margin: 0;
}

.validation ul li {
  position: relative;
  font-size: 16px;
  font-weight: lighter;
  list-style: none;
  transition: 0.3s;
}

.validation ul li.valid {
  color: #0349b4;
}

.validation ul li::before {
  content: "\f192";
  font-family: fontAwesome;
  width: 22px;
  display: inline-flex;
}

.validation ul li.valid::before {
  content: "\f00c";
  font-family: fontAwesome;
  transition: 0.1s;
}

.default {
  cursor: not-allowed;
  background-color: white;
  color: black;
  border-radius: 0.25rem;
  font-size: 16px;
  border: none;
  width: 120px;
  display: inline-block;
  position: relative;
  text-decoration: none;
  padding: 8px;
  transition: 0.5s;
  border: 1px solid #20252c;
}

.box .checkBox {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  padding: 5px;
  border-radius: 0.25rem;
  margin-bottom: 12px;
  border: 1px solid #20252c;
  font-weight: normal;
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