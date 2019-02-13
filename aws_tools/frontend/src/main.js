import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/css/bootstrap.css'

import App from './components/App.vue'
import store from './store'

Vue.use(BootstrapVue)

// eslint-disable-next-line
new Vue({
  el: '#app',
  store,
  render: h => h(App)
})
