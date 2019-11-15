import Vue from 'vue'
import Router from 'vue-router'

import HomeView from '../components/home'
import InstanceView from '../components/TheInstanceView'
import PageNotFound from '../components/404'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },
    {
      path: '/instances',
      name: 'InstanceView',
      component: InstanceView
      // meta: { requiresAuth: true }
    },
    {
      path: '*',
      name: 'PageNotFound',
      component: PageNotFound
    }
  ]
})

router.beforeEach((to, from, next) => {
  next()
})

export default router
