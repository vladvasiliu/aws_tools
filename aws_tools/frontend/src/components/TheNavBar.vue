<template>
  <b-navbar
    type="dark"
    variant="dark"
  >
    <div class="container">
      <b-navbar-brand to="/">
        AWS Tools
      </b-navbar-brand>
      <b-navbar-nav v-if="oidcUser !== null">
        <b-nav-item
          :to="{ name: 'InstanceView' }"
          active-class="active"
        >
          <font-awesome-icon :icon="serverIcon" /> EC2
        </b-nav-item>
        <b-nav-item
          :to="{ name: 'RDSView' }"
          active-class="active"
        >
          <font-awesome-icon :icon="dbIcon" /> RDS
        </b-nav-item>
        <!--        <b-nav-item-->
        <!--          :to="{ name: 'SecurityGroupView' }"-->
        <!--          active-class="active"-->
        <!--        >-->
        <!--          <font-awesome-icon :icon="securityIcon" /> Security-->
        <!--        </b-nav-item>-->
        <b-nav-item
          :to="{ name: 'ScheduleView' }"
          active-class="active"
        >
          <font-awesome-icon :icon="scheduleIcon" /> Schedules
        </b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav
        v-if="oidcUser !== null"
        class="ml-auto"
      >
        <b-nav-item-dropdown right>
          <span
            slot="button-content"
          >
            <font-awesome-icon :icon="userIcon" /> {{ oidcUser.name }}
          </span>
          <b-dropdown-item @click="signOutOidc">
            Logout
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </div>
  </b-navbar>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUser, faCalendarAlt } from '@fortawesome/free-regular-svg-icons'
import { faUserSlash, faShieldAlt, faServer, faDatabase } from '@fortawesome/free-solid-svg-icons'

library.add(faUser, faUserSlash, faServer, faShieldAlt, faCalendarAlt, faDatabase)

export default {
  name: 'NavBar',

  computed: {
    ...mapGetters(['oidcUser']),
    dbIcon () { return faDatabase },
    userIcon () { return faUser },
    serverIcon () { return faServer },
    securityIcon () { return faShieldAlt },
    scheduleIcon () { return faCalendarAlt }
  },

  methods: {
    ...mapActions(['signOutOidc'])
  }
}
</script>

<style scoped></style>
