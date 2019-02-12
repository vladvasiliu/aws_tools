<template>
    <b-card header="Accounts">
        <b-list-group flush>
            <b-list-group-item action @click="select()" v-bind:active="!aws_account_selected"><small>All</small></b-list-group-item>
            <b-list-group-item action @click="select(account)" v-bind:active="aws_account_selected == account" v-for="account in aws_accounts" :key="account.id"><small>{{account._name}}</small></b-list-group-item>
        </b-list-group>
    </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
//        computed: {
//            accounts_list: function () { return this.$store.state.aws_accounts },
//        },
  computed: {
    ...mapGetters([
      'aws_accounts',
      'aws_account_selected'
    ])
  },
  created () {
    this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
  },
  methods: {
    select: function (account) {
      if (account) {
        this.$store.commit('SET_SELECTED_ACCOUNT', { account: account })
      } else {
        this.$store.commit('SET_SELECTED_ACCOUNT', { account: null })
      }
    }
  }
}
</script>
