import Vue from 'vue'
import Vuex from 'vuex'

import awsAccount from './modules/aws_account'
import instance from './modules/instance'
import auth from './modules/auth'
import rds from './modules/rds'
import securityGroup from './modules/SecurityGroup'
import schedule from './modules/schedule'

Vue.use(Vuex)

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  modules: {
    aws_account: awsAccount,
    auth,
    instance,
    rds,
    schedule,
    securityGroup
  }
})
