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
import router from '../router'
export default {
  name: 'Home',
  components: { NavBar },
  mounted () {
    this.$store.dispatch('getUser')
  },
  updated () {
    router.push({ name: 'InstanceView' })
  }
}
</script>

<style scoped>

</style>
