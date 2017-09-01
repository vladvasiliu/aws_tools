import axios_instance from '../../api/index'

const state = {
    volumes: []
};
const actions = {
    GET_ALL_VOLUMES: function({ commit }) {
        axios_instance.get('/Volumes/').then((response) => {
            commit('UPDATE_VOLUME_LIST', { new_volume_list: response.data })
        }, (err) => {
            console.log(err)
        })
    },
};

const mutations = {
    UPDATE_VOLUME_LIST: (state, { new_volume_list }) => {
        state.volumes = new_volume_list;
    },
};

const getters = {
    volumes: state => state.volumes,
    volumes_for_instance : (state, getters) => (instance) => {
        if (instance) {
            return state.volumes.filter(volume => volume.instance === instance.url);
        } else {
            return state.volumes;
        }
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}