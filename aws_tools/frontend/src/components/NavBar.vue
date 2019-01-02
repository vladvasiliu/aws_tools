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
        <b-nav-item-dropdown right>
          <span slot="button-content"><font-awesome-icon :icon="userIcon" /> {{ userName }}</span>
          <b-dropdown-item @click="logout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import { mapGetters } from 'vuex'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUser } from '@fortawesome/free-regular-svg-icons'
import { faUserSlash } from '@fortawesome/free-solid-svg-icons'

library.add(faUser, faUserSlash)

export default {
  name: 'NavBar',

  computed: {
    ...mapGetters(['userName', 'isAuthenticated']),
    userIcon: function () {
      return this.isAuthenticated ? faUser : faUserSlash
    }
  },

  mounted () {
    this.$store.dispatch('getUser')
      .then()
      .catch((reason) => {
        console.log('logging for getUser')
        console.log(reason)
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
