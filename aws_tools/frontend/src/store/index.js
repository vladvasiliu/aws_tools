import Vue from 'vue'
import Vuex from 'vuex'

import awsAccount from './modules/aws_account'
import instance from './modules/instance'
import volume from './modules/volume'

import auth from '@/auth/'

Vue.use(Vuex)

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  modules: {
    aws_account: awsAccount,
    instance,
    volume,
    auth
  }
})
