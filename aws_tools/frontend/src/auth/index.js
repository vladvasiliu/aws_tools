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
  storageType: 'cookieStorage'

})

export default {
  state: {
    isAuthenticated: vueAuth.isAuthenticated(),
    token: vueAuth.getToken()
  },

  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    token: (state) => state.token
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
        .catch((error) => {
          let message = null
          if (error.response) {
            if (error.response.status === 400) {
              message = 'Invalid credentials'
            } else {
              message = 'Internal server error'
            }
          } else {
            message = 'Cannot contact backend server'
          }
          return Promise.reject(new Error(message))
        })
    }
  }
}
