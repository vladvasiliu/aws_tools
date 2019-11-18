<template>
  <div id="app">
    <NavBar />

    <div
      v-if="userName"
      class="container mt-3 mb-3"
    >
      <router-view />
    </div>
    <Unauthorized v-else />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import NavBar from './TheNavBar'
import Unauthorized from './403'

export default {
  components: {
    NavBar,
    Unauthorized
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
