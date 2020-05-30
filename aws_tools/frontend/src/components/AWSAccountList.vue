<template>
  <ObjectListGroupCard
    card-title="Accounts"
    :show-all="true"
    :object-error="aws_accounts_error"
    :object-list="aws_accounts"
    :route-dest-fun="routeDestFun"
    :route-dest-all="routeDestAll"
  />
</template>

<script>
import { mapGetters } from 'vuex'
import ObjectListGroupCard, { RouteDest } from './ObjectListGroupCard'

export default {
  components: { ObjectListGroupCard },
  props: {
    routeDestFun: { type: Function, required: true },
    routeDestAll: { type: RouteDest, required: true }
  },
  computed: {
    ...mapGetters(['aws_accounts', 'aws_accounts_error'])
  },
  created () {
    this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
  }
}
</script>
