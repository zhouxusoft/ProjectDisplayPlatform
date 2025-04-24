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

// 获取项目信息
export function projectsAPI(data) {
  return api.post('/projects', data)
}

// 获取展示类型数据
export function kindsAPI() {
  return api.get('/kinds', {})
}

// 获取语言种类数据
export function languagesAPI() {
  return api.get('/languages', {})
}

// 获取标签数据
export function tagsAPI() {
  return api.get('/tags', {})
}

// 获取项目详情数据
export function projectDetailAPI(data) {
  return api.post('/projectDetail', data)
}

// 获取项目的评论数据
export function projectCommentsAPI(data) {
  return api.post('/projectComments', data)
}

// 发表评论
export function userCommentAPI(data) {
  return api.post('/userComment', data)
}