<template>
  <b-card
    header="Accounts"
    body-class="px-0"
  >
    <b-list-group
      v-if="Array.isArray(aws_accounts) && aws_accounts.length > 0"
      flush
    >
      <b-list-group-item
        v-if="aws_accounts.length>1"
        :active="!aws_account_selected"
        action
        @click="select()"
      >
        All
      </b-list-group-item>
      <b-list-group-item
        v-for="account in aws_accounts"
        :key="account.id"
        :active="aws_account_selected === account || aws_accounts.length === 1"
        action
        @click="select(account)"
      >
        {{ account._name }}
      </b-list-group-item>
    </b-list-group>
    <div
      v-else
      class="text-danger"
    >
      <em>None</em>
    </div>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  //        computed: {
  //            accounts_list: function () { return this.$store.state.aws_accounts },
  //        },
  computed: {
    ...mapGetters(['aws_accounts', 'aws_account_selected'])
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

<style scoped>
/* Workaround for broken modal display */
.list-group-item.active {
  z-index: 0;
}
</style>
