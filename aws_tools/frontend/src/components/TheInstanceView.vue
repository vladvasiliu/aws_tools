<template>
  <div class="row">
    <div class="col-3">
      <account-list
        :selected-account="selectedAccount"
        @selectAccount="selectAccount"
      />
    </div>
    <div class="col">
      <instance-list :selected-account="selectedAccount" />
    </div>
  </div>
</template>

<script>
// import AccountList from './account_list.vue'
// import InstanceList from './instance_list.vue'

export default {
  components: {
    AccountList: () => ({ component: import('./account_list') }),
    InstanceList: () => ({ component: import('./instance_list') })
  },
  data: function () {
    return {
      selectedAccount: null
    }
  },
  methods: {
    selectAccount: function (event) {
      this.selectedAccount = event.account
    }
  }
}
</script>
