import axiosInstance from '@/api/'

const state = {
  volumes: []
}

const actions = {
  GET_ALL_VOLUMES: function ({ commit }) {
    axiosInstance.get('/Volumes/').then((response) => {
      commit('UPDATE_VOLUME_LIST', { newVolumeList: response.data })
    }, (err) => {
      console.log(err)
    })
  }
}

const mutations = {
  UPDATE_VOLUME_LIST: (state, { newVolumeList }) => {
    state.volumes = newVolumeList
  }
}

const getters = {
  volumes: state => state.volumes,
  volumes_for_instance: (state) => (instance) => {
    if (instance) {
      return state.volumes.filter(volume => volume.instance === instance.url)
    } else {
      return state.volumes
    }
  },
  volume_name: () => (volume) => { return volume._name || volume.id }
}

export default {
  state,
  getters,
  actions,
  mutations
}
