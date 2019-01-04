<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: { ...mapGetters(['isAuthenticated']) },

  created () {
    if (!this.isAuthenticated) {
      this.$router.push({name: 'AccountLogin'})
    } else {
      this.$store.dispatch('getUser')
    }
  }
}
</script>
