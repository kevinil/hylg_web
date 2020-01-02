<template>
    <div id="index">
        <div class="main-cnt" >
            <div>
                <div class="banner">
                    <div class="banner-desc">
                        <h1>涉烟违法信息大数据分析平台</h1>
                        <p>多平台数据汇总，重塑案件预警分析系统</p>
                    </div>
                </div>
                <div class="jumbotron">
                    <img src="../assets/caseCloud.png" alt>
                </div>

<!--                <div class="sponsors">-->
<!--                    <a href="" target="_blank" class="sponsor">-->
<!--                        <img width="80px" src="../assets/bg.jpg" alt="hehe">-->
<!--                        <div>-->
<!--                            <p>华蓥市</p>-->
<!--                            <p>创新求变</p>-->
<!--                        </div>-->
<!--                    </a>-->
<!--                </div>-->
                <div class="cards">
                    <ul  class="container">
                        <li >
                            <div  class="card">
                                <img  src="../assets/fenxi.png" alt="">
                                <h3>数据分析</h3>
                                <p>了解案情趋势，数据变化，区域预测。</p>
                                <a href="/case/" class="">查看详情
                                </a>
                            </div>
                        </li>
                        <li>
                            <div class="card">
                                <img src="../assets/shuju.png" alt="">
                                <h3>原始数据</h3>
                                <p>以零售户为单位搭建数据网络。</p>
                                <a href="/data/" class="">查看详情
                                </a>
                            </div>
                        </li>
                        <li>
                            <div class="card">
                                <img src="../assets/baobiao.png" alt="">
                                <h3>报表定制</h3>
                                <p>查询平台数据，生成指定报表</p>
                                <a href="/report/" class="">查看详情
                                </a>
                            </div>
                        </li>
                        <li>
                            <div class="card">
                                <img src="../assets/xiansuo.png" alt="">
                                <h3>提交线索</h3>
                                <p>市场走访，数据留存。</p>
                                <a href="/clue/" class="">查看详情
                                </a>
                            </div>
                        </li>

                    </ul>
                </div>

            </div>
        </div>
        <footer class="footer">
            <div class="container">
                <div class="footer-main">
                    <h4>链接</h4>
                    <a href="http://10.88.4.84/nportal/portal/s/sjcs/content.psml?MAIN_ID=1502346993049&pageNumber=1&COLUMNID=54297B43429DBDDAC915BDD0127FF322&COLUMN_NAME=%B3%A3%D3%C3%D7%CA%C1%CF" target="_blank" class="footer-main-link">专卖法律</a>
                    <a href="#" target="_blank" class="footer-main-link">营销政策</a>

                </div>
                <div class="footer-main">
                    <h4>关于</h4>
                    <el-popover
                            placement="right"
                            title="华蓥市烟草局"
                            width="200"
                            trigger="hover"
                            content="创新项目小组">
                        <el-link :underline="false" slot="reference" class="footer-main-link">开发人员</el-link>
                    </el-popover>

                    <el-popover
                            placement="right"
                            title="测试版"
                            width="200"
                            trigger="hover"
                            content="v1.0">
                        <el-link :underline="false" slot="reference" class="footer-main-link">历史版本</el-link>
                    </el-popover>

                </div>
                <div class="footer-social">
                    <p class="footer-social-title">HYLG-Web 1.0</p>

<!--                    <i class="doc-icon-weixin elementdoc el-popover__reference" aria-describedby="el-popover-7312" tabindex="0"></i>-->
<!--                    <a href="https://github.com/elemefe" target="_blank">-->
<!--                        呵呵-->
<!--                        <i class="doc-icon-github elementdoc"></i>-->
<!--                    </a>-->
<!--                    <a href="https://gitter.im/ElemeFE/element" target="_blank">-->
<!--                        <i class="doc-icon-gitter elementdoc"></i>-->
<!--                    </a>-->
                </div>
            </div>
        </footer>

    </div>

</template>

<script>


    export default {


    }
</script>


