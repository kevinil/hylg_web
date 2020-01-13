<template>
    <div id="clue">
        <div class="main-cnt">
            <div class="clue-form">
                <div class="wraper-form">
                    <div style="float:left;width: 262px;height: 20px;">
                        <el-carousel height="200px" direction="vertical" :autoplay="true">
                            <el-carousel-item>
                                <div class="carousel-div" style="margin-top: -32px;">
                                    <h3>敦笃励志</h3>
                                    <h3>果毅力行</h3>
                                </div>
                            </el-carousel-item>
                            <el-carousel-item>
                                <div class="carousel-div" style="margin-top: -60px;">
                                    <h3>积极乐观</h3>
                                    <h3>忠诚团结</h3>
                                    <h3>开拓创新</h3>
                                    <h3>勇往直前</h3>
                                </div>
                            </el-carousel-item>
                            <el-carousel-item>
                                <div class="carousel-div" style="margin-top: -32px;">
                                    <h3>不要等待奇迹的发生</h3>
                                    <h3>因为奇迹在等我们去创造</h3>
                                </div>
                            </el-carousel-item>
<!--                            <el-carousel-item v-for="item in tips" :key="item">-->
<!--&lt;!&ndash;                                <img src="../assets/huizhang.png" class="image">&ndash;&gt;-->
<!--                                <p class="medium">{{ item }}<br></p>-->
<!--                            </el-carousel-item>-->
                        </el-carousel>

                        <el-card style="margin-top: 8px;" shadow="never">
                            <el-divider content-position="center">线索范围</el-divider>
                            <!--                            <el-tooltip content="" placement="top" effect="dark" open-delay="300">-->
                            <el-tag style="margin-right: 8px;">无证信息</el-tag>
                            <!--                            </el-tooltip>-->
                            <!--                            <el-tooltip content="" placement="top" effect="dark" open-delay="300">-->
                            <el-tag style="margin-right: 8px;">假烟信息</el-tag>
                            <!--                            </el-tooltip>-->
                            <!--                            <el-tooltip content="" placement="top" effect="dark" open-delay="300">-->
                            <el-tag>关系网</el-tag>
                            <!--                            </el-tooltip>-->
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

                    <el-tabs type="border-card" style="float: left;margin-left: 20px;width: 850px;">
                        <el-tab-pane>
                            <span slot="label"><i class="el-icon-edit"></i> 填写信息</span>


                            <div style="float:left;width:100%;">
                                <el-form ref="form" :model="form" label-position="left" label-width="100px">

                                    <el-form-item label="流程选择">
                                        <el-radio-group v-model="form.clueType" @change="clueTypeChange">
                                            <el-radio-button label="标准化"></el-radio-button>
                                            <el-radio-button label="简易化"></el-radio-button>
                                        </el-radio-group>
                                    </el-form-item>


                                    <el-form-item label="客户确认">
                                        <el-col :span="4" style="margin-right: 8px;">
                                            <el-input v-model="custQuery" placeholder="请输入姓名" clearable></el-input>
                                        </el-col>
                                        <el-col :span="4">
                                            <el-popover placement="right" width="550" trigger="manual"
                                                        v-model="queryVisible">
                                                <el-button type="primary" size="mini" @click="queryTableBtnClicked">
                                                    确认为新无证户
                                                </el-button>
                                                <el-table :data="queryTable" height="300"
                                                          @row-click="queryTableClicked">
                                                    <el-table-column width="150" property="certId"
                                                                     label="许可证号"></el-table-column>
                                                    <el-table-column width="100" property="faren"
                                                                     label="姓名"></el-table-column>
                                                    <el-table-column width="300" property="zihao"
                                                                     label="企业名称"></el-table-column>
                                                </el-table>
                                            </el-popover>
                                            <el-tag type="success" v-show="custIsSet&!custIsWu">零售户</el-tag>
                                            <el-tag type="warning" v-show="custIsSet&custIsWu">无证户</el-tag>
                                        </el-col>
                                    </el-form-item>

                                    <el-form-item label="车辆确认" v-show="clueIsStandard">
                                        <el-col :span="8">
                                            <el-input v-model="form.caseCars" placeholder="输入车牌号，以空格间隔">

                                            </el-input>
                                        </el-col>
                                    </el-form-item>


                                    <el-form-item label="相关区域" v-show="clueIsStandard">
                                        <el-col :span="6">
                                            <el-select v-model="form.region" clearable filterable placeholder="请选择主要区域">
                                                <el-option v-for="didian in locations" :key="didian" :label="didian"
                                                           :value="didian">
                                                    <span style="float: left">{{ didian }}</span>
                                                    <span style="float: right; color: #8492a6; font-size: 13px">{{ "华蓥市" }}</span>
                                                </el-option>
                                            </el-select>
                                        </el-col>
                                        <el-col :span="0.5" style="margin:0 15px;">-</el-col>
                                        <el-col :span="10">
                                            <el-input :span="4" v-model="form.addr" placeholder="详细地址"></el-input>
                                        </el-col>
                                        <el-col :span="1" style="margin-left: 20px;">
                                            <el-checkbox v-model="addRelate">添加关联地址</el-checkbox>
                                        </el-col>
                                    </el-form-item>

                                    <el-form-item label="" v-show="addRelate&clueIsStandard">
                                        <el-col :span="24">
                                            <el-input :span="4" v-model="form.relateTip" prefix-icon="el-icon-info"
                                                      placeholder="线索关联地址信息"></el-input>
                                        </el-col>

                                    </el-form-item>

                                    <el-form-item label="情况发生">
                                        <el-col :span="8">
                                            <el-date-picker type="date" placeholder="选择日期" v-model="form.date"
                                                            format="yyyy 年 MM 月 dd 日" value-format="yyyyMMdd"
                                                            style="width: 100%;"></el-date-picker>
                                        </el-col>
                                    </el-form-item>


                                    <el-form-item label="线索性质" v-show="custIsSet&clueIsStandard">
                                        <el-checkbox-group v-model="form.caseTypes">
                                            <el-checkbox label="无证运输烟草专卖品" name="type"
                                                         :checked="custIsWu"></el-checkbox>
                                            <el-checkbox label="假冒伪劣烟草制品" name="type"></el-checkbox>

                                            <el-checkbox label="未亮证经营" name="type" :disabled="custIsWu"></el-checkbox>
                                            <el-checkbox label="未在当地烟草批发企业进货" name="type"
                                                         :disabled="custIsWu"></el-checkbox>

                                            <el-checkbox label="无证经营" name="type" :disabled="!custIsWu"></el-checkbox>
                                        </el-checkbox-group>
                                    </el-form-item>


                                    <el-form-item label="线索物品" v-show="custIsSet&clueIsStandard">
                                        <el-radio-group v-model="form.caseAmount">
                                            <el-radio label="1条以下"></el-radio>
                                            <el-radio label="1至10条"></el-radio>
                                            <el-radio label="10至50条"></el-radio>
                                            <el-radio label="50条以上"></el-radio>
                                        </el-radio-group>
                                    </el-form-item>
                                    <el-form-item label="备注信息">
                                        <el-input type="textarea" v-model="form.info" placeholder="如：卷烟品牌"
                                                  maxlength="200"></el-input>
                                    </el-form-item>

                                    <el-form-item label="图片上传">
                                        <el-upload disabled
                                                   class="upload-demo"
                                                   action="../assets/"
                                                   :on-preview="handlePreview"
                                                   :on-remove="handleRemove"
                                                   :file-list="fileList"
                                                   list-type="picture">
                                            <el-button size="small" type="primary" disabled>点击上传</el-button>
                                            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
                                        </el-upload>
                                    </el-form-item>


                                    <el-form-item>
                                        <el-button type="primary" @click="onSubmit">点击提交</el-button>
                                    </el-form-item>
                                </el-form>
                            </div>
                        </el-tab-pane>
