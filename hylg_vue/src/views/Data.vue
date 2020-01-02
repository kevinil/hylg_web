<template>
    <div id="data">
        <div class="main-cnt">
            <div>
                <div class="dataTabs" v-show="seeTab">
                    <el-tabs :tab-position="tabPosition" style="height: 600px;">
                        <el-tab-pane label="客户查询">
                            <div class="list">
                                <br>
                                <el-divider content-position="left">重点大户</el-divider>
                                <br>
                                <el-breadcrumb separator="/">
                                    <el-breadcrumb-item>
                                        <el-link @click="getVipCustDetail(511681101886)" target="_blank" type="warning"
                                                 :underline="false">冯永技
                                        </el-link>
                                    </el-breadcrumb-item>
                                    <el-breadcrumb-item>
                                        <el-link @click="getVipCustDetail(511681102410)" target="_blank" type="warning"
                                                 :underline="false">王道林
                                        </el-link>
                                    </el-breadcrumb-item>
                                    <el-breadcrumb-item>
                                        <el-link @click="getVipCustDetail(511681100875)" target="_blank" type="warning"
                                                 :underline="false">王光华
                                        </el-link>
                                    </el-breadcrumb-item>
                                    <el-breadcrumb-item>
                                        <el-link @click="getVipCustDetail(511681100890)" target="_blank" type="warning"
                                                 :underline="false">雷九弟
                                        </el-link>
                                    </el-breadcrumb-item>
                                    <el-breadcrumb-item></el-breadcrumb-item>
                                </el-breadcrumb>
                                <br>
                                <el-divider content-position="left">
                                    搜索
                                    <el-input v-model="peopleQuery" placeholder="模糊查询，请输入关键字" class="searchInput">
                                    </el-input>
                                </el-divider>
                                <el-table
                                        :data="custTable"
                                        height="340"
                                        border
                                        v-loading="storeloading"
                                        v-infinite-scroll="load"
                                        class="custTable"
                                >
                                    <el-table-column
                                            prop="certId"
                                            label="许可证号"
                                            sortable
                                            width="180">
                                        <!--                                        <template scope="scope">-->
                                        <!--                                            <div style="color:red;text-decoration:underline;cursor:pointer;"-->
                                        <!--                                                 @click="goCustomerDetail(scope.row)">{{ scope.row.date }}-->
                                        <!--                                            </div>-->
                                        <!--                                        </template>-->
                                    </el-table-column>
                                    <el-table-column
                                            prop="faren"
                                            label="姓名"
                                            width="180">
                                    </el-table-column>

                                    <el-table-column
                                            prop="zihao"
                                            label="企业字号">
                                    </el-table-column>
                                    <el-table-column
                                            fixed="left"
                                            label="操作"
                                            width="50px;">
                                        <template slot-scope="scope">
                                            <el-button @click="goCustomerDetail(scope.row)" type="text" size="small">查看
                                            </el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </el-tab-pane>
                        <el-tab-pane label="其他查询">
                            <p style="color:#999">需求分析中</p>
                        </el-tab-pane>
                    </el-tabs>
                </div>

                <div class="dataDetail" v-show="seeDetail">
                    <el-page-header @back="goBack" content="详情页面" style="font-family: serif;">
                    </el-page-header>


                    <template>

                        <div style="margin-top: 40px;float: left;">
                            <el-card class="box-card" shadow="always">
                                <div slot="header">

                                    <el-row :gutter="20">
                                        <el-col :span="10">
                                            <p style="color: black;font-size: 20px;margin-left: 20px;">{{
                                                this.custDetailInfo["faren"] }}</p>
                                        </el-col>
                                        <div class="right-top">
                                            <el-progress type="dashboard" :percentage="perTotal"
                                                         :color="colors"></el-progress>
                                        </div>
                                        <p class="text">{{ this.custDetailInfo["key"] }}</p>
                                        <p class="text">{{ this.custDetailInfo["zihao"] }}</p>
                                        <p class="text">{{ this.custDetailInfo["saleaddr"] }}</p>
                                        <el-col :span="12">
                                        </el-col>
                                    </el-row>


                                </div>

                                <div style="margin-left: 20px;margin-right: 2px;">
                                    <div>
                                        <el-progress  style="margin-bottom: 12px;" :percentage="perClue" :format="formatClue"
                                                     :color="colors"></el-progress>

                                        <el-progress style="margin-bottom: 12px;" :percentage="perRelationship" :format="formatRelationship"
                                                     :color="colors"></el-progress>
                                        <el-progress style="margin-bottom: 12px;" :percentage="perOrder" :format="formatOrder"
                                                     :color="colors"></el-progress>
                                        <el-progress style="margin-bottom: 12px;" :percentage="perCase" :format="formatCase"
                                                     :color="colors"></el-progress>
                                    </div>
                                    <!--                                    <p style="color: black;font-size: 20px;">{{ this.custDetailInfo["faren"] }}</p>-->
