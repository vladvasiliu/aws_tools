<template>
  <div class="row">
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

export default {
  components: {
    AccountList: () => ({ component: import('./AWSAccountList') })
  },
  data: function () {
    return {
      routeDestAll: new RouteDest('All', { name: 'InstanceView' })
    }
  },
  methods: {
    routeDestFun: (account) => ({ name: 'InstanceViewForAccount', params: { id: account.id } })
  }
}
</script>
