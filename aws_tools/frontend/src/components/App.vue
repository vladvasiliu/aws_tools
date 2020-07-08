<template>
  <div id="app">
    <div class="main-content">
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
    <footer class="footer bg-light text-secondary text-center">
      <b-container>
        <b-row>
          <b-col>
            AWS Tools <small>v0.1.0</small>
          </b-col>
        </b-row>
      </b-container>
    </footer>
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

<style>
  div.main-content {
    min-height: 100vh;
    overflow: auto;
    padding-bottom: 3em;
  }
  footer {
    bottom: 0;
    height: 3em;
    margin-top: -3em;
    padding-top: 0.5em;
  }
</style>
