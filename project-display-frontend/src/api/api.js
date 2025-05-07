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

// 获取圈子列表
export function circleListAPI(data) {
  return api.post('/circleList', data)
}

// 获取用户列表
export function userListAPI(data) {
  return api.post('/userList', data)
}

// 关注/取消关注用户
export function followUserAPI(data) {
  return api.post('/followUser', data)
}

// 获取圈子详细信息
export function circleDetailAPI(data) {
  return api.post('/circleDetail', data)
}

// 获取我的详细信息
export function myInfoAPI(data) {
  return api.post('/myInfo', data)
}

// 获取用户个人信息
export function userInfoAPI(data) {
  return api.post('/userInfo', data)
}

// 获取用户点赞列表
export function userStarredAPI(data) {
  return api.post('/userStarred', data)
}

// 获取用户点赞列表
export function starredListAPI(data) {
  return api.post('/starredList', data)
}

// 上传图片
export function uploadImageAPI(data) {
  return api.post('/uploadImage', data)
}

// 发布文章
export function createProjectAPI(data) {
  return api.post('/createProject', data)
}

// 点赞文章
export function starProjectAPI(data) {
  return api.post('/starProject', data)
}

// 更新用户信息
export function updateProfileAPI(data) {
  return api.post('/updateProfile', data)
}

// 创建圈子
export function createCircleAPI(data) {
  return api.post('/createCircle', data)
}