import axios_instance from '../../api/index'

const state = {
    volumes: []
};
const actions = {
    LOAD_VOLUME_LIST: function({ commit }) {
        axios_instance.get('/Volumes/').then((response) => {
            commit('SET_VOLUME_LIST', { list: response.data })
        }, (err) => {
            console.log(err)
        })
    },
};

const mutations = {
    SET_VOLUME_LIST: (state, { list }) => { state.volumes = list },
};

const getters = {
    volumes: state => state.instances,
    volumes_for_selected_instance : (state, instance) => {
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