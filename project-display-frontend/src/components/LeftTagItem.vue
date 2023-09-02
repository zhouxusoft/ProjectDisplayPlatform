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
    padding: 2px 5px;   
    border-radius: 8px;
    cursor: pointer;
}

.tagitemname {
    font-size: 14px;
    margin: 0 6px;
    color: rgb(3, 73, 180);
}

.tagitembox:hover {
    background-color: rgb(223, 247, 255);
}

.tagitemactive {
    background-color: rgb(3, 73, 180) !important;
    color: #FFFFFF;
}
</style>