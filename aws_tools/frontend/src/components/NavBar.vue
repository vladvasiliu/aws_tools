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
import { faUser } from '@fortawesome/free-solid-svg-icons'

library.add(faUser)

export default {
  name: 'NavBar',

  data () {
    return {
      userIcon: faUser
    }
  },

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
