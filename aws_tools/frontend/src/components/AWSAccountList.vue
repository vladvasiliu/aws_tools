<template>
  <ObjectListGroupCard
    card-title="Accounts"
    :show-all="true"
    :loading="loading"
    :object-error="error"
    :object-list="aws_accounts"
    :route-dest-fun="routeDestFun"
    :route-dest-all="routeDestAll"
  />
</template>

<script>
import { mapGetters } from 'vuex'
import ObjectListGroupCard, { RouteDest } from './ObjectListGroupCard'
import { Error } from './ErrorView'

export default {
  components: { ObjectListGroupCard },
  props: {
    routeDestFun: { type: Function, required: true },
    routeDestAll: { type: RouteDest, required: true }
  },
  data: function () {
    return {
      loading: true,
      error: undefined
    }
  },
  computed: {
    ...mapGetters(['aws_accounts', 'aws_accounts_error'])
  },
  created () {
    this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
      .then(
        () => {},
        (err) => { this.error = new Error('Failed to load accounts', err.data) }
      )
      .finally(() => { this.loading = false })
  }
}
</script>
