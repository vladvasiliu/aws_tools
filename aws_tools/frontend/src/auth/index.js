import Vue from 'vue'
import VueAxios from 'vue-axios'
import { VueAuthenticate } from 'vue-authenticate'
import axios from 'axios'

import axiosInstance from '@/api/'

Vue.use(VueAxios, axios)

const vueAuth = new VueAuthenticate(Vue.prototype.$http, {
  baseUrl: 'http://127.0.0.1:8000/rest-auth/',
  loginUrl: 'login/',
  tokenName: 'key',
  storageType: 'memoryStorage'

})

export default {
  state: {
    isAuthenticated: false,
    token: null
  },

  getters: {
    isAuthenticated: (state) => state.isAuthenticated
  },

  mutations: {
    IS_AUTHENTICATED (state, payload) {
      state.isAuthenticated = payload.isAuthenticated
      state.token = payload.token
    }
  },

  actions: {
    login (context, payload) {
      return vueAuth.login(payload.user, payload.requestOptions)
        .then(() => {
          const isAuthenticated = vueAuth.isAuthenticated()
          const token = vueAuth.getToken()
          context.commit('IS_AUTHENTICATED', {
            isAuthenticated: isAuthenticated,
            token: token
          })
          if (token) {
            axiosInstance.defaults.headers.common['Authorization'] = 'Token ' + token
          }
        })
    }
  }
}
