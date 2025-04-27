<template>
  <div class="userbox" @click="toCircleDetail(circle.id)">
    <div class="useravatar" style="border-radius: 0.25em;"><img :src="circle.cover" alt="" style="width: 80px;"
        referrerpolicy="no-referrer">
    </div>
    <div class="userinfo">
      <div style="font-weight: 700;">{{ circle.name }}</div>
      <div style="color: #333333; margin-top: 4px;">{{ circle.description }}</div>
      <div style="color: #333333; margin-top: 4px; font-size: 14px; display: flex; align-items: center;"><span
          class="kindicon" style="font-size: 14px">&#xf0c0</span>成员：{{ circle.member_count + 1
          }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 14px">&#xf06e</span>粉丝：{{
          circle.follower_count
        }}&nbsp;&nbsp;&nbsp;&nbsp;<span class="kindicon" style="font-size: 14px">&#xf1ea</span>作品：{{
          circle.project_count }}</div>
    </div>
    <div>
      <div class="projectstar d-none d-sm-flex">
        <button class="starfontbtn" v-if="circle.flag == 1">
          <span class="starfont">&#xf005</span>
          我创建的
        </button>
        <button class="starfontbtn" v-if="circle.flag == 2">
          <span class="starredfont">&#xf00c</span>
          我加入的
        </button>
        <button class="starfontbtn" v-if="circle.flag == 3">
          <span class="starfont">&#xf004</span>
          我关注的
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
export default {
  props: {
    circle: {
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
    toCircleDetail(circleid) {
      this.$router.push({ path: `/circle/${circleid}` })
    }
  },

  created() {
    this.projectStar = this.debounce(this.projectStar, 500, true)
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