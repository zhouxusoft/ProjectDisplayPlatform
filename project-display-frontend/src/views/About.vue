<template>
    <h1 class="font-success">这是关于页</h1>
    <button @click="requestBtn">请求</button>
</template>

<script setup>
import { getInfo } from './qingqiu.js'
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'

const router = useRouter()

const requestBtn = () => {
    getInfo().then(res => {
        console.log(res)
    })
}
</script>