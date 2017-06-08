import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const axios_instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
});

export default new Vuex.Store({
    state: {
        aws_accounts: []
    },
    actions: {
        LOAD_AWS_ACCOUNT_LIST: function({ commit }) {
            axios_instance.get('/AWSAccounts/').then((response) => {
                commit('SET_ACCOUNT_LIST', { list: response.data })
            }, (err) => {
                console.log(err)
            })
        },
    },
    mutations: {
        SET_ACCOUNT_LIST: (state, { list }) => { state.aws_accounts = list },
    },
    getters: {
        aws_accounts: state => state.aws_accounts,
    }
})
