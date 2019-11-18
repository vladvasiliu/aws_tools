import Vue from 'vue'
import VueAxios from 'vue-axios'
import axios from 'axios'
// import router from '@/router/'

Vue.use(VueAxios, axios)

function userName (response) {
  const fullName = `${response.data.first_name} ${response.data.last_name}`
  return fullName !== ' ' ? fullName : response.data.username
}

export default {
  state: {
    userName: null
  },

  getters: {
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
    getUser (context) {
      return axios
        .get('/user/')
        .then(response => {
          context.commit('SET_USERNAME', { userName: userName(response) })
        })
        .catch(error => {
          if (error.response && error.response.status === 403) {
            console.error('Unauthenticated')
          } else {
            console.error(error.request)
          }
        })
    }
  }
}
