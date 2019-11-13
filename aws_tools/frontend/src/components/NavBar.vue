<template>
  <b-navbar
    type="dark"
    variant="dark"
  >
    <div class="container">
      <b-navbar-brand>AWS Tools</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <span
            slot="button-content"
          >
            <font-awesome-icon :icon="userIcon" /> {{ userName }}
          </span>
          <b-dropdown-item @click="logout">
            Logout
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </div>
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
    ...mapGetters(['userName']),
    userIcon () {
      return faUser
    }
  },

  methods: {
    logout () {
      this.$store.dispatch('logout', {}).then(() => {
        location.reload()
      })
    }
  }
}
</script>

<style scoped></style>
