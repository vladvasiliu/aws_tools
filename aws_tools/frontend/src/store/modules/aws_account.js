import axiosInstance from '../../api/index'

const state = {
  aws_accounts: [],
  aws_account_selected: ''
}
const actions = {
  LOAD_AWS_ACCOUNT_LIST: function ({ commit }) {
    axiosInstance.get('/AWSAccounts/').then((response) => {
      commit('SET_ACCOUNT_LIST', { list: response.data })
    }, (err) => {
      console.log(err)
    })
  }
}

const mutations = {
  SET_ACCOUNT_LIST: (state, { list }) => { state.aws_accounts = list },
  SET_SELECTED_ACCOUNT: (state, { account }) => {
    state.aws_account_selected = account
  }
}

const getters = {
  aws_accounts: state => state.aws_accounts,
  aws_account_selected: state => state.aws_account_selected
}

export default {
  state,
  getters,
  actions,
  mutations
}
