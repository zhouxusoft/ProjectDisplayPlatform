<template>
  <div class="userbox">
    <div class="useravatar"><img :src="user.usericon" alt="" style="width: 80px;" referrerpolicy="no-referrer"></div>
    <div class="userinfo" @click="toUserDetail(user.user_id)">
      <div style="font-weight: 700;">{{ user.nickname }}</div>
      <div style="color: #333333; margin-top: 4px;">{{ user.bio || '这个人很神秘，什么都没有写' }}</div>
      <div style="color: #333333; margin-top: 4px; font-size: 14px; display: flex; align-items: center;"><span
          class="kindicon" style="font-size: 14px">&#xf0c0</span>粉丝：{{ user.follower_num
          }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 14px">&#xf06e</span>关注：{{
          user.following_num }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 14px">&#xf1ea</span>作品：{{
          user.projects_num }}</div>
    </div>
    <div>
      <div class="projectstar d-none d-sm-flex">
        <button class="starfontbtn" v-if="user.flag == 0" @click="userFollow(user.user_id)">
          <span class="starfont">&#xf005</span>
          关注
        </button>
        <button class="starfontbtn" v-if="user.flag == 1" @click="userFollow(user.user_id)">
          <span class="starfont">&#xf004</span>
          回关
        </button>
        <button class="starfontbtn" v-if="user.flag == 2" @click="userFollow(user.user_id)">
          <span class="starredfont">&#xf00c</span>
          已关注
        </button>
        <button class="starfontbtn" v-if="user.flag == 3" @click="userFollow(user.user_id)">
          <span class="starredfont">&#xf0c1</span>
          已互粉
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { followUserAPI } from '@/api/api.js'
export default {
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
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
    userFollow(userid) {
      followUserAPI({userid: userid})
        .then((response) => {
          if (response.code == 200) {
            this.$emit('updateUser', userid)
            ElMessage({
              message: response.message,
              type: 'success',
              plain: true,
              offset: 9,
            })
          } else {
            ElMessage({
              message: '操作失败',
              type: 'error',
              plain: true,
              offset: 9,
            })
          }
        })
        .catch((error) => {
          console.error(error)
          ElMessage({
            message: '网络错误，请稍后再试',
            type: 'error',
            plain: true,
            offset: 9,
          })
        })
    },
    handleImageError(event) {
      // 检查当前src是否已经是默认图片，避免无限循环
      if (!event.target.src.endsWith('/error_img.png')) {
        this.imgUrl = '/error_img.png'
      }
    },
    toUserDetail(userid) {
      this.$router.push({ path: `/user/${userid}` })
    }
  },

  created() {
    this.userFollow = this.debounce(this.userFollow, 1000, true)
  }
}
</script>

<style lang="scss" scoped>
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
}

.userbox {
  border: 1px solid black;
  border-radius: 4px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  cursor: pointer;
}

.userbox:hover {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12);
  background-color: #FDFDFD;
}

.useravatar {
  border-radius: 50%;
  overflow: hidden;
  height: 80px;
  min-width: 80px;
  margin-right: 16px;
}

.userinfo {
  width: 100%;
}

.kindicon {
  font-size: 13px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 4px;
  font-family: "Font Awesome 6 Free";
  font-weight: 600;
  color: #555555;
}
</style>