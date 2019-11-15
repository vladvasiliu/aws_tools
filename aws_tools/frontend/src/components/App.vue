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
  created () {
    document.title = 'AWS Tools'
  }
}
</script>
