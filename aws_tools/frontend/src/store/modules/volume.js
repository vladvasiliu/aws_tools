import axiosInstance from '../../api/index'

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
  UPDATE_VOLUME_LIST: (state, { new_volume_list: newVolumeList }) => {
    state.volumes = newVolumeList
  }
}

const getters = {
  volumes: state => state.volumes,
  volumes_for_instance: (state, getters) => (instance) => {
    if (instance) {
      return state.volumes.filter(volume => volume.instance === instance.url)
    } else {
      return state.volumes
    }
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
