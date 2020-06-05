import axios from 'axios'
import Vue from 'vue'
import VueAxios from 'vue-axios'
import VueRouter from 'vue-router'
import BootstrapVue, { BVConfigPlugin } from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/css/bootstrap.css'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueMoment from 'vue-moment'
import moment from 'moment-timezone'

import App from './components/App.vue'
import store from './store'
import router from './router'

import bootstrapConfig from './bootstrap_config'

Vue.use(BVConfigPlugin, bootstrapConfig)

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.use(VueRouter)
Vue.use(VueMoment, { moment })

Vue.component('font-awesome-icon', FontAwesomeIcon)

axios.defaults.baseURL = window.location.origin + '/api'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
})
