<template>
  <div>
    <NavBar/>

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
import NavBar from './NavBar'

export default {
  components: { AccountList, InstanceList, NavBar },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },

  created () {
    if (!this.isAuthenticated) {
      this.$router.push({name: 'AccountLogin'})
    }
  }
}
</script>
