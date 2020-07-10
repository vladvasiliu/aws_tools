<template>
  <loading v-if="loading" />
  <error-view
    v-else-if="error"
    :error="error"
  />
  <b-row
    v-else
    align-h="between"
  >
    <b-col cols="3">
      <account-list
        :route-dest-all="routeDestAll"
        :route-dest-fun="routeDestFun"
      />
    </b-col>
    <b-col>
      <router-view :schedule-list="scheduleSelectOptions" />
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import { RouteDest } from './ObjectListGroupCard'
import Loading from './loading'
import { Error } from './ErrorView'

export default {
  name: 'TheRDSView',
  components: {
    Loading,
    AccountList: () => ({ component: import('./AWSAccountList') }),
    ErrorView: () => ({ component: import('./ErrorView') })
  },
  data: function () {
    return {
      routeDestAll: new RouteDest('All', { name: 'RDSView' }),
      error: undefined,
      loading: true
    }
  },
  computed: {
    ...mapGetters(['rds', 'scheduleSelectOptions'])
  },
  created () {
    this.$store.dispatch('RDS_LOAD_LIST').then(
      () => {},
      (err) => {
        this.error = new Error('Failed to retrieve databases', err.message)
      }
    ).finally(() => { this.loading = false })
    this.$store.dispatch('SCHEDULE_LOAD_LIST').then(() => {}, () => {})
  },
  methods: {
    routeDestFun: (account) => ({ name: 'RDSList', params: { id: account.id } })
  }
}
</script>

<style scoped>

</style>
