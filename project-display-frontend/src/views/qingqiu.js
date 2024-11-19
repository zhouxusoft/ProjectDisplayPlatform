import request from "./request"

export function getInfo() {
  return request({
    url: '/captchaImage',
    method: 'get',
  })
}