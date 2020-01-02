<template>
    <div id="case">
        <div class="main-cnt">
            <div class="case-form">
                <transition name="el-zoom-in-top">
                    <div v-show="show">
                        <div style="float:left;width: 262px;height: 20px;">
                            <el-card shadow="never">
                                <el-divider content-position="center">四维分析</el-divider>
                                <el-tooltip content="全员提交重要信息" placement="top" effect="dark" open-delay="300">
                                    <span class="four-tag" style="margin-right:8px;">线索</span>
                                </el-tooltip>
                                <el-tooltip content="精准打击团伙网络" placement="top" effect="dark" open-delay="300">>
                                    <span class="four-tag" style="margin-right:8px;">关系网</span>
                                </el-tooltip>
                                <el-tooltip content="结合营销投放政策" placement="top" effect="dark" open-delay="300">>
                                    <span class="four-tag" style="margin-right:8px;">订单</span>
                                </el-tooltip>
                                <el-tooltip content="过往案件痕迹查询" placement="top" effect="dark" open-delay="300">>
                                    <span class="four-tag">案件</span>
                                </el-tooltip>
                            </el-card>

                            <el-row style="margin-top: 8px;">
                                <el-col>
                                    <el-card shadow="never" :body-style="{ padding: '0px' }">
                                        <img src="../assets/huizhang.png" class="image">
                                        <el-row style="margin-top: 12px;margin-bottom: 12px;" type="flex" class="row-bg"
                                                justify="center">
                                            <span class="logo-text">华蓥烟草 创新求变</span>
                                        </el-row>
                                    </el-card>
                                </el-col>
                            </el-row>
                        </div>

                        <el-tabs  type="border-card" style="float: left;margin-left: 20px;width: 850px;">
                            <el-tab-pane >
                               <span slot="label"><i class="el-icon-refresh"></i> 实时分析</span>
                                <el-row :gutter="20" >
                                    <el-col :span="6" v-for="tab in tables" :key="tab.title">
                                        <el-card :body-style="{ padding: '0px' }">
                                            <div style="padding: 14px;">
