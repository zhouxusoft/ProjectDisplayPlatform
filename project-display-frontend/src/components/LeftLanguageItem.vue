<template>
    <div class="languageitembox" :class="{ languageitemactive: language.isactive }">
        <div class="languageitemicon" :style="{ backgroundColor: '#' + language.color }"></div>
        <div class="languageitemname">{{ language.name }}</div>
    </div>
</template>

<script>
export default {
    props: {
        language: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped>
.languageitembox {
    display: flex;
    white-space: nowrap;
    align-items: center;
    padding: 6px 8px;
    margin: 0 8px;
    border-radius: 6px;
    color: #0E1116;
    cursor: pointer;
}

.languageitemicon {
    border-radius: 8px;
    border-style: solid;
    border-width: 1px;
    border-color: rgba(1, 4, 9, 0.1);
    width: 10px;
    height: 10px;
    margin: 5px;
}

.languageitemname {
    font-size: 14px;
    height: 20px;
    margin: 0 6px;
}

.languageitembox:hover {
    background-color: rgb(231, 236, 240);
}

.languageitemactive {
    background-color: rgb(206, 213, 220) !important;
}
</style>