<style>


    /*
        footer
    */
    .footer .footer-social {
        float: right;
        text-align: right;
    }
    .footer .footer-social .footer-social-title {
        color: #666;
        font-size: 18px;
        line-height: 1;
        margin: 0 0 20px;
        padding: 0;
        font-weight: 700;
    }
    .footer .footer-social {
        float: right;
        text-align: right;
    }
    .footer .footer-main .footer-main-link {
        display: block;
        margin: 0;
        line-height: 2;
        font-size: 14px;
        color: #666;
    }
    h4 {
        display: block;
        margin-block-start: 1.33em;
        margin-block-end: 1.33em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        font-weight: bold;
    }
    .footer .footer-main h4 {
        font-size: 18px;
        color: #333;
        line-height: 1;
        margin: 0 0 15px;
    }
    .footer .footer-main {
        font-size: 0;
        display: inline-block;
        vertical-align: top;
        margin-right: 110px;
    }
    .footer .container {
        box-sizing: border-box;
        width: auto;
    }
    .footer{
        background-color: #f7fbfd;
        width: 100%;
        padding: 40px 150px;
        margin-top: -200px;
        box-sizing: border-box;
        height: 200px;
    }
    footer{
        display: block;
    }


    /*
        main-cnt
    */

    .card a:hover{
        background-color: #409eff;
        color: white;
    }

    .card a {
        height: 53px;
        line-height: 52px;
        font-size: 14px;
        color: #409eff;
        text-align: center;
        border: 0;
        border-top: 1px solid #eaeefb;
        padding: 0;
        cursor: pointer;
        width: 100%;
        position: absolute;
        bottom: 0;
        left: 0;
        background-color: #fff;
        border-radius: 0 0 5px 5px;
        transition: all .3s;
        text-decoration: none;
        display: block;
    }
    .card p {
        font-size: 14px;
        color: #99a9bf;
        padding: 0 25px;
        line-height: 20px;
    }
    h3 {
        display: block;
        font-size: 1.17em;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        font-weight: bold;
    }
    .card h3{
        margin: 0;
        font-size: 18px;
        color: #1f2f3d;
        font-weight: 400;
    }
    .card img {
        margin: 66px auto 60px;
        width: 80px;
        height: 80px;
    }
    .card::before{
        box-shadow: 0px 10px 10px #9A9A9A;
        /*background: radial-gradient(ellipse at center,rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 80%);*/
        height: 100%;
        width: 100%;
        opacity: 0;
        position: absolute;
        content:'';
        z-index: -1;
        top: -5px;
        left:0;
        transition-duration: 0.3s;
        transition-property: transform, opacity;
    }
    .card:hover:before{
        opacity: 0.3;
        transform: translateY(5px);
    }
    .card:hover{
        transform: translateY(-5px);
    }
    .card {
        height: 430px;
        width: 100%;
        background: #fff;
        border: 1px solid #eaeefb;
        border-radius: 5px;
        box-sizing: border-box;
        text-align: center;
        position: relative;
        transition: all .3s ease-in-out;
        bottom: 0;
    }
    .cards li {
        width: 25%;
        padding: 0 19px;
        box-sizing: border-box;
        float: left;
        list-style: none;
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
    .cards .container {
        padding: 0;
        margin: 0 -11px;
        width: auto;
    }
    .cards {
        height: 430px;
        margin: 0 auto 110px;
        width: 1140px;
    }
    .sponsor p {
        margin: 0;
        line-height: 1.8;
        color: #999;
        font-size: 14px;
    }
    .sponsor div {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .sponsor img{
        margin-right: 20px;
    }
    .sponsor {
        margin: 0 20px 50px;
        display: inline-flex;
        width: 300px;
        height: 100px;
        justify-content: center;
    }

    .sponsors {
        display: flex;
        justify-content: center;
    }

    .jumbotron img {
        width: 100%;
    }
    .jumbotron {
        width: 800px;
        margin: 10px auto;
        position: relative;
    }
    p {
        display: block;
        margin-block-start: 1em;
        margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
    }
    .banner-desc p {
        font-size: 18px;
        line-height: 28px;
        color: #888;
        margin: 10px 0 5px;
    }
    .banner-desc h1 {
        font-size: 34px;
        margin: 0;
        line-height: 48px;
        color: #555;
    }
    .banner-desc{
        padding-top: 20px;
    }
    .banner{
        text-align: center;
    }

    .main-cnt {
        /*overflow-y: hidden;*/
        margin-top: -80px;
        padding: 80px 0 200px;
        box-sizing: border-box;
        min-height: 100%;
    }


    /*
        app
     */
    div {
        display: block;
    }




</style>