<!--                        <el-tab-pane>-->
<!--                            <span slot="label"><i class="el-icon-magic-stick"></i> 审核信息</span>-->
<!--                            <div>-->
<!--                                <el-card style="margin-bottom: 8px;" v-for="item in flyingClueTable" shadow="always"-->
<!--                                         :key="item.custName">-->

<!--                                    <el-row style="margin-top: 8px;">-->
<!--                                        <el-col :span="5">-->
<!--                                            <span style="text-shadow:1px 1px 3px rgba(31,47,61,0.47);font-size:40px;font-weight: bold;color: #25344e;margin-left: 10px;">{{ item.custName }}</span>-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="4">-->
<!--                                            <div style="float: left;height: 28px;margin-left: 4px;">-->
<!--                                                <span class="col-span">{{ item.date }}</span>-->
<!--                                            </div>-->
<!--                                            <div style="float: left;margin-left: 4px;">-->
<!--                                                <span class="col-span">{{ item.custType }}</span>-->
<!--                                            </div>-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="6">-->
<!--                                        <el-rate-->
<!--                                                style="margin-top: 18px;"-->
<!--                                                :texts="rateArray"-->
<!--                                                show-text="true"-->
<!--                                                v-model="item.rateValue"-->
<!--                                                :colors="colors">-->
<!--                                        </el-rate>-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="4" style="margin-left: -10px;">-->
<!--                                        <el-button :disabled="!item.rateValue" type="success" style="margin-top: 10px;">-->
<!--                                            完成审核-->
<!--                                        </el-button>-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="4" style="margin-left: -10px;">-->
<!--                                        <el-button :disabled="item.rateValue" type="danger" style="margin-top: 10px;">-->
<!--                                            删除明显错误线索-->
<!--                                        </el-button>-->
<!--                                        </el-col>-->
<!--                                    </el-row>-->
<!--                                    <el-row style="margin-top: 16px;margin-left: 10px;">-->
<!--                                        <el-col :span="0.5" style="margin-top: 1px;">-->
<!--                                            <img src="../assets/bianhao.png" style="height: 20px;">-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="4" style="margin-left: 8px;margin-top: 2px;">-->
<!--                                            <span>{{ item.custId }}</span>-->
<!--                                        </el-col>-->

