<template>
  <ObjectListGroupCard
    card-title="Accounts"
    :show-all="true"
    :object-error="aws_accounts_error"
    :object-list="aws_accounts"
    :selected-object="selectedAccount"
    @selectObject="select"
  />
</template>

<script>
import { mapGetters } from 'vuex'
import ObjectListGroupCard from './ObjectListGroupCard'

export default {
  components: { ObjectListGroupCard },
  props: {
    selectedAccount: { type: Object, default: null }
  },
  computed: {
    ...mapGetters(['aws_accounts', 'aws_accounts_error'])
  },
  created () {
    this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
  },
  methods: {
    select: function (account) {
      this.$emit('selectAccount', { account: account })
    }
  }
}
</script>
