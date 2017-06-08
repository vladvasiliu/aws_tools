import axios from 'axios'

const axios_instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
});

const state = {
    aws_accounts: []
};
const actions = {
    LOAD_AWS_ACCOUNT_LIST: function({ commit }) {
        axios_instance.get('/AWSAccounts/').then((response) => {
            commit('SET_ACCOUNT_LIST', { list: response.data })
        }, (err) => {
            console.log(err)
        })
    },
};

const mutations = {
    SET_ACCOUNT_LIST: (state, { list }) => { state.aws_accounts = list },
};

const getters = {
    aws_accounts: state => state.aws_accounts,
};

export default {
    state,
    getters,
    actions,
    mutations
}