<!--                                    <p>{{ this.custDetailInfo["key"] }}</p>-->
<!--                                    <p>{{ this.custDetailInfo["zihao"] }}</p>-->
<!--                                    <p>{{ this.custDetailInfo["saleaddr"] }}</p>-->
                                    <!--                                    <p>{{ this.custDetailInfo["idNum"] }}</p>-->
                                    <!--                                    <p>{{ this.custDetailInfo["district"] }}</p>-->
                                </div>
                            </el-card>
                        </div>

                        <div style="margin-left: 40px;float: left;margin-top: -20px;">
                            <h3>线索搜集</h3>

                        </div>

                        <div class="clueLine" style="margin-left: 400px;margin-top: 40px;">
                            <el-timeline>
                                <el-timeline-item v-for="(clue,index) in this.clues" :key="index" :timestamp="clue.time"
                                                  placement="top">
                                    <el-card>
                                        <p>{{ "车辆： " + clue.car }}</p>
                                        <p>{{ "区域： " + clue.maddr }}</p>
                                        <p>{{ "地址： " + clue.daddr }}</p>
                                        <p>{{ "关联地址： " + clue.raddr }}</p>
                                        <p>{{ "性质： " + clue.caseTypes }}</p>
                                        <p>{{ "物品： " + clue.caseAmount }}</p>
                                        <p>{{ "备注信息： " + clue.caseInfo }}</p>
                                    </el-card>
                                </el-timeline-item>
                            </el-timeline>
                        </div>
                    </template>

                </div>


            </div>

        </div>
    </div>
</template>

