
import Vue from 'vue'
import Router from 'vue-router'


//组件模块
import Index from './views/Index.vue'
import Case from './views/Case.vue'
import Data from './views/Data.vue'
import Report from './views/Report'
import Clue from './views/Clue'
import Account from  './views/Account'
// import Logout from './views/Logout'

//
Vue.use(Router)
//
export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '*',
            redirect: '/index'
        },
        {
            path: '/index',
            name: 'index',
            component: Index
        },
        {
            path: '/case',
            name: 'case',
            component: Case
        },
        {
            path: '/data',
            name: 'data',
            component: Data
        },
        {
            path: '/report',
            name: 'report',
            component: Report
        },
        {
            path: '/clue',
            name: 'clue',
            component: Clue
        },
        {
            path: '/account',
            name: 'account',
            component: Account
        },

        // {
        //     path: '/logout',
        //     name: 'logout',
        //     component: Logout
        // },

    ]
})