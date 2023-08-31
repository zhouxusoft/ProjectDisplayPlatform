<template>
    <a class="kinditem" :key="kind.id" :class="{ kinditemactive: kind.isactive }">
        <span class="kindicon" v-html="kind.icon"></span>
        <span class="kindname">{{ kind.name }}</span>
    </a>
</template>

<script>
export default {
    props: {
        kind: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped>
.kinditem {
    position: relative;
    text-decoration: none;
    padding: 6px 8px;
    margin: 0 8px;
    display: flex;
    flex-grow: 1;
    border-radius: 6px;
    color: #0E1116;
    cursor: pointer;
}

.kinditemactive {
    background-color: rgb(206, 213, 220);
}

.kinditemactive::after {
    position: absolute;
    top: calc(50% - 12px);
    left: -8px;
    width: 4px;
    height: 24px;
    content: "";
    background-color: rgb(3, 73, 180);
    border-radius: 6px;
}

.kinditem:hover {
    background-color: rgb(231, 236, 240);
}

.kindicon {
    font-size: 14px;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 8px;
    font-family: "Font Awesome 6 Free";
    font-weight: 600;
}

.kindname {
    font-size: 14px;
    height: 20px;
}
</style>