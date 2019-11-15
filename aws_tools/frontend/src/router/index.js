import Vue from 'vue'
import Router from 'vue-router'

import HomeView from '../components/home'
import TheInstanceView from '../components/TheInstanceView'
import TheSecurityGroupView from '../components/TheSecurityGroupView'
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
      component: TheInstanceView
      // meta: { requiresAuth: true }
    },
    {
      path: '/security_groups',
      name: 'SecurityGroupView',
      component: TheSecurityGroupView
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
