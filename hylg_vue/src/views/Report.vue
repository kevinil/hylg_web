<template>
    <div id="report">
        <div class="main-cnt">
            <div class="report-form">

                <el-row class="each-row" style="display: none;">
                    <el-col :span="4.5"><h3>输入专卖账号</h3></el-col>
                    <el-col :span="2" style="margin-right:25px;"><img src="../assets/zhanghao.png" style="width:18px;margin: 23px 0 0 2px;" alt=""></el-col>
                    <el-col :span="2"><h4>用户名</h4></el-col>
                    <el-col :span="6"><el-input v-model="usrinput" clearable placeholder="请输入用户名" type="text" style="margin-top: 12px;"></el-input></el-col>
                </el-row>
                <el-row class="each-row" style="display: none;">
                    <el-col :span="4" style="margin-right:47px;"><h4>  </h4></el-col>
                    <el-col :span="2"><h4>密码</h4></el-col>
                    <el-col :span="6"><el-input v-model="psdinput" clearable placeholder="请输入密码" show-password style="margin-top: 12px;"></el-input></el-col>
                </el-row>

                <el-row class="each-row">
                    <el-col :span="3.5"><h3>选择时间范围</h3></el-col>
                    <el-col :span="2"><img src="../assets/shijian.png" style="width:20px;margin: 22px 0 0 3px;" alt=""></el-col>
                    <el-col :span="1"><h4> </h4></el-col>
                    <el-col :span="8">
                        <el-date-picker
                                style="margin-top: 12px;"
                                v-model="choosedate"
                                type="daterange"
                                text-align="right"
                                unlink-panels
                                range-separator="至"
                                start-placeholder="开始日期"
                                end-placeholder="结束日期"
                                :picker-options="pickerOptions">
                        </el-date-picker>
                    </el-col>
                </el-row>

                <el-row class="each-row">
                    <el-col :span="3.5"><h3>选择案发地点</h3></el-col>
                    <el-col :span="3"><img src="../assets/didian.png" style="width:20px;margin: 22px 0 0 2px;" alt=""></el-col>
                    <el-col :span="6">
                        <el-select v-model="formselect"
                                   allow-create
                                   multiple
                                   filterable
                                   placeholder="可输入"
                                   style="margin-top:12px;">
                            <el-option
                                    v-for="item in options"
                                    :key="item.location"
                                    :label="item.location"
                                    :value="item.location">
                                <span style="float: left">{{ item.location }}</span>
                                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.district }}</span>
                            </el-option>
                        </el-select>
                    </el-col>
                </el-row>

                <el-row class="each-row">
                    <el-col :span="3.5"><h3>选择关键字</h3></el-col>
                    <el-col :span="3" style="margin-right: 20px;"><img src="../assets/guanjian.png" style="width:20px;margin: 23px 0 0 2px;" alt=""></el-col>
                    <el-col :span="0.5" class="biaoqian" style="margin-left: -1px;">

                        <el-checkbox v-model="wuliu" label="物流" border></el-checkbox>
                    </el-col>
                    <el-col :span="0.5" class="biaoqian">
                        <el-checkbox v-model="jidi" label="寄递" border></el-checkbox>
                    </el-col>
                    <el-col :span="0.5" class="biaoqian">
                        <el-checkbox v-model="qita" label="其他" border disabled></el-checkbox>
                    </el-col>
                </el-row>

                <el-row class="each-row">
                    <el-col :span="5" style="margin-right: 21px;"><h4>  </h4></el-col>
                    <el-col :span="2" style="margin-top: 10px;"><el-button type="primary" @click="startreport" :loading="reportloading">生成报表</el-button></el-col>
                </el-row>


                <div>
                    <el-table
                            :data="reportTable"
                            border
                            style="width: 100%; margin-top: 20px">
                        <el-table-column
                                prop="type"
                                label="类型"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="case"
                                label="案件（起）">
                        </el-table-column>
                        <el-table-column
                                prop="carton"
                                label="数量（万支）">
                        </el-table-column>
                        <el-table-column
                                prop="price"
                                label="案值（万元）">
                        </el-table-column>
                    </el-table>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Report",
        data() {
            return{

                usrinput:'',
                psdinput:'',

                pickerOptions: {
                    shortcuts:
                        [{
                            text: '最近一周',
                            onClick(picker) {
                                const end = new Date();
                                const start = new Date();
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                                picker.$emit('pick', [start, end]);
                            }
                        }, {
                            text: '最近一个月',
                            onClick(picker) {
                                const end = new Date();
                                const start = new Date();
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                                picker.$emit('pick', [start, end]);
                            }
                        }, {
                            text: '最近三个月',
                            onClick(picker) {
                                const end = new Date();
                                const start = new Date();
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                                picker.$emit('pick', [start, end]);
                            }
                        }]
                },
                choosedate:'',

                options: [{
                    district: '华蓥市',
                    location: '溪口镇'
                }, {
                    district: '华蓥市',
                    location: '庆华镇'
                }],
                formselect: '',


                wuliu: false,
                jidi: false,
                qita: false,

                reportloading: false,

                reportTable: '',
            }
        },
        computed: {

        },
        methods: {
            startreport() {
                // this.reportloading = true; //启动按钮
                if (!this.choosedate) {
                    this.$notify({
                        title: '警告',
                        message: '日期不能为空',
                        type: 'warning',
                        offset: 100
                    });
                    // this.reportloading = false; //恢复按钮
                }
                var date1 = new Date(this.choosedate[0]);
                var date2 = new Date(this.choosedate[1]);
                var date11 = date1.getFullYear()+""+(date1.getMonth()>9? date1.getMonth():"0"+date1.getMonth())+''+(date1.getDate()>9? date1.getDate():"0"+date1.getDate());
                var date22 = date2.getFullYear()+""+(date2.getMonth()>9? date2.getMonth():"0"+date2.getMonth())+''+(date2.getDate()>9? date2.getDate():"0"+date2.getDate());

                if(this.choosedate){
                    this.$axios.post('/reportRequest/', JSON.stringify({
                        d1: date11,
                        d2: date22,
                        locations: this.formselect,
                        wl: this.wuliu,
                        jd: this.jidi,
                    })).then(res => {
                        this.reportloading = false;
                        console.log(res.data);
                        this.reportTable = res.data
                    });
                }

                console.log(date11+ '    ' + date22);

                for (var i = 0; i < this.formselect.length; i++) {
                    console.log(this.formselect[i])
                }
            },


        }
    }
</script>

<style>
    h4{
        margin: 20px;
        color: #8c939d;
    }
    h3{
        margin-left: 0;
        color: #797b7f;
    }

    .each-row{
        margin-left: 50px;
        margin-top: 20px;
    }

    .report-form{
        width: 1140px;
        margin: auto;
    }
</style>