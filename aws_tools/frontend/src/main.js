import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue';

import App from './components/App.vue'
import store from './store'

Vue.use(BootstrapVue);

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
    el: '#app',
    store,
    render: h => h(App)
});
