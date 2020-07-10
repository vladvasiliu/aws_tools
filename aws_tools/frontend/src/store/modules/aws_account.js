import axios from 'axios'

export default {
  state: {
    aws_accounts: null
  },
  actions: {
    LOAD_AWS_ACCOUNT_LIST ({ commit }) {
      return new Promise((resolve, reject) =>
        axios.get('/AWSAccounts/').then(
          response => {
            commit('SET_ACCOUNT_LIST', { list: response.data })
            resolve()
          },
          err => {
            commit('SET_ACCOUNTS_ERROR', { error: err })
            reject(err.toJSON())
          }
        )
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
