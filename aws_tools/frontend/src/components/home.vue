<template>
  <div>
    <NavBar />

    <div class="container mt-3 mb-3">
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar'
export default {
  name: 'Home',
  components: { NavBar },
  mounted () {
    this.$store.dispatch('getUser')
  }
}
</script>

<style scoped>

</style>
