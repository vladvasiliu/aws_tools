<template>
  <div>
    <b-navbar
      type="dark"
      variant="dark">

      <b-navbar-brand>
        <span>AWS Tools</span>
      </b-navbar-brand>

    </b-navbar>

    <div class="container-fluid mt-3">
      <div class="row">
        <div class="col-2">
          <account-list/>
        </div>
        <div class="col">
          <instance-list/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccountList from './account_list.vue'
import InstanceList from './instance_list.vue'

export default {
  components: { AccountList, InstanceList },
  created () {
    if (!this.$store.getters.isAuthenticated) {
      console.log('not authenticated, redirecting...')
      this.$router.push({name: 'AccountLogin'})
    } else {
      console.log('authenticated')
    }
  }
}

</script>
