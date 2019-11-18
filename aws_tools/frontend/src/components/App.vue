<template>
  <div id="app">
    <NavBar />

    <div
      v-if="userName"
      class="container mt-3 mb-3"
    >
      <router-view />
    </div>
    <unauthorized v-else />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  components: {
    NavBar: () => import('./TheNavBar'),
    Unauthorized: () => import('./403')
  },
  computed: {
    ...mapGetters(['userName'])
  },
  beforeCreate () {
    document.title = 'AWS Tools'
    this.$store.dispatch('getUser')
    // .then(() => {
    //   this.$router.push({ name: 'InstanceView' })
    // })
    // .catch(() => {
    //   this.$router.replace({ name: 'UnauthorizedView' })
    // })
  }
}
</script>
