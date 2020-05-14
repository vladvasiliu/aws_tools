<template>
  <b-card
    no-body
  >
    <template v-slot:header>
      <strong>Accounts</strong>
    </template>
    <div
      v-if="aws_accounts == null && aws_accounts_error == null"
      class="text-center"
    >
      <b-spinner />
    </div>
    <div
      v-else-if="aws_accounts == null && aws_accounts_error != null"
      v-b-tooltip.hover
      class="text-center text-danger"
      :title="aws_accounts_error"
    >
      <font-awesome-icon :icon="faExclamationTriangle" />
    </div>
    <b-list-group
      v-if="Array.isArray(aws_accounts) && aws_accounts.length > 0"
      flush
    >
      <b-list-group-item
        v-if="aws_accounts.length>1"
        :active="!selectedAccount"
        action
        @click="select()"
      >
        All
      </b-list-group-item>
      <b-list-group-item
        v-for="account in aws_accounts"
        :key="account.id"
        :active="selectedAccount === account || aws_accounts.length === 1"
        action
        @click="select(account)"
      >
        {{ account._name }}
      </b-list-group-item>
    </b-list-group>
    <div
      v-else-if="Array.isArray(aws_accounts)"
      class="text-danger"
    >
      <em>None</em>
    </div>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'

export default {
  props: {
    selectedAccount: { type: Object, default: null }
  },
  computed: {
    ...mapGetters(['aws_accounts', 'aws_accounts_error']),
    faExclamationTriangle () { return faExclamationTriangle }
  },
  created () {
    this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
  },
  methods: {
    select: function (account) {
      if (account) {
        // this.$store.commit('SET_SELECTED_ACCOUNT', { account: account })
        this.$emit('selectAccount', { account: account })
      } else {
        // this.$store.commit('SET_SELECTED_ACCOUNT', { account: null })
        this.$emit('selectAccount', { account: null })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "~bootstrap/scss/bootstrap";
  @import "~bootstrap-vue/dist/bootstrap-vue.css";

  .list-group-item.list-group-item-action {
      border-bottom: $border-width solid transparent;
  }

  .list-group-item.list-group-item-action.active {
    background: $light;
    color: $dark;
    border: $border-width solid transparent;
    font-weight: $font-weight-bolder;
  }
</style>
