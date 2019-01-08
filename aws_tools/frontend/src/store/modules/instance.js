import axios from 'axios'

const state = {
  instances: []
}
const actions = {
  LOAD_INSTANCE_LIST: function ({ commit }) {
    return axios.get('/Instances/').then(
      response => {
        commit('SET_INSTANCE_LIST', { list: response.data })
      },
      err => {
        console.log(err)
      }
    )
  },
  UPDATE_INSTANCE: function ({ commit }, newValue) {
    axios.put(newValue.instance.url, newValue.changes).then(response => {
      commit('UPDATE_INSTANCE', { newInstance: response.data })
    })
  }
}

const mutations = {
  SET_INSTANCE_LIST: (state, { list }) => {
    state.instances = list
  },
  UPDATE_INSTANCE: (state, { newInstance }) => {
    state.instances = state.instances.map(instance => {
      if (instance.id === newInstance.id) {
        return Object.assign({}, instance, newInstance)
      }
      return instance
    })
  }
}

const getters = {
  instances: state => state.instances,
  instances_for_selected_account: (state, getters) => {
    if (getters.aws_account_selected) {
      return state.instances.filter(
        instance => instance.aws_account === getters.aws_account_selected.url
      )
    } else {
      return state.instances
    }
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
