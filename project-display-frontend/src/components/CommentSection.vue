<template>
  <div class="borderbox">
    <div style="padding-right: 60px;"><el-divider style="margin:0 0 0 60px;"/></div>
    <div class="commentbox">
      <div class="usericon">
        <img :src="comment.usericon" alt="" class="usericonimg" referrerpolicy="no-referrer">
      </div>
      <div class="mainbox">
        <div>{{ comment.nickname }}</div>
        <div class="commentcontent">{{ comment.content }}</div>
        <div class="commentabout">{{ comment.time }}
          <el-divider direction="vertical" />
          {{ comment.position }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.borderbox:hover {
  background-color: #fcfcfc;
}

.kindicon {
  font-size: 13px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Font Awesome 6 Free";
  font-weight: 600;
}

.commentabout {
  font-size: 12px;
  color: #666666;
  display: flex;
  align-items: center;
}

.commentcontent {
  margin: 6px 0;
  color: #555555;
}

.mainbox {
  margin-left: 10px;
  color: #333;
}

.commentbox {
  display: flex;
  padding: 10px 6px;
}

.usericon {
  min-width: 40px;
  max-width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.usericonimg {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>