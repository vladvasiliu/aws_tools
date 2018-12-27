<template>
  <div class="container">
    <div class="row">
      <button @click="login">Login</button>
    </div>
    <span class="row mt-3">Is authenticated ? {{ isAuthenticated }}</span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'isAuthenticated'
    ])
  },
  methods: {
    login () {
      this.$store.dispatch('login', {user: {username: 'vlad', password: '123'}}).then(() => {
        console.log('Logged in. Redirecting...')
        this.$router.push({name: 'Home'})
      })
    }
  }
}
</script>
