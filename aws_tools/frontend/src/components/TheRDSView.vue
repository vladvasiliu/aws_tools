<template>
  <loading v-if="loading" />
  <error
    v-else-if="error"
    :message="error.message"
    :details="error.details"
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
      <router-view />
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import { RouteDest } from './ObjectListGroupCard'
import Loading from './loading'

export default {
  name: 'TheRDSView',
  components: {
    Loading,
    AccountList: () => ({ component: import('./AWSAccountList') }),
    Error: () => ({ component: import('./error') })
  },
  data: function () {
    return {
      routeDestAll: new RouteDest('All', { name: 'RDSView' }),
      error: undefined,
      loading: true
    }
  },
  computed: {
    ...mapGetters(['rds'])
  },
  created () {
    this.$store.dispatch('RDS_LOAD_LIST').then(
      () => {},
      (err) => {
        this.error = {
          message: 'Failed to retrieve databases',
          details: err.message
        }
      }
    ).finally(() => { this.loading = false })
  },
  methods: {
    routeDestFun: (account) => ({ name: 'RDSList', params: { id: account.id } })
  }
}
</script>

<style scoped>

</style>