<!--                                                <span class="four-tag">{{ tab.title }}</span>-->
                                                <el-tag>{{ tab.title }}</el-tag>
                                                <el-table
                                                        style="margin-top: 10px;"
                                                        :data="tab.data"
                                                        :show-header="tableHeaderStatus"
                                                        :highlight-current-row="highlightStatus">
                                                    <el-table-column
                                                            prop="customer"
                                                            label="客户"
                                                            width="100xp;">
                                                        <template slot-scope="scope">
                                                            <h3 style="color: #475669;opacity: 0.75;font-size:25px;margin-left: -8px;">{{ scope.row.customer }}</h3>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                            style="height: 40px;"
                                                            prop="value"
                                                            label="风险值"
                                                            width="55xp;">
                                                        <template slot-scope="scope">
                                                            <h3 :style=colorSelect(parseInt(scope.row.value))>{{ scope.row.value }}</h3>
                                                        </template>
                                                    </el-table-column>

                                                </el-table>
                                            </div>
                                        </el-card>
                                    </el-col>
                                </el-row>
                            </el-tab-pane>
                            <el-tab-pane>
                                <span slot="label"><i class="el-icon-date"></i> 预警历史</span>
                                <el-table
                                        :data="tableYujing"
                                        :show-header="tableHeaderStatus"
                                        :highlight-current-row="highlightStatus">
                                    <el-table-column
                                            prop="customer"
                                            label="客户"
                                            width="200xp;">
                                    </el-table-column>
                                    <el-table-column
                                            prop="value"
                                            label="风险值"
                                            width="200xp;">
                                    </el-table-column>
                                    <el-table-column
                                            prop="date"
                                            label="日期"
                                            width="370xp;">
                                    </el-table-column>

                                </el-table>
                            </el-tab-pane>
                            <el-tab-pane label="查找区域">参数</el-tab-pane>
                        </el-tabs>
                    </div>
                </transition>
            </div>
            <div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                show: false,
                activeNames: ['1'],
                items: [
                    {type: '', label: "全员提交"},
                    {type: '', label: "全员提交"},
                    {type: '', label: "全员提交"},
                ],
                tableHeaderStatus: false,
                highlightStatus: false,
                tableYujing: [
                    {
                        customer: "张无忌",
                        value: "62%",
                        date: "21 days ago"
                    },
                    {
                        customer: "楚留香",
                        value: "75%",
                        date: "12 Jun 2019"
                    },
                ],


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

                tables: [
                    {
                        title: "线索",
                        data: [
                            {
                                customer: "王道林",
                                value: "55",
                            },
                            {
                                customer: "冯永技",
                                value: "40",
                            },
                            {
                                customer: "周刚",
                                value: "25",
                            },
                        ],
                    },
                    {
                        title: "关系网",
                        data: [
                            {
                                customer: "冯永技",
                                value: "65",
                            },
                            {
                                customer: "杨天碧",
                                value: "60",
                            },
                            {
                                customer: "周刚",
                                value: "45",
                            },
                        ],
                    },
                    {
                        title: "订单",
                        data: [
                            {
                                customer: "胡中华",
                                value: "20",
                            },
                            {
                                customer: "洪善平",
                                value: "15",
                            },
                            {
                                customer: "江秀丽",
                                value: "15",
                            },
                        ],
                    },
                    {
                        title: "案件",
                        data: [
                            {
                                customer: "王海兰",
                                value: "70",
                            },
                            {
                                customer: "冯永技",
                                value: "65",
                            },
                            {
                                customer: "杨波",
                                value: "55",
                            },
                        ],
                    },


                ],


                currentDate: new Date(),
                realtime: [
                    {type: '线索', label: '11', table: this.tableClue},
                    {type: '关系网', label: '22', table: this.tableRelationship},
                    {type: '订单', label: '33', table: this.tableOrder},
                    {type: '案底', label: '44', table: this.tableCase},
                ]
            }
        },
        created() {


        },

        mounted() {
            this.show = true
        },

        methods: {
            handleChange(val) {
                console.log(val)
            },
            tableRowClassName(row) {
                if (parseFloat(row.value) >= 0.6 ) {
                    return "warning-row"
                }else {
                    return "normal-row"
                }
            },
            colorSelect(value) {
                if (value >= 90) {
                    return "color:#f500e2;font-size:25px;"
                } else if (value >= 80) {
                    return "color:#e620a5;font-size:26px;"
                } else if (value >= 70) {
                    return "color:#df3c9b;font-size:24px;"
                } else if (value >= 60) {
                    return "color:#de2d4b;font-size:23px;"
                } else if (value >= 50) {
                    return "color:#e64c23;font-size:22px;"
                } else if (value >= 40) {
                    return "color:#e2ab40;font-size:21px;"
                } else if (value >= 30) {
                    return "color:#e7d561;font-size:20px;"
                } else if (value >= 20) {
                    return "color:#d7e085;font-size:19px;"
                } else if (value >= 10) {
                    return "color:#4fb85e;font-size:18px;"
                } else {
                    return "color:#478d58;font-size:17px;"
                }

            },
            valueFormat(percentage) {
               return percentage;
            }

        }
    }
</script>

<style>
    .transition-box {
        margin-bottom: 10px;
        width: 200px;
        height: 100px;
        border-radius: 4px;
        background-color: #409EFF;
        text-align: center;
        color: #fff;
        padding: 40px 20px;
        box-sizing: border-box;
        margin-right: 20px;
    }

    .collapse {
        width: 1140px;
        margin: auto;
        border-top: 0px;
    }

    /*.main-cnt {*/
    /*    overflow-y: hidden;*/
    /*    margin-top: -80px;*/
    /*    padding: 80px 0 340px;*/
    /*    box-sizing: border-box;*/
    /*    min-height: 100%;*/
    /*}*/

    .case-form {
        width: 1140px;
        margin: auto;
        margin-top: 20px;
    }

    h2 {
        width: 200px;
        margin: auto;
        color: #797b7f;
    }

    .ciyun {
        width: 80%;
    }

    .ciyun {
        margin: 30px auto;
    }

    .badge-item {
        margin: 10px 40px 0 0;
    }

    .image {
        width: 100%;
        display: block;
    }

    .logo-text {
        text-align: center;
        font-weight: bolder;
        font-size: 16px;
    }

    .el-table tbody tr:hover > td {
        background-color: white !important
    }

    .el-table .warning-row {
        background: oldlace;
    }

    .value-color{

    }



    div {
        display: block;
    }

    .four-tag {
        font-size: 12px;
        color: #0366d6;
        background-color: #f1f8ff;
        padding: 5px 11px;
        border-radius: 3px;
    }
</style>