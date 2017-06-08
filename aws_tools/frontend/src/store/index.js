import Vue from 'vue'
import Vuex from 'vuex'

import aws_account from './modules/aws_account'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        aws_account
    }
})
