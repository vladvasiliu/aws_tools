<template>
  <b-navbar
    type="dark"
    variant="dark"
    toggleable>
    <b-navbar-brand>AWS Tools</b-navbar-brand>
    <b-collapse
      id="nav_dropdown_collapse"
      is-nav>
      <b-navbar-nav class="ml-auto">
        <!-- Navbar dropdowns -->
        <b-nav-item-dropdown
          :text="userName"
          right>
          <b-dropdown-item @click="logout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'NavBar',

  computed: { ...mapGetters(['userName']) },

  mounted () {
    this.$store.dispatch('getUser')
      .then()
      .catch((reason) => {
      })
  },

  methods: {
    logout () {
      this.$store.dispatch('logout', {})
        .then(() => {
          location.reload()
        })
    }
  }
}
</script>

<style scoped>

</style>
