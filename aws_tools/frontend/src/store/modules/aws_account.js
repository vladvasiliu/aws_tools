import axios from 'axios'

export default {
  state: {
    aws_accounts: null,
    aws_accounts_error: null
  },
  actions: {
    LOAD_AWS_ACCOUNT_LIST ({ commit }) {
      axios.get('/AWSAccounts/').then(
        response => {
          commit('SET_ACCOUNT_LIST', { list: response.data })
        },
        err => {
          console.error(err)
          commit('SET_ACCOUNTS_ERROR', { error: err })
        }
      )
    }
  },
  mutations: {
    SET_ACCOUNT_LIST: (state, { list }) => {
      state.aws_accounts = list
    },
    SET_ACCOUNTS_ERROR: (state, { error }) => {
      state.aws_accounts_error = error.message
    }
  },
  getters: {
    aws_accounts: state => state.aws_accounts,
    aws_accounts_error: state => state.aws_accounts_error
  }
}
