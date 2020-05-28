<template>
  <div class="row">
    <div class="col-3">
      <account-list
        :route-dest="routeDest"
        :route-dest-all="routeDestAll"
      />
    </div>
    <div class="col">
      <router-view />
    </div>
  </div>
</template>

<script>
import { RouteDestAll } from './ObjectListGroupCard'

export default {
  components: {
    AccountList: () => ({ component: import('./AWSAccountList') })
  },
  data: function () {
    return {
      routeDestAll: new RouteDestAll('All', { name: 'InstanceView' })
    }
  },
  methods: {
    routeDest: (account) => ({ name: 'InstanceViewForAccount', params: { id: account.id } })
  }
}
</script>
