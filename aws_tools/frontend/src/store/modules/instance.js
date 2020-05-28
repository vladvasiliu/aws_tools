import axios from 'axios'

const state = {
  instances: []
}

export class Instance {
  constructor (instance = {}) {
    this.id = instance.id
    this.url = instance.url
    this.ebsvolume_set = instance.ebsvolume_set
    this.name = instance.name
    this.aws_account = instance.aws_account
    this.schedule = instance.schedule
    this.present = instance.present
    this.region_name = instance.region_name
    this.backup_time = instance.backup_time
    this.backup = instance.backup
  }
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
    axios.patch(newValue.instance.url, newValue.changes).then(response => {
      commit('UPDATE_INSTANCE', { newInstance: response.data })
    })
  }
}

const mutations = {
  SET_INSTANCE_LIST: (state, { list }) => {
    state.instances = list.map(i => new Instance(i))
  },
  UPDATE_INSTANCE: (state, { newInstance }) => {
    state.instances = state.instances.map(instance => {
      if (instance.id === newInstance.id) {
        return Object.assign(instance, newInstance)
      }
      return instance
    })
  }
}

const getters = {
  instances: state => state.instances
}

export default {
  state,
  getters,
  actions,
  mutations
}
