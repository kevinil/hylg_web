<template>
    <div id="account">
        <div class="main-cnt">
            <div class="profile">
                <el-tabs type="border-card">
                    <el-tab-pane label="个人资料">
                        <el-col :span="10">
                            <span style="font-size: larger;">用户名:</span>
                            <span style="text-shadow:1px 1px 3px rgba(31,47,61,0.47);font-size:40px;font-weight: bold;color: #25344e;margin-left: 10px;">
                                {{ this.userName }}</span>
                        </el-col>
                    </el-tab-pane>
                    <el-tab-pane label="更改密码">
                        <el-col :span="18" :offset="3" style="margin-top: 10px;">
                            <el-input placeholder="请输入新密码" v-model="psd1">
                                <template slot="prepend">新密码</template>
                            </el-input>
                        </el-col>
                        <el-col :span="18" :offset="3" style="margin-top: 20px;">
                            <el-input placeholder="请再次输入新密码" v-model="psd2">
                                <template slot="prepend">新密码</template>
                            </el-input>
                        </el-col>
                        <el-col :span="18" :offset="3" style="margin-top: 20px;" @disabled="btnAble">
                            <el-button type="primary" style="display:block;margin:20px auto;" @click="psdChanged">
                                确认修改
                            </el-button>
                        </el-col>

                    </el-tab-pane>
                </el-tabs>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        data() {
            return {
                userName: '',
                psd1: '',
                psd2: '',
                btnAble: true,
                changeTimer: null,
            }

        },

        created() {
            this.$axios.post('/user/', JSON.stringify({getData: "user"})).then(res => {
                this.userName = res.data[0]
                console(this.userName)
            })


        },
        methods: {
            showNotify(text, type) {
                this.$notify({
                    title: '警告',
                    message: text,
                    type: type,
                    duration: 3000,
                    offset: 100
                });
            },
            psdChanged() {
                this
                if (!this.psd1 || !this.psd2) {
                    this.showNotify("密码不能为空", 'warning')
                } else if (this.psd1 != this.psd2) {
                    this.showNotify("两次密码输入不一致", 'warning')
                } else {
                    this.btnAble = false
                    this.showNotify("修改密码成功，3秒后退出登陆", 'success')
                    this.changeTimer = setTimeout(() => {
                        this.$axios.post('/user/', JSON.stringify({
                            getData: "psd",
                            name: this.userName,
                            psd: this.psd1
                        })).then(res => {
                            this.userName = res.data[0]
                            console(this.userName)
                        })
                        window.location.href = '/logout';
                    }, 3000)
                }

            }
        },
    }
</script>

<style scoped>

    .profile {
        width: 800px;
        margin: auto;
        margin-top: 20px;

    }

</style>