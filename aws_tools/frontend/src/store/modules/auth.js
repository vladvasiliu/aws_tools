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
  storageType: 'cookieStorage',
  providers: {
    oauth2: {
      url: '/azure/',
      name: 'AzureAD',
      redirectUri: 'http://127.0.0.1:8080/account/login/sso',
      clientId: '9bb654b1-7a7f-4969-8f02-3496e46e4511',
      authorizationEndpoint:
        'https://login.microsoftonline.com/6643a3bd-8975-46e6-a6ce-1b8025b70944/oauth2/authorize'
    }
  }
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
    isAuthenticated: () => vueAuth.isAuthenticated(),
    userName: state => state.userName,
    auth: () => vueAuth
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
    socialLogin: function (context) {
      return vueAuth
        .authenticate('oauth2')
        .then(function () {
          context.dispatch('getUser')
        })
        .catch(error => {
          console.log('sso failed :(')
          console.log(error)
          return Promise.reject(error)
        })
    },
    login (context, payload) {
      return vueAuth
        .login(payload.user, payload.requestOptions)
        .then(() => {
          context.dispatch('getUser')
        })
        .catch(error => {
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
      return vueAuth
        .logout(payload.requestOptions)
        .then(() => {
          context.dispatch('getUser')
        })
        .catch(error => {
          console.log(error)
        })
    },
    getUser (context) {
      axios
        .get('/rest-auth/user/')
        .then(response => {
          context.commit('SET_USERNAME', { userName: userName(response) })
        })
        .catch(error => {
          console.log(error.request)
        })
    }
  }
}
