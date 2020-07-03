<template>
  <div id="app">
    <NavBar />
    <loading v-if="loading" />
    <error-view
      v-else-if="error"
      :error="error"
    />
    <div
      v-else
      class="container mt-3 mb-3"
    >
      <router-view />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Error } from './ErrorView'
import Loading from './loading'

export default {
  components: {
    Loading,
    ErrorView: () => import('./ErrorView'),
    NavBar: () => import('./TheNavBar')
  },
  data: function () {
    return {
      loading: true,
      error: undefined
    }
  },
  computed: {
    ...mapGetters(['userName'])
  },
  beforeCreate () {
    document.title = 'AWS Tools'
    this.$store.dispatch('getUser')
      .then(() => {
        // this.$router.push({ name: 'InstanceView' })
      })
      .catch((error) => {
        let details2 = ''
        if (error.response) {
          details2 = error.response.data
        }
        this.error = new Error(
          'Failed to check authentication',
          error.message,
          details2
        )
      })
      .finally(() => { this.loading = false })
  }
}
</script>
