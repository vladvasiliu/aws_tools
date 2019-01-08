import axios from 'axios'
import Vue from 'vue'
import VueAxios from 'vue-axios'
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/css/bootstrap.css'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import App from './components/App.vue'
import store from './store'
import router from './router'

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.use(VueRouter)
Vue.use(require('vue-moment'))

Vue.component('font-awesome-icon', FontAwesomeIcon)

axios.defaults.baseURL = process.env.VUE_APP_AXIOS_BASE_URL

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
})
