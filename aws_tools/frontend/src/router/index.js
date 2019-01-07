import Vue from 'vue'
import Router from 'vue-router'

import Home from '../components/main'
import AccountLogin from '../components/accountLogin'
import PageNotFound from '../components/404'
import auth from '@/store/modules/auth'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/account/login',
      name: 'AccountLogin',
      component: AccountLogin
    },
    {
      path: '/account/login/sso',
      name: 'AccountLoginSSO',
      component: AccountLogin
    },
    {
      path: '*',
      name: 'PageNotFound',
      component: PageNotFound
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!auth.getters.isAuthenticated()) {
      next({
        name: 'AccountLogin',
        query: { redirect: to.fullPath }
      })
    }
  }
  next()
})

export default router
