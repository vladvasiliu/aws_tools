<template>
  <b-navbar
    type="dark"
    variant="dark"
  >
    <div class="container">
      <b-navbar-brand to="/">
        AWS Tools
      </b-navbar-brand>
      <b-navbar-nav>
        <b-nav-item
          :to="{ name: 'InstanceView' }"
          active-class="active"
        >
          <font-awesome-icon :icon="serverIcon" /> Instances
        </b-nav-item>
        <b-nav-item
          :to="{ name: 'SecurityGroupView' }"
          active-class="active"
        >
          <font-awesome-icon :icon="securityIcon" /> Security groups
        </b-nav-item>
      </b-navbar-nav>
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
import { faUserSlash, faShieldAlt, faServer } from '@fortawesome/free-solid-svg-icons'

library.add(faUser, faUserSlash, faServer, faShieldAlt)

export default {
  name: 'NavBar',

  computed: {
    ...mapGetters(['userName']),
    userIcon () {
      return faUser
    },
    serverIcon () {
      return faServer
    },
    securityIcon () {
      return faShieldAlt
    }
  },

  mounted () {
    this.$store.dispatch('getUser')
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
