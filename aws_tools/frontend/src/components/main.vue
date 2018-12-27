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
import { mapGetters } from 'vuex'
import AccountList from './account_list.vue'
import InstanceList from './instance_list.vue'

export default {
  components: { AccountList, InstanceList },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  created () {
    console.log(this.isAuthenticated)
    if (!this.isAuthenticated) {
      console.log('not authenticated, redirecting...')
      this.$router.push({name: 'AccountLogin'})
    } else {
      console.log('authenticated')
    }
  }
}
</script>
