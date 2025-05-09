// api.js
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,  // 设置默认的API地址
  timeout: 30000,  // 设置请求超时时间
})

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 在跨域请求中发送 cookies 和 http 认证信息
    config.withCredentials = true
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    const code = response.data.code || 200

    if (code == 401) {
      ElMessage({
        message: '登录已过期，请重新登录',
        type: 'warning',
        plain: true,
        offset: 9,
      })
      window.location.href = '/login'
    }

    return response.data
  },
  (error) => {
    // 对响应错误做处理
    let errorMsg = '请求失败'
    if (error.response) {
      // 服务器响应了状态码，但状态码不在2xx范围内
      errorMsg = error.response.data.message || '服务器错误'
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      errorMsg = '网络错误'
    }
    return Promise.reject(error)
  }
)

// 封装请求方法
const api = {
  get(url, params) {
    return instance.get(url, { params })
  },
  post(url, data) {
    return instance.post(url, data)
  },
}

export default api