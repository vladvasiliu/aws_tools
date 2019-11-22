import axios from 'axios'
import Vue from 'vue'

export default {
  state: {
    securityGroupList: [],
    securityGroupRules: [],
    securityGroupIPRanges: [],
    securityGroupUserGroupPairs: []
  },
  actions: {
    getSecurityGroupList ({ commit }) {
      axios.get('/SecurityGroups').then(
        response => { commit('SET_SECURITY_GROUP_LIST', { list: response.data }) },
        err => { console.error(err) }
      )
    },
    getSecurityGroupRules ({ commit }, securityGroup) {
      axios.get(securityGroup.rule_list).then(
        response => { commit('ADD_SECURITY_GROUP_RULES', { list: response.data }) },
        err => { console.error(err) }
      )
    }
  },
  mutations: {
    SET_SECURITY_GROUP_LIST: (state, { list }) => {
      Vue.set(state, 'securityGroupList', list)
    },
    SET_SECURITY_GROUP_IP_RANGES: (state, { list }) => {
      state.securityGroupIPRanges = list
    },
    SET_SECURITY_GROUP_USER_GROUP_PAIRS: (state, { list }) => {
      state.securityGroupUserGroupPairs = list
    },
    ADD_SECURITY_GROUP_RULES: (state, { list }) => {
      state.securityGroupRules.push(...list)
    }
  },
  getters: {
    securityGroupList: state => {
      return state.securityGroupList
    }
  }
}
