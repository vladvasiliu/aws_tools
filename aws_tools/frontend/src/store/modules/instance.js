import axios_instance from '../../api/index'

const state = {
    instances: []
};
const actions = {
    LOAD_INSTANCE_LIST: function({ commit }) {
        axios_instance.get('/Instances/').then((response) => {
            commit('SET_INSTANCE_LIST', { list: response.data })
        }, (err) => {
            console.log(err)
        })
    },
};

const mutations = {
    SET_INSTANCE_LIST: (state, { list }) => { state.instances = list },
};

const getters = {
    instances: state => state.instances,
};

export default {
    state,
    getters,
    actions,
    mutations
}
