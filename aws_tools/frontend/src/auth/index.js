import Vue from 'vue'
import Vuex from 'vuex'
import VueAxios from 'vue-axios'
import { VueAuthenticate } from 'vue-authenticate'
import axios from 'axios'

Vue.use(Vuex)
Vue.use(VueAxios, axios)

const state = {}

const vueAuth = new VueAuthenticate(Vue.prototype.$http, {
  baseUrl: 'http://127.0.0.1:8000/rest-auth/',
  loginUrl: 'login/',
  tokenName: 'key',
  storageArea: 'cookies'
})

const getters = {
  isAuthenticated: () => {
    return vueAuth.isAuthenticated()
  }
}

const mutations = {
  isAuthenticated (state, payload) {
    state.isAuthenticated = payload.isAuthenticated
  }
}

const actions = {
  login (context, payload) {
    vueAuth.login(payload.user, payload.requestOptions).then(() => {
      context.commit('isAuthenticated', {
        isAuthenticated: vueAuth.isAuthenticated()
      })
    }).then()
      .catch((error) => {
        console.log(error)
      })
  }
}

export default {
  auth: vueAuth,
  state,
  getters,
  actions,
  mutations
}
