import Vue from 'vue'
import Router from 'vue-router'

// import auth from '../store'

import HomeView from '../components/home'
import TheInstanceView from '../components/TheInstanceView'
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
      component: TheInstanceView,
      children: [
        {
          path: '',
          name: 'InstanceView',
          component: () => import('../components/InstanceList')
        },
        {
          name: 'InstanceViewForAccount',
          path: 'for_account/:id',
          component: () => import('../components/InstanceList'),
          props: (route) => ({ selectedAccountID: route.params.id })
        }
      ]
      // meta: { requiresAuth: true }
    },
    {
      path: '/security_groups',
      name: 'SecurityGroupView',
      component: () => import('../components/TheSecurityGroupView'),
      children: [
        { path: 'by_account', component: () => import('../components/TheSecurityGroupByAccount'), name: 'SecGroupByAccount' },
        { path: 'by_source', component: () => import('../components/TheSecurityGroupBySource'), name: 'SecGroupBySource' }
      ]
    },
    {
      path: '/schedules',
      component: () => import('../components/TheScheduleView'),
      children: [
        {
          path: '',
          name: 'ScheduleView',
          component: () => import('../components/NothingSelected'),
          props: { title: 'No schedule selected', message: 'Please select a schedule' }
        },
        {
          path: 'new',
          name: 'ScheduleViewNew',
          component: () => import('../components/ScheduleDetail')
        },
        {
          path: ':id(\\d+)',
          name: 'ScheduleViewID',
          component: () => import('../components/ScheduleDetail'),
          props: (route) => ({ selectedScheduleID: parseInt(route.params.id) })
        }
      ]
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
