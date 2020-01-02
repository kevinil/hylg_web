<template>

    <div id="app">
        <div class="headerWrapper">
            <header class="header">
                <div class="container">




                    <div class="nav">
<!--                        <div class="logo">-->
<!--                            <img class="nav-logo" width="40px" alt="Vue logo" src="./assets/logo.png">-->
<!--                        </div>-->
<!--                        <div class="nav-item">-->
<!--                            <i class="el-icon-switch-button"></i>-->
<!--                            <span slot="title">列表项</span>-->
<!--                        </div>-->


                        <el-menu :default-active="activeNav" router class="el-menu" mode="horizontal"
                                 @select="handleSelect" background-color="#222831" text-color="white" active-text-color="#00adb5">
                            <el-menu-item class="el-menu-item" index="/index">
                                <img class="nav-logo" width="40px" alt="Vue logo" src="./assets/logoBlack.png">
                            </el-menu-item>
                            <el-menu-item class="el-menu-item bold-item" index="/case">
                                <i class="el-icon-s-data"></i>
                                数据分析
                            </el-menu-item>
                            <el-menu-item class="el-menu-item bold-item" index="/data">
                                <i class="el-icon-menu"></i>
                                原始数据
                            </el-menu-item>
                            <el-menu-item class="el-menu-item bold-item" index="/report">
                                <i class="el-icon-document-add"></i>
                                <span slot="title">定制报表</span>
                            </el-menu-item>
                            <el-menu-item class="el-menu-item bold-item" index="/clue">
                                <i class="el-icon-position"></i>
                                <span slot="title">提交线索</span>
                            </el-menu-item>
                            <el-menu-item class="el-menu-item bold-item" style="float: right;" index="/logout" >
                                    <span slot="title"
                                    style="border: 1px solid #e1e4e8!important;border-radius: 3px!important;padding: 8px;">
                                        退出登录</span>

                            </el-menu-item>
                            <el-menu-item class="el-menu-item bold-item" style="float: right" index="/account">
                                <i class="el-icon-user"></i>
                                <span slot="title">账号管理</span>
                            </el-menu-item>

                        </el-menu>
                    </div>
                </div>
                <div class="router-view">
                    <router-view/>
                </div>
            </header>
        </div>
    </div>

</template>

<script>


    export default {
        storeData: "",
        data() {
            return {
                activeNav: "/index",
            }
        },
        mounted() {
            // 导航高亮
            var _this = this
            var href = window.location.href
            href = href.split('/')[3]
            _this.activeNav = '/' + href
        },

        methods: {
            handleSelect(key) {
                switch (key) {
                    // case "index":
                    //     this.$router.push({path:'/index'});
                    //     break;
                    // case "case":
                    //     this.$router.push({path:'/case'});
                    //     break;
                    // case "data":
                    //     this.$router.push({path:'/data'});
                    //     break;
                    // case "report":
                    //     this.$router.push({path:'/report'});
                    //     break;
                    // case "clue":
                    //     this.$router.push({path:'/clue'});
                    //     break;
                    case "/logout":
                        console.log("log out here")
                        // window.open('/logout')
                        window.location.href = '/logout';

                        // this.$router.push({path:'/logout'});

                        // this.$axios.post('/logout/', JSON.stringify({ usrname: "kevin"})).then(res => {
                        //     console.log(res.data)
                        // });
                        // this.$router.push({path:'/logout'});
                        break;
                    default:
                        break;
                }
            }
        }
    }
</script>


<style>


    /*
        header
    */

    button, input, select, textarea {
        font-family: inherit;
        font-size: inherit;
        line-height: inherit;
        color: inherit;
    }

    ul {
        display: block;
        list-style-type: disc;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-inline-start: 40px;
    }

    .header .nav {
        /*float: right;*/
        display: block;
        height: 72px;
        line-height: 72px;
        background: transparent;
        padding: 0;
        margin: 0;
    }

    a {
        color: #409eff;
        text-decoration: none;
    }

    h1 {
        display: block;
        font-size: 2em;
        margin-block-start: 0.67em;
        margin-block-end: 0.67em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        font-weight: bold;
    }

    .container {
        /*width: 1140px;*/
        width:100%;
        padding: 0;
        margin: 0 auto;
    }

    .header {
        background-color: #fff;
        /*color: #fff;*/
        top: 0;
        left: 0;
        width: 100%;
        z-index: 100;
        position: relative;
    }


    header {
        display: block;
    }


    /*
        app
     */
    div {
        display: block;
    }

    #app {
        height: 100%;
    }

    /*.router-view {*/
    /*    background-color: #EEEEEE;*/
    /*}*/

    /*.container {*/
    /*    background-color: #222831;*/
    /*}*/

    /*.fade-nav {*/
    /*    height: 100%;*/
    /*    height: 80px;*/
    /*    line-height: 80px;*/
    /*    background: transparent;*/
    /*    padding: 0;*/
    /*    margin: 0;*/
    /*}*/

    .logo {

        float: left;
    }

    .nav-item {
        float: left;
    }

    .bold-item {
        font-weight: bold;
    }


</style>








