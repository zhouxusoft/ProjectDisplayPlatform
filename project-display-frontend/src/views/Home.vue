<template>
    <div class="container">
        <div class="notloginbox">
            <img src="../../public/你还未登录哦.png" alt="" class="notloginimg img-fluid">
            <div class="notlogincontent mb-3">你还未登录哦</div>
            <div class="notloginbtngroup">
                <button class="btn btn-outline-success m-1 notloginbtn">去登录</button>
                <button class="btn btn-outline-primary m-1 notloginbtn">去注册</button>
            </div>
        </div>
    </div>
</template>

<script>

</script>

<style scoped>
    .notloginbox {
        width: fit-content;
        margin: auto;
    }
    
    .notloginimg {
        width: 480px;
    }

    .notlogincontent {
        margin: auto;
        width: fit-content;
        font-size: 1.5rem;
        color: #002d80;
    }

    .notloginbtngroup {
        width: fit-content;
        margin: auto;
    }

    .notloginbtn {
        width: 120px;
    }
</style>