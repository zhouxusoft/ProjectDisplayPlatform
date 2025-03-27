<script setup>
import { onMounted, ref } from 'vue'
// 声明接收路由参数
const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

// 使用示例
onMounted(() => {
})
</script>

<template>
  <div>当前项目ID: {{ id }}</div>
</template>