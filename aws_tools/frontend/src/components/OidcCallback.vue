<template>
  <loading v-if="loading" />
  <error-view
    v-else-if="error"
    :error="error"
  />
</template>

<script>
import { mapActions } from 'vuex'
import Loading from './loading'
import { Error } from './ErrorView'

export default {
  name: 'OidcCallback',
  components: {
    Loading,
    ErrorView: () => (import('./ErrorView'))
  },
  data: () => {
    return {
      error: undefined,
      loading: true
    }
  },
  mounted () {
    this.oidcSignInCallback()
      .then((redirectedPath) => {
        this.$router.push(redirectedPath)
      })
      .catch((err) => {
        this.error = new Error('Authorization failed', err.message)
      })
      .finally(() => { this.loading = false })
  },
  methods: {
    ...mapActions(['oidcSignInCallback'])
  }
}
</script>

<style scoped>

</style>
