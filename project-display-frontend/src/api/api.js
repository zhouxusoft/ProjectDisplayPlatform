import api from '@/utils/request'

// 校验登录状态
export function checkLoginAPI() {
  return api.post('/checkLogin', {})
}

// 退出登录
export function clearCookieAPI() {
  return api.post('/clearCookie', {})
}

// 登录
export function loginAPI(data) {
  return api.post('/login', data)
}

// 注册
export function registerAPI(data) {
  return api.post('/register', data)
}