<template>
  <div id="app">
    <NavBar />

    <div class="container mt-3 mb-3">
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from './TheNavBar'

export default {
  components: { NavBar },
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
