import Vue from 'vue'
import VueAxios from 'vue-axios'
import { VueAuthenticate } from 'vue-authenticate'
import axios from 'axios'
import router from '@/router/'

Vue.use(VueAxios, axios)

const vueAuth = new VueAuthenticate(Vue.prototype.$http, {
  baseUrl: process.env.VUE_APP_AXIOS_BASE_URL + '/rest-auth/',
  loginUrl: 'login/',
  tokenName: 'key',
  tokenType: 'Token',
  storageType: 'cookieStorage',
  providers: {
    oauth2: {
      url: '/azure/',
      name: 'AzureAD',
      redirectUri:
        window.location.origin + router.options.routes.find(route => route.name === 'AccountLoginSSO').path,
      clientId: process.env.VUE_APP_SSO_AZUREAD_CLIENTID,
      authorizationEndpoint: process.env.VUE_APP_SSO_AZUREAD_AUTHORIZATION_ENDPOINT
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
    userName: state => state.userName
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