<script>
    export default {

        data() {
            return {
                storeTable: "",
                peopleQuery: "",
                peopleSearch: "",
                custTimer: null,
                queryVisible: false,
                radio1: "1",
                tabPosition: 'top',
                storeloading: true,

                seeTab: true,
                seeDetail: false,

                custDetailId: "",
                custDetailInfo: "",

                clues: [],

                colors:[
                    {color: '#478d58', percentage: 10},
                    {color: '#4fb85e', percentage: 20},
                    {color: '#d7e085', percentage: 30},
                    {color: '#e7d561', percentage: 40},
                    {color: '#e2ab40', percentage: 50},
                    {color: '#e64c23', percentage: 60},
                    {color: '#de2d4b', percentage: 70},
                    {color: '#df3c9b', percentage: 80},
                    {color: '#e620a5', percentage: 90},
                    {color: '#f500e2', percentage: 100},
                ],

                perClue: 70,
                perRelationship: 12,
                perOrder: 23,
                perCase: 54,
                perTotal: 62,
                // dict = {
                //     "key": cust.cust_key,
                //     "zihao": cust.cust_zihao,
                //     "faren": cust.cust_faren,
                //     "idNum": cust.cust_idnum,
                //     "saleaddr": cust.cust_saleaddr,
                //     "idaddr": cust.cust_idaddr,
                //     "contman": cust.cust_contman,
                //     "contphone": cust.cust_contphone,
                //     "special": cust.cust_special,
                //     "district": cust.cust_district
                // }
            }
        },
        watch: {
            // 监控输入缓响应查询
            peopleQuery(val) {
                clearTimeout(this.custTimer);
                this.storeloading = true;
                this.custTimer = setTimeout(() => {
                    this.storeloading = false;
                    this.peopleSearch = val;
                    this.queryVisible = val === null
                }, 200)
            }

        },
        computed: {
            custTable() {
                console.log("计算");
                const peopleSearch = this.peopleSearch;
                if (peopleSearch) {

                    return this.storeTable.filter(data => {
                        return Object.keys(data).some(key => {
                            return String(data[key]).toLowerCase().indexOf(peopleSearch) > -1
                        })
                    })
                }
                return "";
            }
        },
        created() {
            this.$axios.post('/data/', JSON.stringify({getData: "customers"})).then(res => {
                this.storeloading = false;
                this.storeTable = res.data
            })


        },
        methods: {
            goCustomerDetail(row) {
                this.$axios.post('/data/', JSON.stringify({getData: row.certId})).then(res => {
                    // 一定将对象转化称JSON字符串传递
                    this.custDetailInfo = res.data[0];
                    this.clues = this.custDetailInfo["clues"];
                    console.log("收到数据");
                    console.log(this.clues)
                    // console.log(res.data)
                    // this.GLOBAL.storeCustTable = res.data
                    // 接收到的res格式 经过Django的HttpResponse的包装，你所需要的数据在res.data中
                    // 请保持在传递数据时使用JSON字符串的好习惯，否则坑无数
                });

                this.seeTab = false;
                this.seeDetail = true
            },
            goBack() {
                this.seeTab = true;
                this.seeDetail = false
            },
            getVipCustDetail(id) {
                this.$axios.post('/data/', JSON.stringify({getData: id})).then(res => {
                    // 一定将对象转化称JSON字符串传递
                    this.custDetailInfo = res.data[0];
                    this.clues = this.custDetailInfo["clues"];
                    console.log("收到vip数据");
                    console.log(this.clues)
                    // console.log(res.data)
                    // this.GLOBAL.storeCustTable = res.data
                    // 接收到的res格式 经过Django的HttpResponse的包装，你所需要的数据在res.data中
                    // 请保持在传递数据时使用JSON字符串的好习惯，否则坑无数
                });
                this.seeTab = false;
                this.seeDetail = true
            },
            formatClue() {
                return  "线索"
            },
            formatRelationship() {
                return "关系网"
            },
            formatOrder() {
                return "订单"
            },
            formatCase() {
                return "案件"
            },
            formatType(types){
                var text = ""
                for (var i = 0; i <types.count ; i++) {
                    text += types[i]
                }
                return text
            }
        }
    }
</script>

<style>
    .searchInput {
        margin: 10px 5px;
        width: 200px;
    }

    .dataTabs {
        width: 1140px;
        margin: auto;
        margin-top: 20px;

    }


    .list {
        width: 1140px;
        margin: auto;
        margin-top: -10px;
    }

    .custTable {
        width: 1140px;
        margin: auto;
        margin-top: 40px;
    }

    .dataDetail {
        width: 1140px;
        margin: auto;
        margin-top: 20px;
    }

    .element.style {
        height: 400px;
    }

    .text {
        margin-left: 30px;
        font-size: 16px;
        color: #888;
    }

    /*.item {*/
    /*    padding: 18px 0;*/
    /*}*/

    .box-card {
        width: 400px;
    }

    .right-top{
        float: right;
        margin-right: 20px;
        margin-top: 10px;
    }

    /*.main-cnt {*/
    /*    margin-top: -80px;*/
    /*    padding-top: 80px;*/
    /*    box-sizing: border-box;*/
    /*    min-height: 100%;*/
    /*}*/
</style>