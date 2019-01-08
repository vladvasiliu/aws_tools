import axios from 'axios'

export default {
  state: {
    aws_accounts: [],
    aws_account_selected: ''
  },
  actions: {
    LOAD_AWS_ACCOUNT_LIST ({ commit }) {
      axios.get('/AWSAccounts/').then(
        response => {
          commit('SET_ACCOUNT_LIST', { list: response.data })
        },
        err => {
          console.log(err)
        }
      )
    }
  },
  mutations: {
    SET_ACCOUNT_LIST: (state, { list }) => {
      state.aws_accounts = list
    },
    SET_SELECTED_ACCOUNT: (state, { account }) => {
      state.aws_account_selected = account
    }
  },
  getters: {
    aws_accounts: state => state.aws_accounts,
    aws_account_selected: state => state.aws_account_selected
  }
}
