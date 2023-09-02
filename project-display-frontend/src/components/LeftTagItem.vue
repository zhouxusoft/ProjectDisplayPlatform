<template>
    <div class="tagitembox" :class="{ tagitemactive: tag.isactive }">
        <div class="tagitemname">{{ tag.name }}</div>
    </div>
</template>

<script>
export default {
    props: {
        tag: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped>
.tagitembox {
    user-select: none;
    padding: 3px 8px;   
    border-radius: 6px;
    cursor: pointer;
    color: rgb(3, 73, 180);
    font-size: 13px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.tagitembox:hover {
    background-color: rgb(223, 247, 255);
}

.tagitemactive {
    background-color: rgb(11, 83, 192) !important;
    color: rgb(255, 255, 255) !important;
}
</style>