<!--                                        <el-col :span="0.5" style="margin-top: 1px;">-->
<!--                                            <img src="../assets/location.png" style="height: 20px;">-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="1.5" style="margin-left: 8px;">-->
<!--                                            <span>{{ item.region }}-</span>-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="6.5" style="margin-left: 8px;">-->
<!--                                            <span>{{ item.addr }}-</span>-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="5.5" style="margin-left: 8px;">-->
<!--                                            <span>{{ item.relateTip }}-</span>-->
<!--                                        </el-col>-->
<!--                                    </el-row>-->
<!--                                    <el-row style="margin-top: 8px;margin-left: 10px;">-->
<!--                                        <el-col :span="0.5" style="margin-top: 1px;">-->
<!--                                            <img src="../assets/qingsuan.png" style="height: 20px;">-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="4" style="margin-left: 8px;">-->
<!--                                            <span>{{ item.caseAmount }}</span>-->
<!--                                        </el-col>-->

<!--                                        <el-col :span="0.5" style="margin-top: 1px;">-->
<!--                                            <img src="../assets/car.png" style="height: 20px;">-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="15" style="margin-left: 8px;">-->
<!--                                            <span>{{ item.caseCars }}</span>-->
<!--                                        </el-col>-->
<!--                                    </el-row>-->
<!--                                    <el-row style="margin-top: 8px;margin-left: 10px;">-->
<!--                                        <el-col :span="0.5" style="margin-top: 1px;">-->
<!--                                            <img src="../assets/falv.png" style="height: 20px;">-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="2.5" style="margin-left: 8px;">-->
<!--                                            <span>{{ item.caseTypes.join(',') }}</span>-->
<!--                                        </el-col>-->
<!--                                    </el-row>-->
<!--                                    <el-row style="margin-top: 8px;margin-left: 12px;">-->
<!--                                        <el-col :span="0.5" style="margin-top: 3px;">-->
<!--                                            <img src="../assets/cluebeizhu.png" style="height: 16px;">-->
<!--                                        </el-col>-->
<!--                                        <el-col :span="2.5" style="margin-left: 10px;">-->
<!--                                            <span>{{ item.info }}</span>-->
<!--                                        </el-col>-->
<!--                                    </el-row>-->
<!--                                </el-card>-->


<!--                            </div>-->

<!--                        </el-tab-pane>-->

                    </el-tabs>


                </div>
            </div>

        </div>
    </div>

</template>

