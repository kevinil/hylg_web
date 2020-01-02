import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import router from './router'
import axios from 'axios'

import global_ from './components/Global'//引用文件
Vue.prototype.GLOBAL = global_//挂载到Vue实例上面
// import 'css/override-element-ui.css';
// import VueAxios from 'vue-axios'

axios.defaults.baseURL = 'http://10.89.124.47:8000'
Vue.prototype.$axios = axios

// Vue.use(VueAxios, axios)
Vue.config.productionTip = false

new Vue({
    el: "#app",
    router,
    render: h => h(App),
})



// new Vue({
//     el:"#app",
//     router,
//     render: h => h(App),
// }).$mount('#app')