import Vue from 'vue'
import Router from 'vue-router'

import Home from '../components/main'
import AccountLogin from '../components/accountLogin'
import PageNotFound from '../components/404'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/account/login',
      name: 'AccountLogin',
      component: AccountLogin
    },
    {
      path: '*',
      name: 'PageNotFound',
      component: PageNotFound
    }
  ]
})
