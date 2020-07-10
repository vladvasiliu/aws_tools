<template>
  <loading v-if="loading" />
  <error-view
    v-else-if="error"
    :error="error"
  />
  <div
    v-else
    class="row"
  >
    <div class="col-3">
      <account-list
        :route-dest-fun="routeDestFun"
        :route-dest-all="routeDestAll"
      />
    </div>
    <div class="col">
      <router-view />
    </div>
  </div>
</template>

<script>
import { RouteDest } from './ObjectListGroupCard'
import Loading from './loading'
import { Error } from './ErrorView'

export default {
  components: {
    ErrorView: () => (import('./ErrorView')),
    Loading,
    AccountList: () => ({ component: import('./AWSAccountList') })
  },
  data: function () {
    return {
      routeDestAll: new RouteDest('All', { name: 'InstanceView' }),
      error: undefined,
      loading: true
    }
  },
  mounted () {
    this.$store.dispatch('LOAD_INSTANCE_LIST')
      .then(
        () => {},
        (err) => { this.error = new Error('Failed to retrieve instances', err.message) }
      )
      .finally(() => { this.loading = false })
  },
  methods: {
    routeDestFun: (account) => ({ name: 'InstanceViewForAccount', params: { id: account.id } })
  }
}
</script>
