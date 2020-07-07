import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'

import awsAccount from './modules/aws_account'
import instance from './modules/instance'
import rds from './modules/rds'
import securityGroup from './modules/SecurityGroup'
import schedule from './modules/schedule'

import { vuexOidcCreateStoreModule } from 'vuex-oidc'
import { oidcSettings } from '../oidc_config'

Vue.use(Vuex)

function setAuthToken (user) {
  axios.defaults.headers.common.Authorization = 'JWT ' + user.id_token
}

function unsetAuthToken () {
  delete axios.defaults.headers.common.Authorization
}

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  modules: {
    aws_account: awsAccount,
    instance,
    rds,
    schedule,
    securityGroup,
    oidcStore: vuexOidcCreateStoreModule(
      oidcSettings,
      { dispatchEventsOnWindow: true },
      {
        userLoaded: (user) => setAuthToken(user),
        userUnloaded: () => unsetAuthToken(),
        accessTokenExpired: () => unsetAuthToken(),
        silentRenewError: () => unsetAuthToken(),
        userSignedOut: () => unsetAuthToken()
      })
  }
})
