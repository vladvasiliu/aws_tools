import Vue from 'vue'
import VueAxios from 'vue-axios'
import { VueAuthenticate } from 'vue-authenticate'
import axios from 'axios'

Vue.use(VueAxios, axios)

const vueAuth = new VueAuthenticate(Vue.prototype.$http, {
  baseUrl: 'http://127.0.0.1:8000/api/rest-auth/',
  loginUrl: 'login/',
  tokenName: 'key',
  tokenType: 'Token',
  storageType: 'cookieStorage'
})

function userName (response) {
  const fullName = `${response.data.first_name} ${response.data.last_name}`
  return fullName !== ' ' ? fullName : response.data.username
}

export default {
  state: {
    userName: null
  },

  getters: {
    // isAuthenticated: (state) => state.isAuthenticated,
    isAuthenticated () { return vueAuth.isAuthenticated() },
    userName: (state) => state.userName
  },

  mutations: {
    SET_USERNAME (state, payload) {
      if (payload.userName) {
        state.userName = payload.userName
      } else {
        state.userName = null
      }
    }
  },

  actions: {
    login (context, payload) {
      return vueAuth.login(payload.user, payload.requestOptions)
        .then(() => {
          context.dispatch('getUser')
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
    },
    logout (context, payload) {
      return vueAuth.logout(payload.requestOptions)
        .then(() => {
          context.dispatch('getUser')
        })
        .catch((error) => {
          console.log(error)
        })
    },
    getUser (context) {
      axios.get('/rest-auth/user/')
        .then((response) => {
          context.commit('SET_USERNAME', {userName: userName(response)})
        })
        .catch((error) => {
          console.log(error.request)
        })
    }
  }
}
