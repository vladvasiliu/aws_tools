import Vue from 'vue'
import Router from 'vue-router'

// import auth from '../store'

import HomeView from '../components/home'
import TheInstanceView from '../components/TheInstanceView'
import TheSecurityGroupView from '../components/TheSecurityGroupView'
import PageNotFound from '../components/404'
import Unauthorized from '../components/403'

Vue.use(Router)

const index = new Router({
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
      path: '/403',
      name: 'UnauthorizedView',
      component: Unauthorized
    },
    {
      path: '*',
      name: 'PageNotFound',
      component: PageNotFound
    }
  ]
})

// index.beforeEach((to, from, next) => {
//   console.log('to: ', to)
//   if (to.name !== 'UnauthorizedView' && auth.getters.isAuthenticated() === null) {
//     next({ name: 'UnauthorizedView', replace: true })
//   } else {
//     next()
//   }
// })

export default index