<script>

    export default {
        name: "Clue",
        data() {

            return {

                tips:[
                    "敦笃励志，" +
                    "果毅力行！",
                    "忠诚团结、" +
                    "积极乐观、" +
                    "开拓创新、" +
                    "勇往直前！",
                    "不要等待奇迹的发生，" +
                    "因为奇迹在等我们去创造！"
                ],

                // 流程转换
                clueIsStandard: true,

                // 零售户列表
                custIsSet: false,      // 是否确认客户
                custQuery: '',         // 文本
                custTimer: null,       // 缓响应
                custSearch: '',        // 筛查
                custStoreTable: '',    // 缓存数据库
                queryVisible: false,   // 是否显示
                custIsWu: false,       // 是否无证户


                // 主要区域
                locations: [
                    '天池镇',
                    '禄市镇',
                    '永兴镇',
                    '双河街道',
                    '阳和镇',
                    '高兴镇',
                    '观音溪镇',
                    '庆华镇',
                    '溪口镇'],

                // 添加关联地址转换
                addRelate: false,

                // 表单数据
                form: {
                    clueType: '标准化',  // 流程类型
                    custType: '旧客户',  // 客户类型
                    custId: '',
                    caseCars: '',       // 涉案车辆
                    region: '',         // 区域
                    addr: '',           // 地址
                    relateTip: '',      // 关联地址
                    date: '',           // 线索日期
                    caseTypes: [],      // 案件类型
                    caseAmount: '',     // 涉案物品
                    info: ''            // 备注信息
                },


                colors: { 1: '#33ffba', 2: '#2eff11', 3: '#f78e21', 4: '#ff3a09', 5: '#ff15ee' },

                rateArray: ["普通","特别","显著","重要","危险"],
                flyingClueTable: [

                    {
                        clueType: '简易化',  // 流程类型
                        custType: '旧客户',  // 客户类型
                        custId: '5116819988',
                        custName: '王XX',
                        caseCars: '川X23333',       // 涉案车辆
                        region: '双河街道',         // 区域
                        addr: '红星一路',           // 地址
                        relateTip: '华蓥山广场',      // 关联地址
                        date: '20190909',           // 线索日期
                        caseTypes: ['假冒伪劣卷烟'],      // 案件类型
                        caseAmount: '50条以上',     // 涉案物品
                        info: '网络团伙',
                        rateValue: null,
                    },
                    {
                        clueType: '简易化',  // 流程类型
                        custType: '新客户',  // 客户类型
                        custId: '100002',
                        custName: '许某强',
                        caseCars: '无',       // 涉案车辆
                        region: '无',         // 区域
                        addr: '无',           // 地址
                        relateTip: '无',      // 关联地址
                        date: '20190805',           // 线索日期
                        caseTypes: [],      // 案件类型
                        caseAmount: '无',     // 涉案物品
                        info: '在双河搞事情',
                        rateValue: null,
                    },
                    {
                        clueType: '简易化',  // 流程类型
                        custType: '新客户',  // 客户类型
                        custId: '100001',
                        custName: '李XX',
                        caseCars: '无',       // 涉案车辆
                        region: '无',         // 区域
                        addr: '无',           // 地址
                        relateTip: '无',      // 关联地址
                        date: '201901018',           // 线索日期
                        caseTypes: [],      // 案件类型
                        caseAmount: '无',     // 涉案物品
                        info: '收烟',
                        rateValue: null,
                    },

                ]
            }

        },


        watch: {
            // 监控输入缓响应查询
            custQuery(val) {
                clearTimeout(this.custTimer);
                this.custTimer = setTimeout(() => {
                    if (val) {
                        if (!this.custIsSet) {
                            this.custSearch = val;
                            this.queryVisible = true
                        }
                    } else {
                        this.custIsSet = false;
                        this.queryVisible = false;
                        this.form.caseTypes = [];
                        this.form.caseAmount = ''
                    }
                }, 200)
            }

        },
        computed: {
            // 筛选显示
            queryTable() {
                console.log("查询零售户");
                const custSearch = this.custSearch;
                if (custSearch) {
                    return this.custStoreTable.filter(data => {
                        return Object.keys(data).some(key => {
                            return String(data[key]).toLowerCase().indexOf(custSearch) > -1
                        })
                    })
                }
                return "";
            }
        },
        created() {
            // 获取客户数据
            this.$axios.post('/data/', JSON.stringify({getData: "customers"})).then(res => {
                this.custStoreTable = res.data;
                console.log('获取custStoreTable')
            })
        },


        methods: {
            showBlankNotify(text) {
                this.$notify({
                    title: '警告',
                    message: '【' + text + '】不能为空',
                    type: 'warning',
                    duration: 3000,
                    offset: 100
                });
            },
            checkBlank() {
                var checkPass = true;
                if (!this.custQuery || !this.custIsSet) {
                    console.log(this.custIsSet);
                    this.showBlankNotify("客户确认");
                    checkPass = false;
                } else if (!this.form.date) {
                    console.log("情况发生了啊！！！")
                    this.showBlankNotify("情况发生");
                    checkPass = false;
                } else if (!this.form.region) {
                    if (this.form.clueType === "标准化") {
                        this.showBlankNotify("主要区域");
                        checkPass = false;
                    }
                } else if (this.form.caseTypes.length === 0) {
                    this.showBlankNotify("线索性质");
                    checkPass = false;
                } else if (!this.form.caseAmount) {
                    this.showBlankNotify("线索物品");
                    checkPass = false;
                }
                return checkPass


            },
            onSubmit() {
                var checkResult = this.checkBlank();
                const h = this.$createElement;
                if (checkResult) {
                    var caseInfos = [
                        h('p', null, "【客户确认】: " + this.custQuery),
                        h('p', null, "【车辆确认】: " + this.form.caseCars),
                        h('p', null, "【主要区域】: " + this.form.region),
                        h('p', null, "【详细地址】: " + this.form.addr),
                        h('p', null, "【关联地址】: " + this.form.relateTip),
                        h('p', null, "【情况发生】: " + this.form.date),
                        h('p', null, "【线索性质】: " + this.form.caseTypes.join(",")),
                        h('p', null, "【线索物品】: " + this.form.caseAmount),
                        h('p', null, "【备注信息】: " + this.form.info),
                    ];

                    this.$confirm('确认', '线索信息确认', {
                        // title: "线索信息确认",
                        message: h('div', null, caseInfos),
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                        beforeClose: (action, instance, done) => {
                            if (action === 'confirm') {
                                instance.confirmButtonLoading = true;
                                instance.confirmButtonText = '执行中...';

                                // 上传线索数据到后台
                                this.$axios.post('/clue/', JSON.stringify({
                                    custType: this.form.custType,
                                    clueType: this.form.clueType,
                                    custId: this.form.custId,
                                    custName: this.custQuery,
                                    caseCars: this.form.caseCars,
                                    mainAddr: this.form.region,
                                    detailAddr: this.form.addr,
                                    relateAddr: this.form.relateTip,
                                    getDate: this.form.date,
                                    caseTypes: this.form.caseTypes.join(","),
                                    caseAmount: this.form.caseAmount,
                                    caseInfos: this.form.info
                                })).then(res => {
                                    console.log(res)
                                });

                                setTimeout(() => {
                                    done();
                                    setTimeout(() => {
                                        instance.confirmButtonLoading = false;
                                    }, 300);
                                }, 3000);
                            } else {
                                done();
                            }
                        }
                        // center: true
                    }).then(() => {
                        this.$message({
                            type: 'success',
                            duration: 1000,
                            message: '提交线索成功'
                        });
                    });
                }
                console.log(this.form.clueType);
                console.log(this.custQuery);
                console.log(this.form.caseCars);
                console.log(this.form.region);
                console.log(this.form.addr);
                console.log(this.addRelate ? this.form.relateTip : '无关联地址');
                console.log(this.form.date);
                console.log((this.form.caseTypes).join("-"));
                console.log(this.form.caseAmount);
                console.log(this.form.info);
                console.log();
                console.log();

                console.log('submit!');
            },
            clueTypeChange() {
                // 流程切换
                this.clueIsStandard = !this.clueIsStandard
            },
            queryTableClicked(row) {
                //  零售户
                this.queryVisible = false;
                this.custIsSet = true;
                this.custIsWu = (row.certId[0] === "1");
                console.log(row);
                this.custQuery = row.faren;
                this.form.custId = row.certId;
                this.form.custType = "旧客户"
            },
            queryTableBtnClicked() {
                //  无证户
                this.queryVisible = false;
                this.custIsSet = true;
                this.custIsWu = true;
                this.form.custType = "新客户"
            },

            // 图片
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePreview(file) {
                console.log(file);
            },


        }
    }

</script>

<style>

    .clue-row {
        margin-left: 50px;
        margin-top: 15px;
    }

    .clue-form {
        width: 1140px;
        margin: auto;
        margin-top: 20px;
    }

    .wraper-form {
    }

    .carousel-div {
        /*display: block;*/
        /*height: 40px;*/
        width: 200px;
        top: 50%;

        text-align: center;
        position: relative;
        margin: 0 auto;

    }

    .el-carousel__item h3 {

        color: #475669;
        font-size: 18px;
        font-weight: bold;
        opacity: 0.75;
        line-height: 20px;
        margin: 8px 0;

    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }

    .col-span {
        font-size: 20px;
        font-weight: bold;
        color:gray;
    }
</style>