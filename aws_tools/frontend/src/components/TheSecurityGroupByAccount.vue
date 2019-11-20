<template>
  <div class="row">
    <div class="col-3">
      <account-list
        :selected-account="selectedAccount"
        @selectAccount="selectAccount"
      />
    </div>
    <div class="col">
      <security-group-list :selected-account="selectedAccount" />
    </div>
  </div>
</template>

<script>
import AccountList from './account_list'
import SecurityGroupList from './SecurityGroupList'

export default {
  name: 'TheSecurityGroupByAccount',

  components: {
    SecurityGroupList,
    AccountList
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

<style scoped>

</style>
