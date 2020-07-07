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
// import { Error } from './ErrorView'
import Loading from './loading'

export default {
  components: {
    Loading,
    ErrorView: () => import('./ErrorView'),
    NavBar: () => import('./TheNavBar')
  },
  data: function () {
    return {
      loading: false,
      error: undefined
    }
  },
  computed: {
  },
  beforeCreate () {
    document.title = 'AWS Tools'
  }
}
</script>
